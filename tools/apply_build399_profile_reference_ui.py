#!/usr/bin/env python3
from pathlib import Path
p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")
ps=src.index("class _ProfilPageState extends State<ProfilPage>")
pe=src.index("\nclass _ProfilEtkilesimRozeti",ps)
prof=src[ps:pe]

old=r'''                  Row(
                    children: [
                      const Spacer(),
                      IconButton(tooltip:t('profilePreview'),onPressed:aktifKullanici==null?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:aktifKullanici!.uid,ziyaretciOnizleme:true))),icon:const Icon(Icons.visibility_outlined,color:Colors.black,size:27)),
                      IconButton(onPressed:aktifKullanici==null?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>ProfilAramaPage(uid:aktifKullanici!.uid))),icon:const Icon(Icons.search_rounded,color:Colors.black,size:28)),
                      StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:aktifKullanici!.uid).limit(100).snapshots(),builder:(_,s){final sayi=(s.data?.docs??[]).where((d)=>d.data()['read']!=true&&ngelxAktiviteBildirimiGosterilir(d.data())).length;return IconButton(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),icon:sayi==0?const Icon(Icons.notifications_none_rounded,color:Colors.black,size:28):Badge(label:Text(sayi>99?'99+':'$sayi'),child:const Icon(Icons.notifications_none_rounded,color:Colors.black,size:28)));}),
                      Tooltip(
                        message:'NgelX Premium',
                        child:InkWell(
                          onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXPremiumPage())),
                          borderRadius:BorderRadius.circular(13),
                          child:Container(
                            width:38,height:38,
                            margin:const EdgeInsets.symmetric(horizontal:2),
                            decoration:BoxDecoration(
                              gradient:const LinearGradient(colors:[Color(0xFF1768E8),Color(0xFF7844F3)]),
                              borderRadius:BorderRadius.circular(13),
                            ),
                            child:const Icon(Icons.workspace_premium_rounded,color:Colors.white,size:22),
                          ),
                        ),
                      ),
                      IconButton(tooltip:t('settingsTitle'),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page())),icon:const Icon(Icons.settings_outlined,color:Colors.black,size:28)),
                    ],
                  ),
                  const SizedBox(height: 18),
                  SizedBox(
                    width:132,height:132,
                    child:Stack(
                      alignment:Alignment.center,
                      children:[
                        GestureDetector(behavior:HitTestBehavior.opaque,onTap:hikayeyiAc,onLongPress:fotografYukle,child:NgelXHikayeliAvatar(uid:aktifKullanici?.uid??'',fotoUrl:fotoUrl,kullanici:kullanici,radius:59,etkin:false,hikayeYoksaTikla:fotografYukle,uzunBas:fotografYukle)),
                        if(fotoYukleniyor)
                          const CircularProgressIndicator(color:Colors.white),
                        Positioned(
                          right:0,bottom:0,
                          child:GestureDetector(
                            onTap:fotografYukle,
                            child:Container(
                              padding:const EdgeInsets.all(9),
                              decoration:const BoxDecoration(color:Colors.white,shape:BoxShape.circle,boxShadow:[BoxShadow(color:Colors.black26,blurRadius:10)]),
                              child:const Icon(Icons.photo_camera_rounded,color:Colors.black,size:20),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),'''
new=r'''                  SizedBox(
                    height:265,
                    child:Stack(clipBehavior:Clip.none,children:[
                      Positioned(left:-18,right:-18,top:-12,height:190,child:ClipRRect(
                        borderRadius:const BorderRadius.vertical(bottom:Radius.circular(28)),
                        child:kapakUrl.isEmpty
                          ?Container(decoration:const BoxDecoration(gradient:LinearGradient(colors:[Color(0xFFE6EDFF),Color(0xFFF0E3FF)])),child:const Center(child:Icon(Icons.landscape_outlined,color:Color(0xFF9589C8),size:56)))
                          :Image(image:NgelXAgImageProvider(kapakUrl),fit:BoxFit.cover,alignment:Alignment(0,kapakY)),
                      )),
                      Positioned(left:0,right:0,top:2,child:Row(mainAxisAlignment:MainAxisAlignment.end,children:[
                        _profilKapakIkon(Icons.search_rounded,()=>aktifKullanici==null?null:Navigator.push(context,MaterialPageRoute(builder:(_)=>ProfilAramaPage(uid:aktifKullanici!.uid)))),
                        _profilKapakIkon(Icons.more_horiz_rounded,()=>_profilDahaFazlaAc()),
                        _profilKapakIkon(Icons.notifications_none_rounded,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()))),
                        _profilKapakIkon(Icons.settings_outlined,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page()))),
                      ])),
                      Positioned(right:0,top:125,child:FilledButton.icon(
                        style:FilledButton.styleFrom(backgroundColor:Colors.black.withValues(alpha:.66),foregroundColor:Colors.white,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14))),
                        onPressed:kapakYukleniyor?null:kapakFotografiDuzenle,
                        icon:kapakYukleniyor?const SizedBox(width:16,height:16,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.photo_camera_rounded,size:18),
                        label:const Text('Kapak Fotoğrafını\nDeğiştir',style:TextStyle(fontSize:11,fontWeight:FontWeight.w800)),
                      )),
                      Positioned(left:4,top:126,child:SizedBox(
                        width:132,height:132,
                        child:Stack(alignment:Alignment.center,children:[
                          Container(padding:const EdgeInsets.all(4),decoration:const BoxDecoration(color:Colors.white,shape:BoxShape.circle),child:GestureDetector(behavior:HitTestBehavior.opaque,onTap:hikayeyiAc,onLongPress:fotografYukle,child:NgelXHikayeliAvatar(uid:aktifKullanici?.uid??'',fotoUrl:fotoUrl,kullanici:kullanici,radius:59,etkin:false,hikayeYoksaTikla:fotografYukle,uzunBas:fotografYukle))),
                          if(fotoYukleniyor)const CircularProgressIndicator(color:Colors.white),
                          Positioned(right:0,bottom:0,child:GestureDetector(onTap:fotografYukle,child:Container(padding:const EdgeInsets.all(9),decoration:const BoxDecoration(color:Colors.white,shape:BoxShape.circle,boxShadow:[BoxShadow(color:Colors.black26,blurRadius:10)]),child:const Icon(Icons.photo_camera_rounded,color:Colors.black,size:20)))),
                        ]),
                      )),
                    ]),
                  ),
                  const SizedBox(height: 4),'''
if old not in prof: raise SystemExit("profile top anchor missing")
prof=prof.replace(old,new,1)

# No free blue verified tick in this layout.
prof=prof.replace("                      if(dogrulanmis)...[","                      if(false)...[",1)

# Stats get a unified rounded card.
oldstats="""                           return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                             _beyazIstatistik('$canliTakip',t('following'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'following',baslik:'Takip')))),
                             _beyazIstatistik('$canliTakipci',t('followers'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'followers',baslik:'Takipçiler')))),
                             _beyazIstatistik('$etkilesim',t('interaction'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>EtkilesimOzetiPage(uid:aktifKullanici!.uid)))),
                             _beyazIstatistik('$canliArkadas',t('friends'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage()))),
                           ]);"""
newstats="""                           return Container(
                             width:double.infinity,
                             padding:const EdgeInsets.symmetric(vertical:8),
                             decoration:BoxDecoration(color:const Color(0xFFF8F8FD),borderRadius:BorderRadius.circular(21)),
                             child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                               Expanded(child:_beyazIstatistik('$canliTakip',t('following'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'following',baslik:'Takip'))))),
                               Expanded(child:_beyazIstatistik('$canliTakipci',t('followers'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'followers',baslik:'Takipçiler'))))),
                               Expanded(child:_beyazIstatistik('$etkilesim',t('interaction'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>EtkilesimOzetiPage(uid:aktifKullanici!.uid)))),
                               Expanded(child:_beyazIstatistik('$canliArkadas',t('friends'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())))),
                             ]),
                           );"""
if oldstats in prof: prof=prof.replace(oldstats,newstats,1)

# Edit button becomes the locked purple-blue gradient.
oldedit="""                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[SizedBox(width:235,height:50,child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1F2F6),foregroundColor:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:duzenle,icon:const Icon(Icons.edit_outlined),label:Text(aktifKullanici?.isAnonymous==true?t('createAccountShort'):t('editProfile'),style:const TextStyle(fontWeight:FontWeight.w800)))),const SizedBox(width:10),SizedBox(width:52,height:50,child:FilledButton(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1ECFF),foregroundColor:Colors.black,padding:EdgeInsets.zero,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),child:const Icon(Icons.person_add_alt_1)))])"""
newedit="""                  Row(children:[
                    Expanded(child:Container(
                      decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFFA23BFF),Color(0xFF2860FF)]),borderRadius:BorderRadius.circular(18)),
                      child:FilledButton.icon(
                        style:FilledButton.styleFrom(backgroundColor:Colors.transparent,shadowColor:Colors.transparent,foregroundColor:Colors.white,minimumSize:const Size.fromHeight(54),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18))),
                        onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:duzenle,
                        icon:const Icon(Icons.edit_rounded,color:Colors.white),
                        label:Text(aktifKullanici?.isAnonymous==true?t('createAccountShort'):t('editProfile'),style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:16)),
                      ),
                    )),
                    const SizedBox(width:10),
                    SizedBox(width:122,height:54,child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF6F1FF),foregroundColor:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18))),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),icon:const Icon(Icons.person_add_alt_1),label:const Text('Arkadaş Ekle',style:TextStyle(fontSize:11,fontWeight:FontWeight.w800)))),
                  ])"""
if oldedit not in prof: raise SystemExit("profile edit anchor missing")
prof=prof.replace(oldedit,newedit,1)

# Tabs follow locked reference order (stories replaces liked).
prof=prof.replace("_ProfilSekme(t('liked'),profilSekme==3,()=>setState(()=>profilSekme=3))","_ProfilSekme('Hikayeler',profilSekme==3,()=>setState(()=>profilSekme=3))",1)
prof=prof.replace("    if(profilSekme==3)return _begenilenGrid();","    if(profilSekme==3)return _profilHikayeGridFinal();",1)

# Add helpers before _profilGrid.
anchor="  Widget _profilGrid(){"
helpers=r'''  Widget _profilKapakIkon(IconData ikon,VoidCallback? tikla)=>Padding(
    padding:const EdgeInsets.only(left:7),
    child:InkWell(onTap:tikla,borderRadius:BorderRadius.circular(24),child:Container(width:44,height:44,decoration:BoxDecoration(color:Colors.white.withValues(alpha:.92),shape:BoxShape.circle),child:Icon(ikon,color:Colors.black,size:24))),
  );

  Future<void> _profilDahaFazlaAc()async{
    await showModalBottomSheet<void>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(leading:const Icon(Icons.visibility_outlined),title:Text(t('profilePreview')),onTap:(){Navigator.pop(c);final u=aktifKullanici;if(u!=null)Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:u.uid,ziyaretciOnizleme:true)));}),
        ListTile(leading:const Icon(Icons.history_rounded),title:Text(t('archive')),onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXArsivMerkeziPage()));}),
        ListTile(leading:const Icon(Icons.settings_outlined),title:Text(t('settingsTitle')),onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page()));}),
      ])),
    );
  }

  Widget _profilHikayeGridFinal()=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
    stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:aktifKullanici!.uid).where('type',isEqualTo:'story').limit(100).snapshots(),
    builder:(_,s){
      final docs=s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[];
      if(docs.isEmpty)return _profilBosDurum(Icons.auto_stories_outlined,'Henüz hikâye yok.');
      return GridView.builder(
        shrinkWrap:true,physics:const NeverScrollableScrollPhysics(),padding:const EdgeInsets.all(6),itemCount:docs.length,
        gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:3,crossAxisSpacing:6,mainAxisSpacing:6,childAspectRatio:.76),
        itemBuilder:(_,i){
          final d=docs[i],v=d.data(),url=(v['mediaUrl']??'').toString(),video=(v['storyMediaType']??'photo').toString()=='video';
          return GestureDetector(
            onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(url:url,mediaType:(v['storyMediaType']??'photo').toString(),kullanici:kullanici,fotoUrl:fotoUrl,ownerUid:aktifKullanici?.uid??'',storyId:d.id,createdAt:v['createdAt'],expiresAt:v['expiresAt']))),
            child:ClipRRect(borderRadius:BorderRadius.circular(12),child:video?NgelXVideoKapakOnizleme(url:url):NgelXAgResmi(url:url,fit:BoxFit.cover)),
          );
        },
      );
    },
  );

'''
if anchor not in prof: raise SystemExit("profile helper anchor missing")
prof=prof.replace(anchor,helpers+anchor,1)

src=src[:ps]+prof+src[pe:]
p.write_text(src,encoding="utf-8")
print("Build 399 Profile reference UI applied.")
