from pathlib import Path
p=Path('app/lib/build448_incoming_calls.dart');s=p.read_text()
needle="        final active=s.docs.where((d)"
assert needle in s
s=s.replace(needle,"        for(final change in s.docChanges){if(change.type!=DocumentChangeType.removed)unawaited(_pushOutgoing452(change.doc.id,change.doc.data()??<String,dynamic>{},user.uid));}\n"+needle,1)
pos=s.index('  Future<void> _stop(')
s=s[:pos]+'''  final Set<String> _dispatch452=<String>{};
  Future<void> _pushOutgoing452(String chat,Map<String,dynamic> value,String uid)async{
    const endpoint=String.fromEnvironment('NGELX_CALL_PUSH_URL');
    if(endpoint.isEmpty||FirebaseAuth.instance.currentUser?.uid!=uid)return;
    final room=(value['callRoomName']??'').toString(),status=(value['callStatus']??'').toString();
    final created=value['callCreatedAt'];
    final changed=status=='active'?value['callAnsweredAt']:value['callEndedAt'];
    if(room.isEmpty)return;
    if(status=='ringing'){
      if(value['callStartedBy']!=uid||created is! Timestamp||DateTime.now().difference(created.toDate()).inSeconds>=60)return;
    }else{
      if(!const ['active','ended','rejected','missed'].contains(status)||changed is! Timestamp||DateTime.now().difference(changed.toDate()).inSeconds>=60)return;
    }
    final key='$uid:$chat:$room:$status';
    if(!_dispatch452.add(key))return;
    // Bound session memory. A later server lease still prevents duplicate alerts.
    if(_dispatch452.length>200)_dispatch452.remove(_dispatch452.first);
    Future<bool> attempt()async{
      var offset=0;
      for(var chunk=0;chunk<15;chunk++){
        final user=FirebaseAuth.instance.currentUser;if(user?.uid!=uid)return true;
        final token=await user!.getIdToken();
        final response=await http.post(Uri.parse('$endpoint/call'),headers:{'Authorization':'Bearer $token','Content-Type':'application/json'},body:jsonEncode({'chatId':chat,'roomName':room,'offset':offset})).timeout(const Duration(seconds:12));
        if(response.statusCode>=500)return false;
        if(response.statusCode!=200)return true;
        final body=jsonDecode(response.body) as Map<String,dynamic>;
        final next=body['nextOffset'];if(next==null)return true;
        if(next is! int||next<=offset)return true;offset=next;
      }
      return true;
    }
    try{if(await attempt())return;}catch(_){}
    await Future<void>.delayed(const Duration(seconds:16));
    if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
    try{await attempt();}catch(_){}
  }
''' +s[pos:]
p.write_text(s)
print('Build452 caller-triggered authenticated free push integration applied')
