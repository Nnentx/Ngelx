part of 'main.dart';

String ngelxSesliSureMetni(Duration d){
  final toplam=d.inSeconds<0?0:d.inSeconds;
  final s=toplam%60,m=(toplam~/60)%60,h=toplam~/3600;
  String iki(int v)=>v.toString().padLeft(2,'0');
  return h>0?'${iki(h)}:${iki(m)}:${iki(s)}':'${iki(m)}:${iki(s)}';
}

class NgelxSesliSureSayaci extends StatefulWidget{
  final DateTime? baslangic;
  final bool bitti;
  const NgelxSesliSureSayaci({super.key,required this.baslangic,this.bitti=false});
  @override State<NgelxSesliSureSayaci> createState()=>_NgelxSesliSureSayaciState();
}
class _NgelxSesliSureSayaciState extends State<NgelxSesliSureSayaci>{
  Timer? _timer;
  Duration _sure=Duration.zero;
  void _hesapla(){
    final b=widget.baslangic;
    if(b==null)return;
    final yeni=DateTime.now().difference(b);
    if(mounted)setState(()=>_sure=yeni.isNegative?Duration.zero:yeni);
  }
  void _timerKur(){
    _timer?.cancel();
    _hesapla();
    if(!widget.bitti&&widget.baslangic!=null){
      _timer=Timer.periodic(const Duration(seconds:1),(_)=>_hesapla());
    }
  }
  @override void initState(){super.initState();_timerKur();}
  @override void didUpdateWidget(covariant NgelxSesliSureSayaci oldWidget){
    super.didUpdateWidget(oldWidget);
    if(oldWidget.baslangic!=widget.baslangic||oldWidget.bitti!=widget.bitti)_timerKur();
  }
  @override Widget build(BuildContext context)=>Container(
    padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),
    decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(14),border:Border.all(color:const Color(0xFFE4D8FA))),
    child:Row(mainAxisSize:MainAxisSize.min,children:[
      Icon(widget.bitti?Icons.stop_circle_outlined:Icons.timer_outlined,size:15,color:widget.bitti?Colors.redAccent:mor),
      const SizedBox(width:4),
      Text(ngelxSesliSureMetni(_sure),style:const TextStyle(color:Colors.black87,fontSize:12,fontWeight:FontWeight.w900)),
    ]),
  );
  @override void dispose(){_timer?.cancel();super.dispose();}
}

Future<void> ngelxSesliKatilimciYaz({
  required String roomId,
  required String uid,
  required String ad,
  required String foto,
  required String rol,
})async{
  if(roomId.isEmpty||uid.isEmpty)return;
  await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).collection('participants').doc(uid).set({
    'userId':uid,
    'displayName':ad,
    'photoUrl':foto,
    'role':rol,
    'active':true,
    'removed':false,
    'joinedAt':FieldValue.serverTimestamp(),
    'lastSeenAt':FieldValue.serverTimestamp(),
  },SetOptions(merge:true));
}

Future<void> ngelxSesliKatilimciAyril(String roomId,String uid)async{
  if(roomId.isEmpty||uid.isEmpty)return;
  try{
    await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).collection('participants').doc(uid).set({
      'active':false,
      'leftAt':FieldValue.serverTimestamp(),
      'lastSeenAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
  }catch(_){}
}

Future<void> ngelxSesliTepkiGonder(String roomId,String emoji)async{
  final u=FirebaseAuth.instance.currentUser;if(u==null||roomId.isEmpty)return;
  await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).collection('reactions').add({
    'userId':u.uid,
    'emoji':emoji,
    'createdAt':FieldValue.serverTimestamp(),
  });
}

class NgelxSesliTepkiAkisi extends StatelessWidget{
  final String roomId;
  const NgelxSesliTepkiAkisi({super.key,required this.roomId});
  @override Widget build(BuildContext context)=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
    stream:FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).collection('reactions').orderBy('createdAt',descending:true).limit(16).snapshots(),
    builder:(_,s){
      final simdi=DateTime.now();
      final docs=(s.data?.docs??[]).where((d){
        final t=d.data()['createdAt'];
        return t is Timestamp&&simdi.difference(t.toDate()).inSeconds<=45;
      }).toList();
      if(docs.isEmpty)return const SizedBox.shrink();
      return Container(
        margin:const EdgeInsets.only(top:10),
        padding:const EdgeInsets.symmetric(horizontal:10,vertical:8),
        decoration:BoxDecoration(color:const Color(0xFFFBF9FE),borderRadius:BorderRadius.circular(18)),
        child:Wrap(spacing:8,runSpacing:5,children:docs.take(12).map((d)=>Text((d.data()['emoji']??'👏').toString(),style:const TextStyle(fontSize:22))).toList()),
      );
    },
  );
}

Future<void> ngelxSesliPaylas(BuildContext context,String roomId,String baslik)async{
  await ngelxSesliNgelxIcindePaylas(context,roomId,baslik);
}

String ngelxSesliMesajRolEtiketi(String rol){
  if(rol=='owner')return 'ADMIN';
  if(rol=='moderator')return 'YÖNETİCİ';
  if(rol=='speaker')return 'KONUŞMACI';
  return '';
}

Widget ngelxSesliMesajRolRozeti(String rol){
  final yazi=ngelxSesliMesajRolEtiketi(rol);
  if(yazi.isEmpty)return const SizedBox.shrink();
  final admin=rol=='owner';
  final yonetici=rol=='moderator';
  final renk=admin?Colors.red:yonetici?const Color(0xFFFF8A00):mor;
  return Container(
    margin:const EdgeInsets.only(left:5),
    padding:const EdgeInsets.symmetric(horizontal:6,vertical:2),
    decoration:BoxDecoration(color:renk.withValues(alpha:admin?1:.12),borderRadius:BorderRadius.circular(8),border:admin?null:Border.all(color:renk.withValues(alpha:.35))),
    child:Text(yazi,style:TextStyle(color:admin?Colors.white:renk,fontSize:8.5,fontWeight:FontWeight.w900)),
  );
}

int ngelxSesliMesajHash(String text){
  var h=17;
  for(final x in text.codeUnits)h=((h*31)+x)&0x7fffffff;
  return h;
}

Future<String?> ngelxSesliMesajGonder({
  required String roomId,
  required String ad,
  required String foto,
  required String text,
  Map<String,String> mentionlar=const <String,String>{},
})async{
  final u=FirebaseAuth.instance.currentUser,t=text.trim();
  if(u==null||t.isEmpty)return null;
  try{
    final odaRef=FirebaseFirestore.instance.collection('audio_rooms').doc(roomId);
    final oda=(await odaRef.get()).data()??<String,dynamic>{};
    if(oda['active']!=true)return 'Bu sesli oda sona erdi.';
    final susturulan=List<String>.from(oda['chatMutedUserIds']??const[]);
    final katilimci=(await odaRef.collection('participants').doc(u.uid).get()).data()??<String,dynamic>{};
    if(susturulan.contains(u.uid)||katilimci['chatMuted']==true)return 'ADMIN veya yönetici seni sohbetten susturdu.';
    final owner=(oda['ownerId']??'').toString();
    final mods=List<String>.from(oda['moderatorIds']??const[]);
    final sp=List<String>.from(oda['speakerIds']??const[]);
    final rol=u.uid==owner?'owner':mods.contains(u.uid)?'moderator':sp.contains(u.uid)?'speaker':'listener';
    final temiz=t.length>600?t.substring(0,600):t;
    final bucket=DateTime.now().millisecondsSinceEpoch~/3000;
    final mesajId='${u.uid}_${bucket}_${ngelxSesliMesajHash(temiz)}';
    final gecerliMentionlar=<String,String>{};
    for(final e in mentionlar.entries){
      if(e.key!=u.uid&&e.key.isNotEmpty&&e.value.trim().isNotEmpty&&temiz.toLowerCase().contains('@${e.value.trim().toLowerCase()}')){
        gecerliMentionlar[e.key]=e.value.trim();
      }
    }
    await odaRef.collection('messages').doc(mesajId).set({
      'userId':u.uid,
      'displayName':ad,
      'photoUrl':foto,
      'text':temiz,
      'authorRole':rol,
      'createdAt':FieldValue.serverTimestamp(),
      'pinned':false,
      'mentionedUserIds':gecerliMentionlar.keys.toList(),
      'clientDedupeKey':mesajId,
    });
    final odaBaslik=(oda['title']??'Sesli oda').toString();
    for(final hedefUid in gecerliMentionlar.keys){
      unawaited(uygulamaBildirimiGonder(
        toUid:hedefUid,
        fromUid:u.uid,
        tur:'audio_live',
        metin:'“$odaBaslik” sesli odasında senden bahsetti.',
        belgeId:roomId,
        hedefTuru:'audio_room',
        hedefBaslik:odaBaslik,
        olayTuru:'audio_room_mention',
        onizleme:temiz,
        eylem:'open_audio_room',
        dedupeKey:'audio_room_mention_${roomId}_${mesajId}_$hedefUid',
      ));
    }
    return null;
  }catch(_){
    return 'Mesaj gönderilemedi.';
  }
}

Future<void> ngelxSesliMesajDuzenle(BuildContext context,DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> v)async{
  final controller=TextEditingController(text:(v['text']??'').toString());
  final yeni=await showDialog<String>(
    context:context,
    builder:(c)=>AlertDialog(
      title:const Text('Mesajı düzenle'),
      content:TextField(
        controller:controller,
        autofocus:true,
        maxLength:600,
        minLines:1,
        maxLines:5,
        style:const TextStyle(color:Colors.black87),
        decoration:const InputDecoration(hintText:'Mesaj'),
      ),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Vazgeç')),
        FilledButton(onPressed:()=>Navigator.pop(c,controller.text.trim()),child:const Text('Kaydet')),
      ],
    ),
  );
  controller.dispose();
  if(yeni==null||yeni.isEmpty||yeni==(v['text']??'').toString().trim())return;
  try{
    await ref.update({'text':yeni,'editedAt':FieldValue.serverTimestamp()});
  }catch(_){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj düzenlenemedi.')));
  }
}

String? ngelxSesliEtiketAramasi(String text){
  final i=text.lastIndexOf('@');
  if(i<0)return null;
  final once=i==0?' ':text.substring(i-1,i);
  if(i>0&&!RegExp(r'\s').hasMatch(once))return null;
  final q=text.substring(i+1);
  if(q.contains('\n')||q.length>36)return null;
  return q.trim().toLowerCase();
}

Future<void> ngelxSesliKullaniciMenuAc(BuildContext context,String roomId,String hedefUid,String ad)async{
  final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null)return;
  final ref=FirebaseFirestore.instance.collection('audio_rooms').doc(roomId);
  final oda=(await ref.get()).data()??<String,dynamic>{};
  final owner=(oda['ownerId']??'').toString();
  final mods=List<String>.from(oda['moderatorIds']??const[]);
  final admin=owner==ben,yonetici=mods.contains(ben);
  if(!admin&&!yonetici){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu işlem için yönetici yetkisi gerekiyor.')));
    return;
  }
  if(hedefUid==owner){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('ADMIN hesabı yönetilemez.')));
    return;
  }
  if(yonetici&&mods.contains(hedefUid)){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yöneticiler birbirini yönetemez.')));
    return;
  }
  final speakers=List<String>.from(oda['speakerIds']??const[]);
  final susturulan=List<String>.from(oda['chatMutedUserIds']??const[]);
  final hedefMod=mods.contains(hedefUid),speaker=speakers.contains(hedefUid),chatMuted=susturulan.contains(hedefUid);
  if(!context.mounted)return;
  final sec=await showModalBottomSheet<String>(
    context:context,
    backgroundColor:Colors.white,
    showDragHandle:true,
    builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Padding(padding:const EdgeInsets.fromLTRB(18,0,18,8),child:Row(children:[
        Icon(admin?Icons.admin_panel_settings_rounded:Icons.shield_rounded,color:admin?Colors.red:const Color(0xFFFF8A00)),
        const SizedBox(width:8),
        Expanded(child:Text(ad,style:const TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900))),
      ])),
      if(!speaker)ListTile(leading:const Icon(Icons.mic_rounded,color:mor),title:const Text('Konuşmacı yap'),onTap:()=>Navigator.pop(c,'speaker')),
      if(speaker)ListTile(leading:const Icon(Icons.mic_off_rounded,color:Colors.orange),title:const Text('Mikrofonunu kapat / dinleyici yap'),onTap:()=>Navigator.pop(c,'mute')),
      if(admin&&!hedefMod)ListTile(leading:const Icon(Icons.shield_outlined,color:Color(0xFFFF8A00)),title:const Text('Yönetici yap'),onTap:()=>Navigator.pop(c,'moderator')),
      if(admin&&hedefMod)ListTile(leading:const Icon(Icons.shield_outlined,color:Colors.orange),title:const Text('Yöneticiliği kaldır'),onTap:()=>Navigator.pop(c,'unmoderator')),
      ListTile(leading:Icon(chatMuted?Icons.chat_bubble_outline:Icons.comments_disabled_outlined,color:Colors.orange),title:Text(chatMuted?'Sohbet susturmasını kaldır':'Sohbetten sustur'),onTap:()=>Navigator.pop(c,'chatmute')),
      const Divider(height:1),
      ListTile(leading:const Icon(Icons.person_remove_alt_1_rounded,color:Colors.redAccent),title:const Text('Odadan çıkar',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'remove')),
      if(admin)ListTile(leading:const Icon(Icons.block_rounded,color:Colors.red),title:const Text('Odadan çıkar ve tekrar girişini engelle',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w900)),onTap:()=>Navigator.pop(c,'ban')),
    ])),
  );
  if(sec!=null&&context.mounted)await ngelxSesliRolDegistir(context:context,roomId:roomId,hedefUid:hedefUid,islem:sec);
}

Future<void> ngelxSesliRolDegistir({
  required BuildContext context,
  required String roomId,
  required String hedefUid,
  required String islem,
})async{
  final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||hedefUid.isEmpty||hedefUid==ben)return;
  final ref=FirebaseFirestore.instance.collection('audio_rooms').doc(roomId);
  final pref=ref.collection('participants').doc(hedefUid);
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final d=await tx.get(ref),v=d.data()??<String,dynamic>{};
      final owner=(v['ownerId']??'').toString();
      final sp=List<String>.from(v['speakerIds']??const[]);
      final mods=List<String>.from(v['moderatorIds']??const[]);
      final banned=List<String>.from(v['bannedUserIds']??const[]);
      final chatMuted=List<String>.from(v['chatMutedUserIds']??const[]);
      final admin=owner==ben,yonetici=mods.contains(ben);
      if(!admin&&!yonetici)throw StateError('manager_only');
      if(hedefUid==owner)throw StateError('admin_target');
      if(yonetici&&mods.contains(hedefUid))throw StateError('manager_target');
      if(yonetici&&!const ['speaker','listener','mute','chatmute','remove'].contains(islem))throw StateError('admin_only');

      if(islem=='speaker'){
        if(!sp.contains(hedefUid)&&sp.length>=ngelxSesliMaksKonusmaci)throw StateError('speaker_limit');
        if(!sp.contains(hedefUid))sp.add(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':mods.contains(hedefUid)?'moderator':'speaker','removed':false,'banned':false,'active':true,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='listener'||islem=='mute'){
        sp.remove(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':mods.contains(hedefUid)?'moderator':'listener','forcedMutedAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='moderator'){
        if(!admin)throw StateError('admin_only');
        if(!mods.contains(hedefUid)&&mods.length>=ngelxSesliMaksModerator)throw StateError('moderator_limit');
        if(!mods.contains(hedefUid))mods.add(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':'moderator','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='unmoderator'){
        if(!admin)throw StateError('admin_only');
        mods.remove(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':sp.contains(hedefUid)?'speaker':'listener','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='chatmute'){
        final participantDoc=await tx.get(pref);
        final participantMuted=participantDoc.data()?['chatMuted']==true;
        final yeniMuted=chatMuted.contains(hedefUid)?false:!participantMuted;
        if(admin){
          if(yeniMuted&&!chatMuted.contains(hedefUid))chatMuted.add(hedefUid);
          if(!yeniMuted)chatMuted.remove(hedefUid);
          tx.update(ref,{'chatMutedUserIds':chatMuted,'updatedAt':FieldValue.serverTimestamp()});
        }
        tx.set(pref,{'chatMuted':yeniMuted,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='remove'||islem=='ban'){
        if(islem=='ban'&&!admin)throw StateError('admin_only');
        sp.remove(hedefUid);mods.remove(hedefUid);
        if(islem=='ban'&&!banned.contains(hedefUid))banned.add(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'moderatorIds':mods,'bannedUserIds':banned,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':'removed','active':false,'removed':true,'banned':islem=='ban','removedAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }
    });
    if(context.mounted){
      final m=islem=='ban'?'Kullanıcı odadan çıkarıldı ve tekrar girişi engellendi.':islem=='remove'?'Kullanıcı odadan çıkarıldı.':islem=='chatmute'?'Sohbet yetkisi güncellendi.':'Kullanıcı yetkisi güncellendi.';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(m)));
    }
  }catch(e){
    if(context.mounted){
      final s=e.toString();
      final m=s.contains('speaker_limit')?'Konuşmacı sınırı dolu.':s.contains('moderator_limit')?'Yönetici sınırı dolu.':s.contains('admin_only')?'Bu işlem yalnızca ADMIN tarafından yapılabilir.':s.contains('admin_target')?'ADMIN hesabı yönetilemez.':s.contains('manager_target')?'Yöneticiler birbirini yönetemez.':s.contains('manager_only')?'Yönetici yetkisi gerekiyor.':'İşlem tamamlanamadı.';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(m)));
    }
  }
}

Future<void> ngelxSesliKatilimcilarAc(BuildContext context,String roomId,String ownerId)async{
  final ben=FirebaseAuth.instance.currentUser?.uid;
  if(ben==null)return;
  final oda=(await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).get()).data()??<String,dynamic>{};
  final mods=List<String>.from(oda['moderatorIds']??const[]);
  final benYonetici=ben==ownerId||mods.contains(ben);
  await showModalBottomSheet<void>(
    context:context,
    backgroundColor:Colors.white,
    showDragHandle:true,
    isScrollControlled:true,
    shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
    builder:(c)=>SafeArea(
      top:false,
      child:SizedBox(
        height:MediaQuery.sizeOf(c).height*.62,
        child:Column(children:[
          Padding(
            padding:const EdgeInsets.fromLTRB(18,0,10,8),
            child:Row(children:[
              const Icon(Icons.headphones_rounded,color:mor),
              const SizedBox(width:9),
              const Expanded(child:Text('Odadaki kişiler',style:TextStyle(color:Colors.black87,fontSize:18,fontWeight:FontWeight.w900))),
              IconButton(onPressed:()=>Navigator.pop(c),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
            ]),
          ),
          const Divider(height:1,color:Color(0xFFEDE8F2)),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).collection('participants').where('active',isEqualTo:true).limit(100).snapshots(),
            builder:(_,s){
              if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
              if(s.hasError)return const Center(child:Text('Katılımcılar yüklenemedi.',style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)));
              final docs=s.data?.docs??[];
              if(docs.isEmpty)return const Center(child:Text('Şu anda aktif katılımcı yok.',style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)));
              return ListView.separated(
                itemCount:docs.length,
                separatorBuilder:(_,__)=>const Divider(height:1,indent:70,color:Color(0xFFF1EDF4)),
                itemBuilder:(_,i){
                  final d=docs[i],v=d.data(),id=(v['userId']??d.id).toString(),foto=(v['photoUrl']??'').toString(),rol=(v['role']??'listener').toString();
                  final sahip=id==ownerId;
                  final rolYazi=sahip?'ADMIN':rol=='moderator'?'YÖNETİCİ':rol=='speaker'?'Konuşmacı':'Dinleyici';
                  return ListTile(
                    leading:CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),
                    title:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
                    subtitle:Text(rolYazi,style:TextStyle(color:rol=='moderator'?mor:Colors.black45,fontWeight:FontWeight.w700)),
                    trailing:benYonetici&&!sahip?IconButton(
                      tooltip:'Kullanıcıyı yönet',
                      onPressed:()=>ngelxSesliKullaniciMenuAc(c,roomId,id,(v['displayName']??'NgelX').toString()),
                      icon:const Icon(Icons.admin_panel_settings_outlined,color:mor),
                    ):null,
                  );
                },
              );
            },
          )),
        ]),
      ),
    ),
  );
}

Future<bool> ngelxSesliMesajSilOnayi(BuildContext context)async{
  if(!context.mounted)return false;
  return await showDialog<bool>(
    context:context,
    builder:(c)=>AlertDialog(
      backgroundColor:Colors.white,
      surfaceTintColor:Colors.white,
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(24)),
      icon:const Icon(Icons.delete_outline_rounded,color:Colors.redAccent,size:34),
      title:const Text('Mesaj silinsin mi?',textAlign:TextAlign.center,style:TextStyle(fontWeight:FontWeight.w900)),
      content:const Text('Bu işlem geri alınamaz.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
        FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.redAccent),onPressed:()=>Navigator.pop(c,true),child:const Text('Sil')),
      ],
    ),
  )??false;
}

class NgelxSesliSohbetPanel extends StatefulWidget{
  final String roomId;
  final bool yonetici,sahibiyim,bitti;
  const NgelxSesliSohbetPanel({super.key,required this.roomId,required this.yonetici,required this.sahibiyim,required this.bitti});
  @override State<NgelxSesliSohbetPanel> createState()=>_NgelxSesliSohbetPanelState();
}
class _NgelxSesliSohbetPanelState extends State<NgelxSesliSohbetPanel>{
  final _mesaj=TextEditingController();
  bool _gonderiyor=false;
  String _ad='NgelX',_foto='';
  String? _etiketArama;
  final Map<String,String> _etiketler=<String,String>{};
  @override void initState(){super.initState();_mesaj.addListener(_metinDegisti);unawaited(_profil());}
  void _metinDegisti(){
    final q=ngelxSesliEtiketAramasi(_mesaj.text);
    if(q!=_etiketArama&&mounted)setState(()=>_etiketArama=q);
  }
  void _etiketSec(String uid,String ad){
    final t=_mesaj.text,i=t.lastIndexOf('@');if(i<0)return;
    final yeni=t.substring(0,i)+'@'+ad+' ';
    _etiketler[uid]=ad;
    _mesaj.value=TextEditingValue(text:yeni,selection:TextSelection.collapsed(offset:yeni.length));
    if(mounted)setState(()=>_etiketArama=null);
  }
  Widget _etiketOnerileri(){
    if(_etiketArama==null)return const SizedBox.shrink();
    final ben=FirebaseAuth.instance.currentUser?.uid,q=_etiketArama!;
    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('participants').where('active',isEqualTo:true).limit(20).snapshots(),
      builder:(_,s){
        final docs=(s.data?.docs??[]).where((d){
          final v=d.data(),uid=(v['userId']??d.id).toString(),ad=(v['displayName']??'').toString();
          return uid!=ben&&ad.isNotEmpty&&(q.isEmpty||ad.toLowerCase().contains(q));
        }).take(8).toList();
        if(docs.isEmpty)return const SizedBox.shrink();
        return SizedBox(height:46,child:ListView.separated(
          padding:const EdgeInsets.symmetric(horizontal:10,vertical:4),
          scrollDirection:Axis.horizontal,
          itemCount:docs.length,
          separatorBuilder:(_,__)=>const SizedBox(width:5),
          itemBuilder:(_,i){
            final v=docs[i].data(),uid=(v['userId']??docs[i].id).toString(),ad=(v['displayName']??'NgelX').toString(),foto=(v['photoUrl']??'').toString();
            return ActionChip(
              avatar:CircleAvatar(radius:10,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,size:11):null),
              label:Text('@'+ad,maxLines:1,overflow:TextOverflow.ellipsis),
              onPressed:()=>_etiketSec(uid,ad),
            );
          },
        ));
      },
    );
  }
  Future<void> _profil()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null)return;
    try{
      final p=(await FirebaseFirestore.instance.collection('users').doc(u.uid).get()).data()??<String,dynamic>{};
      if(mounted)setState((){_ad=(p['displayName']??p['username']??u.displayName??'NgelX').toString();_foto=(p['photoUrl']??'').toString();});
    }catch(_){}
  }
  Future<void> _gonder()async{
    final t=_mesaj.text.trim();
    if(t.isEmpty||_gonderiyor||widget.bitti)return;
    setState(()=>_gonderiyor=true);
    final mentionlar=<String,String>{for(final e in _etiketler.entries)if(t.toLowerCase().contains('@'+e.value.toLowerCase()))e.key:e.value};
    _mesaj.clear();_etiketler.clear();
    final hata=await ngelxSesliMesajGonder(roomId:widget.roomId,ad:_ad,foto:_foto,text:t,mentionlar:mentionlar);
    if(hata!=null&&mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hata)));
    if(mounted)setState(()=>_gonderiyor=false);
  }
  Future<void> _mesajIslem(DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> v)async{
    final ben=FirebaseAuth.instance.currentUser?.uid,benim=(v['userId']??'').toString()==ben;
    final sec=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      if(benim)ListTile(leading:const Icon(Icons.edit_outlined,color:mor),title:const Text('Mesajı düzenle',style:TextStyle(color:mor,fontWeight:FontWeight.w900)),onTap:()=>Navigator.pop(c,'edit')),
      if(widget.yonetici&&!benim)ListTile(leading:const Icon(Icons.push_pin_outlined,color:mor),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle'),onTap:()=>Navigator.pop(c,'pin')),
      if(widget.yonetici&&!benim)ListTile(leading:const Icon(Icons.admin_panel_settings_outlined,color:mor),title:const Text('Kullanıcıyı yönet'),onTap:()=>Navigator.pop(c,'manage')),
      if(widget.yonetici||benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.redAccent),title:const Text('Mesajı sil',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'delete')),
    ])));
    if(sec=='edit'&&mounted)await ngelxSesliMesajDuzenle(context,ref,v);
    if(sec=='delete'&&await ngelxSesliMesajSilOnayi(context))await ref.delete();
    if(sec=='pin')await ref.set({'pinned':v['pinned']!=true,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    if(sec=='manage'&&mounted)await ngelxSesliKullaniciMenuAc(context,widget.roomId,(v['userId']??'').toString(),(v['displayName']??'NgelX').toString());
  }
  @override Widget build(BuildContext context){
    final ben=FirebaseAuth.instance.currentUser?.uid;
    return Material(
      color:Colors.white,
      child:SafeArea(
        top:false,
        child:Column(children:[
          Padding(padding:const EdgeInsets.fromLTRB(18,4,10,8),child:Row(children:[
            const Icon(Icons.chat_bubble_rounded,color:mor),const SizedBox(width:9),
            const Expanded(child:Text('Oda sohbeti',style:TextStyle(color:Colors.black87,fontSize:18,fontWeight:FontWeight.w900))),
            IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
          ])),
          const Divider(height:1,color:Color(0xFFEDE8F2)),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('messages').orderBy('createdAt',descending:true).limit(100).snapshots(),
            builder:(_,s){
              if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
              final docs=s.data?.docs??[];
              if(docs.isEmpty)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.forum_outlined,color:mor,size:38),SizedBox(height:8),Text('Henüz mesaj yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),Text('İlk mesajı sen yazabilirsin.',style:TextStyle(color:Colors.black45))]));
              return ListView.builder(
                reverse:true,
                padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
                itemCount:docs.length,
                itemBuilder:(_,i){
                  final d=docs[i],v=d.data(),benim=(v['userId']??'').toString()==ben,pin=v['pinned']==true,foto=(v['photoUrl']??'').toString();
                  return Align(
                    alignment:benim?Alignment.centerRight:Alignment.centerLeft,
                    child:GestureDetector(
                      onTap:()=>_mesajIslem(d.reference,v),
                      onLongPress:()=>_mesajIslem(d.reference,v),
                      child:Container(
                        constraints:BoxConstraints(maxWidth:MediaQuery.sizeOf(context).width*.78),
                        margin:const EdgeInsets.symmetric(vertical:4),
                        padding:const EdgeInsets.fromLTRB(12,8,12,9),
                        decoration:BoxDecoration(color:benim?const Color(0xFFF0E8FF):const Color(0xFFF4F4F6),borderRadius:BorderRadius.circular(16),border:pin?Border.all(color:mor):null),
                        child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                          Row(mainAxisSize:MainAxisSize.min,children:[
                            CircleAvatar(radius:9,backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,size:10,color:mor):null),
                            const SizedBox(width:5),
                            if(pin)...[const Icon(Icons.push_pin_rounded,size:13,color:mor),const SizedBox(width:3)],
                            Flexible(child:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black54,fontSize:10.5,fontWeight:FontWeight.w900))),
                            ngelxSesliMesajRolRozeti((v['authorRole']??'').toString()),
                          ]),
                          const SizedBox(height:2),
                          Text((v['text']??'').toString(),style:const TextStyle(color:Colors.black87,fontSize:14.5,height:1.3)),
                          if(v['editedAt']!=null)const Padding(padding:EdgeInsets.only(top:2),child:Text('düzenlendi',style:TextStyle(color:Colors.black38,fontSize:9,fontStyle:FontStyle.italic))),
                        ]),
                      ),
                    ),
                  );
                },
              );
            },
          )),
          _etiketOnerileri(),
          Container(
            padding:EdgeInsets.fromLTRB(10,8,10,8+MediaQuery.viewInsetsOf(context).bottom),
            decoration:const BoxDecoration(color:Colors.white,border:Border(top:BorderSide(color:Color(0xFFEDE8F2)))),
            child:Row(children:[
              Expanded(child:TextField(
                controller:_mesaj,
                enabled:!widget.bitti,
                minLines:1,maxLines:4,
                style:const TextStyle(color:Colors.black87),
                decoration:InputDecoration(hintText:widget.bitti?'Bu oda sona erdi':'Mesaj yaz...',hintStyle:const TextStyle(color:Colors.black38),filled:true,fillColor:const Color(0xFFF5F5F8),contentPadding:const EdgeInsets.symmetric(horizontal:14,vertical:10),border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none)),
                onSubmitted:(_)=>_gonder(),
              )),
              const SizedBox(width:7),
              IconButton.filled(style:IconButton.styleFrom(backgroundColor:mor),onPressed:_gonderiyor||widget.bitti?null:_gonder,icon:_gonderiyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded,color:Colors.white)),
            ]),
          ),
        ]),
      ),
    );
  }
  @override void dispose(){_mesaj.removeListener(_metinDegisti);_mesaj.dispose();super.dispose();}
}

Future<void> ngelxSesliSohbetAc(BuildContext context,String roomId,bool yonetici,{required bool sahibiyim,required bool bitti})async{
  await showModalBottomSheet<void>(
    context:context,
    backgroundColor:Colors.white,
    isScrollControlled:true,
    useSafeArea:true,
    shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
    builder:(c)=>FractionallySizedBox(heightFactor:.78,child:NgelxSesliSohbetPanel(roomId:roomId,yonetici:yonetici,sahibiyim:sahibiyim,bitti:bitti)),
  );
}


class NgelxSesliInlineSohbet extends StatefulWidget{
  final String roomId;
  final bool yonetici,sahibiyim,bitti;
  const NgelxSesliInlineSohbet({super.key,required this.roomId,required this.yonetici,required this.sahibiyim,required this.bitti});
  @override State<NgelxSesliInlineSohbet> createState()=>_NgelxSesliInlineSohbetState();
}
class _NgelxSesliInlineSohbetState extends State<NgelxSesliInlineSohbet>{
  final _mesaj=TextEditingController();
  final _liste=ScrollController();
  bool _gonderiyor=false,_enYenide=true;
  String _ad='NgelX',_foto='';
  String? _etiketArama;
  final Map<String,String> _etiketler=<String,String>{};

  @override void initState(){
    super.initState();
    _liste.addListener(_kaydirmaDegisti);
    _mesaj.addListener(_metinDegisti);
    unawaited(_profil());
  }

  void _metinDegisti(){
    final q=ngelxSesliEtiketAramasi(_mesaj.text);
    if(q!=_etiketArama&&mounted)setState(()=>_etiketArama=q);
  }

  void _etiketSec(String uid,String ad){
    final t=_mesaj.text,i=t.lastIndexOf('@');if(i<0)return;
    final yeni=t.substring(0,i)+'@'+ad+' ';
    _etiketler[uid]=ad;
    _mesaj.value=TextEditingValue(text:yeni,selection:TextSelection.collapsed(offset:yeni.length));
    if(mounted)setState(()=>_etiketArama=null);
  }

  Widget _etiketOnerileri(){
    if(_etiketArama==null)return const SizedBox.shrink();
    final ben=FirebaseAuth.instance.currentUser?.uid,q=_etiketArama!;
    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('participants').where('active',isEqualTo:true).limit(20).snapshots(),
      builder:(_,s){
        final docs=(s.data?.docs??[]).where((d){
          final v=d.data(),uid=(v['userId']??d.id).toString(),ad=(v['displayName']??'').toString();
          return uid!=ben&&ad.isNotEmpty&&(q.isEmpty||ad.toLowerCase().contains(q));
        }).take(8).toList();
        if(docs.isEmpty)return const SizedBox.shrink();
        return SizedBox(height:42,child:ListView.separated(
          padding:const EdgeInsets.symmetric(horizontal:8,vertical:2),
          scrollDirection:Axis.horizontal,
          itemCount:docs.length,
          separatorBuilder:(_,__)=>const SizedBox(width:4),
          itemBuilder:(_,i){
            final v=docs[i].data(),uid=(v['userId']??docs[i].id).toString(),ad=(v['displayName']??'NgelX').toString(),foto=(v['photoUrl']??'').toString();
            return ActionChip(
              avatar:CircleAvatar(radius:9,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,size:10):null),
              label:Text('@'+ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:11)),
              onPressed:()=>_etiketSec(uid,ad),
            );
          },
        ));
      },
    );
  }

  void _kaydirmaDegisti(){
    if(!_liste.hasClients)return;
    final yeni=_liste.offset<36;
    if(yeni!=_enYenide&&mounted)setState(()=>_enYenide=yeni);
  }

  Future<void> _profil()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null)return;
    try{
      final p=(await FirebaseFirestore.instance.collection('users').doc(u.uid).get()).data()??<String,dynamic>{};
      if(mounted)setState((){_ad=(p['displayName']??p['username']??u.displayName??'NgelX').toString();_foto=(p['photoUrl']??'').toString();});
    }catch(_){}
  }

  Future<void> _gonder()async{
    final t=_mesaj.text.trim();
    if(t.isEmpty||_gonderiyor||widget.bitti)return;
    setState(()=>_gonderiyor=true);
    _mesaj.clear();
    final hata=await ngelxSesliMesajGonder(roomId:widget.roomId,ad:_ad,foto:_foto,text:t);
    if(hata!=null&&mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hata)));
    if(mounted){
      setState(()=>_gonderiyor=false);
      WidgetsBinding.instance.addPostFrameCallback((_){
        if(mounted&&_liste.hasClients)_liste.animateTo(0,duration:const Duration(milliseconds:220),curve:Curves.easeOut);
      });
    }
  }

  Future<void> _mesajIslem(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final v=d.data(),ben=FirebaseAuth.instance.currentUser?.uid,benim=(v['userId']??'').toString()==ben;
    final sec=await showModalBottomSheet<String>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        if(benim)ListTile(leading:const Icon(Icons.edit_outlined,color:mor),title:const Text('Mesajı düzenle',style:TextStyle(color:mor,fontWeight:FontWeight.w900)),onTap:()=>Navigator.pop(c,'edit')),
        if(widget.yonetici&&!benim)ListTile(leading:const Icon(Icons.push_pin_outlined,color:mor),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle'),onTap:()=>Navigator.pop(c,'pin')),
        if(widget.yonetici&&!benim)ListTile(leading:const Icon(Icons.admin_panel_settings_outlined,color:mor),title:const Text('Kullanıcıyı yönet'),onTap:()=>Navigator.pop(c,'manage')),
        if(widget.yonetici||benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.redAccent),title:const Text('Mesajı sil',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'delete')),
      ])),
    );
    if(sec=='edit'&&mounted)await ngelxSesliMesajDuzenle(context,d.reference,v);
    if(sec=='delete'&&await ngelxSesliMesajSilOnayi(context))await d.reference.delete();
    if(sec=='pin')await d.reference.set({'pinned':v['pinned']!=true,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    if(sec=='manage'&&mounted)await ngelxSesliKullaniciMenuAc(context,widget.roomId,(v['userId']??'').toString(),(v['displayName']??'NgelX').toString());
  }

  Widget _mesajBalonu(QueryDocumentSnapshot<Map<String,dynamic>> d){
    final v=d.data(),ben=FirebaseAuth.instance.currentUser?.uid;
    final benim=(v['userId']??'').toString()==ben;
    final ad=(v['displayName']??'NgelX').toString(),metin=(v['text']??'').toString(),rol=(v['authorRole']??'').toString(),pin=v['pinned']==true,foto=(v['photoUrl']??'').toString();
    return Align(
      alignment:benim?Alignment.centerRight:Alignment.centerLeft,
      child:GestureDetector(
        onTap:()=>_mesajIslem(d),
        onLongPress:()=>_mesajIslem(d),
        child:Container(
          constraints:BoxConstraints(maxWidth:MediaQuery.sizeOf(context).width*.82),
          margin:const EdgeInsets.symmetric(horizontal:10,vertical:3),
          padding:const EdgeInsets.fromLTRB(11,7,11,8),
          decoration:BoxDecoration(
            color:benim?const Color(0xFFF0E8FF):const Color(0xFFF5F5F7),
            borderRadius:BorderRadius.circular(15),
            border:pin?Border.all(color:mor,width:1.2):null,
          ),
          child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
            Row(mainAxisSize:MainAxisSize.min,children:[
              CircleAvatar(radius:9,backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,size:10,color:mor):null),
              const SizedBox(width:5),
              if(pin)...[const Icon(Icons.push_pin_rounded,size:12,color:mor),const SizedBox(width:3)],
              Flexible(child:Text(ad,overflow:TextOverflow.ellipsis,style:const TextStyle(color:mor,fontSize:10.5,fontWeight:FontWeight.w900))),
              ngelxSesliMesajRolRozeti(rol),
            ]),
            const SizedBox(height:2),
            Text(metin,style:const TextStyle(color:Colors.black87,fontSize:13.5,height:1.25)),
            if(v['editedAt']!=null)const Padding(padding:EdgeInsets.only(top:2),child:Text('düzenlendi',style:TextStyle(color:Colors.black38,fontSize:8.8,fontStyle:FontStyle.italic))),
          ]),
        ),
      ),
    );
  }

  @override Widget build(BuildContext context)=>Container(
    height:230,
    decoration:const BoxDecoration(color:Colors.white,border:Border(top:BorderSide(color:Color(0xFFEDE8F2)))),
    child:Column(children:[
      SizedBox(
        height:38,
        child:Padding(
          padding:const EdgeInsets.symmetric(horizontal:12),
          child:Row(children:[
            const Icon(Icons.chat_bubble_rounded,color:mor,size:17),
            const SizedBox(width:6),
            const Text('Sohbet',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
            const Spacer(),
            if(!_enYenide)
              TextButton.icon(
                style:TextButton.styleFrom(padding:const EdgeInsets.symmetric(horizontal:7),visualDensity:VisualDensity.compact),
                onPressed:(){
                  if(_liste.hasClients)_liste.animateTo(0,duration:const Duration(milliseconds:240),curve:Curves.easeOut);
                },
                icon:const Icon(Icons.arrow_downward_rounded,size:14),
                label:const Text('Yeni mesajlar',style:TextStyle(fontSize:10.5,fontWeight:FontWeight.w800)),
              ),
          ]),
        ),
      ),
      Expanded(
        child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('messages').orderBy('createdAt',descending:true).limit(80).snapshots(),
          builder:(_,s){
            final docs=s.data?.docs??[];
            if(s.connectionState==ConnectionState.waiting&&docs.isEmpty)return const Center(child:SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:mor)));
            if(docs.isEmpty)return Center(child:Padding(padding:const EdgeInsets.symmetric(horizontal:18),child:Text(widget.bitti?'Bu oda sona erdi • Sohbet salt okunur.':'Henüz mesaj yok • Mesajlar burada akış gibi görünecek.',textAlign:TextAlign.center,style:const TextStyle(color:Colors.black38,fontSize:11.5,fontWeight:FontWeight.w600))));
            return ListView.builder(
              controller:_liste,
              reverse:true,
              padding:const EdgeInsets.fromLTRB(2,2,2,5),
              physics:const BouncingScrollPhysics(parent:AlwaysScrollableScrollPhysics()),
              itemCount:docs.length,
              itemBuilder:(_,i)=>_mesajBalonu(docs[i]),
            );
          },
        ),
      ),
      _etiketOnerileri(),
      Padding(
        padding:const EdgeInsets.fromLTRB(10,5,10,8),
        child:Row(children:[
          Expanded(child:TextField(
            controller:_mesaj,
            enabled:!widget.bitti,
            minLines:1,maxLines:2,
            textInputAction:TextInputAction.send,
            style:const TextStyle(color:Colors.black87,fontSize:13.5),
            decoration:InputDecoration(
              hintText:widget.bitti?'Bu oda sona erdi':'Mesaj yaz...',
              hintStyle:const TextStyle(color:Colors.black38),
              filled:true,
              fillColor:const Color(0xFFF5F5F8),
              isDense:true,
              contentPadding:const EdgeInsets.symmetric(horizontal:13,vertical:10),
              border:OutlineInputBorder(borderRadius:BorderRadius.circular(20),borderSide:BorderSide.none),
            ),
            onSubmitted:widget.bitti?null:(_)=>_gonder(),
          )),
          const SizedBox(width:6),
          IconButton.filled(
            style:IconButton.styleFrom(backgroundColor:mor,minimumSize:const Size(42,42)),
            onPressed:_gonderiyor||widget.bitti?null:_gonder,
            icon:_gonderiyor?const SizedBox(width:17,height:17,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded,color:Colors.white,size:19),
          ),
        ]),
      ),
    ]),
  );

  @override void dispose(){
    _liste.removeListener(_kaydirmaDegisti);
    _mesaj.removeListener(_metinDegisti);
    _liste.dispose();
    _mesaj.dispose();
    super.dispose();
  }
}




class NgelxYerlesikMuzik{
  final String id,baslik,kategori,aciklama;
  final IconData ikon;
  const NgelxYerlesikMuzik(this.id,this.baslik,this.kategori,this.aciklama,this.ikon);
}

const List<NgelxYerlesikMuzik> ngelxYerlesikMuzikler=[
  NgelxYerlesikMuzik('mor_gece','Mor Gece','Chill','Yumuşak ambient döngü • NgelX Original',Icons.nightlight_round),
  NgelxYerlesikMuzik('sakin_akis','Sakin Akış','Chill','Rahat sohbet ritmi • NgelX Original',Icons.waves_rounded),
  NgelxYerlesikMuzik('odak','Odak','Odak','Minimal arpej döngüsü • NgelX Original',Icons.center_focus_strong_rounded),
  NgelxYerlesikMuzik('gun_dogumu','Gün Doğumu','Ambient','Sıcak pad ve hafif armoni • NgelX Original',Icons.wb_sunny_outlined),
  NgelxYerlesikMuzik('gece_yolu','Gece Yolu','Ambient','Derin ve sakin arka plan • NgelX Original',Icons.route_rounded),
  NgelxYerlesikMuzik('hafif_tempo','Hafif Tempo','Sohbet','Canlı ama konuşmayı bastırmayan döngü • NgelX Original',Icons.graphic_eq_rounded),
];

Future<String> ngelxYerlesikMuzikDosyasi(String trackId)async{
  final dir=await getTemporaryDirectory();
  final file=File('${dir.path}/ngelx_original_$trackId.wav');
  try{
    if(await file.exists()&&await file.length()>200000)return file.path;
  }catch(_){}
  const sampleRate=16000;
  const seconds=12;
  const totalSamples=sampleRate*seconds;
  const dataBytes=totalSamples*2;
  final data=ByteData(44+dataBytes);
  void ascii(int offset,String value){
    for(var i=0;i<value.length;i++)data.setUint8(offset+i,value.codeUnitAt(i));
  }
  ascii(0,'RIFF');
  data.setUint32(4,36+dataBytes,Endian.little);
  ascii(8,'WAVE');
  ascii(12,'fmt ');
  data.setUint32(16,16,Endian.little);
  data.setUint16(20,1,Endian.little);
  data.setUint16(22,1,Endian.little);
  data.setUint32(24,sampleRate,Endian.little);
  data.setUint32(28,sampleRate*2,Endian.little);
  data.setUint16(32,2,Endian.little);
  data.setUint16(34,16,Endian.little);
  ascii(36,'data');
  data.setUint32(40,dataBytes,Endian.little);

  late List<double> roots;
  late int style;
  switch(trackId){
    case 'sakin_akis': roots=[196.0,220.0,174.61,196.0];style=1;break;
    case 'odak': roots=[220.0,246.94,261.63,196.0];style=2;break;
    case 'gun_dogumu': roots=[261.63,293.66,220.0,246.94];style=3;break;
    case 'gece_yolu': roots=[146.83,164.81,130.81,146.83];style=4;break;
    case 'hafif_tempo': roots=[220.0,246.94,196.0,220.0];style=5;break;
    default: roots=[174.61,196.0,164.81,174.61];style=0;
  }
  final twoPi=math.pi*2;
  for(var i=0;i<totalSamples;i++){
    final t=i/sampleRate;
    final section=((t/3).floor())%roots.length;
    final root=roots[section];
    final local=t%3;
    final fadeIn=(local/.32).clamp(0.0,1.0).toDouble();
    final fadeOut=((3-local)/.38).clamp(0.0,1.0).toDouble();
    final env=math.min(fadeIn,fadeOut);
    double x=0;
    if(style==2){
      final step=((t*4).floor())%4;
      final note=<double>[1,1.25,1.5,2][step];
      x=.45*math.sin(twoPi*root*note*t)+.18*math.sin(twoPi*root*.5*t);
    }else{
      final third=style==3?1.2599:1.1892;
      const fifth=1.4983;
      x=.34*math.sin(twoPi*root*t)+.22*math.sin(twoPi*root*third*t)+.18*math.sin(twoPi*root*fifth*t)+.10*math.sin(twoPi*root*.5*t);
      if(style==1||style==5){
        final beat=t%.5;
        if(beat<.08)x+=.20*math.sin(twoPi*62*beat)*(1-beat/.08);
        final hat=t%.25;
        if(hat<.025)x+=.035*math.sin(i*1.618)*(1-hat/.025);
      }
      if(style==4)x+=.08*math.sin(twoPi*55*t);
    }
    x*=env*(style == 5 ? 0.72 : 0.64);
    final v=(x.clamp(-1.0,1.0)*32760).round();
    data.setInt16(44+i*2,v,Endian.little);
  }
  await file.writeAsBytes(data.buffer.asUint8List(),flush:true);
  return file.path;
}

class NgelxSesliMuzikKontrolu extends StatefulWidget{
  final String roomId;
  final bool yonetici,bitti;
  const NgelxSesliMuzikKontrolu({super.key,required this.roomId,required this.yonetici,required this.bitti});
  @override State<NgelxSesliMuzikKontrolu> createState()=>_NgelxSesliMuzikKontroluState();
}

class _NgelxSesliMuzikKontroluState extends State<NgelxSesliMuzikKontrolu>{
  final AudioPlayer _oynatici=AudioPlayer();
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _odaAboneligi;
  String _url='',_baslik='';
  bool _oynuyor=false,_hazirlaniyor=false,_yukleniyor=false;
  int _konumMs=0;
  Timestamp? _baslatildi;
  double _ses=.42;

  @override void initState(){
    super.initState();
    unawaited(_oynatici.setVolume(_ses));
    _odaAboneligi=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).snapshots().listen((d){
      final v=d.data()??<String,dynamic>{};
      unawaited(_durumuUygula(v));
    });
  }

  int _hedefKonumMs(){
    var hedef=_konumMs;
    if(_oynuyor&&_baslatildi!=null){
      final ek=DateTime.now().difference(_baslatildi!.toDate()).inMilliseconds;
      if(ek>0)hedef+=ek;
    }
    final sure=_oynatici.duration?.inMilliseconds??0;
    if(sure>0){
      if(_url.startsWith('ngelx://original/'))hedef=hedef%sure;
      else hedef=hedef.clamp(0,sure).toInt();
    }
    return hedef<0?0:hedef;
  }

  Future<void> _durumuUygula(Map<String,dynamic> v)async{
    final url=(v['musicUrl']??'').toString();
    final baslik=(v['musicTitle']??'').toString();
    final oynuyor=v['musicPlaying']==true&&!widget.bitti;
    final konum=(v['musicPositionMs'] is num)?(v['musicPositionMs'] as num).toInt():0;
    final baslatildi=v['musicStartedAt'] is Timestamp?v['musicStartedAt'] as Timestamp:null;
    if(mounted)setState((){_baslik=baslik;_oynuyor=oynuyor;_konumMs=konum;_baslatildi=baslatildi;});
    if(url.isEmpty){
      _url='';
      try{await _oynatici.stop();}catch(_){}
      return;
    }
    try{
      if(url!=_url){
        _url=url;
        if(mounted)setState(()=>_hazirlaniyor=true);
        if(url.startsWith('ngelx://original/')){
          final id=url.substring('ngelx://original/'.length);
          final path=await ngelxYerlesikMuzikDosyasi(id);
          await _oynatici.setFilePath(path);
          await _oynatici.setLoopMode(LoopMode.one);
        }else{
          await _oynatici.setUrl(url);
          await _oynatici.setLoopMode(LoopMode.off);
        }
        await _oynatici.setVolume(_ses);
      }
      final hedef=_hedefKonumMs();
      final fark=(_oynatici.position.inMilliseconds-hedef).abs();
      if(fark>1200)await _oynatici.seek(Duration(milliseconds:hedef));
      if(oynuyor){
        if(!_oynatici.playing)unawaited(_oynatici.play());
      }else if(_oynatici.playing){
        await _oynatici.pause();
      }
    }catch(_){
    }finally{
      if(mounted)setState(()=>_hazirlaniyor=false);
    }
  }

  Future<void> _muzikEkle()async{
    if(!widget.yonetici||widget.bitti||_yukleniyor)return;
    final arama=TextEditingController();
    var kategori='Tümü';
    NgelxYerlesikMuzik? secilen;
    if(!mounted)return;
    secilen=await showModalBottomSheet<NgelxYerlesikMuzik>(
      context:context,
      backgroundColor:Colors.white,
      isScrollControlled:true,
      showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
      builder:(sheet)=>StatefulBuilder(builder:(sheet,setSheet){
        final q=arama.text.trim().toLowerCase();
        final liste=ngelxYerlesikMuzikler.where((x)=>(kategori=='Tümü'||x.kategori==kategori)&&(q.isEmpty||x.baslik.toLowerCase().contains(q)||x.kategori.toLowerCase().contains(q))).toList();
        return SafeArea(top:false,child:Padding(
          padding:EdgeInsets.fromLTRB(16,4,16,18+MediaQuery.viewInsetsOf(sheet).bottom),
          child:SizedBox(
            height:math.min(MediaQuery.sizeOf(sheet).height*.76,620.0).toDouble(),
            child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
              const Row(children:[
                CircleAvatar(backgroundColor:Color(0xFFF0E8FF),child:Icon(Icons.library_music_rounded,color:mor)),
                SizedBox(width:10),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text('NgelX Müzik Kütüphanesi',style:TextStyle(fontSize:20,fontWeight:FontWeight.w900)),
                  Text('NgelX için üretilmiş orijinal döngüler',style:TextStyle(color:Colors.black54,fontSize:12)),
                ])),
              ]),
              const SizedBox(height:12),
              Container(
                padding:const EdgeInsets.symmetric(horizontal:11,vertical:9),
                decoration:BoxDecoration(color:const Color(0xFFF7F2FF),borderRadius:BorderRadius.circular(14)),
                child:const Row(children:[
                  Icon(Icons.verified_rounded,color:mor,size:18),
                  SizedBox(width:7),
                  Expanded(child:Text('Telefon dosyaları açılmaz. Harici telifli parça yüklenmez.',style:TextStyle(color:Colors.black54,fontSize:11.5,fontWeight:FontWeight.w700))),
                ]),
              ),
              const SizedBox(height:10),
              TextField(
                controller:arama,
                onChanged:(_)=>setSheet((){}),
                decoration:InputDecoration(
                  hintText:'Müzik ara',
                  prefixIcon:const Icon(Icons.search_rounded),
                  filled:true,
                  fillColor:const Color(0xFFF6F6F8),
                  border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none),
                ),
              ),
              const SizedBox(height:9),
              SizedBox(height:38,child:ListView(
                scrollDirection:Axis.horizontal,
                children:['Tümü','Chill','Ambient','Odak','Sohbet'].map((x)=>Padding(
                  padding:const EdgeInsets.only(right:7),
                  child:ChoiceChip(label:Text(x),selected:kategori==x,onSelected:(_)=>setSheet(()=>kategori=x)),
                )).toList(),
              )),
              const SizedBox(height:8),
              Expanded(child:liste.isEmpty
                ?const Center(child:Text('Eşleşen müzik yok.',style:TextStyle(color:Colors.black45)))
                :ListView.separated(
                  itemCount:liste.length,
                  separatorBuilder:(_,__)=>const Divider(height:1),
                  itemBuilder:(_,i){
                    final x=liste[i];
                    final aktif=_url=='ngelx://original/${x.id}';
                    return ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:4,vertical:4),
                      leading:CircleAvatar(backgroundColor:aktif?mor:const Color(0xFFF0E8FF),child:Icon(x.ikon,color:aktif?Colors.white:mor)),
                      title:Text(x.baslik,style:const TextStyle(fontWeight:FontWeight.w900)),
                      subtitle:Text('${x.kategori} • ${x.aciklama}',maxLines:2,overflow:TextOverflow.ellipsis),
                      trailing:FilledButton.tonalIcon(
                        onPressed:()=>Navigator.pop(sheet,x),
                        icon:Icon(aktif?Icons.replay_rounded:Icons.play_arrow_rounded,size:18),
                        label:Text(aktif?'Yeniden':'Seç'),
                      ),
                    );
                  },
                ),
              ),
            ]),
          ),
        ));
      }),
    );
    arama.dispose();
    if(secilen==null||!mounted)return;
    setState(()=>_yukleniyor=true);
    try{
      final path=await ngelxYerlesikMuzikDosyasi(secilen.id);
      int sureMs=12000;
      try{
        final p=AudioPlayer();
        final sure=await p.setFilePath(path);
        sureMs=sure?.inMilliseconds??12000;
        await p.dispose();
      }catch(_){}
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).set({
        'musicUrl':'ngelx://original/${secilen.id}',
        'musicTitle':secilen.baslik,
        'musicPlaying':true,
        'musicPositionMs':0,
        'musicStartedAt':FieldValue.serverTimestamp(),
        'musicDurationMs':sureMs,
        'musicAddedBy':FirebaseAuth.instance.currentUser?.uid??'',
        'musicUpdatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('${secilen.baslik} odaya eklendi.')));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Müzik hazırlanamadı: ${_ngelxKisaHata(e)}')));
    }finally{
      if(mounted)setState(()=>_yukleniyor=false);
    }
  }

  Future<void> _oynatDuraklat()async{
    if(!widget.yonetici||_url.isEmpty||widget.bitti)return;
    final ref=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId);
    try{
      if(_oynuyor){
        final pos=_oynatici.position.inMilliseconds;
        await ref.set({
          'musicPlaying':false,
          'musicPositionMs':pos,
          'musicStartedAt':null,
          'musicUpdatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true));
      }else{
        final pos=_oynatici.position.inMilliseconds;
        await ref.set({
          'musicPlaying':true,
          'musicPositionMs':pos,
          'musicStartedAt':FieldValue.serverTimestamp(),
          'musicUpdatedAt':FieldValue.serverTimestamp(),
        },SetOptions(merge:true));
      }
    }catch(_){}
  }

  Future<void> _muzigiKapat()async{
    if(!widget.yonetici||widget.bitti)return;
    try{
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).set({
        'musicUrl':'',
        'musicTitle':'',
        'musicPlaying':false,
        'musicPositionMs':0,
        'musicStartedAt':null,
        'musicDurationMs':0,
        'musicAddedBy':'',
        'musicUpdatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));
    }catch(_){}
  }

  Future<void> _panelAc()async{
    if(!mounted)return;
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      isScrollControlled:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(24))),
      builder:(c)=>StatefulBuilder(builder:(c,setSheet){
        return SafeArea(top:false,child:Padding(
          padding:const EdgeInsets.fromLTRB(18,4,18,20),
          child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
            Row(children:[
              const CircleAvatar(backgroundColor:Color(0xFFF0E8FF),child:Icon(Icons.music_note_rounded,color:mor)),
              const SizedBox(width:10),
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                const Text('Oda müziği',style:TextStyle(color:Colors.black87,fontSize:19,fontWeight:FontWeight.w900)),
                Text(_baslik.isEmpty?'Henüz müzik seçilmedi':(_baslik+' • NgelX Original'),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)),
              ])),
            ]),
            const SizedBox(height:14),
            Row(children:[
              const Icon(Icons.volume_down_rounded,color:Colors.black54),
              Expanded(child:Slider(
                value:_ses,
                min:0,max:1,
                onChanged:(v){setSheet(()=>_ses=v);if(mounted)setState(()=>_ses=v);unawaited(_oynatici.setVolume(v));},
              )),
              Text('${(_ses*100).round()}%',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)),
            ]),
            if(widget.yonetici&&!widget.bitti)...[
              const SizedBox(height:8),
              Row(children:[
                Expanded(child:FilledButton.icon(
                  style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(46)),
                  onPressed:_yukleniyor?null:()async{Navigator.pop(c);await _muzikEkle();},
                  icon:_yukleniyor?const SizedBox(width:17,height:17,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.library_music_rounded),
                  label:Text(_url.isEmpty?'Kütüphaneyi aç':'Müziği değiştir',style:const TextStyle(fontWeight:FontWeight.w900)),
                )),
                if(_url.isNotEmpty)...[
                  const SizedBox(width:8),
                  IconButton.filledTonal(
                    tooltip:_oynuyor?'Duraklat':'Oynat',
                    onPressed:()async{await _oynatDuraklat();if(c.mounted)Navigator.pop(c);},
                    icon:Icon(_oynuyor?Icons.pause_rounded:Icons.play_arrow_rounded),
                  ),
                  const SizedBox(width:6),
                  IconButton.filledTonal(
                    tooltip:'Müziği kapat',
                    style:IconButton.styleFrom(foregroundColor:Colors.red),
                    onPressed:()async{await _muzigiKapat();if(c.mounted)Navigator.pop(c);},
                    icon:const Icon(Icons.stop_circle_outlined),
                  ),
                ],
              ]),
            ],
            if(!widget.yonetici&&_url.isEmpty)
              const Padding(padding:EdgeInsets.only(top:8),child:Text('ADMIN veya yönetici NgelX kütüphanesinden müzik seçtiğinde burada dinleyebilirsin.',style:TextStyle(color:Colors.black45))),
          ]),
        ));
      }),
    );
  }

  @override void didUpdateWidget(covariant NgelxSesliMuzikKontrolu oldWidget){
    super.didUpdateWidget(oldWidget);
    if(widget.bitti&&!oldWidget.bitti){
      _oynuyor=false;
      unawaited(_oynatici.stop());
    }
  }

  @override Widget build(BuildContext context){
    final varMi=_url.isNotEmpty;
    return OutlinedButton.icon(
      onPressed:_panelAc,
      icon:Icon(varMi&&_oynuyor?Icons.music_note_rounded:Icons.music_off_rounded,size:18,color:varMi?mor:Colors.black45),
      label:ConstrainedBox(
        constraints:const BoxConstraints(maxWidth:120),
        child:Text(
          _hazirlaniyor?'Müzik hazırlanıyor':varMi?(_oynuyor?_baslik:'Müzik duraklatıldı'):'Müzik',
          maxLines:1,
          overflow:TextOverflow.ellipsis,
        ),
      ),
    );
  }

  @override void dispose(){
    _odaAboneligi?.cancel();
    unawaited(_oynatici.stop());
    unawaited(_oynatici.dispose());
    super.dispose();
  }
}
