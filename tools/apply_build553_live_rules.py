from pathlib import Path
import sys
TAG='// Build553 live moderator and timed comment permissions'
def transform(s):
 if TAG in s:return s
 start=s.index('    match /live_streams/{streamId} {')
 a=s.index('      match /comments/{commentId} {',start);b=s.index('      match /reactions/{uid} {',a)
 declaration='''      // Build553 live moderator and timed comment permissions
      function live553() { return get(/databases/$(database)/documents/live_streams/$(streamId)).data; }
      function host553() { return signedIn() && request.auth.uid == live553().ownerId; }
      function mod553() { return signedIn() && request.auth.uid in live553().get('moderatorUids553', []); }
      function timed553(v, uid) {
        let until = v.get('commentMuteUntil553', {}).get(uid, null);
        return until == null || (until is timestamp && request.time >= until);
      }
      function canComment553() {
        let v = live553();
        return signedIn() && v.get('active', false) == true
          && !(request.auth.uid in v.get('bannedUsers', []))
          && !(request.auth.uid in v.get('mutedUsers', []))
          && timed553(v, request.auth.uid)
          && (v.get('commentsEnabled', true) == true || host553());
      }
      function safeModeratorUpdate553() {
        let old = resource.data;
        let next = request.resource.data;
        let affected = next.diff(old).affectedKeys();
        let before = old.get('bannedUsers', []).toSet();
        let after = next.get('bannedUsers', []).toSet();
        let added = after.difference(before);
        return mod553() && old.get('active', false) == true
          && affected.hasOnly(['bannedUsers'])
          && next.bannedUsers is list && next.bannedUsers.size() <= 1000
          && before.difference(after).size() == 0 && added.size() == 1
          && !added.hasAny([old.ownerId, request.auth.uid])
          && added.intersection(old.get('moderatorUids553', []).toSet()).size() == 0;
      }
      allow update: if safeModeratorUpdate553();
      match /comments/{commentId} {
        function validGift553() {
          let g=request.resource.data;
          let qty=g.get('quantity',0);
          let points=g.get('points',-1);
          let name=g.get('giftName','');
          return g.keys().hasOnly(['uid','userId','username','text','kind','giftName','giftEmoji','quantity','points','createdAt'])
            && g.get('uid','') == request.auth.uid && g.get('userId','') == request.auth.uid
            && g.get('createdAt',null) == request.time
            && qty is int && qty >= 1 && qty <= 10 && points is int
            && ((name == 'Gül' && points == qty) || (name == 'Kalp' && points == qty*3)
              || (name == 'Yıldız' && points == qty*5) || (name in ['Elmas','Kalp Taşı'] && points == qty*15)
              || (name in ['Ayıcık','Taç'] && points == qty*25) || (name == 'NgelX Roket' && points == qty*50)
              || (name == 'Galaksi' && points == qty*100) || (name == 'Aslan' && points == qty*150)
              || (name == 'Evren' && points == qty*200));
        }
        allow read: if true;
        allow create: if signedIn() && request.resource.data.get('userId','') == request.auth.uid
          && (request.resource.data.get('kind','comment') == 'gift'
            ? (live553().get('active',false) == true && !(request.auth.uid in live553().get('bannedUsers',[])) && validGift553())
            : canComment553());
        allow update: if signedIn() && resource.data.get('kind','') != 'gift'
          && request.resource.data.get('kind','') != 'gift' && resource.data.get('userId','') == request.auth.uid
          && request.resource.data.get('userId','') == request.auth.uid && canComment553();
        allow delete: if signedIn() && resource.data.get('kind','') != 'gift'
          && (resource.data.get('userId','') == request.auth.uid || host553() || mod553());
      }
'''
 return s[:a]+declaration+s[b:]
if __name__=='__main__':
 p=Path(sys.argv[1]);p.write_text(transform(p.read_text()))
