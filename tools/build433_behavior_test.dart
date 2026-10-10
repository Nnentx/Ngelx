import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
void main(){
  final now=DateTime.now();
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
