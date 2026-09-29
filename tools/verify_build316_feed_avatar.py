#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 316 verification failed: "+message)

require("version: 1.0.97+316" in PUB,"pubspec version")
require("defaultValue: '1.0.97'" in MAIN and "defaultValue: '316'" in MAIN,"runtime version")
require("class GorselYaziKarti extends StatefulWidget" in MAIN,"photo/text feed card exists")
require("bool _profilFotoIstendi = false;" in MAIN,"photo feed avatar fetch guard")
require("Future<void> profilFotosunuGetir() async" in MAIN,"avatar loader")
require("backgroundImage:profilFoto.isEmpty?null:NgelXAgImageProvider(profilFoto)" in MAIN,"photo feed renders network avatar")
require("onTap:paylasanProfiliAc" in MAIN,"avatar opens publisher profile")
require(MAIN.count("unawaited(profilFotosunuGetir());") >= 4,"photo and video active cards load avatars")

print("Build 316 feed avatar verification passed.")
