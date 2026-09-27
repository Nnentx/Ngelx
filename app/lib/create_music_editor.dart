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

class NgelXMedyaYaziAyariSheet extends StatefulWidget{
  final String yazi;
  final int renk;
  final int arkaPlanRenk;
  final double boyut;
  const NgelXMedyaYaziAyariSheet({
    super.key,
    this.yazi='',
    this.renk=0xFFFFFFFF,
    this.arkaPlanRenk=0x99000000,
    this.boyut=22,
  });
  @override State<NgelXMedyaYaziAyariSheet> createState()=>_NgelXMedyaYaziAyariSheetState();
}

class _NgelXMedyaYaziAyariSheetState extends State<NgelXMedyaYaziAyariSheet>{
  late final TextEditingController kontrol;
  late int renk;
  late int arkaPlanRenk;
  late double boyut;
  static const renkler=<int>[
    0xFFFFFFFF,0xFF111111,0xFFFF3B30,0xFFFFD60A,0xFF0A84FF,
    0xFF30D158,0xFFBF5AF2,0xFF64D2FF,0xFFFF9F0A,0xFFFF2D55,
  ];

  @override void initState(){
    super.initState();
    kontrol=TextEditingController(text:widget.yazi);
    renk=widget.renk;
    arkaPlanRenk=widget.arkaPlanRenk;
    boyut=widget.boyut.clamp(14,54).toDouble();
  }
  @override void dispose(){kontrol.dispose();super.dispose();}

  @override Widget build(BuildContext context){
    return Theme(
      data:ThemeData.light(),
      child:SafeArea(
        top:false,
        child:Padding(
          padding:EdgeInsets.fromLTRB(18,16,18,MediaQuery.viewInsetsOf(context).bottom+18),
          child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[
            const Text('Yazıyı düzenle',style:TextStyle(fontSize:21,fontWeight:FontWeight.w900)),
            const SizedBox(height:12),
            TextField(
              controller:kontrol,autofocus:true,maxLength:120,maxLines:3,
              style:TextStyle(color:Color(renk),fontSize:boyut,fontWeight:FontWeight.w800),
              decoration:InputDecoration(
                hintText:'Yazını ekle',
                filled:true,fillColor:const Color(0xFFF3F4F7),
                border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none),
              ),
            ),
            const SizedBox(height:6),
            const Text('Yazı rengi',style:TextStyle(fontWeight:FontWeight.w800)),
            const SizedBox(height:8),
            Wrap(spacing:9,runSpacing:9,children:renkler.map((c)=>InkWell(
              onTap:()=>setState(()=>renk=c),
              borderRadius:BorderRadius.circular(24),
              child:Container(
                width:34,height:34,
                decoration:BoxDecoration(
                  color:Color(c),shape:BoxShape.circle,
                  border:Border.all(color:renk==c?mor:Colors.black12,width:renk==c?3:1),
                ),
                child:renk==c?Icon(Icons.check_rounded,color:c==0xFFFFFFFF?Colors.black:Colors.white,size:19):null,
              ),
            )).toList()),
            const SizedBox(height:12),
            Row(children:[
              const Expanded(child:Text('Yazı arka planı',style:TextStyle(fontWeight:FontWeight.w800))),
              Switch(
                value:arkaPlanRenk!=0,
                onChanged:(v)=>setState(()=>arkaPlanRenk=v?0x99000000:0),
              ),
            ]),
            Row(children:[
              const Text('Boyut',style:TextStyle(fontWeight:FontWeight.w800)),
              Expanded(child:Slider(
                min:14,max:54,value:boyut,
                onChanged:(v)=>setState(()=>boyut=v),
              )),
              SizedBox(width:42,child:Text(boyut.round().toString(),textAlign:TextAlign.right)),
            ]),
            const SizedBox(height:6),
            Row(children:[
              TextButton(onPressed:()=>Navigator.pop(context),child:const Text('Vazgeç')),
              TextButton(onPressed:()=>Navigator.pop(context,<String,dynamic>{'text':'','color':renk,'backgroundColor':arkaPlanRenk,'fontSize':boyut}),child:const Text('Temizle')),
              const Spacer(),
              FilledButton(
                onPressed:()=>Navigator.pop(context,<String,dynamic>{
                  'text':kontrol.text.trim(),
                  'color':renk,
                  'backgroundColor':arkaPlanRenk,
                  'fontSize':boyut,
                }),
                child:const Text('Uygula'),
              ),
            ]),
          ]),
        ),
      ),
    );
  }
}

class NgelXSuruklenebilirYaziKatmani extends StatefulWidget{
  final String yazi;
  final int renk,arkaPlanRenk;
  final double boyut,x,y,scale,rotation,canvasWidth,canvasHeight;
  final void Function(double x,double y,double scale,double rotation) onChanged;
  const NgelXSuruklenebilirYaziKatmani({
    super.key,
    required this.yazi,
    required this.renk,
    required this.arkaPlanRenk,
    required this.boyut,
    required this.x,
    required this.y,
    required this.scale,
    required this.rotation,
    required this.canvasWidth,
    required this.canvasHeight,
    required this.onChanged,
  });
  @override State<NgelXSuruklenebilirYaziKatmani> createState()=>_NgelXSuruklenebilirYaziKatmaniState();
}

class _NgelXSuruklenebilirYaziKatmaniState extends State<NgelXSuruklenebilirYaziKatmani>{
  double basScale=1,basRotation=0;
  @override Widget build(BuildContext context){
    if(widget.yazi.trim().isEmpty)return const SizedBox.shrink();
    return Align(
      alignment:Alignment(widget.x.clamp(-.95,.95),widget.y.clamp(-.95,.95)),
      child:Transform.rotate(
        angle:widget.rotation,
        child:Transform.scale(
          scale:widget.scale.clamp(.45,3.2),
          child:GestureDetector(
            behavior:HitTestBehavior.opaque,
            onScaleStart:(_){basScale=widget.scale;basRotation=widget.rotation;},
            onScaleUpdate:(d){
              final nx=(widget.x+d.focalPointDelta.dx/math.max(1,widget.canvasWidth/2)).clamp(-.95,.95).toDouble();
              final ny=(widget.y+d.focalPointDelta.dy/math.max(1,widget.canvasHeight/2)).clamp(-.95,.95).toDouble();
              final ns=(basScale*d.scale).clamp(.45,3.2).toDouble();
              final nr=basRotation+d.rotation;
              widget.onChanged(nx,ny,ns,nr);
            },
            child:Container(
              padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
              decoration:BoxDecoration(
                color:widget.arkaPlanRenk==0?Colors.transparent:Color(widget.arkaPlanRenk),
                borderRadius:BorderRadius.circular(12),
              ),
              child:Text(
                widget.yazi,
                textAlign:TextAlign.center,
                style:TextStyle(
                  color:Color(widget.renk),
                  fontSize:widget.boyut,
                  fontWeight:FontWeight.w900,
                  shadows:const [Shadow(color:Colors.black45,blurRadius:3,offset:Offset(0,1))],
                ),
              ),
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
  final int yaziRenk;
  final int yaziArkaPlanRenk;
  final double yaziBoyut,yaziX,yaziY,yaziScale,yaziRotation;
  const NgelXVideoDuzenlemePage({
    super.key,
    required this.dosya,
    this.baslangicMs = 0,
    this.bitisMs = 0,
    this.yazi = '',
    this.yaziRenk=0xFFFFFFFF,
    this.yaziArkaPlanRenk=0x99000000,
    this.yaziBoyut=22,
    this.yaziX=0,
    this.yaziY=0,
    this.yaziScale=1,
    this.yaziRotation=0,
  });

  @override
  State<NgelXVideoDuzenlemePage> createState() => _NgelXVideoDuzenlemePageState();
}

class _NgelXVideoDuzenlemePageState extends State<NgelXVideoDuzenlemePage> {
  late final VideoPlayerController kontrol;
  late final TextEditingController yazi;
  bool hazir = false;
  bool oynuyor = false;
  bool trimOncesiOynuyordu=false;
  double bas = 0;
  double son = 1;
  double toplam = 1;
  late int yaziRenk,yaziArkaPlanRenk;
  late double yaziBoyut,yaziX,yaziY,yaziScale,yaziRotation;
  Timer? seekTimer;

  static const renkler=<int>[
    0xFFFFFFFF,0xFF111111,0xFFFF3B30,0xFFFFD60A,0xFF0A84FF,
    0xFF30D158,0xFFBF5AF2,0xFF64D2FF,0xFFFF9F0A,0xFFFF2D55,
  ];

  @override
  void initState() {
    super.initState();
    yazi = TextEditingController(text: widget.yazi);
    yaziRenk=widget.yaziRenk;
    yaziArkaPlanRenk=widget.yaziArkaPlanRenk;
    yaziBoyut=widget.yaziBoyut;
    yaziX=widget.yaziX;yaziY=widget.yaziY;yaziScale=widget.yaziScale;yaziRotation=widget.yaziRotation;
    kontrol = VideoPlayerController.file(File(widget.dosya.path));
    kontrol.initialize().then((_) async {
      toplam = math.max(1.0, kontrol.value.duration.inMilliseconds / 1000.0).toDouble();
      bas = (widget.baslangicMs / 1000.0).clamp(0.0, toplam).toDouble();
      son = widget.bitisMs > 0
          ? (widget.bitisMs / 1000.0).clamp(math.min(toplam,bas + .1), toplam).toDouble()
          : toplam;
      if (son <= bas) son = math.min(toplam, bas + .5);
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

  void _trimSeek(double saniye){
    seekTimer?.cancel();
    seekTimer=Timer(const Duration(milliseconds:60),(){
      if(!mounted||!kontrol.value.isInitialized)return;
      unawaited(kontrol.seekTo(Duration(milliseconds:(saniye*1000).round())));
    });
  }

  @override
  void dispose() {
    seekTimer?.cancel();
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
                        'overlayColor':yaziRenk,
                        'overlayBackgroundColor':yaziArkaPlanRenk,
                        'overlayFontSize':yaziBoyut,
                        'overlayX':yaziX,
                        'overlayY':yaziY,
                        'overlayScale':yaziScale,
                        'overlayRotation':yaziRotation,
                      }),
              child: const Text('Bitti', style: TextStyle(color: mavi, fontWeight: FontWeight.w900)),
            ),
          ],
        ),
        body: SafeArea(
          child: hazir
              ? ListView(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 30),
                  children: [
                    AspectRatio(
                      aspectRatio: kontrol.value.aspectRatio <= 0 ? 9 / 16 : kontrol.value.aspectRatio,
                      child: LayoutBuilder(builder:(_,c)=>Stack(
                        fit: StackFit.expand,
                        children: [
                          VideoPlayer(kontrol),
                          if (yazi.text.trim().isNotEmpty)
                            NgelXSuruklenebilirYaziKatmani(
                              yazi:yazi.text.trim(),renk:yaziRenk,arkaPlanRenk:yaziArkaPlanRenk,boyut:yaziBoyut,
                              x:yaziX,y:yaziY,scale:yaziScale,rotation:yaziRotation,
                              canvasWidth:c.maxWidth,canvasHeight:c.maxHeight,
                              onChanged:(x,y,s,r)=>setState((){yaziX=x;yaziY=y;yaziScale=s;yaziRotation=r;}),
                            ),
                          Center(
                            child: IconButton.filled(
                              onPressed: _oynat,
                              style: IconButton.styleFrom(backgroundColor: Colors.black54),
                              icon: Icon(oynuyor ? Icons.pause_rounded : Icons.play_arrow_rounded, size: 34),
                            ),
                          ),
                          Positioned(left:0,right:0,bottom:0,child:VideoProgressIndicator(kontrol,allowScrubbing:true,padding:EdgeInsets.zero)),
                        ],
                      )),
                    ),
                    const SizedBox(height: 16),
                    const Text('Kes / kırp',style:TextStyle(fontSize:17,fontWeight:FontWeight.w900)),
                    const SizedBox(height:4),
                    const Text('Kolları sürüklediğinde video seçtiğin zamana gider.',style:TextStyle(color:Colors.white60,fontSize:12)),
                    const SizedBox(height:6),
                    Row(children:[
                      Text(_sure(bas),style:const TextStyle(fontWeight:FontWeight.w800)),
                      const Spacer(),
                      Text(_sure(son),style:const TextStyle(fontWeight:FontWeight.w800)),
                    ]),
                    RangeSlider(
                      min:0,max:toplam,values:RangeValues(bas,son),
                      labels:RangeLabels(_sure(bas),_sure(son)),
                      onChangeStart:(_){
                        trimOncesiOynuyordu=kontrol.value.isPlaying;
                        unawaited(kontrol.pause());
                      },
                      onChanged:(v){
                        var s=v.start,e=v.end;
                        if(e-s<.5){
                          if((s-bas).abs()>(e-son).abs())s=math.max(0.0,e-.5);
                          else e=math.min(toplam,s+.5);
                        }
                        final startDegisti=(s-bas).abs()>=(e-son).abs();
                        setState((){bas=s;son=e;});
                        _trimSeek(startDegisti?s:e);
                      },
                      onChangeEnd:(v)async{
                        seekTimer?.cancel();
                        await kontrol.seekTo(Duration(milliseconds:(v.start*1000).round()));
                        if(trimOncesiOynuyordu)await kontrol.play();
                      },
                    ),
                    const SizedBox(height:10),
                    TextField(
                      controller:yazi,maxLength:120,
                      onChanged:(_)=>setState((){}),
                      decoration:InputDecoration(
                        labelText:'Video üzerine yazı',
                        prefixIcon:const Icon(Icons.text_fields_rounded),
                        filled:true,fillColor:const Color(0xFF1D1D1F),
                        border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none),
                      ),
                    ),
                    const Text('Yazı rengi',style:TextStyle(fontWeight:FontWeight.w800)),
                    const SizedBox(height:8),
                    Wrap(spacing:9,runSpacing:9,children:renkler.map((c)=>InkWell(
                      onTap:()=>setState(()=>yaziRenk=c),
                      borderRadius:BorderRadius.circular(22),
                      child:Container(
                        width:32,height:32,
                        decoration:BoxDecoration(color:Color(c),shape:BoxShape.circle,border:Border.all(color:yaziRenk==c?mavi:Colors.white24,width:yaziRenk==c?3:1)),
                        child:yaziRenk==c?Icon(Icons.check_rounded,color:c==0xFFFFFFFF?Colors.black:Colors.white,size:18):null,
                      ),
                    )).toList()),
                    const SizedBox(height:8),
                    Row(children:[
                      const Expanded(child:Text('Yazı arka planı',style:TextStyle(fontWeight:FontWeight.w800))),
                      Switch(value:yaziArkaPlanRenk!=0,onChanged:(v)=>setState(()=>yaziArkaPlanRenk=v?0x99000000:0)),
                    ]),
                    Row(children:[
                      const Text('Yazı boyutu',style:TextStyle(fontWeight:FontWeight.w800)),
                      Expanded(child:Slider(min:14,max:54,value:yaziBoyut.clamp(14,54),onChanged:(v)=>setState(()=>yaziBoyut=v))),
                    ]),
                    const SizedBox(height:6),
                    const Text('Yazının üzerine basıp sürükle. İki parmakla büyüt/küçült ve döndür.',style:TextStyle(color:Colors.white60,fontSize:12)),
                  ],
                )
              : const Center(child: CircularProgressIndicator(color: mavi)),
        ),
      ),
    );
  }
}
