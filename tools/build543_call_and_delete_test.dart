import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/build440_behavior.dart';
import '../lib/main.dart' show Ngelx543DeleteConfirmation;
void main(){
  final now=DateTime.utc(2026,10,20,7,0);
  Map<String,dynamic> call()=>{'callStatus':'ringing','callRoomName':'group_test_123','callCreatedAt':Timestamp.fromDate(now)};
  test('new call is joinable despite a previous room heartbeat',(){final data=call()..['callHeartbeatAt']=Timestamp.fromDate(now.subtract(const Duration(hours:5)));expect(ngelx440CallJoinable(data,now),isTrue);});
  test('short device clock skew does not hide a newly ringing call',(){expect(ngelx440CallJoinable(call(),now.subtract(const Duration(seconds:10))),isTrue);});
  test('stale calls and invalid future timestamps stay hidden',(){expect(ngelx440CallJoinable(call(),now.add(const Duration(minutes:4))),isFalse);expect(ngelx440CallJoinable(call(),now.subtract(const Duration(minutes:4))),isFalse);});
  test('ended state and explicit ended timestamp cannot be revived',(){for(final status in ['ended','rejected','missed']){expect(ngelx440CallJoinable(call()..['callStatus']=status,now),isFalse);}expect(ngelx440CallJoinable(call()..['callEndedAt']=Timestamp.fromDate(now),now),isFalse);});
  test('missing room and server timestamps fail closed',(){expect(ngelx440CallJoinable(call()..remove('callCreatedAt'),now),isFalse);expect(ngelx440CallJoinable(call()..['callRoomName']='',now),isFalse);});
  testWidgets('permanent deletion requires exact typed community name',(tester)async{
    await tester.pumpWidget(const MaterialApp(home:Scaffold(body:Ngelx543DeleteConfirmation(name:'PARLAMENT'))));
    final button=find.widgetWithText(FilledButton,'Kalıcı olarak sil');
    expect(tester.widget<FilledButton>(button).onPressed,isNull);
    await tester.enterText(find.byType(TextField),'PARLAMENT ');await tester.pump();
    expect(tester.widget<FilledButton>(button).onPressed,isNull);
    await tester.enterText(find.byType(TextField),'PARLAMENT');await tester.pump();
    expect(tester.widget<FilledButton>(button).onPressed,isNotNull);
    expect(find.textContaining('geri alınamaz'),findsOneWidget);
  });
}
