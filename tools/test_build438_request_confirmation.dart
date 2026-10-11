import 'dart:async';
import 'build438_request_confirmation.dart';

Future<void> main() async {
  var checks = 0;
  Future<bool> confirm() async { checks++; return true; }
  if (!await ngelx438AwaitRequest(Future.value(true), confirm)) throw StateError('success');
  if (await ngelx438AwaitRequest(Future.value(false), confirm)) throw StateError('already pending');
  if (checks != 0) throw StateError('unnecessary confirmation');
  final pending = Completer<bool>();
  if (!await ngelx438AwaitRequest(pending.future, confirm, timeout: Duration.zero)) throw StateError('confirmed commit');
  pending.complete(true);
  for (final confirmation in <Future<bool> Function()>[
    () async => false,
    () async => throw StateError('offline'),
  ]) {
    final delayed = Completer<bool>();
    try {
      await ngelx438AwaitRequest(delayed.future, confirmation, timeout: Duration.zero);
      throw StateError('uncertain commit reported as successful');
    } on TimeoutException {
      delayed.complete(false);
    }
  }
  try {
    await ngelx438AwaitRequest(Future.error(StateError('denied')), confirm);
    throw ArgumentError('failure swallowed');
  } on StateError { }
  if (checks != 1) throw StateError('confirmation count');
  print('Social request confirmation: 6 scenarios passed');
}
