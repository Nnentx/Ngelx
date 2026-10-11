import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/build440_behavior.dart';
class StoryDoc440 implements QueryDocumentSnapshot<Map<String,dynamic>>{
 final Map<String,dynamic> value;StoryDoc440(this.value);
 @override Map<String,dynamic> data()=>value;
 @override dynamic noSuchMethod(Invocation invocation)=>super.noSuchMethod(invocation);
}
class StoryQuery440 implements QuerySnapshot<Map<String,dynamic>>{
 @override final List<QueryDocumentSnapshot<Map<String,dynamic>>> docs;
 StoryQuery440(this.docs);
 @override dynamic noSuchMethod(Invocation invocation)=>super.noSuchMethod(invocation);
}
void main(){
 testWidgets('story leaves active screen at expiry without another Firestore event', (tester)async{
  var now=DateTime.utc(2026,10,11,20);
  final stream=StreamController<QuerySnapshot<Map<String,dynamic>>>();
  final story={'type':'story','expiresAt':Timestamp.fromDate(now.add(const Duration(seconds:1)))};
  await tester.pumpWidget(MaterialApp(home:NgelXStorySnapshotBuilder(stream:stream.stream,now:()=>now,builder:(_,snapshot)=>Text((snapshot.data?.docs??[]).any((d)=>ngelx440StoryActive(d.data(),now))?'story':'empty'))));
  stream.add(StoryQuery440([StoryDoc440(story)]));await tester.pumpAndSettle();
  expect(find.text('story'),findsOneWidget);
  now=now.add(const Duration(seconds:1));await tester.pump(const Duration(milliseconds:1010));await tester.pump();
  expect(find.text('empty'),findsOneWidget);
  await tester.pumpWidget(const SizedBox());unawaited(stream.close());await tester.pump(const Duration(hours:1));
 });
 test('new pin wins over older pins and newer unpinned messages after reload',(){
  final pins={'rojin','selma','group'},times={'rojin':1,'group':2,'selma':3};
  final rows=['latest','rojin','group','selma'];
  rows.sort((a,b)=>ngelx440PinCompare(a,b,Set.of(pins),Map.of(times),a=='latest'?999:100,b=='latest'?999:100));
  expect(rows,['selma','group','rojin','latest']);
  pins.remove('selma');
  rows.sort((a,b)=>ngelx440PinCompare(a,b,pins,times,100,100));
  expect(rows.first,'group');
 });
 test('story expires at boundary; legacy creation gets 24 hours; unknown age hidden',(){
  final now=DateTime.utc(2026,10,11,20);
  expect(ngelx440StoryActive({'type':'story','expiresAt':Timestamp.fromDate(now)},now),false);
  expect(ngelx440StoryActive({'type':'story','createdAt':Timestamp.fromDate(now.subtract(const Duration(hours:24)))},now),false);
  expect(ngelx440StoryActive({'type':'story','createdAt':Timestamp.fromDate(now.subtract(const Duration(hours:23)))},now),true);
  expect(ngelx440StoryActive({'type':'story'},now),false);
  expect(ngelx440StoryActive({'type':'video','expiresAt':Timestamp.fromDate(now.add(const Duration(hours:1)))},now),false);
 });
 test('ended, expired and unknown-age calls never offer join; heartbeat keeps long call',(){
  final now=DateTime.utc(2026,10,11,20);
  final live={'callStatus':'active','callRoomName':'group_x','callCreatedAt':Timestamp.fromDate(now.subtract(const Duration(hours:1))),'callHeartbeatAt':Timestamp.fromDate(now.subtract(const Duration(seconds:30)))};
  expect(ngelx440CallJoinable(live,now),true);
  expect(ngelx440CallJoinable({...live,'callEndedAt':Timestamp.fromDate(now)},now),false);
  expect(ngelx440CallJoinable({...live,'callHeartbeatAt':Timestamp.fromDate(now.subtract(const Duration(minutes:3)))},now),false);
  expect(ngelx440CallJoinable({'callStatus':'ringing','callRoomName':'group_x'},now),false);
  expect(ngelx440CallJoinable({...live,'callStatus':'missed'},now),false);
 });
}
