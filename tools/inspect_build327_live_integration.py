#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[1]
main=(root/"app/lib/main.dart").read_text(encoding="utf-8")
live=(root/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")

patterns=[
  "collection('messages')","collection(\"messages\")",
  "collection('chats')","collection(\"chats\")",
  "collection('conversations')","collection(\"conversations\")",
  "collection('groups')","collection(\"groups\")",
  "collection('notifications')","collection(\"notifications\")",
  "uygulamaBildirimiGonder","friends","friend_request","message",
  "Sohbet","Gelen Kutusu","Mesaj","chatId","sohbetId",
]

def show(label,text,pat):
    start=0
    seen=0
    while seen<6:
        i=text.find(pat,start)
        if i<0: break
        a=max(0,i-900); b=min(len(text),i+2200)
        print(f"\n===== {label} :: {pat} :: hit {seen+1} =====\n")
        print(text[a:b])
        start=i+len(pat); seen+=1

for p in patterns:
    show("MAIN",main,p)
for p in ["_paylas","comments","reactions","remoteParticipants","connectionState","ConnectionState","ownerId","username"]:
    show("LIVE",live,p)
