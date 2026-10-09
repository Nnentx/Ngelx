#!/usr/bin/env python3
"""Build422: Messenger-style pending requests and one inbox, no duplicate Activity.

Reuse the EXISTING Build397 acceptance transaction. Only navigation/UI changes,
no Firestore rule changes or deletion of notifications. Exact source contracts.
"""
from pathlib import Path
import re
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class MesajPage extends StatefulWidget')
b=s.index('\nclass ArsivSohbetlerPage',a)
inbox=s[a:b]

def once(old,new,label):
    global inbox
    n=inbox.count(old)
    if n!=1:raise SystemExit('Build422 inbox '+label+': '+str(n))
    inbox=inbox.replace(old,new,1)

once('const MesajPage({super.key});',
     "const MesajPage({super.key,this.initialFilter='Tümü'});\n  final String initialFilter;",
     'initial tab')
once("String filtre='Tümü';",
     'late String filtre=widget.initialFilter;',
     'state initializes selected tab')

# Inbox notification rows open the sender's profile directly; never a second
# Activity screen. Missing sender stays in current section, not an empty route.
once("if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));",
     """final from=(v['fromUid']??'').toString();
                  if(context.mounted&&from.isNotEmpty){
                    await Navigator.push(context,MaterialPageRoute(
                      builder:(_)=>KullaniciProfilPage(uid:from)));
                  }""",
     'notification inline profile')
once("""if(pending)setState(()=>filtre='İstekler');
                      else Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));""",
     """final from=(v['fromUid']??'').toString();
                      if(from.isNotEmpty){
                        await Navigator.push(context,MaterialPageRoute(
                          builder:(_)=>KullaniciProfilPage(uid:from)));
                      }else{
                        setState(()=>filtre=pending?'İstekler':'Bildirimler');
                      }""",
     'all-tab notification profile')

# Remove the redundant request-summary tile; the rows now appear here.
start=inbox.index("""              Container(
                decoration:BoxDecoration(color:const Color(0xFFF7F9FC),borderRadius:BorderRadius.circular(20)),""")
end=inbox.index("              const SizedBox(height:10),",start)
inbox=inbox[:start]+"""              Padding(
                padding:const EdgeInsets.fromLTRB(6,6,6,12),
                child:Text(lt('Arkadaşlık ve takip istekleri','Friend and follow requests'),
                  style:const TextStyle(fontSize:18,fontWeight:FontWeight.w900)),
              ),
"""+inbox[end:]

# Existing Build397 request list is a secure, working acceptance path:
# keep the caller, build a clearer Messenger-like display around it.
patch397=Path('tools/apply_build397_inbox_complete_fixes.py').read_text(encoding='utf-8')
m=re.search(r"new_request_map = r'''(.*?)'''",patch397,re.S)
if not m or inbox.count(m.group(1))!=1:
    raise SystemExit('Build422 generated Build397 row contract drift')
old=m.group(1)
new="""                ...sosyal.take(40).map((d){
                  final v=d.data(),from=(v['fromUid']??'').toString();
                  final tur=(v['type']??'').toString();
                  final arkadaslik=tur=='friend_request';
                  return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                    stream:from.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(from).snapshots(),
                    builder:(_,u){
                      final profil=u.data?.data()??<String,dynamic>{};
                      final ad=(profil['displayName']??profil['username']??
                        v['senderName']??v['fromName']??'NgelX kullanıcısı').toString();
                      final foto=(profil['photoUrl']??v['photoUrl']??'').toString();
                      if(sohbetSorgu.isNotEmpty&&!ad.toLowerCase().contains(sohbetSorgu)){
                        return const SizedBox.shrink();
                      }
                      final gorunur=profil['showFriends']!=false&&
                        profil['friendsVisibility']!='only_me'&&
                        profil['friendsVisibility']!='private';
                      final karsinin=profil['friends'] is Iterable
                        ?(profil['friends'] as Iterable).map((e)=>e.toString()).toSet()
                        :<String>{};
                      final ortak=gorunur
                        ?arkadaslar.where(karsinin.contains).where((id)=>id!=from&&id!=ben).toList()
                        :<String>[];
                      return Container(
                        margin:const EdgeInsets.only(bottom:10),
                        padding:const EdgeInsets.all(12),
                        decoration:BoxDecoration(color:Colors.white,
                          borderRadius:BorderRadius.circular(18),
                          border:Border.all(color:const Color(0xFFECECF4))),
                        child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                          InkWell(
                            onTap:from.isEmpty?null:()=>Navigator.push(context,
                              MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:from))),
                            child:Row(children:[
                              CircleAvatar(radius:28,
                                backgroundColor:const Color(0xFFF1EBFE),
                                backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),
                                child:foto.isEmpty?const Icon(Icons.person_rounded,color:mor):null),
                              const SizedBox(width:12),
                              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                                Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,
                                  style:const TextStyle(fontSize:15,fontWeight:FontWeight.w900)),
                                Text(arkadaslik?'Arkadaşlık isteği':'Takip isteği',
                                  style:const TextStyle(color:Colors.black54,fontSize:12)),
                                if(ortak.isNotEmpty)Row(children:[
                                  for(final id in ortak.take(3))
                                    Padding(padding:const EdgeInsets.only(right:2),
                                      child:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                                        future:_kullaniciGetir(id),
                                        builder:(_,x){
                                          final photo=(x.data?.data()?['photoUrl']??'').toString();
                                          return CircleAvatar(radius:9,
                                            backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
                                            child:photo.isEmpty?const Icon(Icons.person,size:10):null);
                                        })),
                                  const SizedBox(width:5),
                                  Expanded(child:Text(ortak.length.toString()+' ortak arkadaş',
                                    maxLines:1,overflow:TextOverflow.ellipsis,
                                    style:const TextStyle(color:Colors.black54,fontSize:11))),
                                ]),
                                Text(zamanKisa(v['createdAt']),
                                  style:const TextStyle(color:Colors.black38,fontSize:11)),
                              ])),
                              const Icon(Icons.chevron_right,color:Colors.black38),
                            ]),
                          ),
                          const SizedBox(height:10),
                          Row(children:[
                            Expanded(child:FilledButton(
                              style:FilledButton.styleFrom(backgroundColor:mor,
                                foregroundColor:Colors.white,
                                minimumSize:const Size.fromHeight(42)),
                              onPressed:()=>gelenKutusuIsteginiSonuclandir(d,true),
                              child:const Text('Onayla'))),
                            const SizedBox(width:8),
                            Expanded(child:OutlinedButton(
                              style:OutlinedButton.styleFrom(
                                minimumSize:const Size.fromHeight(42),
                                backgroundColor:const Color(0xFFF0F0F3),
                                foregroundColor:Colors.black87,side:BorderSide.none),
                              onPressed:()=>gelenKutusuIsteginiSonuclandir(d,false),
                              child:const Text('Sil'))),
                          ]),
                        ]),
                      );
                    },
                  );
                }),"""
inbox=inbox.replace(old,new,1)

# Do not remove the existing Activity implementation until old deep-links are
# audited. Remove user-facing navigations; legacy activity links safely land in
# the inbox instead of duplicating activities.
inbox=inbox.replace('const AktivitePage()', "const MesajPage(initialFilter:'Bildirimler')")
s=s[:a]+inbox+s[b:]
owner_a=s.index('class _ProfilPageState extends State<ProfilPage>')
owner_b=s.index('\nclass _ProfilEtkilesimRozeti',owner_a)
owner=s[owner_a:owner_b]
owner=owner.replace('const AktivitePage()', "const MesajPage(initialFilter:'Bildirimler')")
s=s[:owner_a]+owner+s[owner_b:]
p.write_text(s,encoding='utf-8')
print('Build422 inbox: direct profiles, no duplicate Activity routes, pending request Onayla/Sil, privacy-aware mutuals.')
