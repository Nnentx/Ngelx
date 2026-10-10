from pathlib import Path
s=Path('app/lib/main.dart').read_text()
def region(a,b,fn):
 global s
 start=s.index(a);end=s.index(b,start);s=s[:start]+fn(s[start:end])+s[end:]
def replace(p,a,b):
 if p.count(a)!=1:raise SystemExit('Build432 anchor: '+a[:85]+' count='+str(p.count(a)))
 return p.replace(a,b,1)
def inbox(p):
 a=p.index('  final Map<String,Stream<QuerySnapshot');b=p.index('\n  Set<String> engellenenler',a)
 p=p[:a]+'''  final Map<String,NgelxSnapshotCache<QuerySnapshot<Map<String,dynamic>>>> _akislari={};
  Stream<QuerySnapshot<Map<String,dynamic>>> _sohbetAkisi(String ben,int limit)=>
    _akislari.putIfAbsent('chat|'+ben,()=>NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('chats')
      .where('members',arrayContains:ben).limit(200).snapshots())).stream;
  Stream<QuerySnapshot<Map<String,dynamic>>> _bildirimAkisi(String ben,int limit)=>
    _akislari.putIfAbsent('notification|'+ben,()=>NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('notifications')
      .where('toUid',isEqualTo:ben).limit(200).snapshots())).stream;
'''+p[b:]
 p=replace(p,"()=>FirebaseFirestore.instance.collection('users').doc(id).get());","()=>FirebaseFirestore.instance.collection('users').doc(id).get().timeout(const Duration(seconds:12)).then((v)=>v,onError:(Object error,StackTrace trace){_kullaniciCache.remove(id);Error.throwWithStackTrace(error,trace);}));")
 p=p.replace('      _kullaniciCache.clear();','      _kullaniciCache.clear();\n      for(final cache in _akislari.values){cache.retry();}')
 p=replace(p,'@override void dispose(){sohbetAra.dispose();super.dispose();}','@override void dispose(){for(final cache in _akislari.values){cache.dispose();}sohbetAra.dispose();super.dispose();}')
 a=p.index('    Widget isteklerIcerigi()');b=p.index('          final hamSosyal',a)
 p=p[:b]+"          if(snap.hasError)return ngelx432YuklemeHatasi(()=>unawaited(_gelenKutusunuYenile()),'İstekler yüklenemedi.');\n          if(!snap.hasData)return const Center(child:CircularProgressIndicator(color:mor));\n"+p[b:]
 return p
region('class _MesajPageState','class ArsivSohbetlerPage',inbox)
def requests(p):
 p=replace(p,'class MesajIstekleriPage extends StatelessWidget {','class MesajIstekleriPage extends StatefulWidget {')
 p=replace(p,'  @override Widget build(BuildContext context) => Theme(','''  @override State<MesajIstekleriPage> createState()=>_MesajIstekleriPageState();
}
class _MesajIstekleriPageState extends State<MesajIstekleriPage>{
  String get uid=>widget.uid;
  late final _me=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('users').doc(uid).snapshots());
  late final _chats=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('chats').where('members',arrayContains:uid).limit(200).snapshots());
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _profiles={};
  Future<DocumentSnapshot<Map<String,dynamic>>> _profile(String id)=>_profiles.putIfAbsent(id,
    ()=>FirebaseFirestore.instance.collection('users').doc(id).get().timeout(const Duration(seconds:12)).then((v)=>v,onError:(Object e,StackTrace st){_profiles.remove(id);Error.throwWithStackTrace(e,st);}));
  void _retry(){_me.retry();_chats.retry();_profiles.clear();setState((){});}
  @override void dispose(){_me.dispose();_chats.dispose();super.dispose();}
  @override Widget build(BuildContext context) => Theme(''')
 p=p.replace('body: FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(','body: StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(').replace("future: FirebaseFirestore.instance.collection('users').doc(uid).get(),",'stream:_me.stream,')
 p=p.replace("stream: FirebaseFirestore.instance.collection('chats').where('members', arrayContains: uid).limit(200).snapshots(),",'stream:_chats.stream,')
 p=p.replace("return const Center(child:Text('İstekler yüklenemedi. Geri dönüp tekrar dene.'));","return ngelx432YuklemeHatasi(_retry,'İstekler yüklenemedi.');").replace("return const Center(child:Text('Mesaj istekleri yüklenemedi. Geri dönüp tekrar dene.'));","return ngelx432YuklemeHatasi(_retry,'Mesaj istekleri yüklenemedi.');")
 p=replace(p,"if(docs.isEmpty) return Center(child: Text(t('noMessageRequests'), style: const TextStyle(color: Colors.black54)));","""if(docs.isEmpty)return Center(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
                const Icon(Icons.mark_chat_read_outlined,size:52,color:mor),const SizedBox(height:14),
                Text(t('noMessageRequests'),textAlign:TextAlign.center,style:const TextStyle(fontWeight:FontWeight.w700)),
                const SizedBox(height:8),const Text('Yeni mesaj istekleri burada görünür.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)),
                TextButton.icon(onPressed:_retry,icon:const Icon(Icons.refresh),label:const Text('Yenile')),
              ])));""")
 p=p.replace("future: FirebaseFirestore.instance.collection('users').doc(other).get(),",'future:_profile(other),')
 return p
region('class MesajIstekleriPage','class MesajIstegiOnizlemePage',requests)
def search(p):
 p=replace(p,"  String q='';",'''  Timer? _searchTimer;
  void _deleted(){if(mounted)setState((){});}
  @override void initState(){super.initState();ngelxIcerikSilmeRevizyonu.addListener(_deleted);}
  @override void dispose(){_searchTimer?.cancel();_paylasimCache.dispose();ngelxIcerikSilmeRevizyonu.removeListener(_deleted);super.dispose();}
  String q='';''')
 p=replace(p,"  late final _paylasimAkisi=FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.uid).limit(100).snapshots();","  late final _paylasimCache=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.uid).limit(100).snapshots());")
 p=p.replace('stream:_paylasimAkisi,','stream:_paylasimCache.stream,')
 p=replace(p,"onChanged:(v)=>setState(()=>q=v.trim().toLowerCase()),","onChanged:(v){_searchTimer?.cancel();_searchTimer=Timer(const Duration(milliseconds:220),(){if(mounted)setState(()=>q=v.trim().toLowerCase());});},")
 p=p.replace("return const Center(child:Text('Profil araması yüklenemedi. Tekrar dene.',style:TextStyle(color:Colors.black54)));","return ngelx432YuklemeHatasi(()=>_paylasimCache.retry(),'Profil araması yüklenemedi.');")
 p=p.replace("d.data()['type']!='story'&&d.data()['deleted']!=true&&d.data()['isDeleted']!=true","d.data()['type']!='story'&&ngelx432IcerikGorunur(d.id,d.data(),FirebaseAuth.instance.currentUser?.uid??'')")
 return p
region('class _ProfilAramaPageState','class HikayeArsiviPage',search)
def archive(p):
 p=replace(p,'class HikayeArsiviPage extends StatelessWidget{','class HikayeArsiviPage extends StatefulWidget{')
 p=replace(p,'  @override Widget build(BuildContext context){', '''  @override State<HikayeArsiviPage> createState()=>_HikayeArsiviPageState();
}
class _HikayeArsiviPageState extends State<HikayeArsiviPage>{
  late final _uid=FirebaseAuth.instance.currentUser?.uid;
  late final _archive=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:_uid).where('type',isEqualTo:'story').limit(100).snapshots());
  void _deleted(){if(mounted)setState((){});}
  @override void initState(){super.initState();ngelxIcerikSilmeRevizyonu.addListener(_deleted);}
  @override void dispose(){_archive.dispose();ngelxIcerikSilmeRevizyonu.removeListener(_deleted);super.dispose();}
  @override Widget build(BuildContext context){''')
 p=p.replace("final uid=FirebaseAuth.instance.currentUser?.uid;","final uid=_uid;")
 p=p.replace("stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).where('type',isEqualTo:'story').limit(100).snapshots(),",'stream:_archive.stream,')
 p=p.replace('if(s.connectionState==ConnectionState.waiting)','if(s.connectionState==ConnectionState.waiting&&!s.hasData)')
 p=p.replace('onPressed:()=>Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>const HikayeArsiviPage())),','onPressed:()=>_archive.retry(),')
 a=p.index('          final docs=');b=p.index('          }).toList()',a)
 p=p[:a]+'''          final docs=(s.data?.docs??[]).where((d){
            return ngelx432ArsivGorunur(d.id,d.data(),uid);
'''+p[b:]
 p=p.replace("onPressed:()=>d.reference.set({'highlighted':!oneCikan},SetOptions(merge:true)),","onPressed:()async{try{await d.reference.update({'highlighted':!oneCikan}).timeout(const Duration(seconds:10));}catch(_){if(context.mounted)ngelxDurumMesaji(context,'Hikâye güncellenemedi.',tip:'hata');}},")
 return p
region('class HikayeArsiviPage','class IcerikGizlemePage',archive)
def profile(p):
 p=replace(p,'  String get uid=>widget.uid;', '''  Future<List<DocumentSnapshot<Map<String,dynamic>>?>>? _profileFuture;
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _profileDocs={};
  String _profileIdentity='';
  Future<DocumentSnapshot<Map<String,dynamic>>> _profileDoc(String id)=>_profileDocs.putIfAbsent(id,
    ()=>FirebaseFirestore.instance.collection('users').doc(id).get().timeout(const Duration(seconds:12)));
  Future<List<DocumentSnapshot<Map<String,dynamic>>?>> _profiles(String? me){
    final key='${widget.uid}|${me??""}';
    if(key!=_profileIdentity){_profileIdentity=key;_profileFuture=null;_profileDocs.clear();}
    return _profileFuture??=Future.wait<DocumentSnapshot<Map<String,dynamic>>?>([_profileDoc(widget.uid),me==null?Future.value(null):_profileDoc(me)]);
  }
  void _profileUpdate(VoidCallback change){_profileFuture=null;_profileDocs.clear();setState(change);}
  String get uid=>widget.uid;''')
 # Only calls outside the helper; rebuilds caused by actions must invalidate the snapshot.
 p=p.replace('setState(()','_profileUpdate(()')
 p=p.replace("    final hedef = FirebaseFirestore.instance.collection('users').doc(uid).get();\n    final benim = me == null ? Future.value(null) : FirebaseFirestore.instance.collection('users').doc(me).get();\n",'    final profiles=_profiles(me);\n')
 p=p.replace('future: Future.wait([hedef, benim]),','future:profiles,')
 p=p.replace("future:FirebaseFirestore.instance.collection('users').doc(me).get(),","future:_profileDoc(me),")
 p=replace(p,'          if (!s.hasData) return const Center(child: CircularProgressIndicator(color: mavi));',"          if(s.hasError)return ngelx432YuklemeHatasi(()=>_profileUpdate((){}),'Profil yüklenemedi.');\n          if (!s.hasData) return const Center(child: CircularProgressIndicator(color: mavi));")
 return p
region('class _KullaniciProfilPageState','class NgelXVideoKapakOnizleme',profile)
s+='\n'+Path('tools/build432_snapshot_cache.dart').read_text()
s=s.replace("defaultValue: '431'","defaultValue: '432'").replace("defaultValue: '1.0.206'","defaultValue: '1.0.207'")
Path('app/lib/main.dart').write_text(s)
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.206+431','version: 1.0.207+432'))
# Story preloading: keep and await the in-flight initialization instead of recreating it.
p=Path('app/lib/story_v66.dart');v=p.read_text()
v=replace(v,'  String sonrakiVideoUrl=\'\';',"  String sonrakiVideoUrl='';\n  Future<void>? sonrakiVideoHazirlama;\n  Timer? _bufferTimer;\n  bool _userPaused=false;\n  VoidCallback? _videoListener;")
v=v.replace('sonrakiVideoKontrol?.value.isInitialized==true)return;','sonrakiVideoKontrol!=null)return;')
v=v.replace('      await x.initialize().timeout(const Duration(seconds:12));','      final pending=x.initialize().timeout(const Duration(seconds:30));\n      sonrakiVideoHazirlama=pending;\n      await pending;',1)
v=v.replace(".limit(100).get();",".limit(100).get().timeout(const Duration(seconds:15));")
v=v.replace("return v['type']=='story'&&bitis is Timestamp&&bitis.toDate().isAfter(simdi);","return v['type']=='story'&&ngelx432IcerikGorunur(d.id,v,widget.ownerUid)&&bitis is Timestamp&&bitis.toDate().isAfter(simdi);")
v=replace(v,'    final nesil=++medyaNesli;', '    final nesil=++medyaNesli;\n    _bufferTimer?.cancel();_userPaused=false;\n    if(videoKontrol!=null&&_videoListener!=null)videoKontrol!.removeListener(_videoListener!);\n    _videoListener=null;')
v=replace(v,'    // Build 398: if the next story was already initialized, reuse it instantly.', '''    // Await a matching preload already in flight; do not start a second request.
    if(sonrakiVideoIndex==aktif&&sonrakiVideoUrl==medyaAdresi&&sonrakiVideoKontrol!=null){
      try{await sonrakiVideoHazirlama;}catch(_){}
      if(!mounted||nesil!=medyaNesli)return;
    }
    // Build 398: if the next story was already initialized, reuse it instantly.''')
v=v.replace('await x.initialize().timeout(const Duration(seconds:12));','await x.initialize().timeout(const Duration(seconds:30));')
v=v.replace('      await hazirSiradaki.play();','      await hazirSiradaki.play();\n      _videoIzle(hazirSiradaki,nesil);')
v=v.replace('      await x.play();','      await x.play();\n      _videoIzle(x,nesil);',1)
v=replace(v,'      setState(()=>videoHata=true);\n      sure.stop();', '''      final failed=videoKontrol;videoKontrol=null;
      if(failed!=null)unawaited(failed.dispose());
      setState(()=>videoHata=true);
      sure.stop();''')
v=replace(v,'  void _duraklat(){','''  void _videoIzle(VideoPlayerController x,int nesil){
    _videoListener=(){
      if(!mounted||nesil!=medyaNesli||videoKontrol!=x)return;
      if(x.value.hasError){_videoBasarisiz(x);return;}
      if(x.value.isBuffering){
        sure.stop();
        _bufferTimer??=Timer(const Duration(seconds:20),(){
          _bufferTimer=null;
          if(mounted&&nesil==medyaNesli&&videoKontrol==x&&x.value.isBuffering)_videoBasarisiz(x);
        });
      }else{
        _bufferTimer?.cancel();_bufferTimer=null;
        if(!_userPaused&&!videoHata&&videoHazir&&x.value.isPlaying&&!sure.isAnimating)sure.forward();
      }
    };
    x.addListener(_videoListener!);
    _videoListener!();
  }
  void _videoBasarisiz(VideoPlayerController x){
    _bufferTimer?.cancel();_bufferTimer=null;sure.stop();
    if(_videoListener!=null)x.removeListener(_videoListener!);
    _videoListener=null;videoKontrol=null;
    unawaited(x.dispose());
    if(mounted)setState((){videoHazir=false;videoHata=true;});
  }
  void _duraklat(){
    _userPaused=true;''')
v=replace(v,'  void _devam(){','  void _devam(){\n    _userPaused=false;')
v=replace(v,'    medyaNesli++;\n    cevap.dispose();','    medyaNesli++;\n    _bufferTimer?.cancel();\n    if(videoKontrol!=null&&_videoListener!=null)videoKontrol!.removeListener(_videoListener!);\n    cevap.dispose();')
p.write_text(v)
print('Build432 replay cache + ten follow-ups applied')
