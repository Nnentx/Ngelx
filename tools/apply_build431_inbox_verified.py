from pathlib import Path
s=Path('app/lib/main.dart').read_text()
def one(old,new):
 global s
 if s.count(old)!=1:raise SystemExit('Build431 anchor drift: '+old[:100]+' count='+str(s.count(old)))
 s=s.replace(old,new,1)
a=s.index('class _MesajPageState');b=s.index('class MesajIstekleriPage',a)
part=s[a:b]
# A keyed stream prevents Flutter from retaining a chat snapshot in a notification pane.
part=part.replace('stream:_bildirimAkisi(ben,100),',"key:ValueKey('inbox-notifications-'+ben),\n        stream:_bildirimAkisi(ben,100),")
part=part.replace('stream:_bildirimAkisi(ben,120),',"key:ValueKey('inbox-requests-'+ben),\n        stream:_bildirimAkisi(ben,120),")
part=part.replace('where((d)=>ngelxAktiviteBildirimiGosterilir(d.data()))','where((d)=>ngelxBildirimKaydiGecerli(d.reference.parent.path,d.data(),ben)&&ngelxAktiviteBildirimiGosterilir(d.data()))')
part=part.replace("final metin=(v['text']??v['message']??v['content']??lt('Yeni bildirim','New notification')).toString();","final metin=ngelxBildirimMetni(v);")
part=part.replace("subtitle:Text(zamanKisa(v['createdAt']),","subtitle:Text(ngelxBildirimTarihi(v)==null?'Tarih bilgisi yok':zamanKisa(ngelxBildirimTarihi(v)),")
part=part.replace("try{await d.reference.set({'read':true},SetOptions(merge:true));}catch(_){}","try{await d.reference.update({'read':true});}catch(_){}")
part=part.replace('if(!ngelxAktiviteBildirimiGosterilir(v))continue;',"if(!ngelxBildirimKaydiGecerli(d.reference.parent.path,v,ben)||!ngelxAktiviteBildirimiGosterilir(v))continue;")
# The three request categories remain visible even when a category is empty.
start=part.index('              Padding(\n',part.index('Widget isteklerIcerigi()'))
end=part.index('              const SizedBox(height:10),',start)
part=part[:start]+'''              ...['follow_request','friend_request'].map((kind){
                final count=sosyal.where((d)=>d.data()['type']==kind).length;
                final follow=kind=='follow_request';
                return Card(color:Colors.white,child:ListTile(
                  leading:const Icon(Icons.person_add_alt_1_rounded,color:mor),
                  title:Text(follow?'Takip istekleri':'Arkadaşlık istekleri',style:const TextStyle(fontWeight:FontWeight.w900)),
                  subtitle:Text('$count bekleyen istek'),
                  trailing:const Icon(Icons.chevron_right_rounded),
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>AktivitePage(initialFilter:follow?'follow_requests':'friend_requests'))),
                ));
              }),
'''+part[end:]
part=part.replace("subtitle:Text(t('messageRequestsSub')),",'''subtitle:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:_sohbetAkisi(ben,200),
                    builder:(_,cs){
                      if(cs.hasError)return const Text('İstek sayısı yüklenemedi');
                      if(!cs.hasData)return const Text('İstekler yükleniyor…');
                      final count=cs.data!.docs.where((d)=>!arsivSohbetler.contains(d.id)&&ngelxBekleyenMesajIstegi(d.data(),ben,arkadaslar)).length;
                      return Text('$count bekleyen mesaj isteği');
                    }),''')
old="final pending=membersList.length==2&&!arkadaslar.contains(other)&&(v['lastMessage']??'').toString().trim().isNotEmpty&&v['isGroup']!=true&&(v['requestRecipientUid']??'').toString()==ben&&v['requestAccepted_$ben']!=true&&v['requestRejected_$ben']!=true&&!List<String>.from(v['hiddenFor']??const[]).contains(ben);"
assert old in part
part=part.replace(old,'final pending=ngelxBekleyenMesajIstegi(v,ben,arkadaslar);').replace("              final other=membersList.firstWhere((id)=>id!=ben,orElse:()=>ben!);\n",'').replace("              final membersList=List<String>.from(v['members']??const[]);\n",'')
s=s[:a]+part+s[b:]
# Route the category cards directly to their existing Activity filters.
one('const AktivitePage({super.key});',"final String initialFilter;\n  const AktivitePage({super.key,this.initialFilter='all'});")
one("String _filtre='all';","late String _filtre=widget.initialFilter;")
# Ignore legacy read-only shells; they are not activities.
one("return tur!='message';","return tur!='message'&&(tur.isNotEmpty||(v['eventKind']??'').toString().isNotEmpty||['text','message','content'].any((k)=>(v[k]??'').toString().trim().isNotEmpty));")
# Match request eligibility and query window in the list and badge.
a=s.index('class MesajIstekleriPage');b=s.index('class MesajIstegiOnizlemePage',a)
part=s[a:b].replace('.limit(60).snapshots()', '.limit(200).snapshots()')
part=part.replace('          final arkadaslar =',"          if(!me.hasData&&!me.hasError)return const Center(child:CircularProgressIndicator(color:mor));\n          if(me.hasError)return const Center(child:Text('İstekler yüklenemedi. Geri dönüp tekrar dene.'));\n          final archived=Set<String>.from(List<dynamic>.from(me.data?.data()?['archivedChats']??const[]));\n          final arkadaslar =")
start=part.index('              final docs = ');end=part.index('              if(docs.isEmpty)',start)
part=part[:start]+'''              if(s.connectionState==ConnectionState.waiting&&!s.hasData)return const Center(child:CircularProgressIndicator(color:mor));
              if(s.hasError)return const Center(child:Text('Mesaj istekleri yüklenemedi. Geri dönüp tekrar dene.'));
              final docs=(s.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[])
                .where((d)=>!archived.contains(d.id)&&ngelxBekleyenMesajIstegi(d.data(),uid,arkadaslar)).toList();
'''+part[end:]
s=s[:a]+part+s[b:]
s+='\n'+Path('tools/build431_notification_helpers.dart').read_text()
s=s.replace("defaultValue: '430'","defaultValue: '431'").replace("defaultValue: '1.0.205'","defaultValue: '1.0.206'")
Path('app/lib/main.dart').write_text(s)
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.205+430','version: 1.0.206+431'))
print('Build431 keyed notification pane, request categories and shared eligibility applied')
