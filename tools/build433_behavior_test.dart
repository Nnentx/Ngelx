import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
class _Notification implements QueryDocumentSnapshot<Map<String,dynamic>>{
  @override final String id;
  final Map<String,dynamic> value;
  _Notification(this.id,this.value);
  @override Map<String,dynamic> data()=>value;
  @override dynamic noSuchMethod(Invocation i)=>super.noSuchMethod(i);
}
void main(){
  final now=DateTime.now();
  test('shared request counter deduplicates and excludes answered and wrong-recipient requests',(){
    Map<String,dynamic> v(String kind,String state,int age,String actor)=>{'type':kind,'status':state,'fromUid':actor,'toUid':'me','createdAt':Timestamp.fromDate(now.subtract(Duration(minutes:age)))};
    final docs=[_Notification('old',v('friend_request','pending',4,'bob')),_Notification('new',v('friend_request','accepted',1,'bob')),_Notification('follow',v('follow_request','pending',2,'bob')),_Notification('dup',v('follow_request','pending',3,'bob')),_Notification('friend',v('friend_request','pending',1,'alice')),_Notification('other',{...v('friend_request','pending',1,'eve'),'toUid':'other'})];
    expect(ngelx433SosyalIstekler(docs,'me').map((d)=>d.id).toSet(),{'follow','friend'});
  });
  test('active live never expires even without save',(){expect(ngelx433CanliTemizlenir({'active':true,'lastHeartbeatAt':Timestamp.fromDate(now)},now),false);});
  test('ended unsaved expires, saved survives until day30',(){
    final v=<String,dynamic>{'active':false,'endedAt':Timestamp.fromDate(now.subtract(const Duration(days:2)))};
    expect(ngelx433CanliTemizlenir(v,now),true);
    v['saved']=true;expect(ngelx433CanliTemizlenir(v,now),false);
    v['endedAt']=Timestamp.fromDate(now.subtract(const Duration(days:30)));expect(ngelx433CanliTemizlenir(v,now),true);
  });
  test('pending cleanup retries without deleting live or unknown-active records',(){
    expect(ngelx433CanliTemizlenir({'active':false,'deleting':true,'saved':true},now),true);
    expect(ngelx433CanliTemizlenir({'active':true},now),false);
  });
  testWidgets('notification highlights actor only and retains other text',(tester)async{
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:ngelx433RenkliBildirim({'senderName':'Umay Umay','text':'Umay Umay seni takip etmeye başladı'}))));
    final rich=tester.widget<Text>(find.byType(Text));final spans=(rich.textSpan as TextSpan).children!.cast<TextSpan>();
    expect(spans.where((s)=>s.style?.color==mor).single.text,'Umay Umay');
    expect(rich.textSpan!.toPlainText(),'Umay Umay seni takip etmeye başladı');
  });
}
