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
    avatar_return="    return SizedBox("
    if voice.count(avatar_return)!=1:raise RuntimeError("Build494 voice participant markup changed")
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
    voice=voice.replace(avatar_return,video_preview+avatar_return,1)
    body=body[:voice_start]+voice+body[voice_end:]
    a=body.index("  Widget _grupAramaAlani(){")
    b=body.index("  Widget _videoAlani(){",a)
    group=body[a:b]
    anchor="""        Expanded(child:Center(child:SingleChildScrollView("""
    new="""        Padding(padding:const EdgeInsets.fromLTRB(14,4,14,2),
          child:FilledButton.tonalIcon(
            onPressed:_toggleVoiceGroupVideo494,
            icon:Icon(_voiceGroupVideoOn494?Icons.videocam_off_rounded:Icons.videocam_rounded),
            label:Text(_voiceGroupVideoOn494?'Görüntüyü kapat':'Görüntüyü aç'),
          ),
        ),
        Expanded(child:Center(child:SingleChildScrollView("""
    group=once(group,anchor,new,"top camera control in voice group")
    body=body[:a]+group+body[b:]
    body=once(body,
      "      oda=arkaPlan.room;\n      baglaniyor=false;",
      """      oda=arkaPlan.room;
      if(!widget.goruntulu&&grupAramasi){
        _voiceGroupVideoOn494=arkaPlan.room.localParticipant?.videoTrackPublications
          .any((p)=>!p.muted&&p.track is lk.VideoTrack)??false;
      }
      baglaniyor=false;""",
      "restore camera state from minimized call")
    body=once(body,
      """      if(widget.goruntulu)await yerel.setCameraEnabled(true,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));""",
      """      if(widget.goruntulu)await yerel.setCameraEnabled(true,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      // Reconnect may restore the user's already-approved video choice.
      if(!widget.goruntulu&&grupAramasi&&_voiceGroupVideoOn494){
        if(await Permission.camera.isGranted){
          try{await yerel.setCameraEnabled(true,cameraCaptureOptions:const lk.CameraCaptureOptions(
            params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));}
          catch(_){_voiceGroupVideoOn494=false;}
        }else{_voiceGroupVideoOn494=false;}
      }""",
      "audio to video reconnect behavior")
    for token in ("await yerel.setMicrophoneEnabled(true)","hoparlorDegistir",
                  "grupAramasinaKisiDavetEt","_aramaEkraniniKucult",
                  "Widget _videoAlani()"):
        if token not in body:raise RuntimeError("Build494 missing preserved call feature "+token)
    return head+body+foot


if __name__=="__main__":
    old=FILE.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding="utf-8")
    print("Build494 group voice camera may publish on same LiveKit room, denial keeps audio")
