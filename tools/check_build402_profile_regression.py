#!/usr/bin/env python3
"""Build 402 preservation and reference layout contract checks."""
from pathlib import Path
main=Path('app/lib/main.dart').read_text(encoding='utf-8')
pub=Path('app/pubspec.yaml').read_text(encoding='utf-8')
p=main[main.index('class _ProfilPageState extends State<ProfilPage>'):main.index('\nclass _ProfilEtkilesimRozeti',main.index('class _ProfilPageState extends State<ProfilPage>'))]
nav=main[main.index('bottomNavigationBar:akis&&temizAkis'):main.index('            ),\n          );',main.index('bottomNavigationBar:akis&&temizAkis'))]
checks={
  'version v1.0.178+402': "version: 1.0.178+402" in pub and "defaultValue: '402'" in main,
  'avatar/name horizontal': 'Positioned(\n                        left:145,right:4,top:206' in p and 'Text(\n                    kullanici,' in p,
  'stats separated card': "Color(0xFFF5F1FD)" in p and p.count('Container(height:44,width:1,color:const Color(0xFFE4DFF1))')==3,
  'live stats counters': all(k in p for k in ["'$canliTakip'","'$canliTakipci'","'$etkilesim'","'$canliArkadas'"]),
  'full friend button': "Text('Arkadaş Ekle',maxLines:1" in p and "FittedBox(fit:BoxFit.scaleDown" in p,
  'no truncated shortcuts': "Text(yazi,textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.visible" in p,
  'intro video action and actual player': 'ProfilTanitimVideoKarti(url:tanitimVideoUrl)' in p and 'onPressed:tanitimVideosuYukle' in p,
  'highlights real data': "(v['highlightTitle']??(video?'Video':'Öne çıkan')).toString()" in p and 'NgelXVideoKapakOnizleme(url:url)' in p,
  'highlight no demo data': "if(h.isEmpty)const Padding" in p and "where('type',isEqualTo:'story')" in p,
  'cover kind remains supported': "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in p,
  'cover crop persists': 'kapakFotografiDuzenle' in p and 'NgelXKapakKonumlandirPage' in main,
  'cover cached across frames': 'gaplessPlayback:true' in p,
  'profile bio save remains': 'Future<void> duzenle()' in p,
  'friends list retained': 'const ArkadaslarPage()' in p,
  'saved tab data retained': '_kaydedilenGrid()' in p and "collection('saved')" in p,
  'story/album grid retained': '_profilHikayeGridFinal()' in p,
  'selected nav keep callbacks': 'onDestinationSelected:(i)async{' in nav and "if(i!=0&&await misafirEngeli(context))return;" in nav,
  '5 nav destination unchanged': all("label:t('"+x+"')" in nav for x in ['flow','explore','create','chat','me']),
  'prominent central create': 'width:54,height:46' in nav and 'width:58,height:48' in nav,
  'message requests retained': 'gelenKutusuIsteginiSonuclandir' in main,
  'published media flow retained': '_finalUretKart' in main,
}
for k,v in checks.items():
 print(('OK:   ' if v else 'FAIL: ')+k,flush=True)
if not all(checks.values()):
 raise SystemExit('Build 402 regression failed')
print('Build 402 profile preservation and visual contract passed.',flush=True)
