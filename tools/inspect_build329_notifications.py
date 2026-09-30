#!/usr/bin/env python3
from pathlib import Path
text=(Path(__file__).resolve().parents[1]/"app/lib/main.dart").read_text(encoding="utf-8")
for needle in ["_bildirimBasligi(","onTap:()=>_aktiviteAc","_aktiviteAc(context","eventKind']??","sourceId']??"]:
    start=0
    for n in range(12):
        i=text.find(needle,start)
        if i<0: break
        print(f"\n===== {needle} HIT {n+1} @ {i} =====\n")
        print(text[max(0,i-1800):min(len(text),i+6000)])
        start=i+len(needle)
