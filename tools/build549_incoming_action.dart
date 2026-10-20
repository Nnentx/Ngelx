  Future<void> _action(Map<String,dynamic> args)async{
    final chat=(args['chat']??'').toString(),room=(args['room']??'').toString(),action=args['action'];
    if(action=='resume'){await ngelx446Calls.returnTo454();return;}
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null||chat.isEmpty||room.isEmpty||_handling==room)return;
    if(action=='open'){await ngelx454OpenIncoming(chat,room);return;}
    if(action!='answer'&&action!='reject')return;
    _handling=room;await _stop();
    try{await channel.invokeMethod<void>('cancel',{'room':room});}catch(_){}
    var reserved=false;
    try{
      if(ngelxCallSession444.room==room&&ngelxCallSession444.busy){
        await ngelx446Calls.returnTo454();return;
      }
      final ref=FirebaseFirestore.instance.collection('chats').doc(chat);
      final doc=await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
      if(FirebaseAuth.instance.currentUser?.uid!=me)return;
      final v=doc.data()??<String,dynamic>{};
      bool eligible(Map<String,dynamic> data){
        final stamp=data['callCreatedAt'];
        return ngelx549CanAnswer(sameRoom:data['callRoomName']==room,
          member:List<String>.from(data['members']??const[]).contains(me),
          group:data['isGroup']==true,status:(data['callStatus']??'').toString(),
          ageSeconds:stamp is Timestamp?DateTime.now().difference(stamp.toDate()).inSeconds:-1,
          kicked:data['callModerationRoom']==room&&List<String>.from(data['callKickedUids']??const[]).contains(me),
          exited:data['callExitedRoomName']==room&&List<String>.from(data['callExitedUids']??const[]).contains(me));
      }
      if(!eligible(v))throw StateError('call_invitation_unavailable');
      if(action=='reject'&&v['isGroup']==true){
        // Declining one group invite must never end everybody else's call.
        _dismissed549.add(room);
        if(_dismissed549.length>100)_dismissed549.remove(_dismissed549.first);
        return;
      }
      if(action=='answer'){
        final context=ngelxNavigatorKey.currentContext;
        if(context==null||!context.mounted||!ngelx444ReserveCall(context,room))return;
        reserved=true;
        if(v['isGroup']==true&&!await ngelx542PrepareManualJoin(room,me)){
          throw ngelx549LastLeaveError??StateError('pending_leave');
        }
      }
      await FirebaseFirestore.instance.runTransaction((tx)async{
        final s=await tx.get(ref),current=s.data()??<String,dynamic>{};
        if(FirebaseAuth.instance.currentUser?.uid!=me||!eligible(current))throw StateError('call_invitation_unavailable');
        if(action=='reject'){
          tx.update(ref,{'callStatus':'rejected','callEndedBy':me,'callEndedAt':FieldValue.serverTimestamp()});
        }else{
          tx.update(ref,{'callStatus':'active','callParticipants':FieldValue.arrayUnion([me]),'callAnsweredAt':FieldValue.serverTimestamp()});
        }
      },maxAttempts:2).timeout(const Duration(seconds:10));
      if(action!='answer'||FirebaseAuth.instance.currentUser?.uid!=me)return;
      final context=ngelxNavigatorKey.currentContext;
      if(context==null||!context.mounted)return;
      await Navigator.of(context).push(MaterialPageRoute(builder:(_)=>NgelXAramaPage(
        roomName:room,baslik:(v['callTitle']??v['groupName']??'NgelX araması').toString(),
        foto:(v['groupPhotoUrl']??'').toString(),goruntulu:v['callVideo']==true,aramaRef:ref)));
    }catch(error){
      if(FirebaseAuth.instance.currentUser?.uid==me)ngelx549CallNotice(error);
    }finally{
      if(reserved)ngelxCallSession444.releasePending(room);
      _handling=null;
    }
  }
