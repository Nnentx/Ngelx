#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
live=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
pub=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

checks={
  "version":"version: 1.0.107+326" in pub,
  "pro presets":"ngelxCanliProFiltreleri" in live and "Kontrast+" in live and "Portre Pro" in live,
  "matrix engine":"ngelxCanliRenkMatrisi" in live,
  "beauty":"filterBrightness" in live and "filterContrast" in live and "filterSaturation" in live and "filterWarmth" in live and "filterClarity" in live,
  "auto enhance":"autoEnhance" in live and "lowLight" in live,
  "camera focus":"CameraFocusMode.auto" in live and "CameraExposureMode.auto" in live,
  "prepare studio":"NgelX Görüntü Stüdyosu" in live,
  "live studio":"Future<void> _goruntuStudyoPaneli()" in live,
  "viewer effect":"ngelxCanliEfektKatmani(veri:veri" in live,
  "compact snackbar":"SnackBarBehavior.floating" in live,
  "build number":"defaultValue: '326'" in main,
}

failed=[name for name,ok in checks.items() if not ok]
for name,ok in checks.items():
    print(("OK  " if ok else "FAIL")+" "+name)
if failed:
    raise SystemExit("Build 326 verification failed: "+", ".join(failed))
print("Build 326 verification passed.")
