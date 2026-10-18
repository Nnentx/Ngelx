#!/usr/bin/env python3
"""Build510 QA: keep live comment history scrollable without losing new messages.

Run after Build490/Build509 patch steps. This UI-only patch preserves the
existing Firestore read, moderation, pinned comments, input and LiveKit room.
It changes no Firestore rules, production API, or payment/coin behavior.
"""
from pathlib import Path

FILE=Path("app/lib/live_broadcast_studio.dart")
START="class _CanliYayinPageState extends State<CanliYayinPage> {"
END="\nclass _CanliOzetSatiri extends StatelessWidget"
MARK="// Build510: manual livestream comment scrolling and return-to-latest"

EXTRA= r"""
  // Build510: manual livestream comment scrolling and return-to-latest.
  final ScrollController _commentScroll510=ScrollController();
  final ValueNotifier<bool> _readingOld510=ValueNotifier<bool>(false);
  final ValueNotifier<int> _newComments510=ValueNotifier<int>(0);
  String? _newestComment510;
  void _onCommentScroll510(){
    if(!_commentScroll510.hasClients)return;
    // reverse:true means offset zero is the newest (bottom) edge.
    final reading=_commentScroll510.offset>56;
    if(_readingOld510.value!=reading)_readingOld510.value=reading;
    if(!reading&&_newComments510.value!=0)_newComments510.value=0;
  }
  void _observeComments510(List<QueryDocumentSnapshot<Map<String,dynamic>>> docs){
    if(docs.isEmpty)return;
    final newest=docs.first.id;
    final previous=_newestComment510;
    _newestComment510=newest;
    if(previous==null||previous==newest)return;
    // Avoid notifications when browsing at the bottom. Snapshot listeners
    // remain active even if the host hides the comments with Build490.
    final index=docs.indexWhere((d)=>d.id==previous);
    final arrived=index>0?index:1;
    WidgetsBinding.instance.addPostFrameCallback((_){
      if(!mounted||!_commentScroll510.hasClients)return;
      if(_commentScroll510.offset>56){
        _newComments510.value=(_newComments510.value+arrived).clamp(0,999).toInt();
      }
    });
  }
  void _latestComments510(){
    if(_commentScroll510.hasClients){
      unawaited(_commentScroll510.animateTo(0,
        duration:const Duration(milliseconds:250),curve:Curves.easeOut));
    }
    _newComments510.value=0;
    _readingOld510.value=false;
  }
  Widget _newCommentChip510(){
    return ValueListenableBuilder<bool>(
      valueListenable:_readingOld510,
      builder:(_,reading,__)=>
        ValueListenableBuilder<int>(
          valueListenable:_newComments510,
          builder:(_,count,___){
            if(!reading&&count==0)return const SizedBox.shrink();
            return Material(color:Colors.transparent,child:Semantics(
              button:true,label:count>0?'Yeni yorumlar, en alta dön':'En yeni yorumlara dön',
              child:InkWell(
                onTap:_latestComments510,
                borderRadius:BorderRadius.circular(18),
                child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:10,vertical:7),
                  decoration:BoxDecoration(
                    color:const Color(0xE5342260),
                    borderRadius:BorderRadius.circular(18),
                    border:Border.all(color:Colors.white38),
                  ),
                  child:Row(mainAxisSize:MainAxisSize.min,children:[
                    const Icon(Icons.keyboard_arrow_down_rounded,color:Colors.white,size:17),
                    const SizedBox(width:4),
                    Text(count>0?'Yeni yorumlar ($count) · En alta dön':'En alta dön',
                      style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
                  ]),
                ),
              ),
            ));
          },
        ),
    );
  }
"""

def once(source:str,old:str,new:str,label:str)->str:
    count=source.count(old)
    if count!=1:
        raise RuntimeError(f"Build510 {label}: expected 1 match; got {count}")
    return source.replace(old,new,1)

def transform(src:str)->str:
    if MARK in src:return src
    start=src.index(START)
    stop=src.index(END,start)
    part=src[start:stop]
    if "Offstage(offstage:_commentsHidden490,child:_yorumPaneli())" not in part:
        raise RuntimeError("Build510 requires Build490 independent comment toggle")
    part=once(part,
        "  final yorum = TextEditingController();",
        "  final yorum = TextEditingController();\n"+EXTRA,
        "comment scrolling state")
    part=once(part,
        "    super.initState();",
        "    super.initState();\n    _commentScroll510.addListener(_onCommentScroll510);",
        "init listener")
    part=once(part,
        "    yorum.dispose();",
        """    _commentScroll510.removeListener(_onCommentScroll510);
    _commentScroll510.dispose();
    _readingOld510.dispose();
    _newComments510.dispose();
    yorum.dispose();""",
        "dispose scrolling state")
    a=part.index("  Widget _yorumPaneli(){")
    # Older Build453/490 generated sources can rename/move the comment input
    # method; stop at the NEXT top-level State method, not one exact name.
    import re
    following=part[a+len("  Widget _yorumPaneli(){"):]
    next_method=re.search(r"(?m)^  (?:Widget|Future|void|bool|int)\s+[_a-zA-Z]",following)
    if next_method is None:
        raise RuntimeError("Build510 comment panel closing method boundary missing")
    b=a+len("  Widget _yorumPaneli(){")+next_method.start()
    pre,comments,post=part[:a],part[a:b],part[b:]
    # Place the return-to-latest chip below Build490's comments Offstage
    # surface. No assumption about Build453's StreamBuilder/Flexible nesting.
    pre=once(pre,
        "Offstage(offstage:_commentsHidden490,child:_yorumPaneli()),",
        "Offstage(offstage:_commentsHidden490,child:_yorumPaneli()),\n        if(!_commentsHidden490)_newCommentChip510(),",
        "independent chip in Build490 comments section")

    # Only mutate the current comment stream, never pinned messages, LiveKit
    # or the caller's existing list layout. The generated versions may use
    # different whitespace and Flutter widget nesting.
    import re
    matchedLimits=re.findall(r"\.limit\(\d+\)\.snapshots\(\)",comments)
    if len(matchedLimits)!=1:
        raise RuntimeError(f"Build510 comment history query: expected 1 limit, got {len(matchedLimits)}")
    comments=comments.replace(matchedLimits[0],".limit(100).snapshots()",1)
    comments,observed=re.subn(
        r"(final yorumlar\s*=\s*[^\n;]+;)",
        r"\1\n            _observeComments510(yorumlar);",
        comments,count=1)
    if observed!=1:
        raise RuntimeError("Build510 comment docs observer: no unique declaration")
    matches=len(re.findall(r"ListView\.builder\(",comments))
    if matches!=1:
        raise RuntimeError(f"Build510 comment ListView.builder count: {matches}")
    comments=comments.replace("ListView.builder(",
        "ListView.builder(controller:_commentScroll510,",1)
    for guard in (
        "_yorumYonet(d.id,y)",
        "if(kind=='gift')",
        "if(kind=='join')",
        "'pinnedComment'",
        "stream:ref.collection('comments')",
        "controller:_commentScroll510",
        "reverse:true",
        "Yeni yorumlar ($count) · En alta dön",
    ):
        if guard not in (pre+comments+post):
            raise RuntimeError("Build510 preserved comment contract missing: "+guard)
    out=src[:start]+pre+comments+post+src[stop:]
    if out.count(MARK)!=1:raise RuntimeError("Build510 marker duplicated")
    return out

if __name__=="__main__":
    before=FILE.read_text(encoding="utf-8")
    after=transform(before)
    if after!=before:FILE.write_text(after,encoding="utf-8")
    print("Build510: 100 recent comments, manual scrolling, unread count, return-to-latest; no server writes")
