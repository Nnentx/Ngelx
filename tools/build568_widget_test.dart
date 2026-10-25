import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';
Map<String,dynamic> room()=>{'id':'583921','owner':'a','capacity':2,'status':'playing','revision':1,'mode':'classic','team':false,'botGame':true,'players':[{'uid':'a','seat':0,'name':'Sen'},{'uid':'bot','seat':2,'name':'Makine','bot':true}],'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),'power':List.generate(4,(_)=>{'control':1,'double':1,'shield':1}),'turn':0,'dice':null,'chat':[]};
void main(){
 test('numeric and previous invitations both remain readable',(){expect(ngelx565RoomId('https://ngelxsocial.com/ludo/583921'),'583921');expect(ngelx565RoomId('https://ngelxsocial.com/ludo/ABCDEF0123456789'),'ABCDEF0123456789');expect(ngelx565RoomId('https://evil.test/ludo/583921'),'');});
 testWidgets('bot options send settings and open the existing game table',(t)async{
  final calls=<Map<String,dynamic>>[];
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoLobby(userId:'a',request:(b)async{calls.add(b);return room();})));
  await t.tap(find.text('Makineye karşı oyna'));await t.pumpAndSettle();
  await t.scrollUntilVisible(find.text('Oyuna başla'),250);await t.tap(find.text('Oyuna başla'));await t.pumpAndSettle();
  expect(calls.first['action'],'bot');expect(calls.first['difficulty'],'medium');expect(find.text('Makine'),findsOneWidget);expect(find.text('ODA · 583921'),findsOneWidget);expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('random search has cancel and no host start button',(t)async{
  final r=room()..['status']='waiting'..['matchmaking']=true;r['players']=[{'uid':'a','seat':0,'name':'Sen'}];
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583921',userId:'a',initial:r,request:(b)async=>r)));
  await t.pumpAndSettle();expect(find.text('Rakip aranıyor…'),findsOneWidget);expect(find.text('Başlat'),findsNothing);expect(find.text('Vazgeç'),findsOneWidget);expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('chat composer stays above Android navigation with keyboard closed or open',(t)async{
  t.view.physicalSize=const Size(393,851);t.view.devicePixelRatio=1;t.view.viewPadding=const FakeViewPadding(bottom:34);t.view.padding=const FakeViewPadding(bottom:34);
  addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);addTearDown(t.view.resetViewPadding);addTearDown(t.view.resetPadding);addTearDown(t.view.resetViewInsets);
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'583921',userId:'a',initial:room(),request:(b)async=>room())));
  await t.tap(find.byTooltip('Emoji ve sohbet'));await t.pumpAndSettle();expect(t.getRect(find.byType(TextField)).bottom,lessThanOrEqualTo(851-34));expect(t.takeException(),isNull);
  t.view.viewInsets=const FakeViewPadding(bottom:300);await t.pumpAndSettle();expect(t.getRect(find.byType(TextField)).bottom,lessThanOrEqualTo(851-300));expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
}
