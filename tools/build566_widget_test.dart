import 'dart:convert';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build566_transport.dart';
import '../lib/build566_policy.dart';
class GameAdapter implements HttpClientAdapter {
 final Future<ResponseBody> Function(RequestOptions,int) handle;final calls=<RequestOptions>[];
 GameAdapter(this.handle);
 @override Future<ResponseBody> fetch(RequestOptions o,Stream<Uint8List>? s,Future<void>? c){calls.add(o);return handle(o,calls.length);}
 @override void close({bool force=false}){}
}
ResponseBody room()=>ResponseBody.fromString(jsonEncode({'room':{'id':'ABCDEF0123456789','revision':0}}),200,headers:{Headers.contentTypeHeader:['application/json']});
void main(){
 test('PK initial loading and cached opponent never terminate an accepted match',(){
  for(final v in [(false,false,false),(true,false,false),(true,true,true)]){
   expect(ngelx566PkShouldEnd(remaining:180,opponentLoaded:v.$1,serverConfirmed:v.$2,opponentFresh:v.$3),false);
  }
  expect(ngelx566PkShouldEnd(remaining:180,opponentLoaded:true,serverConfirmed:true,opponentFresh:false),true);
  expect(ngelx566PkShouldEnd(remaining:0,opponentLoaded:false,serverConfirmed:false,opponentFresh:true),true);
 });
 test('announcement sorts with chats; opening Parlament or a newer message moves it above notices',(){
  final rows=[(id:'notice',pinned:false,time:100),(id:'parlament',pinned:false,time:90),(id:'pinned',pinned:true,time:50)];
  void sort()=>rows.sort((a,b)=>ngelx566InboxCompare(a.pinned,a.time,b.pinned,b.time));
  sort();expect(rows.map((r)=>r.id),['pinned','notice','parlament']);
  rows[2]=(id:'parlament',pinned:false,time:ngelx566InboxTime(90,110));sort();expect(rows.map((r)=>r.id),['pinned','parlament','notice']);
  rows[2]=(id:'notice',pinned:false,time:120);sort();expect(rows.map((r)=>r.id),['pinned','notice','parlament']);
  expect(ngelx566InboxTime(130,110),130);
 });
 test('owned hostname is primary and fallback preserves one create request id',()async{
  final client=Dio();final adapter=GameAdapter((o,n)async{if(n==1)throw DioException(requestOptions:o,type:DioExceptionType.connectionError);return room();});client.httpClientAdapter=adapter;
  final t=Ngelx566LudoTransport(client:client);await t.request({'action':'create','capacity':2},token:'test-token');
  expect(adapter.calls.map((r)=>r.uri.host),['oyun.ngelxsocial.com','ngelx-live-moderation.alihancaglar76.workers.dev']);
  final bodies=adapter.calls.map((r)=>(r.data is String?jsonDecode(r.data as String):r.data) as Map).toList();expect(bodies[0]['requestId'],bodies[1]['requestId']);expect((bodies[0]['requestId'] as String).length,32);
  expect(adapter.calls.every((r)=>r.headers['Authorization']=='Bearer test-token'),true);
 });
 test('authentication and membership failures do not switch hosts',()async{
  for(final status in [401,403]){
   final client=Dio(),adapter=GameAdapter((o,n)async=>ResponseBody.fromString('{"error":"not_a_player"}',status,headers:{Headers.contentTypeHeader:['application/json']}));client.httpClientAdapter=adapter;
   await expectLater(Ngelx566LudoTransport(client:client).request({'action':'sync'},token:'token'),throwsA(isA<DioException>()));expect(adapter.calls.length,1);
  }
 });
 test('an intermediary HTML rejection can use the other verified HTTPS host',()async{
  final client=Dio(),adapter=GameAdapter((o,n)async=>n==1?ResponseBody.fromString('<html>unavailable</html>',403):room());client.httpClientAdapter=adapter;
  expect((await Ngelx566LudoTransport(client:client).request({'action':'sync'},token:'token'))['revision'],0);expect(adapter.calls.length,2);
 });
 test('both unavailable hosts surface an error instead of a fake room',()async{
  final client=Dio(),adapter=GameAdapter((o,n)async{throw DioException(requestOptions:o,type:DioExceptionType.receiveTimeout);});client.httpClientAdapter=adapter;
  await expectLater(Ngelx566LudoTransport(client:client).request({'action':'sync'},token:'token'),throwsA(isA<DioException>()));expect(adapter.calls.length,2);
 });
 test('a redirect is never followed with the Firebase bearer token',()async{
  final client=Dio(),adapter=GameAdapter((o,n)async=>ResponseBody.fromString('',302,headers:{'location':['https://untrusted.example/']}));client.httpClientAdapter=adapter;
  await expectLater(Ngelx566LudoTransport(client:client).request({'action':'sync'},token:'token'),throwsA(isA<DioException>()));expect(adapter.calls.single.followRedirects,false);
 });
}
