part of 'main.dart';

class NgelXKameraFiltre {
  final String ad;
  final List<double> matris;
  final double parlaklik;
  final double doygunluk;
  final double sicaklik;
  const NgelXKameraFiltre(this.ad,this.matris,{this.parlaklik=1,this.doygunluk=1,this.sicaklik=0});
}

const List<NgelXKameraFiltre> ngelxKameraFiltreleri=[
  NgelXKameraFiltre('Doğal',<double>[
    1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0,
  ]),
  NgelXKameraFiltre('Canlı',<double>[
    1.12,0,0,0,4, 0,1.06,0,0,2, 0,0,1.10,0,2, 0,0,0,1,0,
  ],doygunluk:1.18),
  NgelXKameraFiltre('Portre',<double>[
    1.04,0,0,0,5, 0,1.02,0,0,4, 0,0,.98,0,2, 0,0,0,1,0,
  ],parlaklik:1.04,doygunluk:1.03,sicaklik:.06),
  NgelXKameraFiltre('Clean',<double>[
    1.03,0,0,0,4, 0,1.03,0,0,4, 0,0,1.02,0,3, 0,0,0,1,0,
  ],parlaklik:1.05,doygunluk:1.02),
  NgelXKameraFiltre('Soft',<double>[
    1.02,0,0,0,7, 0,1.01,0,0,6, 0,0,1.00,0,5, 0,0,0,1,0,
  ],parlaklik:1.06,doygunluk:.98,sicaklik:.04),
  NgelXKameraFiltre('Glow',<double>[
    1.05,0,0,0,8, 0,1.03,0,0,6, 0,0,1.01,0,4, 0,0,0,1,0,
  ],parlaklik:1.07,doygunluk:1.05,sicaklik:.05),
  NgelXKameraFiltre('HD',<double>[
    1.06,0,0,0,2, 0,1.05,0,0,2, 0,0,1.06,0,2, 0,0,0,1,0,
  ],parlaklik:1.02,doygunluk:1.06),
  NgelXKameraFiltre('Sıcak',<double>[
    1.10,0,0,0,5, 0,1.03,0,0,2, 0,0,.92,0,-2, 0,0,0,1,0,
  ],sicaklik:.18),
  NgelXKameraFiltre('Soğuk',<double>[
    .94,0,0,0,-2, 0,1.02,0,0,1, 0,0,1.12,0,5, 0,0,0,1,0,
  ],sicaklik:-.18),
  NgelXKameraFiltre('Sinematik',<double>[
    1.08,-.03,-.03,0,-4, -.02,1.03,-.02,0,-1, -.02,-.02,.98,0,3, 0,0,0,1,0,
  ],doygunluk:.92),
  NgelXKameraFiltre('Retro',<double>[
    .96,.05,.02,0,5, .02,.91,.02,0,2, .04,.02,.82,0,-2, 0,0,0,1,0,
  ],doygunluk:.82,sicaklik:.16),
  NgelXKameraFiltre('S/B',<double>[
    .33,.59,.11,0,0, .33,.59,.11,0,0, .33,.59,.11,0,0, 0,0,0,1,0,
  ],doygunluk:0),
];

class NgelXCameraStudioPage extends StatefulWidget{
  final bool baslangicVideo;
  final Duration maxVideo;
  const NgelXCameraStudioPage({super.key,this.baslangicVideo=false,this.maxVideo=const Duration(minutes:10)});
  @override State<NgelXCameraStudioPage> createState()=>_NgelXCameraStudioPageState();
}

class _NgelXCameraStudioPageState extends State<NgelXCameraStudioPage> with WidgetsBindingObserver{
  List<CameraDescription> kameralar=<CameraDescription>[];
  CameraController? kontrol;
  int kameraIndex=0;
  bool video=false,kayit=false,hazirlaniyor=true,isleniyor=false,ayna=false,izgara=false,otomatikPortre=true;
  int sayac=0;
  Timer? sayacTimer,kayitTimer;
  Duration kayitSure=Duration.zero;
  FlashMode flash=FlashMode.off;
  double zoom=1,minZoom=1,maxZoom=1,retus=.34,filtreYogunluk=1;
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
      try{await eski.dispose();}catch(_){}
      await Future<void>.delayed(const Duration(milliseconds:140));
    }
    final preset=kamera.lensDirection==CameraLensDirection.front?ResolutionPreset.veryHigh:ResolutionPreset.high;
    final yeni=CameraController(kamera,preset,enableAudio:video,imageFormatGroup:ImageFormatGroup.jpeg);
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
    }catch(e){
      try{await yeni.dispose();}catch(_){}
      if(mounted)setState(()=>hazirlaniyor=false);
      rethrow;
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

  Future<XFile> _fotoyuIsle(XFile ham)async{
    final onKamera=kontrol?.description.lensDirection==CameraLensDirection.front;
    final portre=onKamera&&otomatikPortre;
    if(filtreIndex==0&&retus<=.01&&oran=='9:16'&&!portre)return ham;
    try{
      final bytes=await ham.readAsBytes();
      var g=img.decodeImage(bytes);
      if(g==null)return ham;
      g=img.bakeOrientation(g);
      if(oran!='9:16'){
        final hedef=oran=='1:1'?1.0:16/9;
        final mevcut=g.width/g.height;
        int x=0,y=0,w=g.width,h=g.height;
        if(mevcut>hedef){w=(g.height*hedef).round();x=((g.width-w)/2).round();}
        else{h=(g.width/hedef).round();y=((g.height-h)/2).round();}
        g=img.copyCrop(g,x:x,y:y,width:w,height:h);
      }
      final f=ngelxKameraFiltreleri[filtreIndex];
      if(f.ad=='S/B'){
        g=img.adjustColor(g,saturation:(1-filtreYogunluk).clamp(0.0,1.0),brightness:1+(retus*.04)+(portre?.02:0),contrast:1+(retus*.02)-(portre?.015:0));
      }else if(f.ad=='Retro'&&filtreYogunluk>.55){
        g=img.sepia(g);
      }else{
        g=img.adjustColor(
          g,
          brightness:1+((f.parlaklik-1)*filtreYogunluk)+(retus*.04)+(portre?.025:0),
          saturation:1+((f.doygunluk-1)*filtreYogunluk)+(retus*.045)+(portre?.018:0),
          contrast:1+(retus*.018)-(portre?.018:0),
        );
      }
      final dir=await getTemporaryDirectory();
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
        final ham=await c.takePicture();
        final sonuc=await _fotoyuIsle(ham);
        if(mounted)Navigator.pop(context,<String,dynamic>{'file':sonuc,'video':false,'filter':ngelxKameraFiltreleri[filtreIndex].ad,'retouch':retus});
      }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Fotoğraf çekilemedi: $e')));}
      finally{if(mounted)setState(()=>isleniyor=false);}
    });
  }

  Future<void> _videoBaslat()async{
    final c=kontrol;if(c==null||!c.value.isInitialized||kayit)return;
    try{
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
    final b=255*(a*.035);
    return <double>[
      1+a*.03,0,0,0,b,
      0,1+a*.02,0,0,b,
      0,0,1-a*.01,0,b,
      0,0,0,1,0,
    ];
  }

  Widget _kameraOnizleme(){
    final c=kontrol;
    if(c==null||!c.value.isInitialized)return const Center(child:CircularProgressIndicator(color:Colors.white));
    Widget p=CameraPreview(c);
    final f=ngelxKameraFiltreleri[filtreIndex];
    if(filtreIndex!=0)p=ColorFiltered(colorFilter:ColorFilter.matrix(_filtreMatris(f.matris)),child:p);
    if(retus>.01)p=ColorFiltered(colorFilter:ColorFilter.matrix(_retusMatris()),child:p);
    if(c.description.lensDirection==CameraLensDirection.front&&ayna)p=Transform(alignment:Alignment.center,transform:Matrix4.rotationY(math.pi),child:p);
    return GestureDetector(
      onScaleStart:(_)=>_zoomBaslangic=zoom,
      onScaleUpdate:(d){if(d.pointerCount<2)return;final z=(_zoomBaslangic*d.scale).clamp(minZoom,maxZoom).toDouble();zoom=z;unawaited(c.setZoomLevel(z));if(mounted)setState((){});},
      child:Stack(fit:StackFit.expand,children:[
        p,
        if(izgara)CustomPaint(painter:_NgelXIzgaraPainter()),
      ]),
    );
  }
  double _zoomBaslangic=1;

  Widget _yuvarlak(IconData ikon,VoidCallback? onTap,{String? yazi})=>Column(mainAxisSize:MainAxisSize.min,children:[
    InkWell(onTap:onTap,borderRadius:BorderRadius.circular(28),child:Container(width:48,height:48,decoration:BoxDecoration(color:Colors.black45,shape:BoxShape.circle,border:Border.all(color:Colors.white24)),child:Icon(ikon,color:Colors.white))),
    if(yazi!=null)...[const SizedBox(height:3),Text(yazi,style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w700))],
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
            TextButton(onPressed:(){setState(()=>filtreIndex=0);setP((){});},child:const Text('Sıfırla')),
          ]),
          SizedBox(height:92,child:ListView.separated(
            scrollDirection:Axis.horizontal,itemCount:ngelxKameraFiltreleri.length,separatorBuilder:(_,__)=>const SizedBox(width:8),
            itemBuilder:(_,i){
              final secili=i==filtreIndex;
              return InkWell(onTap:(){setState(()=>filtreIndex=i);setP((){});},child:SizedBox(width:72,child:Column(children:[
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
          Row(children:[const Text('Rötuş',style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900)),const Spacer(),TextButton(onPressed:(){setState(()=>retus=0);setP((){});},child:const Text('Sıfırla'))]),
          const Text('Doğal görünüm için düşük ve orta seviyeler önerilir.',style:TextStyle(color:Colors.white60,fontSize:11)),
          Row(children:[const Icon(Icons.face_retouching_natural_rounded,color:Colors.white70),Expanded(child:Slider(value:retus,min:0,max:1,onChanged:(v){setState(()=>retus=v);setP((){});})),Text('%${(retus*100).round()}',style:const TextStyle(color:Colors.white))]),
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
          _yuvarlak(Icons.cameraswitch_rounded,_kameraCevir,yazi:'Çevir'),
        ])),
        Positioned(top:74,right:12,child:Column(children:[
          _yuvarlak(_flashIkon,_flashDegistir,yazi:'Flaş'),const SizedBox(height:10),
          _yuvarlak(Icons.timer_outlined,(){setState(()=>sayac=sayac==0?3:sayac==3?10:0);},yazi:sayac==0?'Sayaç':'${sayac}s'),const SizedBox(height:10),
          _yuvarlak(Icons.grid_3x3_rounded,()=>setState(()=>izgara=!izgara),yazi:'Izgara'),const SizedBox(height:10),
          _yuvarlak(Icons.aspect_ratio_rounded,(){setState(()=>oran=oran=='9:16'?'1:1':oran=='1:1'?'16:9':'9:16');},yazi:oran),const SizedBox(height:10),
          _yuvarlak(Icons.face_retouching_natural_rounded,()=>unawaited(_retusPaneli()),yazi:'Rötuş'),const SizedBox(height:10),
          _yuvarlak(Icons.filter_alt_rounded,()=>unawaited(_filtrePaneli()),yazi:'Filtre'),
        ])),
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
