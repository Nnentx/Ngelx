part of 'main.dart';

// A media disconnect succeeds locally even if Firestore is offline. Keep the
// exact room and owner until a server-confirmed, self-only leave completes.
final Set<String> _leaveInFlight542={};
Future<void> ngelx542LeaveGroupCall(DocumentReference<Map<String,dynamic>> ref,String room,String uid,{required bool video,String? displayName})async{
  if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
  final prefs=await SharedPreferences.getInstance();
  final key='pending_call_leave_542_${uid}_$room';
  await prefs.setString(key,jsonEncode({'path':ref.path,'room':room,'uid':uid,'video':video,'name':displayName}));
  await _ngelx542AttemptLeave(key,prefs);
}
Future<void> _ngelx542AttemptLeave(String key,SharedPreferences prefs)async{
  while(_leaveInFlight542.contains(key)){await Future<void>.delayed(const Duration(milliseconds:60));}
  if(!_leaveInFlight542.add(key))return;
  try{
    final raw=prefs.getString(key);
    if(raw==null)return;
    final data=jsonDecode(raw) as Map<String,dynamic>;
    final uid=data['uid'] as String,room=data['room'] as String;
    if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
    if(data['receipt']==true){
      final receipt=FirebaseFirestore.instance.doc(data['path'] as String);
      final old=await receipt.get(const GetOptions(source:Source.server));
      if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
      if(!old.exists)await receipt.set({...Map<String,dynamic>.from(data['payload'] as Map),'createdAt':FieldValue.serverTimestamp()});
      await prefs.remove(key);return;
    }
    final ref=FirebaseFirestore.instance.doc(data['path'] as String);
    final current=(await ref.get(const GetOptions(source:Source.server))).data();
    if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
    // A later call or a revoked membership must never be touched by replay.
    if(current==null||current['callRoomName']!=room||
       !List<String>.from(current['members']??const[]).contains(uid)){
      await prefs.remove(key);return;
    }
    await ngelx517LeaveGroupCall(ref,room,uid,video:data['video']==true,displayName:data['name'] as String?);
    await prefs.remove(key);
  }finally{_leaveInFlight542.remove(key);}
}
Future<void> ngelx542RetryPendingLeaves()async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null)return;
  final prefs=await SharedPreferences.getInstance();
  final keys=prefs.getKeys().where((k)=>k.startsWith('pending_call_leave_542_${uid}_')).toList();
  for(final key in keys){
    if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
    try{await _ngelx542AttemptLeave(key,prefs);}catch(error){debugPrint('Pending self-leave retained: $error');}
  }
}

Future<void> ngelx542QueueReceipt(DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> payload)async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null||payload['actorUid']!=uid)return;
  final prefs=await SharedPreferences.getInstance();
  final key='pending_call_leave_542_${uid}_receipt_${ref.id}';
  final serializable=Map<String,dynamic>.from(payload)..remove('createdAt');
  await prefs.setString(key,jsonEncode({'receipt':true,'path':ref.path,'room':'receipt','uid':uid,'payload':serializable}));
  try{await _ngelx542AttemptLeave(key,prefs);}catch(error){
    // Membership already committed. History is independently retriable and
    // must not falsely report that the authoritative leave failed.
    debugPrint('Call history queued for retry: $error');
  }
}

Future<bool> ngelx542PrepareManualJoin(String room,String uid)async{
  final prefs=await SharedPreferences.getInstance();
  final key='pending_call_leave_542_${uid}_$room';
  if(prefs.containsKey(key)){
    try{await _ngelx542AttemptLeave(key,prefs);}catch(_){return false;}
  }
  return FirebaseAuth.instance.currentUser?.uid==uid&&!prefs.containsKey(key);
}
