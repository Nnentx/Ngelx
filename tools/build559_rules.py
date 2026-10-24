"""Keep existing profile/relationship rules; identity fields are server-owned."""
def patch_rules(text):
 if '// Build559 server-owned profile identity' in text:return text
 old='''      allow create, delete: if isMe(uid);
      allow update: if isMe(uid) || relationshipUpdate();'''
 new='''      // Build559 server-owned profile identity
      // Account deletion uses the existing server deletion workflow. A client
      // cannot erase/recreate its profile to reset the identity cooldown.
      allow create: if isMe(uid)
        && !request.resource.data.keys().hasAny(['displayNameChangedAt559', 'usernameChangedAt559']);
      allow delete: if false;
      allow update: if (isMe(uid) && !request.resource.data.diff(resource.data).affectedKeys().hasAny([
        'displayName', 'name', 'fullName', 'username', 'usernameLower', 'displayNameChangedAt559', 'usernameChangedAt559'
      ])) || relationshipUpdate();'''
 assert text.count(old)==1,'Unexpected profile rules baseline'
 text=text.replace(old,new)
 marker='    match /users/{uid} {'
 assert text.count(marker)==1
 text=text.replace(marker,'''    // Username ownership/retirement is private and maintained atomically by Admin SDK.
    match /login_usernames/{name} { allow read, write: if false; }
'''+marker)
 return text
