#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
PUBSPEC = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Build 295 sohbet medya kontrolu eksik: {message}")


require("version: 1.0.82+301" in PUBSPEC, "Build 301 surumu")
require("defaultValue: '1.0.82'" in MAIN and "defaultValue: '301'" in MAIN,
        "uygulama ici surum varsayilanlari")
require("String ngelxMesajMedyaUrl(" in MAIN,
        "eski ve yeni sohbet medya alanlari icin URL cozumleyici")
for field in ("imageUrl", "photoUrl", "downloadUrl", "attachmentUrl"):
    require(f"veri['{field}']" in MAIN, f"fotograf geri donus alani: {field}")
for field in ("thumbnailUrl", "posterUrl", "previewUrl", "coverUrl"):
    require(f"veri['{field}']" in MAIN, f"video kapak geri donus alani: {field}")
require("class NgelXSohbetFotoOnizleme" in MAIN and
        "Fotoğraf yüklenemedi" in MAIN,
        "sabit boyutlu fotograf yukleme/hata gorunumu")
require("class NgelXSohbetVideoOnizleme" in MAIN and
        "thumbnailUrl:videoKapakUrl" in MAIN,
        "videoya ait kapak/ilk kare onizlemesi")
require("final medyaUrl=ngelxMesajMedyaUrl(v,video:video);" in MAIN,
        "ozel sohbet medya URL cozumleme baglantisi")
require("TamEkranMedyaPage(url:medyaUrl)" in MAIN and
        "TamEkranVideoPage(url:medyaUrl)" in MAIN,
        "tam ekran medya acilislarinin cozumlenen URL kullanmasi")
require("NgelXSohbetFotoOnizleme(url:medyaUrl)" in MAIN,
        "ozel sohbet fotograf karti baglantisi")
require("NgelXSohbetVideoOnizleme(url:medyaUrl,thumbnailUrl:videoKapakUrl)" in MAIN,
        "ozel sohbet video karti baglantisi")

print("Build 295 sohbet fotograf/video onizleme kontrolleri dogrulandi.")
