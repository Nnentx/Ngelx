#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[1]/"app/lib"
needles=[
  "ngelxKisiyeIcerikGonder",
  "shared_content",
  "collection('chats')",
  'collection("chats")',
  "live_streams",
  "Canlı yayınlar",
  "CanliYayin",
  "_canliSecimKutusu",
]
for p in root.rglob("*.dart"):
    try:
        text=p.read_text(encoding="utf-8")
    except Exception:
        continue
    for n in needles:
        start=0
        hit=0
        while hit<8:
            i=text.find(n,start)
            if i<0: break
            a=max(0,i-1800); b=min(len(text),i+6500)
            print(f"\n===== {p.relative_to(root)} :: {n} :: hit {hit+1} @ {i} =====\n")
            print(text[a:b])
            start=i+len(n)
            hit+=1
