#!/usr/bin/env python3
"""Build 405 regressions: single-phone fixes. Remote-participant E2E deliberately deferred."""
from pathlib import Path

def load(path): return Path(path).read_text(encoding="utf-8")
m=load("app/lib/main.dart")
s=load("app/lib/story_v66.dart")
l=load("app/lib/live_broadcast_studio.dart")
a=load("app/lib/audio_live_rooms.dart")
p=load("app/pubspec.yaml")
t=load("app/lib/build258_settings.dart")
owner=m[m.index("class _ProfilPageState extends State<ProfilPage>"):m.index("\nclass _ProfilEtkilesimRozeti")]
checks={
  "version": "version: 1.0.181+405" in p and "defaultValue: '405'" in m,
  "profile real video preserved":"ProfilTanitimVideoKarti(url:tanitimVideoUrl)" in owner,
  "profile saved/friends": "'Arkadaşlar'" in owner and "SizedBox(height:28,child:Center(child:Text(yazi" in owner,
  "profile stable intro player": "initialize().timeout(const Duration(seconds:15))" in m,
  "profile saved video retry":"initialize().timeout(const Duration(seconds:12))" in m,
  "real profile uploads":"kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in m,
  "story next video prefetched":"sonrakiVideoKontrol" in s and "Duration(seconds:12)" in s,
  "story next image prefetched":"precacheImage(NgelXAgImageProvider(adres),context)" in s,
  "story photo gated on load":"await precacheImage(NgelXAgImageProvider(medyaAdresi),context)" in s,
  "story retry visible":"Tekrar dene" in s and "videoHata=true" in s,
  "story duration preserves video length":"sure.duration=Duration(milliseconds:ms)" in s,
  "story skip on error prevented":"if(videoHata||(videoMu&&!videoHazir))return" in s,
  "live one summary view":"Widget _bitisEkrani()" in l and "if(yayinBitti)Positioned.fill(child:_bitisEkrani())" in l,
  "live no modal summary":"showDialog<void>" not in l[l.index("Future<bool> _geri() async {"):l.index("Future<Map<String, dynamic>> _aktifProfil() async {")],
  "live leave only via action":"onPressed:bitisOzetiHazir?()=>Navigator.pop(context):null" in l,
  "live real counts":"sonYorumSayisi=yorumSayisi" in l and "sonHediyePuani=hediyePuani" in l,
  "live real streaming":"widget.oda.disconnect()" in l,
  "voice real functionality":"speaker_requests" in a and "2. kişi bekleniyor • Davet edebilirsin" in a,
  "premium blue only": "e.baslik==t('premiumWallet')?const Color(0xFFEAF2FF)" in t,
  "inbox preserved":"gelenKutusuIsteginiSonuclandir" in m,
  "explore/create preserved":"_finalUretKart" in m and "_profilHikayeGridFinal()" in m,
}
for name,ok in checks.items():print(("OK   " if ok else "FAIL ")+name,flush=True)
if not all(checks.values()):raise SystemExit("Build 405 regression check failed")
print("Build 405 source regression checks passed. Android device & two-account E2E not certified.",flush=True)
