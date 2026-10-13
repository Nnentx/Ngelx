from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text();s=s.replace("part 'live_broadcast_studio.dart';","part 'live_broadcast_studio.dart';\npart 'community450.dart';")
a=s.index('class _KesfetPageState');b=s.index('class _TrendEtiketi',a);x=s[a:b]
x=x.replace('int kategori=-1;','int kategori=0;').replace('int kategori = -1;','int kategori = 0;')
x=x.replace("IconButton(tooltip:t('search'),onPressed:_aramaAc,icon:const Icon(Icons.search_rounded,color:Colors.black,size:28)),","IconButton(tooltip:'Topluluk oluştur',onPressed:()async{if(await misafirEngeli(context))return;if(context.mounted)Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXCommunityCreate450()));},icon:const Icon(Icons.add_circle_outline_rounded,color:mor,size:28)),")
start=x.index('          SliverToBoxAdapter(child:SizedBox(\n            height:52,');end=x.index('          if(kategori==-1)',start)
x=x[:start]+'''          SliverToBoxAdapter(child:NgelXDiscoveryTabs450(selected:kategori,onSelected:(value)=>setState(()=>kategori=value))),
          if(kategori==0)SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.fromLTRB(16,8,16,0),child:Align(alignment:Alignment.centerLeft,child:ActionChip(avatar:const Icon(Icons.mic,size:16),label:const Text('Sesli odalar'),onPressed:()=>setState(()=>kategori=1))))),
          if(kategori==5)const SliverToBoxAdapter(child:NgelXCommunityDirectory450()),
''' +x[end:]
x=x.replace("(Icons.groups_rounded,t('groups')),","(Icons.groups_rounded,t('groups')),\n              (Icons.forum_rounded,'Topluluk'),")
x=x.replace("color:const Color(0xFFF7F7FA),borderRadius:BorderRadius.circular(20),border:Border.all(color:Colors.black.withValues(alpha:.05))","color:Colors.white,borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE7E7ED))")
x=x.replace("color:const Color(0xFFF6F3FF),borderRadius:BorderRadius.circular(20),border:Border.all(color:mor.withValues(alpha:.09))","color:Colors.white,borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE7E7ED))")
x=x.replace("Text(aciklama.isEmpty?'NgelX topluluğu':aciklama","Text(aciklama.isEmpty||aciklama=='NgelX topluluğu'?'Sohbete katıl, birlikte paylaş':aciklama")
x=x.replace("Text('$sayi ${t('member')}',style:const TextStyle(color:Colors.black45,fontSize:12)),","NgelXFounder450(uid:(v['createdBy']??'').toString()),\n              Text('$sayi üye · ${v['joinApproval']==true?'Onay gerekli':'Herkese açık'}',style:const TextStyle(color:Colors.black45,fontSize:11)),")
x=x.replace("onPressed:pending&&!katildi?null:()=>_grupDurumuDegistir(id,katildi,ad:ad,foto:foto)","onPressed:pending&&!katildi?()async{try{await FirebaseFirestore.instance.collection('chats').doc(id).collection('joinRequests').doc(ben).update({'status':'cancelled','updatedAt':FieldValue.serverTimestamp()});}catch(e){if(context.mounted)_communityError450(context,e);}}:()=>_grupDurumuDegistir(id,katildi,ad:ad,foto:foto)")
x=x.replace("style:FilledButton.styleFrom(backgroundColor:katildi?const Color(0xFFECECF2):mor,foregroundColor:katildi?Colors.black87:Colors.white,padding:const EdgeInsets.symmetric(horizontal:13)),","style:FilledButton.styleFrom(backgroundColor:katildi||pending?const Color(0xFFF0E8FF):mor,foregroundColor:katildi||pending?mor:Colors.white,padding:const EdgeInsets.symmetric(horizontal:10)),")
x=x.replace("pending?'İstek gönderildi':t('join')","pending?'İptal et':v['joinApproval']==true?'İstek gönder':t('join')")
# Keep existing joins and membership server checks; display pending status explicitly.
x=x.replace("final pending=request.data?.data()?['status']=='pending';return FilledButton(","final pending=request.data?.data()?['status']=='pending';return Column(mainAxisSize:MainAxisSize.min,children:[if(pending)const Text('İstek gönderildi',style:TextStyle(color:mor,fontSize:10)),FilledButton(")
x=x.replace("              );},\n            ),","              )]);},\n            ),")
# Live discovery becomes a 2-column grid, with the existing live join action untouched.
start=x.index('  List<Widget> _canliSliverleri(');end=x.index('  List<Widget> _trendSliverleri()',start)
x=x[:start]+'''  List<Widget> _canliSliverleri({bool trend=false})=>[
    SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.fromLTRB(16,18,16,10),child:Text(trend?'Öne çıkan yayınlar':'Canlı yayınlar',style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)))),
    StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('live_streams').where('active',isEqualTo:true).limit(20).snapshots(),builder:(c,snap){
      if(!snap.hasData)return SliverToBoxAdapter(child:SizedBox(height:160,child:snap.hasError?_bosKart('Yayınlar yüklenemedi',Icons.cloud_off):const Center(child:CircularProgressIndicator())));
      final ds=snap.data!.docs.where((d)=>ngelxCanliKaydiTaze(d.data())).toList()..sort((a,b)=>ngelxCanliTrendPuani(b.data()).compareTo(ngelxCanliTrendPuani(a.data())));
      if(ds.isEmpty)return SliverToBoxAdapter(child:SizedBox(height:180,child:_bosKart(t('noLive'),Icons.live_tv_outlined)));
      return SliverPadding(padding:const EdgeInsets.symmetric(horizontal:16),sliver:SliverGrid(gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:2,childAspectRatio:.76,crossAxisSpacing:10,mainAxisSpacing:10),delegate:SliverChildBuilderDelegate((c,i){final v=ds[i].data();return InkWell(onTap:()=>_yayinIzle(context,v,ds[i].id),child:ClipRRect(borderRadius:BorderRadius.circular(18),child:Stack(fit:StackFit.expand,children:[Container(color:const Color(0xFF292348),child:(v['coverUrl']??'').toString().isEmpty?const Icon(Icons.videocam,color:Colors.white38,size:50):NgelXAgResmi(imageUrl:v['coverUrl'],fit:BoxFit.cover)),const DecoratedBox(decoration:BoxDecoration(gradient:LinearGradient(begin:Alignment.center,end:Alignment.bottomCenter,colors:[Colors.transparent,Colors.black87]))),Positioned(top:9,left:8,child:Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:4),decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(10)),child:const Text('● CANLI',style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900)))),Positioned(top:10,right:8,child:Text('◉ ${v['viewerCount']??0}',style:const TextStyle(color:Colors.white,fontSize:10))),Positioned(bottom:10,left:10,right:10,child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text((v['displayName']??v['username']??'Yayıncı').toString(),maxLines:1,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900)),Text((v['title']??'Canlı yayın').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white70,fontSize:11))]))])));},childCount:ds.length)));
    }),
  ];

''' +x[end:]
# Trend remains wired to real video documents and original detail/menus.
x=x.replace('    ..._canliSliverleri(trend:true),','')
start=x.index('          return SliverGrid(',x.index('  List<Widget> _trendSliverleri'));end=x.index('\n        },',start)
x=x[:start]+'''          return SliverList(delegate:SliverChildBuilderDelegate((c,i){final v=belgeler[i].data();final tur=(v['type']??'video').toString(),url=(v['mediaUrl']??v['videoUrl']??'').toString();return Container(margin:const EdgeInsets.symmetric(horizontal:10,vertical:7),decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(18),border:Border.all(color:const Color(0xFFE7E7ED))),child:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:belgeler[i].id))),onLongPress:()=>kendiPaylasimMenusu(context,belgeler[i].id,v),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[ClipRRect(borderRadius:const BorderRadius.vertical(top:Radius.circular(18)),child:SizedBox(height:200,width:double.infinity,child:MedyaOnizleme(tur:tur,url:url,thumbnailUrl:(v['thumbnailUrl']??'').toString(),yazi:(v['description']??'').toString(),arkaPlan:const Color(0xFF292348)))),Padding(padding:const EdgeInsets.all(12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text((v['description']??'').toString(),maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black,fontWeight:FontWeight.w800)),const SizedBox(height:6),Text('@${v['username']??'ngelx'}   ♡ ${v['likeCount']??0}   ◉ ${v['viewCount']??0}',style:const TextStyle(color:Colors.black54,fontSize:12))]))])));},childCount:belgeler.length));''' +x[end:]

x=x.replace('class _KesfetPageState extends State<KesfetPage> {',"class _KesfetPageState extends State<KesfetPage> {\n  String _groupCategory450='Tümü'; bool _newPeople450=false;")
x=x.replace('  List<Widget> _grupSliverleri()=>[',"  List<Widget> _grupSliverleri()=>[\n    SliverToBoxAdapter(child:SingleChildScrollView(scrollDirection:Axis.horizontal,padding:const EdgeInsets.fromLTRB(16,12,16,0),child:Row(children:['Tümü','Sohbet','Müzik','Spor','Teknoloji'].map((c)=>Padding(padding:const EdgeInsets.only(right:6),child:ChoiceChip(label:Text(c),selected:_groupCategory450==c,onSelected:(_)=>setState(()=>_groupCategory450=c)))).toList()))),")
x=x.replace("return d.data()['groupDeleted']!=true&&!ad.contains('oyun')&&!ad.contains('game');","return d.data()['groupDeleted']!=true&&!ad.contains('oyun')&&!ad.contains('game')&&(_groupCategory450=='Tümü'||(d.data()['groupCategory']??'Sohbet')==_groupCategory450);")
x=x.replace('  List<Widget> _kisiSliverleri()=>[',"  List<Widget> _kisiSliverleri()=>[\n    SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.fromLTRB(16,12,16,0),child:Row(children:[ChoiceChip(label:const Text('Önerilen'),selected:!_newPeople450,onSelected:(_)=>setState(()=>_newPeople450=false)),const SizedBox(width:8),ChoiceChip(label:const Text('Yeni katılanlar'),selected:_newPeople450,onSelected:(_)=>setState(()=>_newPeople450=true))]))),")
x=x.replace("if(kisiler.isEmpty)return SliverToBoxAdapter", "if(_newPeople450)kisiler.sort((a,b)=>((b.data()['createdAt'] as Timestamp?)?.millisecondsSinceEpoch??0).compareTo((a.data()['createdAt'] as Timestamp?)?.millisecondsSinceEpoch??0));\n        if(kisiler.isEmpty)return SliverToBoxAdapter")

s=s[:a]+x+s[b:];p.write_text(s)
# Shared host/viewer control panel preserves media, guests, PK and lifecycle callbacks.
p=Path('app/lib/live_broadcast_studio.dart');s=p.read_text();s=s.replace('    final c = onizleme;','    if(baglaniyor)return const ColoredBox(color:Color(0xFF151515),child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[CircularProgressIndicator(color:Colors.white),SizedBox(height:12),Text(\'Yayın hazırlanıyor…\',style:TextStyle(color:Colors.white))])));\n    final c = onizleme;',1)
start=s.index('  Widget _yorumGirisAlani()');end=s.index('  Future<void> _goruntuStudyoPaneli()',start);v=s[start:end]
v=v.replace('controller:yorum,enabled:etkin','style:const TextStyle(color:Colors.black87),controller:yorum,enabled:etkin').replace('hintText:hint,filled:true,fillColor:Colors.black54','hintText:hint,hintStyle:const TextStyle(color:Colors.black45),filled:true,fillColor:const Color(0xFFF3F4F7),border:OutlineInputBorder(borderSide:BorderSide.none,borderRadius:BorderRadius.circular(24))').replace('Icon(Icons.send_rounded)','Icon(Icons.send_rounded,color:Color(0xFF00BFCB))')
s=s[:start]+v+s[end:]
start=s.index('              Row(children: [\n                Expanded(child:_yorumGirisAlani()),',s.index('  Widget build(BuildContext context)',s.index('class CanliYayinPage')))
end=s.index('\n            ]),\n          )),',start)
s=s[:start]+'''              Container(padding:const EdgeInsets.fromLTRB(12,12,12,8),decoration:const BoxDecoration(color:Colors.white,borderRadius:BorderRadius.vertical(top:Radius.circular(26))),child:Theme(data:ThemeData.light().copyWith(colorScheme:ColorScheme.fromSeed(seedColor:mor)),child:Column(mainAxisSize:MainAxisSize.min,children:[
                Ngelx448GuestControls(liveId:widget.belgeId,ownerUid:widget.ownerId,host:widget.yayinSahibi),\n                _yorumGirisAlani(),
                const SizedBox(height:10),
                if(widget.yayinSahibi)Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                  _control450(mikrofonAcik?Icons.mic:Icons.mic_off,'Mikrofon',_yayinMikrofonunuDegistir),
                  _control450(kameraAcik?Icons.videocam:Icons.videocam_off,'Kamera',_yayinKamerasiniAcKapat),
                  Column(children:[NgelXCanliPkButonu(liveId:widget.belgeId,ownerUid:widget.ownerId),const Text('PK',style:TextStyle(color:Colors.black,fontSize:11))]),
                  _control450(Icons.tune,'Efektler',_goruntuStudyoPaneli),
                  _control450(Icons.share,'Paylaş',_paylas),
                ])else Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                  _control450(Icons.favorite,'Beğen',kalpIsleniyor?null:_kalpDegistir),
                  _control450(Icons.card_giftcard,'Hediye',hediyeGonderiliyor?null:_hediyePaneli),
                  _control450(Icons.share,'Paylaş',_paylas),
                ]),
                if(widget.yayinSahibi)Padding(padding:const EdgeInsets.only(top:10),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[IconButton(tooltip:'Kamerayı çevir',onPressed:kameraAcik&&!kameraDegisiyor?_yayinKamerasiniCevir:null,icon:const Icon(Icons.cameraswitch,color:mor)),FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFFF1744),foregroundColor:Colors.white),onPressed:()async{if(await _geri()&&mounted)Navigator.pop(context);},icon:const Icon(Icons.stop_circle_outlined),label:const Text('Yayını bitir'))])),
              ]))),''' +s[end:]
pos=s.index('  @override\n  Widget build(BuildContext context)',s.index('class CanliYayinPage'))
s=s[:pos]+'''  Widget _control450(IconData icon,String label,VoidCallback? action)=>Expanded(child:Column(mainAxisSize:MainAxisSize.min,children:[IconButton.filledTonal(style:IconButton.styleFrom(backgroundColor:const Color(0xFFE7F7F9),foregroundColor:const Color(0xFF008FA2)),onPressed:action,icon:Icon(icon)),Text(label,style:const TextStyle(color:Colors.black,fontSize:10,fontWeight:FontWeight.w800))]));

''' +s[pos:]
# Compact neutral comments; badges remain to distinguish moderators/host.
s=s.replace("color:yayinci?const Color(0xCCB00020):const Color(0x665D5FEF)","color:const Color(0xAA222222)").replace("color:hostMesaji?const Color(0xCCB00020):const Color(0x77000000)","color:const Color(0x99222222)")
s=s.replace('              Ngelx448GuestControls(liveId:widget.belgeId,ownerUid:widget.ownerId,host:widget.yayinSahibi),\n','',1)
p.write_text(s)
p=Path('app/lib/build448_live_guests.dart');g=p.read_text().replace("'Yayına katılma isteği'","'Konuk ol'");p.write_text(g)
p=Path('firestore.rules');r=p.read_text();fragment=Path('tools/community450.rules.fragment').read_text();pos=r.index('    match /');r=r[:pos]+fragment+'\n'+r[pos:];p.write_text(r)
print('Build450 approved discovery, shared live panel, community module and rules applied')
