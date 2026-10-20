"""Apply only after the verified Build545 source regeneration."""
from pathlib import Path
TAG='// Build546 live guest continuity'
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError('Build546 anchor mismatch '+a[:100]+': '+str(s.count(a)))
 return s.replace(a,b,1)
def studio(s):
 if TAG in s:return s
 s=once(s,'    _liveServer453=widget.serverUrl;_liveToken453=widget.participantToken;','    _liveServer453=widget.serverUrl;_liveToken453=widget.participantToken;\n    _liveRoom546=widget.oda.name??\"\";')
 start=s.index('  Future<void> _guestSync448(bool accepted)async{');end=s.index('\n  void _yenile()',start)
 s=s[:start]+Path('tools/build546_guest_session.dart').read_text()+s[end:]
 s=once(s,'  Widget _liveBottom540()=>Column(mainAxisSize:MainAxisSize.min,children:[','  Widget _liveBottom540()=>Column(mainAxisSize:MainAxisSize.min,children:[\n    _guestStatus546(),')
 s=once(s,'    _guestSub448?.cancel();','    _guestRetry546?.cancel();\n    _guestSub448?.cancel();')
 old="""            _guestWanted448=accepted;_guestActive448=accepted;
            await widget.oda.localParticipant?.setMicrophoneEnabled(accepted&&!_guestAudioMuted489);
            await widget.oda.localParticipant?.setCameraEnabled(accepted,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0));"""
 s=once(s,old,"""            _guestActive448=false;
            await _guestSync448(accepted);""")
 s=once(s,"await Future<void>.delayed(Duration(seconds:deneme==1?1:deneme==2?2:4));","await Future<void>.delayed(Duration(seconds:deneme==1?0:deneme==2?1:3));")
 s=once(s,"ownerUid:widget.ownerId,host:host,viewerUids:","ownerUid:widget.ownerId,host:host,cameraPreferred:_guestCameraWanted546,onCameraPreference:(value){if(mounted)setState(()=>_guestCameraWanted546=value);},viewerUids:")
 # Only the recovery loop refreshes tokens; ordinary viewer/guest connection stays intact.
 anchor='        await widget.oda.connect(_liveServer453,_liveToken453);'
 s=once(s,anchor,"""        final recoveryUid546=FirebaseAuth.instance.currentUser?.uid;
        if(recoveryUid546==null)break;
        final recoveryToken546=await NgelXLiveKitSource441().fetch(lk.TokenRequestOptions(roomName:_liveRoom546,participantIdentity:recoveryUid546));
        if(kapatildi||yayinBitti||FirebaseAuth.instance.currentUser?.uid!=recoveryUid546)break;
        _liveServer453=recoveryToken546.serverUrl;_liveToken453=recoveryToken546.participantToken;
        await widget.oda.connect(_liveServer453,_liveToken453);""")
 return s+'\n'+TAG+'\n'
def main(s):
 if TAG in s:return s
 return once(s,"import 'build541_pk_policy.dart';","import 'build541_pk_policy.dart';\nimport 'build546_guest_policy.dart';")+'\n'+TAG+'\n'
if __name__=='__main__':
 for name,fn in [('app/lib/main.dart',main),('app/lib/live_broadcast_studio.dart',studio)]:
  p=Path(name);p.write_text(fn(p.read_text()))
 from build546_guest_controls import controls
 control=Path('app/lib/build448_live_guests.dart');control.write_text(controls(control.read_text()))
 Path('app/lib/build546_guest_policy.dart').write_text(Path('tools/build546_guest_policy.dart').read_text())
