import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
void main(){
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
