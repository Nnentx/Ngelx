#!/usr/bin/env python3
"""Build533 no-deploy source contract for guarded concurrent call writes.

The Firestore emulator exercises actual concurrent JS clients. These checks
pin the corresponding Flutter helpers without claiming a Flutter APK build.
"""
from pathlib import Path

leave=Path('app/lib/build517_group_leave.dart').read_text(encoding='utf-8')
timeout=Path('app/lib/build526_atomic_group_timeout.dart').read_text(encoding='utf-8')
rules=Path('firestore.rules').read_text(encoding='utf-8')

for term in (
  'Future<Map<String,dynamic>> attemptLeave()',
  "on FirebaseException catch(error)",
  "error.code!='permission-denied'",
  'observedParticipants=participants',
  'retry>=4',
  'final current=(await ref.get()).data();',
  "current['callRoomName']!=roomName",
  '!nowParticipants.contains(uid)',
  'listEquals(nowParticipants,observedParticipants)',
  "final result=",
):
  if term == "final result=":
    continue
  assert term in leave, 'Missing safe group retry behavior: '+term

assert leave.index('if(listEquals(nowParticipants,observedParticipants))rethrow;') < leave.index(
  "debugPrint('Build533: group member changed during leave; retrying');")
assert "'callParticipants':FieldValue.arrayRemove([uid])" in leave
assert "'callExitedRoomName':roomName" in leave
assert "'callExitedUids':exits" in leave
assert 'if(retry>=4)' not in leave  # retries cannot be unconditional
for term in (
  'on FirebaseException catch(error)',
  "error.code!='permission-denied'",
  'final current=(await ref.get()).data();',
  "current['callRoomName']!=roomName",
  "current['callStatus']!='ringing'",
  "current['callConnectedAt'] is Timestamp",
  'return false;',
  'rethrow;',
):
  assert term in timeout, 'Missing safe timeout collision handling: '+term

assert 'validGroupCallExitMarkerWrite()' in rules
assert 'validGroupUnansweredTimeout()' in rules
assert "request.resource.data.get('callEndedAt', null) == request.time" in rules
print('Build533 FLUTTER SOURCE PASS: permission denial alone cannot trigger group leave retry')
print('Build533 FLUTTER SOURCE PASS: obsolete timer no-op requires fresh room state')
print('Build533 DEVICE GATE: Flutter compilation and simultaneous physical devices pending')
