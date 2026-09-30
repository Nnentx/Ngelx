#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
main=(root/"app/lib/main.dart").read_text(encoding="utf-8")
live=(root/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")

targets=[
  ("SEND_HELPER",main,"Future<void> ngelxKisiyeIcerikGonder"),
  ("SHARE_UI",main,"NgelXPaylas"),
  ("MESAJ_PAGE",main,"class MesajPage"),
  ("CHAT_PAGE",main,"class Sohbet"),
  ("FRIENDS_FIELD",main,"['friends']"),
  ("GROUP_COLLECTION",main,"collection('groups')"),
  ("NOTIFY_HELPER",main,"Future<void> uygulamaBildirimiGonder"),
  ("USERS_STREAM",main,"collection('users')"),
  ("LIVE_SHARE",live,"Future<void> _paylas()"),
  ("LIVE_BUILD",live,"class _CanliYayinPageState"),
]

for label,text,needle in targets:
    i=text.find(needle)
    if i<0:
        print(f"===== {label} NOT FOUND: {needle} =====")
        continue
    a=max(0,i-1400); b=min(len(text),i+7000)
    print(f"\n===== {label} =====\n")
    print(text[a:b])
