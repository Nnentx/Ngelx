import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';

Map<String,dynamic> room583({int players=3,int? dice})=>{
 'id':'583583','owner':'a','capacity':4,'status':'playing','revision':1,
 'mode':'classic','team':false,'chips':5317,'gems':0,
 'players':[for(var i=0;i<players;i++){'uid':['a','b','c','d'][i],'seat':i,'name':['Alihan','Ahsen Can','Rızgar Umut','Oyuncu'][i],'level':1}],
 'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),'power':List.generate(4,(_)=>{'control':1,'double':1,'shield':1}),
 'turn':0,'dice':dice,'deadline':DateTime.now().millisecondsSinceEpoch+15000,'chat':[],'gifts':[],
};
Future<void> shot583(WidgetTester t,String name)async{
 final boundary=t.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('capture583')));
 await t.runAsync(()async{final image=await boundary.toImage(pixelRatio:2);
  final data=await image.toByteData(format:ui.ImageByteFormat.png);
  Directory('test/screenshots').createSync(recursive:true);
  File('test/screenshots/$name.png').writeAsBytesSync(data!.buffer.asUint8List());image.dispose();});
}
void main(){
 setUp(()=>SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false}));
 test('gift receipts animate once, with no replay on entry or duplicate poll',(){
  final q=Ngelx583GiftQueue(),now=DateTime.now().millisecondsSinceEpoch;
  Map<String,dynamic> event(int at)=>{'from':'a','to':'b','kind':'rose','at':at};
  q.observe([event(now-200)],now);expect(q.pending,isEmpty);
  q.observe([event(now-200),event(now)],now);expect(q.pending.length,1);
  q.observe([event(now-200),event(now)],now);expect(q.pending.length,1);
  q.observe([event(now-20000)],now);expect(q.pending.length,1);
 });
 test('every rotated player can touch stacked legal stones outside tiny sprites',(){
  for(var seat=0;seat<4;seat++){
   final room=room583(players:4,dice:6);room['turn']=seat;room['tokens'][seat]=[0,0,-1,-1];
   const cell=24.0;final p=ngelx565Rotate(ngelx565TokenPoint(seat,0,0),(3-seat+4)%4);
   final point=Offset((p.dx+.5)*cell,(p.dy+.5)*cell);
   expect(ngelx583HitToken(room,seat,cell,point),isIn([0,1]));
   expect(ngelx583HitToken(room,seat,cell,point+const Offset(0,15)),isIn([0,1]));
   room['dice']=1;expect(ngelx583HitToken(room,seat,cell,const Offset(350,350)),isNull);
  }
 });
 testWidgets('GO rolls on first press and retries only a known rejected revision',(t)async{
  var room=room583();var rolls=0,moves=0;
  Future<Map<String,dynamic>> request(Map<String,dynamic> b)async{
   if(b['action']=='roll'){
    rolls++;
    if(rolls==1){room={...room,'revision':2};throw const Ngelx567Failure('state_changed','stale');}
    room={...room,'revision':3,'dice':6,'lastRoll':{'seat':0,'value':6,'revision':3}};
   }
   if(b['action']=='move')moves++;
   return room;
  }
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:request)));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-main-dice')));
  await t.pump();await t.pump(const Duration(milliseconds:500));
  expect(rolls,2);expect(room['dice'],6);expect(moves,0);expect(t.takeException(),isNull);
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('one GO gesture with slow response never sends a duplicate roll',(t)async{
  final pending=Completer<Map<String,dynamic>>();var rolls=0;final room=room583();
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b){
   if(b['action']=='roll'){rolls++;return pending.future;}return Future.value(room);
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-main-dice')));await t.pump();
  await t.tap(find.byKey(const ValueKey('ludo-main-dice')));await t.pump();expect(rolls,1);
  pending.complete({...room,'revision':2,'dice':6});await t.pump();expect(rolls,1);
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('a stalled request releases the board rather than locking busy forever',(t)async{
  final g=Ngelx567RoomController(id:'583583',uid:'a',initial:room583(),request:(_)=>Completer<Map<String,dynamic>>().future);
  final done=g.perform('roll');expect(g.busy,true);
  await t.pump(const Duration(seconds:13));expect(await done,false);expect(g.busy,false);g.dispose();
 });
 for(final players in [2,3,4])testWidgets('$players player board fills available phone width and renders six',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  final room=room583(players:players,dice:6);
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('capture583'),child:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(_)async=>room))));
  await t.pump();await t.pump(const Duration(milliseconds:500));
  expect(t.getSize(find.byType(Ngelx565LudoBoard)).width,greaterThan(370));
  expect(find.byWidgetPredicate((w)=>w is Ngelx567Dice&&w.value==6),findsWidgets);
  expect(t.takeException(),isNull);await shot583(t,'ludo-$players-players');
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('gift names and prices are dark and readable and send as a flight',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  var room=room583();var gifts=0;
  Future<Map<String,dynamic>> request(Map<String,dynamic> b)async{
   if(b['action']=='wallet')return {'blockedUsers':[]};
   if(b['action']=='gift_catalog')return {'gifts':{'rose':{'emoji':'🌹','label':'Gül','chips':20}}};
   if(b['action']=='gift'){gifts++;room={...room,'revision':2,'gifts':[{'from':'a','to':'b','fromName':'Alihan','toName':'Ahsen Can','kind':'rose','emoji':'🌹','at':DateTime.now().millisecondsSinceEpoch}]};}
   return room;
  }
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('capture583'),child:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:request))));await t.pump();
  await t.tap(find.byKey(const ValueKey('ludo-player-b')));await t.pump();await t.pump(const Duration(milliseconds:300));
  expect(t.widget<Text>(find.text('Gül')).style!.color,const Color(0xFF27204C));
  expect(find.text('20 çip'),findsOneWidget);await shot583(t,'gift-readable');
  await t.tap(find.text('Gül'));await t.pump();await t.pump(const Duration(milliseconds:350));
  await t.tap(find.text('Gönder'));await t.pump();await t.pump(const Duration(milliseconds:400));
  expect(gifts,1);expect(find.text('Hediye gönderildi 🎁'),findsNothing);
  expect(find.text('🌹'),findsOneWidget);await shot583(t,'gift-flight');
  await t.pump(const Duration(seconds:2));expect(find.text('🌹'),findsNothing);
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 test('last server six remains visible after turn changes',(){
  expect(ngelx570ShownDice({...room583(),'turn':1,'lastRoll':{'seat':0,'value':6}}),6);
 });
}
