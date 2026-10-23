import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart' show Ngelx456Cover;
void main() {
  testWidgets('community cover stays bounded with missing image and bad alignment', (tester) async {
    tester.view.physicalSize = const Size(320,640);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(const MaterialApp(home: Scaffold(body:
      SingleChildScrollView(child: Ngelx456Cover(url:'',alignment:double.nan)))));
    expect(tester.getSize(find.byType(Ngelx456Cover)), const Size(320,190));
    expect(tester.takeException(), isNull);
  });
}
