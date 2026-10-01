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
    if(gizlilik!='public'&&owner!=user.uid){
      final p=(await FirebaseFirestore.instance.collection('users').doc(owner).get()).data()??<String,dynamic>{};
      final izin=gizlilik=='friends'?List<String>.from(p['friends']??const[]).contains(user.uid):List<String>.from(p['followers']??const[]).contains(user.uid);
      if(!izin){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu sesli odaya katılma iznin yok.')));return;}
    }
    final roomName=(v['roomName']??'').toString();if(roomName.isEmpty)throw StateError('room_name');
    final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
    final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString();
    final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId).fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:const {'role':'listener','mode':'audio'}));
    oda=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
    await oda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:18));
    await oda.localParticipant?.setMicrophoneEnabled(false);
    if(!context.mounted){await oda.disconnect();await oda.dispose();return;}
    await Navigator.push(context,MaterialPageRoute(builder:(_)=>SesliOdaPage(oda:oda!,odaId:odaId,ownerId:owner,baslik:(v['title']??'Sesli oda').toString(),yayinSahibi:false,serverUrl:cevap.serverUrl,participantToken:cevap.participantToken)));
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
      final d=await FirebaseFirestore.instance.collection('audio_rooms').add({'roomName':roomName,'ownerId':user.uid,'ownerName':ad,'ownerPhotoUrl':foto,'title':baslik.text.trim(),'category':kategori,'visibility':gizlilik,'active':true,'startedAt':FieldValue.serverTimestamp(),'lastHeartbeatAt':FieldValue.serverTimestamp(),'speakerIds':[user.uid],'moderatorIds':<String>[],'speakerCount':1,'listenerCount':0,'maxSpeakers':ngelxSesliMaksKonusmaci,'maxModerators':ngelxSesliMaksModerator,'mode':'audio'});
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'isAudioLive':true,'currentAudioRoomId':d.id,'audioRoomTitle':baslik.text.trim()},SetOptions(merge:true));
      if(!mounted)return;Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>SesliOdaPage(oda:oda!,odaId:d.id,ownerId:user.uid,baslik:baslik.text.trim(),yayinSahibi:true,serverUrl:cevap.serverUrl,participantToken:cevap.participantToken)));
    }catch(_){if(oda!=null){try{await oda.disconnect();await oda.dispose();}catch(_){} }if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli oda başlatılamadı.')));}finally{if(mounted)setState(()=>baslatiliyor=false);}
  }
  @override Widget build(BuildContext context)=>Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,foregroundColor:Colors.black,title:const Text('Sesli oda oluştur',style:TextStyle(fontWeight:FontWeight.w900))),body:SafeArea(child:ListView(padding:const EdgeInsets.all(18),children:[
    Container(padding:const EdgeInsets.all(18),decoration:BoxDecoration(color:const Color(0xFFF6F0FF),borderRadius:BorderRadius.circular(22)),child:const Row(children:[CircleAvatar(radius:26,backgroundColor:mor,child:Icon(Icons.mic_rounded,color:Colors.white)),SizedBox(width:12),Expanded(child:Text('Kamera yok. Ses odakta.\n12 konuşmacıya kadar sahne hazır.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800,height:1.35)))])),const SizedBox(height:18),
    TextField(controller:baslik,maxLength:80,cursorColor:mor,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800),decoration:InputDecoration(labelText:'Oda başlığı',labelStyle:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700),floatingLabelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w800),hintText:'Örn. Akşam sohbeti',hintStyle:const TextStyle(color:Color(0xFF9A9AA2)),counterStyle:const TextStyle(color:Colors.black45),filled:true,fillColor:const Color(0xFFF5F5F8),enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:Color(0xFFE5E2EA))),focusedBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:mor,width:1.5)),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none))),const SizedBox(height:8),
    Wrap(spacing:8,children:['Sohbet','Müzik','Teknoloji','Spor','Gündem'].map((x)=>ChoiceChip(label:Text(x),selected:kategori==x,onSelected:(_)=>setState(()=>kategori=x))).toList()),const SizedBox(height:16),
    SegmentedButton<String>(segments:const [ButtonSegment(value:'public',label:Text('Herkes')),ButtonSegment(value:'followers',label:Text('Takipçiler')),ButtonSegment(value:'friends',label:Text('Arkadaşlar'))],selected:{gizlilik},onSelectionChanged:(x)=>setState(()=>gizlilik=x.first)),const SizedBox(height:22),
    FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(54)),onPressed:baslatiliyor?null:baslat,icon:baslatiliyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.graphic_eq_rounded),label:Text(baslatiliyor?'Oda açılıyor...':'Sesli odayı başlat',style:const TextStyle(fontWeight:FontWeight.w900))),
  ])));
}

class SesliOdaPage extends StatefulWidget{
  final lk.Room oda;final String odaId,ownerId,baslik,serverUrl,participantToken;final bool yayinSahibi;
  const SesliOdaPage({super.key,required this.oda,required this.odaId,required this.ownerId,required this.baslik,required this.yayinSahibi,required this.serverUrl,required this.participantToken});
  @override State<SesliOdaPage> createState()=>_SesliOdaPageState();
}
class _SesliOdaPageState extends State<SesliOdaPage>{
  Timer? heartbeat;StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? abonelik;Map<String,dynamic> veri={};bool mikrofon=false,mikrofonTercihi=false,bitti=false,kapatiliyor=false,yeniden=false;String durum='';
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);bool get konusmaciyim=>uid!=null&&speakers.contains(uid);bool get bagli=>widget.oda.connectionState==lk.ConnectionState.connected;
  @override void initState(){super.initState();mikrofon=widget.yayinSahibi;mikrofonTercihi=widget.yayinSahibi;widget.oda.addListener(odaDegisti);abonelik=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).snapshots().listen((d){final v=d.data()??<String,dynamic>{};if(!mounted)return;final once=konusmaciyim;setState((){veri=v;bitti=v.isNotEmpty&&v['active']!=true;});if(once&&!konusmaciyim&&mikrofon){mikrofon=false;unawaited(widget.oda.localParticipant?.setMicrophoneEnabled(false));}});if(widget.yayinSahibi){unawaited(kalp());heartbeat=Timer.periodic(const Duration(seconds:6),(_)=>unawaited(kalp()));}}
  void odaDegisti(){
    if(!mounted)return;
    final koptu=widget.oda.connectionState==lk.ConnectionState.disconnected;
    if(koptu&&mikrofon)mikrofon=false;
    setState((){
      if(koptu&&!kapatiliyor&&!bitti)durum='Bağlantı koptu. Yeniden bağlanılıyor...';
      if(!koptu&&bagli)durum='';
    });
    if(koptu&&!kapatiliyor&&!bitti)unawaited(tekrarBaglan());
  }
  Future<void> kalp()async{if(!widget.yayinSahibi||kapatiliyor||bitti)return;try{await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'lastHeartbeatAt':FieldValue.serverTimestamp(),'listenerCount':widget.oda.remoteParticipants.length,'speakerCount':speakers.isEmpty?1:speakers.length},SetOptions(merge:true));}catch(_){}}
  Future<void> tekrarBaglan()async{
    if(yeniden||kapatiliyor||bitti)return;
    final user=FirebaseAuth.instance.currentUser;if(user==null)return;
    yeniden=true;
    for(var i=1;i<=4;i++){
      if(mounted)setState(()=>durum='Tekrar bağlanılıyor $i/4');
      try{
        await Future.delayed(Duration(milliseconds:450*i));
        final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        final v=d.data()??<String,dynamic>{};
        if(!d.exists||v['active']!=true){bitti=true;throw StateError('audio_room_ended');}
        final roomName=(v['roomName']??'').toString();if(roomName.isEmpty)throw StateError('room_name');
        final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
        final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString();
        final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId).fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:{'role':sahibiyim?'host':'listener','mode':'audio'}));
        await widget.oda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:12));
        final micAcik=konusmaciyim&&mikrofonTercihi;
        await widget.oda.localParticipant?.setMicrophoneEnabled(micAcik);
        yeniden=false;
        if(mounted)setState((){mikrofon=micAcik;durum='';});
        return;
      }catch(_){}
    }
    yeniden=false;
    if(mounted)setState((){mikrofon=false;durum=bitti?'Bu sesli oda sona erdi.':'Bağlantı kurulamadı. Tekrar denemek için dokun.';});
  }
  Future<void> mic()async{
    if(!konusmaciyim)return;
    if(!bagli){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Ses bağlantısı yok. Yeniden bağlanılıyor...')));unawaited(tekrarBaglan());return;}
    final yeni=!mikrofonTercihi;
    if(yeni&&!(await Permission.microphone.request()).isGranted)return;
    try{
      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      if(mounted)setState((){mikrofonTercihi=yeni;mikrofon=yeni;});
    }catch(_){
      if(mounted)setState(()=>mikrofon=false);
      unawaited(tekrarBaglan());
    }
  }
  Future<void> sozIste()async{final ben=uid;if(ben==null||konusmaciyim)return;final p=(await FirebaseFirestore.instance.collection('users').doc(ben).get()).data()??<String,dynamic>{};await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('speaker_requests').doc(ben).set({'userId':ben,'displayName':(p['displayName']??p['username']??'NgelX').toString(),'photoUrl':(p['photoUrl']??'').toString(),'status':'pending','createdAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Söz isteğin gönderildi.')));}
  Future<void> istekler()async{
    if(!sahibiyim)return;
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
                    final docs=s.data?.docs??[];
                    if(docs.isEmpty)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.pan_tool_alt_outlined,color:mor,size:38),SizedBox(height:9),Text('Bekleyen söz isteği yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bir dinleyici söz istediğinde burada görünecek.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black45))])));
                    return ListView.separated(
                      padding:const EdgeInsets.symmetric(vertical:6),
                      itemCount:docs.length,
                      separatorBuilder:(_,__)=>const Divider(height:1,indent:70,color:Color(0xFFF0EDF3)),
                      itemBuilder:(_,i){
                        final d=docs[i],v=d.data(),foto=(v['photoUrl']??'').toString();
                        return ListTile(
                          leading:CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),
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
  Future<void> bitir()async{if(!sahibiyim)return;final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sesli oda bitsin mi?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Bitir'))]));if(ok!=true)return;kapatiliyor=true;heartbeat?.cancel();await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'active':false,'endedAt':FieldValue.serverTimestamp(),'endReason':'host_ended'},SetOptions(merge:true));final ben=uid;if(ben!=null)await FirebaseFirestore.instance.collection('users').doc(ben).set({'isAudioLive':false,'currentAudioRoomId':FieldValue.delete()},SetOptions(merge:true));try{await widget.oda.disconnect();}catch(_){}if(mounted)Navigator.pop(context);}
  Future<void> ayril()async{if(sahibiyim){await bitir();return;}kapatiliyor=true;try{await widget.oda.disconnect();}catch(_){}if(mounted)Navigator.pop(context);}
  Widget koltuk(String id){if(id.isEmpty)return Container(decoration:BoxDecoration(color:const Color(0xFFF8F6FA),borderRadius:BorderRadius.circular(18)),child:const Column(mainAxisAlignment:MainAxisAlignment.center,children:[CircleAvatar(backgroundColor:Color(0xFFEDEAF0),child:Icon(Icons.add,color:Colors.black26)),SizedBox(height:5),Text('Boş',style:TextStyle(color:Colors.black38,fontSize:11))]));return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(id).snapshots(),builder:(_,s){final p=s.data?.data()??<String,dynamic>{},foto=(p['photoUrl']??'').toString(),ad=(p['displayName']??p['username']??(id==widget.ownerId?'Oda sahibi':'Konuşmacı')).toString();return Container(padding:const EdgeInsets.all(8),decoration:BoxDecoration(color:const Color(0xFFF8F4FD),borderRadius:BorderRadius.circular(18),border:Border.all(color:id==widget.ownerId?mor:const Color(0xFFEAE3F2))),child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[CircleAvatar(radius:24,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),const SizedBox(height:5),Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:10.5,fontWeight:FontWeight.w900)),Text(id==widget.ownerId?'SAHİP':'KONUŞMACI',style:TextStyle(fontSize:8,color:id==widget.ownerId?mor:Colors.black38,fontWeight:FontWeight.w900))]));});}
  @override Widget build(BuildContext context){final sp=speakers.isEmpty?[widget.ownerId]:speakers;return Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,foregroundColor:Colors.black,leading:IconButton(onPressed:ayril,icon:const Icon(Icons.arrow_back)),title:const Text('Sesli',style:TextStyle(fontWeight:FontWeight.w900)),actions:[if(sahibiyim)IconButton(tooltip:'Söz istekleri',onPressed:istekler,icon:const Icon(Icons.pan_tool_alt_rounded,color:mor))]),body:SafeArea(child:Column(children:[if(durum.isNotEmpty)InkWell(onTap:!yeniden&&!bitti?()=>unawaited(tekrarBaglan()):null,child:Container(width:double.infinity,padding:const EdgeInsets.all(9),color:const Color(0xFFFFF5D9),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[Icon(bitti?Icons.stop_circle_outlined:Icons.wifi_off_rounded,size:18,color:bitti?Colors.redAccent:Colors.black54),const SizedBox(width:7),Flexible(child:Text(durum,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)))]))),Expanded(child:ListView(padding:const EdgeInsets.all(16),children:[Container(padding:const EdgeInsets.all(16),decoration:BoxDecoration(color:const Color(0xFFF6F0FF),borderRadius:BorderRadius.circular(22)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Row(children:[Icon(bitti?Icons.stop_circle:Icons.graphic_eq_rounded,color:bitti?Colors.redAccent:mor),const SizedBox(width:6),Text(bitti?'SONA ERDİ':'SESLİ CANLI',style:TextStyle(color:bitti?Colors.redAccent:mor,fontWeight:FontWeight.w900)),const Spacer(),const Icon(Icons.headphones,size:17,color:Colors.black45),Text(' ${widget.oda.remoteParticipants.length}',style:const TextStyle(fontWeight:FontWeight.w800))]),const SizedBox(height:9),Text((veri['title']??widget.baslik).toString(),style:const TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:4),Text('${sp.length}/12 konuşmacı',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700))])),const SizedBox(height:14),Row(children:[const Text('Sahne',style:TextStyle(fontSize:18,fontWeight:FontWeight.w900)),const Spacer(),if(sahibiyim)TextButton.icon(onPressed:istekler,icon:const Icon(Icons.pan_tool_alt,size:16),label:const Text('İstekler'))]),GridView.builder(shrinkWrap:true,physics:const NeverScrollableScrollPhysics(),gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:3,crossAxisSpacing:8,mainAxisSpacing:8,childAspectRatio:.9),itemCount:ngelxSesliMaksKonusmaci,itemBuilder:(_,i)=>koltuk(i<sp.length?sp[i]:'')),if(!konusmaciyim&&!bitti)...[const SizedBox(height:14),FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF0E8FF),foregroundColor:mor),onPressed:sozIste,icon:const Icon(Icons.pan_tool_alt_rounded),label:const Text('Söz iste'))],if(bitti)...[const SizedBox(height:14),const Text('Bu sesli oda sona erdi.',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w900))]])),Container(padding:const EdgeInsets.all(12),decoration:const BoxDecoration(border:Border(top:BorderSide(color:Color(0xFFEDE8F2)))),child:Row(children:[Expanded(child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:konusmaciyim&&mikrofon?mor:const Color(0xFFF0E8FF),foregroundColor:konusmaciyim&&mikrofon?Colors.white:mor),onPressed:konusmaciyim&&!bitti&&bagli?mic:null,icon:Icon(mikrofon?Icons.mic:Icons.mic_off),label:Text(!bagli?'Bağlantı bekleniyor':konusmaciyim?(mikrofon?'Mikrofon açık':'Mikrofon kapalı'):'Dinleyici'))),const SizedBox(width:8),OutlinedButton.icon(onPressed:ayril,icon:Icon(sahibiyim?Icons.stop_circle:Icons.logout),label:Text(sahibiyim?'Bitir':'Ayrıl'))]))])));
  }
  @override void dispose(){kapatiliyor=true;heartbeat?.cancel();abonelik?.cancel();widget.oda.removeListener(odaDegisti);if(!widget.yayinSahibi)unawaited(widget.oda.disconnect());unawaited(widget.oda.dispose());super.dispose();}
}
