import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('relative times omit clock and seconds', () {
    final now = DateTime(2026, 10, 14, 16, 0);
    expect(
      ngelx456Time(
        Timestamp.fromDate(now.subtract(const Duration(seconds: 45))),
        now: now,
      ),
      'Az önce',
    );
    expect(
      ngelx456Time(
        Timestamp.fromDate(now.subtract(const Duration(minutes: 4))),
        now: now,
      ),
      '4 dk önce',
    );
    expect(
      ngelx456Time(
        Timestamp.fromDate(now.subtract(const Duration(days: 1))),
        now: now,
      ),
      'Dün',
    );
  });
  test('infrastructure failures never leak host or stack trace', () {
    expect(
      ngelx456Error(
        Exception(
          'UPLOAD upload-r2 NATIVE_R2_PUT UnknownHostException unable to resolve host secret',
        ),
      ),
      isNot(contains('secret')),
    );
    expect(
      ngelx456DnsFailure(Exception('SocketException: Failed host lookup')),
      isTrue,
    );
  });
  test('invite parsing rejects path and malformed codes', () {
    expect(ngelx456InviteCode('Hello\nngelx://community/AbC_123'), 'AbC_123');
    expect(ngelx456InviteCode('https://example.com'), isNull);
  });
  testWidgets('malformed invite never crashes on tap', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Ngelx456InviteCard(
            text: 'Bozuk bağlantı',
            own: false,
          ),
        ),
      ),
    );
    expect(find.text('Davet bağlantısı geçersiz'), findsOneWidget);
    await tester.tap(find.text('Davet bağlantısı geçersiz'));
    await tester.pump();
    expect(tester.takeException(), isNull);
  });
  testWidgets('valid invite remains visibly actionable', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Ngelx456InviteCard(
            text: 'Davetin hazır\\nngelx://community/AbC_123',
            own: false,
          ),
        ),
      ),
    );
    expect(find.text('Daveti aç →'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
  for (final size in [const Size(320, 640), const Size(390, 844)])
    testWidgets('empty state fits ${size.width}', (tester) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ListView(children: [Ngelx456Empty(onCreate: () {})]),
          ),
        ),
      );
      expect(find.text('İlk paylaşım senden olsun'), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
}
