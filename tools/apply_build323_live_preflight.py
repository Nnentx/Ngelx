from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
main_path = root / 'app/lib/main.dart'
pub_path = root / 'app/pubspec.yaml'

main = main_path.read_text(encoding='utf-8')
pub = pub_path.read_text(encoding='utf-8')

for required in [
    'class CanliHazirlikPage extends StatefulWidget {',
    'class YuklePage extends StatefulWidget {',
]:
    if required not in main:
        raise SystemExit(f'Build 323 marker missing: {required}')

new_block = r'''class CanliHazirlikPage extends StatefulWidget {
  const CanliHazirlikPage({super.key});

  @override
  State<CanliHazirlikPage> createState() => _CanliHazirlikPageState();
}

class _CanliHazirlikPageState extends State<CanliHazirlikPage> {
  final baslik = TextEditingController();
  lk.Room? oda;
  String? odaAdi;
  bool baglaniyor = false;
  bool onizlemeHazir = false;
  bool mikrofon = true;
  bool kamera = true;
  bool arkaKamera = false;
  bool rotus = false;
  bool devredildi = false;
  int filtre = 0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => unawaited(_onizlemeyiHazirla()));
  }

  void _odaDegisti() {
    if (mounted) setState(() {});
  }

  lk.VideoTrack? get _yerelVideo {
    final yerel = oda?.localParticipant;
    if (yerel == null) return null;
    for (final pub in yerel.videoTrackPublications) {
      final track = pub.track;
      if (track is lk.VideoTrack && !pub.muted) return track;
    }
    return null;
  }

  Future<void> _odayiKapat(lk.Room? r) async {
    if (r == null) return;
    try {
      r.removeListener(_odaDegisti);
    } catch (_) {}
    try {
      await r.disconnect();
    } catch (_) {}
    try {
      await r.dispose();
    } catch (_) {}
  }

  Future<void> _onizlemeyiHazirla() async {
    if (baglaniyor || onizlemeHazir) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.isAnonymous) return;
    if (mounted) setState(() => baglaniyor = true);
    lk.Room? yeniOda;
    try {
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();
      final isim = 'ngelx_${user.uid}_${DateTime.now().millisecondsSinceEpoch}';
      final kaynak = lk.DevelopmentTokenSource(id: liveKitTestSunucuId);
      final cevap = await kaynak.fetch(lk.TokenRequestOptions(
        roomName: isim,
        participantIdentity: user.uid,
        participantName: ad,
        participantAttributes: const {'role': 'host'},
      ));
      yeniOda = lk.Room(roomOptions: lk.RoomOptions(adaptiveStream: true, dynacast: true));
      yeniOda.addListener(_odaDegisti);
      await yeniOda.connect(cevap.serverUrl, cevap.participantToken);
      final yerel = yeniOda.localParticipant;
      if (yerel == null) throw Exception('Canlı yayın önizlemesi hazırlanamadı.');
      if (kamera) {
        await yerel.setCameraEnabled(
          true,
          cameraCaptureOptions: const lk.CameraCaptureOptions(
            params: lk.VideoParametersPresets.h360_169,
            maxFrameRate: 20.0,
            stopCameraCaptureOnMute: true,
          ),
        );
      }
      await yerel.setMicrophoneEnabled(mikrofon);
      if (!mounted) {
        await _odayiKapat(yeniOda);
        return;
      }
      oda = yeniOda;
      odaAdi = isim;
      onizlemeHazir = true;
      setState(() => baglaniyor = false);
    } catch (e) {
      await _odayiKapat(yeniOda);
      if (!mounted) return;
      setState(() {
        baglaniyor = false;
        onizlemeHazir = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Kamera önizlemesi hazırlanamadı: $e')),
      );
    }
  }

  Future<void> _mikrofonDegistir() async {
    final yeni = !mikrofon;
    try {
      await oda?.localParticipant?.setMicrophoneEnabled(yeni);
      if (mounted) setState(() => mikrofon = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Mikrofon değiştirilemedi.')),
        );
      }
    }
  }

  Future<void> _kameraDegistir() async {
    final yeni = !kamera;
    try {
      await oda?.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: const lk.CameraCaptureOptions(
          params: lk.VideoParametersPresets.h360_169,
          maxFrameRate: 20.0,
          stopCameraCaptureOnMute: true,
        ),
      );
      if (mounted) setState(() => kamera = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Kamera değiştirilemedi. Kamera iznini kontrol et.')),
        );
      }
    }
  }

  Future<void> _kameraCevir() async {
    final track = _yerelVideo;
    if (track is! lk.LocalVideoTrack) return;
    final yeni = !arkaKamera;
    try {
      await track.setCameraPosition(yeni ? lk.CameraPosition.back : lk.CameraPosition.front);
      if (mounted) setState(() => arkaKamera = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Kamera yönü değiştirilemedi.')),
        );
      }
    }
  }

  Future<void> _filtreSec() async {
    final secim = await showModalBottomSheet<int>(
      context: context,
      backgroundColor: const Color(0xFF14111D),
      showDragHandle: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 2, 16, 22),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Canlı yayın filtresi',
                style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 5),
              const Text(
                'Yayından önce görünümü seç. Değişiklik anında önizlemede görünür.',
                style: TextStyle(color: Colors.white60, fontSize: 12),
              ),
              const SizedBox(height: 14),
              SizedBox(
                height: 96,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  itemCount: ngelxAramaEfektAdlari.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 8),
                  itemBuilder: (_, i) => InkWell(
                    onTap: () => Navigator.pop(c, i),
                    borderRadius: BorderRadius.circular(18),
                    child: Container(
                      width: 78,
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: i == filtre ? const Color(0xFF352154) : const Color(0xFF211837),
                        borderRadius: BorderRadius.circular(18),
                        border: Border.all(
                          color: i == filtre ? const Color(0xFF9C73FF) : Colors.white10,
                        ),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            i == 0
                                ? Icons.block_rounded
                                : i == ngelxAramaEfektAdlari.length - 1
                                    ? Icons.filter_b_and_w_rounded
                                    : Icons.auto_awesome_rounded,
                            color: Colors.white,
                            size: 27,
                          ),
                          const SizedBox(height: 7),
                          Text(
                            ngelxAramaEfektAdlari[i],
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(
                              color: i == filtre ? const Color(0xFFCDB9FF) : Colors.white70,
                              fontSize: 10,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    if (secim != null && mounted) setState(() => filtre = secim);
  }

  Future<void> baslat() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.isAnonymous || baglaniyor) return;
    if (baslik.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('En az 3 karakterlik yayın başlığı yaz.')),
      );
      return;
    }
    if (!onizlemeHazir || oda == null || odaAdi == null) {
      await _onizlemeyiHazirla();
      if (!mounted || oda == null || odaAdi == null) return;
    }
    setState(() => baglaniyor = true);
    try {
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();
      final belge = await FirebaseFirestore.instance.collection('live_streams').add({
        'roomName': odaAdi,
        'ownerId': user.uid,
        'username': ad,
        'title': baslik.text.trim(),
        'active': true,
        'startedAt': FieldValue.serverTimestamp(),
        'filterIndex': filtre,
        'retouch': rotus,
        'cameraPosition': arkaKamera ? 'back' : 'front',
        'microphoneEnabled': mikrofon,
        'cameraEnabled': kamera,
      });
      if (!mounted) return;
      devredildi = true;
      final aktifOda = oda!;
      oda = null;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => CanliYayinPage(
            oda: aktifOda,
            belgeId: belge.id,
            baslik: baslik.text.trim(),
            yayinSahibi: true,
            baslangicFiltre: filtre,
            baslangicRotus: rotus,
            baslangicArkaKamera: arkaKamera,
            baslangicMikrofon: mikrofon,
            baslangicKamera: kamera,
          ),
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Yayın başlatılamadı: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => baglaniyor = false);
    }
  }

  @override
  void dispose() {
    baslik.dispose();
    final r = oda;
    oda = null;
    if (!devredildi && r != null) unawaited(_odayiKapat(r));
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final track = _yerelVideo;
    Widget onizleme = track == null
        ? Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFF102C43), Color(0xFF301331)],
              ),
            ),
            child: Center(
              child: baglaniyor
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Icon(Icons.videocam_rounded, size: 82, color: Colors.white38),
            ),
          )
        : lk.VideoTrackRenderer(track, fit: lk.VideoViewFit.cover);
    if (track != null) {
      onizleme = ngelxAramaEfekti(
        onizleme,
        filtre,
        rotus: rotus && !arkaKamera,
        bulanik: false,
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        title: const Text('Canlı yayın ön hazırlık'),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
          children: [
            Container(
              height: 430,
              clipBehavior: Clip.antiAlias,
              decoration: BoxDecoration(
                color: const Color(0xFF15151B),
                borderRadius: BorderRadius.circular(28),
                border: Border.all(color: Colors.white12),
              ),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  onizleme,
                  Positioned(
                    top: 12,
                    left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.black54,
                        borderRadius: BorderRadius.circular(13),
                      ),
                      child: const Text(
                        'ÖNİZLEME',
                        style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w900),
                      ),
                    ),
                  ),
                  Positioned(
                    top: 10,
                    right: 10,
                    child: IconButton.filledTonal(
                      tooltip: 'Kamerayı çevir',
                      onPressed: kamera && track != null ? _kameraCevir : null,
                      icon: const Icon(Icons.cameraswitch_rounded),
                    ),
                  ),
                  Positioned(
                    left: 12,
                    right: 12,
                    bottom: 12,
                    child: SizedBox(
                      height: 54,
                      child: ListView(
                        scrollDirection: Axis.horizontal,
                        children: [
                          _CanliHazirlikButonu(
                            ikon: Icons.auto_awesome_rounded,
                            yazi: filtre == 0 ? 'Filtre' : ngelxAramaEfektAdlari[filtre],
                            secili: filtre != 0,
                            onTap: _filtreSec,
                          ),
                          const SizedBox(width: 8),
                          _CanliHazirlikButonu(
                            ikon: Icons.face_retouching_natural_rounded,
                            yazi: 'Rötuş',
                            secili: rotus,
                            onTap: arkaKamera ? null : () => setState(() => rotus = !rotus),
                          ),
                          const SizedBox(width: 8),
                          _CanliHazirlikButonu(
                            ikon: mikrofon ? Icons.mic_rounded : Icons.mic_off_rounded,
                            yazi: mikrofon ? 'Mikrofon' : 'Sessiz',
                            secili: mikrofon,
                            onTap: _mikrofonDegistir,
                          ),
                          const SizedBox(width: 8),
                          _CanliHazirlikButonu(
                            ikon: kamera ? Icons.videocam_rounded : Icons.videocam_off_rounded,
                            yazi: kamera ? 'Kamera' : 'Kapalı',
                            secili: kamera,
                            onTap: _kameraDegistir,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: baslik,
              maxLength: 100,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.edit_rounded),
                hintText: 'Yayın başlığı yaz',
                filled: true,
                fillColor: Colors.white10,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(18),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
            const ListTile(
              contentPadding: EdgeInsets.zero,
              leading: Icon(Icons.public_rounded, color: Colors.white70),
              title: Text('Herkese açık', style: TextStyle(color: Colors.white)),
              subtitle: Text('Keşfet bölümünde görünecek', style: TextStyle(color: Colors.white54)),
            ),
            const ListTile(
              contentPadding: EdgeInsets.zero,
              leading: Icon(Icons.high_quality_rounded, color: Colors.white70),
              title: Text('Canlı yayın kalite modu', style: TextStyle(color: Colors.white)),
              subtitle: Text('360p • 20 FPS • düşük cihazlarda daha kararlı', style: TextStyle(color: Colors.white54)),
            ),
            const SizedBox(height: 10),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                backgroundColor: const Color(0xFFFF1744),
                minimumSize: const Size.fromHeight(58),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
              ),
              onPressed: baglaniyor ? null : baslat,
              icon: baglaniyor
                  ? const SizedBox(
                      width: 22,
                      height: 22,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                    )
                  : const Icon(Icons.sensors_rounded),
              label: Text(
                baglaniyor ? 'Hazırlanıyor...' : 'Canlı yayını başlat',
                style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CanliHazirlikButonu extends StatelessWidget {
  final IconData ikon;
  final String yazi;
  final bool secili;
  final VoidCallback? onTap;

  const _CanliHazirlikButonu({
    required this.ikon,
    required this.yazi,
    required this.secili,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return FilledButton.tonalIcon(
      onPressed: onTap,
      style: FilledButton.styleFrom(
        backgroundColor: secili ? const Color(0xFF6D4AFF) : Colors.black54,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      ),
      icon: Icon(ikon, size: 19),
      label: Text(yazi, style: const TextStyle(fontWeight: FontWeight.w800)),
    );
  }
}

class CanliYayinPage extends StatefulWidget {
  final lk.Room oda;
  final String belgeId;
  final String baslik;
  final bool yayinSahibi;
  final int baslangicFiltre;
  final bool baslangicRotus;
  final bool baslangicArkaKamera;
  final bool baslangicMikrofon;
  final bool baslangicKamera;

  const CanliYayinPage({
    super.key,
    required this.oda,
    required this.belgeId,
    required this.baslik,
    required this.yayinSahibi,
    this.baslangicFiltre = 0,
    this.baslangicRotus = false,
    this.baslangicArkaKamera = false,
    this.baslangicMikrofon = true,
    this.baslangicKamera = true,
  });

  @override
  State<CanliYayinPage> createState() => _CanliYayinPageState();
}

class _CanliYayinPageState extends State<CanliYayinPage> {
  final yorum = TextEditingController();
  Timer? sayac;
  StreamSubscription<DocumentSnapshot<Map<String, dynamic>>>? yayinAboneligi;
  int saniye = 0;
  late int filtre;
  late bool rotus;
  late bool arkaKamera;
  late bool mikrofonAcik;
  late bool kameraAcik;
  bool kapatildi = false;
  bool kalpIsleniyor = false;

  @override
  void initState() {
    super.initState();
    filtre = widget.baslangicFiltre;
    rotus = widget.baslangicRotus;
    arkaKamera = widget.baslangicArkaKamera;
    mikrofonAcik = widget.baslangicMikrofon;
    kameraAcik = widget.baslangicKamera;
    widget.oda.addListener(_yenile);
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => saniye++);
    });
    yayinAboneligi = FirebaseFirestore.instance
        .collection('live_streams')
        .doc(widget.belgeId)
        .snapshots()
        .listen((d) {
      final v = d.data();
      if (v == null || !mounted) return;
      final yeniFiltre = (v['filterIndex'] as num?)?.toInt() ?? filtre;
      final yeniRotus = v['retouch'] == true;
      final yeniArka = (v['cameraPosition'] ?? 'front').toString() == 'back';
      final yeniMikrofon = v['microphoneEnabled'] != false;
      final yeniKamera = v['cameraEnabled'] != false;
      if (yeniFiltre != filtre ||
          yeniRotus != rotus ||
          yeniArka != arkaKamera ||
          yeniMikrofon != mikrofonAcik ||
          yeniKamera != kameraAcik) {
        setState(() {
          filtre = yeniFiltre.clamp(0, ngelxAramaEfektAdlari.length - 1);
          rotus = yeniRotus;
          arkaKamera = yeniArka;
          mikrofonAcik = yeniMikrofon;
          kameraAcik = yeniKamera;
        });
      }
    });
  }

  void _yenile() {
    if (mounted) setState(() {});
  }

  lk.VideoTrack? _goruntu() {
    if (widget.yayinSahibi) {
      for (final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]) {
        if (!p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
      }
    } else {
      for (final katilimci in widget.oda.remoteParticipants.values) {
        for (final p in katilimci.videoTrackPublications) {
          if (p.subscribed && !p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
        }
      }
    }
    return null;
  }

  Future<void> _ayarYaz(Map<String, dynamic> veri) async {
    if (!widget.yayinSahibi) return;
    await FirebaseFirestore.instance
        .collection('live_streams')
        .doc(widget.belgeId)
        .set(veri, SetOptions(merge: true));
  }

  Future<void> _mikrofonDegistir() async {
    final yeni = !mikrofonAcik;
    try {
      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      await _ayarYaz({'microphoneEnabled': yeni});
      if (mounted) setState(() => mikrofonAcik = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Mikrofon değiştirilemedi.')),
        );
      }
    }
  }

  Future<void> _kameraDegistir() async {
    final yeni = !kameraAcik;
    try {
      await widget.oda.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: const lk.CameraCaptureOptions(
          params: lk.VideoParametersPresets.h360_169,
          maxFrameRate: 20.0,
          stopCameraCaptureOnMute: true,
        ),
      );
      await _ayarYaz({'cameraEnabled': yeni});
      if (mounted) setState(() => kameraAcik = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Kamera değiştirilemedi.')),
        );
      }
    }
  }

  Future<void> _kameraCevir() async {
    final track = _goruntu();
    if (track is! lk.LocalVideoTrack) return;
    final yeni = !arkaKamera;
    try {
      await track.setCameraPosition(yeni ? lk.CameraPosition.back : lk.CameraPosition.front);
      await _ayarYaz({'cameraPosition': yeni ? 'back' : 'front'});
      if (mounted) setState(() => arkaKamera = yeni);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Kamera yönü değiştirilemedi.')),
        );
      }
    }
  }

  Future<void> _filtreSec() async {
    final secim = await showModalBottomSheet<int>(
      context: context,
      backgroundColor: const Color(0xFF14111D),
      showDragHandle: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 2, 16, 22),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Canlı yayın filtresi',
                style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 14),
              SizedBox(
                height: 96,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  itemCount: ngelxAramaEfektAdlari.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 8),
                  itemBuilder: (_, i) => InkWell(
                    onTap: () => Navigator.pop(c, i),
                    borderRadius: BorderRadius.circular(18),
                    child: Container(
                      width: 78,
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: i == filtre ? const Color(0xFF352154) : const Color(0xFF211837),
                        borderRadius: BorderRadius.circular(18),
                        border: Border.all(
                          color: i == filtre ? const Color(0xFF9C73FF) : Colors.white10,
                        ),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.auto_awesome_rounded, color: Colors.white, size: 27),
                          const SizedBox(height: 7),
                          Text(
                            ngelxAramaEfektAdlari[i],
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(
                              color: i == filtre ? const Color(0xFFCDB9FF) : Colors.white70,
                              fontSize: 10,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    if (secim == null) return;
    await _ayarYaz({'filterIndex': secim});
    if (mounted) setState(() => filtre = secim);
  }

  Future<void> _rotusDegistir() async {
    if (arkaKamera) return;
    final yeni = !rotus;
    await _ayarYaz({'retouch': yeni});
    if (mounted) setState(() => rotus = yeni);
  }

  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;
    if (widget.yayinSahibi) {
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set(
        {'active': false, 'endedAt': FieldValue.serverTimestamp()},
        SetOptions(merge: true),
      );
    }
    await widget.oda.disconnect();
    await widget.oda.dispose();
    if (geriDon && mounted) Navigator.pop(context);
  }

  Future<bool> _geri() async {
    if (widget.yayinSahibi) {
      final onay = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog(
              title: const Text('Yayın bitsin mi?'),
              content: const Text('Canlı yayın tüm izleyiciler için kapanacak.'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context, false),
                  child: const Text('Devam et'),
                ),
                FilledButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: const Text('Yayını bitir'),
                ),
              ],
            ),
          ) ??
          false;
      if (!onay) return false;
    }
    await _bitir(geriDon: false);
    return true;
  }

  Future<void> _kalpDegistir() async {
    if (kalpIsleniyor) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    kalpIsleniyor = true;
    final ref = FirebaseFirestore.instance
        .collection('live_streams')
        .doc(widget.belgeId)
        .collection('reactions')
        .doc(user.uid);
    try {
      final mevcut = await ref.get();
      if (mevcut.exists) {
        await ref.delete();
      } else {
        await ref.set({
          'uid': user.uid,
          'type': 'heart',
          'createdAt': FieldValue.serverTimestamp(),
        });
      }
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Canlı yayın tepkisi gönderilemedi.')),
        );
      }
    } finally {
      kalpIsleniyor = false;
    }
  }

  Future<void> _yorumGonder() async {
    final metin = yorum.text.trim();
    final user = FirebaseAuth.instance.currentUser;
    if (metin.isEmpty || user == null) return;
    yorum.clear();
    final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    await FirebaseFirestore.instance
        .collection('live_streams')
        .doc(widget.belgeId)
        .collection('comments')
        .add({
      'uid': user.uid,
      'username': (profil.data()?['username'] ?? 'ngelx').toString(),
      'text': metin,
      'createdAt': FieldValue.serverTimestamp(),
    });
  }

  @override
  void dispose() {
    sayac?.cancel();
    yayinAboneligi?.cancel();
    yorum.dispose();
    widget.oda.removeListener(_yenile);
    if (!kapatildi) unawaited(_bitir(geriDon: false));
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final track = _goruntu();
    final dakika = (saniye ~/ 60).toString().padLeft(2, '0');
    final sn = (saniye % 60).toString().padLeft(2, '0');

    Widget goruntu = track == null
        ? const Center(child: CircularProgressIndicator())
        : lk.VideoTrackRenderer(track, fit: lk.VideoViewFit.cover);
    if (track != null) {
      goruntu = ngelxAramaEfekti(
        goruntu,
        filtre,
        rotus: rotus && !arkaKamera,
        bulanik: false,
      );
    }

    return WillPopScope(
      onWillPop: _geri,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(
          children: [
            Positioned.fill(child: goruntu),
            Positioned.fill(
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Colors.black54, Colors.transparent, Colors.black.withOpacity(.8)],
                  ),
                ),
              ),
            ),
            SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFF1744),
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: const Text(
                            '● CANLI',
                            style: TextStyle(fontWeight: FontWeight.w900),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.black45,
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: Text('$dakika:$sn'),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.black45,
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: Text('👁 ${widget.oda.remoteParticipants.length}'),
                        ),
                        const Spacer(),
                        IconButton(
                          onPressed: () async {
                            if (await _geri() && mounted) Navigator.pop(context);
                          },
                          icon: const Icon(Icons.close_rounded, size: 31),
                        ),
                      ],
                    ),
                    const Spacer(),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Container(
                        constraints: const BoxConstraints(maxWidth: 330, maxHeight: 210),
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.black38,
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                          stream: FirebaseFirestore.instance
                              .collection('live_streams')
                              .doc(widget.belgeId)
                              .collection('comments')
                              .orderBy('createdAt', descending: true)
                              .limit(20)
                              .snapshots(),
                          builder: (_, snap) {
                            final yorumlar = snap.data?.docs ?? [];
                            if (yorumlar.isEmpty) {
                              return Text(
                                widget.baslik,
                                style: const TextStyle(fontWeight: FontWeight.w800),
                              );
                            }
                            return ListView.builder(
                              reverse: true,
                              shrinkWrap: true,
                              itemCount: yorumlar.length,
                              itemBuilder: (_, i) {
                                final y = yorumlar[i].data();
                                return Padding(
                                  padding: const EdgeInsets.symmetric(vertical: 3),
                                  child: Text('@${y['username'] ?? 'ngelx'}  ${y['text'] ?? ''}'),
                                );
                              },
                            );
                          },
                        ),
                      ),
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: yorum,
                            onSubmitted: (_) => _yorumGonder(),
                            decoration: InputDecoration(
                              hintText: 'Yorum yaz...',
                              filled: true,
                              fillColor: Colors.black54,
                              suffixIcon: IconButton(
                                onPressed: _yorumGonder,
                                icon: const Icon(Icons.send_rounded),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        if (widget.yayinSahibi)
                          SizedBox(
                            width: 228,
                            height: 48,
                            child: ListView(
                              scrollDirection: Axis.horizontal,
                              children: [
                                IconButton.filled(
                                  tooltip: 'Mikrofon',
                                  onPressed: _mikrofonDegistir,
                                  icon: Icon(mikrofonAcik ? Icons.mic : Icons.mic_off),
                                ),
                                const SizedBox(width: 6),
                                IconButton.filled(
                                  tooltip: 'Kamera',
                                  onPressed: _kameraDegistir,
                                  icon: Icon(kameraAcik ? Icons.videocam : Icons.videocam_off),
                                ),
                                const SizedBox(width: 6),
                                IconButton.filled(
                                  tooltip: 'Kamerayı çevir',
                                  onPressed: kameraAcik ? _kameraCevir : null,
                                  icon: const Icon(Icons.cameraswitch_rounded),
                                ),
                                const SizedBox(width: 6),
                                IconButton.filled(
                                  tooltip: 'Filtre',
                                  onPressed: _filtreSec,
                                  icon: const Icon(Icons.auto_awesome_rounded),
                                ),
                                const SizedBox(width: 6),
                                IconButton.filled(
                                  tooltip: 'Rötuş',
                                  onPressed: arkaKamera ? null : _rotusDegistir,
                                  icon: Icon(
                                    Icons.face_retouching_natural_rounded,
                                    color: rotus ? const Color(0xFFFFC4F3) : null,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                FilledButton(
                                  style: FilledButton.styleFrom(
                                    backgroundColor: const Color(0xFFFF1744),
                                  ),
                                  onPressed: () async {
                                    if (await _geri() && mounted) Navigator.pop(context);
                                  },
                                  child: const Text('Bitir'),
                                ),
                              ],
                            ),
                          )
                        else
                          StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                            stream: FirebaseFirestore.instance
                                .collection('live_streams')
                                .doc(widget.belgeId)
                                .collection('reactions')
                                .snapshots(),
                            builder: (_, s) {
                              final user = FirebaseAuth.instance.currentUser;
                              final benim = user != null &&
                                  (s.data?.docs ?? []).any((d) => d.id == user.uid);
                              final sayi = s.data?.docs.length ?? 0;
                              return FilledButton.tonalIcon(
                                onPressed: kalpIsleniyor ? null : _kalpDegistir,
                                icon: Icon(
                                  benim
                                      ? Icons.favorite_rounded
                                      : Icons.favorite_border_rounded,
                                  color: Colors.redAccent,
                                ),
                                label: Text(sayi > 0 ? '$sayi' : 'Beğen'),
                              );
                            },
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''

start = main.index('class CanliHazirlikPage extends StatefulWidget {')
end = main.index('class YuklePage extends StatefulWidget {', start)
main = main[:start] + new_block + '\n\n' + main[end:]

main = re.sub(
    r"const ngelxVersionName = String\.fromEnvironment\('NGELX_VERSION_NAME', defaultValue: '[^']+'\);",
    "const ngelxVersionName = String.fromEnvironment('NGELX_VERSION_NAME', defaultValue: '1.0.104');",
    main,
    count=1,
)
main = re.sub(
    r"const ngelxBuildNumber = String\.fromEnvironment\('NGELX_BUILD_NUMBER', defaultValue: '[^']+'\);",
    "const ngelxBuildNumber = String.fromEnvironment('NGELX_BUILD_NUMBER', defaultValue: '323');",
    main,
    count=1,
)
pub = re.sub(r'^version:\s*[^\n]+$', 'version: 1.0.104+323', pub, count=1, flags=re.M)

main_path.write_text(main, encoding='utf-8')
pub_path.write_text(pub, encoding='utf-8')
print('Build 323 live preflight patch applied.')
