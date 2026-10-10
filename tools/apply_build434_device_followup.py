from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:150]
 s=s.replace(a,b)
rep("defaultValue: '1.0.207'","defaultValue: '1.0.209'")
rep("defaultValue: '432'","defaultValue: '434'")
# One status-aware text source across the inbox, all tab, and profile bell.
rep("String ngelxBildirimMetni(Map<String,dynamic> v) {","String ngelxBildirimMetni(Map<String,dynamic> v) {\n  final outcome=ngelx434IstekSonucu(v);if(outcome!=null)return outcome;")
rep("    final tam=(v['text']??v['message']??v['content']??'Yeni bildirim').toString();","    final tam=ngelxBildirimMetni(v);")
rep("style:const TextStyle(fontWeight:FontWeight.w900)),\n            const TextSpan(text:' • Canlı yayın sona erdi')","style:const TextStyle(color:mor,fontWeight:FontWeight.w900)),\n            const TextSpan(text:' • Canlı yayın sona erdi')")
rep("return Text(ad+' adlı kullanıcının '+grup+' grubuna katılma isteği '+sonuc+'.',\n               style:TextStyle(fontWeight:okundu?FontWeight.w500:FontWeight.w800));","return ngelx433RenkliBildirim({...v,'text':ad+' adlı kullanıcının '+grup+' grubuna katılma isteği '+sonuc+'.','read':okundu},maxLines:4);")
# The Activity handler previously completed only one notification. Finish older
# duplicates in the same commit, without touching a newer request generation.
anchor="    final toplu=FirebaseFirestore.instance.batch();\n    toplu.update(belge.reference,{"
rep(anchor,"""    final toplu=FirebaseFirestore.instance.batch();
    try{
    final copies=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).get().timeout(const Duration(seconds:10));
    final generation=(veri['requestGeneration']??'').toString();
    final created=veri['createdAt'];
    for(final copy in copies.docs){
      final cv=copy.data(),stamp=cv['createdAt'];
      if(copy.id==belge.id||cv['fromUid']!=gonderen||cv['type']!=istekTuru||cv['status']!='pending')continue;
      final same=(cv['requestGeneration']??'').toString()==generation;
      final older=stamp is Timestamp&&created is Timestamp&&stamp.compareTo(created)<=0;
      if(same||older)toplu.update(copy.reference,{'status':kabul?'accepted':'rejected','read':true,'answeredAt':FieldValue.serverTimestamp()});
    }
    }catch(_){/* Old copies retry on refresh; legitimate answer still proceeds. */}
    toplu.update(belge.reference,{""")
# Resolve legacy pending rows against the sender relationship and canonical
# request before displaying them. A failed read never invents an outcome.
anchor="          return goster(v);\n        },\n      );\n    }\n\n    Widget ngelxSekmeliSayaclar()"
rep(anchor,"""          if(tur=='friend_request'||tur=='follow_request'){
            final target=(v['toUid']??ben??'').toString();
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              stream:from.isEmpty?null:sosyalIstekRef(from,target,tur).snapshots(),
              builder:(_,request){
                final rv=request.data?.data();
                if(rv!=null){
                  final id=(rv['notificationId']??'').toString();
                  if(rv['status']!='pending')v['status']=rv['status'];
                  else if(id.isNotEmpty&&id!=(v['_notificationId']??''))v['status']='superseded';
                }
                return goster(v);
              },
            );
          }
          return goster(v);
        },
      );
    }

    Widget ngelxSekmeliSayaclar()""")
rep("bildirimGonderenIle(d.data(),(v)","bildirimGonderenIle({...d.data(),'_notificationId':d.id},(v)")
# Pending rows are redundant with dedicated category pages. Keep the three
# request cards only, as explicitly requested by the user.
a=s.index('              if(sosyal.isNotEmpty)...[',s.index('    Widget isteklerIcerigi()'))
b=s.index('\n            ],',a)
s=s[:a]+s[b:]
# Avatar presence in both inbox list variants and the friend list.
a="leading:CircleAvatar(radius:27,backgroundColor:const Color(0xFFEFF3F8),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,color:Color(0xFF61708D)):null),"
rep(a,"leading:Ngelx434AktifAvatar(uid:other,photo:foto,initial:p),")
a="""          leading:CircleAvatar(
            radius:27,
            backgroundColor:const Color(0xFFF1EEFF),
            backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),
            child:foto.isEmpty?const Icon(Icons.person_rounded,color:mor):null,
          ),"""
rep(a,"          leading:Ngelx434AktifAvatar(uid:id,photo:foto,initial:v),")
rep("subtitle:Text(alt,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:13)),","subtitle:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(alt,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:13)),AktiflikDurumuYazisi(uid:id)]),")
a=s.index('  String _etiket(Map<String,dynamic> v){',s.index('class _AktiflikDurumuYazisiState'));b=s.index('  @override Widget build',a)
s=s[:a]+"  String _etiket(Map<String,dynamic> v)=>ngelx434Aktiflik(v);\n"+s[b:]
rep('  @override void initState(){super.initState();tercihleriGetir();}',"  @override void initState(){super.initState();tercihleriGetir();final me=uid;if(me!=null)unawaited(ngelx434EskiIstekleriUzlastir(me));}")
rep('    _notificationCache.retry();', '    _notificationCache.retry();\n    unawaited(ngelx434EskiIstekleriUzlastir(ben));')
rep('      _kullaniciCache.clear();', '      unawaited(ngelx434EskiIstekleriUzlastir(ben));\n      _kullaniciCache.clear();')
s+='\n'+Path('tools/build434_presence.dart').read_text();p.write_text(s)
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.208+433','version: 1.0.209+434'))
print('Build434 device fixes applied')
