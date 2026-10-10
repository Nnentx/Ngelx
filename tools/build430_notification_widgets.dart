// Used after the existing Build429 source has been generated.
class NgelXProfilBildirimZili extends StatefulWidget {
  const NgelXProfilBildirimZili({super.key});
  @override State<NgelXProfilBildirimZili> createState()=>_NgelXProfilBildirimZiliState();
}
class _NgelXProfilBildirimZiliState extends State<NgelXProfilBildirimZili>{
  late final String? _uid=FirebaseAuth.instance.currentUser?.uid;
  late final _stream=_uid==null?null:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:_uid).limit(200).snapshots();
  @override Widget build(BuildContext context)=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
    stream:_stream,
    builder:(_,snap){
      final count=ngelxOkunmamisAktiviteSayisi(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]);
      return IconButton(
        tooltip:'Bildirimler',
        onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),
        icon:Stack(clipBehavior:Clip.none,children:[
          const Icon(Icons.notifications_none_rounded,color:mor),
          if(count>0)Positioned(right:-9,top:-8,child:Container(
            padding:const EdgeInsets.symmetric(horizontal:4,vertical:2),
            decoration:BoxDecoration(color:Colors.red,borderRadius:BorderRadius.circular(12)),
            child:Text(count>99?'99+':count.toString(),style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)),
          )),
        ]),
      );
    },
  );
}

// Only mark rows intersecting the viewport of the active route as read.
// Pending request decisions remain independent of notification read state.
class NgelXGorulenBildirim extends StatefulWidget{
  final QueryDocumentSnapshot<Map<String,dynamic>> bildirim;
  final Widget child;
  const NgelXGorulenBildirim({super.key,required this.bildirim,required this.child});
  @override State<NgelXGorulenBildirim> createState()=>_NgelXGorulenBildirimState();
}
class _NgelXGorulenBildirimState extends State<NgelXGorulenBildirim>{
  bool _writing=false;
  Timer? _timer;
  @override void initState(){super.initState();_timer=Timer.periodic(const Duration(seconds:1),(_)=>_schedule());}
  @override void dispose(){_timer?.cancel();super.dispose();}
  void _schedule(){
    if(!mounted||_writing||widget.bildirim.data()['read']==true)return;
    WidgetsBinding.instance.addPostFrameCallback((_)=>_markVisible());
  }
  Future<void> _markVisible()async{
    if(!mounted||_writing||widget.bildirim.data()['read']==true||ModalRoute.of(context)?.isCurrent!=true)return;
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null||widget.bildirim.data()['toUid']!=uid)return;
    final box=context.findRenderObject();
    if(box is! RenderBox||!box.hasSize||!box.attached)return;
    final top=box.localToGlobal(Offset.zero).dy;
    final height=MediaQuery.sizeOf(context).height;
    if(top>=height||top+box.size.height<=0)return;
    _writing=true;
    try{
      await widget.bildirim.reference.update({'read':true}).timeout(const Duration(seconds:8));
    }catch(_){
      // Leave the unread badge intact; retry when connectivity returns.
    }finally{_writing=false;}
  }
  @override Widget build(BuildContext context){_schedule();return widget.child;}
}
