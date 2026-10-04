from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app/lib/main.dart"
STORY = ROOT / "app/lib/story_v66.dart"

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    return text.replace(old, new, 1)

def replace_exact_count(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{label}: expected exactly {expected} matches, found {count}")
    return text.replace(old, new)

main = MAIN.read_text(encoding="utf-8")

# 1) Private chat: shared background/theme for both participants.
old = "body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,tema){final veri=tema.data?.data()??<String,dynamic>{},ham=veri['theme_$uid'];final arkaPlan=ham is int?Color(ham):Colors.white,arkaPlanUrl=(veri['backgroundUrl_$uid']??'').toString(),hizliEmoji=(veri['quickEmoji_$uid']??'👍').toString(),arkaPlanOpaklik=(veri['backgroundOpacity_$uid'] is num?(veri['backgroundOpacity_$uid'] as num).toDouble():.30).clamp(.05,.85).toDouble(),mesajYaziBoyutu=(veri['messageFontSize_$uid'] is num?(veri['messageFontSize_$uid'] as num).toDouble():16.0).clamp(12.0,22.0).toDouble();return Container"
new = "body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,tema){final veri=tema.data?.data()??<String,dynamic>{},ham=veri['theme']??veri['theme_$uid'],arkaPlanHam=veri['backgroundOpacity']??veri['backgroundOpacity_$uid'];final arkaPlan=ham is int?Color(ham):Colors.white,arkaPlanUrl=(veri['backgroundUrl']??veri['backgroundUrl_$uid']??'').toString(),hizliEmoji=(veri['quickEmoji_$uid']??'👍').toString(),arkaPlanOpaklik=(arkaPlanHam is num?arkaPlanHam.toDouble():.30).clamp(.05,.85).toDouble(),mesajYaziBoyutu=(veri['messageFontSize_$uid'] is num?(veri['messageFontSize_$uid'] as num).toDouble():16.0).clamp(12.0,22.0).toDouble();return Container"
main = replace_once(main, old, new, "chat shared background read")

main = replace_once(
    main,
    "const ListTile(title:Text('Sohbeti özelleştir',style:TextStyle(fontWeight:FontWeight.w900)),subtitle:Text('Bu görünüm yalnızca sende görünür.')),",
    "const ListTile(title:Text('Sohbeti özelleştir',style:TextStyle(fontWeight:FontWeight.w900)),subtitle:Text('Arka plan değişiklikleri iki tarafta görünür. Yazı boyutu ve hızlı emoji sana özeldir.')),",
    "chat customization subtitle",
)
main = replace_once(main, "await ref.set({'backgroundOpacity_$me':oran},SetOptions(merge:true));", "await ref.set({'backgroundOpacity':oran,'backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));", "shared background opacity")
main = replace_exact_count(main, "final eskiArkaPlan=(onceki.data()?['backgroundUrl_$me']??'').toString();", "final eskiArkaPlan=(onceki.data()?['backgroundUrl']??onceki.data()?['backgroundUrl_$me']??'').toString();", 3, "shared background legacy fallback")
main = replace_once(
    main,
    """        'theme_$me':ngelxPrivateBlueCanvas.toARGB32(),
        'backgroundUrl_$me':'',
        'backgroundOpacity_$me':.30,
        'messageFontSize_$me':16.0,
        'quickEmoji_$me':'👍',""",
    """        'theme':ngelxPrivateBlueCanvas.toARGB32(),
        'backgroundUrl':'',
        'backgroundOpacity':.30,
        'backgroundUpdatedBy':me,
        'backgroundUpdatedAt':FieldValue.serverTimestamp(),
        'messageFontSize_$me':16.0,
        'quickEmoji_$me':'👍',""",
    "reset shared background",
)
main = replace_once(main, "await ref.set({'theme_$me':secim},SetOptions(merge:true));", "await ref.set({'theme':secim,'backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));", "shared background color")
main = replace_once(main, "await ref.set({'backgroundUrl_$me':''},SetOptions(merge:true));", "await ref.set({'backgroundUrl':'','backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));", "shared remove image")
main = replace_once(main, "await ref.set({'backgroundUrl_$me':url},SetOptions(merge:true));", "await ref.set({'backgroundUrl':url,'backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));", "shared upload image")
main = replace_once(main, "const SnackBar(content:Text('Özel sohbet arka planın kaydedildi.'))", "const SnackBar(content:Text('Sohbet arka planı iki taraf için güncellendi.'))", "shared background snackbar")

# 2) Message typing: keep keystroke hot path local and debounce mention lookup.
main = replace_once(
    main,
    "Timer? yaziyorZamanlayici,yaziyorBaslatZamanlayici,sureliMesajZamanlayici,sesKaydiZamanlayici;",
    "Timer? yaziyorZamanlayici,yaziyorBaslatZamanlayici,mentionZamanlayici,sureliMesajZamanlayici,sesKaydiZamanlayici;",
    "typing timer field",
)
main = replace_once(
    main,
    """    PrivateDraftStore.schedule(widget.chatId,deger);
    mentionAra(deger);
    final ben=uid;if(ben==null)return;""",
    """    PrivateDraftStore.schedule(widget.chatId,deger);
    mentionZamanlayici?.cancel();
    final sonParca=deger.split(RegExp(r'\\s+')).last;
    if(sonParca.startsWith('@')){
      mentionZamanlayici=Timer(const Duration(milliseconds:220),(){
        if(mounted)unawaited(mentionAra(mesaj.text));
      });
    }else if(mentionOnerileri.isNotEmpty&&mounted){
      setState(()=>mentionOnerileri.clear());
    }
    final ben=uid;if(ben==null)return;""",
    "debounce mention lookup",
)
main = replace_once(
    main,
    """    yaziyorZamanlayici?.cancel();
    yaziyorBaslatZamanlayici?.cancel();
    sureliMesajZamanlayici?.cancel();""",
    """    yaziyorZamanlayici?.cancel();
    yaziyorBaslatZamanlayici?.cancel();
    mentionZamanlayici?.cancel();
    sureliMesajZamanlayici?.cancel();""",
    "dispose mention timer",
)

# 3) Account add/switch bottom sheet: respect device safe area and keyboard.
main = replace_once(
    main,
    "context:context,isScrollControlled:true,backgroundColor:Colors.white,\n      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),\n      builder:(ctx)=>Theme(data:ThemeData.light(),child:StatefulBuilder(builder:(ctx,setP)=>Padding(\n        padding:EdgeInsets.fromLTRB(20,22,20,MediaQuery.of(ctx).viewInsets.bottom+24),\n        child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[\n          const Text('Hesap ekle'",
    "context:context,isScrollControlled:true,useSafeArea:true,backgroundColor:Colors.white,\n      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),\n      builder:(ctx)=>Theme(data:ThemeData.light(),child:StatefulBuilder(builder:(ctx,setP)=>Padding(\n        padding:EdgeInsets.fromLTRB(20,22,20,MediaQuery.of(ctx).viewInsets.bottom+MediaQuery.of(ctx).viewPadding.bottom+40),\n        child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[\n          const Text('Hesap ekle'",
    "account add safe area",
)

# 4) Follow/follower state: wait for Firestore pending writes so profile/list state stays consistent.
main = replace_once(
    main,
    """  await batch.commit();
  if(!takipte)await uygulamaBildirimiGonder(toUid:hedefUid,fromUid:ben,tur:'friend',metin:'Seni takip etmeye başladı');""",
    """  await batch.commit();
  await FirebaseFirestore.instance.waitForPendingWrites();
  if(!takipte)await uygulamaBildirimiGonder(toUid:hedefUid,fromUid:ben,tur:'friend',metin:'Seni takip etmeye başladı');""",
    "follow pending writes",
)
main = replace_once(
    main,
    """    await batch.commit();
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takipçi kaldırıldı.')));""",
    """    await batch.commit();
    await FirebaseFirestore.instance.waitForPendingWrites();
    try{
      await FirebaseFirestore.instance.collection('users').doc(benim).get(const GetOptions(source:Source.server));
    }catch(_){}
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takipçi kaldırıldı.')));""",
    "follower removal consistency",
)

# 5) Interaction cards: make all 4 actionable and open a useful detail list.
main = replace_once(
    main,
    "Row(children:[_kart(Icons.favorite_rounded,'Beğeni',begeni,Colors.red),_kart(Icons.comment_rounded,'Yorum',yorum,Colors.blue)]),",
    "Row(children:[_kart(context,Icons.favorite_rounded,'Beğeni',begeni,Colors.red,'likes'),_kart(context,Icons.comment_rounded,'Yorum',yorum,Colors.blue,'comments')]),",
    "interaction row 1",
)
main = replace_once(
    main,
    "Row(children:[_kart(Icons.send_rounded,'Paylaşım',paylasim,mor),_kart(Icons.grid_view_rounded,'Gönderi',d.length,Colors.orange)]),",
    "Row(children:[_kart(context,Icons.send_rounded,'Paylaşım',paylasim,mor,'shares'),_kart(context,Icons.grid_view_rounded,'Gönderi',d.length,Colors.orange,'posts')]),",
    "interaction row 2",
)
main = replace_once(
    main,
    "Widget _kart(IconData i,String t,int n,Color c)=>Expanded(child:Container(margin:const EdgeInsets.all(5),padding:const EdgeInsets.all(18),decoration:BoxDecoration(color:c.withValues(alpha:.10),borderRadius:BorderRadius.circular(20)),child:Column(children:[Icon(i,color:c),const SizedBox(height:8),Text(n.toString(),style:const TextStyle(fontSize:24,fontWeight:FontWeight.w900)),Text(t,style:const TextStyle(color:Colors.black54))])));",
    """Widget _kart(BuildContext context,IconData i,String t,int n,Color c,String metric)=>Expanded(child:Padding(
    padding:const EdgeInsets.all(5),
    child:Material(
      color:c.withValues(alpha:.10),
      borderRadius:BorderRadius.circular(20),
      clipBehavior:Clip.antiAlias,
      child:InkWell(
        onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>EtkilesimDetayPage(uid:uid,baslik:t,metric:metric,ikon:i,renk:c))),
        child:Padding(
          padding:const EdgeInsets.all(18),
          child:Column(children:[Icon(i,color:c),const SizedBox(height:8),Text(n.toString(),style:const TextStyle(fontSize:24,fontWeight:FontWeight.w900)),Text(t,style:const TextStyle(color:Colors.black54))]),
        ),
      ),
    ),
  ));""",
    "interaction card tappable",
)

detail_class = r'''
class EtkilesimDetayPage extends StatelessWidget{
  final String uid,baslik,metric;
  final IconData ikon;
  final Color renk;
  const EtkilesimDetayPage({super.key,required this.uid,required this.baslik,required this.metric,required this.ikon,required this.renk});

  int _deger(Map<String,dynamic> v){
    switch(metric){
      case 'likes': return (v['likeCount'] as num?)?.toInt()??0;
      case 'comments': return (v['commentCount'] as num?)?.toInt()??0;
      case 'shares': return (v['shareCount'] as num?)?.toInt()??0;
      default: return 1;
    }
  }

  int _zaman(Map<String,dynamic> v){
    final t=v['createdAt']??v['clientCreatedAt'];
    return t is Timestamp?t.millisecondsSinceEpoch:0;
  }

  @override
  Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:Text(baslik,style:const TextStyle(fontWeight:FontWeight.w900))),
      body:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).limit(100).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting&&!s.hasData)return const Center(child:CircularProgressIndicator(color:mor));
          if(s.hasError)return const Center(child:Text('İstatistik ayrıntıları yüklenemedi.',style:TextStyle(color:Colors.black54)));
          final docs=(s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[])
              .where((d)=>d.data()['type']!='story')
              .where((d)=>metric=='posts'||_deger(d.data())>0)
              .toList();
          if(metric=='posts'){
            docs.sort((a,b)=>_zaman(b.data()).compareTo(_zaman(a.data())));
          }else{
            docs.sort((a,b){
              final k=_deger(b.data()).compareTo(_deger(a.data()));
              return k!=0?k:_zaman(b.data()).compareTo(_zaman(a.data()));
            });
          }
          if(docs.isEmpty)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
            CircleAvatar(radius:34,backgroundColor:renk.withValues(alpha:.12),child:Icon(ikon,color:renk,size:32)),
            const SizedBox(height:12),
            Text(metric=='posts'?'Henüz gönderi yok.':'Bu istatistikte henüz içerik yok.',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)),
          ]));
          return ListView.separated(
            padding:const EdgeInsets.all(14),
            itemCount:docs.length,
            separatorBuilder:(_,__)=>const Divider(height:1),
            itemBuilder:(_,i){
              final d=docs[i],v=d.data(),aciklama=(v['description']??'').toString().trim(),zaman=zamanKisa(v['createdAt']??v['clientCreatedAt']);
              return ListTile(
                contentPadding:const EdgeInsets.symmetric(horizontal:6,vertical:6),
                leading:CircleAvatar(backgroundColor:renk.withValues(alpha:.12),child:Icon(ikon,color:renk)),
                title:Text(aciklama.isEmpty?'Gönderi':aciklama,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w800)),
                subtitle:Text(metric=='posts'?(zaman.isEmpty?'Gönderi':zaman):'$baslik: \${_deger(v)}\${zaman.isEmpty?'':' • $zaman'}'),
                trailing:const Icon(Icons.chevron_right_rounded),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:d.id))),
              );
            },
          );
        },
      ),
    ),
  );
}

'''
main = replace_once(main, "\nclass ProfilAramaPage extends StatefulWidget{", "\n"+detail_class+"class ProfilAramaPage extends StatefulWidget{", "insert interaction detail page")

MAIN.write_text(main, encoding="utf-8")

# 6) Story menu: share/highlight/archive plus safe delete confirmation.
story = STORY.read_text(encoding="utf-8")
old_func_start = story.index("  Future<void> _secenekler()async{")
old_func_end = story.index("\n  @override\n  void dispose()", old_func_start)
new_func = r'''  Future<void> _secenekler()async{
    _duraklat();
    final benim=FirebaseAuth.instance.currentUser?.uid==widget.ownerUid;
    final oneCikan=veri['highlighted']==true;
    final sec=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        if(benim)ListTile(
          leading:const Icon(Icons.share_outlined,color:mor),
          title:const Text('Hikâyeyi paylaş',style:TextStyle(fontWeight:FontWeight.w800)),
          onTap:()=>Navigator.pop(c,'share'),
        ),
        if(benim)ListTile(
          leading:Icon(oneCikan?Icons.star_rounded:Icons.star_border_rounded,color:oneCikan?Colors.amber:mor),
          title:Text(oneCikan?'Öne çıkanlardan kaldır':'Öne çıkanlara ekle',style:const TextStyle(fontWeight:FontWeight.w800)),
          onTap:()=>Navigator.pop(c,'highlight'),
        ),
        if(benim)ListTile(
          leading:const Icon(Icons.archive_outlined,color:mor),
          title:const Text('Arşive taşı',style:TextStyle(fontWeight:FontWeight.w800)),
          subtitle:const Text('Hikâye aktif görünümden kalkar, arşivinde kalır.'),
          onTap:()=>Navigator.pop(c,'archive'),
        ),
        if(benim)ListTile(
          leading:const Icon(Icons.delete_outline_rounded,color:Colors.red),
          title:const Text('Hikâyeyi sil',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),
          onTap:()=>Navigator.pop(c,'delete'),
        ),
        if(!benim)ListTile(
          leading:const Icon(Icons.flag_outlined,color:Colors.redAccent),
          title:const Text('Hikâyeyi bildir'),
          onTap:()=>Navigator.pop(c,'report'),
        ),
        ListTile(leading:const Icon(Icons.close_rounded),title:const Text('Kapat'),onTap:()=>Navigator.pop(c,'close')),
      ])),
    );
    if(!mounted)return;
    final d=belge;
    if(sec=='share'&&url.isNotEmpty){
      try{
        await SharePlus.instance.share(ShareParams(text:url));
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye paylaşılamadı.')));
      }
    }else if(sec=='highlight'&&d!=null){
      try{
        await d.reference.set({'highlighted':!oneCikan,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
        if(mounted)setState((){});
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(oneCikan?'Öne çıkanlardan kaldırıldı.':'Öne çıkanlara eklendi.')));
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Öne çıkanlar güncellenemedi.')));
      }
    }else if(sec=='archive'&&d!=null){
      try{
        await d.reference.set({
          'expiresAt':Timestamp.now(),
          'archivedAt':FieldValue.serverTimestamp(),
          'updatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true));
        hikayeler.removeAt(aktif);
        if(hikayeler.isEmpty){
          if(mounted){
            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye arşive taşındı.')));
            Navigator.pop(context);
          }
          return;
        }
        if(aktif>=hikayeler.length)aktif=hikayeler.length-1;
        if(mounted)setState((){});
        await _aktifHikayeyiBaslat();
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye arşive taşındı.')));
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye arşivlenemedi.')));
      }
    }else if(sec=='delete'&&storyId.isNotEmpty){
      final onay=await showDialog<bool>(
        context:context,
        builder:(c)=>AlertDialog(
          backgroundColor:Colors.white,
          surfaceTintColor:Colors.white,
          title:const Text('Hikâye silinsin mi?',style:TextStyle(fontWeight:FontWeight.w900)),
          content:const Text('Bu hikâye kalıcı olarak silinecek. Bu işlem geri alınamaz.'),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
            FilledButton(
              style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),
              onPressed:()=>Navigator.pop(c,true),
              child:const Text('Sil'),
            ),
          ],
        ),
      )??false;
      if(!onay){
        _devam();
        return;
      }
      try{
        await FirebaseFirestore.instance.collection('videos').doc(storyId).delete();
        hikayeler.removeAt(aktif);
        if(hikayeler.isEmpty){
          if(mounted){
            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye silindi.')));
            Navigator.pop(context);
          }
          return;
        }
        if(aktif>=hikayeler.length)aktif=hikayeler.length-1;
        if(mounted)setState((){});
        await _aktifHikayeyiBaslat();
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye silindi.')));
      }catch(_){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye silinemedi.')));
      }
    }else if(sec=='report'&&storyId.isNotEmpty){
      if(mounted)await sikayetEt(context,hedefTuru:'hikaye',hedefId:storyId,hedefUid:widget.ownerUid);
    }
    _devam();
  }
'''
story = story[:old_func_start] + new_func + story[old_func_end:]
STORY.write_text(story, encoding="utf-8")

print("Build 386 consolidated device fixes applied.")
