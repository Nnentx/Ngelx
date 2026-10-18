#!/usr/bin/env python3
"""Build496 B4: tap-to-focus in the broadcaster's pre-live camera preview.

Does not modify LiveKit permissions, streaming codecs or camera resolution.
The native device may not support focus/exposure points; failures are quiet.
Run after prior live source steps in QA only.
"""
from pathlib import Path

FILE=Path("app/lib/live_broadcast_studio.dart")
MARK="// Build496: preview tap focus without changing stream resolution"

ADDITION=r"""
  // Build496: preview tap focus without changing stream resolution.
  Offset? _onizlemeOdak496;
  int _odakSirasi496=0;

  Future<void> _onizlemeOdakla496(Offset local,Size size)async{
    final c=onizleme;
    if(c==null||!c.value.isInitialized||onizlemeHazirlaniyor||
        baglaniyor||!kamera||size.width<=0||size.height<=0)return;
    final focus=Offset(
      (local.dx/size.width).clamp(0.0,1.0).toDouble(),
      (local.dy/size.height).clamp(0.0,1.0).toDouble());
    final number=++_odakSirasi496;
    try{
      await c.setFocusMode(FocusMode.auto);
      await c.setFocusPoint(focus);
    }catch(_){
      // Camera may lack user-selected autofocus; auto focus keeps working.
    }
    try{await c.setExposurePoint(focus);}catch(_){}
    if(!mounted||!identical(onizleme,c))return;
    setState(()=>_onizlemeOdak496=focus);
    await Future<void>.delayed(const Duration(milliseconds:850));
    if(mounted&&identical(onizleme,c)&&number==_odakSirasi496){
      setState(()=>_onizlemeOdak496=null);
    }
  }

"""


def once(s,old,new,label):
    count=s.count(old)
    if count!=1:raise RuntimeError(f"Build496 {label}: expected one match, got {count}")
    return s.replace(old,new,1)


def transform(source):
    if MARK in source:return source
    start=source.index("  Widget _kameraOnizlemesi()")
    end=source.index("  Future<void> _geriSayimCalistir()",start)
    a,b,c=source[:start],source[start:end],source[end:]
    a=once(a,
      "if (mounted) setState(() { onizlemeHazirlaniyor = true; kameraHatasi = null; });",
      "if (mounted) setState(() { onizlemeHazirlaniyor = true; kameraHatasi = null; _onizlemeOdak496=null; ++_odakSirasi496; });",
      "clear old focus marker on camera restart")
    a+=ADDITION
    b=once(b,
      """      child:Stack(fit:StackFit.expand,children:[
        FittedBox(fit:BoxFit.cover,""",
      """      child:LayoutBuilder(builder:(_,bounds)=>GestureDetector(
        behavior:HitTestBehavior.opaque,
        onTapDown:(details)=>unawaited(_onizlemeOdakla496(
          details.localPosition,Size(bounds.maxWidth,bounds.maxHeight))),
        child:Stack(fit:StackFit.expand,children:[
        FittedBox(fit:BoxFit.cover,""",
      "preview-only focus target")
    b=once(b,
      """        if(retus>.01)IgnorePointer(child:ColoredBox(""",
      """        if(_onizlemeOdak496!=null)Positioned(
          left:_onizlemeOdak496!.dx*bounds.maxWidth-22,
          top:_onizlemeOdak496!.dy*bounds.maxHeight-22,
          child:IgnorePointer(child:Container(
            width:44,height:44,decoration:BoxDecoration(
              shape:BoxShape.circle,
              border:Border.all(color:Colors.white,width:2),
              color:Colors.transparent)))),
        if(retus>.01)IgnorePointer(child:ColoredBox(""",
      "tap focus feedback ring")
    b=once(b,"""      ]),
    );
  }
""","""      ]),
      )),
    );
  }
""","layout close")
    for must in (
       "CameraPreview(c)", "ColorFiltered(", "retus>.01",
       "'540p' => ResolutionPreset.medium",
       "'1080p' => ResolutionPreset.veryHigh",
       "LK_OPTIONAL_SENTINEL"):
        if must=="LK_OPTIONAL_SENTINEL":continue
        if must not in a+b+c:raise RuntimeError("Build496 preserved feature missing: "+must)
    return a+b+c


if __name__=="__main__":
    old=FILE.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding="utf-8")
    print("Build496: tap-to-focus preview, unsupported cameras fall back to auto-focus")
