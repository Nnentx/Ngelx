import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
class NotificationDoc extends Fake implements QueryDocumentSnapshot<Map<String,dynamic>>{
  @override final String id;
  final Map<String,dynamic> value;
  NotificationDoc(this.id,this.value);
  @override Map<String,dynamic> data()=>value;
}
void main(){
  test('Newest read request suppresses an older unread duplicate',(){
    final old=NotificationDoc('old',{'type':'follow_request','fromUid':'a','toUid':'b','requestKey':'follow_a_b','read':false,'createdAt':Timestamp.fromMillisecondsSinceEpoch(1000)});
    final newer=NotificationDoc('new',{'type':'follow_request','fromUid':'a','toUid':'b','requestKey':'follow_a_b','read':true,'createdAt':Timestamp.fromMillisecondsSinceEpoch(2000)});
    expect(ngelxOkunmamisAktiviteSayisi([old,newer]),0);
    expect(ngelxOkunmamisAktiviteSayisi([newer,old]),0);
  });
  test('Different request types remain independent',(){
    final follow=NotificationDoc('follow',{'type':'follow_request','fromUid':'a','toUid':'b','read':false});
    final friend=NotificationDoc('friend',{'type':'friend_request','fromUid':'a','toUid':'b','read':false});
    expect(ngelxOkunmamisAktiviteSayisi([follow,friend]),2);
  });
  test('Ordinary message notifications do not inflate Activity badge',(){
    expect(ngelxOkunmamisAktiviteSayisi([NotificationDoc('message',{'type':'message','read':false})]),0);
  });
  test('Hidden activity never reveals a live heartbeat',(){
    expect(ngelxPresenceOnline({'showActivityStatus':false,'isOnline':true,'lastSeenAt':Timestamp.now()}),false);
  });
  test('Fresh heartbeat marks an opted-in user online',(){
    expect(ngelxPresenceOnline({'isOnline':true,'lastSeenAt':Timestamp.now()}),true);
  });
  test('Stale heartbeat cannot keep a closed app online',(){
    expect(ngelxPresenceOnline({'isOnline':true,'lastSeenAt':Timestamp.fromDate(DateTime.now().subtract(const Duration(minutes:3)))}),false);
  });
  test('Missing heartbeat and offline flags do not imply online',(){
    expect(ngelxPresenceOnline({'isOnline':true}),false);
    expect(ngelxPresenceOnline({'isOnline':false,'lastSeenAt':Timestamp.now()}),false);
  });
  test('Invalid future timestamp cannot imply online',(){
    expect(ngelxPresenceOnline({'online':true,'lastSeenAt':Timestamp.fromDate(DateTime.now().add(const Duration(minutes:2)))}),false);
  });
}
