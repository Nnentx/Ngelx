#!/usr/bin/env python3
"""Build 409: fix notification status for both 'group' and legacy event type.
Run after Build 408, which added the join-request lookup UI.
"""
from pathlib import Path
p=Path("app/lib/main.dart")
s=p.read_text(encoding="utf-8")
start=s.index("Widget bildirimGonderenIle(Map<String,dynamic> ham,")
end=s.index("Widget bildirimlerIcerigi()",start)
seg=s[start:end]
a="if(tur=='group_join_request'){"
b="if(tur=='group_join_request'||(v['eventKind']??'')=='group_join_request'){"
if seg.count(a)!=1:raise SystemExit("Inbox group event patch anchor drifted")
seg=seg.replace(a,b,1)
a="final chatId=(v['chatId']??v['groupId']??'').toString();"
b="final chatId=(v['chatId']??v['groupId']??v['sourceId']??v['belgeId']??'').toString();"
if seg.count(a)!=1:raise SystemExit("Inbox join-request reference anchor drifted")
seg=seg.replace(a,b,1)
a="final memberId=(v['fromUid']??v['senderUid']??'').toString();"
b="final memberId=(v['fromUid']??v['senderUid']??v['senderId']??v['userId']??'').toString();"
if seg.count(a)!=1:raise SystemExit("Inbox sender identity anchor drifted")
seg=seg.replace(a,b,1)
s=s[:start]+seg+s[end:]
p.write_text(s,encoding="utf-8")
print("Build 409: resolved invite status reads eventKind on all inbox rows.")
