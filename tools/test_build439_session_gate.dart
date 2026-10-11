import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/build439_session_gate.dart';
void main(){
  testWidgets('root recreation and stale auth events use the current session',(tester)async{
    final events=StreamController<String?>.broadcast();
    String? current='old-account';
    Widget gate(Key key)=>MaterialApp(home:NgelXSessionGate<String>(key:key,
      changes:events.stream,current:()=>current,
      builder:(_,session)=>Text(session??'login')));
    await tester.pumpWidget(gate(const ValueKey(1)));
    expect(find.text('old-account'),findsOneWidget);
    current=null;
    await tester.pumpWidget(gate(const ValueKey(2)));
    expect(find.text('login'),findsOneWidget);
    events.add('old-account');await tester.pumpAndSettle();
    expect(find.text('login'),findsOneWidget);
    current='new-account';events.add(null);await tester.pumpAndSettle();
    expect(find.text('new-account'),findsOneWidget);
    current=null;events.add(null);await tester.pumpAndSettle();
    expect(find.text('login'),findsOneWidget);
    await tester.pumpWidget(const SizedBox());
    events.add('old-account');await tester.pumpAndSettle();
    expect(tester.takeException(),isNull);
    await events.close();
  });
}
