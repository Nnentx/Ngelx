import 'package:flutter_test/flutter_test.dart';
import '../lib/build445_inbox_policy.dart';
void main(){
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
