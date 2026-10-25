import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';
Map<String,dynamic> state({int count=1,String status='waiting',int revision=1})=>{'id':'ABCDEF0123456789','owner':'a','capacity':2,'status':status,'revision':revision,'mode':'power','team':false,'players':[{'uid':'a','seat':0,'name':'Alihan'},if(count==2){'uid':'b','seat':2,'name':'Arkadaşın'}],'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),'power':List.generate(4,(_)=>{'control':2,'double':2,'shield':2}),'turn':0,'dice':null,'chat':[]};
Future<void> preview(WidgetTester t,String name)async{
 await t.pumpAndSettle();
 await t.runAsync(()async{final boundary=t.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('preview')));final image=await boundary.toImage(pixelRatio:2);final bytes=await image.toByteData(format:ui.ImageByteFormat.png);Directory('build567-previews').createSync();File('build567-previews/$name.png').writeAsBytesSync(bytes!.buffer.asUint8List());image.dispose();});
}
void main(){
 TestWidgetsFlutterBinding.ensureInitialized();
 setUpAll(()async{
  final text=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(text.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(text.readAsBytesSync().buffer)))).load();
  final root=Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
  final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
  if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
 });
 test('late polling membership error cannot undo successful leave',()async{
  final pending=Completer<Map<String,dynamic>>();final g=Ngelx567RoomController(id:'x',uid:'a',initial:state(),request:(b)async=>b['action']=='sync'?pending.future:state(status:'closed',revision:2));
  final sync=g.sync();expect(await g.leave(),true);pending.completeError(const Ngelx567Failure('not_a_player','gone'));await sync;expect(g.detached,true);expect(g.error,isEmpty);g.dispose();
 });
 test('already left and expired rooms return to lobby without another leave loop',()async{
  for(final code in ['not_a_player','already_left','room_expired','room_not_found']){final g=Ngelx567RoomController(id:'x',uid:'a',initial:state(),request:(b)async=>throw Ngelx567Failure(code,'gone'));expect(await g.leave(),true);expect(g.detached,true);expect(g.error,isEmpty);g.dispose();}
 });
 test('revision conflict refreshes once and retains leave idempotency key',()async{
  final calls=<Map<String,dynamic>>[];final g=Ngelx567RoomController(id:'x',uid:'a',initial:state(),request:(b)async{calls.add(b);if(calls.length==1)throw const Ngelx567Failure('state_changed','stale');return state(revision:2,status:calls.length==3?'closed':'waiting');});
  expect(await g.leave(),true);expect(calls.map((b)=>b['action']),['leave','sync','leave']);expect(calls.first['requestId'],calls.last['requestId']);expect(calls.last['revision'],2);g.dispose();
 });
 test('offline leave remains retryable and concurrent leave is not duplicated',()async{
  final pending=Completer<Map<String,dynamic>>();var calls=0;final g=Ngelx567RoomController(id:'x',uid:'a',initial:state(),request:(b){calls++;return pending.future;});final leaving=g.leave();expect(await g.leave(),false);expect(calls,1);pending.completeError(Exception('offline'));expect(await leaving,false);expect(g.detached,false);expect(g.busy,false);expect(g.error,'offline');g.dispose();
 });
 test('start requires owner and every required seat',(){
  for(final count in [1,2]){final g=Ngelx567RoomController(id:'x',uid:'a',initial:state(count:count),request:(b)async=>state());expect(g.canStart,count==2);g.dispose();}final guest=Ngelx567RoomController(id:'x',uid:'b',initial:state(count:2),request:(b)async=>state());expect(guest.canStart,false);guest.dispose();
 });
 test('home sockets and pawn centers are symmetric in all four houses',(){
  const centers=[Offset(3,3),Offset(12,3),Offset(12,12),Offset(3,12)];
  for(var seat=0;seat<4;seat++){final points=[for(var token=0;token<4;token++)ngelx565TokenPoint(seat,token,-1)+const Offset(.5,.5)];final center=points.reduce((a,b)=>a+b)/4;expect(center,centers[seat]);expect(points.toSet().length,4);for(final p in points)expect((p-center).distance,closeTo(1.41421356,.00001));}
 });
 test('pawn motion follows each track cell rather than cutting across board',(){
  for(var seat=0;seat<4;seat++)for(var pos=0;pos<55;pos++){expect(ngelx567MovingPoint(seat,0,pos,pos+1,0),ngelx565TokenPoint(seat,0,pos));expect(ngelx567MovingPoint(seat,0,pos,pos+1,1),ngelx565TokenPoint(seat,0,pos+1));}
 });
 for(final size in [const Size(393,851),const Size(320,568),const Size(720,360)]){
 testWidgets('waiting start remains readable at $size',(t)async{
  t.view.physicalSize=size;t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('preview'),child:Ngelx565LudoRoom(id:'ABCDEF0123456789',userId:'a',initial:state(),request:(b)async=>state(),onInvite:(){}))));await t.pumpAndSettle();expect(find.text('Başlat'),findsOneWidget);expect(t.takeException(),isNull);
  final button=t.widget<Ngelx567GameButton>(find.widgetWithText(Ngelx567GameButton,'Başlat'));expect(button.onPressed,isNull);
  expect(t.getRect(find.text('Başlat')).bottom,lessThan(size.height));
  if(size.width==393)await preview(t,'waiting');await t.pumpWidget(const SizedBox());
 });}
 testWidgets('full room starts through real action callback and playing layout renders',(t)async{
  t.view.physicalSize=const Size(393,851);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);final calls=<String>[];
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('preview'),child:Ngelx565LudoRoom(id:'ABCDEF0123456789',userId:'a',initial:state(count:2),request:(b)async{calls.add(b['action']);return state(count:2,status:'playing',revision:2);},onInvite:(){}))));await t.pumpAndSettle();await t.tap(find.text('Başlat'));await t.pumpAndSettle();expect(calls,['start']);expect(find.text('Sıra sende'),findsOneWidget);expect(t.takeException(),isNull);await preview(t,'playing');await t.pumpWidget(const SizedBox());
 });
 testWidgets('confirmed leave pops room even when server says membership is gone',(t)async{
  await t.pumpWidget(MaterialApp(home:Builder(builder:(c)=>TextButton(onPressed:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:'ABCDEF0123456789',userId:'a',initial:state(),request:(b)async=>throw const Ngelx567Failure('not_a_player','gone')))),child:const Text('Open')))));await t.tap(find.text('Open'));await t.pumpAndSettle();await t.tap(find.byKey(const ValueKey('ludo-back')));await t.pumpAndSettle();await t.tap(find.byKey(const ValueKey('confirm-ludo-leave')));await t.pumpAndSettle();expect(find.text('Open'),findsOneWidget);expect(find.byType(Ngelx565LudoRoom),findsNothing);
 });
 testWidgets('lobby visual reference',(t)async{t.view.physicalSize=const Size(393,851);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);await t.pumpWidget(const MaterialApp(home:RepaintBoundary(key:ValueKey('preview'),child:Ngelx565LudoLobby())));await preview(t,'lobby');expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());});
}
