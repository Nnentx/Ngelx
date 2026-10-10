import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
void main(){
 final now=DateTime.utc(2026,10,10,12);
 Map<String,dynamic> presence(int minutes,{bool online=false,bool visible=true})=>{'lastSeenAt':Timestamp.fromDate(now.subtract(Duration(minutes:minutes))),'isOnline':online,'showActivityStatus':visible};
 test('online requires fresh heartbeat, privacy applies to both states',(){
  expect(ngelx434Aktiflik(presence(0,online:true),now:now),'Çevrimiçi');
  expect(ngelx434Aktiflik(presence(3,online:true),now:now),'3 dk önce aktif');
  expect(ngelx434Aktiflik(presence(0,online:true,visible:false),now:now),'');
  expect(ngelx434Aktiflik(presence(37,visible:false),now:now),'');
  expect(ngelx434Aktiflik({},now:now),'');
 });
 test('last active minutes hours days and future timestamp are truthful',(){
  expect(ngelx434Aktiflik(presence(37),now:now),'37 dk önce aktif');
  expect(ngelx434Aktiflik(presence(120),now:now),'2 sa önce aktif');
  expect(ngelx434Aktiflik(presence(2880),now:now),'2 gün önce aktif');
  expect(ngelx434Aktiflik(presence(-10,online:true),now:now),'');
 });
 test('answered requests never retain pending wording',(){
  for(final kind in ['friend_request','follow_request']){
   for(final state in ['accepted','rejected','cancelled','superseded']){
    final text=ngelxBildirimMetni({'type':kind,'status':state,'senderName':'Umay Umay','text':'sana arkadaşlık isteği gönderdi'});
    expect(text,contains('Umay Umay'));
    expect(text,contains('isteği'));
    expect(text, isNot(contains('gönderdi')));
   }
  }
  expect(ngelx434IstekSonucu({'type':'friend_request','status':'pending'}),null);
 });
}
