part of 'main.dart';

const ngelx559IdentityUrl = String.fromEnvironment(
  'NGELX_PROFILE_IDENTITY_URL',
);
const ngelx559VerificationUrl = String.fromEnvironment(
  'NGELX_VERIFICATION_EMAIL_URL',
);
DateTime ngelx559ThreeMonths(DateTime value) {
  final d = value.toUtc(), month = d.month + 3;
  final last = DateTime.utc(d.year, month + 1, 0).day;
  return DateTime.utc(
    d.year,
    month,
    math.min(d.day, last),
    d.hour,
    d.minute,
    d.second,
    d.millisecond,
    d.microsecond,
  );
}

DateTime? ngelx559EligibleDate(dynamic raw) =>
    raw is Timestamp ? ngelx559ThreeMonths(raw.toDate()) : null;
String ngelx559DateLabel(DateTime d) {
  final v = d.toLocal();
  return '${v.day.toString().padLeft(2, '0')}.${v.month.toString().padLeft(2, '0')}.${v.year}';
}

String? ngelx559MentionQuery(String word) {
  final token = word.startsWith('@') ? word.substring(1) : word;
  if (!word.startsWith('@') &&
      (token.length < 2 ||
          !RegExp(r'^[\p{L}\p{N}_.]+$', unicode: true).hasMatch(token)))
    return null;
  return ngelx556Search(token);
}

String? ngelx559MentionEmptyLabel(String token, bool empty) =>
    token.startsWith('@') && empty ? 'Eşleşen grup üyesi bulunamadı.' : null;
Map<String, String> ngelx559ActiveMentions(
  String text,
  Map<String, String> handles,
) {
  final tokens = RegExp(r'@([A-Za-z0-9_ÇĞİÖŞÜçğıöşü.]+)')
      .allMatches(text)
      .map((m) => m.group(1))
      .toSet();
  return {
    for (final e in handles.entries)
      if (tokens.contains(e.key)) e.key: e.value,
  };
}

Future<Map<String, dynamic>> ngelx559AuthenticatedPost(
  String endpoint,
  Map<String, dynamic> body,
) async {
  final uri = Uri.tryParse(endpoint);
  if (uri == null ||
      uri.scheme != 'https' ||
      uri.host.isEmpty ||
      uri.userInfo.isNotEmpty)
    throw StateError('Bu hizmet henüz etkin değil. Daha sonra tekrar dene.');
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) throw StateError('Oturumun sona erdi. Yeniden giriş yap.');
  final token = await user.getIdToken();
  if (FirebaseAuth.instance.currentUser?.uid != user.uid)
    throw StateError('Hesabın değişti. İşlemi tekrar başlat.');
  try {
    final response =
        await Dio(
          BaseOptions(
            connectTimeout: const Duration(seconds: 8),
            receiveTimeout: const Duration(seconds: 20),
          ),
        ).postUri(
          uri,
          data: body,
          options: Options(
            headers: {'Authorization': 'Bearer $token'},
            validateStatus: (s) => s != null && s < 600,
          ),
        );
    final data = response.data is Map
        ? Map<String, dynamic>.from(response.data as Map)
        : <String, dynamic>{};
    if (response.statusCode == 200) return data;
    final code = data['error'];
    if (code == 'cooldown')
      throw StateError(
        'Üç aylık değişiklik süresi henüz dolmadı. Profilindeki sonraki değişiklik tarihini kontrol et.',
      );
    if (code == 'username-taken')
      throw StateError(
        'Bu kullanıcı adı kullanılıyor. Başka bir kullanıcı adı seç.',
      );
    if (code == 'invalid-username')
      throw StateError(
        'Bu kullanıcı adı kullanılamıyor. Başka bir kullanıcı adı seç.',
      );
    if (response.statusCode == 429)
      throw StateError('Çok sık denedin. Bir dakika sonra tekrar dene.');
    if (response.statusCode == 401)
      throw StateError('Oturumunu yenileyip tekrar dene.');
    throw StateError('İşlem tamamlanamadı. Lütfen tekrar dene.');
  } on DioException {
    throw StateError(
      'Bağlantı kurulamadı. İnternetini kontrol edip tekrar dene.',
    );
  }
}

Future<void> ngelx559SaveIdentity(
  Map<String, dynamic> changes, {
  required String expectedUid,
}) async {
  if (FirebaseAuth.instance.currentUser?.uid != expectedUid)
    throw StateError('Hesabın değişti. İşlemi tekrar başlat.');
  if (changes.isEmpty) return;
  await ngelx559AuthenticatedPost(ngelx559IdentityUrl, changes);
}

Future<void> ngelx559SendVerification(User user) async {
  if (FirebaseAuth.instance.currentUser?.uid != user.uid)
    throw StateError('Hesabın değişti. İşlemi tekrar başlat.');
  await FirebaseAuth.instance
      .setLanguageCode('tr')
      .timeout(const Duration(seconds: 6));
  if (ngelx559VerificationUrl.isNotEmpty) {
    await ngelx559AuthenticatedPost(ngelx559VerificationUrl, {});
  } else {
    await user.sendEmailVerification().timeout(const Duration(seconds: 12));
  }
}

class Ngelx559IdentityHint extends StatelessWidget {
  final Map<String, dynamic> data;
  const Ngelx559IdentityHint({super.key, required this.data});
  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 14),
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: const Color(0xFFF5F0FF),
      borderRadius: BorderRadius.circular(16),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'İsim değişikliği',
          style: TextStyle(fontWeight: FontWeight.w800),
        ),
        const SizedBox(height: 6),
        const Text(
          'Ad soyad ve kullanıcı adı ayrı ayrı, üç ayda bir değiştirilebilir. Kaydetmeden önce yeni tarih gösterilir.',
        ),
        for (final field in ['displayName', 'username'])
          if (ngelx559EligibleDate(data[field + 'ChangedAt559'])
              case final DateTime next)
            Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Text(
                '${field == 'username' ? 'Kullanıcı adı' : 'Ad soyad'}: ${DateTime.now().toUtc().isBefore(next) ? 'sonraki değişiklik ' + ngelx559DateLabel(next) : 'değiştirilebilir'}',
              ),
            ),
      ],
    ),
  );
}

class Ngelx559VerificationPage extends StatefulWidget {
  final User user;
  final Future<void> Function() onCheck, onSignOut;
  const Ngelx559VerificationPage({
    super.key,
    required this.user,
    required this.onCheck,
    required this.onSignOut,
  });
  @override
  State<Ngelx559VerificationPage> createState() =>
      _Ngelx559VerificationPageState();
}

class _Ngelx559VerificationPageState extends State<Ngelx559VerificationPage> {
  Timer? ticker;
  int seconds = 0;
  bool sending = false, checking = false;
  String? status;
  String get key559 => 'verification559_${widget.user.uid}';
  @override
  void initState() {
    super.initState();
    unawaited(restore());
  }

  Future<void> restore() async {
    final prefs = await SharedPreferences.getInstance();
    final at = prefs.getInt(key559) ?? 0;
    final left = ((at + 60000 - DateTime.now().millisecondsSinceEpoch) / 1000)
        .ceil()
        .clamp(0, 60);
    if (!mounted) return;
    setState(() => seconds = left);
    startTicker();
  }

  void startTicker() {
    ticker?.cancel();
    if (seconds <= 0) return;
    ticker = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!mounted) return;
      if (seconds <= 1) ticker?.cancel();
      setState(() => seconds = math.max(0, seconds - 1));
    });
  }

  @override
  void dispose() {
    ticker?.cancel();
    super.dispose();
  }

  Future<void> send() async {
    if (sending || seconds > 0) return;
    setState(() {
      sending = true;
      status = null;
    });
    try {
      await ngelx559SendVerification(widget.user);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setInt(key559, DateTime.now().millisecondsSinceEpoch);
      if (mounted) {
        setState(() {
          seconds = 60;
          status = 'Doğrulama e-postası gönderildi. Gelen kutunu ve spam klasörünü kontrol et.';
        });
        startTicker();
      }
    } on FirebaseAuthException catch (e) {
      if (mounted)
        setState(
          () => status = e.code == 'too-many-requests'
              ? 'Çok sık denedin. Biraz bekleyip tekrar dene.'
              : 'E-posta gönderilemedi. Adresini ve bağlantını kontrol et.',
        );
    } on StateError catch (e) {
      if (mounted) setState(() => status = e.message.toString());
    } catch (_) {
      if (mounted)
        setState(
          () => status =
              'E-posta gönderilemedi. İnternetini kontrol edip tekrar dene.',
        );
    } finally {
      if (mounted) setState(() => sending = false);
    }
  }

  Future<void> check() async {
    if (checking) return;
    setState(() => checking = true);
    try {
      await widget.onCheck();
    } finally {
      if (mounted) setState(() => checking = false);
    }
  }

  Future<void> correctEmail() async {
    final email = TextEditingController(text: widget.user.email),
        password = TextEditingController();
    final confirmed =
        await showDialog<bool>(
          context: context,
          builder: (c) => AlertDialog(
            title: const Text('E-posta adresini düzelt'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Güvenliğin için mevcut şifreni gir. Yeni adresine doğrulama bağlantısı göndereceğiz.',
                  ),
                  TextField(
                    controller: email,
                    keyboardType: TextInputType.emailAddress,
                    decoration: const InputDecoration(
                      labelText: 'Yeni e-posta',
                    ),
                  ),
                  TextField(
                    controller: password,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Mevcut şifre',
                    ),
                  ),
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(c, false),
                child: const Text('Vazgeç'),
              ),
              FilledButton(
                onPressed: () => Navigator.pop(c, true),
                child: const Text('Doğrulama gönder'),
              ),
            ],
          ),
        ) ??
        false;
    final address = email.text.trim(), secret = password.text;
    email.dispose();
    password.dispose();
    if (!confirmed || !mounted) return;
    if (!RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(address)) {
      setState(() => status = 'Geçerli bir e-posta adresi gir.');
      return;
    }
    setState(() => sending = true);
    try {
      await widget.user.reauthenticateWithCredential(
        EmailAuthProvider.credential(
          email: widget.user.email!,
          password: secret,
        ),
      );
      await FirebaseAuth.instance.setLanguageCode('tr');
      await widget.user
          .verifyBeforeUpdateEmail(address)
          .timeout(const Duration(seconds: 15));
      if (mounted)
        setState(
          () => status = 'Yeni adresine bağlantı gönderildi. Adresin, bu bağlantıyı doğrulayınca değişecek. Sonra “Doğruladım” düğmesine dokun.',
        );
    } catch (_) {
      if (mounted)
        setState(
          () => status =
              'Adres değiştirilemedi. Şifreni ve yeni adresini kontrol et.',
        );
    } finally {
      if (mounted) setState(() => sending = false);
    }
  }

  @override
  Widget build(BuildContext context) => Theme(
    data: ThemeData.light(),
    child: Scaffold(
      backgroundColor: const Color(0xFFFAF8FF),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 440),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(
                    Icons.mark_email_read_rounded,
                    color: mor,
                    size: 70,
                  ),
                  const SizedBox(height: 18),
                  const Text(
                    'NgelX',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.w900,
                      color: mor,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'E-postanı doğrula',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 25, fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    widget.user.email ?? '',
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 14),
                  const Text(
                    'E-postandaki “E-postamı doğrula” düğmesine dokun. Ardından buraya dönüp doğrulamayı kontrol et.',
                    textAlign: TextAlign.center,
                  ),
                  if (status != null)
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      child: Semantics(
                        liveRegion: true,
                        child: Text(
                          status!,
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontWeight: FontWeight.w600),
                        ),
                      ),
                    ),
                  const SizedBox(height: 22),
                  FilledButton.icon(
                    onPressed: checking || sending ? null : check,
                    icon: Icon(
                      checking ? Icons.hourglass_top : Icons.verified_outlined,
                    ),
                    label: Text(
                      checking ? 'Kontrol ediliyor…' : 'Doğruladım, kontrol et',
                    ),
                  ),
                  const SizedBox(height: 10),
                  OutlinedButton.icon(
                    onPressed: sending || seconds > 0 ? null : send,
                    icon: const Icon(Icons.forward_to_inbox_outlined),
                    label: Text(
                      sending
                          ? 'Gönderiliyor…'
                          : seconds > 0
                          ? 'Yeniden gönder ($seconds sn)'
                          : 'Bağlantıyı yeniden gönder',
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Bağlantı geçersizse veya süresi dolduysa yeni bir bağlantı iste. En son gelen e-postayı kullan.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.black54),
                  ),
                  TextButton(
                    onPressed: sending || checking ? null : correctEmail,
                    child: const Text('E-posta adresim yanlış'),
                  ),
                  TextButton(
                    onPressed: sending || checking ? null : widget.onSignOut,
                    child: const Text('Başka hesapla giriş yap'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
