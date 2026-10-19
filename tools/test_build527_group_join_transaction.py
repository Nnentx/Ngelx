#!/usr/bin/env python3
"""Build527 read-only source assertions after integrated Flutter generation."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('b527','tools/apply_build527_group_join_transaction.py')
assert spec and spec.loader
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
src=Path('app/lib/main.dart').read_text(encoding='utf-8')
helper=Path('app/lib/build527_group_join_transaction.dart').read_text(encoding='utf-8')
assert p.transform(src)==src
assert src.count(p.MARK)==1
assert "part 'build527_group_join_transaction.dart';" in src
a=src.index('class _NgelXAramaPageState')
b=src.index('class GrupBilgiPage',a)
call=src[a:b]
for term in (
  'if(grupAramasi){\n          unawaited(ngelx527ConfirmGroupRemoteTrack(',
  'cancelled:()=>bitiyor||!_alive444||!identical(oda,r)',
  'final accepted=await ngelx527RegisterGroupParticipant(',
  'if(!accepted)throw StateError(',
  'if(aktif&&!grupAramasi)',
  'await ngelx517LeaveGroupCall(',
  'ngelx526ExpireUnansweredGroupCall(',
  'Ngelx520PipBridge.active',
):
    assert term in call,'Build527 missing call path: '+term
assert call.count('final accepted=await ngelx527RegisterGroupParticipant(')==1
assert call.count('unawaited(ngelx527ConfirmGroupRemoteTrack(')==1
for term in (
  'runTransaction<bool>',
  "data['callRoomName']!=roomName",
  "data['callStatus']",
  "members.contains(uid)",
  "kicks.contains(uid)",
  "moderationRoom==roomName",
  "if(cancelled?.call()==true)return false;",
  "tx.update(ref,<String,dynamic>{",
  "'callParticipants':FieldValue.arrayUnion([uid])",
  "'callStatus':status",
  "if(status=='active'&&data['callConnectedAt'] is! Timestamp)",
):
    assert term in helper,'Missing transaction safety '+term
assert helper.count("if(cancelled?.call()==true)return false;")==2
for forbidden in ('deleteRoom(','removeParticipant(','disconnect(','DevelopmentTokenSource('):
    assert forbidden not in helper,forbidden
print('Build527 SOURCE PASS: group audio/video joins and callback revalidate exact current room')
print('Build527 SOURCE PASS: private calls unaffected, Build517 leave + Build526 timers preserved')
print('Build527 DEVICE GATE: three-phone and LiveKit reconnect timing acceptance still required')
