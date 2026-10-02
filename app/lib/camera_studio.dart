part of 'main.dart';

class NgelXKameraFiltre {
  final String ad;
  final List<double> matris;
  final double parlaklik;
  final double doygunluk;
  final double kontrast;
  final double gamma;
  final double pozlama;
  final double hue;
  final double kirmizi;
  final double yesil;
  final double mavi;
  final double varsayilanYogunluk;

  const NgelXKameraFiltre(
    this.ad,
    this.matris,{
    this.parlaklik=1,
    this.doygunluk=1,
    this.kontrast=1,
    this.gamma=1,
    this.pozlama=0,
    this.hue=0,
    this.kirmizi=0,
    this.yesil=0,
    this.mavi=0,
    this.varsayilanYogunluk=.55,
  });
}

/// Build 370 Pro Filters
///
/// Bunlar "tam kareyi patlatan" eski parlaklik filtreleri degil.
/// Canli onizlemede ColorMatrix, fotograf ciktisinda ise ayni preset'in
/// brightness/saturation/contrast/gamma/exposure/hue + kanal offset ayarlari
/// kullanilir. Varsayilan yogunluklar bilerek %40-%65 bandinda tutulur;
/// kullanici isterse %100'e cikabilir.
const List<NgelXKameraFiltre> ngelxKameraFiltreleri=[
  NgelXKameraFiltre('Doğal',<double>[
    1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0,
  ],varsayilanYogunluk:0),

  NgelXKameraFiltre('Canlı',<double>[
    1.07,-.015,-.01,0,2,
    -.01,1.045,-.005,0,1,
    -.005,-.01,1.065,0,1,
    0,0,0,1,0,
  ],parlaklik:1.008,doygunluk:1.12,kontrast:1.055,gamma:.985,pozlama:.015,varsayilanYogunluk:.58),

  NgelXKameraFiltre('Portre',<double>[
    1.035,.008,-.012,0,3,
    .004,1.018,-.008,0,2,
    -.01,.004,.982,0,1,
    0,0,0,1,0,
  ],parlaklik:1.018,doygunluk:1.025,kontrast:.985,gamma:.975,pozlama:.018,hue:1.0,kirmizi:2,yesil:1,mavi:-1,varsayilanYogunluk:.56),

  NgelXKameraFiltre('Clean',<double>[
    1.025,-.006,-.006,0,3,
    -.004,1.022,-.004,0,3,
    -.004,-.004,1.018,0,2,
    0,0,0,1,0,
  ],parlaklik:1.025,doygunluk:1.015,kontrast:1.012,gamma:.965,pozlama:.012,kirmizi:1,yesil:1,mavi:1,varsayilanYogunluk:.50),

  NgelXKameraFiltre('Soft',<double>[
    .985,.012,.008,0,5,
    .008,.992,.006,0,4,
    .008,.010,.985,0,4,
    0,0,0,1,0,
  ],parlaklik:1.018,doygunluk:.97,kontrast:.94,gamma:.965,pozlama:.018,kirmizi:2,yesil:1,mavi:1,varsayilanYogunluk:.48),

  NgelXKameraFiltre('Glow',<double>[
    1.025,.006,-.008,0,5,
    .004,1.018,-.004,0,4,
    -.006,.006,1.006,0,3,
    0,0,0,1,0,
  ],parlaklik:1.035,doygunluk:1.035,kontrast:.97,gamma:.945,pozlama:.020,kirmizi:2,yesil:1,mavi:0,varsayilanYogunluk:.46),

  NgelXKameraFiltre('HD',<double>[
    1.075,-.025,-.02,0,-1,
    -.015,1.06,-.015,0,-1,
    -.015,-.02,1.075,0,-1,
    0,0,0,1,0,
  ],parlaklik:1.0,doygunluk:1.035,kontrast:1.10,gamma:1.0,pozlama:0,varsayilanYogunluk:.45),

  NgelXKameraFiltre('Sıcak',<double>[
    1.055,.010,-.010,0,4,
    .008,1.018,-.006,0,2,
    -.012,-.006,.955,0,-2,
    0,0,0,1,0,
  ],parlaklik:1.008,doygunluk:1.055,kontrast:1.02,gamma:.99,pozlama:.008,hue:1.2,kirmizi:5,yesil:1,mavi:-4,varsayilanYogunluk:.52),

  NgelXKameraFiltre('Soğuk',<double>[
    .965,-.006,.010,0,-2,
    -.004,1.008,.008,0,0,
    .006,.012,1.06,0,4,
    0,0,0,1,0,
  ],parlaklik:1.002,doygunluk:1.03,kontrast:1.025,gamma:1.0,pozlama:0,hue:-1.0,kirmizi:-4,yesil:0,mavi:5,varsayilanYogunluk:.50),

  NgelXKameraFiltre('Sinematik',<double>[
    1.025,-.035,.010,0,-4,
    -.020,1.015,.018,0,-1,
    -.018,.020,1.025,0,4,
    0,0,0,1,0,
  ],parlaklik:.995,doygunluk:.89,kontrast:1.115,gamma:1.025,pozlama:-.010,hue:-1.5,kirmizi:1,yesil:0,mavi:3,varsayilanYogunluk:.56),

  NgelXKameraFiltre('Retro',<double>[
    1.015,.018,-.012,0,5,
    .010,.982,.004,0,2,
    .012,.010,.925,0,-3,
    0,0,0,1,0,
  ],parlaklik:1.012,doygunluk:.82,kontrast:.92,gamma:.97,pozlama:.018,hue:2.0,kirmizi:6,yesil:2,mavi:-5,varsayilanYogunluk:.50),

  NgelXKameraFiltre('S/B',<double>[
    .2126,.7152,.0722,0,0,
    .2126,.7152,.0722,0,0,
    .2126,.7152,.0722,0,0,
    0,0,0,1,0,
  ],parlaklik:1.0,doygunluk:0,kontrast:1.08,gamma:.985,pozlama:0,varsayilanYogunluk:.72),
];


bool _ngelxTenPikseli(num r,num g,num b){
  final mx=math.max(r,math.max(g,b)),mn=math.min(r,math.min(g,b));
  final klasik=r>82&&g>32&&b>18&&(mx-mn)>12&&(r-g).abs()>8&&r>g&&r>b;
  final acikTen=r>170&&g>145&&b>125&&(r-g).abs()<55&&r>b&&g>b;
  return klasik||acikTen;
}

double _ngelxNoktaUzaklik(double x,double y,Offset? p){
  if(p==null)return 999999;
  final dx=x-p.dx,dy=y-p.dy;
  return math.sqrt(dx*dx+dy*dy);
}

img.Image _ngelxYuzBolgeselRetus(
  img.Image kaynak,
  List<Face> yuzler,
  double yogunluk,{
  double gozCanlilik=.18,
  double yuzIsigi=.14,
}){
  if(yuzler.isEmpty||yogunluk<=.01)return kaynak;
  final amount=yogunluk.clamp(0.0,1.0).toDouble();
  final blur=img.gaussianBlur(kaynak.clone(),radius:math.max(1,(1+amount*3).round()));
  for(final face in yuzler){
    final box=face.boundingBox;
    final fw=box.width,fh=box.height;
    if(fw<20||fh<20)continue;
    final cx=box.center.dx,cy=box.center.dy;
    final rx=math.max(12.0,fw*.58),ry=math.max(16.0,fh*.66);
    final x0=math.max(0,(cx-rx).floor()),x1=math.min(kaynak.width-1,(cx+rx).ceil());
    final y0=math.max(0,(cy-ry).floor()),y1=math.min(kaynak.height-1,(cy+ry).ceil());

    Offset? lm(FaceLandmarkType t){
      final p=face.landmarks[t]?.position;
      return p==null?null:Offset(p.x.toDouble(),p.y.toDouble());
    }
    final solGoz=lm(FaceLandmarkType.leftEye);
    final sagGoz=lm(FaceLandmarkType.rightEye);
    final agizAlt=lm(FaceLandmarkType.bottomMouth);
    final burun=lm(FaceLandmarkType.noseBase);

    for(var y=y0;y<=y1;y++){
      for(var x=x0;x<=x1;x++){
        final nx=(x-cx)/rx,ny=(y-cy)/ry;
        final elips=nx*nx+ny*ny;
        if(elips>=1)continue;
        final p=kaynak.getPixel(x,y);
        final r=p.r.toDouble(),g=p.g.toDouble(),b=p.b.toDouble();
        if(!_ngelxTenPikseli(r,g,b))continue;

        var detay=1.0;
        final gozR=fw*.105,agizR=fw*.14,burunR=fw*.075;
        if(_ngelxNoktaUzaklik(x.toDouble(),y.toDouble(),solGoz)<gozR)detay*=.18;
        if(_ngelxNoktaUzaklik(x.toDouble(),y.toDouble(),sagGoz)<gozR)detay*=.18;
        if(_ngelxNoktaUzaklik(x.toDouble(),y.toDouble(),agizAlt)<agizR)detay*=.22;
        if(_ngelxNoktaUzaklik(x.toDouble(),y.toDouble(),burun)<burunR)detay*=.52;

        final kenar=math.pow((1-elips).clamp(0.0,1.0),.62).toDouble();
        final a=(amount*.58*kenar*detay).clamp(0.0,.62).toDouble();
        if(a<=.01)continue;
        final q=blur.getPixel(x,y);
        final light=(amount*2.8+yuzIsigi.clamp(0.0,1.0)*5.0)*kenar;
        kaynak.setPixelRgba(
          x,y,
          (r*(1-a)+q.r*a+light).clamp(0,255),
          (g*(1-a)+q.g*a+light*.78).clamp(0,255),
          (b*(1-a)+q.b*a+light*.52).clamp(0,255),
          p.a,
        );
      }
    }

    // Gözleri bulanıklaştırmak yerine çok hafif canlı tut.
    for(final eye in <Offset?>[solGoz,sagGoz]){
      if(eye==null)continue;
      final rr=math.max(2,(fw*.055).round());
      for(var yy=math.max(0,eye.dy.round()-rr);yy<=math.min(kaynak.height-1,eye.dy.round()+rr);yy++){
        for(var xx=math.max(0,eye.dx.round()-rr);xx<=math.min(kaynak.width-1,eye.dx.round()+rr);xx++){
          final d=_ngelxNoktaUzaklik(xx.toDouble(),yy.toDouble(),eye);
          if(d>rr)continue;
          final p=kaynak.getPixel(xx,yy);
          final boost=(1-d/rr)*(amount*4.0+gozCanlilik.clamp(0.0,1.0)*10.0);
          kaynak.setPixelRgba(
            xx,yy,
            (p.r+boost).clamp(0,255),
            (p.g+boost).clamp(0,255),
            (p.b+boost*1.15).clamp(0,255),
            p.a,
          );
        }
      }
    }
  }
  return kaynak;
}

class NgelXCameraStudioPage extends StatefulWidget{
  final bool baslangicVideo;
  final Duration maxVideo;
  const NgelXCameraStudioPage({super.key,this.baslangicVideo=false,this.maxVideo=const Duration(minutes:10)});
  @override State<NgelXCameraStudioPage> createState()=>_NgelXCameraStudioPageState();
}

class _NgelXCameraStudioPageState extends State<NgelXCameraStudioPage> with WidgetsBindingObserver{
  final FaceDetector _yuzAlgilayici=FaceDetector(options:FaceDetectorOptions(
    performanceMode:FaceDetectorMode.fast,
    enableLandmarks:true,
    enableContours:false,
    enableClassification:false,
    enableTracking:true,
  ));
  int _sonYuzSayisi=0;
  List<Face> _canliYuzler=<Face>[];
  Size? _canliYuzGoruntuBoyutu;
  InputImageRotation? _canliYuzRotasyon;
  DateTime _sonCanliYuzAnalizi=DateTime.fromMillisecondsSinceEpoch(0);
  bool _canliYuzIsleniyor=false,_canliYuzAkisiAcik=false;
  static const Map<DeviceOrientation,int> _yuzYonleri=<DeviceOrientation,int>{
    DeviceOrientation.portraitUp:0,
    DeviceOrientation.landscapeLeft:90,
    DeviceOrientation.portraitDown:180,
    DeviceOrientation.landscapeRight:270,
  };
  List<CameraDescription> kameralar=<CameraDescription>[];
  CameraController? kontrol;
  int kameraIndex=0;
  bool video=false,kayit=false,hazirlaniyor=true,isleniyor=false,ayna=false,izgara=false,otomatikPortre=false;
  int sayac=0;
  Timer? sayacTimer,kayitTimer;
  Duration kayitSure=Duration.zero;
  FlashMode flash=FlashMode.off;
  double zoom=1,minZoom=1,maxZoom=1,retus=0,gozCanlilik=0,yuzIsigi=0,filtreYogunluk=0;
  int filtreIndex=0;
  String oran='9:16';

  @override void initState(){
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    video=widget.baslangicVideo;
    unawaited(_baslat());
  }

  Future<void> _baslat()async{
    try{
      kameralar=await availableCameras();
      if(kameralar.isEmpty)throw Exception('Kamera bulunamadı.');
      if(video){
        final mic=await Permission.microphone.request();
        if(!mic.isGranted)video=false;
      }
      final on=kameraIndex<kameralar.length?kameralar[kameraIndex]:kameralar.first;
      await _kontroluKur(on);
    }catch(e){
      if(mounted){setState(()=>hazirlaniyor=false);ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kamera açılamadı: $e')));}
    }
  }

  Future<void> _kontroluKur(CameraDescription kamera)async{
    final eski=kontrol;
    kontrol=null;
    if(mounted)setState(()=>hazirlaniyor=true);
    if(eski!=null){
      try{if(eski.value.isStreamingImages)await eski.stopImageStream();}catch(_){}
      try{await eski.dispose();}catch(_){}
      _canliYuzAkisiAcik=false;
      _canliYuzler=<Face>[];
      await Future<void>.delayed(const Duration(milliseconds:140));
    }
    final preset=kamera.lensDirection==CameraLensDirection.front?ResolutionPreset.veryHigh:ResolutionPreset.high;
    final format=Platform.isAndroid?ImageFormatGroup.nv21:Platform.isIOS?ImageFormatGroup.bgra8888:ImageFormatGroup.jpeg;
    final yeni=CameraController(kamera,preset,enableAudio:video,imageFormatGroup:format);
    try{
      await yeni.initialize();
      try{await yeni.setFocusMode(FocusMode.auto);}catch(_){}
      try{await yeni.setExposureMode(ExposureMode.auto);}catch(_){}
      if(kamera.lensDirection==CameraLensDirection.front){
        try{
          final minExp=await yeni.getMinExposureOffset();
          final maxExp=await yeni.getMaxExposureOffset();
          await yeni.setExposureOffset((-0.18).clamp(minExp,maxExp).toDouble());
        }catch(_){}
      }
      minZoom=await yeni.getMinZoomLevel();maxZoom=await yeni.getMaxZoomLevel();
      zoom=zoom.clamp(minZoom,maxZoom).toDouble();
      try{await yeni.setZoomLevel(zoom);}catch(_){}
      try{await yeni.setFlashMode(kamera.lensDirection==CameraLensDirection.front?FlashMode.off:flash);}catch(_){}
      if(!mounted){await yeni.dispose();return;}
      kontrol=yeni;
      setState(()=>hazirlaniyor=false);
      unawaited(_canliYuzAkisiniGuncelle());
    }catch(e){
      try{await yeni.dispose();}catch(_){}
      if(mounted)setState(()=>hazirlaniyor=false);
      rethrow;
    }
  }

  InputImage? _canliInputImage(CameraImage image,CameraController c){
    final kamera=c.description;
    final sensor=kamera.sensorOrientation;
    InputImageRotation? rotation;
    if(Platform.isIOS){
      rotation=InputImageRotationValue.fromRawValue(sensor);
    }else if(Platform.isAndroid){
      var komp=_yuzYonleri[c.value.deviceOrientation];
      if(komp==null)return null;
      komp=kamera.lensDirection==CameraLensDirection.front
        ?(sensor+komp)%360
        :(sensor-komp+360)%360;
      rotation=InputImageRotationValue.fromRawValue(komp);
    }
    if(rotation==null)return null;
    final format=InputImageFormatValue.fromRawValue(image.format.raw);
    if(format==null)return null;
    if(Platform.isAndroid&&format!=InputImageFormat.nv21)return null;
    if(Platform.isIOS&&format!=InputImageFormat.bgra8888)return null;
    if(image.planes.length!=1)return null;
    final plane=image.planes.first;
    _canliYuzGoruntuBoyutu=Size(image.width.toDouble(),image.height.toDouble());
    _canliYuzRotasyon=rotation;
    return InputImage.fromBytes(
      bytes:plane.bytes,
      metadata:InputImageMetadata(
        size:_canliYuzGoruntuBoyutu!,
        rotation:rotation,
        format:format,
        bytesPerRow:plane.bytesPerRow,
      ),
    );
  }

  Future<void> _canliYuzIsle(CameraImage image,CameraController kaynak)async{
    if(_canliYuzIsleniyor||!mounted||!identical(kontrol,kaynak))return;
    final simdi=DateTime.now();
    if(simdi.difference(_sonCanliYuzAnalizi)<const Duration(milliseconds:145))return;
    _sonCanliYuzAnalizi=simdi;
    final input=_canliInputImage(image,kaynak);
    if(input==null)return;
    _canliYuzIsleniyor=true;
    try{
      final yuzler=await _yuzAlgilayici.processImage(input);
      if(!mounted||!identical(kontrol,kaynak))return;
      _sonYuzSayisi=yuzler.length;
      setState(()=>_canliYuzler=yuzler.take(3).toList(growable:false));
    }catch(_){
      // Canlı akış tek karede hata verirse kamerayı kesme; sonraki kare devam eder.
    }finally{
      _canliYuzIsleniyor=false;
    }
  }

  Future<void> _canliYuzAkisiniDurdur([CameraController? hedef])async{
    final c=hedef??kontrol;
    if(c==null)return;
    try{if(c.value.isStreamingImages)await c.stopImageStream();}catch(_){}
    _canliYuzAkisiAcik=false;
    if(mounted&&_canliYuzler.isNotEmpty)setState(()=>_canliYuzler=<Face>[]);
  }

  Future<void> _canliYuzAkisiniGuncelle()async{
    final c=kontrol;
    if(c==null||!c.value.isInitialized||kayit||isleniyor||video)return;
    final gerekli=c.description.lensDirection==CameraLensDirection.front&&(otomatikPortre||retus>.01||gozCanlilik>.01||yuzIsigi>.01);
    if(!gerekli){await _canliYuzAkisiniDurdur(c);return;}
    if(_canliYuzAkisiAcik||c.value.isStreamingImages)return;
    try{
      await c.startImageStream((image)=>unawaited(_canliYuzIsle(image,c)));
      _canliYuzAkisiAcik=true;
    }catch(e){
      debugPrint('Canlı yüz takibi başlatılamadı: $e');
      _canliYuzAkisiAcik=false;
    }
  }

  Future<void> _videoModu(bool yeni)async{
    if(kayit||isleniyor||video==yeni)return;
    if(yeni){
      final mic=await Permission.microphone.request();
      if(!mic.isGranted){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli video için mikrofon izni vermelisin.')));
        return;
      }
    }
    setState((){video=yeni;hazirlaniyor=true;});
    final d=kontrol?.description??(kameralar.isNotEmpty?kameralar[kameraIndex]:null);
    if(d==null)return;
    try{await _kontroluKur(d);}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kamera modu değiştirilemedi: $e')));}
  }

  Future<void> _kameraCevir()async{
    if(isleniyor||kayit||hazirlaniyor||kameralar.length<2)return;
    final mevcut=kontrol?.description.lensDirection??kameralar[kameraIndex].lensDirection;
    final hedefYon=mevcut==CameraLensDirection.front?CameraLensDirection.back:CameraLensDirection.front;
    var hedef=kameralar.indexWhere((k)=>k.lensDirection==hedefYon);
    if(hedef<0)hedef=(kameraIndex+1)%kameralar.length;
    kameraIndex=hedef;
    try{await _kontroluKur(kameralar[hedef]);}
    catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kamera değiştirilemedi. Tekrar dene.')));}
  }

  Future<void> _flashDegistir()async{
    final c=kontrol;if(c==null||!c.value.isInitialized)return;
    if(c.description.lensDirection==CameraLensDirection.front){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Ön kamerada donanım flaşı yok. Arka kameraya geçince flaş kullanılabilir.')));
      return;
    }
    final siradaki=switch(flash){FlashMode.off=>FlashMode.auto,FlashMode.auto=>FlashMode.always,FlashMode.always=>FlashMode.torch,FlashMode.torch=>FlashMode.off};
    try{
      await c.setFlashMode(siradaki);
      if(mounted)setState(()=>flash=siradaki);
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu cihaz seçilen flaş modunu desteklemiyor.')));
    }
  }

  IconData get _flashIkon=>switch(flash){FlashMode.off=>Icons.flash_off_rounded,FlashMode.auto=>Icons.flash_auto_rounded,FlashMode.always=>Icons.flash_on_rounded,FlashMode.torch=>Icons.highlight_rounded};

  Future<void> _sayacCalistir(Future<void> Function() islem)async{
    if(sayac<=0){await islem();return;}
    for(int i=sayac;i>0;i--){
      if(!mounted)return;
      setState(()=>_aktifSayac=i);
      await Future.delayed(const Duration(seconds:1));
    }
    if(mounted)setState(()=>_aktifSayac=0);
    await islem();
  }
  int _aktifSayac=0;

  Future<img.Image> _aiYuzRetusuUygula(img.Image g,Directory dir)async{
    if(retus<=.01&&!otomatikPortre)return g;
    try{
      final yol='${dir.path}/ngelx_face_detect_${DateTime.now().microsecondsSinceEpoch}.jpg';
      final dosya=File(yol);
      await dosya.writeAsBytes(img.encodeJpg(g,quality:94),flush:true);
      final yuzler=await _yuzAlgilayici.processImage(InputImage.fromFilePath(yol)).timeout(const Duration(seconds:8));
      _sonYuzSayisi=yuzler.length;
      try{await dosya.delete();}catch(_){}
      if(yuzler.isEmpty)return g;
      return _ngelxYuzBolgeselRetus(g,yuzler,retus <= .01 ? .18 : retus,gozCanlilik:gozCanlilik,yuzIsigi:yuzIsigi);
    }catch(e){
      debugPrint('AI yüz rötuşu atlandı: $e');
      return g;
    }
  }

  Future<XFile> _fotoyuIsle(XFile ham)async{
    final onKamera=kontrol?.description.lensDirection==CameraLensDirection.front;
    final portre=onKamera&&otomatikPortre;
    if(filtreIndex==0&&retus<=.01&&oran=='9:16'&&!portre)return ham;
    try{
      final bytes=await ham.readAsBytes();
      var g=img.decodeImage(bytes);
      if(g==null)return ham;
      g=img.bakeOrientation(g);
      final dir=await getTemporaryDirectory();
      if((kontrol?.description.lensDirection==CameraLensDirection.front)&&(retus>.01||otomatikPortre)){
        g=await _aiYuzRetusuUygula(g,dir);
      }
      if(oran!='9:16'){
        final hedef=oran=='1:1'?1.0:16/9;
        final mevcut=g.width/g.height;
        int x=0,y=0,w=g.width,h=g.height;
        if(mevcut>hedef){w=(g.height*hedef).round();x=((g.width-w)/2).round();}
        else{h=(g.width/hedef).round();y=((g.height-h)/2).round();}
        g=img.copyCrop(g,x:x,y:y,width:w,height:h);
      }
      final f=ngelxKameraFiltreleri[filtreIndex];
      final filtreMiktari=filtreIndex==0?0.0:filtreYogunluk.clamp(0.0,1.0).toDouble();
      if(filtreMiktari>0){
        g=img.adjustColor(
          g,
          brightness:f.parlaklik,
          saturation:f.doygunluk,
          contrast:f.kontrast,
          gamma:f.gamma,
          exposure:f.pozlama,
          hue:f.hue,
          amount:filtreMiktari,
        );
        if(f.kirmizi!=0||f.yesil!=0||f.mavi!=0){
          g=img.colorOffset(
            g,
            red:f.kirmizi*filtreMiktari,
            green:f.yesil*filtreMiktari,
            blue:f.mavi*filtreMiktari,
          );
        }
      }
      if(retus>.01||portre){
        g=img.adjustColor(
          g,
          brightness:1+(retus*.006)+(portre?.008:0),
          saturation:1+(retus*.006)+(portre?.006:0),
          contrast:1-(portre?.010:0),
          amount:1,
        );
      }
      final yol='${dir.path}/ngelx_camera_${DateTime.now().microsecondsSinceEpoch}.jpg';
      await File(yol).writeAsBytes(img.encodeJpg(g,quality:90),flush:true);
      return XFile(yol,mimeType:'image/jpeg');
    }catch(_){return ham;}
  }

  Future<void> _cek()async{
    final c=kontrol;if(c==null||!c.value.isInitialized||isleniyor)return;
    if(video){
      if(kayit){await _videoDurdur();return;}
      await _sayacCalistir(_videoBaslat);
      return;
    }
    await _sayacCalistir(()async{
      try{
        setState(()=>isleniyor=true);
        await _canliYuzAkisiniDurdur(c);
        final ham=await c.takePicture();
        final sonuc=await _fotoyuIsle(ham);
        if(mounted)Navigator.pop(context,<String,dynamic>{'file':sonuc,'video':false,'filter':ngelxKameraFiltreleri[filtreIndex].ad,'retouch':retus,'eyeBoost':gozCanlilik,'faceLight':yuzIsigi,'aiFaceRetouch':_sonYuzSayisi>0,'facesDetected':_sonYuzSayisi});
      }catch(e){if(mounted){ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Fotoğraf çekilemedi: $e')));setState(()=>isleniyor=false);unawaited(_canliYuzAkisiniGuncelle());}}
      finally{if(mounted&&isleniyor)setState(()=>isleniyor=false);}
    });
  }

  Future<void> _videoBaslat()async{
    final c=kontrol;if(c==null||!c.value.isInitialized||kayit)return;
    try{
      await _canliYuzAkisiniDurdur(c);
      await c.startVideoRecording();
      kayitSure=Duration.zero;
      kayitTimer?.cancel();
      kayitTimer=Timer.periodic(const Duration(seconds:1),(_){
        if(!mounted)return;
        final yeni=kayitSure+const Duration(seconds:1);
        if(yeni>=widget.maxVideo){unawaited(_videoDurdur());return;}
        setState(()=>kayitSure=yeni);
      });
      setState(()=>kayit=true);
    }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Video başlatılamadı: $e')));}
  }

  Future<void> _videoDurdur()async{
    final c=kontrol;if(c==null||!kayit||isleniyor)return;
    try{
      setState(()=>isleniyor=true);
      final x=await c.stopVideoRecording();
      kayitTimer?.cancel();
      if(mounted)Navigator.pop(context,<String,dynamic>{
        'file':x,'video':true,'filter':ngelxKameraFiltreleri[filtreIndex].ad,'retouch':retus,
        'filterPreviewOnly':filtreIndex!=0||retus>.01,
      });
    }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Video tamamlanamadı: $e')));}
    finally{if(mounted)setState((){kayit=false;isleniyor=false;});}
  }

  String get _kayitYazi{
    final m=kayitSure.inMinutes.toString().padLeft(2,'0'),s=(kayitSure.inSeconds%60).toString().padLeft(2,'0');
    return '$m:$s';
  }

  List<double> _filtreMatris(List<double> kaynak){
    const kimlik=<double>[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0];
    final a=filtreYogunluk.clamp(0.0,1.0);
    return List<double>.generate(20,(i)=>kimlik[i]+((kaynak[i]-kimlik[i])*a));
  }

  List<double> _retusMatris(){
    final a=retus.clamp(0.0,1.0);
    final b=255*(a*.045);
    return <double>[
      1+a*.018,0,0,0,b,
      0,1+a*.014,0,0,b,
      0,0,1-a*.012,0,b*.78,
      0,0,0,1,0,
    ];
  }

  List<double> _otomatikPortreMatris()=>const <double>[
    1.015,0,0,0,2.4,
    0,1.008,0,0,2.0,
    0,0,.992,0,1.2,
    0,0,0,1,0,
  ];

  Widget _kameraOnizleme(){
    final c=kontrol;
    if(c==null||!c.value.isInitialized)return const Center(child:CircularProgressIndicator(color:Colors.white));
    Widget p=CameraPreview(c);
    final onKamera=c.description.lensDirection==CameraLensDirection.front;
    if(onKamera&&otomatikPortre)p=ColorFiltered(colorFilter:ColorFilter.matrix(_otomatikPortreMatris()),child:p);
    final f=ngelxKameraFiltreleri[filtreIndex];
    if(filtreIndex!=0)p=ColorFiltered(colorFilter:ColorFilter.matrix(_filtreMatris(f.matris)),child:p);
    if(retus>.01)p=ColorFiltered(colorFilter:ColorFilter.matrix(_retusMatris()),child:p);
    if(c.description.lensDirection==CameraLensDirection.front&&ayna)p=Transform(alignment:Alignment.center,transform:Matrix4.rotationY(math.pi),child:p);
    return GestureDetector(
      onScaleStart:(_)=>_zoomBaslangic=zoom,
      onScaleUpdate:(d){if(d.pointerCount<2)return;final z=(_zoomBaslangic*d.scale).clamp(minZoom,maxZoom).toDouble();zoom=z;unawaited(c.setZoomLevel(z));if(mounted)setState((){});},
      child:Stack(fit:StackFit.expand,children:[
        p,
        if(onKamera&&_canliYuzler.isNotEmpty&&_canliYuzGoruntuBoyutu!=null&&_canliYuzRotasyon!=null&&(retus>.01||otomatikPortre))
          Positioned.fill(child:IgnorePointer(child:ClipPath(
            clipper:_NgelXCanliYuzClipper(
              yuzler:_canliYuzler,
              imageSize:_canliYuzGoruntuBoyutu!,
              rotation:_canliYuzRotasyon!,
              lensDirection:c.description.lensDirection,
              ayna:ayna,
            ),
            child:BackdropFilter(
              filter:ui.ImageFilter.blur(sigmaX:1.2+retus*4.2,sigmaY:1.2+retus*4.2),
              child:ColoredBox(color:Colors.white.withValues(alpha:(.015+retus*.035).clamp(0.0,.05).toDouble())),
            ),
          ))),
        if(onKamera&&_canliYuzler.isNotEmpty&&_canliYuzGoruntuBoyutu!=null&&_canliYuzRotasyon!=null&&(retus>.01||otomatikPortre))
          Positioned.fill(child:IgnorePointer(child:CustomPaint(painter:_NgelXCanliYuzGlowPainter(
            yuzler:_canliYuzler,
            imageSize:_canliYuzGoruntuBoyutu!,
            rotation:_canliYuzRotasyon!,
            lensDirection:c.description.lensDirection,
            ayna:ayna,
            yogunluk:retus,
          )))),
        if(izgara)CustomPaint(painter:_NgelXIzgaraPainter()),
      ]),
    );
  }
  double _zoomBaslangic=1;

  Widget _yuvarlak(IconData ikon,VoidCallback? onTap,{String? yazi,bool aktif=false})=>Column(mainAxisSize:MainAxisSize.min,children:[
    InkWell(
      onTap:onTap,
      borderRadius:BorderRadius.circular(28),
      child:AnimatedContainer(
        duration:const Duration(milliseconds:140),
        width:48,height:48,
        decoration:BoxDecoration(
          color:aktif?mor.withValues(alpha:.88):Colors.black45,
          shape:BoxShape.circle,
          border:Border.all(color:aktif?Colors.white70:Colors.white24,width:aktif?1.6:1),
        ),
        child:Icon(ikon,color:Colors.white),
      ),
    ),
    if(yazi!=null)...[const SizedBox(height:3),Text(yazi,style:TextStyle(color:aktif?Colors.white:Colors.white70,fontSize:9,fontWeight:FontWeight.w800))],
  ]);

  Future<void> _filtrePaneli()async{
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:const Color(0xEE0B0B10),
      isScrollControlled:true,
      builder:(c)=>SafeArea(top:false,child:StatefulBuilder(builder:(c,setP)=>Padding(
        padding:const EdgeInsets.fromLTRB(12,12,12,18),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Container(width:42,height:4,decoration:BoxDecoration(color:Colors.white24,borderRadius:BorderRadius.circular(8))),
          const SizedBox(height:12),
          Row(children:[
            const Text('Filtreler',style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),
            const Spacer(),
            TextButton(onPressed:(){setState((){filtreIndex=0;filtreYogunluk=0;});setP((){});},child:const Text('Sıfırla')),
          ]),
          SizedBox(height:92,child:ListView.separated(
            scrollDirection:Axis.horizontal,itemCount:ngelxKameraFiltreleri.length,separatorBuilder:(_,__)=>const SizedBox(width:8),
            itemBuilder:(_,i){
              final secili=i==filtreIndex;
              return InkWell(onTap:(){final f=ngelxKameraFiltreleri[i];setState((){filtreIndex=i;filtreYogunluk=f.varsayilanYogunluk;});setP((){});},child:SizedBox(width:72,child:Column(children:[
                AnimatedContainer(duration:const Duration(milliseconds:150),width:58,height:58,decoration:BoxDecoration(shape:BoxShape.circle,color:secili?mor:Colors.white12,border:Border.all(color:secili?Colors.white:Colors.white24,width:2)),child:const Icon(Icons.filter_vintage_rounded,color:Colors.white)),
                const SizedBox(height:5),Text(ngelxKameraFiltreleri[i].ad,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:secili?Colors.white:Colors.white70,fontSize:10,fontWeight:secili?FontWeight.w900:FontWeight.w600)),
              ])));
            },
          )),
          Row(children:[const Text('Yoğunluk',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),Expanded(child:Slider(value:filtreYogunluk,min:0,max:1,onChanged:(v){setState(()=>filtreYogunluk=v);setP((){});})),Text('%${(filtreYogunluk*100).round()}',style:const TextStyle(color:Colors.white))]),
        ]),
      ))),
    );
  }

  Future<void> _retusPaneli()async{
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:const Color(0xEE0B0B10),
      builder:(c)=>SafeArea(child:StatefulBuilder(builder:(c,setP)=>Padding(
        padding:const EdgeInsets.all(18),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Row(children:[const Text('AI Yüz Rötuşu',style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),const Spacer(),TextButton(onPressed:(){setState((){retus=0;gozCanlilik=0;yuzIsigi=0;});setP((){});},child:const Text('Sıfırla'))]),
          const Text('AI yüz algılama cildi bölgesel işler; göz, ağız ve yüz detaylarını mümkün olduğunca korur.',style:TextStyle(color:Colors.white60,fontSize:11)),
          Row(children:[const SizedBox(width:78,child:Text('Cilt',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700))),Expanded(child:Slider(value:retus,min:0,max:1,onChanged:(v){setState(()=>retus=v);setP((){});unawaited(_canliYuzAkisiniGuncelle());})),Text('%${(retus*100).round()}',style:const TextStyle(color:Colors.white))]),
          Row(children:[const SizedBox(width:78,child:Text('Göz',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700))),Expanded(child:Slider(value:gozCanlilik,min:0,max:.7,onChanged:(v){setState(()=>gozCanlilik=v);setP((){});unawaited(_canliYuzAkisiniGuncelle());})),Text('%${(gozCanlilik*100).round()}',style:const TextStyle(color:Colors.white))]),
          Row(children:[const SizedBox(width:78,child:Text('Yüz ışığı',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700))),Expanded(child:Slider(value:yuzIsigi,min:0,max:.7,onChanged:(v){setState(()=>yuzIsigi=v);setP((){});unawaited(_canliYuzAkisiniGuncelle());})),Text('%${(yuzIsigi*100).round()}',style:const TextStyle(color:Colors.white))]),
          SwitchListTile(
            contentPadding:EdgeInsets.zero,dense:true,value:otomatikPortre,
            onChanged:(v){setState(()=>otomatikPortre=v);setP((){});unawaited(_canliYuzAkisiniGuncelle());},
            secondary:const Icon(Icons.auto_awesome_rounded,color:Colors.white70),
            title:const Text('Otomatik doğal portre',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
            subtitle:const Text('Ön kamerada ışık, ten tonu ve sert kontrastı dengeler.',style:TextStyle(color:Colors.white60,fontSize:11)),
          ),
        ]),
      ))),
    );
  }

  @override void didChangeAppLifecycleState(AppLifecycleState state){
    final c=kontrol;if(c==null||!c.value.isInitialized)return;
    if(state==AppLifecycleState.inactive||state==AppLifecycleState.paused){
      if(kayit)unawaited(_videoDurdur());else{kontrol=null;unawaited(c.dispose());}
    }else if(state==AppLifecycleState.resumed&&kontrol==null&&kameralar.isNotEmpty){
      setState(()=>hazirlaniyor=true);unawaited(_kontroluKur(kameralar[kameraIndex]));
    }
  }

  @override void dispose(){
    WidgetsBinding.instance.removeObserver(this);
    sayacTimer?.cancel();kayitTimer?.cancel();
    unawaited(kontrol?.dispose());
    unawaited(_yuzAlgilayici.close());
    super.dispose();
  }

  @override Widget build(BuildContext context){
    return Scaffold(
      backgroundColor:Colors.black,
      body:SafeArea(child:Stack(children:[
        Positioned.fill(child:ClipRRect(borderRadius:BorderRadius.circular(28),child:_kameraOnizleme())),
        Positioned(top:10,left:10,right:10,child:Row(children:[
          _yuvarlak(Icons.close_rounded,()=>Navigator.pop(context)),
          const Spacer(),
          if(kayit)Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),decoration:BoxDecoration(color:Colors.red,borderRadius:BorderRadius.circular(18)),child:Text(_kayitYazi,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900))),
          const Spacer(),
          _yuvarlak(Icons.cameraswitch_rounded,_kameraCevir,yazi:'Çevir',aktif:kontrol?.description.lensDirection==CameraLensDirection.front),
        ])),
        Positioned(top:74,right:12,child:Column(children:[
          _yuvarlak(_flashIkon,_flashDegistir,yazi:'Flaş',aktif:flash!=FlashMode.off),const SizedBox(height:10),
          _yuvarlak(Icons.timer_outlined,(){setState(()=>sayac=sayac==0?3:sayac==3?10:0);},yazi:sayac==0?'Sayaç':'${sayac}s',aktif:sayac>0),const SizedBox(height:10),
          _yuvarlak(Icons.grid_3x3_rounded,()=>setState(()=>izgara=!izgara),yazi:'Izgara',aktif:izgara),const SizedBox(height:10),
          _yuvarlak(Icons.aspect_ratio_rounded,(){setState(()=>oran=oran=='9:16'?'1:1':oran=='1:1'?'16:9':'9:16');},yazi:oran,aktif:oran!='9:16'),const SizedBox(height:10),
          _yuvarlak(Icons.filter_alt_rounded,()=>unawaited(_filtrePaneli()),yazi:'Filtre',aktif:filtreIndex!=0),
        ])),
        if(oran!='9:16')Positioned.fill(child:IgnorePointer(child:Center(child:AspectRatio(
          aspectRatio:oran=='1:1'?1:16/9,
          child:Container(decoration:BoxDecoration(border:Border.all(color:Colors.white70,width:2),borderRadius:BorderRadius.circular(14))),
        )))),
        if(_aktifSayac>0)Center(child:Text(_aktifSayac.toString(),style:const TextStyle(color:Colors.white,fontSize:92,fontWeight:FontWeight.w900,shadows:[Shadow(blurRadius:18,color:Colors.black)]))),
        Positioned(left:12,right:12,bottom:18,child:Column(children:[
          if(zoom>1.01)Padding(padding:const EdgeInsets.only(bottom:8),child:Text('${zoom.toStringAsFixed(1)}x',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900))),
          Row(mainAxisAlignment:MainAxisAlignment.center,children:[
            TextButton(onPressed:kayit?null:()=>unawaited(_videoModu(false)),child:Text('FOTOĞRAF',style:TextStyle(color:!video?Colors.white:Colors.white54,fontWeight:FontWeight.w900))),
            const SizedBox(width:8),
            GestureDetector(
              onTap:()=>unawaited(_cek()),
              child:AnimatedContainer(
                duration:const Duration(milliseconds:160),
                width:82,height:82,
                decoration:BoxDecoration(
                  shape:BoxShape.circle,
                  color:kayit?Colors.red:Colors.white,
                  border:Border.all(color:Colors.white,width:5),
                  boxShadow:const [BoxShadow(color:Colors.black45,blurRadius:12)],
                ),
                child:isleniyor?const Padding(padding:EdgeInsets.all(25),child:CircularProgressIndicator(strokeWidth:3,color:Colors.black54)):Icon(kayit?Icons.stop_rounded:(video?Icons.videocam_rounded:Icons.camera_alt_rounded),color:kayit?Colors.white:Colors.black,size:32),
              ),
            ),
            const SizedBox(width:8),
            TextButton(onPressed:kayit?null:()=>unawaited(_videoModu(true)),child:Text('VİDEO',style:TextStyle(color:video?Colors.white:Colors.white54,fontWeight:FontWeight.w900))),
          ]),
          const SizedBox(height:8),
          Text(
            video&&filtreIndex!=0?lt('Video filtresi canlı önizlemede gösterilir; yayın sonrası filtre işleme sonraki kalite aşamasında tamamlanacak.','Video filter is previewed live; post-processing will be completed in the next quality pass.'):lt('İki parmakla yakınlaştır • Ön/arka kamerayı istediğin an çevir','Pinch to zoom • Switch front/back camera anytime'),
            textAlign:TextAlign.center,
            style:const TextStyle(color:Colors.white54,fontSize:10.5),
          ),
        ])),
      ])),
    );
  }
}

Rect _ngelxCanliYuzRect({
  required Rect raw,
  required Size canvas,
  required Size image,
  required InputImageRotation rotation,
  required CameraLensDirection lensDirection,
  required bool ayna,
}){
  Offset donustur(double x,double y){
    double rx=x,ry=y,rw=image.width,rh=image.height;
    switch(rotation){
      case InputImageRotation.rotation90deg:
        rx=image.height-y;ry=x;rw=image.height;rh=image.width;break;
      case InputImageRotation.rotation180deg:
        rx=image.width-x;ry=image.height-y;break;
      case InputImageRotation.rotation270deg:
        rx=y;ry=image.width-x;rw=image.height;rh=image.width;break;
      case InputImageRotation.rotation0deg:
        break;
    }
    if((lensDirection==CameraLensDirection.front)^ayna)rx=rw-rx;
    final scale=math.max(canvas.width/rw,canvas.height/rh);
    final dx=(canvas.width-rw*scale)/2,dy=(canvas.height-rh*scale)/2;
    return Offset(dx+rx*scale,dy+ry*scale);
  }
  final p1=donustur(raw.left,raw.top),p2=donustur(raw.right,raw.bottom);
  var r=Rect.fromLTRB(math.min(p1.dx,p2.dx),math.min(p1.dy,p2.dy),math.max(p1.dx,p2.dx),math.max(p1.dy,p2.dy));
  final ex=r.width*.10,ey=r.height*.08;
  r=Rect.fromLTRB(r.left-ex,r.top-ey,r.right+ex,r.bottom+ey);
  return r.intersect(Offset.zero&canvas);
}

class _NgelXCanliYuzClipper extends CustomClipper<Path>{
  final List<Face> yuzler;
  final Size imageSize;
  final InputImageRotation rotation;
  final CameraLensDirection lensDirection;
  final bool ayna;
  const _NgelXCanliYuzClipper({required this.yuzler,required this.imageSize,required this.rotation,required this.lensDirection,required this.ayna});
  @override Path getClip(Size size){
    final p=Path();
    for(final f in yuzler){
      final r=_ngelxCanliYuzRect(raw:f.boundingBox,canvas:size,image:imageSize,rotation:rotation,lensDirection:lensDirection,ayna:ayna);
      if(r.width>8&&r.height>8)p.addOval(r);
    }
    return p;
  }
  @override bool shouldReclip(covariant _NgelXCanliYuzClipper old)=>old.yuzler!=yuzler||old.imageSize!=imageSize||old.rotation!=rotation||old.lensDirection!=lensDirection||old.ayna!=ayna;
}

class _NgelXCanliYuzGlowPainter extends CustomPainter{
  final List<Face> yuzler;
  final Size imageSize;
  final InputImageRotation rotation;
  final CameraLensDirection lensDirection;
  final bool ayna;
  final double yogunluk;
  const _NgelXCanliYuzGlowPainter({required this.yuzler,required this.imageSize,required this.rotation,required this.lensDirection,required this.ayna,required this.yogunluk});
  @override void paint(Canvas canvas,Size size){
    final a=(.018+yogunluk*.032).clamp(0.0,.05).toDouble();
    for(final f in yuzler){
      final r=_ngelxCanliYuzRect(raw:f.boundingBox,canvas:size,image:imageSize,rotation:rotation,lensDirection:lensDirection,ayna:ayna);
      if(r.width<8||r.height<8)continue;
      final paint=Paint()..shader=RadialGradient(colors:[Colors.white.withValues(alpha:a),Colors.transparent],stops:const [.12,1]).createShader(r);
      canvas.drawOval(r,paint);
    }
  }
  @override bool shouldRepaint(covariant _NgelXCanliYuzGlowPainter old)=>old.yuzler!=yuzler||old.imageSize!=imageSize||old.rotation!=rotation||old.lensDirection!=lensDirection||old.ayna!=ayna||old.yogunluk!=yogunluk;
}

class _NgelXIzgaraPainter extends CustomPainter{
  @override void paint(Canvas canvas,Size size){
    final p=Paint()..color=Colors.white30..strokeWidth=1;
    canvas.drawLine(Offset(size.width/3,0),Offset(size.width/3,size.height),p);
    canvas.drawLine(Offset(size.width*2/3,0),Offset(size.width*2/3,size.height),p);
    canvas.drawLine(Offset(0,size.height/3),Offset(size.width,size.height/3),p);
    canvas.drawLine(Offset(0,size.height*2/3),Offset(size.width,size.height*2/3),p);
  }
  @override bool shouldRepaint(covariant CustomPainter oldDelegate)=>false;
}
