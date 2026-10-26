import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

void main() {
  testWidgets('Auto button can turn off again and shows a green check only while active',
      (tester) async {
    bool active=true;
    int pressed=0;
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:StatefulBuilder(
      builder:(context,set)=>Center(child:Ngelx575AutoBadge(
        enabled:active,onPressed:(){pressed++;set(()=>active=!active);},
      )),
    ))));
    expect(find.byKey(const ValueKey('ludo-auto-toggle')),findsOneWidget);
    expect(find.byIcon(Icons.check_circle),findsOneWidget);
    await tester.tap(find.byKey(const ValueKey('ludo-auto-toggle')));
    await tester.pump();
    expect(pressed,1);
    expect(find.byIcon(Icons.autorenew_rounded),findsOneWidget);
    await tester.tap(find.byKey(const ValueKey('ludo-auto-toggle')));
    await tester.pump();
    expect(pressed,2);
    expect(find.byIcon(Icons.check_circle),findsOneWidget);
  });

  testWidgets('server-confirmed chip balance animates to updated amount', (tester) async {
    await tester.pumpWidget(const MaterialApp(home:Scaffold(
      body:Center(child:Ngelx575AnimatedBalance(amount:15)),
    )));
    await tester.pumpAndSettle();
    expect(find.text('15'),findsOneWidget);
    await tester.pumpWidget(const MaterialApp(home:Scaffold(
      body:Center(child:Ngelx575AnimatedBalance(amount:45)),
    )));
    await tester.pumpAndSettle();
    expect(find.text('45'),findsOneWidget);
  });

  testWidgets('tapping another player avatar opens its profile callback', (tester) async {
    String? seen;
    final room=<String,dynamic>{
      'id':'754321','status':'playing','capacity':2,'mode':'classic',
      'players':[
        {'uid':'a','seat':0,'name':'Sen','photo':''},
        {'uid':'b','seat':2,'name':'Rakip','photo':''},
      ],
      'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),
      'turn':0,'dice':null,'deadline':0,'revision':1,
    };
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:Center(
      child:SizedBox(width:380,height:520,child:Ngelx567Table(
        room:room,seat:0,uid:'a',enabled:true,busy:false,
        onToken:(_){},onRoll:(){},
        onPlayerTap:(p)=>seen=p['uid']?.toString(),
      )),
    ))));
    await tester.pump();
    expect(find.byKey(const ValueKey('ludo-player-b')),findsOneWidget);
    await tester.tap(find.byKey(const ValueKey('ludo-player-b')));
    await tester.pump();
    expect(seen,'b');
  });

  for(final width in [320.0,360.0,393.0,440.0]) {
    testWidgets('wallet and compact Auto controls fit ${width.toInt()}px mobile width',
        (tester) async {
      tester.view.physicalSize=Size(width,740);
      tester.view.devicePixelRatio=1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(
        width:width,child:Column(children:[
          Ngelx573WalletBar(room:{'chips':1250,'gems':5}),
          const SizedBox(height:10),
          Row(children:[
            const Ngelx575AutoBadge(enabled:true,onPressed:null),
            const SizedBox(width:8),
            Expanded(child:Text('10',textAlign:TextAlign.center)),
            const SizedBox(width:12),
            const Icon(Icons.casino_rounded),
          ]),
        ]),
      ))));
      await tester.pumpAndSettle();
      expect(tester.takeException(),isNull);
      expect(find.text('1250'),findsOneWidget);
      expect(find.byKey(const ValueKey('ludo-auto-toggle')),findsOneWidget);
    });
  }
}
