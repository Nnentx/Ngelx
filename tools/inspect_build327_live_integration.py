#!/usr/bin/env python3
from pathlib import Path
main=(Path(__file__).resolve().parents[1]/"app/lib/main.dart").read_text(encoding="utf-8")

for needle in ["shared_content","contentId","m['type']","v['type']","mesaj['type']"]:
    print("\n###",needle)
    start=0
    for n in range(8):
        i=main.find(needle,start)
        if i<0: break
        print(f"\n===== {needle} HIT {n+1} @ {i} =====\n")
        print(main[max(0,i-1200):min(len(main),i+3600)])
        start=i+len(needle)
