part of 'main.dart';

String ngelx558CallDuration(DateTime? start, DateTime now) {
  if (start == null) return 'Aranıyor…';
  final seconds = now.difference(start).inSeconds.clamp(0, 359999);
  return '${(seconds ~/ 60).toString().padLeft(2, '0')}:${(seconds % 60).toString().padLeft(2, '0')}';
}

/// A local repaint only. Call state and the connection start survive navigation.
class Ngelx558CallClock extends StatefulWidget {
  final String roomName;
  const Ngelx558CallClock({super.key, required this.roomName});
  @override
  State<Ngelx558CallClock> createState() => _Ngelx558CallClockState();
}

class _Ngelx558CallClockState extends State<Ngelx558CallClock> {
  Timer? _timer;
  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() {});
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final start = _ngelxArkaPlanAramaBaslangiclari[widget.roomName];
    final time = ngelx558CallDuration(start, DateTime.now());
    return Semantics(
      label: 'Arama süresi $time',
      liveRegion: false,
      child: Text(
        time,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 14,
          fontWeight: FontWeight.w800,
          fontFeatures: [ui.FontFeature.tabularFigures()],
        ),
      ),
    );
  }
}

Future<String?> ngelx558MessageMenu(
  BuildContext context, {
  required bool hasText,
}) => showModalBottomSheet<String>(
  context: context,
  backgroundColor: Colors.white,
  showDragHandle: true,
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
  ),
  builder: (c) => SafeArea(
    child: Padding(
      padding: const EdgeInsets.fromLTRB(12, 0, 12, 18),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            margin: const EdgeInsets.fromLTRB(6, 2, 6, 16),
            padding: const EdgeInsets.symmetric(vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(28),
              boxShadow: const [
                BoxShadow(
                  color: Color(0x22000000),
                  blurRadius: 18,
                  offset: Offset(0, 5),
                ),
              ],
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                for (final emoji in const ['❤️', '😂', '😮', '😢', '😡', '👍'])
                  Flexible(
                    child: InkWell(
                      onTap: () => Navigator.pop(c, 'reaction:$emoji'),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(
                          vertical: 6,
                          horizontal: 2,
                        ),
                        child: Text(
                          emoji,
                          style: const TextStyle(fontSize: 25),
                        ),
                      ),
                    ),
                  ),
                InkWell(
                  onTap: () => Navigator.pop(c, 'reactionMore'),
                  child: const CircleAvatar(
                    radius: 17,
                    backgroundColor: Color(0xFFF1F2F4),
                    child: Icon(Icons.add, color: Colors.black87),
                  ),
                ),
              ],
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              for (final action in <(IconData, String, String, bool)>[
                (Icons.reply_rounded, 'Yanıtla', 'reply', true),
                (Icons.copy_rounded, 'Kopyala', 'copy', hasText),
                (Icons.schedule_rounded, 'Hatırlatma ayarla', 'remind', true),
                (Icons.more_horiz_rounded, 'Daha fazla', 'more', true),
              ])
                Expanded(
                  child: InkWell(
                    onTap: action.$4 ? () => Navigator.pop(c, action.$3) : null,
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: Column(
                        children: [
                          Icon(
                            action.$1,
                            color: action.$4
                                ? const Color(0xFF454A52)
                                : Colors.black26,
                            size: 29,
                          ),
                          const SizedBox(height: 6),
                          Text(
                            action.$2,
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: action.$4
                                  ? Colors.black87
                                  : Colors.black26,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ],
      ),
    ),
  ),
);

Future<List<XFile>> ngelx558PickChatMedia() async {
  List<XFile> selected;
  if (Platform.isAndroid) {
    try {
      selected = await _ngelxAndroidBelgelerSec(const ['image/*', 'video/*']);
    } on MissingPluginException {
      selected = await ImagePicker().pickMultipleMedia();
    } on PlatformException {
      return [];
    }
  } else {
    selected = await ImagePicker().pickMultipleMedia();
  }
  // Copy before leaving picker lifecycle; existing normalization protects photo decoders.
  if (selected.length > 100)
    throw StateError('Bir albümde en fazla 100 medya seçebilirsin.');
  final result = <XFile>[];
  for (final file in selected) {
    result.add(
      ngelxSohbetVideoMu(file)
          ? await _ngelxKaliciYerelKopya(
              file,
              uzanti: _ngelxYerelUzanti(file, varsayilan: 'mp4'),
              mimeType: file.mimeType ?? 'video/mp4',
            )
          : await _ngelxGaleridenResmiNormalizeEt(file),
    );
  }
  return result;
}

Future<List<Map<String, String>>> ngelx558UploadAlbum(
  List<XFile> files,
  String chatId, {
  required void Function(int, int) progress,
}) async {
  final result = <Map<String, String>>[];
  final batch = DateTime.now().microsecondsSinceEpoch;
  for (final file in files) {
    if (ngelxSohbetVideoMu(file) && await file.length() > 80 * 1024 * 1024)
      throw StateError('Video 80 MB’den küçük olmalı.');
  }
  for (var i = 0; i < files.length; i++) {
    final file = files[i];
    final video = ngelxSohbetVideoMu(file);
    progress(i + 1, files.length);
    final ext = _ngelxYerelUzanti(file, varsayilan: video ? 'mp4' : 'jpg');
    final path = 'chats/$chatId/${batch}_$i.$ext';
    final url = video
        ? await ngelxMedyaYukleDosya(
            dosya: file,
            kind: 'videos',
            ext: ext,
            legacyPath: path,
            contentType: ext == 'mov' ? 'video/quicktime' : 'video/mp4',
          ).timeout(const Duration(minutes: 3))
        : await ngelxFotografYukle(
            dosya: file,
            kind: 'chats',
            ext: ext,
            legacyPath: path,
          ).timeout(const Duration(minutes: 2));
    result.add({'url': url, 'type': video ? 'video' : 'photo'});
  }
  return result;
}

List<Map<String, String>> ngelx558AlbumItems(Map<String, dynamic> data) {
  final raw = data['albumItems558'];
  if (raw is! List) return [];
  return raw
      .whereType<Map>()
      .map(
        (item) => {
          'url': (item['url'] ?? '').toString(),
          'type': item['type'] == 'video' ? 'video' : 'photo',
        },
      )
      .where((item) {
        final uri = Uri.tryParse(item['url']!);
        return uri != null && uri.scheme == 'https' && uri.host.isNotEmpty;
      })
      .toList();
}

Future<void> ngelx558Download(
  BuildContext context,
  List<Map<String, String>> items,
) async {
  if (items.isEmpty) return;
  var completed = 0;
  try {
    if (!await Gal.hasAccess()) {
      await Gal.requestAccess();
      if (!await Gal.hasAccess()) throw StateError('Galeri izni gerekli.');
    }
    final folder = await getTemporaryDirectory();
    for (var i = 0; i < items.length; i++) {
      if (!context.mounted) return;
      final item = items[i], video = item['type'] == 'video';
      final file = File(
        '${folder.path}/ngelx_${DateTime.now().microsecondsSinceEpoch}_$i.${video ? 'mp4' : 'jpg'}',
      );
      try {
        await Dio().download(
          item['url']!,
          file.path,
          options: Options(receiveTimeout: const Duration(minutes: 3)),
        );
        if (!context.mounted) return;
        if (video) {
          await Gal.putVideo(file.path);
        } else {
          await Gal.putImage(file.path);
        }
        completed++;
      } finally {
        if (await file.exists()) await file.delete();
      }
    }
    if (context.mounted)
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('$completed medya galeriye kaydedildi.')),
      );
  } catch (_) {
    if (context.mounted)
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '$completed/${items.length} kaydedildi. Galeri iznini ve bağlantını kontrol et.',
          ),
        ),
      );
  }
}

String ngelx558AlbumLabel(List<Map<String, String>> items) =>
    '${items.length} ${items.every((x) => x['type'] == 'photo') ? 'fotoğraf' : 'medya'}';

class Ngelx558AlbumPreview extends StatelessWidget {
  final List<Map<String, String>> items;
  const Ngelx558AlbumPreview({super.key, required this.items});
  @override
  Widget build(BuildContext context) => SizedBox(
    width: 230,
    height: 252,
    child: Stack(
      children: [
        for (var layer = math.min(2, items.length - 1); layer >= 0; layer--)
          Positioned(
            left: layer * 7.0,
            top: layer * 7.0,
            right: 14 - layer * 7.0,
            bottom: 22 - layer * 7.0,
            child: Transform.rotate(
              angle: layer * .035,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(18),
                child: items[layer]['type'] == 'video'
                    ? Container(
                        color: const Color(0xFF292435),
                        child: const Icon(
                          Icons.play_circle_outline,
                          color: Colors.white,
                          size: 60,
                        ),
                      )
                    : NgelXAgResmi(
                        url: items[layer]['url']!,
                        fit: BoxFit.cover,
                      ),
              ),
            ),
          ),
        Positioned(
          right: 20,
          bottom: 28,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: const Color(0xAA000000),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              ngelx558AlbumLabel(items),
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ),
      ],
    ),
  );
}

class Ngelx558AlbumPage extends StatefulWidget {
  final List<Map<String, String>> items;
  final DocumentReference<Map<String, dynamic>> message;
  const Ngelx558AlbumPage({
    super.key,
    required this.items,
    required this.message,
  });
  @override
  State<Ngelx558AlbumPage> createState() => _Ngelx558AlbumPageState();
}

class _Ngelx558AlbumPageState extends State<Ngelx558AlbumPage> {
  bool saving = false;
  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: Colors.white,
    appBar: AppBar(
      title: Text(ngelx558AlbumLabel(widget.items)),
      backgroundColor: Colors.white,
      actions: [
        IconButton(
          tooltip: 'Tümünü indir',
          onPressed: saving
              ? null
              : () async {
                  setState(() => saving = true);
                  try {
                    await ngelx558Download(context, widget.items);
                  } finally {
                    if (mounted) setState(() => saving = false);
                  }
                },
          icon: saving
              ? const SizedBox(
                  width: 22,
                  height: 22,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.download_rounded),
        ),
      ],
    ),
    body: GridView.builder(
      padding: const EdgeInsets.all(16),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: .75,
      ),
      itemCount: widget.items.length,
      itemBuilder: (_, i) {
        final item = widget.items[i];
        return InkWell(
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => Ngelx435MedyaKaynagi(
                ref: widget.message,
                child: item['type'] == 'video'
                    ? TamEkranVideoPage(url: item['url']!)
                    : TamEkranMedyaPage(url: item['url']!),
              ),
            ),
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(18),
            child: item['type'] == 'video'
                ? Container(
                    color: const Color(0xFF292435),
                    child: const Icon(
                      Icons.play_circle_outline,
                      color: Colors.white,
                      size: 48,
                    ),
                  )
                : NgelXAgResmi(url: item['url']!, fit: BoxFit.cover),
          ),
        );
      },
    ),
  );
}

class Ngelx558DownloadButton extends StatefulWidget {
  final List<Map<String, String>> items;
  const Ngelx558DownloadButton({super.key, required this.items});
  @override
  State<Ngelx558DownloadButton> createState() => _Ngelx558DownloadButtonState();
}

class _Ngelx558DownloadButtonState extends State<Ngelx558DownloadButton> {
  bool saving = false;
  @override
  Widget build(BuildContext context) => IconButton(
    tooltip: 'İndir',
    onPressed: saving
        ? null
        : () async {
            setState(() => saving = true);
            try {
              await ngelx558Download(context, widget.items);
            } finally {
              if (mounted) setState(() => saving = false);
            }
          },
    icon: saving
        ? const SizedBox(
            width: 22,
            height: 22,
            child: CircularProgressIndicator(strokeWidth: 2),
          )
        : const Icon(Icons.download_rounded),
  );
}

/// Identity is UID-based: display-name changes never grant verification.
/// Provision the four account IDs in the release build; never infer them from names.
const ngelx558FounderUid = String.fromEnvironment('NGELX_FOUNDER_UID');
const ngelx558VerifiedUids = String.fromEnvironment('NGELX_VERIFIED_UIDS');
bool ngelx558Verified(
  String uid, {
  String founderUid = ngelx558FounderUid,
  String verifiedUids = ngelx558VerifiedUids,
}) {
  if (uid.isEmpty) return false;
  if (founderUid.isNotEmpty && uid == founderUid) return true;
  final ids = verifiedUids
      .split(',')
      .map((x) => x.trim())
      .where((x) => x.isNotEmpty && x != founderUid)
      .toSet();
  // Reject an accidental broad grant instead of awarding extra badges.
  return ids.length == 3 && ids.contains(uid);
}

class Ngelx558VerifiedBadge extends StatelessWidget {
  final String uid;
  final double size;
  const Ngelx558VerifiedBadge({super.key, required this.uid, this.size = 22});
  @override
  Widget build(BuildContext context) {
    if (!ngelx558Verified(uid)) return const SizedBox.shrink();
    final founder = uid == ngelx558FounderUid;
    return Semantics(
      label: 'Doğrulanmış hesap',
      child: Padding(
        padding: const EdgeInsets.only(left: 5),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (founder)
              Container(
                width: size,
                height: size,
                decoration: const BoxDecoration(
                  color: Color(0xFF1687FF),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.check_rounded,
                  color: Colors.white,
                  size: size * .75,
                ),
              )
            else
              Icon(
                Icons.verified_rounded,
                color: const Color(0xFF1687FF),
                size: size,
              ),
          ],
        ),
      ),
    );
  }
}

Future<void> ngelx558Remind(
  BuildContext context,
  String chatId,
  String messageId,
  String text,
) async {
  final uid = FirebaseAuth.instance.currentUser?.uid;
  if (uid == null) return;
  final delay = await showModalBottomSheet<Duration>(
    context: context,
    backgroundColor: Colors.white,
    showDragHandle: true,
    builder: (c) => SafeArea(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const ListTile(title: Text('Hatırlatma ayarla')),
          for (final option in const [
            ('1 saat', Duration(hours: 1)),
            ('4 saat', Duration(hours: 4)),
            ('Yarın', Duration(days: 1)),
            ('1 hafta', Duration(days: 7)),
          ])
            ListTile(
              title: Text(option.$1),
              onTap: () => Navigator.pop(c, option.$2),
            ),
        ],
      ),
    ),
  );
  if (delay == null ||
      !context.mounted ||
      FirebaseAuth.instance.currentUser?.uid != uid)
    return;
  try {
    await FirebaseFirestore.instance
        .collection('users')
        .doc(uid)
        .collection('messageReminders')
        .add({
          'chatId': chatId,
          'messageId': messageId,
          'text': text,
          'remindAt': Timestamp.fromDate(DateTime.now().add(delay)),
          'createdAt': FieldValue.serverTimestamp(),
        })
        .timeout(const Duration(seconds: 10));
    if (context.mounted)
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Hatırlatma kaydedildi.')));
  } catch (_) {
    if (context.mounted)
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Hatırlatma kaydedilemedi.')),
      );
  }
}
