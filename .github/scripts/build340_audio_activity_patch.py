from pathlib import Path
import base64

main_path=Path('app/lib/main.dart')
pubspec_path=Path('app/pubspec.yaml')
rules_path=Path('firestore.rules')
parts_dir=Path('.github/build340_parts')
audio_path=Path('app/lib/audio_live_rooms.dart')

parts=sorted(parts_dir.glob('audio_live_rooms.b64.*'))
if parts:
    raw=''.join(p.read_text(encoding='utf-8').strip() for p in parts)
    data=base64.b64decode(raw)
    if len(data)!=22102:
        raise SystemExit(f'audio module byte size mismatch: {len(data)}')
    audio_path.write_bytes(data)
if not audio_path.exists():
    raise SystemExit('audio_live_rooms.dart missing')
audio=audio_path.read_text(encoding='utf-8')
for marker in ["part of 'main.dart';","class SesliOdaHazirlikPage","class SesliOdaPage","collection('audio_rooms')","ngelxSesliMaksKonusmaci=12"]:
    if marker not in audio:
        raise SystemExit('audio module marker missing: '+marker)

s=main_path.read_text(encoding='utf-8')

if "part 'audio_live_rooms.dart';" not in s:
    marker="part 'live_broadcast_studio.dart';\n"
    if marker not in s: raise SystemExit('live part marker missing')
    s=s.replace(marker, marker+"part 'audio_live_rooms.dart';\n",1)
s=s.replace("defaultValue: '1.0.120'","defaultValue: '1.0.121'",1)
s=s.replace("defaultValue: '339'","defaultValue: '340'",1)
if "defaultValue: '1.0.121'" not in s or "defaultValue: '340'" not in s:
    raise SystemExit('version patch failed')

fields_old="""  String sohbetSorgu='';
  String filtre='Tümü';
"""
fields_new="""  String sohbetSorgu='';
  String filtre='Tümü';
  bool _gelenKutusuYenileniyor=false;
"""
if '_gelenKutusuYenileniyor' not in s:
    if fields_old not in s: raise SystemExit('inbox field marker missing')
    s=s.replace(fields_old,fields_new,1)

old_refresh="""  Future<void> _gelenKutusunuYenile()async{
    final ben=uid;if(ben==null)return;
    try{
      await Future.wait([
        FirebaseFirestore.instance.collection('users').doc(ben).get(const GetOptions(source:Source.server)),
        FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(100).get(const GetOptions(source:Source.server)),
        FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).get(const GetOptions(source:Source.server)),
      ]).timeout(const Duration(seconds:10));
      _kullaniciCache.clear();await tercihleriGetir();if(mounted)setState((){});
    }catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Gelen Kutusu yenilenemedi. Tekrar dene.','Inbox could not be refreshed. Try again.'))));}
  }
"""
new_refresh="""  Future<void> _gelenKutusunuYenile()async{
    final ben=uid;if(ben==null||_gelenKutusuYenileniyor)return;
    if(mounted)setState(()=>_gelenKutusuYenileniyor=true);
    var basarili=0;
    Future<void> dene(Future<dynamic> islem)async{
      try{await islem.timeout(const Duration(seconds:9));basarili++;}catch(_){}
    }
    try{
      await Future.wait([
        dene(FirebaseFirestore.instance.collection('users').doc(ben).get(const GetOptions(source:Source.server))),
        dene(FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(100).get(const GetOptions(source:Source.server))),
        dene(FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).get(const GetOptions(source:Source.server))),
      ]);
      if(basarili==0)throw StateError('inbox_refresh_all_failed');
      _kullaniciCache.clear();
      try{await tercihleriGetir();}catch(_){}
      if(mounted){
        setState((){});
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content:Text(basarili==3?lt('Gelen Kutusu yenilendi.','Inbox refreshed.'):lt('Gelen Kutusu yenilendi. Bazı veriler gecikebilir.','Inbox refreshed. Some data may be delayed.')),
          duration:const Duration(milliseconds:1200),behavior:SnackBarBehavior.floating,
        ));
      }
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Gelen Kutusu yenilenemedi. Tekrar dene.','Inbox could not be refreshed. Try again.'))));
    }finally{
      if(mounted)setState(()=>_gelenKutusuYenileniyor=false);
    }
  }
"""
if "inbox_refresh_all_failed" not in s:
    if old_refresh not in s: raise SystemExit('inbox refresh marker missing')
    s=s.replace(old_refresh,new_refresh,1)

old_icon="IconButton(constraints:const BoxConstraints.tightFor(width:38),padding:EdgeInsets.zero,tooltip:lt('Yenile','Refresh'),onPressed:ben==null?null:_gelenKutusunuYenile,icon:const Icon(Icons.refresh_rounded,color:mor))"
new_icon="IconButton(constraints:const BoxConstraints.tightFor(width:38),padding:EdgeInsets.zero,tooltip:lt('Yenile','Refresh'),onPressed:ben==null||_gelenKutusuYenileniyor?null:_gelenKutusunuYenile,icon:_gelenKutusuYenileniyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:mor)):const Icon(Icons.refresh_rounded,color:mor))"
if new_icon not in s:
    if old_icon not in s: raise SystemExit('inbox icon marker missing')
    s=s.replace(old_icon,new_icon,1)

activity_head="""class _AktivitePageState extends State<AktivitePage> {
  String _filtre='all';

  Future<void> _aktiviteyiYenile()async{
    final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null)return;
    try{await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10));if(mounted)setState((){});}
    catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Aktiviteler yenilenemedi.','Activity could not be refreshed.'))));}
  }
"""
activity_new="""class _AktivitePageState extends State<AktivitePage> {
  String _filtre='all';
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _sunucuAktiviteleri=[];
  bool _aktiviteYenileniyor=false;

  @override void initState(){
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)unawaited(_aktiviteyiYenile(sessiz:true));});
  }

  Future<void> _aktiviteyiYenile({bool sessiz=false})async{
    final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||_aktiviteYenileniyor)return;
    if(mounted)setState(()=>_aktiviteYenileniyor=true);
    try{
      final q=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10));
      if(!mounted)return;
      setState(()=>_sunucuAktiviteleri=q.docs);
      if(!sessiz)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Aktiviteler yenilendi.','Activity refreshed.')),duration:const Duration(milliseconds:1100),behavior:SnackBarBehavior.floating));
    }catch(_){
      if(mounted&&!sessiz)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Aktiviteler yenilenemedi.','Activity could not be refreshed.'))));
    }finally{
      if(mounted)setState(()=>_aktiviteYenileniyor=false);
    }
  }
"""
if '_sunucuAktiviteleri' not in s:
    if activity_head not in s: raise SystemExit('activity head marker missing')
    s=s.replace(activity_head,activity_new,1)

old_activity_icon="IconButton(tooltip:lt('Yenile','Refresh'),onPressed:_aktiviteyiYenile,icon:const Icon(Icons.refresh_rounded,color:mor))"
new_activity_icon="IconButton(tooltip:lt('Yenile','Refresh'),onPressed:_aktiviteYenileniyor?null:()=>_aktiviteyiYenile(),icon:_aktiviteYenileniyor?const SizedBox(width:19,height:19,child:CircularProgressIndicator(strokeWidth:2,color:mor)):const Icon(Icons.refresh_rounded,color:mor))"
if new_activity_icon not in s:
    if old_activity_icon not in s: raise SystemExit('activity refresh icon marker missing')
    s=s.replace(old_activity_icon,new_activity_icon,1)

old_builder="""        builder: (_, s) {
          if(s.hasError)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:52),const SizedBox(height:10),Text(t('activityLoadFailed'),style:const TextStyle(color:Colors.black,fontWeight:FontWeight.w800)),Text(t('checkConnectionRetry'),style:const TextStyle(color:Colors.black54))]));
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final gelenDocs=(s.data?.docs??[]).toList();
"""
new_builder="""        builder: (_, s) {
          if(s.hasError&&_sunucuAktiviteleri.isEmpty)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:52),const SizedBox(height:10),Text(t('activityLoadFailed'),style:const TextStyle(color:Colors.black,fontWeight:FontWeight.w800)),Text(t('checkConnectionRetry'),style:const TextStyle(color:Colors.black54))]));
          if(s.connectionState==ConnectionState.waiting&&_sunucuAktiviteleri.isEmpty)return const Center(child:CircularProgressIndicator(color:mor));
          final birlesik=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in s.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[])birlesik[d.id]=d;
          for(final d in _sunucuAktiviteleri)birlesik[d.id]=d;
          final gelenDocs=birlesik.values.toList();
"""
if 'final birlesik=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};' not in s:
    if old_builder not in s: raise SystemExit('activity builder marker missing')
    s=s.replace(old_builder,new_builder,1)

old_tabs="""                _kesfetSekmesi(Icons.live_tv_rounded,t('live'),0),
                _kesfetSekmesi(Icons.local_fire_department_rounded,t('trend'),1),
                _kesfetSekmesi(Icons.person_rounded,t('people'),2),
                _kesfetSekmesi(Icons.groups_rounded,t('groups'),3),
"""
new_tabs="""                _kesfetSekmesi(Icons.live_tv_rounded,t('live'),0),
                _kesfetSekmesi(Icons.mic_rounded,'Sesli',1),
                _kesfetSekmesi(Icons.local_fire_department_rounded,t('trend'),2),
                _kesfetSekmesi(Icons.person_rounded,t('people'),3),
                _kesfetSekmesi(Icons.groups_rounded,t('groups'),4),
"""
if "_kesfetSekmesi(Icons.mic_rounded,'Sesli',1)" not in s:
    if old_tabs not in s: raise SystemExit('explore tabs marker missing')
    s=s.replace(old_tabs,new_tabs,1)

old_slivers="""          if(kategori==0)..._canliSliverleri(),
          if(kategori==1)..._trendSliverleri(),
          if(kategori==2)..._kisiSliverleri(),
          if(kategori==3)..._grupSliverleri(),
"""
new_slivers="""          if(kategori==0)..._canliSliverleri(),
          if(kategori==1)...ngelxSesliKesfetSliverleri(context),
          if(kategori==2)..._trendSliverleri(),
          if(kategori==3)..._kisiSliverleri(),
          if(kategori==4)..._grupSliverleri(),
"""
if 'ngelxSesliKesfetSliverleri(context)' not in s:
    if old_slivers not in s: raise SystemExit('explore slivers marker missing')
    s=s.replace(old_slivers,new_slivers,1)

old_fab="""      floatingActionButton:kategori==0?FilledButton.icon(
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0xFFFF1744),
          minimumSize: const Size(230, 54),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
          elevation: 12,
        ),
        onPressed: () async {
          if (await misafirEngeli(context)) return;
          if (context.mounted) Navigator.push(context, MaterialPageRoute(builder: (_) => const CanliHazirlikPage()));
        },
        icon: const Icon(Icons.videocam_rounded),
        label: Text(t('startLive'), style: const TextStyle(fontWeight: FontWeight.w800)),
      ):null,
"""
new_fab="""      floatingActionButton:kategori==0?FilledButton.icon(
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0xFFFF1744),
          minimumSize: const Size(230, 54),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
          elevation: 12,
        ),
        onPressed: () async {
          if (await misafirEngeli(context)) return;
          if (context.mounted) Navigator.push(context, MaterialPageRoute(builder: (_) => const CanliHazirlikPage()));
        },
        icon: const Icon(Icons.videocam_rounded),
        label: Text(t('startLive'), style: const TextStyle(fontWeight: FontWeight.w800)),
      ):kategori==1?FilledButton.icon(
        style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size(230,54),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(24)),elevation:12),
        onPressed:()async{if(await misafirEngeli(context))return;if(context.mounted)Navigator.push(context,MaterialPageRoute(builder:(_)=>const SesliOdaHazirlikPage()));},
        icon:const Icon(Icons.mic_rounded),label:const Text('Sesli oda başlat',style:TextStyle(fontWeight:FontWeight.w900)),
      ):null,
"""
if "label:const Text('Sesli oda başlat'" not in s:
    if old_fab not in s: raise SystemExit('explore fab marker missing')
    s=s.replace(old_fab,new_fab,1)

main_path.write_text(s,encoding='utf-8')

pub=pubspec_path.read_text(encoding='utf-8')
pub=pub.replace('version: 1.0.120+339','version: 1.0.121+340',1)
if 'version: 1.0.121+340' not in pub: raise SystemExit('pubspec version patch failed')
pubspec_path.write_text(pub,encoding='utf-8')

rules=rules_path.read_text(encoding='utf-8')
if 'match /audio_rooms/{roomId}' not in rules:
    insert="""
    match /audio_rooms/{roomId} {
      allow read: if signedIn();
      allow create: if signedIn()
        && request.resource.data.ownerId == request.auth.uid
        && request.auth.uid in request.resource.data.get('speakerIds', [])
        && request.resource.data.get('speakerIds', []).size() <= 12
        && request.resource.data.get('moderatorIds', []).size() <= 3;
      allow update: if signedIn()
        && resource.data.ownerId == request.auth.uid
        && request.resource.data.get('speakerIds', []).size() <= 12
        && request.resource.data.get('moderatorIds', []).size() <= 3;
      allow delete: if false;
      match /speaker_requests/{uid} {
        allow read: if signedIn() && (
          isMe(uid)
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
        allow create: if isMe(uid)
          && request.resource.data.get('userId', '') == request.auth.uid
          && request.resource.data.get('status', '') == 'pending';
        allow update: if signedIn() && (
          (
            isMe(uid)
            && request.resource.data.get('userId', '') == request.auth.uid
            && request.resource.data.get('status', '') in ['pending', 'cancelled']
          )
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
        allow delete: if signedIn() && (
          isMe(uid)
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
        );
      }
    }
"""
    marker="    match /live_streams/{streamId} {\n"
    if marker not in rules: raise SystemExit('rules live marker missing')
    rules=rules.replace(marker,insert+marker,1)
rules_path.write_text(rules,encoding='utf-8')

checks=[
    (main_path,"Future<void> canliPaylasimMesajiniAc"),
    (main_path,"onTap:canliPaylasimi"),
    (main_path,"Yayına gitmek için dokun"),
    (main_path,"Bu canlı yayın bitti."),
    (main_path,"part 'live_pk.dart';"),
]
for path,marker in checks:
    if marker not in path.read_text(encoding='utf-8'): raise SystemExit('regression marker missing: '+marker)

print('Build 340 patch applied successfully')
