#!/usr/bin/env python3
"""Regression gate: Build 401 improves presentation without deleting working routes."""
from pathlib import Path
import sys

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
pub=Path('app/pubspec.yaml').read_text(encoding='utf-8')
story=main[main.index('class _HikayeGosterPageState'):main.index('\nclass ',main.index('class _HikayeGosterPageState')+20)]
profile=main[main.index('class _ProfilPageState'):main.index('\nclass _ProfilEtkilesimRozeti',main.index('class _ProfilPageState'))]
cover=profile[profile.index('Future<void> kapakFotografiDuzenle()'):profile.index('Future<void> tanitimVideosuYukle()')]

checks={
 'Build 401 version': 'version: 1.0.177+401' in pub and "defaultValue: '401'" in main,
 'cover R2 upload preserved': "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in cover,
 'cover menu black labels': "Text('Galeriden seç',style:TextStyle(color:Colors.black87" in cover and "Text('Kapağı yeniden konumlandır',style:TextStyle(color:Colors.black87" in cover,
 'cover removal preserved': "Navigator.pop(c,'remove')" in cover,
 'story action labels contrast': "Text('Hikâyeyi paylaş',style:TextStyle(color:Colors.black87" in story and "Text('NgelX içinde özele gönder',style:TextStyle(color:Colors.black87" in story,
 'story external share preserved': 'SharePlus.instance.share' in story,
 'story private share preserved': 'ngelxOzeldenPaylas' in story,
 'intro video real uploader preserved': 'onPressed:tanitimVideosuYukle' in profile and 'ProfilTanitimVideoKarti(url:tanitimVideoUrl)' in profile,
 'stats retained': all(x in profile for x in ["'$canliTakip'","'$canliTakipci'","'$etkilesim'","'$canliArkadas'"]),
 'reference tabs': " _ProfilSekme('Hikayeler',profilSekme==3" in profile and "_ProfilSekme(t('saved'),profilSekme==4" in profile,
 'story tab action': 'if(profilSekme==3)return _profilHikayeGridFinal();' in profile,
 'saved tab real data': 'if(profilSekme==4)return _kaydedilenGrid();' in profile,
 'follow links preserved': "alan:'following'" in profile and "alan:'followers'" in profile,
 'profile search preserved': 'ProfilAramaPage(uid:' in profile,
 'chat preserved': 'gelenKutusuIsteginiSonuclandir' in main,
 'create preserved': '_finalUretKart' in main,
 '5-tab navigation preserved': "label:t('flow')" in main and "label:t('chat')" in main and "label:t('me')" in main,
 'white bottom nav': 'bottomNavigationBar:akis&&temizAkis' in main and 'border:Border(top:BorderSide(color:Color(0xFFE6E8EF)))' in main,
}
for k,v in checks.items():
 print(('OK   ' if v else 'FAIL ')+k,flush=True)
if not all(checks.values()):
 sys.exit(1)
print('Build 401 profile regression checks passed.',flush=True)
