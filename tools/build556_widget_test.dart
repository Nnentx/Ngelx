import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart' show Ngelx556InfoDialog,Ngelx556Section,Ngelx556MediaPreview;
void main(){
  testWidgets('community section fits narrow phone with large text',(tester)async{
    tester.view.physicalSize=const Size(320,640);tester.view.devicePixelRatio=1;
    addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(textScaler:TextScaler.linear(2)),child:const Scaffold(body:SingleChildScrollView(child:Ngelx556Section(title:'Gizlilik ve onaylar',subtitle:'Kimlerin katılacağını ve paylaşım yapacağını belirle.',icon:Icons.shield_outlined))))));
    expect(tester.takeException(),isNull);
  });
  testWidgets('new community has a bounded cover and avatar preview',(tester)async{
    await tester.pumpWidget(const MaterialApp(home:Scaffold(body:Ngelx556MediaPreview())));
    expect(tester.getSize(find.byType(Ngelx556MediaPreview)).height,180);
    expect(tester.takeException(),isNull);
  });
  testWidgets('editing name updates Save eligibility immediately',(tester)async{
    final name=TextEditingController(text:'ab'),description=TextEditingController(),rules=TextEditingController();
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:Ngelx556InfoDialog(name:name,description:description,rules:rules))));
    expect(tester.widget<FilledButton>(find.byType(FilledButton)).onPressed,isNull);
    await tester.enterText(find.byType(TextField).first,'PARLAMENT');await tester.pump();
    expect(tester.widget<FilledButton>(find.byType(FilledButton)).onPressed,isNotNull);
    await tester.pumpWidget(const SizedBox.shrink());name.dispose();description.dispose();rules.dispose();
  });
}
