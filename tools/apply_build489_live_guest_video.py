#!/usr/bin/env python3
"""Build489 B2: real guest video rail and host-only audio/guest controls.

Run AFTER apply_build488_live_reference_stage1.py on generated Flutter sources.
The existing LiveKit room, guest transition helper and comment moderation stay intact.
No production deployment is performed by this patch.
"""
from pathlib import Path

FILE=Path("app/lib/live_broadcast_studio.dart")
MARKER="// Build489: video guest rail with host-only moderation"

METHOD=r"""
  // Build488: compact stream identity and right-side guest previews
  // Build489: video guest rail with host-only moderation.
  bool _guestRailOpen488=false;
  bool _guestAudioMuted489=false;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _guestAudioPolicySub489;
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _guestProfiles489={};

  lk.VideoTrack? _guestVideo489(String uid){
    if(uid==FirebaseAuth.instance.currentUser?.uid&&!widget.yayinSahibi){
      for(final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]){
        if(!p.muted&&p.track is lk.VideoTrack)return p.track as lk.VideoTrack;
      }
    }
    for(final participant in widget.oda.remoteParticipants.values){
      if(_izleyiciUid(participant)!=uid)continue;
      for(final p in participant.videoTrackPublications){
        if(p.subscribed&&!p.muted&&p.track is lk.VideoTrack)return p.track as lk.VideoTrack;
      }
    }
    return null;
  }

  List<String> _viewerGuestIds489(){
    final ids=<String>{};
    for(final participant in widget.oda.remoteParticipants.values){
      final uid=_izleyiciUid(participant);
      if(uid.isEmpty||uid==widget.ownerId)continue;
      if(participant.videoTrackPublications.any((p)=>p.subscribed&&!p.muted&&p.track is lk.VideoTrack)){
        ids.add(uid);
      }
    }
    final me=FirebaseAuth.instance.currentUser?.uid??'';
    if(!widget.yayinSahibi&&_guestActive448&&me.isNotEmpty&&_guestVideo489(me)!=null)ids.add(me);
    return ids.take(10).toList();
  }

  Future<void> _hostGuestAction489(String uid,String action)async{
    if(!widget.yayinSahibi||uid.isEmpty||uid==widget.ownerId||
       FirebaseAuth.instance.currentUser?.uid!=widget.ownerId)return;
    if(action=='kick'){
      await ngelx448GuestAction(context,widget.belgeId,widget.ownerId,uid,'reject');
      return;
    }
    if(action!='mute'&&action!='unmute')return;
    try{
      final liveRef=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
      await FirebaseFirestore.instance.runTransaction((tx)async{
        final live=await tx.get(liveRef);
        final guest=await tx.get(ngelx448GuestRef(widget.belgeId,uid));
        if(live.data()?['active']!=true||live.data()?['ownerId']!=widget.ownerId||
            guest.data()?['status']!='accepted')throw StateError('guest_not_active');
        tx.update(liveRef,{
          'guestAudioMutedUids':action=='mute'
            ?FieldValue.arrayUnion([uid]):FieldValue.arrayRemove([uid]),
        });
      });
    }catch(_){
      if(mounted)ngelxDurumMesaji(context,'Konuk ses işlemi tamamlanamadı.',tip:'hata');
    }
  }

  Widget _guestTile489(String uid,{required bool muted}){
    return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      future:_guestProfiles489.putIfAbsent(uid,()=>FirebaseFirestore.instance.collection('users').doc(uid).get()),
      builder:(_,personSnap){
        final person=personSnap.data?.data()??<String,dynamic>{};
        final photo=(person['photoUrl']??'').toString();
        final name=(person['displayName']??person['username']??'Konuk').toString();
        final track=_guestVideo489(uid);
        return Padding(
          padding:const EdgeInsets.only(bottom:6),
          child:Semantics(
            label:'Konuk $name',
            child:SizedBox(width:72,height:83,child:ClipRRect(
              borderRadius:BorderRadius.circular(12),
              child:Stack(children:[
                Positioned.fill(child:ColoredBox(
                  color:const Color(0xFF31234D),
                  child:track==null
                    ?Center(child:CircleAvatar(radius:19,
                        backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
                        child:photo.isEmpty?const Icon(Icons.person_rounded,color:Colors.white,size:18):null))
                    :lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover),
                )),
                Positioned(left:0,right:0,bottom:0,child:Container(
                  padding:const EdgeInsets.fromLTRB(3,5,3,3),
                  decoration:const BoxDecoration(gradient:LinearGradient(
                    begin:Alignment.topCenter,end:Alignment.bottomCenter,
                    colors:[Colors.transparent,Colors.black87])),
                  child:Text(name,maxLines:1,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,
                    style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w700)),
                )),
                if(widget.yayinSahibi)Positioned(top:0,right:0,child:PopupMenuButton<String>(
                  tooltip:'Konuk yönetimi',
                  padding:EdgeInsets.zero,
                  constraints:const BoxConstraints(minWidth:135,maxWidth:185),
                  icon:const Icon(Icons.more_vert_rounded,size:18,color:Colors.white),
                  color:const Color(0xFF282134),
                  onSelected:(action)=>unawaited(_hostGuestAction489(uid,action)),
                  itemBuilder:(_)=>[
                    PopupMenuItem(value:muted?'unmute':'mute',
                      child:Text(muted?'Sesini aç':'Sessize al',
                        style:const TextStyle(color:Colors.white,fontSize:12))),
                    const PopupMenuItem(value:'kick',
                      child:Text('Sesten at',style:TextStyle(color:Colors.white,fontSize:12))),
                  ],
                )),
                if(muted)const Positioned(left:3,top:3,
                  child:Icon(Icons.mic_off_rounded,size:13,color:Colors.white)),
              ]),
            )),
          ),
        );
      },
    );
  }

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
      if(_guestRailOpen488)...[
        const SizedBox(height:7),
        Container(
          width:76,
          constraints:BoxConstraints(maxHeight:math.min(324.0,MediaQuery.sizeOf(context).height*.37)),
          padding:const EdgeInsets.symmetric(horizontal:2,vertical:5),
          decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(15),border:Border.all(color:Colors.white24)),
          child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
            builder:(_,liveSnap){
              final muted=List<String>.from(liveSnap.data?.data()?['guestAudioMutedUids']??const[]);
              if(widget.yayinSahibi){
                // Firestore guest_requests list permission is host-only.
                return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId)
                    .collection('guest_requests').snapshots(),
                  builder:(_,guestSnap){
                    final ids=(guestSnap.data?.docs??[])
                      .where((d)=>d.data()['status']=='accepted'&&d.id!=widget.ownerId)
                      .map((d)=>d.id).take(10).toList();
                    if(guestSnap.hasError)return const Text('Konuklar alınamadı',
                      style:TextStyle(color:Colors.white70,fontSize:10));
                    if(ids.isEmpty)return const Padding(padding:EdgeInsets.all(5),
                      child:Text('Konuk yok',style:TextStyle(color:Colors.white70,fontSize:10)));
                    return ListView.builder(shrinkWrap:true,itemCount:ids.length,
                      itemBuilder:(_,i)=>_guestTile489(ids[i],muted:muted.contains(ids[i])));
                  },
                );
              }
              // Non-hosts can only read their own guest request; use real
              // published LiveKit tracks, not forbidden guest_requests.list.
              final ids=_viewerGuestIds489();
              if(ids.isEmpty)return const Padding(padding:EdgeInsets.all(5),
                child:Text('Konuk yok',style:TextStyle(color:Colors.white70,fontSize:10)));
              return ListView.builder(shrinkWrap:true,itemCount:ids.length,
                itemBuilder:(_,i)=>_guestTile489(ids[i],muted:muted.contains(ids[i])));
            },
          ),
        ),
      ],
    ]);
  }

"""


def replace_one(s,old,new,label):
    count=s.count(old)
    if count!=1:raise RuntimeError(f"Build489 {label}: expected one match, found {count}")
    return s.replace(old,new,1)


def transform(source):
    if MARKER in source:return source
    begin=source.index("class _CanliYayinPageState")
    head,body=source[:begin],source[begin:]
    a=body.index("  // Build488: compact stream identity and right-side guest previews")
    b=body.index("  Widget _yorumPaneli(){",a)
    body=body[:a]+METHOD+body[b:]
    body=replace_one(body,
        "    _reactionSub453=FirebaseFirestore.instance.collection('live_streams')",
        """    _guestAudioPolicySub489=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots().listen((snapshot){
      if(widget.yayinSahibi||!mounted)return;
      final uid=FirebaseAuth.instance.currentUser?.uid;
      if(uid==null)return;
      final flags=snapshot.data()?['guestAudioMutedUids'];
      final muted=flags is List && flags.contains(uid);
      final changed=muted!=_guestAudioMuted489;
      _guestAudioMuted489=muted;
      if(changed&&_guestActive448){
        unawaited(widget.oda.localParticipant?.setMicrophoneEnabled(!muted) ?? Future<void>.value());
      }
    },onError:(_){});
    _reactionSub453=FirebaseFirestore.instance.collection('live_streams')""",
        "guest audio policy listener")
    body=replace_one(body,"    _reactionSub453?.cancel();",
        "    _guestAudioPolicySub489?.cancel();\n    _reactionSub453?.cancel();",
        "listener cleanup")
    # The guest's own live doc is fetched before a newly accepted guest
    # activates the microphone. Snapshot updates apply host mute live.
    syncA=body.index("  Future<void> _guestSync448(")
    syncB=body.index("  void _yenile()",syncA)
    sync=body[syncA:syncB]
    sync=replace_one(sync,
        "      final d=await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).get();",
        """      final d=await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).get();
      final uid=FirebaseAuth.instance.currentUser?.uid;
      _guestAudioMuted489=uid!=null&&List<String>.from(d.data()?['guestAudioMutedUids']??const[]).contains(uid);""",
        "guest initial mute")
    body=body[:syncA]+sync+body[syncB:]
    old="await widget.oda.localParticipant?.setMicrophoneEnabled(accepted);"
    if body.count(old)<2:raise RuntimeError("Build489 requires guest connect and reconnect microphone gates")
    body=body.replace(old,
        "await widget.oda.localParticipant?.setMicrophoneEnabled(accepted&&!_guestAudioMuted489);")
    body=replace_one(body,
        "bottom:MediaQuery.viewInsetsOf(context).bottom+(widget.yayinSahibi?270:225)",
        "bottom:MediaQuery.viewInsetsOf(context).bottom+math.min(MediaQuery.sizeOf(context).height*.33,widget.yayinSahibi?270.0:225.0)",
        "small-screen guest rail bottom")
    for token in ("_guestControl453(true)","_guestControl453(false)",
                  "_kalpDegistir()","_hearts453","NgelXCanliPkKatmani("):
        if token not in body:raise RuntimeError("Build489 preserved feature missing: "+token)
    return head+body


def main():
    before=FILE.read_text(encoding="utf-8")
    after=transform(before)
    if after!=before:FILE.write_text(after,encoding="utf-8")
    print("Build489 B2: host-approved video guest rail, role-scoped mute/reject, viewer-safe track discovery")


if __name__=="__main__":main()
