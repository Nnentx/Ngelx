#!/usr/bin/env python3
from pathlib import Path

path = Path("app/lib/main.dart")
src = path.read_text(encoding="utf-8")

src = src.replace("defaultValue: '396'", "defaultValue: '397'", 1)
src = src.replace("defaultValue: '1.0.172'", "defaultValue: '1.0.173'", 1)

build_anchor = """  @override Widget build(BuildContext context){
    final ben=uid;
"""
if build_anchor not in src:
    raise SystemExit("MesajPage build anchor missing")

helpers = r'''  @override Widget build(BuildContext context){
    final ben=uid;

    Future<String> grupGorunenAdi(Map<String,dynamic> v,List<String> members) async {
      final ham=(v['groupName']??v['name']??v['title']??v['displayName']??'').toString().trim();
      if(ham.isNotEmpty)return ham;
      final diger=members.where((x)=>x.isNotEmpty&&x!=ben).take(3).toList();
      if(diger.isEmpty)return lt('Grup sohbeti','Group chat');
      final adlar=<String>[];
      for(final id in diger){
        try{
          final p=await FirebaseFirestore.instance.collection('users').doc(id).get().timeout(const Duration(seconds:4));
          final pv=p.data()??<String,dynamic>{};
          final ad=(pv['displayName']??pv['username']??'').toString().trim();
          if(ad.isNotEmpty)adlar.add(ad);
        }catch(_){}
      }
      if(adlar.isEmpty)return lt('Grup sohbeti','Group chat');
      return adlar.length==1
        ?lt('${adlar.first} ile grup','Group with ${adlar.first}')
        :adlar.take(2).join(', ');
    }

    Widget grupBasligi(Map<String,dynamic> v,List<String> members,TextStyle style){
      final ham=(v['groupName']??v['name']??v['title']??v['displayName']??'').toString().trim();
      if(ham.isNotEmpty)return Text(ham,maxLines:1,overflow:TextOverflow.ellipsis,style:style);
      return FutureBuilder<String>(
        future:grupGorunenAdi(v,members),
        builder:(_,s)=>Text(
          (s.data??lt('Grup sohbeti','Group chat')).trim().isEmpty?lt('Grup sohbeti','Group chat'):(s.data??lt('Grup sohbeti','Group chat')),
          maxLines:1,
          overflow:TextOverflow.ellipsis,
          style:style,
        ),
      );
    }

    Future<void> gelenKutusuIsteginiSonuclandir(QueryDocumentSnapshot<Map<String,dynamic>> belge,bool kabul) async {
      final benUid=FirebaseAuth.instance.currentUser?.uid;
      final veri=belge.data();
      final gonderen=(veri['fromUid']??'').toString();
      final hamTur=(veri['type']??'').toString();
      final eskiArkadaslik=belge.id.startsWith('friend_request_')||(veri['text']??'').toString().toLowerCase().contains('arkadaşlık');
      final arkadaslikIstegi=hamTur=='friend_request'||eskiArkadaslik;
      final istekTuru=arkadaslikIstegi?'friend_request':'follow_request';
      final takipIstegi=istekTuru=='follow_request';
      if(benUid==null||gonderen.isEmpty||veri['status']!='pending')return;

      final istekRef=sosyalIstekRef(gonderen,benUid,istekTuru);
      DocumentSnapshot<Map<String,dynamic>>? istekSnap;
      try{
        istekSnap=await istekRef.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:7));
        if(istekSnap.exists){
          final iv=istekSnap.data()??<String,dynamic>{};
          final aktifBildirimId=(iv['notificationId']??'').toString();
          final eskiVeyaSonuclanmis=iv['status']!='pending'||(aktifBildirimId.isNotEmpty&&aktifBildirimId!=belge.id);
          if(eskiVeyaSonuclanmis){
            await belge.reference.set({'status':'superseded','read':true,'supersededAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
            return;
          }
        }
      }catch(_){}

      final batch=FirebaseFirestore.instance.batch();
      batch.update(belge.reference,{
        'status':kabul?'accepted':'rejected',
        'read':true,
        'answeredAt':FieldValue.serverTimestamp(),
      });
      if(istekSnap?.exists==true){
        batch.update(istekRef,{
          'status':kabul?'accepted':'rejected',
          'answeredAt':FieldValue.serverTimestamp(),
          'updatedAt':FieldValue.serverTimestamp(),
        });
      }
      if(kabul&&takipIstegi){
        batch.set(FirebaseFirestore.instance.collection('users').doc(benUid),{'followers':FieldValue.arrayUnion([gonderen])},SetOptions(merge:true));
        batch.set(FirebaseFirestore.instance.collection('users').doc(gonderen),{'following':FieldValue.arrayUnion([benUid])},SetOptions(merge:true));
      }
      if(kabul&&arkadaslikIstegi){
        batch.set(FirebaseFirestore.instance.collection('users').doc(benUid),{'friends':FieldValue.arrayUnion([gonderen])},SetOptions(merge:true));
        batch.set(FirebaseFirestore.instance.collection('users').doc(gonderen),{'friends':FieldValue.arrayUnion([benUid])},SetOptions(merge:true));
        final ids=[benUid,gonderen]..sort();
        batch.set(FirebaseFirestore.instance.collection('friendships').doc(ids.join('_')),{
          'members':ids,'active':true,'since':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true));
      }

      try{
        await batch.commit().timeout(const Duration(seconds:12));
        if(kabul){
          unawaited(uygulamaBildirimiGonder(
            toUid:gonderen,
            fromUid:benUid,
            tur:takipIstegi?'follow_accepted':'friend_accepted',
            metin:takipIstegi?'takip isteğini kabul etti':'arkadaşlık isteğini kabul etti',
            olayTuru:takipIstegi?'follow_accepted':'friend_accepted',
            dedupeKey:'social_${takipIstegi?'follow':'friend'}_accepted_${gonderen}_${benUid}',
          ).catchError((_){ }));
        }
        if(mounted){
          final ad=takipIstegi?lt('Takip isteği','Follow request'):lt('Arkadaşlık isteği','Friend request');
          ngelxDurumMesaji(context,kabul?'$ad kabul edildi.':'$ad reddedildi.',tip:kabul?'basari':'uyari');
        }
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(lt('İstek işlenemedi. Tekrar dene.','Request could not be processed. Try again.'))));
      }
    }
'''
src = src.replace(build_anchor, helpers, 1)

old_social = """          final sosyal=(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d){
            final v=d.data(),tur=(v['type']??'').toString();
            return (tur=='follow_request'||tur=='friend_request')&&v['status']=='pending';
          }).toList();"""
new_social = """          final sosyal=(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d){
            final v=d.data(),tur=(v['type']??'').toString();
            if(!((tur=='follow_request'||tur=='friend_request')&&v['status']=='pending'))return false;
            if(sohbetSorgu.isEmpty)return true;
            final ara='${v['text']??''} ${v['message']??''} ${v['senderName']??''} ${v['fromName']??''}'.toLowerCase();
            return ara.contains(sohbetSorgu);
          }).toList();"""
if old_social not in src:
    raise SystemExit("request filter anchor missing")
src = src.replace(old_social,new_social,1)

old_request_map = r'''                ...sosyal.take(12).map((d){
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
                }),'''
new_request_map = r'''                ...sosyal.take(20).map((d){
                  final v=d.data(),from=(v['fromUid']??'').toString(),metin=(v['text']??v['message']??lt('Yeni istek','New request')).toString();
                  return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                    stream:from.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(from).snapshots(),
                    builder:(_,u){
                      final p=u.data?.data()??<String,dynamic>{};
                      final ad=(p['displayName']??p['username']??v['senderName']??v['fromName']??'NgelX').toString();
                      final kullanici=(p['username']??'').toString();
                      final ara='$ad $kullanici $metin'.toLowerCase();
                      if(sohbetSorgu.isNotEmpty&&!ara.contains(sohbetSorgu))return const SizedBox.shrink();
                      final foto=(p['photoUrl']??v['photoUrl']??'').toString();
                      return Container(
                        margin:const EdgeInsets.only(bottom:8),
                        decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(18),border:Border.all(color:const Color(0xFFEEF0F5))),
                        child:Padding(
                          padding:const EdgeInsets.fromLTRB(10,8,8,8),
                          child:Row(children:[
                            CircleAvatar(radius:24,backgroundColor:const Color(0xFFEDE7FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,color:mor):null),
                            const SizedBox(width:10),
                            Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                              Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w900,color:Color(0xFF111827))),
                              const SizedBox(height:2),
                              Text(metin,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:12.5)),
                              Text(zamanKisa(v['createdAt']),style:const TextStyle(color:Color(0xFFA0A7B8),fontSize:11)),
                            ])),
                            const SizedBox(width:6),
                            IconButton(
                              tooltip:lt('Reddet','Reject'),
                              style:IconButton.styleFrom(backgroundColor:const Color(0xFFFFEEEE)),
                              onPressed:()=>gelenKutusuIsteginiSonuclandir(d,false),
                              icon:const Icon(Icons.close_rounded,color:Color(0xFFE53935)),
                            ),
                            const SizedBox(width:4),
                            IconButton(
                              tooltip:lt('Kabul Et','Accept'),
                              style:IconButton.styleFrom(backgroundColor:const Color(0xFFE9F8F0)),
                              onPressed:()=>gelenKutusuIsteginiSonuclandir(d,true),
                              icon:const Icon(Icons.check_rounded,color:Color(0xFF20A866)),
                            ),
                          ]),
                        ),
                      );
                    },
                  );
                }),'''
if old_request_map not in src:
    raise SystemExit("request row anchor missing")
src = src.replace(old_request_map,new_request_map,1)

sohbet_anchor = "    Widget sohbetlerIcerigi(){"
if sohbet_anchor not in src:
    raise SystemExit("sohbetlerIcerigi anchor missing")

tum_widget = r'''    Widget tumIcerigi(){
      if(ben==null)return const SizedBox.shrink();
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(100).snapshots(),
        builder:(_,chatSnap)=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(120).snapshots(),
          builder:(_,notifSnap){
            if(chatSnap.connectionState==ConnectionState.waiting&&notifSnap.connectionState==ConnectionState.waiting){
              return const Center(child:CircularProgressIndicator(color:mor));
            }
            int zaman(dynamic ham)=>ham is Timestamp?ham.millisecondsSinceEpoch:0;
            final items=<Map<String,dynamic>>[];

            for(final d in chatSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]){
              final v=d.data();
              if(List<String>.from(v['hiddenFor']??const[]).contains(ben)||arsivSohbetler.contains(d.id))continue;
              final members=List<String>.from(v['members']??const[]);
              final grup=v['isGroup']==true||members.length>2;
              if(!grup){
                final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben);
                final gelenIstek=(v['requestRecipientUid']??'').toString()==ben&&v['requestAccepted_$ben']!=true&&v['requestRejected_$ben']!=true&&!arkadaslar.contains(other);
                if(gelenIstek)continue;
              }
              if(grup&&sohbetSorgu.isNotEmpty){
                final ara='${v['groupName']??''} ${v['name']??''} ${v['title']??''} ${v['lastMessage']??''}'.toLowerCase();
                if(!ara.contains(sohbetSorgu))continue;
              }
              items.add({'kind':'chat','doc':d,'time':zaman(v['updatedAt']??v['lastMessageClientAt'])});
            }

            for(final d in notifSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]){
              final v=d.data();
              if(!ngelxAktiviteBildirimiGosterilir(v))continue;
              final ara='${v['text']??''} ${v['message']??''} ${v['content']??''} ${v['senderName']??''} ${v['fromName']??''}'.toLowerCase();
              if(sohbetSorgu.isNotEmpty&&!ara.contains(sohbetSorgu))continue;
              items.add({'kind':'notification','doc':d,'time':zaman(v['createdAt']??v['clientCreatedAt'])});
            }

            items.sort((a,b)=>(b['time'] as int).compareTo(a['time'] as int));
            if(items.isEmpty)return ListView(
              physics:const AlwaysScrollableScrollPhysics(),
              padding:EdgeInsets.only(bottom:ngelxAltGuvenliBosluk(context,extra:72)),
              children:[SizedBox(height:260,child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const CircleAvatar(radius:34,backgroundColor:Color(0xFFF2F5FA),child:Icon(Icons.inbox_outlined,color:Color(0xFF7C86A0),size:34)),
                const SizedBox(height:12),
                Text(lt('Gelen kutun boş','Your inbox is empty'),style:const TextStyle(fontWeight:FontWeight.w900,fontSize:16)),
              ])))],
            );

            return ListView.separated(
              physics:const AlwaysScrollableScrollPhysics(),
              padding:EdgeInsets.fromLTRB(12,4,12,ngelxAltGuvenliBosluk(context,extra:72)),
              itemCount:items.length,
              separatorBuilder:(_,__)=>const Divider(height:1,indent:72,color:Color(0xFFF0F2F6)),
              itemBuilder:(_,i){
                final item=items[i],kind=item['kind'] as String;
                if(kind=='notification'){
                  final d=item['doc'] as QueryDocumentSnapshot<Map<String,dynamic>>,v=d.data();
                  final tur=(v['type']??'').toString(),pending=(tur=='follow_request'||tur=='friend_request')&&v['status']=='pending';
                  final metin=(v['text']??v['message']??v['content']??lt('Yeni bildirim','New notification')).toString();
                  final foto=(v['photoUrl']??v['senderPhotoUrl']??'').toString();
                  return ListTile(
                    contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                    leading:CircleAvatar(radius:27,backgroundColor:pending?const Color(0xFFEAF4FF):const Color(0xFFF2EDFF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?Icon(pending?Icons.person_add_alt_1_rounded:Icons.notifications_rounded,color:pending?const Color(0xFF1678F4):mor):null),
                    title:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF111827),fontWeight:v['read']==true?FontWeight.w600:FontWeight.w900)),
                    subtitle:Text(zamanKisa(v['createdAt']),style:const TextStyle(color:Color(0xFF8A93A8),fontSize:11.5)),
                    trailing:pending?Container(
                      padding:const EdgeInsets.symmetric(horizontal:9,vertical:6),
                      decoration:BoxDecoration(color:const Color(0xFFEAF4FF),borderRadius:BorderRadius.circular(12)),
                      child:Text(lt('İstek','Request'),style:const TextStyle(color:Color(0xFF1678F4),fontSize:11,fontWeight:FontWeight.w900)),
                    ):null,
                    onTap:()async{
                      try{await d.reference.set({'read':true},SetOptions(merge:true));}catch(_){}
                      if(!mounted)return;
                      if(pending)setState(()=>filtre='İstekler');
                      else Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));
                    },
                  );
                }

                final d=item['doc'] as QueryDocumentSnapshot<Map<String,dynamic>>,v=d.data(),members=List<String>.from(v['members']??const[]);
                final grup=v['isGroup']==true||members.length>2;
                final unread=(v['unread_$ben'] as num?)?.toInt()??0;
                final zamanYazi=saatEtiketi(v['updatedAt']??v['lastMessageClientAt']);
                final trailing=SizedBox(
                  width:64,
                  child:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.end,children:[
                    if(zamanYazi.isNotEmpty)Text(zamanYazi,textAlign:TextAlign.right,style:const TextStyle(color:Color(0xFF8A93A8),fontSize:11.5)),
                    if(unread>0)...[
                      const SizedBox(height:5),
                      Container(
                        constraints:const BoxConstraints(minWidth:24,minHeight:24),
                        padding:const EdgeInsets.symmetric(horizontal:7),
                        alignment:Alignment.center,
                        decoration:const BoxDecoration(color:Color(0xFF1678F4),shape:BoxShape.circle),
                        child:Text(_sayacEtiketi(unread),style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w900)),
                      ),
                    ],
                  ]),
                );

                if(grup){
                  final ham=(v['groupName']??v['name']??v['title']??v['displayName']??'').toString().trim(),foto=(v['groupPhotoUrl']??'').toString();
                  final acilisAdi=ham.isEmpty?lt('Grup sohbeti','Group chat'):ham;
                  return ListTile(
                    contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                    onTap:()=>sohbetiAc(d.id,GrupSohbetPage(chatId:d.id,ad:acilisAdi,foto:foto)),
                    onLongPress:()=>sohbetMenusu(context,d.id,grup:true),
                    leading:CircleAvatar(radius:27,backgroundColor:const Color(0xFFE9F7FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups_rounded,color:Color(0xFF237BEF),size:28):null),
                    title:grupBasligi(v,members,TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),
                    subtitle:Text((v['lastMessage']??t('groupCreated')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),
                    trailing:trailing,
                  );
                }

                final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben);
                return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('users').doc(other).snapshots(),
                  builder:(_,u){
                    final p=u.data?.data()??<String,dynamic>{};
                    if(p['deactivated']==true)return const SizedBox.shrink();
                    final ad=(p['displayName']??p['username']??'NgelX').toString(),kullanici=(p['username']??'').toString(),foto=(p['photoUrl']??'').toString();
                    final ara='$ad $kullanici ${v['lastMessage']??''}'.toLowerCase();
                    if(sohbetSorgu.isNotEmpty&&!ara.contains(sohbetSorgu))return const SizedBox.shrink();
                    return ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:5),
                      onTap:()=>sohbetiAc(d.id,SohbetPage(chatId:d.id,digerUid:other,ad:ad,foto:foto)),
                      onLongPress:()=>sohbetMenusu(context,d.id),
                      leading:CircleAvatar(radius:27,backgroundColor:const Color(0xFFEFF3F8),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,color:Color(0xFF61708D)):null),
                      title:Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),
                      subtitle:Text((v['lastMessage']??t('newChat')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),
                      trailing:trailing,
                    );
                  },
                );
              },
            );
          },
        ),
      );
    }

'''
src = src.replace(sohbet_anchor,tum_widget+sohbet_anchor,1)

old_govde = """    Widget govde=filtre=='Bildirimler'
      ?bildirimlerIcerigi()
      :filtre=='İstekler'
        ?isteklerIcerigi()
        :sohbetlerIcerigi();"""
new_govde = """    Widget govde=filtre=='Tümü'
      ?tumIcerigi()
      :filtre=='Bildirimler'
        ?bildirimlerIcerigi()
        :filtre=='İstekler'
          ?isteklerIcerigi()
          :sohbetlerIcerigi();"""
if old_govde not in src:
    raise SystemExit("govde selector missing")
src = src.replace(old_govde,new_govde,1)

quick_start = src.find("            if(filtre=='Tümü'&&ben!=null)")
if quick_start >= 0:
    quick_end = src.find("            Expanded(child:RefreshIndicator(color:mor,onRefresh:_gelenKutusunuYenile,child:govde)),",quick_start)
    if quick_end < 0:
        raise SystemExit("quick cards end missing")
    src = src[:quick_start] + src[quick_end:]

sohbet_start = src.index("    Widget sohbetlerIcerigi(){")
sohbet_end = src.index("\n    Widget govde=",sohbet_start)
block = src[sohbet_start:sohbet_end]

block = block.replace(
    "final hamAd=(v['groupName']??v['name']??v['title']??'').toString().trim(),ad=hamAd.isEmpty?t('groupChat'):hamAd,foto=(v['groupPhotoUrl']??'').toString();",
    "final hamAd=(v['groupName']??v['name']??v['title']??v['displayName']??'').toString().trim(),ad=hamAd.isEmpty?lt('Grup sohbeti','Group chat'):hamAd,foto=(v['groupPhotoUrl']??'').toString();",
)
block = block.replace(
    "title:Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),",
    "title:grupBasligi(v,members,TextStyle(color:const Color(0xFF101827),fontSize:15.5,fontWeight:unread>0?FontWeight.w900:FontWeight.w800)),",
    1,
)

needle = "trailing:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.end,children:["
for _ in range(2):
    pos=block.find(needle)
    if pos<0:
        break
    block=block[:pos] + "trailing:SizedBox(width:64,child:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.end,children:[" + block[pos+len(needle):]
    close=block.find("]),",pos+20)
    if close>0:
        block=block[:close+2] + ")," + block[close+3:]

src = src[:sohbet_start] + block + src[sohbet_end:]

src = src.replace(
    "hintText:t('searchChats'),",
    "hintText:filtre=='İstekler'?lt('İsteklerde ara','Search requests'):filtre=='Bildirimler'?lt('Bildirimlerde ara','Search notifications'):t('searchChats'),",
    1,
)

path.write_text(src,encoding="utf-8")
print("Build 397 inbox completion patch applied.")
