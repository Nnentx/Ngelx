import 'package:flutter_test/flutter_test.dart';
import '../lib/build444_call_session.dart';
void main() {
  test('pending launch excludes another private or group call', () {
    final s=NgelxCallSession444();
    expect(s.reserve('private-a'),isTrue);
    expect(s.reserve('group-b'),isFalse);
    expect(s.attach('private-a'),isTrue);
    expect(s.attach('private-a'),isFalse);
  });
  test('minimized call keeps ownership and resumes once', () {
    final s=NgelxCallSession444()..reserve('a')..attach('a');
    s.minimize('a');
    s.releasePending('a');
    expect(s.reserve('b'),isFalse);
    expect(s.attach('a'),isTrue);
    expect(s.attach('a'),isFalse);
  });
  test('late connection is invalid after end and after new call', () {
    final s=NgelxCallSession444()..reserve('a');
    final epoch=s.generation;
    s.release('a');
    expect(s.current('a',epoch),isFalse);
    s.reserve('a');
    expect(s.current('a',epoch),isFalse);
    s.release('different');
    expect(s.busy,isTrue);
  });
  test('failed pending launch releases without ending a minimized call', () {
    final s=NgelxCallSession444()..reserve('a');
    s.releasePending('a');
    expect(s.busy,isFalse);
    expect(s.reserve('b'),isTrue);
  });
}
