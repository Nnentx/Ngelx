import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

void main(){
 testWidgets('approved lobby preserves game mode selection and accessible update actions',(t)async{
  await t.binding.setSurfaceSize(const Size(360,740));
  addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(const MaterialApp(home:Ngelx565LudoLobby(userId:'preview')));
  await t.pump();
  expect(t.takeException(),isNull);
  expect(find.byKey(const ValueKey('ludo-daily-gift')),findsOneWidget);
  expect(find.byKey(const ValueKey('ludo-timed-chest')),findsOneWidget);
  expect(find.byKey(const ValueKey('ludo-profile-stats')),findsOneWidget);
  expect(find.text('Nasıl oynamak istersin?'),findsOneWidget);
  await t.scrollUntilVisible(find.text('Oyun modu'),180,scrollable:find.byType(Scrollable).first);
  expect(find.text('Klasik'),findsOneWidget);
  expect(find.text('Power'),findsOneWidget);
  await t.scrollUntilVisible(find.text('Oyuncu sayısı'),160,scrollable:find.byType(Scrollable).first);
  expect(find.text('2 kişi'),findsOneWidget);
  expect(find.text('4 kişi'),findsOneWidget);
  expect(find.text('2V2'),findsOneWidget);
  expect(t.takeException(),isNull);
 });
 testWidgets('new illustration fits invite cards in a narrow device',(t)async{
  await t.binding.setSurfaceSize(const Size(320,568));
  addTearDown(()=>t.binding.setSurfaceSize(null));
  await t.pumpWidget(const MaterialApp(home:Scaffold(body:Center(child:SizedBox(width:300,height:158,child:Ngelx581Hero())))));
  await t.pump();
  expect(find.text('LUDO'),findsOneWidget);
  expect(t.takeException(),isNull);
 });
}
