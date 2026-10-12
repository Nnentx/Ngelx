import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build443_capture_guard.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  const channel = MethodChannel('com.nnentx.ngelx_app/capture');
  late Set<String> leases;
  late List<MethodCall> calls;
  late StreamController<bool> privacy;
  setUp(() {
    leases = {}; calls = []; privacy = StreamController<bool>();
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (call) async {
      calls.add(call);
      final args = Map<String, dynamic>.from(call.arguments as Map);
      if (args['secure'] == true) { leases.add(args['lease'] as String); }
      else { leases.remove(args['lease']); }
      return null;
    });
  });
  tearDown(() async {
    await privacy.close();
    debugDefaultTargetPlatformOverride = null;
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel, null);
  });
  Widget profile({String uid='alice', Stream<bool>? stream, Widget? child}) => MaterialApp(home:
      NgelxProfileCaptureGuard(uid:uid, privacyStream:stream??privacy.stream,
          child:child??const Text('private profile')));

  void captureTest(String name, Future<void> Function(WidgetTester) body) {
    testWidgets(name, (tester) async {
      debugDefaultTargetPlatformOverride = TargetPlatform.android;
      try { await body(tester); }
      finally { debugDefaultTargetPlatformOverride = null; }
    });
  }

  captureTest('content waits for native protection acknowledgement', (tester) async {
    final ack = Completer<void>();
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (_) async { await ack.future; return null; });
    await tester.pumpWidget(profile());
    expect(find.text('private profile'), findsNothing);
    ack.complete(); await tester.pump();
    expect(find.text('private profile'), findsOneWidget);
    await tester.pumpWidget(const SizedBox()); await tester.pump();
  });

  captureTest('only explicit allow releases protection; errors restore protection', (tester) async {
    await tester.pumpWidget(profile()); await tester.pump();
    expect(leases.length, 1);
    privacy.add(true); await tester.pump(); await tester.pump();
    expect(leases, isEmpty);
    privacy.addError(StateError('offline')); await tester.pump(); await tester.pump();
    expect(leases.length, 1);
    privacy.add(false); await tester.pump(); await tester.pump();
    expect(find.text('private profile'), findsOneWidget);
    await tester.pumpWidget(const SizedBox()); await tester.pump();
    expect(leases, isEmpty);
  });

  captureTest('nested profile removal cannot release its parent lease', (tester) async {
    final nestedPrivacy = StreamController<bool>();
    final nested = NgelxProfileCaptureGuard(uid:'bob', privacyStream:nestedPrivacy.stream,
        child:const Text('nested media'));
    await tester.pumpWidget(profile(child:nested)); await tester.pump(); await tester.pump();
    expect(leases.length, 2);
    await tester.pumpWidget(profile()); await tester.pump();
    expect(leases.length, 1);
    await tester.pumpWidget(const SizedBox()); await tester.pump();
    expect(leases, isEmpty);
    unawaited(nestedPrivacy.close());
  });

  captureTest('native failure never exposes profile content', (tester) async {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,
        (_) async => throw PlatformException(code:'SECURE_UNAVAILABLE'));
    await tester.pumpWidget(profile()); await tester.pump();
    expect(find.text('private profile'), findsNothing);
    expect(find.byIcon(Icons.refresh), findsOneWidget);
    await tester.pumpWidget(const SizedBox()); await tester.pump();
  });

  captureTest('old acknowledgement cannot reveal content after new privacy request', (tester) async {
    await tester.pumpWidget(profile()); await tester.pump();
    final first = Completer<void>(), second = Completer<void>();
    var request = 0;
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,
        (_) async { await (++request == 1 ? first.future : second.future); return null; });
    privacy.add(true); await tester.pump();
    privacy.add(false); await tester.pump();
    first.complete(); await tester.pump();
    expect(find.text('private profile'), findsNothing);
    second.complete(); await tester.pump();
    expect(find.text('private profile'), findsOneWidget);
    await tester.pumpWidget(const SizedBox()); await tester.pump();
  });
}
