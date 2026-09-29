#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Build 315 verification failed: "+message)

require("version: 1.0.96+315" in PUB,"pubspec version")
require("defaultValue: '1.0.96'" in MAIN and "defaultValue: '315'" in MAIN,"runtime version")
token="if(!hazirlik.sohbetMevcut)'members':[ben,widget.digerUid],"
require(MAIN.count(token)==3,"all private message send paths preserve existing member order")
require(MAIN.count("'members':[ben,widget.digerUid],")>=3,"new private chat creation still writes members")
require("Mesaj gönderilemedi: $hata" in MAIN,"send failure exposes actionable Firestore error")
require("await ngelxBatchCommitDogrula(" in MAIN,"verified batch commit remains active")

print("Build 315 private chat send fix verification passed.")
