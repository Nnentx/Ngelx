#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[1]/"app/lib"

def emit(label,p,text,i,before=1800,after=6000):
    print(f"\n===== {label} :: {p.relative_to(root)} @ {i} =====\n")
    print(text[max(0,i-before):min(len(text),i+after)])

for p in root.rglob("*.dart"):
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    for label,needle in [
        ("SEND_HELPER","Future<void> ngelxKisiyeIcerikGonder"),
        ("SHARED_RENDER","shared_content"),
        ("LIVE_SHARE_RENDER","liveShare"),
        ("EXPLORE_LIVE_TITLE","Canlı yayınlar"),
        ("EXPLORE_ACTIVE_QUERY",".where('active'"),
        ("EXPLORE_LIVE_COLLECTION","collection('live_streams')"),
        ("LIVE_OPEN","CanliYayinPage("),
    ]:
        start=0
        hits=0
        while hits<6:
            i=text.find(needle,start)
            if i<0:break
            emit(label,p,text,i)
            start=i+len(needle);hits+=1
