#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]/"app/lib"
needles=[
 "hedefTuru",
 "live_started",
 "live_share",
 "bildirim",
 "Bildirim",
 "notifications",
 "olayTuru",
 "uygulamaBildirimiGonder",
]
for p in root.rglob("*.dart"):
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    for n in needles:
        start=0; hit=0
        while hit<8:
            i=text.find(n,start)
            if i<0: break
            print(f"\n===== {p.relative_to(root)} :: {n} :: {hit+1} @ {i} =====\n")
            print(text[max(0,i-1800):min(len(text),i+6500)])
            start=i+len(n); hit+=1
