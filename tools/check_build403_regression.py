#!/usr/bin/env python3
"""Build 403 regression: verify UX changes while preserving existing live/audio/profile actions."""
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
p=Path('app/pubspec.yaml').read_text(encoding='utf-8')
a=Path('app/lib/audio_live_rooms.dart').read_text(encoding='utf-8')
l=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
settings=Path('app/lib/build258_settings.dart').read_text(encoding='utf-8')
audio_pro=Path('app/lib/audio_live_rooms_pro.dart').read_text(encoding='utf-8')
pk=Path('app/lib/live_pk.dart').read_text(encoding='utf-8')
intro=s[s.index('class _ProfilTanitimVideoKartiState'):s.index('\nclass ',s.index('class _ProfilTanitimVideoKartiState')+10)]
saved=s[s.index('class KaydedilenlerPage'):s.index('\nclass Logo extends StatelessWidget',s.index('class KaydedilenlerPage'))]
checks={
 'version': 'version: 1.0.179+403' in p and "defaultValue: '403'" in s,
 'R2 cover kind preserved': "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in s,
 'real intro duration only if initialized': 'if(x.value.duration>Duration.zero)' in intro and "x.value.duration.inMinutes.toString().padLeft(2,'0')" in intro,
 'real video player stays': 'VideoPlayer(x)' in intro and 'x.setVolume' in intro,
 'saved actual entries': "collection('saved')" in saved and "onLongPress: () async" in saved,
 'saved thumbnail metadata fallback': "const ['thumbnailUrl','coverUrl','posterUrl','imageUrl']" in saved,
 'thumbnail bounded wait': 'initialize().timeout(const Duration(seconds:12))' in s,
 'thumbnail retry': "Text('Tekrar dene',style:TextStyle(color:Colors.black54,fontSize:10))" in s,
 'only premium row blue': "e.baslik==t('premiumWallet')?const Color(0xFFEAF2FF)" in settings and "Color(0xFF2368E8)" in settings,
 'all settings routes retained': "const HesapDegistirPage()" in settings and "const GizlilikMerkeziV366Page()" in settings,
 'voice request existing Firestore stream preserved': "collection('speaker_requests').where('status',isEqualTo:'pending').limit(30).snapshots()" in a,
 'voice request timeout guidance': "İstekler hâlâ yükleniyor" in a and "unawaited(istekler())" in a,
 'voice request empty state': "Henüz söz isteği yok" in a,
 'voice request accept reject': "istekSonuc(d.id,true)" in a and "istekSonuc(d.id,false)" in a,
 'voice privacy Firestore semantics': "gizlilik=='public'" in a and "Sesli odayı başlat" in a,
 'voice music preserved': "Oda müziği" in audio_pro,
 'live studio expandable': "child:ExpansionTile(" in l and "title:const Text('Görüntü Stüdyosu'" in l,
 'live camera available': "Ön/arka kamerayı çevir" in l,
 'live filters intact': "_proSlider('Güzellik'" in l and "_proSlider('Kontrast'" in l,
 'live start preserved': 'Canlı yayına başla' in l,
 'live controls preserved': 'Canlı yayın araçları' in l and 'Canlı Yayın' in pk,
 'profile tabs intact': '_profilHikayeGridFinal()' in s and '_kaydedilenGrid()' in s,
 'create/inbox intact': '_finalUretKart' in s and 'gelenKutusuIsteginiSonuclandir' in s,
}
for name,ok in checks.items():print(('OK   ' if ok else 'FAIL ')+name,flush=True)
if not all(checks.values()):raise SystemExit('Build 403 regression failed')
print('Build 403 checked: existing backend behavior preserved, UX hotfix markers verified.',flush=True)
