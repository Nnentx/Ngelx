#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 320 verification failed: "+msg)

req("version: 1.0.101+320" in PUB,"pubspec version")
req("defaultValue: '1.0.101'" in MAIN and "defaultValue: '320'" in MAIN,"runtime version")

for token in [
    "Future<void> _gelenKutusunuYenile()",
    "onRefresh:_gelenKutusunuYenile",
    "tooltip:lt('Yenile','Refresh'),onPressed:ben==null?null:_gelenKutusunuYenile",
    "Future<void> _grupSohbetiniYenile()",
    "onRefresh:_grupSohbetiniYenile",
    "onPressed:_grupSohbetiniYenile",
    "Future<void> _ozelSohbetiYenile()",
    "onRefresh:_ozelSohbetiYenile",
    "onPressed:_ozelSohbetiYenile",
    "Future<void> _aktiviteyiYenile()",
    "onPressed:_aktiviteyiYenile",
    "GetOptions(source:Source.server)",
    "AlwaysScrollableScrollPhysics()",
]:
    req(token in MAIN,token)

req(MAIN.count("RefreshIndicator(") >= 7,"refresh indicator regression")
print("Build 320 refresh/quality verification passed.")
