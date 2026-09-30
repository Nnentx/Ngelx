#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
main=(root/"app/lib/main.dart").read_text(encoding="utf-8")

def hits(label,needle,before=1300,after=5500,limit=5):
    start=0
    for n in range(limit):
        i=main.find(needle,start)
        if i<0: break
        print(f"\n===== {label} HIT {n+1} =====\n")
        print(main[max(0,i-before):min(len(main),i+after)])
        start=i+len(needle)

hits("SHARED_CONTENT_RENDER","shared_content",1500,6500,6)
hits("CHAT_MESSAGES_RENDER","collection('messages').orderBy",1800,6500,4)
hits("GROUPS","collection('groups')",1600,6500,6)
hits("OPEN_PROFILE","ProfilPage(",1200,3200,3)
