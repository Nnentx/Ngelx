import 'dart:async';

/// A timeout does not cancel a Firestore transaction. Confirm only this attempt.
Future<bool> ngelx438AwaitRequest(
  Future<bool> commit,
  Future<bool> Function() confirmed, {
  Duration timeout = const Duration(seconds: 12),
}) async {
  try {
    return await commit.timeout(timeout);
  } on TimeoutException {
    try {
      if (await confirmed()) return true;
    } catch (_) {
      // Keep the original uncertain result when confirmation is unavailable.
    }
    rethrow;
  }
}
