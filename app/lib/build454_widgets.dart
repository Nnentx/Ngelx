part of 'main.dart';

Size ngelx454PhotoBounds(Size screen)=>Size(math.min(280.0,screen.width*.67),math.min(390.0,screen.height*.46));
double? ngelx454UploadFraction(int sent,int total)=>total<=0?null:(sent/total).clamp(0.0,1.0).toDouble();

bool _openingIncoming454=false;
Future<void> ngelx454OpenIncoming(String chat,String room)async{
  if(_openingIncoming454)return;
  final context=ngelxNavigatorKey.currentContext,me=FirebaseAuth.instance.currentUser?.uid;
  if(context==null||me==null)return;
  _openingIncoming454=true;
  try{
    final ref=FirebaseFirestore.instance.collection('chats').doc(chat);
    final doc=await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
    final v=doc.data()??<String,dynamic>{},stamp=v['callCreatedAt'];
    if(!context.mounted||FirebaseAuth.instance.currentUser?.uid!=me||v['callRoomName']!=room||v['callStatus']!='ringing'||stamp is! Timestamp||DateTime.now().difference(stamp.toDate()).inSeconds>=60||!List<String>.from(v['members']??const[]).contains(me))return;
    await showModalBottomSheet<void>(context:context,isScrollControlled:true,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:ref.snapshots(),builder:(_,snapshot){
      final data=snapshot.data?.data()??v;
      final active=data['callRoomName']==room&&data['callStatus']=='ringing';
      return SafeArea(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
        const Icon(Icons.call_rounded,color:mor,size:52),const SizedBox(height:16),
        Text((data['callTitle']??data['groupName']??'Gelen arama').toString(),style:const TextStyle(color:Colors.black87,fontSize:22,fontWeight:FontWeight.w800)),
        const SizedBox(height:12),Text(active?(data['callVideo']==true?'Gelen görüntülü arama':'Gelen sesli arama'):'Bu arama sona erdi.',style:const TextStyle(color:Colors.black54,fontSize:16)),const SizedBox(height:24),
        Row(children:[Expanded(child:OutlinedButton.icon(onPressed:active?()async{Navigator.pop(c);await ngelx448Incoming._action({'chat':chat,'room':room,'action':'reject'});}:()=>Navigator.pop(c),icon:const Icon(Icons.call_end,color:Colors.red),label:Text(active?'Reddet':'Kapat'))),const SizedBox(width:12),if(active)Expanded(child:FilledButton.icon(onPressed:()async{Navigator.pop(c);await ngelx448Incoming._action({'chat':chat,'room':room,'action':'answer'});},icon:const Icon(Icons.call),label:const Text('Cevapla')))]),
      ])));
    }));
  }catch(_){if(context.mounted)ngelxDurumMesaji(context,'Arama ekranı açılamadı. Tekrar dene.',tip:'hata');}
  finally{_openingIncoming454=false;}
}

Future<void> ngelx454RemoveHighlight(BuildContext context,String id)async{
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null||id.isEmpty)return;
  final yes=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Öne çıkandan kaldır?'),content:const Text('Hikâye arşivinde kalacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Kaldır'))]));
  if(yes!=true)return;
  try{await FirebaseFirestore.instance.runTransaction((tx)async{final ref=FirebaseFirestore.instance.collection('videos').doc(id);final doc=await tx.get(ref);if(doc.data()?['ownerId']!=me||FirebaseAuth.instance.currentUser?.uid!=me)throw StateError('owner');tx.update(ref,{'highlighted':false});}).timeout(const Duration(seconds:10));if(context.mounted)ngelxDurumMesaji(context,'Öne çıkandan kaldırıldı.');}
  catch(_){if(context.mounted)ngelxDurumMesaji(context,'Öne çıkan kaldırılamadı. Tekrar dene.',tip:'hata');}
}

class Ngelx454LocalMedia extends StatefulWidget{
  final XFile file;final bool video;
  const Ngelx454LocalMedia({super.key,required this.file,required this.video});
  @override State<Ngelx454LocalMedia> createState()=>_Ngelx454LocalMediaState();
}
class _Ngelx454LocalMediaState extends State<Ngelx454LocalMedia>{
  VideoPlayerController? _video;bool _error=false;
  @override void initState(){super.initState();if(widget.video){final v=kIsWeb?VideoPlayerController.networkUrl(Uri.parse(widget.file.path)):VideoPlayerController.file(File(widget.file.path));_video=v;v.initialize().then((_){if(mounted)setState((){});}).catchError((_){if(mounted)setState(()=>_error=true);});}}
  @override void dispose(){_video?.dispose();super.dispose();}
  @override Widget build(BuildContext c){final v=_video;
    return ClipRRect(borderRadius:BorderRadius.circular(20),child:Container(color:const Color(0xFFF3F4F7),constraints:const BoxConstraints(maxHeight:280),child:widget.video
      ? _error?const SizedBox(height:160,child:Center(child:Text('Önizleme açılamadı; dosyayı yeniden seçebilirsin.'))):v?.value.isInitialized==true?Stack(alignment:Alignment.center,children:[AspectRatio(aspectRatio:v!.value.aspectRatio>0?v.value.aspectRatio:16/9,child:VideoPlayer(v)),IconButton.filled(onPressed:(){setState((){v.value.isPlaying?v.pause():v.play();});},icon:Icon(v.value.isPlaying?Icons.pause:Icons.play_arrow)),Positioned(bottom:8,right:8,child:Container(padding:const EdgeInsets.all(6),color:Colors.black54,child:Text('${v.value.duration.inMinutes}:${(v.value.duration.inSeconds%60).toString().padLeft(2,'0')}',style:const TextStyle(color:Colors.white))))]):const SizedBox(height:160,child:Center(child:CircularProgressIndicator()))
      :kIsWeb?Image.network(widget.file.path,fit:BoxFit.contain):Image.file(File(widget.file.path),fit:BoxFit.contain,cacheWidth:800)));
  }
}
