import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart' show ngelx563NoticeTarget,Ngelx563CommentViewport,NgelXYorumYazici;

void main(){
 test('content and community targets take precedence over actor and empty aliases',(){
  expect(ngelx563NoticeTarget({'type':'like','fromUid':'ahsen','sourceId':'','videoId':'video1'}),(kind:'content',id:'video1'));
  expect(ngelx563NoticeTarget({'type':'comment','postId':'photo1','sourceId':'comment1'}),(kind:'content',id:'photo1'));
  expect(ngelx563NoticeTarget({'type':'community_join_request','communityId':'community1','sourceId':'','fromUid':'ahsen'}),(kind:'community',id:'community1'));
  expect(ngelx563NoticeTarget({'targetKind':'community','sourceId':'legacy1'}),(kind:'community',id:'legacy1'));
  expect(ngelx563NoticeTarget({'type':'friend_accepted','fromUid':'ahsen'}).kind,'other');
  expect(ngelx563NoticeTarget({'type':'call','sourceId':'chat1'}).kind,'other');
  expect(ngelx563NoticeTarget({'type':'like','fromUid':'ahsen'}),(kind:'content',id:''));
 });
 testWidgets('real modal keyboard preserves comment rows and send controls without overflow',(tester)async{
  tester.view.physicalSize=const Size(393,850);tester.view.devicePixelRatio=1;
  addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);addTearDown(tester.view.resetViewInsets);
  final controller=TextEditingController();addTearDown(controller.dispose);
  var builds=0,sends=0;
  await tester.pumpWidget(MaterialApp(home:Scaffold(resizeToAvoidBottomInset:false,body:Builder(builder:(context)=>TextButton(child:const Text('Yorumlar'),onPressed:()=>showModalBottomSheet<void>(context:context,isScrollControlled:true,useSafeArea:true,builder:(_)=>Ngelx563CommentViewport(child:Column(children:[
   const SizedBox(height:60,child:Text('80 yorum')),
   Expanded(child:Builder(builder:(_){builds++;return ListView.builder(itemCount:80,itemBuilder:(_,i)=>Text('Yorum $i'));})),
   NgelXYorumYazici(controller:controller,yanitYaziliyor:false,gonderiliyor:false,onGonder:()=>sends++),
  ]))))))));
  await tester.tap(find.text('Yorumlar'));await tester.pumpAndSettle();
  final before=builds;
  await tester.tap(find.byType(TextField));
  for(final inset in [60.0,120.0,220.0,320.0]){
   tester.view.viewInsets=FakeViewPadding(bottom:inset);await tester.pump(const Duration(milliseconds:40));
   expect(tester.takeException(),isNull);
   expect(tester.getBottomRight(find.byType(TextField)).dy,lessThanOrEqualTo(850-inset));
   expect(tester.getSize(find.byType(ListView)).height,greaterThan(100));
  }
  await tester.enterText(find.byType(TextField),'Profil yorum testi');await tester.pumpAndSettle();
  expect(builds,before);await tester.tap(find.byIcon(Icons.send_rounded));expect(sends,1);
  expect(tester.takeException(),isNull);
  await tester.pumpWidget(const SizedBox());
 });
}
