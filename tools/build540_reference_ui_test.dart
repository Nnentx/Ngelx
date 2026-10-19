import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build540_reference_ui.dart';

void main() {
  test('mini call stays in viewport and above keyboard, snaps to nearest edge', () {
    for (final size in [const Size(320, 640), const Size(412, 915), const Size(915, 412)]) {
      for (final keyboard in [0.0, 240.0]) {
        const padding = EdgeInsets.only(top: 24, bottom: 24);
        for (final point in [const Offset(-999, -999), const Offset(9999, 9999)]) {
          final p = ngelx540BoundMini(point, size, padding, keyboard, 156);
          expect(p.dx, greaterThanOrEqualTo(0));
          expect(p.dx + 156, lessThanOrEqualTo(size.width));
          expect(p.dy, greaterThanOrEqualTo(0));
          if (size.height - keyboard >= 252) {
            expect(p.dy + 220, lessThanOrEqualTo(size.height - keyboard));
          }
          final snapped = ngelx540SnapMini(p, size, padding, keyboard, 156);
          expect(snapped.dx == 8 || snapped.dx == size.width - 164, isTrue);
        }
      }
    }
  });

  for (final width in [280.0, 320.0, 412.0]) {
    for (final scale in [1.0, 2.0]) {
      testWidgets('live bar keeps input low at width $width, scale $scale', (tester) async {
        await tester.binding.setSurfaceSize(Size(width, 640));
        addTearDown(() => tester.binding.setSurfaceSize(null));
        await tester.pumpWidget(MaterialApp(home: MediaQuery(
          data: MediaQueryData(size: Size(width, 640), textScaler: TextScaler.linear(scale)),
          child: Scaffold(body: Align(alignment: Alignment.bottomCenter,
            child: Ngelx540LiveBar(composer: const TextField(key: ValueKey('input')),
              actions: List.generate(4, (i) => IconButton(
                key: ValueKey('action$i'), onPressed: () {}, icon: const Icon(Icons.more_horiz))))),
          ),
        )));
        expect(tester.takeException(), isNull);
        expect(tester.getBottomLeft(find.byKey(const ValueKey('input'))).dy,
            closeTo(638, 3));
      });
    }
  }

  testWidgets('keyboard preserves the same input and hides auxiliary actions', (tester) async {
    final controller = TextEditingController(text: 'Gönderilmemiş yorum');
    addTearDown(controller.dispose);
    Widget page(double keyboard) => MaterialApp(home: MediaQuery(
      data: MediaQueryData(viewInsets: EdgeInsets.only(bottom: keyboard)),
      child: Scaffold(body: Ngelx540LiveBar(composer: TextField(controller: controller),
        actions: [IconButton(key: const ValueKey('gift'), onPressed: () {}, icon: const Icon(Icons.card_giftcard))])),
    ));
    await tester.pumpWidget(page(0));
    expect(find.byKey(const ValueKey('gift')), findsOneWidget);
    await tester.pumpWidget(page(240));
    expect(find.byKey(const ValueKey('gift')), findsNothing);
    expect(controller.text, 'Gönderilmemiş yorum');
    expect(tester.takeException(), isNull);
  });
}
