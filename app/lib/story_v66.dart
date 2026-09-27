part of 'main.dart';

bool ngelxHikayeAktif(Map<String,dynamic> v){
  final bitis=v['expiresAt'];
  return v['type']=='story' &&
      bitis is Timestamp &&
      bitis.toDate().isAfter(DateTime.now());
}

int ngelxHikayeZamani(Map<String,dynamic> v){
  final t=v['createdAt']??v['clientCreatedAt'];
  return t is Timestamp?t.millisecondsSinceEpoch:0;
}

class NgelXHikayeliAvatar extends StatelessWidget{
  final String uid;
  final String fotoUrl;
  final String kullanici;
  final double radius;
  final bool etkin;
  final VoidCallback? hikayeYoksaTikla;
  final VoidCallback? uzunBas;
  const NgelXHikayeliAvatar({
    super.key,
    required this.uid,
    required this.fotoUrl,
    required this.kullanici,
    this.radius=55,
    this.etkin=true,
    this.hikayeYoksaTikla,
    this.uzunBas,
  });

  @override
  Widget build(BuildContext context){
    if(uid.isEmpty)return _avatar(false,null);
    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).limit(100).snapshots(),
      builder:(_,s){
        final aktif=(s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[])
          .where((d)=>ngelxHikayeAktif(d.data()))
          .toList()
          ..sort((a,b)=>ngelxHikayeZamani(a.data()).compareTo(ngelxHikayeZamani(b.data())));
        final varMi=aktif.isNotEmpty;
        return GestureDetector(
          onTap:!etkin?null:varMi
            ?()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXHikayeSeriPage(
              ownerUid:uid,
              initialStoryId:aktif.first.id,
              kullanici:kullanici,
              fotoUrl:fotoUrl,
            )))
            :hikayeYoksaTikla,
          onLongPress:uzunBas,
          child:_avatar(varMi,aktif.isEmpty?null:aktif.first.id),
        );
      },
    );
  }

  Widget _avatar(bool hikayeVar,String? storyId){
    final avatar=CircleAvatar(
      radius:radius,
      backgroundColor:Colors.white,
      backgroundImage:fotoUrl.isEmpty?null:CachedNetworkImageProvider(fotoUrl),
      child:fotoUrl.isEmpty?Text(
        kullanici.replaceFirst('@','').isEmpty?'N':kullanici.replaceFirst('@','')[0].toUpperCase(),
        style:TextStyle(fontSize:radius*.72,fontWeight:FontWeight.w800),
      ):null,
    );
    if(!hikayeVar)return avatar;
    return Container(
      padding:const EdgeInsets.all(3),
      decoration:const BoxDecoration(
        shape:BoxShape.circle,
        gradient:LinearGradient(colors:[Color(0xFF22D3EE),Color(0xFF3B82F6),Color(0xFF8B5CF6)]),
      ),
      child:avatar,
    );
  }
}

class NgelXHikayeSeriPage extends StatefulWidget{
  final String ownerUid;
  final String initialStoryId;
  final String kullanici;
  final String fotoUrl;
  const NgelXHikayeSeriPage({
    super.key,
    required this.ownerUid,
    this.initialStoryId='',
    required this.kullanici,
    this.fotoUrl='',
  });

  @override
  State<NgelXHikayeSeriPage> createState()=>_NgelXHikayeSeriPageState();
}

class _NgelXHikayeSeriPageState extends State<NgelXHikayeSeriPage> with SingleTickerProviderStateMixin{
  late final AnimationController sure;
  final cevap=TextEditingController();
  List<QueryDocumentSnapshot<Map<String,dynamic>>> hikayeler=<QueryDocumentSnapshot<Map<String,dynamic>>>[];
  int aktif=0;
  bool yukleniyor=true;
  bool gonderiliyor=false;
  bool sessiz=false;
  bool videoHazir=false;
  bool videoHata=false;
  int medyaNesli=0;
  VideoPlayerController? videoKontrol;

  QueryDocumentSnapshot<Map<String,dynamic>>? get belge=>
      hikayeler.isEmpty||aktif<0||aktif>=hikayeler.length?null:hikayeler[aktif];
  Map<String,dynamic> get veri=>belge?.data()??<String,dynamic>{};
  String get storyId=>belge?.id??'';
  String get url=><dynamic>[
    veri['mediaUrl'],veri['videoUrl'],veri['playbackUrl'],veri['downloadUrl'],veri['url'],
  ].map((e)=>(e??'').toString().trim()).firstWhere((e)=>e.isNotEmpty,orElse:()=>'');
  String get mediaType=>(veri['storyMediaType']??veri['mediaType']??'photo').toString().toLowerCase();

  bool get videoMu{
    if(mediaType=='video')return true;
    final temiz=url.split('?').first.toLowerCase();
    return temiz.endsWith('.mp4')||temiz.endsWith('.mov')||temiz.endsWith('.m4v')||temiz.endsWith('.webm');
  }

  @override
  void initState(){
    super.initState();
    sure=AnimationController(vsync:this,duration:const Duration(seconds:7))
      ..addStatusListener((s){
        if(s==AnimationStatus.completed&&mounted)_sonraki();
      });
    unawaited(_yukle());
  }

  Future<void> _yukle()async{
    try{
      final q=await FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.ownerUid).limit(100).get();
      final simdi=DateTime.now();
      final list=q.docs.where((d){
        final v=d.data(),bitis=v['expiresAt'];
        return v['type']=='story'&&bitis is Timestamp&&bitis.toDate().isAfter(simdi);
      }).toList()
        ..sort((a,b)=>ngelxHikayeZamani(a.data()).compareTo(ngelxHikayeZamani(b.data())));
      if(!mounted)return;
      if(list.isEmpty){
        Navigator.pop(context);
        return;
      }
      var ilk=0;
      if(widget.initialStoryId.isNotEmpty){
        final i=list.indexWhere((d)=>d.id==widget.initialStoryId);
        if(i>=0)ilk=i;
      }
      setState((){hikayeler=list;aktif=ilk;yukleniyor=false;});
      await _aktifHikayeyiBaslat();
    }catch(_){
      if(!mounted)return;
      setState(()=>yukleniyor=false);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâyeler yüklenemedi.')));
    }
  }

  Future<void> _aktifHikayeyiBaslat()async{
    final nesil=++medyaNesli;
    sure.stop();
    sure.reset();
    videoHazir=false;
    videoHata=false;
    final onceki=videoKontrol;
    videoKontrol=null;
    if(onceki!=null)unawaited(onceki.dispose());

    final d=belge;
    if(d==null)return;
    final medyaAdresi=url;
    if(medyaAdresi.isEmpty||Uri.tryParse(medyaAdresi)?.hasScheme!=true){
      videoHata=true;
      sure.duration=const Duration(seconds:7);
      if(mounted)setState((){});
      sure.forward(from:0);
      return;
    }
    unawaited(_gorulduKaydet(d));

    if(!videoMu){
      sure.duration=const Duration(seconds:7);
      if(mounted)setState((){});
      sure.forward(from:0);
      return;
    }

    try{
      final x=VideoPlayerController.networkUrl(Uri.parse(medyaAdresi));
      videoKontrol=x;
      await x.initialize();
      if(!mounted||nesil!=medyaNesli){await x.dispose();return;}
      final ms=math.max(1000,x.value.duration.inMilliseconds).toInt();
      sure.duration=Duration(milliseconds:ms);
      await x.setLooping(false);
      await x.setVolume(sessiz?0:1);
      setState(()=>videoHazir=true);
      sure.forward(from:0);
      await x.play();
    }catch(_){
      if(!mounted||nesil!=medyaNesli)return;
      setState(()=>videoHata=true);
      sure.duration=const Duration(seconds:7);
      sure.forward(from:0);
    }
  }

  Future<void> _gorulduKaydet(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    var yeniGoruldu=true;
    try{
      final h=await SharedPreferences.getInstance();
      final anahtar='ngelx_story_seen_${me??'guest'}';
      final seen=<String>{...(h.getStringList(anahtar)??const <String>[])};
      yeniGoruldu=seen.add(d.id);
      if(yeniGoruldu)await h.setStringList(anahtar,seen.take(500).toList());
    }catch(_){}
    if(me==null||me==widget.ownerUid||!yeniGoruldu)return;
    try{
      await d.reference.set({'viewCount':FieldValue.increment(1)},SetOptions(merge:true));
    }catch(_){}
  }

  void _duraklat(){
    sure.stop();
    final x=videoKontrol;
    if(x?.value.isInitialized==true)unawaited(x!.pause());
  }

  void _devam(){
    if(!mounted||yukleniyor||belge==null)return;
    if(!sure.isAnimating)sure.forward();
    final x=videoKontrol;
    if(videoMu&&x?.value.isInitialized==true)unawaited(x!.play());
  }

  Future<void> _sonraki()async{
    if(!mounted)return;
    if(aktif+1>=hikayeler.length){
      Navigator.pop(context);
      return;
    }
    setState(()=>aktif++);
    await _aktifHikayeyiBaslat();
  }

  Future<void> _onceki()async{
    if(!mounted)return;
    if(aktif<=0){
      sure.forward(from:0);
      final x=videoKontrol;
      if(x?.value.isInitialized==true){
        await x!.seekTo(Duration.zero);
        await x.play();
      }
      return;
    }
    setState(()=>aktif--);
    await _aktifHikayeyiBaslat();
  }

  Future<void> _sesDegistir()async{
    final yeni=!sessiz;
    setState(()=>sessiz=yeni);
    final x=videoKontrol;
    if(x?.value.isInitialized==true)await x!.setVolume(yeni?0:1);
  }

  String _saat(DateTime x)=>'${x.hour.toString().padLeft(2,'0')}:${x.minute.toString().padLeft(2,'0')}';
  String _tarihSaat(DateTime x)=>'${x.day.toString().padLeft(2,'0')}.${x.month.toString().padLeft(2,'0')} ${_saat(x)}';

  String get zamanBilgisi{
    final olusma=veri['createdAt'] is Timestamp?(veri['createdAt'] as Timestamp).toDate():
        (veri['clientCreatedAt'] is Timestamp?(veri['clientCreatedAt'] as Timestamp).toDate():null);
    final bitis=veri['expiresAt'] is Timestamp?(veri['expiresAt'] as Timestamp).toDate():null;
    if(olusma==null)return 'Az önce';
    if(bitis==null)return 'Başladı: ${_saat(olusma)}';
    final kalan=bitis.difference(DateTime.now());
    final kalanYazi=kalan.isNegative
      ?'süresi doldu'
      :kalan.inHours>=1
        ?'${kalan.inHours} sa kaldı'
        :'${kalan.inMinutes.clamp(1,59)} dk kaldı';
    return 'Başladı: ${_saat(olusma)} • Biter: ${_tarihSaat(bitis)} • $kalanYazi';
  }

  Future<void> _yanitGonder(String ham,{bool tepki=false})async{
    final ben=FirebaseAuth.instance.currentUser;
    final hedef=widget.ownerUid.trim();
    final metin=ham.trim();
    if(ben==null||metin.isEmpty||gonderiliyor||hedef.isEmpty||hedef==ben.uid)return;
    setState(()=>gonderiliyor=true);
    _duraklat();
    try{
      final ids=<String>[ben.uid,hedef]..sort();
      final chatId=ids.join('_');
      final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
      final mesajRef=chat.collection('messages').doc();
      final batch=FirebaseFirestore.instance.batch();
      batch.set(chat,{
        'members':ids,
        'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedef':FieldValue.increment(1),
      },SetOptions(merge:true));
      batch.set(mesajRef,{
        'senderId':ben.uid,'text':metin,'type':'story_reply',
        'storyId':storyId,'storyUrl':url,'storyOwnerId':hedef,'storyMediaType':mediaType,
        'reaction':tepki,'createdAt':FieldValue.serverTimestamp(),'clientCreatedAt':Timestamp.now(),
      });
      if(storyId.isNotEmpty){
        batch.set(FirebaseFirestore.instance.collection('videos').doc(storyId),{
          'replyCount':FieldValue.increment(1),
          if(tepki)'reactionCount':FieldValue.increment(1),
        },SetOptions(merge:true));
      }
      await batch.commit().timeout(const Duration(seconds:12));
      cevap.clear();
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(tepki?'Tepkin gönderildi.':'Yanıtın gönderildi.')));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye yanıtı gönderilemedi.')));
    }finally{
      if(mounted){setState(()=>gonderiliyor=false);_devam();}
    }
  }

  Widget _medya(){
    if(url.isEmpty)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Icon(Icons.broken_image_outlined,color:Colors.white54,size:60),
      SizedBox(height:10),
      Text('Hikâye medyası bulunamadı',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
    ]));
    if(!videoMu){
      return CachedNetworkImage(
        imageUrl:url,
        fit:BoxFit.contain,
        placeholder:(_,__)=>const Center(child:CircularProgressIndicator(color:Colors.white)),
        errorWidget:(_,__,___)=>const Center(child:Icon(Icons.broken_image_outlined,color:Colors.white54,size:60)),
      );
    }
    if(videoHata)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Icon(Icons.videocam_off_outlined,color:Colors.white54,size:62),
      SizedBox(height:10),
      Text('Video hikâye açılamadı',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
    ]));
    if(!videoHazir||videoKontrol==null)return const Center(child:CircularProgressIndicator(color:Colors.white));
    final oran=videoKontrol!.value.aspectRatio<=0?9/16:videoKontrol!.value.aspectRatio;
    return Center(child:AspectRatio(aspectRatio:oran,child:VideoPlayer(videoKontrol!)));
  }

  Widget _ilerleme(){
    return Row(children:List.generate(hikayeler.length,(i)=>Expanded(
      child:Padding(
        padding:EdgeInsets.only(right:i==hikayeler.length-1?0:4),
        child:ClipRRect(
          borderRadius:BorderRadius.circular(8),
          child:i<aktif
            ?const LinearProgressIndicator(value:1,minHeight:3,color:Colors.white,backgroundColor:Colors.white24)
            :i>aktif
              ?const LinearProgressIndicator(value:0,minHeight:3,color:Colors.white,backgroundColor:Colors.white24)
              :AnimatedBuilder(animation:sure,builder:(_,__)=>LinearProgressIndicator(value:sure.value,minHeight:3,color:Colors.white,backgroundColor:Colors.white24)),
        ),
      ),
    )));
  }

  Widget _takipButonu(){
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null||me==widget.ownerUid)return const SizedBox.shrink();
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(me).snapshots(),
      builder:(_,ben){
        final takipte=List<String>.from(ben.data?.data()?['following']??const[]).contains(widget.ownerUid);
        return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('users').doc(widget.ownerUid).snapshots(),
          builder:(_,hedef){
            final gizli=hedef.data?.data()?['privateAccount']==true;
            return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
              stream:FirebaseFirestore.instance.collection('notifications').where('fromUid',isEqualTo:me).limit(100).snapshots(),
              builder:(_,n){
                final bekliyor=gidenSosyalIstekBekliyor(n.data,widget.ownerUid,'follow_request');
                final yazi=takipte?'Takiptesin':bekliyor?'İstek gönderildi':'Takip Et';
                return FilledButton(
                  style:FilledButton.styleFrom(backgroundColor:Colors.white,foregroundColor:Colors.black,padding:const EdgeInsets.symmetric(horizontal:13),minimumSize:const Size(0,38)),
                  onPressed:takipte||bekliyor?null:()async{
                    _duraklat();
                    try{
                      if(gizli){
                        await sosyalIstekGonder(hedefUid:widget.ownerUid,tur:'follow_request',metin:'Yeni takip isteğin var');
                      }else{
                        await takipDurumuDegistir(widget.ownerUid,false);
                      }
                    }finally{_devam();}
                  },
                  child:Text(yazi,style:const TextStyle(fontWeight:FontWeight.w800)),
                );
              },
            );
          },
        );
      },
    );
  }

  Future<void> _secenekler()async{
    _duraklat();
    final benim=FirebaseAuth.instance.currentUser?.uid==widget.ownerUid;
    final sec=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        if(benim)ListTile(
          leading:const Icon(Icons.delete_outline_rounded,color:Colors.red),
          title:const Text('Hikâyeyi sil',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),
          onTap:()=>Navigator.pop(c,'delete'),
        ),
        if(!benim)ListTile(
          leading:const Icon(Icons.flag_outlined,color:Colors.redAccent),
          title:const Text('Hikâyeyi bildir'),
          onTap:()=>Navigator.pop(c,'report'),
        ),
        ListTile(leading:const Icon(Icons.close_rounded),title:const Text('Kapat'),onTap:()=>Navigator.pop(c,'close')),
      ])),
    );
    if(!mounted)return;
    if(sec=='delete'&&storyId.isNotEmpty){
      try{
        await FirebaseFirestore.instance.collection('videos').doc(storyId).delete();
        hikayeler.removeAt(aktif);
        if(hikayeler.isEmpty){if(mounted)Navigator.pop(context);return;}
        if(aktif>=hikayeler.length)aktif=hikayeler.length-1;
        if(mounted)setState((){});
        await _aktifHikayeyiBaslat();
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye silinemedi.')));
      }
    }else if(sec=='report'&&storyId.isNotEmpty){
      if(mounted)await sikayetEt(context,hedefTuru:'hikaye',hedefId:storyId,hedefUid:widget.ownerUid);
    }
    _devam();
  }

  @override
  void dispose(){
    medyaNesli++;
    cevap.dispose();
    sure.dispose();
    final x=videoKontrol;
    if(x!=null)unawaited(x.dispose());
    super.dispose();
  }

  @override
  Widget build(BuildContext context){
    final benim=FirebaseAuth.instance.currentUser?.uid==widget.ownerUid;
    return Scaffold(
      backgroundColor:Colors.black,
      body:yukleniyor
        ?const Center(child:CircularProgressIndicator(color:Colors.white))
        :Stack(fit:StackFit.expand,children:[
          _medya(),
          Positioned.fill(child:IgnorePointer(child:DecoratedBox(decoration:BoxDecoration(
            gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Colors.black54,Colors.transparent,Colors.black54],stops:[0,.38,1]),
          )))),
          Positioned.fill(child:GestureDetector(
            behavior:HitTestBehavior.translucent,
            onTapUp:(d){
              final w=MediaQuery.sizeOf(context).width;
              if(d.localPosition.dx<w*.35){unawaited(_onceki());}else{unawaited(_sonraki());}
            },
            onLongPressStart:(_)=>_duraklat(),
            onLongPressEnd:(_)=>_devam(),
            onVerticalDragEnd:(d){
              if((d.primaryVelocity??0)>550&&mounted)Navigator.pop(context);
            },
          )),
          SafeArea(child:Padding(
            padding:const EdgeInsets.fromLTRB(14,10,14,12),
            child:Column(children:[
              _ilerleme(),
              const SizedBox(height:10),
              Row(children:[
                GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:CircleAvatar(radius:20,backgroundColor:mor,backgroundImage:widget.fotoUrl.isEmpty?null:CachedNetworkImageProvider(widget.fotoUrl),child:widget.fotoUrl.isEmpty?Text(widget.kullanici.replaceFirst('@','').isEmpty?'N':widget.kullanici.replaceFirst('@','')[0].toUpperCase()):null),
                ),
                const SizedBox(width:9),
                Expanded(child:GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                    Text(widget.kullanici,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:16)),
                    Text(zamanBilgisi,style:const TextStyle(color:Colors.white70,fontSize:12)),
                  ]),
                )),
                _takipButonu(),
                if(videoMu)IconButton(onPressed:_sesDegistir,icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:_secenekler,icon:const Icon(Icons.more_horiz_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.white,size:32)),
              ]),
              const Spacer(),
              if(!benim&&widget.ownerUid.isNotEmpty)
                Row(children:[
                  Expanded(child:TextField(
                    controller:cevap,
                    onTap:_duraklat,
                    onSubmitted:(v)=>_yanitGonder(v),
                    style:const TextStyle(color:Colors.white),
                    decoration:InputDecoration(
                      hintText:'Mesaj...',
                      hintStyle:const TextStyle(color:Colors.white60),
                      filled:true,fillColor:Colors.black54,
                      contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:12),
                      border:OutlineInputBorder(borderRadius:BorderRadius.circular(28),borderSide:BorderSide.none),
                      suffixIcon:gonderiliyor?const Padding(padding:EdgeInsets.all(13),child:SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white))):null,
                    ),
                  )),
                  for(final e in const ['😍','😂','❤️'])
                    InkWell(onTap:gonderiliyor?null:()=>_yanitGonder(e,tepki:true),borderRadius:BorderRadius.circular(25),child:Padding(padding:const EdgeInsets.all(7),child:Text(e,style:const TextStyle(fontSize:27)))),
                  IconButton(onPressed:gonderiliyor?null:()=>_yanitGonder(cevap.text),icon:const Icon(Icons.send_rounded,color:Colors.white,size:29)),
                ])
              else
                Container(
                  padding:const EdgeInsets.symmetric(horizontal:13,vertical:9),
                  decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(18)),
                  child:Row(mainAxisSize:MainAxisSize.min,children:[
                    Text('${aktif+1}/${hikayeler.length}',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w900)),
                    const SizedBox(width:13),
                    const Icon(Icons.visibility_rounded,color:Colors.white70,size:17),
                    const SizedBox(width:4),
                    Text('${(veri['viewCount'] as num?)?.toInt()??0}',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800)),
                    const SizedBox(width:10),
                    const Icon(Icons.reply_rounded,color:Colors.white70,size:17),
                    const SizedBox(width:4),
                    Text('${(veri['replyCount'] as num?)?.toInt()??0}',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800)),
                    const SizedBox(width:10),
                    const Text('❤️',style:TextStyle(fontSize:15)),
                    const SizedBox(width:3),
                    Text('${(veri['reactionCount'] as num?)?.toInt()??0}',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800)),
                  ]),
                ),
            ]),
          )),
        ]),
    );
  }
}
