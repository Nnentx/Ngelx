part of 'main.dart';

class NgelxSesliMiniDurum{
  final String roomId;
  final String baslik;
  final DateTime? baslangic;
  final bool sahibiyim;
  const NgelxSesliMiniDurum({
    required this.roomId,
    required this.baslik,
    required this.baslangic,
    required this.sahibiyim,
  });
}

final ValueNotifier<NgelxSesliMiniDurum?> ngelxSesliMiniDurum=ValueNotifier<NgelxSesliMiniDurum?>(null);

void ngelxSesliMiniTemizle(String roomId){
  final d=ngelxSesliMiniDurum.value;
  if(d!=null&&d.roomId==roomId)ngelxSesliMiniDurum.value=null;
}

class NgelxSesliMiniGlobalOverlay extends StatelessWidget{
  const NgelxSesliMiniGlobalOverlay({super.key});

  void _odayaDon(NgelxSesliMiniDurum d){
    ngelxSesliMiniDurum.value=null;
    WidgetsBinding.instance.addPostFrameCallback((_){
      ngelxNavigatorKey.currentState?.popUntil((r)=>r.settings.name=='/audio_room/${d.roomId}');
    });
  }

  @override Widget build(BuildContext context)=>ValueListenableBuilder<NgelxSesliMiniDurum?>(
    valueListenable:ngelxSesliMiniDurum,
    builder:(_,d,__){
      if(d==null)return const SizedBox.shrink();
      return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('audio_rooms').doc(d.roomId).snapshots(),
        builder:(_,s){
          final v=s.data?.data();
          if(v!=null&&v['active']!=true){
            WidgetsBinding.instance.addPostFrameCallback((_){ngelxSesliMiniTemizle(d.roomId);});
            return const SizedBox.shrink();
          }
          final bas=v?['startedAt'];
          final baslangic=bas is Timestamp?bas.toDate():d.baslangic;
          final baslik=(v?['title']??d.baslik).toString();
          return Positioned(
            top:0,left:0,right:0,
            child:SafeArea(
              bottom:false,
              child:Material(
                color:Colors.transparent,
                child:InkWell(
                  onTap:()=>_odayaDon(d),
                  child:Container(
                    margin:const EdgeInsets.fromLTRB(10,7,10,0),
                    padding:const EdgeInsets.fromLTRB(12,9,10,9),
                    decoration:BoxDecoration(
                      color:const Color(0xFF211837),
                      borderRadius:BorderRadius.circular(20),
                      border:Border.all(color:const Color(0xFF5B447E)),
                      boxShadow:const [BoxShadow(color:Color(0x44000000),blurRadius:18,offset:Offset(0,7))],
                    ),
                    child:Row(children:[
                      const CircleAvatar(
                        radius:20,
                        backgroundColor:mor,
                        child:Icon(Icons.graphic_eq_rounded,color:Colors.white,size:21),
                      ),
                      const SizedBox(width:9),
                      Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
                        Text(baslik,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:13.5,fontWeight:FontWeight.w900)),
                        const SizedBox(height:2),
                        Text(d.sahibiyim?'Sesli oda devam ediyor • Sahipsin':'Sesli oda devam ediyor',style:const TextStyle(color:Color(0xFFC9BDD8),fontSize:10.5,fontWeight:FontWeight.w700)),
                      ])),
                      if(baslangic!=null)NgelxSesliSureSayaci(baslangic:baslangic),
                      const SizedBox(width:7),
                      const Icon(Icons.open_in_full_rounded,color:Colors.white,size:20),
                    ]),
                  ),
                ),
              ),
            ),
          );
        },
      );
    },
  );
}

Future<void> ngelxSesliOdaBaslangicBildirimi({
  required String roomId,
  required String baslik,
})async{
  final u=FirebaseAuth.instance.currentUser;if(u==null||roomId.isEmpty)return;
  try{
    final p=(await FirebaseFirestore.instance.collection('users').doc(u.uid).get()).data()??<String,dynamic>{};
    final arkadaslar=Set<String>.from(List<String>.from(p['friends']??const[]));
    final takipciler=Set<String>.from(List<String>.from(p['followers']??const[]));
    final takipEdilen=Set<String>.from(List<String>.from(p['following']??const[]));
    final karsilikli=takipciler.intersection(takipEdilen);
    final hedefler=<String>{...arkadaslar,...karsilikli}..remove(u.uid);
    var sayac=0;
    for(final hedef in hedefler){
      if(sayac>=150)break;
      sayac++;
      unawaited(
        uygulamaBildirimiGonder(
          toUid:hedef,
          fromUid:u.uid,
          tur:'audio_live',
          metin:'sesli oda başlattı: $baslik',
          belgeId:roomId,
          hedefTuru:'audio_room',
          hedefBaslik:baslik,
          olayTuru:'audio_room_started',
          dedupeKey:'audio_room_started_${roomId}_$hedef',
        ).catchError((_){ }),
      );
    }
  }catch(_){}
}

Future<Map<String,String>> _ngelxSesliPaylasChatEtiketi(Map<String,dynamic> v,String uid)async{
  final members=List<String>.from(v['members']??const[]);
  final grup=v['isGroup']==true||members.length>2;
  if(grup){
    return {
      'ad':(v['groupName']??'Grup').toString(),
      'foto':(v['groupPhotoUrl']??'').toString(),
      'tur':'group',
    };
  }
  final diger=members.firstWhere((x)=>x!=uid,orElse:()=>'');
  if(diger.isEmpty)return {'ad':'Özel sohbet','foto':'','tur':'private'};
  try{
    final p=(await FirebaseFirestore.instance.collection('users').doc(diger).get()).data()??<String,dynamic>{};
    return {
      'ad':(p['displayName']??p['username']??'NgelX kullanıcısı').toString(),
      'foto':(p['photoUrl']??'').toString(),
      'tur':'private',
    };
  }catch(_){
    return {'ad':'Özel sohbet','foto':'','tur':'private'};
  }
}

Future<void> _ngelxSesliPaylasGonder({
  required QueryDocumentSnapshot<Map<String,dynamic>> chat,
  required String uid,
  required String roomId,
  required String baslik,
})async{
  final v=chat.data(),members=List<String>.from(v['members']??const[]);
  if(!members.contains(uid))return;
  final grup=v['isGroup']==true||members.length>2;
  final ref=chat.reference;
  final mesajRef=ref.collection('messages').doc();
  final batch=FirebaseFirestore.instance.batch();
  batch.set(mesajRef,{
    'senderId':uid,
    'type':'audio_room_share',
    'audioRoomId':roomId,
    'audioRoomTitle':baslik,
    'text':'🔊 $baslik • Sesli odaya katıl',
    'createdAt':FieldValue.serverTimestamp(),
    'clientCreatedAt':Timestamp.now(),
  });
  final g=<String,dynamic>{
    'lastMessage':'🔊 Sesli oda: $baslik',
    'updatedAt':FieldValue.serverTimestamp(),
    'hiddenFor':FieldValue.arrayRemove(members),
  };
  for(final x in members){if(x!=uid)g['unread_$x']=FieldValue.increment(1);}
  batch.set(ref,g,SetOptions(merge:true));
  await batch.commit();

  for(final hedef in members){
    if(hedef==uid)continue;
    unawaited(uygulamaBildirimiGonder(
      toUid:hedef,
      fromUid:uid,
      tur:'message',
      metin:grup?'gruba bir sesli oda daveti gönderdi':'sana bir sesli oda daveti gönderdi',
      belgeId:ref.id,
      hedefTuru:grup?'group':null,
      hedefBaslik:grup?(v['groupName']??'Grup').toString():null,
      hedefFoto:grup?(v['groupPhotoUrl']??'').toString():null,
      olayTuru:grup?'group_message':null,
      onizleme:'🔊 $baslik',
      eylem:'sesli oda daveti gönderdi',
      dedupeKey:'audio_room_share_${roomId}_${ref.id}_$hedef',
    ).catchError((_){ }));
  }
}

Future<void> ngelxSesliNgelxIcindePaylas(BuildContext context,String roomId,String baslik)async{
  final u=FirebaseAuth.instance.currentUser;if(u==null||roomId.isEmpty)return;
  QuerySnapshot<Map<String,dynamic>> snap;
  try{
    snap=await FirebaseFirestore.instance.collection('chats').where('members',arrayContains:u.uid).limit(80).get().timeout(const Duration(seconds:10));
  }catch(_){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sohbetler yüklenemedi.')));
    return;
  }
  if(!context.mounted)return;
  final docs=snap.docs.where((d){
    final v=d.data();
    return v['groupDeleted']!=true&&!List<String>.from(v['hiddenFor']??const[]).contains(u.uid);
  }).toList();
  if(docs.isEmpty){
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Paylaşabileceğin bir NgelX sohbeti bulunamadı.')));
    return;
  }

  final secilen=<String>{};
  bool gonderiliyor=false;
  await showModalBottomSheet<void>(
    context:context,
    isScrollControlled:true,
    backgroundColor:Colors.white,
    showDragHandle:true,
    shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
    builder:(sheet)=>StatefulBuilder(builder:(sheet,setSheet)=>SafeArea(
      top:false,
      child:SizedBox(
        height:MediaQuery.sizeOf(sheet).height*.72,
        child:Column(children:[
          Padding(
            padding:const EdgeInsets.fromLTRB(18,0,12,8),
            child:Row(children:[
              const CircleAvatar(backgroundColor:Color(0xFFF0E8FF),child:Icon(Icons.send_rounded,color:mor)),
              const SizedBox(width:10),
              const Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Text('NgelX içinde paylaş',style:TextStyle(color:Colors.black87,fontSize:19,fontWeight:FontWeight.w900)),
                Text('Özel sohbet veya grup seç',style:TextStyle(color:Colors.black45,fontSize:11.5,fontWeight:FontWeight.w600)),
              ])),
              IconButton(onPressed:gonderiliyor?null:()=>Navigator.pop(sheet),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
            ]),
          ),
          const Divider(height:1),
          Expanded(child:ListView.separated(
            padding:const EdgeInsets.symmetric(vertical:6),
            itemCount:docs.length,
            separatorBuilder:(_,__)=>const Divider(height:1,indent:70),
            itemBuilder:(_,i){
              final d=docs[i],secili=secilen.contains(d.id);
              return FutureBuilder<Map<String,String>>(
                future:_ngelxSesliPaylasChatEtiketi(d.data(),u.uid),
                builder:(_,s){
                  final x=s.data??{'ad':'NgelX sohbeti','foto':'','tur':'private'},foto=x['foto']??'',grup=x['tur']=='group';
                  return ListTile(
                    onTap:gonderiliyor?null:()=>setSheet(()=>secili?secilen.remove(d.id):secilen.add(d.id)),
                    leading:CircleAvatar(
                      backgroundColor:grup?ngelxGroupGreenSoft:const Color(0xFFF0E8FF),
                      backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),
                      child:foto.isEmpty?Icon(grup?Icons.groups_rounded:Icons.person_rounded,color:grup?ngelxGroupGreen:mor):null,
                    ),
                    title:Text(x['ad']??'NgelX sohbeti',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                    subtitle:Text(grup?'Grup':'Özel sohbet',style:const TextStyle(color:Colors.black45,fontSize:11)),
                    trailing:Checkbox(value:secili,onChanged:gonderiliyor?null:(v)=>setSheet(()=>v==true?secilen.add(d.id):secilen.remove(d.id)),activeColor:mor),
                  );
                },
              );
            },
          )),
          Padding(
            padding:const EdgeInsets.fromLTRB(14,8,14,12),
            child:FilledButton.icon(
              style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(50)),
              onPressed:gonderiliyor||secilen.isEmpty?null:()async{
                setSheet(()=>gonderiliyor=true);
                var basarili=0;
                for(final id in secilen.toList()){
                  final d=docs.firstWhere((x)=>x.id==id);
                  try{await _ngelxSesliPaylasGonder(chat:d,uid:u.uid,roomId:roomId,baslik:baslik);basarili++;}catch(_){}
                }
                if(sheet.mounted)Navigator.pop(sheet);
                if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('$basarili sohbete gönderildi.')));
              },
              icon:gonderiliyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded),
              label:Text(secilen.isEmpty?'Sohbet seç':'${secilen.length} sohbete gönder',style:const TextStyle(fontWeight:FontWeight.w900)),
            ),
          ),
        ]),
      ),
    )),
  );
}

Future<void> ngelxSesliPaylasimMesajiniAc(BuildContext context,Map<String,dynamic> v)async{
  final roomId=(v['audioRoomId']??'').toString();
  if(roomId.isEmpty)return;
  try{
    final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(roomId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
    final oda=d.data()??<String,dynamic>{};
    if(!d.exists||!ngelxSesliOdaTaze(oda)){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu sesli oda sona erdi.')));
      return;
    }
    if(context.mounted)await ngelxSesliOdayaKatil(context,roomId);
  }catch(_){
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli oda açılamadı.')));
  }
}
