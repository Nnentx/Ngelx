import 'package:flutter_test/flutter_test.dart';
import '../lib/build541_pk_policy.dart';
void main(){
 const now=1000000;
 Ngelx541PkRoom room(String id,String owner,{bool fresh=true,bool active=false,String session='',String peer='',int end=0})=>Ngelx541PkRoom(id:id,owner:owner,publicAndFresh:fresh,active:active,session:session,peer:peer,endsAt:end);
 bool accept({String uid='b',String inviter='a',String invitee='b',String status='pending',int expiry=1045000,bool fresh=true,bool busy=false})=>ngelx541PkCanAccept(own:room('B','b',fresh:fresh,active:busy),other:room('A','a'),uid:uid,inviterUid:inviter,inviteeUid:invitee,inviterRoom:'A',inviteeRoom:'B',status:status,expiresAt:expiry,now:now);
 test('only named invitee host may accept an unexpired idle public room invitation',(){
  expect(accept(),isTrue);
  expect(accept(uid:'viewer'),isFalse);expect(accept(inviter:'attacker'),isFalse);
  expect(accept(invitee:'attacker'),isFalse);expect(accept(status:'rejected'),isFalse);
  expect(accept(expiry:now),isFalse);expect(accept(expiry:now+61000),isFalse);
  expect(accept(fresh:false),isFalse);expect(accept(busy:true),isFalse);
 });
 test('no audio subscription before reciprocal owner room attestations',(){
  final a=room('A','a',active:true,session:'s',peer:'B',end:now+180000);
  bool mutual(Ngelx541PkRoom b)=>ngelx541PkMutual(a,b,now);
  expect(mutual(room('B','b',active:true,session:'s',peer:'A',end:now+180000)),isTrue);
  expect(mutual(room('B','b')),isFalse);
  expect(mutual(room('B','b',active:true,session:'forged',peer:'A',end:now+180000)),isFalse);
  expect(mutual(room('B','b',active:true,session:'s',peer:'C',end:now+180000)),isFalse);
  expect(mutual(room('B','a',active:true,session:'s',peer:'A',end:now+180000)),isFalse);
  expect(mutual(room('B','b',fresh:false,active:true,session:'s',peer:'A',end:now+180000)),isFalse);
  expect(mutual(room('B','b',active:true,session:'s',peer:'A',end:now+170000)),isFalse);
  expect(ngelx541PkMutual(a,room('B','b',active:true,session:'s',peer:'A',end:now+180000),now+180001),isFalse);
 });
}
