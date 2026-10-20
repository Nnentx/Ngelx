part of 'main.dart';

/// A group row watches its call document directly, independently of inbox
/// profile/preview loading. Timer also expires stale join buttons without a write.
class Ngelx543GroupJoin extends StatefulWidget{
  final String chatId;final Map<String,dynamic> seed;final VoidCallback join;final Widget usual;
  const Ngelx543GroupJoin({super.key,required this.chatId,required this.seed,required this.join,required this.usual});
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
    if(snap.hasError||chat==null||uid==null||chat['isGroup']!=true||
       !List<String>.from(chat['members']??const[]).contains(uid)||
       !ngelx440CallJoinable(chat,DateTime.now()))return widget.usual;
    return SizedBox(width:100,child:FilledButton.icon(
      style:FilledButton.styleFrom(backgroundColor:const Color(0xFF21852C),foregroundColor:Colors.white,padding:const EdgeInsets.symmetric(horizontal:10,vertical:8)),
      onPressed:widget.join,icon:const Icon(Icons.call,size:16),
      label:const Text('KATIL',style:TextStyle(fontSize:12,fontWeight:FontWeight.w800))));
  });
}
