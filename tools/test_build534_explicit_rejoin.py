#!/usr/bin/env python3
"""Build534 explicit rejoin source contract, independent of source assembly."""
from pathlib import Path
import importlib.util

p=Path('tools/apply_build534_explicit_rejoin.py')
spec=importlib.util.spec_from_file_location('build534',p)
module=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
example="part 'build527_group_join_transaction.dart';\nclass _Test{}"
assembled=module.transform(example)
assert assembled.count(module.PART)==1
assert module.transform(assembled)==assembled
try:
    module.transform('class _Test{}')
    raise AssertionError('Unassembled Flutter source accepted')
except RuntimeError:
    pass

helper=Path('app/lib/build534_explicit_group_rejoin.dart').read_text()
join=Path('app/lib/build527_group_join_transaction.dart').read_text()
rules=Path('firestore.rules').read_text()
policy=Path('server/livekit443/room-policy.mjs').read_text()
assert helper.startswith("part of 'main.dart';")
for term in (
  'ngelx534ExplicitRejoinGroupCall(',
  'ngelx534ConfirmAndRejoinGroupCall(',
  'required bool userConfirmed',
  'if (!userConfirmed',
  'FirebaseAuth.instance.currentUser?.uid != uid',
  'showDialog<bool>',
  "const Text('Yeniden katıl')",
  'return ngelx534ExplicitRejoinGroupCall(',
  'FirebaseFirestore.instance.runTransaction<bool>',
  "data['callStatus'] != 'active'",
  "data['callExitedRoomName'] != roomName",
  "kicked.contains(uid)",
  'cancelled?.call() == true',
  "'callExitedUids':FieldValue.arrayRemove([uid])",
  "'callParticipants':FieldValue.arrayUnion([uid])",
):
  assert term in helper, 'Missing approved self-rejoin behavior: '+term
assert 'ngelx534ExplicitRejoinGroupCall(' not in join
assert 'ngelx534ConfirmAndRejoinGroupCall(' not in join
assert 'validGroupExplicitSelfRejoin()' in rules
assert "&& resource.data.get('callStatus', '') == 'active'" in rules
assert "request.resource.data.get('callExitedUids', []) ==" in rules
assert "request.resource.data.get('callParticipants', []) ==" in rules
assert 'room.callExitedRoomName === currentRoom' in policy
assert 'list(room.callExitedUids).includes(uid)' in policy
assert 'removeParticipant(' not in helper and 'deleteRoom(' not in helper
print('Build534 SOURCE PASS: explicit user-confirmation, authenticated self-rejoin helper')
print('Build534 SOURCE PASS: no automatic RTC callback clears exit; generated part inclusion idempotent')
print('Build534 RELEASE GATE: UI button wiring, RTC connection failure rollback, Flutter compilation and physical devices still pending')
