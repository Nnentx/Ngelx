import 'build438_login_identifier.dart';

void main() {
  void valid(String input, LoginIdentifierKind kind, String value) {
    final result = parseLoginIdentifier(input);
    if (result.kind != kind || result.value != value) {
      throw StateError('Incorrect classification: $input');
    }
  }
  void invalid(String input) {
    try {
      parseLoginIdentifier(input);
    } on FormatException {
      return;
    }
    throw StateError('Unexpected acceptance: $input');
  }
  valid(' USER.Name_1 ', LoginIdentifierKind.username, 'user.name_1');
  valid('1234567890', LoginIdentifierKind.username, '1234567890');
  valid('abcdefghijklmnopqrst', LoginIdentifierKind.username,
      'abcdefghijklmnopqrst');
  valid(' USER@Example.COM ', LoginIdentifierKind.email, 'user@example.com');
  valid('+90 (555) 123-45-67', LoginIdentifierKind.phone, '+905551234567');
  for (final input in [
    '', 'ab', 'abcdefghijklmnopqrstu', 'user name', 'user\nname',
    'user@example', '+05551234567', '+90555', '+90555123456789012',
    '+90abc1234567', 'user/name',
  ]) {
    invalid(input);
  }
  print('Login identifier validation passed (16 cases).');
}
