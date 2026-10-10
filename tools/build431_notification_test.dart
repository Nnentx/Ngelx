import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';
void main(){
  test('Chat snapshots cannot become notifications even with text',(){
    expect(ngelxBildirimKaydiGecerli('chats',{'toUid':'a','text':'hello'},'a'),false);
    expect(ngelxBildirimKaydiGecerli('notifications',{'toUid':'b','type':'like'},'a'),false);
    expect(ngelxBildirimKaydiGecerli('notifications',{'toUid':'a','read':true},'a'),false);
    expect(ngelxBildirimKaydiGecerli('notifications',{'toUid':'a','type':'like'},'a'),true);
  });
  test('Notification content uses nonempty legacy fields and sender once',(){
    expect(ngelxBildirimMetni({'text':'','message':'seni takip etmek istiyor','senderName':'Ali'}),'Ali seni takip etmek istiyor');
    expect(ngelxBildirimMetni({'text':'Ali sana yazdı','senderName':'Ali'}),'Ali sana yazdı');
    expect(ngelxBildirimMetni({'type':'friend_request','senderName':'Ali'}),'Ali sana arkadaşlık isteği gönderdi');
  });
  test('Missing notification date stays unknown and client fallback works',(){
    expect(ngelxBildirimTarihi({}),null);
    final t=Timestamp.fromMillisecondsSinceEpoch(1700000000000);
    expect(ngelxBildirimTarihi({'clientCreatedAt':t}),t);
    expect(ngelxBildirimTarihi({'createdAt':'bad','clientCreatedAt':t}),t);
  });
  test('Request badge and list exclude accepted, rejected, hidden and friends',(){
    final v=<String,dynamic>{'members':['a','b'],'lastMessage':'hello','requestRecipientUid':'a'};
    expect(ngelxBekleyenMesajIstegi(v,'a',{}),true);
    expect(ngelxBekleyenMesajIstegi(v,'b',{}),false);
    expect(ngelxBekleyenMesajIstegi(v,'a',{'b'}),false);
    for(final change in [{'requestAccepted_a':true},{'requestRejected_a':true},{'hiddenFor':['a']},{'isGroup':true},{'lastMessage':''}]){
      expect(ngelxBekleyenMesajIstegi({...v,...change},'a',{}),false);
    }
  });
}
