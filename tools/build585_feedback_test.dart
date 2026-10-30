import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import 'build583_feedback_test.dart' as fixtures;

void main(){
 setUpAll(()async{
  final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
  final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
  final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
  if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
 });
 setUp((){
  SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false});
  TestWidgetsFlutterBinding.ensureInitialized().handleAppLifecycleStateChanged(AppLifecycleState.resumed);
 });
 test('six steps now take 660ms and one step still has a visible animation',(){
  expect(ngelx585PawnDuration(0,6),const Duration(milliseconds:660));
  expect(ngelx585PawnDuration(0,1),const Duration(milliseconds:180));
 });
 testWidgets('one legal pawn moves without tapping, only once during a slow response',(t)async{
  var room=fixtures.room583(dice:1);room['tokens'][0]=[0,-1,-1,-1];
  var moves=0;final pending=Completer<Map<String,dynamic>>();
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='move'){moves++;expect(b['token'],0);return pending.future;}
   return room;
  })));
  await t.pump();await t.pump(const Duration(milliseconds:250));expect(moves,1);
  await t.pump(const Duration(seconds:2));expect(moves,1);
  pending.complete({...room,'revision':2,'dice':null,'turn':1});await t.pump();
  await t.pumpWidget(const SizedBox());expect(t.takeException(),isNull);
 });
 testWidgets('a newly rolled die automatically advances its only legal pawn',(t)async{
  var room=fixtures.room583();room['tokens'][0]=[0,-1,-1,-1];var rolls=0,moves=0;
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='roll'){rolls++;room={...room,'revision':2,'dice':1};}
   if(b['action']=='move'){moves++;expect(b['token'],0);room={...room,'revision':3,'dice':null,'turn':1};}
   return room;
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();
  await t.pump(const Duration(milliseconds:250));expect(rolls,1);expect(moves,1);
  await t.pumpWidget(const SizedBox());expect(t.takeException(),isNull);
 });
 testWidgets('multiple legal pawns wait for selection and spectators never move',(t)async{
  for(final watch in [false,true]){
   final room=fixtures.room583(dice:1);room['tokens'][0]=watch?[0,-1,-1,-1]:[0,3,-1,-1];var moves=0;
   await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',watch:watch,request:(b)async{
    if(b['action']=='move')moves++;return room;
   })));
   await t.pump();await t.pump(const Duration(seconds:2));expect(moves,0);
   await t.pumpWidget(const SizedBox());
  }
 });
 testWidgets('backgrounding during the short delay cancels the automatic choice',(t)async{
  final initial=fixtures.room583(dice:1);initial['tokens'][0]=[0,-1,-1,-1];var moves=0;
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:initial,userId:'a',request:(b)async{
   if(b['action']=='move')moves++;return {...initial,'revision':2,'turn':1};
  })));
  await t.pump();t.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
  await t.pump(const Duration(milliseconds:300));expect(moves,0);
  await t.pumpWidget(const SizedBox());
  t.binding.handleAppLifecycleStateChanged(AppLifecycleState.resumed);
 });
 for(final size in [const Size(320,640),const Size(393,852),const Size(852,393)]){
  testWidgets('clean controls on $size keep avatar dice, Auto, chat and board usable',(t)async{
   await t.binding.setSurfaceSize(size);addTearDown(()=>t.binding.setSurfaceSize(null));
   var room=fixtures.room583();var rolls=0;
   await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
    if(b['action']=='roll'){rolls++;room={...room,'dice':6,'revision':2};}return room;
   }))));await t.pump();
   expect(find.byType(Ngelx570Clock),findsNothing);
   expect(find.byKey(const ValueKey('ludo-main-dice')),findsNothing);
   expect(find.text('İyi oyunlar'),findsNothing);expect(find.text('Güzel hamle'),findsNothing);
   expect(find.byKey(const ValueKey('ludo-auto-toggle')).hitTestable(),findsOneWidget);
   expect(find.text('Sohbet').hitTestable(),findsOneWidget);
   await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();expect(rolls,1);
   expect(find.byKey(const ValueKey('ludo-expanded-board')),findsOneWidget);
   expect(t.takeException(),isNull);
   if(size==const Size(393,852))await fixtures.shot583(t,'ludo585-clean-controls');
   await t.pumpWidget(const SizedBox());
  });
 }
}
