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

class Ngelx455Comments extends StatefulWidget {
  final DocumentReference<Map<String, dynamic>> post;
  final bool member, admin;
  const Ngelx455Comments({super.key, required this.post,
    required this.member, required this.admin});
  @override State<Ngelx455Comments> createState() => _Ngelx455CommentsState();
}

class _Ngelx455CommentsState extends State<Ngelx455Comments> {
  final input = TextEditingController();
  late final comments = widget.post.collection('comments').orderBy('createdAt').snapshots();
  String replyId = '', replyName = '';
  bool sending = false;
  final expandedReplies = <String>{};
  @override void dispose() { input.dispose(); super.dispose(); }
  Future<void> send() async {
    final body = input.text.trim(), me = _communityUid450;
    if (body.isEmpty || me.isEmpty || sending) return;
    setState(() => sending = true);
    try {
      final user = await FirebaseFirestore.instance.collection('users').doc(me).get();
      if (_communityUid450 != me) return;
      await widget.post.collection('comments').add({
        'uid': me, 'name': ngelx455ProfileName(user.data() ?? {}),
        'photoUrl': (user.data()?['photoUrl'] ?? '').toString(),
        'text': body, 'replyTo': replyId, 'replyName': replyName,
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted) setState(() { input.clear(); replyId = ''; replyName = ''; });
    } catch (e) { if (mounted) _communityError450(context, e); }
    finally { if (mounted) setState(() => sending = false); }
  }
  Widget comment(QueryDocumentSnapshot<Map<String, dynamic>> doc, {int replyCount = 0, bool isReply = false}) {
    final v = doc.data(), uid = (doc.data()['uid'] ?? '').toString();
    final name = (v['name'] ?? 'Üye').toString();
    final timestamp = v['createdAt'];
    final date = timestamp is Timestamp ? timestamp.toDate().toLocal().toString().substring(0, 16) : 'Gönderiliyor…';
    return Padding(padding: EdgeInsets.fromLTRB(isReply ? 48 : 16, 6, 16, 6),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        InkWell(onTap: uid.isEmpty ? null : () => Navigator.push(context,
          MaterialPageRoute(builder: (_) => KullaniciProfilPage(uid: uid))),
          child: _communityImage450((v['photoUrl'] ?? '').toString(), size: 36, circle: true)),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(width: double.infinity, padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: const Color(0xFFF4F3F8), borderRadius: BorderRadius.circular(16)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [Expanded(child: Text(name, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800))),
                if (widget.member && (uid == _communityUid450 || widget.admin))
                  PopupMenuButton<String>(onSelected: (_) async {
                    final yes = await showDialog<bool>(context: context, builder: (c) => AlertDialog(
                      title: const Text('Yorumu sil?'), actions: [
                        TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('Vazgeç')),
                        FilledButton(onPressed: () => Navigator.pop(c, true), child: const Text('Sil'))]));
                    if (yes == true) { try { await doc.reference.delete(); } catch (e) { if (mounted) _communityError450(context, e); } }
                  }, itemBuilder: (_) => [const PopupMenuItem(value: 'delete', child: Text('Sil'))]),
              ]),
              if ((v['replyTo'] ?? '').toString().isNotEmpty)
                Padding(padding: const EdgeInsets.only(bottom: 6), child: Text('${v['replyName'] ?? 'Üye'} kişisine yanıt',
                  style: const TextStyle(fontSize: 12, color: Color(0xFF6744C8)))),
              Text((v['text'] ?? '').toString(), style: const TextStyle(fontSize: 15, height: 1.35)),
            ])),
          Wrap(crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, children: [
            Text(date, style: const TextStyle(fontSize: 11, color: Color(0xFF697386))),
            if (widget.member) TextButton(onPressed: () => setState(() { replyId = isReply ? (v['replyTo'] ?? doc.id).toString() : doc.id; replyName = name; }), child: const Text('Yanıtla')),
            Ngelx455Reactions(ref: doc.reference.collection('reactions'), enabled: widget.member),
            if (replyCount > 0) TextButton(onPressed: () => setState(() {
              expandedReplies.contains(doc.id) ? expandedReplies.remove(doc.id) : expandedReplies.add(doc.id);
            }), child: Text(expandedReplies.contains(doc.id) ? 'Yanıtları gizle' : '$replyCount yanıtı gör')),
          ]),
        ])),
      ]));
  }
  @override Widget build(BuildContext context) => SafeArea(child: Padding(
    padding: EdgeInsets.only(bottom: MediaQuery.viewInsetsOf(context).bottom),
    child: SizedBox(height: MediaQuery.sizeOf(context).height * .72,
      child: Column(children: [
        Expanded(child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(stream: comments, builder: (c, s) {
          if (s.hasError) return const Center(child: Text('Yorumlar yüklenemedi. Yeniden açmayı dene.'));
          if (!s.hasData) return const Center(child: CircularProgressIndicator());
          final docs = s.data!.docs;
          final ids = docs.map((d) => d.id).toSet();
          final roots = docs.where((d) => !ids.contains((d.data()['replyTo'] ?? '').toString())).toList();
          // Replies always target the original root so nested responses remain visible.
          final rows = <Widget>[];
          for (final root in roots) {
            final replies = docs.where((d) => d.data()['replyTo'] == root.id).toList();
            rows.add(comment(root, replyCount: replies.length));
            if (expandedReplies.contains(root.id)) rows.addAll(replies.map((d) => comment(d, isReply: true)));
          }
          return Column(children: [
            Padding(padding: const EdgeInsets.all(12), child: Text('Yorumlar (${docs.length})', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800))),
            Expanded(child: docs.isEmpty ? const Center(child: Text('İlk yorumu sen yaz.')) : ListView(children: rows)),
          ]);
        })),
        if (replyId.isNotEmpty) ListTile(dense: true, title: Text('$replyName kişisine yanıt'), trailing: IconButton(
          onPressed: () => setState(() { replyId = ''; replyName = ''; }), icon: const Icon(Icons.close))),
        if (widget.member) Padding(padding: const EdgeInsets.fromLTRB(16, 8, 12, 12), child: Row(children: [
          Expanded(child: TextField(controller: input, enabled: !sending, minLines: 1, maxLines: 4, maxLength: 500,
            style: const TextStyle(fontSize: 15), decoration: InputDecoration(hintText: 'Yorum yaz…',
              filled: true, fillColor: const Color(0xFFF4F3F8), border: OutlineInputBorder(borderSide: BorderSide.none, borderRadius: BorderRadius.circular(24))))),
          IconButton(onPressed: sending ? null : send, tooltip: 'Yorumu gönder', icon: sending ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.send_rounded, color: mor)),
        ])),
      ]))));
}

class Ngelx455Reactions extends StatefulWidget {
  final CollectionReference<Map<String, dynamic>> ref;
  final bool enabled;
  const Ngelx455Reactions({super.key, required this.ref, required this.enabled});
  @override State<Ngelx455Reactions> createState() => _Ngelx455ReactionsState();
}
class _Ngelx455ReactionsState extends State<Ngelx455Reactions> {
  late Stream<QuerySnapshot<Map<String, dynamic>>> stream = widget.ref.snapshots();
  @override void didUpdateWidget(covariant Ngelx455Reactions oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.ref.path != widget.ref.path) stream = widget.ref.snapshots();
  }
  bool busy = false;
  Future<void> setReaction(String emoji, String selected) async {
    if (busy || !widget.enabled || _communityUid450.isEmpty) return;
    setState(() => busy = true);
    try {
      final doc = widget.ref.doc(_communityUid450);
      if (selected == emoji) { await doc.delete(); }
      else { await doc.set({'uid': _communityUid450, 'emoji': emoji, 'createdAt': FieldValue.serverTimestamp()}); }
    } catch (e) { if (mounted) _communityError450(context, e); }
    finally { if (mounted) setState(() => busy = false); }
  }
  @override Widget build(BuildContext context) => StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(stream: stream, builder: (c, s) {
    final docs = s.data?.docs ?? [], counts = <String, int>{};
    var selected = '';
    for (final doc in docs) { final emoji = (doc.data()['emoji'] ?? '❤️').toString(); counts[emoji] = (counts[emoji] ?? 0) + 1; if (doc.id == _communityUid450) selected = emoji; }
    return InkWell(onTap: !widget.enabled || busy ? null : () => setReaction('❤️', selected),
      onLongPress: !widget.enabled || busy ? null : () async {
        final choice = await showModalBottomSheet<String>(context: context, backgroundColor: Colors.white, builder: (b) => SafeArea(child: Padding(
          padding: const EdgeInsets.all(20), child: Wrap(spacing: 12, children: ['❤️','👍','😂','😮','😢','😡'].map((e) => IconButton(
            onPressed: () => Navigator.pop(b, e), icon: Text(e, style: const TextStyle(fontSize: 26)))).toList()))));
        if (choice != null && mounted) await setReaction(choice, selected);
      }, child: Padding(padding: const EdgeInsets.all(8), child: Text(s.hasError ? 'Tepkiler yüklenemedi' : counts.isEmpty ? '♡ Beğen' : counts.entries.map((e) => '${e.key} ${e.value}').join('  '),
        style: TextStyle(fontSize: 13, color: selected.isEmpty ? const Color(0xFF697386) : mor, fontWeight: FontWeight.w600))));
  });
}

bool ngelx455PostVisible(Rect bounds, Rect viewport) {
  final visible = bounds.intersect(viewport);
  return !visible.isEmpty && visible.height >= bounds.height.clamp(0, viewport.height) * .5;
}

class Ngelx455PostView extends StatefulWidget {
  final DocumentReference<Map<String, dynamic>> ref;
  final Widget child;
  const Ngelx455PostView({super.key, required this.ref, required this.child});
  @override State<Ngelx455PostView> createState() => _Ngelx455PostViewState();
}
class _Ngelx455PostViewState extends State<Ngelx455PostView> {
  Timer? timer;
  DateTime? visibleSince;
  bool recorded = false;
  void schedule() { timer?.cancel(); timer = Timer.periodic(const Duration(milliseconds: 500), (_) => check()); }
  @override void initState() { super.initState(); schedule(); }
  @override void didUpdateWidget(covariant Ngelx455PostView oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.ref.path != oldWidget.ref.path) { recorded = false; visibleSince = null; schedule(); }
  }
  void check() {
    if (!mounted || recorded || FirebaseAuth.instance.currentUser?.isAnonymous != false || _communityUid450.isEmpty) return;
    final box = context.findRenderObject();
    final route = ModalRoute.of(context);
    final lifecycle = WidgetsBinding.instance.lifecycleState;
    if (box is! RenderBox || !box.hasSize || route?.isCurrent != true ||
        (lifecycle != null && lifecycle != AppLifecycleState.resumed)) { visibleSince = null; return; }
    final bounds = box.localToGlobal(Offset.zero) & box.size;
    final screen = MediaQuery.sizeOf(context);
    final viewport = Rect.fromLTWH(0, MediaQuery.paddingOf(context).top + kToolbarHeight,
        screen.width, screen.height - MediaQuery.paddingOf(context).vertical - kToolbarHeight);
    final visible = ngelx455PostVisible(bounds, viewport);
    if (!visible) { visibleSince = null; return; }
    visibleSince ??= DateTime.now();
    if (DateTime.now().difference(visibleSince!).inSeconds < 2) return;
    final me = _communityUid450;
    recorded = true;
    timer?.cancel();
    widget.ref.collection('views').doc(me).set({'uid': me, 'createdAt': FieldValue.serverTimestamp()})
      .catchError((Object _) { if (mounted) { recorded = false; visibleSince = null;
        timer = Timer(const Duration(seconds: 30), () { if (mounted) schedule(); }); } });
  }
  @override void dispose() { timer?.cancel(); super.dispose(); }
  @override Widget build(BuildContext context) => widget.child;
}

class Ngelx455PostCounts extends StatefulWidget {
  final DocumentReference<Map<String, dynamic>> ref;
  const Ngelx455PostCounts({super.key, required this.ref});
  @override State<Ngelx455PostCounts> createState() => _Ngelx455PostCountsState();
}
class _Ngelx455PostCountsState extends State<Ngelx455PostCounts> {
  late Map<String, Stream<QuerySnapshot<Map<String, dynamic>>>> streams = create();
  Map<String, Stream<QuerySnapshot<Map<String, dynamic>>>> create() => {
    for (final key in ['likes','comments','shares','views']) key: widget.ref.collection(key).snapshots(),
  };
  @override void didUpdateWidget(covariant Ngelx455PostCounts oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.ref.path != oldWidget.ref.path) streams = create();
  }
  @override Widget build(BuildContext context) => Padding(padding: const EdgeInsets.only(top: 10),
    child: Wrap(spacing: 14, runSpacing: 6, children: [
      for (final entry in {'likes':'tepki','comments':'yorum','shares':'paylaşan','views':'kişi gördü'}.entries)
        StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(stream: streams[entry.key], builder: (_, s) => Text(
          '${s.hasError ? '—' : s.hasData ? s.data!.size : '…'} ${entry.value}',
          style: const TextStyle(fontSize: 12, color: Color(0xFF697386)))),
    ]));
}

Future<void> ngelx455SharePost(BuildContext context, DocumentReference<Map<String, dynamic>> ref,
    Map<String, dynamic> value) async {
  final me = _communityUid450;
  try {
    final result = await SharePlus.instance.share(ShareParams(
      text: '${value['text'] ?? ''}\n${value['mediaUrl'] ?? ''}\nNgelX gönderi: ${ref.path}'));
    if (result.status == ShareResultStatus.success && FirebaseAuth.instance.currentUser?.isAnonymous == false && me.isNotEmpty && _communityUid450 == me) {
      await ref.collection('shares').doc(me).set({'uid': me, 'createdAt': FieldValue.serverTimestamp()});
    }
  } catch (e) { if (context.mounted) _communityError450(context, e); }
}
