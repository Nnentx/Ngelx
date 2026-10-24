"""Extend the existing sender/admin tombstone path for album metadata only."""
from build435_rules import patch_rules as deletion_rules

def patch_rules(text):
    if '// Build558 album tombstone safety' in text:
        return text
    # The modern retained rules must first agree with the existing Build435 client.
    text=deletion_rules(text)
    start=text.index('      match /messages/{messageId} {',text.index('    match /chats/{chatId}'))
    end=text.index('      match /joinRequests/',start)
    block=text[start:end]
    marker="'cleanupMediaUrls', 'mediaCleanupState', 'thumbnailUrl', 'posterUrl', 'coverUrl', 'imageUrl'"
    assert block.count(marker)==1
    block=block.replace(marker,marker+", 'albumItems558', 'mediaUrls'")
    expected="["+", ".join("resource.data.get('%s', '')"%f for f in ['mediaUrl','videoUrl','audioUrl','fileUrl','thumbnailUrl','posterUrl','coverUrl','imageUrl'])+"]"
    assert block.count('== '+expected)==1
    block=block.replace('== '+expected,'== '+expected+".concat(resource.data.get('mediaUrls', []))")
    anchor="              && request.resource.data.get('deletedForEveryone', false) == true"
    assert block.count(anchor)==1
    block=block.replace(anchor,"""              // Build558 album tombstone safety
              && (!request.resource.data.diff(resource.data).affectedKeys().hasAny(['albumItems558', 'mediaUrls']) || (
                request.resource.data.get('albumItems558', []) == []
                && request.resource.data.get('mediaUrls', []) == []
              ))
"""+anchor)
    return text[:start]+block+text[end:]
