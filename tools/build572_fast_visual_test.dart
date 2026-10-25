import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

Map<String,dynamic> fixture()=>{
 'id':'534157','status':'playing','mode':'power','capacity':2,
 'players':[{'uid':'a','seat':0,'name':'Sen'},{'uid':'bot','seat':2,'name':'Makine'}],
 'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),
 'powerTiles':<String,dynamic>{'7':'shield','23':'double'},
 'turn':0,'dice':6,
};
void main(){
 test('overlapping pieces receive distinct offsets without modifying their underlying game positions',(){
  final r=fixture();
  (r['tokens'] as List)[0][0]=10;
  (r['tokens'] as List)[2][1]=36; // same physical cell: (26+36)%52 == 10
  final a=ngelx572StackOffset(r,0,0),b=ngelx572StackOffset(r,2,1);
  expect(a, isNot(b));
  expect((r['tokens'] as List)[0][0],10);
  expect((r['tokens'] as List)[2][1],36);
 });
 test('home tokens remain at their original sockets',(){
  final r=fixture();
  expect(ngelx572StackOffset(r,0,0),Offset.zero);
  expect(ngelx572StackOffset(r,2,2),Offset.zero);
 });
 test('reference mode title distinguishes classic, power, two and four players',(){
  final r=fixture();
  expect(ngelx572ModeTitle(r),'POWER • 2 KİŞİ');
  r['capacity']=4;r['mode']='classic';expect(ngelx572ModeTitle(r),'KLASİK • 4 KİŞİ');
  r['botGame']=true;expect(ngelx572ModeTitle(r),'MAKİNEYE KARŞI');
 });
 test('Power pickup painter reacts to relocated reward positions',(){
  final p=Ngelx565BoardPainter(power:true,powerTiles:{'7':'shield'});
  final newer=Ngelx565BoardPainter(power:true,powerTiles:{'19':'shield'});
  expect(newer.shouldRepaint(p),true);
 });
 testWidgets('Power buttons register a single press without blocking their parent', (t) async{
  var taps=0;
  await t.pumpWidget(MaterialApp(home:Scaffold(body:Center(child:Ngelx570Power(kind:'shield',label:'Kalkan',count:2,onTap:()=>taps++)))));
  await t.tap(find.byType(Ngelx570Power));
  await t.pump();
  expect(taps,1);
  expect(find.text('Kalkan'),findsOneWidget);
 });
}
