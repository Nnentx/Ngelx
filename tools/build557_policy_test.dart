import '../app/lib/build557_policy.dart';
void check(bool value, String reason) { if (!value) throw StateError(reason); }
void main() {
  for (final value in [null, 'bad', {}, [], double.nan, double.infinity, '-Infinity']) {
    check(ngelx557CoverAlignment(value) == 0, 'Malformed alignment: $value');
  }
  check(ngelx557CoverAlignment('0.5') == 0.5, 'Legacy numeric string');
  check(ngelx557CoverAlignment(9) == 1, 'Upper bound');
  check(ngelx557CoverAlignment(-9) == -1, 'Lower bound');
  for (final value in [null, 123, {}, '', 'https:', 'javascript:alert(1)', 'file:///tmp/a']) {
    check(ngelx557MediaUrl(value).isEmpty, 'Invalid media must not build a player');
  }
  check(ngelx557MediaUrl(' https://media.ngelxsocial.com/a?token=abc ') ==
      'https://media.ngelxsocial.com/a?token=abc', 'Keep signed media URL');
  check(ngelx557Ids(['real', null, 7, '', 'other']).join(',') == 'real,other',
      'Malformed IDs must not become members');
  check(ngelx557Ids({'real': true}).isEmpty, 'Unexpected shape grants no membership');
  print('Build557 legacy media, cover and membership edge cases passed');
}
