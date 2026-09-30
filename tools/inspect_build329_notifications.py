#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]/"app/lib"

targets=[
 ("LIVE_TARGET_COMPARE","hedefTuru=='live'"),
 ("LIVE_TARGET_COMPARE2","hedefTuru == 'live'"),
 ("LIVE_EVENT_COMPARE","olayTuru=='live_started'"),
 ("LIVE_EVENT_COMPARE2","olayTuru == 'live_started'"),
 ("NOTIFICATION_CARD","class Bildirim"),
 ("NOTIFICATION_TAP","onTap:"),
 ("OPEN_LIVE","canliYayinaKatil"),
 ("OPEN_LIVE2","canliYayin"),
]
for p in root.rglob("*.dart"):
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    for label,n in targets:
        start=0; hit=0
        while hit<10:
            i=text.find(n,start)
            if i<0: break
            print(f"\n===== {label} :: {p.relative_to(root)} :: {hit+1} @ {i} =====\n")
            print(text[max(0,i-1400):min(len(text),i+4200)])
            start=i+len(n); hit+=1
