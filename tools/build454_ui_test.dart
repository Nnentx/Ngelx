import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

void main(){
  testWidgets('portrait chat photo fits a small viewport without cropping or overflow',(tester)async{
    final recorder=ui.PictureRecorder();final canvas=Canvas(recorder);canvas.drawRect(const Rect.fromLTWH(0,0,20,800),Paint()..color=Colors.blue);
    final picture=recorder.endRecording();final bitmap=await picture.toImage(20,800);final bytes=await bitmap.toByteData(format:ui.ImageByteFormat.png);
    await tester.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(size:Size(320,640)),child:Scaffold(body:Align(alignment:Alignment.topLeft,child:Ngelx453Photo(url:'',provider:MemoryImage(bytes!.buffer.asUint8List())))))));
    await tester.pumpAndSettle();
    final size=tester.getSize(find.byType(Image));
    expect(size.width,lessThanOrEqualTo(320*.67));expect(size.height,lessThanOrEqualTo(640*.46));
    expect(tester.widget<Image>(find.byType(Image)).fit,BoxFit.contain);expect(tester.takeException(),isNull);
    await tester.pumpWidget(const SizedBox());bitmap.dispose();picture.dispose();
  });
  test('upload indicator handles unknown totals and retry counters honestly',(){
    expect(ngelx454UploadFraction(42,0),isNull);expect(ngelx454UploadFraction(50,100),.5);
    expect(ngelx454UploadFraction(200,100),1);expect(ngelx454UploadFraction(-1,100),0);
    expect(ngelx454UploadFraction(0,100),0);
  });
}
