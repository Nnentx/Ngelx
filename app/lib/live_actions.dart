import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dio/dio.dart';
import 'package:livekit_client/livekit_client.dart' as lk;

class LiveApi {
  static const endpoint = String.fromEnvironment('NGELX_LIVE_API_URL');
  static Future<Map<String, dynamic>> call(String action, Map<String, dynamic> data) async {
    if (endpoint.isEmpty) throw Exception('Canlı yayın sunucusu henüz yapılandırılmadı.');
    final uri = Uri.parse(endpoint);
    if (uri.scheme != 'https' || uri.host.isEmpty) throw Exception('Canlı yayın sunucu adresi geçersiz.');
    final token = await FirebaseAuth.instance.currentUser?.getIdToken();
    if (token == null) throw Exception('Oturum açmalısın.');
    try {
      final response = await Dio(BaseOptions(connectTimeout: const Duration(seconds: 15), receiveTimeout: const Duration(seconds: 30)))
          .post('${endpoint.replaceFirst(RegExp(r'/+$'), '')}/$action', data: data, options: Options(headers: {'Authorization': 'Bearer $token'}));
      return Map<String, dynamic>.from(response.data as Map);
    } on DioException catch (e) {
      throw Exception(e.response?.data is Map ? e.response!.data['message'] : 'Sunucuya ulaşılamadı. Tekrar dene.');
    }
  }
}

class LiveActions extends StatefulWidget {
  final String streamId;
  final lk.Room room;
  const LiveActions({super.key, required this.streamId, required this.room});
  @override
  State<LiveActions> createState() => _LiveActionsState();
}

class _LiveActionsState extends State<LiveActions> {
  bool busy = false;
  bool publishing = false;
  StreamSubscription<DocumentSnapshot<Map<String, dynamic>>>? subscription;
  String get uid => FirebaseAuth.instance.currentUser?.uid ?? '';
  DocumentReference<Map<String, dynamic>> get ref => FirebaseFirestore.instance.collection('live_streams').doc(widget.streamId);
  @override
  void initState() {
    super.initState();
    subscription = ref.snapshots().listen((snapshot) async {
      final data = snapshot.data();
      if (data == null || data['active'] != true || data['guestUid'] != uid || publishing) return;
      publishing = true;
      try {
        await LiveApi.call('publish', {'streamId': widget.streamId});
        if (!mounted) return;
        await widget.room.localParticipant?.setCameraEnabled(true);
        await widget.room.localParticipant?.setMicrophoneEnabled(true);
      } catch (e) {
        publishing = false;
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e')));
      }
    });
  }
  @override
  void dispose() { subscription?.cancel(); super.dispose(); }
  Future<void> run(String action, [Map<String, dynamic> extra = const {}]) async {
    if (busy) return;
    setState(() => busy = true);
    try { await LiveApi.call(action, {'streamId': widget.streamId, ...extra}); }
    catch (e) { if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e'))); }
    finally { if (mounted) setState(() => busy = false); }
  }
  Future<void> requests() async {
    await showModalBottomSheet<void>(context: context, isScrollControlled: true, backgroundColor: Colors.white, builder: (sheet) => SafeArea(child: SizedBox(height: 360, child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: ref.collection('join_requests').where('status', isEqualTo: 'pending').snapshots(),
      builder: (_, snapshot) {
        if (snapshot.hasError) return const Center(child: Text('İstekler yüklenemedi.'));
        final docs = snapshot.data?.docs ?? [];
        if (docs.isEmpty) return const Center(child: Text('Bekleyen katılım isteği yok.'));
        return ListView(children: [const ListTile(title: Text('Katılım istekleri')), ...docs.map((d) => ListTile(title: Text('${d.data()['name']}'), trailing: Row(mainAxisSize: MainAxisSize.min, children: [
          IconButton(tooltip: 'Reddet', icon: const Icon(Icons.close), onPressed: () { Navigator.pop(sheet); run('reject', {'targetUid': d.id}); }),
          IconButton(tooltip: 'Kabul et', icon: const Icon(Icons.check), onPressed: () { Navigator.pop(sheet); run('approve', {'targetUid': d.id}); }),
        ])))]);
      },
    ))));
  }
  Future<void> invite() async {
    final controller = TextEditingController();
    final target = await showDialog<String>(context: context, builder: (dialog) => AlertDialog(title: const Text('Yayına davet et'), content: TextField(controller: controller, decoration: const InputDecoration(labelText: 'Kullanıcı adı')), actions: [TextButton(onPressed: () => Navigator.pop(dialog), child: const Text('Vazgeç')), FilledButton(onPressed: () => Navigator.pop(dialog, controller.text.trim()), child: const Text('Davet et'))]));
    controller.dispose();
    if (target == null || target.isEmpty || !mounted || busy) return;
    setState(() => busy = true);
    try {
      final users = await FirebaseFirestore.instance.collection('users').where('username', isEqualTo: target.replaceFirst('@', '')).limit(2).get();
      if (users.docs.length != 1) throw Exception('Kullanıcı bulunamadı veya kullanıcı adı benzersiz değil.');
      await LiveApi.call('invite', {'streamId': widget.streamId, 'targetUid': users.docs.single.id});
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Davet gönderildi.')));
    } catch (e) { if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e'))); }
    finally { if (mounted) setState(() => busy = false); }
  }
  Future<void> gift(Map<String, dynamic> stream) async {
    try {
      final catalog = await LiveApi.call('catalog', {});
      if (!mounted) return;
      await showModalBottomSheet<void>(context: context, backgroundColor: Colors.white, isScrollControlled: true, builder: (sheet) => _GiftSheet(streamId: widget.streamId, stream: stream, gifts: Map<String, dynamic>.from(catalog['gifts'] as Map)));
    } catch (e) { if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e'))); }
  }
  @override
  Widget build(BuildContext context) => StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(stream: ref.snapshots(), builder: (_, snapshot) {
    final data = snapshot.data?.data() ?? <String, dynamic>{};
    if (data['backendVersion'] != 1) return const SizedBox.shrink();
    if (data['active'] != true) return const Text('Yayın sona erdi.');
    final host = data['ownerId'] == uid, guest = data['guestUid'] == uid;
    final pk = Map<String, dynamic>.from(data['pk'] as Map? ?? {});
    return Column(mainAxisSize: MainAxisSize.min, children: [
      if (pk.isNotEmpty) _PkStatus(pk: pk, streamId: widget.streamId),
      if (guest && pk['status'] == 'pending') Wrap(children: [TextButton(onPressed: busy ? null : () => run('pk-accept'), child: const Text('PK kabul et')), TextButton(onPressed: busy ? null : () => run('pk-reject'), child: const Text('Reddet'))]),
      if (!host && !guest) StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(stream: ref.collection('join_requests').doc(uid).snapshots(), builder: (_, request) {
        final status = request.data?.data()?['status'];
        if (status == 'invited') return Wrap(children: [TextButton(onPressed: busy ? null : () => run('accept'), child: const Text('Davet kabul et')), TextButton(onPressed: busy ? null : () => run('reject'), child: const Text('Reddet'))]);
        return TextButton(onPressed: busy ? null : () => run(status == 'pending' ? 'reject' : 'request'), child: Text(status == 'pending' ? 'İsteği iptal et' : 'Yayına katıl'));
      }),
      Wrap(alignment: WrapAlignment.center, spacing: 8, children: [
        if (host) ...[TextButton(onPressed: busy ? null : requests, child: const Text('İstekler')), TextButton(onPressed: busy ? null : invite, child: const Text('Davet et')),
          PopupMenuButton<int>(enabled: !busy && '${data['guestUid'] ?? ''}'.isNotEmpty && !['active', 'pending'].contains(pk['status']), onSelected: (s) => run('pk-propose', {'seconds': s}), itemBuilder: (_) => [60,180,300].map((s) => PopupMenuItem(value: s, child: Text('${s ~/ 60} dakika PK'))).toList(), child: const Padding(padding: EdgeInsets.all(12), child: Text('PK')))],
        if (!host || '${data['guestUid'] ?? ''}'.isNotEmpty) TextButton.icon(onPressed: busy ? null : () => gift(data), icon: const Icon(Icons.card_giftcard), label: const Text('Hediye')),
      ]),
      if (busy) const LinearProgressIndicator(),
    ]);
  });
}

class _PkStatus extends StatefulWidget {
  final Map<String, dynamic> pk;
  final String streamId;
  const _PkStatus({required this.pk, required this.streamId});
  @override
  State<_PkStatus> createState() => _PkStatusState();
}
class _PkStatusState extends State<_PkStatus> {
  Timer? timer;
  bool finalizing = false;
  DateTime? lastAttempt;
  String? attemptedPk;
  Future<void> finalize() async {
    if (finalizing || widget.pk['status'] != 'active') return;
    final endsAt = (widget.pk['endsAtMs'] as num?)?.toInt();
    final now = DateTime.now();
    if (endsAt == null || endsAt > now.millisecondsSinceEpoch) return;
    final id = '${widget.pk['id']}';
    if (attemptedPk == id && lastAttempt != null && now.difference(lastAttempt!).inSeconds < 5) return;
    finalizing = true;
    attemptedPk = id;
    lastAttempt = now;
    try { await LiveApi.call('pk-finish', {'streamId': widget.streamId}); }
    catch (_) { /* The server scheduler also finalizes expired matches. */ }
    finally { finalizing = false; }
  }
  @override
  void initState() { super.initState(); timer = Timer.periodic(const Duration(seconds: 1), (_) { if (mounted && widget.pk['status'] == 'active') { setState(() {}); unawaited(finalize()); } }); }
  @override
  void dispose() { timer?.cancel(); super.dispose(); }
  @override
  Widget build(BuildContext context) {
    final pk = widget.pk;
    final left = (((pk['endsAtMs'] as num?)?.toInt() ?? 0) - DateTime.now().millisecondsSinceEpoch) ~/ 1000;
    final label = pk['status'] == 'pending' ? 'PK daveti bekleniyor' : pk['status'] == 'active' ? (left > 0 ? '${left ~/ 60}:${(left % 60).toString().padLeft(2, '0')}' : 'Süre bitti') : pk['status'] == 'ended' ? (pk['result'] == 'draw' ? 'Berabere' : pk['result'] == 'host' ? 'Yayıncı kazandı' : 'Konuk kazandı') : 'PK iptal edildi';
    return Padding(padding: const EdgeInsets.all(8), child: Text('PK  ${pk['hostScore'] ?? 0} — ${pk['guestScore'] ?? 0}  •  $label', style: const TextStyle(color: Colors.deepPurple, fontWeight: FontWeight.bold)));
  }
}

class _GiftSheet extends StatefulWidget {
  final String streamId;
  final Map<String, dynamic> stream, gifts;
  const _GiftSheet({required this.streamId, required this.stream, required this.gifts});
  @override
  State<_GiftSheet> createState() => _GiftSheetState();
}
class _GiftSheetState extends State<_GiftSheet> {
  String? recipient, selected, requestId;
  bool sending = false;
  int quantity = 1;
  @override
  Widget build(BuildContext context) {
    final uid = FirebaseAuth.instance.currentUser?.uid ?? '';
    final targets = <String, String>{'${widget.stream['ownerId']}': '${widget.stream['username'] ?? 'Yayıncı'}', if ('${widget.stream['guestUid'] ?? ''}'.isNotEmpty) '${widget.stream['guestUid']}': '${widget.stream['guestName'] ?? 'Konuk'}'}..remove(uid);
    return SafeArea(child: SingleChildScrollView(child: Padding(padding: const EdgeInsets.all(20), child: Column(mainAxisSize: MainAxisSize.min, children: [
      const Text('Hediye gönder', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(stream: FirebaseFirestore.instance.collection('wallets').doc(uid).snapshots(), builder: (_, s) => Text('Bakiye: ${s.data?.data()?['coins'] ?? 0} jeton')),
      const Text('Jeton yükleme henüz açık değil.'),
      DropdownButton<String>(value: recipient, hint: const Text('Hediye alıcısı'), items: targets.entries.map((e) => DropdownMenuItem(value: e.key, child: Text(e.value))).toList(), onChanged: sending || requestId != null ? null : (v) => setState(() => recipient = v)),
      Wrap(spacing: 8, children: widget.gifts.entries.map((e) { final gift = Map<String, dynamic>.from(e.value as Map); return ChoiceChip(label: Text('${gift['emoji']} ${gift['name']} • ${gift['coins']}'), selected: selected == e.key, onSelected: sending || requestId != null ? null : (_) => setState(() => selected = e.key)); }).toList()),
      DropdownButton<int>(value: quantity, items: [1,5,10].map((n) => DropdownMenuItem(value: n, child: Text('$n adet'))).toList(), onChanged: sending || requestId != null ? null : (n) => setState(() => quantity = n!)),
      FilledButton(onPressed: sending || recipient == null || selected == null ? null : () async {
        setState(() => sending = true);
        requestId ??= FirebaseFirestore.instance.collection('live_streams').doc().id;
        try {
          await LiveApi.call('gift', {'streamId': widget.streamId, 'targetUid': recipient, 'giftId': selected, 'quantity': quantity, 'requestId': requestId});
          if (context.mounted) Navigator.pop(context);
        } catch (e) { if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e'))); }
        finally { if (mounted) setState(() => sending = false); }
      }, child: Text(sending ? 'Gönderiliyor…' : requestId != null ? 'Aynı gönderimi tekrar dene' : 'Gönder')),
    ]))));
  }
}
