#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
def section(a,b):
 start=s.index(a)
 end=s.index(b,start+len(a))
 return s[start:end]
own=section('class _ProfilPageState extends State<ProfilPage>','\nclass _ProfilEtkilesimRozeti')
visitor=section('class _KullaniciProfilPageState extends State<KullaniciProfilPage>','\nclass NgelXVideoKapakOnizleme')
story=section('class _HikayeGosterPageState extends State<HikayeGosterPage>','\nclass HesapDegistirPage')
test={
 'owner no-cover compact 152x194':"SizedBox(height:152,width:194" in own,
 'owner no-cover image stays centered':"kullanici:kullanici,radius:59,etkin:false" in own,
 'owner avatar actions unchanged':"onTap:hikayeyiAc,onLongPress:fotografYukle" in own,
 'owner cover layout 265 unchanged':"height:265" in own,
 'visitor coverless compact 156x205':"SizedBox(height:156,width:205" in visitor,
 'visitor covered image stays original':"Positioned(left:0,right:0,top:0,height:172" in visitor,
 'visitor actions unchanged':"takipDurumuDegistir(uid" in visitor and
    "sosyalIstekGonder(hedefUid:uid,tur:'friend_request'" in visitor,
 'join date agrees in covered and coverless':visitor.count('Text(katilim,')==2,
 'join date no year-only variant':"NgelX’e katıldı: '+katilimHam.toDate().year" not in visitor,
 'join grammar unchanged correct':"tarihinde katıldı" in own and "tarihinde katıldı" in visitor,
 'story true createdAt timestamp':"final ham=widget.createdAt;" in story and
     "if(ham is! Timestamp)return 'Paylaşım zamanı henüz bilinmiyor'" in story,
 'story true expiresAt timestamp':"final ham=widget.expiresAt;" in story and
     "if(ham is! Timestamp)return 'Bitiş zamanı henüz bilinmiyor'" in story,
 'story shows actual start and end':"Paylaşıldı:" in story and
     "Biter:" in story and "Bitti:" in story,
 'story has remaining time and refresh':"dk kaldı" in story and
     "animation:sure" in story,
 'story viewer closes same way':'sure=AnimationController' in story and
     'Navigator.pop(context)' in story,
 'story reply still intact':"'type':'story_reply'" in story and
     'uygulamaBildirimiGonder(' in story,
 'story media player untouched':"VideoPlayerController.networkUrl(Uri.parse(widget.url))" in story,
 'global account search retained':"chip('people','Kişiler'" in s,
 'recent follow and cancel guards retained':"Takip durumu alınamadı." in visitor and
     "İstek artık beklemede değil veya iptal edilemedi." in s,
 'Firestore unchanged':Path('firestore.rules').is_file(),
}
for name,ok in test.items():print(('PASS ' if ok else 'FAIL ')+name,flush=True)
if not all(test.values()):raise SystemExit('Build421 last three regression guards FAILED')
print('Build421 three remaining source regression guards PASSED. Device QA pending.')
