class NgelXGrupVideoMesaj extends StatefulWidget{
  final String url;final bool compact;
  const NgelXGrupVideoMesaj({super.key,required this.url,this.compact=true});
  @override State<NgelXGrupVideoMesaj> createState()=>_NgelXGrupVideoMesajState();
}
class _NgelXGrupVideoMesajState extends State<NgelXGrupVideoMesaj>{
  VideoPlayerController? kontrol;
  bool yukleniyor=false,hata=false;
  Timer? _bufferTimer;
  int _generation=0;
  bool _lastPlaying=false,_lastBuffering=false;
  @override void initState(){super.initState();if(!widget.compact)WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)unawaited(oynat());});}
  @override void didUpdateWidget(covariant NgelXGrupVideoMesaj old){
    super.didUpdateWidget(old);
    if(old.url!=widget.url){_reset();if(!widget.compact)unawaited(oynat());}
  }
  void _reset(){
    _generation++;_bufferTimer?.cancel();_bufferTimer=null;
    final old=kontrol;kontrol=null;
    if(old!=null){old.removeListener(_changed);unawaited(old.dispose());}
    yukleniyor=false;hata=false;
  }
  void _changed(){
    final c=kontrol;if(!mounted||c==null)return;
    if(c.value.hasError){_failed(c);return;}
    if(c.value.isBuffering){
      _bufferTimer??=Timer(const Duration(seconds:15),(){if(mounted&&kontrol==c&&c.value.isBuffering)_failed(c);});
    }else{_bufferTimer?.cancel();_bufferTimer=null;}
    if(_lastPlaying!=c.value.isPlaying||_lastBuffering!=c.value.isBuffering){
      _lastPlaying=c.value.isPlaying;_lastBuffering=c.value.isBuffering;setState((){});
    }
  }
  void _failed(VideoPlayerController c){
    if(!mounted||kontrol!=c)return;
    _bufferTimer?.cancel();_bufferTimer=null;
    c.removeListener(_changed);unawaited(c.pause());
    setState((){hata=true;yukleniyor=false;});
  }
  Future<void> oynat()async{
    if(yukleniyor)return;
    final existing=kontrol;
    if(existing!=null&&existing.value.isInitialized&&!hata){
      try{if(existing.value.isPlaying){await existing.pause();}else{if(existing.value.position>=existing.value.duration)await existing.seekTo(Duration.zero);await existing.play();}}catch(_){_failed(existing);}
      return;
    }
    _reset();final generation=_generation;
    setState(()=>yukleniyor=true);
    VideoPlayerController? ready;
    for(final url in ngelxMedyaUrlAdaylari(widget.url)){
      if(!mounted||generation!=_generation)return;
      final candidate=VideoPlayerController.networkUrl(Uri.parse(url));kontrol=candidate;
      try{
        await candidate.initialize().timeout(const Duration(seconds:15));
        if(!mounted||generation!=_generation||kontrol!=candidate)return;
        ready=candidate;break;
      }catch(_){
        if(kontrol==candidate)kontrol=null;
        await candidate.dispose();
      }
    }
    if(!mounted||generation!=_generation)return;
    if(ready==null){setState((){hata=true;yukleniyor=false;});return;}
    final c=ready;
    c.addListener(_changed);
    try{await c.setLooping(widget.compact);await c.play();}catch(_){_failed(c);}
    if(mounted&&generation==_generation)setState(()=>yukleniyor=false);
  }
  Future<void> atla(int seconds)async{
    final c=kontrol;if(c==null||!c.value.isInitialized)return;
    final end=c.value.duration.inMilliseconds;
    await c.seekTo(Duration(milliseconds:(c.value.position.inMilliseconds+seconds*1000).clamp(0,end).toInt()));
  }
  @override void dispose(){_reset();super.dispose();}
  @override Widget build(BuildContext context){
    final c=kontrol;
    final height=widget.compact?178.0:MediaQuery.sizeOf(context).height*.68;
    if(hata)return SizedBox(width:widget.compact?246:double.infinity,height:150,child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      const Text('Video yüklenemedi.',style:TextStyle(color:Colors.white)),
      TextButton.icon(onPressed:()=>unawaited(oynat()),icon:const Icon(Icons.refresh_rounded),label:const Text('Tekrar dene')),
    ])));
    if(c==null||!c.value.isInitialized)return GestureDetector(onTap:()=>unawaited(oynat()),child:Container(width:widget.compact?246:double.infinity,height:150,color:const Color(0xFF211837),alignment:Alignment.center,child:yukleniyor?const CircularProgressIndicator(color:Colors.white,strokeWidth:2):const Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:48),Text('Dokun ve oynat',style:TextStyle(color:Colors.white70))])));
    final playing=c.value.isPlaying;
    return GestureDetector(onTap:()=>unawaited(oynat()),child:ClipRRect(borderRadius:BorderRadius.circular(widget.compact?14:0),child:Stack(alignment:Alignment.center,children:[
      SizedBox(width:widget.compact?246:double.infinity,height:height,child:ColoredBox(color:Colors.black,child:FittedBox(fit:BoxFit.contain,child:SizedBox(width:c.value.size.width,height:c.value.size.height,child:VideoPlayer(c))))),
      if(c.value.isBuffering)const IgnorePointer(child:CircularProgressIndicator(color:Colors.white)),
      if(!playing&&!c.value.isBuffering)const IgnorePointer(child:Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:52)),
      if(!widget.compact)...[
        Positioned(left:12,child:IconButton(onPressed:()=>unawaited(atla(-10)),tooltip:'10 saniye geri',icon:const Icon(Icons.replay_10_rounded,color:Colors.white))),
        Positioned(right:12,child:IconButton(onPressed:()=>unawaited(atla(10)),tooltip:'10 saniye ileri',icon:const Icon(Icons.forward_10_rounded,color:Colors.white))),
        Positioned(left:14,right:14,bottom:10,child:VideoProgressIndicator(c,allowScrubbing:true,colors:const VideoProgressColors(playedColor:Colors.white,bufferedColor:Colors.white38,backgroundColor:Colors.white24))),
      ],
    ])));
  }
}
