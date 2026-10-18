#!/usr/bin/env python3
"""Build488 B1: compact livestream identity and slim vertical guest previews.

Runs after Build453 and all earlier UI transformations. Keep existing
LiveKit/Firestore guest acceptance and host moderation functional.
Changes are additive presentation, scoped to _CanliYayinPageState.
"""
from pathlib import Path

FILE=Path("app/lib/live_broadcast_studio.dart")
START="class _CanliYayinPageState"
MARKER="// Build488: compact stream identity and right-side guest previews"


def one(src,old,new,label):
    n=src.count(old)
    if n!=1:
        raise RuntimeError(f"Build488 {label}: expected 1 match, got {n}")
    return src.replace(old,new,1)


METHOD=r"""
  // Build488: compact stream identity and right-side guest previews.
  // Guest thumbnails are a view on already accepted guest requests;
  // opening the list cannot accept a request or create a LiveKit room.
  bool _guestRailOpen488=false;
  Widget _guestRail488(){
    if(yayinBitti||kapatildi||MediaQuery.viewInsetsOf(context).bottom>0){
      return const SizedBox.shrink();
    }
    return Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.end,children:[
      Semantics(label:'Konukları aç veya kapat',button:true,child:InkWell(
        onTap:()=>setState(()=>_guestRailOpen488=!_guestRailOpen488),
        borderRadius:BorderRadius.circular(24),
        child:Container(
          width:38,height:38,
          decoration:BoxDecoration(color:Colors.black54,shape:BoxShape.circle,border:Border.all(color:Colors.white54)),
          child:Icon(_guestRailOpen488?Icons.close_rounded:Icons.add_rounded,color:Colors.white,size:23),
        ),
      )),
      if(_guestRailOpen488) ...[
        const SizedBox(height:7),
        Container(
          width:76,
          constraints:BoxConstraints(maxHeight:math.min(324.0,MediaQuery.sizeOf(context).height*.37)),
          padding:const EdgeInsets.symmetric(horizontal:4,vertical:6),
          decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(18),border:Border.all(color:Colors.white24)),
          child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId)
                .collection('guest_requests').snapshots(),
            builder:(_,snap){
              final guests=(snap.data?.docs??[])
                  .where((d)=>d.data()['status']=='accepted'&&d.id!=widget.ownerId)
                  .take(10).toList();
              if(guests.isEmpty){
                return const Padding(padding:EdgeInsets.symmetric(vertical:14),child:Text(
                  'Konuk yok',textAlign:TextAlign.center,
                  style:TextStyle(color:Colors.white70,fontSize:10),
                ));
              }
              return ListView.builder(
                shrinkWrap:true,
                itemCount:guests.length,
                itemBuilder:(_,i){
                  final uid=guests[i].id;
                  return Padding(
                    padding:const EdgeInsets.only(bottom:6),
                    child:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                      future:FirebaseFirestore.instance.collection('users').doc(uid).get(),
                      builder:(_,personSnap){
                        final p=personSnap.data?.data()??<String,dynamic>{};
                        final photo=(p['photoUrl']??'').toString();
                        final name=(p['displayName']??p['username']??'Konuk').toString();
                        return Column(mainAxisSize:MainAxisSize.min,children:[
                          CircleAvatar(radius:20,backgroundColor:const Color(0xFF31234D),
                            backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
                            child:photo.isEmpty?const Icon(Icons.person_rounded,color:Colors.white,size:18):null),
                          const SizedBox(height:2),
                          Text(name,maxLines:1,overflow:TextOverflow.ellipsis,
                            style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w700)),
                        ]);
                      },
                    ),
                  );
                },
              );
            },
          ),
        ),
      ],
    ]);
  }
"""


def transform(source):
    if MARKER in source:return source
    if source.count(START)!=1:
        raise RuntimeError("Build488 main live class not found once")
    a=source.index(START)
    region=source[a:]
    if "_hearts453" not in region or "_guestControl453" not in region:
        raise RuntimeError("Build488 requires preserved Build453 live controls and hearts")
    region=one(region,"  Widget _yorumPaneli(){",METHOD+"\n  Widget _yorumPaneli(){","guest rail declaration")
    # Live header varies slightly after historical UI passes. Keep the current
    # follow relationship callback; change only its already-following label.
    import re
    hstart=region.index("  Widget _yayinBasligi(){")
    hend=region.index("  Future<void> _yorumYonet(",hstart)
    header=region[hstart:hend]
    # Old Build453 may localize the unfollowed label with _ngelx438Ui.
    # Replace ONLY the already-followed text; preserve the existing callback,
    # Firestore follow check and the localized "Takip et" label.
    followPattern=r"""(takipte\s*\?\s*)'Takipte'(\s*:\s*(?:'Takip et'|_ngelx438Ui\("Takip et"\)))"""
    matches=list(re.finditer(followPattern,header))
    if len(matches)!=1:
        raise RuntimeError(f"Build488 follow header: expected one known follow widget, got {len(matches)}")
    header=re.sub(followPattern,r"\1'Takiptesin'\2",header,count=1)
    # Show the live like counter directly below the host name.
    likeWidget=r"""StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
                  builder:(_,likesSnap){
                    final storedLikes=(likesSnap.data?.data()?['likeCount'] as num?)?.toInt()??0;
                    // The stored likeCount is updated by the host heartbeat,
                    // not on every reaction. Listen to the original reaction
                    // documents so the count updates immediately while live.
                    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').snapshots(),
                      builder:(_,reactionSnap){
                        final liveLikes=reactionSnap.data?.docs.fold<int>(0,
                          (sum,d)=>sum+((d.data()['count'] as num?)?.toInt()??1));
                        final likes=liveLikes??storedLikes;
                        final display=likes>=1000
                          ?(likes/1000).toStringAsFixed(1).replaceAll('.',',')+' B'
                          :likes.toString();
                        return Row(mainAxisSize:MainAxisSize.min,children:[
                          const Icon(Icons.favorite_rounded,color:Color(0xFFFF5578),size:13),
                          const SizedBox(width:4),
                          Text(display,style:const TextStyle(color:Colors.white70,fontSize:11,fontWeight:FontWeight.w700)),
                        ]);
                      },
                    );
                  },
                ),"""

    # The displayed name is a single Text(ad,..) statement; unlike @username
    # the host displayName has remained stable across historical builds.
    namePattern=r"Text\(ad,maxLines:1,overflow:TextOverflow\.ellipsis,[^\n]*\),"
    names=list(re.finditer(namePattern,header))
    if len(names)!=1:
        raise RuntimeError("Build488: unique display-name label not found")
    hostName=names[0].group(0)
    header=header.replace(hostName,hostName+"\n              "+likeWidget,1)
    # Shrink the owner avatar only in the header, not chat/guest avatars.
    avatarPattern=r"CircleAvatar\(radius:\d+,backgroundImage:foto"
    avatars=list(re.finditer(avatarPattern,header))
    if len(avatars)==1:
        header=header.replace(avatars[0].group(0),"CircleAvatar(radius:17,backgroundImage:foto",1)
    else:
        raise RuntimeError("Build488: unique owner avatar not found")
    region=region[:hstart]+header+region[hend:]
    # The + and its vertical panel live down the right side, away from the host head.
    old="          if(yayinBitti)Positioned.fill"
    new="          if(!yayinBitti)Positioned(right:9,bottom:MediaQuery.viewInsetsOf(context).bottom+(widget.yayinSahibi?270:225),child:_guestRail488()),\n          if(yayinBitti)Positioned.fill"
    region=one(region,old,new,"slim guest rail positioning")
    # The transparent touch layer sits behind controls and does not take over
    # comment input, PK controls, gifts or the accepted-guest panel.
    old="          SafeArea(child: Padding("
    new="""          if(!widget.yayinSahibi&&!yayinBitti)Positioned.fill(
            child:GestureDetector(
              behavior:HitTestBehavior.translucent,
              onDoubleTap:()=>unawaited(_kalpDegistir()),
            ),
          ),
          SafeArea(child: Padding("""
    region=one(region,old,new,"double tap like")
    for contract in ("_guestControl453(true)","_guestControl453(false)",
                     "_kalpDegistir()","_hearts453","_yorumPaneli()"):
        if contract not in region:raise RuntimeError("Preserved live UI contract missing "+contract)
    return source[:a]+region


def main():
    before=FILE.read_text(encoding="utf-8")
    after=transform(before)
    if after!=before:FILE.write_text(after,encoding="utf-8")
    print("Build488 B1: compact follow/profile, heart counter, double-tap and max ten right-side guest previews")


if __name__=="__main__":main()
