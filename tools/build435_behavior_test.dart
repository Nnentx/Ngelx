import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';
void main(){
 test('benden sil hides only this account, including received messages',(){
  final v={'senderId':'alice','hiddenFor':['bob'],'mediaUrl':'shared-photo'};
  expect(ngelx435BendenGizli(v,'bob'),isTrue);
  expect(ngelx435BendenGizli(v,'alice'),isFalse);
  expect(ngelx435BendenGizli(v,null),isFalse);
  expect(v['mediaUrl'],'shared-photo');
  expect(v['deletedForEveryone'],isNull);
 });
 test('durable media manifest includes thumbnail audio file and poster',(){
  final v={'mediaUrl':'photo','videoUrl':'video','audioUrl':'audio','fileUrl':'file','thumbnailUrl':'thumb','posterUrl':'poster','coverUrl':'cover','imageUrl':'image'};
  expect(ngelx435MedyaListesi(v),['photo','video','audio','file','thumb','poster','cover','image']);
  expect(ngelx435MedyaListesi({}),List.filled(8,''));
  expect(v['mediaUrl'],'photo');
 });
}
