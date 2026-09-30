part of 'main.dart';


class _NgelXCanliFiltrePreset {
  final String ad;
  final double parlaklik, kontrast, doygunluk, sicaklik, netlik;
  const _NgelXCanliFiltrePreset(this.ad,{required this.parlaklik,required this.kontrast,required this.doygunluk,required this.sicaklik,required this.netlik});
}

const List<_NgelXCanliFiltrePreset> ngelxCanliProFiltreleri=[
  _NgelXCanliFiltrePreset('Doğal',parlaklik:-.015,kontrast:1.03,doygunluk:1.02,sicaklik:.01,netlik:.06),
  _NgelXCanliFiltrePreset('Canlı',parlaklik:0,kontrast:1.12,doygunluk:1.14,sicaklik:.025,netlik:.13),
  _NgelXCanliFiltrePreset('Portre Pro',parlaklik:.005,kontrast:1.05,doygunluk:1.04,sicaklik:.055,netlik:.05),
  _NgelXCanliFiltrePreset('Clean HD',parlaklik:-.01,kontrast:1.08,doygunluk:1.01,sicaklik:0,netlik:.16),
  _NgelXCanliFiltrePreset('Parlak',parlaklik:.035,kontrast:1.04,doygunluk:1.06,sicaklik:.02,netlik:.06),
  _NgelXCanliFiltrePreset('Sıcak',parlaklik:-.005,kontrast:1.06,doygunluk:1.08,sicaklik:.15,netlik:.07),
  _NgelXCanliFiltrePreset('Soğuk',parlaklik:-.01,kontrast:1.07,doygunluk:1.05,sicaklik:-.11,netlik:.08),
  _NgelXCanliFiltrePreset('Kontrast+',parlaklik:-.025,kontrast:1.19,doygunluk:1.08,sicaklik:.01,netlik:.18),
  _NgelXCanliFiltrePreset('Gece',parlaklik:.07,kontrast:1.03,doygunluk:1.04,sicaklik:.035,netlik:.04),
];

double _ngelxCanliDouble(dynamic value,double fallback)=>value is num?value.toDouble():fallback;

bool ngelxCanliKaydiTaze(Map<String,dynamic> veri){
  if(veri['active']!=true)return false;
  final simdi=DateTime.now();
  final hb=veri['lastHeartbeatAt'];
  if(hb is Timestamp)return simdi.difference(hb.toDate()).inSeconds<=85;
  final baslangic=veri['startedAt'];
  if(baslangic is Timestamp)return simdi.difference(baslangic.toDate()).inMinutes<=3;
  return false;
}

_NgelXCanliFiltrePreset ngelxCanliPresetBul(String? ad){
  final aranan=(ad??'').trim();
  for(final p in ngelxCanliProFiltreleri){if(p.ad==aranan)return p;}
  return ngelxCanliProFiltreleri.first;
}

List<double> ngelxCanliRenkMatrisi({
  required _NgelXCanliFiltrePreset preset,
  double parlaklik=0,double kontrast=1,double doygunluk=1,double sicaklik=0,double netlik=0,
  double ciltTonu=.10,double highlightKoruma=.72,double golgeAcma=.18,double guzellik=.34,
  bool otomatikIyilestirme=true,bool dusukIsik=false,
}){
  var b=(preset.parlaklik+parlaklik).clamp(-.18,.24).toDouble();
  var c=(preset.kontrast*kontrast).clamp(.75,1.55).toDouble();
  var s=(preset.doygunluk*doygunluk).clamp(.65,1.65).toDouble();
  var w=(preset.sicaklik+sicaklik).clamp(-.55,.55).toDouble();
  final n=(preset.netlik+netlik).clamp(0.0,1.0).toDouble();
  final hp=highlightKoruma.clamp(0.0,1.0).toDouble();
  final sh=golgeAcma.clamp(0.0,1.0).toDouble();
  final skin=ciltTonu.clamp(-1.0,1.0).toDouble();
  final beauty=guzellik.clamp(0.0,1.0).toDouble();
  if(otomatikIyilestirme){b+=.004;c*=.985;s*=1.018;w+=.006;}
  if(dusukIsik){b+=.050;c*=.955;s*=1.020;w+=.018;}
  b-=hp*.026;
  c*=1-(hp*.075);
  b+=sh*.040;
  c*=1-(sh*.024);
  w+=skin*.095;
  s*=1+(skin.abs()*.014);
  c*=1-(beauty*.060);
  s*=1-(beauty*.016);
  b+=beauty*.006;
  c=(c*(1+n*.085)).clamp(.75,1.60).toDouble();
  s=(s*(1+n*.035)).clamp(.65,1.70).toDouble();
  const lr=.2126,lg=.7152,lb=.0722;
  final inv=1-s;
  final wr=(1+w*.12).clamp(.90,1.10).toDouble();
  final wb=(1-w*.12).clamp(.90,1.10).toDouble();
  final offset=(1-c)*128+b*255;
  return <double>[
    (inv*lr+s)*c*wr,(inv*lg)*c*wr,(inv*lb)*c*wr,0,offset+w*5,
    (inv*lr)*c,(inv*lg+s)*c,(inv*lb)*c,0,offset,
    (inv*lr)*c*wb,(inv*lg)*c*wb,(inv*lb+s)*c*wb,0,offset-w*5,
    0,0,0,1,0,
  ];
}

Widget ngelxCanliEfektKatmani({required Widget child,required Map<String,dynamic> veri}){
  final preset=ngelxCanliPresetBul((veri['filterPro']??veri['filter']??'Doğal').toString());
  final beauty=_ngelxCanliDouble(veri['beauty']??veri['retouch'],.34).clamp(0.0,1.0).toDouble();
  final matris=ngelxCanliRenkMatrisi(
    preset:preset,
    parlaklik:_ngelxCanliDouble(veri['filterBrightness'],0),
    kontrast:_ngelxCanliDouble(veri['filterContrast'],1),
    doygunluk:_ngelxCanliDouble(veri['filterSaturation'],1),
    sicaklik:_ngelxCanliDouble(veri['filterWarmth'],0),
    netlik:_ngelxCanliDouble(veri['filterClarity'],.10),
    ciltTonu:_ngelxCanliDouble(veri['skinTone'],.10),
    highlightKoruma:_ngelxCanliDouble(veri['highlightProtect'],.72),
    golgeAcma:_ngelxCanliDouble(veri['shadowLift'],.18),
    guzellik:beauty,
    otomatikIyilestirme:veri['autoEnhance']!=false,
    dusukIsik:veri['lowLight']==true,
  );
  return ColorFiltered(
    colorFilter:ColorFilter.matrix(matris),
    child:Stack(fit:StackFit.expand,children:[
      child,
      if(beauty>.01)IgnorePointer(child:ColoredBox(color:const Color(0xFFFFE7DE).withOpacity((beauty*.012).clamp(0.0,.014).toDouble()))),
    ]),
  );
}

class CanliHazirlikPage extends StatefulWidget {
  const CanliHazirlikPage({super.key});
  @override
  State<CanliHazirlikPage> createState() => _CanliHazirlikPageState();
}

class _CanliHazirlikPageState extends State<CanliHazirlikPage> {
  final baslik = TextEditingController();
  bool baglaniyor = false;
  bool mikrofon = true;
  bool kamera = true;
  bool onizlemeHazirlaniyor = true;
  bool arkaKamera = false;
  bool flashAcik = false;
  double retus = .36;
  double parlaklik = 0;
  double kontrast = .98;
  double doygunluk = 1.03;
  double sicaklik = .02;
  double netlik = .08;
  double ciltTonu = .10;
  double highlightKoruma = .72;
  double golgeAcma = .18;
  bool otomatikIyilestirme = true;
  bool dusukIsik = false;
  int filtreIndex = 2;
  String oran = '9:16';
  String kalite = '720p';
  String gizlilik = 'Herkese açık';
  String kategori = 'Sohbet';
  int fps = 30;
  bool geriSayim = true;
  int baslangicSayaci = 0;
  bool _gizlilikElleDegisti = false;
  String? kameraHatasi;
  List<CameraDescription> kameralar = <CameraDescription>[];
  CameraController? onizleme;

  @override
  void initState() {
    super.initState();
    unawaited(_canliTercihleriniYukle());
    unawaited(_onizlemeyiBaslat());
  }

  Future<void> _canliTercihleriniYukle() async {
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null)return;
    try{
      final d=await FirebaseFirestore.instance.collection('users').doc(uid)
          .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:6));
      final kayit=(d.data()?['lastLiveVisibility']??'').toString();
      if(!_gizlilikElleDegisti&&mounted&&const ['Herkese açık','Takipçiler','Arkadaşlar'].contains(kayit)){
        setState(()=>gizlilik=kayit);
      }
    }catch(_){}
  }

  Future<void> _gizlilikDegistir(String yeni) async {
    if(!const ['Herkese açık','Takipçiler','Arkadaşlar'].contains(yeni))return;
    _gizlilikElleDegisti=true;
    if(mounted)setState(()=>gizlilik=yeni);
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null)return;
    try{
      await FirebaseFirestore.instance.collection('users').doc(uid).set({
        'lastLiveVisibility':yeni,
        'lastLiveVisibilityUpdatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:6));
    }catch(_){}
  }

  @override
  void dispose() {
    final controller = onizleme;
    onizleme = null;
    if (controller != null) unawaited(controller.dispose());
    baslik.dispose();
    super.dispose();
  }

  ResolutionPreset get _onizlemeKalitesi => switch (kalite) {
    '540p' => ResolutionPreset.medium,
    '1080p' => ResolutionPreset.veryHigh,
    _ => ResolutionPreset.high,
  };

  lk.VideoParameters get _yayinKalitesi => switch (kalite) {
    '540p' => lk.VideoParametersPresets.h540_169,
    '1080p' => lk.VideoParametersPresets.h1080_169,
    _ => lk.VideoParametersPresets.h720_169,
  };

  lk.CameraCaptureOptions get _kameraAyarlari => lk.CameraCaptureOptions(
    cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front,
    focusMode: lk.CameraFocusMode.auto,
    exposureMode: lk.CameraExposureMode.auto,
    params: _yayinKalitesi,
    maxFrameRate: fps.toDouble(),
    stopCameraCaptureOnMute: true,
  );

  Future<void> _onizlemeyiBaslat() async {
    if (!kamera || baglaniyor) return;
    if (mounted) setState(() { onizlemeHazirlaniyor = true; kameraHatasi = null; });
    try {
      final izin = await Permission.camera.request();
      if (!izin.isGranted) throw Exception('Kamera izni verilmedi.');
      kameralar = await availableCameras();
      if (kameralar.isEmpty) throw Exception('Bu cihazda kullanılabilir kamera bulunamadı.');
      var secilen = kameralar.indexWhere((k) => k.lensDirection == (arkaKamera ? CameraLensDirection.back : CameraLensDirection.front));
      if (secilen < 0) secilen = 0;
      arkaKamera = kameralar[secilen].lensDirection == CameraLensDirection.back;
      final eski = onizleme;
      onizleme = null;
      if (eski != null) {
        try { await eski.dispose(); } catch (_) {}
        await Future<void>.delayed(const Duration(milliseconds: 140));
      }
      final yeni = CameraController(kameralar[secilen], _onizlemeKalitesi, enableAudio: false, imageFormatGroup: ImageFormatGroup.jpeg);
      await yeni.initialize();
      try { await yeni.setFocusMode(FocusMode.auto); } catch (_) {}
      try { await yeni.setExposureMode(ExposureMode.auto); } catch (_) {}
      try {
        final minExp=await yeni.getMinExposureOffset();
        final maxExp=await yeni.getMaxExposureOffset();
        await yeni.setExposureOffset((-0.35).clamp(minExp,maxExp).toDouble());
      } catch (_) {}
      if (!arkaKamera) flashAcik = false;
      try { await yeni.setFlashMode(flashAcik ? FlashMode.torch : FlashMode.off); } catch (_) { flashAcik = false; }
      if (!mounted) { await yeni.dispose(); return; }
      onizleme = yeni;
      setState(() => onizlemeHazirlaniyor = false);
    } catch (e) {
      if (mounted) setState(() { onizlemeHazirlaniyor = false; kameraHatasi = e.toString().replaceFirst('Exception: ', ''); });
    }
  }

  Future<void> _kamerayiAcKapat(bool acik) async {
    if (baglaniyor) return;
    setState(() { kamera = acik; flashAcik = false; });
    if (acik) {
      await _onizlemeyiBaslat();
    } else {
      final eski = onizleme;
      onizleme = null;
      if (eski != null) await eski.dispose();
      if (mounted) setState(() => onizlemeHazirlaniyor = false);
    }
  }

  Future<void> _kamerayiCevir() async {
    if (baglaniyor || !kamera || onizlemeHazirlaniyor || kameralar.length < 2) return;
    setState(() { arkaKamera = !arkaKamera; flashAcik = false; });
    await _onizlemeyiBaslat();
  }

  Future<void> _flasiDegistir() async {
    final c = onizleme;
    if (c == null || !c.value.isInitialized || !arkaKamera) return;
    final yeni = !flashAcik;
    try {
      await c.setFlashMode(yeni ? FlashMode.torch : FlashMode.off);
      if (mounted) setState(() => flashAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Bu cihaz canlı önizlemede flaşı desteklemiyor.')));
    }
  }

  Future<void> _kaliteDegistir(String yeni) async {
    if (yeni == kalite || baglaniyor) return;
    setState(() => kalite = yeni);
    if (kamera) await _onizlemeyiBaslat();
  }

  Widget _kameraOnizlemesi() {
    final c = onizleme;
    if (!kamera) return const ColoredBox(color: Color(0xFF151515), child: Center(child: Icon(Icons.videocam_off_rounded, size: 72, color: Colors.white38)));
    if (onizlemeHazirlaniyor) return const ColoredBox(color: Color(0xFF151515), child: Center(child: CircularProgressIndicator(color: Colors.white)));
    if (c == null || !c.value.isInitialized) {
      return ColoredBox(color: const Color(0xFF151515), child: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisSize: MainAxisSize.min, children: [
        const Icon(Icons.no_photography_rounded, size: 54, color: Colors.white54),
        const SizedBox(height: 12),
        Text(kameraHatasi ?? 'Kamera önizlemesi açılamadı.', textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70)),
        const SizedBox(height: 12),
        OutlinedButton(onPressed: _onizlemeyiBaslat, child: const Text('Tekrar dene')),
      ]))));
    }
    final filtre=ngelxCanliProFiltreleri[filtreIndex];
    final matris=ngelxCanliRenkMatrisi(
      preset:filtre,parlaklik:parlaklik,kontrast:kontrast,doygunluk:doygunluk,sicaklik:sicaklik,netlik:netlik,
      ciltTonu:ciltTonu,highlightKoruma:highlightKoruma,golgeAcma:golgeAcma,guzellik:retus,
      otomatikIyilestirme:otomatikIyilestirme,dusukIsik:dusukIsik,
    );
    return ColorFiltered(
      colorFilter:ColorFilter.matrix(matris),
      child:Stack(fit:StackFit.expand,children:[
        FittedBox(fit:BoxFit.cover,child:SizedBox(width:c.value.previewSize?.height??720,height:c.value.previewSize?.width??1280,child:CameraPreview(c))),
        if(retus>.01)IgnorePointer(child:ColoredBox(color:const Color(0xFFFFE7DE).withOpacity((retus*.012).clamp(0.0,.014).toDouble()))),
        Positioned(left:10,bottom:10,child:Container(
          padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),
          decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(12)),
          child:Text('${filtre.ad} • PRO',style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
        )),
      ]),
    );
  }

  Future<void> _geriSayimCalistir() async {
    if(!mounted)return;
    final sayac=ValueNotifier<int>(3);
    final overlay=Overlay.of(context,rootOverlay:true);
    late final OverlayEntry giris;
    giris=OverlayEntry(builder:(_)=>Positioned.fill(
      child:IgnorePointer(
        child:ColoredBox(
          color:const Color(0xAA000000),
          child:Center(child:ValueListenableBuilder<int>(
            valueListenable:sayac,
            builder:(_,deger,__)=>Container(
              width:132,height:132,
              decoration:BoxDecoration(
                color:Colors.black87,
                shape:BoxShape.circle,
                border:Border.all(color:Colors.white,width:3),
                boxShadow:const [BoxShadow(color:Colors.black45,blurRadius:28,spreadRadius:8)],
              ),
              alignment:Alignment.center,
              child:Text('$deger',style:const TextStyle(
                color:Colors.white,fontSize:72,fontWeight:FontWeight.w900,height:1,
              )),
            ),
          )),
        ),
      ),
    ));
    overlay.insert(giris);
    try{
      for(var i=3;i>=1;i--){
        if(!mounted)break;
        sayac.value=i;
        setState(()=>baslangicSayaci=i);
        await Future<void>.delayed(const Duration(seconds:1));
      }
    }finally{
      if(mounted)setState(()=>baslangicSayaci=0);
      giris.remove();
      sayac.dispose();
    }
  }

  Future<void> baslat() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.isAnonymous || baglaniyor) return;
    if (baslik.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('En az 3 karakterlik yayın başlığı yaz.')));
      return;
    }
    if (mikrofon) {
      final izin = await Permission.microphone.request();
      if (!izin.isGranted) {
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mikrofon açık başlayacaksa mikrofon izni vermelisin.')));
        return;
      }
    }
    setState(() => baglaniyor = true);
    if (geriSayim) await _geriSayimCalistir();
    lk.Room? oda;
    try {
      final eskiOnizleme = onizleme;
      onizleme = null;
      if (eskiOnizleme != null) {
        try { await eskiOnizleme.setFlashMode(FlashMode.off); } catch (_) {}
        await eskiOnizleme.dispose();
        await Future<void>.delayed(const Duration(milliseconds: 180));
      }
      final odaAdi = 'ngelx_${user.uid}_${DateTime.now().millisecondsSinceEpoch}';
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final eskiCanli=(profil.data()?['currentLiveId']??'').toString();
      if(eskiCanli.isNotEmpty){
        try{
          await FirebaseFirestore.instance.collection('live_streams').doc(eskiCanli).set({
            'active':false,'endedAt':FieldValue.serverTimestamp(),'endReason':'replaced_by_new_live',
          },SetOptions(merge:true));
        }catch(_){}
      }
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();
      final kaynak = lk.DevelopmentTokenSource(id: liveKitTestSunucuId);
      final cevap = await kaynak.fetch(lk.TokenRequestOptions(
        roomName: odaAdi,
        participantIdentity: user.uid,
        participantName: ad,
        participantAttributes: const {'role': 'host'},
      ));
      oda = lk.Room(roomOptions: lk.RoomOptions(
        adaptiveStream: true,
        dynacast: true,
        defaultCameraCaptureOptions: _kameraAyarlari,
      ));
      await oda.connect(cevap.serverUrl, cevap.participantToken);
      final yerelKatilimci = oda.localParticipant;
      if (yerelKatilimci == null) throw Exception('Canlı yayın katılımcısı hazırlanamadı.');
      if (kamera) await yerelKatilimci.setCameraEnabled(true, cameraCaptureOptions: _kameraAyarlari);
      if (mikrofon) await yerelKatilimci.setMicrophoneEnabled(true);
      final belge = await FirebaseFirestore.instance.collection('live_streams').add({
        'roomName': odaAdi,
        'ownerId': user.uid,
        'username': ad,
        'title': baslik.text.trim(),
        'active': true,
        'startedAt': FieldValue.serverTimestamp(),
        'lastHeartbeatAt': FieldValue.serverTimestamp(),
        'cameraPosition': arkaKamera ? 'back' : 'front',
        'microphoneEnabled': mikrofon,
        'cameraEnabled': kamera,
        'filter': ngelxCanliProFiltreleri[filtreIndex].ad,
        'filterPro': ngelxCanliProFiltreleri[filtreIndex].ad,
        'retouch': retus,
        'beauty': retus,
        'filterBrightness': parlaklik,
        'filterContrast': kontrast,
        'filterSaturation': doygunluk,
        'filterWarmth': sicaklik,
        'filterClarity': netlik,
        'skinTone': ciltTonu,
        'highlightProtect': highlightKoruma,
        'shadowLift': golgeAcma,
        'autoEnhance': otomatikIyilestirme,
        'lowLight': dusukIsik,
        'aspectRatio': oran,
        'quality': kalite,
        'fps': fps,
        'visibility': gizlilik,
        'category': kategori,
        'viewerCount': 0,
        'likeCount': 0,
        'giftPoints': 0,
        'pkActive': false,
        'commentsEnabled': true,
        'slowModeSeconds': 0,
        'mutedUsers': <String>[],
        'bannedUsers': <String>[],
        'shareCount': 0,
        'welcomeMessage': 'Hoş geldiniz 👋',
      });
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'isLive': true,
        'currentLiveId': belge.id,
        'liveTitle': baslik.text.trim(),
        'liveStartedAt': FieldValue.serverTimestamp(),
        'lastLiveVisibility':gizlilik,
        'lastLiveVisibilityUpdatedAt':FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
      final profilVeri=profil.data()??<String,dynamic>{};
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
        unawaited(Future.wait(canliHedefler.take(120).map((hedefUid)async{
          try{
            await uygulamaBildirimiGonder(
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
            );
            return true;
          }catch(_){
            return false;
          }
        })).then((sonuclar)async{
          final basarili=sonuclar.where((x)=>x).length;
          final basarisiz=sonuclar.length-basarili;
          try{
            await FirebaseFirestore.instance.collection('live_streams').doc(belge.id).set({
              'startNotificationSent':basarili,
              'startNotificationFailed':basarisiz,
              'startNotificationUpdatedAt':FieldValue.serverTimestamp(),
            },SetOptions(merge:true));
          }catch(_){}
        }));
      }
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => CanliYayinPage(
        oda: oda!,
        belgeId: belge.id,
        baslik: baslik.text.trim(),
        yayinSahibi: true,
        ilkArkaKamera: arkaKamera,
        ilkMikrofonAcik: mikrofon,
        ilkKameraAcik: kamera,
        kameraAyarlari: _kameraAyarlari,
        ownerId: user.uid,
        username: ad,
        serverUrl:cevap.serverUrl,
        participantToken:cevap.participantToken,
      )));
    } catch (e) {
      if (oda != null) {
        await oda.disconnect();
        await oda.dispose();
      }
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Yayın başlatılamadı: $e')));
    } finally {
      if (mounted) {
        setState(() => baglaniyor = false);
        if (ModalRoute.of(context)?.isCurrent == true && kamera && onizleme == null) unawaited(_onizlemeyiBaslat());
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final onizlemeOrani = switch (oran) { '1:1' => 1.0, '16:9' => 16 / 9, _ => 9 / 16 };
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(backgroundColor: Colors.white, foregroundColor: Colors.black, title: const Text('Canlı yayın hazırla')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(18, 8, 18, 28),
          children: [
            Center(child: ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 430),
              child: AspectRatio(
                aspectRatio: onizlemeOrani,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(28),
                  child: Stack(fit: StackFit.expand, children: [
                    _kameraOnizlemesi(),
                    Positioned(top: 12, left: 12, child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 7),
                      decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(14)),
                      child: Text('${arkaKamera ? 'Arka' : 'Ön'} kamera • $kalite', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700)),
                    )),
                    if (baslangicSayaci > 0) Center(child: Container(
                      width: 92, height: 92,
                      decoration: BoxDecoration(color: Colors.black54, shape: BoxShape.circle, border: Border.all(color: Colors.white70, width: 2)),
                      alignment: Alignment.center,
                      child: Text('$baslangicSayaci', style: const TextStyle(color: Colors.white, fontSize: 52, fontWeight: FontWeight.w900)),
                    )),
                    Positioned(top: 8, right: 8, child: Row(children: [
                      IconButton.filledTonal(onPressed: kamera && !onizlemeHazirlaniyor && kameralar.length > 1 ? _kamerayiCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: const Icon(Icons.cameraswitch_rounded)),
                      const SizedBox(width: 5),
                      IconButton.filledTonal(onPressed: kamera && arkaKamera && !onizlemeHazirlaniyor ? _flasiDegistir : null, tooltip: 'Flaş', icon: Icon(flashAcik ? Icons.flash_on_rounded : Icons.flash_off_rounded)),
                    ])),
                  ]),
                ),
              ),
            )),
            const SizedBox(height: 18),
            TextField(
              controller:baslik,maxLength:100,
              onTapOutside:(_)=>FocusScope.of(context).unfocus(),
              textInputAction:TextInputAction.done,
              onSubmitted:(_)=>FocusScope.of(context).unfocus(),
              style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600),
              decoration:InputDecoration(prefixIcon:const Icon(Icons.edit_rounded,color:Colors.black54),hintText:'Yayın başlığı yaz',hintStyle:const TextStyle(color:Colors.black45,fontWeight:FontWeight.w600),filled:true,fillColor:const Color(0xFFF4F6F8),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none)),
            ),
            Container(
              padding:const EdgeInsets.fromLTRB(14,14,14,10),
              decoration:BoxDecoration(color:const Color(0xFFF7F8FA),borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE8EBEF))),
              child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(children:[
                  const Icon(Icons.auto_awesome_rounded,color:Color(0xFF7C4DFF)),
                  const SizedBox(width:8),
                  const Expanded(child:Text('NgelX Görüntü Stüdyosu',style:TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900))),
                  Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:4),decoration:BoxDecoration(color:Color(0xFF111111),borderRadius:BorderRadius.all(Radius.circular(10))),child:const Text('PRO',style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900))),
                ]),
                const SizedBox(height:11),
                Wrap(spacing:7,runSpacing:7,children:[
                  for(var i=0;i<ngelxCanliProFiltreleri.length;i++)ChoiceChip(
                    label:Text(ngelxCanliProFiltreleri[i].ad),selected:filtreIndex==i,
                    onSelected:baglaniyor?null:(_)=>setState(()=>filtreIndex=i),
                  ),
                ]),
                const Divider(height:24),
                _proSlider('Güzellik',Icons.face_retouching_natural_rounded,retus,0,1,(v)=>setState(()=>retus=v),yuzde:true),
                _proSlider('Parlaklık',Icons.light_mode_rounded,parlaklik,-.12,.16,(v)=>setState(()=>parlaklik=v)),
                _proSlider('Kontrast',Icons.contrast_rounded,kontrast,.82,1.30,(v)=>setState(()=>kontrast=v),merkez:1),
                _proSlider('Canlılık',Icons.palette_rounded,doygunluk,.82,1.35,(v)=>setState(()=>doygunluk=v),merkez:1),
                _proSlider('Sıcaklık',Icons.thermostat_rounded,sicaklik,-.35,.35,(v)=>setState(()=>sicaklik=v)),
                _proSlider('Netlik',Icons.hd_rounded,netlik,0,.60,(v)=>setState(()=>netlik=v),yuzde:true),
                _proSlider('Cilt tonu',Icons.face_rounded,ciltTonu,-.40,.40,(v)=>setState(()=>ciltTonu=v)),
                _proSlider('Parlak alan',Icons.wb_sunny_outlined,highlightKoruma,0,1,(v)=>setState(()=>highlightKoruma=v),yuzde:true),
                _proSlider('Gölgeler',Icons.brightness_4_rounded,golgeAcma,0,1,(v)=>setState(()=>golgeAcma=v),yuzde:true),
                SwitchListTile(
                  contentPadding:EdgeInsets.zero,dense:true,value:otomatikIyilestirme,
                  onChanged:baglaniyor?null:(v)=>setState(()=>otomatikIyilestirme=v),
                  secondary:const Icon(Icons.auto_mode_rounded,color:Color(0xFF00A6C8)),
                  title:const Text('Otomatik görüntü iyileştirme',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:const Text('Işık, kontrast ve canlılığı dengeler.',style:TextStyle(color:Colors.black54)),
                ),
                SwitchListTile(
                  contentPadding:EdgeInsets.zero,dense:true,value:dusukIsik,
                  onChanged:baglaniyor?null:(v)=>setState(()=>dusukIsik=v),
                  secondary:const Icon(Icons.nightlight_round,color:Color(0xFF5D5FEF)),
                  title:const Text('Düşük ışık desteği',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.',style:TextStyle(color:Colors.black54)),
                ),
              ]),
            ),
            Row(children: [
              Expanded(child: _canliSecimKutusu('Oran', oran, const ['9:16', '1:1', '16:9'], (v) => setState(() => oran = v))),
              const SizedBox(width: 12),
              Expanded(child: _canliSecimKutusu('Kalite', kalite, const ['540p', '720p', '1080p'], _kaliteDegistir)),
            ]),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _canliSecimKutusu('Kategori', kategori, const ['Sohbet', 'Müzik', 'Oyun', 'Spor', 'Eğlence', 'Eğitim'], (v) => setState(() => kategori = v))),
              const SizedBox(width: 12),
              Expanded(child: _canliSecimKutusu('Gizlilik', gizlilik, const ['Herkese açık', 'Takipçiler', 'Arkadaşlar'], _gizlilikDegistir)),
            ]),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _canliSecimKutusu('FPS', '$fps', const ['30', '60'], (v) => setState(() => fps = int.parse(v)))),
              const SizedBox(width: 12),
              Expanded(child: SwitchListTile(
                contentPadding: const EdgeInsets.symmetric(horizontal: 10),
                value: geriSayim,
                onChanged: baglaniyor ? null : (v) => setState(() => geriSayim = v),
                title: const Text('3-2-1', style: TextStyle(color:Colors.black87,fontWeight: FontWeight.w700)),
                subtitle: const Text('Başlangıç',style:TextStyle(color:Colors.black54)),
              )),
            ]),
            const SizedBox(height: 8),
            SwitchListTile(contentPadding: EdgeInsets.zero, value: kamera, onChanged: baglaniyor ? null : _kamerayiAcKapat, secondary: Icon(kamera ? Icons.videocam_rounded : Icons.videocam_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Kamera', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: const Text('Seçimler yayını otomatik başlatmaz.',style:TextStyle(color:Colors.black54))),
            SwitchListTile(contentPadding: EdgeInsets.zero, value: mikrofon, onChanged: baglaniyor ? null : (v) => setState(() => mikrofon = v), secondary: Icon(mikrofon ? Icons.mic_rounded : Icons.mic_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Mikrofon', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700))),
            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text(gizlilik, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('$kategori • ${fps} FPS • $kalite',style:const TextStyle(color:Colors.black54))),
            const SizedBox(height: 16),
            FilledButton.icon(
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744), minimumSize: const Size.fromHeight(58), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22))),
              onPressed: baglaniyor ? null : baslat,
              icon: baglaniyor ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.sensors_rounded),
              label: Text(baglaniyor ? 'Bağlanıyor...' : 'Canlı yayına başla', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
            ),
            const SizedBox(height: 10),
            const Text('Yayın yalnızca “Canlı yayını başlat” düğmesine bastığında başlar.', textAlign: TextAlign.center, style: TextStyle(color: Colors.black54)),
          ],
        ),
      ),
    );
  }

  Widget _proSlider(String etiket,IconData ikon,double deger,double min,double max,ValueChanged<double> degisti,{bool yuzde=false,double? merkez}){
    final yazi=yuzde?'%${(deger*100).round()}':(merkez!=null?'${deger.toStringAsFixed(2)}x':(deger>=0?'+${deger.toStringAsFixed(2)}':deger.toStringAsFixed(2)));
    return Row(children:[
      SizedBox(width:31,child:Icon(ikon,size:20,color:const Color(0xFF5F6368))),
      SizedBox(width:78,child:Text(etiket,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700,fontSize:12.5))),
      Expanded(child:Slider(value:deger.clamp(min,max).toDouble(),min:min,max:max,onChanged:baglaniyor?null:degisti)),
      SizedBox(width:50,child:Text(yazi,textAlign:TextAlign.end,style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700,fontSize:12))),
    ]);
  }

  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {
    return Theme(
      data:ThemeData.light(),
      child:InputDecorator(
        decoration:InputDecoration(
          labelText:etiket,
          labelStyle:const TextStyle(color:Color(0xFF5F6368),fontWeight:FontWeight.w700),
          floatingLabelStyle:const TextStyle(color:Color(0xFF5F6368),fontWeight:FontWeight.w800),
          filled:true,fillColor:const Color(0xFFF2F3F5),
          border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none),
        ),
        child:DropdownButtonHideUnderline(child:DropdownButton<String>(
          value:deger,isDense:true,isExpanded:true,dropdownColor:Colors.white,
          iconEnabledColor:const Color(0xFF5F6368),
          style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800),
          items:secenekler.map((e)=>DropdownMenuItem<String>(
            value:e,child:Text(e,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          )).toList(),
          onChanged:baglaniyor?null:(v){if(v!=null)unawaited(Future.sync(()=>degisti(v)));},
        )),
      ),
    );
  }
}

class CanliYayinPage extends StatefulWidget {
  final lk.Room oda;
  final String belgeId;
  final String baslik;
  final bool yayinSahibi;
  final bool ilkArkaKamera;
  final bool ilkMikrofonAcik;
  final bool ilkKameraAcik;
  final lk.CameraCaptureOptions kameraAyarlari;
  final String ownerId;
  final String username;
  final String serverUrl;
  final String participantToken;
  const CanliYayinPage({
    super.key,
    required this.oda,
    required this.belgeId,
    required this.baslik,
    required this.yayinSahibi,
    this.ilkArkaKamera = false,
    this.ilkMikrofonAcik = true,
    this.ilkKameraAcik = true,
    this.kameraAyarlari = const lk.CameraCaptureOptions(),
    this.ownerId = '',
    this.username = 'ngelx',
    this.serverUrl = '',
    this.participantToken = '',
  });
  @override
  State<CanliYayinPage> createState() => _CanliYayinPageState();
}

class _CanliYayinPageState extends State<CanliYayinPage> {
  final yorum = TextEditingController();
  Timer? sayac;
  Timer? heartbeat;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? canliDurumAboneligi;
  int saniye = 0;
  bool mikrofonAcik = true;
  bool kameraAcik = true;
  bool kapatildi = false;
  bool kalpIsleniyor = false;
  bool arkaKamera = false;
  bool kameraDegisiyor = false;
  bool hediyeGonderiliyor = false;
  bool katilimKaydiYapildi = false;
  bool yayinBitti=false;
  bool yenidenBaglaniyor=false;
  bool uzakKameraAcik=true;
  bool pkAktifYerel=false;
  int heartbeatTik=0;
  int yenidenBaglanmaDenemesi=0;
  String bitisMesaji='Canlı yayın sona erdi.';
  int maxIzleyici = 0;
  int sonToplamKalp = 0;
  int sonHediyePuani = 0;
  int sonYorumSayisi = 0;
  int yerelKalpSerisi = 0;
  DateTime? sonYorumZamani;

  @override
  void initState() {
    super.initState();
    arkaKamera = widget.ilkArkaKamera;
    mikrofonAcik = widget.ilkMikrofonAcik;
    kameraAcik = widget.ilkKameraAcik;
    uzakKameraAcik=widget.ilkKameraAcik;
    widget.oda.addListener(_yenile);
    canliDurumAboneligi=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots().listen((snap){
      final v=snap.data()??<String,dynamic>{};
      final yeniPk=v['pkActive']==true;
      if(mounted&&pkAktifYerel!=yeniPk)setState(()=>pkAktifYerel=yeniPk);
      if(!widget.yayinSahibi&&v.isNotEmpty){
        final kameraDurumu=v['cameraEnabled']!=false;
        if(mounted&&uzakKameraAcik!=kameraDurumu)setState(()=>uzakKameraAcik=kameraDurumu);
        final benUid=FirebaseAuth.instance.currentUser?.uid??'';
        if(benUid.isNotEmpty&&List<String>.from(v['bannedUsers']??const[]).contains(benUid)&&!yayinBitti){
          unawaited(_izleyicideYayinBitti('removed'));
        }else if(v['active']==false&&!yayinBitti){
          final neden=(v['endReason']??'').toString();
          unawaited(_izleyicideYayinBitti(neden));
        }
      }
    });
    if (!widget.yayinSahibi) {
      unawaited(_katildimKaydet());
    } else {
      unawaited(_heartbeatYaz());
      heartbeat=Timer.periodic(const Duration(seconds:6),(_)=>unawaited(_heartbeatYaz()));
    }
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      final izleyici = widget.oda.remoteParticipants.length;
      if (izleyici > maxIzleyici) maxIzleyici = izleyici;
      if (mounted) setState(() => saniye++);
    });
  }

  void _yenile() {
    if (mounted) setState(() {});
    if(widget.oda.connectionState==lk.ConnectionState.disconnected&&!kapatildi&&!yayinBitti){
      unawaited(_otomatikYenidenBaglan());
    }
  }

  Future<void> _izleyicideYayinBitti(String neden)async{
    if(widget.yayinSahibi||yayinBitti)return;
    sayac?.cancel();
    bitisMesaji=neden=='host_ended'
      ?'Yayıncı canlı yayını bitirdi.'
      :neden=='removed'
        ?'Yayıncı seni bu canlı yayından çıkardı.'
        :'Canlı yayın sona erdi.';
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

  Future<void> _heartbeatYaz()async{
    if(!widget.yayinSahibi||kapatildi||widget.oda.connectionState==lk.ConnectionState.disconnected)return;
    heartbeatTik++;
    final yama=<String,dynamic>{
      'active':true,
      'lastHeartbeatAt':FieldValue.serverTimestamp(),
      'viewerCount':_aktifIzleyiciler().length,
    };
    if(pkAktifYerel||heartbeatTik%3==0){
      try{
        final sonuc=await Future.wait([
          FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').get(),
          FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').get(),
        ]);
        final rs=sonuc[0] as QuerySnapshot<Map<String,dynamic>>;
        final cs=sonuc[1] as QuerySnapshot<Map<String,dynamic>>;
        var kalp=0,hediye=0,yorumSayisi=0;
        for(final d in rs.docs)kalp+=(d.data()['count'] as num?)?.toInt()??1;
        for(final d in cs.docs){
          final v=d.data();
          if(v['kind']=='gift')hediye+=(v['points'] as num?)?.toInt()??0;
          if((v['kind']??'comment')=='comment')yorumSayisi++;
        }
        yama['likeCount']=kalp;
        yama['giftPoints']=hediye;
        yama['commentCount']=yorumSayisi;
      }catch(_){}
    }
    try{
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set(yama,SetOptions(merge:true));
    }catch(_){}
  }

  lk.VideoTrack? _goruntu() {
    if (widget.yayinSahibi) {
      for (final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]) {
        if (!p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
      }
    } else {
      for (final katilimci in widget.oda.remoteParticipants.values) {
        for (final p in katilimci.videoTrackPublications) {
          if (p.subscribed && !p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
        }
      }
    }
    return null;
  }

  lk.LocalVideoTrack? _yerelKameraTrack() {
    for (final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]) {
      if (p.track is lk.LocalVideoTrack) return p.track as lk.LocalVideoTrack;
    }
    return null;
  }

  Future<void> _yayinKamerasiniCevir() async {
    if (!widget.yayinSahibi || !kameraAcik || kameraDegisiyor) return;
    final track = _yerelKameraTrack();
    if (track == null) return;
    final yeniArka = !arkaKamera;
    setState(() => kameraDegisiyor = true);
    try {
      await track.restartTrack(widget.kameraAyarlari.copyWith(cameraPosition: yeniArka ? lk.CameraPosition.back : lk.CameraPosition.front));
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'cameraPosition': yeniArka ? 'back' : 'front'}, SetOptions(merge: true));
      if (mounted) setState(() => arkaKamera = yeniArka);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Kamera değiştirilemedi; yayın bağlantısı korunuyor.')));
    } finally {
      if (mounted) setState(() => kameraDegisiyor = false);
    }
  }

  Future<void> _yayinMikrofonunuDegistir() async {
    final yeni = !mikrofonAcik;
    try {
      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'microphoneEnabled':yeni},SetOptions(merge:true));
      if (mounted) setState(() => mikrofonAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mikrofon ayarı değiştirilemedi.')));
    }
  }

  Future<void> _yayinKamerasiniAcKapat() async {
    final yeni = !kameraAcik;
    try {
      await widget.oda.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: widget.kameraAyarlari.copyWith(cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front),
      );
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'cameraEnabled':yeni},SetOptions(merge:true));
      if (mounted) setState(() => kameraAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Kamera ayarı değiştirilemedi.')));
    }
  }

  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;
    yenidenBaglaniyor=false;
    yenidenBaglanmaDenemesi=0;
    bitisMesaji='Canlı yayın sona erdi.';
    if(mounted)setState(()=>yayinBitti=true);
    sayac?.cancel();
    sayac=null;
    heartbeat?.cancel();
    heartbeat=null;
    if (widget.yayinSahibi) {
      unawaited(ngelxCanliPkYayindanCik(widget.belgeId));
      var toplamKalp = 0;
      var hediyePuani = 0;
      var yorumSayisi = 0;
      try {
        final rs = await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').get();
        for (final d in rs.docs) {
          toplamKalp += (d.data()['count'] as num?)?.toInt() ?? 1;
        }
        final cs = await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').get();
        for (final d in cs.docs) {
          final data = d.data();
          if (data['kind'] == 'gift') hediyePuani += (data['points'] as num?)?.toInt() ?? 0;
          if ((data['kind'] ?? 'comment') == 'comment') yorumSayisi++;
        }
      } catch (_) {}
      sonToplamKalp=toplamKalp;
      sonHediyePuani=hediyePuani;
      sonYorumSayisi=yorumSayisi;
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active': false,
        'status':'ended',
        'endReason':'host_ended',
        'endedAt': FieldValue.serverTimestamp(),
        'lastHeartbeatAt':FieldValue.serverTimestamp(),
        'cameraEnabled':false,
        'durationSeconds': saniye,
        'maxViewers': maxIzleyici,
        'likeCount': toplamKalp,
        'giftPoints': hediyePuani,
        'commentCount': yorumSayisi,
      }, SetOptions(merge: true));
      final uid = widget.ownerId.isNotEmpty ? widget.ownerId : FirebaseAuth.instance.currentUser?.uid;
      if (uid != null) {
        await FirebaseFirestore.instance.collection('users').doc(uid).set({
          'isLive': false,
          'currentLiveId': FieldValue.delete(),
          'liveTitle': FieldValue.delete(),
          'liveEndedAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true));
      }
    }
    await widget.oda.disconnect();
    await widget.oda.dispose();
    if (geriDon && mounted) Navigator.pop(context);
  }

  Future<bool> _geri() async {
    if (widget.yayinSahibi) {
      final onay = await showDialog<bool>(context: context, builder: (_) => AlertDialog(
        title: const Text('Yayın bitsin mi?'),
        content: const Text('Canlı yayın tüm izleyiciler için anında kapanacak, Keşfet’ten kaldırılacak ve bildirimlerde “yayın sona erdi” olarak görünecek.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Devam et')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Yayını bitir')),
        ],
      )) ?? false;
      if (!onay) return false;
    }
    await _bitir(geriDon: false);
    if(widget.yayinSahibi&&mounted){
      final dk=saniye~/60;
      final sn=(saniye%60).toString().padLeft(2,'0');
      await showDialog<void>(
        context:context,
        barrierDismissible:false,
        builder:(ctx)=>AlertDialog(
          title:const Row(children:[
            Icon(Icons.analytics_rounded,color:Color(0xFFFF1744)),
            SizedBox(width:9),
            Text('Canlı yayın özeti'),
          ]),
          content:Column(mainAxisSize:MainAxisSize.min,children:[
            _CanliOzetSatiri(ikon:Icons.schedule_rounded,etiket:'Süre',deger:'$dk:$sn'),
            _CanliOzetSatiri(ikon:Icons.visibility_rounded,etiket:'En yüksek izleyici',deger:'$maxIzleyici'),
            _CanliOzetSatiri(ikon:Icons.favorite_rounded,etiket:'Beğeni',deger:'$sonToplamKalp'),
            _CanliOzetSatiri(ikon:Icons.chat_bubble_rounded,etiket:'Yorum',deger:'$sonYorumSayisi'),
            _CanliOzetSatiri(ikon:Icons.card_giftcard_rounded,etiket:'Hediye puanı',deger:'$sonHediyePuani'),
          ]),
          actions:[
            FilledButton(onPressed:()=>Navigator.pop(ctx),child:const Text('Tamam')),
          ],
        ),
      );
    }
    return true;
  }

  Future<Map<String, dynamic>> _aktifProfil() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return <String, dynamic>{};
    try {
      final p = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      return p.data() ?? <String, dynamic>{};
    } catch (_) {
      return <String, dynamic>{};
    }
  }

  Future<void> _katildimKaydet() async {
    if (katilimKaydiYapildi) return;
    katilimKaydiYapildi = true;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    final p = await _aktifProfil();
    try {
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
        'uid': user.uid,
        'userId': user.uid,
        'username': (p['username'] ?? user.displayName ?? 'ngelx').toString(),
        'text': 'yayına katıldı',
        'kind': 'join',
        'createdAt': FieldValue.serverTimestamp(),
      });
    } catch (_) {}
  }


  String _izleyiciUid(lk.RemoteParticipant p){
    final kimlik=p.identity;
    if(kimlik==widget.ownerId)return kimlik;
    final parcalar=kimlik.split('-');
    if(parcalar.length>1&&RegExp(r'^\d{10,}$').hasMatch(parcalar.last)){
      return parcalar.sublist(0,parcalar.length-1).join('-');
    }
    return kimlik;
  }

  List<lk.RemoteParticipant> _aktifIzleyiciler()=>widget.oda.remoteParticipants.values
      .where((p)=>_izleyiciUid(p)!=widget.ownerId)
      .toList(growable:false);

  Widget _baglantiRozeti(){
    final durum=widget.oda.connectionState;
    final kalite=widget.oda.localParticipant?.connectionQuality??lk.ConnectionQuality.unknown;
    String yazi='Bağlı';
    Color renk=const Color(0xFF27D17F);
    if(yayinBitti){
      yazi='Sona erdi';
      renk=Colors.white54;
    }else if(yenidenBaglaniyor){
      yazi='Tekrar $yenidenBaglanmaDenemesi/3';
      renk=const Color(0xFFFFB020);
    }else if(durum==lk.ConnectionState.reconnecting||durum==lk.ConnectionState.connecting){
      yazi='Bağlanıyor';
      renk=const Color(0xFFFFB020);
    }else if(durum==lk.ConnectionState.disconnected){
      yazi='Kesildi';
      renk=const Color(0xFFFF4D5A);
    }else if(kalite==lk.ConnectionQuality.poor){
      yazi='Zayıf';
      renk=const Color(0xFFFFB020);
    }else if(kalite==lk.ConnectionQuality.good){
      yazi='İyi';
    }else if(kalite==lk.ConnectionQuality.excellent){
      yazi='Çok iyi';
    }
    return Container(
      padding:const EdgeInsets.symmetric(horizontal:8,vertical:5),
      decoration:BoxDecoration(color:Colors.black45,borderRadius:BorderRadius.circular(12),border:Border.all(color:renk.withOpacity(.55))),
      child:Row(mainAxisSize:MainAxisSize.min,children:[
        Container(width:7,height:7,decoration:BoxDecoration(color:renk,shape:BoxShape.circle)),
        const SizedBox(width:5),
        Text(yazi,style:const TextStyle(color:Colors.white,fontSize:10.5,fontWeight:FontWeight.w800)),
      ]),
    );
  }

  Future<void> _izleyiciGuvenlikMenusu()async{
    if(widget.yayinSahibi)return;
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(sheetContext)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(
          leading:const Icon(Icons.flag_outlined,color:Colors.redAccent),
          title:const Text('Canlı yayını şikâyet et',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),
          onTap:(){
            Navigator.pop(sheetContext);
            unawaited(sikayetEt(context,hedefTuru:'canli_yayin',hedefId:widget.belgeId,hedefUid:widget.ownerId));
          },
        ),
        if(widget.ownerId.isNotEmpty)ListTile(
          leading:const Icon(Icons.block_rounded,color:Colors.black87),
          title:const Text('Yayıncıyı engelle',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          subtitle:const Text('Engellediğinde içerikleri ve mesajları da gizlenir.',style:TextStyle(color:Colors.black54,fontSize:12)),
          onTap:(){
            Navigator.pop(sheetContext);
            unawaited(kullaniciyiEngelle(context,widget.ownerId));
          },
        ),
      ])),
    );
  }

  Future<void> _izleyiciListesiniAc()async{
    final izleyiciler=_aktifIzleyiciler();
    await showModalBottomSheet<void>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,isScrollControlled:true,
      builder:(sheetContext)=>SafeArea(child:SizedBox(
        height:MediaQuery.of(sheetContext).size.height*.62,
        child:Column(children:[
          Padding(
            padding:const EdgeInsets.fromLTRB(18,0,18,12),
            child:Row(children:[
              const Expanded(child:Text('Canlı izleyicileri',style:TextStyle(fontSize:20,fontWeight:FontWeight.w900))),
              Text('${izleyiciler.length}',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)),
            ]),
          ),
          Expanded(child:izleyiciler.isEmpty
            ?const Center(child:Text('Henüz izleyici yok.',style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)))
            :ListView.separated(
              itemCount:izleyiciler.length,
              separatorBuilder:(_,__)=>const Divider(height:1),
              itemBuilder:(_,i){
                final p=izleyiciler[i];
                final uid=_izleyiciUid(p);
                return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  future:FirebaseFirestore.instance.collection('users').doc(uid).get(),
                  builder:(_,snap){
                    final v=snap.data?.data()??<String,dynamic>{};
                    final foto=(v['photoUrl']??'').toString();
                    final ad=(v['displayName']??v['username']??p.name).toString();
                    return ListTile(
                      leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded):null),
                      title:Text(ad.isEmpty?'NgelX izleyicisi':ad,style:const TextStyle(fontWeight:FontWeight.w800)),
                      subtitle:Text((v['username']??'').toString().isEmpty?'Canlı yayında':'@${v['username']}'),
                      trailing:widget.yayinSahibi&&uid.isNotEmpty
                        ?PopupMenuButton<String>(
                          tooltip:'İzleyici yönetimi',
                          onSelected:(secim)async{
                            if(secim=='profile'){
                              if(sheetContext.mounted)Navigator.pop(sheetContext);
                              if(mounted)Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uid)));
                              return;
                            }
                            if(secim=='mute'){
                              await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
                                'mutedUsers':FieldValue.arrayUnion([uid]),
                              },SetOptions(merge:true));
                              return;
                            }
                            if(secim=='remove'){
                              await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
                                'bannedUsers':FieldValue.arrayUnion([uid]),
                                'mutedUsers':FieldValue.arrayUnion([uid]),
                              },SetOptions(merge:true));
                              if(sheetContext.mounted)ScaffoldMessenger.of(sheetContext).showSnackBar(const SnackBar(content:Text('İzleyici canlı yayından çıkarıldı.')));
                            }
                          },
                          itemBuilder:(_)=>const [
                            PopupMenuItem(value:'profile',child:ListTile(contentPadding:EdgeInsets.zero,leading:Icon(Icons.person_outline_rounded),title:Text('Profili aç'))),
                            PopupMenuItem(value:'mute',child:ListTile(contentPadding:EdgeInsets.zero,leading:Icon(Icons.volume_off_rounded),title:Text('Yorumlarını sustur'))),
                            PopupMenuItem(value:'remove',child:ListTile(contentPadding:EdgeInsets.zero,leading:Icon(Icons.block_rounded,color:Colors.redAccent),title:Text('Yayından çıkar',style:TextStyle(color:Colors.redAccent)))),
                          ],
                        )
                        :const Icon(Icons.chevron_right_rounded),
                      onTap:uid.isEmpty?null:(){
                        Navigator.pop(sheetContext);
                        Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uid)));
                      },
                    );
                  },
                );
              },
            ),
          ),
        ]),
      )),
    );
  }

  Widget _yayinBasligi(){
    final ben=FirebaseAuth.instance.currentUser?.uid??'';
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(widget.ownerId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        final foto=(v['photoUrl']??'').toString();
        final ad=(v['displayName']??v['username']??widget.username).toString();
        final username=(v['username']??widget.username).toString();
        return Container(
          padding:const EdgeInsets.fromLTRB(7,6,8,6),
          decoration:BoxDecoration(color:Colors.black38,borderRadius:BorderRadius.circular(18)),
          child:Row(children:[
            InkWell(
              onTap:widget.ownerId.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerId))),
              child:CircleAvatar(radius:18,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,size:19):null),
            ),
            const SizedBox(width:8),
            Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
              Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12.5,fontWeight:FontWeight.w900)),
              Text('@$username • ${widget.baslik}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white70,fontSize:10.5,fontWeight:FontWeight.w600)),
            ])),
            if(ben.isNotEmpty&&ben!=widget.ownerId)StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              stream:FirebaseFirestore.instance.collection('users').doc(ben).snapshots(),
              builder:(_,benSnap){
                final takipte=List<String>.from(benSnap.data?.data()?['following']??const[]).contains(widget.ownerId);
                return TextButton(
                  style:TextButton.styleFrom(foregroundColor:Colors.white,backgroundColor:takipte?Colors.white12:const Color(0xFFFF1744),padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),minimumSize:Size.zero),
                  onPressed:()=>takipDurumuDegistir(widget.ownerId,takipte),
                  child:Text(takipte?'Takipte':'Takip et',style:const TextStyle(fontSize:10.5,fontWeight:FontWeight.w900)),
                );
              },
            ),
          ]),
        );
      },
    );
  }

  Future<void> _yorumYonet(String yorumId,Map<String,dynamic> y)async{
    if(!widget.yayinSahibi)return;
    final uid=(y['uid']??y['userId']??'').toString();
    final username=(y['username']??'ngelx').toString();
    final metin=(y['text']??'').toString();
    await showModalBottomSheet<void>(
      context:context,backgroundColor:const Color(0xFF15151B),showDragHandle:true,
      builder:(sheetContext)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(
          leading:const Icon(Icons.push_pin_rounded,color:Color(0xFFFFC14D)),
          title:const Text('Yorumu sabitle',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            final yayinci=uid.isNotEmpty&&uid==widget.ownerId;
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
              'pinnedComment':{
                'commentId':yorumId,
                'uid':uid,
                'username':username,
                'text':metin,
                'isHost':yayinci||y['isHost']==true,
                'role':yayinci||y['isHost']==true?'host':'viewer',
                'pinnedAt':FieldValue.serverTimestamp(),
              },
            },SetOptions(merge:true));
          },
        ),
        if(uid.isNotEmpty&&uid!=widget.ownerId)ListTile(
          leading:const Icon(Icons.volume_off_rounded,color:Color(0xFFFFB020)),
          title:Text('@$username kullanıcısını sustur',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'mutedUsers':FieldValue.arrayUnion([uid])},SetOptions(merge:true));
          },
        ),
        ListTile(
          leading:const Icon(Icons.delete_outline_rounded,color:Color(0xFFFF5A67)),
          title:const Text('Yorumu sil',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').doc(yorumId).delete();
          },
        ),
      ])),
    );
  }

  Widget _yorumPaneli(){
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    return Container(
      constraints:const BoxConstraints(maxWidth:340,maxHeight:220),
      padding:const EdgeInsets.all(9),
      decoration:BoxDecoration(color:Colors.black38,borderRadius:BorderRadius.circular(18)),
      child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
        StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:ref.snapshots(),
          builder:(_,snap){
            final veri=snap.data?.data()??<String,dynamic>{};
            final pinned=veri['pinnedComment'];
            Map<String,dynamic>? p;
            var sabit=false;
            if(pinned is Map){
              final aday=Map<String,dynamic>.from(pinned);
              if((aday['text']??'').toString().trim().isNotEmpty){
                p=aday;
                sabit=true;
              }
            }
            if(p==null){
              final welcome=(veri['welcomeMessage']??'Hoş geldiniz 👋').toString().trim();
              if(welcome.isEmpty)return const SizedBox.shrink();
              p=<String,dynamic>{
                'uid':widget.ownerId,
                'username':widget.username,
                'text':welcome,
                'isHost':true,
                'role':'host',
              };
            }
            final yayinci=p['isHost']==true||p['role']=='host'||(p['uid']??'').toString()==widget.ownerId;
            return Container(
              width:double.infinity,
              margin:const EdgeInsets.only(bottom:6),
              padding:const EdgeInsets.symmetric(horizontal:9,vertical:7),
              decoration:BoxDecoration(
                color:yayinci?const Color(0xCCB00020):const Color(0x665D5FEF),
                borderRadius:BorderRadius.circular(12),
                border:yayinci?Border.all(color:const Color(0xFFFF5A67).withOpacity(.55)):null,
              ),
              child:Row(children:[
                Icon(sabit?Icons.push_pin_rounded:Icons.waving_hand_rounded,color:Colors.white,size:15),
                const SizedBox(width:6),
                if(yayinci)...[
                  Container(
                    padding:const EdgeInsets.symmetric(horizontal:6,vertical:3),
                    decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(7)),
                    child:const Text('YAYINCI',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900,letterSpacing:.3)),
                  ),
                  const SizedBox(width:6),
                ],
                Expanded(child:Text(
                  '@${p['username']??widget.username}  ${p['text']??''}',
                  maxLines:2,
                  overflow:TextOverflow.ellipsis,
                  style:const TextStyle(color:Colors.white,fontSize:11.5,fontWeight:FontWeight.w800),
                )),
                if(widget.yayinSahibi&&sabit)IconButton(
                  visualDensity:VisualDensity.compact,
                  tooltip:'Sabitlemeyi kaldır',
                  onPressed:()=>ref.set({'pinnedComment':FieldValue.delete()},SetOptions(merge:true)),
                  icon:const Icon(Icons.close_rounded,color:Colors.white70,size:16),
                ),
              ]),
            );
          },
        ),
        Flexible(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:ref.collection('comments').orderBy('createdAt',descending:true).limit(30).snapshots(),
          builder:(_,snap){
            final yorumlar=snap.data?.docs??[];
            if(yorumlar.isEmpty)return Text(widget.baslik,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800));
            return ListView.builder(reverse:true,shrinkWrap:true,itemCount:yorumlar.length,itemBuilder:(_,i){
              final d=yorumlar[i],y=d.data();
              final kind=(y['kind']??'comment').toString();
              if(kind=='join'){
                return Padding(padding:const EdgeInsets.symmetric(vertical:3),child:Text('👋 ${y['username']??'ngelx'} katıldı',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w600)));
              }
              if(kind=='gift'){
                return Padding(padding:const EdgeInsets.symmetric(vertical:4),child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:9,vertical:6),
                  decoration:BoxDecoration(color:const Color(0x668D6BFF),borderRadius:BorderRadius.circular(12)),
                  child:Text('${y['giftEmoji']??'🎁'} ${y['username']??'ngelx'} • ${y['giftName']??'N-Hediye'} +${y['points']??0} N',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
                ));
              }
              final yorumUid=(y['uid']??y['userId']??'').toString();
              final yayiniciMesaji=y['isHost']==true||y['role']=='host'||(yorumUid.isNotEmpty&&yorumUid==widget.ownerId);
              return GestureDetector(
                onLongPress:widget.yayinSahibi?()=>_yorumYonet(d.id,y):null,
                child:Padding(
                  padding:const EdgeInsets.symmetric(vertical:3),
                  child:yayiniciMesaji
                    ?Container(
                        padding:const EdgeInsets.symmetric(horizontal:8,vertical:6),
                        decoration:BoxDecoration(
                          color:const Color(0x99B00020),
                          borderRadius:BorderRadius.circular(10),
                          border:Border.all(color:const Color(0xFFFF5A67).withOpacity(.45)),
                        ),
                        child:Row(mainAxisSize:MainAxisSize.min,children:[
                          Container(
                            padding:const EdgeInsets.symmetric(horizontal:5,vertical:2),
                            decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(6)),
                            child:const Text('YAYINCI',style:TextStyle(color:Colors.white,fontSize:8.5,fontWeight:FontWeight.w900,letterSpacing:.3)),
                          ),
                          const SizedBox(width:6),
                          Flexible(child:Text(
                            '@${y['username']??widget.username}  ${y['text']??''}',
                            style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800),
                          )),
                        ]),
                      )
                    :Text('@${y['username']??'ngelx'}  ${y['text']??''}',style:const TextStyle(color:Colors.white)),
                ),
              );
            });
          },
        )),
      ]),
    );
  }

  Widget _yorumGirisAlani(){
    final uid=FirebaseAuth.instance.currentUser?.uid??'';
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        final acik=v['commentsEnabled']!=false||widget.yayinSahibi;
        final susturuldu=List<String>.from(v['mutedUsers']??const[]).contains(uid)&&!widget.yayinSahibi;
        final etkin=acik&&!susturuldu;
        final hint=susturuldu?'Yorum yapman susturuldu':acik?'Yorum yaz...':'Yorumlar kapalı';
        return TextField(
          controller:yorum,enabled:etkin,onSubmitted:etkin?(_)=>_yorumGonder():null,
          decoration:InputDecoration(
            hintText:hint,filled:true,fillColor:Colors.black54,
            suffixIcon:IconButton(onPressed:etkin?_yorumGonder:null,icon:const Icon(Icons.send_rounded)),
          ),
        );
      },
    );
  }

  Future<void> _goruntuStudyoPaneli() async {
    if(!widget.yayinSahibi)return;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    final belge=await ref.get();
    final veri=belge.data()??<String,dynamic>{};
    var presetAdi=(veri['filterPro']??veri['filter']??'Doğal').toString();
    var beauty=_ngelxCanliDouble(veri['beauty']??veri['retouch'],.18).clamp(0.0,1.0).toDouble();
    var bright=_ngelxCanliDouble(veri['filterBrightness'],0).clamp(-.12,.16).toDouble();
    var contrast=_ngelxCanliDouble(veri['filterContrast'],1).clamp(.82,1.30).toDouble();
    var saturation=_ngelxCanliDouble(veri['filterSaturation'],1).clamp(.82,1.35).toDouble();
    var warmth=_ngelxCanliDouble(veri['filterWarmth'],0).clamp(-.35,.35).toDouble();
    var clarity=_ngelxCanliDouble(veri['filterClarity'],.10).clamp(0.0,.60).toDouble();
    var skinTone=_ngelxCanliDouble(veri['skinTone'],.08).clamp(-.40,.40).toDouble();
    var highlightProtect=_ngelxCanliDouble(veri['highlightProtect'],.65).clamp(0.0,1.0).toDouble();
    var shadowLift=_ngelxCanliDouble(veri['shadowLift'],.10).clamp(0.0,1.0).toDouble();
    var autoEnhance=veri['autoEnhance']!=false;
    var lowLight=veri['lowLight']==true;
    var commentsEnabled=veri['commentsEnabled']!=false;
    var slowMode=(veri['slowModeSeconds'] as num?)?.toInt()??0;
    Future<void> yaz(Map<String,dynamic> yama)=>ref.set(yama,SetOptions(merge:true));
    if(!mounted)return;
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,backgroundColor:Colors.white,showDragHandle:true,
      builder:(sheetContext)=>StatefulBuilder(builder:(context,setSheet){
        Widget ayarSlider(String ad,IconData ikon,double value,double min,double max,ValueChanged<double> change,ValueChanged<double> save,{bool percent=false}){
          return Row(children:[
            SizedBox(width:34,child:Icon(ikon,color:const Color(0xFF5F6368))),
            SizedBox(width:78,child:Text(ad,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700,fontSize:12.5))),
            Expanded(child:Slider(value:value,min:min,max:max,onChanged:change,onChangeEnd:save)),
            SizedBox(width:46,child:Text(percent?'%${(value*100).round()}':value.toStringAsFixed(2),textAlign:TextAlign.end,style:const TextStyle(fontWeight:FontWeight.w700,color:Colors.black54,fontSize:12))),
          ]);
        }
        Future<void> sifirla()async{
          setSheet((){
            presetAdi='Doğal';beauty=.18;bright=0;contrast=1;saturation=1;warmth=0;clarity=.10;skinTone=.08;highlightProtect=.65;shadowLift=.10;autoEnhance=true;lowLight=false;
          });
          await yaz({
            'filter':'Doğal','filterPro':'Doğal','beauty':.18,'retouch':.18,
            'filterBrightness':0.0,'filterContrast':1.0,'filterSaturation':1.0,'filterWarmth':0.0,'filterClarity':.10,
            'skinTone':.08,'highlightProtect':.65,'shadowLift':.10,
            'autoEnhance':true,'lowLight':false,
          });
        }
        return SafeArea(child:Padding(
          padding:EdgeInsets.fromLTRB(16,0,16,18+MediaQuery.of(context).viewInsets.bottom),
          child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
            Row(children:[
              const Expanded(child:Text('Canlı yayın araçları',style:TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900))),
              TextButton.icon(onPressed:sifirla,icon:const Icon(Icons.restart_alt_rounded),label:const Text('Sıfırla')),
            ]),
            const Text('Görüntü ve yorum ayarlarını yayın kapanmadan değiştirebilirsin.',style:TextStyle(color:Colors.black54)),
            const SizedBox(height:12),
            const Text('Görüntü Stüdyosu',style:TextStyle(color:Colors.black87,fontSize:15,fontWeight:FontWeight.w900)),
            const SizedBox(height:8),
            Wrap(spacing:7,runSpacing:7,children:[
              for(final p in ngelxCanliProFiltreleri)ChoiceChip(
                label:Text(p.ad),selected:p.ad==presetAdi,
                onSelected:(_){setSheet(()=>presetAdi=p.ad);unawaited(yaz({'filter':p.ad,'filterPro':p.ad}));},
              ),
            ]),
            const Divider(height:24),
            ayarSlider('Güzellik',Icons.face_retouching_natural_rounded,beauty,0,1,(v)=>setSheet(()=>beauty=v),(v)=>unawaited(yaz({'beauty':v,'retouch':v})),percent:true),
            ayarSlider('Parlaklık',Icons.light_mode_rounded,bright,-.12,.16,(v)=>setSheet(()=>bright=v),(v)=>unawaited(yaz({'filterBrightness':v}))),
            ayarSlider('Kontrast',Icons.contrast_rounded,contrast,.82,1.30,(v)=>setSheet(()=>contrast=v),(v)=>unawaited(yaz({'filterContrast':v}))),
            ayarSlider('Canlılık',Icons.palette_rounded,saturation,.82,1.35,(v)=>setSheet(()=>saturation=v),(v)=>unawaited(yaz({'filterSaturation':v}))),
            ayarSlider('Sıcaklık',Icons.thermostat_rounded,warmth,-.35,.35,(v)=>setSheet(()=>warmth=v),(v)=>unawaited(yaz({'filterWarmth':v}))),
            ayarSlider('Netlik',Icons.hd_rounded,clarity,0,.60,(v)=>setSheet(()=>clarity=v),(v)=>unawaited(yaz({'filterClarity':v})),percent:true),
            ayarSlider('Cilt tonu',Icons.face_rounded,skinTone,-.40,.40,(v)=>setSheet(()=>skinTone=v),(v)=>unawaited(yaz({'skinTone':v}))),
            ayarSlider('Parlak alan',Icons.wb_sunny_outlined,highlightProtect,0,1,(v)=>setSheet(()=>highlightProtect=v),(v)=>unawaited(yaz({'highlightProtect':v})),percent:true),
            ayarSlider('Gölgeler',Icons.brightness_4_rounded,shadowLift,0,1,(v)=>setSheet(()=>shadowLift=v),(v)=>unawaited(yaz({'shadowLift':v})),percent:true),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:autoEnhance,
              onChanged:(v){setSheet(()=>autoEnhance=v);unawaited(yaz({'autoEnhance':v}));},
              secondary:const Icon(Icons.auto_mode_rounded,color:Color(0xFF00A6C8)),
              title:const Text('Otomatik iyileştirme',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
              subtitle:const Text('Parlak bölgeleri koruyup kontrastı dengeler.',style:TextStyle(color:Colors.black54)),
            ),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:lowLight,
              onChanged:(v){setSheet(()=>lowLight=v);unawaited(yaz({'lowLight':v}));},
              secondary:const Icon(Icons.nightlight_round,color:Color(0xFF5D5FEF)),
              title:const Text('Düşük ışık',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            ),
            const Divider(height:28),
            const Text('Yorum ve moderasyon',style:TextStyle(color:Colors.black87,fontSize:15,fontWeight:FontWeight.w900)),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:commentsEnabled,
              onChanged:(v){setSheet(()=>commentsEnabled=v);unawaited(yaz({'commentsEnabled':v}));},
              secondary:Icon(commentsEnabled?Icons.mode_comment_rounded:Icons.comments_disabled_rounded,color:const Color(0xFF5D5FEF)),
              title:const Text('Yorumlara izin ver',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            ),
            const Text('Yavaş mod',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            const SizedBox(height:7),
            Wrap(spacing:7,children:[
              for(final s in const [0,5,10,30])ChoiceChip(
                label:Text(s==0?'Kapalı':'$s sn'),
                selected:slowMode==s,
                onSelected:(_){setSheet(()=>slowMode=s);unawaited(yaz({'slowModeSeconds':s}));},
              ),
            ]),
            const SizedBox(height:10),
            const Text('İpucu: Bir yoruma uzun basarak sabitleyebilir, silebilir veya kullanıcıyı susturabilirsin.',style:TextStyle(color:Colors.black54,fontSize:12)),
          ])),
        ));
      }),
    );
  }

  Future<bool> _canliKisiyeGonder(User ben,String hedefUid)async{
    if(hedefUid.isEmpty||hedefUid==ben.uid)return false;

    // Doğrudan canlı paylaşımın ana teslim kanalı Aktivite bildirimidir.
    // Sohbet gizlilik ayarları mesaj kartını engellese bile canlı daveti kaybolmaz.
    final teslimAnahtari='live_share_${widget.belgeId}_${ben.uid}_$hedefUid';
    await uygulamaBildirimiGonder(
      toUid:hedefUid,
      fromUid:ben.uid,
      tur:'live',
      metin:'Sana bir canlı yayın gönderdi',
      belgeId:widget.belgeId,
      hedefTuru:'live',
      hedefBaslik:widget.baslik,
      olayTuru:'live_share',
      onizleme:widget.baslik,
      dedupeKey:teslimAnahtari,
    ).timeout(const Duration(seconds:12));

    // Başarı sayısı ancak Aktivite belgesi gerçekten oluştuysa artar.
    final teslimId=ngelxBildirimBelgeId(teslimAnahtari);
    final teslim=await FirebaseFirestore.instance.collection('notifications').doc(teslimId)
      .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
    final tv=teslim.data()??<String,dynamic>{};
    if(!teslim.exists||(tv['toUid']??'').toString()!=hedefUid||(tv['sourceId']??'').toString()!=widget.belgeId){
      throw StateError('live_share_delivery_not_confirmed');
    }

    // Sohbete canlı kartı düşürmek ikincil kanaldır. Mesaj izni yüzünden bu adım
    // başarısız olursa bildirim teslim edilmiş sayılır.
    try{
      final ids=<String>[ben.uid,hedefUid]..sort();
      String chatId='';
      var mevcutSohbet=false;
      try{
        final mevcut=await FirebaseFirestore.instance.collection('chats')
            .where('members',arrayContains:ben.uid).limit(100)
            .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        for(final d in mevcut.docs){
          final v=d.data();
          final uyeler=List<String>.from(v['members']??const[]);
          final grup=v['isGroup']==true||uyeler.length>2;
          if(!grup&&uyeler.length==2&&uyeler.contains(ben.uid)&&uyeler.contains(hedefUid)){
            chatId=d.id;
            mevcutSohbet=true;
            break;
          }
        }
      }catch(_){}
      if(chatId.isEmpty)chatId=ids.join('_');
      final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
      final metin='🔴 CANLI • ${widget.baslik}\n@${widget.username}\nYayına katıl: ngelx://live/${widget.belgeId}';
      if(mevcutSohbet){
        // Build 338: canlı paylaşım kartı için mevcut özel sohbet üyelerini koru.
        // Mevcut özel sohbette üyeler dizisini yeniden yazma. Eski sohbetlerde üye
        // sırası farklı olabildiği için Firestore kuralları bunu üyelik değişikliği
        // sayıp canlı kartını reddedebiliyordu.
        await chat.set({
          'updatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true)).timeout(const Duration(seconds:8));
      }else{
        await chat.set({
          'members':ids,
          'isGroup':false,
          'createdAt':FieldValue.serverTimestamp(),
          'updatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true)).timeout(const Duration(seconds:8));
      }
      final mesajRef=await chat.collection('messages').add({
        'senderId':ben.uid,
        'text':metin,
        'type':'text',
        'liveShare':true,
        'liveId':widget.belgeId,
        'liveTitle':widget.baslik,
        'liveOwnerId':widget.ownerId,
        'liveUsername':widget.username,
        'createdAt':FieldValue.serverTimestamp(),
      }).timeout(const Duration(seconds:8));
      await chat.set({
        'lastMessage':'🔴 ${widget.baslik}',
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedefUid':FieldValue.increment(1),
      },SetOptions(merge:true)).timeout(const Duration(seconds:8));
      final mesaj=await mesajRef.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:6));
      return mesaj.exists;
    }catch(_){
      return false;
    }
  }

  Future<void> _baglantiKopyala()async{
    await Clipboard.setData(ClipboardData(text:'NgelX canlı yayın • ${widget.baslik}\nngelx://live/${widget.belgeId}'));
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content:const Text('Bağlantı kopyalandı.',style:TextStyle(fontWeight:FontWeight.w700)),
      behavior:SnackBarBehavior.floating,
      width:230,
      duration:const Duration(milliseconds:1100),
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
    ));
  }

  Future<void> _paylas() async {
    if(await misafirEngeli(context))return;
    final ben=FirebaseAuth.instance.currentUser;
    if(ben==null)return;
    final benim=await FirebaseFirestore.instance.collection('users').doc(ben.uid).get();
    final engellenen=Set<String>.from(List<dynamic>.from(benim.data()?['blocked']??const[]));
    final yakin=<String>{
      ...List<String>.from(benim.data()?['friends']??const[]),
      ...List<String>.from(benim.data()?['following']??const[]),
    };
    if(!mounted)return;
    String sorgu='';
    final secilen=<String>{};
    bool gonderiliyor=false;
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,backgroundColor:Colors.white,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
      builder:(sheetContext)=>StatefulBuilder(builder:(sheetContext,setSheet)=>SafeArea(child:SizedBox(
        height:MediaQuery.of(sheetContext).size.height*.76,
        child:Column(children:[
          Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.black26,borderRadius:BorderRadius.circular(9))),
          const Text('Canlı yayını NgelX’te paylaş',style:TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),
          const SizedBox(height:5),
          const Padding(
            padding:EdgeInsets.symmetric(horizontal:20),
            child:Text('Arkadaş veya kullanıcı seç • aynı anda birden fazla kişiye gönderebilirsin.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:12.5,height:1.35)),
          ),
          Padding(
            padding:const EdgeInsets.fromLTRB(14,14,14,8),
            child:TextField(
              autofocus:false,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700),
              onChanged:(v)=>setSheet(()=>sorgu=v.trim().toLowerCase()),
              decoration:InputDecoration(
                hintText:'NgelX’te kişi ara',hintStyle:const TextStyle(color:Colors.black45,fontWeight:FontWeight.w600),
                prefixIcon:const Icon(Icons.search_rounded,color:Colors.black45),
                filled:true,fillColor:const Color(0xFFF3F4F6),
                border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none),
              ),
            ),
          ),
          if(secilen.isNotEmpty)Padding(
            padding:const EdgeInsets.fromLTRB(18,0,18,6),
            child:Align(alignment:Alignment.centerLeft,child:Container(
              padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
              decoration:BoxDecoration(color:const Color(0xFFF0E9FF),borderRadius:BorderRadius.circular(14)),
              child:Text('${secilen.length} kişi seçildi',style:const TextStyle(color:Color(0xFF6F41D8),fontWeight:FontWeight.w800)),
            )),
          ),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('users').limit(100).snapshots(),
            builder:(_,snap){
              if(snap.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());
              final docs=(snap.data?.docs??[]).where((d){
                if(d.id==ben.uid||engellenen.contains(d.id))return false;
                final v=d.data();
                if(v['deactivated']==true)return false;
                if(List<String>.from(v['blocked']??const[]).contains(ben.uid))return false;
                final ad='${v['displayName']??''} ${v['username']??''}'.toLowerCase();
                return sorgu.isEmpty||ad.contains(sorgu);
              }).toList()
                ..sort((a,b){
                  final ap=yakin.contains(a.id)?0:1,bp=yakin.contains(b.id)?0:1;
                  if(ap!=bp)return ap.compareTo(bp);
                  final an=(a.data()['displayName']??a.data()['username']??'').toString();
                  final bn=(b.data()['displayName']??b.data()['username']??'').toString();
                  return an.toLowerCase().compareTo(bn.toLowerCase());
                });
              if(docs.isEmpty)return const Center(child:Text('Kullanıcı bulunamadı.',style:TextStyle(color:Colors.black54)));
              return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){
                final d=docs[i],v=d.data();
                final foto=(v['photoUrl']??'').toString();
                final ad=(v['displayName']??v['username']??'NgelX kullanıcısı').toString();
                final secili=secilen.contains(d.id);
                return ListTile(
                  leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded):null),
                  title:Text(ad,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:Text('@${v['username']??'ngelx'}',style:const TextStyle(color:Colors.black54)),
                  trailing:Checkbox(value:secili,onChanged:gonderiliyor?null:(_)=>setSheet((){secili?secilen.remove(d.id):secilen.add(d.id);})),
                  onTap:gonderiliyor?null:()=>setSheet((){secili?secilen.remove(d.id):secilen.add(d.id);}),
                );
              });
            },
          )),
          Padding(
            padding:const EdgeInsets.fromLTRB(14,8,14,12),
            child:Row(children:[
              OutlinedButton.icon(
                style:OutlinedButton.styleFrom(foregroundColor:const Color(0xFF7C4DFF),side:const BorderSide(color:Color(0xFFB9A7F7)),padding:const EdgeInsets.symmetric(horizontal:14,vertical:14)),
                onPressed:gonderiliyor?null:()async{Navigator.pop(sheetContext);await _baglantiKopyala();},
                icon:const Icon(Icons.link_rounded),label:const Text('Kopyala',style:TextStyle(fontWeight:FontWeight.w800)),
              ),
              const SizedBox(width:10),
              Expanded(child:FilledButton.icon(
                style:FilledButton.styleFrom(minimumSize:const Size.fromHeight(52),backgroundColor:const Color(0xFFFF1744)),
                onPressed:secilen.isEmpty||gonderiliyor?null:()async{
                  setSheet(()=>gonderiliyor=true);
                  var basarili=0;
                  var basarisiz=0;
                  var sohbetBasarisiz=0;
                  for(final uid in secilen.toList()){
                    try{
                      final sohbetTamam=await _canliKisiyeGonder(ben,uid);
                      basarili++;
                      if(!sohbetTamam)sohbetBasarisiz++;
                    }catch(_){basarisiz++;}
                  }
                  if(basarili>0){
                    try{await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'shareCount':FieldValue.increment(basarili)},SetOptions(merge:true));}catch(_){}
                    if(sheetContext.mounted)Navigator.pop(sheetContext);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:Text(
                        basarisiz>0
                          ?'$basarili kişiye Aktivite bildirimi gönderildi • $basarisiz kişiye gönderilemedi.'
                          :sohbetBasarisiz>0
                            ?'Bildirim $basarili kişiye ulaştı • $sohbetBasarisiz sohbet kartı gizlilik nedeniyle gönderilemedi.'
                            :'Canlı yayın $basarili kişiye Aktivite ve Sohbet üzerinden gönderildi.',
                        style:const TextStyle(fontWeight:FontWeight.w700),
                      ),
                      behavior:SnackBarBehavior.floating,width:360,duration:const Duration(milliseconds:2200),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
                    ));
                  }else{
                    if(sheetContext.mounted)setSheet(()=>gonderiliyor=false);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:const Text('Gönderilemedi • tekrar deneyebilirsin.',style:TextStyle(fontWeight:FontWeight.w700)),
                      behavior:SnackBarBehavior.floating,width:285,duration:const Duration(milliseconds:1500),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
                    ));
                  }
                },
                icon:gonderiliyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded),
                label:Text(secilen.isEmpty?'Kişi seç':'${secilen.length} kişiye gönder',style:const TextStyle(fontWeight:FontWeight.w900)),
              )),
            ]),
          ),
        ]),
      ))),
    );
  }


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

  Future<void> _hediyeGonder(String ad, String emoji, int puan) async {
    if (hediyeGonderiliyor) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    hediyeGonderiliyor = true;
    try {
      final p = await _aktifProfil();
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
        'uid': user.uid,
        'userId': user.uid,
        'username': (p['username'] ?? user.displayName ?? 'ngelx').toString(),
        'text': '$emoji $ad',
        'kind': 'gift',
        'giftName': ad,
        'giftEmoji': emoji,
        'points': puan,
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$emoji $ad gönderildi • +$puan N-Puan')));
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hediye gönderilemedi.')));
    } finally {
      hediyeGonderiliyor = false;
    }
  }

  Future<void> _hediyePaneli() async {
    final hediyeler = <Map<String, dynamic>>[
      {'ad': 'Gül', 'emoji': '🌹', 'puan': 1},
      {'ad': 'Yıldız', 'emoji': '⭐', 'puan': 5},
      {'ad': 'Kalp Taşı', 'emoji': '💎', 'puan': 15},
      {'ad': 'Taç', 'emoji': '👑', 'puan': 25},
      {'ad': 'NgelX Roket', 'emoji': '🚀', 'puan': 50},
      {'ad': 'Galaksi', 'emoji': '🌌', 'puan': 100},
    ];
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: const Color(0xFF15151B),
      showDragHandle: true,
      builder: (c) => SafeArea(child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 4, 16, 18),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('N-Hediye', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          const Text('Canlı yayını destekle • hediyeler N-Puan kazandırır', style: TextStyle(color: Colors.white60)),
          const SizedBox(height: 14),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .95, crossAxisSpacing: 10, mainAxisSpacing: 10),
            itemCount: hediyeler.length,
            itemBuilder: (_, i) {
              final h = hediyeler[i];
              return InkWell(
                onTap: () async {
                  Navigator.pop(c);
                  await _hediyeGonder(h['ad'] as String, h['emoji'] as String, h['puan'] as int);
                },
                borderRadius: BorderRadius.circular(18),
                child: Container(
                  decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(18), border: Border.all(color: Colors.white12)),
                  padding: const EdgeInsets.all(10),
                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    Text(h['emoji'] as String, style: const TextStyle(fontSize: 30)),
                    const SizedBox(height: 5),
                    Text(h['ad'] as String, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800), textAlign: TextAlign.center),
                    Text('${h['puan']} N', style: const TextStyle(color: Color(0xFF8D6BFF), fontWeight: FontWeight.w800)),
                  ]),
                ),
              );
            },
          ),
        ]),
      )),
    );
  }

  Future<void> _kalpDegistir() async {
    if(kalpIsleniyor)return;
    final user=FirebaseAuth.instance.currentUser;
    if(user==null)return;
    kalpIsleniyor=true;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').doc(user.uid);
    try{
      await FirebaseFirestore.instance.runTransaction((tx) async {
        final mevcut = await tx.get(ref);
        final onceki = (mevcut.data()?['count'] as num?)?.toInt() ?? 0;
        tx.set(ref, {
          'uid': user.uid,
          'userId': user.uid,
          'type': 'heart',
          'count': onceki + 1,
          'updatedAt': FieldValue.serverTimestamp(),
          if (!mevcut.exists) 'createdAt': FieldValue.serverTimestamp(),
        });
      });
      if (mounted) setState(() => yerelKalpSerisi++);
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayın tepkisi gönderilemedi.')));
    }finally{
      kalpIsleniyor=false;
    }
  }

  Future<void> _yorumGonder() async {
    final metin=yorum.text.trim();
    final user=FirebaseAuth.instance.currentUser;
    if(metin.isEmpty||user==null)return;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    final canli=await ref.get();
    final v=canli.data()??<String,dynamic>{};
    if(!widget.yayinSahibi&&v['commentsEnabled']==false){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yayıncı yorumları kapattı.')));
      return;
    }
    if(!widget.yayinSahibi&&List<String>.from(v['mutedUsers']??const[]).contains(user.uid)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu yayında yorum yapman susturuldu.')));
      return;
    }
    final yavas=(v['slowModeSeconds'] as num?)?.toInt()??0;
    if(!widget.yayinSahibi&&yavas>0&&sonYorumZamani!=null){
      final kalan=yavas-DateTime.now().difference(sonYorumZamani!).inSeconds;
      if(kalan>0){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Yavaş mod açık. $kalan saniye bekle.')));
        return;
      }
    }
    yorum.clear();
    final profil=await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    await ref.collection('comments').add({
      'uid':user.uid,'userId':user.uid,
      'username':(profil.data()?['username']??'ngelx').toString(),
      'text':metin,
      'kind':'comment',
      'isHost':widget.yayinSahibi,
      'role':widget.yayinSahibi?'host':'viewer',
      'createdAt':FieldValue.serverTimestamp(),
    });
    sonYorumZamani=DateTime.now();
  }

  @override
  void dispose() {
    sayac?.cancel();
    heartbeat?.cancel();
    canliDurumAboneligi?.cancel();
    yorum.dispose();
    widget.oda.removeListener(_yenile);
    if (!kapatildi) _bitir(geriDon: false);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final track = _goruntu();
    final dakika = (saniye ~/ 60).toString().padLeft(2, '0');
    final sn = (saniye % 60).toString().padLeft(2, '0');
    return WillPopScope(
      onWillPop: _geri,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(children: [
          Positioned.fill(
            child:NgelXCanliPkGoruntuKatmani(
              liveId:widget.belgeId,
              child:track==null
                ?_goruntuYokEkrani()
                :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
                  builder:(_,snap){
                    final veri=snap.data?.data()??<String,dynamic>{};
                    return ngelxCanliEfektKatmani(veri:veri,child:lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover));
                  },
                ),
            ),
          ),
          Positioned.fill(child:DecoratedBox(decoration:BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Colors.black54,Colors.transparent,Colors.black.withOpacity(.8)])))),
          if(!yayinBitti&&!kapatildi&&widget.oda.connectionState==lk.ConnectionState.reconnecting)
            Positioned(
              top:74,left:70,right:70,
              child:SafeArea(child:Container(
                padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),
                decoration:BoxDecoration(color:const Color(0xDD1A1A1A),borderRadius:BorderRadius.circular(14)),
                child:const Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  SizedBox(width:15,height:15,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFFFFB020))),
                  SizedBox(width:8),
                  Text('Bağlantı yeniden kuruluyor…',style:TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
                ]),
              )),
            ),
          SafeArea(child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(children: [
              Row(children: [
                Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8), decoration: BoxDecoration(color: const Color(0xFFFF1744), borderRadius: BorderRadius.circular(14)), child: const Text('● CANLI', style: TextStyle(fontWeight: FontWeight.w900))),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('$dakika:$sn')),
                const SizedBox(width: 8),
                InkWell(
                  onTap:_izleyiciListesiniAc,
                  borderRadius:BorderRadius.circular(14),
                  child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:8),decoration:BoxDecoration(color:Colors.black45,borderRadius:BorderRadius.circular(14)),child:Text('👁 ${_aktifIzleyiciler().length}')),
                ),
                const Spacer(),
                if(!widget.yayinSahibi)IconButton(
                  tooltip:'Canlı yayın seçenekleri',
                  onPressed:_izleyiciGuvenlikMenusu,
                  icon:const Icon(Icons.more_horiz_rounded,size:28),
                ),
                IconButton(onPressed:()async{if(await _geri()&&mounted)Navigator.pop(context);},icon:const Icon(Icons.close_rounded,size:31)),
              ]),
              const SizedBox(height:7),
              Row(children:[
                Expanded(child:_yayinBasligi()),
                const SizedBox(width:7),
                _baglantiRozeti(),
              ]),
              const SizedBox(height:8),
              NgelXCanliPkKatmani(liveId:widget.belgeId,yayinSahibi:widget.yayinSahibi),
              const Spacer(),
              Align(alignment:Alignment.centerLeft,child:_yorumPaneli()),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(child:_yorumGirisAlani()),
                if (!widget.yayinSahibi) ...[
                  const SizedBox(width: 8),
                  StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').snapshots(),
                    builder:(_,s){
                      final docs=s.data?.docs??[];
                      final sayi=docs.fold<int>(0,(t,d)=>t+((d.data()['count'] as num?)?.toInt()??1));
                      return FilledButton.tonalIcon(
                        onPressed:kalpIsleniyor?null:_kalpDegistir,
                        icon:const Icon(Icons.favorite_rounded,color:Colors.redAccent),
                        label:Text(sayi>0?'$sayi':'Kalp'),
                      );
                    },
                  ),
                  const SizedBox(width: 6),
                  IconButton.filledTonal(onPressed: hediyeGonderiliyor ? null : _hediyePaneli, tooltip: 'N-Hediye', icon: const Icon(Icons.card_giftcard_rounded, color: Color(0xFFFF4F93))),
                  const SizedBox(width: 4),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Paylaş', icon: const Icon(Icons.share_rounded)),
                ],
              ]),
              if (yerelKalpSerisi >= 5 && !widget.yayinSahibi)
                Padding(padding: const EdgeInsets.only(top: 6), child: Align(alignment: Alignment.centerRight, child: Text('N-Kombo x$yerelKalpSerisi ❤️', style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w800)))),
              if (widget.yayinSahibi) ...[
                const SizedBox(height: 9),
                Wrap(
                  alignment:WrapAlignment.center,
                  spacing:9,
                  runSpacing:7,
                  children:[
                    IconButton.filled(onPressed: _yayinMikrofonunuDegistir, tooltip: mikrofonAcik ? 'Mikrofonu kapat' : 'Mikrofonu aç', icon: Icon(mikrofonAcik ? Icons.mic : Icons.mic_off)),
                    IconButton.filled(onPressed: _yayinKamerasiniAcKapat, tooltip: kameraAcik ? 'Kamerayı kapat' : 'Kamerayı aç', icon: Icon(kameraAcik ? Icons.videocam : Icons.videocam_off)),
                    IconButton.filled(onPressed: kameraAcik && !kameraDegisiyor ? _yayinKamerasiniCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: kameraDegisiyor ? const SizedBox(width: 19, height: 19, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.cameraswitch_rounded)),
                    IconButton.filledTonal(onPressed: _goruntuStudyoPaneli, tooltip: 'Görüntü Stüdyosu', icon: const Icon(Icons.tune_rounded)),
                    NgelXCanliPkButonu(liveId:widget.belgeId,ownerUid:widget.ownerId),
                    IconButton.filledTonal(onPressed: _paylas, tooltip: 'Yayını paylaş', icon: const Icon(Icons.share_rounded)),
                    FilledButton.icon(style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744)), onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.stop_circle_outlined), label: const Text('Bitir')),
                  ],
                ),
              ],
            ]),
          )),
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
}


class _CanliOzetSatiri extends StatelessWidget{
  final IconData ikon;
  final String etiket;
  final String deger;
  const _CanliOzetSatiri({required this.ikon,required this.etiket,required this.deger});
  @override Widget build(BuildContext context)=>Padding(
    padding:const EdgeInsets.symmetric(vertical:7),
    child:Row(children:[
      Icon(ikon,color:const Color(0xFFFF1744),size:21),
      const SizedBox(width:10),
      Expanded(child:Text(etiket,style:const TextStyle(fontWeight:FontWeight.w700))),
      Text(deger,style:const TextStyle(fontWeight:FontWeight.w900)),
    ]),
  );
}

