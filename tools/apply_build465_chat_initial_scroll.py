#!/usr/bin/env python3
"""Build465: land group/private chats on newest messages at first open.

The existing ascending Firestore order, message widgets, drafts, search,
reply anchors and manual scroll behavior stay unchanged.
Runs after Build464 and PR62/63 generated-source patches; refuses drift.
"""
from pathlib import Path
import re

MAIN=Path("app/lib/main.dart")
FIELD="  final mesaj=TextEditingController(),liste=ScrollController();"
ADDED="""  // Build465: do not restore stale message-list offsets across chat openings.
  final mesaj=TextEditingController(),liste=ScrollController(keepScrollOffset:false);
  Timer? _ngelx465OpeningScrollTimer;
  bool _ngelx465OpeningScrollStarted=false;
  void _ngelx465StopOpeningBottom(){
    _ngelx465OpeningScrollTimer?.cancel();
    _ngelx465OpeningScrollTimer=null;
  }
  void _ngelx465ScheduleBottomOnOpen(){
    if(_ngelx465OpeningScrollStarted)return;
    _ngelx465OpeningScrollStarted=true;
    var ticks=0;
    _ngelx465OpeningScrollTimer=Timer.periodic(
      const Duration(milliseconds:140),(timer){
        if(!mounted||++ticks>16){
          timer.cancel();
          _ngelx465OpeningScrollTimer=null;
          return;
        }
        WidgetsBinding.instance.addPostFrameCallback((_){
          if(!mounted||!liste.hasClients||!timer.isActive)return;
          final pos=liste.position;
          if(!pos.hasContentDimensions)return;
          if(pos.maxScrollExtent>pos.pixels+1){
            liste.jumpTo(pos.maxScrollExtent);
          }
        });
      },
    );
  }
"""

def one(src,old,new,what):
    count=src.count(old)
    if count!=1:
        raise RuntimeError(f"Build465 open latest {what}: expected 1 anchor, found {count}")
    return src.replace(old,new,1)

def call_close(src,at):
    # Scan balanced Dart call delimiters, ignoring quoted text and comments.
    depth=0;quote=None;escaped=False;line_comment=False;block_comment=False
    i=at
    while i<len(src):
        c=src[i];n=src[i+1] if i+1<len(src) else ""
        if line_comment:
            if c=="\n":line_comment=False
        elif block_comment:
            if c=="*" and n=="/":block_comment=False;i+=1
        elif quote:
            if escaped:escaped=False
            elif c=="\\":escaped=True
            elif c==quote:quote=None
        elif c=="/" and n=="/":line_comment=True;i+=1
        elif c=="/" and n=="*":block_comment=True;i+=1
        elif c in ("'","\""):quote=c
        elif c=="(":depth+=1
        elif c==")":
            depth-=1
            if depth==0:return i
        i+=1
    raise RuntimeError("Build465 open latest: unterminated ListView builder")

def wrap_touch(src,anchor):
    if src.count(anchor)!=1:
        raise RuntimeError(f"Build465 open latest: scroll listener anchor count {src.count(anchor)}")
    beginning=src.index(anchor)
    open_paren=beginning+len("child:ListView.builder")
    ending=call_close(src,open_paren)
    # Listener absorbs pointer-down only to stop automatic *opening* layout
    # corrections; other scroll, reactions and long-press gestures pass through.
    src=src[:ending+1]+")"+src[ending+1:]
    return src.replace(anchor,
        anchor.replace("child:ListView.builder(",
          "child:Listener(onPointerDown:(_)=>_ngelx465StopOpeningBottom(),child:ListView.builder("),
        1)

def patch_state(src,begin,end,marker,list_anchor,kind):
    a=src.index(begin);b=src.index(end,a)
    area=src[a:b]
    area=one(area,FIELD,ADDED,"state field "+kind)
    area=one(area,marker,marker.replace("sonaGit();",
        "{sonaGit();_ngelx465ScheduleBottomOnOpen();}"),
        "snapshot trigger "+kind)
    # The disposal method of the conversation state is its first such method.
    disposal=re.search(r"@override\s+void\s+dispose\s*\(\s*\)\s*\{",area)
    if not disposal:raise RuntimeError("Build465 open latest: no dispose in "+kind)
    spot=disposal.end()
    area=area[:spot]+"_ngelx465StopOpeningBottom();"+area[spot:]
    area=wrap_touch(area,list_anchor)
    return src[:a]+area+src[b:]

def transform(src):
    if "// Build465: do not restore stale message-list offsets" in src:
        return src
    src=patch_state(
        src,"class _GrupSohbetPageState","class TamEkranMedyaPage",
        "if(_ilkMesajKaydirma||_enAltta)sonaGit();",
        "child:ListView.builder(\n                    controller:liste,","group",
    )
    src=patch_state(
        src,"class _SohbetPageState","class NgelXGrupVideoMesaj",
        "if(s.hasData)sonaGit();",
        "child:ListView.builder(\n            key:PageStorageKey<String>('private_chat_'+widget.chatId),",
        "private",
    )
    return src

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding="utf-8")
    print("Build465: group and private conversations open at latest messages; user scroll stays manual")

if __name__=="__main__":
    main()
