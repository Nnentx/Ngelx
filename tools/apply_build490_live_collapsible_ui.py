#!/usr/bin/env python3
"""Build490 QA: independent collapsible host controls and livestream comments.

Applied after Build489 source generation; touches only _CanliYayinPageState,
retaining comment Firestore listeners, LiveKit, callbacks, safety dialogs and
the existing comment text input. Does not publish an APK or alter production.
"""
from pathlib import Path

FILE=Path("app/lib/live_broadcast_studio.dart")
MARKER="// Build490: independent live comment and host dock visibility"

METHOD=r"""
  // Build490: independent live comment and host dock visibility.
  bool _commentsHidden490=false;
  bool _hostDockOpen490=true;

  Widget _commentSection490(){
    return Align(alignment:Alignment.centerLeft,child:ConstrainedBox(
      constraints:BoxConstraints(maxWidth:math.min(340.0,MediaQuery.sizeOf(context).width-28)),
      child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
        Semantics(button:true,label:_commentsHidden490?'Yorumları göster':'Yorumları gizle',child:InkWell(
          onTap:()=>setState(()=>_commentsHidden490=!_commentsHidden490),
          borderRadius:BorderRadius.circular(17),
          child:Container(
            padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
            decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(17)),
            child:Row(mainAxisSize:MainAxisSize.min,children:[
              Icon(_commentsHidden490?Icons.chat_bubble_outline_rounded:Icons.keyboard_arrow_down_rounded,
                size:17,color:Colors.white),
              const SizedBox(width:6),
              Text(_commentsHidden490?'Yorumlar gizli · Dokun aç':'Yorumları gizle',
                style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w700)),
            ]),
          ),
        )),
        // Offstage deliberately keeps _yorumPaneli's state and live streams
        // connected so comments continue arriving while the user hides them.
        Offstage(offstage:_commentsHidden490,child:_yorumPaneli()),
      ]),
    ));
  }

  Widget _hostDockHandle490(){
    if(!widget.yayinSahibi||yayinBitti||kapatildi)return const SizedBox.shrink();
    return Semantics(button:true,label:_hostDockOpen490?'Yayın kontrollerini gizle':'Yayın kontrollerini göster',
      child:GestureDetector(
        behavior:HitTestBehavior.opaque,
        onTap:()=>setState(()=>_hostDockOpen490=!_hostDockOpen490),
        onVerticalDragEnd:(details){
          final speed=details.primaryVelocity??0;
          if(speed.abs()<90)return;
          if(mounted)setState(()=>_hostDockOpen490=speed<0);
        },
        child:ConstrainedBox(
          constraints:const BoxConstraints(minHeight:44),
          child:Center(child:Container(
            padding:const EdgeInsets.symmetric(horizontal:14,vertical:7),
            decoration:BoxDecoration(color:Colors.black87,borderRadius:BorderRadius.circular(22)),
            child:Row(mainAxisSize:MainAxisSize.min,children:[
              Icon(_hostDockOpen490?Icons.keyboard_arrow_down_rounded:Icons.keyboard_arrow_up_rounded,
                color:Colors.white,size:19),
              const SizedBox(width:5),
              Text(_hostDockOpen490?'Kontrolleri gizle':'Kontroller · Yukarı çek',
                style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w700)),
            ]),
          )),
        ),
      ),
    );
  }
"""


def replace_once(s,old,new,label):
    n=s.count(old)
    if n!=1: raise RuntimeError(f"Build490 {label}: expected 1 match, got {n}")
    return s.replace(old,new,1)


def transform(source):
    if MARKER in source:return source
    start=source.index("class _CanliYayinPageState")
    head,body=source[:start],source[start:]
    body=replace_once(body,"  Widget _yorumPaneli(){",METHOD+"\n  Widget _yorumPaneli(){","methods")
    body=replace_once(body,
      "              Align(alignment:Alignment.centerLeft,child:_yorumPaneli()),",
      "              _commentSection490(),",
      "comments view replacement")
    # Build453 approved bottom strip. Keep its LiveKit/PK/share/comment callbacks
    # and all viewer actions unchanged. Only the host control group collapses.
    a=body.index("              Container(key:const ValueKey('live-controls-panel453')")
    b=body.index("\n            ]),\n          )),",a)
    original=body[a:b]
    oldStart="                if(MediaQuery.of(context).viewInsets.bottom==0)...[\n                  const SizedBox(height:12),\n                  if(widget.yayinSahibi)Row("
    newStart="""                if(MediaQuery.of(context).viewInsets.bottom==0)...[
                  if(widget.yayinSahibi)_hostDockHandle490(),
                  AnimatedSize(
                    duration:const Duration(milliseconds:180),
                    alignment:Alignment.topCenter,
                    child:(!widget.yayinSahibi||_hostDockOpen490)
                      ?Column(mainAxisSize:MainAxisSize.min,children:[
                          const SizedBox(height:12),
                          if(widget.yayinSahibi)Row("""
    if original.count(oldStart)!=1:raise RuntimeError("Build490 host dock contents changed unexpectedly")
    original=original.replace(oldStart,newStart,1)
    tail="""                  else const Text('Konuk olmak için yayıncıya istek gönder',style:TextStyle(color:Colors.black45,fontSize:11)),
                ],
              ]))),
"""
    amended="""                  else const Text('Konuk olmak için yayıncıya istek gönder',style:TextStyle(color:Colors.black45,fontSize:11)),
                      ])
                      :const SizedBox.shrink(),
                  ),
                ],
              ]))),
"""
    if original.count(tail)!=1:raise RuntimeError("Build490 dock closing structure changed unexpectedly")
    original=original.replace(tail,amended,1)
    body=body[:a]+original+body[b:]
    for must in (
        "_guestRail488()", "_hearts453", "_kalpDegistir()",
        "_guestControl453(false)", "_guestControl453(true)",
        "NgelXCanliPkButonu", "_yayinMikrofonunuDegistir",
        "_yayinKamerasiniAcKapat", "_yorumGirisAlani()",
        "Yayını bitir", "_hostGuestAction489"):
        if must not in body:raise RuntimeError("Build490 missing preserved feature: "+must)
    return head+body


if __name__=="__main__":
    original=FILE.read_text(encoding="utf-8")
    modified=transform(original)
    if modified!=original:FILE.write_text(modified,encoding="utf-8")
    print("Build490: independent comments/dock, drag and tap controls, no LiveKit lifecycle changes")
