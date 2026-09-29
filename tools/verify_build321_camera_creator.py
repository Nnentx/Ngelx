#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")
CAM=(ROOT/"app/lib/camera_studio.dart").read_text(encoding="utf-8")
BADGE=(ROOT/"app/lib/feed_creator_badge.dart").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 321 verification failed: "+msg)

req("version: 1.0.102+321" in PUB,"pubspec version")
req("camera: ^" in PUB,"camera dependency")
req("package:camera/camera.dart" in MAIN,"camera import")
req("part 'camera_studio.dart';" in MAIN,"camera part")
req("part 'feed_creator_badge.dart';" in MAIN,"creator badge part")
req("defaultValue: '321'" in MAIN,"runtime build")
req("NgelXCameraStudioPage" in MAIN and "NgelXCameraStudioPage" in CAM,"camera studio wiring")
for token in (
    "CameraPreview",
    "cameraswitch_rounded",
    "FlashMode",
    "timer_outlined",
    "grid_3x3_rounded",
    "aspect_ratio_rounded",
    "face_retouching_natural_rounded",
    "filter_alt_rounded",
    "İki parmakla yakınlaştır",
    "Future<XFile> _fotoyuIsle",
):
    req(token in CAM,token)
for token in (
    "class NgelXIcerikUreticisiRozeti",
    "İçerik Üreticisi",
    "class NgelXPaylasanSatiri",
):
    req(token in BADGE,token)
req(MAIN.count("NgelXPaylasanSatiri(")>=2,"feed creator rows")
req("'creatorId':user.uid" in MAIN and "'creatorUsername':adi" in MAIN,"creator attribution")
req(len(MAIN)<=1_220_000,"main.dart size contract")
print("Build 321 camera/creator verification passed.")
