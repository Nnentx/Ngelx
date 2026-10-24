import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

import '../lib/main.dart'
    show
        ngelx559ThreeMonths,
        ngelx559MentionQuery,
        ngelx559ActiveMentions,
        Ngelx559IdentityHint,
        Ngelx559VerificationPage,
        Ngelx437MessageJump;

class _User extends Fake implements User {
  @override
  String get uid => 'test559';
  @override
  String get email => 'test@example.test';
}

void main() {
  test('calendar quarter clamps day and preserves time in UTC', () {
    expect(
      ngelx559ThreeMonths(DateTime.utc(2026, 1, 31, 23, 12)),
      DateTime.utc(2026, 4, 30, 23, 12),
    );
    expect(
      ngelx559ThreeMonths(DateTime.utc(2023, 11, 30)),
      DateTime.utc(2024, 2, 29),
    );
  });
  test('mention search matches @, direct Turkish names, and prunes removed handles', () {
    expect(ngelx559MentionQuery('@'), '');
    expect(ngelx559MentionQuery('Rızgar'), 'rizgar');
    expect(ngelx559MentionQuery('@RIZGAR'), 'rizgar');
    expect(ngelx559MentionQuery('r'), isNull);
    expect(
      ngelx559ActiveMentions('Merhaba @yilmaz', {
        'yilmaz': 'UID-A',
        'removed': 'UID-B',
      }),
      {'yilmaz': 'UID-A'},
    );
  });
  testWidgets(
    'identity hint shows separate eligibility dates on narrow screen',
    (tester) async {
      tester.view.physicalSize = const Size(320, 720);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Ngelx559IdentityHint(
              data: {
                'displayNameChangedAt559': Timestamp.fromDate(
                  DateTime.utc(2090, 1, 31),
                ),
              },
            ),
          ),
        ),
      );
      expect(find.textContaining('30.04.2090'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );
  testWidgets(
    'verification screen scrolls above bottom navigation, check is debounced, resend cooldown survives remount',
    (tester) async {
      SharedPreferences.setMockInitialValues({
        'verification559_test559': DateTime.now().millisecondsSinceEpoch,
      });
      tester.view.physicalSize = const Size(320, 500);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      var checks = 0;
      await tester.pumpWidget(
        MaterialApp(
          home: MediaQuery(
            data: const MediaQueryData(
              size: Size(320, 500),
              padding: EdgeInsets.only(bottom: 40),
            ),
            child: Ngelx559VerificationPage(
              user: _User(),
              onCheck: () async {
                checks++;
              },
              onSignOut: () async {},
            ),
          ),
        ),
      );
      await tester.pump();
      await tester.pump();
      expect(find.textContaining('Yeniden gönder ('), findsOneWidget);
      await tester.ensureVisible(find.text('Doğruladım, kontrol et'));
      await tester.tap(find.text('Doğruladım, kontrol et'));
      await tester.pump();
      expect(checks, 1);
      await tester.ensureVisible(find.text('Başka hesapla giriş yap'));
      await tester.pump();
      expect(
        tester.getBottomLeft(find.text('Başka hesapla giriş yap')).dy,
        lessThanOrEqualTo(460),
      );
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(const SizedBox());
    },
  );
  testWidgets(
    'sent media follows final layout but explicit cancellation preserves old reading position',
    (tester) async {
      final key = GlobalKey<_FollowState>();
      await tester.pumpWidget(MaterialApp(home: _Follow(key: key)));
      await tester.pump();
      key.currentState!.scroll.jumpTo(
        key.currentState!.scroll.position.maxScrollExtent,
      );
      key.currentState!.followSentMedia559();
      key.currentState!.grow();
      await tester.pump();
      await tester.pump();
      expect(
        key.currentState!.scroll.offset,
        key.currentState!.scroll.position.maxScrollExtent,
      );
      key.currentState!.cancelMediaFollow559();
      key.currentState!.scroll.jumpTo(100);
      key.currentState!.grow();
      key.currentState!.followSentMedia559();
      await tester.pump();
      expect(key.currentState!.scroll.offset, 100);
      await tester.pumpWidget(const SizedBox());
    },
  );
}

class _Follow extends StatefulWidget {
  const _Follow({super.key});
  @override
  State<_Follow> createState() => _FollowState();
}

class _FollowState extends State<_Follow> with Ngelx437MessageJump<_Follow> {
  final scroll = ScrollController();
  double height = 1800;
  @override
  String get jumpChatId => 'test';
  @override
  ScrollController get jumpScroll => scroll;
  void grow() => setState(() => height += 300);
  @override
  void dispose() {
    scroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SingleChildScrollView(
      controller: scroll,
      child: SizedBox(height: height, child: const Text('sent media')),
    ),
  );
}
