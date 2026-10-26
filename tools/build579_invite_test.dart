import 'dart:async';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';

Map<String,dynamic> room579()=>{
 'id':'270565','owner':'a','capacity':2,'status':'waiting','revision':1,
 'mode':'power','team':false,'chips':5000,'gems':0,
 'players':[{'uid':'a','seat':0,'name':'A'},{'uid':'b','seat':2,'name':'B'}],
 'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),
 'power':List.generate(4,(_)=>{'control':1,'double':1,'shield':1}),
 'turn':0,'dice':null,'deadline':0,'chat':[],
 // Deliberately no powerTiles: this previously froze the UI synchronously.
};
Future<void> frames579(WidgetTester t)async{
 for(var i=0;i<8;i++){await t.pump(const Duration(milliseconds:100));}
}
void main(){
 setUp(()=>SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false}));
 test('mutation waits for in-flight poll and uses its latest revision',()async{
  final pending=Completer<Map<String,dynamic>>();final calls=<Map<String,dynamic>>[];
  final game=Ngelx567RoomController(id:'270565',uid:'a',initial:room579(),request:(b){
   calls.add(Map.of(b));
   return b['action']=='sync'?pending.future:Future.value({...room579(),'revision':3});
  });
  final poll=game.sync();final action=game.perform('auto',{'enabled':true});
  expect(calls.length,1);pending.complete({...room579(),'revision':2});
  await poll;expect(await action,true);expect(calls.last['revision'],2);expect(calls.last['action'],'auto');game.dispose();
 });
 test('Auto/bot sync revision conflicts recover without reconnect warning',()async{
  var attempts=0;
  final game=Ngelx567RoomController(id:'270565',uid:'a',initial:room579(),request:(b)async{
   attempts++;if(attempts<3)throw const Ngelx567Failure('state_changed','stale');
   return {...room579(),'revision':3,'autoSeats':{'0':true}};
  });
  await game.sync();expect(attempts,3);expect(game.room['revision'],3);expect(game.room['autoSeats'],{'0':true});
  expect(game.error,isEmpty);expect(game.reconnectNeeded579,false);game.dispose();
 });
 test('only repeated transport failures show reconnect; a successful sync clears it',()async{
  var attempts=0;
  final game=Ngelx567RoomController(id:'270565',uid:'a',initial:room579(),request:(b)async{
   attempts++;if(attempts<=2)throw const Ngelx567Failure('connection','offline');return room579();
  });
  await game.sync();expect(game.reconnectNeeded579,false);
  await game.sync();expect(game.reconnectNeeded579,true);
  await game.sync();expect(game.reconnectNeeded579,false);expect(game.error,isEmpty);game.dispose();
 });
 test('a stale manual move refreshes the board without replaying the move or claiming disconnection',()async{
  final calls=<String>[];
  final game=Ngelx567RoomController(id:'270565',uid:'a',initial:room579(),request:(b)async{
   calls.add(b['action'] as String);if(b['action']=='move')throw const Ngelx567Failure('state_changed','stale');
   return {...room579(),'revision':2};
  });
  expect(await game.perform('move',{'token':0}),false);expect(calls,['move','sync']);
  expect(game.room['revision'],2);expect(game.reconnectNeeded579,false);expect(game.error,isEmpty);game.dispose();
 });
 test('missing Power map is a bounded paint for every orientation, including loading/classic',(){
  for(final power in [false,true])for(var turns=0;turns<4;turns++){
   final recorder=ui.PictureRecorder(),canvas=Canvas(recorder);
   Ngelx565BoardPainter(turns:turns,power:power).paint(canvas,const Size(300,300));
   recorder.endRecording().dispose();
  }
 });
 testWidgets('visible invite Join opens room and Back works while join request is pending',(t)async{
  final pending=Completer<Map<String,dynamic>>();var joins=0;
  await t.binding.setSurfaceSize(const Size(393,852));
  addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(MaterialApp(home:Builder(builder:(context)=>Scaffold(body:Column(children:[
   const Text('Chat579'),Ngelx565LudoInviteCard(id:'270565',mine:false,onLongPress:(){},onJoin:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(
    id:'270565',userId:'a',request:(body){joins++;expect(body['action'],'join');return pending.future;},
   )))),
  ])))));
  await t.tap(find.byKey(const ValueKey('ludo-invite-join')));await frames579(t);
  expect(joins,1);expect(find.byType(Ngelx565LudoRoom),findsOneWidget);expect(t.takeException(),isNull);
  await t.tap(find.byKey(const ValueKey('ludo-back')));await frames579(t);await frames579(t);
  expect(find.byType(Ngelx565LudoRoom),findsNothing);expect(find.text('Chat579'),findsOneWidget);
  pending.complete(room579());await frames579(t);expect(t.takeException(),isNull);
 });
 testWidgets('joined room with no pickup map paints and exits back to chat',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));
  addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(MaterialApp(home:Builder(builder:(context)=>Scaffold(body:TextButton(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(
   id:'270565',userId:'a',request:(body)async=>body['action']=='leave'?{...room579(),'status':'closed','revision':2}:room579(),
  ))),child:const Text('Open579'))))));
  await t.tap(find.text('Open579'));await frames579(t);await frames579(t);
  expect(find.byType(Ngelx565LudoRoom),findsOneWidget);expect(t.takeException(),isNull);
  await t.tap(find.byKey(const ValueKey('ludo-back')));await frames579(t);
  await t.tap(find.byKey(const ValueKey('confirm-ludo-leave')));await frames579(t);await frames579(t);
  expect(find.text('Open579'),findsOneWidget);expect(find.byType(Ngelx565LudoRoom),findsNothing);expect(t.takeException(),isNull);
 });
}
