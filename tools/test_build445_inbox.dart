import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import '../lib/main.dart' as app;
import '../lib/build445_inbox_policy.dart';
void main(){
 testWidgets('call changes during route build notify overlay safely on next frame',(tester)async{
   final initial=app.ngelx445CallRevision.value;
   var requested=false;
   await tester.pumpWidget(MaterialApp(home:ValueListenableBuilder<int>(
     valueListenable:app.ngelx445CallRevision,
     builder:(_,value,__)=>Builder(builder:(_){
       if(!requested){requested=true;app.ngelx445CallChanged();app.ngelx445CallChanged();}
       return Text('$value');
     }),
   )));
   await tester.pump();
   expect(tester.takeException(),isNull);
   expect(app.ngelx445CallRevision.value,initial+1);
 });
 test('All includes only visible accepted private and group chats',(){
   for(final group in [false,true]){
     expect(ngelx445ChatFilter('Tümü',group:group,pending:false,hidden:false),isTrue);
     expect(ngelx445ChatFilter('Tümü',group:group,pending:true,hidden:false),isFalse);
     expect(ngelx445ChatFilter('Tümü',group:group,pending:false,hidden:true),isFalse);
   }
 });
 test('Notification and request tabs never select conversations',(){
   for(final filter in ['Bildirimler','İstekler']){
     expect(ngelx445ChatFilter(filter,group:false,pending:false,hidden:false),isFalse);
     expect(ngelx445ChatFilter(filter,group:true,pending:false,hidden:false),isFalse);
   }
 });
 test('Private and group filters preserve classification',(){
   expect(ngelx445ChatFilter('Mesajlar',group:false,pending:false,hidden:false),isTrue);
   expect(ngelx445ChatFilter('Mesajlar',group:true,pending:false,hidden:false),isFalse);
   expect(ngelx445ChatFilter('Gruplar',group:true,pending:false,hidden:false),isTrue);
 });
 test('All badge sums only unread conversations',(){expect(ngelx445AllUnread(9,25),34);});
}
