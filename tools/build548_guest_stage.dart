  bool _guestConsent548=false;
  Set<String> _hostMuted548=<String>{};
  List<String> _stageGuests548(){final ids=_viewerGuestIds489()..sort();return ids;}
  lk.Participant? _stageParticipant548(String uid){
    if(uid==FirebaseAuth.instance.currentUser?.uid)return widget.oda.localParticipant;
    for(final participant in widget.oda.remoteParticipants.values){if(_izleyiciUid(participant)==uid)return participant;}
    return null;
  }
  Widget _stageTile548(String uid,{bool host=false})=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
    future:_guestProfiles489.putIfAbsent(uid,()=>FirebaseFirestore.instance.collection('users').doc(uid).get()),
    builder:(_,snapshot){
      final profile=snapshot.data?.data()??<String,dynamic>{};
      final photo=(profile['photoUrl']??'').toString();
      final mine=uid==FirebaseAuth.instance.currentUser?.uid;
      final name=(profile['displayName']??profile['username']??(host?'Yayıncı':'Konuk')).toString();
      final participant=_stageParticipant548(uid);
      final track=host?_goruntu():_guestVideo489(uid);
      final speaking=participant?.isSpeaking==true;
      final hostMuted=_hostMuted548.contains(uid);
      final muted=!(participant?.audioTrackPublications.any((p)=>!p.muted)??false);
      return LayoutBuilder(builder:(_,bounds)=>Semantics(label:'$name ${host?'yayıncı':mine?'sen':'konuk'} ${track==null?'sesli':'görüntülü'}',child:Container(
        clipBehavior:Clip.antiAlias,
        decoration:BoxDecoration(color:const Color(0xFF282034),borderRadius:BorderRadius.circular(12),
          border:Border.all(color:speaking?const Color(0xFFAE68FF):Colors.white24,width:speaking?2.5:1)),
        child:Stack(fit:StackFit.expand,children:[
          if(track!=null)lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover)
          else Center(child:CircleAvatar(radius:math.min(35.0,math.max(14.0,bounds.maxHeight*.24)),
            backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?const Icon(Icons.person,color:Colors.white):null)),
          Positioned(left:3,right:3,bottom:3,child:Container(padding:const EdgeInsets.symmetric(horizontal:4,vertical:3),
            decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(7)),
            child:Row(children:[if(host)const Icon(Icons.star_rounded,color:Color(0xFFCB95FF),size:11),
              Expanded(child:Text(mine?'$name · Sen':name,maxLines:1,overflow:TextOverflow.ellipsis,
                style:const TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w700))),
              Icon(muted?Icons.mic_off:Icons.mic,color:muted?const Color(0xFFFF8C9C):Colors.white,size:12)]))),
          if(widget.yayinSahibi&&!host)Positioned(top:0,right:0,child:PopupMenuButton<String>(
            tooltip:'Konuk yönetimi',padding:EdgeInsets.zero,
            icon:const Icon(Icons.more_vert_rounded,color:Colors.white,size:18),
            onSelected:(action)=>unawaited(_hostGuestAction489(uid,action)),
            itemBuilder:(_)=>[
              PopupMenuItem(value:hostMuted?'unmute':'mute',child:Text(hostMuted?'Mikrofon izni ver':'Sessize al')),
              const PopupMenuItem(value:'kick',child:Text('Konukluktan çıkar')),
            ])),
        ]))));
    });
  Widget _stage548(){
    final guests=_stageGuests548();
    if(guests.isEmpty||yayinBitti||kapatildi)return const SizedBox.expand();
    if(ngelx548UseGrid(guests.length)&&!pkAktifYerel){
      final ids=<String>[widget.ownerId,...guests];
      return LayoutBuilder(builder:(_,box){
        final columns=ngelx548GridColumns(ids.length),rows=(ids.length/columns).ceil();
        final width=(box.maxWidth-(columns-1)*5)/columns;
        final height=(box.maxHeight-(rows-1)*5)/rows;
        if(width<=0||height<=0)return const SizedBox.shrink();
        return GridView.builder(padding:EdgeInsets.zero,physics:const NeverScrollableScrollPhysics(),
          itemCount:ids.length,gridDelegate:SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount:columns,crossAxisSpacing:5,mainAxisSpacing:5,childAspectRatio:width/height),
          itemBuilder:(_,i)=>_stageTile548(ids[i],host:i==0));
      });
    }
    return LayoutBuilder(builder:(_,box){
      if(box.maxHeight<guests.length*24)return const SizedBox.shrink();
      final width=math.min(98.0,box.maxWidth*.25);
      final count=guests.length;
      final height=math.min(112.0,math.max(0.0,(box.maxHeight-(count-1)*5)/count));
      return Align(alignment:Alignment.topRight,child:SizedBox(width:width,child:Column(
        mainAxisSize:MainAxisSize.min,children:[for(var i=0;i<count;i++)...[
          if(i>0)const SizedBox(height:5),
          SizedBox(height:height,child:_stageTile548(guests[i])),
        ]])));
    });
  }
  void _chooseGuestMedia548(bool camera){
    if(!mounted)return;
    setState((){_guestConsent548=true;_guestCameraWanted546=camera;});
    if(_guestWanted448&&!_guestActive448)unawaited(_guestSync448(true));
  }
  bool _guestBack548=false;
  Future<void> _guestFlip548()async{
    if(_guestMediaBusy546||!_guestActive448)return;
    final local=widget.oda.localParticipant;
    if(local==null)return;
    for(final publication in local.videoTrackPublications){
      final track=publication.track;
      if(track is lk.LocalVideoTrack){
        try{final next=!_guestBack548;await track.setCameraPosition(next?lk.CameraPosition.back:lk.CameraPosition.front);_guestBack548=next;}catch(_){}
        return;
      }
    }
  }
