part of 'main.dart';

class Ngelx453InboxPreview extends StatefulWidget{
  final Map<String,dynamic> chat;final String me;final bool unread;
  const Ngelx453InboxPreview({super.key,required this.chat,required this.me,required this.unread});
  @override State<Ngelx453InboxPreview> createState()=>_Ngelx453InboxPreviewState();
}
class _Ngelx453InboxPreviewState extends State<Ngelx453InboxPreview>{
  String _sender='';Stream<DocumentSnapshot<Map<String,dynamic>>>? _profile;
  void _connect(){final sender=(widget.chat['lastSenderId']??'').toString();if(sender==_sender)return;_sender=sender;_profile=sender.isEmpty||sender==widget.me?null:FirebaseFirestore.instance.collection('users').doc(sender).snapshots();}
  @override void initState(){super.initState();_connect();}
  @override void didUpdateWidget(covariant Ngelx453InboxPreview old){super.didUpdateWidget(old);_connect();}
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_profile,builder:(_,p){
    final person=p.data?.data()??<String,dynamic>{};
    final name=_sender==widget.me?'Sen':(person['displayName']??person['username']??'').toString();
    final message=(widget.chat['lastMessage']??'Grup oluşturuldu').toString();
    return Text(name.isEmpty?message:'$name: $message',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:widget.unread?const Color(0xFF252B36):const Color(0xFF727886),fontSize:14,fontWeight:widget.unread?FontWeight.w700:FontWeight.w400));
  });
}

class Ngelx453Photo extends StatelessWidget {
  final String url;
  const Ngelx453Photo({super.key,required this.url});
  @override Widget build(BuildContext context){
    final width=math.min(320.0,MediaQuery.sizeOf(context).width*.72);
    return ClipRRect(borderRadius:BorderRadius.circular(18),child:Image(
      image:ResizeImage(NgelXAgImageProvider(url),width:(width*MediaQuery.devicePixelRatioOf(context)).ceil()),
      width:width,fit:BoxFit.contain,gaplessPlayback:true,
      frameBuilder:(_,child,frame,sync)=>frame!=null||sync?child:SizedBox(width:width,height:width*1.2,child:const Center(child:CircularProgressIndicator(strokeWidth:2))),
      errorBuilder:(_,__,___)=>SizedBox(width:width,height:160,child:const Center(child:Icon(Icons.broken_image_outlined))),
    ));
  }
}

class Ngelx453Hearts extends StatefulWidget {
  final ValueListenable<int> pulses;
  const Ngelx453Hearts({super.key,required this.pulses});
  @override State<Ngelx453Hearts> createState()=>_Ngelx453HeartsState();
}
class _Ngelx453HeartsState extends State<Ngelx453Hearts>{
  final List<int> _hearts=[];int _serial=0;
  @override void initState(){super.initState();widget.pulses.addListener(_add);}
  @override void didUpdateWidget(covariant Ngelx453Hearts old){super.didUpdateWidget(old);if(old.pulses!=widget.pulses){old.pulses.removeListener(_add);widget.pulses.addListener(_add);}}
  void _add(){if(!mounted)return;setState((){_hearts.add(++_serial);if(_hearts.length>24)_hearts.removeAt(0);});}
  @override void dispose(){widget.pulses.removeListener(_add);super.dispose();}
  @override Widget build(BuildContext context)=>IgnorePointer(child:SizedBox(width:90,height:280,child:Stack(children:_hearts.map((id)=>TweenAnimationBuilder<double>(
    key:ValueKey(id),tween:Tween(begin:0,end:1),duration:Duration(milliseconds:1800+(id%4)*120),
    onEnd:(){if(mounted)setState(()=>_hearts.remove(id));},
    builder:(_,t,__)=>Positioned(bottom:240*t,left:12+(id%4)*11+math.sin(t*math.pi*2+id)*8,child:Opacity(opacity:1-t,child:Transform.scale(scale:.7+.5*math.sin(t*math.pi),child:Icon(Icons.favorite,color:const Color(0xFFFF4081),size:26+(id%3)*5.0)))),
  )).toList())));
}

class Ngelx453LiveComposer extends StatefulWidget{
  final TextEditingController controller;final FocusNode focus;
  final Stream<DocumentSnapshot<Map<String,dynamic>>> stream;
  final bool host;final String uid;final Future<void> Function() send;
  const Ngelx453LiveComposer({super.key,required this.controller,required this.focus,required this.stream,required this.host,required this.uid,required this.send});
  @override State<Ngelx453LiveComposer> createState()=>_Ngelx453LiveComposerState();
}
class _Ngelx453LiveComposerState extends State<Ngelx453LiveComposer>{
  bool _sending=false;
  Future<void> _send()async{if(_sending||widget.controller.text.trim().isEmpty)return;setState(()=>_sending=true);try{await widget.send();}catch(_){if(mounted)ngelxDurumMesaji(context,'Yorum gönderilemedi. Yazdığın metin korundu.',tip:'hata');}finally{if(mounted){setState(()=>_sending=false);}}}
  Future<void> _emoji()async{
    final selected=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,builder:(c)=>SafeArea(child:Padding(padding:const EdgeInsets.all(16),child:Wrap(spacing:12,runSpacing:12,children:['❤️','👏','😂','🔥','😍','👋','🎉','👍'].map((e)=>TextButton(onPressed:()=>Navigator.pop(c,e),child:Text(e,style:const TextStyle(fontSize:30)))).toList()))));
    if(!mounted)return;if(selected!=null){final value=widget.controller.value;final selection=value.selection.isValid?value.selection:TextSelection.collapsed(offset:value.text.length);final text=value.text.replaceRange(selection.start,selection.end,selected);widget.controller.value=TextEditingValue(text:text,selection:TextSelection.collapsed(offset:selection.start+selected.length));}widget.focus.requestFocus();
  }
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:widget.stream,builder:(_,snap){
    final v=snap.data?.data()??<String,dynamic>{},uid=widget.uid;
    final muted=!widget.host&&List<String>.from(v['mutedUsers']??const[]).contains(uid);
    final enabled=widget.host||(v['commentsEnabled']!=false&&!muted);
    return Row(key:const ValueKey('live-composer-row453'),children:[Expanded(child:TextField(
      key:const ValueKey('live-comment-input453'),controller:widget.controller,focusNode:widget.focus,enabled:enabled,
      textInputAction:TextInputAction.send,onEditingComplete:(){},onSubmitted:enabled?(_)=>_send():null,style:const TextStyle(color:Colors.black87,fontSize:15),
      decoration:InputDecoration(hintText:enabled?'Yorum yaz…':muted?'Yorumların susturuldu':'Yorumlar kapalı',filled:true,fillColor:const Color(0xFFF0F2F5),contentPadding:const EdgeInsets.symmetric(horizontal:16,vertical:13),border:OutlineInputBorder(borderRadius:BorderRadius.circular(28),borderSide:BorderSide.none),suffixIcon:IconButton(tooltip:'Emoji',onPressed:enabled?_emoji:null,icon:const Icon(Icons.sentiment_satisfied_alt,color:Colors.black54))),
    )),const SizedBox(width:8),IconButton.filled(tooltip:'Yorumu gönder',style:IconButton.styleFrom(backgroundColor:const Color(0xFF20C5CA),foregroundColor:Colors.white),onPressed:enabled&&!_sending?_send:null,icon:_sending?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded))]);
  });
}
