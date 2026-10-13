import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  testWidgets(
    'All five discovery tabs remain reachable on narrow screens with large text',
    (tester) async {
      tester.view.physicalSize = const Size(320, 700);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      int? chosen;
      await tester.pumpWidget(
        MaterialApp(
          home: MediaQuery(
            data: const MediaQueryData(textScaler: TextScaler.linear(1.6)),
            child: Scaffold(
              body: NgelXDiscoveryTabs450(
                selected: 0,
                onSelected: (v) => chosen = v,
              ),
            ),
          ),
        ),
      );
      for (final entry in [
        (0, 'Canlı'),
        (2, 'Trend'),
        (3, 'Kişiler'),
        (4, 'Gruplar'),
        (5, 'Topluluk'),
      ]) {
        await tester.tap(find.text(entry.$2));
        expect(chosen, entry.$1);
        expect(tester.takeException(), isNull);
      }
    },
  );
  testWidgets(
    'Community creation form fits small screens and toggles privacy',
    (tester) async {
      tester.view.physicalSize = const Size(320, 700);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        const MaterialApp(home: NgelXCommunityCreate450()),
      );
      expect(tester.takeException(), isNull);
      await tester.scrollUntilVisible(find.text('Özel topluluk'), 200, scrollable:find.byType(Scrollable).first);
      await tester.tap(find.text('Özel topluluk'));
      await tester.pump();
      expect(
        find.text('Yalnızca davetle bulunur; gönderiler üyelere açıktır.'),
        findsOneWidget,
      );
      expect(tester.takeException(), isNull);
    },
  );
}
