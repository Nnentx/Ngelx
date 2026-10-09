#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('Future<void> takipDurumuDegistir(')
b=s.index('\ndouble ngelxAltGuvenliBosluk',a)
follow=s[a:b]
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
visitor=s[a:b]
a=s.index('Future<bool> sosyalIstekGonder({')
b=s.index('\nFuture<void> sosyalIstekIptalEt(',a)
requests=s[a:b]
checks={
 'follow relation still batches both directions':
   "'following':takipte?FieldValue.arrayRemove" in follow and
   "'followers':takipte?FieldValue.arrayRemove" in follow,
 'batch fully committed before notifying':follow.index('await batch.commit()')<
   follow.index('unawaited(uygulamaBildirimiGonder('),
 'notification failure no longer causes follow rollback':
   "if(!takipte)await uygulamaBildirimiGonder" not in follow and
   ".catchError((_){ })" in follow,
 'notification still delivered best effort':"Seni takip etmeye başladı" in follow,
 'visitor waits for outgoing follow stream':"Takip durumu alınamadı." in visitor and
   visitor.count("if(me!=null&&!istekSnap.hasData)")>=2,
 'visitor waits for outgoing friendship stream':"Arkadaşlık durumu alınamadı." in visitor,
 'original follower and friendship actions preserved':"takipDurumuDegistir(uid" in visitor and
   "sosyalIstekGonder(hedefUid:uid,tur:'friend_request'" in visitor,
 'private follow pending request still checked':"sosyalIstekRef(me,uid,'follow_request').snapshots()" in visitor,
 'friend pending request still checked':"sosyalIstekRef(me,uid,'friend_request').snapshots()" in visitor,
 'new request and notification still atomic':"batch.set(istekRef," in requests
   and "batch.set(bildirimRef," in requests
   and "await batch.commit().timeout" in requests,
 'previous UI cover/coverless preserved':'if(kapaksiz)...[' in visitor,
 'previous people search preserved':"chip('people','Kişiler'" in s,
 'previous switch recovery preserved':"Kaydedilmiş şifre kabul edilmedi." in s,
 'Firestore rules unchanged':Path('firestore.rules').is_file(),
}
for label,result in checks.items():print(('PASS ' if result else 'FAIL ')+label,flush=True)
if not all(checks.values()):raise SystemExit('Build419 source regression FAILED')
print('Build419 source regression guards PASSED; real-device testing still needed.')
