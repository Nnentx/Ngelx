#!/usr/bin/env python3
"""Extends the read-only audited live community policy in an ephemeral emulator only."""
from pathlib import Path
import re
TAG='// Build543 community deletion lifecycle guard'
def transform(s):
 if TAG in s:return s
 a=s.index('    // Build450 communities');b=s.index('    match /users/{uid}',a)
 block=s[a:b]
 # Begin deletion is server-only. Do not let clients recreate an ID mid-purge.
 assert block.count('allow create: if communitySigned450() && communityValid450(request.resource.data)')==1
 block=block.replace('allow create: if communitySigned450() && communityValid450(request.resource.data)',"allow create: if communitySigned450() && !exists(/databases/$(database)/documents/community_deletions543/$(cid)) && communityValid450(request.resource.data)",1)
 start=block.index('    match /communities450/{cid} {');end=block.index('      match /requests/',start)
 root=block[start:end]
 root=root.replace('allow update: if communitySigned450()',"allow update: if communitySigned450() && resource.data.get('deletion543',{}).get('state','') != 'deleting'")
 # Additive root settings compatibility: no roles, member lists, timestamps or
 # identity changes. Legacy admin lists need not be silently promoted/repaired.
 insert="""
      // Build543 community deletion lifecycle guard.
      allow update: if communitySigned450()
        && resource.data.get('deletion543',{}).get('state','') != 'deleting'
        && request.auth.uid in resource.data.get('members',[])
        && (request.auth.uid == resource.data.get('founderId','') || request.auth.uid in resource.data.get('admins',[]))
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['name','description','rules','visibility','joinApproval','postApproval','paused','photoUrl','coverUrl','coverAlignment'])
        && request.resource.data.get('name','') is string && request.resource.data.get('name','').size() >= 3 && request.resource.data.get('name','').size() <= 60
        && request.resource.data.get('description','') is string && request.resource.data.get('description','').size() <= 240
        && request.resource.data.get('rules','') is string && request.resource.data.get('rules','').size() <= 2000
        && request.resource.data.get('visibility','public') in ['public','private']
        && request.resource.data.get('joinApproval',false) is bool && request.resource.data.get('postApproval',false) is bool && request.resource.data.get('paused',false) is bool
        && request.resource.data.get('photoUrl','') is string && request.resource.data.get('photoUrl','').size() <= 2048
        && request.resource.data.get('coverUrl','') is string && request.resource.data.get('coverUrl','').size() <= 2048
        && request.resource.data.get('coverAlignment',0) is number && request.resource.data.get('coverAlignment',0) >= -1 && request.resource.data.get('coverAlignment',0) <= 1;
"""
 root=root.replace('    match /communities450/{cid} {','    match /communities450/{cid} {'+insert,1)
 block=block[:start]+root+block[end:]
 # Every root update branch (including older OR-authorized branches) must be
 # frozen while a server deletion job owns the root. Nested writes use these
 # shared role helpers; author-owned comment deletion remains independently safe.
 for name in ['communityMember450','communityAdmin450','communityModerator456']:
  p=block.index('function '+name+'(cid)');q=block.index('return communitySigned450()',p)+len('return communitySigned450()')
  block=block[:q]+" && community450(cid).get('deletion543',{}).get('state','') != 'deleting' && request.auth.uid in community450(cid).get('members',[])"+block[q:]
 # Older cover-only clauses are additive too; freeze their root update guards.
 root_start=block.index('    match /communities450/{cid} {');root_end=block.index('      match /requests/',root_start)
 part=block[root_start:root_end]
 part=part.replace('allow update: if signedIn()',"allow update: if signedIn() && resource.data.get('deletion543',{}).get('state','') != 'deleting'")
 block=block[:root_start]+part+block[root_end:]
 # Freeze every nested write, including join requests and author-only deletes.
 nested_start=block.index('      match /requests/')
 nested_end=block.index('    match /communityInvites450/{code}',nested_start)
 head,tail,after=block[:nested_start],block[nested_start:nested_end],block[nested_end:]
 tail=re.sub(r'allow ((?:create|update|delete|write)(?:,\s*(?:create|update|delete|write))*): if ',r'allow \1: if communityWritable543(cid) && ',tail)
 block="    function communityWritable543(cid) { return !exists(/databases/$(database)/documents/community_deletions543/$(cid)); }\n"+head+tail+after
 out=s[:a]+block+s[b:]
 assert out[:a]==s[:a] and out.split('    match /users/{uid}',1)[1]==s.split('    match /users/{uid}',1)[1]
 return out
if __name__=='__main__':
 p=Path('firestore.rules');s=p.read_text();out=transform(s);assert transform(out)==out;p.write_text(out)
 print('Build543 community candidate prepared for emulator only; no release API writes')
