import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart' show ngelx558CallDuration,ngelx558Verified,ngelx558MessageMenu,ngelx558AlbumItems,ngelx558AlbumLabel;

void main(){
  test('call duration survives remounts, handles future start, and is not wall-clock minutes',(){
    final start=DateTime.utc(2026,10,24,0,58,59);
    expect(ngelx558CallDuration(start,start.add(const Duration(seconds:62))),'01:02');
    expect(ngelx558CallDuration(start,start.add(const Duration(minutes:77,seconds:51))),'77:51');
    expect(ngelx558CallDuration(start,start.subtract(const Duration(seconds:10))),'00:00');
    expect(ngelx558CallDuration(null,start),'Aranıyor…');
  });
  test('badges match account IDs only and reject accidental extra recipients',(){
    bool allowed(String uid,String list)=>ngelx558Verified(uid,founderUid:'founder',verifiedUids:list);
    for(final uid in ['founder','yilmaz','ahsen','rizgar'])expect(allowed(uid,'yilmaz,ahsen,rizgar'),true);
    expect(allowed('same-display-name','yilmaz,ahsen,rizgar'),false);
    expect(allowed('','yilmaz,ahsen,rizgar'),false);
    expect(allowed('yilmaz','yilmaz,ahsen,rizgar,extra'),false);
    expect(allowed('yilmaz','yilmaz,ahsen'),false);
  });
  test('album reader tolerates old and malformed data without exposing local paths',(){
    expect(ngelx558AlbumItems({}),isEmpty);
    expect(ngelx558AlbumItems({'albumItems558':'legacy'}),isEmpty);
    final items=ngelx558AlbumItems({'albumItems558':[null,{'url':'file:///private.jpg'},{'url':'https://example.test/a.jpg','type':'photo'},{'url':'https://example.test/a.mp4','type':'video'}]});
    expect(items.length,2);expect(ngelx558AlbumLabel(items),'2 medya');
    expect(ngelx558AlbumLabel([items.first]),'1 fotoğraf');
  });
  testWidgets('group action sheet fits a narrow phone and returns reaction and More', (tester)async{
    tester.view.physicalSize=const Size(320,720);tester.view.devicePixelRatio=1;
    addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
    String? selected;
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:Builder(builder:(context)=>TextButton(onPressed:()async{selected=await ngelx558MessageMenu(context,hasText:true);},child:const Text('Open'))))));
    await tester.tap(find.text('Open'));await tester.pumpAndSettle();
    expect(tester.takeException(),isNull);
    expect(find.text('Yanıtla'),findsOneWidget);expect(find.text('Hatırlatma ayarla'),findsOneWidget);
    await tester.tap(find.text('❤️'));await tester.pumpAndSettle();expect(selected,'reaction:❤️');
    await tester.tap(find.text('Open'));await tester.pumpAndSettle();
    await tester.tap(find.text('Daha fazla'));await tester.pumpAndSettle();expect(selected,'more');
  });
}
