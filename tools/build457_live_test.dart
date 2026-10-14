import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('Live preview uses a finite retry threshold rather than endless spinner', () {
    expect(ngelx457CanRetryLiveVideo(
      cameraEnabled: true, reconnecting: false,
      elapsedWithoutVideoSeconds: 9), isFalse);
    expect(ngelx457CanRetryLiveVideo(
      cameraEnabled: true, reconnecting: false,
      elapsedWithoutVideoSeconds: 10), isTrue);
    expect(ngelx457CanRetryLiveVideo(
      cameraEnabled: true, reconnecting: false,
      elapsedWithoutVideoSeconds: 30), isTrue);
    expect(ngelx457CanRetryLiveVideo(
      cameraEnabled: false, reconnecting: false,
      elapsedWithoutVideoSeconds: 30), isFalse);
    expect(ngelx457CanRetryLiveVideo(
      cameraEnabled: true, reconnecting: true,
      elapsedWithoutVideoSeconds: 30), isFalse);
  });
}
