#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
PUB = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 310 verification failed: " + message)

require("version: 1.0.91+310" in PUB, "pubspec version")
require("defaultValue: '1.0.91'" in MAIN and "defaultValue: '310'" in MAIN, "runtime version")

require("Future<String> ngelxFotografYukle({" in MAIN, "shared photo helper")
helper = MAIN.split("Future<String> ngelxFotografYukle({",1)[1].split("Future<void> ngelxMedyaSil(",1)[0]
require("ngelxMedyaYukleBytes(" in helper, "photo helper uses byte normalization")
require("ngelxMedyaYukleDosya(" not in helper, "photo helper must not bypass normalization")

kind_region = MAIN.split("bool _ngelxFotoKind",1)[1].split("}.contains(kind);",1)[0]
require("'chats'" in kind_region, "chat photos normalized")
require("'profiles'" in kind_region and "'groups'" in kind_region and "'stories'" in kind_region, "profile/group/story normalization preserved")

g0 = MAIN.find("class _GorselYaziKartiState")
g1 = MAIN.find("\nclass ", g0 + 10) if g0 >= 0 else -1
feed_region = MAIN[g0:(g1 if g1 > g0 else len(MAIN))] if g0 >= 0 else ""
require("fotoListesi[i]" in feed_region and "NgelXAgResmi(" in feed_region, "feed media host fallback")

require("class NgelXAgResmi extends StatefulWidget" in MAIN, "network image fallback helper")
require("yuklenecekBytes=await ngelxFotoDuzenle(bytes)" in MAIN, "photo bytes re-encoded")
require("Future<XFile?> ngelxResimSec" in MAIN, "Android photo picker fallback preserved")
require("ACTION_GET_CONTENT" in (ROOT / "app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8"), "native picker preserved")

print("Build 310 global media fix verified.")
