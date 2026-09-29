#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
LIVE=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 325 verification failed: "+msg)

req("version: 1.0.106+325" in PUB,"version")
for marker in [
    "Future<void> ngelxCanliYayinaKatil",
    "final canliBildirimi=tur=='live'||olayTuru=='live_started'",
    "case 'live':return Icons.live_tv_rounded",
    "if(tur=='live'&&kaynak.isNotEmpty)",
    "bool profilCanli=false",
    "_profilCanliAboneligi",
    "if(profilCanli)Positioned",
    "p['isLive']==true",
    "final canli=v['isLive']==true",
    "Canlı yayını izle",
    "kontrollerGorunur",
    "_videoDurumu",
    "final yukseklik=videoOrani<1?340.0:210.0",
]:
    req(marker in MAIN,marker)
for marker in [
    "final canliHedefler=List<String>.from",
    "tur:'live'",
    "olayTuru:'live_started'",
]:
    req(marker in LIVE,marker)
print("Build 325 live presence verification passed.")
