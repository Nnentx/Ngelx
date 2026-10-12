part of 'main.dart';

final ngelx445CallRevision=ValueNotifier<int>(0);
bool _ngelx445CallFrameQueued=false;
void ngelx445CallChanged(){
  if(_ngelx445CallFrameQueued)return;
  _ngelx445CallFrameQueued=true;
  WidgetsBinding.instance.addPostFrameCallback((_){
    _ngelx445CallFrameQueued=false;
    ngelx445CallRevision.value++;
  });
  WidgetsBinding.instance.scheduleFrame();
}
final Map<String,({String title,String photo,String uid,bool video,DocumentReference<Map<String,dynamic>> ref})> ngelx445CallDetails={};

class Ngelx445FriendsStrip extends StatefulWidget{
  final String uid;
  const Ngelx445FriendsStrip({super.key,required this.uid});
  @override State<Ngelx445FriendsStrip> createState()=>_Ngelx445FriendsStripState();
}
class _Ngelx445FriendsStripState extends State<Ngelx445FriendsStrip>{
  late final _me=FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots();
  late final _stories=FirebaseFirestore.instance.collection('videos').where('type',isEqualTo:'story').limit(100).snapshots();
  final Map<String,Stream<DocumentSnapshot<Map<String,dynamic>>>> _profiles={};
  String? _opening;
  Future<void> _open(String id,Map<String,dynamic> profile)async{
    if(_opening!=null||FirebaseAuth.instance.currentUser?.uid!=widget.uid)return;
    if(id==widget.uid){await Navigator.push(context,MaterialPageRoute(builder:(_)=>const YuklePage()));return;}
    setState(()=>_opening=id);
    try{
      await ngelx445OpenPrivateChat(context,uid:id,ad:(profile['displayName']??profile['username']??'').toString(),foto:(profile['photoUrl']??'').toString());
    }finally{if(mounted)setState(()=>_opening=null);}
  }
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
    stream:_me,builder:(_,me){
      final data=me.data?.data()??<String,dynamic>{};
      final blocked=Set<String>.from(List<String>.from(data['blocked']??const[]));
      final friends=Set<String>.from(List<String>.from(data['friends']??const[]));
      final ids=<String>{widget.uid,...friends,...List<String>.from(data['following']??const[])}
        .where((id)=>id.isNotEmpty&&!blocked.contains(id)).take(40).toList();
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:_stories,builder:(_,stories){
        final owners=(stories.data?.docs??[]).where((d)=>ngelxHikayeAktif(d.data())&&d.data()['archived']!=true)
          .map((d)=>(d.data()['ownerId']??'').toString()).toSet();
        return SizedBox(height:108,child:ListView.builder(
          key:PageStorageKey('inbox-friends-'+widget.uid),scrollDirection:Axis.horizontal,
          padding:const EdgeInsets.symmetric(horizontal:12),itemExtent:66,itemCount:ids.length,
          itemBuilder:(_,index){
            final id=ids[index];
            final stream=_profiles.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('users').doc(id).snapshots());
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:stream,builder:(_,snap){
              final p=snap.data?.data()??(id==widget.uid?data:<String,dynamic>{});
              if(p['deactivated']==true||List<String>.from(p['blocked']??const[]).contains(widget.uid))return const SizedBox.shrink();
              final self=id==widget.uid,name=self?_ngelx438Ui('Sen'):(p['displayName']??p['username']??'').toString().split(' ').first;
              final photo=(p['photoUrl']??'').toString();
              final story=owners.contains(id)&&(self||p['friendsOnlyStory']==false||friends.contains(id));
              final noteExpiry=p['inboxNoteExpiresAt'];
              final note=noteExpiry is Timestamp&&noteExpiry.toDate().isAfter(DateTime.now())?(p['inboxNote']??'').toString():'';
              return Semantics(button:true,label:name,child:InkWell(
                borderRadius:BorderRadius.circular(18),onTap:_opening==null?()=>_open(id,p):null,
                child:Column(children:[
                  SizedBox(height:24,child:note.isEmpty?null:Align(alignment:Alignment.bottomCenter,child:Container(
                    padding:const EdgeInsets.symmetric(horizontal:5,vertical:3),
                    decoration:BoxDecoration(color:const Color(0xFFF4F0FC),borderRadius:BorderRadius.circular(12)),
                    child:Text(note,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:9)),
                  ))),
                  const SizedBox(height:3),
                  Stack(clipBehavior:Clip.none,children:[
                    Container(padding:const EdgeInsets.all(2),decoration:BoxDecoration(shape:BoxShape.circle,border:Border.all(color:story?mor:Colors.transparent,width:1.8)),
                      child:CircleAvatar(radius:23,backgroundColor:const Color(0xFFF1EDF9),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?const Icon(Icons.person_outline,color:mor):null)),
                    if(self)Positioned(right:0,bottom:0,child:Container(width:18,height:18,decoration:BoxDecoration(color:mor,shape:BoxShape.circle,border:Border.all(color:Colors.white,width:2)),child:const Icon(Icons.add,color:Colors.white,size:13))),
                    if(!self&&ngelx434Aktiflik(p)=='Çevrimiçi')Positioned(right:0,bottom:0,child:Ngelx436PresenceAccess(other:id,target:p,child:Container(width:13,height:13,decoration:BoxDecoration(color:const Color(0xFF28B76B),shape:BoxShape.circle,border:Border.all(color:Colors.white,width:2))))),
                  ]),
                  const SizedBox(height:4),
                  Text(name,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF101827),fontSize:11,fontWeight:FontWeight.w600)),
                ]),
              ));
            });
          },
        ));
      });
    });
}

Future<void> ngelx445ReturnCall(String name)async{
  final d=ngelx445CallDetails[name];
  if(d==null||!_ngelxArkaPlanAramaOdalari.containsKey(name)||FirebaseAuth.instance.currentUser?.uid!=d.uid)return;
  await ngelxNavigatorKey.currentState?.push(MaterialPageRoute(builder:(_)=>NgelXAramaPage(roomName:name,baslik:d.title,foto:d.photo,goruntulu:d.video,aramaRef:d.ref)));
}
Future<void> ngelx445EndBackground(String name)async{
  final detail=ngelx445CallDetails[name];
  final me=FirebaseAuth.instance.currentUser?.uid;
  await ngelxArkaPlanAramayiTemizle(name);
  if(detail==null||me!=detail.uid)return;
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final doc=await tx.get(detail.ref),v=doc.data()??<String,dynamic>{};
      if(FirebaseAuth.instance.currentUser?.uid!=me||v['callRoomName']!=name||!['ringing','active'].contains(v['callStatus']))return;
      final participants=List<String>.from(v['callParticipants']??const[]).where((x)=>x!=me).toList();
      final ended=!name.startsWith('group_')||v['callStartedBy']==me||participants.isEmpty;
      tx.set(detail.ref,{'callParticipants':FieldValue.arrayRemove([me]),if(ended)'callStatus':'ended',if(ended)'callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      final id=(v['callMessageId']??'').toString();
      if(ended&&id.isNotEmpty)tx.set(detail.ref.collection('messages').doc(id),{'callStatus':'ended','callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    }).timeout(const Duration(seconds:8));
  }catch(_){}
}
class Ngelx445CallOverlay extends StatefulWidget{
  const Ngelx445CallOverlay({super.key});
  @override State<Ngelx445CallOverlay> createState()=>_Ngelx445CallOverlayState();
}
class _Ngelx445CallOverlayState extends State<Ngelx445CallOverlay>{
  Timer? _tick;StreamSubscription<User?>? _auth;
  double? _left,_top;
  @override void initState(){super.initState();
    _tick=Timer.periodic(const Duration(seconds:1),(_){
      if(mounted&&_ngelxArkaPlanAramaOdalari.isNotEmpty)setState((){});
      if(DateTime.now().second%30==0){
        final name=ngelxCallSession444.room,detail=ngelx445CallDetails[name];
        if(name!=null&&detail!=null&&ngelxCallSession444.background&&FirebaseAuth.instance.currentUser?.uid==detail.uid){
          unawaited(FirebaseFirestore.instance.runTransaction((tx)async{
            final d=await tx.get(detail.ref);
            if(FirebaseAuth.instance.currentUser?.uid==detail.uid&&_ngelxArkaPlanAramaOdalari.containsKey(name)&&d.data()?['callRoomName']==name&&d.data()?['callStatus']=='active'){
              tx.set(detail.ref,{'callHeartbeatAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
            }
          }).timeout(const Duration(seconds:8)).catchError((_){ }));
        }
      }
    });
    _auth=FirebaseAuth.instance.authStateChanges().listen((user){
      for(final e in ngelx445CallDetails.entries.toList()){
        if(user?.uid!=e.value.uid)unawaited(ngelxArkaPlanAramayiTemizle(e.key));
      }
    });
  }
  @override void dispose(){_tick?.cancel();_auth?.cancel();super.dispose();}
  @override Widget build(BuildContext context)=>ValueListenableBuilder<int>(valueListenable:ngelx445CallRevision,builder:(_,rev,__){
    final name=ngelxCallSession444.room,detail=ngelx445CallDetails[name];
    final room=_ngelxArkaPlanAramaOdalari[name];
    if(name==null||detail==null||room==null||!ngelxCallSession444.background||FirebaseAuth.instance.currentUser?.uid!=detail.uid)return const SizedBox.shrink();
    final screen=MediaQuery.sizeOf(context),padding=MediaQuery.paddingOf(context);
    final start=_ngelxArkaPlanAramaBaslangiclari[name];
    final seconds=start==null?null:DateTime.now().difference(start).inSeconds.clamp(0,359999);
    final duration=seconds==null?_ngelx438Ui('Aranıyor…'):'${(seconds~/60).toString().padLeft(2,'0')}:${(seconds%60).toString().padLeft(2,'0')}';
    final x=(_left??screen.width-128).clamp(8.0,(screen.width-120).clamp(8.0,double.infinity)).toDouble();
    final y=(_top??screen.height-padding.bottom-224).clamp(padding.top+56,(screen.height-padding.bottom-180).clamp(padding.top+56,double.infinity)).toDouble();
    return Positioned(left:x,top:y,width:112,child:Material(color:Colors.transparent,child:GestureDetector(
      onPanUpdate:(delta)=>setState((){_left=x+delta.delta.dx;_top=y+delta.delta.dy;}),
      child:Container(padding:const EdgeInsets.all(10),decoration:BoxDecoration(color:const Color(0xFF39206F),borderRadius:BorderRadius.circular(18),boxShadow:const[BoxShadow(color:Color(0x33000000),blurRadius:15)]),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          InkWell(onTap:()=>ngelx445ReturnCall(name),child:Column(children:[
            Text(detail.title,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
            const SizedBox(height:7),
            CircleAvatar(radius:20,backgroundColor:const Color(0xFF6F4AB2),backgroundImage:detail.photo.isEmpty?null:NgelXAgImageProvider(detail.photo),child:detail.photo.isEmpty?Icon(detail.video?Icons.videocam:Icons.call,color:Colors.white,size:20):null),
            const SizedBox(height:7),Text(duration,style:const TextStyle(color:Colors.white,fontSize:11)),
          ])),
          Ngelx445CallControls(
            microphone:room.localParticipant?.isMicrophoneEnabled()==true,
            speaker:lk.AudioManager.instance.isSpeakerOutputPreferred,
            onMicrophone:()async{
              final local=room.localParticipant;if(local==null)return;
              try{await local.setMicrophoneEnabled(!local.isMicrophoneEnabled());if(mounted)setState((){});}catch(_){}
            },
            onSpeaker:()async{try{await lk.AudioManager.instance.setSpeakerOutputPreferred(!lk.AudioManager.instance.isSpeakerOutputPreferred);if(mounted)setState((){});}catch(_){} },
            onEnd:()=>ngelx445EndBackground(name),
          ),
        ]),
      ),
    )));
  });
}
class Ngelx445InboxCallBanner extends StatelessWidget{
  const Ngelx445InboxCallBanner({super.key});
  @override Widget build(BuildContext context)=>ValueListenableBuilder<int>(valueListenable:ngelx445CallRevision,builder:(_,rev,__){
    final name=ngelxCallSession444.room,detail=ngelx445CallDetails[name];
    if(name==null||detail==null||!_ngelxArkaPlanAramaOdalari.containsKey(name)||detail.uid!=FirebaseAuth.instance.currentUser?.uid)return const SizedBox.shrink();
    return Padding(padding:const EdgeInsets.fromLTRB(16,2,16,6),child:Material(color:mor,borderRadius:BorderRadius.circular(18),child:InkWell(
      borderRadius:BorderRadius.circular(18),onTap:()=>ngelx445ReturnCall(name),child:Padding(padding:const EdgeInsets.all(12),child:Row(children:[
        Icon(detail.video?Icons.videocam:Icons.call,color:Colors.white,size:23),const SizedBox(width:12),
        Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(detail.title,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),Text(_ngelx438Ui('Aramaya dönmek için dokun'),style:const TextStyle(color:Colors.white70,fontSize:11))])),
        const Icon(Icons.chevron_right,color:Colors.white),
      ])),
    )));
  });
}

Future<void> ngelx445OpenCallChat(BuildContext context,Map<String,dynamic> v)async{
  final me=FirebaseAuth.instance.currentUser?.uid;
  final source=(v['sourceId']??v['chatId']??v['belgeId']??'').toString();
  if(me==null||source.isEmpty)return;
  try{
    final chat=await FirebaseFirestore.instance.collection('chats').doc(source).get().timeout(const Duration(seconds:8));
    final data=chat.data()??<String,dynamic>{};
    final group=data['isGroup']==true;
    final members=List<String>.from(data['members']??const[]);
    final former=List<String>.from(data['formerMembers']??const[]);
    if((!members.contains(me)&&!(group&&former.contains(me)))||List<String>.from(data['hiddenFor']??const[]).contains(me))return;
    if(group){
      if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:source,ad:(data['groupName']??v['targetTitle']??'').toString(),foto:(data['groupPhotoUrl']??'').toString())));
    }else{
      final other=members.firstWhere((x)=>x!=me,orElse:()=> '');if(other.isEmpty)return;
      final user=await FirebaseFirestore.instance.collection('users').doc(other).get().timeout(const Duration(seconds:8));
      final profile=user.data()??<String,dynamic>{};
      if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:source,digerUid:other,ad:(profile['displayName']??profile['username']??'').toString(),foto:(profile['photoUrl']??'').toString())));
    }
  }catch(_){if(context.mounted)ngelxDurumMesaji(context,lt('Sohbet açılamadı. Tekrar dene.','Could not open chat. Try again.'),tip:'hata');}
}

Widget ngelx445CallTrailing(Map<String,dynamic> chat,Widget usual)=>ValueListenableBuilder<int>(
  valueListenable:ngelx445CallRevision,builder:(_,revision,__){
    final name=(chat['callRoomName']??'').toString();
    final detail=ngelx445CallDetails[name];
    if(name.isEmpty||ngelxCallSession444.room!=name||!ngelxCallSession444.background||detail?.uid!=FirebaseAuth.instance.currentUser?.uid)return usual;
    return SizedBox(width:104,child:TextButton(
      style:TextButton.styleFrom(backgroundColor:const Color(0xFF25B85E),foregroundColor:Colors.white,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(20)),padding:const EdgeInsets.symmetric(horizontal:10,vertical:9)),
      onPressed:()=>ngelx445ReturnCall(name),
      child:FittedBox(fit:BoxFit.scaleDown,child:Text(_ngelx438Ui('Aramaya dön'),style:const TextStyle(fontSize:11,fontWeight:FontWeight.w800))),
    ));
  });

/// Exact compact layout, independent of platform IconButton minimum tap padding.
class Ngelx445CallControls extends StatelessWidget{
  final bool microphone,speaker;
  final VoidCallback onMicrophone,onSpeaker,onEnd;
  const Ngelx445CallControls({super.key,required this.microphone,required this.speaker,required this.onMicrophone,required this.onSpeaker,required this.onEnd});
  Widget _control(String label,IconData icon,VoidCallback action,{bool end=false})=>Tooltip(message:label,child:Semantics(label:label,button:true,child:InkWell(
    onTap:action,borderRadius:BorderRadius.circular(18),
    child:SizedBox(width:28,height:32,child:Center(child:Container(
      width:28,height:28,decoration:end?const BoxDecoration(color:Color(0xFFFF414A),shape:BoxShape.circle):null,
      child:Icon(icon,color:Colors.white,size:18),
    ))),
  )));
  @override Widget build(BuildContext context)=>Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
    _control(_ngelx438Ui('Mikrofon'),microphone?Icons.mic:Icons.mic_off,onMicrophone),
    _control(_ngelx438Ui('Hoparlör'),speaker?Icons.volume_up:Icons.volume_off,onSpeaker),
    _control(_ngelx438Ui('Aramayı bitir'),Icons.call_end,onEnd,end:true),
  ]);
}
