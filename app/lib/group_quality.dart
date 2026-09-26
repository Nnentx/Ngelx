import 'dart:async';
import 'dart:convert';

import 'package:cached_network_image/cached_network_image.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

const _groupGreen = Color(0xFF0A8F45);
const _groupGreenSoft = Color(0xFFE4F6EA);
const _ink = Color(0xFF202124);
const _muted = Color(0xFF777B80);

Future<String> ngelxCurrentDisplayName() async {
  final uid = FirebaseAuth.instance.currentUser?.uid;
  if (uid == null) return 'NgelX kullanıcısı';
  try {
    final snap = await FirebaseFirestore.instance.collection('users').doc(uid).get();
    final data = snap.data() ?? <String, dynamic>{};
    final display = (data['displayName'] ?? '').toString().trim();
    if (display.isNotEmpty) return display;
    final username = (data['username'] ?? '').toString().trim();
    if (username.isNotEmpty) return username;
  } catch (_) {}
  return 'NgelX kullanıcısı';
}

bool ngelxPresenceOnline(
  Map<String, dynamic> data, {
  Duration maxAge = const Duration(seconds: 100),
}) {
  if (data['isOnline'] != true && data['online'] != true) return false;
  final last = data['lastSeenAt'];
  if (last is! Timestamp) return false;
  final age = DateTime.now().difference(last.toDate());
  return !age.isNegative && age <= maxAge;
}

Future<bool> ngelxCanManageGroup(String chatId, [String? explicitUid]) async {
  final uid = explicitUid ?? FirebaseAuth.instance.currentUser?.uid;
  if (uid == null) return false;
  try {
    final snap = await FirebaseFirestore.instance.collection('chats').doc(chatId).get();
    final data = snap.data() ?? <String, dynamic>{};
    final admins = List<String>.from(data['admins'] ?? const <String>[]);
    final owner = (data['createdBy'] ?? '').toString();
    return owner == uid || admins.contains(uid);
  } catch (_) {
    return false;
  }
}


DocumentReference<Map<String, dynamic>> ngelxGroupArchiveRef(String uid, String chatId) =>
    FirebaseFirestore.instance.collection('group_archives').doc(uid).collection('items').doc(chatId);

Future<void> ngelxRecordGroupArchive({
  required String chatId,
  required String targetUid,
  required String exitType,
  required String actorUid,
  required String actorName,
  required String groupName,
  required String groupPhotoUrl,
}) async {
  await ngelxGroupArchiveRef(targetUid, chatId).set(<String, dynamic>{
    'chatId': chatId,
    'targetUid': targetUid,
    'exitType': exitType,
    'actorUid': actorUid,
    'actorName': actorName,
    'groupName': groupName,
    'groupPhotoUrl': groupPhotoUrl,
    'archivedAt': FieldValue.serverTimestamp(),
    'updatedAt': FieldValue.serverTimestamp(),
  }, SetOptions(merge: true));
}

Future<void> ngelxClearGroupArchive(String uid, String chatId) async {
  try {
    await ngelxGroupArchiveRef(uid, chatId).delete();
  } catch (_) {}
}

Future<void> ngelxMarkGroupMessagesSeen({
  required String chatId,
  required List<QueryDocumentSnapshot<Map<String, dynamic>>> docs,
  required String uid,
  required bool shareReadReceipt,
}) async {
  if (docs.isEmpty) return;
  final batch = FirebaseFirestore.instance.batch();
  var changed = 0;
  for (final d in docs.reversed.take(30)) {
    final v = d.data();
    if ((v['senderId'] ?? '').toString() == uid) continue;
    if ((v['type'] ?? '').toString() == 'system') continue;
    final delivered = List<String>.from(v['deliveredTo'] ?? const <String>[]);
    final seen = List<String>.from(v['seenBy'] ?? const <String>[]);
    final needsDelivered = !delivered.contains(uid);
    final needsSeen = shareReadReceipt && !seen.contains(uid);
    if (!needsDelivered && !needsSeen) continue;
    batch.set(d.reference, <String, dynamic>{
      if (needsDelivered) 'deliveredTo': FieldValue.arrayUnion(<String>[uid]),
      if (needsSeen) 'seenBy': FieldValue.arrayUnion(<String>[uid]),
    }, SetOptions(merge: true));
    changed++;
  }
  if (changed > 0) await batch.commit();
}

class GroupDraftStore {
  static final Map<String, Timer> _timers = <String, Timer>{};

  static String _legacyKey(String chatId) => 'group_draft_' + chatId;
  static String _key(String chatId) {
    final uid = FirebaseAuth.instance.currentUser?.uid ?? 'guest';
    return 'group_draft_' + uid + '_' + chatId;
  }

  static Future<String> load(String chatId) async {
    final h = await SharedPreferences.getInstance();
    // Eski sürümlerde taslak anahtarı hesaptan bağımsızdı. Hesap değişiminde
    // başka kullanıcının taslağının görünmesini önlemek için eski anahtarı
    // bilinçli olarak taşımıyor, temizliyoruz.
    await h.remove(_legacyKey(chatId));
    return h.getString(_key(chatId)) ?? '';
  }

  static void schedule(String chatId, String text) {
    // UID ve saklama anahtarını şimdi yakala. Kullanıcı timer çalışmadan önce
    // hesap değiştirirse eski hesabın metni yeni hesaba yazılmasın.
    final key = _key(chatId);
    _timers.remove(key)?.cancel();
    _timers[key] = Timer(const Duration(milliseconds: 450), () async {
      final h = await SharedPreferences.getInstance();
      if (text.trim().isEmpty) {
        await h.remove(key);
      } else {
        await h.setString(key, text);
      }
      _timers.remove(key);
    });
  }

  static Future<void> clear(String chatId) async {
    final key = _key(chatId);
    _timers.remove(key)?.cancel();
    final h = await SharedPreferences.getInstance();
    await h.remove(key);
  }
}

class PrivateDraftStore {
  static final Map<String, Timer> _timers = <String, Timer>{};

  static String _legacyKey(String chatId) => 'private_draft_' + chatId;
  static String _key(String chatId) {
    final uid = FirebaseAuth.instance.currentUser?.uid ?? 'guest';
    return 'private_draft_' + uid + '_' + chatId;
  }

  static Future<String> load(String chatId) async {
    final h = await SharedPreferences.getInstance();
    // Özel sohbet taslakları cihaz genelinde değil, hesap + sohbet bazında
    // saklanır. Eski ortak anahtar güvenli biçimde silinir.
    await h.remove(_legacyKey(chatId));
    return h.getString(_key(chatId)) ?? '';
  }

  static void schedule(String chatId, String text) {
    // UID ve saklama anahtarını şimdi yakala. Kullanıcı timer çalışmadan önce
    // hesap değiştirirse eski hesabın metni yeni hesaba yazılmasın.
    final key = _key(chatId);
    _timers.remove(key)?.cancel();
    _timers[key] = Timer(const Duration(milliseconds: 450), () async {
      final h = await SharedPreferences.getInstance();
      if (text.trim().isEmpty) {
        await h.remove(key);
      } else {
        await h.setString(key, text);
      }
      _timers.remove(key);
    });
  }

  static Future<void> clear(String chatId) async {
    final key = _key(chatId);
    _timers.remove(key)?.cancel();
    final h = await SharedPreferences.getInstance();
    await h.remove(key);
  }
}

class GroupOfflineQueue {
  static String _legacyKey(String chatId) => 'group_pending_' + chatId;
  static String _key(String chatId, [String? explicitUid]) {
    final uid = explicitUid ?? FirebaseAuth.instance.currentUser?.uid ?? 'guest';
    return 'group_pending_' + uid + '_' + chatId;
  }

  static Future<void> _dropLegacy(String chatId) async {
    final h = await SharedPreferences.getInstance();
    await h.remove(_legacyKey(chatId));
  }

  static Future<void> enqueue({
    required String chatId,
    required String id,
    required Map<String, dynamic> payload,
    required String lastMessage,
  }) async {
    await _dropLegacy(chatId);
    final h = await SharedPreferences.getInstance();
    final current = h.getStringList(_key(chatId)) ?? <String>[];
    final filtered = <String>[];
    for (final raw in current) {
      try {
        final m = Map<String, dynamic>.from(jsonDecode(raw) as Map);
        if ((m['id'] ?? '').toString() != id) filtered.add(raw);
      } catch (_) {}
    }
    filtered.add(jsonEncode(<String, dynamic>{
      'id': id,
      'payload': payload,
      'lastMessage': lastMessage,
      'createdAt': DateTime.now().toIso8601String(),
    }));
    await h.setStringList(_key(chatId), filtered.length > 40 ? filtered.sublist(filtered.length - 40) : filtered);
  }

  static Future<void> remove(String chatId, String id) async {
    await _dropLegacy(chatId);
    final h = await SharedPreferences.getInstance();
    final current = h.getStringList(_key(chatId)) ?? <String>[];
    final kept = <String>[];
    for (final raw in current) {
      try {
        final m = Map<String, dynamic>.from(jsonDecode(raw) as Map);
        if ((m['id'] ?? '').toString() != id) kept.add(raw);
      } catch (_) {}
    }
    if (kept.isEmpty) {
      await h.remove(_key(chatId));
    } else {
      await h.setStringList(_key(chatId), kept);
    }
  }

  static Future<void> _removeFor(String chatId, String id, String uid) async {
    final h = await SharedPreferences.getInstance();
    final key = _key(chatId, uid);
    final current = h.getStringList(key) ?? <String>[];
    final kept = <String>[];
    for (final raw in current) {
      try {
        final m = Map<String, dynamic>.from(jsonDecode(raw) as Map);
        if ((m['id'] ?? '').toString() != id) kept.add(raw);
      } catch (_) {}
    }
    if (kept.isEmpty) {
      await h.remove(key);
    } else {
      await h.setStringList(key, kept);
    }
  }

  static Future<int> pendingCount(String chatId) async {
    await _dropLegacy(chatId);
    final h = await SharedPreferences.getInstance();
    return (h.getStringList(_key(chatId)) ?? <String>[]).length;
  }

  static Future<int> flush({
    required String chatId,
    required String senderUid,
    Future<bool> Function(String id, Map<String,dynamic> payload, String lastMessage)? sender,
  }) async {
    await _dropLegacy(chatId);
    final h = await SharedPreferences.getInstance();
    final rawItems = h.getStringList(_key(chatId, senderUid)) ?? <String>[];
    if (rawItems.isEmpty) return 0;

    final chatRef = FirebaseFirestore.instance.collection('chats').doc(chatId);
    final chat = await chatRef.get();
    final data = chat.data() ?? <String, dynamic>{};
    final members = List<String>.from(data['members'] ?? const <String>[]);
    final admins = List<String>.from(data['admins'] ?? const <String>[]);
    final owner = (data['createdBy'] ?? '').toString();
    final canManage = owner == senderUid || admins.contains(senderUid);
    if (!members.contains(senderUid)) return 0;
    if (data['onlyAdminsCanPost'] == true && !canManage) return 0;

    var sent = 0;
    for (final raw in rawItems.take(12)) {
      Map<String, dynamic> item;
      try {
        item = Map<String, dynamic>.from(jsonDecode(raw) as Map);
      } catch (_) {
        continue;
      }
      final id = (item['id'] ?? '').toString();
      final payloadRaw = item['payload'];
      if (id.isEmpty || payloadRaw is! Map) continue;
      final payload = Map<String, dynamic>.from(payloadRaw);
      final lastMessage=(item['lastMessage'] ?? payload['text'] ?? 'Mesaj').toString();

      if(sender!=null){
        final ok=await sender(id,payload,lastMessage);
        if(ok){
          await _removeFor(chatId, id, senderUid);
          sent++;
          continue;
        }
        break;
      }

      final messageRef = chatRef.collection('messages').doc(id);

      try {
        final existing = await messageRef.get();
        if (existing.exists) {
          await _removeFor(chatId, id, senderUid);
          sent++;
          continue;
        }
      } catch (_) {
        break;
      }

      final batch = FirebaseFirestore.instance.batch();
      batch.set(messageRef, <String, dynamic>{
        'senderId': senderUid,
        'createdAt': FieldValue.serverTimestamp(),
        'clientCreatedAt': Timestamp.now(),
        ...payload,
      });
      final chatUpdate = <String, dynamic>{
        'lastMessage': lastMessage,
        'updatedAt': FieldValue.serverTimestamp(),
        'hiddenFor': FieldValue.arrayRemove(members),
      };
      for (final member in members) {
        if (member != senderUid) chatUpdate['unread_' + member] = FieldValue.increment(1);
      }
      batch.set(chatRef, chatUpdate, SetOptions(merge: true));
      try {
        await batch.commit().timeout(const Duration(seconds: 12));
        await _removeFor(chatId, id, senderUid);
        sent++;
      } catch (_) {
        break;
      }
    }
    return sent;
  }
}

Future<Map<String, String>> fetchGroupLinkPreview(String text) async {
  final match = RegExp(r'https?://[^\s]+', caseSensitive: false).firstMatch(text);
  if (match == null) return <String, String>{};
  final raw = match.group(0)!.replaceAll(RegExp(r'[),.!?]+$'), '');
  final uri = Uri.tryParse(raw);
  if (uri == null) return <String, String>{};

  String clean(String value) => value
      .replaceAll(RegExp(r'<[^>]+>'), ' ')
      .replaceAll('&amp;', '&')
      .replaceAll('&quot;', '"')
      .replaceAll('&#39;', "'")
      .replaceAll(RegExp(r'\s+'), ' ')
      .trim();

  try {
    final response = await Dio(BaseOptions(
      connectTimeout: const Duration(seconds: 3),
      receiveTimeout: const Duration(seconds: 3),
      responseType: ResponseType.plain,
      validateStatus: (s) => s != null && s < 500,
      headers: const <String, dynamic>{'User-Agent': 'NgelX/1.0'},
    )).getUri(uri);
    final html = response.data?.toString() ?? '';

    String meta(String key) {
      final escaped = RegExp.escape(key);
      final first = RegExp(
        '<meta[^>]+(?:property|name)=["\\\']' + escaped + '["\\\'][^>]+content=["\\\']([^"\\\']+)["\\\']',
        caseSensitive: false,
      ).firstMatch(html);
      final second = RegExp(
        '<meta[^>]+content=["\\\']([^"\\\']+)["\\\'][^>]+(?:property|name)=["\\\']' + escaped + '["\\\']',
        caseSensitive: false,
      ).firstMatch(html);
      return clean(first?.group(1) ?? second?.group(1) ?? '');
    }

    final titleMeta = meta('og:title');
    final titleTag = clean(
      RegExp(r'<title[^>]*>(.*?)</title>', caseSensitive: false, dotAll: true)
              .firstMatch(html)
              ?.group(1) ??
          '',
    );
    final description = meta('og:description').isNotEmpty ? meta('og:description') : meta('description');
    var image = meta('og:image');
    if (image.isNotEmpty) {
      final imageUri = Uri.tryParse(image);
      if (imageUri != null && !imageUri.hasScheme) image = uri.resolveUri(imageUri).toString();
    }

    return <String, String>{
      'linkUrl': raw,
      'linkHost': uri.host.replaceFirst('www.', ''),
      if ((titleMeta.isNotEmpty ? titleMeta : titleTag).isNotEmpty)
        'linkTitle': titleMeta.isNotEmpty ? titleMeta : titleTag,
      if (description.isNotEmpty) 'linkDescription': description,
      if (image.isNotEmpty) 'linkImage': image,
    };
  } catch (_) {
    return <String, String>{
      'linkUrl': raw,
      'linkHost': uri.host.replaceFirst('www.', ''),
    };
  }
}

Future<String?> showGroupStickerPicker(BuildContext context) {
  const stickers = <String>[
    '😂','😍','🥳','😎','😭','😡','🤯','🥹',
    '❤️','🔥','👏','👍','🙏','💯','🎉','✨',
    '🐥','🐱','🐶','🦁','🌈','⭐','🚀','🎁',
  ];
  return showModalBottomSheet<String>(
    context: context,
    backgroundColor: Colors.white,
    showDragHandle: true,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
    builder: (c) => SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 22),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Çıkartmalar', style: TextStyle(color: _ink, fontSize: 20, fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          const Text('Bir çıkartma seç ve sohbete gönder.', style: TextStyle(color: _muted, fontSize: 12)),
          const SizedBox(height: 14),
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 6,
            mainAxisSpacing: 8,
            crossAxisSpacing: 8,
            children: [
              for (final sticker in stickers)
                InkWell(
                  onTap: () => Navigator.pop(c, sticker),
                  borderRadius: BorderRadius.circular(16),
                  child: Container(
                    alignment: Alignment.center,
                    decoration: BoxDecoration(color: _groupGreenSoft, borderRadius: BorderRadius.circular(16)),
                    child: Text(sticker, style: const TextStyle(fontSize: 30)),
                  ),
                ),
            ],
          ),
        ]),
      ),
    ),
  );
}

Future<void> showGroupMessageInfo({
  required BuildContext context,
  required DocumentReference<Map<String, dynamic>> chatRef,
  required Map<String, dynamic> message,
  required String currentUid,
}) async {
  final createdRaw = message['createdAt'] ?? message['clientCreatedAt'];
  final created = createdRaw is Timestamp ? createdRaw.toDate() : null;
  final chat = await chatRef.get();
  final data = chat.data() ?? <String, dynamic>{};
  final members = List<String>.from(data['members'] ?? const <String>[]);
  final deliveredIds = <String>[];
  final seenIds = <String>[];
  final directDelivered = List<String>.from(message['deliveredTo'] ?? const <String>[]);
  final directSeen = List<String>.from(message['seenBy'] ?? const <String>[]);

  if (directDelivered.isNotEmpty || directSeen.isNotEmpty) {
    for (final id in <String>{...directDelivered, ...directSeen}) {
      if (id == currentUid) continue;
      if (directSeen.contains(id)) {
        seenIds.add(id);
      } else {
        deliveredIds.add(id);
      }
    }
  } else if (created != null) {
    for (final id in members) {
      if (id == currentUid) continue;
      final delivered = data['lastDeliveredAt_' + id];
      if (delivered is Timestamp && !delivered.toDate().isBefore(created)) {
        deliveredIds.add(id);
      }
      if (data['readReceipts_' + id] == false) continue;
      final read = data['lastReadAt_' + id];
      if (read is Timestamp && !read.toDate().isBefore(created)) {
        seenIds.add(id);
      }
    }
  }

  final deliveredOnlyIds = deliveredIds.where((id) => !seenIds.contains(id)).toList();

  String timeText(Object? raw) {
    if (raw is! Timestamp) return '';
    final local = raw.toDate().toLocal();
    final today = DateTime.now();
    final sameDay = local.year == today.year && local.month == today.month && local.day == today.day;
    final hh = local.hour.toString().padLeft(2, '0');
    final mm = local.minute.toString().padLeft(2, '0');
    if (sameDay) return 'Bugün ' + hh + ':' + mm;
    final dd = local.day.toString().padLeft(2, '0');
    final mo = local.month.toString().padLeft(2, '0');
    return dd + '.' + mo + '.' + local.year.toString() + ' ' + hh + ':' + mm;
  }

  Widget personRow(String id, {required bool seen}) {
    final rawTime = data[(seen ? 'lastReadAt_' : 'lastDeliveredAt_') + id];
    final statusTime = timeText(rawTime);
    return FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      future: FirebaseFirestore.instance.collection('users').doc(id).get(),
      builder: (_, snap) {
        final user = snap.data?.data() ?? <String, dynamic>{};
        final name = (user['displayName'] ?? user['username'] ?? 'Grup üyesi').toString();
        final username = (user['username'] ?? '').toString().trim();
        final photo = (user['photoUrl'] ?? '').toString();
        return ListTile(
          dense: true,
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
          leading: CircleAvatar(
            radius: 20,
            backgroundColor: _groupGreenSoft,
            backgroundImage: photo.isEmpty ? null : CachedNetworkImageProvider(photo),
            child: photo.isEmpty ? const Icon(Icons.person_rounded, color: _groupGreen) : null,
          ),
          title: Text(name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _ink, fontWeight: FontWeight.w800)),
          subtitle: Text(
            [
              if (username.isNotEmpty) '@' + username,
              if (statusTime.isNotEmpty) statusTime,
            ].join(' • '),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(color: _muted, fontSize: 11),
          ),
          trailing: Icon(seen ? Icons.visibility_rounded : Icons.done_all_rounded, color: _groupGreen, size: 21),
        );
      },
    );
  }

  if (!context.mounted) return;
  await showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    showDragHandle: true,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
    builder: (sheet) => SafeArea(
      child: SizedBox(
        height: MediaQuery.sizeOf(sheet).height * .80,
        child: ListView(
          padding: const EdgeInsets.only(bottom: 18),
          children: [
            const ListTile(
              leading: CircleAvatar(backgroundColor: _groupGreenSoft, child: Icon(Icons.info_outline_rounded, color: _groupGreen)),
              title: Text('Mesaj bilgisi', style: TextStyle(color: _ink, fontWeight: FontWeight.w900)),
              subtitle: Text('Kim gördü, kime teslim edildi', style: TextStyle(color: _muted)),
            ),
            const Divider(height: 1),
            ListTile(
              leading: const Icon(Icons.check_circle_outline_rounded, color: _groupGreen),
              title: const Text('Gönderildi', style: TextStyle(color: _ink, fontWeight: FontWeight.w800)),
              subtitle: Text(
                created == null ? 'Gönderim zamanı hazırlanıyor' : timeText(Timestamp.fromDate(created)),
                style: const TextStyle(color: _muted),
              ),
            ),
            Container(
              margin: const EdgeInsets.fromLTRB(14, 4, 14, 10),
              padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 11),
              decoration: BoxDecoration(color: _groupGreenSoft, borderRadius: BorderRadius.circular(16)),
              child: Row(children: [
                const Icon(Icons.visibility_outlined, color: _groupGreen, size: 20),
                const SizedBox(width: 8),
                Expanded(child: Text(
                  seenIds.isEmpty ? 'Henüz kimse görmedi' : seenIds.length.toString() + ' kişi gördü',
                  style: const TextStyle(color: _ink, fontWeight: FontWeight.w900),
                )),
                const SizedBox(width: 8),
                const Icon(Icons.done_all_rounded, color: _groupGreen, size: 20),
                const SizedBox(width: 6),
                Text(
                  deliveredOnlyIds.isEmpty ? '0 teslim' : deliveredOnlyIds.length.toString() + ' teslim',
                  style: const TextStyle(color: _muted, fontSize: 12, fontWeight: FontWeight.w800),
                ),
              ]),
            ),
            if (seenIds.isNotEmpty) ...[
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 3),
                child: Text('Görüldü • ' + seenIds.length.toString(), style: const TextStyle(color: _groupGreen, fontSize: 13, fontWeight: FontWeight.w900)),
              ),
              ...seenIds.map((id) => personRow(id, seen: true)),
            ],
            if (deliveredOnlyIds.isNotEmpty) ...[
              const Divider(height: 24, indent: 16, endIndent: 16),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 2, 16, 3),
                child: Text('Teslim edildi • ' + deliveredOnlyIds.length.toString(), style: const TextStyle(color: _groupGreen, fontSize: 13, fontWeight: FontWeight.w900)),
              ),
              ...deliveredOnlyIds.map((id) => personRow(id, seen: false)),
            ],
            if (seenIds.isEmpty && deliveredOnlyIds.isEmpty)
              const Padding(
                padding: EdgeInsets.fromLTRB(18, 18, 18, 6),
                child: Text(
                  'Teslim ve görülme bilgileri geldikçe burada kişi bazında görünecek.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: _muted, fontSize: 12, height: 1.35),
                ),
              ),
          ],
        ),
      ),
    ),
  );
}

Future<void> showGroupForwardSheet({
  required BuildContext context,
  required String sourceChatId,
  required String sourceMessageId,
  required Map<String, dynamic> sourceMessage,
}) async {
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) return;
  final uid = user.uid;
  final allowedTypes = <String>{'text','photo','gif','video','audio','file','location','sticker','shared_content'};
  final type = (sourceMessage['type'] ?? 'text').toString();
  if (!allowedTypes.contains(type)) {
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Bu mesaj türü iletilemiyor.')));
    }
    return;
  }

  final chats = await FirebaseFirestore.instance
      .collection('chats')
      .where('members', arrayContains: uid)
      .limit(60)
      .get();
  final rows = chats.docs.where((d) => d.id != sourceChatId).toList();

  if (!context.mounted) return;
  final selected = <String>{};
  var sending = false;
  final profileFutures = <String, Future<DocumentSnapshot<Map<String, dynamic>>>>{};

  await showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    showDragHandle: true,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
    builder: (sheetContext) => Theme(
      data: ThemeData.light().copyWith(
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSeed(seedColor: _groupGreen),
        listTileTheme: const ListTileThemeData(textColor: _ink, iconColor: _groupGreen),
      ),
      child: StatefulBuilder(builder: (sheet, setSheet) {
        return SafeArea(
          child: SizedBox(
            height: MediaQuery.sizeOf(sheet).height * .76,
            child: Column(children: [
              const Padding(
                padding: EdgeInsets.fromLTRB(18, 2, 18, 12),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text('Mesajı ilet', style: TextStyle(color: _ink, fontSize: 20, fontWeight: FontWeight.w900)),
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: rows.isEmpty
                    ? const Center(child: Text('İletilebilecek başka sohbet yok.', style: TextStyle(color: _muted, fontWeight: FontWeight.w700)))
                    : ListView.separated(
                        padding: const EdgeInsets.symmetric(vertical: 6),
                        itemCount: rows.length,
                        separatorBuilder: (_, __) => const Divider(height: 1, indent: 74, color: Color(0xFFF0F0F0)),
                        itemBuilder: (_, i) {
                          final doc = rows[i];
                          final data = doc.data();
                          final members = List<String>.from(data['members'] ?? const <String>[]);
                          final isGroup = data['isGroup'] == true || members.length > 2;
                          final checked = selected.contains(doc.id);

                          Widget row(String name, String subtitle, String photo, {required bool group}) {
                            return ListTile(
                              minVerticalPadding: 6,
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
                              onTap: sending ? null : () => setSheet(() => checked ? selected.remove(doc.id) : selected.add(doc.id)),
                              leading: CircleAvatar(
                                radius: 23,
                                backgroundColor: _groupGreenSoft,
                                backgroundImage: photo.isEmpty ? null : CachedNetworkImageProvider(photo),
                                child: photo.isEmpty ? Icon(group ? Icons.groups_rounded : Icons.person_rounded, color: _groupGreen) : null,
                              ),
                              title: Text(name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _ink, fontSize: 15, fontWeight: FontWeight.w900)),
                              subtitle: subtitle.isEmpty ? null : Text(subtitle, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _muted, fontSize: 11.5)),
                              trailing: AnimatedContainer(
                                duration: const Duration(milliseconds: 140),
                                width: 29,
                                height: 29,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  color: checked ? _groupGreen : Colors.white,
                                  border: Border.all(color: checked ? _groupGreen : const Color(0xFFD1D5DB), width: 1.4),
                                ),
                                child: checked ? const Icon(Icons.check_rounded, color: Colors.white, size: 18) : null,
                              ),
                            );
                          }

                          if (isGroup) {
                            return row(
                              (data['groupName'] ?? 'Grup sohbeti').toString(),
                              (data['lastMessage'] ?? 'Grup sohbeti').toString(),
                              (data['groupPhotoUrl'] ?? '').toString(),
                              group: true,
                            );
                          }

                          final other = members.firstWhere((x) => x != uid, orElse: () => '');
                          if (other.isEmpty) return row('Sohbet', '', '', group: false);
                          final future = profileFutures.putIfAbsent(
                            other,
                            () => FirebaseFirestore.instance.collection('users').doc(other).get(),
                          );
                          return FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
                            future: future,
                            builder: (_, snap) {
                              final p = snap.data?.data() ?? <String, dynamic>{};
                              final name = (p['displayName'] ?? p['username'] ?? 'Sohbet').toString();
                              final username = (p['username'] ?? '').toString().trim();
                              return row(name, username.isEmpty ? 'Özel sohbet' : '@' + username, (p['photoUrl'] ?? '').toString(), group: false);
                            },
                          );
                        },
                      ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(14, 8, 14, 14),
                child: SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: FilledButton.icon(
                    style: FilledButton.styleFrom(backgroundColor: _groupGreen),
                    onPressed: selected.isEmpty || sending
                        ? null
                        : () async {
                            setSheet(() => sending = true);
                            var sent = 0;
                            for (final chatId in selected) {
                              final target = FirebaseFirestore.instance.collection('chats').doc(chatId);
                              try {
                                final targetDoc = await target.get();
                                final targetData = targetDoc.data() ?? <String, dynamic>{};
                                final members = List<String>.from(targetData['members'] ?? const <String>[]);
                                final admins = List<String>.from(targetData['admins'] ?? const <String>[]);
                                final owner = (targetData['createdBy'] ?? '').toString();
                                if (!members.contains(uid)) continue;
                                if (targetData['onlyAdminsCanPost'] == true && !admins.contains(uid) && owner != uid) continue;

                                final out = <String, dynamic>{
                                  'senderId': uid,
                                  'type': type,
                                  'createdAt': FieldValue.serverTimestamp(),
                                  'clientCreatedAt': Timestamp.now(),
                                  'forwarded': true,
                                  'forwardedFromChatId': sourceChatId,
                                  'forwardedFromMessageId': sourceMessageId,
                                };
                                for (final key in <String>[
                                  'text','mediaUrl','audioUrl','durationSeconds','fileUrl','fileName','fileSize',
                                  'locationText','sticker','contentId','linkUrl','linkHost','linkTitle','linkDescription','linkImage'
                                ]) {
                                  if (sourceMessage.containsKey(key)) out[key] = sourceMessage[key];
                                }
                                final messageRef = target.collection('messages').doc();
                                final update = <String, dynamic>{
                                  'lastMessage': type == 'text'
                                      ? (sourceMessage['text'] ?? 'İletilen mesaj').toString()
                                      : '↪️ İletilen mesaj',
                                  'updatedAt': FieldValue.serverTimestamp(),
                                  'hiddenFor': FieldValue.arrayRemove(members),
                                };
                                for (final member in members) {
                                  if (member != uid) update['unread_' + member] = FieldValue.increment(1);
                                }
                                final batch = FirebaseFirestore.instance.batch();
                                batch.set(messageRef, out);
                                batch.set(target, update, SetOptions(merge: true));
                                await batch.commit();
                                sent++;
                              } catch (_) {}
                            }
                            if (sheet.mounted) Navigator.pop(sheet);
                            if (context.mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(sent > 0 ? sent.toString() + ' sohbete iletildi.' : 'Mesaj iletilemedi.')),
                              );
                            }
                          },
                    icon: sending
                        ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                        : const Icon(Icons.forward_rounded),
                    label: Text(sending ? 'İletiliyor...' : 'İlet'),
                  ),
                ),
              ),
            ]),
          ),
        );
      }),
    ),
  );
}

