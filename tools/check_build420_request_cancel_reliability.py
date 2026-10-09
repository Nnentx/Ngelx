#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('Future<void> sosyalIstekIptalEt(')
b=s.index('\nbool gidenSosyalIstekBekliyor(',a)
cancel=s[a:b]
a=s.index('Future<bool> sosyalIstekGonder({')
b=s.index('\nFuture<void> sosyalIstekIptalEt(',a)
send=s[a:b]
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
visitor=s[a:b]
checks={
  'missing request doc returns visible error':"throw StateError('Geri çekilecek istek bulunamadı.')" in cancel,
  'missing notification returns visible error':"throw StateError('Geri çekilecek istek bildirimi bulunamadı.')" in cancel,
  'source request read is not silently ignored':"if(istekRef!=null){\n    // The outgoing request is the source of truth." in cancel,
  'requires actual write':"if(!degisiklik){" in cancel and
    "await batch.commit().timeout(const Duration(seconds:10))" in cancel,
  'request cancel status and timestamp preserved':"'status':'cancelled'" in cancel and
    "'cancelledAt':FieldValue.serverTimestamp()" in cancel,
  'notification companion still cancels':"'read':true" in cancel and
    "batch.update(bildirimRef," in cancel,
  'original request creation remains atomic':"batch.set(istekRef," in send
    and "batch.set(bildirimRef," in send and "await batch.commit()" in send,
  'follow relationship kept':"takipDurumuDegistir(uid" in visitor,
  'friend request callbacks kept':"sosyalIstekGonder(hedefUid:uid,tur:'friend_request'" in visitor,
  'visitor follow and friend cancellation still use helper':visitor.count('await sosyalIstekIptalEt(pendingSnap.reference)')==2,
  'follow notification separation kept':"if(!takipte){\n    unawaited(uygulamaBildirimiGonder(" in s,
  'pending request UI guards kept':visitor.count('if(me!=null&&!istekSnap.hasData)')>=2,
  'past profile choices and people search kept':"if(kapaksiz)...[" in visitor and
    "chip('people','Kişiler'" in s,
  'no server rules edits':Path('firestore.rules').is_file(),
}
for label,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+label,flush=True)
if not all(checks.values()):raise SystemExit('Build420 request cancellation regressions FAILED')
print('Build420 cancellation guards PASSED. Real-device testing still needed.')
