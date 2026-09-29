#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")
ANDROID = (ROOT / "app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 312 verification failed: " + message)

require("version: 1.0.93+312" in PUB, "pubspec version")
require("defaultValue: '1.0.93'" in MAIN and "defaultValue: '312'" in MAIN, "runtime version")
picker_start = MAIN.index("Future<XFile?> ngelxResimSec({")
picker_end = MAIN.index("Future<XFile?> ngelxVideoSec({", picker_start)
picker = MAIN[picker_start:picker_end]
require("yenidenKodla=false" in picker, "Android fallback disables local image recompression")
require("imageQuality:yenidenKodla?imageQuality:null" in picker, "single picker fallback is raw")
require("maxWidth:yenidenKodla?maxWidth:null" in picker, "single picker resize is disabled on fallback")
require(MAIN.count("ImagePicker().pickImage(") == 1, "single image picker remains centralized")
multi_start = MAIN.index("Future<List<XFile>> ngelxCokluResimSec({")
multi_end = MAIN.index("Future<XFile?> ngelxDosyaSec", multi_start)
multi = MAIN[multi_start:multi_end]
require("yenidenKodla=false" in multi, "Android multi-picker fallback disables recompression")
require("imageQuality:yenidenKodla?imageQuality:null" in multi, "multi-picker fallback is raw")
require(MAIN.count("ImagePicker().pickMultiImage(") == 1, "multi image picker remains centralized")
upload_start = MAIN.index("Future<String> ngelxFotografYukle({")
upload_end = MAIN.index("Future<void> ngelxMedyaSil(", upload_start)
upload = MAIN[upload_start:upload_end]
for signature in ("0xFF,0xD8,0xFF", "GIF8", "WEBP", "ftyp", "image/avif", "image/heic", "image/heif"):
    require(signature in upload, "photo header detection: " + signature)
require("dosya.openRead(0,32)" in upload, "header detection streams only the prefix")
require("ngelxMedyaYukleDosya(" in upload, "photo upload remains file-stream based")
require("pickerRequestedImage" in ANDROID, "native picker remembers requested media kind")
require("copyUriToCache(it, requestedImage)" in ANDROID, "native picker forwards image intent")
require("private fun detectImageType(file: File)" in ANDROID, "native file signature detection")
require("requestedImage || mimeType?.startsWith(\"image/\")" in ANDROID, "missing MIME still normalizes images")
print("Build 312 media root fix verified.")
