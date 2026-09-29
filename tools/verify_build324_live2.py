#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LIVE=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")
RULES=(ROOT/"firestore.rules").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 324 verification failed: "+msg)

req("version: 1.0.105+324" in PUB,"version")
for marker in [
    "String gizlilik = 'Herkese açık'",
    "String kategori = 'Sohbet'",
    "int fps = 30",
    "_geriSayimCalistir",
    "'isLive': true",
    "'currentLiveId': belge.id",
    "'kind': 'join'",
    "'kind': 'gift'",
    "'giftPoints': hediyePuani",
    "N-Kombo",
    "N-Hediye",
    "hintStyle: const TextStyle(color: Colors.black45",
    "final sayi=docs.fold<int>",
]:
    req(marker in LIVE,marker)
req("request.resource.data.uid == request.auth.uid" in RULES,"live comment rules uid compatibility")
print("Build 324 LIVE 2.0 verification passed.")
