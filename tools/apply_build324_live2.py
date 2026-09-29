#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "app/lib/live_broadcast_studio.dart"
PUB = ROOT / "app/pubspec.yaml"
MAIN = ROOT / "app/lib/main.dart"
RULES = ROOT / "firestore.rules"

live = LIVE.read_text(encoding="utf-8")
pub = PUB.read_text(encoding="utf-8")
main = MAIN.read_text(encoding="utf-8")
rules = RULES.read_text(encoding="utf-8")

def rep(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Build 324 patch failed: marker not found: {label}")
    return text.replace(old, new, 1)

pub = rep(pub, "version: 1.0.104+323", "version: 1.0.105+324", "pubspec version")
main = main.replace("defaultValue: '1.0.104'", "defaultValue: '1.0.105'")
main = main.replace("defaultValue: '323'", "defaultValue: '324'")

live = rep(
    live,
    "  String oran = '9:16';\n  String kalite = '720p';\n  String? kameraHatasi;",
    "  String oran = '9:16';\n  String kalite = '720p';\n  String gizlilik = 'Herkese açık';\n  String kategori = 'Sohbet';\n  int fps = 30;\n  bool geriSayim = true;\n  int baslangicSayaci = 0;\n  String? kameraHatasi;",
    "preparation state",
)

live = rep(live, "    maxFrameRate: 30,\n", "    maxFrameRate: fps,\n", "fps camera options")

live = rep(
    live,
    "  Future<void> baslat() async {\n",
    """  Future<void> _geriSayimCalistir() async {
    for (var i = 3; i >= 1; i--) {
      if (!mounted) return;
      setState(() => baslangicSayaci = i);
      await Future<void>.delayed(const Duration(milliseconds: 700));
    }
    if (mounted) setState(() => baslangicSayaci = 0);
  }

  Future<void> baslat() async {
""",
    "countdown helper",
)

live = rep(
    live,
    "    setState(() => baglaniyor = true);\n    lk.Room? oda;",
    "    setState(() => baglaniyor = true);\n    if (geriSayim) await _geriSayimCalistir();\n    lk.Room? oda;",
    "countdown call",
)

live = rep(
    live,
    "        'quality': kalite,\n      });",
    """        'quality': kalite,
        'fps': fps,
        'visibility': gizlilik,
        'category': kategori,
        'viewerCount': 0,
        'likeCount': 0,
        'giftPoints': 0,
        'pkActive': false,
      });
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'isLive': true,
        'currentLiveId': belge.id,
        'liveTitle': baslik.text.trim(),
        'liveStartedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));""",
    "live metadata",
)

live = rep(
    live,
    "        kameraAyarlari: _kameraAyarlari,\n      )));",
    """        kameraAyarlari: _kameraAyarlari,
        ownerId: user.uid,
        username: ad,
      )));""",
    "pass owner metadata",
)

live = rep(
    live,
    "                    Positioned(top: 8, right: 8, child: Row(children: [",
    """                    if (baslangicSayaci > 0) Center(child: Container(
                      width: 92, height: 92,
                      decoration: BoxDecoration(color: Colors.black54, shape: BoxShape.circle, border: Border.all(color: Colors.white70, width: 2)),
                      alignment: Alignment.center,
                      child: Text('$baslangicSayaci', style: const TextStyle(color: Colors.white, fontSize: 52, fontWeight: FontWeight.w900)),
                    )),
                    Positioned(top: 8, right: 8, child: Row(children: [""",
    "countdown overlay",
)

live = rep(
    live,
    "TextField(controller: baslik, maxLength: 100, style: const TextStyle(color: Colors.black87), decoration: InputDecoration(prefixIcon: const Icon(Icons.edit_rounded), hintText: 'Yayın başlığı yaz', filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none))),",
    "TextField(controller: baslik, maxLength: 100, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w600), decoration: InputDecoration(prefixIcon: const Icon(Icons.edit_rounded, color: Colors.black54), hintText: 'Yayın başlığı yaz', hintStyle: const TextStyle(color: Colors.black45, fontWeight: FontWeight.w600), filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none))),",
    "title readability",
)

live = rep(
    live,
    "            SizedBox(height: 42, child: ListView.separated(\n              scrollDirection: Axis.horizontal,",
    "            SizedBox(height: 42, child: ListView.separated(\n              padding: const EdgeInsets.only(right: 22),\n              scrollDirection: Axis.horizontal,",
    "filter trailing padding",
)

live = rep(
    live,
    """            Row(children: [
              Expanded(child: _canliSecimKutusu('Oran', oran, const ['9:16', '1:1', '16:9'], (v) => setState(() => oran = v))),
              const SizedBox(width: 12),
              Expanded(child: _canliSecimKutusu('Kalite', kalite, const ['540p', '720p', '1080p'], _kaliteDegistir)),
            ]),
            const SizedBox(height: 8),""",
    """            Row(children: [
              Expanded(child: _canliSecimKutusu('Oran', oran, const ['9:16', '1:1', '16:9'], (v) => setState(() => oran = v))),
              const SizedBox(width: 12),
              Expanded(child: _canliSecimKutusu('Kalite', kalite, const ['540p', '720p', '1080p'], _kaliteDegistir)),
            ]),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _canliSecimKutusu('Kategori', kategori, const ['Sohbet', 'Müzik', 'Oyun', 'Spor', 'Eğlence', 'Eğitim'], (v) => setState(() => kategori = v))),
              const SizedBox(width: 12),
              Expanded(child: _canliSecimKutusu('Gizlilik', gizlilik, const ['Herkese açık', 'Takipçiler', 'Arkadaşlar'], (v) => setState(() => gizlilik = v))),
            ]),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _canliSecimKutusu('FPS', '$fps', const ['30', '60'], (v) => setState(() => fps = int.parse(v)))),
              const SizedBox(width: 12),
              Expanded(child: SwitchListTile(
                contentPadding: const EdgeInsets.symmetric(horizontal: 10),
                value: geriSayim,
                onChanged: baglaniyor ? null : (v) => setState(() => geriSayim = v),
                title: const Text('3-2-1', style: TextStyle(fontWeight: FontWeight.w700)),
                subtitle: const Text('Başlangıç'),
              )),
            ]),
            const SizedBox(height: 8),""",
    "category privacy fps controls",
)

live = rep(
    live,
    "            const ListTile(contentPadding: EdgeInsets.zero, leading: Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text('Herkese açık', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('Keşfet bölümünde görünecek')),\n",
    "            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text(gizlilik, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('$kategori • ${fps} FPS • $kalite')),\n",
    "privacy summary",
)

live = rep(
    live,
    "  final lk.CameraCaptureOptions kameraAyarlari;\n  const CanliYayinPage({",
    "  final lk.CameraCaptureOptions kameraAyarlari;\n  final String ownerId;\n  final String username;\n  const CanliYayinPage({",
    "live page fields",
)

live = rep(
    live,
    "    this.kameraAyarlari = const lk.CameraCaptureOptions(),\n  });",
    "    this.kameraAyarlari = const lk.CameraCaptureOptions(),\n    this.ownerId = '',\n    this.username = 'ngelx',\n  });",
    "live page constructor",
)

live = rep(
    live,
    "  bool kameraDegisiyor = false;\n",
    """  bool kameraDegisiyor = false;
  bool hediyeGonderiliyor = false;
  bool katilimKaydiYapildi = false;
  int maxIzleyici = 0;
  int yerelKalpSerisi = 0;
""",
    "live interaction state",
)

live = rep(
    live,
    """    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => saniye++);
    });
  }""",
    """    if (!widget.yayinSahibi) unawaited(_katildimKaydet());
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      final izleyici = widget.oda.remoteParticipants.length;
      if (izleyici > maxIzleyici) maxIzleyici = izleyici;
      if (mounted) setState(() => saniye++);
    });
  }""",
    "join event init",
)

live = rep(
    live,
    "  Future<void> _kalpDegistir() async {\n",
    r"""  Future<Map<String, dynamic>> _aktifProfil() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return <String, dynamic>{};
    try {
      final p = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      return p.data() ?? <String, dynamic>{};
    } catch (_) {
      return <String, dynamic>{};
    }
  }

  Future<void> _katildimKaydet() async {
    if (katilimKaydiYapildi) return;
    katilimKaydiYapildi = true;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    final p = await _aktifProfil();
    try {
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
        'uid': user.uid,
        'userId': user.uid,
        'username': (p['username'] ?? user.displayName ?? 'ngelx').toString(),
        'text': 'yayına katıldı',
        'kind': 'join',
        'createdAt': FieldValue.serverTimestamp(),
      });
    } catch (_) {}
  }

  Future<void> _paylas() async {
    await Clipboard.setData(ClipboardData(text: 'NgelX canlı yayın • ${widget.baslik}\nngelx://live/${widget.belgeId}'));
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Canlı yayın bağlantısı kopyalandı.')));
  }

  Future<void> _hediyeGonder(String ad, String emoji, int puan) async {
    if (hediyeGonderiliyor) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    hediyeGonderiliyor = true;
    try {
      final p = await _aktifProfil();
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
        'uid': user.uid,
        'userId': user.uid,
        'username': (p['username'] ?? user.displayName ?? 'ngelx').toString(),
        'text': '$emoji $ad',
        'kind': 'gift',
        'giftName': ad,
        'giftEmoji': emoji,
        'points': puan,
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$emoji $ad gönderildi • +$puan N-Puan')));
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hediye gönderilemedi.')));
    } finally {
      hediyeGonderiliyor = false;
    }
  }

  Future<void> _hediyePaneli() async {
    final hediyeler = <Map<String, dynamic>>[
      {'ad': 'Gül', 'emoji': '🌹', 'puan': 1},
      {'ad': 'Yıldız', 'emoji': '⭐', 'puan': 5},
      {'ad': 'Kalp Taşı', 'emoji': '💎', 'puan': 15},
      {'ad': 'Taç', 'emoji': '👑', 'puan': 25},
      {'ad': 'NgelX Roket', 'emoji': '🚀', 'puan': 50},
      {'ad': 'Galaksi', 'emoji': '🌌', 'puan': 100},
    ];
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: const Color(0xFF15151B),
      showDragHandle: true,
      builder: (c) => SafeArea(child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 4, 16, 18),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('N-Hediye', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          const Text('Canlı yayını destekle • hediyeler N-Puan kazandırır', style: TextStyle(color: Colors.white60)),
          const SizedBox(height: 14),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .95, crossAxisSpacing: 10, mainAxisSpacing: 10),
            itemCount: hediyeler.length,
            itemBuilder: (_, i) {
              final h = hediyeler[i];
              return InkWell(
                onTap: () async {
                  Navigator.pop(c);
                  await _hediyeGonder(h['ad'] as String, h['emoji'] as String, h['puan'] as int);
                },
                borderRadius: BorderRadius.circular(18),
                child: Container(
                  decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(18), border: Border.all(color: Colors.white12)),
                  padding: const EdgeInsets.all(10),
                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    Text(h['emoji'] as String, style: const TextStyle(fontSize: 30)),
                    const SizedBox(height: 5),
                    Text(h['ad'] as String, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800), textAlign: TextAlign.center),
                    Text('${h['puan']} N', style: const TextStyle(color: Color(0xFF8D6BFF), fontWeight: FontWeight.w800)),
                  ]),
                ),
              );
            },
          ),
        ]),
      )),
    );
  }

  Future<void> _kalpDegistir() async {
""",
    "interaction helpers",
)

live = rep(
    live,
    """      final mevcut=await ref.get();
      if(mevcut.exists){
        await ref.delete();
      }else{
        await ref.set({'uid':user.uid,'type':'heart','createdAt':FieldValue.serverTimestamp()});
      }""",
    """      await FirebaseFirestore.instance.runTransaction((tx) async {
        final mevcut = await tx.get(ref);
        final onceki = (mevcut.data()?['count'] as num?)?.toInt() ?? 0;
        tx.set(ref, {
          'uid': user.uid,
          'userId': user.uid,
          'type': 'heart',
          'count': onceki + 1,
          'updatedAt': FieldValue.serverTimestamp(),
          if (!mevcut.exists) 'createdAt': FieldValue.serverTimestamp(),
        });
      });
      if (mounted) setState(() => yerelKalpSerisi++);""",
    "heart increment",
)

live = rep(
    live,
    """      'uid': user.uid,
      'username': (profil.data()?['username'] ?? 'ngelx').toString(),
      'text': metin,
      'createdAt': FieldValue.serverTimestamp(),""",
    """      'uid': user.uid,
      'userId': user.uid,
      'username': (profil.data()?['username'] ?? 'ngelx').toString(),
      'text': metin,
      'kind': 'comment',
      'createdAt': FieldValue.serverTimestamp(),""",
    "comment userId",
)

live = rep(
    live,
    """    if (widget.yayinSahibi) {
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'active': false, 'endedAt': FieldValue.serverTimestamp()}, SetOptions(merge: true));
    }""",
    """    if (widget.yayinSahibi) {
      var toplamKalp = 0;
      var hediyePuani = 0;
      var yorumSayisi = 0;
      try {
        final rs = await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').get();
        for (final d in rs.docs) {
          toplamKalp += (d.data()['count'] as num?)?.toInt() ?? 1;
        }
        final cs = await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').get();
        for (final d in cs.docs) {
          final data = d.data();
          if (data['kind'] == 'gift') hediyePuani += (data['points'] as num?)?.toInt() ?? 0;
          if ((data['kind'] ?? 'comment') == 'comment') yorumSayisi++;
        }
      } catch (_) {}
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active': false,
        'endedAt': FieldValue.serverTimestamp(),
        'durationSeconds': saniye,
        'maxViewers': maxIzleyici,
        'likeCount': toplamKalp,
        'giftPoints': hediyePuani,
        'commentCount': yorumSayisi,
      }, SetOptions(merge: true));
      final uid = widget.ownerId.isNotEmpty ? widget.ownerId : FirebaseAuth.instance.currentUser?.uid;
      if (uid != null) {
        await FirebaseFirestore.instance.collection('users').doc(uid).set({
          'isLive': false,
          'currentLiveId': FieldValue.delete(),
          'liveTitle': FieldValue.delete(),
          'liveEndedAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true));
      }
    }""",
    "end analytics",
)

live = rep(
    live,
    """                      final y = yorumlar[i].data();
                      return Padding(padding: const EdgeInsets.symmetric(vertical: 3), child: Text('@${y['username'] ?? 'ngelx'}  ${y['text'] ?? ''}'));""",
    """                      final y = yorumlar[i].data();
                      final kind = (y['kind'] ?? 'comment').toString();
                      if (kind == 'join') {
                        return Padding(padding: const EdgeInsets.symmetric(vertical: 3), child: Text('👋 ${y['username'] ?? 'ngelx'} katıldı', style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w600)));
                      }
                      if (kind == 'gift') {
                        return Padding(padding: const EdgeInsets.symmetric(vertical: 4), child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
                          decoration: BoxDecoration(color: const Color(0x668D6BFF), borderRadius: BorderRadius.circular(12)),
                          child: Text('${y['giftEmoji'] ?? '🎁'} ${y['username'] ?? 'ngelx'} • ${y['giftName'] ?? 'N-Hediye'} +${y['points'] ?? 0} N', style: const TextStyle(fontWeight: FontWeight.w800)),
                        ));
                      }
                      return Padding(padding: const EdgeInsets.symmetric(vertical: 3), child: Text('@${y['username'] ?? 'ngelx'}  ${y['text'] ?? ''}'));""",
    "event rendering",
)

live = rep(
    live,
    """                      final user=FirebaseAuth.instance.currentUser;
                      final benim=user!=null&&(s.data?.docs??[]).any((d)=>d.id==user.uid);
                      final sayi=s.data?.docs.length??0;
                      return FilledButton.tonalIcon(
                        onPressed:kalpIsleniyor?null:_kalpDegistir,
                        icon:Icon(benim?Icons.favorite_rounded:Icons.favorite_border_rounded,color:Colors.redAccent),
                        label:Text(sayi>0?'$sayi':'Beğen'),
                      );""",
    """                      final docs=s.data?.docs??[];
                      final sayi=docs.fold<int>(0,(t,d)=>t+((d.data()['count'] as num?)?.toInt()??1));
                      return FilledButton.tonalIcon(
                        onPressed:kalpIsleniyor?null:_kalpDegistir,
                        icon:const Icon(Icons.favorite_rounded,color:Colors.redAccent),
                        label:Text(sayi>0?'$sayi':'Kalp'),
                      );""",
    "heart UI",
)

live = rep(
    live,
    """                ],
              ]),
              if (widget.yayinSahibi) ...[""",
    """                  const SizedBox(width: 6),
                  IconButton.filledTonal(onPressed: hediyeGonderiliyor ? null : _hediyePaneli, tooltip: 'N-Hediye', icon: const Icon(Icons.card_giftcard_rounded, color: Color(0xFFFF4F93))),
                  const SizedBox(width: 4),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Paylaş', icon: const Icon(Icons.share_rounded)),
                ],
              ]),
              if (yerelKalpSerisi >= 5 && !widget.yayinSahibi)
                Padding(padding: const EdgeInsets.only(top: 6), child: Align(alignment: Alignment.centerRight, child: Text('N-Kombo x$yerelKalpSerisi ❤️', style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w800)))),
              if (widget.yayinSahibi) ...[""",
    "viewer gift share controls",
)

live = rep(
    live,
    """                  const SizedBox(width: 9),
                  FilledButton.icon(style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744)), onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.stop_circle_outlined), label: const Text('Bitir')),""",
    """                  const SizedBox(width: 9),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Yayını paylaş', icon: const Icon(Icons.share_rounded)),
                  const SizedBox(width: 9),
                  FilledButton.icon(style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744)), onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.stop_circle_outlined), label: const Text('Bitir')),""",
    "host share",
)

rules = rules.replace(
    "allow create: if signedIn() && request.resource.data.userId == request.auth.uid;",
    "allow create: if signedIn() && (request.resource.data.userId == request.auth.uid || request.resource.data.uid == request.auth.uid);",
    1,
)
rules = rules.replace(
    "allow update, delete: if signedIn() && resource.data.userId == request.auth.uid;",
    "allow update, delete: if signedIn() && (resource.data.userId == request.auth.uid || resource.data.uid == request.auth.uid);",
    1,
)

LIVE.write_text(live, encoding="utf-8")
PUB.write_text(pub, encoding="utf-8")
MAIN.write_text(main, encoding="utf-8")
RULES.write_text(rules, encoding="utf-8")
print("Build 324 LIVE 2.0 interaction foundation patch applied.")
