import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('Build461: cover choice is honored even when remote cover URL is empty', () {
    expect(ngelx459KapaksizGorunum('cover',''), false);
    expect(ngelx459KapaksizGorunum('cover','https://example.com/x.jpg'), false);
    expect(ngelx459KapaksizGorunum('coverless','https://example.com/x.jpg'), true);
  });
  test('Build461: editor initializes from saved mode, not photo loading state', () {
    expect(ngelx461BaslangicProfilGorunumu('cover'), 'cover');
    expect(ngelx461BaslangicProfilGorunumu('coverless'), 'coverless');
    expect(ngelx461BaslangicProfilGorunumu(null), 'coverless');
  });
  test('Build461: media error code hides raw signed URL and categorizes reason', () {
    expect(ngelx461VideoHataKodu('HTTP 403 for /media/signed-token'), contains('V461-403'));
    expect(ngelx461VideoHataKodu('HTTP 404'), contains('V461-404'));
    expect(ngelx461VideoHataKodu('Unsupported codec'), contains('V461-FORMAT'));
    expect(ngelx461VideoHataKodu('Socket connection timeout'), contains('V461-AG'));
    expect(ngelx461VideoHataKodu('other'), contains('V461-PLAYER'));
    expect(ngelx461VideoHataKodu('HTTP 403 for /media/signed-token'), isNot(contains('signed-token')));
  });
}
