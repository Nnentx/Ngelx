#!/usr/bin/env python3
"""Build494 QA: camera toggle inside an existing group voice call.

No new room, new invitation, microphone reset or callVideo document rewrite.
Peer video tracks render only when published. Permission denial leaves audio.
"""
from pathlib import Path
FILE=Path("app/lib/main.dart")
MARK="// Build494: optional video in the same group voice call"

METHOD=r"""
  // Build494: optional video in the same group voice call.
  bool _voiceGroupVideoOn494=false;
  Future<void> _toggleVoiceGroupVideo494()async{
    if(!grupAramasi||widget.goruntulu||bitiyor||oda?.localParticipant==null)return;
    final enabled=!_voiceGroupVideoOn494;
    if(enabled){
      final permission=await Permission.camera.request();
      if(!permission.isGranted){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('Görüntüyü açmak için kamera izni gerekli. Sesli görüşme devam ediyor.')));
        return;
      }
    }
    try{
      await oda!.localParticipant!.setCameraEnabled(enabled,
        cameraCaptureOptions:const lk.CameraCaptureOptions(
          params:lk.VideoParametersPresets.h360_169,
          maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      if(mounted)setState(()=>_voiceGroupVideoOn494=enabled);
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Kamera değiştirilemedi. Sesli görüşme devam ediyor.')));
    }
  }

"""


def once(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f"Build494 {label}: expected 1, got {n}")
    return s.replace(old,new,1)


def transform(source):
    if MARK in source:return source
    start=source.index("class _NgelXAramaPageState")
    stop=source.index("class GrupBilgiPage",start)
    head,body,foot=source[:start],source[start:stop],source[stop:]
    body=once(body,"  Widget _grupSesliKatilimci(lk.Participant p,",
      METHOD+"  Widget _grupSesliKatilimci(lk.Participant p,",
      "same-room camera toggle")
    # Audio-only group call participant with a published video gets a thumbnail;
    # others retain the microphone/avatar card. Never auto-open someone else's camera.
    # Build469 rewrites the speaker animation state and adds a host-scoped
    # participant popup. Keep those changes; inject video preview only before
    # the generated voice/avatar return widget.
    voice_start=body.index("  Widget _grupSesliKatilimci(lk.Participant p,{bool yerel=false}){")
    voice_end=body.index("  Widget _grupAramaAlani(){",voice_start)
    voice=body[voice_start:voice_end]
    # Build465/469 may wrap the original voice tile in different widgets.
    # The participant name still uniquely precedes every original tile.
    avatar_return="    final ad=_katilimciAdi(p,yerel:yerel);"
    if voice.count(avatar_return)!=1:raise RuntimeError("Build494 voice participant identity changed")
    video_preview="""    final track=_katilimciVideosu(p);
    if(track!=null){
      return SizedBox(width:126,child:Column(mainAxisSize:MainAxisSize.min,children:[
        Stack(children:[
          ClipRRect(borderRadius:BorderRadius.circular(16),
            child:SizedBox(width:126,height:148,
              child:lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover))),
          Positioned(right:0,top:0,child:_ngelx469ParticipantMenu(p,yerel:yerel)),
        ]),
        const SizedBox(height:7),
        Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,
          style:const TextStyle(color:Colors.white,fontSize:12.5,fontWeight:FontWeight.w800)),
      ]));
    }
"""
    voice=voice.replace(avatar_return,avatar_return+"\n"+video_preview,1)
    body=body[:voice_start]+voice+body[voice_end:]
    # Build465/469 can rewrite the entire voice group participant layout.
    # Put camera control with the existing call mic/speaker/invite buttons,
    # where it remains visible only in voice GROUP calls.
    row_control="""              _aramaKontrol(mikrofon?Icons.mic_rounded:Icons.mic_off_rounded,'Mikrofon',mikrofonDegistir,mikrofon),"""
    row_new="""              if(grupAramasi&&!widget.goruntulu)_aramaKontrol(
                _voiceGroupVideoOn494?Icons.videocam_off_rounded:Icons.videocam_rounded,
                _voiceGroupVideoOn494?'Görüntüyü kapat':'Görüntüyü aç',
                _toggleVoiceGroupVideo494,_voiceGroupVideoOn494),
              _aramaKontrol(mikrofon?Icons.mic_rounded:Icons.mic_off_rounded,'Mikrofon',mikrofonDegistir,mikrofon),"""
    body=once(body,row_control,row_new,"group voice control in existing actions row")
    # Earlier call-routing fixes add state updates between restoring the
    # background room and clearing the loading indicator. Do not remove them.
    import re
    restore=r"(?m)^(\s*)oda=arkaPlan\.room;"
    if len(re.findall(restore,body))!=1:
        raise RuntimeError("Build494 expected one minimized call restoration")
    body=re.sub(restore,lambda m:m.group(0)+"""
      if(!widget.goruntulu&&grupAramasi){
        _voiceGroupVideoOn494=arkaPlan.room.localParticipant?.videoTrackPublications
          .any((p)=>!p.muted&&p.track is lk.VideoTrack)??false;
      }""",body,count=1)
    # Room reconnection remains owned by the existing audio-call lifecycle;
    # only a deliberate camera tap changes video publishing in this QA step.
    for token in ("mikrofonDegistir","hoparlorDegistir",
                  "grupAramasinaKisiDavetEt","_aramaEkraniniKucult",
                  "Widget _videoAlani()"):
        if token not in body:raise RuntimeError("Build494 missing preserved call feature "+token)
    return head+body+foot


if __name__=="__main__":
    old=FILE.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding="utf-8")
    print("Build494 group voice camera may publish on same LiveKit room, denial keeps audio")
