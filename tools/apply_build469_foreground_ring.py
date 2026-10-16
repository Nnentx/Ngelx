#!/usr/bin/env python3
"""Build469 incoming-call foreground gap: don't cancel a ringtone from stale inbox cache.
A group call may already be active when the 3rd/4th participant is invited.
Keep account-bound checks, call TTL and native cancel semantics.
"""
from pathlib import Path
FILE=Path('app/lib/build448_incoming_calls.dart')
TAG='// Build469: verify empty snapshots before stopping a ringing call'
def one(s,old,new,what):
    if s.count(old)!=1:raise RuntimeError(f'Build469 call reception {what}: {s.count(old)}')
    return s.replace(old,new,1)
def transform(src):
    if TAG in src:return src
    s=one(src,
      '  String? _ringing,_handling,_account455;',
      '''  String? _ringing,_handling,_account455,_ringingChat469;
  bool _verifyingMissing469=false;''','ringing state')
    s=one(s,
      """        final active=s.docs.where((d){final v=d.data(),t=v['callCreatedAt'];return v['callStartedBy']!=user.uid&&v['callStatus']=='ringing'&&t is Timestamp&&DateTime.now().difference(t.toDate()).inSeconds<60;}).toList();
        if(active.isEmpty){unawaited(_stop());return;}""",
      """        // Build469: verify empty snapshots before stopping a ringing call.
        // Initial offline-cache snapshots can be empty even when the server
        // still has an unanswered incoming call. Don't silence the ringtone.
        final active=s.docs.where((d){
          final v=d.data(),t=v['callCreatedAt'];
          if(v['callStartedBy']==user.uid||t is! Timestamp)return false;
          final age=DateTime.now().difference(t.toDate()).inSeconds;
          if(age<0||age>=60)return false;
          if(v['callStatus']=='ringing')return true;
          // Later group invitees can arrive after somebody answered.
          return v['isGroup']==true&&v['callStatus']=='active'
            &&!List<String>.from(v['callParticipants']??const[]).contains(user.uid);
        }).toList();
        if(active.isEmpty){
          final roomToCheck=_ringing,chatToCheck=_ringingChat469;
          if(roomToCheck==null||chatToCheck==null){
            unawaited(_stop());
          }else if(!_verifyingMissing469){
            _verifyingMissing469=true;
            unawaited(()async{
              try{
                final d=await FirebaseFirestore.instance.collection('chats')
                  .doc(chatToCheck).get(const GetOptions(source:Source.server))
                  .timeout(const Duration(seconds:6));
                final v=d.data()??<String,dynamic>{};
                final participants=List<String>.from(v['callParticipants']??const[]);
                final stillIncoming=v['callRoomName']==roomToCheck&&
                  (v['callStatus']=='ringing'||
                   v['isGroup']==true&&v['callStatus']=='active'&&!participants.contains(user.uid));
                if(!stillIncoming&&_ringing==roomToCheck&&FirebaseAuth.instance.currentUser?.uid==user.uid){
                  await _stop();
                }
              }catch(_){
                // Prefer ringing until the native timeout over silencing a
                // real call on an offline/cached snapshot.
              }finally{_verifyingMissing469=false;}
            }());
          }
          return;
        }""",'group invitations and cache-safe stop')
    s=one(s,'    final room=_ringing;_ringing=null;',
        '    final room=_ringing;_ringing=null;_ringingChat469=null;','cancel room plus chat')
    s=one(s,'_ringing=room;\n    if(caller.isNotEmpty)',
        '_ringing=room;_ringingChat469=chat;\n    if(caller.isNotEmpty)','track ringing chat')
    for req in ('if(_ringing==room)return','ngelxCallSession444.busy','channel.invokeMethod<void>(\'cancel\'','_pushOutgoing452'):
      if req not in s:raise RuntimeError('call privacy/state guard drift '+req)
    return s
if __name__=='__main__':
    old=FILE.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding='utf-8')
    print('Build469: call TTL and sender/receiver guard kept; group active invite rings; ignore stale empty cache')
