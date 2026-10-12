from pathlib import Path
r=Path('.')
guest='''
      match /guest_requests/{uid} {
        function live() { return get(/databases/$(database)/documents/live_streams/$(streamId)).data; }
        function host() { return signedIn() && request.auth.uid == live().ownerId; }
        function validGuest() {
          return signedIn() && live().active == true && uid != live().ownerId
            && !(uid in live().get('bannedUsers', []))
            && request.resource.data.keys().hasOnly(['liveId','hostUid','guestUid','status','startedBy','updatedAt'])
            && request.resource.data.liveId == streamId && request.resource.data.hostUid == live().ownerId
            && request.resource.data.guestUid == uid;
        }
        allow get: if signedIn() && (request.auth.uid == uid || host());
        allow list: if host();
        allow create: if validGuest() && (
          (request.auth.uid == uid && request.resource.data.status == 'pending' && request.resource.data.startedBy == uid)
          || (host() && request.resource.data.status == 'invited' && request.resource.data.startedBy == request.auth.uid)
        );
        allow update: if validGuest() && (
          (resource.data.status == 'pending' && host() && request.resource.data.status == 'accepted' && request.resource.data.startedBy == resource.data.startedBy)
          || (resource.data.status == 'invited' && request.auth.uid == uid && request.resource.data.status == 'accepted' && request.resource.data.startedBy == resource.data.startedBy)
          || ((host() || request.auth.uid == uid) && request.resource.data.status == 'rejected' && request.resource.data.startedBy == resource.data.startedBy)
          || (resource.data.status in ['rejected','cancelled'] && ((request.auth.uid == uid && request.resource.data.status == 'pending' && request.resource.data.startedBy == uid) || (host() && request.resource.data.status == 'invited' && request.resource.data.startedBy == request.auth.uid)))
        );
        allow delete: if host();
      }
'''
devices='''    match /_call_devices/{uid}/tokens/{tokenId} {
      allow read, delete: if isMe(uid);
      allow create, update: if isMe(uid) && request.resource.data.uid == uid
        && request.resource.data.keys().hasOnly(['token','uid','updatedAt'])
        && request.resource.data.token is string && request.resource.data.token.size() > 20 && request.resource.data.token.size() < 4096;
    }
'''
discovery='''        allow create: if signedIn() && request.auth.uid == requestUid
          && groupDoc(chatId).data.get('isGroup',false) == true && groupDoc(chatId).data.get('discoverable',false) == true
          && request.resource.data.uid == requestUid && request.resource.data.type == 'discovery_join' && request.resource.data.status == 'pending'
          && request.resource.data.keys().hasOnly(['uid','type','targetName','targetPhoto','status','createdAt','updatedAt']);
        allow update: if signedIn() && request.auth.uid == requestUid && resource.data.uid == requestUid
          && resource.data.get('status','') in ['rejected','cancelled','autojoin']
          && groupDoc(chatId).data.get('discoverable',false) == true
          && request.resource.data.uid == requestUid && request.resource.data.type == 'discovery_join' && request.resource.data.status == 'pending'
          && request.resource.data.keys().hasOnly(['uid','type','targetName','targetPhoto','status','createdAt','updatedAt']);
'''
def patch(s):
 a=s.index('    function validPublicSelfJoin() {');b=s.index('\n    }',a)+6;s=s[:a]+'    function validPublicSelfJoin() { return false; }'+s[b:]
 s=s.replace('      match /joinRequests/{requestUid} {','      match /joinRequests/{requestUid} {\n'+discovery,1)
 s=s.replace('    match /live_streams/{streamId} {',devices+'    match /live_streams/{streamId} {'+guest,1)
 return s

p=Path('firestore.rules');p.write_text(patch(p.read_text()))
