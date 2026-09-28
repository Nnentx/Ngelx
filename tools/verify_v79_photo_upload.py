#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(c,m):
    if not c:
        raise SystemExit("Build 298 fotoğraf yükleme kontrolu eksik: "+m)

require("version: 1.0.82+301" in PUB,"Build 301 surumu")
require("defaultValue: '1.0.82'" in MAIN and "defaultValue: '301'" in MAIN,"uygulama ici surum")

group_start=MAIN.index("Future<void> _grupFotografiniGonder")
group_end=MAIN.index("Future<void> grupVideoGonder",group_start)
group=MAIN[group_start:group_end]
require("ngelxFotografYukle(" in group,"grup fotografi ortak fallback yukleme yolu")
require("ngelxMedyaYukleBytes(" not in group,"grup fotografinda bozuk bytes yukleme yolu kaldirilmasi")
require("dosya:x" in group and "kind:'groups'" in group,"grup fotograf dosyasi ve kind")
require("'type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url" in group,"grup fotograf mesaj alanlari")

private_start=MAIN.index("Future<void> medyaGonder(ImageSource kaynak)", MAIN.index("class _SohbetPageState"))
private_end=MAIN.index("Future<void> videoGonder",private_start)
private=MAIN[private_start:private_end]
require("ngelxFotografYukle(" in private,"ozel sohbet fotografi ortak fallback yukleme yolu")
require("ngelxMedyaYukleBytes(" not in private,"ozel sohbet fotografinda bozuk bytes yukleme yolu kaldirilmasi")
require("dosya:x" in private and "kind:'chats'" in private,"ozel fotograf dosyasi ve kind")
require("'senderId':ben,'text':'','type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url" in private,"ozel fotograf mesaj alanlari")

require("NgelXSohbetFotoOnizleme(url:media)" in MAIN,"grup fotograf onizlemesi")
require("NgelXSohbetFotoOnizleme(url:medyaUrl)" in MAIN,"ozel fotograf onizlemesi")

print("Build 298 grup/ozel fotograf yükleme yolu dogrulandi.")
