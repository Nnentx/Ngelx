part of 'main.dart';

class NgelXMuzikSecPage extends StatefulWidget {
  const NgelXMuzikSecPage({super.key});
  @override
  State<NgelXMuzikSecPage> createState() => _NgelXMuzikSecPageState();
}

class _NgelXMuzikSecPageState extends State<NgelXMuzikSecPage> {
  final ara = TextEditingController();
  final AudioPlayer onizleme = AudioPlayer();
  String sorgu = '';
  int sekme = 0;
  String? oynayanId;
  Set<String> kaydedilenler = <String>{};

  @override
  void initState() {
    super.initState();
    unawaited(_kaydedilenleriGetir());
  }

  Future<void> _kaydedilenleriGetir() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;
    try {
      final d = await FirebaseFirestore.instance.collection('users').doc(uid).get();
      if (!mounted) return;
      setState(() {
        kaydedilenler = Set<String>.from(List<dynamic>.from(d.data()?['savedMusic'] ?? const []));
      });
    } catch (_) {}
  }

  bool _lisansUygun(Map<String, dynamic> v) {
    final durum = (v['licenseStatus'] ?? '').toString().toLowerCase().trim();
    return v['royaltyFree'] == true ||
        v['licensed'] == true ||
        durum == 'licensed' ||
        durum == 'royalty-free' ||
        durum == 'royalty_free' ||
        durum == 'permissioned' ||
        durum == 'public-domain' ||
        durum == 'public_domain';
  }

  Future<void> _onizle(String id, String url) async {
    if (url.isEmpty) return;
    try {
      if (oynayanId == id && onizleme.playing) {
        await onizleme.pause();
        if (mounted) setState(() {});
        return;
      }
      await onizleme.stop();
      await onizleme.setUrl(url);
      await onizleme.setLoopMode(LoopMode.one);
      oynayanId = id;
      await onizleme.play();
      if (mounted) setState(() {});
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Müzik önizlemesi açılamadı.')),
        );
      }
    }
  }

  Future<void> _kaydet(String id) async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null || id.isEmpty) return;
    final ekle = !kaydedilenler.contains(id);
    if (mounted) {
      setState(() {
        if (ekle) {
          kaydedilenler.add(id);
        } else {
          kaydedilenler.remove(id);
        }
      });
    }
    try {
      await FirebaseFirestore.instance.collection('users').doc(uid).set({
        'savedMusic': ekle ? FieldValue.arrayUnion([id]) : FieldValue.arrayRemove([id]),
      }, SetOptions(merge: true));
    } catch (_) {
      if (!mounted) return;
      setState(() {
        if (ekle) {
          kaydedilenler.remove(id);
        } else {
          kaydedilenler.add(id);
        }
      });
    }
  }

  @override
  void dispose() {
    ara.dispose();
    unawaited(onizleme.dispose());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData.light(),
      child: Scaffold(
        backgroundColor: const Color(0xFF202124),
        appBar: AppBar(
          backgroundColor: const Color(0xFF202124),
          foregroundColor: Colors.white,
          title: const Text('Müzik ekle', style: TextStyle(fontWeight: FontWeight.w900)),
          surfaceTintColor: Colors.transparent,
        ),
        body: SafeArea(
          top: false,
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 10, 16, 10),
                child: TextField(
                  controller: ara,
                  onChanged: (v) => setState(() => sorgu = v.trim().toLowerCase()),
                  style: const TextStyle(color: Colors.white),
                  decoration: InputDecoration(
                    hintText: 'Müziklerde ara',
                    hintStyle: const TextStyle(color: Colors.white54),
                    prefixIcon: const Icon(Icons.search_rounded, color: Colors.white54),
                    suffixIcon: sorgu.isEmpty
                        ? null
                        : IconButton(
                            onPressed: () {
                              ara.clear();
                              setState(() => sorgu = '');
                            },
                            icon: const Icon(Icons.close_rounded, color: Colors.white54),
                          ),
                    filled: true,
                    fillColor: const Color(0xFF343538),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(28),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: Row(
                  children: [
                    _sekmeButonu(0, 'Senin için', Icons.auto_awesome_rounded),
                    _sekmeButonu(1, 'Popüler', Icons.trending_up_rounded),
                    _sekmeButonu(2, 'Kaydedilenler', Icons.bookmark_rounded),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                  stream: FirebaseFirestore.instance
                      .collection('music_catalog')
                      .where('active', isEqualTo: true)
                      .limit(100)
                      .snapshots(),
                  builder: (_, snap) {
                    if (snap.connectionState == ConnectionState.waiting && !snap.hasData) {
                      return const Center(child: CircularProgressIndicator(color: mavi));
                    }
                    if (snap.hasError) {
                      return const Center(
                        child: Padding(
                          padding: EdgeInsets.all(24),
                          child: Text(
                            'Müzik kataloğu şu anda yüklenemedi.',
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.white70),
                          ),
                        ),
                      );
                    }
                    var docs = (snap.data?.docs ?? const <QueryDocumentSnapshot<Map<String, dynamic>>>[])
                        .where((d) => _lisansUygun(d.data()))
                        .where((d) {
                          final v = d.data();
                          final araMetni =
                              '${v['title'] ?? ''} ${v['artist'] ?? ''} ${v['tags'] ?? ''}'.toLowerCase();
                          return sorgu.isEmpty || araMetni.contains(sorgu);
                        })
                        .toList();

                    if (sekme == 2) {
                      docs = docs.where((d) => kaydedilenler.contains(d.id)).toList();
                    } else if (sekme == 1) {
                      docs.sort((a, b) {
                        final ap = (a.data()['popularity'] as num?)?.toInt() ?? 0;
                        final bp = (b.data()['popularity'] as num?)?.toInt() ?? 0;
                        return bp.compareTo(ap);
                      });
                    } else {
                      docs.sort((a, b) {
                        final ar = (a.data()['recommendedScore'] as num?)?.toDouble() ?? 0;
                        final br = (b.data()['recommendedScore'] as num?)?.toDouble() ?? 0;
                        return br.compareTo(ar);
                      });
                    }

                    if (docs.isEmpty) {
                      return const Center(
                        child: Padding(
                          padding: EdgeInsets.all(28),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.library_music_outlined, color: Colors.white38, size: 54),
                              SizedBox(height: 10),
                              Text(
                                'Bu bölümde kullanım hakkı uygun müzik bulunamadı.',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: Colors.white60, fontWeight: FontWeight.w700),
                              ),
                              SizedBox(height: 6),
                              Text(
                                'Yalnızca lisanslı, izinli veya telifsiz parçalar gösterilir.',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: Colors.white38, fontSize: 12),
                              ),
                            ],
                          ),
                        ),
                      );
                    }

                    return ListView.separated(
                      padding: const EdgeInsets.fromLTRB(12, 4, 12, 22),
                      itemCount: docs.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 3),
                      itemBuilder: (_, i) {
                        final d = docs[i];
                        final v = d.data();
                        final baslik = (v['title'] ?? 'NgelX müziği').toString();
                        final sanatci = (v['artist'] ?? 'NgelX Music').toString();
                        final kapak = (v['coverUrl'] ?? '').toString();
                        final url = (v['audioUrl'] ?? '').toString();
                        final kayitli = kaydedilenler.contains(d.id);
                        final oynuyor = oynayanId == d.id && onizleme.playing;
                        return Material(
                          color: Colors.transparent,
                          child: InkWell(
                            borderRadius: BorderRadius.circular(18),
                            onTap: url.isEmpty
                                ? null
                                : () {
                                    unawaited(onizleme.pause());
                                    Navigator.pop(context, <String, dynamic>{
                                      'id': d.id,
                                      'title': baslik,
                                      'artist': sanatci,
                                      'audioUrl': url,
                                      'coverUrl': kapak,
                                      'licenseStatus': (v['licenseStatus'] ?? (v['royaltyFree'] == true ? 'royalty-free' : 'licensed')).toString(),
                                      'durationSeconds': (v['durationSeconds'] as num?)?.toInt() ?? 0,
                                    });
                                  },
                            child: Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                              child: Row(
                                children: [
                                  ClipRRect(
                                    borderRadius: BorderRadius.circular(12),
                                    child: kapak.isEmpty
                                        ? Container(
                                            width: 58,
                                            height: 58,
                                            color: const Color(0xFF3B3C40),
                                            child: const Icon(Icons.music_note_rounded, color: Colors.white70),
                                          )
                                        : CachedNetworkImage(
                                            imageUrl: kapak,
                                            width: 58,
                                            height: 58,
                                            fit: BoxFit.cover,
                                            errorWidget: (_, __, ___) => Container(
                                              width: 58,
                                              height: 58,
                                              color: const Color(0xFF3B3C40),
                                              child: const Icon(Icons.music_note_rounded, color: Colors.white70),
                                            ),
                                          ),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          baslik,
                                          maxLines: 1,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w900),
                                        ),
                                        const SizedBox(height: 3),
                                        Text(
                                          sanatci,
                                          maxLines: 1,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white70, fontSize: 13),
                                        ),
                                      ],
                                    ),
                                  ),
                                  IconButton(
                                    tooltip: kayitli ? 'Kaydedilenlerden çıkar' : 'Kaydet',
                                    onPressed: () => unawaited(_kaydet(d.id)),
                                    icon: Icon(kayitli ? Icons.bookmark_rounded : Icons.bookmark_border_rounded, color: Colors.white70),
                                  ),
                                  IconButton(
                                    tooltip: oynuyor ? 'Duraklat' : 'Önizle',
                                    onPressed: url.isEmpty ? null : () => unawaited(_onizle(d.id, url)),
                                    icon: CircleAvatar(
                                      backgroundColor: const Color(0xFF3B3C40),
                                      child: Icon(oynuyor ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.white),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _sekmeButonu(int deger, String yazi, IconData ikon) {
    final secili = sekme == deger;
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 3),
        child: InkWell(
          onTap: () => setState(() => sekme = deger),
          borderRadius: BorderRadius.circular(18),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 10),
            decoration: BoxDecoration(
              color: secili ? const Color(0xFF17365A) : Colors.transparent,
              borderRadius: BorderRadius.circular(18),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(ikon, size: 17, color: secili ? const Color(0xFF78B7FF) : Colors.white70),
                const SizedBox(width: 5),
                Flexible(
                  child: Text(
                    yazi,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: secili ? const Color(0xFF78B7FF) : Colors.white,
                      fontWeight: secili ? FontWeight.w900 : FontWeight.w700,
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class NgelXVideoDuzenlemePage extends StatefulWidget {
  final XFile dosya;
  final int baslangicMs;
  final int bitisMs;
  final String yazi;
  const NgelXVideoDuzenlemePage({
    super.key,
    required this.dosya,
    this.baslangicMs = 0,
    this.bitisMs = 0,
    this.yazi = '',
  });

  @override
  State<NgelXVideoDuzenlemePage> createState() => _NgelXVideoDuzenlemePageState();
}

class _NgelXVideoDuzenlemePageState extends State<NgelXVideoDuzenlemePage> {
  late final VideoPlayerController kontrol;
  late final TextEditingController yazi;
  bool hazir = false;
  bool oynuyor = false;
  double bas = 0;
  double son = 1;
  double toplam = 1;

  @override
  void initState() {
    super.initState();
    yazi = TextEditingController(text: widget.yazi);
    kontrol = VideoPlayerController.file(File(widget.dosya.path));
    kontrol.initialize().then((_) async {
      toplam = math.max(1.0, kontrol.value.duration.inMilliseconds / 1000.0).toDouble();
      bas = (widget.baslangicMs / 1000.0).clamp(0.0, toplam).toDouble();
      son = widget.bitisMs > 0
          ? (widget.bitisMs / 1000.0).clamp(bas + .1, toplam).toDouble()
          : toplam;
      if (son <= bas) son = math.min(toplam, bas + .1);
      await kontrol.seekTo(Duration(milliseconds: (bas * 1000).round()));
      kontrol.addListener(_konumKontrol);
      if (mounted) setState(() => hazir = true);
    }).catchError((_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Video düzenleme önizlemesi açılamadı.')),
        );
      }
    });
  }

  void _konumKontrol() {
    if (!hazir || !kontrol.value.isInitialized) return;
    final sn = kontrol.value.position.inMilliseconds / 1000.0;
    if (sn >= son && kontrol.value.isPlaying) {
      unawaited(kontrol.seekTo(Duration(milliseconds: (bas * 1000).round())).then((_) => kontrol.play()));
    }
    final yeni = kontrol.value.isPlaying;
    if (mounted && yeni != oynuyor) setState(() => oynuyor = yeni);
  }

  String _sure(double sn) {
    final s = sn.round().clamp(0, 24 * 60 * 60);
    final dk = s ~/ 60;
    final kalan = s % 60;
    return '$dk:${kalan.toString().padLeft(2, '0')}';
  }

  Future<void> _oynat() async {
    if (!hazir) return;
    if (kontrol.value.isPlaying) {
      await kontrol.pause();
    } else {
      final pos = kontrol.value.position.inMilliseconds / 1000.0;
      if (pos < bas || pos >= son) {
        await kontrol.seekTo(Duration(milliseconds: (bas * 1000).round()));
      }
      await kontrol.play();
    }
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    kontrol.removeListener(_konumKontrol);
    kontrol.dispose();
    yazi.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData.dark(),
      child: Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(
          backgroundColor: Colors.black,
          title: const Text('Videoyu düzenle', style: TextStyle(fontWeight: FontWeight.w900)),
          actions: [
            TextButton(
              onPressed: !hazir
                  ? null
                  : () => Navigator.pop(context, <String, dynamic>{
                        'trimStartMs': (bas * 1000).round(),
                        'trimEndMs': son >= toplam - .05 ? 0 : (son * 1000).round(),
                        'overlayText': yazi.text.trim(),
                      }),
              child: const Text('Bitti', style: TextStyle(color: mavi, fontWeight: FontWeight.w900)),
            ),
          ],
        ),
        body: SafeArea(
          child: hazir
              ? ListView(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                  children: [
                    AspectRatio(
                      aspectRatio: kontrol.value.aspectRatio <= 0 ? 9 / 16 : kontrol.value.aspectRatio,
                      child: Stack(
                        fit: StackFit.expand,
                        children: [
                          VideoPlayer(kontrol),
                          if (yazi.text.trim().isNotEmpty)
                            Center(
                              child: Container(
                                margin: const EdgeInsets.all(18),
                                padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 8),
                                decoration: BoxDecoration(
                                  color: Colors.black54,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  yazi.text.trim(),
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w900),
                                ),
                              ),
                            ),
                          Center(
                            child: IconButton.filled(
                              onPressed: _oynat,
                              style: IconButton.styleFrom(backgroundColor: Colors.black54),
                              icon: Icon(oynuyor ? Icons.pause_rounded : Icons.play_arrow_rounded, size: 34),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 18),
                    Row(
                      children: [
                        Text(_sure(bas), style: const TextStyle(fontWeight: FontWeight.w800)),
                        const Spacer(),
                        Text(_sure(son), style: const TextStyle(fontWeight: FontWeight.w800)),
                      ],
                    ),
                    RangeSlider(
                      min: 0,
                      max: toplam,
                      values: RangeValues(bas, son),
                      labels: RangeLabels(_sure(bas), _sure(son)),
                      onChanged: (v) {
                        var s = v.start;
                        var e = v.end;
                        if (e - s < .5) {
                          if (s != bas) {
                            s = math.max(0.0, e - .5);
                          } else {
                            e = math.min(toplam, s + .5);
                          }
                        }
                        setState(() {
                          bas = s;
                          son = e;
                        });
                      },
                      onChangeEnd: (_) => kontrol.seekTo(Duration(milliseconds: (bas * 1000).round())),
                    ),
                    const Text(
                      'Kes / kırp',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900),
                    ),
                    const SizedBox(height: 5),
                    const Text(
                      'Videoda görünmesini istediğin başlangıç ve bitiş aralığını seç.',
                      style: TextStyle(color: Colors.white60, fontSize: 12),
                    ),
                    const SizedBox(height: 18),
                    TextField(
                      controller: yazi,
                      maxLength: 120,
                      onChanged: (_) => setState(() {}),
                      decoration: InputDecoration(
                        labelText: 'Video üzerine yazı',
                        prefixIcon: const Icon(Icons.text_fields_rounded),
                        filled: true,
                        fillColor: const Color(0xFF1D1D1F),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(18),
                          borderSide: BorderSide.none,
                        ),
                      ),
                    ),
                  ],
                )
              : const Center(child: CircularProgressIndicator(color: mavi)),
        ),
      ),
    );
  }
}
