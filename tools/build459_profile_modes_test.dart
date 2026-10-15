import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('Build459: saved coverless always uses centered header', () {
    expect(ngelx459KapaksizGorunum('coverless', 'https://example.com/cover.png'), isTrue);
    expect(ngelx459KapaksizGorunum('coverless', ''), isTrue);
  });
  test('Build459: covered profile with a saved URL stays covered', () {
    expect(ngelx459KapaksizGorunum('cover', 'https://example.com/cover.png'), isFalse);
    expect(ngelx459KapaksizGorunum('', 'https://example.com/legacy.png'), isFalse);
  });
  test('Build459: missing cover URL safely falls back without deleting data', () {
    expect(ngelx459KapaksizGorunum('cover', ''), isTrue);
    expect(ngelx459KapaksizGorunum('', ''), isTrue);
  });
}
