import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../lib/main.dart'
    show
        ngelx561IsCommunity,
        ngelx561CommunityName,
        ngelx561Upper,
        Ngelx561ResolvedCommunityNotice,
        NgelXYorumYazici,
        Ngelx561KeyboardStableMedia;

void main() {
  testWidgets(
    'profile media does not rebuild or shrink during keyboard animation',
    (tester) async {
      tester.view.physicalSize = const Size(393, 850);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      addTearDown(tester.view.resetViewInsets);
      var builds = 0;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            resizeToAvoidBottomInset: false,
            body: Ngelx561KeyboardStableMedia(
              child: Builder(
                builder: (context) {
                  builds++;
                  final media = MediaQuery.of(context);
                  return SizedBox(
                    key: const ValueKey('profile-media'),
                    width: media.size.width,
                    height: media.size.height,
                  );
                },
              ),
            ),
          ),
        ),
      );
      final before = builds;
      final size = tester.getSize(find.byKey(const ValueKey('profile-media')));
      for (final inset in [60.0, 120.0, 220.0, 300.0, 0.0]) {
        tester.view.viewInsets = FakeViewPadding(bottom: inset);
        await tester.pump(const Duration(milliseconds: 40));
        expect(builds, before);
        expect(
          tester.getSize(find.byKey(const ValueKey('profile-media'))),
          size,
        );
      }
      expect(tester.takeException(), isNull);
    },
  );
  test(
    'community variants and empty legacy fields resolve the actual name',
    () {
      for (final data in [
        {'targetKind': 'community', 'targetTitle': 'Ngel ailesi'},
        {
          'eventKind': 'community_join_request',
          'targetTitle': '',
          'communityName': 'Ngel ailesi',
        },
        {'type': 'community_join_request', 'communityName': 'Ngel ailesi'},
        {
          'type': 'interaction',
          'text': 'topluluğa katılmak istiyor',
          'communityName': 'Ngel ailesi',
        },
      ]) {
        expect(ngelx561IsCommunity(data), true);
        expect(ngelx561CommunityName(data), 'Ngel ailesi');
      }
      expect(
        ngelx561IsCommunity({
          'eventKind': 'group_join_request',
          'groupName': 'Arkadaşlar',
        }),
        false,
      );
      expect(
        ngelx561CommunityName({
          'targetTitle': 'Topluluk',
          'communityName': 'Bilim',
        }),
        'Bilim',
      );
      expect(ngelx561CommunityName({'targetTitle': 'Topluluk'}), '');
      expect(ngelx561Upper('bilim ışığı'), 'BİLİM IŞIĞI');
    },
  );
  for (final width in [280.0, 393.0, 600.0]) {
    testWidgets('community name is purple uppercase and wraps at $width', (
      tester,
    ) async {
      tester.view.physicalSize = Size(width, 800);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: MediaQuery(
              data: MediaQueryData(
                size: Size(width, 800),
                textScaler: const TextScaler.linear(1.5),
              ),
              child: const Ngelx561ResolvedCommunityNotice(
                data: {
                  'senderName': 'ADEM baykar',
                  'type': 'community_join_request',
                  'targetTitle': 'Bilim ve teknoloji topluluğu',
                },
                read: false,
              ),
            ),
          ),
        ),
      );
      final paragraph = tester.widget<Text>(find.byType(Text).first);
      final root = paragraph.textSpan as TextSpan;
      final title = root.children![1] as TextSpan;
      expect(title.text, 'BİLİM VE TEKNOLOJİ TOPLULUĞU');
      expect(title.style!.color, const Color(0xFF8651D8));
      expect(root.toPlainText(), contains('katılmak istiyor'));
      expect(tester.takeException(), isNull);
    });
  }
  testWidgets(
    'typing and keyboard animation do not rebuild the comments list',
    (tester) async {
      tester.view.physicalSize = const Size(393, 850);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final controller = TextEditingController();
      addTearDown(controller.dispose);
      var listBuilds = 0, sends = 0;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            resizeToAvoidBottomInset: false,
            body: Column(
              children: [
                Expanded(
                  child: Builder(
                    builder: (_) {
                      listBuilds++;
                      return ListView.builder(
                        itemCount: 80,
                        itemBuilder: (_, i) => Text('Yorum $i'),
                      );
                    },
                  ),
                ),
                NgelXYorumYazici(
                  controller: controller,
                  yanitYaziliyor: false,
                  gonderiliyor: false,
                  onGonder: () => sends++,
                ),
              ],
            ),
          ),
        ),
      );
      final before = listBuilds;
      await tester.tap(find.byType(TextField));
      for (final inset in [60.0, 120.0, 220.0, 300.0]) {
        tester.view.viewInsets = FakeViewPadding(bottom: inset);
        await tester.pump(const Duration(milliseconds: 40));
      }
      addTearDown(tester.view.resetViewInsets);
      await tester.enterText(
        find.byType(TextField),
        'Profil üzerinden hızlı bir yorum',
      );
      await tester.pumpAndSettle();
      expect(listBuilds, before);
      expect(controller.text, 'Profil üzerinden hızlı bir yorum');
      await tester.tap(find.byIcon(Icons.send_rounded));
      expect(sends, 1);
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(const SizedBox());
    },
  );
  testWidgets(
    'send spinner disables repeated submission while permission is checked',
    (tester) async {
      final controller = TextEditingController(text: 'yorum');
      addTearDown(controller.dispose);
      var sends = 0;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: NgelXYorumYazici(
              controller: controller,
              yanitYaziliyor: false,
              gonderiliyor: true,
              onGonder: () => sends++,
            ),
          ),
        ),
      );
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(
        tester.widget<IconButton>(find.byType(IconButton).last).onPressed,
        isNull,
      );
      expect(sends, 0);
      await tester.pumpWidget(const SizedBox());
    },
  );
}
