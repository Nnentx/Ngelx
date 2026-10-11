// Input classification only. This does not resolve accounts or authenticate.
enum LoginIdentifierKind { email, username, phone }

class LoginIdentifier {
  final LoginIdentifierKind kind;
  final String value;
  const LoginIdentifier(this.kind, this.value);
}

LoginIdentifier parseLoginIdentifier(String input) {
  final value = input.trim();
  if (value.isEmpty || value.length > 254) {
    throw const FormatException('Giriş bilgini kontrol et.');
  }
  if (value.contains('@')) {
    if (!RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(value)) {
      throw const FormatException('Geçerli bir e-posta gir.');
    }
    return LoginIdentifier(LoginIdentifierKind.email, value.toLowerCase());
  }
  // Require an explicit country code. Never guess from locale or interpret a
  // numeric username as a telephone number.
  if (value.startsWith('+')) {
    final phone = value.replaceAll(RegExp(r'[ ()-]'), '');
    if (!RegExp(r'^\+[1-9][0-9]{7,14}$').hasMatch(phone)) {
      throw const FormatException('Telefonu ülke koduyla gir.');
    }
    return LoginIdentifier(LoginIdentifierKind.phone, phone);
  }
  if (!RegExp(r'^[a-zA-Z0-9._]{3,20}$').hasMatch(value)) {
    throw const FormatException(
      'Kullanıcı adı 3–20 karakter olmalı; boşluk kullanılamaz.',
    );
  }
  return LoginIdentifier(LoginIdentifierKind.username, value.toLowerCase());
}
