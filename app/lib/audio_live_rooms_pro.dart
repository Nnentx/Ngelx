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

Future<void> ngelxSesliRolDegistir({
  required BuildContext context,
  required String roomId,
  required String hedefUid,
  required String islem,
})async{
  final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||hedefUid.isEmpty)return;
  final ref=FirebaseFirestore.instance.collection('audio_rooms').doc(roomId);
  final pref=ref.collection('participants').doc(hedefUid);
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final d=await tx.get(ref),v=d.data()??<String,dynamic>{};
      if((v['ownerId']??'').toString()!=ben)throw StateError('owner_only');
      final sp=List<String>.from(v['speakerIds']??const[]),mods=List<String>.from(v['moderatorIds']??const[]);
      if(islem=='speaker'){
        if(!sp.contains(hedefUid)&&sp.length>=ngelxSesliMaksKonusmaci)throw StateError('speaker_limit');
        if(!sp.contains(hedefUid))sp.add(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':mods.contains(hedefUid)?'moderator':'speaker','removed':false,'active':true,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='listener'){
        sp.remove(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':mods.contains(hedefUid)?'moderator':'listener','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='moderator'){
        if(!mods.contains(hedefUid)&&mods.length>=ngelxSesliMaksModerator)throw StateError('moderator_limit');
        if(!mods.contains(hedefUid))mods.add(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':'moderator','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='unmoderator'){
        mods.remove(hedefUid);
        tx.update(ref,{'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':sp.contains(hedefUid)?'speaker':'listener','updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }else if(islem=='remove'){
        sp.remove(hedefUid);mods.remove(hedefUid);
        tx.update(ref,{'speakerIds':sp,'speakerCount':sp.length,'moderatorIds':mods,'updatedAt':FieldValue.serverTimestamp()});
        tx.set(pref,{'role':'removed','active':false,'removed':true,'removedAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }
    });
  }catch(e){
    if(context.mounted){
      final m=e.toString().contains('speaker_limit')?'Konuşmacı sınırı dolu.':e.toString().contains('moderator_limit')?'Moderatör sınırı dolu.':'İşlem tamamlanamadı.';
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
                    trailing:ben==ownerId&&!sahip?PopupMenuButton<String>(
                      tooltip:'Yönet',
                      onSelected:(x)=>ngelxSesliRolDegistir(context:c,roomId:roomId,hedefUid:id,islem:x),
                      itemBuilder:(_)=>[
                        if(rol!='speaker'&&rol!='moderator')const PopupMenuItem(value:'speaker',child:Text('Konuşmacı yap')),
                        if(rol=='speaker'||rol=='moderator')const PopupMenuItem(value:'listener',child:Text('Sahneden indir')),
                        if(rol!='moderator')const PopupMenuItem(value:'moderator',child:Text('Moderatör yap')),
                        if(rol=='moderator')const PopupMenuItem(value:'unmoderator',child:Text('Moderatörlüğü kaldır')),
                        const PopupMenuDivider(),
                        const PopupMenuItem(value:'remove',child:Text('Odadan çıkar',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800))),
                      ],
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
  final bool yonetici;
  const NgelxSesliSohbetPanel({super.key,required this.roomId,required this.yonetici});
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
    final u=FirebaseAuth.instance.currentUser,t=_mesaj.text.trim();
    if(u==null||t.isEmpty||_gonderiyor)return;
    setState(()=>_gonderiyor=true);
    _mesaj.clear();
    try{
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('messages').add({
        'userId':u.uid,'displayName':_ad,'photoUrl':_foto,'text':t.length>600?t.substring(0,600):t,'createdAt':FieldValue.serverTimestamp(),'pinned':false,
      });
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gönderilemedi.')));
    }finally{if(mounted)setState(()=>_gonderiyor=false);}
  }
  Future<void> _mesajIslem(DocumentReference<Map<String,dynamic>> ref,Map<String,dynamic> v)async{
    final ben=FirebaseAuth.instance.currentUser?.uid,benim=(v['userId']??'').toString()==ben;
    final sec=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      if(widget.yonetici)ListTile(leading:const Icon(Icons.push_pin_outlined,color:mor),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle'),onTap:()=>Navigator.pop(c,'pin')),
      if(widget.yonetici||benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.redAccent),title:const Text('Mesajı sil',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w800)),onTap:()=>Navigator.pop(c,'delete')),
    ])));
    if(sec=='delete')await ref.delete();
    if(sec=='pin')await ref.set({'pinned':v['pinned']!=true,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
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
                minLines:1,maxLines:4,
                style:const TextStyle(color:Colors.black87),
                decoration:InputDecoration(hintText:'Mesaj yaz...',hintStyle:const TextStyle(color:Colors.black38),filled:true,fillColor:const Color(0xFFF5F5F8),contentPadding:const EdgeInsets.symmetric(horizontal:14,vertical:10),border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none)),
                onSubmitted:(_)=>_gonder(),
              )),
              const SizedBox(width:7),
              IconButton.filled(style:IconButton.styleFrom(backgroundColor:mor),onPressed:_gonderiyor?null:_gonder,icon:_gonderiyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded,color:Colors.white)),
            ]),
          ),
        ]),
      ),
    );
  }
  @override void dispose(){_mesaj.dispose();super.dispose();}
}

Future<void> ngelxSesliSohbetAc(BuildContext context,String roomId,bool yonetici)async{
  await showModalBottomSheet<void>(
    context:context,
    backgroundColor:Colors.white,
    isScrollControlled:true,
    useSafeArea:true,
    shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
    builder:(c)=>FractionallySizedBox(heightFactor:.78,child:NgelxSesliSohbetPanel(roomId:roomId,yonetici:yonetici)),
  );
}


class NgelxSesliInlineSohbet extends StatefulWidget{
  final String roomId;
  final bool yonetici;
  const NgelxSesliInlineSohbet({super.key,required this.roomId,required this.yonetici});
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
    final u=FirebaseAuth.instance.currentUser,t=_mesaj.text.trim();
    if(u==null||t.isEmpty||_gonderiyor)return;
    setState(()=>_gonderiyor=true);
    _mesaj.clear();
    try{
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.roomId).collection('messages').add({
        'userId':u.uid,
        'displayName':_ad,
        'photoUrl':_foto,
        'text':t.length>600?t.substring(0,600):t,
        'createdAt':FieldValue.serverTimestamp(),
        'pinned':false,
      });
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gönderilemedi.')));
    }finally{if(mounted)setState(()=>_gonderiyor=false);}
  }
  Widget _satir(Map<String,dynamic> v){
    final ad=(v['displayName']??'NgelX').toString(),metin=(v['text']??'').toString();
    return Padding(
      padding:const EdgeInsets.symmetric(vertical:1),
      child:Row(children:[
        Flexible(child:Text(ad,overflow:TextOverflow.ellipsis,style:const TextStyle(color:mor,fontSize:11,fontWeight:FontWeight.w900))),
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
              onPressed:()=>ngelxSesliSohbetAc(context,widget.roomId,widget.yonetici),
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
            if(docs.isEmpty)return const Center(child:Text('Henüz mesaj yok • Yazışma ses açıkken burada görünür.',style:TextStyle(color:Colors.black38,fontSize:11.5,fontWeight:FontWeight.w600)));
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
            minLines:1,maxLines:1,
            textInputAction:TextInputAction.send,
            style:const TextStyle(color:Colors.black87,fontSize:13.5),
            decoration:InputDecoration(
              hintText:'Mesaj yaz...',
              hintStyle:const TextStyle(color:Colors.black38),
              filled:true,
              fillColor:const Color(0xFFF5F5F8),
              isDense:true,
              contentPadding:const EdgeInsets.symmetric(horizontal:13,vertical:10),
              border:OutlineInputBorder(borderRadius:BorderRadius.circular(20),borderSide:BorderSide.none),
            ),
            onSubmitted:(_)=>_gonder(),
          )),
          const SizedBox(width:6),
          IconButton.filled(
            style:IconButton.styleFrom(backgroundColor:mor,minimumSize:const Size(40,40)),
            onPressed:_gonderiyor?null:_gonder,
            icon:_gonderiyor?const SizedBox(width:17,height:17,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded,color:Colors.white,size:19),
          ),
        ]),
      ),
    ]),
  );
  @override void dispose(){_mesaj.dispose();super.dispose();}
}
