import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build540_reference_ui.dart';

void main(){
  for(final width in [280.0,320.0,360.0,412.0]){
    testWidgets('reference composer and four actions share one row at $width',(tester)async{
      tester.view.physicalSize=Size(width,760);tester.view.devicePixelRatio=1;
      addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
      final preview=GlobalKey();var taps=0;
      await tester.pumpWidget(RepaintBoundary(key:preview,child:MaterialApp(home:Scaffold(
        backgroundColor:const Color(0xFF41434A),
        body:Align(alignment:Alignment.bottomCenter,child:Padding(padding:const EdgeInsets.all(14),
          child:Ngelx540LiveBar(composer:const TextField(key:ValueKey('composer554'),
            decoration:InputDecoration(hintText:'Yorum yaz…',filled:true,fillColor:Colors.black26,
              border:OutlineInputBorder(borderRadius:BorderRadius.all(Radius.circular(28))))),
            actions:[for(final label in ['+Konuk','Gül','Hediye','Daha fazla'])
              Ngelx540LiveAction(icon:const Icon(Icons.star,color:Colors.white),label:label,onPressed:()=>taps++)])))))));
      expect(tester.takeException(),isNull);
      final composer=tester.getRect(find.byKey(const ValueKey('composer554')));
      final action=tester.getRect(find.byType(Ngelx540LiveAction).first);
      expect((composer.center.dy-action.center.dy).abs(),lessThan(1));
      expect(composer.width,greaterThanOrEqualTo(110));
      await tester.ensureVisible(find.text('Daha fazla'));
      await tester.tap(find.text('Daha fazla'));expect(taps,1);
      if(width==360){
        await tester.pump();
        await tester.runAsync(()async{
          final boundary=preview.currentContext!.findRenderObject() as RenderRepaintBoundary;
          final image=await boundary.toImage();final bytes=await image.toByteData(format:ui.ImageByteFormat.png);
          Directory('test-output').createSync();
          File('test-output/live554-reference.png').writeAsBytesSync(bytes!.buffer.asUint8List());image.dispose();
        });
      }
    });
  }
}
