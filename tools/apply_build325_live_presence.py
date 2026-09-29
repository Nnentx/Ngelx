#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/"app/lib/main.dart"
LIVE=ROOT/"app/lib/live_broadcast_studio.dart"
PUB=ROOT/"app/pubspec.yaml"

main=MAIN.read_text(encoding="utf-8")
live=LIVE.read_text(encoding="utf-8")
pub=PUB.read_text(encoding="utf-8")

def rep(text,old,new,label):
    if old not in text:
        raise SystemExit("Build 325 patch failed: marker not found: "+label)
    return text.replace(old,new,1)

pub=rep(pub,"version: 1.0.105+324","version: 1.0.106+325","version")
main=main.replace("defaultValue: '1.0.105'","defaultValue: '1.0.106'")
main=main.replace("defaultValue: '324'","defaultValue: '325'")

# Global helper: notification/profile -> active live stream.
main=rep(
    main,
    "String ngelxBildirimBelgeId(String raw){",
    """Future<void> ngelxCanliYayinaKatil(BuildContext context,String belgeId)async{
  if(belgeId.isEmpty||await misafirEngeli(context))return;
  final user=FirebaseAuth.instance.currentUser;
  if(user==null)return;
  lk.Room? oda;
  try{
    final belge=await FirebaseFirestore.instance.collection('live_streams').doc(belgeId).get().timeout(const Duration(seconds:8));
    final veri=belge.data()??<String,dynamic>{};
    final roomName=(veri['roomName']??'').toString();
    if(veri['active']!=true||roomName.isEmpty){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu canlı yayın sona ermiş.')));
      return;
    }
    final kaynak=lk.DevelopmentTokenSource(id:liveKitTestSunucuId);
    final kimlik='${user.uid}-${DateTime.now().millisecondsSinceEpoch}';
    final cevap=await kaynak.fetch(lk.TokenRequestOptions(
      roomName:roomName,
      participantIdentity:kimlik,
      participantName:user.displayName?.isNotEmpty==true?user.displayName!:'NgelX izleyicisi',
      participantAttributes:const {'role':'viewer'},
    ));
    oda=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
    await oda.connect(cevap.serverUrl,cevap.participantToken);
    if(!context.mounted){
      await oda.disconnect();
      await oda.dispose();
      return;
    }
    Navigator.push(context,MaterialPageRoute(builder:(_)=>CanliYayinPage(
      oda:oda!,
      belgeId:belgeId,
      baslik:(veri['title']??'NgelX canlı yayını').toString(),
      yayinSahibi:false,
      ownerId:(veri['ownerId']??'').toString(),
      username:(veri['username']??'ngelx').toString(),
    )));
  }catch(e){
    if(oda!=null){try{await oda.disconnect();await oda.dispose();}catch(_){}}
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayına şu anda bağlanılamadı.')));
  }
}

String ngelxBildirimBelgeId(String raw){""",
    "global live join helper",
)

# Live notification preference support.
main=rep(
    main,
    "  final aramaBildirimi=tur=='call';\n",
    "  final aramaBildirimi=tur=='call';\n  final canliBildirimi=tur=='live'||olayTuru=='live_started';\n",
    "live notification classifier",
)
main=rep(
    main,
    "  if(aramaBildirimi&&ayar['callNotifications']==false)return;\n",
    "  if(aramaBildirimi&&ayar['callNotifications']==false)return;\n  if(canliBildirimi&&ayar['liveNotifications']==false)return;\n",
    "live notification setting",
)

# Feed profile avatar listens to live presence in real time.
main=rep(
    main,
    "  String profilFoto = '';\n  PageRoute<dynamic>? _rota;",
    "  String profilFoto = '';\n  bool profilCanli=false;\n  String profilCanliId='';\n  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _profilCanliAboneligi;\n  PageRoute<dynamic>? _rota;",
    "feed live state",
)
main=rep(
    main,
    """  Future<void> profilFotosunuGetir() async {
    if(_profilFotoIstendi)return;
    _profilFotoIstendi=true;
    if (widget.ownerId.isEmpty) return;
    final belge = await FirebaseFirestore.instance
        .collection('users')
        .doc(widget.ownerId)
        .get();
    if (!mounted) return;
    setState(() => profilFoto = (belge.data()?['photoUrl'] ?? '').toString());
  }""",
    """  Future<void> profilFotosunuGetir() async {
    if(_profilFotoIstendi)return;
    _profilFotoIstendi=true;
    if(widget.ownerId.isEmpty)return;
    await _profilCanliAboneligi?.cancel();
    _profilCanliAboneligi=FirebaseFirestore.instance.collection('users').doc(widget.ownerId).snapshots().listen((belge){
      if(!mounted)return;
      final v=belge.data()??<String,dynamic>{};
      setState((){
        profilFoto=(v['photoUrl']??'').toString();
        profilCanli=v['isLive']==true&&(v['currentLiveId']??'').toString().isNotEmpty;
        profilCanliId=(v['currentLiveId']??'').toString();
      });
    });
  }""",
    "feed profile live listener",
)
main=rep(
    main,
    "    kontrol.removeListener(_kesimKontrol);\n    final p=muzikOynatici;",
    "    kontrol.removeListener(_kesimKontrol);\n    unawaited(_profilCanliAboneligi?.cancel());\n    final p=muzikOynatici;",
    "feed listener dispose",
)
main=rep(
    main,
    """              GestureDetector(
                onTap:paylasanProfiliAc,
                child:CircleAvatar(
                  radius:27,
                  backgroundColor:mavi,
                  child:CircleAvatar(
                    radius:23,
                    backgroundColor:panel,
                    backgroundImage:profilFoto.isEmpty?null:NgelXAgImageProvider(profilFoto),
                    child:profilFoto.isNotEmpty?null:const Text('N',style:TextStyle(fontWeight:FontWeight.bold)),
                  ),
                ),
              ),""",
    """              GestureDetector(
                onTap:paylasanProfiliAc,
                child:Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[
                  CircleAvatar(
                    radius:28,
                    backgroundColor:profilCanli?const Color(0xFFFF1744):mavi,
                    child:CircleAvatar(
                      radius:23,
                      backgroundColor:panel,
                      backgroundImage:profilFoto.isEmpty?null:NgelXAgImageProvider(profilFoto),
                      child:profilFoto.isNotEmpty?null:const Text('N',style:TextStyle(fontWeight:FontWeight.bold)),
                    ),
                  ),
                  if(profilCanli)Positioned(bottom:-5,child:Container(
                    padding:const EdgeInsets.symmetric(horizontal:6,vertical:2),
                    decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(7),border:Border.all(color:Colors.white,width:1)),
                    child:const Text('CANLI',style:TextStyle(color:Colors.white,fontSize:8,fontWeight:FontWeight.w900)),
                  )),
                ]),
              ),""",
    "feed live ring",
)

# Chat list live ring + realtime user document.
main=rep(
    main,
    "return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:_kullaniciGetir(other),builder:(_,u){",
    "return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(other).snapshots(),builder:(_,u){",
    "chat user realtime",
)
main=rep(
    main,
    "                leading:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:NgelXAgImageProvider(p['photoUrl'])),",
    """                leading:Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[
                  Container(
                    padding:EdgeInsets.all(p['isLive']==true?2.5:0),
                    decoration:BoxDecoration(shape:BoxShape.circle,border:p['isLive']==true?Border.all(color:const Color(0xFFFF1744),width:2.5):null),
                    child:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:NgelXAgImageProvider(p['photoUrl'])),
                  ),
                  if(p['isLive']==true)const Positioned(bottom:-4,child:Text('CANLI',style:TextStyle(color:Color(0xFFFF1744),fontSize:7.5,fontWeight:FontWeight.w900))),
                ]),""",
    "chat live ring",
)

# Notification activity icon/color and tap opens live.
main=rep(
    main,
    "  IconData _ikon(String tur){switch(tur){case 'like':case 'interaction':return Icons.favorite_rounded;case 'comment':return Icons.mode_comment_rounded;case 'message':return Icons.chat_bubble_rounded;case 'security':return Icons.shield_rounded;case 'friend':case 'follow_request':case 'friend_request':return Icons.person_add_alt_1_rounded;case 'friend_accepted':return Icons.people_rounded;case 'follow_accepted':return Icons.person_rounded;default:return Icons.notifications_rounded;}}",
    "  IconData _ikon(String tur){switch(tur){case 'live':return Icons.live_tv_rounded;case 'like':case 'interaction':return Icons.favorite_rounded;case 'comment':return Icons.mode_comment_rounded;case 'message':return Icons.chat_bubble_rounded;case 'security':return Icons.shield_rounded;case 'friend':case 'follow_request':case 'friend_request':return Icons.person_add_alt_1_rounded;case 'friend_accepted':return Icons.people_rounded;case 'follow_accepted':return Icons.person_rounded;default:return Icons.notifications_rounded;}}",
    "activity live icon",
)
main=rep(
    main,
    "  Color _renk(String tur){switch(tur){case 'like':case 'interaction':return const Color(0xFFFF3B73);case 'comment':return Colors.blue;case 'security':return Colors.orange;case 'friend':case 'follow_request':case 'friend_request':return mor;default:return const Color(0xFF20B86A);}}",
    "  Color _renk(String tur){switch(tur){case 'live':return const Color(0xFFFF1744);case 'like':case 'interaction':return const Color(0xFFFF3B73);case 'comment':return Colors.blue;case 'security':return Colors.orange;case 'friend':case 'follow_request':case 'friend_request':return mor;default:return const Color(0xFF20B86A);}}",
    "activity live color",
)
main=rep(
    main,
    "    final hedefTuru=(v['targetKind']??'').toString();\n\n    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){",
    """    final hedefTuru=(v['targetKind']??'').toString();

    if(tur=='live'&&kaynak.isNotEmpty){
      await ngelxCanliYayinaKatil(context,kaynak);
      return;
    }

    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){""",
    "activity live navigation",
)

# Profile page shows live ring + direct watch button.
main=rep(
    main,
    "          final foto = (v['photoUrl'] ?? '').toString();\n          final arkadaslar =",
    "          final foto = (v['photoUrl'] ?? '').toString();\n          final canli=v['isLive']==true&&(v['currentLiveId']??'').toString().isNotEmpty;\n          final canliId=(v['currentLiveId']??'').toString();\n          final arkadaslar =",
    "profile live state",
)
main=rep(
    main,
    """              Center(child:NgelXHikayeliAvatar(
                uid:uid,
                fotoUrl:foto,
                kullanici:'@'+(v['username']??'ngelx').toString(),
                radius:55,
                etkin:erisimVar,
              )),""",
    """              Center(child:Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[
                Container(
                  padding:EdgeInsets.all(canli?4:0),
                  decoration:BoxDecoration(shape:BoxShape.circle,border:canli?Border.all(color:const Color(0xFFFF1744),width:3):null),
                  child:NgelXHikayeliAvatar(
                    uid:uid,
                    fotoUrl:foto,
                    kullanici:'@'+(v['username']??'ngelx').toString(),
                    radius:55,
                    etkin:erisimVar,
                  ),
                ),
                if(canli)Positioned(bottom:-7,child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:10,vertical:3),
                  decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(9),border:Border.all(color:Colors.white,width:1.5)),
                  child:const Text('CANLI',style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900)),
                )),
              ])),""",
    "profile live ring",
)
main=rep(
    main,
    """              Wrap(alignment:WrapAlignment.center,spacing:12,runSpacing:6,children:[
                if((v['createdAt']??v['joinedAt']) is Timestamp)
                  Text('NgelX’e katıldı: '+((v['createdAt']??v['joinedAt']) as Timestamp).toDate().year.toString(),style:const TextStyle(color:Colors.black54,fontSize:12)),
                AktiflikDurumuYazisi(uid:uid),
              ]),
              if((v['introVideoUrl']??'').toString().isNotEmpty) ...[""",
    """              Wrap(alignment:WrapAlignment.center,spacing:12,runSpacing:6,children:[
                if((v['createdAt']??v['joinedAt']) is Timestamp)
                  Text('NgelX’e katıldı: '+((v['createdAt']??v['joinedAt']) as Timestamp).toDate().year.toString(),style:const TextStyle(color:Colors.black54,fontSize:12)),
                AktiflikDurumuYazisi(uid:uid),
              ]),
              if(canli&&canliId.isNotEmpty)...[
                const SizedBox(height:12),
                Center(child:FilledButton.icon(
                  style:FilledButton.styleFrom(backgroundColor:const Color(0xFFFF1744),foregroundColor:Colors.white,padding:const EdgeInsets.symmetric(horizontal:22,vertical:12)),
                  onPressed:()=>ngelxCanliYayinaKatil(context,canliId),
                  icon:const Icon(Icons.live_tv_rounded),
                  label:const Text('Canlı yayını izle',style:TextStyle(fontWeight:FontWeight.w900)),
                )),
              ],
              if((v['introVideoUrl']??'').toString().isNotEmpty) ...[""",
    "profile watch live button",
)

# Intro video: after play, center overlay disappears; tap reveals controls briefly.
main=rep(
    main,
    "  bool hazir=false,yukleniyor=false,hata=false;\n  PageRoute<dynamic>? _rota;",
    "  bool hazir=false,yukleniyor=false,hata=false,kontrollerGorunur=false,sessiz=false;\n  Timer? kontrolZamanlayici;\n  PageRoute<dynamic>? _rota;",
    "intro video control state",
)
main=rep(
    main,
    """  void _yenidenGorunur(){
    final x=c;
    if(_geriDonusteOynat&&x?.value.isInitialized==true)unawaited(x!.play());
    _geriDonusteOynat=false;
  }""",
    """  void _yenidenGorunur(){
    final x=c;
    if(_geriDonusteOynat&&x?.value.isInitialized==true)unawaited(x!.play());
    _geriDonusteOynat=false;
  }
  void _kontrolleriGoster(){
    if(!mounted)return;
    kontrolZamanlayici?.cancel();
    setState(()=>kontrollerGorunur=true);
    kontrolZamanlayici=Timer(const Duration(seconds:2),(){
      final x=c;
      if(mounted&&x?.value.isPlaying==true)setState(()=>kontrollerGorunur=false);
    });
  }
  void _videoDurumu(){
    final x=c;
    if(!mounted||x==null||!x.value.isInitialized)return;
    final bitti=x.value.duration>Duration.zero&&x.value.position>=x.value.duration-const Duration(milliseconds:180)&&!x.value.isPlaying;
    if(bitti&&!kontrollerGorunur)setState(()=>kontrollerGorunur=true);
  }""",
    "intro control helpers",
)
main=rep(
    main,
    """      await x.initialize();
      await x.setLooping(false);
      if(!mounted)return;
      setState(()=>hazir=true);
      await x.play();""",
    """      await x.initialize();
      await x.setLooping(false);
      await x.setVolume(sessiz?0:1);
      x.addListener(_videoDurumu);
      if(!mounted)return;
      setState((){hazir=true;kontrollerGorunur=false;});
      await x.play();""",
    "intro auto hide after play",
)
main=rep(
    main,
    """  @override void dispose(){
    WidgetsBinding.instance.removeObserver(this);
    ngelxRouteObserver.unsubscribe(this);
    final x=c;if(x!=null)unawaited(x.dispose());
    super.dispose();
  }""",
    """  @override void dispose(){
    WidgetsBinding.instance.removeObserver(this);
    ngelxRouteObserver.unsubscribe(this);
    kontrolZamanlayici?.cancel();
    final x=c;
    if(x!=null){x.removeListener(_videoDurumu);unawaited(x.dispose());}
    super.dispose();
  }""",
    "intro dispose",
)
main=rep(
    main,
    """    return SizedBox(
      height:150,
      width:double.infinity,
      child:ClipRRect(
        borderRadius:BorderRadius.circular(18),
        child:ColoredBox(
          color:Colors.black,
          child:Stack(fit:StackFit.expand,children:[
            Center(child:AspectRatio(
              aspectRatio:x.value.aspectRatio==0?16/9:x.value.aspectRatio,
              child:VideoPlayer(x),
            )),
            Center(child:IconButton.filledTonal(
              onPressed:(){setState((){x.value.isPlaying?x.pause():x.play();});},
              icon:Icon(x.value.isPlaying?Icons.pause_rounded:Icons.play_arrow_rounded,size:32),
            )),
          ]),
        ),
      ),
    );""",
    """    final videoOrani=x.value.aspectRatio==0?16/9:x.value.aspectRatio;
    final yukseklik=videoOrani<1?340.0:210.0;
    return SizedBox(
      height:yukseklik,
      width:double.infinity,
      child:ClipRRect(
        borderRadius:BorderRadius.circular(18),
        child:GestureDetector(
          onTap:_kontrolleriGoster,
          child:ColoredBox(
            color:Colors.black,
            child:Stack(fit:StackFit.expand,children:[
              Center(child:AspectRatio(aspectRatio:videoOrani,child:VideoPlayer(x))),
              Positioned(top:8,right:8,child:IconButton.filledTonal(
                tooltip:sessiz?'Sesi aç':'Sesi kapat',
                onPressed:()async{
                  sessiz=!sessiz;
                  await x.setVolume(sessiz?0:1);
                  if(mounted)setState((){});
                },
                icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded),
              )),
              if(kontrollerGorunur||!x.value.isPlaying)Center(child:IconButton.filledTonal(
                onPressed:()async{
                  if(x.value.isPlaying){
                    await x.pause();
                    if(mounted)setState(()=>kontrollerGorunur=true);
                  }else{
                    if(x.value.duration>Duration.zero&&x.value.position>=x.value.duration-const Duration(milliseconds:180))await x.seekTo(Duration.zero);
                    await x.play();
                    if(mounted)setState(()=>kontrollerGorunur=false);
                  }
                },
                icon:Icon(x.value.isPlaying?Icons.pause_rounded:Icons.play_arrow_rounded,size:32),
              )),
            ]),
          ),
        ),
      ),
    );""",
    "intro clean player",
)

# Live start -> friends get a direct-open notification.
live=rep(
    live,
    """      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'isLive': true,
        'currentLiveId': belge.id,
        'liveTitle': baslik.text.trim(),
        'liveStartedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
      if (!mounted) return;""",
    """      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'isLive': true,
        'currentLiveId': belge.id,
        'liveTitle': baslik.text.trim(),
        'liveStartedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
      final canliHedefler=List<String>.from(profil.data()?['friends']??const[]);
      if(canliHedefler.isNotEmpty){
        unawaited(Future.wait(canliHedefler.take(60).map((hedefUid)=>uygulamaBildirimiGonder(
          toUid:hedefUid,
          fromUid:user.uid,
          tur:'live',
          metin:'canlı yayında',
          belgeId:belge.id,
          hedefTuru:'live',
          hedefBaslik:baslik.text.trim(),
          olayTuru:'live_started',
          onizleme:baslik.text.trim(),
          dedupeKey:'live_${belge.id}_$hedefUid',
        ))));
      }
      if (!mounted) return;""",
    "live friend notifications",
)

MAIN.write_text(main,encoding="utf-8")
LIVE.write_text(live,encoding="utf-8")
PUB.write_text(pub,encoding="utf-8")
print("Build 325 live presence, notifications and intro-video polish applied.")
