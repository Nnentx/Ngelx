#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
STORY = (ROOT / "app/lib/story_v66.dart").read_text(encoding="utf-8")
MUSIC = (ROOT / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("V82 medya güvenilirliği kontrolü eksik: " + message)


require("version: 1.0.83+302" in PUB, "Build 302 sürümü")
require("defaultValue: '1.0.83'" in MAIN and "defaultValue: '302'" in MAIN,
        "uygulama içi Build 302 bilgisi")
require("List<String> ngelxMedyaUrlAdaylari" in MAIN and "_ngelxMediaApiBackup" in MAIN,
        "ana/yedek medya URL çözümlemesi")
require("class NgelXAgResmi extends StatefulWidget" in MAIN,
        "okuma hatasında yedek kaynağa geçen ortak görsel")
require("bytes=0-63" in MAIN and "no-cache, no-store" in MAIN,
        "yükleme sonrası gerçek içerik doğrulaması")
require("_ngelxFotoKind" in MAIN and "yuklenecekBytes=await ngelxFotoDuzenle(bytes)" in MAIN,
        "profil, grup, hikâye ve akış fotoğraflarının PNG normalizasyonu")
require("'ownerPhotoUrl':fotoUrl" in MAIN and "'ownerPhotoUrl':sahipFoto" in MAIN,
        "iki hikâye yayın yolunda profil fotoğrafı referansı")
require("grupFotografiIsleniyor" in MAIN and "finally{if(mounted)setState(()=>grupFotografiIsleniyor=false);}" in MAIN,
        "grup fotoğrafı işlemi tekilleştirme kilidi")
require("isScrollControlled:true,useSafeArea:true" in MAIN and
        "Şikâyet nedenini seç" in MAIN and "child:ListView(shrinkWrap:true" in MAIN,
        "şikâyet ekranı taşma düzeltmesi")
require("NgelXAgResmi(" in STORY,
        "hikâyede yedek kaynaklı görsel oynatma")
require("Cihazımdan müzik ekle" in MUSIC,
        "boş katalogda çalışan cihaz müziği yolu")

print("V82 Build 302 medya/Firebase güvenilirliği doğrulandı.")
