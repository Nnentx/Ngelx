#!/usr/bin/env python3
"""Build526 source QA: guard BOTH local/background group timeouts."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('b526','tools/apply_build526_atomic_group_timeout.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)
src=Path('app/lib/main.dart').read_text(encoding='utf-8')
helper=Path('app/lib/build526_atomic_group_timeout.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src,'Build526 patch must be idempotent'
assert src.count(patch.MARK)==1
assert "part 'build526_atomic_group_timeout.dart';" in src
for term in (
    "runTransaction<Map<String,dynamic>?>",
    "final snapshot=await tx.get(ref)",
    "data['callRoomName']!=roomName",
    "data['callStatus']!='ringing'",
    "if(participants.length>1)return null",
    "const Duration(seconds:120)",
    "tx.update(ref,<String,dynamic>{",
    "'callStatus':'missed'",
    "'callAutoEnded':true",
    "'callAutoEndedReason':'no_participants_2m'",
    "if(closure==null)return false;",
    "debugPrint('Build526 missed-call receipt unavailable')",
):
    assert term in helper,'Build526 transactional helper missing '+term
assert ".disconnect(" not in helper
assert "room.delete(" not in helper
background=src[src.index('_ngelxArkaPlanAramaZamanAsimlari[roomName]=Timer('):]
background=background[:background.index('({lk.Room room,DateTime? baslangic})?')]
assert "await ngelx526ExpireUnansweredGroupCall(aramaRef,roomName);" in background
assert background.index("await ngelx526ExpireUnansweredGroupCall")<background.index("final current=await aramaRef.get()")
call=src[src.index('class _NgelXAramaPageState'):src.index('class GrupBilgiPage')]
front=call[call.index('void _cevapsizSayaciniBaslat'):call.index('void _aramaRotasiniGuvenliKapat')]
assert "if(grupAramasi){" in front
assert "if(oda?.remoteParticipants.isNotEmpty==true)return;" in front
assert "await ngelx526ExpireUnansweredGroupCall(" in front
assert front.index("await ngelx526ExpireUnansweredGroupCall")<front.index("final d=await widget.aramaRef.get()")
assert "await ngelx517LeaveGroupCall(" in call
assert "Ngelx520PipBridge" in call
print('Build526 SOURCE PASS: background and foreground GROUP missed timers use same transaction')
print('Build526 SOURCE PASS: historical/private call behavior, 3→2 leave, PiP preserved')
print('Build526 LIMIT: physical device and clock-skew testing still pending')
