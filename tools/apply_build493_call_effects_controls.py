#!/usr/bin/env python3
"""Build493 QA: video-call effects in ⋮ menu and tap-to-hide UI overlays.

Only in _NgelXAramaPageState, preserves call controls, audio-only layout,
room, participant tiles, outgoing/incoming call and system back/minimization.
"""
from pathlib import Path
FILE=Path("app/lib/main.dart")
MARK="// Build493: tap video to toggle call overlays"

METHOD=r"""
  // Build493: tap video to toggle call overlays.
  bool _videoCallControlsVisible493=true;
  void _toggleVideoCallControls493(){
    if(widget.goruntulu&&bitisDurumu==null&&hata==null&&mounted){
      setState(()=>_videoCallControlsVisible493=!_videoCallControlsVisible493);
    }
  }

  Widget _videoEffectMenu493()=>Align(
    alignment:Alignment.centerRight,
    child:PopupMenuButton<String>(
      tooltip:'Görüntülü arama efektleri',
      icon:const Icon(Icons.more_vert_rounded,color:Colors.white),
      color:const Color(0xFF211837),
      onSelected:(choice){
        switch(choice){
          case 'retouch':setState(()=>rotus=!rotus);break;
          case 'blur':setState(()=>bulanik=!bulanik);break;
          case 'effects':unawaited(efektSec());break;
        }
      },
      itemBuilder:(_)=>[
        CheckedPopupMenuItem(value:'retouch',checked:rotus,
          child:const Text('Rötuş',style:TextStyle(color:Colors.white))),
        CheckedPopupMenuItem(value:'blur',checked:bulanik,
          child:const Text('Bulanık',style:TextStyle(color:Colors.white))),
        const PopupMenuItem(value:'effects',
          child:Text('Efektler',style:TextStyle(color:Colors.white))),
      ],
    ),
  );

"""


def once(src,old,new,label):
    n=src.count(old)
    if n!=1:raise RuntimeError(f"Build493 {label}: expected 1 match, got {n}")
    return src.replace(old,new,1)


def transform(source):
    if MARK in source:return source
    start=source.index("class _NgelXAramaPageState")
    finish=source.index("class GrupBilgiPage",start)
    prefix,body,suffix=source[:start],source[start:finish],source[finish:]
    body=once(body,"  Widget _efektliVideo(lk.VideoTrack track)",
      METHOD+"  Widget _efektliVideo(lk.VideoTrack track)","video menu/state")
    # Group tiles: only tapping the video tile toggles UI, not menu buttons.
    begin=body.index("  Widget _katilimciKutusu(")
    end=body.index("  Widget _grupSesliKatilimci(",begin)
    sect=body[begin:end]
    sect=once(sect,
      """    return Container(
      clipBehavior:Clip.antiAlias,""",
      """    return GestureDetector(
      behavior:HitTestBehavior.translucent,
      onTap:_toggleVideoCallControls493,
      child:Container(
      clipBehavior:Clip.antiAlias,""",
      "group video tile tap")
    sect=once(sect,"""      ]),
    );
  }""","""      ]),
      ),
    );
  }""","group tile gesture close")
    sect=once(sect,
      """        Positioned(
          left:10,right:10,bottom:10,""",
      """        if(_videoCallControlsVisible493)Positioned(
          left:10,right:10,bottom:10,""",
      "group tile title hide")
    body=body[:begin]+sect+body[end:]
    # Hide video-call group title, preserve audio-only header.
    begin=body.index("    final sutun=katilimcilar.length<=1?1:2;")
    end=body.index("  Widget _videoAlani(){",begin)
    sect=body[begin:end]
    sect=once(sect,
      """    return Expanded(child:Column(children:[
      Padding(""",
      """    return Expanded(child:Column(children:[
      if(_videoCallControlsVisible493)Padding(""",
      "group video heading hide")
    body=body[:begin]+sect+body[end:]
    # Private video surface remains tappable while the overlays are hidden.
    begin=body.index("  Widget _videoAlani(){")
    end=body.index("  Widget _sesliAlani()",begin)
    sect=body[begin:end]
    sect=once(sect,
      "      Positioned.fill(child:Container(",
      """      Positioned.fill(child:GestureDetector(
        behavior:HitTestBehavior.opaque,
        onTap:_toggleVideoCallControls493,
        child:Container(""",
      "video touch layer")
    sect=once(sect,
      """        ])),
      )),
      Positioned(top:18,left:20,child:""",
      """        ])),
      ))),
      if(_videoCallControlsVisible493)Positioned(top:18,left:20,child:""",
      "video surface close and settings toggle")
    sect=once(sect,
      """      Positioned(left:30,right:30,bottom:20,child:Container(""",
      """      if(_videoCallControlsVisible493)Positioned(left:30,right:30,bottom:20,child:Container(""",
      "video text hide")
    body=body[:begin]+sect+body[end:]
    # Both bottom control rows hide only during video call; voice-only unchanged.
    bottom=body.index("  @override Widget build(BuildContext context)=>PopScope(")
    tail=body[bottom:]
    old="""          if(bitisDurumu==null&&hata==null&&widget.goruntulu)Padding(
            padding:const EdgeInsets.fromLTRB(12,9,12,4),
            child:Wrap(spacing:8,runSpacing:8,alignment:WrapAlignment.center,children:[
              _efektChip('✨ Rötuş',rotus,(v)=>setState(()=>rotus=v)),
              _efektChip('◌ Bulanık',bulanik,(v)=>setState(()=>bulanik=v)),
              ActionChip(label:const Text('☺ Efektler'),onPressed:efektSec,backgroundColor:Colors.white10,side:BorderSide(color:Colors.white.withValues(alpha:.10)),labelStyle:const TextStyle(color:Colors.white,fontWeight:FontWeight.w700)),
            ]),
          ),"""
    new="""          if(bitisDurumu==null&&hata==null&&widget.goruntulu&&_videoCallControlsVisible493)
            _videoEffectMenu493(),"""
    tail=once(tail,old,new,"effect menu replacement")
    first="          if(bitisDurumu==null&&hata==null)Padding("
    if tail.count(first)!=2:raise RuntimeError("Build493 requires bottom control and hangup rows")
    tail=tail.replace(first,"          if(bitisDurumu==null&&hata==null&&(!widget.goruntulu||_videoCallControlsVisible493))Padding(")
    body=body[:bottom]+tail
    for control in ("_aramaKontrol(", "grupAramasinaKisiDavetEt", "kameraDegistir",
                    "mikrofonDegistir", "hoparlorDegistir", "onTap:()=>bitir()",
                    "_aramaEkraniniKucult()"):
        if control not in body:raise RuntimeError("Build493 preserved call control missing: "+control)
    return prefix+body+suffix


if __name__=="__main__":
    original=FILE.read_text(encoding="utf-8")
    updated=transform(original)
    if updated!=original:FILE.write_text(updated,encoding="utf-8")
    print("Build493: video overlay on tap, effects in three-dot menu, voice-only preserved")
