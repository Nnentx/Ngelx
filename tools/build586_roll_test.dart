import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';
import 'build583_feedback_test.dart' as fixtures;

void main(){
 setUp((){
  SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false});
  TestWidgetsFlutterBinding.ensureInitialized().handleAppLifecycleStateChanged(AppLifecycleState.resumed);
 });
 for(final faces in [[1,3,5],[2,6],[6]]){
  testWidgets('one GO gesture completes opening sequence $faces without more taps',(t)async{
   var room=fixtures.room583(),rolls=0;
   await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
    if(b['action']=='roll'){
     final face=faces[rolls++];final count=(room['openingRolls'] as int? ?? 0)+1;
     room={...room,'revision':rolls+1,'dice':face==6?6:null,'openingRolls':face==6?count-1:count<3?count:0,
      'turn':face!=6&&count==3?1:0,'lastRoll':{'seat':0,'value':face,'revision':rolls+1}};
    }return room;
   })));
   await t.pump();await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();
   expect(rolls,1);
   for(var i=1;i<faces.length;i++){
    final dice=find.descendant(of:find.byKey(const ValueKey('ludo-dice')),matching:find.byType(Ngelx567Dice));
    expect(t.widget<Ngelx567Dice>(dice).value,faces[i-1]);
    await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();expect(rolls,i);
    await t.pump(const Duration(milliseconds:370));await t.pump();expect(rolls,i+1);
   }
   await t.pump(const Duration(milliseconds:400));expect(rolls,faces.length);
   if(faces.last==6)expect(room['dice'],6);else expect(room['turn'],1);
   expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
  });
 }
 testWidgets('a single gesture retries rejected revisions without rerolling an accepted result',(t)async{
  var room=fixtures.room583(),requests=0;
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='roll'){
    requests++;room={...room,'revision':requests+1};
    if(requests<3)throw const Ngelx567Failure('state_changed','stale');
    room={...room,'dice':6,'lastRoll':{'seat':0,'value':6,'revision':requests+1}};
   }return room;
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();
  expect(requests,3);expect(room['dice'],6);
  await t.pump(const Duration(seconds:1));expect(requests,3);
  await t.pumpWidget(const SizedBox());
 });
 testWidgets('tapping GO while another action is busy queues exactly one roll',(t)async{
  var room=fixtures.room583(),rolls=0;final pending=Completer<Map<String,dynamic>>();
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='auto')return pending.future;
   if(b['action']=='roll'){rolls++;room={...room,'revision':3,'dice':6,'autoSeats':{},'lastRoll':{'seat':0,'value':6,'revision':3}};}
   return room;
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-auto-toggle')));await t.pump();
  await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();expect(rolls,0);
  pending.complete({...room,'revision':2,'autoSeats':{'0':true}});await t.pump();await t.pump();
  expect(rolls,1);await t.pumpWidget(const SizedBox());
 });
 testWidgets('the padded die hit area accepts a tap outside its visible square',(t)async{
  final room=fixtures.room583();var rolls=0;
  await t.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(width:393,height:620,child:Ngelx567Table(room:room,seat:0,uid:'a',enabled:true,busy:false,onToken:(_){},onRoll:()=>rolls++)))));
  await t.pump();final target=t.getRect(find.byKey(const ValueKey('ludo-dice')));
  expect(target.width,48);await t.tapAt(Offset(target.left+2,target.center.dy));await t.pump();expect(rolls,1);
  expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('backgrounding cancels remaining opening attempts',(t)async{
  var room=fixtures.room583(),rolls=0;
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583583',initial:room,userId:'a',request:(b)async{
   if(b['action']=='roll'){rolls++;room={...room,'revision':2,'openingRolls':1,'lastRoll':{'seat':0,'value':2,'revision':2}};}return room;
  })));
  await t.pump();await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();expect(rolls,1);
  t.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
  await t.pump(const Duration(seconds:1));expect(rolls,1);
  await t.pumpWidget(const SizedBox());t.binding.handleAppLifecycleStateChanged(AppLifecycleState.resumed);
 });
}
