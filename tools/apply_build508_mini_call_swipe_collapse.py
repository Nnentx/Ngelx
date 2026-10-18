#!/usr/bin/env python3
"""Build508: swipe-down to collapse in-app mini call into a return-call chip.

Runs AFTER Build469's optional remote video thumbnail injection. Reuses the
existing background LiveKit room, signed-in UID guard and return-call route.
The call is never ended or disconnected by a swipe. No system overlay grant.
"""
from pathlib import Path

FILE=Path("app/lib/build445_inbox_model.dart")
START="class _Ngelx445CallOverlayState extends State<Ngelx445CallOverlay>{"
END="class Ngelx445InboxCallBanner extends StatelessWidget"
MARK="// Build508: swipe down hides card, never ends the call"

def once(source: str, old: str, new: str, label: str) -> str:
    count=source.count(old)
    if count!=1:
        raise RuntimeError(f"Build508 {label}: expected one anchor, got {count}")
    return source.replace(old,new,1)

def transform(source: str) -> str:
    if MARK in source:
        return source
    if "// Build469: Messenger-style live thumbnail in the EXISTING mini call" not in source:
        raise RuntimeError("Build508 must run after existing Build469 live thumbnail")

    start=source.index(START)
    stop=source.index(END,start)
    prefix,body,suffix=source[:start],source[start:stop],source[stop:]

    body=once(body,
      "  double? _left,_top;",
      """  double? _left,_top;
  // Build508: swipe down hides card, never ends the call.
  String? _collapsedRoom508;
  double _verticalDrag508=0;
  void _returnCall508(String roomName){
    if(mounted)setState(()=>_collapsedRoom508=null);
    ngelx445ReturnCall(roomName);
  }
  bool _hasLiveVideo508(lk.Room active){
    for(final p in active.remoteParticipants.values){
      if(p.videoTrackPublications.any((t)=>!t.muted&&t.track is lk.VideoTrack))return true;
    }
    return active.localParticipant?.videoTrackPublications
      .any((t)=>!t.muted&&t.track is lk.VideoTrack)??false;
  }
""",
      "collapse state and presence from published tracks")

    body=once(body,
      """    if(remote==null){
      return CircleAvatar(radius:26""",
      """    if(remote==null&&active.localParticipant!=null){
      for(final pub in active.localParticipant!.videoTrackPublications){
        if(!pub.muted&&pub.track is lk.VideoTrack){
          remote=pub.track as lk.VideoTrack;break;
        }
      }
    }
    if(remote==null){
      return CircleAvatar(radius:26""",
      "local self-video fallback when peer is voice-only")

    # A collapsed call must remain recoverable everywhere the in-app overlay
    # exists, so replacing it with SizedBox.shrink() would lose return access.
    anchor="""    final x=(_left??screen.width-128).clamp(8.0,(screen.width-120).clamp(8.0,double.infinity)).toDouble();"""
    chip="""    // A conscious downward swipe collapses only the floating card, never RTC.
    // Keep a visible and accessible return button in this same in-app Stack.
    if(_collapsedRoom508==name){
      return Positioned(right:12,bottom:padding.bottom+86,width:126,
        child:Material(color:Colors.transparent,child:Semantics(
          button:true,label:'Görüşmeye geri dön',
          child:Tooltip(message:'Görüşmeye dön',child:InkWell(
            borderRadius:BorderRadius.circular(28),
            onTap:()=>_returnCall508(name),
            child:Container(
              padding:const EdgeInsets.symmetric(horizontal:10,vertical:9),
              decoration:BoxDecoration(color:const Color(0xFF39206F),
                borderRadius:BorderRadius.circular(28),
                boxShadow:const [BoxShadow(color:Color(0x55000000),blurRadius:12)]),
              child:Row(mainAxisSize:MainAxisSize.min,children:[
                Icon(_hasLiveVideo508(room)?Icons.videocam_rounded:Icons.call_rounded,
                  size:20,color:Colors.white),
                const SizedBox(width:7),
                Expanded(child:Text(duration,maxLines:1,
                  overflow:TextOverflow.ellipsis,
                  style:const TextStyle(color:Colors.white,
                    fontSize:11,fontWeight:FontWeight.w700))),
              ]),
            ),
          )),
        )));
    }
"""
    body=once(body,anchor,chip+anchor,"always visible collapsed call chip")

    body=once(body,
      """      onPanUpdate:(delta)=>setState((){_left=x+delta.delta.dx;_top=y+delta.delta.dy;}),""",
      """      onPanStart:(_){_verticalDrag508=0;},
      onPanUpdate:(delta)=>setState((){
        _verticalDrag508+=delta.delta.dy;
        _left=x+delta.delta.dx;_top=y+delta.delta.dy;
      }),
      onPanEnd:(_){
        if(_verticalDrag508>=96&&mounted){
          setState(()=>_collapsedRoom508=name);
        }
        _verticalDrag508=0;
      },""",
      "downward swipe collapse threshold without destroying call")

    body=once(body,
      "onTap:()=>ngelx445ReturnCall(name)",
      "onTap:()=>_returnCall508(name)",
      "existing floating card still returns to full call")
    body=once(body,
      "if(detail.video)_ngelx469Preview(room,detail.photo)",
      "if(detail.video||_hasLiveVideo508(room))_ngelx469Preview(room,detail.photo)",
      "voice-to-video also shows a real floating preview")

    for preserved in (
      "onEnd:()=>ngelx445EndBackground(name)",
      "FirebaseAuth.instance.currentUser?.uid!=detail.uid",
      "final room=_ngelxArkaPlanAramaOdalari[name];",
      "onMicrophone:()async{",
      "onSpeaker:()async{",
      "ngelx445ReturnCall(roomName)",
      "_ngelxArkaPlanAramaOdalari.isNotEmpty",
      "onPanEnd:(_){",
    ):
        if preserved not in body:
            raise RuntimeError("Build508 protected call contract missing: "+preserved)

    return prefix+body+suffix

if __name__=="__main__":
    original=FILE.read_text(encoding="utf-8")
    revised=transform(original)
    if revised!=original:
        FILE.write_text(revised,encoding="utf-8")
    print("Build508 in-app mini call: video/audio draggable; swipe-down collapses to return chip, no hang-up")
