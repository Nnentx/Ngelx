#!/usr/bin/env python3
from pathlib import Path

path = Path("app/lib/main.dart")
src = path.read_text(encoding="utf-8")

src = src.replace("defaultValue: '394'", "defaultValue: '395'", 1)
src = src.replace("defaultValue: '1.0.170'", "defaultValue: '1.0.171'", 1)

# Final login screen: visual-only replacement. Existing auth, reset, remember-me
# and account creation methods remain untouched.
login_class = src.index("class _GirisPageState extends State<GirisPage>")
login_build_start = src.index("  @override\n  Widget build(BuildContext context) {", login_class)
login_build_end = src.index("\n}\n\nclass _NgelXRenkliBaslik", login_build_start)

login_build = r'''  @override
  Widget build(BuildContext context) {
    Widget ozellik(IconData ikon,String yazi,Color renk)=>Expanded(
      child:Container(
        height:54,
        decoration:BoxDecoration(
          color:Colors.white.withValues(alpha:.82),
          borderRadius:BorderRadius.circular(22),
          border:Border.all(color:renk.withValues(alpha:.12)),
          boxShadow:[BoxShadow(color:renk.withValues(alpha:.08),blurRadius:18,offset:const Offset(0,7))],
        ),
        child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
          Icon(ikon,color:renk,size:24),
          const SizedBox(width:8),
          Flexible(child:Text(yazi,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:renk,fontSize:14,fontWeight:FontWeight.w800))),
        ]),
      ),
    );

    Widget sosyal({required Widget ikon,required VoidCallback onTap})=>Expanded(
      child:OutlinedButton(
        style:OutlinedButton.styleFrom(
          minimumSize:const Size.fromHeight(56),
          backgroundColor:Colors.white.withValues(alpha:.9),
          side:const BorderSide(color:Color(0x1107142E)),
          shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(24)),
        ),
        onPressed:onTap,
        child:ikon,
      ),
    );

    InputDecoration alanDekorasyon({required IconData ikon,required String ipucu,Widget? son})=>InputDecoration(
      prefixIcon:Icon(ikon,color:const Color(0xFF33436B)),
      hintText:ipucu,
      hintStyle:const TextStyle(color:Color(0xFF75809D),fontSize:15),
      suffixIcon:son,
      filled:true,
      fillColor:Colors.white.withValues(alpha:.92),
      contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:19),
      border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none),
      enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:const BorderSide(color:Color(0x100B1E4D))),
      focusedBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:const BorderSide(color:Color(0x553B82F6),width:1.3)),
    );

    return Theme(
      data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,colorScheme:ColorScheme.fromSeed(seedColor:mor)),
      child:Scaffold(
        backgroundColor:Colors.white,
        body:Stack(children:[
          const Positioned(left:-95,top:-110,child:_NgelXSoftBlob(size:300,colors:[Color(0x5533C6FF),Color(0x337B61FF)])),
          const Positioned(right:-135,top:250,child:_NgelXSoftBlob(size:300,colors:[Color(0x2228D7FF),Color(0x335F6BFF)])),
          const Positioned(left:-150,bottom:-150,child:_NgelXSoftBlob(size:330,colors:[Color(0x337B61FF),Color(0x224DD8FF)])),
          const Positioned(right:-130,bottom:-120,child:_NgelXSoftBlob(size:300,colors:[Color(0x4434D6FF),Color(0x227C58FF)])),
          SafeArea(
            child:LayoutBuilder(builder:(context,kisit)=>SingleChildScrollView(
              padding:const EdgeInsets.fromLTRB(24,14,24,28),
              child:ConstrainedBox(
                constraints:BoxConstraints(minHeight:(kisit.maxHeight-42).clamp(0,double.infinity)),
                child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                  Align(
                    alignment:Alignment.centerRight,
                    child:PopupMenuButton<String>(
                      initialValue:uygulamaDili.value,
                      onSelected:diliDegistir,
                      itemBuilder:(_)=>dilAdlari.entries.map((e)=>PopupMenuItem(value:e.key,child:Text(e.value))).toList(),
                      child:Container(
                        padding:const EdgeInsets.symmetric(horizontal:15,vertical:9),
                        decoration:BoxDecoration(
                          color:Colors.white.withValues(alpha:.88),
                          borderRadius:BorderRadius.circular(24),
                          border:Border.all(color:const Color(0x1107142E)),
                          boxShadow:const [BoxShadow(color:Color(0x0D07142E),blurRadius:18,offset:Offset(0,7))],
                        ),
                        child:Row(mainAxisSize:MainAxisSize.min,children:[
                          const Icon(Icons.language_rounded,size:21,color:Color(0xFF15254C)),
                          const SizedBox(width:8),
                          Text(uygulamaDili.value.toUpperCase(),style:const TextStyle(color:Color(0xFF15254C),fontWeight:FontWeight.w800)),
                          const SizedBox(width:4),
                          const Icon(Icons.keyboard_arrow_down_rounded,color:Color(0xFF15254C)),
                        ]),
                      ),
                    ),
                  ),
                  const SizedBox(height:36),
                  Center(child:Image.asset('assets/ngelx_logo.png',width:104,height:104,fit:BoxFit.contain)),
                  const SizedBox(height:2),
                  const Center(child:Text('ngelxsocial.com',style:TextStyle(color:Color(0xFF7682A2),fontSize:13.5,fontWeight:FontWeight.w600,letterSpacing:.1))),
                  const SizedBox(height:24),
                  const _NgelXRenkliBaslik(),
                  const SizedBox(height:7),
                  Center(child:Text(t('tagline'),textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFF68738F),fontSize:15.5,fontWeight:FontWeight.w500))),
                  const SizedBox(height:24),
                  Row(children:[
                    ozellik(Icons.explore_rounded,lt('Keşfet','Discover'),const Color(0xFF0A8DF4)),
                    const SizedBox(width:9),
                    ozellik(Icons.send_rounded,lt('Paylaş','Share'),const Color(0xFF7C3AED)),
                    const SizedBox(width:9),
                    ozellik(Icons.groups_rounded,lt('Bağlan','Connect'),const Color(0xFF0BA7D9)),
                  ]),
                  const SizedBox(height:24),
                  TextField(
                    controller:email,
                    keyboardType:TextInputType.emailAddress,
                    textInputAction:TextInputAction.next,
                    autofillHints:const [AutofillHints.email,AutofillHints.username],
                    autocorrect:false,
                    enableSuggestions:false,
                    decoration:alanDekorasyon(ikon:Icons.alternate_email_rounded,ipucu:t('email')),
                  ),
                  if(epostaOnerileri.isNotEmpty)Container(
                    margin:const EdgeInsets.only(top:6),
                    decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(18),border:Border.all(color:Colors.black12),boxShadow:const [BoxShadow(color:Colors.black12,blurRadius:12)]),
                    child:Column(mainAxisSize:MainAxisSize.min,children:epostaOnerileri.map((adres)=>ListTile(dense:true,leading:const Icon(Icons.account_circle_outlined),title:Text(adres),onTap:()=>oneriyiSec(adres))).toList()),
                  ),
                  const SizedBox(height:13),
                  TextField(
                    controller:sifre,
                    obscureText:gizli,
                    textInputAction:TextInputAction.done,
                    autofillHints:const [AutofillHints.password],
                    onSubmitted:yukleniyor?null:(_)=>girisYap(),
                    onChanged:(_){if(girisHatasi!=null)setState(()=>girisHatasi=null);},
                    decoration:alanDekorasyon(
                      ikon:Icons.lock_rounded,
                      ipucu:t('password'),
                      son:IconButton(onPressed:()=>setState(()=>gizli=!gizli),icon:Icon(gizli?Icons.visibility_off_rounded:Icons.visibility_rounded,color:const Color(0xFF33436B))),
                    ),
                  ),
                  if(girisHatasi!=null)Container(
                    margin:const EdgeInsets.only(top:9),
                    padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
                    decoration:BoxDecoration(color:const Color(0xFFFFF1F1),borderRadius:BorderRadius.circular(14),border:Border.all(color:const Color(0xFFFFC7C7))),
                    child:Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
                      const Icon(Icons.error_outline_rounded,color:Color(0xFFD93025),size:19),
                      const SizedBox(width:8),
                      Expanded(child:Text(girisHatasi!,style:const TextStyle(color:Color(0xFF9D201A),fontSize:13,fontWeight:FontWeight.w700))),
                    ]),
                  ),
                  const SizedBox(height:7),
                  Row(children:[
                    Checkbox(value:beniHatirla,onChanged:(v)=>hatirlamayiDegistir(v??false),activeColor:const Color(0xFF6547F5),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(5))),
                    Expanded(child:Text(t('remember'),style:const TextStyle(color:Color(0xFF111827),fontWeight:FontWeight.w700))),
                    TextButton(
                      onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SifreYenilePage(baslangicEposta:email.text.trim()))),
                      child:Text(t('forgot'),style:const TextStyle(color:Color(0xFF7C2EF2),fontWeight:FontWeight.w800)),
                    ),
                  ]),
                  const SizedBox(height:4),
                  InkWell(
                    borderRadius:BorderRadius.circular(24),
                    onTap:yukleniyor?null:girisYap,
                    child:Ink(
                      height:58,
                      decoration:BoxDecoration(
                        borderRadius:BorderRadius.circular(24),
                        gradient:const LinearGradient(colors:[Color(0xFF13D5EA),Color(0xFF1678F4),Color(0xFF9128F5)]),
                        boxShadow:const [BoxShadow(color:Color(0x332C74FF),blurRadius:20,offset:Offset(0,8))],
                      ),
                      child:Row(children:[
                        const SizedBox(width:48),
                        Expanded(child:Center(child:yukleniyor
                          ?const SizedBox(width:22,height:22,child:CircularProgressIndicator(strokeWidth:2.5,color:Colors.white))
                          :Text(t('login'),style:const TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900)))),
                        const Icon(Icons.arrow_forward_rounded,color:Colors.white,size:29),
                        const SizedBox(width:20),
                      ]),
                    ),
                  ),
                  const SizedBox(height:20),
                  Row(children:[
                    const Expanded(child:Divider(color:Color(0xFFD8DEEB))),
                    Padding(padding:const EdgeInsets.symmetric(horizontal:14),child:Text(lt('veya','or'),style:const TextStyle(color:Color(0xFF7C86A0),fontWeight:FontWeight.w700))),
                    const Expanded(child:Divider(color:Color(0xFFD8DEEB))),
                  ]),
                  const SizedBox(height:14),
                  Row(children:[
                    sosyal(
                      ikon:const Text('G',style:TextStyle(color:Color(0xFF4285F4),fontSize:24,fontWeight:FontWeight.w900)),
                      onTap:()=>ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Google ile giriş bağlantısı hazırlanıyor.','Google sign-in is being prepared.')))),
                    ),
                    const SizedBox(width:12),
                    sosyal(
                      ikon:const Icon(Icons.apple_rounded,color:Colors.black,size:31),
                      onTap:()=>ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('Apple ile giriş bağlantısı hazırlanıyor.','Apple sign-in is being prepared.')))),
                    ),
                  ]),
                  const SizedBox(height:17),
                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                    Flexible(child:Text(t('noAccount'),style:const TextStyle(color:Color(0xFF6F7994),fontWeight:FontWeight.w600))),
                    const SizedBox(width:5),
                    const Text('|',style:TextStyle(color:Color(0xFF9AA3B7))),
                    const SizedBox(width:5),
                    TextButton(
                      onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const KayitPage())),
                      child:Text(t('createAccount'),style:const TextStyle(color:Color(0xFF7028E9),fontWeight:FontWeight.w900)),
                    ),
                  ]),
                ]),
              ),
            )),
          ),
        ]),
      ),
    );
  }
'''

src = src[:login_build_start] + login_build + src[login_build_end:]

title_start = src.index("class _NgelXRenkliBaslik extends StatelessWidget")
title_end = src.index("\nclass SifreYenilePage", title_start)
title_block = src[title_start:title_end].replace(
    "alignment: rtl ? Alignment.centerRight : Alignment.centerLeft,",
    "alignment: Alignment.center,",
)
src = src[:title_start] + title_block + src[title_end:]

blob_marker = "\nclass SifreYenilePage extends StatefulWidget"
if "class _NgelXSoftBlob extends StatelessWidget" not in src:
    blob = r'''
class _NgelXSoftBlob extends StatelessWidget{
  final double size;
  final List<Color> colors;
  const _NgelXSoftBlob({required this.size,required this.colors});
  @override Widget build(BuildContext context)=>IgnorePointer(
    child:Container(
      width:size,height:size,
      decoration:BoxDecoration(
        shape:BoxShape.circle,
        gradient:LinearGradient(colors:colors,begin:Alignment.topLeft,end:Alignment.bottomRight),
      ),
    ),
  );
}
'''
    src = src.replace(blob_marker, "\n"+blob+blob_marker, 1)

# Final inbox shell. Existing chat documents, notification collections, request
# handling and message pages are reused; only the presentation layer is replaced.
src = src.replace(
    "  bool _gelenKutusuYenileniyor=false;",
    "  bool _gelenKutusuYenileniyor=false;\n  bool _aramaAcik=false;",
    1,
)

msg_class = src.index("class _MesajPageState extends State<MesajPage>")
msg_build_start = src.index("  @override Widget build(BuildContext context){", msg_class)
msg_build_end = src.index("\n}\n\nclass ArsivSohbetlerPage", msg_build_start)

msg_build = r'''  @override Widget build(BuildContext context){
    final ben=uid;

    String saatEtiketi(dynamic ham){
      if(ham is! Timestamp)return '';
      final d=ham.toDate(),n=DateTime.now();
      if(d.year==n.year&&d.month==n.month&&d.day==n.day){
        final h=d.hour.toString().padLeft(2,'0'),m=d.minute.toString().padLeft(2,'0');
        return '$h:$m';
      }
      final dun=DateTime(n.year,n.month,n.day).subtract(const Duration(days:1));
      if(d.year==dun.year&&d.month==dun.month&&d.day==dun.day)return lt('Dün','Yesterday');
      return '${d.day.toString().padLeft(2,'0')}.${d.month.toString().padLeft(2,'0')}';
    }

    Widget sekme(String ad){
      final secili=filtre==ad;
      return Padding(
        padding:const EdgeInsets.only(right:7),
        child:InkWell(
          borderRadius:BorderRadius.circular(20),
          onTap:()=>setState(()=>filtre=ad),
          child:AnimatedContainer(
            duration:const Duration(milliseconds:180),
            padding:const EdgeInsets.symmetric(horizontal:15,vertical:9),
            decoration:BoxDecoration(
              gradient:secili?const LinearGradient(colors:[Color(0xFF13C8EE),Color(0xFF176EF4),Color(0xFF6E45F5)]):null,
              color:secili?null:const Color(0xFFF5F7FB),
              borderRadius:BorderRadius.circular(20),
              boxShadow:secili?const [BoxShadow(color:Color(0x263B82F6),blurRadius:14,offset:Offset(0,5))]:null,
            ),
            child:Text(ad,style:TextStyle(color:secili?Colors.white:const Color(0xFF6F7891),fontSize:12.5,fontWeight:secili?FontWeight.w900:FontWeight.w700)),
          ),
        ),
      );
    }

    Widget bildirimlerIcerigi(){
      if(ben==null)return const SizedBox.shrink();
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(100).snapshots(),
        builder:(_,snap){
          final docs=(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d)=>ngelxAktiviteBildirimiGosterilir(d.data())).toList()
            ..sort((a,b){
              final at=a.data()['createdAt'],bt=b.data()['createdAt'];
              final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
              return bm.compareTo(am);
            });
          if(snap.connectionState==ConnectionState.waiting&&docs.isEmpty)return const Center(child:CircularProgressIndicator(color:mor));
          if(docs.isEmpty)return Center(child:Text(t('noActivity'),style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)));
          return ListView.separated(
            physics:const AlwaysScrollableScrollPhysics(),
            padding:EdgeInsets.fromLTRB(12,8,12,ngelxAltGuvenliBosluk(context,extra:72)),
            itemCount:docs.length,
            separatorBuilder:(_,__)=>const Divider(height:1,indent:72,color:Color(0xFFEDF0F5)),
            itemBuilder:(_,i){
              final d=docs[i],v=d.data(),okundu=v['read']==true;
              final tur=(v['type']??'').toString();
              final metin=(v['text']??v['message']??v['content']??lt('Yeni bildirim','New notification')).toString();
              final foto=(v['photoUrl']??v['senderPhotoUrl']??'').toString();
              IconData ikon=Icons.notifications_rounded;
              Color renk=const Color(0xFF7C3AED);
              if(tur=='like'||tur=='interaction'){ikon=Icons.favorite_rounded;renk=const Color(0xFFFF3B73);}
              else if(tur=='comment'){ikon=Icons.mode_comment_rounded;renk=const Color(0xFF2088F5);}
              else if(tur=='follow_request'||tur=='friend_request'||tur=='friend_accepted'){ikon=Icons.person_add_alt_1_rounded;renk=const Color(0xFF2F80ED);}
              else if(tur=='security'){ikon=Icons.shield_rounded;renk=Colors.orange;}
              return ListTile(
                contentPadding:const EdgeInsets.symmetric(horizontal:8,vertical:5),
                leading:Stack(clipBehavior:Clip.none,children:[
                  CircleAvatar(radius:25,backgroundColor:renk.withValues(alpha:.12),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?Icon(ikon,color:renk):null),
                  if(!okundu)const Positioned(right:-1,top:-1,child:CircleAvatar(radius:5,backgroundColor:Color(0xFFFF3B73))),
                ]),
                title:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF111827),fontSize:13.5,fontWeight:okundu?FontWeight.w600:FontWeight.w900)),
                subtitle:Text(zamanKisa(v['createdAt']),style:const TextStyle(color:Color(0xFF8A93A8),fontSize:11.5)),
                onTap:()async{
                  try{await d.reference.set({'read':true},SetOptions(merge:true));}catch(_){}
                  if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));
                },
              );
            },
          );
        },
      );
    }

    Widget isteklerIcerigi(){
      if(ben==null)return const SizedBox.shrink();
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(120).snapshots(),
        builder:(_,snap){
          final sosyal=(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d){
            final v=d.data(),tur=(v['type']??'').toString();
            return (tur=='follow_request'||tur=='friend_request')&&v['status']=='pending';
          }).toList();
          return ListView(
            physics:const AlwaysScrollableScrollPhysics(),
            padding:EdgeInsets.fromLTRB(14,10,14,ngelxAltGuvenliBosluk(context,extra:72)),
            children:[
              Container(
                decoration:BoxDecoration(color:const Color(0xFFF7F9FC),borderRadius:BorderRadius.circular(20)),
                child:ListTile(
                  leading:const CircleAvatar(backgroundColor:Color(0xFFE9E3FF),child:Icon(Icons.person_add_alt_1_rounded,color:mor)),
                  title:Text(lt('Takip ve arkadaşlık istekleri','Follow & friend requests'),style:const TextStyle(fontWeight:FontWeight.w900)),
                  subtitle:Text(sosyal.isEmpty?lt('Bekleyen istek yok','No pending requests'):lt('${sosyal.length} bekleyen istek','${sosyal.length} pending requests')),
                  trailing:sosyal.isEmpty?const Icon(Icons.chevron_right_rounded):Badge(label:Text(_sayacEtiketi(sosyal.length)),child:const Icon(Icons.chevron_right_rounded)),
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),
                ),
              ),
              const SizedBox(height:10),
              Container(
                decoration:BoxDecoration(color:const Color(0xFFF4F9FF),borderRadius:BorderRadius.circular(20)),
                child:ListTile(
                  leading:const CircleAvatar(backgroundColor:Color(0xFFDDEEFF),child:Icon(Icons.chat_bubble_outline_rounded,color:Color(0xFF1784E8))),
                  title:Text(t('messageRequests'),style:const TextStyle(fontWeight:FontWeight.w900)),
                  subtitle:Text(t('messageRequestsSub')),
                  trailing:const Icon(Icons.chevron_right_rounded),
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>MesajIstekleriPage(uid:ben))),
                ),
              ),
              if(sosyal.isNotEmpty)...[
                const SizedBox(height:14),
                ...sosyal.take(12).map((d){
                  final v=d.data(),foto=(v['photoUrl']??'').toString(),metin=(v['text']??v['message']??'Yeni istek').toString();
                  return Container(
                    margin:const EdgeInsets.only(bottom:7),
                    decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(18),border:Border.all(color:const Color(0xFFEEF0F5))),
                    child:ListTile(
                      leading:CircleAvatar(backgroundColor:const Color(0xFFEDE7FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,color:mor):null),
                      title:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w800)),
                      subtitle:Text(zamanKisa(v['createdAt']),style:const TextStyle(color:Colors.black45)),
                      trailing:FilledButton(
                        style:FilledButton.styleFrom(backgroundColor:const Color(0xFF1678F4),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14))),
                        onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),
                        child:Text(lt('Aç','Open')),
                      ),
                    ),
                  );
                }),
              ],
            ],
          );
        },
      );
    }

    Widget sohbetlerIcerigi(){
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:ben==null?null:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(100).snapshots(),
        builder:(_,s){
          final docs=(s.data?.docs??[]).where((d){
            final v=d.data();
            if(List<String>.from(v['hiddenFor']??const[]).contains(ben)||arsivSohbetler.contains(d.id))return false;
            final members=List<String>.from(v['members']??const[]);
            final grup=v['isGroup']==true||members.length>2;
            if(filtre=='Mesajlar'&&grup)return false;
            if(filtre=='Gruplar'&&!grup)return false;
            if(!grup){
              final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');
              final gelenIstek=(v['requestRecipientUid']??'').toString()==ben&&v['requestAccepted_$ben']!=true&&v['requestRejected_$ben']!=true&&!arkadaslar.contains(other);
              if(gelenIstek)return false;
              return true;
            }
            final grupArama='${v['groupName']??''} ${v['lastMessage']??''}'.toLowerCase();
            return sohbetSorgu.isEmpty||grupArama.contains(sohbetSorgu);
          }).toList()..sort((a,b){
            final ap=sabitSohbetler.contains(a.id),bp=sabitSohbetler.contains(b.id);
            if(ap!=bp)return ap?-1:1;
            final at=a.data()['updatedAt']??a.data()['lastMessageClientAt'],bt=b.data()['updatedAt']??b.data()['lastMessageClientAt'];
            final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
            return bm.compareTo(am);
          });

          final altBosluk=ngelxAltGuvenliBosluk(context,extra:72);
          return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:ben==null?null:FirebaseFirestore.instance.collection('group_archives').doc(ben).collection('items').limit(30).snapshots(),
            builder:(_,eskiSnap){
              final eski=filtre=='Mesajlar'
                ?<QueryDocumentSnapshot<Map<String,dynamic>>>[]
                :(eskiSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d){
                    final v=d.data(),ad=(v['groupName']??t('groupChat')).toString().toLowerCase();
                    return (filtre=='Tümü'||filtre=='Gruplar')&&(sohbetSorgu.isEmpty||ad.contains(sohbetSorgu));
                  }).toList();
              int zaman(dynamic ham)=>ham is Timestamp?ham.millisecondsSinceEpoch:0;
              final satirlar=<({bool eski,QueryDocumentSnapshot<Map<String,dynamic>> d,bool sabit,int zaman})>[
                ...docs.map((d)=>(eski:false,d:d,sabit:sabitSohbetler.contains(d.id),zaman:zaman(d.data()['updatedAt']??d.data()['lastMessageClientAt']))),
                ...eski.map((d)=>(eski:true,d:d,sabit:false,zaman:zaman(d.data()['updatedAt']??d.data()['archivedAt']))),
              ]..sort((a,b){
                if(a.sabit!=b.sabit)return a.sabit?-1:1;
                return b.zaman.compareTo(a.zaman);
              });

              if(satirlar.isEmpty)return ListView(
                physics:const AlwaysScrollableScrollPhysics(),
                padding:EdgeInsets.only(bottom:altBosluk),
                children:[SizedBox(height:220,child:Center(child:Text(t('noChats'),textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54))))],
              );

              return ListView.builder(
                key:PageStorageKey<String>('inbox_merged_'+filtre),
                physics:const AlwaysScrollableScrollPhysics(),
                padding:EdgeInsets.fromLTRB(12,4,12,altBosluk),
                itemCount:satirlar.length,
                itemBuilder:(_,i){
                  final satir=satirlar[i];
                  if(satir.eski){
                    final v=satir.d.data(),chatId=(v['chatId']??satir.d.id).toString(),ad=(v['groupName']??t('groupChat')).toString(),foto=(v['groupPhotoUrl']??'').toString();
                    return ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                      onTap:chatId.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:chatId,ad:ad,foto:foto))),
                      leading:CircleAvatar(radius:27,backgroundColor:ngelxGroupGreenSoft,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups_rounded,color:ngelxGroupGreen):null),
                      title:Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF101827),fontWeight:FontWeight.w900)),
                      subtitle:Text(lt('Arşivlenmiş grup','Archived group'),style:const TextStyle(color:Color(0xFF8B93A6))),
                      trailing:const Icon(Icons.lock_outline_rounded,color:Color(0xFF9B949E),size:19),
                    );
                  }

                  final d=satir.d,v=d.data(),members=List<String>.from(v['members']??[]);
                  final grup=v['isGroup']==true||members.length>2;
                  final unread=(v['unread_$ben'] as num?)?.toInt()??0;
                  final zamanYazi=saatEtiketi(v['updatedAt']??v['lastMessageClientAt']);

                  if(grup){
                    final ad=(v['groupName']??t('groupChat')).toString(),foto=(v['groupPhotoUrl']??'').toString();
                    return ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                      onTap:()=>sohbetiAc(d.id,GrupSohbetPage(chatId:d.id,ad:ad,foto:foto)),
                      onLongPress:()=>sohbetMenusu(context,d.id,grup:true),
                      leading:CircleAvatar(radius:27,backgroundColor:const Color(0xFFE9F7FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups_rounded,color:Color(0xFF237BEF),size:28):null),
                      title:Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),
                      subtitle:Text((v['lastMessage']??t('groupCreated')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),
                      trailing:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.end,children:[
                        if(zamanYazi.isNotEmpty)Text(zamanYazi,style:const TextStyle(color:Color(0xFF8A93A8),fontSize:11.5)),
                        if(unread>0)...[
                          const SizedBox(height:5),
                          Container(
                            constraints:const BoxConstraints(minWidth:24,minHeight:24),
                            padding:const EdgeInsets.symmetric(horizontal:7),
                            alignment:Alignment.center,
                            decoration:const BoxDecoration(color:Color(0xFF1678F4),shape:BoxShape.circle),
                            child:Text(_sayacEtiketi(unread),style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w900)),
                          ),
                        ]else if(sessizSohbetler.contains(d.id))const Padding(padding:EdgeInsets.only(top:5),child:Icon(Icons.notifications_off_outlined,color:Color(0xFF9AA2B4),size:18)),
                      ]),
                    );
                  }

                  final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');
                  return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                    stream:FirebaseFirestore.instance.collection('users').doc(other).snapshots(),
                    builder:(_,u){
                      final p=u.data?.data()??{};
                      if(p['deactivated']==true)return const SizedBox.shrink();
                      final hamTakmalar=v['nicknames'],takmalar=hamTakmalar is Map?Map<String,dynamic>.from(hamTakmalar):<String,dynamic>{};
                      final takma=(ben==null?'':(takmalar[ben]??'').toString()).trim(),profilAdi=(p['displayName']??p['username']??'NgelX').toString(),gorunenAd=takma.isNotEmpty?takma:profilAdi;
                      final aranan='$gorunenAd ${p['displayName']??''} ${p['username']??''} ${v['lastMessage']??''}'.toLowerCase();
                      if(sohbetSorgu.isNotEmpty&&!aranan.contains(sohbetSorgu))return const SizedBox.shrink();
                      final foto=(p['photoUrl']??'').toString();
                      final sessiz=sessizSohbetler.contains(d.id);
                      return ListTile(
                        contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                        onTap:()=>sohbetiAc(d.id,SohbetPage(chatId:d.id,digerUid:other,ad:gorunenAd,foto:foto)),
                        onLongPress:()=>sohbetMenusu(context,d.id),
                        leading:CircleAvatar(radius:27,backgroundColor:const Color(0xFFEFF3F8),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,color:Color(0xFF61708D)):null),
                        title:Text(gorunenAd,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),
                        subtitle:Text((v['lastMessage']??t('newChat')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),
                        trailing:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.end,children:[
                          if(zamanYazi.isNotEmpty)Text(zamanYazi,style:const TextStyle(color:Color(0xFF8A93A8),fontSize:11.5)),
                          if(unread>0)...[
                            const SizedBox(height:5),
                            Container(
                              constraints:const BoxConstraints(minWidth:24,minHeight:24),
                              padding:const EdgeInsets.symmetric(horizontal:7),
                              alignment:Alignment.center,
                              decoration:const BoxDecoration(color:Color(0xFF1678F4),shape:BoxShape.circle),
                              child:Text(_sayacEtiketi(unread),style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w900)),
                            ),
                          ]else if(sessiz)const Padding(padding:EdgeInsets.only(top:5),child:Icon(Icons.notifications_off_outlined,color:Color(0xFF9AA2B4),size:18)),
                        ]),
                      );
                    },
                  );
                },
              );
            },
          );
        },
      );
    }

    Widget govde=filtre=='Bildirimler'
      ?bildirimlerIcerigi()
      :filtre=='İstekler'
        ?isteklerIcerigi()
        :sohbetlerIcerigi();

    return Theme(
      data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,dividerColor:const Color(0xFFEDF0F5)),
      child:ColoredBox(
        color:Colors.white,
        child:SafeArea(
          child:Column(children:[
            Padding(
              padding:const EdgeInsets.fromLTRB(20,18,12,10),
              child:Row(children:[
                Expanded(child:Text(t('inbox'),style:const TextStyle(color:Color(0xFF07142E),fontSize:30,fontWeight:FontWeight.w900,letterSpacing:-.8))),
                IconButton(
                  tooltip:t('searchChats'),
                  onPressed:()=>setState(()=>_aramaAcik=!_aramaAcik),
                  icon:Icon(_aramaAcik?Icons.close_rounded:Icons.search_rounded,color:const Color(0xFF07142E),size:29),
                ),
                IconButton(
                  tooltip:t('newChat'),
                  onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const YeniSohbetPage())),
                  icon:const Icon(Icons.add_rounded,color:Color(0xFF07142E),size:32),
                ),
              ]),
            ),
            Padding(
              padding:const EdgeInsets.fromLTRB(16,0,0,10),
              child:SizedBox(
                height:42,
                child:ListView(
                  scrollDirection:Axis.horizontal,
                  children:[sekme('Tümü'),sekme('Mesajlar'),sekme('Gruplar'),sekme('Bildirimler'),sekme('İstekler')],
                ),
              ),
            ),
            AnimatedSwitcher(
              duration:const Duration(milliseconds:160),
              child:_aramaAcik
                ?Padding(
                    key:const ValueKey('search'),
                    padding:const EdgeInsets.fromLTRB(16,0,16,10),
                    child:TextField(
                      controller:sohbetAra,
                      autofocus:true,
                      onChanged:(v)=>setState(()=>sohbetSorgu=v.trim().toLowerCase()),
                      style:const TextStyle(color:Color(0xFF111827)),
                      decoration:InputDecoration(
                        hintText:t('searchChats'),
                        prefixIcon:const Icon(Icons.search_rounded,color:Color(0xFF7D879D)),
                        filled:true,
                        fillColor:const Color(0xFFF5F7FA),
                        border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none),
                      ),
                    ),
                  )
                :const SizedBox.shrink(key:ValueKey('nosearch')),
            ),
            Expanded(child:RefreshIndicator(color:mor,onRefresh:_gelenKutusunuYenile,child:govde)),
          ]),
        ),
      ),
    );
  }'''

src = src[:msg_build_start] + msg_build + src[msg_build_end:]

path.write_text(src, encoding="utf-8")
print("Build 395 final login + inbox UI patch applied.")
