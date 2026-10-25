import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';
void main(){
 test('board track has 52 distinct bounded cells and opposite seats',(){
  final track=ngelx565Track();expect(track.length,52);expect(track.toSet().length,52);
  for(final p in track){expect(p.dx,inInclusiveRange(0,14));expect(p.dy,inInclusiveRange(0,14));}
  expect(ngelx565TokenPoint(2,0,0),track[26]);
  expect(ngelx565Rotate(const Offset(2,3),4),const Offset(2,3));
 });
 test('every move from start through home follows an adjacent square',(){
  for(var seat=0;seat<4;seat++){
   for(var position=0;position<56;position++){
    final a=ngelx565TokenPoint(seat,0,position),b=ngelx565TokenPoint(seat,0,position+1);
    expect((a.dx-b.dx).abs()+(a.dy-b.dy).abs(),1,reason:'seat $seat position $position');
   }
  }
 });
 test('only six launches and finishing requires an exact roll',(){
  final r=<String,dynamic>{'dice':5,'tokens':[[-1,51,52,56]],'doubled':false};
  expect(ngelx565Legal(r,0),[1]);r['dice']=6;expect(ngelx565Legal(r,0),[0]);
  r['dice']=2;r['doubled']=true;expect(ngelx565Legal(r,0),[1,2]);
 });
 test('only complete trusted invite links are recognized',(){
  expect(ngelx565RoomId('🎲 Ludo daveti\nhttps://ngelxsocial.com/ludo/ABCDEF0123456789\nKatıl'),'ABCDEF0123456789');
  expect(ngelx565RoomId('https://evil.example/ludo/ABCDEF0123456789'),'');
  expect(ngelx565RoomId('https://ngelxsocial.com/ludo/ABCDEF0123456789evil'),'');
 });
 testWidgets('update announcement uses Güncelle and invokes its action',(tester)async{
  var calls=0;await tester.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx565AnnouncementCard(icon:Icons.system_update,title:'Uygulama güncellemesi',text:'Yeni sürüm',button:'Güncelle',onPressed:()=>calls++))));
  expect(find.text('İndir'),findsNothing);await tester.tap(find.text('Güncelle'));expect(calls,1);expect(tester.takeException(),isNull);
 });
 for(final width in [280.0,393.0]){
  testWidgets('board at $width selects only a legal own token',(tester)async{
   final selected=<int>[];final room=<String,dynamic>{'dice':6,'players':[{'seat':0},{'seat':2}],'tokens':List.generate(4,(_)=>[-1,-1,-1,-1])};
   await tester.pumpWidget(MaterialApp(home:Scaffold(body:Center(child:SizedBox(width:width,height:width,child:Ngelx565LudoBoard(room:room,seat:0,enabled:true,onToken:selected.add))))));
   await tester.tap(find.byKey(const ValueKey('ludo-0-0')));expect(selected,[0]);
   await tester.tap(find.byKey(const ValueKey('ludo-2-0')));expect(selected,[0]);expect(tester.takeException(),isNull);
  });
 }
}
