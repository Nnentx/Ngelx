"""Only extend the existing community comment rule block; preserve all others."""
from pathlib import Path

def transform(source):
    metrics = ''
    for collection in ('views', 'shares'):
        metrics += '''        match /COLLECTION/{uid} {
          allow read: if communityVisible450(cid) && get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.status == 'approved';
          allow create, update: if communitySigned450() && communityVisible450(cid) && uid == request.auth.uid
            && get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.status == 'approved'
            && request.resource.data.keys().hasOnly(['uid','createdAt'])
            && request.resource.data.uid == uid && request.resource.data.createdAt == request.time;
          allow delete: if false;
        }
'''.replace('COLLECTION', collection)
    if 'reactionVisible455' in source:
        community = source[source.index('match /communities450/'):source.index('match /communityInvites450/')]
        if metrics.strip() in community: return source
        if 'match /views/' in community or 'match /shares/' in community:
            raise RuntimeError('Different community metric rules already present')
        return source.replace('        match /comments/{commentId} {', metrics+'        match /comments/{commentId} {',1)
    like_start = source.index('        match /likes/{uid} {', source.index('match /communities450/'))
    like_end = source.index('        match /comments/{commentId}', like_start)
    likes = source[like_start:like_end]
    likes = likes.replace("keys().hasOnly(['uid','createdAt'])", "keys().hasOnly(['uid','createdAt','emoji']) && request.resource.data.get('emoji','❤️') in ['❤️','👍','😂','😮','😢','😡']")
    likes = likes.replace('allow create:', 'allow create, update:').replace('          allow update: if false;\n', '')
    source = source[:like_start]+likes+source[like_end:]
    source = source.replace('        match /comments/{commentId} {', metrics+'        match /comments/{commentId} {',1)
    old = "request.resource.data.keys().hasOnly(['uid','name','text','createdAt'])"
    new = """request.resource.data.keys().hasOnly(['uid','name','text','createdAt','photoUrl','replyTo','replyName'])
            && request.resource.data.get('photoUrl','') is string && request.resource.data.get('photoUrl','').size() <= 2048
            && request.resource.data.get('replyName','') is string && request.resource.data.get('replyName','').size() <= 100
            && request.resource.data.get('replyTo','') is string
            && (request.resource.data.get('replyTo','') == '' ||
              exists(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)/comments/$(request.resource.data.replyTo)))"""
    if source.count(old) != 1: raise RuntimeError('Unexpected community comment schema')
    source = source.replace(old, new)
    start = source.index('        match /comments/{commentId} {')
    end = source.index('          allow update: if false;', start) + len('          allow update: if false;')
    rules = """
          match /reactions/{uid} {
            function reactionVisible455() { return communityVisible450(cid)
              && get(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)).data.status == 'approved'
              && exists(/databases/$(database)/documents/communities450/$(cid)/posts/$(pid)/comments/$(commentId)); }
            function validReaction455() { return request.resource.data.keys().hasOnly(['uid','emoji','createdAt'])
              && request.resource.data.uid == request.auth.uid
              && request.resource.data.emoji in ['❤️','👍','😂','😮','😢','😡']
              && request.resource.data.createdAt == request.time; }
            allow read: if reactionVisible455();
            allow create, update: if communityMember450(cid) && uid == request.auth.uid && reactionVisible455() && validReaction455();
            allow delete: if communityMember450(cid) && uid == request.auth.uid;
          }
"""
    return source[:end] + rules + source[end:]

if __name__ == '__main__':
    path = Path('firestore.rules')
    path.write_text(transform(path.read_text()))
    print('Build455 bounded community comment/reaction rules applied')
