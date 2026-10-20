part of 'main.dart';

bool ngelx543MiniCameraVisible({required bool owned,required bool pip,required bool foreground,required bool background,required bool cardVisible})=>owned&&(pip||(foreground&&background&&cardVisible));

/// Reuses the one existing LiveKit room. No token, camera or connection is
/// created by minimizing. Android owns cross-app dragging and resize behavior.
class Ngelx543PipCall {
  static lk.Room? foreground;
  static String? roomName,ownerUid;
  static String title='NgelX';
  static Future<void> Function(String)? foregroundAction;
  static bool _installed=false,_ending=false,_closing=false;
  static StreamSubscription<User?>? _auth;
  static void install(){
    if(_installed)return;
    _installed=true;
    void closeEnded(){if(Ngelx520PipBridge.active.value&&current==null&&!_ending)unawaited(_endPip());}
    void refresh(){closeEnded();unawaited(ngelx446Calls.refreshMini543());}
    ngelx445CallRevision.addListener(refresh);
    Ngelx520PipBridge.active.addListener(refresh);
    ngelx448HiddenCallCard.addListener(refresh);
    _auth=FirebaseAuth.instance.authStateChanges().listen((_)=>refresh());
  }
  static void bind(lk.Room? room,String name,String heading,Future<void> Function(String) action){
    install();
    foreground=room;roomName=name;title=heading;
    ownerUid=room?.localParticipant?.identity.toString();foregroundAction=action;
  }
  static void clear(String name){
    if(roomName!=name)return;
    foreground=null;roomName=null;foregroundAction=null;ownerUid=null;
  }
  static ({lk.Room room,String title})? get current {
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null)return null;
    if(foreground!=null&&ownerUid==uid)return (room:foreground!,title:title);
    final name=ngelxCallSession444.room,detail=ngelx445CallDetails[ngelxCallSession444.room];
    if(name==null||detail==null||detail.uid!=uid||!ngelxCallSession444.background)return null;
    final room=_ngelxArkaPlanAramaOdalari[name];
    return room==null||room.localParticipant?.identity.toString()!=uid?null:(room:room,title:detail.title);
  }
  static bool _restoring=false;
  static Future<void> restoreAfterExpand()async{
    if(_restoring)return;
    _restoring=true;
    try{
      await Future<void>.delayed(const Duration(milliseconds:350));
      final name=ngelxCallSession444.room;
      if(WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed&&
         !Ngelx520PipBridge.active.value&&foreground==null&&name!=null&&current!=null){
        await ngelx445ReturnCall(name);
      }
    }finally{_restoring=false;}
  }
  static Future<bool> background()async{
    if(current==null)return false;
    if(Ngelx520PipBridge.active.value)return true;
    await Ngelx509FloatingCallBridge.hide();
    return Ngelx520PipBridge.enter();
  }
  static Future<void> _endPip()async{
    if(_closing)return;
    _closing=true;
    try{await const MethodChannel('com.nnentx.ngelx_app/call_pip_520').invokeMethod<void>('endPip543');}catch(_){}
    Ngelx520PipBridge.active.value=false;
    _closing=false;
  }
  static Future<void> action(String action)async{
    if(current==null)return;
    if(foreground!=null&&ownerUid==FirebaseAuth.instance.currentUser?.uid){
      if(action=='end'){
        _ending=true;
        try{await foregroundAction?.call(action);}finally{_ending=false;if(current==null)await _endPip();}
      }else{await foregroundAction?.call(action);}
      return;
    }
    final name=ngelxCallSession444.room;
    if(name==null)return;
    final room=_ngelxArkaPlanAramaOdalari[name];
    if(room==null)return;
    if(action=='end'){_ending=true;try{await ngelx445EndBackground(name);}finally{_ending=false;await _endPip();}return;}
    if(action=='microphone'){
      if(ngelx446Calls.muted(name))return;
      final local=room.localParticipant;
      if(local!=null)await local.setMicrophoneEnabled(!local.isMicrophoneEnabled());
    }else if(action=='speaker'){
      await lk.AudioManager.instance.setSpeakerOutputPreferred(!lk.AudioManager.instance.isSpeakerOutputPreferred);
    }
  }
}
class Ngelx543GlobalPip extends StatelessWidget{
  const Ngelx543GlobalPip({super.key});
  @override Widget build(BuildContext context)=>ValueListenableBuilder<bool>(
    valueListenable:Ngelx520PipBridge.active,builder:(_,active,__){
      final call=Ngelx543PipCall.current;
      if(!active||call==null)return const SizedBox.shrink();
      return Positioned.fill(child:Material(child:Ngelx543MiniCall(room:call.room,title:call.title)));
    });
}
class Ngelx543MiniCall extends StatelessWidget{
  final lk.Room room;final String title;
  const Ngelx543MiniCall({super.key,required this.room,required this.title});
  @override Widget build(BuildContext context)=>AnimatedBuilder(animation:room,builder:(_,__){
    final people=<lk.Participant>[if(room.localParticipant!=null)room.localParticipant!,...room.remoteParticipants.values];
    final visible=people.take(12).toList();
    return ColoredBox(color:const Color(0xFF21133F),child:Padding(
      padding:const EdgeInsets.all(5),child:Column(children:[
        Text('$title · ${people.length} kişi',maxLines:1,overflow:TextOverflow.ellipsis,
          style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w700)),
        const SizedBox(height:3),
        Expanded(child:visible.isEmpty?const Center(child:Text('Bağlanıyor…',style:TextStyle(color:Colors.white))):
          Ngelx543MiniGrid(children:[for(final person in visible)
            Ngelx543MiniParticipant(key:ValueKey(person.identity),participant:person,local:identical(person,room.localParticipant))])),
      ])));
  });
}
/// Twelve visible seats adapt to Android's actual PiP bounds.
class Ngelx543MiniGrid extends StatelessWidget{
  final List<Widget> children;
  const Ngelx543MiniGrid({super.key,required this.children});
  @override Widget build(BuildContext context)=>LayoutBuilder(builder:(_,box){
    final count=math.min(children.length,12);
    if(count==0)return const SizedBox.shrink();
    final columns=count>=10?4:count>=5?3:count==1?1:2;
    final rows=(count/columns).ceil();
    return GridView.builder(padding:EdgeInsets.zero,physics:const NeverScrollableScrollPhysics(),itemCount:count,
      gridDelegate:SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:columns,crossAxisSpacing:3,mainAxisSpacing:3,
        mainAxisExtent:((box.maxHeight-3*(rows-1))/rows).clamp(1.0,1000.0).toDouble()),
      itemBuilder:(_,index)=>children[index]);
  });
}
class Ngelx543MiniParticipant extends StatefulWidget{
  final lk.Participant participant;final bool local;
  const Ngelx543MiniParticipant({super.key,required this.participant,required this.local});
  @override State<Ngelx543MiniParticipant> createState()=>_Ngelx543MiniParticipantState();
}
class _Ngelx543MiniParticipantState extends State<Ngelx543MiniParticipant>{
  late final profile=FirebaseFirestore.instance.collection('users').doc(widget.participant.identity.toString()).get();
  @override Widget build(BuildContext context){
    final person=widget.participant;
    lk.VideoTrack? video;
    for(final publication in person.videoTrackPublications){
      if(!publication.muted&&publication.track is lk.VideoTrack){video=publication.track as lk.VideoTrack;break;}
    }
    final name=widget.local?'Sen':person.name.toString().trim().isEmpty?'Katılımcı':person.name.toString();
    return DecoratedBox(decoration:BoxDecoration(color:Colors.white10,borderRadius:BorderRadius.circular(7),
      border:Border.all(color:person.isSpeaking?const Color(0xFF24DB78):Colors.transparent,width:1.5)),child:ClipRRect(
      borderRadius:BorderRadius.circular(6),child:Column(children:[
        Expanded(child:video!=null?lk.VideoTrackRenderer(video,fit:lk.VideoViewFit.cover):FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          future:profile,builder:(_,snap){
            final photo=(snap.data?.data()?['photoUrl']??'').toString();
            return LayoutBuilder(builder:(_,box)=>Center(child:CircleAvatar(radius:(math.min(box.maxHeight,box.maxWidth)/2-2).clamp(5.0,60.0).toDouble(),
              backgroundColor:const Color(0xFF594078),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
              child:photo.isEmpty?const Icon(Icons.person,color:Colors.white,size:18):null)));
          })),
        Text(name,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:9)),
      ])));
  }
}

/// Root back exits to the launcher without destroying an ongoing call's engine.
/// Normal route back/minimize behavior stays inside each existing call page.
class Ngelx543ExitGuard extends StatelessWidget{
  final Widget child;
  const Ngelx543ExitGuard({super.key,required this.child});
  @override Widget build(BuildContext context)=>ValueListenableBuilder<int>(
    valueListenable:ngelx445CallRevision,builder:(_,revision,__)=>PopScope(
      canPop:Ngelx543PipCall.current==null||!ngelxCallSession444.background,
      onPopInvokedWithResult:(popped,_)async{
        if(popped||Ngelx543PipCall.current==null)return;
        final entered=await Ngelx543PipCall.background();
        if(!entered){try{await const MethodChannel('com.nnentx.ngelx_app/call_pip_520').invokeMethod<void>('home543');}catch(_){}}
      },child:child));
}
