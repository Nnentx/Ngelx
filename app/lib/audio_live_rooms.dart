part of 'main.dart';

const int ngelxSesliMaksKonusmaci=12;
const int ngelxSesliMaksModerator=3;

bool ngelxSesliOdaTaze(Map<String,dynamic> v){
  if(v['active']!=true)return false;
  final h=v['lastHeartbeatAt']??v['startedAt'];
  if(h is! Timestamp)return true;
  final s=DateTime.now().difference(h.toDate()).inSeconds;
  return s>=-30&&s<=45;
}

Future<void> ngelxSesliOdayaKatil(BuildContext context,String odaId)async{
  if(odaId.isEmpty||await misafirEngeli(context))return;
  final user=FirebaseAuth.instance.currentUser;if(user==null)return;
  lk.Room? oda;
  try{
    final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
    final v=d.data()??<String,dynamic>{};
    if(!d.exists||!ngelxSesliOdaTaze(v)){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu sesli oda sona erdi.')));return;
    }
    final gizlilik=(v['visibility']??'public').toString(),owner=(v['ownerId']??'').toString();
    final yasaklilar=List<String>.from(v['bannedUserIds']??const[]);
    if(yasaklilar.contains(user.uid)){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('ADMIN bu odaya tekrar girişini engelledi.')));
      return;
    }
    if(gizlilik!='public'&&owner!=user.uid){
      final p=(await FirebaseFirestore.instance.collection('users').doc(owner).get()).data()??<String,dynamic>{};
      final izin=gizlilik=='friends'?List<String>.from(p['friends']??const[]).contains(user.uid):List<String>.from(p['followers']??const[]).contains(user.uid);
      if(!izin){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu sesli odaya katılma iznin yok.')));return;}
    }
    final roomName=(v['roomName']??'').toString();if(roomName.isEmpty)throw StateError('room_name');
    final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
    final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString(),foto=(p['photoUrl']??'').toString();
    String serverUrl='',participantToken='';
    Object? sonHata;
    for(var deneme=1;deneme<=3;deneme++){
      lk.Room? aday;
      try{
        final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId)
            .fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:const {'role':'listener','mode':'audio'}))
            .timeout(const Duration(seconds:12));
        aday=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
        await aday.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:22));
        if(aday.connectionState!=lk.ConnectionState.connected)throw StateError('livekit_not_connected');
        await aday.localParticipant?.setMicrophoneEnabled(false);
        oda=aday;serverUrl=cevap.serverUrl;participantToken=cevap.participantToken;
        sonHata=null;
        break;
      }catch(e){
        sonHata=e;
        if(aday!=null){try{await aday.disconnect();}catch(_){}try{await aday.dispose();}catch(_){}}
        if(deneme<3)await Future.delayed(Duration(milliseconds:650*deneme));
      }
    }
    if(oda==null||oda.connectionState!=lk.ConnectionState.connected)throw StateError('livekit_join_failed:$sonHata');
    await ngelxSesliKatilimciYaz(roomId:odaId,uid:user.uid,ad:ad,foto:foto,rol:'listener');
    if(!context.mounted){await oda.disconnect();await oda.dispose();return;}
    await Navigator.push(context,MaterialPageRoute(settings:RouteSettings(name:'/audio_room/$odaId'),builder:(_)=>SesliOdaPage(oda:oda!,odaId:odaId,ownerId:owner,baslik:(v['title']??'Sesli oda').toString(),yayinSahibi:false,serverUrl:serverUrl,participantToken:participantToken)));
  }catch(_){
    if(oda!=null){try{await oda.disconnect();await oda.dispose();}catch(_){} }
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli odaya bağlanılamadı.')));
  }
}

List<Widget> ngelxSesliKesfetSliverleri(BuildContext context)=>[
  const SliverToBoxAdapter(child:Padding(padding:EdgeInsets.fromLTRB(16,18,16,10),child:Text('Sesli odalar',style:TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)))),
  SliverToBoxAdapter(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
    stream:FirebaseFirestore.instance.collection('audio_rooms').where('active',isEqualTo:true).limit(30).snapshots(),
    builder:(_,s){
      if(s.connectionState==ConnectionState.waiting)return const SizedBox(height:180,child:Center(child:CircularProgressIndicator(color:mor)));
      final docs=(s.data?.docs??[]).where((d)=>ngelxSesliOdaTaze(d.data())).toList();
      if(docs.isEmpty)return Container(height:170,margin:const EdgeInsets.symmetric(horizontal:16),decoration:BoxDecoration(color:const Color(0xFFFAF8FD),borderRadius:BorderRadius.circular(22)),child:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.mic_none_rounded,color:mor,size:38),SizedBox(height:8),Text('Henüz açık sesli oda yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),Text('İlk sesli odayı sen başlatabilirsin.',style:TextStyle(color:Colors.black45,fontSize:12))])));
      return SizedBox(height:190,child:ListView.separated(padding:const EdgeInsets.symmetric(horizontal:16),scrollDirection:Axis.horizontal,itemCount:docs.length,separatorBuilder:(_,__)=>const SizedBox(width:10),itemBuilder:(_,i){
        final d=docs[i],v=d.data(),foto=(v['ownerPhotoUrl']??'').toString();
        return InkWell(borderRadius:BorderRadius.circular(22),onTap:()=>ngelxSesliOdayaKatil(context,d.id),child:Container(width:260,padding:const EdgeInsets.all(15),decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE4D8FA)),boxShadow:const [BoxShadow(color:Color(0x10000000),blurRadius:14,offset:Offset(0,6))]),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
          Row(children:[CircleAvatar(radius:22,backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.mic_rounded,color:mor):null),const SizedBox(width:9),Expanded(child:Text((v['ownerName']??'NgelX').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w900))),const Icon(Icons.graphic_eq_rounded,color:mor)]),
          const SizedBox(height:12),Text((v['title']??'Sesli oda').toString(),maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black,fontSize:17,fontWeight:FontWeight.w900)),const Spacer(),
          Row(children:[const Icon(Icons.headphones_rounded,size:16,color:Colors.black45),const SizedBox(width:4),Text('${v['listenerCount']??0}',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)),const SizedBox(width:12),const Icon(Icons.mic_rounded,size:16,color:mor),const SizedBox(width:4),Text('${v['speakerCount']??1}/12',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)),const Spacer(),Text((v['category']??'Sohbet').toString(),style:const TextStyle(color:Colors.black45,fontSize:11,fontWeight:FontWeight.w700))]),
        ])));
      }));
    },
  )),
];

class SesliOdaHazirlikPage extends StatefulWidget{const SesliOdaHazirlikPage({super.key});@override State<SesliOdaHazirlikPage> createState()=>_SesliOdaHazirlikPageState();}
class _SesliOdaHazirlikPageState extends State<SesliOdaHazirlikPage>{
  final baslik=TextEditingController();String kategori='Sohbet',gizlilik='public';bool baslatiliyor=false;
  @override void dispose(){baslik.dispose();super.dispose();}
  Future<void> baslat()async{
    final user=FirebaseAuth.instance.currentUser;if(user==null||baslatiliyor)return;
    if(baslik.text.trim().length<3){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('En az 3 karakterlik oda başlığı yaz.')));return;}
    if(!(await Permission.microphone.request()).isGranted)return;
    setState(()=>baslatiliyor=true);lk.Room? oda;
    try{
      final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
      final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString(),foto=(p['photoUrl']??'').toString(),roomName='ngelx_audio_${user.uid}_${DateTime.now().millisecondsSinceEpoch}';
      final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId).fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:const {'role':'host','mode':'audio'}));
      oda=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));await oda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:18));await oda.localParticipant?.setMicrophoneEnabled(true);
      final d=await FirebaseFirestore.instance.collection('audio_rooms').add({'roomName':roomName,'ownerId':user.uid,'ownerName':ad,'ownerPhotoUrl':foto,'title':baslik.text.trim(),'category':kategori,'visibility':gizlilik,'active':true,'startedAt':FieldValue.serverTimestamp(),'lastHeartbeatAt':FieldValue.serverTimestamp(),'speakerIds':[user.uid],'moderatorIds':<String>[],'bannedUserIds':<String>[],'chatMutedUserIds':<String>[],'speakerCount':1,'listenerCount':0,'maxSpeakers':ngelxSesliMaksKonusmaci,'maxModerators':ngelxSesliMaksModerator,'mode':'audio'});
      await ngelxSesliKatilimciYaz(roomId:d.id,uid:user.uid,ad:ad,foto:foto,rol:'speaker');
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'isAudioLive':true,'currentAudioRoomId':d.id,'audioRoomTitle':baslik.text.trim()},SetOptions(merge:true));
      unawaited(ngelxSesliOdaBaslangicBildirimi(roomId:d.id,baslik:baslik.text.trim()));
      if(!mounted)return;Navigator.pushReplacement(context,MaterialPageRoute(settings:RouteSettings(name:'/audio_room/'+d.id),builder:(_)=>SesliOdaPage(oda:oda!,odaId:d.id,ownerId:user.uid,baslik:baslik.text.trim(),yayinSahibi:true,serverUrl:cevap.serverUrl,participantToken:cevap.participantToken)));
    }catch(_){if(oda!=null){try{await oda.disconnect();await oda.dispose();}catch(_){} }if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli oda başlatılamadı.')));}finally{if(mounted)setState(()=>baslatiliyor=false);}
  }
  @override Widget build(BuildContext context)=>Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,foregroundColor:Colors.black,title:const Text('Sesli oda oluştur',style:TextStyle(fontWeight:FontWeight.w900))),body:SafeArea(child:ListView(padding:const EdgeInsets.all(18),children:[
    Container(padding:const EdgeInsets.all(18),decoration:BoxDecoration(color:const Color(0xFFF6F0FF),borderRadius:BorderRadius.circular(22)),child:const Row(children:[CircleAvatar(radius:26,backgroundColor:mor,child:Icon(Icons.mic_rounded,color:Colors.white)),SizedBox(width:12),Expanded(child:Text('Kamera yok. Ses odakta.\n12 konuşmacıya kadar sahne hazır.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800,height:1.35)))])),const SizedBox(height:18),
    TextField(controller:baslik,maxLength:80,cursorColor:mor,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800),decoration:InputDecoration(labelText:'Oda başlığı',labelStyle:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700),floatingLabelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w800),hintText:'Örn. Akşam sohbeti',hintStyle:const TextStyle(color:Color(0xFF9A9AA2)),counterStyle:const TextStyle(color:Colors.black45),filled:true,fillColor:const Color(0xFFF5F5F8),enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:Color(0xFFE5E2EA))),focusedBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:mor,width:1.5)),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none))),const SizedBox(height:8),
    Wrap(spacing:8,children:['Sohbet','Müzik','Teknoloji','Spor','Gündem'].map((x)=>ChoiceChip(label:Text(x),selected:kategori==x,onSelected:(_)=>setState(()=>kategori=x))).toList()),const SizedBox(height:16),
    Container(
      padding:const EdgeInsets.all(4),
      decoration:BoxDecoration(color:const Color(0xFFF3F1F6),borderRadius:BorderRadius.circular(18)),
      child:Row(children:[
        for(final x in const [('public','Herkes'),('followers','Takipçiler'),('friends','Arkadaşlar')])
          Expanded(child:Padding(
            padding:const EdgeInsets.symmetric(horizontal:2),
            child:InkWell(
              onTap:()=>setState(()=>gizlilik=x.$1),
              borderRadius:BorderRadius.circular(14),
              child:AnimatedContainer(
                duration:const Duration(milliseconds:160),
                height:42,
                alignment:Alignment.center,
                decoration:BoxDecoration(color:gizlilik==x.$1?mor:Colors.transparent,borderRadius:BorderRadius.circular(14)),
                child:FittedBox(fit:BoxFit.scaleDown,child:Text(x.$2,style:TextStyle(color:gizlilik==x.$1?Colors.white:Colors.black54,fontWeight:FontWeight.w900,fontSize:12))),
              ),
            ),
          )),
      ]),
    ),const SizedBox(height:22),
    FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(54)),onPressed:baslatiliyor?null:baslat,icon:baslatiliyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.graphic_eq_rounded),label:Text(baslatiliyor?'Oda açılıyor...':'Sesli odayı başlat',style:const TextStyle(fontWeight:FontWeight.w900))),
  ])));
}

class SesliOdaPage extends StatefulWidget{
  final lk.Room oda;final String odaId,ownerId,baslik,serverUrl,participantToken;final bool yayinSahibi;
  const SesliOdaPage({super.key,required this.oda,required this.odaId,required this.ownerId,required this.baslik,required this.yayinSahibi,required this.serverUrl,required this.participantToken});
  @override State<SesliOdaPage> createState()=>_SesliOdaPageState();
}
class _SesliOdaPageState extends State<SesliOdaPage>{
  late lk.Room aktifOda;
  Timer? heartbeat,yalnizlikTimer;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? abonelik,katilimAboneligi;
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? odaKatilimAboneligi;
  Map<String,dynamic> veri={};
  DateTime? yalnizlikBasladi;
  int yalnizlikKalan=600,aktifKisiSayisi=1;
  bool enAzIkiKisiOldu=false,mikrofon=false,mikrofonTercihi=false,bitti=false,kapatiliyor=false,yeniden=false,kucultulmus=false;
  String durum='';
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);List<String> get moderatorler=>List<String>.from(veri['moderatorIds']??const[]);bool get moderatorum=>uid!=null&&moderatorler.contains(uid);bool get yoneticiyim=>sahibiyim||moderatorum;bool get konusmaciyim=>uid!=null&&speakers.contains(uid);bool get bagli=>aktifOda.connectionState==lk.ConnectionState.connected;
  @override void initState(){
    super.initState();
    aktifOda=widget.oda;
    mikrofon=widget.yayinSahibi;mikrofonTercihi=widget.yayinSahibi;
    aktifOda.addListener(odaDegisti);
    abonelik=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).snapshots().listen((d){
      final v=d.data()??<String,dynamic>{};if(!mounted)return;
      final once=konusmaciyim;
      final yeniBitti=v.isNotEmpty&&v['active']!=true;
      setState((){veri=v;bitti=yeniBitti;if(yeniBitti){durum='';yeniden=false;}});
      if(yeniBitti)unawaited(_odaBittiTemizle());
      if(once&&!konusmaciyim&&mikrofon){mikrofon=false;unawaited(aktifOda.localParticipant?.setMicrophoneEnabled(false));}
      if(sahibiyim&&aktifKisiSayisi<2&&yalnizlikBasladi==null&&!bitti)_yalnizlikBaslat();
    });
    final ben=uid;
    if(ben!=null){
      katilimAboneligi=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('participants').doc(ben).snapshots().listen((d){
        final v=d.data();
        if(v!=null&&v['removed']==true&&!sahibiyim&&!kapatiliyor)unawaited(odadanCikarildi(yasakli:v['banned']==true));
      });
    }
    if(widget.yayinSahibi){
      odaKatilimAboneligi=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('participants').where('active',isEqualTo:true).snapshots().listen((s){
        if(!mounted)return;
        final simdi=DateTime.now();
        var sayi=0;
        for(final d in s.docs){
          final v=d.data(),t=v['lastSeenAt']??v['joinedAt'];
          if(t is! Timestamp||simdi.difference(t.toDate()).inSeconds<=20)sayi++;
        }
        _aktifKisiDegisti(sayi);
      });
    }
    unawaited(kalp());
    heartbeat=Timer.periodic(const Duration(seconds:6),(_)=>unawaited(kalp()));
  }
  void _aktifKisiDegisti(int sayi){
    if(!mounted)return;
    final onceki=aktifKisiSayisi;
    setState(()=>aktifKisiSayisi=sayi);
    if(!sahibiyim||kapatiliyor||bitti)return;
    if(sayi>=2){
      enAzIkiKisiOldu=true;
      _yalnizlikIptal();
      return;
    }
    if(onceki>=2||yalnizlikBasladi==null)_yalnizlikBaslat();
  }
  void _yalnizlikBaslat(){
    if(!sahibiyim||kapatiliyor||bitti||aktifKisiSayisi>=2||yalnizlikBasladi!=null)return;
    final bas=veri['startedAt'];
    yalnizlikBasladi=enAzIkiKisiOldu?DateTime.now():(bas is Timestamp?bas.toDate():DateTime.now());
    yalnizlikTimer?.cancel();
    void tik(){
      if(!mounted||kapatiliyor||bitti||aktifKisiSayisi>=2)return;
      final gecen=DateTime.now().difference(yalnizlikBasladi!).inSeconds;
      final kalan=600-gecen;
      if(kalan<=0){
        yalnizlikTimer?.cancel();
        yalnizlikTimer=null;
        unawaited(_yetersizKatilimciKapat());
        return;
      }
      if(mounted)setState(()=>yalnizlikKalan=kalan);
    }
    tik();
    yalnizlikTimer=Timer.periodic(const Duration(seconds:1),(_)=>tik());
  }
  void _yalnizlikIptal(){
    yalnizlikTimer?.cancel();yalnizlikTimer=null;yalnizlikBasladi=null;
    if(mounted)setState(()=>yalnizlikKalan=600);
  }
  Future<void> _yetersizKatilimciKapat()async{
    ngelxSesliMiniTemizle(widget.odaId);
    if(!sahibiyim||kapatiliyor||bitti||aktifKisiSayisi>=2)return;
    kapatiliyor=true;bitti=true;
    heartbeat?.cancel();yalnizlikTimer?.cancel();
    mikrofon=false;mikrofonTercihi=false;
    try{await aktifOda.localParticipant?.setMicrophoneEnabled(false);}catch(_){}
    final bas=veri['startedAt'];
    final sure=bas is Timestamp?DateTime.now().difference(bas.toDate()).inSeconds:0;
    try{
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({
        'active':false,
        'endedAt':FieldValue.serverTimestamp(),
        'durationSeconds':sure<0?0:sure,
        'endReason':'not_enough_participants',
        'autoClosed':true,
        'minParticipantsRequired':2,
        'autoCloseAfterSeconds':600,
      },SetOptions(merge:true));
    }catch(_){}
    final ben=uid;
    if(ben!=null){
      await ngelxSesliKatilimciAyril(widget.odaId,ben);
      try{await FirebaseFirestore.instance.collection('users').doc(ben).set({'isAudioLive':false,'currentAudioRoomId':FieldValue.delete()},SetOptions(merge:true));}catch(_){}
    }
    try{await aktifOda.disconnect();}catch(_){}
    if(!mounted)return;
    await showDialog<void>(
      context:context,
      barrierDismissible:false,
      builder:(c)=>AlertDialog(
        title:const Text('Sesli oda kapandı'),
        content:const Text('10 dakika boyunca odada en az 2 kişi olmadığı için sesli oda otomatik kapatıldı.'),
        actions:[FilledButton(onPressed:()=>Navigator.pop(c),child:const Text('Tamam'))],
      ),
    );
    if(mounted)Navigator.pop(context);
  }

  Future<void> _odaBittiTemizle()async{
    ngelxSesliMiniTemizle(widget.odaId);
    yalnizlikTimer?.cancel();
    mikrofon=false;mikrofonTercihi=false;
    try{await aktifOda.localParticipant?.setMicrophoneEnabled(false);}catch(_){}
    if(aktifOda.connectionState!=lk.ConnectionState.disconnected){
      try{await aktifOda.disconnect();}catch(_){}
    }
    if(mounted)setState((){durum='';yeniden=false;});
  }
  Future<void> odadanCikarildi({bool yasakli=false})async{
    ngelxSesliMiniTemizle(widget.odaId);
    if(kapatiliyor)return;
    kapatiliyor=true;
    mikrofon=false;mikrofonTercihi=false;
    try{await aktifOda.localParticipant?.setMicrophoneEnabled(false);}catch(_){}
    try{await aktifOda.disconnect();}catch(_){}
    if(mounted){
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(yasakli?'ADMIN bu odaya tekrar girişini engelledi.':'ADMIN veya yönetici seni odadan çıkardı.')));
      Navigator.pop(context);
    }
  }
  void odaDegisti(){
    if(!mounted)return;
    final koptu=aktifOda.connectionState==lk.ConnectionState.disconnected;
    if(koptu&&mikrofon)mikrofon=false;
    setState((){
      if(koptu&&!kapatiliyor&&!bitti)durum='Bağlantı koptu. Yeniden bağlanılıyor...';else if(bitti)durum='';
      if(!koptu&&bagli)durum='';
    });
    if(koptu&&!kapatiliyor&&!bitti)unawaited(tekrarBaglan());
  }
  Future<void> kalp()async{
    if(kapatiliyor||bitti)return;
    final ben=uid;
    if(ben!=null){
      try{await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('participants').doc(ben).set({'active':true,'lastSeenAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}catch(_){}
    }
    if(!widget.yayinSahibi)return;
    try{
      final dinleyici=aktifOda.remoteParticipants.length;
      final onceki=(veri['peakListenerCount'] is num)?(veri['peakListenerCount'] as num).toInt():0;
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({
        'lastHeartbeatAt':FieldValue.serverTimestamp(),
        'listenerCount':dinleyici,
        'peakListenerCount':dinleyici>onceki?dinleyici:onceki,
        'speakerCount':speakers.isEmpty?1:speakers.length,
      },SetOptions(merge:true));
    }catch(_){}
  }
  Future<void> tekrarBaglan()async{
    if(yeniden||kapatiliyor||bitti)return;
    final user=FirebaseAuth.instance.currentUser;if(user==null)return;
    yeniden=true;
    for(var i=1;i<=4;i++){
      if(mounted)setState(()=>durum='Tekrar bağlanılıyor $i/4');
      lk.Room? yeniOda;
      try{
        await Future.delayed(Duration(milliseconds:450*i));
        final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        final v=d.data()??<String,dynamic>{};
        if(!d.exists||v['active']!=true){bitti=true;throw StateError('audio_room_ended');}
        final roomName=(v['roomName']??'').toString();if(roomName.isEmpty)throw StateError('room_name');
        final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
        final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString();
        final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId)
            .fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:{'role':sahibiyim?'host':'listener','mode':'audio'}))
            .timeout(const Duration(seconds:12));

        yeniOda=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
        await yeniOda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:22));
        if(yeniOda.connectionState!=lk.ConnectionState.connected)throw StateError('reconnect_not_connected');

        final eskiOda=aktifOda;
        eskiOda.removeListener(odaDegisti);
        aktifOda=yeniOda;
        aktifOda.addListener(odaDegisti);
        yeniOda=null;

        final micAcik=konusmaciyim&&mikrofonTercihi;
        await aktifOda.localParticipant?.setMicrophoneEnabled(micAcik);
        try{await eskiOda.disconnect();}catch(_){}
        try{await eskiOda.dispose();}catch(_){}

        yeniden=false;
        if(mounted)setState((){mikrofon=micAcik;durum='';});
        return;
      }catch(_){
        if(yeniOda!=null){
          try{await yeniOda.disconnect();}catch(_){}
          try{await yeniOda.dispose();}catch(_){}
        }
      }
    }
    yeniden=false;
    if(mounted)setState((){mikrofon=false;durum=bitti?'':'Bağlantı kurulamadı. Tekrar denemek için dokun.';});
  }
  Future<void> mic()async{
    if(!konusmaciyim)return;
    if(!bagli){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Ses bağlantısı yok. Yeniden bağlanılıyor...')));unawaited(tekrarBaglan());return;}
    final yeni=!mikrofonTercihi;
    if(yeni&&!(await Permission.microphone.request()).isGranted)return;
    try{
      await aktifOda.localParticipant?.setMicrophoneEnabled(yeni);
      if(mounted)setState((){mikrofonTercihi=yeni;mikrofon=yeni;});
    }catch(_){
      if(mounted)setState(()=>mikrofon=false);
      unawaited(tekrarBaglan());
    }
  }
  Future<void> sozIste()async{final ben=uid;if(ben==null||konusmaciyim)return;final p=(await FirebaseFirestore.instance.collection('users').doc(ben).get()).data()??<String,dynamic>{};await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('speaker_requests').doc(ben).set({'userId':ben,'displayName':(p['displayName']??p['username']??'NgelX').toString(),'photoUrl':(p['photoUrl']??'').toString(),'status':'pending','createdAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Söz isteğin gönderildi.')));}
  Future<void> istekler()async{
    if(!yoneticiyim)return;
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
      builder:(c)=>Theme(
        data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),
        child:SafeArea(
          top:false,
          child:SizedBox(
            height:320,
            child:Column(children:[
              Padding(
                padding:const EdgeInsets.fromLTRB(18,0,10,8),
                child:Row(children:[
                  const Icon(Icons.pan_tool_alt_rounded,color:mor),
                  const SizedBox(width:9),
                  const Expanded(child:Text('Söz istekleri',style:TextStyle(color:Colors.black87,fontSize:18,fontWeight:FontWeight.w900))),
                  IconButton(tooltip:'Kapat',onPressed:()=>Navigator.pop(c),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
                ]),
              ),
              const Divider(height:1,color:Color(0xFFEDE8F2)),
              Expanded(
                child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('speaker_requests').where('status',isEqualTo:'pending').limit(30).snapshots(),
                  builder:(_,s){
                    if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
                    if(s.hasError)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:36),SizedBox(height:8),Text('İstekler yüklenemedi.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bağlantını kontrol edip tekrar dene.',style:TextStyle(color:Colors.black45))])));
                    final docs=(s.data?.docs??[]).toList()..sort((a,b){final aa=a.data()['createdAt'],bb=b.data()['createdAt'];final am=aa is Timestamp?aa.millisecondsSinceEpoch:0,bm=bb is Timestamp?bb.millisecondsSinceEpoch:0;return am.compareTo(bm);});
                    if(docs.isEmpty)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.pan_tool_alt_outlined,color:mor,size:38),SizedBox(height:9),Text('Bekleyen söz isteği yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bir dinleyici söz istediğinde burada görünecek.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black45))])));
                    return ListView.separated(
                      padding:const EdgeInsets.symmetric(vertical:6),
                      itemCount:docs.length,
                      separatorBuilder:(_,__)=>const Divider(height:1,indent:70,color:Color(0xFFF0EDF3)),
                      itemBuilder:(_,i){
                        final d=docs[i],v=d.data(),foto=(v['photoUrl']??'').toString();
                        return ListTile(
                          leading:Stack(clipBehavior:Clip.none,children:[CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),Positioned(right:-5,bottom:-5,child:CircleAvatar(radius:9,backgroundColor:mor,child:Text('${i+1}',style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900))))]),
                          title:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
                          subtitle:const Text('Konuşmacı olmak istiyor',style:TextStyle(color:Colors.black45)),
                          trailing:Wrap(spacing:2,children:[
                            IconButton(tooltip:'Kabul et',onPressed:()=>istekSonuc(d.id,true),icon:const Icon(Icons.check_circle_rounded,color:Colors.green)),
                            IconButton(tooltip:'Reddet',onPressed:()=>istekSonuc(d.id,false),icon:const Icon(Icons.cancel_rounded,color:Colors.redAccent)),
                          ]),
                        );
                      },
                    );
                  },
                ),
              ),
            ]),
          ),
        ),
      ),
    );
  }
  Future<void> istekSonuc(String hedef,bool kabul)async{final ref=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId),req=ref.collection('speaker_requests').doc(hedef);if(kabul){await FirebaseFirestore.instance.runTransaction((tx)async{final d=await tx.get(ref),v=d.data()??<String,dynamic>{},sp=List<String>.from(v['speakerIds']??const[]);if(!sp.contains(hedef)&&sp.length>=ngelxSesliMaksKonusmaci)throw StateError('limit');if(!sp.contains(hedef))sp.add(hedef);tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'updatedAt':FieldValue.serverTimestamp()});tx.set(req,{'status':'accepted','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));});}else{await req.set({'status':'declined','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}}
  Future<void> kucult()async{
    if(kapatiliyor)return;
    if(bitti){if(mounted)Navigator.pop(context);return;}
    if(kucultulmus)return;
    final bas=veri['startedAt'];
    ngelxSesliMiniDurum.value=NgelxSesliMiniDurum(
      roomId:widget.odaId,
      baslik:(veri['title']??widget.baslik).toString(),
      baslangic:bas is Timestamp?bas.toDate():null,
      sahibiyim:sahibiyim,
    );
    kucultulmus=true;
    if(!mounted)return;
    await Navigator.push(
      context,
      MaterialPageRoute(
        settings:RouteSettings(name:'/audio_mini_shell/'+widget.odaId),
        builder:(_)=>const AnaEkran(),
      ),
    );
    kucultulmus=false;
    ngelxSesliMiniTemizle(widget.odaId);
    if(!bitti&&!kapatiliyor){
      if(!bagli){
        await tekrarBaglan();
      }else if(konusmaciyim&&mikrofonTercihi&&!mikrofon){
        try{
          await aktifOda.localParticipant?.setMicrophoneEnabled(true);
          if(mounted)setState(()=>mikrofon=true);
        }catch(_){unawaited(tekrarBaglan());}
      }
    }
  }
  Future<void> bitir()async{
    ngelxSesliMiniTemizle(widget.odaId);
    if(!sahibiyim)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sesli odayı bitirmek istiyor musun?'),content:const Text('Oda kapanacak ve odadaki herkes çıkarılacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Bitir'))]));
    if(ok!=true)return;
    kapatiliyor=true;heartbeat?.cancel();yalnizlikTimer?.cancel();
    final bas=veri['startedAt'];
    final sure=bas is Timestamp?DateTime.now().difference(bas.toDate()).inSeconds:0;
    await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'active':false,'endedAt':FieldValue.serverTimestamp(),'durationSeconds':sure<0?0:sure,'endReason':'host_ended'},SetOptions(merge:true));
    final ben=uid;
    if(ben!=null){
      await ngelxSesliKatilimciAyril(widget.odaId,ben);
      await FirebaseFirestore.instance.collection('users').doc(ben).set({'isAudioLive':false,'currentAudioRoomId':FieldValue.delete()},SetOptions(merge:true));
    }
    try{await aktifOda.disconnect();}catch(_){}
    if(mounted)Navigator.pop(context);
  }
  Future<void> ayril()async{
    ngelxSesliMiniTemizle(widget.odaId);
    if(sahibiyim){await bitir();return;}
    if(bitti){if(mounted)Navigator.pop(context);return;}
    final ok=await showDialog<bool>(
      context:context,
      builder:(c)=>AlertDialog(
        title:const Text('Sesli odadan ayrılmak istiyor musun?'),
        content:const Text('Ayrılırsan ses bağlantın kesilecek. Daha sonra oda açıksa tekrar katılabilirsin.'),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
          FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Ayrıl')),
        ],
      ),
    );
    if(ok!=true)return;
    kapatiliyor=true;
    final ben=uid;if(ben!=null)await ngelxSesliKatilimciAyril(widget.odaId,ben);
    try{await aktifOda.localParticipant?.setMicrophoneEnabled(false);}catch(_){}
    try{await aktifOda.disconnect();}catch(_){}
    if(mounted)Navigator.pop(context);
  }
  dynamic _liveKitKatilimci(String id){
    if(id.isEmpty)return null;
    if(id==uid)return aktifOda.localParticipant;
    for(final p in aktifOda.remoteParticipants.values){
      if(p.identity==id)return p;
    }
    return null;
  }

  Widget koltuk(String id,{String mesaj=''}){
    if(id.isEmpty)return Container(
      decoration:BoxDecoration(color:const Color(0xFFF8F6FA),borderRadius:BorderRadius.circular(18),border:Border.all(color:const Color(0xFFECE7F0))),
      child:const Column(mainAxisAlignment:MainAxisAlignment.center,children:[
        CircleAvatar(backgroundColor:Color(0xFFEDEAF0),child:Icon(Icons.add,color:Colors.black26)),
        SizedBox(height:5),
        Text('Boş',style:TextStyle(color:Colors.black38,fontSize:11)),
      ]),
    );
    final dynamic lkKisi=_liveKitKatilimci(id);
    final konusuyor=lkKisi?.isSpeaking==true;
    final micAcik=id==uid?mikrofon:(lkKisi?.isMicrophoneEnabled()==true);
    final admin=id==widget.ownerId;
    final yonetici=moderatorler.contains(id);
    final rol=admin?'ADMIN':yonetici?'YÖNETİCİ':'KONUŞMACI';
    final rolRenk=admin?Colors.red:yonetici?const Color(0xFFFF8A00):mor;
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(id).snapshots(),
      builder:(_,s){
        final p=s.data?.data()??<String,dynamic>{},foto=(p['photoUrl']??'').toString(),ad=(p['displayName']??p['username']??(admin?'ADMIN':'Konuşmacı')).toString();
        return Container(
          padding:const EdgeInsets.all(7),
          decoration:BoxDecoration(
            color:const Color(0xFFF8F4FD),
            borderRadius:BorderRadius.circular(18),
            border:Border.all(color:konusuyor?const Color(0xFF22C55E):rolRenk.withValues(alpha:admin?1:.45),width:konusuyor?2.5:1.2),
            boxShadow:konusuyor?const [BoxShadow(color:Color(0x3322C55E),blurRadius:12,spreadRadius:1)]:null,
          ),
          child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
            Stack(clipBehavior:Clip.none,children:[
              CircleAvatar(radius:24,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?Icon(Icons.person,color:rolRenk):null),
              Positioned(
                right:-4,bottom:-3,
                child:Container(
                  width:19,height:19,
                  decoration:BoxDecoration(color:micAcik?const Color(0xFF22C55E):Colors.red,shape:BoxShape.circle,border:Border.all(color:Colors.white,width:2)),
                  child:Icon(micAcik?Icons.mic_rounded:Icons.mic_off_rounded,color:Colors.white,size:11),
                ),
              ),
            ]),
            const SizedBox(height:5),
            Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:10.5,fontWeight:FontWeight.w900)),
            Text(rol,style:TextStyle(fontSize:8,color:rolRenk,fontWeight:FontWeight.w900)),
            if(mesaj.isNotEmpty)...[
              const SizedBox(height:4),
              Container(
                constraints:const BoxConstraints(maxWidth:105),
                padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),
                decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(10),border:Border.all(color:const Color(0xFFE7E1EB))),
                child:Text(mesaj,maxLines:2,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontSize:9.5,fontWeight:FontWeight.w700)),
              ),
            ],
          ]),
        );
      },
    );
  }

  @override Widget build(BuildContext context){final sp=speakers.isEmpty?[widget.ownerId]:speakers;final sayfa=Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,foregroundColor:Colors.black,leading:IconButton(tooltip:'Küçült',onPressed:kucult,icon:const Icon(Icons.keyboard_arrow_down_rounded)),title:const Text('Sesli',style:TextStyle(fontWeight:FontWeight.w900))),body:SafeArea(child:Column(children:[
    if(durum.isNotEmpty&&!bitti)InkWell(onTap:!yeniden&&!bitti?()=>unawaited(tekrarBaglan()):null,child:Container(width:double.infinity,padding:const EdgeInsets.all(9),color:const Color(0xFFFFF5D9),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[Icon(bitti?Icons.stop_circle_outlined:Icons.wifi_off_rounded,size:18,color:bitti?Colors.redAccent:Colors.black54),const SizedBox(width:7),Flexible(child:Text(durum,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)))]))),
    if(sahibiyim&&aktifKisiSayisi<2&&yalnizlikBasladi!=null&&!bitti)
      Container(
        width:double.infinity,
        padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
        color:const Color(0xFFFFF8E8),
        child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
          const Icon(Icons.group_off_outlined,size:17,color:Color(0xFF8C6500)),
          const SizedBox(width:6),
          Flexible(child:Text('2. kişi bekleniyor • ${ngelxSesliSureMetni(Duration(seconds:yalnizlikKalan))} sonra oda kapanır',textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFF6F5200),fontSize:12,fontWeight:FontWeight.w800))),
        ]),
      ),
    Expanded(child:ListView(padding:const EdgeInsets.all(16),children:[Container(padding:const EdgeInsets.all(16),decoration:BoxDecoration(color:const Color(0xFFF6F0FF),borderRadius:BorderRadius.circular(22)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Row(children:[Icon(bitti?Icons.stop_circle:Icons.graphic_eq_rounded,color:bitti?Colors.redAccent:mor),const SizedBox(width:6),Text(bitti?'SONA ERDİ':'SESLİ CANLI',style:TextStyle(color:bitti?Colors.redAccent:mor,fontWeight:FontWeight.w900)),const SizedBox(width:8),NgelxSesliSureSayaci(baslangic:veri['startedAt'] is Timestamp?(veri['startedAt'] as Timestamp).toDate():null,bitti:bitti),const Spacer(),const Icon(Icons.headphones,size:17,color:Colors.black45),Text(' ${aktifOda.remoteParticipants.length}',style:const TextStyle(fontWeight:FontWeight.w800))]),const SizedBox(height:9),Text((veri['title']??widget.baslik).toString(),style:const TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:4),Text('${sp.length}/12 konuşmacı',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700))])),NgelxSesliTepkiAkisi(roomId:widget.odaId),const SizedBox(height:10),Wrap(spacing:8,runSpacing:8,children:[
  OutlinedButton.icon(onPressed:()=>ngelxSesliKatilimcilarAc(context,widget.odaId,widget.ownerId),icon:const Icon(Icons.headphones_rounded,size:18),label:const Text('Dinleyiciler')),
  PopupMenuButton<String>(
    tooltip:'Tepki gönder',
    onSelected:(x)=>ngelxSesliTepkiGonder(widget.odaId,x),
    itemBuilder:(_)=>['❤️','👏','😂','🔥','🎉'].map((x)=>PopupMenuItem(value:x,child:Text(x,style:const TextStyle(fontSize:24)))).toList(),
    child:Container(padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),decoration:BoxDecoration(border:Border.all(color:const Color(0xFFD5CEDD)),borderRadius:BorderRadius.circular(20)),child:const Row(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.add_reaction_outlined,size:18,color:mor),SizedBox(width:6),Text('Tepki',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))])),
  ),
  OutlinedButton.icon(onPressed:()=>ngelxSesliPaylas(context,widget.odaId,(veri['title']??widget.baslik).toString()),icon:const Icon(Icons.ios_share_rounded,size:18),label:const Text('Davet')),
]),const SizedBox(height:14),Row(children:[const Text('Sahne',style:TextStyle(fontSize:18,fontWeight:FontWeight.w900)),const Spacer(),if(yoneticiyim&&!bitti)TextButton.icon(onPressed:istekler,icon:const Icon(Icons.pan_tool_alt,size:16),label:const Text('İstekler'))]),StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
  stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('messages').orderBy('createdAt',descending:true).limit(40).snapshots(),
  builder:(_,ms){
    final son=<String,String>{};
    for(final d in ms.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]){
      final v=d.data(),k=(v['userId']??'').toString(),t=(v['text']??'').toString().trim();
      if(k.isNotEmpty&&t.isNotEmpty&&!son.containsKey(k))son[k]=t.length>42?t.substring(0,42)+'…':t;
    }
    final gorunen=(sp.length+(sp.length<ngelxSesliMaksKonusmaci?1:0)).clamp(3,ngelxSesliMaksKonusmaci).toInt();
    return GridView.builder(
      shrinkWrap:true,
      physics:const NeverScrollableScrollPhysics(),
      gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:3,crossAxisSpacing:8,mainAxisSpacing:8,childAspectRatio:.78),
      itemCount:gorunen,
      itemBuilder:(_,i){
        final id=i<sp.length?sp[i]:'';
        return koltuk(id,mesaj:id.isEmpty?'':(son[id]??''));
      },
    );
  },
),if(!konusmaciyim&&!bitti)...[const SizedBox(height:14),FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF0E8FF),foregroundColor:mor),onPressed:sozIste,icon:const Icon(Icons.pan_tool_alt_rounded),label:const Text('Söz iste'))],if(bitti)...[const SizedBox(height:14),const Text('Bu sesli oda sona erdi.',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w900))]])),Container(
  padding:const EdgeInsets.fromLTRB(12,9,12,9),
  decoration:const BoxDecoration(color:Color(0xFFFDFBFF),border:Border(top:BorderSide(color:Color(0xFFEDE8F2)),bottom:BorderSide(color:Color(0xFFEDE8F2)))),
  child:bitti
    ?FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:Colors.red,minimumSize:const Size.fromHeight(48)),onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded),label:const Text('Kapat',style:TextStyle(fontWeight:FontWeight.w900)))
    :Row(children:[
      Expanded(child:FilledButton.icon(
        style:FilledButton.styleFrom(backgroundColor:konusmaciyim&&mikrofon?mor:const Color(0xFFF0E8FF),foregroundColor:konusmaciyim&&mikrofon?Colors.white:mor),
        onPressed:konusmaciyim?(bagli?mic:()=>unawaited(tekrarBaglan())):null,
        icon:Icon(!bagli?Icons.refresh_rounded:(mikrofon?Icons.mic:Icons.mic_off)),
        label:Text(!bagli?(konusmaciyim?'Yeniden bağlan':'Bağlantı bekleniyor'):konusmaciyim?(mikrofon?'Mikrofon açık':'Mikrofon kapalı'):'Dinleyici'),
      )),
      const SizedBox(width:8),
      OutlinedButton.icon(
        style:OutlinedButton.styleFrom(foregroundColor:Colors.red,side:const BorderSide(color:Colors.redAccent)),
        onPressed:ayril,
        icon:Icon(sahibiyim?Icons.stop_circle:Icons.logout),
        label:Text(sahibiyim?'Bitir':'Ayrıl',style:const TextStyle(fontWeight:FontWeight.w900)),
      ),
    ]),
),NgelxSesliInlineSohbet(roomId:widget.odaId,yonetici:yoneticiyim,sahibiyim:sahibiyim,bitti:bitti)])));
    return PopScope(canPop:false,onPopInvokedWithResult:(didPop,result){if(!didPop)unawaited(kucult());},child:sayfa);
  }
  @override void dispose(){kapatiliyor=true;heartbeat?.cancel();yalnizlikTimer?.cancel();abonelik?.cancel();katilimAboneligi?.cancel();odaKatilimAboneligi?.cancel();aktifOda.removeListener(odaDegisti);final ben=uid;if(ben!=null&&!bitti)unawaited(ngelxSesliKatilimciAyril(widget.odaId,ben));if(!widget.yayinSahibi)unawaited(aktifOda.disconnect());unawaited(aktifOda.dispose());super.dispose();}
}
