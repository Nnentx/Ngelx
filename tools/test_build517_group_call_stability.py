#!/usr/bin/env python3
"""Build517 generated Flutter regression contract (not a two/three-phone test).
Runs after all older CI source transformations, including 493/494/506/507.
"""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('b517','tools/apply_build517_group_call_stability.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)
src=Path('app/lib/main.dart').read_text(encoding='utf-8')
helper=Path('app/lib/build517_group_leave.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src,'Build517 should be idempotent'
assert "part 'build517_group_leave.dart';" in src
call=src[src.index('class _NgelXAramaPageState'):src.index('class GrupBilgiPage')]
leave=call[call.index('  Future<void> bitir('):call.index('  @override void dispose()',call.index('  Future<void> bitir('))]
assert 'await ngelx517LeaveGroupCall(' in leave
assert 'baslatan==me||kalan.isEmpty' not in leave
assert 'if(grup&&me!=null)' in leave
assert "'callStatus':'ended'" not in leave[:leave.index("}else{\n          final participants=List<String>")], 'group branch must not end everyone'
for token in (
    'runTransaction<Map<String,dynamic>>',
    'await tx.get(ref)', 'tx.update(ref,',
    'participants.where((id)=>id!=uid).toSet()',
    "'callStatus':isLast?finalStatus:'active'",
    "'callParticipants':FieldValue.arrayRemove([uid])",
    "if(isLast)'callEndedAt':FieldValue.serverTimestamp()",
    "if (!participants.contains(uid))",
    "data['callRoomName']!=roomName",
    "result['kind']=='last'",
    "result['kind']=='stale'",
    "'systemAction':'call_leave'",
    "Build517 call receipt update denied or unavailable",
):
    assert token in helper, 'atomic leave missing '+token
for unsafe in ('room.disconnect(', 'deleteRoom(', 'DeleteRoom', 'remoteParticipant.disconnect'):
    assert unsafe not in helper, 'group leave must never disconnect a peer'
for token in (
    '_voiceGroupCameraBusy517', '_toggleVoiceGroupVideo494',
    'await Permission.camera.request()', 'local.isCameraEnabled()',
    'videoTrackPublications.any(', 'group_camera_track_not_published',
    '_voiceGroupVideoOn494=enable', 'if(!widget.goruntulu&&grupAramasi&&_voiceGroupVideoOn494)',
    'if((widget.goruntulu||grupAramasi)&&bitisDurumu==null&&hata==null&&mounted)',
    'if(_videoCallControlsVisible493)Padding(',
    'onTap:_toggleVideoCallControls493',
    'if(bitisDurumu==null&&hata==null&&(!grupAramasi&&!widget.goruntulu||_videoCallControlsVisible493))',
    '_confirmGroupExit517()',
    'Yalnız sen ayrılacaksın.',
    'width:48,height:48',
):
    assert token in call, 'group controls/media missing: '+token
assert 'width:58,height:58' not in call
assert "'Mikrofon',mikrofonDegistir" in call
assert 'grupAramasinaKisiDavetEt' in call
assert '_ngelx469ParticipantMenu' in call
assert "if(track!=null)" in call
assert "setCameraEnabled(true" in call
assert 'return Expanded(child:Column(children:[' in call
print('Build517 SOURCE PASS: group initiator/member departure is transaction-scoped; peers unaffected')
print('Build517 SOURCE PASS: published LiveKit track required; denied camera keeps voice')
print('Build517 SOURCE PASS: compact, confirm-exit and group voice/video tap-hide')
print('Build517 DEVICE GATE PENDING: 3 real Android phones, remote tracks, kick/rejoin, overlays')
