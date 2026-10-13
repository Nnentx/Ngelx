import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/main.dart';

void main(){
  testWidgets('live composer retains focus and draft when keyboard and controls change', (tester)async{
    final controller=TextEditingController(),focus=FocusNode(),key=GlobalKey();
    final stream=const Stream<DocumentSnapshot<Map<String,dynamic>>>.empty();
    Widget shell(double inset,bool tools)=>MaterialApp(home:MediaQuery(data:MediaQueryData(viewInsets:EdgeInsets.only(bottom:inset)),child:Scaffold(resizeToAvoidBottomInset:false,body:Column(children:[
      Ngelx453LiveComposer(key:key,controller:controller,focus:focus,stream:stream,host:true,uid:'host',send:()async{}),
      if(tools)const Text('Controls'),
    ]))));
    await tester.pumpWidget(shell(0,true));await tester.tap(find.byType(TextField));await tester.enterText(find.byType(TextField),'Yayından merhaba');
    await tester.pumpWidget(shell(300,false));await tester.pump();
    expect(focus.hasFocus,isTrue);expect(controller.text,'Yayından merhaba');
    await tester.pumpWidget(shell(0,true));expect(focus.hasFocus,isTrue);expect(controller.text,'Yayından merhaba');
    await tester.pumpWidget(const SizedBox());controller.dispose();focus.dispose();
  });
  testWidgets('rapid heart taps overlap, remain bounded and disappear', (tester)async{
    final pulses=ValueNotifier<int>(0);
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx453Hearts(pulses:pulses))));
    pulses.value++;pulses.value++;pulses.value++;await tester.pump();
    expect(find.byIcon(Icons.favorite),findsNWidgets(3));
    for(var n=0;n<100;n++)pulses.value++;
    await tester.pump();expect(find.byIcon(Icons.favorite),findsNWidgets(24));
    await tester.pump(const Duration(seconds:3));await tester.pump();expect(find.byIcon(Icons.favorite),findsNothing);
    await tester.pumpWidget(const SizedBox());pulses.dispose();
  });
  testWidgets('sending never discards text typed during an outstanding request', (tester)async{
    final controller=TextEditingController(),focus=FocusNode();final completion=Completer<void>();var calls=0;
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx453LiveComposer(controller:controller,focus:focus,stream:const Stream<DocumentSnapshot<Map<String,dynamic>>>.empty(),host:true,uid:'host',send:(){calls++;return completion.future;}))));
    await tester.enterText(find.byType(TextField),'İlk mesaj');await tester.tap(find.byTooltip('Yorumu gönder'));await tester.pump();
    await tester.enterText(find.byType(TextField),'Yeni taslak');expect(calls,1);
    completion.complete();await tester.pump();expect(controller.text,'Yeni taslak');expect(focus.hasFocus,isTrue);
    await tester.pumpWidget(const SizedBox());controller.dispose();focus.dispose();
  });
}
