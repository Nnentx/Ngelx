#!/usr/bin/env python3
"""Build535: verify consent preflight against real repository call-screen text.

app/lib/main.dart contains a historical large source; tests insert *fixture*
sentinels for the preceding Build527/534 transformations in memory only.
No call site is claimed compiled without the complete generated build.
"""
from pathlib import Path
import importlib.util

path=Path('tools/apply_build535_consented_group_rejoin.py')
spec=importlib.util.spec_from_file_location('build535',path)
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

base=Path('app/lib/main.dart').read_text(encoding='utf-8')
assert base.count('class _NgelXAramaPageState')==1, 'real call screen missing'
assert base.count('class GrupBilgiPage')==1, 'chat call boundary missing'
assert base.count('  Future<void> baglan({bool yeniden=false})async{')==1
assert base.count('      await _izinleriIste();')>=1

# The preceding scripts add these two methods. Use an in-memory representative
# so Build535's exact call-site anchors are exercised on real original source.
fixture=("part 'build534_explicit_group_rejoin.dart';\n"+
    base.replace('  Future<void> baglan({bool yeniden=false})async{',
    "  void _confirmGroupExit517(){}\n"
    "  void _build527TestOnly(){ngelx527RegisterGroupParticipant();}\n"
    "  Future<void> baglan({bool yeniden=false})async{",1))
patched=patch.transform(fixture)
assert patch.transform(patched)==patched, 'repeat patch must be idempotent'
bundle_spec=importlib.util.spec_from_file_location(
    'build535_bundle','tools/apply_build535_rejoin_bundle.py')
assert bundle_spec and bundle_spec.loader
bundle=importlib.util.module_from_spec(bundle_spec)
bundle_spec.loader.exec_module(bundle)
bundle_fixture=fixture.replace(
    "part 'build534_explicit_group_rejoin.dart';",
    "part 'build527_group_join_transaction.dart';",1)
bundle_output=bundle.transform(bundle_fixture)
assert bundle_output.count(patch.PART)==1
assert bundle_output.count(patch.MARK)==1
assert bundle.transform(bundle_output)==bundle_output
assert bundle_output[bundle_output.index(patch.CALL_START):] == patched[
    patched.index(patch.CALL_START):], 'bundle changed the actual call-screen patch'

assert patched.count(patch.MARK)==1
call=patched[patched.index(patch.CALL_START):patched.index(patch.CALL_END)]
begin=call.index('  Future<void> baglan({bool yeniden=false})async{')
end=call.index('  lk.VideoTrack? _katilimciVideosu(',begin)
connect=call[begin:end]

for phrase in (
  'if(grupAramasi){',
  "call['callRoomName']!=widget.roomName",
  "call['callExitedRoomName']==widget.roomName",
  "List<String>.from(call['callExitedUids']",
  'if(yeniden)throw StateError(',
  'await ngelx534ConfirmAndRejoinGroupCall(',
  'cancelled:()=>bitiyor||!_alive444',
  "hata='Yeniden katılım iptal edildi veya izin verilmedi.'",
  'bool rejoinApproved535=false;',
  'bool rtcConnected535=false;',
  'rtcConnected535=true;',
  'if(rejoinApproved535&&!rtcConnected535&&mounted&&!bitiyor)',
  'final discard=await showDialog<bool>(',
  'if(discard&&!bitiyor){',
  'await ngelx517LeaveGroupCall(',
):
    assert phrase in connect, 'missing guarded call screen step: '+phrase

pre=connect.index(patch.MARK)
permissions=connect.index('await _izinleriIste();')
rtc=connect.index('await r.connect(')
setConnected=connect.index('rtcConnected535=true;')
approval=connect.index('rejoinApproved535=true;')
catch=connect.index('}catch(e){')
revert=connect.index('await ngelx517LeaveGroupCall(')
assert begin<pre<approval<permissions<rtc<setConnected<catch<revert
assert 'if(yeniden)throw StateError(' in connect[pre:approval]
assert 'if(discard&&!bitiyor)' in connect[catch:revert]
assert 'await ngelx517LeaveGroupCall(' not in connect[:catch]
assert "call['callStatus']" in connect[pre:permissions]
assert 'showDialog<bool>' not in connect[:pre]
assert 'if(accepted)' not in connect[:pre]
assert patch.PART in patched
try:
    patch.transform(base)
    raise AssertionError('Unassembled Build534 source must fail closed')
except RuntimeError:
    pass
try:
    patch.transform(fixture.replace('  lk.VideoTrack? _katilimciVideosu(',
        '  lk.VideoTrack? _videoChanged('))
    raise AssertionError('Changed call screen boundary must fail closed')
except (RuntimeError,ValueError):
    pass

# Helper stays the exclusive self-rejoin writer; mere remote media
# callbacks continue to use Build527's guarded transaction.
join=Path('app/lib/build527_group_join_transaction.dart').read_text()
helper=Path('app/lib/build534_explicit_group_rejoin.dart').read_text()
assert 'ngelx535' not in join and 'ngelx534ExplicitRejoinGroupCall(' not in join
assert 'required bool userConfirmed' in helper
assert 'showDialog<bool>' in helper
print('Build535 SOURCE PASS: actual call-screen anchor supports tap-only consent before token request')
print('Build535 SOURCE PASS: reconnect does not auto-consent; post-failure exit is expressly user-approved')
print('Build535 DEVICE GATE: complete generated Flutter compilation, RTC and 3-phone QA pending')
