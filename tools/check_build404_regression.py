#!/usr/bin/env python3
"""Check Build 404 user-visible fixes and preservation contract."""
from pathlib import Path
main=Path('app/lib/main.dart').read_text(encoding='utf-8')
pub=Path('app/pubspec.yaml').read_text(encoding='utf-8')
audio=Path('app/lib/audio_live_rooms.dart').read_text(encoding='utf-8')
live=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
settings=Path('app/lib/build258_settings.dart').read_text(encoding='utf-8')
audio_pro=Path('app/lib/audio_live_rooms_pro.dart').read_text(encoding='utf-8')
profile=main[main.index('class _ProfilTanitimVideoKartiState'):main.index('\nclass ',main.index('class _ProfilTanitimVideoKartiState')+20)]
checks={
 'version 1.0.180+404':"version: 1.0.180+404" in pub and "defaultValue: '404'" in main,
 'profile intro timed video':'initialize().timeout(const Duration(seconds:15))' in profile,
 'profile intro error retry':"Video yüklenemedi • Tekrar dene" in profile and 'unawaited(_hazirla())' in profile,
 'profile real video duration':'x.value.duration.inMinutes' in profile,
 'saved media retry kept':"Text('Tekrar dene'" in main and 'initialize().timeout(const Duration(seconds:12))' in main,
 'saved media pending label':'Video hazırlanıyor' in main,
 'saved does not delete content':"collection('saved')" in main and 'docs[i].reference.delete()' in main,
 'cover R2 upload preserved':"kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in main,
 'voice category background explicit':'backgroundColor:const Color(0xFFF7F5FB)' in audio and 'selectedColor:const Color(0xFFE8DAFF)' in audio,
 'voice category readable label':"const Color(0xFF27223A)" in audio and "const Color(0xFF5825AB)" in audio,
 'voice existing categories':all(k in audio for k in ['Sohbet','Müzik','Teknoloji','Spor','Gündem']),
 'voice room compact waiting':"2. kişi bekleniyor • Davet edebilirsin" in audio and 'color:const Color(0xFFFFF8E8)' not in audio,
 'voice speech waiting timeout kept':"İstekler hâlâ yükleniyor" in audio and 'Henüz söz isteği yok' in audio,
 'voice speech failed retry':"if(s.hasError)return Center(" in audio and 'unawaited(istekler())' in audio,
 'voice speech accepts and rejects':"istekSonuc(d.id,true)" in audio and "istekSonuc(d.id,false)" in audio,
 'voice server stream same':"collection('speaker_requests').where('status',isEqualTo:'pending').limit(30).snapshots()" in audio,
 'voice music kept':"Oda müziği" in audio_pro,
 'live camera waiting text':'Kamera hazırlanıyor...' in live,
 'live existing controls':"Canlı yayına başla" in live and 'Canlı yayın araçları' in live,
 'live preset high contrast':'backgroundColor:const Color(0xFFF8F7FC)' in live and 'selectedColor:const Color(0xFFEDE2FF)' in live,
 'live filter controls retained':"_proSlider('Güzellik'" in live and "_proSlider('Kontrast'" in live,
 'premium row only blue':"e.baslik==t('premiumWallet')?const Color(0xFFEAF2FF)" in settings,
 'chat/create/profile routes':"gelenKutusuIsteginiSonuclandir" in main and '_finalUretKart' in main and '_profilHikayeGridFinal()' in main,
}
for name,ok in checks.items():
 print(('OK   ' if ok else 'FAIL ')+name,flush=True)
if not all(checks.values()):raise SystemExit('Build 404 preservation or UX checks failed')
print('Build 404 regression passed. Real-device/two-account behavior still requires testing.',flush=True)
