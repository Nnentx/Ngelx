#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(cond,msg):
    if not cond:
        raise SystemExit("Build 298 medya/diyalog kontrolu eksik: "+msg)

require("version: 1.0.82+301" in PUB,"Build 301 surumu")
require("defaultValue: '1.0.82'" in MAIN and "defaultValue: '301'" in MAIN,"uygulama ici surum")
require("class NgelXSohbetFotoOnizleme" in MAIN and "ngelxMesajMedyaUrl(v,video:tur=='video')" in MAIN,
        "grup fotograf/video URL cozumleme")
require("videoKapak=ngelxMesajVideoKapagi(v)" in MAIN,
        "grup video kapak alanlari")
require("NgelXSohbetFotoOnizleme(url:media)" in MAIN,
        "grup fotograf karti gercek onizleme")
require("NgelXSohbetVideoOnizleme(url:media,thumbnailUrl:videoKapak)" in MAIN,
        "grup video karti kapak/ilk kare")
require("NgelXVideoKapakOnizleme(url:url)" in MAIN,
        "thumbnail yoksa videonun ilk karesi")
require("'type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url" in MAIN,
        "grup fotograf alanlari geriye donuk uyumlu kayit")
require("'senderId':ben,'text':'','type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url" in MAIN,
        "ozel fotograf alanlari geriye donuk uyumlu kayit")
require("'type':'video','mediaUrl':url,'videoUrl':url" in MAIN,
        "grup video URL kaydi")
require("final thumb=ngelxMesajVideoKapagi(data);" in MAIN and
        "NgelXVideoKapakOnizleme(url:url)" in MAIN,
        "grup medya galerisi video goruntusu")
require("Arkadaşlıktan çıkarılsın mı?" in MAIN and
        "Bu işlem yalnızca arkadaşlığı kaldırır." in MAIN and
        "dialogTheme:const DialogThemeData(backgroundColor:Colors.white" in MAIN,
        "arkadasliktan cikarma diyalogu gorunur metin/stil")

print("Build 298 grup/ozel medya onizleme ve arkadaslik diyalogu dogrulandi.")
# Build 298 final QA trigger
