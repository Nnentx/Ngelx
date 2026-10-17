part of 'main.dart';

final _communities450 = FirebaseFirestore.instance.collection('communities450');
String get _communityUid450 => FirebaseAuth.instance.currentUser?.uid ?? '';
bool _communityAdmin450(Map<String, dynamic> v) =>
    List<String>.from(v['admins'] ?? []).contains(_communityUid450);
bool _communityMember450(Map<String, dynamic> v) =>
    List<String>.from(v['members'] ?? []).contains(_communityUid450);
void _communityError450(BuildContext c, Object e) {
  if (c.mounted)
    ScaffoldMessenger.of(c).showSnackBar(
      SnackBar(content: Text('İşlem tamamlanamadı. ${_ngelxKisaHata(e)}')),
    );
}

Widget _communityImage450(
  String url, {
  double size = 56,
  bool circle = false,
}) => ClipRRect(
  borderRadius: BorderRadius.circular(circle ? size : 14),
  child: url.isEmpty
      ? Container(
          width: size,
          height: size,
          color: const Color(0xFFF0E8FF),
          child: const Icon(Icons.groups_rounded, color: mor),
        )
      : NgelXAgResmi(
          imageUrl: url,
          width: size,
          height: size,
          fit: BoxFit.cover,
          errorWidget: (_, __, ___) => SizedBox(
            width: size,
            height: size,
            child: const Icon(Icons.groups_rounded, color: mor),
          ),
        ),
);
Widget _communitySurface450({
  required String title,
  required Widget body,
  List<Widget>? actions,
}) => Theme(
  data: ThemeData.light().copyWith(
    colorScheme: ColorScheme.fromSeed(seedColor: mor),
    scaffoldBackgroundColor: Colors.white,
  ),
  child: Scaffold(
    backgroundColor: Colors.white,
    appBar: AppBar(
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
      title: Text(title),
      actions: actions,
    ),
    body: SafeArea(child: body),
  ),
);

class NgelXFounder450 extends StatelessWidget {
  final String uid;
  final String label;
  const NgelXFounder450({super.key, required this.uid, this.label = 'Kurucu'});
  @override
  Widget build(BuildContext c) {
    if (uid.isEmpty) return const SizedBox.shrink();
    return FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      future: FirebaseFirestore.instance.collection('users').doc(uid).get(),
      builder: (c, s) {
        final v = s.data?.data() ?? {};
        final name = (v['displayName'] ?? v['username'] ?? 'Kurucu').toString();
        return InkWell(
          onTap: () => Navigator.push(
            c,
            MaterialPageRoute(builder: (_) => KullaniciProfilPage(uid: uid)),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Row(
              children: [
                _communityImage450(
                  (v['photoUrl'] ?? '').toString(),
                  size: 20,
                  circle: true,
                ),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    '$label: $name',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: Colors.black54, fontSize: 11),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class NgelXCommunityDirectory450 extends StatefulWidget {
  const NgelXCommunityDirectory450({super.key});
  @override
  State<NgelXCommunityDirectory450> createState() =>
      _NgelXCommunityDirectory450State();
}

class _NgelXCommunityDirectory450State
    extends State<NgelXCommunityDirectory450> {
  String search = '', category = 'Tümü';
  int limit = 30;
  final categories = [
    'Tümü',
    'Sohbet',
    'Müzik',
    'Spor',
    'Teknoloji',
    'Gezi ve doğa',
  ];
  Future<void> invite() async {
    final field = TextEditingController();
    final code = await showDialog<String>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Davet koduyla katıl'),
        content: TextField(
          controller: field,
          decoration: const InputDecoration(labelText: 'Davet kodu'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(c),
            child: const Text('İptal'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(c, field.text.trim()),
            child: const Text('Devam'),
          ),
        ],
      ),
    );
    field.dispose();
    if (code == null || code.isEmpty || !mounted) return;
    try {
      final d = await FirebaseFirestore.instance
          .collection('communityInvites450')
          .doc(code)
          .get();
      final v = d.data();
      if (v == null ||
          (v['expiresAt'] as Timestamp).toDate().isBefore(DateTime.now()))
        throw Exception('Davet geçersiz veya süresi dolmuş.');
      final id = v['communityId'].toString();
      if (v['joinApproval'] == true) {
        await _communities450
            .doc(id)
            .collection('requests')
            .doc(_communityUid450)
            .set({
              'uid': _communityUid450,
              'status': 'pending',
              'inviteCode': code,
              'createdAt': FieldValue.serverTimestamp(),
            });
        if (mounted)
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Katılma isteğin gönderildi.')),
          );
      } else {
        await _communities450.doc(id).update({
          'members': FieldValue.arrayUnion([_communityUid450]),
          'lastJoinCode': code,
        });
        if (mounted)
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => NgelXCommunityDetail450(id: id)),
          );
      }
    } catch (e) {
      if (mounted) _communityError450(context, e);
    }
  }

  @override
  Widget build(BuildContext c) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: TextField(
          onChanged: (v) => setState(() => search = v.toLowerCase()),
          decoration: InputDecoration(
            hintText: 'Topluluk ara',
            prefixIcon: const Icon(Icons.search),
            filled: true,
            fillColor: const Color(0xFFF4F5F8),
            border: OutlineInputBorder(
              borderSide: BorderSide.none,
              borderRadius: BorderRadius.circular(20),
            ),
          ),
        ),
      ),
      SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(
          children: categories
              .map(
                (v) => Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: ChoiceChip(
                    selectedColor:const Color(0xFFF0E8FF),
                    backgroundColor:Colors.white,
                    checkmarkColor:mor,
                    labelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w700),
                    label: Text(v),
                    selected: category == v,
                    onSelected: (_) => setState(() => category = v),
                  ),
                ),
              )
              .toList(),
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
        child: Row(
          children: [
            const Expanded(
              child: Text(
                'Toplulukları keşfet',
                style: TextStyle(
                  fontSize: 21,
                  fontWeight: FontWeight.w900,
                  color: Colors.black,
                ),
              ),
            ),
            TextButton(
              onPressed: _communityUid450.isEmpty ? null : invite,
              child: const Text('Davet kodu'),
            ),
          ],
        ),
      ),
      if (_communityUid450.isNotEmpty)
        StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
          stream: _communities450
              .where('members', arrayContains: _communityUid450)
              .limit(30)
              .snapshots(),
          builder: (c, s) {
            final ds = (s.data?.docs ?? [])
                .where((d) => d.data()['visibility'] == 'private')
                .toList();
            return Column(
              children: ds
                  .map((d) => NgelXCommunityCard450(id: d.id, value: d.data()))
                  .toList(),
            );
          },
        ),
      StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
        stream: _communities450
            .where('visibility', isEqualTo: 'public')
            .limit(limit)
            .snapshots(),
        builder: (c, s) {
          if (s.hasError)
            return const Padding(
              padding: EdgeInsets.all(24),
              child: Text('Topluluklar yüklenemedi. Yenile ve tekrar dene.'),
            );
          if (!s.hasData)
            return const Padding(
              padding: EdgeInsets.all(24),
              child: Center(child: CircularProgressIndicator()),
            );
          final ds = s.data!.docs.where((d) {
            final v = d.data();
            return (category == 'Tümü' || v['category'] == category) &&
                ('${v['name']} ${v['description']}'.toLowerCase().contains(
                  search,
                ));
          }).toList();
          return Column(
            children: [
              if (ds.isEmpty)
                const Padding(
                  padding: EdgeInsets.all(30),
                  child: Text(
                    'Henüz uygun topluluk yok. + ile ilk topluluğunu oluştur.',
                  ),
                ),
              ...ds.map(
                (d) => NgelXCommunityCard450(id: d.id, value: d.data()),
              ),
              if (s.data!.docs.length >= limit)
                TextButton(
                  onPressed: () => setState(() => limit += 30),
                  child: const Text('Daha fazla göster'),
                ),
            ],
          );
        },
      ),
    ],
  );
}

class NgelXCommunityCard450 extends StatelessWidget {
  final String id;
  final Map<String, dynamic> value;
  const NgelXCommunityCard450({
    super.key,
    required this.id,
    required this.value,
  });
  @override
  Widget build(BuildContext c) => Container(
    margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      border: Border.all(color: const Color(0xFFE7E7ED)),
    ),
    child: InkWell(
      onTap: () => Navigator.push(
        c,
        MaterialPageRoute(builder: (_) => NgelXCommunityDetail450(id: id)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _communityImage450((value['photoUrl'] ?? '').toString(), size: 66),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  value['name'].toString(),
                  style: const TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.w900,
                    fontSize: 16,
                  ),
                ),
                Text(
                  value['description'].toString(),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.black54, fontSize: 12),
                ),
                NgelXFounder450(uid: value['founderId'].toString()),
                Wrap(
                  spacing: 8,
                  crossAxisAlignment: WrapCrossAlignment.center,
                  children: [
                    Text(
                      '${(value['members'] as List).length} üye · ${value['joinApproval'] == true
                          ? 'Onay gerekli'
                          : value['visibility'] == 'private'
                          ? 'Özel'
                          : 'Herkese açık'}',
                      style: const TextStyle(
                        color: Colors.black54,
                        fontSize: 11,
                      ),
                    ),
                    NgelXCommunityJoin450(id: id, value: value),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

class NgelXCommunityJoin450 extends StatefulWidget {
  final String id;
  final Map<String, dynamic> value;
  const NgelXCommunityJoin450({
    super.key,
    required this.id,
    required this.value,
  });
  @override
  State<NgelXCommunityJoin450> createState() => _NgelXCommunityJoin450State();
}

class _NgelXCommunityJoin450State extends State<NgelXCommunityJoin450> {
  bool busy = false;
  Future<void> act(bool pending) async {
    if (await misafirEngeli(context)) return;
    setState(() => busy = true);
    try {
      final ref = _communities450.doc(widget.id);
      if (_communityMember450(widget.value)) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => NgelXCommunityDetail450(id: widget.id),
          ),
        );
      } else if (widget.value['joinApproval'] == true) {
        final r = ref.collection('requests').doc(_communityUid450);
        if (pending) {
          await r.delete();
        } else {
          await r.set({
            'uid': _communityUid450,
            'status': 'pending',
            'inviteCode': '',
            'createdAt': FieldValue.serverTimestamp(),
          });
        }
      } else {
        await ref.update({
          'members': FieldValue.arrayUnion([_communityUid450]),
          'lastJoinCode': '',
        });
      }
    } catch (e) {
      if (mounted) _communityError450(context, e);
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext c) {
    if (_communityUid450.isEmpty)
      return TextButton(
        onPressed: () => misafirEngeli(c),
        child: const Text('Giriş yap'),
      );
    return StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: _communities450
          .doc(widget.id)
          .collection('requests')
          .doc(_communityUid450)
          .snapshots(),
      builder: (c, s) {
        final pending = s.data?.data()?['status'] == 'pending';
        return FilledButton(
          onPressed: busy ? null : () => act(pending),
          style: FilledButton.styleFrom(
            backgroundColor: pending ? const Color(0xFFF0E8FF) : mor,
            foregroundColor: pending ? mor : Colors.white,
          ),
          child: Text(
            _communityMember450(widget.value)
                ? _ngelx438Ui("Aç")
                : pending
                ? 'İstek gönderildi · İptal et'
                : widget.value['joinApproval'] == true
                ? 'İstek gönder'
                : _ngelx438Ui("Katıl"),
            style: const TextStyle(fontSize: 12),
          ),
        );
      },
    );
  }
}

class NgelXCommunityCreate450 extends StatefulWidget {
  const NgelXCommunityCreate450({super.key});
  @override
  State<NgelXCommunityCreate450> createState() =>
      _NgelXCommunityCreate450State();
}

class _NgelXCommunityCreate450State extends State<NgelXCommunityCreate450> {
  final name = TextEditingController(),
      desc = TextEditingController(),
      rules = TextEditingController();
  String category = 'Sohbet';
  bool private = false,
      joinApproval = false,
      postApproval = false,
      busy = false;
  XFile? photo, cover;
  final form = GlobalKey<FormState>();
  @override
  void dispose() {
    name.dispose();
    desc.dispose();
    rules.dispose();
    super.dispose();
  }

  Future<void> create() async {
    if (!form.currentState!.validate() || await misafirEngeli(context)) return;
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Topluluk önizlemesi'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              name.text.trim(),
              style: const TextStyle(fontWeight: FontWeight.w900),
            ),
            Text(desc.text.trim()),
            const SizedBox(height: 12),
            Text(
              private
                  ? 'Özel · Gönderiler yalnızca üyelere görünür'
                  : 'Herkese açık · Keşfet’te görünecek',
            ),
            Text(joinApproval ? 'Üyelik onaylı' : 'Doğrudan katılım'),
            Text(
              postApproval
                  ? 'Gönderiler onaylı'
                  : 'Üyeler doğrudan paylaşabilir',
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(c, false),
            child: Text(_ngelx438Ui("Düzenle")),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(c, true),
            child: const Text('Topluluğu oluştur'),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;
    setState(() => busy = true);
    try {
      final ref = _communities450.doc();
      String p = '', k = '';
      if (photo != null)
        p = await ngelxFotografYukle(
          dosya: photo!,
          kind: 'groups',
          legacyPath: 'communities/${ref.id}/photo.jpg',
        );
      if (cover != null)
        k = await ngelxFotografYukle(
          dosya: cover!,
          kind: 'groups',
          legacyPath: 'communities/${ref.id}/cover.jpg',
        );
      await ref.set({
        'name': name.text.trim(),
        'description': desc.text.trim(),
        'rules': rules.text.trim(),
        'category': category,
        'photoUrl': p,
        'coverUrl': k,
        'founderId': _communityUid450,
        'members': [_communityUid450],
        'admins': [_communityUid450],
        'visibility': private ? 'private' : 'public',
        'joinApproval': joinApproval,
        'postApproval': postApproval,
        'lastJoinCode': '',
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => NgelXCommunityDetail450(id: ref.id),
          ),
        );
    } catch (e) {
      if (mounted) _communityError450(context, e);
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> image(bool isCover) async {
    final x = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (x != null && mounted) setState(() => isCover ? cover = x : photo = x);
  }

  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Topluluk oluştur',
    body: Form(
      key: form,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: busy ? null : () => image(false),
                  icon: const Icon(Icons.photo_camera),
                  label: Text(
                    photo == null ? 'Fotoğraf ekle' : 'Fotoğraf seçildi',
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: busy ? null : () => image(true),
                  icon: const Icon(Icons.landscape),
                  label: Text(cover == null ? 'Kapak ekle' : 'Kapak seçildi'),
                ),
              ),
            ],
          ),
          TextFormField(
            controller: name,
            maxLength: 60,
            decoration: const InputDecoration(labelText: 'Topluluk adı'),
            validator: (v) => v == null || v.trim().length < 3
                ? 'En az 3 karakter gir.'
                : null,
          ),
          TextFormField(
            controller: desc,
            maxLength: 240,
            maxLines: 2,
            decoration: const InputDecoration(labelText: 'Açıklama'),
            validator: (v) =>
                v == null || v.trim().isEmpty ? 'Açıklama gir.' : null,
          ),
          DropdownButtonFormField<String>(
            initialValue: category,
            decoration: InputDecoration(labelText: _ngelx438Ui("Kategori")),
            items: [
              'Sohbet',
              'Müzik',
              'Spor',
              'Teknoloji',
              'Gezi ve doğa',
            ].map((v) => DropdownMenuItem(value: v, child: Text(v))).toList(),
            onChanged: busy ? null : (v) => setState(() => category = v!),
          ),
          TextFormField(
            controller: rules,
            maxLength: 2000,
            maxLines: 3,
            decoration: InputDecoration(
              labelText: _ngelx438Ui("Topluluk kuralları"),
            ),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Özel topluluk'),
            subtitle: Text(
              private
                  ? 'Yalnızca davetle bulunur; gönderiler üyelere açıktır.'
                  : 'Keşfet’te herkes bulabilir.',
            ),
            value: private,
            onChanged: busy ? null : (v) => setState(() => private = v),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Üyelik onayı'),
            value: joinApproval,
            onChanged: busy ? null : (v) => setState(() => joinApproval = v),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Gönderi onayı'),
            value: postApproval,
            onChanged: busy ? null : (v) => setState(() => postApproval = v),
          ),
          FilledButton(
            onPressed: busy ? null : create,
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Text(busy ? 'Oluşturuluyor…' : 'Önizle ve oluştur'),
            ),
          ),
        ],
      ),
    ),
  );
}

class NgelXCommunityDetail450 extends StatefulWidget {
  final String id;
  const NgelXCommunityDetail450({super.key, required this.id});
  @override
  State<NgelXCommunityDetail450> createState() =>
      _NgelXCommunityDetail450State();
}

class _NgelXCommunityDetail450State extends State<NgelXCommunityDetail450> {
  String tab = 'Gönderiler', search = '';
  int postLimit = 40;
  int feedRetry451 = 0;
  Future<void> invite(Map<String, dynamic> v) async {
    try {
      final ref = FirebaseFirestore.instance
          .collection('communityInvites450')
          .doc();
      await ref.set({
        'communityId': widget.id,
        'name': v['name'],
        'joinApproval': v['joinApproval'],
        'createdBy': _communityUid450,
        'expiresAt': Timestamp.fromDate(
          DateTime.now().add(const Duration(days: 6, hours: 23)),
        ),
      });
      await SharePlus.instance.share(
        ShareParams(
          text:
              '${v['name']} topluluğuna davetlisin. NgelX → Keşfet → Topluluk → Davet kodu: ${ref.id}',
        ),
      );
    } catch (e) {
      if (mounted) _communityError450(context, e);
    }
  }

  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Topluluk',
    body: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: _communities450.doc(widget.id).snapshots(),
      builder: (c, s) {
        if (s.hasError)
          return const Center(
            child: Text('Bu topluluğa erişim yok. Davet veya üyelik gerekli.'),
          );
        if (!s.hasData) return const Center(child: CircularProgressIndicator());
        final v = s.data!.data();
        if (v == null) return const Center(child: Text('Topluluk bulunamadı.'));
        final member = _communityMember450(v), admin = _communityAdmin450(v);
        return ListView(
          children: [
            if ((v['coverUrl'] ?? '').toString().isNotEmpty)
              NgelXAgResmi(
                imageUrl: v['coverUrl'],
                height: 150,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      _communityImage450(v['photoUrl'].toString(), size: 64),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              v['name'],
                              style: const TextStyle(
                                fontSize: 21,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                            Text(
                              '${(v['members'] as List).length} üye · ${v['visibility'] == 'public' ? 'Herkese açık' : 'Özel'}',
                            ),
                            NgelXFounder450(uid: v['founderId']),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Text(v['description']),
                  if (v['rules'].toString().isNotEmpty)
                    ExpansionTile(
                      tilePadding: EdgeInsets.zero,
                      title: Text(_ngelx438Ui("Topluluk kuralları")),
                      children: [Text(v['rules'])],
                    ),
                  Wrap(
                    spacing: 8,
                    children: [
                      if (!member)
                        NgelXCommunityJoin450(id: widget.id, value: v)
                      else
                        OutlinedButton(
                          onPressed: v['founderId'] == _communityUid450
                              ? null
                              : () async {
                                  final ok = await showDialog<bool>(
                                    context: c,
                                    builder: (d) => AlertDialog(
                                      title: const Text('Topluluktan ayrıl?'),
                                      actions: [
                                        TextButton(
                                          onPressed: () =>
                                              Navigator.pop(d, false),
                                          child: const Text('İptal'),
                                        ),
                                        FilledButton(
                                          onPressed: () =>
                                              Navigator.pop(d, true),
                                          child: Text(_ngelx438Ui("Ayrıl")),
                                        ),
                                      ],
                                    ),
                                  );
                                  if (ok == true) {
                                    try {
                                      await _communities450
                                          .doc(widget.id)
                                          .update({
                                            'members': FieldValue.arrayRemove([
                                              _communityUid450,
                                            ]),
                                            'admins': FieldValue.arrayRemove([
                                              _communityUid450,
                                            ]),
                                          });
                                      if (mounted &&
                                          v['visibility'] == 'private')
                                        Navigator.pop(context);
                                    } catch (e) {
                                      if (mounted)
                                        _communityError450(context, e);
                                    }
                                  }
                                },
                          child: const Text('Katıldın'),
                        ),
                      if (admin)
                        OutlinedButton.icon(
                          onPressed: () => invite(v),
                          icon: const Icon(Icons.person_add),
                          label: Text(_ngelx438Ui("Davet et")),
                        ),
                      if (admin)
                        OutlinedButton.icon(
                          onPressed: () => Navigator.push(
                            c,
                            MaterialPageRoute(
                              builder: (_) =>
                                  NgelXCommunityAdmin450(id: widget.id),
                            ),
                          ),
                          icon: const Icon(Icons.settings),
                          label: const Text('Yönet'),
                        ),
                    ],
                  ),
                  const Divider(),
                  TextField(
                    onChanged: (x) => setState(() => search = x.toLowerCase()),
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.search),
                      hintText: 'Topluluk içinde ara',
                    ),
                  ),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children:
                          [
                                'Gönderiler',
                                'Öne çıkanlar',
                                'Videolar',
                                'Fotoğraflar',
                              ]
                              .map(
                                (x) => TextButton(
                                  onPressed: () => setState(() => tab = x),
                                  child: Text(
                                    x,
                                    style: TextStyle(
                                      color: tab == x ? mor : Colors.black54,
                                      fontWeight: FontWeight.w800,
                                    ),
                                  ),
                                ),
                              )
                              .toList(),
                    ),
                  ),
                  if (member)
                    OutlinedButton.icon(
                      onPressed: () => Navigator.push(
                        c,
                        MaterialPageRoute(
                          builder: (_) =>
                              NgelXCommunityCompose450(id: widget.id, value: v),
                        ),
                      ),
                      icon: const Icon(Icons.edit),
                      label: const Text('Toplulukla bir şey paylaş…'),
                    ),
                  if (!member && v['visibility'] == 'private')
                    const Text('Gönderiler yalnızca üyelere görünür.'),
                ],
              ),
            ),
            if (member || v['visibility'] == 'public')
              StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                key:ValueKey('community-feed-$feedRetry451'),
                stream: _communities450
                    .doc(widget.id)
                    .collection('posts')
                    .where('status', isEqualTo: 'approved')
                    .orderBy('createdAt', descending: true)
                    .limit(postLimit)
                    .snapshots(),
                builder: (c, p) {
                  if (p.hasError) {
                    final preparing=p.error is FirebaseException&&(p.error as FirebaseException).code=='failed-precondition';
                    return Padding(padding:const EdgeInsets.all(20),child:Column(children:[
                      Text(preparing?'Gönderi akışı henüz hazır değil. Biraz sonra yeniden dene.':'Gönderiler yüklenemedi.'),
                      TextButton.icon(onPressed:()=>setState(()=>feedRetry451++),icon:const Icon(Icons.refresh),label:const Text('Tekrar dene')),
                    ]));
                  }
                  if(!p.hasData)return const Padding(padding:EdgeInsets.all(24),child:Center(child:CircularProgressIndicator()));
                  final ds =
                      (p.data?.docs ?? []).where((d) {
                        final a = d.data();
                        return a['text'].toString().toLowerCase().contains(
                              search,
                            ) &&
                            (tab != 'Öne çıkanlar' || a['pinned'] == true) &&
                            (tab != 'Videolar' || a['mediaType'] == 'video') &&
                            (tab != 'Fotoğraflar' || a['mediaType'] == 'image');
                      }).toList()..sort(
                        (a, b) =>
                            ((b.data()['createdAt'] as Timestamp?)
                                        ?.millisecondsSinceEpoch ??
                                    0)
                                .compareTo(
                                  (a.data()['createdAt'] as Timestamp?)
                                          ?.millisecondsSinceEpoch ??
                                      0,
                                ),
                      );
                  return Column(
                    children: [
                      if (ds.isEmpty)
                        const Padding(
                          padding: EdgeInsets.all(24),
                          child: Text('Henüz gönderi yok.'),
                        ),
                      ...ds.map(
                        (d) => NgelXCommunityPost450(
                          communityId: widget.id,
                          id: d.id,
                          value: d.data(),
                          member: member,
                          admin: admin,
                        ),
                      ),
                      if ((p.data?.docs.length ?? 0) >= postLimit)
                        TextButton(
                          onPressed: () => setState(() => postLimit += 40),
                          child: const Text('Daha fazla gönderi'),
                        ),
                    ],
                  );
                },
              ),
          ],
        );
      },
    ),
  );
}

class NgelXCommunityCompose450 extends StatefulWidget {
  final String id;
  final Map<String, dynamic> value;
  const NgelXCommunityCompose450({
    super.key,
    required this.id,
    required this.value,
  });
  @override
  State<NgelXCommunityCompose450> createState() =>
      _NgelXCommunityCompose450State();
}

class _NgelXCommunityCompose450State extends State<NgelXCommunityCompose450> {
  final text = TextEditingController();
  XFile? media;
  String type = '';
  bool busy = false;
  @override
  void dispose() {
    text.dispose();
    super.dispose();
  }

  Future<void> pick(bool video) async {
    final x = video
        ? await ImagePicker().pickVideo(source: ImageSource.gallery)
        : await ImagePicker().pickImage(source: ImageSource.gallery);
    if (x != null && mounted)
      setState(() {
        media = x;
        type = video ? 'video' : 'image';
      });
  }

  Future<void> publish() async {
    if (text.text.trim().isEmpty && media == null) return;
    setState(() => busy = true);
    try {
      final ref = _communities450.doc(widget.id).collection('posts').doc();
      String url = '';
      if (media != null) {
        url = type == 'image'
            ? await ngelxFotografYukle(
                dosya: media!,
                kind: type == 'video' ? 'videos' : 'photos',
                legacyPath: 'communities/${widget.id}/${ref.id}.jpg',
              )
            : await ngelxMedyaYukleDosya(
                dosya: media!,
                kind: type == 'video' ? 'videos' : 'photos',
                ext: 'mp4',
                legacyPath: 'communities/${widget.id}/${ref.id}.mp4',
              );
      }
      final user = await FirebaseFirestore.instance
          .collection('users')
          .doc(_communityUid450)
          .get();
      final u = user.data() ?? {};
      final pending =
          widget.value['postApproval'] == true &&
          !_communityAdmin450(widget.value);
      await ref.set({
        'authorId': _communityUid450,
        'authorName': (u['displayName'] ?? u['username'] ?? 'Üye').toString(),
        'authorPhoto': (u['photoUrl'] ?? '').toString(),
        'text': text.text.trim(),
        'mediaUrl': url,
        'mediaType': type,
        'status': pending ? 'pending' : 'approved',
        'pinned': false,
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              pending
                  ? 'Gönderin yönetici onayına gönderildi.'
                  : 'Gönderin paylaşıldı.',
            ),
          ),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) _communityError450(context, e);
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Toplulukta paylaş',
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        TextField(
          controller: text,
          maxLength: 3000,
          maxLines: 7,
          decoration: const InputDecoration(hintText: 'Bir şey paylaş…'),
        ),
        Wrap(
          spacing: 8,
          children: [
            OutlinedButton.icon(
              onPressed: busy ? null : () => pick(false),
              icon: const Icon(Icons.photo),
              label: Text(_ngelx438Ui("Fotoğraf")),
            ),
            OutlinedButton.icon(
              onPressed: busy ? null : () => pick(true),
              icon: const Icon(Icons.video_library),
              label: Text(_ngelx438Ui("Video")),
            ),
          ],
        ),
        if (media != null)
          ListTile(
            title: Text(media!.name),
            trailing: IconButton(
              onPressed: busy
                  ? null
                  : () => setState(() {
                      media = null;
                      type = '';
                    }),
              icon: const Icon(Icons.close),
            ),
          ),
        if (widget.value['postApproval'] == true &&
            !_communityAdmin450(widget.value))
          const Text('Bu toplulukta gönderiler yönetici onayından geçer.'),
        FilledButton(
          onPressed: busy ? null : publish,
          child: Text(busy ? 'Yükleniyor…' : _ngelx438Ui("Paylaş")),
        ),
      ],
    ),
  );
}

class NgelXCommunityVideo450 extends StatefulWidget {
  final String url;
  const NgelXCommunityVideo450({super.key, required this.url});
  @override
  State<NgelXCommunityVideo450> createState() => _NgelXCommunityVideo450State();
}

class _NgelXCommunityVideo450State extends State<NgelXCommunityVideo450> {
  VideoPlayerController? player;
  bool failed = false;
  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    try {
      final p = VideoPlayerController.networkUrl(Uri.parse(widget.url));
      player = p;
      await p.initialize();
      if (mounted) setState(() {});
    } catch (_) {
      if (mounted) setState(() => failed = true);
    }
  }

  @override
  void dispose() {
    player?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext c) {
    final p = player;
    if (failed)
      return const SizedBox(
        height: 160,
        child: Center(child: Text('Video açılamadı.')),
      );
    if (p == null || !p.value.isInitialized)
      return const SizedBox(
        height: 160,
        child: Center(child: CircularProgressIndicator()),
      );
    return InkWell(
      onTap: () {
        setState(() {
          p.value.isPlaying ? p.pause() : ngelx444MediaPlay(p);
        });
      },
      child: Stack(
        alignment: Alignment.center,
        children: [
          AspectRatio(aspectRatio: p.value.aspectRatio, child: VideoPlayer(p)),
          if (!p.value.isPlaying)
            const Icon(Icons.play_circle_fill, size: 48, color: Colors.white),
        ],
      ),
    );
  }
}

class NgelXCommunityPost450 extends StatelessWidget {
  final String communityId, id;
  final Map<String, dynamic> value;
  final bool member, admin;
  const NgelXCommunityPost450({
    super.key,
    required this.communityId,
    required this.id,
    required this.value,
    required this.member,
    required this.admin,
  });
  DocumentReference<Map<String, dynamic>> get ref =>
      _communities450.doc(communityId).collection('posts').doc(id);
  Future<void> comments(BuildContext c) async {
    final text = TextEditingController();
    await showModalBottomSheet(
      context: c,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      showDragHandle: true,
      builder: (b) => SafeArea(
        child: Padding(
          padding: EdgeInsets.only(bottom: MediaQuery.of(b).viewInsets.bottom),
          child: SizedBox(
            height: MediaQuery.sizeOf(b).height * .65,
            child: Column(
              children: [
                const Text(
                  'Yorumlar',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
                ),
                Expanded(
                  child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                    stream: ref
                        .collection('comments')
                        .orderBy('createdAt')
                        .limit(100)
                        .snapshots(),
                    builder: (b, s) => ListView(
                      children: (s.data?.docs ?? [])
                          .map(
                            (d) => ListTile(
                              title: Text(d.data()['name'] ?? 'Üye'),
                              subtitle: Text(d.data()['text'] ?? ''),
                            ),
                          )
                          .toList(),
                    ),
                  ),
                ),
                if (member)
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: text,
                          maxLength: 500,
                          decoration: const InputDecoration(
                            hintText: 'Yorum yaz…',
                          ),
                        ),
                      ),
                      IconButton(
                        onPressed: () async {
                          final v = text.text.trim();
                          if (v.isEmpty) return;
                          try {
                            await ref.collection('comments').add({
                              'uid': _communityUid450,
                              'name':
                                  FirebaseAuth
                                      .instance
                                      .currentUser
                                      ?.displayName ??
                                  'Üye',
                              'text': v,
                              'createdAt': FieldValue.serverTimestamp(),
                            });
                            text.clear();
                          } catch (e) {
                            if (b.mounted) _communityError450(b, e);
                          }
                        },
                        icon: const Icon(Icons.send, color: mor),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );
    text.dispose();
  }

  @override
  Widget build(BuildContext c) => Container(
    margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.white,
      border: Border.all(color: const Color(0xFFE7E7ED)),
      borderRadius: BorderRadius.circular(18),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            _communityImage450(
              value['authorPhoto'].toString(),
              size: 36,
              circle: true,
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    value['authorName'],
                    style: const TextStyle(fontWeight: FontWeight.w800),
                  ),
                  Text(
                    value['createdAt'] is Timestamp
                        ? (value['createdAt'] as Timestamp)
                              .toDate()
                              .toLocal()
                              .toString()
                              .substring(0, 16)
                        : 'Gönderiliyor…',
                    style: const TextStyle(color: Colors.black54, fontSize: 11),
                  ),
                ],
              ),
            ),
            PopupMenuButton<String>(
              onSelected: (x) async {
                try {
                  if (x == 'delete') {
                    final yes = await showDialog<bool>(
                      context: c,
                      builder: (d) => AlertDialog(
                        title: const Text('Gönderiyi sil?'),
                        actions: [
                          TextButton(
                            onPressed: () => Navigator.pop(d, false),
                            child: const Text('İptal'),
                          ),
                          FilledButton(
                            onPressed: () => Navigator.pop(d, true),
                            child: Text(_ngelx438Ui("Sil")),
                          ),
                        ],
                      ),
                    );
                    if (yes == true) await ref.update({'status': 'deleted'});
                  }
                  if (x == 'pin')
                    await ref.update({'pinned': value['pinned'] != true});
                  if (x == 'report')
                    await _communities450
                        .doc(communityId)
                        .collection('reports')
                        .doc('${id}_$_communityUid450')
                        .set({
                          'uid': _communityUid450,
                          'postId': id,
                          'status': 'open',
                          'createdAt': FieldValue.serverTimestamp(),
                        });
                } catch (e) {
                  if (c.mounted) _communityError450(c, e);
                }
              },
              itemBuilder: (_) => [
                if (member)
                  PopupMenuItem(
                    value: 'report',
                    child: Text(_ngelx438Ui("Şikâyet et")),
                  ),
                if (admin)
                  PopupMenuItem(
                    value: 'pin',
                    child: Text(
                      value['pinned'] == true
                          ? 'Öne çıkarmayı kaldır'
                          : 'Öne çıkar',
                    ),
                  ),
                if (admin || value['authorId'] == _communityUid450)
                  PopupMenuItem(
                    value: 'delete',
                    child: Text(_ngelx438Ui("Sil")),
                  ),
              ],
            ),
          ],
        ),
        const SizedBox(height: 10),
        Text(value['text'] ?? ''),
        if (value['mediaType'] == 'image' && value['mediaUrl'] != '')
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(14),
              child: NgelXAgResmi(
                imageUrl: value['mediaUrl'],
                width: double.infinity,
                height: 230,
                fit: BoxFit.cover,
              ),
            ),
          ),
        if (value['mediaType'] == 'video' && value['mediaUrl'] != '')
          NgelXCommunityVideo450(url: value['mediaUrl']),
        const Divider(),
        Row(
          children: [
            Expanded(
              child: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
                stream: member
                    ? ref.collection('likes').doc(_communityUid450).snapshots()
                    : null,
                builder: (c, s) => TextButton.icon(
                  onPressed: member
                      ? () async {
                          try {
                            final r = ref
                                .collection('likes')
                                .doc(_communityUid450);
                            if (s.data?.exists == true) {
                              await r.delete();
                            } else {
                              await r.set({
                                'uid': _communityUid450,
                                'createdAt': FieldValue.serverTimestamp(),
                              });
                            }
                          } catch (e) {
                            if (c.mounted) _communityError450(c, e);
                          }
                        }
                      : null,
                  icon: Icon(
                    s.data?.exists == true
                        ? Icons.favorite
                        : Icons.favorite_border,
                    color: mor,
                    size: 19,
                  ),
                  label: const Text('Beğen', style: TextStyle(fontSize: 11)),
                ),
              ),
            ),
            Expanded(
              child: TextButton.icon(
                onPressed: () => comments(c),
                icon: const Icon(Icons.chat_bubble_outline, size: 19),
                label: const Text('Yorum yap', style: TextStyle(fontSize: 11)),
              ),
            ),
            Expanded(
              child: TextButton.icon(
                onPressed: () => SharePlus.instance.share(
                  ShareParams(
                    text: '${value['text']}\nNgelX topluluk: $communityId',
                  ),
                ),
                icon: const Icon(Icons.share_outlined, size: 19),
                label: Text(
                  _ngelx438Ui("Paylaş"),
                  style: TextStyle(fontSize: 11),
                ),
              ),
            ),
          ],
        ),
      ],
    ),
  );
}

class NgelXCommunityAdmin450 extends StatefulWidget {
  final String id;
  const NgelXCommunityAdmin450({super.key, required this.id});
  @override
  State<NgelXCommunityAdmin450> createState() => _NgelXCommunityAdmin450State();
}

class _NgelXCommunityAdmin450State extends State<NgelXCommunityAdmin450> {
  String section = 'Üyelik istekleri';
  bool bulkBusy451 = false;
  Future<void> moderateAll451(List<QueryDocumentSnapshot<Map<String,dynamic>>> docs, bool approve) async {
    if (bulkBusy451 || docs.isEmpty) return;
    final membership = section == 'Üyelik istekleri';
    final confirmed = await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
      title:Text(approve?'Toplu onay':'Toplu ret'),
      content:Text('${docs.length} kayda işlem uygulanacak. Devam edilsin mi?'),
      actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('İptal')),
        FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Uygula'))]));
    if(confirmed!=true || !mounted)return;
    setState(()=>bulkBusy451=true);
    try {
      final root = _communities450.doc(widget.id);
      await FirebaseFirestore.instance.runTransaction((tx) async {
        final community = await tx.get(root);
        final current = <DocumentSnapshot<Map<String,dynamic>>>[];
        for(final d in docs)current.add(await tx.get(d.reference));
        final pending=current.where((d)=>d.exists&&d.data()?['status']=='pending').toList();
        if(membership&&approve){
          final members=Set<String>.from(community.data()?['members']??const[]);
          members.addAll(pending.map((d)=>d.id));
          if(members.length>500)throw StateError('Topluluk 500 üye sınırına ulaşıyor. Daha az isteği onayla.');
          if(pending.isNotEmpty)tx.update(root,{'members':FieldValue.arrayUnion(pending.map((d)=>d.id).toList())});
        }
        for(final d in pending)tx.update(d.reference,{'status':approve?'approved':'rejected'});
      });
    }catch(e){if(mounted)_communityError450(context,e);}
    finally{if(mounted)setState(()=>bulkBusy451=false);}
  }

  Future<void> edit450(Map<String, dynamic> v) async {
    final n = TextEditingController(text: v['name']),
        d = TextEditingController(text: v['description']),
        r = TextEditingController(text: v['rules']);
    final save = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Topluluk bilgileri'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: n,
                maxLength: 60,
                decoration: const InputDecoration(labelText: 'Ad'),
              ),
              TextField(
                controller: d,
                maxLength: 240,
                decoration: const InputDecoration(labelText: 'Açıklama'),
              ),
              TextField(
                controller: r,
                maxLength: 2000,
                maxLines: 4,
                decoration: const InputDecoration(labelText: 'Kurallar'),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(c, false),
            child: const Text('İptal'),
          ),
          FilledButton(
            onPressed: n.text.trim().length < 3
                ? null
                : () => Navigator.pop(c, true),
            child: const Text('Kaydet'),
          ),
        ],
      ),
    );
    if (save == true && mounted) {
      try {
        await _communities450.doc(widget.id).update({
          'name': n.text.trim(),
          'description': d.text.trim(),
          'rules': r.text.trim(),
        });
      } catch (e) {
        if (mounted) _communityError450(context, e);
      }
    }
    n.dispose();
    d.dispose();
    r.dispose();
  }

  @override
  Widget build(BuildContext c) => _communitySurface450(
    title: 'Topluluğu yönet',
    body: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: _communities450.doc(widget.id).snapshots(),
      builder: (c, s) {
        final v = s.data?.data();
        if (v == null) return const Center(child: CircularProgressIndicator());
        if (!_communityAdmin450(v))
          return const Center(child: Text('Yönetici yetkisi gerekli.'));
        final root = _communities450.doc(widget.id);
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              v['name'],
              style: const TextStyle(fontSize: 23, fontWeight: FontWeight.w900),
            ),
            Text('${(v['members'] as List).length} üye'),
            Wrap(
              spacing: 6,
              children:
                  [
                        'Üyelik istekleri',
                        'Bekleyen gönderiler',
                        'Şikâyetler',
                        'İstatistikler',
                        'Üyeler',
                        'Ayarlar',
                      ]
                      .map(
                        (x) => ChoiceChip(
                    selectedColor:const Color(0xFFF0E8FF),
                    backgroundColor:Colors.white,
                    checkmarkColor:mor,
                    labelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w700),
                          label: Text(x),
                          selected: section == x,
                          onSelected: (_) => setState(() => section = x),
                        ),
                      )
                      .toList(),
            ),
            if (section == 'İstatistikler') ...[
              ListTile(
                title: const Text('Üyeler'),
                trailing: Text('${(v['members'] as List).length}'),
              ),
              ...[
                ('posts', 'approved', 'Yayımlanan gönderiler'),
                ('posts', 'pending', 'Bekleyen gönderiler'),
                ('requests', 'pending', 'Bekleyen üyelikler'),
                ('reports', 'open', 'Açık şikâyetler'),
              ].map(
                (x) => FutureBuilder<AggregateQuerySnapshot>(
                  future: root
                      .collection(x.$1)
                      .where('status', isEqualTo: x.$2)
                      .count()
                      .get(),
                  builder: (c, s) => ListTile(
                    title: Text(x.$3),
                    trailing: Text(
                      s.hasError ? 'Yüklenemedi' : '${s.data?.count ?? '…'}',
                    ),
                  ),
                ),
              ),
            ],
            if (section == 'Ayarlar') ...[
              SwitchListTile(
                title: const Text('Özel topluluk'),
                subtitle: const Text(
                  'Özel gönderiler yalnızca üyelere görünür.',
                ),
                value: v['visibility'] == 'private',
                onChanged: (x) async {
                  try {
                    await root.update({'visibility': x ? 'private' : 'public'});
                  } catch (e) {
                    if (c.mounted) _communityError450(c, e);
                  }
                },
              ),
              ListTile(
                title: const Text('Ad, açıklama ve kuralları düzenle'),
                trailing: const Icon(Icons.edit),
                onTap: () => edit450(v),
              ),
              SwitchListTile(
                title: const Text('Üyelik onayı'),
                value: v['joinApproval'] == true,
                onChanged: (x) async {
                  try {
                    await root.update({'joinApproval': x});
                  } catch (e) {
                    if (c.mounted) _communityError450(c, e);
                  }
                },
              ),
              SwitchListTile(
                title: const Text('Gönderi onayı'),
                value: v['postApproval'] == true,
                onChanged: (x) async {
                  try {
                    await root.update({'postApproval': x});
                  } catch (e) {
                    if (c.mounted) _communityError450(c, e);
                  }
                },
              ),
              ListTile(
                title: const Text('Kurallar'),
                subtitle: Text(v['rules']),
              ),
            ],
            if (section == 'Üyeler')
              ...List<String>.from(v['members']).map(
                (uid) => ListTile(
                  title: NgelXFounder450(uid: uid, label: 'Üye'),
                  trailing:
                      v['founderId'] == _communityUid450 &&
                          uid != v['founderId']
                      ? PopupMenuButton<String>(
                          onSelected: (a) async {
                            try {
                              if (a == 'admin') {
                                await root.update({
                                  'admins':
                                      List<String>.from(v['admins'])
                                          .contains(uid)
                                      ? FieldValue.arrayRemove([uid])
                                      : FieldValue.arrayUnion([uid]),
                                });
                              }
                              if (a == 'remove')
                                await root.update({
                                  'members': FieldValue.arrayRemove([uid]),
                                  'admins': FieldValue.arrayRemove([uid]),
                                });
                            } catch (e) {
                              if (c.mounted) _communityError450(c, e);
                            }
                          },
                          itemBuilder: (_) => [
                            PopupMenuItem(
                              value: 'admin',
                              child: Text(
                                List<String>.from(v['admins']).contains(uid)
                                    ? 'Yöneticiliği kaldır'
                                    : 'Yönetici yap',
                              ),
                            ),
                            const PopupMenuItem(
                              value: 'remove',
                              child: Text('Üyeyi çıkar'),
                            ),
                          ],
                        )
                      : null,
                ),
              ),
            if ([
              'Üyelik istekleri',
              'Bekleyen gönderiler',
              'Şikâyetler',
            ].contains(section))
              StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                stream: root
                    .collection(
                      section == 'Üyelik istekleri'
                          ? 'requests'
                          : section == 'Bekleyen gönderiler'
                          ? 'posts'
                          : 'reports',
                    )
                    .where(
                      'status',
                      isEqualTo: section == 'Şikâyetler' ? 'open' : 'pending',
                    )
                    .limit(50)
                    .snapshots(),
                builder: (c, q) {
                  if (q.hasError) return const Text('Kayıtlar yüklenemedi.');
                  final ds = q.data?.docs ?? [];
                  return Column(
                    children: [
                      if (ds.isEmpty)
                        const Padding(
                          padding: EdgeInsets.all(24),
                          child: Text('Bekleyen kayıt yok.'),
                        ),
                      if(ds.isNotEmpty&&section!='Şikâyetler')Wrap(spacing:8,children:[
                        FilledButton(onPressed:bulkBusy451?null:()=>moderateAll451(ds,true),child:Text('Tümünü onayla (${ds.length})')),
                        OutlinedButton(onPressed:bulkBusy451?null:()=>moderateAll451(ds,false),child:const Text('Tümünü reddet')),
                      ]),
                      ...ds.map(
                        (d) => Card(
                          color: Colors.white,
                          child: ListTile(
                            title: section == 'Üyelik istekleri'
                                ? NgelXFounder450(uid: d.id, label: 'Başvuran')
                                : Text(
                                    (d.data()['text'] ??
                                            d.data()['postId'] ??
                                            'Şikâyet')
                                        .toString(),
                                  ),
                            subtitle: Row(
                              children: [
                                TextButton(
                                  onPressed: bulkBusy451 ? null : () async {
                                    try {
                                      if (section == 'Üyelik istekleri') {
                                        final batch = FirebaseFirestore.instance
                                            .batch();
                                        batch.update(root, {
                                          'members': FieldValue.arrayUnion([
                                            d.id,
                                          ]),
                                        });
                                        batch.update(d.reference, {
                                          'status': 'approved',
                                        });
                                        await batch.commit();
                                      } else {
                                        await d.reference.update({
                                          'status': section == 'Şikâyetler'
                                              ? 'closed'
                                              : 'approved',
                                        });
                                      }
                                    } catch (e) {
                                      if (c.mounted) _communityError450(c, e);
                                    }
                                  },
                                  child: Text(
                                    section == 'Şikâyetler'
                                        ? 'İncelendi'
                                        : 'Onayla',
                                  ),
                                ),
                                if (section != 'Şikâyetler')
                                  TextButton(
                                    onPressed: bulkBusy451 ? null : () async {
                                      try {
                                        await d.reference.update({
                                          'status': 'rejected',
                                        });
                                      } catch (e) {
                                        if (c.mounted) _communityError450(c, e);
                                      }
                                    },
                                    child: Text(_ngelx438Ui("Reddet")),
                                  ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
          ],
        );
      },
    ),
  );
}

class NgelXDiscoveryTabs450 extends StatelessWidget {
  final int selected;
  final ValueChanged<int> onSelected;
  const NgelXDiscoveryTabs450({
    super.key,
    required this.selected,
    required this.onSelected,
  });
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(horizontal: 12),
    child: Row(
      children: [
        ...[
          (0, 'Canlı'),
          (2, 'Trend'),
          (3, 'Kişiler'),
          (4, 'Gruplar'),
          (5, 'Topluluk'),
        ].map(
          (item) => Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 3),
              child: Semantics(
                button: true,
                selected: selected == item.$1,
                label: item.$2,
                child: InkWell(
                  onTap: () => onSelected(item.$1),
                  borderRadius: BorderRadius.circular(14),
                  child: Container(
                    height: 42,
                    padding: const EdgeInsets.symmetric(horizontal: 3),
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: selected == item.$1
                          ? mor
                          : const Color(0xFFF3F4F7),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(
                        item.$2,
                        style: TextStyle(
                          fontSize: 11.5,
                          fontWeight: FontWeight.w800,
                          color: selected == item.$1
                              ? Colors.white
                              : Colors.black87,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    ),
  );
}
