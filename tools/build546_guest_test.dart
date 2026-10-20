import 'package:flutter_test/flutter_test.dart';
import '../lib/build546_guest_policy.dart';
void main(){
 bool allowed({String? current='guest',String? status='accepted',bool live=true,String? room='room',String? host='owner',String? guest='guest'})=>ngelx546GuestAuthorized(expectedUid:'guest',currentUid:current,expectedOwner:'owner',room:'room',currentRoom:room,live:live,owner:'owner',host:host,guest:guest,status:status);
 test('accepted guest must match live owner, identity and exact room',(){expect(allowed(),isTrue);for(final s in ['pending','invited','rejected',null]){expect(allowed(status:s),isFalse);}expect(allowed(current:'different'),isFalse);expect(allowed(current:null),isFalse);expect(allowed(live:false),isFalse);expect(allowed(room:'new-room'),isFalse);expect(allowed(host:'forged'),isFalse);expect(allowed(guest:'other'),isFalse);});
 test('reuse requires connected room and actual media permissions',(){
  bool reuse(bool connected,bool publish,List<String> sources,bool mic,bool camera)=>ngelx546CanReuse(connected:connected,canPublish:publish,sources:sources,microphone:mic,camera:camera);
  expect(reuse(true,true,[],true,true),isTrue);
  expect(reuse(false,true,[],true,true),isFalse);
  expect(reuse(true,false,[],false,false),isFalse);
  expect(reuse(true,true,['CAMERA'],true,true),isFalse);
  expect(reuse(true,true,['CAMERA'],false,true),isTrue);
  expect(reuse(true,true,['MICROPHONE'],true,false),isTrue);
  expect(reuse(true,true,['MICROPHONE'],true,true),isFalse);
 });
 test('automatic retry is bounded and stops on leave or disposed screen',(){for(var i=0;i<3;i++){expect(ngelx546ShouldRetry(i,true,true),isTrue);}expect(ngelx546ShouldRetry(3,true,true),isFalse);expect(ngelx546ShouldRetry(0,false,true),isFalse);expect(ngelx546ShouldRetry(0,true,false),isFalse);});
}
