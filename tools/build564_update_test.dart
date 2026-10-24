import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart' show Ngelx564Release,Ngelx564UpdateController,Ngelx564UpdateDialog,ngelx564UpdateFeed;

Map<String,dynamic> manifest({int build=565})=>{'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','build':build,'version':'1.0.335','size':4,'sha256':'a'*64,'url':'https://github.com/Nnentx/Ngelx/releases/download/test/NgelX.apk','notes':'Bildirim ve yorum iyileştirmeleri'};
class Adapter extends HttpClientAdapter {
 Map<String,dynamic> feed=manifest();bool fail=false;int apkRequests=0;
 @override Future<ResponseBody> fetch(RequestOptions options,Stream<Uint8List>? stream,Future<void>? cancel)async{
  if(options.path==ngelx564UpdateFeed)return ResponseBody.fromString(jsonEncode(feed),200,headers:{Headers.contentTypeHeader:['application/json']});
  apkRequests++;
  if(fail)return ResponseBody.fromString('error',500);
  return ResponseBody.fromBytes([1,2,3,4],200,headers:{Headers.contentLengthHeader:['4'],Headers.contentTypeHeader:['application/vnd.android.package-archive']});
 }
 @override void close({bool force=false}){}
}
void main(){
 TestWidgetsFlutterBinding.ensureInitialized();
 const channel=MethodChannel('com.nnentx.ngelx_app/update564');
 late Directory dir;late Adapter adapter;late Ngelx564UpdateController controller;
 var allowed=true,reject=false,verifyCount=0,installCount=0;
 setUp(()async{
  SharedPreferences.setMockInitialValues({});dir=await Directory.systemTemp.createTemp('ngelx-update564');adapter=Adapter();
  final dio=Dio();dio.httpClientAdapter=adapter;controller=Ngelx564UpdateController(client:dio);
  allowed=true;reject=false;verifyCount=0;installCount=0;
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call)async{
   switch(call.method){
    case 'status':return {'build':564,'version':'1.0.334','canInstall':allowed};
    case 'prepare':return '${dir.path}/NgelX-565.apk';
    case 'verify':verifyCount++;if(reject)throw PlatformException(code:'VERIFY');expect(await File(call.arguments['path'] as String).length(),4);return 'verified';
    case 'install':installCount++;return allowed?'installer':'permission';
   }
   throw PlatformException(code:'UNKNOWN');
  });
 });
 tearDown(()async{controller.dispose();await dir.delete(recursive:true);TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null);});
 test('manifest rejects untrusted URL, wrong app, malformed hash, and oversized downloads',(){
  for(final delta in <Map<String,dynamic>>[
   {'url':'http://github.com/Nnentx/Ngelx/releases/download/test/NgelX.apk'},
   {'url':'https://github.com.evil.test/Nnentx/Ngelx/releases/download/test/NgelX.apk'},
   {'url':'https://github.com/another/repo/releases/download/test/NgelX.apk'},
   {'url':'https://github.com/Nnentx/Ngelx/releases/download/test/NgelX.apk?redirect=1'},
   {'sha256':'bad'},{'package':'other.app'},{'abi':'x86'},{'build':0},{'size':209715201},
  ]){expect(()=>Ngelx564Release.parse({...manifest(),...delta}),throwsFormatException);}
 });
 test('startup only checks; an equal or older release never downloads',()async{
  for(final build in [563,564]){adapter.feed=manifest(build:build);await controller.check();expect(controller.state,'current');await controller.download();}
  expect(adapter.apkRequests,0);expect(installCount,0);
  adapter.feed=manifest();await controller.check();expect(controller.state,'available');expect(adapter.apkRequests,0);
 });
 test('download verified before installer; denied permission waits for explicit Android grant',()async{
  allowed=false;await controller.check();await controller.download();expect(verifyCount,1);expect(controller.state,'permission');expect(installCount,1);
  allowed=true;await controller.resumePermission();expect(controller.state,'installer');expect(installCount,2);expect(adapter.apkRequests,1);
 });
 test('verification failure deletes candidate and never launches Android installer',()async{
  reject=true;await controller.check();await controller.download();expect(controller.state,'error');expect(installCount,0);expect(await File('${dir.path}/NgelX-565.apk').exists(),false);
 });
 test('failed download can retry without checking or installing a partial file',()async{
  adapter.fail=true;await controller.check();await controller.download();expect(controller.state,'error');expect(verifyCount,0);expect(installCount,0);
  adapter.fail=false;await controller.download();expect(controller.state,'installer');expect(verifyCount,1);expect(installCount,1);
 });
 testWidgets('update dialog has owner-approved action, progress and retry path',(tester)async{
  await controller.check();
  await tester.pumpWidget(MaterialApp(home:Builder(builder:(context)=>Scaffold(body:TextButton(onPressed:()=>showDialog<void>(context:context,builder:(_)=>Ngelx564UpdateDialog(controller:controller)),child:const Text('Aç'))))));
  await tester.tap(find.text('Aç'));await tester.pumpAndSettle();expect(find.text('Yeni güncelleme hazır'),findsOneWidget);expect(find.text('Güncelle'),findsOneWidget);
  expect(adapter.apkRequests,0);await tester.tap(find.text('Güncelle'));await tester.runAsync(()async{for(var i=0;i<100&&controller.busy;i++){await Future<void>.delayed(const Duration(milliseconds:50));}});await tester.pumpAndSettle();
  expect(installCount,1);expect(find.text('Yüklemeyi aç'),findsOneWidget);expect(tester.takeException(),isNull);
  await tester.pumpWidget(const SizedBox());
 });
}
