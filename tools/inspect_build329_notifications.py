#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]/"app/lib"
targets=[
 ("SOURCE_ID","['sourceId']"),
 ("TARGET_KIND","['targetKind']"),
 ("EVENT_KIND","['eventKind']"),
 ("LIVE_TYPE","['type']=='live'"),
 ("LIVE_TYPE2","['type'] == 'live'"),
 ("NOTIF_ROUTE","notifications"),
]
for p in root.rglob("*.dart"):
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    for label,n in targets:
        start=0; hit=0
        while hit<12:
            i=text.find(n,start)
            if i<0: break
            print(f"\n===== {label} :: {p.relative_to(root)} :: {hit+1} @ {i} =====\n")
            print(text[max(0,i-1500):min(len(text),i+5000)])
            start=i+len(n); hit+=1
