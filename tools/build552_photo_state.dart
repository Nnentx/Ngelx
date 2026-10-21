class _Ngelx548ChatPhotoState extends State<Ngelx548ChatPhoto>{
 ImageStream? _stream;ImageStreamListener? _listener;
 Timer? _timeout;int _generation=0;
 Size? _pixels;bool _failed=false,_retrying=false;
 void _detach(){
  _timeout?.cancel();
  if(_stream!=null&&_listener!=null)_stream!.removeListener(_listener!);
  _stream=null;_listener=null;
 }
 void _resolve(){
  _detach();final generation=++_generation;
  _pixels=null;_failed=false;
  _timeout=Timer(const Duration(seconds:42),(){
   if(mounted&&generation==_generation&&_pixels==null)setState(()=>_failed=true);
  });
  _stream=NgelXAgImageProvider(widget.url).resolve(createLocalImageConfiguration(context));
  _listener=ImageStreamListener((info,sync){
   if(!mounted||generation!=_generation){info.dispose();return;}
   final pixels=Size(info.image.width.toDouble(),info.image.height.toDouble());
   info.dispose();_timeout?.cancel();
   setState((){_pixels=pixels;_failed=false;});
  },onError:(Object error,StackTrace? stack){
   if(mounted&&generation==_generation){_timeout?.cancel();setState(()=>_failed=true);}
  });
  _stream!.addListener(_listener!);
 }
 Future<void> _retry()async{
  if(_retrying)return;
  final url=widget.url;final generation=++_generation;
  _detach();setState(()=>_retrying=true);
  try{await ngelxAgResmiOnbelleginiTemizle(url);}
  finally{
   if(mounted&&url==widget.url&&generation==_generation){
    setState((){_retrying=false;_resolve();});
   }else if(mounted){setState(()=>_retrying=false);}
  }
 }
 @override void didChangeDependencies(){super.didChangeDependencies();if(_stream==null)_resolve();}
 @override void didUpdateWidget(covariant Ngelx548ChatPhoto old){super.didUpdateWidget(old);if(old.url!=widget.url){_retrying=false;_resolve();}}
 @override void dispose(){++_generation;_detach();super.dispose();}
 @override Widget build(BuildContext context){
  final screen=MediaQuery.sizeOf(context);
  final size=ngelx548PhotoSize(_pixels?.width??0,_pixels?.height??0,screen.width,screen.height);
  return SizedBox(width:size.width,height:_pixels==null?110:size.height,child:ClipRRect(
   borderRadius:BorderRadius.circular(12),child:_failed&&!_retrying
    ?Material(color:const Color(0xFFF1F3F2),child:InkWell(onTap:_retry,
     child:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Icon(Icons.refresh),SizedBox(height:5),Text('Fotoğraf yüklenemedi'),Text('Yeniden dene')]))))
    :_pixels==null?const ColoredBox(color:Color(0xFFF1F3F2),child:Center(child:CircularProgressIndicator(strokeWidth:2)))
    :Image(image:NgelXAgImageProvider(widget.url),width:size.width,height:size.height,
     fit:BoxFit.contain,gaplessPlayback:true)));
 }
}
