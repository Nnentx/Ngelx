import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/build440_behavior.dart';

void main(){
  final now=DateTime.utc(2026,10,20,10);
  Map<String,dynamic> call(String status,List<String> people)=>{
    'callStatus':status,'callRoomName':'group_544',
    'callCreatedAt':Timestamp.fromDate(now),'callParticipants':people,
  };
  test('last departure hides every join surface even with fresh heartbeat',(){
    for(final status in ['ringing','active']){
      final data=call(status,[])..['callHeartbeatAt']=Timestamp.fromDate(now);
      expect(ngelx440CallJoinable(data,now),isFalse);
    }
  });
  test('other members keep their active room after one person leaves',(){
    expect(ngelx440CallJoinable(call('active',['other']),now),isTrue);
    expect(ngelx440CallJoinable(call('ringing',['caller']),now),isTrue);
  });
  test('ended call cannot be revived by stale membership or heartbeat',(){
    for(final status in ['ended','missed','rejected']){
      expect(ngelx440CallJoinable(call(status,['old']),now),isFalse);
    }
    expect(ngelx440CallJoinable(call('active',['old'])..['callEndedAt']=Timestamp.fromDate(now),now),isFalse);
  });
  test('new room and legacy ringing compatibility remain intact',(){
    final data=call('ringing',['caller'])..remove('callParticipants');
    expect(ngelx440CallJoinable(data,now),isTrue);
    expect(ngelx440CallJoinable(call('active',['peer']),now.add(const Duration(minutes:3))),isFalse);
  });
}
