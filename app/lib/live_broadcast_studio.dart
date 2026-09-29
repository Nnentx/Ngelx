part of 'main.dart';

class CanliHazirlikPage extends StatefulWidget {
  const CanliHazirlikPage({super.key});
  @override
  State<CanliHazirlikPage> createState() => _CanliHazirlikPageState();
}

class _CanliHazirlikPageState extends State<CanliHazirlikPage> {
  final baslik = TextEditingController();
  bool baglaniyor = false;
  bool mikrofon = true;
  bool kamera = true;
  bool onizlemeHazirlaniyor = true;
  bool arkaKamera = false;
  bool flashAcik = false;
  double retus = .18;
  int filtreIndex = 0;
  String oran = '9:16';
  String kalite = '720p';
  String gizlilik = 'Herkese açık';
  String kategori = 'Sohbet';
  int fps = 30;
  bool geriSayim = true;
  int baslangicSayaci = 0;
  String? kameraHatasi;
  List<CameraDescription> kameralar = <CameraDescription>[];
  CameraController? onizleme;

  @override
  void initState() {
    super.initState();
    unawaited(_onizlemeyiBaslat());
  }

  @override
  void dispose() {
    final controller = onizleme;
    onizleme = null;
    if (controller != null) unawaited(controller.dispose());
    baslik.dispose();
    super.dispose();
  }

  ResolutionPreset get _onizlemeKalitesi => switch (kalite) {
    '540p' => ResolutionPreset.medium,
    '1080p' => ResolutionPreset.veryHigh,
    _ => ResolutionPreset.high,
  };

  lk.VideoParameters get _yayinKalitesi => switch (kalite) {
    '540p' => lk.VideoParametersPresets.h540_169,
    '1080p' => lk.VideoParametersPresets.h1080_169,
    _ => lk.VideoParametersPresets.h720_169,
  };

  lk.CameraCaptureOptions get _kameraAyarlari => lk.CameraCaptureOptions(
    cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front,
    params: _yayinKalitesi,
    maxFrameRate: fps.toDouble(),
    stopCameraCaptureOnMute: true,
  );

  Future<void> _onizlemeyiBaslat() async {
    if (!kamera || baglaniyor) return;
    if (mounted) setState(() { onizlemeHazirlaniyor = true; kameraHatasi = null; });
    try {
      final izin = await Permission.camera.request();
      if (!izin.isGranted) throw Exception('Kamera izni verilmedi.');
      kameralar = await availableCameras();
      if (kameralar.isEmpty) throw Exception('Bu cihazda kullanılabilir kamera bulunamadı.');
      var secilen = kameralar.indexWhere((k) => k.lensDirection == (arkaKamera ? CameraLensDirection.back : CameraLensDirection.front));
      if (secilen < 0) secilen = 0;
      arkaKamera = kameralar[secilen].lensDirection == CameraLensDirection.back;
      final eski = onizleme;
      onizleme = null;
      if (eski != null) {
        try { await eski.dispose(); } catch (_) {}
        await Future<void>.delayed(const Duration(milliseconds: 140));
      }
      final yeni = CameraController(kameralar[secilen], _onizlemeKalitesi, enableAudio: false, imageFormatGroup: ImageFormatGroup.jpeg);
      await yeni.initialize();
      if (!arkaKamera) flashAcik = false;
      try { await yeni.setFlashMode(flashAcik ? FlashMode.torch : FlashMode.off); } catch (_) { flashAcik = false; }
      if (!mounted) { await yeni.dispose(); return; }
      onizleme = yeni;
      setState(() => onizlemeHazirlaniyor = false);
    } catch (e) {
      if (mounted) setState(() { onizlemeHazirlaniyor = false; kameraHatasi = e.toString().replaceFirst('Exception: ', ''); });
    }
  }

  Future<void> _kamerayiAcKapat(bool acik) async {
    if (baglaniyor) return;
    setState(() { kamera = acik; flashAcik = false; });
    if (acik) {
      await _onizlemeyiBaslat();
    } else {
      final eski = onizleme;
      onizleme = null;
      if (eski != null) await eski.dispose();
      if (mounted) setState(() => onizlemeHazirlaniyor = false);
    }
  }

  Future<void> _kamerayiCevir() async {
    if (baglaniyor || !kamera || onizlemeHazirlaniyor || kameralar.length < 2) return;
    setState(() { arkaKamera = !arkaKamera; flashAcik = false; });
    await _onizlemeyiBaslat();
  }

  Future<void> _flasiDegistir() async {
    final c = onizleme;
    if (c == null || !c.value.isInitialized || !arkaKamera) return;
    final yeni = !flashAcik;
    try {
      await c.setFlashMode(yeni ? FlashMode.torch : FlashMode.off);
      if (mounted) setState(() => flashAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Bu cihaz canlı önizlemede flaşı desteklemiyor.')));
    }
  }

  Future<void> _kaliteDegistir(String yeni) async {
    if (yeni == kalite || baglaniyor) return;
    setState(() => kalite = yeni);
    if (kamera) await _onizlemeyiBaslat();
  }

  Widget _kameraOnizlemesi() {
    final c = onizleme;
    if (!kamera) return const ColoredBox(color: Color(0xFF151515), child: Center(child: Icon(Icons.videocam_off_rounded, size: 72, color: Colors.white38)));
    if (onizlemeHazirlaniyor) return const ColoredBox(color: Color(0xFF151515), child: Center(child: CircularProgressIndicator(color: Colors.white)));
    if (c == null || !c.value.isInitialized) {
      return ColoredBox(color: const Color(0xFF151515), child: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisSize: MainAxisSize.min, children: [
        const Icon(Icons.no_photography_rounded, size: 54, color: Colors.white54),
        const SizedBox(height: 12),
        Text(kameraHatasi ?? 'Kamera önizlemesi açılamadı.', textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70)),
        const SizedBox(height: 12),
        OutlinedButton(onPressed: _onizlemeyiBaslat, child: const Text('Tekrar dene')),
      ]))));
    }
    final filtre = ngelxKameraFiltreleri[filtreIndex];
    return ColorFiltered(
      colorFilter: ColorFilter.matrix(filtre.matris),
      child: Stack(fit: StackFit.expand, children: [
        FittedBox(
          fit: BoxFit.cover,
          child: SizedBox(width: c.value.previewSize?.height ?? 720, height: c.value.previewSize?.width ?? 1280, child: CameraPreview(c)),
        ),
        if (retus > .01) IgnorePointer(child: ColoredBox(color: Colors.white.withOpacity(retus * .12))),
      ]),
    );
  }

  Future<void> _geriSayimCalistir() async {
    for (var i = 3; i >= 1; i--) {
      if (!mounted) return;
      setState(() => baslangicSayaci = i);
      await Future<void>.delayed(const Duration(milliseconds: 700));
    }
    if (mounted) setState(() => baslangicSayaci = 0);
  }

  Future<void> baslat() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.isAnonymous || baglaniyor) return;
    if (baslik.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('En az 3 karakterlik yayın başlığı yaz.')));
      return;
    }
    if (mikrofon) {
      final izin = await Permission.microphone.request();
      if (!izin.isGranted) {
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mikrofon açık başlayacaksa mikrofon izni vermelisin.')));
        return;
      }
    }
    setState(() => baglaniyor = true);
    if (geriSayim) await _geriSayimCalistir();
    lk.Room? oda;
    try {
      final eskiOnizleme = onizleme;
      onizleme = null;
      if (eskiOnizleme != null) {
        try { await eskiOnizleme.setFlashMode(FlashMode.off); } catch (_) {}
        await eskiOnizleme.dispose();
        await Future<void>.delayed(const Duration(milliseconds: 180));
      }
      final odaAdi = 'ngelx_${user.uid}_${DateTime.now().millisecondsSinceEpoch}';
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();
      final kaynak = lk.DevelopmentTokenSource(id: liveKitTestSunucuId);
      final cevap = await kaynak.fetch(lk.TokenRequestOptions(
        roomName: odaAdi,
        participantIdentity: user.uid,
        participantName: ad,
        participantAttributes: const {'role': 'host'},
      ));
      oda = lk.Room(roomOptions: lk.RoomOptions(
        adaptiveStream: true,
        dynacast: true,
        defaultCameraCaptureOptions: _kameraAyarlari,
      ));
      await oda.connect(cevap.serverUrl, cevap.participantToken);
      final yerelKatilimci = oda.localParticipant;
      if (yerelKatilimci == null) throw Exception('Canlı yayın katılımcısı hazırlanamadı.');
      if (kamera) await yerelKatilimci.setCameraEnabled(true, cameraCaptureOptions: _kameraAyarlari);
      if (mikrofon) await yerelKatilimci.setMicrophoneEnabled(true);
      final belge = await FirebaseFirestore.instance.collection('live_streams').add({
        'roomName': odaAdi,
        'ownerId': user.uid,
        'username': ad,
        'title': baslik.text.trim(),
        'active': true,
        'startedAt': FieldValue.serverTimestamp(),
        'cameraPosition': arkaKamera ? 'back' : 'front',
        'microphoneEnabled': mikrofon,
        'cameraEnabled': kamera,
        'filter': ngelxKameraFiltreleri[filtreIndex].ad,
        'retouch': retus,
        'aspectRatio': oran,
        'quality': kalite,
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
      }, SetOptions(merge: true));
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => CanliYayinPage(
        oda: oda!,
        belgeId: belge.id,
        baslik: baslik.text.trim(),
        yayinSahibi: true,
        ilkArkaKamera: arkaKamera,
        ilkMikrofonAcik: mikrofon,
        ilkKameraAcik: kamera,
        kameraAyarlari: _kameraAyarlari,
        ownerId: user.uid,
        username: ad,
      )));
    } catch (e) {
      if (oda != null) {
        await oda.disconnect();
        await oda.dispose();
      }
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Yayın başlatılamadı: $e')));
    } finally {
      if (mounted) {
        setState(() => baglaniyor = false);
        if (ModalRoute.of(context)?.isCurrent == true && kamera && onizleme == null) unawaited(_onizlemeyiBaslat());
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final onizlemeOrani = switch (oran) { '1:1' => 1.0, '16:9' => 16 / 9, _ => 9 / 16 };
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(backgroundColor: Colors.white, foregroundColor: Colors.black, title: const Text('Canlı yayın hazırla')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(18, 8, 18, 28),
          children: [
            Center(child: ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 430),
              child: AspectRatio(
                aspectRatio: onizlemeOrani,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(28),
                  child: Stack(fit: StackFit.expand, children: [
                    _kameraOnizlemesi(),
                    Positioned(top: 12, left: 12, child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 7),
                      decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(14)),
                      child: Text('${arkaKamera ? 'Arka' : 'Ön'} kamera • $kalite', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700)),
                    )),
                    if (baslangicSayaci > 0) Center(child: Container(
                      width: 92, height: 92,
                      decoration: BoxDecoration(color: Colors.black54, shape: BoxShape.circle, border: Border.all(color: Colors.white70, width: 2)),
                      alignment: Alignment.center,
                      child: Text('$baslangicSayaci', style: const TextStyle(color: Colors.white, fontSize: 52, fontWeight: FontWeight.w900)),
                    )),
                    Positioned(top: 8, right: 8, child: Row(children: [
                      IconButton.filledTonal(onPressed: kamera && !onizlemeHazirlaniyor && kameralar.length > 1 ? _kamerayiCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: const Icon(Icons.cameraswitch_rounded)),
                      const SizedBox(width: 5),
                      IconButton.filledTonal(onPressed: kamera && arkaKamera && !onizlemeHazirlaniyor ? _flasiDegistir : null, tooltip: 'Flaş', icon: Icon(flashAcik ? Icons.flash_on_rounded : Icons.flash_off_rounded)),
                    ])),
                  ]),
                ),
              ),
            )),
            const SizedBox(height: 18),
            TextField(controller: baslik, maxLength: 100, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w600), decoration: InputDecoration(prefixIcon: const Icon(Icons.edit_rounded, color: Colors.black54), hintText: 'Yayın başlığı yaz', hintStyle: const TextStyle(color: Colors.black45, fontWeight: FontWeight.w600), filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none))),
            const Text('NgelX filtreleri', style: TextStyle(color: Colors.black87, fontSize: 16, fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            SizedBox(height: 42, child: ListView.separated(
              padding: const EdgeInsets.only(right: 22),
              scrollDirection: Axis.horizontal,
              itemCount: ngelxKameraFiltreleri.length,
              separatorBuilder: (_, __) => const SizedBox(width: 7),
              itemBuilder: (_, i) => ChoiceChip(label: Text(ngelxKameraFiltreleri[i].ad), selected: filtreIndex == i, onSelected: baglaniyor ? null : (_) => setState(() => filtreIndex = i)),
            )),
            const SizedBox(height: 12),
            Row(children: [
              const Icon(Icons.auto_fix_high_rounded, color: Color(0xFFE91E63)),
              const SizedBox(width: 9),
              const Text('Doğal rötuş', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)),
              Expanded(child: Slider(value: retus, min: 0, max: 1, divisions: 10, label: '%${(retus * 100).round()}', onChanged: baglaniyor ? null : (v) => setState(() => retus = v))),
              SizedBox(width: 38, child: Text('%${(retus * 100).round()}', style: const TextStyle(color: Colors.black54, fontWeight: FontWeight.w700))),
            ]),
            Row(children: [
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
            const SizedBox(height: 8),
            SwitchListTile(contentPadding: EdgeInsets.zero, value: kamera, onChanged: baglaniyor ? null : _kamerayiAcKapat, secondary: Icon(kamera ? Icons.videocam_rounded : Icons.videocam_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Kamera', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: const Text('Seçimler yayını otomatik başlatmaz.')),
            SwitchListTile(contentPadding: EdgeInsets.zero, value: mikrofon, onChanged: baglaniyor ? null : (v) => setState(() => mikrofon = v), secondary: Icon(mikrofon ? Icons.mic_rounded : Icons.mic_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Mikrofon', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700))),
            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text(gizlilik, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('$kategori • ${fps} FPS • $kalite')),
            const SizedBox(height: 16),
            FilledButton.icon(
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744), minimumSize: const Size.fromHeight(58), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22))),
              onPressed: baglaniyor ? null : baslat,
              icon: baglaniyor ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.sensors_rounded),
              label: Text(baglaniyor ? 'Bağlanıyor...' : 'Canlı yayına başla', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
            ),
            const SizedBox(height: 10),
            const Text('Yayın yalnızca “Canlı yayını başlat” düğmesine bastığında başlar.', textAlign: TextAlign.center, style: TextStyle(color: Colors.black54)),
          ],
        ),
      ),
    );
  }

  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {
    return InputDecorator(
      decoration: InputDecoration(labelText: etiket, filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none)),
      child: DropdownButtonHideUnderline(child: DropdownButton<String>(
        value: deger,
        isDense: true,
        isExpanded: true,
        style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700),
        items: secenekler.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
        onChanged: baglaniyor ? null : (v) { if (v != null) unawaited(Future.sync(() => degisti(v))); },
      )),
    );
  }
}

class CanliYayinPage extends StatefulWidget {
  final lk.Room oda;
  final String belgeId;
  final String baslik;
  final bool yayinSahibi;
  final bool ilkArkaKamera;
  final bool ilkMikrofonAcik;
  final bool ilkKameraAcik;
  final lk.CameraCaptureOptions kameraAyarlari;
  final String ownerId;
  final String username;
  const CanliYayinPage({
    super.key,
    required this.oda,
    required this.belgeId,
    required this.baslik,
    required this.yayinSahibi,
    this.ilkArkaKamera = false,
    this.ilkMikrofonAcik = true,
    this.ilkKameraAcik = true,
    this.kameraAyarlari = const lk.CameraCaptureOptions(),
    this.ownerId = '',
    this.username = 'ngelx',
  });
  @override
  State<CanliYayinPage> createState() => _CanliYayinPageState();
}

class _CanliYayinPageState extends State<CanliYayinPage> {
  final yorum = TextEditingController();
  Timer? sayac;
  int saniye = 0;
  bool mikrofonAcik = true;
  bool kameraAcik = true;
  bool kapatildi = false;
  bool kalpIsleniyor = false;
  bool arkaKamera = false;
  bool kameraDegisiyor = false;
  bool hediyeGonderiliyor = false;
  bool katilimKaydiYapildi = false;
  int maxIzleyici = 0;
  int yerelKalpSerisi = 0;

  @override
  void initState() {
    super.initState();
    arkaKamera = widget.ilkArkaKamera;
    mikrofonAcik = widget.ilkMikrofonAcik;
    kameraAcik = widget.ilkKameraAcik;
    widget.oda.addListener(_yenile);
    if (!widget.yayinSahibi) unawaited(_katildimKaydet());
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      final izleyici = widget.oda.remoteParticipants.length;
      if (izleyici > maxIzleyici) maxIzleyici = izleyici;
      if (mounted) setState(() => saniye++);
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

  lk.LocalVideoTrack? _yerelKameraTrack() {
    for (final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]) {
      if (p.track is lk.LocalVideoTrack) return p.track as lk.LocalVideoTrack;
    }
    return null;
  }

  Future<void> _yayinKamerasiniCevir() async {
    if (!widget.yayinSahibi || !kameraAcik || kameraDegisiyor) return;
    final track = _yerelKameraTrack();
    if (track == null) return;
    final yeniArka = !arkaKamera;
    setState(() => kameraDegisiyor = true);
    try {
      await track.restartTrack(widget.kameraAyarlari.copyWith(cameraPosition: yeniArka ? lk.CameraPosition.back : lk.CameraPosition.front));
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'cameraPosition': yeniArka ? 'back' : 'front'}, SetOptions(merge: true));
      if (mounted) setState(() => arkaKamera = yeniArka);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Kamera değiştirilemedi; yayın bağlantısı korunuyor.')));
    } finally {
      if (mounted) setState(() => kameraDegisiyor = false);
    }
  }

  Future<void> _yayinMikrofonunuDegistir() async {
    final yeni = !mikrofonAcik;
    try {
      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      if (mounted) setState(() => mikrofonAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mikrofon ayarı değiştirilemedi.')));
    }
  }

  Future<void> _yayinKamerasiniAcKapat() async {
    final yeni = !kameraAcik;
    try {
      await widget.oda.localParticipant?.setCameraEnabled(
        yeni,
        cameraCaptureOptions: widget.kameraAyarlari.copyWith(cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front),
      );
      if (mounted) setState(() => kameraAcik = yeni);
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Kamera ayarı değiştirilemedi.')));
    }
  }

  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;
    if (widget.yayinSahibi) {
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
    }
    await widget.oda.disconnect();
    await widget.oda.dispose();
    if (geriDon && mounted) Navigator.pop(context);
  }

  Future<bool> _geri() async {
    if (widget.yayinSahibi) {
      final onay = await showDialog<bool>(context: context, builder: (_) => AlertDialog(
        title: const Text('Yayın bitsin mi?'),
        content: const Text('Canlı yayın tüm izleyiciler için kapanacak.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Devam et')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Yayını bitir')),
        ],
      )) ?? false;
      if (!onay) return false;
    }
    await _bitir(geriDon: false);
    return true;
  }

  Future<Map<String, dynamic>> _aktifProfil() async {
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
    if(kalpIsleniyor)return;
    final user=FirebaseAuth.instance.currentUser;
    if(user==null)return;
    kalpIsleniyor=true;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').doc(user.uid);
    try{
      await FirebaseFirestore.instance.runTransaction((tx) async {
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
      if (mounted) setState(() => yerelKalpSerisi++);
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayın tepkisi gönderilemedi.')));
    }finally{
      kalpIsleniyor=false;
    }
  }

  Future<void> _yorumGonder() async {
    final metin = yorum.text.trim();
    final user = FirebaseAuth.instance.currentUser;
    if (metin.isEmpty || user == null) return;
    yorum.clear();
    final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
      'uid': user.uid,
      'userId': user.uid,
      'username': (profil.data()?['username'] ?? 'ngelx').toString(),
      'text': metin,
      'kind': 'comment',
      'createdAt': FieldValue.serverTimestamp(),
    });
  }

  @override
  void dispose() {
    sayac?.cancel();
    yorum.dispose();
    widget.oda.removeListener(_yenile);
    if (!kapatildi) _bitir(geriDon: false);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final track = _goruntu();
    final dakika = (saniye ~/ 60).toString().padLeft(2, '0');
    final sn = (saniye % 60).toString().padLeft(2, '0');
    return WillPopScope(
      onWillPop: _geri,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(children: [
          Positioned.fill(child: track == null ? const Center(child: CircularProgressIndicator()) : lk.VideoTrackRenderer(track, fit: lk.VideoViewFit.cover)),
          Positioned.fill(child: DecoratedBox(decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.black54, Colors.transparent, Colors.black.withOpacity(.8)])))),
          SafeArea(child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(children: [
              Row(children: [
                Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8), decoration: BoxDecoration(color: const Color(0xFFFF1744), borderRadius: BorderRadius.circular(14)), child: const Text('● CANLI', style: TextStyle(fontWeight: FontWeight.w900))),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('$dakika:$sn')),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('👁 ${widget.oda.remoteParticipants.length}')),
                const Spacer(),
                IconButton(onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.close_rounded, size: 31)),
              ]),
              const Spacer(),
              Align(alignment: Alignment.centerLeft, child: Container(
                constraints: const BoxConstraints(maxWidth: 330, maxHeight: 210),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(color: Colors.black38, borderRadius: BorderRadius.circular(18)),
                child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                  stream: FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').orderBy('createdAt', descending: true).limit(20).snapshots(),
                  builder: (_, snap) {
                    final yorumlar = snap.data?.docs ?? [];
                    if (yorumlar.isEmpty) return Text(widget.baslik, style: const TextStyle(fontWeight: FontWeight.w800));
                    return ListView.builder(reverse: true, shrinkWrap: true, itemCount: yorumlar.length, itemBuilder: (_, i) {
                      final y = yorumlar[i].data();
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
                      return Padding(padding: const EdgeInsets.symmetric(vertical: 3), child: Text('@${y['username'] ?? 'ngelx'}  ${y['text'] ?? ''}'));
                    });
                  },
                ),
              )),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(child: TextField(controller: yorum, onSubmitted: (_) => _yorumGonder(), decoration: InputDecoration(hintText: 'Yorum yaz...', filled: true, fillColor: Colors.black54, suffixIcon: IconButton(onPressed: _yorumGonder, icon: const Icon(Icons.send_rounded))))),
                if (!widget.yayinSahibi) ...[
                  const SizedBox(width: 8),
                  StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').snapshots(),
                    builder:(_,s){
                      final docs=s.data?.docs??[];
                      final sayi=docs.fold<int>(0,(t,d)=>t+((d.data()['count'] as num?)?.toInt()??1));
                      return FilledButton.tonalIcon(
                        onPressed:kalpIsleniyor?null:_kalpDegistir,
                        icon:const Icon(Icons.favorite_rounded,color:Colors.redAccent),
                        label:Text(sayi>0?'$sayi':'Kalp'),
                      );
                    },
                  ),
                  const SizedBox(width: 6),
                  IconButton.filledTonal(onPressed: hediyeGonderiliyor ? null : _hediyePaneli, tooltip: 'N-Hediye', icon: const Icon(Icons.card_giftcard_rounded, color: Color(0xFFFF4F93))),
                  const SizedBox(width: 4),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Paylaş', icon: const Icon(Icons.share_rounded)),
                ],
              ]),
              if (yerelKalpSerisi >= 5 && !widget.yayinSahibi)
                Padding(padding: const EdgeInsets.only(top: 6), child: Align(alignment: Alignment.centerRight, child: Text('N-Kombo x$yerelKalpSerisi ❤️', style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w800)))),
              if (widget.yayinSahibi) ...[
                const SizedBox(height: 9),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  IconButton.filled(onPressed: _yayinMikrofonunuDegistir, tooltip: mikrofonAcik ? 'Mikrofonu kapat' : 'Mikrofonu aç', icon: Icon(mikrofonAcik ? Icons.mic : Icons.mic_off)),
                  const SizedBox(width: 9),
                  IconButton.filled(onPressed: _yayinKamerasiniAcKapat, tooltip: kameraAcik ? 'Kamerayı kapat' : 'Kamerayı aç', icon: Icon(kameraAcik ? Icons.videocam : Icons.videocam_off)),
                  const SizedBox(width: 9),
                  IconButton.filled(onPressed: kameraAcik && !kameraDegisiyor ? _yayinKamerasiniCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: kameraDegisiyor ? const SizedBox(width: 19, height: 19, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.cameraswitch_rounded)),
                  const SizedBox(width: 9),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Yayını paylaş', icon: const Icon(Icons.share_rounded)),
                  const SizedBox(width: 9),
                  FilledButton.icon(style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744)), onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.stop_circle_outlined), label: const Text('Bitir')),
                ]),
              ],
            ]),
          )),
        ]),
      ),
    );
  }
}

