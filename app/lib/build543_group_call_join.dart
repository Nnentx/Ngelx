part of 'main.dart';

/// A group row watches its call document directly, independently of inbox
/// profile/preview loading. Timer also expires stale join buttons without a write.
class Ngelx543GroupJoin extends StatefulWidget{
  final bool group;final String chatId;final Map<String,dynamic> seed;final VoidCallback join;final Widget usual;
  const Ngelx543GroupJoin({super.key,this.group=true,required this.chatId,required this.seed,required this.join,required this.usual});
  @override State<Ngelx543GroupJoin> createState()=>_Ngelx543GroupJoinState();
}
class _Ngelx543GroupJoinState extends State<Ngelx543GroupJoin>{
  late final stream=FirebaseFirestore.instance.collection('chats').doc(widget.chatId).snapshots(includeMetadataChanges:true);
  Timer? clock;
  @override void initState(){super.initState();clock=Timer.periodic(const Duration(seconds:1),(_){if(mounted)setState((){});});}
  @override void dispose(){clock?.cancel();super.dispose();}
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:stream,builder:(_,snap){
    final chat=snap.hasData?snap.data?.data():widget.seed;
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(snap.hasError||chat==null||uid==null||(chat['isGroup']==true)!=widget.group||
       !List<String>.from(chat['members']??const[]).contains(uid)||
       !ngelx440CallJoinable(chat,DateTime.now()))return widget.usual;
    return SizedBox(width:100,child:FilledButton.icon(
      style:FilledButton.styleFrom(backgroundColor:const Color(0xFF21852C),foregroundColor:Colors.white,padding:const EdgeInsets.symmetric(horizontal:10,vertical:8)),
      onPressed:widget.join,icon:Icon(chat['callVideo']==true?Icons.videocam:Icons.call,size:16),
      label:const Text('KATIL',style:TextStyle(fontSize:12,fontWeight:FontWeight.w800))));
  });
}

/// Explicit tap accepts only the fresh current call belonging to this private
/// chat. It never originates another call or changes the peer's media choices.
Future<void> ngelx543JoinPrivate(BuildContext context,String chatId,String title,String photo)async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null)return;
  try{
    final ref=FirebaseFirestore.instance.collection('chats').doc(chatId);
    final data=(await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8))).data();
    if(data==null||data['isGroup']==true||!List<String>.from(data['members']??const[]).contains(uid)||!ngelx440CallJoinable(data,DateTime.now()))return;
    final members=List<String>.from(data['members']??const[]);
    if(members.length!=2)return;
    final peer=members.firstWhere((id)=>id!=uid);
    final profiles=await Future.wait([for(final id in [uid,peer])FirebaseFirestore.instance.collection('users').doc(id).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8))]);
    if(List<String>.from(profiles[0].data()?['blocked']??const[]).contains(peer)||List<String>.from(profiles[1].data()?['blocked']??const[]).contains(uid)||FirebaseAuth.instance.currentUser?.uid!=uid)return;
    final name=(data['callRoomName']??'').toString();
    if(ngelxCallSession444.room==name&&ngelxCallSession444.background){await ngelx445ReturnCall(name);return;}
    if(!context.mounted||!ngelx444ReserveCall(context,name))return;
    await Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXAramaPage(roomName:name,baslik:title,foto:photo,goruntulu:data['callVideo']==true,aramaRef:ref)));
  }catch(_){if(context.mounted)ngelxDurumMesaji(context,'Aramaya katılınamadı. Tekrar dene.',tip:'hata');}
}
