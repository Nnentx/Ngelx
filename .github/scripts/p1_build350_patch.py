from pathlib import Path

path = Path("app/lib/main.dart")
text = path.read_text(encoding="utf-8")
original = text

def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    text = text.replace(old, new, 1)
    print(f"OK {label}")

def replace_between(start: str, end: str, new: str, label: str) -> None:
    global text
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"{label}: start marker missing")
    j = text.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f"{label}: end marker missing")
    text = text[:i] + new + text[j:]
    print(f"OK {label}")

# 1) Private chat: keep the latest visible message order and make search/reply jumps robust.
replace_once(
"""  final Map<String,GlobalKey> _mesajAnahtarlari=<String,GlobalKey>{};
  String? _vurgulananMesajId;
""",
"""  final Map<String,GlobalKey> _mesajAnahtarlari=<String,GlobalKey>{};
  List<String> _sonMesajIdSirasi=<String>[];
  String? _vurgulananMesajId;
""",
"private message order field",
)

replace_between(
"""  Future<void> _yanitlananMesajaGit(String id)async{
""",
"""  Future<({String? engel,Map<String,dynamic> sohbet,Map<String,dynamic> diger,bool sohbetMevcut})> mesajGonderimHazirligi({bool zorla=false}) async {
""",
"""  Future<void> _yanitlananMesajaGit(String id)async{
    if(id.isEmpty||!mounted)return;
    BuildContext? hedef=_mesajAnahtarlari[id]?.currentContext;
    if(hedef==null&&liste.hasClients){
      final sira=_sonMesajIdSirasi.indexOf(id);
      if(sira>=0){
        for(var deneme=0;deneme<3&&hedef==null;deneme++){
          if(!mounted||!liste.hasClients)break;
          final toplam=_sonMesajIdSirasi.length;
          final oran=toplam<=1?0.0:(sira/(toplam-1)).clamp(0.0,1.0).toDouble();
          final konum=(liste.position.maxScrollExtent*oran)
              .clamp(liste.position.minScrollExtent,liste.position.maxScrollExtent)
              .toDouble();
          if(deneme==0){
            liste.jumpTo(konum);
          }else{
            await liste.animateTo(konum,duration:const Duration(milliseconds:180),curve:Curves.easeOutCubic);
          }
          await Future<void>.delayed(Duration(milliseconds:140+(deneme*80)));
          hedef=_mesajAnahtarlari[id]?.currentContext;
        }
      }
    }
    if(hedef==null){
      ScaffoldMessenger.of(context).removeCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj şu an ekranda yüklü değil.')));
      return;
    }
    _mesajVurguZamanlayici?.cancel();
    setState(()=>_vurgulananMesajId=id);
    await Scrollable.ensureVisible(hedef,duration:const Duration(milliseconds:320),curve:Curves.easeOutCubic,alignment:.35);
    HapticFeedback.selectionClick();
    _mesajVurguZamanlayici=Timer(const Duration(seconds:2),(){if(mounted&&_vurgulananMesajId==id)setState(()=>_vurgulananMesajId=null);});
  }

""",
"private robust jump",
)

replace_once(
"""          }).toList();
          sureliMesajTakvimi(docs);
""",
"""          }).toList();
          _sonMesajIdSirasi=docs.map((d)=>d.id).toList(growable:false);
          sureliMesajTakvimi(docs);
""",
"private visible id order",
)

# 2) Search privacy: self-hidden messages must never reappear in search.
replace_once(
"""  String sorgu='';
  int filtre=0;

  @override void dispose(){ara.dispose();super.dispose();}
""",
"""  String sorgu='';
  int filtre=0;
  Set<String> _gizliMesajIdleri=<String>{};
  bool _gizliMesajlarHazir=false,_gizliMesajlarHata=false;

  @override void initState(){
    super.initState();
    if(widget.groupMode){
      _gizliMesajlarHazir=true;
    }else{
      unawaited(_gizliMesajlariYukle());
    }
  }

  Future<void> _gizliMesajlariYukle()async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null){
      if(mounted)setState((){_gizliMesajlarHazir=true;_gizliMesajlarHata=false;});
      return;
    }
    if(mounted)setState((){_gizliMesajlarHazir=false;_gizliMesajlarHata=false;});
    try{
      final d=await FirebaseFirestore.instance.collection('chats').doc(widget.chatId).get();
      final ids=List<String>.from(d.data()?['hiddenMessageIds_$me']??const[]);
      if(mounted)setState((){_gizliMesajIdleri=ids.toSet();_gizliMesajlarHazir=true;_gizliMesajlarHata=false;});
    }catch(_){
      if(mounted)setState((){_gizliMesajlarHazir=false;_gizliMesajlarHata=true;});
    }
  }

  @override void dispose(){ara.dispose();super.dispose();}
""",
"search hidden ids state",
)

replace_between(
"""  Future<void> _aramaSonucuAc(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
""",
"""  Widget _vurguluMetin(String metin){
""",
"""  Future<void> _aramaSonucuAc(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    if(!mounted)return;
    Navigator.pop(context,d.id);
  }

""",
"search result returns exact message",
)

replace_once(
"""          builder:(_,snap){
            if(snap.connectionState==ConnectionState.waiting)return Center(child:CircularProgressIndicator(color:widget.groupMode?ngelxGroupGreen:ngelxPremiumPurple));
            if(sorgu.isEmpty)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
""",
"""          builder:(_,snap){
            if(snap.connectionState==ConnectionState.waiting)return Center(child:CircularProgressIndicator(color:widget.groupMode?ngelxGroupGreen:ngelxPremiumPurple));
            if(!widget.groupMode&&!_gizliMesajlarHazir){
              if(_gizliMesajlarHata)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const Icon(Icons.lock_outline_rounded,color:ngelxPremiumPurple,size:48),
                const SizedBox(height:10),
                const Text('Gizlenen mesajlar doğrulanamadı.',style:TextStyle(color:ngelxPremiumMuted,fontWeight:FontWeight.w700)),
                const SizedBox(height:10),
                OutlinedButton.icon(onPressed:_gizliMesajlariYukle,icon:const Icon(Icons.refresh_rounded),label:const Text('Tekrar dene')),
              ]));
              return const Center(child:CircularProgressIndicator(color:ngelxPremiumPurple));
            }
            if(sorgu.isEmpty)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
""",
"search privacy readiness",
)

replace_once(
"""            final docs=(snap.data?.docs??[]).where((d){
              final v=d.data();
              if(!_aramaFiltresineUyar(v))return false;
              return _aramaMetni(v).toLowerCase().contains(sorgu);
            }).toList();
""",
"""            final docs=(snap.data?.docs??[]).where((d){
              final v=d.data();
              if(!widget.groupMode){
                final me=FirebaseAuth.instance.currentUser?.uid;
                final legacy=List<String>.from(v['hiddenFor']??const[]);
                if(_gizliMesajIdleri.contains(d.id)||(me!=null&&legacy.contains(me)))return false;
              }
              if(!_aramaFiltresineUyar(v))return false;
              return _aramaMetni(v).toLowerCase().contains(sorgu);
            }).toList();
""",
"search hidden message filter",
)

# 3) Group search: return to the chat, load up to the same 300-message search window, scroll and highlight.
replace_once(
"""  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _grupMesajOnbellek=[];
  late Stream<QuerySnapshot<Map<String,dynamic>>> _mesajAkisi;
""",
"""  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _grupMesajOnbellek=[];
  final Map<String,GlobalKey> _grupMesajAnahtarlari=<String,GlobalKey>{};
  List<String> _sonGrupMesajIdSirasi=<String>[];
  String? _grupVurgulananMesajId;
  Timer? _grupMesajVurguZamanlayici;
  late Stream<QuerySnapshot<Map<String,dynamic>>> _mesajAkisi;
""",
"group jump state",
)

replace_once(
"""  Future<void> _enAltaGit()async{
    if(!liste.hasClients)return;
    await liste.animateTo(liste.position.maxScrollExtent,duration:const Duration(milliseconds:240),curve:Curves.easeOut);
    if(mounted)setState((){_enAltta=true;_acilisOkunmamis=0;});
  }

""",
"""  Future<void> _enAltaGit()async{
    if(!liste.hasClients)return;
    await liste.animateTo(liste.position.maxScrollExtent,duration:const Duration(milliseconds:240),curve:Curves.easeOut);
    if(mounted)setState((){_enAltta=true;_acilisOkunmamis=0;});
  }

  Future<void> _grupMesajaGit(String id)async{
    if(id.isEmpty||!mounted)return;
    BuildContext? hedef=_grupMesajAnahtarlari[id]?.currentContext;
    if(hedef==null&&!_sonGrupMesajIdSirasi.contains(id)){
      setState(()=>_mesajAkisi=chatRef.collection('messages').orderBy('createdAt').limitToLast(300).snapshots());
      for(var i=0;i<6&&mounted&&!_sonGrupMesajIdSirasi.contains(id);i++){
        await Future<void>.delayed(const Duration(milliseconds:120));
      }
      hedef=_grupMesajAnahtarlari[id]?.currentContext;
    }
    if(hedef==null&&liste.hasClients){
      final sira=_sonGrupMesajIdSirasi.indexOf(id);
      if(sira>=0){
        for(var deneme=0;deneme<3&&hedef==null;deneme++){
          if(!mounted||!liste.hasClients)break;
          final toplam=_sonGrupMesajIdSirasi.length;
          final oran=toplam<=1?0.0:(sira/(toplam-1)).clamp(0.0,1.0).toDouble();
          final konum=(liste.position.maxScrollExtent*oran)
              .clamp(liste.position.minScrollExtent,liste.position.maxScrollExtent)
              .toDouble();
          if(deneme==0){
            liste.jumpTo(konum);
          }else{
            await liste.animateTo(konum,duration:const Duration(milliseconds:180),curve:Curves.easeOutCubic);
          }
          await Future<void>.delayed(Duration(milliseconds:140+(deneme*80)));
          hedef=_grupMesajAnahtarlari[id]?.currentContext;
        }
      }
    }
    if(hedef==null){
      ScaffoldMessenger.of(context).removeCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Aranan mesaj şu an yüklenemedi.')));
      return;
    }
    _grupMesajVurguZamanlayici?.cancel();
    setState(()=>_grupVurgulananMesajId=id);
    await Scrollable.ensureVisible(hedef,duration:const Duration(milliseconds:320),curve:Curves.easeOutCubic,alignment:.35);
    HapticFeedback.selectionClick();
    _grupMesajVurguZamanlayici=Timer(const Duration(seconds:2),(){if(mounted&&_grupVurgulananMesajId==id)setState(()=>_grupVurgulananMesajId=null);});
  }

  Future<void> _grupBilgisiAc()async{
    final hedef=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId)));
    if(hedef!=null&&hedef.isNotEmpty&&mounted){
      await Future<void>.delayed(const Duration(milliseconds:120));
      if(mounted)await _grupMesajaGit(hedef);
    }
  }

""",
"group jump helpers",
)

replace_once(
"""    mentionZamanlayici?.cancel();_mesajBeklemeZamanlayici?.cancel();_typingZamanlayici?.cancel();_typingBaslatZamanlayici?.cancel();_sesKaydiZamanlayici?.cancel();_offlineRetryZamanlayici?.cancel();
""",
"""    mentionZamanlayici?.cancel();_mesajBeklemeZamanlayici?.cancel();_typingZamanlayici?.cancel();_typingBaslatZamanlayici?.cancel();_sesKaydiZamanlayici?.cancel();_offlineRetryZamanlayici?.cancel();_grupMesajVurguZamanlayici?.cancel();
""",
"group highlight timer dispose",
)

replace_once(
"""                  final docs=<QueryDocumentSnapshot<Map<String,dynamic>>>[...hamDocs].where((d)=>(d.data()['type']??'').toString()!='poll').toList()
                    ..sort((a,b){
                      final ad=a.data(),bd=b.data(),av=ad['createdAt']??ad['clientCreatedAt'],bv=bd['createdAt']??bd['clientCreatedAt'];
                      final ams=av is Timestamp?av.millisecondsSinceEpoch:0,bms=bv is Timestamp?bv.millisecondsSinceEpoch:0;
                      return ams.compareTo(bms);
                    });
""",
"""                  final docs=<QueryDocumentSnapshot<Map<String,dynamic>>>[...hamDocs].where((d)=>(d.data()['type']??'').toString()!='poll').toList()
                    ..sort((a,b){
                      final ad=a.data(),bd=b.data(),av=ad['createdAt']??ad['clientCreatedAt'],bv=bd['createdAt']??bd['clientCreatedAt'];
                      final ams=av is Timestamp?av.millisecondsSinceEpoch:0,bms=bv is Timestamp?bv.millisecondsSinceEpoch:0;
                      return ams.compareTo(bms);
                    });
                  _sonGrupMesajIdSirasi=docs.map((d)=>d.id).toList(growable:false);
""",
"group visible id order",
)

replace_once(
"""                      return RepaintBoundary(
                        key:ValueKey(d.id),
                        child:Column(children:[
""",
"""                      final vurgulu=_grupVurgulananMesajId==d.id;
                      return RepaintBoundary(
                        key:_grupMesajAnahtarlari.putIfAbsent(d.id,()=>GlobalKey()),
                        child:AnimatedContainer(
                          duration:const Duration(milliseconds:180),
                          margin:vurgulu?const EdgeInsets.symmetric(vertical:2):EdgeInsets.zero,
                          padding:vurgulu?const EdgeInsets.all(4):EdgeInsets.zero,
                          decoration:BoxDecoration(
                            color:vurgulu?ngelxGroupGreenSoft:Colors.transparent,
                            borderRadius:BorderRadius.circular(18),
                            border:vurgulu?Border.all(color:ngelxGroupGreen,width:2):null,
                          ),
                          child:Column(children:[
""",
"group highlight wrapper open",
)

replace_once(
"""                          mesajKarti(d,onceki:onceki,grupVerisi:tv,sonMesaj:i==docs.length-1),
                        ]),
                      );
""",
"""                          mesajKarti(d,onceki:onceki,grupVerisi:tv,sonMesaj:i==docs.length-1),
                        ]),
                        ),
                      );
""",
"group highlight wrapper close",
)

replace_once(
"""              onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId))),
""",
"""              onTap:_grupBilgisiAc,
""",
"group title info navigation",
)

replace_once(
"""            onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId))),
""",
"""            onPressed:_grupBilgisiAc,
""",
"group info button navigation",
)

replace_once(
"""                    Expanded(child:_grupKisayol(Icons.search_rounded,'Arama',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:widget.chatId,groupMode:true))))),
""",
"""                    Expanded(child:_grupKisayol(Icons.search_rounded,'Arama',()async{
                      final hedef=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:widget.chatId,groupMode:true)));
                      if(hedef!=null&&hedef.isNotEmpty&&mounted)Navigator.pop(context,hedef);
                    })),
""",
"group search returns message id",
)

# 4) Background blur: remove the fake oval/full-frame effect and clearly disable it until true segmentation exists.
replace_once(
"""  bool baglaniyor=true,mikrofon=true,kamera=true,hoparlor=true,bitiyor=false,bulanik=false,rotus=false,yenidenBaglaniyor=false,arkaKamera=false,kucultuluyor=false;
""",
"""  bool baglaniyor=true,mikrofon=true,kamera=true,hoparlor=true,bitiyor=false,rotus=false,yenidenBaglaniyor=false,arkaKamera=false,kucultuluyor=false;
""",
"remove fake blur state",
)

replace_once(
"""    Widget renderer()=>stil(lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover));
    if(!uygulaEfekt||!bulanik)return renderer();

    // Arka katmanı bulanıklaştırıp merkezdeki kişiyi keskin tut.
    // Bu, tüm yüzü bulanıklaştıran eski tam-kare filtreden daha doğal bir portre etkisi verir.
    return Stack(fit:StackFit.expand,children:[
      ImageFiltered(imageFilter:ui.ImageFilter.blur(sigmaX:10,sigmaY:10),child:renderer()),
      Align(
        alignment:const Alignment(0,-.10),
        child:FractionallySizedBox(
          widthFactor:.72,
          heightFactor:.86,
          child:ClipOval(child:renderer()),
        ),
      ),
    ]);
""",
"""    Widget renderer()=>stil(lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover));
    return renderer();
""",
"remove fake blur renderer",
)

replace_once(
"""              _efektChip('◌ Bulanık',bulanik,(v)=>setState(()=>bulanik=v)),
""",
"""              ActionChip(
                label:const Text('◌ Bulanık'),
                onPressed:(){
                  ScaffoldMessenger.of(context).removeCurrentSnackBar();
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Gerçek arka plan bulanıklığı kişi ayrımı gerektiriyor. Sahte bulanıklık bu test sürümünde kapatıldı.')));
                },
                backgroundColor:Colors.white10,
                side:BorderSide(color:Colors.white.withValues(alpha:.10)),
                labelStyle:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800),
              ),
""",
"disable misleading blur chip",
)

if text == original:
    raise SystemExit("No changes made")

path.write_text(text, encoding="utf-8")
print(f"Patched {path}: {len(original)} -> {len(text)} chars")
