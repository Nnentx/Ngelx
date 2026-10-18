part of 'main.dart';

DocumentReference<Map<String,dynamic>> ngelx448GuestRef(String live,String uid)=>FirebaseFirestore.instance.collection('live_streams').doc(live).collection('guest_requests').doc(uid);
Future<void> ngelx448GuestAction(BuildContext context,String live,String owner,String guest,String action)async{
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
  if(me==guest&&(action=='request'||action=='accept')){
    final permissions=await [Permission.microphone,Permission.camera].request();
    if(permissions.values.any((p)=>!p.isGranted)){if(context.mounted)ngelxDurumMesaji(context,'Yayına katılmak için kamera ve mikrofon izni gerekli.',tip:'uyari');return;}
  }
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final liveRef=FirebaseFirestore.instance.collection('live_streams').doc(live);
      final ref=ngelx448GuestRef(live,guest);
      final l=await tx.get(liveRef),d=await tx.get(ref);
      final v=l.data()??<String,dynamic>{},old=d.data()??<String,dynamic>{};
      if(v['active']!=true||v['ownerId']!=owner||guest==owner)throw StateError('live_ended');
      final status=old['status'];
      String next;
      if(action=='request'&&me==guest)next='pending';
      else if(action=='invite'&&me==owner)next='invited';
      else if(action=='accept'&&((status=='pending'&&me==owner)||(status=='invited'&&me==guest)))next='accepted';
      else if(action=='reject'&&(me==owner||me==guest))next='rejected';
      else throw StateError('invalid_transition');
      tx.set(ref,{'liveId':live,'hostUid':owner,'guestUid':guest,'status':next,'startedBy':next=='pending'?guest:next=='invited'?owner:old['startedBy'],'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    });
  }catch(_){if(context.mounted)ngelxDurumMesaji(context,'Yayın katılım işlemi tamamlanamadı.',tip:'hata');}
}

class Ngelx448GuestControls extends StatelessWidget{
  final String liveId,ownerUid;final bool host;final List<String> viewerUids;
  const Ngelx448GuestControls({super.key,required this.liveId,required this.ownerUid,required this.host,this.viewerUids=const[]});
  Future<void> _panel(BuildContext context)async{
    final stream=FirebaseFirestore.instance.collection('live_streams').doc(liveId).collection('guest_requests').snapshots();
    final profiles=<String,Future<DocumentSnapshot<Map<String,dynamic>>>>{};
    final pending=<String>{};
    await showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,backgroundColor:Colors.white,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:stream,builder:(_,snap){
      if(snap.hasError)return const Padding(padding:EdgeInsets.all(24),child:Text('Konuk listesi yüklenemedi. Yeniden açmayı dene.'));
      if(snap.connectionState==ConnectionState.waiting)return const SizedBox(height:150,child:Center(child:CircularProgressIndicator()));
      final requests=(snap.data?.docs??[]).where((d)=>['pending','invited','accepted'].contains(d.data()['status'])).toList();
      final ids=<String>{...requests.map((d)=>d.id),...viewerUids.where((id)=>id!=ownerUid)}.toList();
      final states={for(final d in requests)d.id:d.data()['status']};
      if(ids.isEmpty)return const Padding(padding:EdgeInsets.fromLTRB(24,8,24,28),child:Column(mainAxisSize:MainAxisSize.min,children:[Text('Konuk ekle',style:TextStyle(fontSize:20,fontWeight:FontWeight.w800)),SizedBox(height:14),Text('Henüz izleyici veya konuk isteği yok.',textAlign:TextAlign.center)]));
      return SizedBox(height:math.min(MediaQuery.sizeOf(c).height*.48,100.0+ids.length*78.0),child:Column(children:[
        const ListTile(title:Text('Konuk ekle',style:TextStyle(fontSize:20,fontWeight:FontWeight.w800)),subtitle:Text('İzleyici davet et veya katılım isteğini yönet')),
        Expanded(child:ListView.builder(itemCount:ids.length,itemBuilder:(_,i){final id=ids[i],status=states[id];return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:profiles.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('users').doc(id).get()),builder:(_,p){
          final person=p.data?.data()??<String,dynamic>{},photo=(person['photoUrl']??'').toString();
          final name=(person['displayName']??person['username']??'İzleyici').toString();
          Future<void> act(String action)async{if(!pending.add(id))return;try{await ngelx448GuestAction(c,liveId,ownerUid,id,action);}finally{pending.remove(id);}}
          return ListTile(leading:CircleAvatar(backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?const Icon(Icons.person):null),title:Text(name,maxLines:1,overflow:TextOverflow.ellipsis),subtitle:Text(status=='accepted'?'Kabul edildi':status=='invited'?'Davet gönderildi':status=='pending'?'Katılmak istiyor':'Canlı izleyicisi'),trailing:Row(mainAxisSize:MainAxisSize.min,children:[
            if(status==null)TextButton(onPressed:()=>act('invite'),child:const Text('Davet et')),
            if(status=='pending')IconButton(tooltip:'Kabul et',icon:const Icon(Icons.check,color:Colors.green),onPressed:()=>act('accept')),
            if(status!=null)IconButton(tooltip:status=='accepted'?'Konuk bağlantısını sonlandır':'Reddet / iptal et',icon:const Icon(Icons.close,color:Colors.red),onPressed:()=>act('reject')),
          ]));
        });})),
      ]));
    }))));
  }
  // Build497: compact viewer-only join sheet. This never enumerates the
  // host-only guest_requests collection; its state comes from the viewer's
  // own guest_requests/{uid} stream. Original transition guards remain intact.
  Future<void> _viewerJoinPanel497(BuildContext context,String uid,String? status)async{
    final invited=status=='invited';
    final pending=status=='pending';
    final joined=status=='accepted';
    final mainAction=invited?'accept':pending||joined?'reject':'request';
    final mainLabel=invited?'Daveti kabul et':joined?'Yayından ayrıl':pending?'İsteği iptal et':'Katılma isteği gönder';
    final detail=invited?'Yayıncı seni canlı yayına davet etti.':
      joined?'Şu anda konuk olarak yayındasın. Ayrılınca kamera ve mikrofon yayınlanmaz.':
      pending?'İsteğin yayıncıya gönderildi. Onaylanmasını bekleyebilir veya iptal edebilirsin.':
      'Katılma isteği göndermek için kamera ve mikrofon izni gerekir. Yayıncı onayladığında yayına bağlanabilirsin.';
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,useSafeArea:true,showDragHandle:true,
      backgroundColor:const Color(0xFF211D2F),
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(24))),
      builder:(sheetContext)=>SingleChildScrollView(
        child:Padding(
          padding:EdgeInsets.fromLTRB(22,8,22,24+MediaQuery.viewInsetsOf(sheetContext).bottom),
          child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[
            const Row(children:[
              Icon(Icons.video_call_rounded,color:Color(0xFF8CE8E6),size:25),
              SizedBox(width:10),
              Expanded(child:Text('Canlı yayına katıl',style:TextStyle(
                color:Colors.white,fontSize:19,fontWeight:FontWeight.w800))),
            ]),
            const SizedBox(height:12),
            Text(detail,style:const TextStyle(color:Colors.white70,fontSize:13.5,height:1.4)),
            const SizedBox(height:16),
            FilledButton.icon(
              style:FilledButton.styleFrom(
                backgroundColor:pending||joined?const Color(0xFF5D526A):const Color(0xFF20B9BD),
                foregroundColor:Colors.white,minimumSize:const Size.fromHeight(48)),
              onPressed:(){
                Navigator.of(sheetContext).pop();
                unawaited(ngelx448GuestAction(context,liveId,ownerUid,uid,mainAction));
              },
              icon:Icon(invited?Icons.check_rounded:joined||pending?Icons.close_rounded:Icons.person_add_alt_1_rounded),
              label:Text(mainLabel),
            ),
            if(invited)...[
              const SizedBox(height:6),
              TextButton(
                onPressed:(){
                  Navigator.of(sheetContext).pop();
                  unawaited(ngelx448GuestAction(context,liveId,ownerUid,uid,'reject'));
                },
                child:const Text('Daveti reddet',style:TextStyle(color:Colors.white70)),
              ),
            ],
          ]),
        ),
      ),
    );
  }

  @override Widget build(BuildContext context){
    if(host)return FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFF20C5CA),foregroundColor:Colors.white),onPressed:()=>_panel(context),icon:const Icon(Icons.person_add_alt_1),label:const Text('Konuk ekle'));
    final uid=FirebaseAuth.instance.currentUser?.uid;if(uid==null||ownerUid.isEmpty)return const SizedBox.shrink();
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:ngelx448GuestRef(liveId,uid).snapshots(),builder:(_,s){
      final status=s.data?.data()?['status'];
      if(status=='invited')return IconButton.filledTonal(
        tooltip:'Yayın davetini görüntüle',
        onPressed:()=>_viewerJoinPanel497(context,uid,'invited'),
        icon:const Icon(Icons.mark_email_unread_rounded));
      final label=status=='accepted'?'Yayından in':status=='pending'?'İptal et':'Konuk ol';
      return Column(mainAxisSize:MainAxisSize.min,children:[IconButton.filledTonal(tooltip:label,style:IconButton.styleFrom(backgroundColor:const Color(0xFFF0E8FF),foregroundColor:mor,minimumSize:const Size(48,48)),onPressed:()=>_viewerJoinPanel497(context,uid,status is String ? status : null),icon:Icon(status=='accepted'?Icons.logout:Icons.person_add_alt_1,size:25)),const SizedBox(height:4),Text(label,style:const TextStyle(color:Colors.black87,fontSize:11.5,fontWeight:FontWeight.w700))]);
    });
  }
}
