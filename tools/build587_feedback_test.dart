import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';
import 'build583_feedback_test.dart' as fixtures;

void main(){
 setUpAll(()async{
  final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
  final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
  final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
  if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
 });
 setUp(()=>SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false}));
 testWidgets('horizontal gifts show prices and send once without confirmation',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  var room=fixtures.room583();var sends=0;
  final pending=Completer<Map<String,dynamic>>();
  await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='wallet')return {'blockedUsers':[]};
   if(b['action']=='gift_catalog')return {'gifts':{
    'rose':{'emoji':'🌹','label':'Gül','chips':20},'heart':{'emoji':'❤️','label':'Kalp','chips':40},
    'crown':{'emoji':'👑','label':'Taç','chips':100},'coffee':{'emoji':'☕','label':'Kahve','chips':15}}};
   if(b['action']=='gift'){sends++;expect(b['to'],'b');expect(b['kind'],'heart');return pending.future;}
   return room;
  }))));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-player-b')));await t.pump();await t.pump(const Duration(milliseconds:350));
  expect(t.getTopLeft(find.text('Gül')).dy,t.getTopLeft(find.text('Kalp')).dy);
  expect(find.text('40 çip'),findsOneWidget);await fixtures.shot583(t,'build587-horizontal-gifts');
  await t.tap(find.byKey(const ValueKey('ludo-gift-heart')));await t.pump();
  expect(sends,1);expect(find.text('Hediye gönderilsin mi?'),findsNothing);
  await t.pump(const Duration(milliseconds:500));expect(sends,1);
  room={...room,'revision':2,'gifts':[{'from':'a','to':'b','fromName':'Alihan','toName':'Ahsen Can','kind':'heart','emoji':'❤️','at':DateTime.now().millisecondsSinceEpoch}]};
  pending.complete(room);await t.pump();await t.pump(const Duration(milliseconds:300));
  expect(find.byType(Ngelx587Hearts),findsOneWidget);await fixtures.shot583(t,'build587-heart-flight');
  await t.pump(const Duration(seconds:3));expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('compact chat has replacement emojis and scrolls old messages',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  final room=fixtures.room583();room['chat']=[for(var i=0;i<15;i++){'uid':'b','name':'Ahsen','text':'Mesaj $i','at':DateTime.now().millisecondsSinceEpoch-20000+i}];
  await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(_)async=>room))));
  await t.pump();await t.tap(find.text('Sohbet'));await t.pump();await t.pump(const Duration(milliseconds:350));
  expect(t.getSize(find.byType(Ngelx570ChatPanel)).height,lessThanOrEqualTo(280));
  for(final e in ['😂','😢','👏','❤️','😡'])expect(find.text(e),findsOneWidget);
  expect(find.text('🎲'),findsNothing);expect(find.text('🎉'),findsNothing);
  expect(find.text('Ahsen: Mesaj 14'),findsOneWidget);
  await t.drag(find.byKey(const ValueKey('ludo-chat-history')),const Offset(0,500));await t.pumpAndSettle();
  expect(find.text('Ahsen: Mesaj 0'),findsOneWidget);await fixtures.shot583(t,'build587-compact-chat');
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('comment strip is below the board and above the composer controls',(t)async{
  await t.binding.setSurfaceSize(const Size(393,852));addTearDown(()=>t.binding.setSurfaceSize(null));
  var room=fixtures.room583();
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='chat')room={...room,'revision':2,'chat':[{'uid':'a','name':'Alihan','text':b['text'],'at':DateTime.now().millisecondsSinceEpoch}]};return room;
  })));
  await t.pump();await t.tap(find.text('Sohbet'));await t.pump();await t.pump(const Duration(milliseconds:350));
  await t.enterText(find.byKey(const ValueKey('ludo-chat-input')),'selam');await t.tap(find.byIcon(Icons.send_rounded));
  await t.pump();await t.pump(const Duration(milliseconds:400));
  final strip=t.getRect(find.byKey(const ValueKey('ludo-bottom-comments')));
  final board=t.getRect(find.byType(Ngelx565LudoBoard));
  expect(strip.top,greaterThanOrEqualTo(board.bottom));
  expect(strip.bottom,lessThanOrEqualTo(t.getTopLeft(find.text('Sohbet')).dy));
  expect(find.text('Alihan: selam'),findsOneWidget);expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('hearts animate once for fresh messages and never replay history',(t)async{
  final now=DateTime.now().millisecondsSinceEpoch;
  Map<String,dynamic> data={'chat':[{'uid':'a','text':'❤️','at':now-20000}],'gifts':[]};
  Widget view()=>MaterialApp(home:Scaffold(body:Ngelx587Hearts(room:data)));
  final paint=find.descendant(of:find.byType(Ngelx587Hearts),matching:find.byType(CustomPaint));
  await t.pumpWidget(view());expect(paint,findsNothing);
  data={'chat':[{'uid':'a','text':'❤️','at':now}],'gifts':[]};
  await t.pumpWidget(view());await t.pump(const Duration(milliseconds:100));expect(paint,findsOneWidget);
  await t.pump(const Duration(seconds:3));expect(paint,findsNothing);
  await t.pumpWidget(view());await t.pump();expect(paint,findsNothing);
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('PK ribbon clamps scores, retains countdown and fits narrow phones',(t)async{
  await t.binding.setSurfaceSize(const Size(320,700));addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:const MaterialApp(home:Scaffold(backgroundColor:Colors.black,body:SafeArea(child:Ngelx587PkRibbon(selfScore:167,opponentScore:86,remaining:178,selfName:'Alihan',opponentName:'Ahsen'))))));
  expect(find.text('167'),findsOneWidget);expect(find.text('86'),findsOneWidget);expect(find.text('02:58'),findsOneWidget);
  expect(t.takeException(),isNull);await fixtures.shot583(t,'build587-pk-score');await t.pumpWidget(const SizedBox());
 });
}
