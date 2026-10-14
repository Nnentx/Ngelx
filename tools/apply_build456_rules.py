"""Add bounded community roles and moderation without touching existing chat/auth rules."""
from pathlib import Path

def transform(source):
 if '// Build456 community moderation' in source:return source
 a=source.index('    // Build450 communities');b=source.index('    match /users/',a)
 block=source[a:b]
 block=block.replace("    function communityVisible450(cid)",'''    // Build456 community moderation
    function communityModerator456(cid) { return communitySigned450() &&
      (request.auth.uid in community450(cid).admins || request.auth.uid in community450(cid).get('moderators',[])); }
    function communityPosting456(cid) { return communityMember450(cid)
      && community450(cid).get('paused',false) == false
      && !(request.auth.uid in community450(cid).get('muted',[])); }
    function communityVisible450(cid)''')
 block=block.replace("'lastJoinCode','createdAt'])","'lastJoinCode','createdAt','coverAlignment','moderators','muted','banned','approvalMembers','paused'])",1)
 block=block.replace('&& v.name is string', '''&& v.get('moderators',[]) is list && v.get('moderators',[]).size() <= 30
        && v.get('moderators',[]).toSet().difference(v.members.toSet()).size() == 0
        && v.get('moderators',[]).toSet().intersection(v.admins.toSet()).size() == 0
        && v.get('muted',[]) is list && v.get('muted',[]).size() <= 500
        && v.get('muted',[]).toSet().difference(v.members.toSet()).size() == 0
        && v.get('muted',[]).toSet().intersection(v.admins.toSet()).size() == 0
        && v.get('banned',[]) is list && v.get('banned',[]).size() <= 500
        && v.get('banned',[]).toSet().intersection(v.members.toSet()).size() == 0
        && v.get('approvalMembers',[]) is list && v.get('approvalMembers',[]).size() <= 500
        && v.get('paused',false) is bool && v.get('coverAlignment',0) is number
        && v.get('coverAlignment',0) >= -1 && v.get('coverAlignment',0) <= 1
        && v.name is string''',1)
 # Creation cannot smuggle management settings or deny its founder.
 block=block.replace("&& request.resource.data.lastJoinCode == ''", "&& request.resource.data.get('moderators',[]) == [] && request.resource.data.get('muted',[]) == [] && request.resource.data.get('banned',[]) == [] && request.resource.data.get('approvalMembers',[]) == []\n        && request.resource.data.lastJoinCode == ''",1)
 # Admins must preserve other admins; only founder may add/remove admins. Existing founder invariant remains.
 block=block.replace("resource.data.joinApproval == false && !(request.auth.uid in resource.data.members)","resource.data.joinApproval == false && !(request.auth.uid in resource.data.members) && !(request.auth.uid in resource.data.get('banned',[]))")
 block=block.replace("hasOnly(['members','admins'])", "hasOnly(['members','admins','moderators'])")
 block=block.replace("&& request.resource.data.admins.toSet() == resource.data.admins.toSet().difference([request.auth.uid].toSet()))","&& request.resource.data.admins.toSet() == resource.data.admins.toSet().difference([request.auth.uid].toSet())\n            && request.resource.data.get('moderators',[]).toSet() == resource.data.get('moderators',[]).toSet().difference([request.auth.uid].toSet()))")
 block=block.replace("&& request.resource.data.status == 'pending' && request.resource.data.createdAt == request.time","&& !(uid in community450(cid).get('banned',[])) && request.resource.data.status == 'pending' && request.resource.data.createdAt == request.time",1)
 block=block.replace("'pinned','createdAt'])","'pinned','createdAt','publishAt'])",1)
 block=block.replace('allow create: if communityMember450(cid) && validPost450()', 'allow create: if communityPosting456(cid) && validPost450()')
 block=block.replace("&& request.resource.data.status == (community450(cid).postApproval == true && !communityAdmin450(cid) ? 'pending' : 'approved');", "&& (request.resource.data.status == ((community450(cid).postApproval == true || request.auth.uid in community450(cid).get('approvalMembers',[])) && !communityAdmin450(cid) ? 'pending' : 'approved')\n          || (communityAdmin450(cid) && request.resource.data.status == 'scheduled' && request.resource.data.publishAt is timestamp && request.resource.data.publishAt > request.time));")
 block=block.replace("(communityAdmin450(cid) && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['status','pinned'])", "(communityModerator456(cid) && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['status','pinned','commentsClosed','slowSeconds'])")
 block=block.replace("&& request.resource.data.status in ['approved','rejected','deleted'] && request.resource.data.pinned is bool)","&& request.resource.data.status in ['approved','rejected','deleted'] && request.resource.data.pinned is bool\n          && request.resource.data.get('commentsClosed',false) is bool && request.resource.data.get('slowSeconds',0) in [0,300])")
 # Comments enforce pause/mute/closed/cooldown on server; reaction collection reads are bounded by parent visibility.
 block=block.replace('allow create: if communityMember450(cid)\n            && get', 'allow create: if communityPosting456(cid)\n            && get')
 block=block.replace("&& request.resource.data.keys().hasOnly(['uid','name','text'", "&& get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.get('commentsClosed',false) == false\n            && (get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.get('slowSeconds',0) == 0 ||\n              (getAfter(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)/commentLimits456/$(request.auth.uid)).data.at == request.time\n              && getAfter(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)/commentLimits456/$(request.auth.uid)).data.commentId == commentId))\n            && request.resource.data.keys().hasOnly(['uid','name','text'")
 block=block.replace('resource.data.uid == request.auth.uid || communityAdmin450(cid)','resource.data.uid == request.auth.uid || communityModerator456(cid)')
 block=block.replace("allow read: if reactionVisible455();", "allow read: if communityVisible450(cid) && get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.status == 'approved';")
 marker='        match /likes/{uid} {'
 extras='''        match /commentLimits456/{uid} {
          allow get: if communityMember450(cid) && uid == request.auth.uid;
          allow create, update: if communityPosting456(cid) && uid == request.auth.uid
            && request.resource.data.keys().hasOnly(['uid','commentId','at'])
            && request.resource.data.uid == uid && request.resource.data.commentId is string && request.resource.data.at == request.time
            && (!exists(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)/commentLimits456/$(uid)) ||
              resource.data.at + duration.value(get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.get('slowSeconds',0),'s') <= request.time);
        }
        match /feedback456/{id} {
          allow read: if communityModerator456(cid) || request.auth.uid == get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.authorId;
          allow create: if communityModerator456(cid) && request.resource.data.keys().hasOnly(['uid','text','createdAt'])
            && request.resource.data.uid == request.auth.uid && request.resource.data.text is string && request.resource.data.text.size() <= 500 && request.resource.data.createdAt == request.time;
        }
'''
 block=block.replace(marker,extras+marker,1)
 block=block.replace("allow read: if communityAdmin450(cid);\n        allow create: if communityMember450(cid)","allow read: if communityModerator456(cid);\n        allow create: if communityMember450(cid)")
 block=block.replace("allow update: if communityAdmin450(cid) && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['status']) && request.resource.data.status == 'closed';", "allow update: if communityModerator456(cid) && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['status']) && request.resource.data.status == 'closed';")
 block=block.replace("      match /reports/{reportId} {",'''      match /audit456/{id} {
        allow read: if communityModerator456(cid);
        allow create: if communityModerator456(cid) && request.resource.data.keys().hasOnly(['actor','target','action','createdAt'])
          && request.resource.data.actor == request.auth.uid && request.resource.data.target is string
          && request.resource.data.action in ['admin','moderator','mute','remove','ban','delete'] && request.resource.data.createdAt == request.time;
      }
      match /reports/{reportId} {''')
 source=source[:a]+block+source[b:]
 source=source.replace('      match /saved/{contentId}', "      match /communityPreferences456/{id} { allow read, write: if isMe(uid); }\n      match /saved/{contentId}",1)
 return source
if __name__=='__main__':
 p=Path('firestore.rules');p.write_text(transform(p.read_text()));print('Build456 community role, pause, moderation and cooldown rules applied')
