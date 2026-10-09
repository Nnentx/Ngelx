#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
v=s[a:b]
a=s.index('class NgelXOnayliProfilDuzenlePage')
b=s.index('class ProfilPage extends StatefulWidget',a)
e=s[a:b]
a=s.index('class _ArkadaslarPageState extends State<ArkadaslarPage>')
b=s.index('\nclass ',a+7)
f=s[a:b]
checks={
  'original cover and coverless appearance retained':"if(kapaksiz)...[" in v and
    "NgelXAgImageProvider(profilKapak)" in v,
  'visitor action layout now two rows':"Column(children:[\n                 SizedBox(height:52" in v
    and v.count("SizedBox(height:52,child:Row(crossAxisAlignment:CrossAxisAlignment.stretch,children:[")>=2,
  'full visitor follow callback retained':"takipDurumuDegistir(uid" in v
    and "sosyalIstekGonder(hedefUid:uid,tur:'follow_request'" in v,
  'full visitor friend callback retained':"_arkadasliktanCikar(me,gorunenAd)" in v
    and "sosyalIstekGonder(hedefUid:uid,tur:'friend_request'" in v,
  'message and mutual group routing retained':"profildenMesajAc(" in v
    and "OrtakGruplarPage(digerUid:uid)" in v,
  'visitor four action text fitting preserved':"FittedBox(fit:BoxFit.scaleDown" in v,
  'crop title not clipped':"AppBar(title:const Text('Kapağı ayarla'" in s,
  'cover editor keeps known initial image':"widget.ilkKapakUrl" in e and
    "final cover=snap.hasData?" in e,
  'cover editor loading and error placeholders':"frameBuilder:(ctx,child,frame,syncLoaded)" in e
    and "errorBuilder:(ctx,error,stack)" in e,
  'cover editor actions and mode unchanged':"onPressed:_kaydediliyor?null:widget.onKapak" in e
    and "'profileViewMode':_gorunum" in e,
  'friend search title no false total':"Arkadaş · Arama sonuçları" in f
    and "ids.length.toString()+' Arkadaş'" in f,
  'search privacy preserved':"discoverableProfile" in s and "blocked" in s,
  'story reply safety kept':"batch.set(story," not in
     s[s.index('  Future<void> _yanitGonder('):s.index('\n  Widget _medya(){',s.index('  Future<void> _yanitGonder('))],
}
for key,val in checks.items():print(('PASS ' if val else 'FAIL ')+key,flush=True)
if not all(checks.values()):raise SystemExit('Build 415 contract FAILED.')
print('Build 415 action/cover regression contracts PASSED; device QA pending.')
