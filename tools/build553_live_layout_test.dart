import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build540_reference_ui.dart';

void main(){
  for(final width in [280.0,320.0,360.0,412.0]){
    for(final scale in [1.0,1.5,2.0]){
      testWidgets('live bar fits $width text $scale',(tester)async{
        tester.view.physicalSize=Size(width,800);
        tester.view.devicePixelRatio=1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        var pressed=false;
        await tester.pumpWidget(MaterialApp(home:MediaQuery(
          data:MediaQueryData(size:Size(width,800),textScaler:TextScaler.linear(scale)),
          child:Scaffold(body:Align(alignment:Alignment.bottomCenter,child:Ngelx540LiveBar(
            composer:const TextField(decoration:InputDecoration(hintText:'Yorum yaz…')),
            actions:List.generate(4,(i)=>Ngelx540LiveAction(icon:const Icon(Icons.more_horiz),label:'Daha fazla',onPressed:()=>pressed=true)),
          ))))));
        expect(tester.takeException(),isNull);
        await tester.tap(find.byType(InkWell).last);
        expect(pressed,isTrue);
      });
    }
  }
  testWidgets('keyboard retains composer without action overflow',(tester)async{
    await tester.pumpWidget(const MaterialApp(home:MediaQuery(
      data:MediaQueryData(size:Size(320,640),viewInsets:EdgeInsets.only(bottom:300)),
      child:Scaffold(body:Ngelx540LiveBar(composer:TextField(),actions:[Text('hidden action')])))));
    expect(find.byType(TextField),findsOneWidget);
    expect(find.text('hidden action'),findsNothing);
    expect(tester.takeException(),isNull);
  });
}
