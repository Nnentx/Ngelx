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
        raise SystemExit("Build 329 patch failed: marker not found: "+label)
    return text.replace(old,new,1)

pub=rep(pub,"version: 1.0.109+328","version: 1.0.110+329","version")
main=main.replace("defaultValue: '1.0.109'","defaultValue: '1.0.110'")
main=main.replace("defaultValue: '328'","defaultValue: '329'")

# ---- Live start notifications: friends + followers with visibility rules ----
old_notify="""      final canliHedefler=List<String>.from(profil.data()?['friends']??const[]);
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
      }"""
new_notify="""      final profilVeri=profil.data()??<String,dynamic>{};
      final arkadaslar=<String>{
        ...List<String>.from(profilVeri['friends']??const[]),
        ...List<String>.from(profilVeri['friendIds']??const[]),
      };
      final takipciler=<String>{
        ...List<String>.from(profilVeri['followers']??const[]),
        ...List<String>.from(profilVeri['followerIds']??const[]),
      };
      final canliHedefler=<String>{
        if(gizlilik=='Arkadaşlar')...arkadaslar,
        if(gizlilik=='Takipçiler')...takipciler,
        if(gizlilik=='Herkese açık')...arkadaslar,
        if(gizlilik=='Herkese açık')...takipciler,
      }..remove(user.uid);
      if(canliHedefler.isNotEmpty){
        unawaited(Future.wait(canliHedefler.take(120).map((hedefUid)=>uygulamaBildirimiGonder(
          toUid:hedefUid,
          fromUid:user.uid,
          tur:'live',
          metin:'canlı yayın başlattı',
          belgeId:belge.id,
          hedefTuru:'live',
          hedefBaslik:baslik.text.trim(),
          olayTuru:'live_started',
          onizleme:baslik.text.trim(),
          dedupeKey:'live_${belge.id}_$hedefUid',
        ))));
      }"""
live=rep(live,old_notify,new_notify,"live notification recipients")

# Store reconnect credentials on page (kept in memory only)
live=rep(live,
"""  final String ownerId;
  final String username;
  const CanliYayinPage({""",
"""  final String ownerId;
  final String username;
  final String serverUrl;
  final String participantToken;
  const CanliYayinPage({""","page credential fields")

live=rep(live,
"""    this.ownerId = '',
    this.username = 'ngelx',
  });""",
"""    this.ownerId = '',
    this.username = 'ngelx',
    this.serverUrl = '',
    this.participantToken = '',
  });""","page credential constructor")

# Host page receives credentials
live=rep(live,
"""        ownerId: user.uid,
        username: ad,
      )));""",
"""        ownerId: user.uid,
        username: ad,
        serverUrl:cevap.serverUrl,
        participantToken:cevap.participantToken,
      )));""","host reconnect credentials")

# Lifecycle state
live=rep(live,
"""  Timer? heartbeat;
  int saniye = 0;""",
"""  Timer? heartbeat;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? canliDurumAboneligi;
  int saniye = 0;""","lifecycle subscription")

live=rep(live,
"""  bool katilimKaydiYapildi = false;
  int maxIzleyici = 0;""",
"""  bool katilimKaydiYapildi = false;
  bool yayinBitti=false;
  bool yenidenBaglaniyor=false;
  bool uzakKameraAcik=true;
  int yenidenBaglanmaDenemesi=0;
  String bitisMesaji='Canlı yayın sona erdi.';
  int maxIzleyici = 0;""","lifecycle states")

# init live state subscription
live=rep(live,
"""    kameraAcik = widget.ilkKameraAcik;
    widget.oda.addListener(_yenile);
    if (!widget.yayinSahibi) {
      unawaited(_katildimKaydet());
    } else {""",
"""    kameraAcik = widget.ilkKameraAcik;
    uzakKameraAcik=widget.ilkKameraAcik;
    widget.oda.addListener(_yenile);
    canliDurumAboneligi=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots().listen((snap){
      final v=snap.data()??<String,dynamic>{};
      if(!widget.yayinSahibi&&v.isNotEmpty){
        final kameraDurumu=v['cameraEnabled']!=false;
        if(mounted&&uzakKameraAcik!=kameraDurumu)setState(()=>uzakKameraAcik=kameraDurumu);
        if(v['active']==false&&!yayinBitti){
          final neden=(v['endReason']??'').toString();
          unawaited(_izleyicideYayinBitti(neden));
        }
      }
    });
    if (!widget.yayinSahibi) {
      unawaited(_katildimKaydet());
    } else {""","live state listener")

# Reconnect when room actually disconnects
live=rep(live,
"""  void _yenile() {
    if (mounted) setState(() {});
  }

  Future<void> _heartbeatYaz()async{""",
"""  void _yenile() {
    if (mounted) setState(() {});
    if(widget.oda.connectionState==lk.ConnectionState.disconnected&&!kapatildi&&!yayinBitti){
      unawaited(_otomatikYenidenBaglan());
    }
  }

  Future<void> _izleyicideYayinBitti(String neden)async{
    if(widget.yayinSahibi||yayinBitti)return;
    sayac?.cancel();
    bitisMesaji=neden=='host_ended'?'Yayıncı canlı yayını bitirdi.':'Canlı yayın sona erdi.';
    if(mounted)setState(()=>yayinBitti=true);
    try{await widget.oda.disconnect();}catch(_){}
  }

  Future<void> _otomatikYenidenBaglan()async{
    if(yenidenBaglaniyor||kapatildi||yayinBitti||widget.serverUrl.isEmpty||widget.participantToken.isEmpty)return;
    yenidenBaglaniyor=true;
    if(mounted)setState((){});
    for(var deneme=1;deneme<=3;deneme++){
      yenidenBaglanmaDenemesi=deneme;
      if(mounted)setState((){});
      if(!widget.yayinSahibi){
        try{
          final doc=await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).get(const GetOptions(source:Source.server));
          final v=doc.data()??<String,dynamic>{};
          if(v['active']==false){
            yenidenBaglaniyor=false;
            await _izleyicideYayinBitti((v['endReason']??'').toString());
            return;
          }
        }catch(_){}
      }
      await Future<void>.delayed(Duration(seconds:deneme==1?1:deneme==2?2:4));
      if(kapatildi||yayinBitti)break;
      try{
        await widget.oda.connect(widget.serverUrl,widget.participantToken);
        if(widget.oda.connectionState==lk.ConnectionState.connected){
          if(widget.yayinSahibi){
            try{
              await widget.oda.localParticipant?.setCameraEnabled(kameraAcik,cameraCaptureOptions:widget.kameraAyarlari.copyWith(cameraPosition:arkaKamera?lk.CameraPosition.back:lk.CameraPosition.front));
              await widget.oda.localParticipant?.setMicrophoneEnabled(mikrofonAcik);
            }catch(_){}
            unawaited(_heartbeatYaz());
          }
          yenidenBaglaniyor=false;
          yenidenBaglanmaDenemesi=0;
          if(mounted)setState((){});
          return;
        }
      }catch(_){}
    }
    yenidenBaglaniyor=false;
    if(mounted)setState((){});
  }

  Future<void> _heartbeatYaz()async{""","reconnect lifecycle")

live=rep(live,
"""  Future<void> _heartbeatYaz()async{
    if(!widget.yayinSahibi||kapatildi)return;
    try{""",
"""  Future<void> _heartbeatYaz()async{
    if(!widget.yayinSahibi||kapatildi||widget.oda.connectionState==lk.ConnectionState.disconnected)return;
    try{""","heartbeat disconnected guard")

# Camera/mic status must propagate to viewers
live=rep(live,
"""      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      if (mounted) setState(() => mikrofonAcik = yeni);""",
"""      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'microphoneEnabled':yeni},SetOptions(merge:true));
      if (mounted) setState(() => mikrofonAcik = yeni);""","mic state firestore")

live=rep(live,
"""      await widget.oda.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: widget.kameraAyarlari.copyWith(cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front),
      );
      if (mounted) setState(() => kameraAcik = yeni);""",
"""      await widget.oda.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: widget.kameraAyarlari.copyWith(cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front),
      );
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'cameraEnabled':yeni},SetOptions(merge:true));
      if (mounted) setState(() => kameraAcik = yeni);""","camera state firestore")

# End broadcast: write end state before room disconnect so viewers see it instantly
live=rep(live,
"""      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active': false,
        'endedAt': FieldValue.serverTimestamp(),""",
"""      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active': false,
        'status':'ended',
        'endReason':'host_ended',
        'endedAt': FieldValue.serverTimestamp(),
        'lastHeartbeatAt':FieldValue.serverTimestamp(),
        'cameraEnabled':false,""","end state broadcast")

# End confirmation clearer
live=rep(live,
"""        content: const Text('Canlı yayın tüm izleyiciler için kapanacak.'),""",
"""        content: const Text('Canlı yayın tüm izleyiciler için anında kapanacak, Keşfet’ten kaldırılacak ve bildirimlerde “yayın sona erdi” olarak görünecek.'),""","end dialog copy")

# Connection badge reflects retry/end state
live=rep(live,
"""    String yazi='Bağlı';
    Color renk=const Color(0xFF27D17F);
    if(durum==lk.ConnectionState.reconnecting||durum==lk.ConnectionState.connecting){""",
"""    String yazi='Bağlı';
    Color renk=const Color(0xFF27D17F);
    if(yayinBitti){
      yazi='Sona erdi';
      renk=Colors.white54;
    }else if(yenidenBaglaniyor){
      yazi='Tekrar $yenidenBaglanmaDenemesi/3';
      renk=const Color(0xFFFFB020);
    }else if(durum==lk.ConnectionState.reconnecting||durum==lk.ConnectionState.connecting){""","connection badge retry")

# Camera-off and reconnect states distinct from track errors
track_helper="""
  Widget _goruntuYokEkrani(){
    final kameraKapali=widget.yayinSahibi?!kameraAcik:!uzakKameraAcik;
    if(kameraKapali){
      return const ColoredBox(
        color:Colors.black,
        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(Icons.videocam_off_rounded,color:Colors.white54,size:58),
          SizedBox(height:12),
          Text('Kamera kapalı',style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
          SizedBox(height:5),
          Text('Canlı yayın ses ve yorumlarla devam ediyor.',style:TextStyle(color:Colors.white60,fontWeight:FontWeight.w600)),
        ])),
      );
    }
    if(yenidenBaglaniyor||widget.oda.connectionState==lk.ConnectionState.reconnecting){
      return ColoredBox(
        color:Colors.black,
        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          const CircularProgressIndicator(color:Color(0xFFFFB020)),
          const SizedBox(height:13),
          Text('Yeniden bağlanıyor… ${yenidenBaglanmaDenemesi>0?'$yenidenBaglanmaDenemesi/3':''}',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900)),
          const SizedBox(height:5),
          const Text('Yayın bağlantısı korunuyor.',style:TextStyle(color:Colors.white60)),
        ])),
      );
    }
    if(widget.oda.connectionState==lk.ConnectionState.disconnected){
      return ColoredBox(
        color:Colors.black,
        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          const Icon(Icons.wifi_off_rounded,color:Color(0xFFFF5A67),size:54),
          const SizedBox(height:12),
          const Text('Yayın bağlantısı kesildi',style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
          const SizedBox(height:8),
          FilledButton.icon(onPressed:_otomatikYenidenBaglan,icon:const Icon(Icons.refresh_rounded),label:const Text('Tekrar bağlan')),
        ])),
      );
    }
    return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      const CircularProgressIndicator(color:Colors.white),
      const SizedBox(height:12),
      Text(saniye<8?'Yayın görüntüsü hazırlanıyor…':'Yayın görüntüsü alınamadı. Bağlantı sürüyorsa kamerayı yeniden açmayı dene.',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
    ]));
  }

"""
live=rep(live,
"""  Future<void> _hediyeGonder(String ad, String emoji, int puan) async {""",
track_helper+"""  Future<void> _hediyeGonder(String ad, String emoji, int puan) async {""","missing video helper")

live=rep(live,
"""            child:track==null
              ?Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const CircularProgressIndicator(color:Colors.white),
                const SizedBox(height:12),
                Text(saniye<8?'Yayın görüntüsü hazırlanıyor…':'Yayın görüntüsü alınamadı. Tekrar bağlanmayı deneyebilirsin.',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
              ]))
              :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"""            child:track==null
              ?_goruntuYokEkrani()
              :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""","track fallback use")

# Viewer end overlay on top of all controls
live=rep(live,
"""          SafeArea(child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(children: [""",
"""          SafeArea(child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(children: [""","safearea keep")

live=rep(live,
"""          )),
        ]),
      ),
    );
  }
}""",
"""          )),
          if(yayinBitti)Positioned.fill(child:ColoredBox(
            color:const Color(0xF2111111),
            child:SafeArea(child:Center(child:Padding(
              padding:const EdgeInsets.all(28),
              child:Column(mainAxisSize:MainAxisSize.min,children:[
                const Icon(Icons.stop_circle_rounded,color:Color(0xFFFF1744),size:74),
                const SizedBox(height:16),
                const Text('CANLI YAYIN SONA ERDİ',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:23,fontWeight:FontWeight.w900)),
                const SizedBox(height:8),
                Text(bitisMesaji,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontSize:14,fontWeight:FontWeight.w600)),
                const SizedBox(height:22),
                FilledButton.icon(
                  style:FilledButton.styleFrom(backgroundColor:Colors.white,foregroundColor:Colors.black,minimumSize:const Size(220,50)),
                  onPressed:()async{await _bitir(geriDon:false);if(mounted)Navigator.pop(context);},
                  icon:const Icon(Icons.explore_rounded),
                  label:const Text('Keşfet’e dön',style:TextStyle(fontWeight:FontWeight.w900)),
                ),
              ]),
            ))),
          )),
        ]),
      ),
    );
  }
}""","viewer end overlay")

# Dispose stream subscription
live=rep(live,
"""    heartbeat?.cancel();
    yorum.dispose();""",
"""    heartbeat?.cancel();
    canliDurumAboneligi?.cancel();
    yorum.dispose();""","lifecycle subscription dispose")

# ---- Main join route receives credentials/camera state and ended wording ----
main=rep(main,
"""        content:const Text('Bu canlı yayın sona ermiş.',style:TextStyle(fontWeight:FontWeight.w700)),""",
"""        content:const Text('Bu canlı yayın bitti.',style:TextStyle(fontWeight:FontWeight.w700)),""","ended join wording")

main=rep(main,
"""      ownerId:(veri['ownerId']??'').toString(),
      username:(veri['username']??'ngelx').toString(),
    )));""",
"""      ownerId:(veri['ownerId']??'').toString(),
      username:(veri['username']??'ngelx').toString(),
      ilkKameraAcik:veri['cameraEnabled']!=false,
      serverUrl:cevap.serverUrl,
      participantToken:cevap.participantToken,
    )));""","viewer reconnect credentials")

# Notification helper respects deactivated/blocked users
main=rep(main,
"""  final ayar=hedef.data()??{};
  if(List<String>.from(ayar['restrictedUsers']??const[]).contains(fromUid))return;
  if(ayar['notificationsEnabled']==false)return;""",
"""  final ayar=hedef.data()??{};
  if(ayar['deactivated']==true)return;
  if(List<String>.from(ayar['blocked']??const[]).contains(fromUid))return;
  if(List<String>.from(ayar['restrictedUsers']??const[]).contains(fromUid))return;
  if(ayar['notificationsEnabled']==false)return;""","notification target block")

main=rep(main,
"""  final gonderenVeri=gonderen.data()??{};
  final gonderenAdi=(gonderenVeri['displayName']??gonderenVeri['username']??'NgelX kullanıcısı').toString();""",
"""  final gonderenVeri=gonderen.data()??{};
  if(gonderenVeri['deactivated']==true)return;
  if(List<String>.from(gonderenVeri['blocked']??const[]).contains(toUid))return;
  final gonderenAdi=(gonderenVeri['displayName']??gonderenVeri['username']??'NgelX kullanıcısı').toString();""","notification sender block")

# Dynamic notification title for ended live streams
notif_widget="""
  bool _canliAktivitesi(Map<String,dynamic> v){
    final tur=(v['type']??'').toString();
    final hedef=(v['targetKind']??'').toString();
    final olay=(v['eventKind']??'').toString();
    return tur=='live'||hedef=='live'||olay=='live_started'||olay=='live_share';
  }

  Widget _bildirimBasligiDurumlu(Map<String,dynamic> v,bool okundu){
    if(!_canliAktivitesi(v))return _bildirimBasligi(v,okundu);
    final kaynak=(v['sourceId']??v['belgeId']??'').toString();
    if(kaynak.isEmpty)return _bildirimBasligi(v,okundu);
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(kaynak).snapshots(),
      builder:(_,snap){
        final canli=snap.data?.data();
        final aktif=canli!=null&&ngelxCanliKaydiTaze(canli);
        if(aktif)return _bildirimBasligi(v,okundu);
        final ad=(v['senderName']??v['fromName']??'NgelX kullanıcısı').toString().trim();
        return Text.rich(
          TextSpan(children:[
            TextSpan(text:ad.isEmpty?'Canlı yayın':ad,style:const TextStyle(fontWeight:FontWeight.w900)),
            const TextSpan(text:' • Canlı yayın sona erdi'),
          ]),
          style:TextStyle(color:Colors.black54,fontWeight:okundu?FontWeight.w500:FontWeight.w700),
        );
      },
    );
  }

"""
main=rep(main,
"""  Widget _bildirimBasligi(Map<String,dynamic> v,bool okundu){""",
notif_widget+"""  Widget _bildirimBasligi(Map<String,dynamic> v,bool okundu){""","live notification status widget")

# Notification tap: live_share/type live both validate before navigation
old_route="""    final hedefTuru=(v['targetKind']??'').toString();

    if(tur=='live'&&kaynak.isNotEmpty){
      await ngelxCanliYayinaKatil(context,kaynak);
      return;
    }

    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){"""
new_route="""    final hedefTuru=(v['targetKind']??'').toString();
    final olay=(v['eventKind']??'').toString();
    final canliHedefi=tur=='live'||hedefTuru=='live'||olay=='live_started'||olay=='live_share';

    if(canliHedefi&&kaynak.isNotEmpty){
      try{
        final canli=await FirebaseFirestore.instance.collection('live_streams').doc(kaynak).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        final cv=canli.data()??<String,dynamic>{};
        if(!ngelxCanliKaydiTaze(cv)){
          try{await d.reference.set({'liveEnded':true},SetOptions(merge:true));}catch(_){}
          if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content:const Text('Bu canlı yayın bitti.',style:TextStyle(fontWeight:FontWeight.w800)),
            behavior:SnackBarBehavior.floating,width:230,duration:const Duration(milliseconds:1400),
            shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
          ));
          return;
        }
      }catch(_){}
      if(context.mounted)await ngelxCanliYayinaKatil(context,kaynak);
      return;
    }

    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){"""
main=rep(main,old_route,new_route,"notification live tap guard")

# Remove duplicate later olay declaration
main=rep(main,
"""    final olay=(v['eventKind']??'').toString();
    if(hedefTuru=='group'&&kaynak.isNotEmpty&&tur!='call'){""",
"""    if(hedefTuru=='group'&&kaynak.isNotEmpty&&tur!='call'){""","remove duplicate notification event")

# Render status-aware title
main=rep(main,
"""              title: _bildirimBasligi(v,okundu),""",
"""              title:_bildirimBasligiDurumlu(v,okundu),""","notification title renderer")

LIVE.write_text(live,encoding="utf-8")
MAIN.write_text(main,encoding="utf-8")
PUB.write_text(pub,encoding="utf-8")
print("Build 329 live lifecycle, reconnect and notification package applied.")
