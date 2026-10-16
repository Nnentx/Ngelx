#!/usr/bin/env python3
"""Build465 Messenger call finishing: truthful ringing state and minimize control.

Change only presentation in the generated Flutter call widget, after prior
Build465 UI patches. The existing room handoff and call permissions stay intact.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
START="class _NgelXAramaPageState extends State<NgelXAramaPage>{"
END="class GrupBilgiPage extends StatefulWidget"
TAG="// Build465 Messenger: clear ringing label and explicit safe minimize action"

VOICE_OLD="Text(yenidenBaglaniyor?'Yeniden bağlanıyor…':baglaniyor?'Bağlanıyor…':'Sesli arama • '+_aramaSureYazi(),"
VOICE_NEW="Text(yenidenBaglaniyor?'Yeniden bağlanıyor…':baglaniyor?'Bağlanıyor…':aramaBaslangic==null?'Aranıyor…':'Sesli arama • '+_aramaSureYazi(),"
VIDEO_OLD="Text(yenidenBaglaniyor?'Yeniden bağlanıyor…':baglaniyor?'Aranıyor…':'Görüntülü arama • '+_aramaSureYazi(),"
VIDEO_NEW="Text(yenidenBaglaniyor?'Yeniden bağlanıyor…':baglaniyor?'Bağlanıyor…':aramaBaslangic==null?'Aranıyor…':'Görüntülü arama • '+_aramaSureYazi(),"
BODY_OLD="        child:SafeArea(child:Column(children:["
BODY_NEW="""        child:SafeArea(child:Column(children:[
          // Build465 Messenger: clear ringing label and explicit safe minimize action.
          // Wait until the room is available so minimizing never loses a new call.
          if(bitisDurumu==null&&hata==null&&oda!=null)Padding(
            padding:const EdgeInsets.fromLTRB(16,4,16,0),
            child:Row(children:[
              IconButton(
                tooltip:'Aramayı küçült ve sohbete dön',
                onPressed:()=>unawaited(_aramaEkraniniKucult()),
                icon:const Icon(Icons.keyboard_arrow_down_rounded,color:Colors.white,size:29),
              ),
              const SizedBox(width:5),
              Expanded(child:Text(
                yenidenBaglaniyor?'Yeniden bağlanıyor…':
                  aramaBaslangic==null?'Aranıyor…':'Görüşme sürüyor',
                maxLines:1,overflow:TextOverflow.ellipsis,
                style:const TextStyle(color:Colors.white70,fontSize:12,fontWeight:FontWeight.w700),
              )),
            ]),
          ),"""

def once(src,old,new,label):
    n=src.count(old)
    if n!=1:
        raise RuntimeError(f"Build465 Messenger call UI {label}: expected one marker, got {n}")
    return src.replace(old,new,1)

def transform(src):
    if TAG in src:return src
    a=src.index(START);b=src.index(END,a)
    segment=src[a:b]
    segment=once(segment,VOICE_OLD,VOICE_NEW,"voice ringing")
    segment=once(segment,VIDEO_OLD,VIDEO_NEW,"video ringing")
    segment=once(segment,BODY_OLD,BODY_NEW,"safe minimize")
    if "_aramaEkraniniKucult()async" not in segment or "oda!=null" not in segment:
        raise RuntimeError("Build465 call UI: existing guarded call handoff missing")
    return src[:a]+segment+src[b:]

def main():
    original=MAIN.read_text(encoding="utf-8")
    modified=transform(original)
    if modified!=original:MAIN.write_text(modified,encoding="utf-8")
    print("Build465: truthful outgoing ringing state and explicit safe call minimize")

if __name__=="__main__":main()
