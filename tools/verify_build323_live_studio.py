#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
LIVE = (ROOT / "app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")


def req(ok, message):
    if not ok:
        raise SystemExit("Build 323 verification failed: " + message)


req("version: 1.0.104+323" in PUB, "pubspec version")
req("defaultValue: '1.0.104'" in MAIN, "runtime version")
req("defaultValue: '323'" in MAIN, "runtime build")
req("part 'live_broadcast_studio.dart';" in MAIN, "live studio module wiring")
req("CameraPreview(c)" in LIVE and "availableCameras()" in LIVE, "real pre-live camera preview")
req("_kamerayiCevir" in LIVE and "CameraLensDirection.back" in LIVE, "front/back preview camera")
req("ngelxKameraFiltreleri" in LIVE and "Doğal rötuş" in LIVE, "NgelX filters and natural retouch")
req("FlashMode.torch" in LIVE and "Bu cihaz canlı önizlemede flaşı desteklemiyor" in LIVE, "supported-device flash")
for ratio in ("9:16", "1:1", "16:9"):
    req(ratio in LIVE, "aspect ratio " + ratio)
for quality in ("540p", "720p", "1080p"):
    req(quality in LIVE, "quality " + quality)
req("Yayın yalnızca “Canlı yayını başlat” düğmesine bastığında başlar." in LIVE, "explicit start contract")
req("defaultCameraCaptureOptions: _kameraAyarlari" in LIVE, "LiveKit camera options")
req("track.restartTrack" in LIVE and "_yayinKamerasiniCevir" in LIVE, "in-room safe camera switch")
req("cameraPosition" in LIVE and "aspectRatio" in LIVE and "quality" in LIVE, "broadcast setting persistence")
req(len(MAIN) <= 1_220_000, "main.dart size contract")
print("Build 323 live studio verification passed.")
