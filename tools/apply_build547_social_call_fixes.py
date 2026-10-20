"""Apply only the owner's three Build546 follow-ups to assembled release source."""
from pathlib import Path
TAG='// Build547 social and call follow-ups'

def once(s, old, new):
    assert s.count(old)==1, f'Expected one anchor: {old[:90]!r}, got {s.count(old)}'
    return s.replace(old,new,1)

def main_source(s):
    if TAG in s:return s
    a=s.index('class _KesfetPageState ');b=s.index('  Future<void> _yayinIzle',a)
    old=s[a:b]
    new=old.replace('  bool hesapYukleniyor=true;', '''  bool hesapYukleniyor=true;
  bool _isteklerYukleniyor547=true;
  final Set<String> _gonderiliyor547=<String>{};
  final Set<String> _aktifArkadaslar547=<String>{};
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _arkadasIstekleri547;
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _arkadasliklar547;''')
    start=new.index('    _gidenIstekAboneligi=')
    end=new.index('\n  }',start)
    new=new[:start]+'''    // Canonical outgoing records have no unrelated notification limit.
    _gidenIstekAboneligi=FirebaseFirestore.instance.collection('follow_requests')
      .doc(uid).collection('outgoing').snapshots().listen((q){
        if(!mounted||ben!=uid)return;
        setState(()=>gonderilenTakipIstekleri=q.docs
          .where((d)=>d.data()['status']=='pending').map((d)=>d.id).toSet());
      },onError:(_){ });
    _arkadasIstekleri547=FirebaseFirestore.instance.collection('friend_requests')
      .doc(uid).collection('outgoing').snapshots().listen((q){
        if(!mounted||ben!=uid)return;
        setState((){
          gonderilenArkadaslikIstekleri=q.docs
            .where((d)=>d.data()['status']=='pending').map((d)=>d.id).toSet();
          _isteklerYukleniyor547=false;
        });
      },onError:(_){
        // A failed lookup is not evidence that no request exists.
        if(mounted&&ben==uid)setState(()=>_isteklerYukleniyor547=true);
      });
    _arkadasliklar547=FirebaseFirestore.instance.collection('friendships')
      .where('members',arrayContains:uid).snapshots().listen((q){
        if(!mounted||ben!=uid)return;
        setState((){
          _aktifArkadaslar547.clear();
          for(final d in q.docs){
            if(d.data()['active']!=true)continue;
            _aktifArkadaslar547.addAll(List<String>.from(d.data()['members']??const[])
              .where((id)=>id!=uid));
          }
        });
      },onError:(_){ });''' +new[end:]
    new=new.replace('    _gidenIstekAboneligi?.cancel();','''    _gidenIstekAboneligi?.cancel();
    _arkadasIstekleri547?.cancel();
    _arkadasliklar547?.cancel();''')
    new=new.replace('if(!mounted)return;','if(!mounted||ben!=uid)return;')
    s=s[:a]+new+s[b:]
    a=s.index('  Future<void> _arkadaslikIstegiGonder(',a);b=s.index('  Future<void> _grupDurumuDegistir',a)
    s=s[:a]+'''  Future<void> _arkadaslikIstegiGonder(String hedefUid)async{
    if(await misafirEngeli(context))return;
    final me=ben;
    if(me==null||!mounted||_gonderiliyor547.contains(hedefUid))return;
    if(arkadaslar.contains(hedefUid)||_aktifArkadaslar547.contains(hedefUid)||
        gonderilenArkadaslikIstekleri.contains(hedefUid))return;
    setState(()=>_gonderiliyor547.add(hedefUid));
    try{
      final gonderildi=await sosyalIstekGonder(
        hedefUid:hedefUid,tur:'friend_request',metin:'Yeni arkadaşlık isteğin var');
      if(!mounted||ben!=me)return;
      if(gonderildi){
        setState(()=>gonderilenArkadaslikIstekleri.add(hedefUid));
        ngelxDurumMesaji(context,'Arkadaşlık isteği gönderildi.',tip:'basari');
      }else{
        // The send path checks both profiles. Reconcile from the same sources;
        // do not clear a real pending request merely because send returned false.
        final db=FirebaseFirestore.instance;
        final records=await Future.wait([
          db.collection('users').doc(me).get(const GetOptions(source:Source.server)),
          db.collection('users').doc(hedefUid).get(const GetOptions(source:Source.server)),
          sosyalIstekRef(me,hedefUid,'friend_request').get(const GetOptions(source:Source.server)),
        ]).timeout(const Duration(seconds:8));
        if(!mounted||ben!=me)return;
        final friends=List<String>.from(records[0].data()?['friends']??const[]).contains(hedefUid)||
          List<String>.from(records[1].data()?['friends']??const[]).contains(me)||
          _aktifArkadaslar547.contains(hedefUid);
        final pending=records[2].data()?['status']=='pending';
        setState((){
          if(friends)arkadaslar.add(hedefUid);
          if(pending&&!friends)gonderilenArkadaslikIstekleri.add(hedefUid);
          else gonderilenArkadaslikIstekleri.remove(hedefUid);
        });
        if(!friends&&!pending)ngelxDurumMesaji(context,
          'İstek gönderilemedi. Profildeki istek durumunu kontrol et.',tip:'uyari');
      }
    }catch(_){
      if(mounted&&ben==me)ngelxDurumMesaji(context,
        'İstek durumu doğrulanamadı. Bağlantını kontrol et.',tip:'hata');
    }finally{
      if(mounted&&ben==me)setState(()=>_gonderiliyor547.remove(hedefUid));
    }
  }

''' +s[b:]
    a=s.index('  Widget _kisiSatiri(String uid,Map<String,dynamic> v)');b=s.index('\n  Widget ',a+15)
    row=s[a:b]
    row=once(row,"    final takipte=takipEdilenler.contains(uid);",'''    final arkadas547=arkadaslar.contains(uid)||_aktifArkadaslar547.contains(uid)||
      (ben!=null&&List<String>.from(v['friends']??const[]).contains(ben));
    final bekliyor547=gonderilenArkadaslikIstekleri.contains(uid)||_gonderiliyor547.contains(uid);
    final takipte=takipEdilenler.contains(uid);''')
    row=row.replace('arkadaslar.contains(uid)||gonderilenArkadaslikIstekleri.contains(uid)?null:',
      'hesapYukleniyor||_isteklerYukleniyor547||arkadas547||bekliyor547?null:')
    row=row.replace('arkadaslar.contains(uid)?','arkadas547?').replace('gonderilenArkadaslikIstekleri.contains(uid)?','bekliyor547?')
    s=s[:a]+row+s[b:]
    a=s.rfind("      if(ngelx440CallJoinable(veri,DateTime.now()))",0,s.index("Text(veri['callVideo']==true?'Görüntülü arama devam ediyor'"))
    b=s.index('      Expanded(child:StreamBuilder<QuerySnapshot',a)
    # Remove only this redundant private-chat banner; preserve the global return
    # control, call routing, call log, mini window and audio session unchanged.
    assert 'Sesli arama devam ediyor' in s[a:b]
    s=s[:a]+s[b:]
    return s+'\n'+TAG+'\n'

if __name__=='__main__':
    p=Path('app/lib/main.dart');p.write_text(main_source(p.read_text()))

def incoming_source(s):
    if TAG in s:return s
    s=once(s,'        val uid=user.uid\n','''        val uid=user.uid
        // Disk cache runs independently of the authenticated remote refresh.
        try { photoExecutor547.execute {
            val bitmap=CallPhoto547.read(this,uid,chat) ?: return@execute
            runOnUiThread {
                if(isFinishing||isDestroyed||!IncomingCallService.isStillRinging470(room)||
                    com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid!=uid){bitmap.recycle();return@runOnUiThread}
                if(frame.tag=="remote547"){bitmap.recycle();return@runOnUiThread}
                frame.clipToOutline=true
                frame.addView(ImageView(this).apply {
                    setImageBitmap(bitmap);scaleType=ImageView.ScaleType.CENTER_CROP
                    contentDescription=if(group)"Grup fotoğrafı" else "Arayan kişinin profil fotoğrafı"
                },FrameLayout.LayoutParams(-1,-1))
            }
        }}catch(_:java.util.concurrent.RejectedExecutionException){}
''')
    s=once(s,'    private val photoExecutor546 =', '''    private val photoExecutor547=java.util.concurrent.Executors.newSingleThreadExecutor()
    private val photoExecutor546 =''')
    s=once(s,'                    runOnUiThread {\n                        if(isFinishing', '''                    CallPhoto547.store(this,uid,chat,bytes)
                    runOnUiThread {
                        if(isFinishing''')
    s=once(s,'                        frame.clipToOutline=true','''                        frame.tag="remote547"
                        frame.clipToOutline=true''')
    s=once(s,'        photoExecutor546.shutdownNow()','''        photoExecutor546.shutdownNow()
        photoExecutor547.shutdownNow()''')
    return s+'\n'+TAG+'\n'

def activity_source(s):
    if TAG in s:return s
    s=once(s,'                    "noteChatKind471" -> {','''                    "noteCallPhoto547" -> {
                        CallPhoto547.remember(this,call.argument<String>("uid").orEmpty(),
                            call.argument<String>("chat").orEmpty(),call.argument<String>("path").orEmpty())
                        result.success(null)
                    }
                    "noteChatKind471" -> {''')
    return s+'\n'+TAG+'\n'

def calls_source(s):
    if TAG in s:return s
    s=once(s,'            unawaited(_pushOutgoing452(change.doc.id,value,user.uid));','''            unawaited(_warmPhoto547(change.doc.id,value,user.uid));
            unawaited(_pushOutgoing452(change.doc.id,value,user.uid));''')
    s=once(s,'  bool _registering453=false;', '''  // Reuse images already cached by the inbox/profile. Never download or block
  // the ringtone here, and never fan out server profile reads for all chats.
  final Map<String,int> _photoWarm547=<String,int>{};
  Future<void> _warmPhoto547(String chat,Map<String,dynamic> value,String uid)async{
    final key='$uid|$chat';
    final now=DateTime.now().millisecondsSinceEpoch;
    if(now-(_photoWarm547[key]??0)<60000)return;
    _photoWarm547[key]=now;
    if(_photoWarm547.length>200)_photoWarm547.remove(_photoWarm547.keys.first);
    try{
      var url=(value['groupPhotoUrl']??'').toString();
      if(value['isGroup']!=true){
        final others=List<String>.from(value['members']??const[]).where((id)=>id!=uid);
        if(others.length!=1)return;
        final profile=await FirebaseFirestore.instance.collection('users').doc(others.single)
          .get(const GetOptions(source:Source.cache));
        url=(profile.data()?['photoUrl']??'').toString();
      }
      if(url.isEmpty||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      var file=await _ngelx464GenelResimCache.getFileFromCache(url);
      file??=await DefaultCacheManager().getFileFromCache(url);
      if(file==null||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      await channel.invokeMethod<void>('noteCallPhoto547',
        {'uid':uid,'chat':chat,'path':file.file.path});
    }catch(_){ }
  }
  bool _registering453=false;''')
    return s+'\n'+TAG+'\n'

if __name__=='__main__':
    root=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app')
    for p,fn in [(root/'IncomingCallActivity470.kt',incoming_source),
                 (root/'MainActivity.kt',activity_source),
                 (Path('app/lib/build448_incoming_calls.dart'),calls_source)]:
        p.write_text(fn(p.read_text()))
    (root/'CallPhoto547.kt').write_text(Path('tools/build547_call_photo.kt').read_text())
