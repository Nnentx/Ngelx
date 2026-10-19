part of 'main.dart';

// Each host only attests its own room. The peer connection is subscribe-only;
// microphones keep their original room and their existing consent/role state.
class Ngelx541AudioPk extends StatefulWidget {
  final String roomId,ownerUid;
  final bool ended;
  const Ngelx541AudioPk({super.key,required this.roomId,required this.ownerUid,required this.ended});
  @override State<Ngelx541AudioPk> createState()=>_Ngelx541AudioPkState();
}
class _Ngelx541AudioPkState extends State<Ngelx541AudioPk> {
  final _db=FirebaseFirestore.instance;
  Timer? _timer;
  StreamSubscription<User?>? _auth;
  lk.Room? _peer;
  String? _peerName,_sessionUid;
  String _message='';
  bool _syncing=false,_busy=false,_disposed=false,_picking=false;
  int _generation=0;
  DateTime _retry=DateTime.fromMillisecondsSinceEpoch(0);
  Map<String,dynamic> _own={},_request={};
  String? _requestId;
  bool get _host=>FirebaseAuth.instance.currentUser?.uid==widget.ownerUid;
  DocumentReference<Map<String,dynamic>> get _ref=>_db.collection('audio_rooms').doc(widget.roomId);
  @override void initState(){
    super.initState();_sessionUid=FirebaseAuth.instance.currentUser?.uid;
    _auth=FirebaseAuth.instance.authStateChanges().listen((u){if(u?.uid!=_sessionUid){_timer?.cancel();unawaited(_drop());}});
    _timer=Timer.periodic(const Duration(seconds:3),(_)=>unawaited(_sync()));
    unawaited(_sync());
  }
  Future<void> _drop()async{
    _generation++;final room=_peer;_peer=null;_peerName=null;
    if(room!=null){try{await room.disconnect();}catch(_){}try{await room.dispose();}catch(_){}}
  }
  bool _active(Map<String,dynamic> v)=>v['active']==true&&v['visibility']=='public'&&ngelxSesliOdaTaze(v);
  bool _validEnd(dynamic v)=>v is Timestamp&&v.toDate().isAfter(DateTime.now())&&v.toDate().difference(DateTime.now()).inSeconds<=190;
  Ngelx541PkRoom _policyRoom(String id,Map<String,dynamic> v)=>Ngelx541PkRoom(id:id,owner:(v['ownerId']??'').toString(),publicAndFresh:_active(v),active:v['pkActive']==true,session:(v['pkSessionId']??'').toString(),peer:(v['pkOpponentRoomId']??'').toString(),endsAt:v['pkEndsAt'] is Timestamp?(v['pkEndsAt'] as Timestamp).millisecondsSinceEpoch:0);
  Map<String,dynamic> _clear()=>{'pkActive':false,'pkSessionId':FieldValue.delete(),'pkOpponentRoomId':FieldValue.delete(),'pkEndsAt':FieldValue.delete(),'pkStartedAt':FieldValue.delete()};
  Future<void> _stop()async{
    if(!_host||_busy)return;setState(()=>_busy=true);
    try{
      final own=(await _ref.get(const GetOptions(source:Source.server))).data()??{};
      final id=(own['pkSessionId']??'').toString();
      await _ref.update(_clear());
      if(id.isNotEmpty)await _db.collection('calls').doc(id).update({'status':'ended','endedAt':FieldValue.serverTimestamp()});
      await _drop();
    }catch(_){if(mounted)setState(()=>_message='PK bitişi doğrulanamadı. Tekrar dene.');}
    finally{if(mounted)setState(()=>_busy=false);}
    await _sync();
  }
  Future<void> _sync()async{
    if(_syncing||_disposed||FirebaseAuth.instance.currentUser?.uid!=_sessionUid)return;
    _syncing=true;
    try{
      final own=(await _ref.get(const GetOptions(source:Source.server))).data()??<String,dynamic>{};
      if(_disposed)return;
      _own=own;
      if(widget.ended||!_active(own)){await _drop();if(mounted)setState((){});return;}
      if(_host&&own['pkActive']==true&&!_validEnd(own['pkEndsAt'])){
        await _ref.update(_clear());await _drop();return;
      }
      // Read only this account's invitations. Viewers never read host call docs.
      if(_host){
        final q=await _db.collection('calls').where('members',arrayContains:_sessionUid).get(const GetOptions(source:Source.server));
        final candidates=q.docs.where((d){final v=d.data();return v['type']=='audio_pk'&&
          (v['inviterRoomId']==widget.roomId||v['inviteeRoomId']==widget.roomId)&&
          ((v['status']=='pending'&&v['requestExpiresAt'] is Timestamp&&(v['requestExpiresAt'] as Timestamp).toDate().isAfter(DateTime.now()))||v['status']=='accepted');}).toList();
        candidates.sort((a,b){final x=a.data()['createdAt'],y=b.data()['createdAt'];return (y is Timestamp?y.millisecondsSinceEpoch:0).compareTo(x is Timestamp?x.millisecondsSinceEpoch:0);});
        _requestId=candidates.isEmpty?null:candidates.first.id;
        _request=candidates.isEmpty?{}:candidates.first.data();
        if(_request['status']=='accepted'&&_request['startedBy']==_sessionUid&&own['pkActive']!=true&&_validEnd(_request['pkEndsAt'])){
          final id=_requestId!,target=(_request['inviteeRoomId']??'').toString();
          await _db.runTransaction((tx)async{
            final me=(await tx.get(_ref)).data()??{};
            final call=(await tx.get(_db.collection('calls').doc(id))).data()??{};
            final other=(await tx.get(_db.collection('audio_rooms').doc(target))).data()??{};
            if(me['ownerId']!=_sessionUid||me['pkActive']==true||!_active(me)||!_active(other)||call['status']!='accepted'||call['startedBy']!=_sessionUid||other['ownerId']!=call['inviteeUid']||other['pkSessionId']!=id||other['pkOpponentRoomId']!=widget.roomId||!_validEnd(call['pkEndsAt']))return;
            tx.update(_ref,{'pkActive':true,'pkSessionId':id,'pkOpponentRoomId':target,'pkEndsAt':call['pkEndsAt'],'pkStartedAt':call['pkStartedAt']});
          });
          return;
        }
      }
      final id=(own['pkSessionId']??'').toString(),target=(own['pkOpponentRoomId']??'').toString();
      if(own['pkActive']!=true||id.isEmpty||target.isEmpty||!_validEnd(own['pkEndsAt'])){await _drop();if(mounted)setState((){});return;}
      final other=(await _db.collection('audio_rooms').doc(target).get(const GetOptions(source:Source.server))).data()??{};
      final mutual=ngelx541PkMutual(_policyRoom(widget.roomId,own),_policyRoom(target,other),DateTime.now().millisecondsSinceEpoch);
      if(!mutual){
        await _drop();_message='Karşı yayıncı bağlantısı bekleniyor';
        final start=own['pkStartedAt'];
        if(_host&&start is Timestamp&&DateTime.now().difference(start.toDate()).inSeconds>15){
          await _ref.update(_clear());
          try{await _db.collection('calls').doc(id).update({'status':'ended','endReason':'peer_left'});}catch(_){}
          _message='PK sona erdi';
        }
        if(mounted)setState((){});return;
      }
      if(_peerName!=other['roomName']&&DateTime.now().isAfter(_retry)){
        await _drop();final generation=_generation;
        final roomName=(other['roomName']??'').toString();if(roomName.isEmpty)return;
        _retry=DateTime.now().add(const Duration(seconds:15));
        final token=await NgelXLiveKitSource441().fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:_sessionUid!,participantName:'NgelX',participantAttributes:{'mode':'audio','role':'listener'})).timeout(const Duration(seconds:12));
        final room=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
        try{
          await room.connect(token.serverUrl,token.participantToken).timeout(const Duration(seconds:18));
          await room.localParticipant?.setMicrophoneEnabled(false);
          if(_disposed||generation!=_generation||FirebaseAuth.instance.currentUser?.uid!=_sessionUid){await room.disconnect();await room.dispose();return;}
          _peer=room;_peerName=roomName;_message='Karşı odanın sesi bağlı';
        }catch(_){try{await room.disconnect();await room.dispose();}catch(_){}rethrow;}
      }
      if(mounted)setState((){});
    }catch(_){if(mounted)setState(()=>_message='PK bağlantısı doğrulanamadı; tekrar denenecek.');}
    finally{_syncing=false;}
  }
  Future<void> _respond(String status)async{
    final id=_requestId;if(!_host||id==null||_busy)return;setState(()=>_busy=true);
    try{
      await _db.runTransaction((tx)async{
        final ref=_db.collection('calls').doc(id),call=(await tx.get(ref)).data()??{};
        final me=(await tx.get(_ref)).data()??{};
        final target=(call['inviterRoomId']??'').toString();
        if(target.isEmpty)throw StateError('missing');
        final other=(await tx.get(_db.collection('audio_rooms').doc(target))).data()??{};
        if(call['type']!='audio_pk'||!ngelx541PkCanAccept(own:_policyRoom(widget.roomId,me),other:_policyRoom(target,other),uid:_sessionUid??'',inviterUid:(call['startedBy']??'').toString(),inviteeUid:(call['inviteeUid']??'').toString(),inviterRoom:target,inviteeRoom:(call['inviteeRoomId']??'').toString(),status:(call['status']??'').toString(),expiresAt:call['requestExpiresAt'] is Timestamp?(call['requestExpiresAt'] as Timestamp).millisecondsSinceEpoch:0,now:DateTime.now().millisecondsSinceEpoch))throw StateError('expired');
        if(status=='accepted'){
          final end=Timestamp.fromDate(DateTime.now().add(const Duration(minutes:3))),start=Timestamp.now();
          tx.update(_ref,{'pkActive':true,'pkSessionId':id,'pkOpponentRoomId':target,'pkEndsAt':end,'pkStartedAt':start});
          tx.update(ref,{'status':status,'pkEndsAt':end,'pkStartedAt':start});
        }else{tx.update(ref,{'status':'rejected'});}
      });
    }catch(_){if(mounted)setState(()=>_message='Davet süresi doldu veya oda uygun değil.');}
    finally{if(mounted)setState(()=>_busy=false);}
    await _sync();
  }
  Future<void> _invite()async{
    if(!_host||_busy||_picking)return;
    _picking=true;
    QuerySnapshot<Map<String,dynamic>> q;
    try{q=await _db.collection('audio_rooms').where('active',isEqualTo:true).limit(40).get(const GetOptions(source:Source.server));}
    catch(_){_picking=false;if(mounted)setState(()=>_message='Açık odalar alınamadı. Tekrar dene.');return;}
    if(!mounted)return;
    final rooms=q.docs.where((d)=>d.id!=widget.roomId&&d.data()['ownerId']!=_sessionUid&&_active(d.data())&&d.data()['pkActive']!=true).toList();
    final target=await showModalBottomSheet<String>(context:context,backgroundColor:const Color(0xFF102B39),builder:(c)=>SafeArea(child:ListView(shrinkWrap:true,children:[const ListTile(title:Text('Sesli PK daveti',style:TextStyle(color:Colors.white,fontWeight:FontWeight.bold)),subtitle:Text('İki yayıncı onayladığında odalar birbirini duyar. Mikrofonun kendi odanda kalır.',style:TextStyle(color:Colors.white70))),if(rooms.isEmpty)const ListTile(title:Text('Uygun açık oda yok',style:TextStyle(color:Colors.white70))),...rooms.map((d)=>ListTile(title:Text((d.data()['title']??'Sesli oda').toString(),style:const TextStyle(color:Colors.white)),trailing:const Icon(Icons.chevron_right,color:Colors.white),onTap:()=>Navigator.pop(c,d.id)))])));
    _picking=false;
    if(target==null||!mounted)return;setState(()=>_busy=true);
    try{
      final ref=_db.collection('calls').doc();
      await _db.runTransaction((tx)async{
        final own=(await tx.get(_ref)).data()??{},other=(await tx.get(_db.collection('audio_rooms').doc(target))).data()??{};
        if(own['ownerId']!=_sessionUid||!_active(own)||!_active(other)||own['pkActive']==true||other['pkActive']==true||other['ownerId']==_sessionUid)throw StateError('unavailable');
        tx.set(ref,{'type':'audio_pk','members':[_sessionUid,other['ownerId']],'startedBy':_sessionUid,'inviteeUid':other['ownerId'],'inviterRoomId':widget.roomId,'inviteeRoomId':target,'status':'pending','createdAt':FieldValue.serverTimestamp(),'requestExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(seconds:45)))});
      });
    }catch(_){if(mounted)setState(()=>_message='PK daveti gönderilemedi.');}
    finally{if(mounted)setState(()=>_busy=false);}
    await _sync();
  }
  @override Widget build(BuildContext context){
    if(widget.ended)return const SizedBox.shrink();
    final active=_own['pkActive']==true&&_validEnd(_own['pkEndsAt']);
    final incoming=_request['status']=='pending'&&_request['inviteeUid']==_sessionUid;
    final pending=_request['status']=='pending';
    final seconds=active?(_own['pkEndsAt'] as Timestamp).toDate().difference(DateTime.now()).inSeconds:0;
    if(!_host&&!active)return const SizedBox.shrink();
    return Container(margin:const EdgeInsets.only(bottom:10),padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),decoration:BoxDecoration(color:const Color(0xFF30205A),borderRadius:BorderRadius.circular(18)),child:Column(mainAxisSize:MainAxisSize.min,children:[Row(children:[const Icon(Icons.bolt,color:Colors.pinkAccent),const SizedBox(width:6),Expanded(child:Text(active?'PK • ${seconds~/60}:${(seconds%60).toString().padLeft(2,'0')}':incoming?'PK daveti':pending?'PK yanıtı bekleniyor':'Sesli PK',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800))),if(_host&&!active&&!pending)TextButton(onPressed:_busy?null:()=>unawaited(_invite()),child:const Text('Davet et')),if(incoming)...[TextButton(onPressed:_busy?null:()=>unawaited(_respond('rejected')),child:const Text('Reddet')),FilledButton(onPressed:_busy?null:()=>unawaited(_respond('accepted')),child:const Text('Kabul et'))],if(_host&&active)TextButton(onPressed:_busy?null:()=>unawaited(_stop()),child:const Text('PK bitir'))]),if(_message.isNotEmpty)Text(_message,style:const TextStyle(color:Colors.white70,fontSize:11))]));
  }
  @override void dispose(){_disposed=true;_timer?.cancel();_auth?.cancel();unawaited(_drop());super.dispose();}
}
