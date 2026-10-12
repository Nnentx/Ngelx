part of 'main.dart';

final ngelx446Calls=Ngelx446CallLifecycle();
class _Call446 {
  final lk.Room room;
  final DocumentReference<Map<String,dynamic>> ref;
  bool hidden=false,restoreCamera=false,muted=false;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? subscription;
  _Call446(this.room,this.ref);
}
class Ngelx446CallLifecycle with WidgetsBindingObserver {
  final Map<String,_Call446> _calls={};
  Future<void> _serial=Future.value();
  bool _observing=false,_foreground=true;
  static const _native=MethodChannel('com.nnentx.ngelx_app/call');
  bool muted(String name)=>_calls[name]?.muted==true;
  Future<void> _enqueue(Future<void> Function() operation){
    final next=_serial.then((_)=>operation());
    _serial=next.catchError((Object e){debugPrint('call lifecycle: $e');});
    return next;
  }
  Future<void> attach(String name,lk.Room room,DocumentReference<Map<String,dynamic>> ref,{bool cameraWanted=false})async{
    if(!_observing){WidgetsBinding.instance.addObserver(this);_observing=true;}
    _foreground=WidgetsBinding.instance.lifecycleState==null||WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed;
    final current=await ref.get().timeout(const Duration(seconds:6));
    final data=current.data()??<String,dynamic>{};
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(data['callModerationRoom']==name&&List<String>.from(data['callKickedUids']??const[]).contains(me))throw StateError('Bu görüşmeden çıkarıldın.');
    await _calls.remove(name)?.subscription?.cancel();
    final entry=_Call446(room,ref)..restoreCamera=cameraWanted&&!_foreground;
    entry.muted=data['callModerationRoom']==name&&List<String>.from(data['callMutedUids']??const[]).contains(me);
    _calls[name]=entry;
    entry.subscription=ref.snapshots().listen((snapshot){
      final v=snapshot.data()??<String,dynamic>{};
      if(v['callRoomName']!=name)return;
      final me=FirebaseAuth.instance.currentUser?.uid;
      entry.muted=v['callModerationRoom']==name&&List<String>.from(v['callMutedUids']??const[]).contains(me);
      if(entry.muted)unawaited(_enqueue(()async{await room.localParticipant?.setMicrophoneEnabled(false);}));
      if(v['callModerationRoom']==name&&List<String>.from(v['callKickedUids']??const[]).contains(me)){
        unawaited(_enqueue(()async{
          await detach(room);await room.disconnect();
          if(_ngelxArkaPlanAramaOdalari.containsKey(name))await ngelxArkaPlanAramayiTemizle(name);
        }));
      }
    });
    if(!kIsWeb&&defaultTargetPlatform==TargetPlatform.android){
      await _native.invokeMethod<void>('start');
    }
  }
  Future<void> detach(lk.Room room)async{
    final names=_calls.entries.where((e)=>identical(e.value.room,room)).map((e)=>e.key).toList();
    for(final name in names){await _calls.remove(name)?.subscription?.cancel();}
    if(_calls.isEmpty&&defaultTargetPlatform==TargetPlatform.android){try{await _native.invokeMethod<void>('stop');}catch(_){} }
  }
  Future<void> _camera(_Call446 entry,bool visible)async{
    final local=entry.room.localParticipant;if(local==null)return;
    if(!visible){
      if(local.isCameraEnabled()){entry.restoreCamera=true;await local.setCameraEnabled(false);}
    }else if(entry.restoreCamera){
      await local.setCameraEnabled(true,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      entry.restoreCamera=false;
    }
  }
  Future<void> hide(String name)=>_enqueue(()async{
    final entry=_calls[name];if(entry==null)return;entry.hidden=true;await _camera(entry,false);
  });
  Future<void> show(String name)=>_enqueue(()async{
    final entry=_calls[name];if(entry==null)return;entry.hidden=false;await _camera(entry,_foreground);
  });
  @override void didChangeAppLifecycleState(AppLifecycleState state){
    _foreground=state==AppLifecycleState.resumed;
    final foreground=_foreground;
    unawaited(_enqueue(()async{
      for(final entry in _calls.values.toList()){
        await _camera(entry,foreground&&!entry.hidden);
        final local=entry.room.localParticipant;
        // Restart only an intentionally enabled mic; never undo a manual/admin mute.
        if(foreground&&!entry.muted&&local?.isMicrophoneEnabled()==true){
          final speaker=lk.AudioManager.instance.isSpeakerOutputPreferred;
          await local!.setMicrophoneEnabled(false);await local.setMicrophoneEnabled(true);
          await lk.AudioManager.instance.setSpeakerOutputPreferred(speaker);
        }
      }
    }).catchError((Object e){debugPrint('call resume: $e');}));
  }
}

Future<void> ngelx446MuteMenu(BuildContext context,DocumentReference<Map<String,dynamic>> ref,String name,String target)async{
  final me=FirebaseAuth.instance.currentUser?.uid;
  if(me==null||target==me||!name.startsWith('group_'))return;
  try{
    final d=await ref.get(),v=d.data()??<String,dynamic>{};
    final owner=v['createdBy'];
    if(owner!=me&&!List<String>.from(v['admins']??const[]).contains(me))return;
    if(owner==target||v['callRoomName']!=name||!context.mounted)return;
    final isMuted=v['callModerationRoom']==name&&List<String>.from(v['callMutedUids']??const[]).contains(target);
    final action=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      ListTile(leading:const Icon(Icons.more_horiz),title:const Text('Katılımcı işlemleri')),
      ListTile(leading:Icon(isMuted?Icons.mic:Icons.mic_off),title:Text(isMuted?'Mikrofon iznini geri ver':'Mikrofonunu sustur'),onTap:()=>Navigator.pop(c,isMuted?'allow':'mute')),
      ListTile(leading:const Icon(Icons.call_end,color:Colors.red),title:const Text('Sesli görüşmeden çıkar'),subtitle:const Text('Grup üyeliği devam eder'),onTap:()=>Navigator.pop(c,'kick')),
    ])));
    if(action==null)return;
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final current=await tx.get(ref),data=current.data()??<String,dynamic>{};
      if(data['callRoomName']!=name||data['createdBy']==target||
         (data['createdBy']!=me&&!List<String>.from(data['admins']??const[]).contains(me)))throw StateError('İşlem yetkisi değişti.');
      final sameRoom=data['callModerationRoom']==name;
      tx.update(ref,{
        'callModerationRoom':name,
        if(action=='kick')'callKickedUids':sameRoom?FieldValue.arrayUnion([target]):[target],
        if(!sameRoom&&action!='kick')'callKickedUids':<String>[],
        if(action=='kick')'callParticipants':FieldValue.arrayRemove([target]),
        if(action=='mute')'callMutedUids':sameRoom?FieldValue.arrayUnion([target]):[target],
        if(!sameRoom&&action!='mute')'callMutedUids':<String>[],
        if(action=='allow')'callMutedUids':FieldValue.arrayRemove([target]),
      });
    });
  }catch(_){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Katılımcı işlemi tamamlanamadı.')));}
}

class Ngelx446SpeakingRing extends StatefulWidget {
  final lk.Participant participant;
  final Widget child;
  const Ngelx446SpeakingRing({super.key,required this.participant,required this.child});
  @override State<Ngelx446SpeakingRing> createState()=>_Ngelx446SpeakingRingState();
}
class _Ngelx446SpeakingRingState extends State<Ngelx446SpeakingRing> with SingleTickerProviderStateMixin {
  late final AnimationController _pulse;
  void _changed(){
    if(widget.participant.isSpeaking){if(!_pulse.isAnimating)_pulse.repeat(reverse:true);}
    else{_pulse.stop();_pulse.value=0;}
    if(mounted)setState((){});
  }
  @override void initState(){super.initState();_pulse=AnimationController(vsync:this,duration:const Duration(milliseconds:650));widget.participant.addListener(_changed);_changed();}
  @override void didUpdateWidget(covariant Ngelx446SpeakingRing old){super.didUpdateWidget(old);if(!identical(old.participant,widget.participant)){old.participant.removeListener(_changed);widget.participant.addListener(_changed);_changed();}}
  @override void dispose(){widget.participant.removeListener(_changed);_pulse.dispose();super.dispose();}
  @override Widget build(BuildContext context)=>AnimatedBuilder(animation:_pulse,child:widget.child,builder:(_,child){
    final speaking=widget.participant.isSpeaking;
    return Container(padding:const EdgeInsets.all(5),decoration:BoxDecoration(shape:BoxShape.circle,
      border:Border.all(color:speaking?const Color(0xFF2AE879):Colors.transparent,width:3),
      boxShadow:speaking?[BoxShadow(color:const Color(0xFF2AE879).withValues(alpha:.15+.25*_pulse.value),blurRadius:8+12*_pulse.value,spreadRadius:1+3*_pulse.value)]:null),child:child);
  });
}
