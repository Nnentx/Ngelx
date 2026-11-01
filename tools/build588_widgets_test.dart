import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';
import 'package:ngelx_app/build553_gift_effect.dart';
void main(){
 testWidgets('matching gift particles stay inside a narrow phone and ignore taps',(tester)async{
  tester.view.physicalSize=const Size(360,780);tester.view.devicePixelRatio=1;
  addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
  await tester.pumpWidget(const MaterialApp(home:Scaffold(body:Ngelx588GiftFlow(emoji:'❤️',name:'Kalp',sender:'Ali',quantity:10))));
  await tester.pump(const Duration(milliseconds:900));
  expect(find.text('❤️'),findsNWidgets(36));expect(find.text('Kalp ×10'),findsOneWidget);expect(tester.takeException(),isNull);
  expect(tester.widget<IgnorePointer>(find.byType(IgnorePointer).last).ignoring,true);
  await tester.pumpWidget(const SizedBox());await tester.pump();expect(tester.takeException(),isNull);
 });
 testWidgets('reduced motion uses a single stable gift',(tester)async{
  await tester.pumpWidget(const MaterialApp(home:MediaQuery(data:MediaQueryData(disableAnimations:true),child:Scaffold(body:Ngelx588GiftFlow(emoji:'🧸',name:'Ayıcık',sender:'Ali',quantity:3)))));
  await tester.pump(const Duration(milliseconds:100));expect(find.text('🧸'),findsOneWidget);expect(tester.takeException(),isNull);
  await tester.pumpWidget(const SizedBox());
 });
 testWidgets('camera off has profile fallback without a camera icon',(tester)async{
  await tester.pumpWidget(const MaterialApp(home:Scaffold(body:Ngelx588ProfileStage(uid:''))));
  expect(find.byIcon(Icons.person_rounded),findsOneWidget);expect(find.byIcon(Icons.videocam_off_rounded),findsNothing);
 });
 testWidgets('cat and tiger bundled effects mount without audio enabled',(tester)async{
  for(final kind in ['Kedi','Kaplan']){
   await tester.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx553GiftEffect(key:ValueKey(kind),kind:kind,sender:'Ali',quantity:1,soundEnabled:false))));
   await tester.pump(const Duration(milliseconds:300));expect(tester.takeException(),isNull);
  }
  await tester.pumpWidget(const SizedBox());
 });
}
