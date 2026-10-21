import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build552_policy.dart';
import '../lib/main.dart' show Ngelx551CallGrid,Ngelx543MiniGrid;
void main(){
 test('volume overlays remain visible; true background states suspend capture',(){
  expect(ngelx552Visible(AppLifecycleState.resumed),isTrue);
  expect(ngelx552Visible(AppLifecycleState.inactive),isTrue);
  for(final s in [AppLifecycleState.hidden,AppLifecycleState.paused,AppLifecycleState.detached]){
   expect(ngelx552Visible(s),isFalse);
  }
 });
 testWidgets('eight voice and video seats all fit in two columns on short phones',(tester)async{
  for(final voice in [true,false]){
   for(final height in [320.0,580.0]){
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(width:320,height:height,
     child:Ngelx551CallGrid(count:8,columns:ngelx552Columns(8),voice:voice,
      itemBuilder:(_,i)=>ColoredBox(key:ValueKey('seat-$i'),color:Colors.purple))))));
    final first=tester.getRect(find.byKey(const ValueKey('seat-0')));
    final second=tester.getRect(find.byKey(const ValueKey('seat-1')));
    final last=tester.getRect(find.byKey(const ValueKey('seat-7')));
    expect(first.top,second.top);expect(second.left,greaterThan(first.right));
    expect(last.bottom,lessThanOrEqualTo(height));
    expect(find.byKey(const ValueKey('seat-7')),findsOneWidget);
    expect(tester.takeException(),isNull);
   }
  }
 });
 testWidgets('all eight mini thumbnails and twelve PiP seats remain visible',(tester)async{
  for(final count in [2,3,8,12]){
   await tester.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(width:174,height:200,
    child:Ngelx543MiniGrid(children:[for(var i=0;i<count;i++)
     ColoredBox(key:ValueKey('mini-$i'),color:Colors.purple)])))));
   for(var i=0;i<count;i++){
    final rect=tester.getRect(find.byKey(ValueKey('mini-$i')));
    expect(rect.top,greaterThanOrEqualTo(0));expect(rect.bottom,lessThanOrEqualTo(200.01));
    expect(rect.right,lessThanOrEqualTo(174.01));
   }
   expect(tester.takeException(),isNull);
  }
 });
}
