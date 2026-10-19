#!/usr/bin/env python3
"""Build536: verify the fully assembled Flutter call screen before compilation.

This MUST run after all Build395–527 source transformations AND the ordered
Build534–535 bundle in the same CI job. It does not use an in-memory fixture.
"""
from pathlib import Path
from collections import Counter

main = Path('app/lib/main.dart').read_text(encoding='utf-8')
helper = Path('app/lib/build534_explicit_group_rejoin.dart').read_text(encoding='utf-8')
exit_helper = Path('app/lib/build517_group_leave.dart').read_text(encoding='utf-8')
rules = Path('firestore.rules').read_text(encoding='utf-8')

required_parts = (
    "part 'build517_group_leave.dart';",
    "part 'build526_atomic_group_timeout.dart';",
    "part 'build527_group_join_transaction.dart';",
    "part 'build534_explicit_group_rejoin.dart';",
)
for part in required_parts:
    assert main.count(part) == 1, f'Missing/duplicated generated Flutter part: {part}'

assert main.count('// Build535: self-rejoin preflight before LiveKit token acquisition') == 1
assert main.count('  Future<void> baglan({bool yeniden=false})async{') == 1
assert main.count('class _NgelXAramaPageState') == 1
assert main.count('class GrupBilgiPage') == 1

call = main[main.index('class _NgelXAramaPageState'):
            main.index('class GrupBilgiPage')]
connect = call[call.index('  Future<void> baglan({bool yeniden=false})async{'):
               call.index('  lk.VideoTrack? _katilimciVideosu(')]

marks = (
    '// Build535: self-rejoin preflight before LiveKit token acquisition',
    'await ngelx534ConfirmAndRejoinGroupCall(',
    'rejoinApproved535=true;',
    'await _izinleriIste();',
    'final kaynak=',       # original token source stays unchanged
    'await r.connect(',
    'rtcConnected535=true;',
    '}catch(e){',
    'final discard=await showDialog<bool>(',
    'if(discard&&!bitiyor){',
    'await ngelx517LeaveGroupCall(',
)
locations = [connect.index(m) for m in marks]
assert locations == sorted(locations), 'User approval must precede token/connect; rollback must follow catch'

for item in (
    'bool rejoinBlocked535=false;',
    'if(rejoinApproved535&&!rtcConnected535&&mounted&&!bitiyor)',
    'if(yeniden&&!rejoinBlocked535&&',
    "if(call==null||call['callRoomName']!=widget.roomName||",
    "call['callExitedRoomName']==widget.roomName",
    "if(yeniden){",
    "rejoinBlocked535=true;",
    'cancelled:()=>bitiyor||!_alive444',
):
    assert item in connect, f'Build536 generated RTC guard missing: {item}'
assert connect.count('await ngelx534ConfirmAndRejoinGroupCall(') == 1
assert connect.count('await ngelx517LeaveGroupCall(') == 1
assert 'ngelx527RegisterGroupParticipant(' in call
assert 'ngelx527ConfirmGroupRemoteTrack(' in call
assert 'await ngelx517LeaveGroupCall(' in call

assert 'required bool userConfirmed' in helper
assert "FirebaseAuth.instance.currentUser?.uid != uid" in helper
assert "'callExitedUids':FieldValue.arrayRemove([uid])" in helper
assert "'callExitedUids':exits" in exit_helper
assert 'validGroupExplicitSelfRejoin()' in rules

print('Build536 ASSEMBLED FLUTTER PASS: old Build517/526/527 parts and new Build534 part coexist once')
print('Build536 ASSEMBLED FLUTTER PASS: real call UI gets consent before token and opt-in recovery after failed RTC')
print('Build536 RELEASE GATE: Flutter analyze / APK build still must pass; 3 physical Android devices pending')
