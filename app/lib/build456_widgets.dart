part of 'main.dart';

const ngelx456Ink = Color(0xFF202039),
    ngelx456Soft = Color(0xFFF6F3FC),
    ngelx456Border = Color(0xFFE7DFF4);
String ngelx456Time(Object? value, {DateTime? now}) {
  if (value is! Timestamp) return 'Az önce';
  final date = value.toDate(),
      current = now ?? DateTime.now(),
      gap = current.difference(date);
  if (gap.inMinutes < 1) return 'Az önce';
  if (gap.inHours < 1) return '${gap.inMinutes} dk önce';
  if (gap.inDays < 1) return '${gap.inHours} sa önce';
  if (gap.inDays == 1) return 'Dün';
  if (gap.inDays < 7) return '${gap.inDays} gün önce';
  return '${date.day.toString().padLeft(2, '0')}.${date.month.toString().padLeft(2, '0')}.${date.year}';
}

String ngelx456Error(Object error) {
  final v = error.toString().toLowerCase();
  if (v.contains('unknownhost') ||
      v.contains('resolve host') ||
      v.contains('socketexception') ||
      v.contains('connection'))
    return 'Yükleme bağlantısı kurulamadı. Bağlantını kontrol edip yeniden dene.';
  if (v.contains('timeout') || v.contains('zaman aşımı'))
    return 'Bağlantı zaman aşımına uğradı. Yeniden dene.';
  if (v.contains('permission') || v.contains('yetki'))
    return 'Bu işlem için iznin bulunmuyor.';
  if (v.contains('upload') || v.contains('r2') || v.contains('presign'))
    return 'Medya yüklenemedi. Dosyan korunuyor; yeniden deneyebilirsin.';
  return 'İşlem tamamlanamadı. Yeniden dene.';
}

bool ngelx456Moderator(Map<String, dynamic> v) =>
    _communityAdmin450(v) ||
    List<String>.from(v['moderators'] ?? const []).contains(_communityUid450);
String ngelx456Role(Map<String, dynamic> v, String uid) => v['founderId'] == uid
    ? 'Kurucu'
    : List<String>.from(v['admins'] ?? const []).contains(uid)
    ? 'Yönetici'
    : List<String>.from(v['moderators'] ?? const []).contains(uid)
    ? 'Moderatör'
    : 'Üye';
Widget ngelx456Pill(String label, {IconData? icon}) => Container(
  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
  decoration: BoxDecoration(
    color: ngelx456Soft,
    borderRadius: BorderRadius.circular(20),
  ),
  child: Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      if (icon != null) ...[
        Icon(icon, size: 14, color: mor),
        const SizedBox(width: 5),
      ],
      Text(
        label,
        style: const TextStyle(
          color: mor,
          fontSize: 12,
          fontWeight: FontWeight.w700,
        ),
      ),
    ],
  ),
);
Future<bool> ngelx456Confirm(
  BuildContext c,
  String title,
  String message,
) async =>
    await showDialog<bool>(
      context: c,
      builder: (b) => Ngelx455WhiteDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(b, false),
            child: const Text('Vazgeç'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(b, true),
            child: const Text('Onayla'),
          ),
        ],
      ),
    ) ==
    true;

class Ngelx456Cover extends StatelessWidget {
  final String url;
  final double alignment;
  final double height;
  const Ngelx456Cover({
    super.key,
    required this.url,
    this.alignment = 0,
    this.height = 190,
  });
  @override
  Widget build(BuildContext c) => SizedBox(
    height: height,
    width: double.infinity,
    child: url.isEmpty
        ? Container(
            color: ngelx456Soft,
            child: const Icon(Icons.groups_outlined, size: 50, color: mor),
          )
        : ClipRect(
            child: Image(
              image: ResizeImage(NgelXAgImageProvider(url), width: 1200),
              fit: BoxFit.cover,
              alignment: Alignment(0, alignment.clamp(-1.0, 1.0).toDouble()),
              errorBuilder: (_, __, ___) => Container(
                color: ngelx456Soft,
                child: const Icon(Icons.landscape_outlined, color: mor),
              ),
            ),
          ),
  );
}

class Ngelx456CoverEditor extends StatefulWidget {
  final String id;
  final Map<String, dynamic> value;
  const Ngelx456CoverEditor({super.key, required this.id, required this.value});
  @override
  State<Ngelx456CoverEditor> createState() => _Ngelx456CoverEditorState();
}

class _Ngelx456CoverEditorState extends State<Ngelx456CoverEditor> {
  XFile? file;
  bool saving = false;
  late double alignment =
      (widget.value['coverAlignment'] as num?)?.toDouble() ?? 0;
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Kapağı düzenle',
    body: ListView(
      padding: const EdgeInsets.all(18),
      children: [
        const Text(
          'Fotoğrafı yukarı–aşağı sürükleyerek kadrajı ayarla.',
          style: TextStyle(color: Colors.black54),
        ),
        const SizedBox(height: 16),
        GestureDetector(
          onVerticalDragUpdate: saving
              ? null
              : (d) => setState(
                  () => alignment = (alignment - d.delta.dy / 100)
                      .clamp(-1.0, 1.0)
                      .toDouble(),
                ),
          child: file == null
              ? Ngelx456Cover(
                  url: (widget.value['coverUrl'] ?? '').toString(),
                  alignment: alignment,
                )
              : SizedBox(
                  height: 190,
                  child: ClipRect(
                    child: kIsWeb
                        ? Image.network(
                            file!.path,
                            fit: BoxFit.cover,
                            alignment: Alignment(0, alignment),
                          )
                        : Image.file(
                            File(file!.path),
                            fit: BoxFit.cover,
                            alignment: Alignment(0, alignment),
                            cacheWidth: 1200,
                          ),
                  ),
                ),
        ),
        Slider(
          value: alignment,
          min: -1,
          max: 1,
          onChanged: saving ? null : (x) => setState(() => alignment = x),
        ),
        OutlinedButton.icon(
          onPressed: saving
              ? null
              : () async {
                  final x = await ngelxResimSec(
                    source: ImageSource.gallery,
                    imageQuality: 85,
                    maxWidth: 1600,
                  );
                  if (x != null && mounted)
                    setState(() {
                      file = x;
                      alignment = 0;
                    });
                },
          icon: const Icon(Icons.photo_library_outlined),
          label: const Text('Fotoğrafı değiştir'),
        ),
        const SizedBox(height: 14),
        FilledButton(
          onPressed: saving ? null : save,
          child: Text(saving ? 'Kaydediliyor…' : 'Kadrajı kaydet'),
        ),
      ],
    ),
  );
  Future<void> save() async {
    setState(() => saving = true);
    try {
      final ref = _communities450.doc(widget.id),
          current = await ref.get(const GetOptions(source: Source.server));
      if (!_communityAdmin450(current.data() ?? {})) throw StateError('yetki');
      final url = file == null
          ? (current.data()?['coverUrl'] ?? '').toString()
          : await ngelxFotografYukle(
              dosya: file!,
              kind: 'groups',
              legacyPath:
                  'communities/${widget.id}/cover_${DateTime.now().millisecondsSinceEpoch}.jpg',
            );
      await ref.update({'coverUrl': url, 'coverAlignment': alignment});
      if (mounted) {
        // Show feedback while the editor route still owns a mounted context.
        ngelx455Status(context, 'Kapak güncellendi');
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) _communityError450(context, e);
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }
}

class Ngelx456Header extends StatelessWidget {
  final String id;
  final Map<String, dynamic> value;
  final VoidCallback invite, compose, manage;
  const Ngelx456Header({
    super.key,
    required this.id,
    required this.value,
    required this.invite,
    required this.compose,
    required this.manage,
  });
  @override
  Widget build(BuildContext c) {
    final v = value,
        admin = _communityAdmin450(v),
        member = _communityMember450(v);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Stack(
          children: [
            Ngelx456Cover(
              url: (v['coverUrl'] ?? '').toString(),
              alignment: (v['coverAlignment'] as num?)?.toDouble() ?? 0,
            ),
            if (admin)
              Positioned(
                right: 14,
                bottom: 14,
                child: FilledButton.tonalIcon(
                  style: FilledButton.styleFrom(
                    backgroundColor: Colors.black54,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () => Navigator.push(
                    c,
                    MaterialPageRoute(
                      builder: (_) => Ngelx456CoverEditor(id: id, value: v),
                    ),
                  ),
                  icon: const Icon(Icons.edit_outlined, size: 16),
                  label: const Text('Düzenle'),
                ),
              ),
          ],
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _communityImage450(
                    (v['photoUrl'] ?? '').toString(),
                    size: 66,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          (v['name'] ?? '').toString(),
                          style: const TextStyle(
                            color: ngelx456Ink,
                            fontSize: 22,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                        const SizedBox(height: 5),
                        Wrap(
                          spacing: 8,
                          runSpacing: 4,
                          children: [
                            ngelx456Pill(
                              v['visibility'] == 'private'
                                  ? 'Özel topluluk'
                                  : 'Herkese açık',
                              icon: v['visibility'] == 'private'
                                  ? Icons.lock_outline
                                  : Icons.public,
                            ),
                            InkWell(
                              onTap: () => Navigator.push(
                                c,
                                MaterialPageRoute(
                                  builder: (_) => Ngelx456Members(id: id),
                                ),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.all(6),
                                child: Text(
                                  '${(v['members'] as List? ?? const []).length} üye',
                                  style: const TextStyle(
                                    fontSize: 13,
                                    color: Colors.black54,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              NgelXFounder450(uid: (v['founderId'] ?? '').toString()),
              const SizedBox(height: 5),
              Text(
                (v['description'] ?? '').toString(),
                style: const TextStyle(
                  fontSize: 14,
                  height: 1.4,
                  color: Color(0xFF57576F),
                ),
              ),
              const SizedBox(height: 12),
              if (member)
                Row(
                  children: [
                    if (ngelx456Moderator(v))
                      Expanded(
                        child: FilledButton.icon(
                          onPressed: manage,
                          icon: const Icon(Icons.shield_outlined, size: 19),
                          label: const Text('Yönet'),
                        ),
                      ),
                    if (ngelx456Moderator(v)) const SizedBox(width: 10),
                    if (admin)
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: invite,
                          icon: const Icon(Icons.person_add_outlined, size: 19),
                          label: const Text('Davet et'),
                        ),
                      ),
                  ],
                ),
              if (member)
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton.icon(
                    onPressed: v['founderId'] == _communityUid450
                        ? null
                        : () async {
                            if (await ngelx456Confirm(
                              c,
                              'Topluluktan ayrıl?',
                              'Üyeliğin ve topluluk yetkilerin kaldırılır.',
                            )) {
                              try {
                                await _communities450.doc(id).update({
                                  'members': FieldValue.arrayRemove([
                                    _communityUid450,
                                  ]),
                                  'admins': FieldValue.arrayRemove([
                                    _communityUid450,
                                  ]),
                                  'moderators': FieldValue.arrayRemove([
                                    _communityUid450,
                                  ]),
                                });
                              } catch (e) {
                                if (c.mounted) _communityError450(c, e);
                              }
                            }
                          },
                    icon: const Icon(Icons.check_circle_outline, size: 16),
                    label: const Text('Katıldın'),
                  ),
                ),
              if (!member) NgelXCommunityJoin450(id: id, value: v),
              if ((v['rules'] ?? '').toString().isNotEmpty)
                Container(
                  decoration: BoxDecoration(
                    color: ngelx456Soft,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: ExpansionTile(
                    leading: const Icon(
                      Icons.verified_user_outlined,
                      color: mor,
                      size: 20,
                    ),
                    title: const Text(
                      'Topluluk kuralları',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.fromLTRB(16, 0, 16, 14),
                        child: Text(v['rules'].toString()),
                      ),
                    ],
                  ),
                ),
              if (v['paused'] == true)
                const Padding(
                  padding: EdgeInsets.all(12),
                  child: Text(
                    'Topluluk geçici olarak durduruldu.',
                    style: TextStyle(color: mor),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}

class Ngelx456Empty extends StatelessWidget {
  final VoidCallback? onCreate;
  const Ngelx456Empty({super.key, this.onCreate});
  @override
  Widget build(BuildContext c) => Container(
    margin: const EdgeInsets.all(16),
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      color: ngelx456Soft,
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: ngelx456Border),
    ),
    child: Column(
      children: [
        const Icon(Icons.forum_outlined, size: 44, color: mor),
        const SizedBox(height: 12),
        const Text(
          'İlk paylaşım senden olsun',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w800,
            color: ngelx456Ink,
          ),
        ),
        const SizedBox(height: 6),
        const Text(
          'Fotoğraf, video veya bir düşünce paylaş.',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.black54, fontSize: 13),
        ),
        if (onCreate != null) ...[
          const SizedBox(height: 16),
          FilledButton.icon(
            onPressed: onCreate,
            icon: const Icon(Icons.edit_outlined, size: 18),
            label: const Text('İlk gönderiyi paylaş'),
          ),
        ],
      ],
    ),
  );
}

class Ngelx456Members extends StatefulWidget {
  final String id;
  const Ngelx456Members({super.key, required this.id});
  @override
  State<Ngelx456Members> createState() => _Ngelx456MembersState();
}

class _Ngelx456MembersState extends State<Ngelx456Members> {
  String search = '', role = 'Tümü';
  late Stream<DocumentSnapshot<Map<String, dynamic>>> stream =
      _communities450.doc(widget.id).snapshots();
  final profiles = <String, Future<DocumentSnapshot<Map<String, dynamic>>>>{};
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Üyeler ve roller',
    body: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: stream,
      builder: (c, s) {
        if (s.hasError) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Üyeler yüklenemedi. Bağlantını kontrol edip yeniden dene.',
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  OutlinedButton.icon(
                    onPressed: () => setState(() {
                      profiles.clear();
                      stream = _communities450.doc(widget.id).snapshots();
                    }),
                    icon: const Icon(Icons.refresh),
                    label: const Text('Yeniden dene'),
                  ),
                ],
              ),
            ),
          );
        }
        if (!s.hasData)
          return const Center(child: CircularProgressIndicator());
        if (s.data?.exists != true)
          return const Center(child: Text('Topluluk bulunamadı.'));
        final v = s.data!.data();
        if (v == null)
          return const Center(child: Text('Üye bilgileri yüklenemedi.'));
        final ids = List<String>.from(v['members'] ?? const [])
            .where((id) => role == 'Tümü' || ngelx456Role(v, id) == role)
            .toList();
        return Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: TextField(
                onChanged: (x) => setState(() => search = x.toLowerCase()),
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.search),
                  hintText: 'Üyelerde ara',
                ),
              ),
            ),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: ['Tümü', 'Kurucu', 'Yönetici', 'Moderatör', 'Üye']
                    .map(
                      (x) => Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: ChoiceChip(
                          label: Text(x),
                          selected: role == x,
                          onSelected: (_) => setState(() => role = x),
                        ),
                      ),
                    )
                    .toList(),
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: ids.length,
                itemBuilder: (c, i) {
                  final uid = ids[i];
                  return FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
                    future: profiles.putIfAbsent(
                      uid,
                      () => FirebaseFirestore.instance
                          .collection('users')
                          .doc(uid)
                          .get(),
                    ),
                    builder: (c, u) {
                      final p = u.data?.data() ?? {},
                          name = ngelx455ProfileName(
                            p,
                            fallback: 'Üye bilgisi yükleniyor…',
                          );
                      if (search.isNotEmpty &&
                          !name.toLowerCase().contains(search))
                        return const SizedBox.shrink();
                      return ListTile(
                        leading: _communityImage450(
                          (p['photoUrl'] ?? '').toString(),
                          size: 42,
                          circle: true,
                        ),
                        title: Text(
                          name,
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                        subtitle: Text(
                          ngelx456Role(v, uid),
                          style: const TextStyle(color: mor, fontSize: 12),
                        ),
                        onTap: () => Navigator.push(
                          c,
                          MaterialPageRoute(
                            builder: (_) => KullaniciProfilPage(uid: uid),
                          ),
                        ),
                        trailing: _communityAdmin450(v) && uid != v['founderId']
                            ? IconButton(
                                icon: const Icon(Icons.more_vert),
                                onPressed: () => actions(uid, v, name),
                              )
                            : null,
                      );
                    },
                  );
                },
              ),
            ),
          ],
        );
      },
    ),
  );
  Future<void> actions(String uid, Map<String, dynamic> v, String name) async {
    final isFounder = v['founderId'] == _communityUid450,
        isAdmin = List<String>.from(v['admins'] ?? const []).contains(uid);
    final options = <String, String>{
      if (isFounder) 'admin': isAdmin ? 'Yöneticiliği kaldır' : 'Yönetici yap',
      if (!isAdmin)
        'moderator':
            List<String>.from(v['moderators'] ?? const []).contains(uid)
            ? 'Moderatörlüğü kaldır'
            : 'Moderatör yap',
      if (!isAdmin || isFounder)
        'mute': List<String>.from(v['muted'] ?? const []).contains(uid)
            ? 'Susturmayı kaldır'
            : 'Sustur',
      if (!isAdmin || isFounder) 'remove': 'Topluluktan çıkar',
      if (!isAdmin || isFounder) 'ban': 'Topluluktan engelle',
    };
    final action = await showModalBottomSheet<String>(
      context: context,
      backgroundColor: Colors.white,
      showDragHandle: true,
      builder: (c) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: Text(
                name,
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
            ),
            ...options.entries.map(
              (e) => ListTile(
                title: Text(e.value),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => Navigator.pop(c, e.key),
              ),
            ),
          ],
        ),
      ),
    );
    if (action == null ||
        !mounted ||
        !await ngelx456Confirm(context, options[action]!, name))
      return;
    try {
      final root = _communities450.doc(widget.id);
      await FirebaseFirestore.instance.runTransaction((tx) async {
        final d = await tx.get(root), current = d.data() ?? {};
        if (!_communityAdmin450(current) || current['founderId'] == uid)
          throw StateError('yetki');
        final patch = <String, dynamic>{};
        if (action == 'admin') {
          if (current['founderId'] != _communityUid450)
            throw StateError('yetki');
          patch['admins'] =
              List<String>.from(current['admins'] ?? const []).contains(uid)
              ? FieldValue.arrayRemove([uid])
              : FieldValue.arrayUnion([uid]);
          patch['moderators'] = FieldValue.arrayRemove([uid]);
        }
        if (action == 'moderator')
          patch['moderators'] =
              List<String>.from(current['moderators'] ?? const []).contains(uid)
              ? FieldValue.arrayRemove([uid])
              : FieldValue.arrayUnion([uid]);
        if (action == 'mute')
          patch['muted'] =
              List<String>.from(current['muted'] ?? const []).contains(uid)
              ? FieldValue.arrayRemove([uid])
              : FieldValue.arrayUnion([uid]);
        if (action == 'remove' || action == 'ban') {
          patch.addAll({
            'members': FieldValue.arrayRemove([uid]),
            'admins': FieldValue.arrayRemove([uid]),
            'moderators': FieldValue.arrayRemove([uid]),
            'muted': FieldValue.arrayRemove([uid]),
          });
          if (action == 'ban') patch['banned'] = FieldValue.arrayUnion([uid]);
        }
        tx.update(root, patch);
        tx.set(root.collection('audit456').doc(), {
          'actor': _communityUid450,
          'target': uid,
          'action': action,
          'createdAt': FieldValue.serverTimestamp(),
        });
      });
      if (mounted) ngelx455Status(context, 'Üye yetkileri güncellendi');
    } catch (e) {
      if (mounted) _communityError450(context, e);
    }
  }
}

Future<void> ngelx456Invite(
  BuildContext context,
  String id,
  Map<String, dynamic> value,
) async {
  final me = FirebaseAuth.instance.currentUser;
  if (me == null || me.isAnonymous) return;
  try {
    final targets = await showModalBottomSheet<List<(String, String)>>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      showDragHandle: true,
      builder: (c) => const Ngelx456ChatPicker(),
    );
    if (targets == null || targets.isEmpty) return;
    final ref = FirebaseFirestore.instance
        .collection('communityInvites450')
        .doc();
    await ref.set({
      'communityId': id,
      'name': value['name'],
      'joinApproval': value['joinApproval'],
      'createdBy': me.uid,
      'expiresAt': Timestamp.fromDate(
        DateTime.now().add(const Duration(days: 6, hours: 23)),
      ),
    });
    var sent = 0;
    for (final target in targets) {
      try {
        await ngelx456SendInvite(
          me,
          target.$1,
          ref.id,
          value['name'].toString(),
          chatId: target.$2,
        );
        sent++;
      } catch (e) {
        if (context.mounted) _communityError450(context, e);
      }
    }
    if (context.mounted && sent > 0)
      ngelx455Status(context, '$sent özel sohbete davet gönderildi');
  } catch (e) {
    if (context.mounted) _communityError450(context, e);
  }
}

class Ngelx456ChatPicker extends StatefulWidget {
  const Ngelx456ChatPicker({super.key});
  @override
  State<Ngelx456ChatPicker> createState() => _Ngelx456ChatPickerState();
}

class _Ngelx456ChatPickerState extends State<Ngelx456ChatPicker> {
  late final stream = FirebaseFirestore.instance
      .collection('chats')
      .where('members', arrayContains: _communityUid450)
      .limit(100)
      .snapshots();
  final profiles = <String, Future<DocumentSnapshot<Map<String, dynamic>>>>{},
      selected = <String>{};
  String search = '';
  final chatIds = <String, String>{};
  @override
  Widget build(BuildContext c) => SafeArea(
    child: SizedBox(
      height: MediaQuery.sizeOf(c).height * .75,
      child: Column(
        children: [
          const ListTile(
            title: Text(
              'NgelX özel sohbetlerine davet et',
              style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: TextField(
              onChanged: (x) => setState(() => search = x.toLowerCase()),
              decoration: const InputDecoration(
                hintText: 'Sohbetlerde ara',
                prefixIcon: Icon(Icons.search),
              ),
            ),
          ),
          Expanded(
            child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: stream,
              builder: (c, s) {
                if (s.hasError)
                  return const Center(child: Text('Sohbetler yüklenemedi.'));
                if (!s.hasData)
                  return const Center(child: CircularProgressIndicator());
                final ids = <String>{};
                chatIds.clear();
                for (final doc in s.data!.docs) {
                  final v = doc.data(),
                      members = List<String>.from(v['members'] ?? const []);
                  if (v['isGroup'] != true && members.length == 2) {
                    for (final uid in members.where(
                      (x) => x != _communityUid450,
                    )) {
                      ids.add(uid);
                      chatIds.putIfAbsent(uid, () => doc.id);
                    }
                  }
                }
                final list = ids.toList();
                if (list.isEmpty)
                  return const Center(
                    child: Text('Davet gönderebileceğin özel sohbet yok.'),
                  );
                return ListView.builder(
                  itemCount: list.length,
                  itemBuilder: (c, i) {
                    final uid = list[i];
                    return FutureBuilder<
                      DocumentSnapshot<Map<String, dynamic>>
                    >(
                      future: profiles.putIfAbsent(
                        uid,
                        () => FirebaseFirestore.instance
                            .collection('users')
                            .doc(uid)
                            .get(),
                      ),
                      builder: (c, u) {
                        final p = u.data?.data() ?? {},
                            name = ngelx455ProfileName(p);
                        if (search.isNotEmpty &&
                            !name.toLowerCase().contains(search))
                          return const SizedBox.shrink();
                        return CheckboxListTile(
                          value: selected.contains(uid),
                          onChanged: u.hasData
                              ? (_) => setState(
                                  () => selected.contains(uid)
                                      ? selected.remove(uid)
                                      : selected.add(uid),
                                )
                              : null,
                          secondary: _communityImage450(
                            (p['photoUrl'] ?? '').toString(),
                            size: 40,
                            circle: true,
                          ),
                          title: Text(name),
                          subtitle: const Text(
                            'Özel sohbet',
                            style: TextStyle(fontSize: 12),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: selected.isEmpty
                    ? null
                    : () => Navigator.pop(c, <(String, String)>[
                        for (final uid in selected)
                          if (chatIds.containsKey(uid)) (uid, chatIds[uid]!),
                      ]),
                icon: const Icon(Icons.send_outlined),
                label: Text('${selected.length} sohbete gönder'),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

Future<void> ngelx456SendInvite(
  User me,
  String target,
  String code,
  String name, {
  required String chatId,
}) async {
  final chat = FirebaseFirestore.instance.collection('chats').doc(chatId);
  final docs = await Future.wait([
    FirebaseFirestore.instance.collection('users').doc(me.uid).get(),
    FirebaseFirestore.instance.collection('users').doc(target).get(),
    chat.get(),
  ]);
  if (FirebaseAuth.instance.currentUser?.uid != me.uid)
    throw StateError('yetki');
  final own = docs[0].data() ?? {},
      peer = docs[1].data() ?? {},
      v = docs[2].data() ?? {};
  if (peer['deactivated'] == true ||
      List<String>.from(own['blocked'] ?? const []).contains(target) ||
      List<String>.from(peer['blocked'] ?? const []).contains(me.uid))
    throw StateError('message-permission');
  final members = List<String>.from(v['members'] ?? const []);
  if (!docs[2].exists ||
      members.length != 2 ||
      !members.contains(me.uid) ||
      !members.contains(target))
    throw StateError('yetki');
  final accepted =
      v['requestAccepted_${me.uid}'] == true ||
      v['requestAccepted_$target'] == true;
  final permission =
      (peer['messagePermission'] ??
              (peer['friendsOnlyMessages'] == true ? 'friends' : 'all'))
          .toString();
  final friend = List<String>.from(peer['friends'] ?? const [])
      .contains(me.uid);
  if (!accepted &&
      (permission == 'none' ||
          permission == 'friends' && !friend ||
          permission == 'following' &&
              !List<String>.from(peer['following'] ?? const [])
                  .contains(me.uid)))
    throw StateError('message-permission');
  final batch = FirebaseFirestore.instance.batch(),
      message = chat.collection('messages').doc();
  final text = '$name topluluğuna davetlisin.\nngelx://community/$code';
  final duration = (v['disappearingSeconds'] as num?)?.toInt() ?? 0;
  batch.set(message, {
    'senderId': me.uid,
    'type': 'text',
    'text': text,
    'createdAt': FieldValue.serverTimestamp(),
    'clientCreatedAt': Timestamp.now(),
    if (duration > 0)
      'expiresAt': Timestamp.fromDate(
        DateTime.now().add(Duration(seconds: duration)),
      ),
  });
  batch.set(chat, {
    'lastMessage': 'Topluluk daveti · $name',
    'lastSenderId': me.uid,
    'lastMessageClientAt': Timestamp.now(),
    'updatedAt': FieldValue.serverTimestamp(),
    'unread_$target': FieldValue.increment(1),
    if (!friend &&
        !accepted &&
        (v['requestSenderUid'] ?? '').toString().isEmpty)
      'requestSenderUid': me.uid,
    if (!friend &&
        !accepted &&
        (v['requestRecipientUid'] ?? '').toString().isEmpty)
      'requestRecipientUid': target,
  }, SetOptions(merge: true));
  await ngelxBatchCommitDogrula(
    batch: batch,
    marker: message,
    timeout: const Duration(seconds: 15),
  );
  unawaited(
    uygulamaBildirimiGonder(
      toUid: target,
      fromUid: me.uid,
      tur: 'message',
      metin: 'Sana topluluk daveti gönderdi',
      belgeId: chat.id,
      dedupeKey: 'community456_${message.id}_$target',
    ).catchError((_) {}),
  );
}

String? ngelx456InviteCode(String text) =>
    RegExp(r'ngelx://community/([A-Za-z0-9_-]{1,99})')
        .firstMatch(text)
        ?.group(1);

class Ngelx456InviteCard extends StatelessWidget {
  final String text;
  final bool own;
  const Ngelx456InviteCard({super.key, required this.text, required this.own});
  @override
  Widget build(BuildContext c) {
    final code = ngelx456InviteCode(text);
    return InkWell(
    onTap: code == null ? null : () => ngelx456OpenInvite(c, code),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.groups_outlined, color: own ? Colors.white : mor),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'TOPLULUK DAVETİ',
                style: TextStyle(
                  color: own ? Colors.white : mor,
                  fontSize: 12,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Text(
          text.split('\n').first,
          style: TextStyle(
            color: own ? Colors.white : Colors.black87,
            fontSize: 15,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          code == null ? 'Davet bağlantısı geçersiz' : 'Daveti aç →',
          style: TextStyle(color: own ? Colors.white70 : mor, fontSize: 13),
        ),
      ],
    ),
    );
  }
}

Future<void> ngelx456OpenInvite(BuildContext c, String code) async {
  try {
    final invite = await FirebaseFirestore.instance
        .collection('communityInvites450')
        .doc(code)
        .get();
    final v = invite.data();
    if (v == null ||
        v['expiresAt'] is! Timestamp ||
        (v['expiresAt'] as Timestamp).toDate().isBefore(DateTime.now()))
      throw StateError('Davet süresi doldu');
    if (!c.mounted) return;
    if (!await ngelx456Confirm(
      c,
      (v['name'] ?? 'Topluluk').toString(),
      v['joinApproval'] == true
          ? 'Katılma isteği gönderilsin mi?'
          : 'Bu topluluğa katılmak ister misin?',
    ))
      return;
    final id = v['communityId'].toString(), me = _communityUid450;
    if (me.isEmpty) return;
    // Check membership first when readable; private nonmembers use the original invite gate.
    var member = false;
    try {
      member = _communityMember450(
        (await _communities450.doc(id).get()).data() ?? {},
      );
    } catch (_) {}
    if (!member) {
      if (v['joinApproval'] == true) {
        await _communities450.doc(id).collection('requests').doc(me).set({
          'uid': me,
          'status': 'pending',
          'inviteCode': code,
          'createdAt': FieldValue.serverTimestamp(),
        });
        if (c.mounted) ngelx455Status(c, 'Katılma isteğin gönderildi');
        return;
      }
      await _communities450.doc(id).update({
        'members': FieldValue.arrayUnion([me]),
        'lastJoinCode': code,
      });
    }
    if (c.mounted)
      Navigator.push(
        c,
        MaterialPageRoute(builder: (_) => NgelXCommunityDetail450(id: id)),
      );
  } catch (e) {
    if (c.mounted)
      ngelx455Status(
        c,
        'Davet açılamadı. Süresi dolmuş veya iptal edilmiş olabilir.',
        error: true,
      );
  }
}

final _ngelx456Profiles =
    <String, Future<DocumentSnapshot<Map<String, dynamic>>>>{};
Future<DocumentSnapshot<Map<String, dynamic>>> ngelx456Profile(String uid) {
  if (_ngelx456Profiles.length >= 128)
    _ngelx456Profiles.remove(_ngelx456Profiles.keys.first);
  return _ngelx456Profiles.putIfAbsent(
    uid,
    () => FirebaseFirestore.instance.collection('users').doc(uid).get(),
  );
}

final ngelx456CountRevision = ValueNotifier<String>('');
bool ngelx456DnsFailure(Object error) {
  final e = error.toString().toLowerCase();
  return e.contains('unknownhost') ||
      e.contains('resolve host') ||
      e.contains('failed host lookup');
}

class Ngelx456Dashboard extends StatefulWidget {
  final String id;
  final Map<String, dynamic> value;
  final ValueChanged<String> open;
  const Ngelx456Dashboard({
    super.key,
    required this.id,
    required this.value,
    required this.open,
  });
  @override
  State<Ngelx456Dashboard> createState() => _Ngelx456DashboardState();
}

class _Ngelx456DashboardState extends State<Ngelx456Dashboard> {
  late final root = _communities450.doc(widget.id);
  late Future<Map<String, int>> counts = load();
  Future<Map<String, int>> load() async {
    final queries = <String, Query<Map<String, dynamic>>>{
      'Şikâyetler': root
          .collection('reports')
          .where('status', isEqualTo: 'open'),
      'Bekleyen gönderiler': root
          .collection('posts')
          .where('status', isEqualTo: 'pending'),
      'Üyelik istekleri': root
          .collection('requests')
          .where('status', isEqualTo: 'pending'),
      'Yayımlanan gönderiler': root
          .collection('posts')
          .where('status', isEqualTo: 'approved'),
    };
    final values = await Future.wait(
      queries.values.map((q) => q.count().get()),
    );
    return {
      for (var i = 0; i < values.length; i++)
        queries.keys.elementAt(i): values[i].count ?? 0,
    };
  }

  Widget card(String title, List<Widget> rows) => Container(
    margin: const EdgeInsets.only(bottom: 16),
    padding: const EdgeInsets.fromLTRB(6, 12, 6, 8),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: ngelx456Border),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          child: Text(
            title,
            style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w800),
          ),
        ),
        ...rows,
      ],
    ),
  );
  Widget row(
    IconData icon,
    String title, {
    String? sub,
    String? count,
    VoidCallback? onTap,
  }) => ListTile(
    leading: Icon(icon, color: mor, size: 24),
    title: Text(
      title,
      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
    ),
    subtitle: sub == null
        ? null
        : Text(sub, style: const TextStyle(fontSize: 12)),
    trailing: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (count != null)
          Text(
            count,
            style: const TextStyle(color: mor, fontWeight: FontWeight.w800),
          ),
        const Icon(Icons.chevron_right, size: 20, color: Colors.black45),
      ],
    ),
    onTap: onTap,
  );
  @override
  Widget build(BuildContext c) => FutureBuilder<Map<String, int>>(
    future: counts,
    builder: (c, s) {
      final v = widget.value;
      String count(String key) =>
          s.hasError ? '—' : (s.data?[key] ?? '…').toString();
      return Column(
        children: [
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: _communityImage450(
              (v['photoUrl'] ?? '').toString(),
              size: 48,
            ),
            title: Text(
              v['name'].toString(),
              style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w800),
            ),
            subtitle: Text(
              '${(v['members'] as List? ?? []).length} üye · ${v['visibility'] == 'private' ? 'Özel' : 'Herkese açık'}',
            ),
          ),
          const SizedBox(height: 16),
          card('Eylem maddeleri', [
            row(
              Icons.report_outlined,
              'Şikâyet edilen içerik',
              count: count('Şikâyetler'),
              onTap: () => widget.open('Şikâyetler'),
            ),
            row(
              Icons.pending_actions_outlined,
              'Bekleyen gönderiler',
              count: count('Bekleyen gönderiler'),
              onTap: () => widget.open('Bekleyen gönderiler'),
            ),
            if (_communityAdmin450(v))
              row(
                Icons.person_add_outlined,
                'Üyelik istekleri',
                count: count('Üyelik istekleri'),
                onTap: () => widget.open('Üyelik istekleri'),
              ),
            row(
              Icons.warning_amber_outlined,
              'Olası spam',
              sub: 'Tekrarlayan gönderileri incele',
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(
                  builder: (_) => Ngelx456PostList(id: widget.id, mode: 'spam'),
                ),
              ),
            ),
          ]),
          card('Araç kısayolları', [
            row(
              Icons.people_outline,
              'Üyeler ve roller',
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(
                  builder: (_) => Ngelx456Members(id: widget.id),
                ),
              ),
            ),
            row(
              Icons.bar_chart_outlined,
              'İstatistikler',
              onTap: () => widget.open('İstatistikler'),
            ),
            row(
              Icons.history,
              'Hareketler dökümü',
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(builder: (_) => Ngelx456Audit(id: widget.id)),
              ),
            ),
            if (_communityAdmin450(v))
              row(
                Icons.schedule,
                'Planlanmış gönderiler',
                onTap: () => Navigator.push(
                  c,
                  MaterialPageRoute(
                    builder: (_) =>
                        Ngelx456PostList(id: widget.id, mode: 'scheduled'),
                  ),
                ),
              ),
            row(
              Icons.checklist_outlined,
              'Yönetici yardımı',
              sub: 'Kurallar, onaylar ve topluluk durumu',
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(builder: (_) => Ngelx456Help(value: v)),
              ),
            ),
          ]),
          card('İstatistikler', [
            row(
              Icons.people_outline,
              'Üyeler',
              count: '${(v['members'] as List? ?? []).length}',
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(
                  builder: (_) => Ngelx456Members(id: widget.id),
                ),
              ),
            ),
            row(
              Icons.article_outlined,
              'Yayımlanan gönderiler',
              count: count('Yayımlanan gönderiler'),
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(
                  builder: (_) => Ngelx456PostList(id: widget.id),
                ),
              ),
            ),
          ]),
          if (_communityAdmin450(v))
            card('Ayarlar', [
              row(
                Icons.settings_outlined,
                'Topluluk ayarları',
                sub: 'Gizlilik, açıklama, kurallar ve onaylar',
                onTap: () => widget.open('Ayarlar'),
              ),
              row(
                Icons.wallpaper_outlined,
                'Kapak fotoğrafını düzenle',
                onTap: () => Navigator.push(
                  c,
                  MaterialPageRoute(
                    builder: (_) =>
                        Ngelx456CoverEditor(id: widget.id, value: v),
                  ),
                ),
              ),
              row(
                v['paused'] == true
                    ? Icons.play_arrow_outlined
                    : Icons.pause_circle_outline,
                v['paused'] == true
                    ? 'Topluluğu devam ettir'
                    : 'Topluluğu durdur',
                sub: 'Üyeler kalır; yeni paylaşımlar durdurulur',
                onTap: () async {
                  if (await ngelx456Confirm(
                    c,
                    'Topluluk durumu',
                    'Bu işlem yeni gönderi ve yorum izinlerini değiştirir.',
                  )) {
                    try {
                      await root.update({'paused': v['paused'] != true});
                    } catch (e) {
                      if (c.mounted) _communityError450(c, e);
                    }
                  }
                },
              ),
            ]),
          TextButton.icon(
            onPressed: () => setState(() => counts = load()),
            icon: const Icon(Icons.refresh),
            label: const Text('Sayaçları yenile'),
          ),
        ],
      );
    },
  );
}

class Ngelx456Help extends StatelessWidget {
  final Map<String, dynamic> value;
  const Ngelx456Help({super.key, required this.value});
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Yönetici yardımı',
    body: ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const ListTile(
          leading: Icon(Icons.shield_outlined, color: mor),
          title: Text('Topluluk yönetimi'),
          subtitle: Text(
            'Yönetici ayarları ve üyeleri yönetir. Moderatör gönderi, yorum ve şikâyetleri denetler. Kurucu yönetici atar.',
          ),
        ),
        for (final e in [
          ('Topluluk kuralları', (value['rules'] ?? '').toString().isNotEmpty),
          ('Üyelik onayı', value['joinApproval'] == true),
          ('Gönderi onayı', value['postApproval'] == true),
          ('Topluluk aktif', value['paused'] != true),
        ])
          ListTile(
            leading: Icon(
              e.$2 ? Icons.check_circle_outline : Icons.info_outline,
              color: e.$2 ? mor : Colors.black45,
            ),
            title: Text(e.$1),
            subtitle: Text(
              e.$2 ? 'Etkin / tamamlandı' : 'Ayarlardan düzenleyebilirsin.',
            ),
          ),
        const ListTile(
          title: Text('Şikâyetleri değerlendir'),
          subtitle: Text(
            'İçeriği incele; gerekirse kaldır. Üye çıkarma ve yetki değişiklikleri işlem geçmişine kaydedilir.',
          ),
        ),
      ],
    ),
  );
}

class Ngelx456Audit extends StatefulWidget {
  final String id;
  const Ngelx456Audit({super.key, required this.id});
  @override
  State<Ngelx456Audit> createState() => _Ngelx456AuditState();
}

class _Ngelx456AuditState extends State<Ngelx456Audit> {
  late final stream = _communities450
      .doc(widget.id)
      .collection('audit456')
      .orderBy('createdAt', descending: true)
      .limit(100)
      .snapshots();
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Yönetim işlem geçmişi',
    body: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: stream,
      builder: (c, s) {
        if (s.hasError)
          return const Center(child: Text('İşlem geçmişi yüklenemedi.'));
        if (!s.hasData) return const Center(child: CircularProgressIndicator());
        final docs = s.data!.docs;
        if (docs.isEmpty)
          return const Center(child: Text('Henüz yönetim işlemi yok.'));
        return ListView.builder(
          itemCount: docs.length,
          itemBuilder: (c, i) {
            final v = docs[i].data();
            return ListTile(
              leading: const Icon(Icons.history, color: mor),
              title: Text(
                {
                      'admin': 'Yönetici rolü değiştirildi',
                      'moderator': 'Moderatör rolü değiştirildi',
                      'mute': 'Susturma değiştirildi',
                      'remove': 'Üye çıkarıldı',
                      'ban': 'Üye engellendi',
                      'delete': 'Gönderi kaldırıldı',
                    }[v['action']] ??
                    v['action'].toString(),
              ),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  NgelXFounder450(
                    uid: (v['actor'] ?? '').toString(),
                    label: 'İşlemi yapan',
                  ),
                  NgelXFounder450(
                    uid: (v['target'] ?? '').toString(),
                    label: 'Üye',
                  ),
                ],
              ),
              trailing: Text(
                ngelx456Time(v['createdAt']),
                style: const TextStyle(fontSize: 11),
              ),
            );
          },
        );
      },
    ),
  );
}

class Ngelx456PostList extends StatefulWidget {
  final String id, mode;
  const Ngelx456PostList({super.key, required this.id, this.mode = 'approved'});
  @override
  State<Ngelx456PostList> createState() => _Ngelx456PostListState();
}

class _Ngelx456PostListState extends State<Ngelx456PostList> {
  late final stream = _communities450
      .doc(widget.id)
      .collection('posts')
      .where(
        'status',
        isEqualTo: widget.mode == 'scheduled' ? 'scheduled' : 'approved',
      )
      .limit(50)
      .snapshots();
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: widget.mode == 'spam'
        ? 'Olası spam'
        : widget.mode == 'scheduled'
        ? 'Planlanmış gönderiler'
        : 'Yayımlanan gönderiler',
    body: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: stream,
      builder: (c, s) {
        if (s.hasError)
          return const Center(child: Text('Gönderiler yüklenemedi.'));
        if (!s.hasData) return const Center(child: CircularProgressIndicator());
        var docs = s.data!.docs;
        final counts = <String, int>{};
        if (widget.mode == 'spam') {
          for (final d in docs) {
            final v = d.data(),
                key =
                    '${v['authorId']}|${(v['text'] ?? '').toString().trim().toLowerCase()}';
            counts[key] = (counts[key] ?? 0) + 1;
          }
          docs = docs.where((d) {
            final v = d.data();
            return (v['text'] ?? '').toString().trim().isNotEmpty &&
                (counts['${v['authorId']}|${(v['text'] ?? '').toString().trim().toLowerCase()}'] ??
                        0) >
                    1;
          }).toList();
        }
        if (docs.isEmpty)
          return Center(
            child: Text(
              widget.mode == 'spam'
                  ? 'Son 50 gönderide tekrarlanan metin yok.'
                  : 'Bu bölümde gönderi yok.',
            ),
          );
        return ListView.builder(
          itemCount: docs.length,
          itemBuilder: (c, i) {
            final d = docs[i], v = d.data();
            return NgelXCommunityPost450(
              communityId: widget.id,
              id: d.id,
              value: v,
              member: true,
              admin: true,
            );
          },
        );
      },
    ),
  );
}

Future<void> ngelx456PostMenu(
  BuildContext context,
  String cid,
  String pid,
  Map<String, dynamic> post,
  bool member,
  bool moderator,
) async {
  final root = _communities450.doc(cid),
      ref = root.collection('posts').doc(pid),
      me = _communityUid450;
  Map<String, dynamic> v;
  try {
    v = (await root.get()).data() ?? {};
  } catch (e) {
    if (context.mounted) _communityError450(context, e);
    return;
  }
  if (!context.mounted) return;
  final admin = _communityAdmin450(v),
      author = (post['authorId'] ?? '').toString();
  final options = <String, (IconData, String, String?)>{
    'save': (
      Icons.bookmark_outline,
      'Gönderiyi kaydet',
      'Profilindeki kaydedilenlere ekle',
    ),
    if (member)
      'report': (Icons.flag_outlined, 'Yöneticilere şikâyet et', null),
    'copy': (Icons.link, 'Bağlantıyı kopyala', null),
    if (member)
      'notify': (
        Icons.notifications_outlined,
        'Gönderi bildirim tercihleri',
        null,
      ),
    if (moderator)
      'pin': (
        Icons.push_pin_outlined,
        post['pinned'] == true
            ? 'Öne çıkarmayı kaldır'
            : 'Öne çıkanlara tuttur',
        null,
      ),
    if (moderator || author == me)
      'delete': (Icons.delete_outline, 'Gönderiyi kaldır', null),
    if (admin &&
        author != v['founderId'] &&
        !List<String>.from(v['admins'] ?? const []).contains(author))
      'approval': (
        Icons.fact_check_outlined,
        'Üye için gönderi onayını aç',
        null,
      ),
    if (admin &&
        author != v['founderId'] &&
        !List<String>.from(v['admins'] ?? const []).contains(author))
      'mute': (
        Icons.volume_off_outlined,
        'Üyenin izinlerini durdur',
        'Yeni gönderi ve yorumları sustur',
      ),
    if (moderator)
      'comments': (
        Icons.comments_disabled_outlined,
        post['commentsClosed'] == true
            ? 'Yorum yapmayı aç'
            : 'Yorum yapmayı kapat',
        null,
      ),
    if (moderator)
      'slow': (
        Icons.slow_motion_video,
        'Yorumları yavaşlat',
        'Her üye 5 dakikada bir yorum yapabilir',
      ),
    if (admin &&
        author != v['founderId'] &&
        !List<String>.from(v['admins'] ?? const []).contains(author))
      'remove': (
        Icons.person_remove_outlined,
        'Gönderiyi sil ve üyeyi çıkar',
        null,
      ),
    if (admin &&
        author != v['founderId'] &&
        !List<String>.from(v['admins'] ?? const []).contains(author))
      'ban': (Icons.block_outlined, 'Gönderiyi sil ve üyeyi engelle', null),
    if (moderator)
      'feedback': (
        Icons.feedback_outlined,
        'Görüş bildir',
        'Gönderiyi yazan kişiye bir öneri gönder',
      ),
  };
  final action = await showModalBottomSheet<String>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    showDragHandle: true,
    builder: (c) => SafeArea(
      child: SizedBox(
        height: MediaQuery.sizeOf(c).height * .75,
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 20),
          children: [
            const Padding(
              padding: EdgeInsets.all(12),
              child: Text(
                'Gönderi seçenekleri',
                style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800),
              ),
            ),
            ...options.entries.map(
              (e) => Card(
                color: ngelx456Soft,
                elevation: 0,
                child: ListTile(
                  leading: Icon(e.value.$1, color: mor),
                  title: Text(
                    e.value.$2,
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  subtitle: e.value.$3 == null
                      ? null
                      : Text(e.value.$3!, style: const TextStyle(fontSize: 12)),
                  onTap: () => Navigator.pop(c, e.key),
                ),
              ),
            ),
          ],
        ),
      ),
    ),
  );
  if (action == null || !context.mounted) return;
  try {
    if ([
          'delete',
          'remove',
          'ban',
          'mute',
          'approval',
          'comments',
          'slow',
        ].contains(action) &&
        !await ngelx456Confirm(
          context,
          options[action]!.$2,
          'Bu değişiklik toplulukta uygulanacak.',
        ))
      return;
    if (action == 'save') {
      await FirebaseFirestore.instance
          .collection('users')
          .doc(me)
          .collection('saved')
          .doc('community_${cid}_$pid')
          .set({
            'communityId': cid,
            'postId': pid,
            'type': 'community',
            'savedAt': FieldValue.serverTimestamp(),
          });
    }
    if (action == 'copy')
      await Clipboard.setData(
        ClipboardData(text: '$ngelxWebAdresi/community/$cid/post/$pid'),
      );
    if (action == 'report')
      await root.collection('reports').doc('${pid}_$me').set({
        'uid': me,
        'postId': pid,
        'status': 'open',
        'createdAt': FieldValue.serverTimestamp(),
      });
    if (action == 'pin') await ref.update({'pinned': post['pinned'] != true});
    if (action == 'delete') await ref.update({'status': 'deleted'});
    if (action == 'comments')
      await ref.update({'commentsClosed': post['commentsClosed'] != true});
    if (action == 'slow')
      await ref.update({'slowSeconds': post['slowSeconds'] == 300 ? 0 : 300});
    if (action == 'mute')
      await root.update({
        'muted': FieldValue.arrayUnion([author]),
      });
    if (action == 'approval')
      await root.update({
        'approvalMembers': FieldValue.arrayUnion([author]),
      });
    if (action == 'remove' || action == 'ban') {
      final batch = FirebaseFirestore.instance.batch();
      batch.update(ref, {'status': 'deleted'});
      batch.update(root, {
        'members': FieldValue.arrayRemove([author]),
        'moderators': FieldValue.arrayRemove([author]),
        'muted': FieldValue.arrayRemove([author]),
        if (action == 'ban') 'banned': FieldValue.arrayUnion([author]),
      });
      batch.set(root.collection('audit456').doc(), {
        'actor': me,
        'target': author,
        'action': action,
        'createdAt': FieldValue.serverTimestamp(),
      });
      await batch.commit();
    }
    if (action == 'notify') {
      final saved = ref.collection('subscribers456').doc(me),
          current = await saved.get();
      await saved.set({
        'uid': me,
        'enabled': current.data()?['enabled'] != true,
      });
    }
    if (action == 'feedback') {
      // Keep draft text in the dialog closure: no controller is disposed
      // before the route's closing transition has finished.
      var draft = '';
      final text = await showDialog<String>(
        context: context,
        builder: (c) => Ngelx455WhiteDialog(
          title: const Text('Gönderiye görüş bildir'),
          content: TextField(
            onChanged: (value) => draft = value,
            maxLength: 500,
            maxLines: 3,
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(c),
              child: const Text('Vazgeç'),
            ),
            FilledButton(
              onPressed: () => Navigator.pop(c, draft.trim()),
              child: const Text('Gönder'),
            ),
          ],
        ),
      );
      if (text == null || text.isEmpty) return;
      await ref.collection('feedback456').add({
        'uid': me,
        'text': text,
        'createdAt': FieldValue.serverTimestamp(),
      });
    }
    if (context.mounted) ngelx455Status(context, 'İşlem tamamlandı');
  } catch (e) {
    if (context.mounted) _communityError450(context, e);
  }
}

class Ngelx456Saved extends StatefulWidget {
  const Ngelx456Saved({super.key});
  @override
  State<Ngelx456Saved> createState() => _Ngelx456SavedState();
}

class _Ngelx456SavedState extends State<Ngelx456Saved> {
  late final query = FirebaseFirestore.instance
      .collection('users')
      .doc(_communityUid450)
      .collection('saved')
      .orderBy('savedAt', descending: true)
      .limit(100);
  late Stream<QuerySnapshot<Map<String, dynamic>>> stream = query.snapshots();
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Kaydedilen topluluk gönderileri',
    body: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: stream,
      builder: (c, s) {
        if (s.hasError)
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Kaydedilenler yüklenemedi. Bağlantını kontrol edip yeniden dene.',
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  OutlinedButton.icon(
                    onPressed: () => setState(() => stream = query.snapshots()),
                    icon: const Icon(Icons.refresh),
                    label: const Text('Yeniden dene'),
                  ),
                ],
              ),
            ),
          );
        if (!s.hasData) return const Center(child: CircularProgressIndicator());
        final docs = s.data!.docs
            .where((d) => d.data()['type'] == 'community')
            .toList();
        if (docs.isEmpty)
          return const Center(
            child: Text('Kaydedilmiş topluluk gönderisi yok.'),
          );
        return ListView.builder(
          itemCount: docs.length,
          itemBuilder: (c, i) {
            final d = docs[i], v = d.data();
            return ListTile(
              leading: const Icon(Icons.bookmark_outline, color: mor),
              title: Text(
                'Topluluk gönderisi',
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              subtitle: const Text('Gönderiyi topluluğunda aç'),
              onTap: () => Navigator.push(
                c,
                MaterialPageRoute(
                  builder: (_) => Ngelx456PostPage(
                    cid: v['communityId'].toString(),
                    pid: v['postId'].toString(),
                  ),
                ),
              ),
              trailing: IconButton(
                tooltip: 'Kaydı kaldır',
                onPressed: () async {
                  try {
                    await d.reference.delete();
                    if (c.mounted) ngelx455Status(c, 'Kayıt kaldırıldı');
                  } catch (error) {
                    if (c.mounted) _communityError450(c, error);
                  }
                },
                icon: const Icon(Icons.bookmark_remove_outlined),
              ),
            );
          },
        );
      },
    ),
  );
}

class Ngelx456PostPage extends StatefulWidget {
  final String cid, pid;
  const Ngelx456PostPage({super.key, required this.cid, required this.pid});
  @override
  State<Ngelx456PostPage> createState() => _Ngelx456PostPageState();
}

class _Ngelx456PostPageState extends State<Ngelx456PostPage> {
  late final community = _communities450.doc(widget.cid).snapshots();
  late final post = _communities450
      .doc(widget.cid)
      .collection('posts')
      .doc(widget.pid)
      .snapshots();
  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Topluluk gönderisi',
    body: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: community,
      builder: (c, s) {
        if (s.hasError)
          return const Center(child: Text('Bu topluluğa artık erişimin yok.'));
        if (!s.hasData) return const Center(child: CircularProgressIndicator());
        final root = s.data?.data() ?? {};
        return StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
          stream: post,
          builder: (c, p) {
            if (p.hasError ||
                p.hasData &&
                    (p.data?.exists != true ||
                        p.data?.data()?['status'] == 'deleted'))
              return const Center(child: Text('Gönderi artık kullanılamıyor.'));
            if (!p.hasData)
              return const Center(child: CircularProgressIndicator());
            return ListView(
              children: [
                ListTile(
                  title: Text(
                    (root['name'] ?? 'Topluluk').toString(),
                    style: const TextStyle(fontWeight: FontWeight.w800),
                  ),
                  onTap: () => Navigator.push(
                    c,
                    MaterialPageRoute(
                      builder: (_) => NgelXCommunityDetail450(id: widget.cid),
                    ),
                  ),
                ),
                NgelXCommunityPost450(
                  communityId: widget.cid,
                  id: widget.pid,
                  value: p.data!.data()!,
                  member: _communityMember450(root),
                  admin: ngelx456Moderator(root),
                ),
              ],
            );
          },
        );
      },
    ),
  );
}
