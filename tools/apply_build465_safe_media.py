#!/usr/bin/env python3
"""Build465 device feedback: constrain full-screen chat photo/video to safe area.

This post-generation patch is UI-only. No media URL, Firestore, Android signature
or call behavior is changed. Refuses to guess if established view classes drift.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")

OLD_PHOTO="""class TamEkranMedyaPage extends StatelessWidget{final String url;const TamEkranMedyaPage({super.key,required this.url});@override Widget build(BuildContext context)=>Scaffold(backgroundColor:Colors.black,appBar:AppBar(backgroundColor:Colors.black,foregroundColor:Colors.white),body:Center(child:InteractiveViewer(minScale:.5,maxScale:5,child:NgelXAgResmi(url:url,fit:BoxFit.contain,placeholder:const Center(child:CircularProgressIndicator(color:Colors.white)),error:const Text('Medya açılamadı.',style:TextStyle(color:Colors.white))))));}"""
NEW_PHOTO="""// Build465 device QA: media never enters the Android navigation inset.
class TamEkranMedyaPage extends StatelessWidget{
  final String url;
  const TamEkranMedyaPage({super.key,required this.url});
  @override Widget build(BuildContext context)=>Scaffold(
    backgroundColor:Colors.black,
    appBar:AppBar(backgroundColor:Colors.black,foregroundColor:Colors.white),
    body:SafeArea(child:LayoutBuilder(builder:(_,area)=>InteractiveViewer(
      minScale:.5,maxScale:5,
      child:SizedBox(
        width:area.maxWidth,height:area.maxHeight,
        child:NgelXAgResmi(
          url:url,fit:BoxFit.contain,
          placeholder:const Center(child:CircularProgressIndicator(color:Colors.white)),
          error:const Center(child:Text('Medya açılamadı.',style:TextStyle(color:Colors.white))),
        ),
      ),
    ))),
  );
}"""

OLD_VIDEO="""    body:Center(child:NgelXGrupVideoMesaj(url:url,compact:false)),"""
NEW_VIDEO="""    body:SafeArea(child:LayoutBuilder(builder:(_,area)=>SizedBox(
      width:area.maxWidth,height:area.maxHeight,
      child:Center(child:NgelXGrupVideoMesaj(url:url,compact:false)),
    ))),"""

OLD_HEIGHT="""    final yukseklik=widget.compact?178.0:MediaQuery.sizeOf(context).height*.68;"""
NEW_HEIGHT="""    // Bound a tall video to the safe viewport even with gesture navigation.
    final ekran=MediaQuery.sizeOf(context);
    final inset=MediaQuery.viewPaddingOf(context);
    final kullanilabilir=math.max(140.0,ekran.height-inset.top-inset.bottom-kToolbarHeight-20);
    final yukseklik=widget.compact?178.0:math.min(ekran.height*.68,kullanilabilir);"""

def once(source,old,new,reason):
    count=source.count(old)
    if count!=1:
        raise RuntimeError(f"Build465 safe media: {reason} anchor count {count}, expected 1")
    return source.replace(old,new,1)

def transform(source):
    if "// Build465 device QA: media never enters" in source:
        return source
    source=once(source,OLD_PHOTO,NEW_PHOTO,"photo viewer")
    start=source.index("class TamEkranVideoPage")
    end=source.index("class GrupMedyaPage",start)
    region=once(source[start:end],OLD_VIDEO,NEW_VIDEO,"video viewer")
    source=source[:start]+region+source[end:]
    # Older source stages differ in their inline video-height expression.
    # SafeArea + the new full-screen LayoutBuilder constrain the player even
    # when Build456 has already changed the height expression.
    occurrences=source.count(OLD_HEIGHT)
    if occurrences==1:
        source=source.replace(OLD_HEIGHT,NEW_HEIGHT,1)
    elif occurrences==0:
        print("Build465 safe media: generated video height differs, keeping it; safe viewport remains enforced")
    else:
        raise RuntimeError("Build465 safe media: ambiguous video height")
    start=source.index("class _NgelXMedyaGaleriPageState")
    end=source.index("class SabitlenenGrupMesajlariPage",start)
    region=source[start:end]
    region=once(region,"    body:widget.urls.isEmpty","    body:SafeArea(child:widget.urls.isEmpty","gallery safe viewport")
    region=once(region,"      ),\n  );\n}","      ),\n    ),\n  );\n}","gallery close safe area")
    source=source[:start]+region+source[end:]
    return source

def main():
    original=MAIN.read_text(encoding="utf-8")
    updated=transform(original)
    if updated!=original:MAIN.write_text(updated,encoding="utf-8")
    print("Build465 device QA: photo, video and gallery viewer respect Android safe viewport")

if __name__=="__main__":main()
