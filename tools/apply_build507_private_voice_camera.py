#!/usr/bin/env python3
"""Build507 QA: allow PRIVATE voice calls to opt into camera, without a new call.

Build506 corrected the group grid. User supplied a separate Build505 screenshot
of an active one-to-one voice call with only mic/speaker/hang-up controls.
Private voice calls also need an independently controlled camera and a video
layout driven by an actual LiveKit track, not the initial call type.
"""
from pathlib import Path

FILE=Path("app/lib/main.dart")
MARK="// Build507: explicit private voice-call camera opt-in"

METHOD=r"""
  // Build507: explicit private voice-call camera opt-in; never enable the peer.
  bool _privateVoiceCameraOn507=false;
  bool _privateVoiceCameraBusy507=false;
  Future<void> _togglePrivateVoiceCamera507()async{
    final local=oda?.localParticipant;
    if(grupAramasi||widget.goruntulu||bitiyor||kucultuluyor||
       _privateVoiceCameraBusy507||local==null)return;
    final turnOn=!_privateVoiceCameraOn507;
    if(mounted)setState(()=>_privateVoiceCameraBusy507=true);
    try{
      if(turnOn){
        final permission=await Permission.camera.request();
        if(!permission.isGranted){
          if(mounted)ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content:Text('Görüntüyü açmak için kamera izni gerekli. Sesli görüşme devam ediyor.')));
          return;
        }
      }
      if(!mounted||bitiyor||!identical(oda?.localParticipant,local))return;
      await local.setCameraEnabled(turnOn,
        cameraCaptureOptions:const lk.CameraCaptureOptions(
          params:lk.VideoParametersPresets.h360_169,
          maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      final published=local.videoTrackPublications.any(
        (p)=>!p.muted&&p.track is lk.VideoTrack);
      if(turnOn&&(!local.isCameraEnabled()||!published)){
        try{await local.setCameraEnabled(false);}catch(_){}
        throw StateError('camera_not_published');
      }
      if(!turnOn&&local.isCameraEnabled()){
        throw StateError('camera_not_stopped');
      }
      if(mounted&&identical(oda?.localParticipant,local)){
        setState(()=>_privateVoiceCameraOn507=turnOn);
      }
    }catch(_){
      if(mounted&&identical(oda?.localParticipant,local)){
        setState(()=>_privateVoiceCameraOn507=local.isCameraEnabled()&&
          local.videoTrackPublications.any((p)=>!p.muted&&p.track is lk.VideoTrack));
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Kamera değiştirilemedi. Sesli görüşme devam ediyor.')));
      }
    }finally{
      if(mounted)setState(()=>_privateVoiceCameraBusy507=false);
    }
  }

"""

def once(s: str, old: str, new: str, why: str) -> str:
    count=s.count(old)
    if count!=1:
        raise RuntimeError(f"Build507 {why}: expected one anchor, got {count}")
    return s.replace(old,new,1)

def transform(source: str) -> str:
    if MARK in source:
        return source
    start=source.index("class _NgelXAramaPageState")
    stop=source.index("class GrupBilgiPage",start)
    head,body,foot=source[:start],source[start:stop],source[stop:]

    body=once(body,"  Future<void> kameraDegistir()async{",
      METHOD+"  Future<void> kameraDegistir()async{","private camera opt-in")

    # Restore only a camera this user had chosen to publish in this session.
    anchor="""      kamera=widget.goruntulu&&(ngelx446Calls._calls[widget.roomName]?.restoreCamera==true||arkaPlan.room.localParticipant?.isCameraEnabled()==true);"""
    body=once(body,anchor,anchor+"""
      if(!widget.goruntulu&&!grupAramasi){
        _privateVoiceCameraOn507=
          ngelx446Calls._calls[widget.roomName]?.restoreCamera==true||
          arkaPlan.room.localParticipant?.isCameraEnabled()==true;
      }""","restore opted-in camera after minimized call")

    # A network reconnect should preserve explicit private call camera choice.
    attach="cameraWanted:widget.goruntulu&&kamera,route:ModalRoute.of(context)"
    body=once(body,attach,
      "cameraWanted:(widget.goruntulu&&kamera)||(!grupAramasi&&_privateVoiceCameraOn507),route:ModalRoute.of(context)",
      "camera intent across reconnection")
    old="""      if(widget.goruntulu)await yerel.setCameraEnabled(kamera&&WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));"""
    new="""      if(widget.goruntulu||(!grupAramasi&&_privateVoiceCameraOn507)){
        await yerel.setCameraEnabled(
          (widget.goruntulu?kamera:_privateVoiceCameraOn507)&&
          WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed,
          cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      }"""
    body=once(body,old,new,"camera publishing on session reconnect")

    # Real private-call video layout also responds to remote-only tracks. This
    # does not force video on the peer, change the call type or replace the room.
    body=once(body,
      "          else if(widget.goruntulu)_videoAlani()",
      "          else if(widget.goruntulu||_privateVoiceCameraOn507||_uzakVideo!=null)_videoAlani()",
      "private video presentation")
    body=once(body,
      ":'Görüntülü arama • '+_aramaSureYazi()",
      ":(widget.goruntulu?'Görüntülü arama • ':'Sesli arama • ')+_aramaSureYazi()",
      "private call status remains voice originated")

    # Build494 already inserted a group-only action in the same controls wrap.
    control="""              _aramaKontrol(mikrofon?Icons.mic_rounded:Icons.mic_off_rounded,'Mikrofon',mikrofonDegistir,mikrofon),"""
    new_control="""              if(!grupAramasi&&!widget.goruntulu)_aramaKontrol(
                _privateVoiceCameraOn507?Icons.videocam_off_rounded:Icons.videocam_rounded,
                _privateVoiceCameraOn507?'Görüntüyü kapat':'Görüntüyü aç',
                _togglePrivateVoiceCamera507,_privateVoiceCameraOn507),
"""+control
    body=once(body,control,new_control,"private camera button near microphone")

    for preserved in (
      "if(grupAramasi&&!widget.goruntulu)_aramaKontrol(",
      "_toggleVoiceGroupVideo494",
      "Future<void> mikrofonDegistir()",
      "Future<void> hoparlorDegistir()",
      "Future<void> _aramaEkraniniKucult()",
      "lk.VideoTrack? get _uzakVideo",
      "lk.VideoTrack? get _yerelVideo",
      "if(widget.goruntulu)_aramaKontrol(kamera?",
      "_ngelx465HangupControl()",
    ):
        if preserved not in body:
            raise RuntimeError(f"Build507 preserved behavior missing: {preserved}")

    return head+body+foot

if __name__=="__main__":
    original=FILE.read_text(encoding="utf-8")
    modified=transform(original)
    if modified!=original:
        FILE.write_text(modified,encoding="utf-8")
    print("Build507 private 1:1 voice call camera on/off, live preview, and same-room audio preserved")
