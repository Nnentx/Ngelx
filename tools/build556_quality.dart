part of 'main.dart';

// Build556: existing routes, collections, permission checks and purple identity.
class Ngelx556Section extends StatelessWidget {
  final String title, subtitle;
  final IconData icon;
  const Ngelx556Section({super.key,required this.title,required this.subtitle,required this.icon});
  @override Widget build(BuildContext context)=>Container(
    padding:const EdgeInsets.all(16),
    decoration:BoxDecoration(color:const Color(0xFFF7F3FF),borderRadius:BorderRadius.circular(20)),
    child:Row(children:[Icon(icon,color:mor,size:28),const SizedBox(width:12),
      Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(title,style:const TextStyle(fontSize:18,fontWeight:FontWeight.w800)),
        const SizedBox(height:4),Text(subtitle,style:const TextStyle(fontSize:13,color:Color(0xFF697386))),
      ])),
    ]),
  );
}
class Ngelx556MediaPreview extends StatelessWidget {
  final XFile? photo,cover;
  const Ngelx556MediaPreview({super.key,this.photo,this.cover});
  Widget picture(XFile file)=>kIsWeb?Image.network(file.path,fit:BoxFit.cover):Image.file(File(file.path),fit:BoxFit.cover,cacheWidth:1000);
  @override Widget build(BuildContext context)=>SizedBox(height:180,child:Stack(children:[
    Positioned.fill(bottom:24,child:ClipRRect(borderRadius:BorderRadius.circular(20),child:cover!=null?picture(cover!):Container(
      decoration:const BoxDecoration(gradient:LinearGradient(colors:[Color(0xFF35205C),Color(0xFF9564EE)])),
      child:const Center(child:Icon(Icons.landscape_outlined,color:Colors.white70,size:40)),
    ))),
    Positioned(left:20,bottom:0,child:Container(width:76,height:76,padding:const EdgeInsets.all(4),decoration:const BoxDecoration(color:Colors.white,shape:BoxShape.circle),
      child:ClipOval(child:photo!=null?picture(photo!):Container(color:const Color(0xFFF0E8FF),child:const Icon(Icons.groups_rounded,color:mor,size:34))))),
  ]));
}
class Ngelx556AdminMenu extends StatelessWidget {
  final DocumentReference<Map<String,dynamic>> root;
  final String selected;
  final ValueChanged<String> onSelected;
  const Ngelx556AdminMenu({super.key,required this.root,required this.selected,required this.onSelected});
  Widget row(String label,IconData icon,{String? collection,String? status}){
    Widget tile(String? count)=>Container(margin:const EdgeInsets.only(bottom:8),decoration:BoxDecoration(
      color:selected==label?const Color(0xFFF0E8FF):Colors.white,borderRadius:BorderRadius.circular(16),
      border:Border.all(color:selected==label?mor:const Color(0xFFE7E7ED))),
      child:ListTile(shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
        leading:Icon(icon,color:mor),title:Text(label,style:const TextStyle(fontWeight:FontWeight.w700)),
        trailing:Row(mainAxisSize:MainAxisSize.min,children:[if(count!=null)Padding(padding:const EdgeInsets.only(right:8),child:Text(count,style:const TextStyle(color:mor,fontWeight:FontWeight.w800))),const Icon(Icons.chevron_right_rounded)]),
        onTap:()=>onSelected(label)));
    if(collection==null)return tile(null);
    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:root.collection(collection).where('status',isEqualTo:status).limit(100).snapshots(),
      builder:(_,s)=>tile(s.hasError?'—':!s.hasData?'…':s.data!.size>=100?'99+':'${s.data!.size}'),
    );
  }
  @override Widget build(BuildContext context)=>Column(children:[
    row('Üyelik istekleri',Icons.person_add_alt_1_outlined,collection:'requests',status:'pending'),
    row('Bekleyen gönderiler',Icons.pending_actions_outlined,collection:'posts',status:'pending'),
    row('Şikâyetler',Icons.flag_outlined,collection:'reports',status:'open'),
    row('Üyeler',Icons.people_outline),row('İstatistikler',Icons.bar_chart_rounded),row('Ayarlar',Icons.settings_outlined),
  ]);
}
class Ngelx556InfoDialog extends StatefulWidget {
  final TextEditingController name,description,rules;
  const Ngelx556InfoDialog({super.key,required this.name,required this.description,required this.rules});
  @override State<Ngelx556InfoDialog> createState()=>_Ngelx556InfoDialogState();
}
class _Ngelx556InfoDialogState extends State<Ngelx556InfoDialog>{
  @override Widget build(BuildContext context)=>AlertDialog(
    backgroundColor:Colors.white,scrollable:true,title:const Text('Topluluk bilgileri'),
    content:SizedBox(width:420,child:Column(mainAxisSize:MainAxisSize.min,children:[
      TextField(controller:widget.name,onChanged:(_)=>setState((){}),maxLength:60,decoration:const InputDecoration(labelText:'Topluluk adı',prefixIcon:Icon(Icons.groups_outlined))),
      const SizedBox(height:12),TextField(controller:widget.description,maxLength:240,minLines:2,maxLines:4,decoration:const InputDecoration(labelText:'Açıklama')),
      const SizedBox(height:12),TextField(controller:widget.rules,maxLength:2000,minLines:3,maxLines:6,decoration:const InputDecoration(labelText:'Topluluk kuralları',hintText:'Saygılı ol, konuya uygun paylaşım yap…')),
    ])),actions:[TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('İptal')),
      FilledButton(onPressed:widget.name.text.trim().length<3?null:()=>Navigator.pop(context,true),child:const Text('Kaydet'))],
  );
}

class Ngelx556Highlights extends StatelessWidget {
  final String uid;
  final Map<String,dynamic> profile,viewer;
  const Ngelx556Highlights({super.key,required this.uid,required this.profile,required this.viewer});
  @override Widget build(BuildContext context)=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
    stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).where('highlighted',isEqualTo:true).limit(30).snapshots(),
    builder:(_,snapshot){
      if(snapshot.hasError)return const Padding(padding:EdgeInsets.symmetric(vertical:12),child:Text('Öne çıkan hikâyeler yüklenemedi.'));
      final docs=(snapshot.data?.docs??[]).where((d)=>ngelx556HighlightVisible(d.data(),uid,profile,viewer,FirebaseAuth.instance.currentUser?.uid)).toList();
      if(docs.isEmpty)return const SizedBox.shrink();
      return SizedBox(height:100,child:ListView.separated(scrollDirection:Axis.horizontal,itemCount:docs.length,separatorBuilder:(_,__)=>const SizedBox(width:12),itemBuilder:(_,i){
        final d=docs[i],v=d.data(),url=(v['mediaUrl']??'').toString(),type=(v['storyMediaType']??'photo').toString();
        return SizedBox(width:72,child:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(
          url:url,mediaType:type,kullanici:(profile['displayName']??profile['username']??'').toString(),fotoUrl:(profile['photoUrl']??'').toString(),ownerUid:uid,storyId:d.id,createdAt:v['createdAt'],expiresAt:v['expiresAt'],
        ))),child:Column(children:[
          ClipOval(child:SizedBox(width:60,height:60,child:type=='video'?NgelXVideoKapakOnizleme(url:url):NgelXAgResmi(imageUrl:url,fit:BoxFit.cover))),
          const SizedBox(height:6),Text((v['highlightTitle']??'Öne çıkan').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:12)),
        ])));
      }));
    },
  );
}
Future<void> ngelx556CommentNotification(DocumentReference<Map<String,dynamic>> post)async{
  try{
    final me=_communityUid450,community=post.parent.parent;
    if(me.isEmpty||community==null)return;
    final p=(await post.get()).data(),c=(await community.get()).data();
    if(p==null||c==null||p['status']!='approved')return;
    final target=(p['authorId']??'').toString();
    if(target.isEmpty||!List<String>.from(c['members']??const[]).contains(target))return;
    await uygulamaBildirimiGonder(toUid:target,fromUid:me,tur:'comment',metin:'topluluk gönderine yorum yaptı',belgeId:community.id,hedefTuru:'community',hedefBaslik:(c['name']??'Topluluk').toString(),olayTuru:'community_comment');
  }catch(_){/* A notification failure never rolls back a saved comment. */}
}

Future<void> ngelx556ShareCommunityPost(BuildContext context,DocumentReference<Map<String,dynamic>> post,Map<String,dynamic> value)async{
  final mode=await showModalBottomSheet<String>(context:context,showDragHandle:true,useSafeArea:true,builder:(sheet)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
    const ListTile(title:Text('Gönderiyi paylaş',style:TextStyle(fontWeight:FontWeight.w800,fontSize:19))),
    ListTile(leading:const Icon(Icons.chat_bubble_outline,color:mor),title:const Text('NgelX içinde paylaş'),subtitle:const Text('Kişi veya grup sohbetine gönder'),onTap:()=>Navigator.pop(sheet,'internal')),
    ListTile(leading:const Icon(Icons.ios_share_rounded),title:const Text('Diğer uygulamalar'),onTap:()=>Navigator.pop(sheet,'external')),
  ])));
  if(!context.mounted||mode==null)return;
  if(mode=='external'){await ngelx455SharePost(context,post,value,externalOnly556:true);return;}
  await showModalBottomSheet<void>(context:context,isScrollControlled:true,useSafeArea:true,showDragHandle:true,backgroundColor:Colors.white,
    builder:(_)=>Ngelx556SharePicker(post:post,value:value));
}
class Ngelx556SharePicker extends StatefulWidget {
  final DocumentReference<Map<String,dynamic>> post;
  final Map<String,dynamic> value;
  const Ngelx556SharePicker({super.key,required this.post,required this.value});
  @override State<Ngelx556SharePicker> createState()=>_Ngelx556SharePickerState();
}
class _Ngelx556SharePickerState extends State<Ngelx556SharePicker>{
  final uid=_communityUid450,selected=<String>{};
  final labels=<String,Future<Map<String,String>>>{};
  final sent=<String>{};
  final messageIds=<String,String>{};
  String search='';bool busy=false;
  late final query=FirebaseFirestore.instance.collection('chats').where('members',arrayContains:uid).limit(100).get();
  @override Widget build(BuildContext context)=>SafeArea(child:SizedBox(height:MediaQuery.sizeOf(context).height*.75,child:Column(children:[
    const ListTile(title:Text('NgelX içinde paylaş',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:Text('Kişi ve grup sohbetlerini seç')),
    Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:TextField(onChanged:(v)=>setState(()=>search=ngelx556Search(v)),decoration:const InputDecoration(hintText:'Sohbet ara',prefixIcon:Icon(Icons.search)))),
    Expanded(child:FutureBuilder<QuerySnapshot<Map<String,dynamic>>>(future:query,builder:(_,snapshot){
      if(snapshot.hasError)return const Center(child:Text('Sohbetler yüklenemedi. Tekrar açmayı dene.'));
      if(!snapshot.hasData)return const Center(child:CircularProgressIndicator());
      final docs=snapshot.data!.docs.where((d)=>d.data()['groupDeleted']!=true&&!List<String>.from(d.data()['hiddenFor']??const[]).contains(uid)).toList();
      if(docs.isEmpty)return const Center(child:Text('Paylaşabileceğin sohbet bulunamadı.'));
      return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){final d=docs[i];return FutureBuilder<Map<String,String>>(
        future:labels.putIfAbsent(d.id,()=>_ngelxSesliPaylasChatEtiketi(d.data(),uid)),builder:(_,s){
          final label=s.data?['ad']??'Sohbet',group=s.data?['tur']=='group';
          if(search.isNotEmpty&&!ngelx556Search(label).contains(search))return const SizedBox.shrink();
          return CheckboxListTile(value:selected.contains(d.id),enabled:!busy&&!sent.contains(d.id),onChanged:(v)=>setState(()=>v==true?selected.add(d.id):selected.remove(d.id)),
            secondary:CircleAvatar(child:Icon(group?Icons.groups_rounded:Icons.person_outline)),title:Text(label,maxLines:1,overflow:TextOverflow.ellipsis),subtitle:Text(sent.contains(d.id)?'Gönderildi':group?'Grup':'Özel sohbet'));
        });});
    })),
    Padding(padding:const EdgeInsets.all(16),child:SizedBox(width:double.infinity,child:FilledButton.icon(onPressed:busy||selected.isEmpty?null:send,icon:const Icon(Icons.send_rounded),label:Text(busy?'Gönderiliyor…':'${selected.length} sohbete gönder')))),
  ])));
  Future<void> send()async{
    setState(()=>busy=true);int failed=0;
    for(final id in selected.toList()){
      try{await ngelx556SendPost(widget.post,widget.value,id,uid,messageIds.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('chats').doc(id).collection('messages').doc().id));sent.add(id);selected.remove(id);}catch(_){failed++;}
    }
    if(!mounted)return;
    setState(()=>busy=false);
    if(failed==0){Navigator.pop(context);return;}
    ngelxDurumMesaji(context,'$failed sohbete gönderilemedi. Gönderilen sohbetler tekrar seçilmez.',tip:'hata');
  }
}
Future<void> ngelx556SendPost(DocumentReference<Map<String,dynamic>> post,Map<String,dynamic> value,String chatId,String uid,String messageId)async{
  final db=FirebaseFirestore.instance,community=post.parent.parent;
  if(community==null||_communityUid450!=uid)throw StateError('session_changed');
  final chat=db.collection('chats').doc(chatId),message=db.collection('chats').doc(chatId).collection('messages').doc(messageId);
  await db.runTransaction((tx)async{
    final room=(await tx.get(chat)).data(),source=(await tx.get(post)).data(),c=(await tx.get(community)).data();
    final existing=await tx.get(message);
    if(existing.exists&&existing.data()?['senderId']==uid)return;
    if(_communityUid450!=uid||room==null||source==null||c==null||source['status']!='approved')throw StateError('unavailable');
    final members=List<String>.from(room['members']??const[]),communityMembers=List<String>.from(c['members']??const[]);
    if(!members.contains(uid)||room['groupDeleted']==true)throw StateError('not_member');
    // Private community content can only be forwarded to existing members.
    if(c['visibility']=='private'&&!members.every(communityMembers.contains))throw StateError('private_community');
    final group=room['isGroup']==true||members.length>2;
    if(group&&room['onlyAdminsCanPost']==true&&room['createdBy']!=uid&&!List<String>.from(room['admins']??const[]).contains(uid))throw StateError('admin_only');
    if(!group){
      final peerId=members.firstWhere((x)=>x!=uid),own=(await tx.get(db.collection('users').doc(uid))).data()??{},peer=(await tx.get(db.collection('users').doc(peerId))).data()??{};
      if(peer['deactivated']==true||List<String>.from(own['blocked']??const[]).contains(peerId)||List<String>.from(peer['blocked']??const[]).contains(uid))throw StateError('blocked');
      final accepted=room['requestAccepted_$uid']==true||room['requestAccepted_$peerId']==true;
      final permission=(peer['messagePermission']??(peer['friendsOnlyMessages']==true?'friends':'all')).toString();
      final friend=List<String>.from(peer['friends']??const[]).contains(uid)||List<String>.from(own['friends']??const[]).contains(peerId);
      if(!accepted&&(permission=='none'||permission=='friends'&&!friend||permission=='following'&&!List<String>.from(peer['following']??const[]).contains(uid)))throw StateError('message_permission');
    }
    final seconds=(room['disappearingSeconds'] as num?)?.toInt()??0;
    final title=(c['name']??'Topluluk').toString();
    tx.set(message,{'senderId':uid,'type':'text','text':'$title · Topluluk gönderisi\n${source['text']??''}',
      'communityId556':community.id,'communityPostId556':post.id,'communityTitle556':title,
      'createdAt':FieldValue.serverTimestamp(),'clientCreatedAt':Timestamp.now(),
      if(seconds>0)'expiresAt':Timestamp.fromDate(DateTime.now().add(Duration(seconds:seconds))),
    });
    tx.update(chat,{'lastMessage':'Topluluk gönderisi · $title','lastSenderId':uid,'lastMessageKind':'text','updatedAt':FieldValue.serverTimestamp(),'hiddenFor':FieldValue.arrayRemove(members),for(final id in members)if(id!=uid)'unread_$id':FieldValue.increment(1)});
  }).timeout(const Duration(seconds:15));
  try{await post.collection('shares').doc(uid).set({'uid':uid,'createdAt':FieldValue.serverTimestamp()});}catch(_){/* Delivered message remains successful. */}
  ngelx456CountRevision.value=post.path+'|'+DateTime.now().microsecondsSinceEpoch.toString();
}
class Ngelx556SharedPost extends StatelessWidget{
  final Map<String,dynamic> value;
  const Ngelx556SharedPost({super.key,required this.value});
  @override Widget build(BuildContext context)=>Card(child:ListTile(leading:const Icon(Icons.groups_outlined,color:mor),title:Text((value['communityTitle556']??'Topluluk').toString()),subtitle:const Text('Topluluk gönderisini aç'),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXCommunityDetail450(id:value['communityId556'].toString())))));
}

Future<void> ngelx556CommunityEvent(String communityId,String event,String entityId,{required bool adminsOnly})async{
  try{
    final uid=_communityUid450;
    if(uid.isEmpty)return;
    final c=(await _communities450.doc(communityId).get()).data();
    if(c==null||_communityUid450!=uid)return;
    final members=List<String>.from(c['members']??const[]);
    final targets=adminsOnly?<String>{...List<String>.from(c['admins']??const[]),(c['founderId']??'').toString()}:members.toSet();
    targets.remove(uid);targets.remove('');targets.removeWhere((id)=>!members.contains(id));
    for(final target in targets){
      if(_communityUid450!=uid)return;
      try{await uygulamaBildirimiGonder(toUid:target,fromUid:uid,tur:'interaction',
        metin:event=='community_join_request'?'topluluğa katılmak istiyor':event=='community_post_pending'?'onay için bir topluluk gönderisi gönderdi':'toplulukta yeni bir gönderi paylaştı',
        belgeId:communityId,hedefTuru:'community',hedefBaslik:(c['name']??'Topluluk').toString(),hedefFoto:(c['photoUrl']??'').toString(),olayTuru:event,dedupeKey:'${event}_${communityId}_${entityId}_$target');}catch(_){/* Preserve successful post/request on notification failure. */}
    }
  }catch(_){}
}
