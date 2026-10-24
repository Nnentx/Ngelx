import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../lib/main.dart'
    show
        Ngelx560InboxHeader,
        Ngelx560CategoryRow,
        Ngelx560CategoryChip,
        Ngelx560ProfileRail,
        ngelx560ShowProfiles,
        ngelx560ProfileHeight;

void main() {
  for (final width in [280.0, 320.0, 360.0, 393.0, 430.0, 600.0]) {
    testWidgets(
      'header at $width: title stays separate, live search closes and plus still works',
      (tester) async {
        tester.view.physicalSize = Size(width, 700);
        tester.view.devicePixelRatio = 1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        final state = GlobalKey<_HeaderHarnessState>();
        await tester.pumpWidget(MaterialApp(home: _HeaderHarness(key: state)));
        expect(find.text('Gelen Kutusu'), findsOneWidget);
        expect(find.byType(TextField), findsNothing);
        await tester.tap(find.byKey(const ValueKey('inbox-search-open560')));
        await tester.pump();
        expect(find.byType(TextField), findsOneWidget);
        expect(find.text('Gelen Kutusu'), findsOneWidget);
        final title = tester.getRect(
              find.byKey(const ValueKey('inbox-title-fit560')),
            ),
            field = tester.getRect(
              find.byKey(const ValueKey('inbox-search445')),
            );
        expect(title.right, lessThanOrEqualTo(field.left));
        expect((title.center.dy - field.center.dy).abs(), lessThan(2));
        await tester.enterText(find.byType(TextField), 'YILMAZ');
        await tester.pump();
        expect(state.currentState!.query, 'yilmaz');
        await tester.tap(find.byKey(const ValueKey('inbox-new560')));
        expect(state.currentState!.created, 1);
        await tester.tap(find.byKey(const ValueKey('inbox-search-close560')));
        await tester.pump();
        expect(find.byType(TextField), findsNothing);
        expect(state.currentState!.query, '');
        expect(tester.takeException(), isNull);
        await tester.pumpWidget(const SizedBox());
      },
    );
  }
  testWidgets('large text keeps the full inbox title and search field apart', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 700);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      MaterialApp(
        home: MediaQuery(
          data: const MediaQueryData(
            size: Size(320, 700),
            textScaler: TextScaler.linear(2),
          ),
          child: _HeaderHarness(),
        ),
      ),
    );
    await tester.tap(find.byKey(const ValueKey('inbox-search-open560')));
    await tester.pump();
    expect(
      tester.getRect(find.byKey(const ValueKey('inbox-title-fit560'))).right,
      lessThanOrEqualTo(tester.getTopLeft(find.byType(TextField)).dx),
    );
    expect(tester.takeException(), isNull);
    await tester.pumpWidget(const SizedBox());
  });
  testWidgets(
    'all five filters remain reachable with their counters on narrow phones',
    (tester) async {
      tester.view.physicalSize = const Size(280, 640);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      String? selected;
      const labels = ['Tümü', 'Mesajlar', 'Gruplar', 'Bildirimler', 'İstekler'];
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Ngelx560CategoryRow(
              children: [
                for (final label in labels)
                  Ngelx560CategoryChip(
                    label: label,
                    countLabel: label == 'Bildirimler' ? '99+' : '7',
                    selected: label == 'Tümü',
                    showCount: true,
                    onTap: () => selected = label,
                  ),
              ],
            ),
          ),
        ),
      );
      for (final label in labels) {
        await tester.ensureVisible(find.text(label));
        await tester.pumpAndSettle();
        await tester.tap(find.text(label));
        expect(selected, label);
      }
      expect(find.text('99+'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );
  testWidgets(
    'compact profile rail is horizontally scrollable and preserves taps',
    (tester) async {
      tester.view.physicalSize = const Size(320, 640);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      int? opened;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                Ngelx560ProfileRail(
                  uid: 'test',
                  itemCount: 8,
                  itemBuilder: (_, i) => InkWell(
                    onTap: () => opened = i,
                    child: Column(
                      children: [
                        const CircleAvatar(radius: 32),
                        Text('Person $i'),
                        const Text('Şu an aktif'),
                      ],
                    ),
                  ),
                ),
                const Expanded(child: Text('Existing live list')),
              ],
            ),
          ),
        ),
      );
      expect(tester.getSize(find.byType(Ngelx560ProfileRail)).height, 124);
      await tester.tap(find.text('Person 0'));
      expect(opened, 0);
      await tester.drag(
        find.byType(Ngelx560ProfileRail),
        const Offset(-600, 0),
      );
      await tester.pumpAndSettle();
      await tester.tap(find.text('Person 7'));
      expect(opened, 7);
      expect(tester.takeException(), isNull);
    },
  );
  test('short keyboard/landscape layouts prioritize searchable results without overflow', () {
    expect(
      ngelx560ShowProfiles(const MediaQueryData(size: Size(393, 850))),
      true,
    );
    expect(
      ngelx560ShowProfiles(
        const MediaQueryData(
          size: Size(320, 568),
          viewInsets: EdgeInsets.only(bottom: 250),
        ),
      ),
      false,
    );
    expect(
      ngelx560ShowProfiles(const MediaQueryData(size: Size(640, 320))),
      false,
    );
    expect(ngelx560ProfileHeight(const TextScaler.linear(2)), 180);
  });
}

class _HeaderHarness extends StatefulWidget {
  const _HeaderHarness({super.key});
  @override
  State<_HeaderHarness> createState() => _HeaderHarnessState();
}

class _HeaderHarnessState extends State<_HeaderHarness> {
  final controller = TextEditingController(), focus = FocusNode();
  bool open = false;
  String query = '';
  int created = 0;
  @override
  void dispose() {
    controller.dispose();
    focus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: Ngelx560InboxHeader(
      title: 'Gelen Kutusu',
      searchHint: 'Sohbetlerde ara',
      searchOpen: open,
      controller: controller,
      focusNode: focus,
      onChanged: (s) => setState(() => query = s.trim().toLowerCase()),
      onToggleSearch: () => setState(() {
        open = !open;
        if (!open) {
          controller.clear();
          query = '';
          focus.unfocus();
        }
      }),
      onNew: () => created++,
    ),
  );
}
