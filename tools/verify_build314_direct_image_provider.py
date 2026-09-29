#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 314 verification failed: "+message)

require("version: 1.0.95+314" in PUB,"pubspec version")
require("defaultValue: '1.0.95'" in MAIN and "defaultValue: '314'" in MAIN,"runtime version")
require("Future<Uint8List> _ngelxAgResmiBaytlari" in MAIN,"direct byte downloader")
require("ui.instantiateImageCodec(bytes)" in MAIN,"Flutter codec verification")
require("class NgelXAgImageProvider extends ImageProvider" in MAIN,"shared image provider")
require("ui.ImmutableBuffer.fromUint8List(bytes)" in MAIN,"provider decodes verified bytes")
require("Future<void> ngelxAgResmiOnbelleginiTemizle" in MAIN,"shared cache eviction")
require("class NgelXAgResmi extends StatefulWidget" in MAIN,"shared image widget")
require("image:NgelXAgImageProvider(temiz)" in MAIN,"widget uses shared provider")
require("CachedNetworkImageProvider" not in MAIN,"cached provider fully removed")
require("CachedNetworkImage(" not in MAIN,"cached widget fully removed")
require("CachedNetworkImage.evictFromCache" not in MAIN,"cached eviction fully removed")
require("package:cached_network_image/cached_network_image.dart" not in MAIN,"cached image import removed")

for marker in ("kind:'profiles'","kind:'stories'","kind:'groups'"):
    require(marker in MAIN,"photo flow remains connected: "+marker)

print("Build 314 direct image provider verification passed.")
