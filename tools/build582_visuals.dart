// Reference assets extracted from the user's approved Ludo screens.
const _ludo582Gold = Color(0xFFFFD95B);
Widget _ludo582Art(String name, double size) => Image.asset(
  'assets/ludo582/$name.png',
  width: size,
  height: size,
  fit: BoxFit.contain,
  excludeFromSemantics: true,
);
BoxDecoration _ludo582Panel({bool dark = false}) => BoxDecoration(
  gradient: LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: dark
        ? const [Color(0xFF1B3273), Color(0xFF25217C)]
        : const [Color(0xFF3737A9), Color(0xFF282283)],
  ),
  borderRadius: BorderRadius.circular(12),
  border: Border.all(color: const Color(0xFF7658E8), width: 1),
  boxShadow: const [
    BoxShadow(color: Color(0x50020E43), blurRadius: 10, offset: Offset(0, 4)),
  ],
);

class Ngelx581Hero extends StatelessWidget {
  final bool statistics;
  const Ngelx581Hero({super.key, this.statistics = false});
  @override
  Widget build(BuildContext context) => Semantics(
    label: statistics
        ? 'LUDO, Oyun istatistiklerim'
        : 'LUDO, Arkadaşlarınla aynı masada',
    image: true,
    child: AspectRatio(
      aspectRatio: statistics ? 4 : 864 / 212,
      child: Image.asset(
        'assets/ludo582/${statistics ? 'stats' : 'lobby'}_header.png',
        fit: BoxFit.fill,
        excludeFromSemantics: true,
      ),
    ),
  );
}

class Ngelx581QuickAction extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback? action;
  final Key? actionKey;
  const Ngelx581QuickAction({
    super.key,
    required this.label,
    required this.icon,
    this.action,
    this.actionKey,
  });
  @override
  Widget build(BuildContext context) => OutlinedButton(
    onPressed: action,
    key: actionKey,
    style: OutlinedButton.styleFrom(
      minimumSize: const Size(0, 36),
      padding: const EdgeInsets.symmetric(horizontal: 5),
      side: const BorderSide(color: Color(0xFF8B7AE7)),
      backgroundColor: const Color(0x993A3399),
      shape: const StadiumBorder(),
    ),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, size: 16, color: _ludo582Gold),
        const SizedBox(width: 3),
        Flexible(
          child: Text(
            label,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 9.5,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
        const Icon(
          Icons.chevron_right_rounded,
          color: Color(0xFFB3A3EF),
          size: 12,
        ),
      ],
    ),
  );
}

class Ngelx581StatsScreen extends StatefulWidget {
  final Map<String, dynamic> stats;
  final Ngelx567Request? request;
  final Map<String, dynamic>? profile;
  const Ngelx581StatsScreen({
    super.key,
    required this.stats,
    this.request,
    this.profile,
  });
  @override
  State<Ngelx581StatsScreen> createState() => _Ngelx581StatsScreenState();
}

class _Ngelx581StatsScreenState extends State<Ngelx581StatsScreen> {
  late Map<String, dynamic> data, profile;
  bool loading = false;
  String filter = 'Tümü', error = '';
  int n(String key) =>
      data[key] is num ? math.max(0, (data[key] as num).toInt()) : 0;
  int get gifts {
    final g = data['receivedGifts'];
    return g is Map
        ? g.values.whereType<num>().fold<int>(0, (a, b) => a + b.toInt())
        : 0;
  }

  @override
  void initState() {
    super.initState();
    data = Map.of(widget.stats);
    profile = widget.profile ?? {};
    if (widget.profile == null) unawaited(_loadProfile());
  }

  Future<void> _loadProfile() async {
    if (Firebase.apps.isEmpty) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    profile = {
      'displayName': user.displayName ?? 'Oyuncu',
      'photoUrl': user.photoURL ?? '',
    };
    try {
      final doc = await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .get();
      if (mounted) setState(() => profile = {...profile, ...?doc.data()});
    } catch (_) {
      if (mounted) setState(() {});
    }
  }

  Future<void> refresh() async {
    if (loading) return;
    setState(() {
      loading = true;
      error = '';
    });
    try {
      final fresh = await (widget.request ?? ngelx565LudoRequest)({
        'action': 'wallet',
      });
      if (mounted) setState(() => data = fresh);
    } catch (_) {
      if (mounted) setState(() => error = 'Puanlar yenilenemedi. Tekrar dene.');
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  List<(String, String, String, bool)> get awards => [
    ('İlk Oyun', '1 oyun oyna', 'first', n('wins') + n('losses') >= 1),
    ('Galibiyet', '1 oyun kazan', 'winner', n('wins') >= 1),
    ('Seri', '2 maç üst üste', 'series', n('streak') >= 2),
    ('Usta', '10 oyun kazan', 'winner', n('wins') >= 10),
    ('Şampiyon', '50 oyun kazan', 'winner', n('wins') >= 50),
  ];
  void showAwards() => showModalBottomSheet<void>(
    context: context,
    backgroundColor: const Color(0xFF172769),
    isScrollControlled: true,
    builder: (c) => SafeArea(
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  const Expanded(
                    child: Text(
                      'Tüm rozetler',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  IconButton(
                    tooltip: 'Kapat',
                    onPressed: () => Navigator.pop(c),
                    icon: const Icon(Icons.close, color: Colors.white),
                  ),
                ],
              ),
              for (final a in awards)
                ListTile(
                  leading: _ludo582Art(a.$4 ? a.$3 : 'locked', 50),
                  title: Text(
                    a.$1,
                    style: const TextStyle(color: Colors.white),
                  ),
                  subtitle: Text(
                    '${a.$2} · ${a.$4 ? 'Kazanıldı' : 'Kilitli'}',
                    style: const TextStyle(color: Color(0xFFBFCBF1)),
                  ),
                ),
            ],
          ),
        ),
      ),
    ),
  );
  @override
  Widget build(BuildContext context) {
    final wins = n('wins'),
        losses = n('losses'),
        all = wins + losses,
        level = n('level').clamp(1, 10000),
        xp = n('xp');
    final start = 50 * level * level + 50 * level - 100,
        next = 50 * (level + 1) * (level + 1) + 50 * (level + 1) - 100;
    final name = (profile['displayName'] ?? profile['username'] ?? 'Oyuncu')
            .toString(),
        photo = (profile['photoUrl'] ?? profile['foto'] ?? '').toString();
    return Theme(
      data: ngelx567LudoTheme(),
      child: Scaffold(
        backgroundColor: const Color(0xFF081D62),
        appBar: AppBar(
          backgroundColor: const Color(0xFF332094),
          title: const Text(
            'NgelX Ludo',
            style: TextStyle(fontWeight: FontWeight.w900),
          ),
          actions: [
            IconButton(
              tooltip: 'Puanları yenile',
              onPressed: loading ? null : refresh,
              icon: loading
                  ? const SizedBox(
                      width: 21,
                      height: 21,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.refresh_rounded),
            ),
          ],
        ),
        body: SafeArea(
          child: RefreshIndicator(
            onRefresh: refresh,
            child: ListView(
              key: const ValueKey('ludo-stats-page'),
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.only(bottom: 16),
              children: [
                const Ngelx581Hero(statistics: true),
                Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 650),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 13),
                      child: Column(
                        children: [
                          if (error.isNotEmpty)
                            Padding(
                              padding: const EdgeInsets.all(8),
                              child: Text(
                                error,
                                style: const TextStyle(color: _ludo582Gold),
                              ),
                            ),
                          Container(
                            decoration: _ludo582Panel(),
                            padding: const EdgeInsets.all(10),
                            child: Row(
                              children: [
                                Container(
                                  width: 67,
                                  height: 67,
                                  decoration: const BoxDecoration(
                                    shape: BoxShape.circle,
                                    gradient: LinearGradient(
                                      colors: [
                                        Color(0xFF5ADAFB),
                                        Color(0xFFCA66F4),
                                      ],
                                    ),
                                  ),
                                  padding: const EdgeInsets.all(3),
                                  child: CircleAvatar(
                                    backgroundColor: const Color(0xFF222C76),
                                    backgroundImage: photo.isEmpty
                                        ? null
                                        : ResizeImage(
                                            NgelXAgImageProvider(photo),
                                            width: 180,
                                          ),
                                    child: photo.isEmpty
                                        ? const Icon(
                                            Icons.person,
                                            color: Colors.white,
                                            size: 37,
                                          )
                                        : null,
                                  ),
                                ),
                                const SizedBox(width: 9),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        children: [
                                          Expanded(
                                            child: Column(
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              children: [
                                                Text(
                                                  name,
                                                  maxLines: 1,
                                                  overflow:
                                                      TextOverflow.ellipsis,
                                                  style: const TextStyle(
                                                    color: Colors.white,
                                                    fontSize: 16,
                                                    fontWeight: FontWeight.w900,
                                                  ),
                                                ),
                                                const Text(
                                                  'Ludo Oyuncusu',
                                                  style: TextStyle(
                                                    color: Color(0xFFBBCBF4),
                                                    fontSize: 12,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                          Container(
                                            padding: const EdgeInsets.symmetric(
                                              horizontal: 9,
                                              vertical: 6,
                                            ),
                                            decoration: _ludo582Panel(
                                              dark: true,
                                            ),
                                            child: Row(
                                              children: [
                                                _ludo582Art('wins', 25),
                                                const SizedBox(width: 4),
                                                Column(
                                                  crossAxisAlignment:
                                                      CrossAxisAlignment.start,
                                                  children: [
                                                    Text(
                                                      '${n('chips')}',
                                                      style: const TextStyle(
                                                        color: Colors.white,
                                                        fontWeight:
                                                            FontWeight.w900,
                                                        fontSize: 17,
                                                      ),
                                                    ),
                                                    const Text(
                                                      'Toplam Çip',
                                                      style: TextStyle(
                                                        color: Color(
                                                          0xFFBBCBF4,
                                                        ),
                                                        fontSize: 9,
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ],
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 7),
                                      Row(
                                        children: [
                                          const Icon(
                                            Icons.star_rounded,
                                            color: _ludo582Gold,
                                            size: 22,
                                          ),
                                          Expanded(
                                            child: Text(
                                              ' Seviye $level',
                                              maxLines: 1,
                                              overflow: TextOverflow.ellipsis,
                                              style: const TextStyle(
                                                color: Colors.white,
                                                fontSize: 11,
                                              ),
                                            ),
                                          ),
                                          Flexible(
                                            child: Text(
                                              '$xp / $next XP',
                                              maxLines: 1,
                                              overflow: TextOverflow.ellipsis,
                                              textAlign: TextAlign.end,
                                              style: const TextStyle(
                                                color: Color(0xFFBFCEF8),
                                                fontSize: 10,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 4),
                                      ClipRRect(
                                        borderRadius: BorderRadius.circular(8),
                                        child: LinearProgressIndicator(
                                          value: ((xp - start) / (next - start))
                                              .clamp(0.0, 1.0),
                                          minHeight: 6,
                                          color: _ludo582Gold,
                                          backgroundColor: const Color(
                                            0xFF5835B7,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 9),
                          LayoutBuilder(
                            builder: (context, box) => GridView.count(
                              key: const ValueKey('ludo-stats-grid'),
                              crossAxisCount: 4,
                              shrinkWrap: true,
                              physics: const NeverScrollableScrollPhysics(),
                              crossAxisSpacing: 5,
                              mainAxisSpacing: 5,
                              childAspectRatio:
                                  1.25 /
                                  math.max(
                                    1.0,
                                    MediaQuery.textScalerOf(context).scale(1),
                                  ),
                              children: [
                                tile('Çip', n('chips'), 'chips', _ludo582Gold),
                                tile(
                                  'Elmas',
                                  n('gems'),
                                  'gems',
                                  const Color(0xFF30C3F4),
                                ),
                                tile(
                                  'Seviye',
                                  level,
                                  'level',
                                  const Color(0xFFE06BF3),
                                ),
                                tile('XP', xp, 'xp', _ludo582Gold),
                                tile(
                                  'Galibiyet',
                                  wins,
                                  'wins',
                                  const Color(0xFF8BE99D),
                                ),
                                tile(
                                  'Mağlubiyet',
                                  losses,
                                  'losses',
                                  const Color(0xFFFF6594),
                                ),
                                tile(
                                  'Toplanan hediye',
                                  gifts,
                                  'gifts',
                                  const Color(0xFFB6EBFF),
                                ),
                                tile(
                                  'Galibiyet serisi',
                                  n('streak'),
                                  'streak',
                                  _ludo582Gold,
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 8),
                          Container(
                            decoration: _ludo582Panel(),
                            padding: const EdgeInsets.all(10),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.bar_chart_rounded,
                                      color: Color(0xFF66DDFB),
                                      size: 23,
                                    ),
                                    const SizedBox(width: 7),
                                    const Expanded(
                                      child: Text(
                                        'Oyun geçmişim',
                                        style: TextStyle(
                                          color: Colors.white,
                                          fontSize: 16,
                                          fontWeight: FontWeight.w900,
                                        ),
                                      ),
                                    ),
                                    PopupMenuButton<String>(
                                      tooltip: 'Oyun geçmişini filtrele',
                                      initialValue: filter,
                                      onSelected: (v) =>
                                          setState(() => filter = v),
                                      itemBuilder: (_) => [
                                        for (final v in [
                                          'Tümü',
                                          'Kazanılan',
                                          'Kaybedilen',
                                        ])
                                          PopupMenuItem(
                                            value: v,
                                            child: Text(v),
                                          ),
                                      ],
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 9,
                                          vertical: 5,
                                        ),
                                        decoration: BoxDecoration(
                                          border: Border.all(
                                            color: const Color(0xFF9561F5),
                                          ),
                                          borderRadius: BorderRadius.circular(
                                            24,
                                          ),
                                        ),
                                        child: Row(
                                          children: [
                                            Text(
                                              filter,
                                              style: const TextStyle(
                                                color: Colors.white,
                                                fontSize: 11,
                                              ),
                                            ),
                                            const Icon(
                                              Icons.expand_more,
                                              color: Color(0xFFBBA6FF),
                                              size: 19,
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Container(
                                  padding: const EdgeInsets.all(7),
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF152466),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Column(
                                    children: [
                                      if (filter != 'Kaybedilen')
                                        history(
                                          'Kazanılan oyunlar',
                                          wins,
                                          all,
                                          'wins',
                                          const Color(0xFF91E477),
                                        ),
                                      if (filter != 'Kazanılan')
                                        history(
                                          'Kaybedilen oyunlar',
                                          losses,
                                          all,
                                          'losses',
                                          const Color(0xFFFF598B),
                                        ),
                                      history(
                                        'Toplam oyun',
                                        all,
                                        all,
                                        'first',
                                        const Color(0xFF36B4F6),
                                        total: true,
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 8),
                          Container(
                            decoration: _ludo582Panel(),
                            padding: const EdgeInsets.all(10),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.workspace_premium_rounded,
                                      color: _ludo582Gold,
                                      size: 23,
                                    ),
                                    const SizedBox(width: 7),
                                    const Expanded(
                                      child: Text(
                                        'Son başarılarım',
                                        style: TextStyle(
                                          color: Colors.white,
                                          fontSize: 16,
                                          fontWeight: FontWeight.w900,
                                        ),
                                      ),
                                    ),
                                    TextButton(
                                      onPressed: showAwards,
                                      style: TextButton.styleFrom(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 7,
                                        ),
                                        minimumSize: const Size(0, 30),
                                        side: const BorderSide(
                                          color: Color(0xFF8174E4),
                                        ),
                                        shape: const StadiumBorder(),
                                      ),
                                      child: const Row(
                                        children: [
                                          Text(
                                            'Tüm rozetler',
                                            style: TextStyle(
                                              color: Colors.white,
                                              fontSize: 10,
                                            ),
                                          ),
                                          Icon(
                                            Icons.chevron_right,
                                            color: Color(0xFFAFB2F7),
                                            size: 16,
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                Container(
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF152466),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  padding: const EdgeInsets.symmetric(
                                    vertical: 6,
                                  ),
                                  child: Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      for (final a in awards)
                                        Expanded(
                                          child: Semantics(
                                            label:
                                                '${a.$1}, ${a.$4 ? 'Kazanıldı' : 'Kilitli'}',
                                            child: Column(
                                              children: [
                                                LayoutBuilder(
                                                  builder: (_, b) =>
                                                      _ludo582Art(
                                                        a.$4 ? a.$3 : 'locked',
                                                        math.min(
                                                          61,
                                                          b.maxWidth - 4,
                                                        ),
                                                      ),
                                                ),
                                                Text(
                                                  a.$1,
                                                  maxLines: 1,
                                                  style: const TextStyle(
                                                    color: Colors.white,
                                                    fontSize: 10,
                                                  ),
                                                ),
                                                const SizedBox(height: 3),
                                                Text(
                                                  a.$2,
                                                  textAlign: TextAlign.center,
                                                  style: const TextStyle(
                                                    color: Color(0xFFBACBF0),
                                                    fontSize: 8,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
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

  Widget tile(String label, int value, String art, Color color) => Container(
    decoration: _ludo582Panel(dark: true),
    padding: const EdgeInsets.symmetric(horizontal: 2, vertical: 4),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Flexible(child: _ludo582Art(art, 27)),
        Text(
          label,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(color: Colors.white, fontSize: 9),
        ),
        Text(
          '$value',
          maxLines: 1,
          style: TextStyle(
            color: color,
            fontSize: 17,
            fontWeight: FontWeight.w900,
          ),
        ),
      ],
    ),
  );
  Widget history(
    String label,
    int count,
    int totalCount,
    String art,
    Color color, {
    bool total = false,
  }) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 3),
    child: Row(
      children: [
        _ludo582Art(art, 23),
        const SizedBox(width: 6),
        Expanded(
          flex: 5,
          child: Text(
            label,
            style: const TextStyle(color: Colors.white, fontSize: 10),
          ),
        ),
        Expanded(
          flex: 5,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(
              value: totalCount == 0 ? 0 : count / totalCount,
              minHeight: 6,
              color: color,
              backgroundColor: const Color(0xFF35358B),
            ),
          ),
        ),
        const SizedBox(width: 10),
        SizedBox(
          width: 24,
          child: Text(
            '$count',
            textAlign: TextAlign.end,
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.w800,
              fontSize: 13,
            ),
          ),
        ),
        SizedBox(
          width: 32,
          child: Text(
            total
                ? ''
                : '%${totalCount == 0 ? 0 : (100 * count / totalCount).round()}',
            textAlign: TextAlign.end,
            style: const TextStyle(color: Color(0xFFB1BDE8), fontSize: 10),
          ),
        ),
      ],
    ),
  );
}
