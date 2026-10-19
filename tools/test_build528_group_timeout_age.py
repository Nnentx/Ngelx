#!/usr/bin/env python3
"""Build528 validates the actual authored Dart expiry helper and integrates earlier patches."""
from pathlib import Path
helper=Path('app/lib/build526_atomic_group_timeout.dart').read_text(encoding='utf-8')
source=Path('app/lib/main.dart').read_text(encoding='utf-8')
for text in (
    "if(data['callConnectedAt'] is Timestamp)return null;",
    "if(createdAt is! Timestamp)return null;",
    "DateTime.now().toUtc().difference(createdAt.toDate().toUtc())",
    "const Duration(seconds:120)",
    "data['callRoomName']!=roomName",
    "data['callStatus']!='ringing'",
    "if(participants.length>1)return null",
    "'callAutoEndedReason':'no_participants_2m'",
):
    assert text in helper,'Build528 missing '+text
assert 'if(createdAt is Timestamp &&' not in helper
assert helper.index("if(data['callConnectedAt'] is Timestamp)return null;")<helper.index("tx.update(ref,")
assert helper.index("if(createdAt is! Timestamp)return null;")<helper.index("tx.update(ref,")
for token in (
    "part 'build526_atomic_group_timeout.dart';",
    "part 'build527_group_join_transaction.dart';",
    "ngelx526ExpireUnansweredGroupCall(",
    "ngelx527RegisterGroupParticipant(",
    "await ngelx517LeaveGroupCall(",
):
    assert token in source,'Build528 integrated group invariant missing '+token
print('Build528 SOURCE PASS: missing callCreatedAt or callConnectedAt blocks group missed timeout')
print('Build528 SOURCE PASS: current-room, >=120 sec, Build517/527 preservation')
