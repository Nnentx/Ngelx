part of 'main.dart';

class Ngelx448IncomingCalls {
  static const channel=MethodChannel('com.nnentx.ngelx_app/incoming');
  StreamSubscription<User?>? _auth;
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _calls;
  String? _ringing,_handling;
  bool _started=false;
  int _epoch448=0;
  void start(){
    if(_started||kIsWeb||defaultTargetPlatform!=TargetPlatform.android)return;_started=true;
    channel.setMethodCallHandler((call)async{if(call.method=='callAction')await _action(Map<String,dynamic>.from(call.arguments as Map));});
    _auth=FirebaseAuth.instance.authStateChanges().listen((user)async{
      await _calls?.cancel();_calls=null;await _stop();
      if(user==null||user.isAnonymous)return;
      try{
        await Permission.notification.request();
        final token=await channel.invokeMethod<String>('getPushToken');
        if(token!=null&&token.isNotEmpty&&FirebaseAuth.instance.currentUser?.uid==user.uid){
          await FirebaseFirestore.instance.collection('_call_devices').doc(user.uid).collection('tokens').doc(token.hashCode.toUnsigned(32).toString()).set({'token':token,'uid':user.uid,'updatedAt':FieldValue.serverTimestamp()});
        }
      }catch(_){}
      if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
      _calls=FirebaseFirestore.instance.collection('chats').where('members',arrayContains:user.uid).limit(100).snapshots().listen((s){
        final active=s.docs.where((d){final v=d.data(),t=v['callCreatedAt'];return v['callStartedBy']!=user.uid&&v['callStatus']=='ringing'&&t is Timestamp&&DateTime.now().difference(t.toDate()).inSeconds<60;}).toList();
        if(active.isEmpty){unawaited(_stop());return;}
        final d=active.first,v=d.data(),room=(v['callRoomName']??'').toString();
        if(room.isEmpty||ngelxCallSession444.busy||_media448!=null){unawaited(_stop());return;}
        if(_ringing==room)return;
        unawaited(_ring(d.id,room,(v['callTitle']??v['groupName']??'NgelX araması').toString(),v['callVideo']==true,caller:v['isGroup']==true?'':(v['callStartedBy']??'').toString()));
      });
      try{final pending=await channel.invokeMapMethod<String,dynamic>('pendingAction');if(pending!=null)await _action(pending);}catch(_){}
    });
  }
  Future<void> _stop({bool invalidate=true})async{
    if(invalidate)_epoch448++;
    final room=_ringing;_ringing=null;
    if(room!=null){try{await channel.invokeMethod<void>('cancel',{'room':room});}catch(_){} }
  }
  Future<void> _ring(String chat,String room,String title,bool video,{String caller=''})async{
    final epoch=++_epoch448;await _stop(invalidate:false);if(epoch!=_epoch448)return;_ringing=room;
    if(caller.isNotEmpty){try{final p=await FirebaseFirestore.instance.collection('users').doc(caller).get().timeout(const Duration(seconds:2));title=(p.data()?['displayName']??p.data()?['username']??title).toString();}catch(_){} }
    if(epoch!=_epoch448)return;
    try{await channel.invokeMethod<void>('show',{'chat':chat,'room':room,'title':title,'video':video});}catch(_){}
    Future<void>.delayed(const Duration(seconds:60),(){if(_ringing==room)unawaited(_stop());});
  }
  Future<void> _action(Map<String,dynamic> args)async{
    final chat=(args['chat']??'').toString(),room=(args['room']??'').toString(),action=args['action'];
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null||chat.isEmpty||room.isEmpty||_handling==room)return;
    _handling=room;await _stop();
    try{
      final ref=FirebaseFirestore.instance.collection('chats').doc(chat),d=await ref.get();
      final v=d.data()??<String,dynamic>{},t=v['callCreatedAt'];
      if(v['callRoomName']!=room||v['callStatus']!='ringing'||!List<String>.from(v['members']??const[]).contains(me)||t is! Timestamp||DateTime.now().difference(t.toDate()).inSeconds>60)return;
      if(action=='reject'){await ref.set({'callStatus':'rejected','callEndedBy':me,'callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));return;}
      if(action!='answer')return;
      final context=ngelxNavigatorKey.currentContext;if(context==null||!ngelx444ReserveCall(context,room))return;
      try{
        await FirebaseFirestore.instance.runTransaction((tx)async{final s=await tx.get(ref);if(s.data()?['callRoomName']!=room||s.data()?['callStatus']!='ringing')throw StateError('expired');tx.update(ref,{'callStatus':'active','callParticipants':FieldValue.arrayUnion([me]),'callAnsweredAt':FieldValue.serverTimestamp()});});
        if(!context.mounted)return;
        await Navigator.of(context).push(MaterialPageRoute(builder:(_)=>NgelXAramaPage(roomName:room,baslik:(v['callTitle']??v['groupName']??'NgelX araması').toString(),foto:(v['groupPhotoUrl']??'').toString(),goruntulu:v['callVideo']==true,aramaRef:ref)));
      }finally{ngelxCallSession444.releasePending(room);}
    }catch(_){}finally{_handling=null;}
  }
}
final ngelx448Incoming=Ngelx448IncomingCalls();
