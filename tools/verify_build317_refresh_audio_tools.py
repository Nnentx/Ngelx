#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
MUSIC=(ROOT/"app/lib/create_music_editor.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 317 verification failed: "+msg)

req("version: 1.0.98+317" in PUB,"pubspec version")
req("defaultValue: '1.0.98'" in MAIN and "defaultValue: '317'" in MAIN,"runtime version")
req("Future<void> _akisiYenile()" in MAIN and "onRefresh:_akisiYenile" in MAIN,"feed refresh")
req("Future<void> _kesfetiYenile()" in MAIN and "onRefresh:_kesfetiYenile" in MAIN,"explore refresh")
req("Future<void> _uretiYenile()" in MAIN and "onRefresh:_uretiYenile" in MAIN,"create refresh")
req("if(p!=null)await p.pause();" in MAIN,"photo music pauses before profile")
req("_oynatmalariDuraklat();\n    await Navigator.push" in MAIN,"video audio pauses before profile")
req("title:const Text('Altyazı dili'" in MAIN,"caption language selector")
req("altyaziUret(setP,zorlaCeviri:true)" in MAIN,"caption translation on language change")
req("NgelX müzik ekle" in MAIN,"photo music CTA")
req("NgelX Müzik" in MUSIC and "NgelX müziklerinde ara" in MUSIC,"music library UI")
req("backgroundImage:profilFoto.isEmpty?null:NgelXAgImageProvider(profilFoto)" in MAIN,"photo feed avatar preserved")
print("Build 317 verification passed.")
