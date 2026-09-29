#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")
ANDROID = (ROOT / "app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 311 verification failed: " + message)

require("version: 1.0.92+311" in PUB, "pubspec version")
require("defaultValue: '1.0.92'" in MAIN and "defaultValue: '311'" in MAIN, "runtime version")

start = MAIN.find("Future<String> ngelxFotografYukle({")
end = MAIN.find("Future<void> ngelxMedyaSil(", start)
require(start >= 0 and end > start, "shared photo helper")
helper = MAIN[start:end]
require("ngelxMedyaYukleDosya(" in helper, "photo helper uses direct file upload")
require("ngelxMedyaYukleBytes(" not in helper, "photo helper must not force byte decode")
require("dosya.mimeType" in helper and "contentType:tur" in helper, "real MIME type preserved")
require("image/avif" in helper and "image/heic" in helper and "image/heif" in helper, "modern image MIME handling")

require("private fun normalizeImageToJpeg(uri: Uri): File?" in ANDROID, "native JPEG normalizer")
require("ImageDecoder.createSource(contentResolver, uri)" in ANDROID, "Android URI decoder")
require("Bitmap.CompressFormat.JPEG, 92" in ANDROID, "native JPEG output")
require('"mimeType" to "image/jpeg"' in ANDROID, "normalized MIME result")
require("ACTION_GET_CONTENT" in ANDROID and "ACTION_OPEN_DOCUMENT" in ANDROID, "native picker fallback preserved")
require("max(width, height)" in ANDROID and "largest > 4096" in ANDROID, "large image downscaling")

print("Build 311 image decode fix verified.")
