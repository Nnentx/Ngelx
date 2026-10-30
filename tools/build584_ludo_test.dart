import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/main.dart';
import 'build583_feedback_test.dart' as fixtures;

void main(){
 setUp(()=>SharedPreferences.setMockInitialValues({'ngelx_ludo_sound':false}));
 for(final count in [2,3,4])for(var seat=0;seat<4;seat++){
  if(count==2&&seat!=0&&seat!=2||count==3&&seat==3)continue;
  testWidgets('$count players seat $seat sees GO despite previous six, then real rolled six',(t)async{
   await t.binding.setSurfaceSize(const Size(393,852));
   addTearDown(()=>t.binding.setSurfaceSize(null));
   var room=fixtures.room583(players:count);
   if(count==2)room['players'][1]['seat']=2;
   room={...room,'turn':seat,'lastRoll':{'seat':seat,'value':6,'revision':0}};
   final uid=(room['players'] as List).firstWhere((p)=>p['seat']==seat)['uid'] as String;
   var rolls=0;
   await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'584584',initial:room,userId:uid,request:(b)async{
    if(b['action']=='roll'){
     rolls++;room={...room,'revision':2,'dice':6,'lastRoll':{'seat':seat,'value':6,'revision':2}};
    }
    return room;
   })));
   await t.pump();
   final main=find.descendant(of:find.byKey(const ValueKey('ludo-dice')),matching:find.byType(Ngelx567Dice));
   final avatar=find.descendant(of:find.byKey(const ValueKey('ludo-dice')),matching:find.byType(Ngelx567Dice));
   expect(t.widget<Ngelx567Dice>(main).value,isNull);
   expect(t.widget<Ngelx567Dice>(avatar).value,isNull);
   await t.tap(find.byKey(const ValueKey('ludo-dice')));await t.pump();
   expect(rolls,1);expect(t.widget<Ngelx567Dice>(main).value,6);
   expect(t.widget<Ngelx567Dice>(avatar).value,6);
   expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
  });
 }
 for(final size in [const Size(320,640),const Size(393,852),const Size(430,932),const Size(852,393)]){
  testWidgets('expanded table fits $size with accessible controls and pawn taps',(t)async{
   await t.binding.setSurfaceSize(size);addTearDown(()=>t.binding.setSurfaceSize(null));
   final room=fixtures.room583(players:2,dice:6);room['players'][1]['seat']=2;
   var moves=0;
   await t.pumpWidget(RepaintBoundary(key:const ValueKey('capture583'),child:MaterialApp(home:Ngelx565LudoRoom(id:'584584',initial:room,userId:'a',request:(b)async{
    if(b['action']=='move')moves++;return room;
   }))));await t.pump();await t.pump(const Duration(milliseconds:250));
   final frame=t.getRect(find.byKey(const ValueKey('ludo-expanded-board')));
   expect(frame.left,greaterThanOrEqualTo(0));expect(frame.right,lessThanOrEqualTo(size.width));
   expect(frame.top,greaterThanOrEqualTo(0));expect(frame.bottom,lessThan(size.height));
   expect(frame.height,greaterThanOrEqualTo(frame.width));
   expect(frame.height,lessThanOrEqualTo(frame.width*1.101));
   if(size.height>800)expect(frame.height,greaterThan(frame.width*1.05));
   // FittedBox must map a visibly stretched pawn back to its original hit target.
   final turns=3,p=ngelx565Rotate(ngelx565TokenPoint(0,0,-1),turns);
   await t.tapAt(Offset(frame.left+(p.dx+.5)*frame.width/15,frame.top+(p.dy+.5)*frame.height/15));
   await t.pump();expect(moves,1);
   expect(find.byKey(const ValueKey('ludo-dice')).hitTestable(),findsOneWidget);
   expect(t.takeException(),isNull);
   if(size==const Size(393,852))await fixtures.shot583(t,'ludo584-expanded-two-players');
   await t.pumpWidget(const SizedBox());
  });
 }
}
