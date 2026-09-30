part of 'main.dart';

String ngelxCanliPkBelgeId(String a,String b){
  final x=a.compareTo(b)<=0?a:b;
  final y=a.compareTo(b)<=0?b:a;
  return ngelxBildirimBelgeId('pk_${x}_${y}');
}

Future<void> ngelxCanliPkYayindanCik(String liveId)async{
  if(liveId.isEmpty)return;
  try{
    final liveRef=FirebaseFirestore.instance.collection('live_streams').doc(liveId);
    final live=await liveRef.get();
    final lv=live.data()??<String,dynamic>{};
    final sessionId=(lv['pkSessionId']??'').toString();
    if(sessionId.isEmpty)return;
    final sessionRef=FirebaseFirestore.instance.collection('live_pk_requests').doc(sessionId);
    final session=await sessionRef.get();
    final sv=session.data()??<String,dynamic>{};
    final a=(sv['inviterLiveId']??'').toString();
    final b=(sv['inviteeLiveId']??'').toString();
    final batch=FirebaseFirestore.instance.batch();
    batch.set(sessionRef,{
      'status':'ended',
      'endReason':'live_ended',
      'endedAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
    for(final id in <String>{a,b,liveId}.where((x)=>x.isNotEmpty)){
      batch.set(FirebaseFirestore.instance.collection('live_streams').doc(id),{
        'pkActive':false,
        'pkSessionId':FieldValue.delete(),
        'pkOpponentLiveId':FieldValue.delete(),
        'pkOpponentUid':FieldValue.delete(),
        'pkEndsAt':FieldValue.delete(),
        'pendingPkRequestId':FieldValue.delete(),
        'pendingPkFromLiveId':FieldValue.delete(),
      },SetOptions(merge:true));
    }
    await batch.commit();
  }catch(_){}
}

Future<void> ngelxCanliPkIstekPaneli(
  BuildContext context,{
  required String liveId,
  required String ownerUid,
}) async {
  if(liveId.isEmpty||ownerUid.isEmpty)return;
  final mevcut=await FirebaseFirestore.instance.collection('live_streams').doc(liveId).get();
  final mv=mevcut.data()??<String,dynamic>{};
  if(!ngelxCanliKaydiTaze(mv)){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayın aktif değil.')));
    return;
  }

  if(!context.mounted)return;
  await showModalBottomSheet<void>(
    context:context,
    backgroundColor:Colors.white,
    showDragHandle:true,
    isScrollControlled:true,
    useSafeArea:true,
    shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
    builder:(sheetContext)=>SafeArea(
      child:SizedBox(
        height:MediaQuery.sizeOf(sheetContext).height*.68,
        child:Column(children:[
          const Padding(
            padding:EdgeInsets.fromLTRB(18,0,18,10),
            child:Row(children:[
              CircleAvatar(backgroundColor:Color(0xFFFFE7EC),child:Icon(Icons.sports_mma_rounded,color:Color(0xFFFF1744))),
              SizedBox(width:10),
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Text('Canlı Yayın PK',style:TextStyle(color:Colors.black87,fontSize:20,fontWeight:FontWeight.w900)),
                Text('Aktif bir yayıncıya 3 dakikalık yarış isteği gönder.',style:TextStyle(color:Colors.black54,fontSize:12)),
              ])),
            ]),
          ),
          const Divider(height:1),
          Expanded(
            child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
              stream:FirebaseFirestore.instance.collection('live_streams').where('active',isEqualTo:true).limit(40).snapshots(),
              builder:(_,snap){
                if(snap.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:Color(0xFFFF1744)));
                final docs=(snap.data?.docs??[]).where((d){
                  if(d.id==liveId)return false;
                  final v=d.data();
                  return ngelxCanliKaydiTaze(v)
                    &&(v['ownerId']??'').toString().isNotEmpty
                    &&(v['ownerId']??'').toString()!=ownerUid
                    &&v['pkActive']!=true;
                }).toList()
                  ..sort((a,b){
                    final av=(a.data()['viewerCount'] as num?)?.toInt()??0;
                    final bv=(b.data()['viewerCount'] as num?)?.toInt()??0;
                    return bv.compareTo(av);
                  });
                if(docs.isEmpty)return const Center(child:Text('Şu anda PK yapılabilecek başka aktif yayın yok.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)));
                return ListView.separated(
                  padding:const EdgeInsets.fromLTRB(14,12,14,24),
                  itemCount:docs.length,
                  separatorBuilder:(_,__)=>const Divider(height:1,indent:66),
                  itemBuilder:(_,i){
                    final d=docs[i],v=d.data();
                    final hedefUid=(v['ownerId']??'').toString();
                    final ad=(v['username']??'NgelX').toString();
                    final izleyici=(v['viewerCount'] as num?)?.toInt()??0;
                    return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                      future:FirebaseFirestore.instance.collection('users').doc(hedefUid).get(),
                      builder:(_,p){
                        final pv=p.data?.data()??<String,dynamic>{};
                        final foto=(pv['photoUrl']??'').toString();
                        final gorunen=(pv['displayName']??pv['username']??ad).toString();
                        return ListTile(
                          leading:CircleAvatar(radius:24,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded):null),
                          title:Text(gorunen,style:const TextStyle(fontWeight:FontWeight.w900)),
                          subtitle:Text('@$ad • $izleyici izleyici'),
                          trailing:FilledButton.icon(
                            style:FilledButton.styleFrom(backgroundColor:const Color(0xFFFF1744),foregroundColor:Colors.white),
                            onPressed:()async{
                              final id=ngelxCanliPkBelgeId(liveId,d.id);
                              final ref=FirebaseFirestore.instance.collection('live_pk_requests').doc(id);
                              final mevcutIstek=await ref.get();
                              final durum=(mevcutIstek.data()?['status']??'').toString();
                              if(durum=='pending'||durum=='active'){
                                if(sheetContext.mounted)ScaffoldMessenger.of(sheetContext).showSnackBar(const SnackBar(content:Text('Bu yayıncıyla zaten açık bir PK isteği var.')));
                                return;
                              }
                              await ref.set({
                                'inviterLiveId':liveId,
                                'inviteeLiveId':d.id,
                                'inviterUid':ownerUid,
                                'inviteeUid':hedefUid,
                                'inviterName':(mv['username']??'NgelX').toString(),
                                'inviteeName':ad,
                                'status':'pending',
                                'durationSeconds':180,
                                'createdAt':FieldValue.serverTimestamp(),
                                'clientCreatedAt':Timestamp.now(),
                                'requestExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(seconds:45))),
                              },SetOptions(merge:true));
                              await FirebaseFirestore.instance.collection('live_streams').doc(d.id).set({
                                'pendingPkRequestId':id,
                                'pendingPkFromLiveId':liveId,
                              },SetOptions(merge:true));
                              unawaited(uygulamaBildirimiGonder(
                                toUid:hedefUid,
                                fromUid:ownerUid,
                                tur:'live',
                                metin:'sana canlı yayın PK isteği gönderdi',
                                belgeId:liveId,
                                hedefTuru:'live',
                                hedefBaslik:(mv['title']??'Canlı yayın').toString(),
                                olayTuru:'live_pk_request',
                                dedupeKey:'live_pk_${id}_$hedefUid',
                              ).catchError((_){ }));
                              if(sheetContext.mounted){
                                Navigator.pop(sheetContext);
                                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('PK isteği gönderildi.')));
                              }
                            },
                            icon:const Icon(Icons.flash_on_rounded,size:18),
                            label:const Text('PK',style:TextStyle(fontWeight:FontWeight.w900)),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
        ]),
      ),
    ),
  );
}

class NgelXCanliPkKatmani extends StatefulWidget{
  final String liveId;
  final bool yayinSahibi;
  const NgelXCanliPkKatmani({super.key,required this.liveId,required this.yayinSahibi});
  @override State<NgelXCanliPkKatmani> createState()=>_NgelXCanliPkKatmaniState();
}

class _NgelXCanliPkKatmaniState extends State<NgelXCanliPkKatmani>{
  Timer? _sayac;
  bool _bitiriliyor=false;

  @override void initState(){
    super.initState();
    _sayac=Timer.periodic(const Duration(seconds:1),(_){if(mounted)setState((){});});
  }
  @override void dispose(){_sayac?.cancel();super.dispose();}

  Future<void> _karar(String requestId,bool kabul)async{
    if(_bitiriliyor)return;
    _bitiriliyor=true;
    try{
      final ref=FirebaseFirestore.instance.collection('live_pk_requests').doc(requestId);
      final r=await ref.get(const GetOptions(source:Source.server));
      final v=r.data()??<String,dynamic>{};
      if((v['status']??'')!='pending')return;
      final aId=(v['inviterLiveId']??'').toString();
      final bId=(v['inviteeLiveId']??'').toString();
      if(aId.isEmpty||bId.isEmpty)return;
      if(!kabul){
        await ref.set({'status':'rejected','answeredAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
        await FirebaseFirestore.instance.collection('live_streams').doc(bId).set({
          'pendingPkRequestId':FieldValue.delete(),
          'pendingPkFromLiveId':FieldValue.delete(),
        },SetOptions(merge:true));
        return;
      }

      final docs=await Future.wait([
        FirebaseFirestore.instance.collection('live_streams').doc(aId).get(const GetOptions(source:Source.server)),
        FirebaseFirestore.instance.collection('live_streams').doc(bId).get(const GetOptions(source:Source.server)),
      ]);
      final a=docs[0].data()??<String,dynamic>{};
      final b=docs[1].data()??<String,dynamic>{};
      if(!ngelxCanliKaydiTaze(a)||!ngelxCanliKaydiTaze(b)){
        await ref.set({'status':'expired','answeredAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
        return;
      }
      final now=DateTime.now();
      final ends=Timestamp.fromDate(now.add(const Duration(minutes:3)));
      final batch=FirebaseFirestore.instance.batch();
      batch.set(ref,{
        'status':'active',
        'startedAt':FieldValue.serverTimestamp(),
        'clientStartedAt':Timestamp.fromDate(now),
        'endsAt':ends,
        'startLikeA':(a['likeCount'] as num?)?.toInt()??0,
        'startLikeB':(b['likeCount'] as num?)?.toInt()??0,
        'startGiftA':(a['giftPoints'] as num?)?.toInt()??0,
        'startGiftB':(b['giftPoints'] as num?)?.toInt()??0,
      },SetOptions(merge:true));
      batch.set(docs[0].reference,{
        'pkActive':true,'pkSessionId':requestId,'pkOpponentLiveId':bId,
        'pkOpponentUid':(b['ownerId']??'').toString(),'pkEndsAt':ends,
      },SetOptions(merge:true));
      batch.set(docs[1].reference,{
        'pkActive':true,'pkSessionId':requestId,'pkOpponentLiveId':aId,
        'pkOpponentUid':(a['ownerId']??'').toString(),'pkEndsAt':ends,
        'pendingPkRequestId':FieldValue.delete(),'pendingPkFromLiveId':FieldValue.delete(),
      },SetOptions(merge:true));
      await batch.commit();
    }finally{
      _bitiriliyor=false;
      if(mounted)setState((){});
    }
  }

  Future<void> _pkBitir(String requestId)async{
    if(_bitiriliyor)return;
    _bitiriliyor=true;
    try{
      final ref=FirebaseFirestore.instance.collection('live_pk_requests').doc(requestId);
      final r=await ref.get();
      final v=r.data()??<String,dynamic>{};
      if((v['status']??'')!='active')return;
      final aId=(v['inviterLiveId']??'').toString(),bId=(v['inviteeLiveId']??'').toString();
      final docs=await Future.wait([
        FirebaseFirestore.instance.collection('live_streams').doc(aId).get(),
        FirebaseFirestore.instance.collection('live_streams').doc(bId).get(),
      ]);
      final a=docs[0].data()??<String,dynamic>{},b=docs[1].data()??<String,dynamic>{};
      final scoreA=((a['likeCount'] as num?)?.toInt()??0)-((v['startLikeA'] as num?)?.toInt()??0)
        +((((a['giftPoints'] as num?)?.toInt()??0)-((v['startGiftA'] as num?)?.toInt()??0))~/10);
      final scoreB=((b['likeCount'] as num?)?.toInt()??0)-((v['startLikeB'] as num?)?.toInt()??0)
        +((((b['giftPoints'] as num?)?.toInt()??0)-((v['startGiftB'] as num?)?.toInt()??0))~/10);
      final batch=FirebaseFirestore.instance.batch();
      batch.set(ref,{'status':'ended','endedAt':FieldValue.serverTimestamp(),'finalScoreA':scoreA,'finalScoreB':scoreB},SetOptions(merge:true));
      for(final d in docs){
        batch.set(d.reference,{
          'pkActive':false,
          'pkSessionId':FieldValue.delete(),
          'pkOpponentLiveId':FieldValue.delete(),
          'pkOpponentUid':FieldValue.delete(),
          'pkEndsAt':FieldValue.delete(),
        },SetOptions(merge:true));
      }
      await batch.commit();
    }finally{
      _bitiriliyor=false;
      if(mounted)setState((){});
    }
  }

  Widget _aktifPk(Map<String,dynamic> live,String requestId){
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_pk_requests').doc(requestId).snapshots(),
      builder:(_,rSnap){
        final r=rSnap.data?.data()??<String,dynamic>{};
        if((r['status']??'')!='active')return const SizedBox.shrink();
        final aId=(r['inviterLiveId']??'').toString(),bId=(r['inviteeLiveId']??'').toString();
        return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('live_streams').doc(aId).snapshots(),
          builder:(_,aSnap)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('live_streams').doc(bId).snapshots(),
            builder:(_,bSnap){
              final a=aSnap.data?.data()??<String,dynamic>{},b=bSnap.data?.data()??<String,dynamic>{};
              final scoreA=((a['likeCount'] as num?)?.toInt()??0)-((r['startLikeA'] as num?)?.toInt()??0)
                +((((a['giftPoints'] as num?)?.toInt()??0)-((r['startGiftA'] as num?)?.toInt()??0))~/10);
              final scoreB=((b['likeCount'] as num?)?.toInt()??0)-((r['startLikeB'] as num?)?.toInt()??0)
                +((((b['giftPoints'] as num?)?.toInt()??0)-((r['startGiftB'] as num?)?.toInt()??0))~/10);
              final ends=r['endsAt'];
              var kalan=180;
              if(ends is Timestamp)kalan=ends.toDate().difference(DateTime.now()).inSeconds.clamp(0,180).toInt();
              if(kalan<=0&&widget.yayinSahibi&&!_bitiriliyor)unawaited(_pkBitir(requestId));
              final dk=(kalan~/60).toString().padLeft(2,'0'),sn=(kalan%60).toString().padLeft(2,'0');
              final toplam=(scoreA+scoreB).clamp(1,1<<30);
              final aOran=(scoreA/toplam).clamp(0.0,1.0).toDouble();
              return Container(
                margin:const EdgeInsets.symmetric(horizontal:18),
                padding:const EdgeInsets.fromLTRB(12,9,12,10),
                decoration:BoxDecoration(
                  color:const Color(0xD9000000),
                  borderRadius:BorderRadius.circular(18),
                  border:Border.all(color:const Color(0x66FFFFFF)),
                ),
                child:Column(mainAxisSize:MainAxisSize.min,children:[
                  Row(children:[
                    Expanded(child:Text('@${r['inviterName']??'NgelX'}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFFFF6B8A),fontWeight:FontWeight.w900))),
                    Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:5),decoration:BoxDecoration(color:Colors.white12,borderRadius:BorderRadius.circular(12)),child:Text('PK $dk:$sn',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900))),
                    Expanded(child:Text('@${r['inviteeName']??'NgelX'}',textAlign:TextAlign.right,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF4DD6FF),fontWeight:FontWeight.w900))),
                  ]),
                  const SizedBox(height:7),
                  Row(children:[
                    Text('$scoreA',style:const TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
                    const SizedBox(width:8),
                    Expanded(child:ClipRRect(borderRadius:BorderRadius.circular(8),child:LinearProgressIndicator(value:aOran,minHeight:9,backgroundColor:const Color(0xFF30BEEA),color:const Color(0xFFFF3E6C)))),
                    const SizedBox(width:8),
                    Text('$scoreB',style:const TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
                  ]),
                ]),
              );
            },
          ),
        );
      },
    );
  }

  @override Widget build(BuildContext context){
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId).snapshots(),
      builder:(_,liveSnap){
        final live=liveSnap.data?.data()??<String,dynamic>{};
        final session=(live['pkSessionId']??'').toString();
        if(live['pkActive']==true&&session.isNotEmpty)return _aktifPk(live,session);
        if(!widget.yayinSahibi)return const SizedBox.shrink();

        return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('live_pk_requests').where('inviteeLiveId',isEqualTo:widget.liveId).limit(10).snapshots(),
          builder:(_,snap){
            final now=DateTime.now();
            QueryDocumentSnapshot<Map<String,dynamic>>? bekleyen;
            for(final d in snap.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[]){
              final v=d.data();
              if((v['status']??'')!='pending')continue;
              final exp=v['requestExpiresAt'];
              if(exp is Timestamp&&exp.toDate().isBefore(now)){
                unawaited(d.reference.set({'status':'expired'},SetOptions(merge:true)));
                continue;
              }
              bekleyen=d;
              break;
            }
            if(bekleyen==null)return const SizedBox.shrink();
            final v=bekleyen.data();
            return Container(
              margin:const EdgeInsets.symmetric(horizontal:18),
              padding:const EdgeInsets.all(12),
              decoration:BoxDecoration(color:const Color(0xEE151515),borderRadius:BorderRadius.circular(18),border:Border.all(color:const Color(0xFFFF1744),width:1.3)),
              child:Row(children:[
                const CircleAvatar(backgroundColor:Color(0xFFFF1744),child:Icon(Icons.sports_mma_rounded,color:Colors.white)),
                const SizedBox(width:10),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text('@${v['inviterName']??'NgelX'} PK isteği gönderdi',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900)),
                  const Text('3 dakikalık canlı yayın yarışı',style:TextStyle(color:Colors.white70,fontSize:11)),
                ])),
                IconButton.filledTonal(onPressed:_bitiriliyor?null:()=>_karar(bekleyen!.id,false),icon:const Icon(Icons.close_rounded)),
                const SizedBox(width:5),
                IconButton.filled(onPressed:_bitiriliyor?null:()=>_karar(bekleyen!.id,true),style:IconButton.styleFrom(backgroundColor:const Color(0xFFFF1744)),icon:const Icon(Icons.check_rounded)),
              ]),
            );
          },
        );
      },
    );
  }
}

class NgelXCanliPkButonu extends StatelessWidget{
  final String liveId;
  final String ownerUid;
  const NgelXCanliPkButonu({super.key,required this.liveId,required this.ownerUid});
  @override Widget build(BuildContext context)=>IconButton.filledTonal(
    tooltip:'PK / Canlı Yayın Maçı',
    onPressed:()=>ngelxCanliPkIstekPaneli(context,liveId:liveId,ownerUid:ownerUid),
    icon:const Icon(Icons.sports_mma_rounded),
  );
}
