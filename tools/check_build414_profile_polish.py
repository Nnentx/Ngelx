#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('class _ArkadaslarPageState extends State<ArkadaslarPage>')
b=s.index('\nclass ',a+7)
friend=s[a:b]
a=s.index('class _ProfilTanitimVideoKartiState')
b=s.index('\nclass OrtakGruplarPage',a)
intro=s[a:b]
a=s.index('class NgelXOnayliProfilDuzenlePage')
b=s.index('class ProfilPage extends StatefulWidget',a)
editor=s[a:b]
checks={
  'friend real count preserved':"ids.length.toString()+' Arkadaş'" in friend,
  'friend filtered label':"Arama sonuçları" in friend,
  'compact tabs':"Tab(text:'Öneriler')" in friend and "Tab(text:'Ortak')" in friend,
  'friend search filtering preserved':'if(!_esles(id,v))return const SizedBox.shrink();' in friend,
  'intro overlay is compact':"size:45" in intro and
    "Tanıtım videosunu oynat" not in intro,
  'intro playback unchanged':'onTap:yukleniyor?null:()=>unawaited(_hazirla())' in intro,
  'small cover edit button':'IconButton.filledTonal(' in editor and
    "tooltip:'Kapak fotoğrafını değiştir'" in editor,
  'cover callbacks unchanged':'onPressed:_kaydediliyor?null:widget.onKapak' in editor,
  'appearance mode preserved':"'profileViewMode':_gorunum" in editor,
  'story and social fixes retained':"final alt=arkadas" in friend
    and "where(FieldPath.documentId" in s
    and "batch.set(story," not in s[s.index('  Future<void> _yanitGonder('):s.index('\n  Widget _medya(){',s.index('  Future<void> _yanitGonder('))],
}
for key,val in checks.items():
 print(('PASS ' if val else 'FAIL ')+key,flush=True)
if not all(checks.values()):
 raise SystemExit('Build414 regression failed')
print('Build414 regression contracts PASSED. Device QA still required.')
