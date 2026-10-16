import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/call_camera_lifecycle.dart';

void main() {
  test('background pauses video and resume restores requested camera', () async {
    final calls = <bool>[];
    final controller = CallCameraLifecycle((v) async => calls.add(v));
    await controller.sync(force: true);
    await controller.setForeground(false);
    await controller.setForeground(true);
    expect(calls, [true, false, true]);
  });
  test('user camera-off choice survives pause, resume and reconnect', () async {
    final calls = <bool>[];
    final controller = CallCameraLifecycle((v) async => calls.add(v));
    await controller.sync();
    await controller.setCameraWanted(false);
    await controller.setForeground(false);
    await controller.setForeground(true);
    await controller.sync(force: true);
    expect(calls, [true, false, false]);
  });
  test('in-flight camera enable is followed by background disable', () async {
    final gate = Completer<void>(), entered = Completer<void>();
    final calls = <bool>[];
    final controller = CallCameraLifecycle((v) async {
      calls.add(v);
      if (calls.length == 1) { entered.complete(); await gate.future; }
    });
    final starting = controller.sync();
    await entered.future;
    final pausing = controller.setForeground(false);
    gate.complete();
    await Future.wait([starting, pausing]);
    expect(calls, [true, false]);
  });
  test('reconnect force reapplies settings after another operation completes', () async {
    final gate = Completer<void>(), entered = Completer<void>();
    final calls = <bool>[];
    final controller = CallCameraLifecycle((v) async {
      calls.add(v);
      if (calls.length == 1) { entered.complete(); await gate.future; }
    });
    final first = controller.sync();
    await entered.future;
    final reconnect = controller.sync(force: true);
    gate.complete();
    await Future.wait([first, reconnect]);
    expect(calls, [true, true]);
  });
  test('stopped call cannot reopen camera through queued resume', () async {
    final calls = <bool>[];
    final controller = CallCameraLifecycle((v) async => calls.add(v));
    final resume = controller.setForeground(true);
    controller.stop();
    await resume;
    expect(calls, isEmpty);
  });
  test('failed operation can retry without poisoning the queue', () async {
    var attempts = 0;
    final controller = CallCameraLifecycle((_) async {
      if (++attempts == 1) throw StateError('camera unavailable');
    });
    await expectLater(controller.sync(), throwsStateError);
    await controller.sync();
    expect(attempts, 2);
  });
}
