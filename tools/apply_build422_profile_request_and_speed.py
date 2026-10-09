#!/usr/bin/env python3
"""Build 422: incoming request Reply on profile, full joined date, cached listeners.

Mutates only UI/client request processing. Preserve Firestore rules, existing
outgoing request logic, friends/followers count and coverless/covered modes.
"""
from pathlib import Path
import re
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

# A pending incoming request is looked up from the authenticated recipient,
# never accepted using stale notification text. Same atomic social writes as
# the existing inbox Build397 handler, now usable from a person's profile.
anchor="Future<bool> sosyalIstekGonder({"
if s.count(anchor)!=1:raise SystemExit('Build422 social helper anchor drift')
helper="""Future<void> ngelxGelenSosyalIstekCevapla({
  required String gonderenUid,
  required String tur,
  required bool kabul,
})async{
  final ben=FirebaseAuth.instance.currentUser?.uid;
  if(ben==null||gonderenUid.isEmpty||gonderenUid==ben||
      (tur!='friend_request'&&tur!='follow_request')){
    throw StateError('Geçerli bir gelen istek bulunamadı.');
  }
  final db=FirebaseFirestore.instance;
  final ref=sosyalIstekRef(gonderenUid,ben,tur);
  final istek=await ref.get(const GetOptions(source:Source.server))
    .timeout(const Duration(seconds:8));
  if(!istek.exists||istek.data()?['status']!='pending'){
    throw StateError('Bu istek artık beklemede değil.');
  }
  final bildirimId=(istek.data()?['notificationId']??'').toString();
  DocumentReference<Map<String,dynamic>>? bildirimRef;
  if(bildirimId.isNotEmpty){
    final refN=db.collection('notifications').doc(bildirimId);
    final n=await refN.get(const GetOptions(source:Source.server))
      .timeout(const Duration(seconds:8));
    if(n.exists&&n.data()?['toUid']==ben&&
        n.data()?['status']=='pending'&&n.data()?['fromUid']==gonderenUid){
      bildirimRef=refN;
    }
  }
  if(kabul){
    final iki=await Future.wait([
      db.collection('users').doc(ben).get(),
      db.collection('users').doc(gonderenUid).get(),
    ]);
    final b=iki[0].data()??<String,dynamic>{};
    final g=iki[1].data()??<String,dynamic>{};
    List<String> ids(dynamic v)=>v is Iterable
      ?v.map((x)=>x.toString()).toList():<String>[];
    if(g['deactivated']==true||ids(b['blocked']).contains(gonderenUid)||
        ids(g['blocked']).contains(ben)){
      throw StateError('Engellenmiş veya kapatılmış hesap isteği kabul edilemez.');
    }
  }
  final batch=db.batch();
  batch.update(ref,{
    'status':kabul?'accepted':'rejected',
    'answeredAt':FieldValue.serverTimestamp(),
    'updatedAt':FieldValue.serverTimestamp(),
  });
  if(bildirimRef!=null){
    batch.update(bildirimRef,{
      'status':kabul?'accepted':'rejected','read':true,
      'answeredAt':FieldValue.serverTimestamp(),
    });
  }
  if(kabul&&tur=='friend_request'){
    batch.set(db.collection('users').doc(ben),{
      'friends':FieldValue.arrayUnion([gonderenUid]),
    },SetOptions(merge:true));
    batch.set(db.collection('users').doc(gonderenUid),{
      'friends':FieldValue.arrayUnion([ben]),
    },SetOptions(merge:true));
    final sirali=<String>[ben,gonderenUid]..sort();
    batch.set(db.collection('friendships').doc(sirali.join('_')),{
      'members':sirali,'active':true,'since':FieldValue.serverTimestamp(),
      'updatedAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
  }
  if(kabul&&tur=='follow_request'){
    batch.set(db.collection('users').doc(ben),{
      'followers':FieldValue.arrayUnion([gonderenUid]),
    },SetOptions(merge:true));
    batch.set(db.collection('users').doc(gonderenUid),{
      'following':FieldValue.arrayUnion([ben]),
    },SetOptions(merge:true));
  }
  await batch.commit().timeout(const Duration(seconds:12));
  if(kabul){
    unawaited(uygulamaBildirimiGonder(toUid:gonderenUid,fromUid:ben,
      tur:tur=='friend_request'?'friend_accepted':'follow_accepted',
      metin:tur=='friend_request'
        ?'arkadaşlık isteğini kabul etti':'takip isteğini kabul etti',
    ).catchError((_){ }));
  }
}

"""
s=s.replace(anchor,helper+anchor,1)

# Embed incoming-request state into the existing friend button. It preserves
# the legacy outgoing request/cancel and friendship removal callbacks.
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
v=s[a:b]
needle='final bekliyor=sunucuBekliyor||_yerelArkadasIstekleri.contains(uid);'
if v.count(needle)!=1:raise SystemExit('Build422 visitor friend pending anchor')
start=v.index('return SizedBox(width:double.infinity,child:FilledButton.icon(',v.index(needle))
end=v.index('\n                      },',start)
old=v[start:end]
needed=['if(arkadas){',"arkadas?'Arkadaşsınız'","onPressed:me==null?null:()async{"]
for n in needed:
    if n not in old:raise SystemExit('Build422 friend widget drift: '+n)
old=old.replace("""if(arkadas){
                              await _arkadasliktanCikar""",
"""if(gelenBekliyor&&!arkadas){
                              final secim=await showModalBottomSheet<bool>(
                                context:context,backgroundColor:Colors.white,
                                showDragHandle:true,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(
                                  child:Column(mainAxisSize:MainAxisSize.min,children:[
                                    const ListTile(title:Text('Arkadaşlık isteğini yanıtla',
                                      style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
                                    ListTile(leading:const Icon(Icons.check_circle,color:mor),
                                      title:const Text('Kabul et',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
                                      onTap:()=>Navigator.pop(c,true)),
                                    ListTile(leading:const Icon(Icons.close_rounded),
                                      title:const Text('Reddet',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
                                      onTap:()=>Navigator.pop(c,false)),
                                  ]))));
                              if(secim!=null){
                                try{
                                  await ngelxGelenSosyalIstekCevapla(
                                    gonderenUid:uid,tur:'friend_request',kabul:secim);
                                  if(context.mounted)ScaffoldMessenger.of(context)
                                    .showSnackBar(SnackBar(content:Text(
                                      secim?'Arkadaşlık kabul edildi.':'İstek reddedildi.')));
                                }catch(e){
                                  if(context.mounted)ScaffoldMessenger.of(context)
                                    .showSnackBar(SnackBar(content:Text(
                                      e is StateError?e.message.toString():'İstek işlenemedi.')));
                                }
                              }
                              return;
                            }
                            if(arkadas){
                              await _arkadasliktanCikar""",1)
old=old.replace("arkadas?'Arkadaşsınız':(bekliyor?'Arkadaşlık isteği bekliyor':'Arkadaş ekle')",
                "arkadas?'Arkadaşsınız':(gelenBekliyor?'Yanıtla':(bekliyor?'Arkadaşlık isteği bekliyor':'Arkadaş ekle'))",1)
old=old.replace("icon:Icon(arkadas?Icons.people_alt_rounded:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1_rounded)",
                "icon:Icon(arkadas?Icons.people_alt_rounded:(gelenBekliyor?Icons.mark_email_unread_rounded:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1_rounded))",1)
wrapped="""return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                        stream:me==null?null:sosyalIstekRef(uid,me,'friend_request').snapshots(),
                        builder:(_,gelenSnap){
                          if(me!=null&&!gelenSnap.hasData){
                            return const SizedBox(height:48,child:Center(
                              child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                          }
                          final gelenBekliyor=gelenSnap.data?.data()?['status']=='pending';
                          """+old+"""
                        },
                      );"""
v=v[:start]+wrapped+v[end:]
s=s[:a]+v+s[b:]

# Real joined date is preserved but no longer ellipsized on the owner's
# narrow location+date row. Both cover styles share this owner metadata.
a=s.index('class _ProfilPageState extends State<ProfilPage>')
b=s.index('\nclass _ProfilEtkilesimRozeti',a)
owner=s[a:b]
old="""Row(mainAxisAlignment:MainAxisAlignment.start,children:[const Icon(Icons.location_on_outlined,color:Colors.black54,size:18),const SizedBox(width:4),Flexible(child:Text(konum,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54))),const SizedBox(width:13),const Icon(Icons.calendar_month_outlined,color:Colors.black54,size:18),const SizedBox(width:4),Flexible(child:Text(katilim,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)))])"""
new="""Column(children:[
                    Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                      const Icon(Icons.location_on_outlined,color:Colors.black54,size:18),
                      const SizedBox(width:5),
                      Flexible(child:Text(konum,textAlign:TextAlign.center,
                        style:const TextStyle(color:Colors.black54))),
                    ]),
                    const SizedBox(height:5),
                    Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                      const Icon(Icons.calendar_month_outlined,color:Colors.black54,size:18),
                      const SizedBox(width:5),
                      Flexible(child:Text(katilim,textAlign:TextAlign.center,
                        softWrap:true,style:const TextStyle(color:Colors.black54))),
                    ]),
                  ])"""
if owner.count(old)!=1:
    k=owner.find('Text(katilim')
    print('Build422 owner date source nearby:',repr(owner[max(0,k-650):k+260]),flush=True)
    raise SystemExit('Build422 full join date layout drift')
owner=owner.replace(old,new,1)
s=s[:a]+owner+s[b:]

# Avoid repeated Firestore stream subscriptions as each feed/inbox rebuilds.
feed_a=s.index('class _VideoAkisiState extends State<VideoAkisi>')
feed_b=s.index('\nclass ',feed_a+30)
feed=s[feed_a:feed_b]
marker='  final PageController akisKontrol=PageController();'
if feed.count(marker)!=1:raise SystemExit('Build422 feed stream marker drift')
feed=feed.replace(marker,marker+"""
  late final Stream<QuerySnapshot<Map<String,dynamic>>> _ngelxSabitAkis=
    FirebaseFirestore.instance.collection('videos')
      .orderBy('createdAt',descending:true).limit(50).snapshots();
""",1)
oldStream="""stream:FirebaseFirestore.instance
          .collection('videos')
          .orderBy('createdAt',descending:true)
          .limit(50)
          .snapshots(),"""
if feed.count(oldStream)!=1:raise SystemExit('Build422 feed stream identity drift')
feed=feed.replace(oldStream,'stream:_ngelxSabitAkis,',1)
feed=feed.replace("""return const Center(child:CircularProgressIndicator(color:mavi));""",
"""return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
              CircularProgressIndicator(color:mavi),
              SizedBox(height:14),
              Text('Akış hazırlanıyor...',style:TextStyle(color:Colors.white70)),
            ]));""",1)
s=s[:feed_a]+feed+s[feed_b:]

# The inbox renders the same Firestore query under multiple tabs. Cache the
# Stream objects per UID and limit so Flutter doesn't resubscribe on rebuild.
a=s.index('class _MesajPageState extends State<MesajPage>')
b=s.index('\nclass ArsivSohbetlerPage',a)
inbox=s[a:b]
mark='  String? get uid=>FirebaseAuth.instance.currentUser?.uid;'
if inbox.count(mark)!=1:raise SystemExit('Build422 inbox stream marker drift')
new=mark+"""
  final Map<String,Stream<QuerySnapshot<Map<String,dynamic>>>> _akislari={};
  Stream<QuerySnapshot<Map<String,dynamic>>> _sohbetAkisi(String ben,int limit)=>
    _akislari.putIfAbsent('chat|'+ben+'|'+limit.toString(),
      ()=>FirebaseFirestore.instance.collection('chats')
        .where('members',arrayContains:ben).limit(limit).snapshots());
  Stream<QuerySnapshot<Map<String,dynamic>>> _bildirimAkisi(String ben,int limit)=>
    _akislari.putIfAbsent('notification|'+ben+'|'+limit.toString(),
      ()=>FirebaseFirestore.instance.collection('notifications')
        .where('toUid',isEqualTo:ben).limit(limit).snapshots());
"""
inbox=inbox.replace(mark,new,1)
for coll,method,field in [('chats','_sohbetAkisi','members'),('notifications','_bildirimAkisi','toUid')]:
    if coll=='chats':
        pat=r"FirebaseFirestore\.instance\.collection\('chats'\)\.where\('members',arrayContains:ben\)\.limit\((\d+)\)\.snapshots\(\)"
    else:
        pat=r"FirebaseFirestore\.instance\.collection\('notifications'\)\.where\('toUid',isEqualTo:ben\)\.limit\((\d+)\)\.snapshots\(\)"
    # Skip the new definitions: they contain a line break before the .where.
    inbox,n=re.subn(pat,lambda m:method+'(ben,'+m.group(1)+')',inbox)
    if n<1:raise SystemExit('Build422 no '+coll+' duplicate listener to stabilize')
s=s[:a]+inbox+s[b:]
p.write_text(s,encoding='utf-8')
print('Build422: profile incoming friend Reply, full date, stable feed/inbox streams, descriptive loading.')
