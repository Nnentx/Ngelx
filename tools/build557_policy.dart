// Read old display values defensively without changing stored data.
double ngelx557CoverAlignment(Object? value) {
  final number = value is num ? value.toDouble() :
      value is String ? double.tryParse(value.trim()) : null;
  if (number == null || !number.isFinite) return 0;
  return number.clamp(-1.0, 1.0).toDouble();
}

String ngelx557MediaUrl(Object? value) {
  if (value is! String) return '';
  final text = value.trim(), uri = Uri.tryParse(value.trim());
  if (uri == null || !['https', 'http'].contains(uri.scheme) || uri.host.isEmpty) return '';
  return text;
}

List<String> ngelx557Ids(Object? value) => value is List
    ? value.whereType<String>().where((id) => id.isNotEmpty).toList()
    : const [];
