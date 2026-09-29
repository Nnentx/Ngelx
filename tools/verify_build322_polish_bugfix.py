#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")
CAM=(ROOT/"app/lib/camera_studio.dart").read_text(encoding="utf-8")
BADGE=(ROOT/"app/lib/feed_creator_badge.dart").read_text(encoding="utf-8")
def req(ok,msg):
    if not ok: raise SystemExit("Build 322 verification failed: "+msg)
req("version: 1.0.103+322" in PUB,"pubspec version")
req("defaultValue: '322'" in MAIN,"runtime build")
req("NgelXYorumKullaniciSatiri" in MAIN,"comment creator badge wiring")
req("NgelXIcerikUreticisiRozeti(kucuk:true)" in BADGE,"small creator badge")
req("ngelxIcerikSilindi(id)" in MAIN and "ngelxSilinenIcerikIdleri.contains" in MAIN,"immediate deletion")
req("tooltip:lt('Yenile','Refresh'),\n            onPressed:_grupSohbetiniYenile" not in MAIN,"group header refresh removed")
req("await eski.dispose()" in CAM and "Duration(milliseconds:140)" in CAM,"camera flip lifecycle")
for name in ("Clean","Soft","Glow","HD"): req(name in CAM,"camera filter "+name)
for name in ("Clean","Soft","Glow","HD"): req(name in BADGE,"call filter "+name)
req("ngelxAramaEfekti" in MAIN,"call effect helper wiring")
req(len(MAIN)<=1_220_000,"main.dart size contract")
print("Build 322 polish/bugfix verification passed.")
