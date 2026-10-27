import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import '../lib/main.dart';

void main() {
  const values = <String, dynamic>{
    'chips': 5270,
    'gems': 0,
    'level': 1,
    'xp': 165,
    'wins': 2,
    'losses': 2,
    'streak': 2,
    'receivedGifts': <String, int>{},
  };
  const profile = <String, dynamic>{'displayName': 'ADEM baykar'};
  testWidgets(
    'reference statistics uses four columns, real refresh and badge details',
    (t) async {
      await t.binding.setSurfaceSize(const Size(400, 820));
      addTearDown(() => t.binding.setSurfaceSize(null));
      var calls = 0;
      await t.pumpWidget(
        MaterialApp(
          home: Ngelx581StatsScreen(
            stats: values,
            profile: profile,
            request: (body) async {
              calls++;
              expect(body['action'], 'wallet');
              return {...values, 'chips': 5300, 'wins': 3};
            },
          ),
        ),
      );
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      final grid = t.widget<GridView>(
        find.byKey(const ValueKey('ludo-stats-grid')),
      );
      expect(
        (grid.gridDelegate as SliverGridDelegateWithFixedCrossAxisCount)
            .crossAxisCount,
        4,
      );
      expect(find.text('ADEM baykar'), findsOneWidget);
      expect(find.text('5270'), findsNWidgets(2));
      // Preserve the server's XP threshold instead of copying sample mockup values.
      expect(find.text('165 / 200 XP'), findsOneWidget);
      await t.tap(find.byTooltip('Puanları yenile'));
      await t.pumpAndSettle();
      expect(calls, 1);
      expect(find.text('5300'), findsNWidgets(2));
      await t.tap(find.byTooltip('Oyun geçmişini filtrele'));
      await t.pumpAndSettle();
      await t.tap(find.text('Kazanılan').last);
      await t.pumpAndSettle();
      expect(find.text('Kaybedilen oyunlar'), findsNothing);
      await t.ensureVisible(find.text('Tüm rozetler'));
      await t.tap(find.text('Tüm rozetler'));
      await t.pumpAndSettle();
      expect(find.text('Tüm rozetler'), findsNWidgets(2));
      expect(find.text('50 oyun kazan · Kilitli'), findsOneWidget);
      expect(t.takeException(), isNull);
    },
  );
  testWidgets('empty wallet and failed refresh keep data visible', (t) async {
    await t.binding.setSurfaceSize(const Size(320, 740));
    addTearDown(() => t.binding.setSurfaceSize(null));
    await t.pumpWidget(
      MaterialApp(
        home: Ngelx581StatsScreen(
          stats: const {},
          profile: profile,
          request: (_) async => throw Exception('offline'),
        ),
      ),
    );
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    await t.tap(find.byTooltip('Puanları yenile'));
    await t.pumpAndSettle();
    expect(find.text('Puanlar yenilenemedi. Tekrar dene.'), findsOneWidget);
    expect(find.text('ADEM baykar'), findsOneWidget);
    expect(t.takeException(), isNull);
  });
  testWidgets('reference screenshots and lobby selection at phone widths', (
    t,
  ) async {
    final f = File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
    if (f.existsSync()) {
      final loader = FontLoader('Roboto')
        ..addFont(Future.value(ByteData.sublistView(f.readAsBytesSync())));
      await loader.load();
    }
    final icons = FontLoader('MaterialIcons')
      ..addFont(rootBundle.load('fonts/MaterialIcons-Regular.otf'));
    await icons.load();
    Future<void> decodeArt() async {
      final context = t.element(find.byKey(const ValueKey('screen')));
      await t.runAsync(() async {
        for (final name in [
          'stats_header',
          'lobby_header',
          'chips',
          'gems',
          'level',
          'xp',
          'wins',
          'losses',
          'gifts',
          'streak',
          'first',
          'winner',
          'series',
          'locked',
        ]) {
          await precacheImage(AssetImage('assets/ludo582/$name.png'), context);
        }
      });
      await t.pumpAndSettle();
    }

    await t.binding.setSurfaceSize(const Size(400, 820));
    addTearDown(() => t.binding.setSurfaceSize(null));
    await t.pumpWidget(
      const MaterialApp(
        home: RepaintBoundary(
          key: ValueKey('screen'),
          child: Ngelx581StatsScreen(stats: values, profile: profile),
        ),
      ),
    );
    await t.pumpAndSettle();
    await decodeArt();
    expect(t.takeException(), isNull);
    await expectLater(
      find.byKey(const ValueKey('screen')),
      matchesGoldenFile('screenshots/build582-stats.png'),
    );
    await t.pumpWidget(
      const MaterialApp(
        home: RepaintBoundary(
          key: ValueKey('screen'),
          child: Ngelx565LudoLobby(userId: 'preview'),
        ),
      ),
    );
    await t.pumpAndSettle();
    await decodeArt();
    expect(t.takeException(), isNull);
    await expectLater(
      find.byKey(const ValueKey('screen')),
      matchesGoldenFile('screenshots/build582-lobby.png'),
    );
    await t.tap(find.text('Makineye karşı oyna'));
    await t.pumpAndSettle();
    expect(find.text('Oda oluştur'), findsNothing);
    await t.scrollUntilVisible(
      find.text('Zorluk'),
      120,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.text('Kolay'), findsOneWidget);
    expect(t.takeException(), isNull);
  });
}
