import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build566_transport.dart';
import '../lib/build567_room_controller.dart';
import 'build579_invite_test.dart' show room579;

Future<void> preview580(WidgetTester t,String name)async{
 final boundary=t.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('preview580')));
 await t.runAsync(()async{
  final image=await boundary.toImage(pixelRatio:2),bytes=await image.toByteData(format:ui.ImageByteFormat.png);
  Directory('build580-previews').createSync();File('build580-previews/$name.png').writeAsBytesSync(bytes!.buffer.asUint8List());image.dispose();
 });
}
void main(){
 setUpAll(()async{
  final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
 });
 setUp(()=>SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false}));
 test('wallet, daily reward and catalog are not mistaken for room responses',()async{
  final dio=Dio()..interceptors.add(InterceptorsWrapper(onRequest:(options,handler){
   final action=(options.data as Map)['action'];
   handler.resolve(Response(requestOptions:options,statusCode:200,data:{'room':action=='gift_catalog'?{'gifts':<String,dynamic>{}}:{'chips':5075,'gems':0,'xp':10,'level':1,'claimed':true}}));
  }));
  final transport=Ngelx566LudoTransport(client:dio);
  for(final action in ['wallet','daily_reward','chest_reward','gift_catalog']){
   expect(await transport.request({'action':action},token:'test'),isNotEmpty);
  }
  await expectLater(transport.request({'action':'sync','id':'270565'},token:'test'),throwsFormatException);
  dio.close();
 });
 test('Auto-off press waits for pending move and survives revision conflict without replaying move',()async{
  final move=Completer<Map<String,dynamic>>();final calls=<String>[];var attempts=0;
  final game=Ngelx567RoomController(id:'270565',uid:'a',initial:{...room579(),'status':'playing','autoSeats':{'0':true}},request:(b)async{
   calls.add(b['action']);
   if(b['action']=='move')return move.future;
   if(b['action']=='auto'&&++attempts==1)throw const Ngelx567Failure('state_changed','stale');
   return {...room579(),'status':'playing','revision':4,'autoSeats':<String,dynamic>{}};
  });
  final pending=game.perform('move',{'token':0});final off=game.setAuto580(false);
  expect(game.pendingAuto580,false);expect(calls,['move']);
  move.complete({...room579(),'status':'playing','revision':2,'autoSeats':{'0':true}});
  await pending;await off;
  expect(calls,['move','auto','sync','auto']);expect(game.pendingAuto580,isNull);
  expect(game.room['autoSeats'],isEmpty);expect(game.error,isEmpty);game.dispose();
 });
 test('four-player waiting room allows host to start at two, while complete teams remain required',(){
  final g=Ngelx567RoomController(id:'270565',uid:'a',request:(_)async=>{},initial:{...room579(),'capacity':4});
  expect(g.canStart,true);g.room={...g.room,'team':true};expect(g.canStart,false);g.dispose();
 });
 test('chat invitation query token preserves room recognition',(){
  final token=List.filled(64,'a').join();final link='🎲 Ludo daveti\nhttps://ngelxsocial.com/ludo/270565?invite=$token\nKatıl';
  expect(ngelx565RoomId(link),'270565');expect(ngelx580InviteToken(link),token);
 });
 testWidgets('white invite search filters people and groups and keeps final row above navigation inset',(t)async{
  await t.binding.setSurfaceSize(const Size(360,720));addTearDown(()=>t.binding.setSurfaceSize(null));
  final targets=List.generate(20,(i)=>Ngelx580InviteTarget(id:'$i',name:i==19?'KRİSTAL':i==0?'Ahsen Can':'Kişi $i',group:i==19));
  await t.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(size:Size(360,720),padding:EdgeInsets.only(bottom:34)),child:RepaintBoundary(key:const ValueKey('preview580'),child:Ngelx580InviteContacts(targets:targets,onPick:(_){})))));
  await t.pump();expect(t.takeException(),isNull);
  await t.enterText(find.byKey(const ValueKey('ludo-invite-search')),'kristal');await t.pump();
  expect(find.text('KRİSTAL'),findsOneWidget);expect(find.text('Ahsen Can'),findsNothing);
  expect(t.getBottomLeft(find.byKey(const ValueKey('invite-contact-19'))).dy,lessThan(686));
  await preview580(t,'white-search-group');
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('invitation expires after two minutes and cannot activate Join',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));var joins=0;
  await t.pumpWidget(MaterialApp(home:Scaffold(body:RepaintBoundary(key:const ValueKey('preview580'),child:Ngelx565LudoInviteCard(id:'270565',mine:false,sentAt:DateTime.now().millisecondsSinceEpoch,onLongPress:(){},onJoin:()=>joins++)))));
  await t.pump();expect(find.text('Bekleniyor'),findsOneWidget);await preview580(t,'visual-invite');
  // Use server-expired state: clock changes alone never permit an expired join.
  await t.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx565LudoInviteCard(key:const ValueKey('expired'),id:'270565',mine:false,sentAt:DateTime.now().millisecondsSinceEpoch-120000,onLongPress:(){},onJoin:()=>joins++))));
  await t.pump();expect(find.text('Süresi doldu'),findsNWidgets(2));
  final button=t.widget<FilledButton>(find.byKey(const ValueKey('ludo-invite-join')));expect(button.onPressed,isNull);expect(joins,0);
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('four-seat waiting panel fits narrow width with larger names and spaced code',(t)async{
  await t.binding.setSurfaceSize(const Size(320,640));addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(MaterialApp(home:Scaffold(body:Center(child:RepaintBoundary(key:const ValueKey('preview580'),child:Ngelx567WaitingPanel(room:{...room579(),'capacity':4},uid:'a',canStart:true,busy:false,onInvite:(){},onStart:(){}))))));
  await t.pump();expect(t.takeException(),isNull);
  final code=t.widget<Text>(find.byKey(const ValueKey('ludo-waiting-code')));expect(code.style!.fontSize,greaterThanOrEqualTo(20));expect(code.style!.letterSpacing,3);
  await preview580(t,'waiting-four-seats-320');await t.pumpWidget(const SizedBox());
 });
 testWidgets('winner celebration covers screen then leaves results after four seconds',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  final room={...room579(),'status':'finished','winner':2};
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('preview580'),child:Ngelx565LudoRoom(id:'270565',userId:'a',initial:room,request:(_)async=>room))));
  await t.pump(const Duration(milliseconds:900));expect(find.byKey(const ValueKey('ludo-fullscreen-victory')),findsOneWidget);
  await preview580(t,'winner-celebration');await t.pump(const Duration(milliseconds:3200));
  expect(find.byKey(const ValueKey('ludo-fullscreen-victory')),findsNothing);expect(find.text('Lobiye dön'),findsOneWidget);
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
}
