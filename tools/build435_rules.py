FIELDS=['mediaUrl','videoUrl','audioUrl','fileUrl','thumbnailUrl','posterUrl','coverUrl','imageUrl']
def patch_rules(text):
 if '// Build435 message deletion safety' in text:return text
 a=text.index('      match /messages/{messageId} {',text.index('    match /chats/{chatId}'))
 b=text.index('      match /joinRequests/',a)
 block=text[a:b]
 old="                'reactions', 'pinned', 'pinnedAt', 'pinnedBy'"
 assert block.count(old)==1
 block=block.replace(old,old+",\n                'cleanupMediaUrls', 'mediaCleanupState', 'thumbnailUrl', 'posterUrl', 'coverUrl', 'imageUrl'")
 anchor="              && request.resource.data.get('deletedForEveryone', false) == true"
 expected='['+', '.join("resource.data.get('%s', '')"%f for f in FIELDS)+']'
 guard="""              // Build435 message deletion safety
              && (!request.resource.data.diff(resource.data).affectedKeys().hasAny(['cleanupMediaUrls', 'mediaCleanupState']) || (
                resource.data.get('deletedForEveryone', false) != true
                && request.resource.data.get('mediaCleanupState', '') == 'pending'
                && request.resource.data.get('cleanupMediaUrls', []) == EXPECTED
              ))
""".replace('EXPECTED',expected)
 assert block.count(anchor)==1;block=block.replace(anchor,guard+anchor)
 anchor="            || onlyChanges(['reactions'])"
 assert block.count(anchor)==1
 block=block.replace(anchor,"""            || (
              onlyChanges(['hiddenFor'])
              && request.resource.data.get('hiddenFor', []).hasAll(resource.data.get('hiddenFor', []))
              && request.resource.data.get('hiddenFor', []).removeAll(resource.data.get('hiddenFor', [])).hasOnly([request.auth.uid])
              && request.auth.uid in request.resource.data.get('hiddenFor', [])
            )
"""+anchor)
 return text[:a]+block+text[b:]
