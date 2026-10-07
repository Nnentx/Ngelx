#!/usr/bin/env python3
from pathlib import Path

path = Path("app/lib/main.dart")
src = path.read_text(encoding="utf-8")

src = src.replace("defaultValue: '395'", "defaultValue: '396'", 1)
src = src.replace("defaultValue: '1.0.171'", "defaultValue: '1.0.172'", 1)

anchor = "  Future<void> sohbetiAc(String chatId,Widget sayfa) async {"
if anchor not in src:
    raise SystemExit("MesajPage action anchor not found")

menu_method = r'''  Future<void> _yeniOlusturMenusu() async {
    final ben=uid;
    if(!mounted)return;
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:SafeArea(
          child:Padding(
            padding:const EdgeInsets.fromLTRB(14,4,14,18),
            child:Column(mainAxisSize:MainAxisSize.min,children:[
              Align(
                alignment:Alignment.centerLeft,
                child:Padding(
                  padding:const EdgeInsets.fromLTRB(10,2,10,8),
                  child:Text(lt('Yeni oluştur','Create new'),style:const TextStyle(color:Color(0xFF07142E),fontSize:20,fontWeight:FontWeight.w900)),
                ),
              ),
              ListTile(
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
                leading:const CircleAvatar(backgroundColor:Color(0xFFEAF4FF),child:Icon(Icons.chat_bubble_rounded,color:Color(0xFF1678F4))),
                title:Text(t('newChat'),style:const TextStyle(fontWeight:FontWeight.w900)),
                subtitle:Text(lt('Yeni bir özel sohbet başlat','Start a private chat')),
                onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const YeniSohbetPage()));},
              ),
              const SizedBox(height:4),
              ListTile(
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
                leading:const CircleAvatar(backgroundColor:Color(0xFFEDE8FF),child:Icon(Icons.group_add_rounded,color:mor)),
                title:Text(t('createGroup'),style:const TextStyle(fontWeight:FontWeight.w900)),
                subtitle:Text(lt('Yeni grup oluştur','Create a new group')),
                onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const GrupOlusturPage()));},
              ),
              const SizedBox(height:4),
              ListTile(
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
                leading:const CircleAvatar(backgroundColor:Color(0xFFE9FFF4),child:Icon(Icons.link_rounded,color:Color(0xFF16A36A))),
                title:Text(t('joinGroup'),style:const TextStyle(fontWeight:FontWeight.w900)),
                subtitle:Text(lt('Davet veya bağlantı ile gruba katıl','Join with an invite or link')),
                onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const GrubaKatilPage()));},
              ),
              if(ben!=null)...[
                const SizedBox(height:4),
                ListTile(
                  shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
                  leading:const CircleAvatar(backgroundColor:Color(0xFFF2F3F6),child:Icon(Icons.archive_outlined,color:Color(0xFF667085))),
                  title:Text(t('archivedChats'),style:const TextStyle(fontWeight:FontWeight.w900)),
                  subtitle:Text(lt('Arşivlediğin sohbet ve gruplar','Archived chats and groups')),
                  onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>ArsivSohbetlerPage(uid:ben)));},
                ),
              ],
            ]),
          ),
        ),
      ),
    );
  }

'''
src = src.replace(anchor, menu_method + anchor, 1)

old_group_leave = "      if(grup)ListTile(leading:const Icon(Icons.exit_to_app_rounded,color:Color(0xFFE23D4F)),title:Text(t('leaveGroup'),style:const TextStyle(color:Color(0xFFE23D4F),fontWeight:FontWeight.w700)),onTap:(){Navigator.pop(c);gelenKutusundanGruptanAyril(context,id);}),"
new_group_leave = """      if(grup)ListTile(leading:const Icon(Icons.info_outline_rounded,color:ngelxGroupGreen),title:Text(lt('Grup bilgisi','Group info'),style:const TextStyle(fontWeight:FontWeight.w700)),onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupUyeleriPage(chatId:id)));}),
      if(grup)ListTile(leading:const Icon(Icons.exit_to_app_rounded,color:Color(0xFFE23D4F)),title:Text(t('leaveGroup'),style:const TextStyle(color:Color(0xFFE23D4F),fontWeight:FontWeight.w700)),onTap:(){Navigator.pop(c);gelenKutusundanGruptanAyril(context,id);}),"""
if old_group_leave not in src:
    raise SystemExit("Group menu anchor not found")
src = src.replace(old_group_leave, new_group_leave, 1)

src = src.replace(
    "final ad=(v['groupName']??t('groupChat')).toString(),foto=(v['groupPhotoUrl']??'').toString();",
    "final hamAd=(v['groupName']??v['name']??v['title']??'').toString().trim(),ad=hamAd.isEmpty?t('groupChat'):hamAd,foto=(v['groupPhotoUrl']??'').toString();",
    1,
)
src = src.replace(
    "final v=satir.d.data(),chatId=(v['chatId']??satir.d.id).toString(),ad=(v['groupName']??t('groupChat')).toString(),foto=(v['groupPhotoUrl']??'').toString();",
    "final v=satir.d.data(),chatId=(v['chatId']??satir.d.id).toString(),hamAd=(v['groupName']??v['name']??v['title']??'').toString().trim(),ad=hamAd.isEmpty?t('groupChat'):hamAd,foto=(v['groupPhotoUrl']??'').toString();",
    1,
)
src = src.replace(
    "final grupArama='\${v['groupName']??''} \${v['lastMessage']??''}'.toLowerCase();",
    "final grupArama='\${v['groupName']??''} \${v['name']??''} \${v['title']??''} \${v['lastMessage']??''}'.toLowerCase();",
    1,
)

old_eski = """              final eski=filtre=='Mesajlar'
                ?<QueryDocumentSnapshot<Map<String,dynamic>>>[]
                :(eskiSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d){
                    final v=d.data(),ad=(v['groupName']??t('groupChat')).toString().toLowerCase();
                    return (filtre=='Tümü'||filtre=='Gruplar')&&(sohbetSorgu.isEmpty||ad.contains(sohbetSorgu));
                  }).toList();"""
new_eski = """              // Build 396: archived groups stay in the dedicated Archive screen.
              final eski=<QueryDocumentSnapshot<Map<String,dynamic>>>[];"""
if old_eski not in src:
    raise SystemExit("Archive merge anchor not found")
src = src.replace(old_eski, new_eski, 1)

old_tabs = """            Padding(
              padding:const EdgeInsets.fromLTRB(16,0,0,10),
              child:SizedBox(
                height:42,
                child:ListView(
                  scrollDirection:Axis.horizontal,
                  children:[sekme('Tümü'),sekme('Mesajlar'),sekme('Gruplar'),sekme('Bildirimler'),sekme('İstekler')],
                ),
              ),
            ),"""
new_tabs = """            Padding(
              padding:const EdgeInsets.fromLTRB(12,0,12,10),
              child:Row(children:[
                Expanded(child:sekme('Tümü')),
                Expanded(child:sekme('Mesajlar')),
                Expanded(child:sekme('Gruplar')),
                Expanded(child:sekme('Bildirimler')),
                Expanded(child:sekme('İstekler')),
              ]),
            ),"""
if old_tabs not in src:
    raise SystemExit("Tab row anchor not found")
src = src.replace(old_tabs, new_tabs, 1)

sekme_start = src.index("    Widget sekme(String ad){")
sekme_end = src.index("\n    Widget bildirimlerIcerigi()", sekme_start)
sekme_block = src[sekme_start:sekme_end]
sekme_block = sekme_block.replace("padding:const EdgeInsets.only(right:7),","padding:const EdgeInsets.symmetric(horizontal:2),",1)
sekme_block = sekme_block.replace("padding:const EdgeInsets.symmetric(horizontal:15,vertical:9),","padding:const EdgeInsets.symmetric(horizontal:4,vertical:9),",1)
sekme_block = sekme_block.replace(
    "child:Text(ad,style:TextStyle(color:secili?Colors.white:const Color(0xFF6F7891),fontSize:12.5,fontWeight:secili?FontWeight.w900:FontWeight.w700)),",
    "child:FittedBox(fit:BoxFit.scaleDown,child:Text(ad,maxLines:1,style:TextStyle(color:secili?Colors.white:const Color(0xFF6F7891),fontSize:11.5,fontWeight:secili?FontWeight.w900:FontWeight.w700))),",
    1,
)
src = src[:sekme_start] + sekme_block + src[sekme_end:]

src = src.replace(
    "onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const YeniSohbetPage())),\n                  icon:const Icon(Icons.add_rounded,color:Color(0xFF07142E),size:32),",
    "onPressed:_yeniOlusturMenusu,\n                  icon:const Icon(Icons.add_rounded,color:Color(0xFF07142E),size:32),",
    1,
)

search_block = """            AnimatedSwitcher(
              duration:const Duration(milliseconds:160),"""
insert_group_cta = """            if(filtre=='Gruplar')
              Padding(
                padding:const EdgeInsets.fromLTRB(16,0,16,9),
                child:Row(children:[
                  Expanded(child:Text(lt('Grupların','Your groups'),style:const TextStyle(color:Color(0xFF667085),fontSize:12.5,fontWeight:FontWeight.w700))),
                  FilledButton.icon(
                    style:FilledButton.styleFrom(
                      backgroundColor:const Color(0xFF1678F4),
                      foregroundColor:Colors.white,
                      padding:const EdgeInsets.symmetric(horizontal:14,vertical:10),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
                    ),
                    onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GrupOlusturPage())),
                    icon:const Icon(Icons.group_add_rounded,size:18),
                    label:Text(lt('Grup Kur +','Create Group +'),style:const TextStyle(fontWeight:FontWeight.w900)),
                  ),
                ]),
              ),
            AnimatedSwitcher(
              duration:const Duration(milliseconds:160),"""
if search_block not in src:
    raise SystemExit("Search block anchor not found")
src = src.replace(search_block, insert_group_cta, 1)

old_empty = """              if(satirlar.isEmpty)return ListView(
                physics:const AlwaysScrollableScrollPhysics(),
                padding:EdgeInsets.only(bottom:altBosluk),
                children:[SizedBox(height:220,child:Center(child:Text(t('noChats'),textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54))))],
              );"""
new_empty = """              if(satirlar.isEmpty)return ListView(
                physics:const AlwaysScrollableScrollPhysics(),
                padding:EdgeInsets.only(bottom:altBosluk),
                children:[SizedBox(
                  height:260,
                  child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                    CircleAvatar(
                      radius:34,
                      backgroundColor:const Color(0xFFF1F5FB),
                      child:Icon(filtre=='Gruplar'?Icons.groups_outlined:Icons.chat_bubble_outline_rounded,color:const Color(0xFF7C86A0),size:34),
                    ),
                    const SizedBox(height:12),
                    Text(
                      filtre=='Gruplar'?lt('Henüz grubun yok','No groups yet'):lt('Henüz mesaj yok','No messages yet'),
                      style:const TextStyle(color:Color(0xFF111827),fontSize:16,fontWeight:FontWeight.w900),
                    ),
                    const SizedBox(height:5),
                    Text(
                      filtre=='Gruplar'?lt('Yeni bir grup kurabilir veya bir gruba katılabilirsin.','Create a group or join one.'):t('noChats'),
                      textAlign:TextAlign.center,
                      style:const TextStyle(color:Color(0xFF8A93A8),fontSize:12.5),
                    ),
                  ])),
                )],
              );"""
if old_empty not in src:
    raise SystemExit("Empty-state anchor not found")
src = src.replace(old_empty, new_empty, 1)

govde_anchor = "            Expanded(child:RefreshIndicator(color:mor,onRefresh:_gelenKutusunuYenile,child:govde)),"
govde_new = r'''            if(filtre=='Tümü'&&ben!=null)
              Padding(
                padding:const EdgeInsets.fromLTRB(12,0,12,8),
                child:Row(children:[
                  Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(200).snapshots(),
                    builder:(_,s){
                      final n=ngelxOkunmamisAktiviteSayisi(s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]);
                      return InkWell(
                        borderRadius:BorderRadius.circular(18),
                        onTap:()=>setState(()=>filtre='Bildirimler'),
                        child:Container(
                          padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
                          decoration:BoxDecoration(color:const Color(0xFFF7F3FF),borderRadius:BorderRadius.circular(18)),
                          child:Row(children:[
                            const CircleAvatar(radius:17,backgroundColor:Color(0xFFE9DEFF),child:Icon(Icons.notifications_rounded,color:mor,size:18)),
                            const SizedBox(width:8),
                            Expanded(child:Text(lt('Bildirimler','Notifications'),style:const TextStyle(fontWeight:FontWeight.w900,fontSize:12))),
                            if(n>0)Badge(label:Text(_sayacEtiketi(n))),
                          ]),
                        ),
                      );
                    },
                  )),
                  const SizedBox(width:8),
                  Expanded(child:InkWell(
                    borderRadius:BorderRadius.circular(18),
                    onTap:()=>setState(()=>filtre='İstekler'),
                    child:Container(
                      padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
                      decoration:BoxDecoration(color:const Color(0xFFF2F8FF),borderRadius:BorderRadius.circular(18)),
                      child:Row(children:[
                        const CircleAvatar(radius:17,backgroundColor:Color(0xFFDCEEFF),child:Icon(Icons.person_add_alt_1_rounded,color:Color(0xFF1678F4),size:18)),
                        const SizedBox(width:8),
                        Expanded(child:Text(lt('İstekler','Requests'),style:const TextStyle(fontWeight:FontWeight.w900,fontSize:12))),
                        const Icon(Icons.chevron_right_rounded,color:Color(0xFF8A93A8),size:18),
                      ]),
                    ),
                  )),
                ]),
              ),
            Expanded(child:RefreshIndicator(color:mor,onRefresh:_gelenKutusunuYenile,child:govde)),'''
if govde_anchor not in src:
    raise SystemExit("Inbox body anchor not found")
src = src.replace(govde_anchor, govde_new, 1)

path.write_text(src, encoding="utf-8")
print("Build 396 inbox final polish patch applied.")
