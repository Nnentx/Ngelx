import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/live_config.dart';

void main() {
  test('live endpoint accepts HTTPS function and Cloud Run URLs', () {
    expect(validLiveEndpoint('https://europe-west1-example.cloudfunctions.net/ngelxLive'), isTrue);
    expect(validLiveEndpoint('https://example.run.app/'), isTrue);
  });
  test('missing or malformed endpoint disables live access', () {
    for (final endpoint in ['', 'https://', 'not-a-url', 'http://example.com',
      'https://user:password@example.com', 'https://example.com?token=secret', 'https://example.com#token']) {
      expect(validLiveEndpoint(endpoint), isFalse, reason: endpoint);
    }
  });
}
