import 'dart:async';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';

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
