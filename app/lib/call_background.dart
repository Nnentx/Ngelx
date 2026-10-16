import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class BackgroundCall {
  static const _channel = MethodChannel('com.nnentx.ngelx_app/active_call');
  static int _sequence = 0;
  static BackgroundCall? _active;
  final String sessionId;
  final VoidCallback onReturn, onUnavailable;
  BackgroundCall(String room, {required this.onReturn, required this.onUnavailable})
      : sessionId = '${room}_${DateTime.now().microsecondsSinceEpoch}_${++_sequence}';
  Future<bool> start() async {
    if (!Platform.isAndroid) return false;
    _active = this;
    _channel.setMethodCallHandler((call) async {
      final current = _active;
      if (current == null || (call.arguments as Map?)?['sessionId'] != current.sessionId) return;
      if (call.method == 'returnToCall') current.onReturn();
      if (call.method == 'unavailable') current.onUnavailable();
    });
    try { return await _channel.invokeMethod<bool>('start', {'sessionId': sessionId}) ?? false; }
    on PlatformException { return false; }
    on MissingPluginException { return false; }
  }
  Future<void> stop() async {
    if (identical(_active, this)) _active = null;
    if (!Platform.isAndroid) return;
    try { await _channel.invokeMethod<void>('stop', {'sessionId': sessionId}); }
    on PlatformException { /* Local room cleanup still proceeds. */ }
    on MissingPluginException { /* Unsupported platform. */ }
  }
}
