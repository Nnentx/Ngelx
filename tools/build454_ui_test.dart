import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

void main(){
  testWidgets('portrait chat photo fits a small viewport without cropping or overflow',(tester)async{
    final bytes=base64Decode('iVBORw0KGgoAAAANSUhEUgAAABQAAAMgCAIAAACs6NV8AAAArElEQVR4nO3LsQ0AAAgDoOr/P+sPbiawU8nkqs9TlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmX5XV5/EQc/rdflpAAAAABJRU5ErkJggg==');
    await tester.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(size:Size(320,640)),child:Scaffold(body:Align(alignment:Alignment.topLeft,child:Ngelx453Photo(url:'',provider:MemoryImage(bytes)))))));
    await tester.runAsync(()=>precacheImage(tester.widget<Image>(find.byType(Image)).image,tester.element(find.byType(Image))));
    await tester.pump();
    final size=tester.getSize(find.byType(Image));
    expect(size.width,lessThanOrEqualTo(320*.67));expect(size.height,lessThanOrEqualTo(640*.46));
    expect(tester.widget<Image>(find.byType(Image)).fit,BoxFit.contain);expect(tester.takeException(),isNull);
    await tester.pumpWidget(const SizedBox());
  });
  test('upload indicator handles unknown totals and retry counters honestly',(){
    expect(ngelx454UploadFraction(42,0),isNull);expect(ngelx454UploadFraction(50,100),.5);
    expect(ngelx454UploadFraction(200,100),1);expect(ngelx454UploadFraction(-1,100),0);
    expect(ngelx454UploadFraction(0,100),0);
  });
}
