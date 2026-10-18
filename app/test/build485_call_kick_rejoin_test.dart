import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/build485_kick_policy_test_api.dart' as ngelx;

void main() {
  const room='group_active_485';
  const uid='member485';
  Map<String,dynamic> doc({int epoch=0,bool legacyKick=false,String atRoom=room})=><String,dynamic>{
    'callModerationRoom':atRoom,
    'callKickEpochs':<String,dynamic>{uid:epoch},
    'callKickedUids':legacyKick?<String>[uid]:<String>[],
  };

  test('an earlier kick is not a lifetime ban on explicit rejoin',(){
    expect(ngelx.ngelx485FreshKick(doc(epoch:1,legacyKick:true),room,uid,
      initialEpoch:1,legacyAtJoin:true),isFalse);
    expect(ngelx.ngelx485FreshKick(doc(epoch:1,legacyKick:true),room,uid,
      initialEpoch:1,legacyAtJoin:true),isFalse);
  });

  test('moderator kick disconnects only once during current attachment',(){
    expect(ngelx.ngelx485FreshKick(doc(epoch:2),room,uid,
      initialEpoch:1,legacyAtJoin:false),isTrue);
    expect(ngelx.ngelx485FreshKick(doc(epoch:1),room,uid,
      initialEpoch:1,legacyAtJoin:false),isFalse);
    expect(ngelx.ngelx485FreshKick(doc(epoch:1,legacyKick:true),room,uid,
      initialEpoch:1,legacyAtJoin:false),isTrue);
  });

  test('new kick after rejoin is a fresh event, including repeat kicks',(){
    final first=ngelx.ngelx485NextKickEpochs(doc(),room,uid);
    expect(first[uid],1);
    final nextState=doc(epoch:1,legacyKick:true);
    final second=ngelx.ngelx485NextKickEpochs(nextState,room,uid);
    expect(second[uid],2);
    expect(ngelx.ngelx485FreshKick(nextState,room,uid,
      initialEpoch:1,legacyAtJoin:true),isFalse);
    expect(ngelx.ngelx485FreshKick(doc(epoch:2,legacyKick:true),room,uid,
      initialEpoch:1,legacyAtJoin:true),isTrue);
  });

  test('a new room resets kick epochs and a different room cannot kick',(){
    expect(ngelx.ngelx485NextKickEpochs(doc(epoch:30,atRoom:'group_old'),room,uid)[uid],1);
    expect(ngelx.ngelx485FreshKick(doc(epoch:50,legacyKick:true,atRoom:'group_old'),room,uid,
      initialEpoch:0,legacyAtJoin:false),isFalse);
  });

  test('other people cannot create a kick event for this account',(){
    final state=doc(epoch:1)..['callKickEpochs']=<String,dynamic>{uid:1,'other':9};
    expect(ngelx.ngelx485FreshKick(state,room,uid,
      initialEpoch:1,legacyAtJoin:false),isFalse);
    expect(ngelx.ngelx485FreshKick(state,room,null,
      initialEpoch:0,legacyAtJoin:false),isFalse);
  });
}
