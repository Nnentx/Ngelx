const ngelx435MedyaAlanlari=<String>['mediaUrl','videoUrl','audioUrl','fileUrl','thumbnailUrl','posterUrl','coverUrl','imageUrl'];
List<String> ngelx435MedyaListesi(Map<String,dynamic> v)=>ngelx435MedyaAlanlari.map((k)=>(v[k]??'').toString()).toList();
bool ngelx435BendenGizli(Map<String,dynamic> v,String? uid)=>uid!=null&&v['hiddenFor'] is Iterable&&(v['hiddenFor'] as Iterable).contains(uid);
bool ngelx435MesajErisilebilir(Map<String,dynamic> v,String? uid)=>v['deletedForEveryone']!=true&&!ngelx435BendenGizli(v,uid);
final _ngelx435SilmeKilidi=<String>{};
Future<void> _ngelx435QueueTail=Future<void>.value();
Future<void> _ngelx435QueueChange(String key,String path,{required bool add}){
  final done=Completer<void>();
  _ngelx435QueueTail=_ngelx435QueueTail.then((_)async{
    try{
      final prefs=await SharedPreferences.getInstance();
      final jobs=prefs.getStringList(key)??<String>[];
      if(add&&!jobs.contains(path)){
        if(jobs.length>=200)throw StateError('Bekleyen silme işlemlerini bağlantı gelince yeniden dene.');
        jobs.add(path);
      }else if(!add){jobs.remove(path);}
      if(!await prefs.setStringList(key,jobs))throw StateError('Silme işlemi kaydedilemedi.');
      done.complete();
    }catch(e,st){done.completeError(e,st);}
  });
  return done.future;
}
Future<void> ngelx435MesajiSil(DocumentReference<Map<String,dynamic>> ref,{bool retry=false}) async {
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
  final key='message_delete435_'+me,lock=me+'/'+ref.path;
  if(!_ngelx435SilmeKilidi.add(lock))return;
  try{
    await _ngelx435QueueChange(key,ref.path,add:true);
    if(FirebaseAuth.instance.currentUser?.uid!=me)return;
    await FirebaseFirestore.instance.runTransaction((tx) async {
      final snap=await tx.get(ref),v=snap.data();
      if(v==null||v['deletedForEveryone']==true)return;
      // Rules authorize the actual sender or the group's administrator.
      tx.update(ref,{
        'deletedForEveryone':true,'deletedAt':FieldValue.serverTimestamp(),'deletedBy':me,
        'cleanupMediaUrls':ngelx435MedyaListesi(v),'mediaCleanupState':'pending',
        'text':'','fileName':'','linkUrl':'','reactions':<String,dynamic>{},
        'pinned':false,'pinnedAt':null,'pinnedBy':null,
        for(final field in ngelx435MedyaAlanlari)field:'',
      });
    }).timeout(const Duration(seconds:15));
    await _ngelx435QueueChange(key,ref.path,add:false);
  }catch(_){if(!retry)rethrow;}finally{_ngelx435SilmeKilidi.remove(lock);}
}
Future<void> ngelx435SilmeTekrar(String chatId) async {
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
  final prefs=await SharedPreferences.getInstance();
  for(final path in List<String>.from(prefs.getStringList('message_delete435_'+me)??const[])){
    if(FirebaseAuth.instance.currentUser?.uid!=me)return;
    final parts=path.split('/');
    if(parts.length!=4||parts[0]!='chats'||parts[1]!=chatId||parts[2]!='messages')continue;
    await ngelx435MesajiSil(FirebaseFirestore.instance.doc(path),retry:true);
  }
}
Future<void> ngelx435BendenSil(DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> v) async {
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
  await ref.update({'hiddenFor':FieldValue.arrayUnion([me])}).timeout(const Duration(seconds:15));
  await ngelx435OnbellekTemizle(ngelx435MedyaListesi(v));
}
Future<void> ngelx435OnbellekTemizle(Iterable<String> urls) async {
  for(final raw in urls.toSet()){
    if(raw.trim().isEmpty)continue;
    try{await ngelxAgResmiOnbelleginiTemizle(raw);}catch(_){}
    try{await CachedNetworkImage.evictFromCache(raw);}catch(_){}
    try{
      final root=await getTemporaryDirectory();
      final dir=Directory('${root.path}/ngelx_message435/'+crypto.sha256.convert(utf8.encode(raw)).toString());
      if(await dir.exists())await dir.delete(recursive:true);
    }catch(_){}
  }
}
Future<String> ngelx435PaylasimDosyasi(String url,String name) async {
  final root=await getTemporaryDirectory();
  final dir=Directory('${root.path}/ngelx_message435/'+crypto.sha256.convert(utf8.encode(url)).toString());
  await dir.create(recursive:true);
  final safe=name.replaceAll(RegExp(r'[\\/:*?"<>|]'),'_');
  final path=dir.path+'/'+(safe.isEmpty||safe=='.'||safe=='..'?'NgelX_dosya':safe);
  await Dio().download(url,path);
  return path;
}
class Ngelx435MesajGorunumu extends StatefulWidget{
  final Map<String,dynamic> data;final Widget Function() builder;
  const Ngelx435MesajGorunumu({super.key,required this.data,required this.builder});
  @override State<Ngelx435MesajGorunumu> createState()=>_Ngelx435MesajGorunumuState();
}
class _Ngelx435MesajGorunumuState extends State<Ngelx435MesajGorunumu>{
  Set<String> _urls=<String>{};bool _removed=false;
  void _sync(){
    final v=widget.data;
    final removed=v['deletedForEveryone']==true||ngelx435BendenGizli(v,FirebaseAuth.instance.currentUser?.uid);
    _urls.addAll(ngelx435MedyaListesi(v));
    if(v['cleanupMediaUrls'] is Iterable)_urls.addAll((v['cleanupMediaUrls'] as Iterable).whereType<String>());
    if(removed&&!_removed){unawaited(ngelx435OnbellekTemizle(_urls));_urls.clear();}
    _removed=removed;
  }
  @override void initState(){super.initState();_sync();}
  @override void didUpdateWidget(covariant Ngelx435MesajGorunumu old){super.didUpdateWidget(old);_sync();}
  @override Widget build(BuildContext context)=>ngelx435BendenGizli(widget.data,FirebaseAuth.instance.currentUser?.uid)?const SizedBox.shrink():widget.builder();
}
class Ngelx435MedyaKaynagi extends StatefulWidget{
  final DocumentReference<Map<String,dynamic>> ref;final Widget child;
  const Ngelx435MedyaKaynagi({super.key,required this.ref,required this.child});
  @override State<Ngelx435MedyaKaynagi> createState()=>_Ngelx435MedyaKaynagiState();
}
class _Ngelx435MedyaKaynagiState extends State<Ngelx435MedyaKaynagi>{
  late final _stream=widget.ref.snapshots();
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
    stream:_stream,builder:(_,snap){
      final data=snap.data?.data();
      if(snap.hasData&&(data==null||!ngelx435MesajErisilebilir(data,FirebaseAuth.instance.currentUser?.uid))){
        return Scaffold(backgroundColor:Colors.white,appBar:AppBar(),body:const Center(child:Text('Bu mesaj artık kullanılamıyor.')));
      }
      return widget.child;
    },
  );
}
