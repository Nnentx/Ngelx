part of 'main.dart';

// The comment sheet handles its own keyboard insets. Keep the underlying
// profile media viewport and repaint layer stable throughout that animation.
class Ngelx561KeyboardStableMedia extends StatelessWidget {
  final Widget child;
  const Ngelx561KeyboardStableMedia({super.key, required this.child});
  @override
  Widget build(BuildContext context) {
    final media = MediaQuery.of(context);
    return MediaQuery(
      data: media.copyWith(
        viewInsets: EdgeInsets.zero,
        padding: media.viewPadding,
      ),
      child: RepaintBoundary(child: child),
    );
  }
}

String ngelx561First(Map<String, dynamic> data, List<String> keys) {
  for (final key in keys) {
    final value = (data[key] ?? '').toString().trim();
    if (value.isNotEmpty) return value;
  }
  return '';
}

bool ngelx561IsCommunity(Map<String, dynamic> data) {
  if (data['targetKind'] == 'community' ||
      ngelx561First(data, ['communityId']).isNotEmpty)
    return true;
  for (final key in ['eventKind', 'type']) {
    if ((data[key] ?? '').toString().startsWith('community_')) return true;
  }
  // Legacy community events carried their meaning only in the text.
  final text = ngelx561First(data, [
    'text',
    'message',
    'content',
  ]).toLowerCase();
  return text.contains('topluluğa katılmak') ||
      text.contains('toplulukta yeni bir gönderi') ||
      text.contains('topluluğuna katılmak');
}

String ngelx561CommunityName(Map<String, dynamic> data) {
  for (final key in ['targetTitle', 'communityName', 'communityTitle']) {
    final value = (data[key] ?? '').toString().trim();
    if (value.isNotEmpty &&
        !['topluluk', 'community'].contains(value.toLowerCase()))
      return value;
  }
  return '';
}

String ngelx561Upper(String name) =>
    name.replaceAll('i', 'İ').replaceAll('ı', 'I').toUpperCase();

class Ngelx561ResolvedCommunityNotice extends StatefulWidget {
  final Map<String, dynamic> data;
  final bool read;
  const Ngelx561ResolvedCommunityNotice({
    super.key,
    required this.data,
    required this.read,
  });
  @override
  State<Ngelx561ResolvedCommunityNotice> createState() =>
      _Ngelx561ResolvedCommunityNoticeState();
}

class _Ngelx561ResolvedCommunityNoticeState
    extends State<Ngelx561ResolvedCommunityNotice> {
  Future<DocumentSnapshot<Map<String, dynamic>>>? _name;
  String get _id => ngelx561First(widget.data, [
    'communityId',
    'sourceId',
    'belgeId',
    'targetId',
  ]);
  void _load() {
    _name = ngelx561CommunityName(widget.data).isNotEmpty || _id.isEmpty
        ? null
        : _communities450.doc(_id).get().timeout(const Duration(seconds: 6));
  }

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didUpdateWidget(covariant Ngelx561ResolvedCommunityNotice oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (ngelx561First(oldWidget.data, [
              'communityId',
              'sourceId',
              'belgeId',
              'targetId',
            ]) !=
            _id ||
        ngelx561CommunityName(oldWidget.data) !=
            ngelx561CommunityName(widget.data))
      _load();
  }

  @override
  Widget build(BuildContext context) {
    if (_name == null)
      return Ngelx561CommunityNotice(data: widget.data, read: widget.read);
    return FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      future: _name,
      builder: (_, snap) {
        final name = (snap.data?.data()?['name'] ?? '').toString().trim();
        return Ngelx561CommunityNotice(
          data: {...widget.data, if (name.isNotEmpty) 'targetTitle': name},
          read: widget.read,
        );
      },
    );
  }
}

class Ngelx561CommunityNotice extends StatelessWidget {
  final Map<String, dynamic> data;
  final bool read;
  const Ngelx561CommunityNotice({
    super.key,
    required this.data,
    required this.read,
  });
  @override
  Widget build(BuildContext context) {
    final actor = ngelx561First(data, ['senderName', 'fromName']);
    final name = ngelx561CommunityName(data);
    var event = ngelx561First(data, ['eventKind', 'type']);
    final text = ngelx561First(data, [
      'text',
      'message',
      'content',
    ]).toLowerCase();
    if (!event.startsWith('community_')) {
      if (text.contains('katılmak istiyor'))
        event = 'community_join_request';
      else if (text.contains('yeni bir gönderi'))
        event = 'community_post';
    }
    final action = switch (event) {
      'community_post' => ' topluluğunda yeni bir gönderi paylaştı.',
      'community_post_approved' => ' topluluğunda bir gönderiyi onayladı.',
      'community_post_pending' =>
        ' topluluğuna onay için bir gönderi gönderdi.',
      'community_join_request' => ' topluluğuna katılmak istiyor.',
      _ => ' topluluğunda yeni bir etkinlik var.',
    };
    if (name.isEmpty) {
      // Never invent a community name when a legacy record cannot be resolved.
      return Text(
        ngelxBildirimMetni(data),
        style: TextStyle(
          color: read ? Colors.black54 : Colors.black87,
          fontWeight: read ? FontWeight.w400 : FontWeight.w700,
        ),
      );
    }
    return Text.rich(
      TextSpan(
        children: [
          TextSpan(
            text: '${actor.isEmpty ? 'Bir kullanıcı' : actor} ',
            style: TextStyle(
              color: read ? const Color(0xFF8B789F) : const Color(0xFF60309A),
              fontWeight: FontWeight.w800,
            ),
          ),
          TextSpan(
            text: ngelx561Upper(name),
            style: const TextStyle(
              color: Color(0xFF8651D8),
              fontWeight: FontWeight.w900,
            ),
          ),
          TextSpan(
            text: action,
            style: TextStyle(
              color: read ? Colors.black54 : const Color(0xFF18131F),
              fontWeight: read ? FontWeight.w400 : FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}

const ngelx561VerificationEndpoint = String.fromEnvironment(
  'NGELX_VERIFICATION_EMAIL_URL',
);

Future<void> ngelx561SendVerification(User user) async {
  if (ngelx561VerificationEndpoint.isEmpty) {
    // Keep the working native sender until the custom service is configured.
    await user.sendEmailVerification().timeout(const Duration(seconds: 12));
    return;
  }
  final uri = Uri.tryParse(ngelx561VerificationEndpoint);
  if (uri == null ||
      uri.scheme != 'https' ||
      uri.host.isEmpty ||
      uri.userInfo.isNotEmpty) {
    throw StateError('Doğrulama hizmeti yapılandırması geçersiz.');
  }
  final token = await user.getIdToken().timeout(const Duration(seconds: 8));
  if (token == null || token.isEmpty)
    throw StateError('Doğrulama için yeniden giriş yap.');
  final response = await Dio().postUri<dynamic>(
    uri,
    data: <String, dynamic>{},
    options: Options(
      headers: {'Authorization': 'Bearer $token'},
      contentType: 'application/json',
      sendTimeout: const Duration(seconds: 12),
      receiveTimeout: const Duration(seconds: 20),
    ),
  );
  final result = response.data;
  if (result is! Map ||
      (result['sent'] != true && result['verified'] != true)) {
    throw StateError('Doğrulama e-postası gönderilemedi. Tekrar dene.');
  }
}
