def patch_rules(s):
 if '// Build436 blocked shared chat changes' in s:return s
 helper="""
    // Build436 blocked shared chat changes
    function pairOpen(a, b) {
      return !(b in get(/databases/$(database)/documents/users/$(a)).data.get('blocked', []))
        && !(a in get(/databases/$(database)/documents/users/$(b)).data.get('blocked', []));
    }
    function chatPairOpen(chatId) {
      let c = get(/databases/$(database)/documents/chats/$(chatId)).data;
      return c.get('isGroup', false) == true
        || (c.members.size() == 2 && pairOpen(c.members[0], c.members[1]));
    }
"""
 s=s.replace('    function onlyChanges(fields) {',helper+'    function onlyChanges(fields) {',1)
 anchor="            resource.data.get('isGroup', false) != true\n            && request.resource.data.members == resource.data.members"
 assert anchor in s
 s=s.replace(anchor,anchor+"\n            && (chatPairOpen(chatId) || onlyChanges(['hiddenFor', 'readReceipts_' + request.auth.uid, 'typingIndicator_' + request.auth.uid, 'typing_' + request.auth.uid]))",1)
 # Apply the private block guard to every update branch, including metadata-only edits.
 a=s.index('    match /chats/{chatId}')
 b=s.index('      match /messages/{messageId} {',a)
 block=s[a:b]
 anchor='      allow update: if ('
 assert anchor in block
 block=block.replace(anchor,"      allow update: if (resource.data.get('isGroup', false) == true || chatPairOpen(chatId) || onlyChanges(['hiddenFor', 'readReceipts_' + request.auth.uid, 'typingIndicator_' + request.auth.uid, 'typing_' + request.auth.uid])) && (",1)
 s=s[:a]+block+s[b:]
 a=s.index('      match /messages/{messageId} {',s.index('    match /chats/{chatId}'))
 b=s.index('      match /joinRequests/',a)
 block=s[a:b]
 anchor="        allow create: if signedIn()"
 assert anchor in block
 block=block.replace(anchor,anchor+'\n          && chatPairOpen(chatId)',1)
 s=s[:a]+block+s[b:]
 # Enforce block state for fresh or reopened social requests on the server too.
 anchor="        && fromUid != toUid"
 assert anchor in s;s=s.replace(anchor,anchor+'\n        && pairOpen(fromUid, toUid)',1)
 anchor="            && request.resource.data.get('status', '') in ['pending', 'cancelled']"
 assert anchor in s;s=s.replace(anchor,anchor+"\n            && (request.resource.data.get('status', '') == 'cancelled' || pairOpen(fromUid, toUid))",1)
 anchor="            && request.resource.data.get('status', '') in ['accepted', 'rejected']"
 assert anchor in s
 s=s.replace(anchor,"            && request.resource.data.get('status', '') in ['accepted', 'rejected', 'cancelled']\n            && (request.resource.data.get('status', '') != 'accepted' || pairOpen(fromUid, toUid))\n            && (request.resource.data.get('status', '') != 'cancelled' || !pairOpen(fromUid, toUid))",1)
 return s
