part of 'main.dart';

// Resolve intrinsic dimensions once, so tall screenshots have no padded frame.
class Ngelx548ChatPhoto extends StatefulWidget{
  final String url;
  const Ngelx548ChatPhoto({super.key,required this.url});
  @override State<Ngelx548ChatPhoto> createState()=>_Ngelx548ChatPhotoState();
}
class _Ngelx548ChatPhotoState extends State<Ngelx548ChatPhoto>{
  ImageStream? _stream;ImageStreamListener? _listener;
  Size? _pixels;bool _failed=false;
  void _resolve(){
    if(_stream!=null&&_listener!=null)_stream!.removeListener(_listener!);
    _pixels=null;_failed=false;
    _stream=NgelXAgImageProvider(widget.url).resolve(createLocalImageConfiguration(context));
    _listener=ImageStreamListener((info,sync){
      if(!mounted){info.dispose();return;}
      final pixels=Size(info.image.width.toDouble(),info.image.height.toDouble());
      info.dispose();setState(()=>_pixels=pixels);
    },onError:(Object error,StackTrace? stack){if(mounted)setState(()=>_failed=true);});
    _stream!.addListener(_listener!);
  }
  @override void didChangeDependencies(){super.didChangeDependencies();if(_stream==null)_resolve();}
  @override void didUpdateWidget(covariant Ngelx548ChatPhoto old){super.didUpdateWidget(old);if(old.url!=widget.url)_resolve();}
  @override void dispose(){if(_stream!=null&&_listener!=null)_stream!.removeListener(_listener!);super.dispose();}
  @override Widget build(BuildContext context){
    final screen=MediaQuery.sizeOf(context);
    final size=ngelx548PhotoSize(_pixels?.width??0,_pixels?.height??0,screen.width,screen.height);
    return SizedBox(width:size.width,height:size.height,child:ClipRRect(
      borderRadius:BorderRadius.circular(12),child:_failed
        ?const Center(child:Icon(Icons.broken_image_outlined))
        :_pixels==null?const Center(child:CircularProgressIndicator(strokeWidth:2))
        :Image(image:NgelXAgImageProvider(widget.url),width:size.width,height:size.height,
          fit:BoxFit.contain,gaplessPlayback:true)));
  }
}

// Private prejoin preview: CameraController never publishes LiveKit tracks.
class Ngelx548GuestPreview extends StatefulWidget{
  final bool video;
  const Ngelx548GuestPreview({super.key,required this.video});
  @override State<Ngelx548GuestPreview> createState()=>Ngelx548GuestPreviewState();
}
class Ngelx548GuestPreviewState extends State<Ngelx548GuestPreview> with WidgetsBindingObserver{
  CameraController? _camera,_opening548;String? _error;int _revision=0;bool _stopped=false;
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);if(widget.video)unawaited(_start());}
  @override void didUpdateWidget(covariant Ngelx548GuestPreview old){super.didUpdateWidget(old);if(old.video!=widget.video){if(widget.video)unawaited(_start());else unawaited(stop548());}}
  Future<void> _start()async{
    final revision=++_revision;_stopped=false;
    final previous=_camera,opening=_opening548;_camera=null;_opening548=null;await previous?.dispose();if(!identical(previous,opening))await opening?.dispose();
    try{
      if(!(await Permission.camera.request()).isGranted)throw StateError('permission');
      if(!mounted||_stopped||revision!=_revision||!widget.video)return;
      final cameras=await availableCameras();
      if(!mounted||_stopped||revision!=_revision||!widget.video)return;
      if(cameras.isEmpty)throw StateError('camera');
      final camera=cameras.firstWhere((c)=>c.lensDirection==CameraLensDirection.front,orElse:()=>cameras.first);
      final controller=CameraController(camera,ResolutionPreset.medium,enableAudio:false);
      _opening548=controller;
      await controller.initialize();
      if(identical(_opening548,controller))_opening548=null;
      if(!mounted||_stopped||revision!=_revision||!widget.video){await controller.dispose();return;}
      setState((){_camera=controller;_error=null;});
    }catch(_){if(mounted&&revision==_revision)setState(()=>_error='Önizleme açılamadı. Sesli katılabilir veya kamerayı sonra açabilirsin.');}
  }
  Future<void> stop548()async{_stopped=true;_revision++;final camera=_camera,opening=_opening548;_camera=null;_opening548=null;await camera?.dispose();if(!identical(camera,opening))await opening?.dispose();}
  @override void didChangeAppLifecycleState(AppLifecycleState state){
    if(state!=AppLifecycleState.resumed)unawaited(stop548());
    else if(widget.video)unawaited(_start());
  }
  @override void dispose(){WidgetsBinding.instance.removeObserver(this);unawaited(stop548());super.dispose();}
  @override Widget build(BuildContext context){
    if(!widget.video)return const Padding(padding:EdgeInsets.all(16),child:Row(children:[
      Icon(Icons.mic_rounded,color:Colors.white),SizedBox(width:12),
      Expanded(child:Text('Yalnızca sesin paylaşılacak. Kamera kapalı.',style:TextStyle(color:Colors.white70)))]));
    final camera=_camera;
    return SizedBox(height:150,child:ClipRRect(borderRadius:BorderRadius.circular(14),child:Stack(fit:StackFit.expand,children:[
      const ColoredBox(color:Color(0xFF161322)),
      if(camera!=null&&camera.value.isInitialized)Center(child:AspectRatio(aspectRatio:camera.value.aspectRatio,child:CameraPreview(camera)))
      else Center(child:Padding(padding:const EdgeInsets.all(12),child:Text(_error??'Önizleme hazırlanıyor…',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70)))),
      const Positioned(bottom:7,left:8,child:Text('Sadece sen görüyorsun',style:TextStyle(color:Colors.white,fontSize:11))),
    ])));
  }
}
