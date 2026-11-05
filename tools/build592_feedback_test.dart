import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';
import 'build583_feedback_test.dart' as f;
void main(){
 setUpAll(()async{
  final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
 });
 setUp((){
  SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false});
  TestWidgetsFlutterBinding.ensureInitialized().handleAppLifecycleStateChanged(AppLifecycleState.resumed);
 });
 test('manual move is sent before pending poll, and late poll cannot roll state back',()async{
  final poll=Completer<Map<String,dynamic>>();var calls=0;final room=f.room583(players:4,dice:6);
  final game=Ngelx567RoomController(id:'583583',uid:'a',initial:room,request:(b)async{
   if(b['action']=='sync')return poll.future;
   calls++;return {...room,'revision':2,'dice':null};
  });
  final syncing=game.sync();expect(await game.perform('move',{'token':0}),isTrue);expect(calls,1);
  poll.complete({...room,'revision':1});await syncing;expect(game.room['revision'],2);game.dispose();
 });
 test('chat-only revision conflict retries one legal move with the same receipt',()async{
  var moves=0;final keys=<String>[];final room=f.room583(players:4,dice:6);
  final game=Ngelx567RoomController(id:'583583',uid:'a',initial:room,request:(b)async{
   if(b['action']=='sync')return {...room,'revision':2};
   moves++;keys.add(b['requestId'] as String);
   if(moves==1)throw const Ngelx567Failure('state_changed','stale');
   return {...room,'revision':3,'dice':null};
  });
  expect(await game.perform('move',{'token':0}),isTrue);expect(moves,2);expect(keys.toSet().length,1);game.dispose();
 });
 testWidgets('tap on a pawn while the accepted roll is loading is queued once',(t)async{
  var room=f.room583(players:4),moves=0;final roll=Completer<Map<String,dynamic>>();
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='roll')return roll.future;
   if(b['action']=='move'){moves++;return {...room,'revision':3,'dice':null};}
   return room;
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();
  await t.tap(find.byKey(const ValueKey('ludo-0-0')));await t.pump();expect(moves,0);
  room={...room,'revision':2,'dice':6,'lastRoll':{'seat':0,'value':6,'revision':2}};
  roll.complete(room);await t.pump();await t.pump();expect(moves,1);
  await t.pumpWidget(const SizedBox());
 });
 test('friends can start with two players while teams wait for four',(){
  final room=f.room583(players:2);room['status']='waiting';
  final game=Ngelx567RoomController(id:'583583',uid:'a',initial:room,request:(_)async=>room);
  expect(game.canStart,isTrue);room['team']=true;expect(game.canStart,isFalse);
  room['players']=f.room583(players:4)['players'];expect(game.canStart,isTrue);
  expect(ngelx558Verified('zvPSPlQvqIYKNlkFL6BqrIMutip2'),isTrue);game.dispose();
 });
 test('pawn animation takes slightly longer without delaying server input',(){
  expect(ngelx585PawnDuration(0,1),const Duration(milliseconds:145));
  expect(ngelx585PawnDuration(0,6),const Duration(milliseconds:408));
 });
 testWidgets('group card stays joinable with two of four seats occupied',(t)async{
  await t.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx565LudoInviteCard(id:'583583',mine:false,onLongPress:(){},onJoin:(){},inviteToken:'a'*64,request:(_)async=>{
   'status':'pending','capacity':4,'joined':2,'expiresAt':DateTime.now().millisecondsSinceEpoch+120000,'serverNow':DateTime.now().millisecondsSinceEpoch,
  }))));await t.pump();
  expect(t.widget<FilledButton>(find.byKey(const ValueKey('ludo-invite-join'))).onPressed,isNotNull);
  expect(find.text('2/4 oyuncu · Katılabilirsin'),findsOneWidget);await t.pumpWidget(const SizedBox());
 });
 testWidgets('all sixteen actual gift images fit the mobile grid',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  const kinds=['flower','heart','crown','coffee','thumbs_up','tomato','pizza','bucket','clock','flame','rooster','slipper','pan','plunger','egg','balloon'];
  await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Scaffold(body:SafeArea(child:GridView.count(crossAxisCount:4,childAspectRatio:.75,children:[for(final kind in kinds)Column(children:[Ngelx587GiftArt(kind:kind,size:80),Text(kind)])]))))));
  await t.runAsync(()=>Future<void>.delayed(const Duration(milliseconds:150)));await t.pump();
  expect(find.byType(Image),findsNWidgets(16));expect(t.takeException(),isNull);await f.shot583(t,'build592-gift-images');await t.pumpWidget(const SizedBox());
 });
 for(final kind in ['flame','bucket','tomato','rooster','balloon'])testWidgets('$kind effect uses fresh receipt, sound once, and clears on deadline',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  var room=f.room583(players:4);final sounds=<String>[];
  Widget view()=>RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Scaffold(backgroundColor:const Color(0xFF193855),body:Stack(children:[const Center(child:Text('NgelX Ludo',style:TextStyle(color:Colors.white,fontSize:28))),Positioned.fill(child:Ngelx592GiftEffects(room:room,soundOn:true,playSound:(kind)async{sounds.add(kind);}))]))));
  await t.pumpWidget(view());await t.pump();expect(sounds,isEmpty);
  room={...room,'gifts':[{'from':'a','to':'b','kind':kind,'at':DateTime.now().millisecondsSinceEpoch}]};
  await t.pumpWidget(view());await t.pump();await t.pump(const Duration(milliseconds:1000));
  expect(find.byKey(ValueKey('ludo-effect-$kind')),findsOneWidget);expect(sounds,[kind]);
  await f.shot583(t,'build592-effect-$kind');await t.pumpWidget(view());await t.pump();expect(sounds,[kind]);
  await t.pump(ngelx592GiftDuration(kind));expect(find.byKey(ValueKey('ludo-effect-$kind')),findsNothing);
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('mute and backgrounding stop new gift sounds and clear active effects',(t)async{
  var room=f.room583(players:4);var soundOn=false;final sounds=<String>[];
  Widget view()=>MaterialApp(home:Scaffold(body:Ngelx592GiftEffects(room:room,soundOn:soundOn,playSound:(kind)async{sounds.add(kind);})));
  await t.pumpWidget(view());
  room={...room,'gifts':[{'from':'a','to':'b','kind':'rooster','at':DateTime.now().millisecondsSinceEpoch}]};
  await t.pumpWidget(view());await t.pump();expect(sounds,isEmpty);
  expect(find.byKey(const ValueKey('ludo-effect-rooster')),findsOneWidget);
  t.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);await t.pump();
  expect(find.byKey(const ValueKey('ludo-effect-rooster')),findsNothing);
  t.binding.handleAppLifecycleStateChanged(AppLifecycleState.resumed);soundOn=true;
  await t.pumpWidget(view());await t.pump();expect(sounds,isEmpty);
  room={...room,'gifts':[{'from':'a','to':'b','kind':'balloon','at':DateTime.now().millisecondsSinceEpoch+1}]};
  await t.pumpWidget(view());await t.pump();expect(sounds,['balloon']);
  await t.pumpWidget(const SizedBox());
 });
 test('flame covers exactly two seconds and all gift sounds have matching offline files',(){
  expect(ngelx592GiftDuration('flame'),const Duration(seconds:2));
  for(final kind in ['balloon','bucket','clock','coffee','crown','egg','flame','flower','heart','pan','pizza','plunger','rooster','slipper','thumbs_up','tomato']){
   expect(File(ngelx592GiftSound(kind)).existsSync(),isTrue,reason:kind);
  }
 });
}
