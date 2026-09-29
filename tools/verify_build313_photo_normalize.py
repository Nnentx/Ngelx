#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")
CREATE = (ROOT / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 313 verification failed: " + message)


require("version: 1.0.94+313" in PUB, "pubspec version")
require("image: ^4.10.1" in PUB, "image codec dependency")
require("defaultValue: '1.0.94'" in MAIN and "defaultValue: '313'" in MAIN, "runtime version")
require("import 'package:image/image.dart' as img;" in MAIN, "image codec import")
require("Future<Uint8List> _ngelxFotografiJpegHazirla" in MAIN, "shared JPEG normalization")
require("await ngelxFotoDuzenle(hamBytes)" in MAIN, "device codec decodes source first")
require("img.encodeJpg(decoded,quality:90)" in MAIN, "real JPEG encoding")
require("img.decodeJpg(sonuc)" in MAIN, "local JPEG decode verification")
require("jpeg[jpeg.length-2]!=0xFF||jpeg.last!=0xD9" in MAIN, "complete JPEG marker verification")
require("Future<String> _ngelxFotografYayininiDogrula" in MAIN, "remote photo verification")
require("responseType:ResponseType.bytes" in MAIN, "remote bytes are downloaded")
require("final decoded=img.decodeImage(bytes)" in MAIN, "remote bytes are decoded")
require("kayıt değiştirilmedi" in MAIN, "failed remote verification blocks metadata changes")

bytes_start = MAIN.index("Future<String> ngelxMedyaYukleBytes({")
bytes_end = MAIN.index("Future<String> ngelxMedyaYukleDosya({", bytes_start)
bytes_upload = MAIN[bytes_start:bytes_end]
require("_ngelxFotografiJpegHazirla(bytes)" in bytes_upload, "all byte photo uploads normalize")
require("zorunluContentType='image/jpeg'" in bytes_upload, "JPEG MIME is authoritative")
require("_ngelxFotografYayininiDogrula(okunabilir)" in bytes_upload, "all photo uploads verify remote decode")

file_start = MAIN.index("Future<String> ngelxFotografYukle({")
file_end = MAIN.index("Future<void> ngelxMedyaSil(", file_start)
file_upload = MAIN[file_start:file_end]
require("dosya.readAsBytes()" in file_upload, "file photo joins byte normalization pipeline")
require("ngelxMedyaYukleBytes(" in file_upload, "file photo uses shared byte uploader")
require("ngelxMedyaYukleDosya(" not in file_upload, "raw photo file upload bypass removed")

require("kind:'photos'" in CREATE and "ngelxMedyaYukleBytes(" in CREATE, "create flow uses normalized pipeline")
for kind in ("kind:'profiles'", "kind:'stories'", "kind:'groups'"):
    require(kind in MAIN, "shared flow remains connected: " + kind)

print("Build 313 photo normalization and remote decode verification passed.")
