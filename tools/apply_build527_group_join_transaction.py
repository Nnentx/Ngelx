#!/usr/bin/env python3
"""Build527 QA applies only after Build526 integrated source transforms."""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
MARK='// Build527: do not resurrect ended group calls on delayed LiveKit events'

def once(s,old,new,label):
    if s.count(old)!=1:raise RuntimeError(f'Build527 {label}: expected one anchor, found {s.count(old)}')
    return s.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    src=once(src,"part 'build526_atomic_group_timeout.dart';",
      "part 'build526_atomic_group_timeout.dart';\npart 'build527_group_join_transaction.dart';",
      'Flutter transaction helper include')
    a=src.index('class _NgelXAramaPageState')
    b=src.index('class GrupBilgiPage',a)
    call=src[a:b]
    old="""        unawaited(widget.aramaRef.set({
          'callStatus':'active',
          'callConnectedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true)).catchError((_){ }));
        unawaited(widget.aramaRef.get().then((d){
          final id=(d.data()?['callMessageId']??'').toString();
          if(id.isNotEmpty)return widget.aramaRef.collection('messages').doc(id).set({
            'callStatus':'active',
            'callConnectedAt':FieldValue.serverTimestamp(),
          },SetOptions(merge:true));
        }).catchError((_){ }));"""
    new="""        // Build527: do not resurrect ended group calls on delayed LiveKit events.
        if(grupAramasi){
          unawaited(ngelx527ConfirmGroupRemoteTrack(
            widget.aramaRef,widget.roomName,
            cancelled:()=>bitiyor||!identical(oda,r)));
        }else{
          unawaited(widget.aramaRef.set({
            'callStatus':'active',
            'callConnectedAt':FieldValue.serverTimestamp(),
          },SetOptions(merge:true)).catchError((_){ }));
          unawaited(widget.aramaRef.get().then((d){
            final id=(d.data()?['callMessageId']??'').toString();
            if(id.isNotEmpty)return widget.aramaRef.collection('messages').doc(id).set({
              'callStatus':'active',
              'callConnectedAt':FieldValue.serverTimestamp(),
            },SetOptions(merge:true));
          }).catchError((_){ }));
        }"""
    call=once(call,old,new,'remote track must not blindly reactivate group')
    old_join="""      unawaited(widget.aramaRef.set(durumGuncelleme,SetOptions(merge:true)).timeout(const Duration(seconds:10)).catchError((_){ }));
      if(widget.roomName.startsWith('group_')){"""
    new_join="""      if(grupAramasi){
        final accepted=await ngelx527RegisterGroupParticipant(
          widget.aramaRef,widget.roomName,u.uid,activate:aktif,
          cancelled:()=>bitiyor||!identical(oda,r));
        if(!accepted)throw StateError('Grup görüşmesi bitti veya katılım izni değişti.');
      }else{
        unawaited(widget.aramaRef.set(durumGuncelleme,SetOptions(merge:true)).timeout(const Duration(seconds:10)).catchError((_){ }));
      }
      if(widget.roomName.startsWith('group_')){"""
    call=once(call,old_join,new_join,'group participant join transaction')
    # Only the private path still updates the original call receipt with a
    # blind asynchronous write. A group receipt follows the current room
    # transaction and cannot revive the call state.
    call=once(call,"      if(aktif){\n        unawaited(widget.aramaRef.get().then((d){",
      "      if(aktif&&!grupAramasi){\n        unawaited(widget.aramaRef.get().then((d){",
      'avoid stale group active receipt writes')
    for name in ('await ngelx517LeaveGroupCall(','_confirmGroupExit517()',
                 'ngelx526ExpireUnansweredGroupCall(',
                 'Ngelx520PipBridge.active','_voiceGroupCameraBusy517'):
        if name not in call:raise RuntimeError('Build527 must preserve '+name)
    src=src[:a]+call+src[b:]
    assert src.count(MARK)==1
    return src

if __name__=='__main__':
    src=MAIN.read_text(encoding='utf-8')
    newer=transform(src)
    if newer!=src: MAIN.write_text(newer,encoding='utf-8')
    print('Build527: group call status cannot be revived by stale background reconnect/remote-track writes')
