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
  final metin="NgelX'te \"$baslik\" sesli odasına katıl.\nOda kodu: $roomId";
  try{
    await SharePlus.instance.share(ShareParams(text:metin,subject:'NgelX Sesli Oda'));
  }catch(_){
    await Clipboard.setData(ClipboardData(text:metin));
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Davet metni panoya kopyalandı.')));
  }
}

String ngelxSesliMesajRolEtiketi(String rol){
  if(rol=='owner')return 'SAHİP';
  if(rol=='moderator')return 'MOD';
  if(rol=='speaker')return 'KONUŞMACI';
  return '';
}

Widget ngelxSesliMesajRolRozeti(String rol){
  final yazi=ngelxSesliMesajRolEtiketi(rol);
  if(yazi.isEmpty)return const SizedBox.shrink();
  final sahip=rol=='owner';
  return Container(
    margin:const EdgeInsets.only(left:5),
    padding:const EdgeInsets.symmetric(horizontal:6,vertical:2),
    decoration:BoxDecoration(color:sahip?mor:const Color(0xFFEDE7F8),borderRadius:BorderRadius.circular(8)),
    child:Text(yazi,style:TextStyle(color:sahip?Colors.white:mor,fontSize:8.5,fontWeight:FontWeight.w900)),
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
})async{
  final u=FirebaseAuth.instance.currentUser,t=text.trim();
  if(u==null||t.isEmpty)return null;
  try{
    final odaRef=FirebaseFirestore.instance.collection('audio_rooms').doc(roomId);
    final oda=(await odaRef.get()).data()??<String,dynamic>{};
    if(oda['active']!=true)return 'Bu sesli oda sona erdi.';
    final susturulan=List<String>.from(oda['chatMutedUserIds']??const[]);
    if(susturulan.contains(u.uid))return 'Oda sahibi seni sohbetten susturdu.';
    final owner=(oda['ownerId']??'').toString();
    final mods=List<String>.from(oda['moderatorIds']??const[]);
    final sp=List<String>.from(oda['speakerIds']??const[]);
    final rol=u.uid==owner?'owner':mods.contains(u.uid)?'moderator':sp.contains(u.uid)?'speaker':'listener';
    final temiz=t.length>600?t.substring(0,600):t;
    final bucket=DateTime.now().millisecondsSinceEpoch~/3000;
    final mesajId='${u.uid}_${bucket}_${ngelxSesliMesajHash(temiz)}';
    await odaRef.collection('messages').doc(mesajId).set({
      'userId':u.uid,
      'displayName':ad,
      'photoUrl':foto,
      'text':temiz,
      'authorRole':rol,
      'createdAt':FieldValue.serverTimestamp(),
      'pinned':false,
      'clientDedupeKey':mesajId,
    });
    return null;
  }catch(_){
    return 'Mesaj gönderilemedi.';
  }
}

Future<void> ngelxSesliKullaniciMenuAc(BuildContext context,String roomId,String hedefUid,String ad)async{
  final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null)return;
  final oda=(await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).get()).data()??<String,dynamic>{};
  if((oda['ownerId']??'').toString()!=ben){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu işlemleri yalnızca oda sahibi yapabilir.')));
    return;
  }
  final mods=List<String>.from(oda['moderatorIds']??const[]);
  final speakers=List<String>.from(oda['speakerIds']??const[]);
  final susturulan=List<String>.from(oda['chatMutedUserIds']??const[]);
  final mod=mods.contains(hedefUid),speaker=speakers.contains(hedefUid),chatMuted=susturulan.contains(hedefUid);
  if(!context.mounted)return;
  final sec=await showModalBottomSheet<String>(
    context:context,
    backgroundColor:Colors.white,
    showDragHandle:true,
    builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Padding(padding:const EdgeInsets.fromLTRB(18,0,18,8),child:Row(children:[const Icon(Icons.admin_panel_settings_rounded,color:mor),const SizedBox(width:8),Expanded(child:Text(ad,style:const TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900)))])),
      if(!speaker)ListTile(leading:const Icon(Icons.mic_rounded,color:mor),title:const Text('Konuşmacı yap'),onTap:()=>Navigator.pop(c,'speaker')),
      if(speaker)ListTile(leading:const Icon(Icons.mic_off_rounded,color:Colors.orange),title:const Text('Mikrofonunu kapat / dinleyici yap'),onTap:()=>Navigator.pop(c,'mute')),
      if(!mod)ListTile(leading:const Icon(Icons.shield_outlined,color:mor),title:const Text('Moderatör yap'),onTap:()=>Navigator.pop(c,'moderator')),
      if(mod)ListTile(leading:const Icon(Icons.shield_outlined,color:Colors.orange),title:const Text('Moderatörlüğü kaldır'),onTap:()=>Navigator.pop(c,'unmoderator')),
      ListTile(leading:Icon(chatMuted?Icons.chat_bubble_outline:Icons.comments_disabled_outlined,color:Colors.orange),title:Text(chatMuted?'Sohbet susturmasını kaldır':'Sohbetten sustur'),onTap:()=>Navigator.pop(c,'chatmute')),
      const Divider(height:1),
      ListTile(leading:const Icon(Icons.person_remove_alt_1_rounded,color:Colors.redAccent),title:const Text('Odadan çıkar',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'remove')),
      ListTile(leading:const Icon(Icons.block_rounded,color:Colors.red),title:const Text('Odadan çıkar ve tekrar girişini engelle',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w900)),onTap:()=>Navigator.pop(c,'ban')),
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
      if((v['ownerId']??'').toString()!=ben)throw StateError('owner_only');
      final sp=List<String>.from(v['speakerIds']??const[]);
      final mods=List<String>.from(v['moderatorIds']??const[]);
      final banned=List<String>.from(v['bannedUserIds']??const[]);
      final chatMuted=List<String>.from(v['chatMutedUserIds']??const[]);
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
        if(!mods.contains(hedefUid)&&mods.length>=ngelxSesliMaksModerator)throw StateError('moderator_limit');
        if(!mods.contains(hedefUid))mods.add(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':'moderator','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='unmoderator'){
        mods.remove(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':sp.contains(hedefUid)?'speaker':'listener','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='chatmute'){
        if(chatMuted.contains(hedefUid))chatMuted.remove(hedefUid);else chatMuted.add(hedefUid);
        tx.update(ref,{'chatMutedUserIds':chatMuted,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'chatMuted':chatMuted.contains(hedefUid),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='remove'||islem=='ban'){
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
      final m=e.toString().contains('speaker_limit')?'Konuşmacı sınırı dolu.':e.toString().contains('moderator_limit')?'Moderatör sınırı dolu.':e.toString().contains('owner_only')?'Bu işlemi yalnızca oda sahibi yapabilir.':'İşlem tamamlanamadı.';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(m)));
    }
  }
}
Future<void> ngelxSesliKatilimcilarAc(BuildContext context,String roomId,String ownerId)async{
  final ben=FirebaseAuth.instance.currentUser?.uid;
  if(ben==null)return;
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
                  final rolYazi=sahip?'Oda sahibi':rol=='moderator'?'Moderatör':rol=='speaker'?'Konuşmacı':'Dinleyici';
                  return ListTile(
                    leading:CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),
                    title:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
                    subtitle:Text(rolYazi,style:TextStyle(color:rol=='moderator'?mor:Colors.black45,fontWeight:FontWeight.w700)),
                    trailing:ben==ownerId&&!sahip?IconButton(
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
  @override void initState(){super.initState();unawaited(_profil());}
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
    if(mounted)setState(()=>_gonderiyor=false);
  }
  Future<void> _mesajIslem(DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> v)async{
    final ben=FirebaseAuth.instance.currentUser?.uid,benim=(v['userId']??'').toString()==ben;
    final sec=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      if(widget.yonetici)ListTile(leading:const Icon(Icons.push_pin_outlined,color:mor),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle'),onTap:()=>Navigator.pop(c,'pin')),
      if(widget.sahibiyim&&!benim)ListTile(leading:const Icon(Icons.admin_panel_settings_outlined,color:mor),title:const Text('Kullanıcıyı yönet'),onTap:()=>Navigator.pop(c,'manage')),
      if(widget.yonetici||benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.redAccent),title:const Text('Mesajı sil',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'delete')),
    ])));
    if(sec=='delete')await ref.delete();
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
                  final d=docs[i],v=d.data(),benim=(v['userId']??'').toString()==ben,pin=v['pinned']==true;
                  return Align(
                    alignment:benim?Alignment.centerRight:Alignment.centerLeft,
                    child:GestureDetector(
                      onLongPress:()=>_mesajIslem(d.reference,v),
                      child:Container(
                        constraints:BoxConstraints(maxWidth:MediaQuery.sizeOf(context).width*.78),
                        margin:const EdgeInsets.symmetric(vertical:4),
                        padding:const EdgeInsets.fromLTRB(12,8,12,9),
                        decoration:BoxDecoration(color:benim?const Color(0xFFF0E8FF):const Color(0xFFF4F4F6),borderRadius:BorderRadius.circular(16),border:pin?Border.all(color:mor):null),
                        child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                          Row(mainAxisSize:MainAxisSize.min,children:[
                            if(pin)...[const Icon(Icons.push_pin_rounded,size:13,color:mor),const SizedBox(width:3)],
                            Flexible(child:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black54,fontSize:10.5,fontWeight:FontWeight.w900))),
                            ngelxSesliMesajRolRozeti((v['authorRole']??'').toString()),
                          ]),
                          const SizedBox(height:2),
                          Text((v['text']??'').toString(),style:const TextStyle(color:Colors.black87,fontSize:14.5,height:1.3)),
                        ]),
                      ),
                    ),
                  );
                },
              );
            },
          )),
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
  @override void dispose(){_mesaj.dispose();super.dispose();}
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
  bool _gonderiyor=false;
  String _ad='NgelX',_foto='';
  @override void initState(){super.initState();unawaited(_profil());}
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
    if(mounted)setState(()=>_gonderiyor=false);
  }
  Widget _satir(Map<String,dynamic> v){
    final ad=(v['displayName']??'NgelX').toString(),metin=(v['text']??'').toString(),rol=(v['authorRole']??'').toString();
    return Padding(
      padding:const EdgeInsets.symmetric(vertical:1),
      child:Row(children:[
        Flexible(child:Text(ad,overflow:TextOverflow.ellipsis,style:const TextStyle(color:mor,fontSize:11,fontWeight:FontWeight.w900))),
        ngelxSesliMesajRolRozeti(rol),
        const SizedBox(width:5),
        Expanded(flex:3,child:Text(metin,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:12.5,fontWeight:FontWeight.w600))),
      ]),
    );
  }
  @override Widget build(BuildContext context)=>Container(
    height:150,
    decoration:const BoxDecoration(color:Colors.white,border:Border(top:BorderSide(color:Color(0xFFEDE8F2)))),
    child:Column(children:[
      SizedBox(
        height:34,
        child:Padding(
          padding:const EdgeInsets.symmetric(horizontal:12),
          child:Row(children:[
            const Icon(Icons.chat_bubble_rounded,color:mor,size:17),
            const SizedBox(width:6),
            const Text('Sohbet',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
            const Spacer(),
            TextButton.icon(
              style:TextButton.styleFrom(padding:const EdgeInsets.symmetric(horizontal:6),visualDensity:VisualDensity.compact),
              onPressed:()=>ngelxSesliSohbetAc(context,widget.roomId,widget.yonetici,sahibiyim:widget.sahibiyim,bitti:widget.bitti),
              icon:const Icon(Icons.open_in_full_rounded,size:15),
              label:const Text('Büyüt',style:TextStyle(fontSize:11,fontWeight:FontWeight.w800)),
            ),
          ]),
        ),
      ),
      Expanded(
        child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('messages').orderBy('createdAt',descending:true).limit(3).snapshots(),
          builder:(_,s){
            final docs=s.data?.docs??[];
            if(s.connectionState==ConnectionState.waiting&&docs.isEmpty)return const Center(child:SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:mor)));
            if(docs.isEmpty)return Center(child:Text(widget.bitti?'Bu oda sona erdi • Sohbet salt okunur.':'Henüz mesaj yok • Yazışma ses açıkken burada görünür.',style:const TextStyle(color:Colors.black38,fontSize:11.5,fontWeight:FontWeight.w600)));
            final gorunen=docs.take(2).toList().reversed.toList();
            return Padding(
              padding:const EdgeInsets.fromLTRB(12,1,12,2),
              child:Column(mainAxisAlignment:MainAxisAlignment.end,children:gorunen.map((d)=>_satir(d.data())).toList()),
            );
          },
        ),
      ),
      Padding(
        padding:const EdgeInsets.fromLTRB(10,4,10,7),
        child:Row(children:[
          Expanded(child:TextField(
            controller:_mesaj,
            enabled:!widget.bitti,
            minLines:1,maxLines:1,
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
            style:IconButton.styleFrom(backgroundColor:mor,minimumSize:const Size(40,40)),
            onPressed:_gonderiyor||widget.bitti?null:_gonder,
            icon:_gonderiyor?const SizedBox(width:17,height:17,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded,color:Colors.white,size:19),
          ),
        ]),
      ),
    ]),
  );
  @override void dispose(){_mesaj.dispose();super.dispose();}
}
