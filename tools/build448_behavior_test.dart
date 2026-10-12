import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/main.dart';
void main(){
 testWidgets('joining lease blocks a second launch and releases after errors',(tester)async{
  late BuildContext ctx;await tester.pumpWidget(MaterialApp(home:Scaffold(body:Builder(builder:(c){ctx=c;return const SizedBox();}))));
  final wait=Completer<void>();var second=false;
  final first=ngelx448MediaSession(ctx,'first',()=>wait.future);
  await ngelx448MediaSession(ctx,'second',()async{second=true;});expect(second,false);
  wait.complete();await first;
  await expectLater(ngelx448MediaSession(ctx,'failure',()async{throw StateError('failed');}),throwsStateError);
  await ngelx448MediaSession(ctx,'third',()async{second=true;});expect(second,true);
 });
 test('recent group activity sorts before older messages',(){
  final now=DateTime.now();expect(ngelx448GroupCompare({'updatedAt':Timestamp.fromDate(now)},{'updatedAt':Timestamp.fromDate(now.subtract(const Duration(hours:1)))},now),lessThan(0));
 });
 test('hiding a minimized card does not release its call',(){
  ngelxCallSession444.reserve('test448');ngelxCallSession444.minimize('test448');
  ngelx448HideCallCard('test448');expect(ngelxCallSession444.busy,true);expect(ngelxCallSession444.background,true);expect(ngelx448HiddenCallCard.value,'test448');
  ngelxCallSession444.release('test448');
 });
}
