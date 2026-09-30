part of 'main.dart';

String ngelxCanliPkBelgeId(String a,String b){
  final x=a.compareTo(b)<=0?a:b;
  final y=a.compareTo(b)<=0?b:a;
  return ngelxBildirimBelgeId('pk_${x}_${y}');
}

Map<String,dynamic> _ngelxPkTemizleAlanlari()=> <String,dynamic>{
  'pkActive':false,
  'pkSessionId':FieldValue.delete(),
  'pkOpponentLiveId':FieldValue.delete(),
  'pkOpponentUid':FieldValue.delete(),
  'pkEndsAt':FieldValue.delete(),
  'pkStartLikeSelf':FieldValue.delete(),
  'pkStartGiftSelf':FieldValue.delete(),
  'pkStartLikeOpponent':FieldValue.delete(),
  'pkStartGiftOpponent':FieldValue.delete(),
  'pkSelfName':FieldValue.delete(),
  'pkOpponentName':FieldValue.delete(),
};

Future<Map<String,int>> _ngelxPkHamSkor(String liveId)async{
  var kalp=0,hediye=0;
  try{
    final sonuc=await Future.wait([
      FirebaseFirestore.instance.collection('live_streams').doc(liveId).collection('reactions').get(),
      FirebaseFirestore.instance.collection('live_streams').doc(liveId).collection('comments').get(),
    ]);
    final rs=sonuc[0] as QuerySnapshot<Map<String,dynamic>>;
    final cs=sonuc[1] as QuerySnapshot<Map<String,dynamic>>;
    for(final d in rs.docs)kalp+=(d.data()['count'] as num?)?.toInt()??1;
    for(final d in cs.docs){
      final v=d.data();
      if(v['kind']=='gift')hediye+=(v['points'] as num?)?.toInt()??0;
    }
  }catch(_){}
  return <String,int>{'likes':kalp,'gifts':hediye};
}

Future<void> ngelxCanliPkYayindanCik(String liveId)async{
  if(liveId.isEmpty)return;
  final me=FirebaseAuth.instance.currentUser?.uid;
  if(me==null)return;
  try{
    final liveRef=FirebaseFirestore.instance.collection('live_streams').doc(liveId);
    final live=await liveRef.get();
    final lv=live.data()??<String,dynamic>{};
    if((lv['ownerId']??'').toString()!=me)return;
    final sessionId=(lv['pkSessionId']??'').toString();
    if(sessionId.isNotEmpty){
      final sessionRef=FirebaseFirestore.instance.collection('calls').doc(sessionId);
      try{
        final session=await sessionRef.get();
        if(session.exists){
          await sessionRef.set({
            'status':'ended',
            'endReason':'live_ended',
            'endedAt':FieldValue.serverTimestamp(),
          },SetOptions(merge:true));
        }
      }catch(_){}
    }
    await liveRef.set(_ngelxPkTemizleAlanlari(),SetOptions(merge:true));
  }catch(_){}
}

Future<void> ngelxCanliPkIstekPaneli(
  BuildContext context,{
  required String liveId,
  required String ownerUid,
}) async {
  if(liveId.isEmpty||ownerUid.isEmpty)return;
  final user=FirebaseAuth.instance.currentUser;
  if(user==null||user.uid!=ownerUid)return;

  final mevcut=await FirebaseFirestore.instance.collection('live_streams').doc(liveId).get();
  final mv=mevcut.data()??<String,dynamic>{};
  if(!ngelxCanliKaydiTaze(mv)){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayın aktif değil.')));
    return;
  }
  if(mv['pkActive']==true){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Zaten aktif bir PK yarışındasın.')));
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
                              final ref=FirebaseFirestore.instance.collection('calls').doc(id);
                              final mevcutIstek=await ref.get();
                              final durum=(mevcutIstek.data()?['status']??'').toString();
                              if(durum=='pending'||durum=='active'){
                                if(sheetContext.mounted)ScaffoldMessenger.of(sheetContext).showSnackBar(const SnackBar(content:Text('Bu yayıncıyla zaten açık bir PK isteği var.')));
                                return;
                              }
                              await ref.set({
                                'type':'live_pk',
                                'members':<String>[ownerUid,hedefUid],
                                'startedBy':ownerUid,
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
                              try{
                                await FirebaseFirestore.instance.collection('live_streams').doc(liveId).set({
                                  'pkInviteStatus':'pending',
                                  'pkInviteSessionId':id,
                                  'pkInviteToLiveId':d.id,
                                  'pkInviteToUid':hedefUid,
                                  'pkInviteExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(seconds:45))),
                                },SetOptions(merge:true));
                              }catch(_){}
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
  bool _islem=false;

  @override void initState(){
    super.initState();
    _sayac=Timer.periodic(const Duration(seconds:1),(_){if(mounted)setState((){});});
  }
  @override void dispose(){_sayac?.cancel();super.dispose();}

  Future<void> _canliyaPkYaz({
    required String sessionId,
    required Map<String,dynamic> session,
    required Map<String,dynamic> self,
    required Map<String,dynamic> opponent,
  })async{
    final selfId=widget.liveId;
    final aId=(session['inviterLiveId']??'').toString();
    final isA=selfId==aId;
    final opponentId=isA?(session['inviteeLiveId']??'').toString():(session['inviterLiveId']??'').toString();
    final ends=session['endsAt'];
    if(opponentId.isEmpty||ends is! Timestamp)return;
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null||(self['ownerId']??'').toString()!=me)return;
    await FirebaseFirestore.instance.collection('live_streams').doc(selfId).set({
      'pkActive':true,
      'pkSessionId':sessionId,
      'pkOpponentLiveId':opponentId,
      'pkOpponentUid':(opponent['ownerId']??'').toString(),
      'pkEndsAt':ends,
      'pkStartLikeSelf':isA?(session['startLikeA']??0):(session['startLikeB']??0),
      'pkStartGiftSelf':isA?(session['startGiftA']??0):(session['startGiftB']??0),
      'pkStartLikeOpponent':isA?(session['startLikeB']??0):(session['startLikeA']??0),
      'pkStartGiftOpponent':isA?(session['startGiftB']??0):(session['startGiftA']??0),
      'pkSelfName':isA?(session['inviterName']??'NgelX'):(session['inviteeName']??'NgelX'),
      'pkOpponentName':isA?(session['inviteeName']??'NgelX'):(session['inviterName']??'NgelX'),
      'pkInviteStatus':FieldValue.delete(),
      'pkInviteSessionId':FieldValue.delete(),
      'pkInviteToLiveId':FieldValue.delete(),
      'pkInviteToUid':FieldValue.delete(),
      'pkInviteExpiresAt':FieldValue.delete(),
    },SetOptions(merge:true));
  }

  Future<void> _kendiPkTemizle()async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null)return;
    try{
      final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId);
      final doc=await ref.get();
      if((doc.data()?['ownerId']??'').toString()!=me)return;
      await ref.set({
        ..._ngelxPkTemizleAlanlari(),
        'pkInviteStatus':FieldValue.delete(),
        'pkInviteSessionId':FieldValue.delete(),
        'pkInviteToLiveId':FieldValue.delete(),
        'pkInviteToUid':FieldValue.delete(),
        'pkInviteExpiresAt':FieldValue.delete(),
      },SetOptions(merge:true));
    }catch(_){}
  }

  Future<void> _karar(String requestId,bool kabul)async{
    if(_islem)return;
    _islem=true;
    try{
      final me=FirebaseAuth.instance.currentUser?.uid;
      if(me==null)return;
      final ref=FirebaseFirestore.instance.collection('calls').doc(requestId);
      final r=await ref.get(const GetOptions(source:Source.server));
      final v=r.data()??<String,dynamic>{};
      if((v['type']??'')!='live_pk'||(v['status']??'')!='pending'||(v['inviteeUid']??'').toString()!=me)return;
      final aId=(v['inviterLiveId']??'').toString();
      final bId=(v['inviteeLiveId']??'').toString();
      if(aId.isEmpty||bId.isEmpty||bId!=widget.liveId)return;

      if(!kabul){
        await ref.set({'status':'rejected','answeredAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
        unawaited(uygulamaBildirimiGonder(
          toUid:(v['inviterUid']??'').toString(),
          fromUid:me,
          tur:'live',
          metin:'PK isteğini reddetti',
          belgeId:bId,
          hedefTuru:'live',
          olayTuru:'live_pk_rejected',
          dedupeKey:'live_pk_rejected_$requestId',
        ).catchError((_){ }));
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
      final hamSkorlar=await Future.wait([_ngelxPkHamSkor(aId),_ngelxPkHamSkor(bId)]);
      final startLikeA=hamSkorlar[0]['likes']??0;
      final startLikeB=hamSkorlar[1]['likes']??0;
      final startGiftA=hamSkorlar[0]['gifts']??0;
      final startGiftB=hamSkorlar[1]['gifts']??0;

      await ref.set({
        'status':'active',
        'answeredAt':FieldValue.serverTimestamp(),
        'startedAt':FieldValue.serverTimestamp(),
        'clientStartedAt':Timestamp.fromDate(now),
        'endsAt':ends,
        'startLikeA':startLikeA,
        'startLikeB':startLikeB,
        'startGiftA':startGiftA,
        'startGiftB':startGiftB,
      },SetOptions(merge:true));

      final session=<String,dynamic>{
        ...v,
        'status':'active',
        'endsAt':ends,
        'startLikeA':startLikeA,
        'startLikeB':startLikeB,
        'startGiftA':startGiftA,
        'startGiftB':startGiftB,
      };
      await _canliyaPkYaz(sessionId:requestId,session:session,self:b,opponent:a);

      unawaited(uygulamaBildirimiGonder(
        toUid:(v['inviterUid']??'').toString(),
        fromUid:me,
        tur:'live',
        metin:'PK isteğini kabul etti',
        belgeId:bId,
        hedefTuru:'live',
        olayTuru:'live_pk_accept',
        dedupeKey:'live_pk_accept_$requestId',
      ).catchError((_){ }));
    }finally{
      _islem=false;
      if(mounted)setState((){});
    }
  }

  Future<void> _pkBitir(String sessionId,Map<String,dynamic> live,Map<String,dynamic> opponent)async{
    if(_islem)return;
    _islem=true;
    try{
      final me=FirebaseAuth.instance.currentUser?.uid;
      if(me==null||(live['ownerId']??'').toString()!=me)return;
      final selfScore=((live['likeCount'] as num?)?.toInt()??0)-((live['pkStartLikeSelf'] as num?)?.toInt()??0)
        +((((live['giftPoints'] as num?)?.toInt()??0)-((live['pkStartGiftSelf'] as num?)?.toInt()??0))~/10);
      final opponentScore=((opponent['likeCount'] as num?)?.toInt()??0)-((live['pkStartLikeOpponent'] as num?)?.toInt()??0)
        +((((opponent['giftPoints'] as num?)?.toInt()??0)-((live['pkStartGiftOpponent'] as num?)?.toInt()??0))~/10);
      try{
        await FirebaseFirestore.instance.collection('calls').doc(sessionId).set({
          'status':'ended',
          'endedAt':FieldValue.serverTimestamp(),
          'endedBy':me,
          'finalScoreByUid':<String,int>{me:selfScore,(opponent['ownerId']??'opponent').toString():opponentScore},
        },SetOptions(merge:true));
      }catch(_){}
      await _kendiPkTemizle();
    }finally{
      _islem=false;
      if(mounted)setState((){});
    }
  }

  Widget _aktifPk(Map<String,dynamic> live,String sessionId){
    final opponentId=(live['pkOpponentLiveId']??'').toString();
    if(opponentId.isEmpty)return const SizedBox.shrink();
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(opponentId).snapshots(),
      builder:(_,oppSnap){
        final opponent=oppSnap.data?.data()??<String,dynamic>{};
        final selfScore=((live['likeCount'] as num?)?.toInt()??0)-((live['pkStartLikeSelf'] as num?)?.toInt()??0)
          +((((live['giftPoints'] as num?)?.toInt()??0)-((live['pkStartGiftSelf'] as num?)?.toInt()??0))~/10);
        final opponentScore=((opponent['likeCount'] as num?)?.toInt()??0)-((live['pkStartLikeOpponent'] as num?)?.toInt()??0)
          +((((opponent['giftPoints'] as num?)?.toInt()??0)-((live['pkStartGiftOpponent'] as num?)?.toInt()??0))~/10);
        final ends=live['pkEndsAt'];
        var kalan=180;
        if(ends is Timestamp)kalan=ends.toDate().difference(DateTime.now()).inSeconds.clamp(0,180).toInt();
        if((kalan<=0||!ngelxCanliKaydiTaze(opponent))&&widget.yayinSahibi&&!_islem){
          unawaited(_pkBitir(sessionId,live,opponent));
        }
        final dk=(kalan~/60).toString().padLeft(2,'0'),sn=(kalan%60).toString().padLeft(2,'0');
        final toplam=(selfScore+opponentScore).clamp(1,1<<30);
        final selfOran=(selfScore/toplam).clamp(0.0,1.0).toDouble();
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
              Expanded(child:Text('@${live['pkSelfName']??'NgelX'}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFFFF6B8A),fontWeight:FontWeight.w900))),
              Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:5),decoration:BoxDecoration(color:Colors.white12,borderRadius:BorderRadius.circular(12)),child:Text('PK $dk:$sn',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900))),
              Expanded(child:Text('@${live['pkOpponentName']??opponent['username']??'NgelX'}',textAlign:TextAlign.right,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF4DD6FF),fontWeight:FontWeight.w900))),
            ]),
            const SizedBox(height:7),
            Row(children:[
              Text('$selfScore',style:const TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
              const SizedBox(width:8),
              Expanded(child:ClipRRect(borderRadius:BorderRadius.circular(8),child:LinearProgressIndicator(value:selfOran,minHeight:9,backgroundColor:const Color(0xFF30BEEA),color:const Color(0xFFFF3E6C)))),
              const SizedBox(width:8),
              Text('$opponentScore',style:const TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
            ]),
          ]),
        );
      },
    );
  }

  Future<void> _aktifOturumuSenkronla(DocumentSnapshot<Map<String,dynamic>> d,Map<String,dynamic> live)async{
    final v=d.data()??<String,dynamic>{};
    final status=(v['status']??'').toString();
    final aId=(v['inviterLiveId']??'').toString();
    final bId=(v['inviteeLiveId']??'').toString();
    if(widget.liveId!=aId&&widget.liveId!=bId)return;

    if(status=='active'){
      if(live['pkActive']==true&&(live['pkSessionId']??'').toString()==d.id)return;
      final oppId=widget.liveId==aId?bId:aId;
      if(oppId.isEmpty)return;
      final opp=await FirebaseFirestore.instance.collection('live_streams').doc(oppId).get();
      final self=await FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId).get();
      final sv=self.data()??<String,dynamic>{},ov=opp.data()??<String,dynamic>{};
      if(!ngelxCanliKaydiTaze(sv)||!ngelxCanliKaydiTaze(ov))return;
      await _canliyaPkYaz(sessionId:d.id,session:v,self:sv,opponent:ov);
      return;
    }

    if((live['pkSessionId']??'').toString()==d.id&&live['pkActive']==true){
      await _kendiPkTemizle();
    }
  }

  @override Widget build(BuildContext context){
    final me=FirebaseAuth.instance.currentUser?.uid??'';
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId).snapshots(),
      builder:(_,liveSnap){
        final live=liveSnap.data?.data()??<String,dynamic>{};
        final session=(live['pkSessionId']??'').toString();
        if(live['pkActive']==true&&session.isNotEmpty){
          if(widget.yayinSahibi&&me.isNotEmpty){
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              stream:FirebaseFirestore.instance.collection('calls').doc(session).snapshots(),
              builder:(_,callSnap){
                final cv=callSnap.data?.data()??<String,dynamic>{};
                final status=(cv['status']??'').toString();
                if(callSnap.hasData&&status!='active'&&!_islem)unawaited(_kendiPkTemizle());
                return _aktifPk(live,session);
              },
            );
          }
          return _aktifPk(live,session);
        }

        if(!widget.yayinSahibi||me.isEmpty)return const SizedBox.shrink();

        return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('calls').where('members',arrayContains:me).limit(40).snapshots(),
          builder:(_,snap){
            final now=DateTime.now();
            QueryDocumentSnapshot<Map<String,dynamic>>? bekleyen;
            QueryDocumentSnapshot<Map<String,dynamic>>? aktif;
            QueryDocumentSnapshot<Map<String,dynamic>>? giden;
            for(final d in snap.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[]){
              final v=d.data();
              if((v['type']??'')!='live_pk')continue;
              final a=(v['inviterLiveId']??'').toString(),b=(v['inviteeLiveId']??'').toString();
              if(widget.liveId!=a&&widget.liveId!=b)continue;
              final status=(v['status']??'').toString();
              if(status=='active'){aktif=d;break;}
              if(status!='pending')continue;
              final exp=v['requestExpiresAt'];
              if(exp is Timestamp&&exp.toDate().isBefore(now)){
                if((v['startedBy']??'').toString()==me)unawaited(d.reference.set({'status':'expired'},SetOptions(merge:true)));
                continue;
              }
              if((v['inviteeLiveId']??'').toString()==widget.liveId&&(v['inviteeUid']??'').toString()==me)bekleyen=d;
              if((v['inviterLiveId']??'').toString()==widget.liveId&&(v['inviterUid']??'').toString()==me)giden=d;
            }

            if(aktif!=null){
              if(!_islem)unawaited(_aktifOturumuSenkronla(aktif!,live));
              return const SizedBox.shrink();
            }

            if(bekleyen!=null){
              final v=bekleyen!.data();
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
                  IconButton.filledTonal(onPressed:_islem?null:()=>_karar(bekleyen!.id,false),icon:const Icon(Icons.close_rounded)),
                  const SizedBox(width:5),
                  IconButton.filled(onPressed:_islem?null:()=>_karar(bekleyen!.id,true),style:IconButton.styleFrom(backgroundColor:const Color(0xFFFF1744)),icon:const Icon(Icons.check_rounded)),
                ]),
              );
            }

            if(giden!=null){
              final v=giden!.data();
              return Container(
                margin:const EdgeInsets.symmetric(horizontal:18),
                padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),
                decoration:BoxDecoration(color:const Color(0xCC151515),borderRadius:BorderRadius.circular(16)),
                child:Row(children:[
                  const SizedBox(width:16,height:16,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFFFF1744))),
                  const SizedBox(width:9),
                  Expanded(child:Text('@${v['inviteeName']??'NgelX'} PK isteğini yanıtlıyor…',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800))),
                ]),
              );
            }
            return const SizedBox.shrink();
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

class NgelXCanliPkGoruntuKatmani extends StatelessWidget{
  final String liveId;
  final Widget child;
  const NgelXCanliPkGoruntuKatmani({super.key,required this.liveId,required this.child});
  @override Widget build(BuildContext context){
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(liveId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        final opponent=(v['pkOpponentLiveId']??'').toString();
        if(v['pkActive']!=true||opponent.isEmpty)return child;
        return Row(children:[
          Expanded(child:ClipRect(child:child)),
          Container(width:1,color:Colors.white24),
          Expanded(child:NgelXPkRakipVideo(liveId:opponent)),
        ]);
      },
    );
  }
}

class NgelXPkRakipVideo extends StatefulWidget{
  final String liveId;
  const NgelXPkRakipVideo({super.key,required this.liveId});
  @override State<NgelXPkRakipVideo> createState()=>_NgelXPkRakipVideoState();
}

class _NgelXPkRakipVideoState extends State<NgelXPkRakipVideo>{
  lk.Room? _oda;
  String _ownerUid='';
  bool _baglaniyor=false;
  String? _hata;

  @override void initState(){
    super.initState();
    unawaited(_baglan());
  }

  @override void didUpdateWidget(covariant NgelXPkRakipVideo oldWidget){
    super.didUpdateWidget(oldWidget);
    if(oldWidget.liveId!=widget.liveId)unawaited(_baglan());
  }

  Future<void> _temizle()async{
    final eski=_oda;
    _oda=null;
    if(eski!=null){
      eski.removeListener(_yenile);
      try{await eski.disconnect();}catch(_){}
      try{await eski.dispose();}catch(_){}
    }
  }

  Future<void> _baglan()async{
    if(_baglaniyor)return;
    _baglaniyor=true;
    _hata=null;
    await _temizle();
    if(mounted)setState((){});
    try{
      final live=await FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId).get(const GetOptions(source:Source.server));
      final v=live.data()??<String,dynamic>{};
      if(!ngelxCanliKaydiTaze(v))throw Exception('Rakip yayın sona erdi');
      final roomName=(v['roomName']??'').toString();
      _ownerUid=(v['ownerId']??'').toString();
      if(roomName.isEmpty)throw Exception('Rakip yayın odası bulunamadı');
      final me=FirebaseAuth.instance.currentUser?.uid??'viewer';
      final kaynak=lk.DevelopmentTokenSource(id:liveKitTestSunucuId);
      final token=await kaynak.fetch(lk.TokenRequestOptions(
        roomName:roomName,
        participantIdentity:'$me-pk-${DateTime.now().microsecondsSinceEpoch}',
        participantName:'PK izleyicisi',
        participantAttributes:const {'role':'pk_viewer'},
      ));
      final room=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
      room.addListener(_yenile);
      await room.connect(token.serverUrl,token.participantToken);
      if(!mounted){
        try{await room.disconnect();await room.dispose();}catch(_){}
        return;
      }
      _oda=room;
      setState((){});
    }catch(e){
      _hata=e.toString();
      if(mounted)setState((){});
    }finally{
      _baglaniyor=false;
    }
  }

  void _yenile(){if(mounted)setState((){});}

  lk.VideoTrack? _track(){
    final room=_oda;
    if(room==null)return null;
    for(final p in room.remoteParticipants.values){
      if(_ownerUid.isNotEmpty&&p.identity!=_ownerUid)continue;
      for(final pub in p.videoTrackPublications){
        if(pub.subscribed&&!pub.muted&&pub.track is lk.VideoTrack)return pub.track as lk.VideoTrack;
      }
    }
    for(final p in room.remoteParticipants.values){
      for(final pub in p.videoTrackPublications){
        if(pub.subscribed&&!pub.muted&&pub.track is lk.VideoTrack)return pub.track as lk.VideoTrack;
      }
    }
    return null;
  }

  @override void dispose(){
    unawaited(_temizle());
    super.dispose();
  }

  @override Widget build(BuildContext context){
    final track=_track();
    if(track==null){
      return ColoredBox(
        color:const Color(0xFF101014),
        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          if(_baglaniyor)const CircularProgressIndicator(color:Color(0xFF4DD6FF))
          else const Icon(Icons.videocam_off_rounded,color:Colors.white54,size:48),
          const SizedBox(height:10),
          Text(_hata==null?'Rakip görüntüsü bağlanıyor…':'Rakip görüntüsü bekleniyor',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
        ])),
      );
    }
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.liveId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        return ngelxCanliEfektKatmani(
          veri:v,
          child:lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover),
        );
      },
    );
  }
}
