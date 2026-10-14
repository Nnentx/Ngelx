part of 'main.dart';

String ngelx455ProfileName(Map<String, dynamic> profile,
    {String fallback = 'Üye'}) {
  for (final key in ['displayName', 'name', 'fullName', 'username']) {
    final value = (profile[key] ?? '').toString().trim();
    if (value.isNotEmpty && value != 'NgelX') return value;
  }
  return fallback;
}

void ngelx455Status(BuildContext context, String message, {bool error = false}) {
  if (!context.mounted) return;
  final messenger = ScaffoldMessenger.of(context);
  messenger.hideCurrentSnackBar();
  messenger.showSnackBar(SnackBar(
    behavior: SnackBarBehavior.floating,
    backgroundColor: error ? const Color(0xFFB42335) : const Color(0xFF6744C8),
    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
    content: Row(children: [
      Icon(error ? Icons.error_outline : Icons.check_circle_outline,
          size: 18, color: Colors.white),
      const SizedBox(width: 8),
      Expanded(child: Text(message,
          style: const TextStyle(fontSize: 13, color: Colors.white))),
    ]),
  ));
}
