#!/usr/bin/env python3
"""Build465 Messenger call controls: compact, responsive buttons and hang-up.

Preserves all existing camera, microphone, speaker, invite, effects,
reconnect and minimized-call state. No backend/Firebase behavior changes.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
START="  Widget _sesliAlani()=>"
END="class GrupBilgiPage extends StatefulWidget"
TAG="// Build465 Messenger call controls: responsive wrap and in-row hang-up"

ROW="""            child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:["""
WRAP="""            // Build465 Messenger call controls: responsive wrap and in-row hang-up.
            child:Wrap(alignment:WrapAlignment.center,spacing:14,runSpacing:12,children:["""
LAST="""              if(widget.goruntulu)_aramaKontrol(hoparlor?Icons.volume_up_rounded:Icons.volume_off_rounded,'Ses',hoparlorDegistir,hoparlor),
            ]),
          ),"""
NEW_LAST="""              if(widget.goruntulu)_aramaKontrol(hoparlor?Icons.volume_up_rounded:Icons.volume_off_rounded,'Ses',hoparlorDegistir,hoparlor),
              _ngelx465HangupControl(),
            ]),
          ),"""
OLD_END="""          if(bitisDurumu==null&&hata==null)Padding(
            padding:const EdgeInsets.only(top:6),
            child:InkWell(
              onTap:()=>bitir(),
              borderRadius:BorderRadius.circular(30),
              child:Container(width:138,height:64,decoration:BoxDecoration(color:const Color(0xFFFF443F),borderRadius:BorderRadius.circular(30),boxShadow:const [BoxShadow(color:Color(0x44FF443F),blurRadius:20,offset:Offset(0,8))]),child:const Icon(Icons.call_end_rounded,color:Colors.white,size:32)),
            ),
          ),
"""
NEW_METHOD="""  Widget _ngelx465HangupControl()=>Column(mainAxisSize:MainAxisSize.min,children:[
    Tooltip(
      message:'Görüşmeyi bitir',
      child:InkWell(
        onTap:()=>bitir(),
        borderRadius:BorderRadius.circular(32),
        child:Container(
          width:60,height:60,
          decoration:const BoxDecoration(
            color:Color(0xFFFF443F),
            shape:BoxShape.circle,
            boxShadow:[BoxShadow(color:Color(0x44FF443F),blurRadius:17,offset:Offset(0,5))],
          ),
          child:const Icon(Icons.call_end_rounded,color:Colors.white,size:30),
        ),
      ),
    ),
    const SizedBox(height:7),
    const Text('Bitir',style:TextStyle(color:Colors.white70,fontSize:10.5,fontWeight:FontWeight.w700)),
  ]);

"""
METHOD_ANCHOR="  Widget _aramaKontrol(IconData icon,String label,Future<void> Function() onTap,bool acik)=>Column("
def once(x,old,new,label):
    n=x.count(old)
    if n!=1:raise RuntimeError(f"Build465 Messenger call {label}: expected one anchor, got {n}")
    return x.replace(old,new,1)

def transform(source):
    if TAG in source:return source
    a=source.index(START);b=source.index(END,a)
    s=source[a:b]
    s=once(s,ROW,WRAP,"control row")
    s=once(s,LAST,NEW_LAST,"hangup inside wrap")
    s=once(s,OLD_END,"","large detached red button")
    s=once(s,METHOD_ANCHOR,NEW_METHOD+METHOD_ANCHOR,"hangup widget")
    return source[:a]+s+source[b:]

def main():
    old=MAIN.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:MAIN.write_text(new,encoding="utf-8")
    print("Build465: responsive Messenger call controls without detached hangup footer")

if __name__=="__main__":main()
