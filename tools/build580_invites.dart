String ngelx580InviteToken(String text)=>RegExp(r'[?&]invite=([a-f0-9]{64})').firstMatch(text)?.group(1)??'';
int? ngelx580MessageTime(Map<String,dynamic> v){
 final time=v['createdAt']??v['clientCreatedAt'];
 return time is Timestamp?time.millisecondsSinceEpoch:time is num?time.toInt():null;
}
Future<String> ngelx580PrepareInvite(String text)async{
 if(!text.startsWith('🎲 Ludo daveti\n'))return text;
 final id=RegExp(r'https://ngelxsocial\.com/ludo/([0-9A-F]{6,16})').firstMatch(text)?.group(1);
 if(id==null)return text;
 final invite=await ngelx565LudoRequest({'action':'invite_create','id':id,
  'requestId':'invite580_${DateTime.now().microsecondsSinceEpoch}_${math.Random.secure().nextInt(1<<32)}'});
 return '🎲 Ludo daveti\nhttps://ngelxsocial.com/ludo/$id?invite=${invite['inviteToken']}\nKatıl ve birlikte oyna!';
}

class Ngelx580InviteTarget {
 final String id,name,photo,other;final bool group;
 const Ngelx580InviteTarget({required this.id,required this.name,this.photo='',this.other='',this.group=false});
}
String ngelx580Search(String value)=>value.replaceAll('İ','i').replaceAll('I','ı').toLowerCase();
class Ngelx565LudoInvitePicker extends StatefulWidget{
 final String id;const Ngelx565LudoInvitePicker({super.key,required this.id});
 @override State<Ngelx565LudoInvitePicker> createState()=>_Ngelx565LudoInvitePickerState();
}
class _Ngelx565LudoInvitePickerState extends State<Ngelx565LudoInvitePicker>{
 late Future<List<Ngelx580InviteTarget>> targets;
 @override void initState(){super.initState();targets=_load();}
 Future<List<Ngelx580InviteTarget>> _load()async{
  final me=FirebaseAuth.instance.currentUser?.uid??'';
  final chats=await FirebaseFirestore.instance.collection('chats').where('members',arrayContains:me).get();
  final result=<Ngelx580InviteTarget>[];
  final visible=chats.docs.where((d)=>!List<dynamic>.from(d.data()['hiddenFor']??[]).contains(me)).toList();
  // Bound concurrent profile reads; do not create a new Future on every keystroke.
  for(var offset=0;offset<visible.length;offset+=8){
   final batch=visible.skip(offset).take(8);
   final loaded=await Future.wait(batch.map((d)async{
    final v=d.data();
    if(v['isGroup']==true)return Ngelx580InviteTarget(id:d.id,group:true,
     name:(v['groupName']??'Grup').toString(),photo:(v['groupPhotoUrl']??v['photoUrl']??'').toString());
    final other=List<String>.from(v['members']??[]).firstWhere((u)=>u!=me,orElse:()=>'');
    if(other.isEmpty)return null;
    final p=(await FirebaseFirestore.instance.collection('users').doc(other).get()).data()??{};
    return Ngelx580InviteTarget(id:d.id,other:other,
     name:(p['displayName']??p['username']??v['name']??'Oyuncu').toString(),photo:(p['photoUrl']??'').toString());
   }));
   result.addAll(loaded.whereType<Ngelx580InviteTarget>());
  }
  result.sort((a,b)=>ngelx580Search(a.name).compareTo(ngelx580Search(b.name)));
  return result;
 }
 Future<void> _open(Ngelx580InviteTarget target)async{
  final draft='🎲 Ludo daveti\nhttps://ngelxsocial.com/ludo/${widget.id}\nKatıl ve birlikte oyna!';
  if(!mounted)return;
  await Navigator.push(context,MaterialPageRoute(builder:(_)=>target.group?
   GrupSohbetPage(chatId:target.id,ad:target.name,foto:target.photo,draft565:draft):
   SohbetPage(chatId:target.id,digerUid:target.other,ad:target.name,foto:target.photo,draft565:draft)));
 }
 @override Widget build(BuildContext context)=>FutureBuilder<List<Ngelx580InviteTarget>>(
  future:targets,builder:(_,snapshot)=>Ngelx580InviteContacts(
   targets:snapshot.data??const [],loading:!snapshot.hasData&&!snapshot.hasError,
   error:snapshot.hasError?'Sohbetler yüklenemedi. Tekrar dene.':null,
   onRetry:(){setState(()=>targets=_load());},onPick:_open));
}
class Ngelx580InviteContacts extends StatefulWidget{
 final List<Ngelx580InviteTarget> targets;final bool loading;
 final String? error;final VoidCallback? onRetry;
 final ValueChanged<Ngelx580InviteTarget> onPick;
 const Ngelx580InviteContacts({super.key,required this.targets,required this.onPick,this.loading=false,this.error,this.onRetry});
 @override State<Ngelx580InviteContacts> createState()=>_Ngelx580InviteContactsState();
}
class _Ngelx580InviteContactsState extends State<Ngelx580InviteContacts>{
 final query=TextEditingController();
 @override void dispose(){query.dispose();super.dispose();}
 @override Widget build(BuildContext context){
  final search=ngelx580Search(query.text.trim());
  final visible=widget.targets.where((p)=>ngelx580Search(p.name).contains(search)).toList();
  return Theme(data:ThemeData.light(useMaterial3:true),child:Scaffold(
   backgroundColor:Colors.white,
   appBar:AppBar(backgroundColor:Colors.white,foregroundColor:const Color(0xFF172A3B),surfaceTintColor:Colors.white,
    title:const Text('Ludo davetini gönder',style:TextStyle(fontSize:19,fontWeight:FontWeight.w700))),
   body:SafeArea(top:false,child:Column(children:[
    Padding(padding:const EdgeInsets.fromLTRB(16,8,16,12),child:TextField(
     key:const ValueKey('ludo-invite-search'),controller:query,onChanged:(_)=>setState((){}),
     decoration:InputDecoration(hintText:'Kişi veya grup ara',prefixIcon:const Icon(Icons.search_rounded),
      suffixIcon:query.text.isEmpty?null:IconButton(tooltip:'Aramayı temizle',onPressed:(){query.clear();setState((){});},icon:const Icon(Icons.close_rounded)),
      filled:true,fillColor:const Color(0xFFF1F3F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none)))),
    Expanded(child:widget.loading?const Center(child:CircularProgressIndicator()):widget.error!=null?
     Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Text(widget.error!),TextButton(onPressed:widget.onRetry,child:const Text('Tekrar dene'))])):
     visible.isEmpty?Center(child:Text(search.isEmpty?'Davet gönderebileceğin sohbet yok.':'Kişi veya grup bulunamadı.',style:const TextStyle(color:Color(0xFF657380)))):
     ListView.builder(key:const ValueKey('ludo-invite-contacts'),keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag,
      padding:const EdgeInsets.fromLTRB(8,0,8,20),itemCount:visible.length,itemBuilder:(_,i){
       final p=visible[i];return ListTile(key:ValueKey('invite-contact-${p.id}'),contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:4),
        leading:CircleAvatar(radius:25,backgroundColor:const Color(0xFFEDF0FA),
         backgroundImage:p.photo.isEmpty?null:ResizeImage(NgelXAgImageProvider(p.photo),width:160),
         child:p.photo.isEmpty?Icon(p.group?Icons.groups_rounded:Icons.person_rounded,color:const Color(0xFF7064BC)):null),
        title:Text(p.name,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF172A3B),fontSize:16,fontWeight:FontWeight.w600)),
        subtitle:Text(p.group?'Grup':'Özel sohbet',style:const TextStyle(color:Color(0xFF78838E),fontSize:12)),
        trailing:const Icon(Icons.chevron_right_rounded,color:Color(0xFF8D98A2)),onTap:()=>widget.onPick(p));
      })),
   ]))));
 }
}

class Ngelx565LudoInviteCard extends StatefulWidget{
 final String id,inviteToken;final bool mine;final int? sentAt;
 final VoidCallback onLongPress;final VoidCallback? onJoin;final Ngelx567Request? request;
 const Ngelx565LudoInviteCard({super.key,required this.id,required this.mine,required this.onLongPress,this.onJoin,this.inviteToken='',this.sentAt,this.request});
 @override State<Ngelx565LudoInviteCard> createState()=>_Ngelx565LudoInviteCardState();
}
class _Ngelx565LudoInviteCardState extends State<Ngelx565LudoInviteCard>{
 late final int legacyStart=DateTime.now().millisecondsSinceEpoch;
 Timer? timer;Map<String,dynamic> invite={};bool busy=false,polling=false;String error='';int offset=0;
 int get now=>DateTime.now().millisecondsSinceEpoch+offset;
 int get expires=>(invite['expiresAt'] as num?)?.toInt()??((widget.sentAt??legacyStart)+120000);
 String get status=>invite['status']=='joined'?'joined':now>=expires?'expired':invite['status']?.toString()??'pending';
 @override void initState(){super.initState();
  if(widget.inviteToken.isNotEmpty)unawaited(_refresh());
  _startTimer();
 }
 void _startTimer(){
  timer?.cancel();
  timer=Timer.periodic(const Duration(seconds:1),(t){
   if(!mounted)return;
   if(status!='pending'){
    timer?.cancel();setState((){});
    if(status=='expired'&&widget.inviteToken.isNotEmpty)unawaited(_refresh());
    return;
   }
   setState((){});
   if(widget.inviteToken.isNotEmpty&&t.tick%5==0&&status!='joined'&&invite['status']!='expired')unawaited(_refresh());
  });
 }
 @override void didUpdateWidget(covariant Ngelx565LudoInviteCard old){super.didUpdateWidget(old);
  if(old.inviteToken!=widget.inviteToken||old.id!=widget.id){invite={};offset=0;error='';if(widget.inviteToken.isNotEmpty)unawaited(_refresh());_startTimer();}
 }
 Future<void> _refresh()async{
  if(polling||busy)return;polling=true;
  try{
   final next=await (widget.request??ngelx565LudoRequest)({'action':'invite_status','inviteToken':widget.inviteToken});
   if(mounted)setState((){invite=next;offset=((next['serverNow'] as num?)?.toInt()??now)-DateTime.now().millisecondsSinceEpoch;error='';});
  }catch(e){if(mounted&&e is Ngelx567Failure&&['invite_expired','room_expired','room_not_found'].contains(e.code))setState(()=>invite={...invite,'status':'expired','expiresAt':0});}
  finally{polling=false;}
 }
 Future<void> _join()async{
  if(busy||status!='pending')return;
  if(widget.onJoin!=null){widget.onJoin!();return;}
  if(widget.inviteToken.isEmpty){
   await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:widget.id)));return;
  }
  setState((){busy=true;error='';});
  try{
   final room=await (widget.request??ngelx565LudoRequest)({'action':'invite_join','inviteToken':widget.inviteToken});
   if(!mounted)return;
   setState(()=>invite={...invite,'status':'joined'});
   await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:widget.id,initial:room,request:widget.request)));
  }catch(e){if(mounted)setState((){
   error=e.toString().replaceFirst('Exception: ','');
   if(e is Ngelx567Failure&&['invite_expired','invite_used','room_full','room_expired','room_not_found'].contains(e.code))invite={...invite,'status':'expired','expiresAt':0};
  });}
  finally{if(mounted)setState(()=>busy=false);}
 }
 @override void dispose(){timer?.cancel();super.dispose();}
 @override Widget build(BuildContext context){
  final name=(invite['name']??'Arkadaşın').toString(),photo=(invite['photo']??'').toString();
  final left=((expires-now)/1000).ceil().clamp(0,120);
  final countdown='${(left~/60).toString().padLeft(2,'0')}:${(left%60).toString().padLeft(2,'0')}';
  final state=status;
  final label=state=='joined'?'Katıldı':state=='expired'?'Süresi doldu':'Bekleniyor';
  return Align(alignment:widget.mine?Alignment.centerRight:Alignment.centerLeft,
   child:GestureDetector(onLongPress:widget.onLongPress,child:Container(
    key:const ValueKey('ludo-visual-invite'),width:300,margin:const EdgeInsets.symmetric(vertical:6,horizontal:4),
    clipBehavior:Clip.antiAlias,decoration:BoxDecoration(color:const Color(0xFFF2F3F8),borderRadius:BorderRadius.circular(24),border:Border.all(color:const Color(0xFFE7E8F0))),
    child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[
     SizedBox(height:158,child:photo.isNotEmpty?
      Image(image:ResizeImage(NgelXAgImageProvider(photo),width:720),fit:BoxFit.cover,errorBuilder:(_,__,___)=>const Ngelx580InviteArtwork()):const Ngelx580InviteArtwork()),
     Padding(padding:const EdgeInsets.fromLTRB(14,14,14,12),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
      Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
       Container(width:42,height:42,decoration:BoxDecoration(color:const Color(0xFF7350DC),borderRadius:BorderRadius.circular(12)),child:const Icon(Icons.casino_rounded,color:Colors.white,size:30)),
       const SizedBox(width:10),Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(widget.mine?'Birlikte Ludo oynayalım!':'$name seni oyuna davet ediyor.',maxLines:3,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF192535),fontSize:16,fontWeight:FontWeight.w800)),
        const SizedBox(height:3),const Text('NgelX Ludo',style:TextStyle(color:Color(0xFF7B808A),fontSize:13)),
       ])),
      ]),const SizedBox(height:12),
      Row(children:[Expanded(child:Text(label,key:const ValueKey('ludo-invite-status'),style:TextStyle(color:state=='joined'?const Color(0xFF248353):const Color(0xFF6E6886),fontWeight:FontWeight.w700))),
       if(state=='pending')Text(countdown,key:const ValueKey('ludo-invite-countdown'),style:const TextStyle(color:Color(0xFF6548C2),fontWeight:FontWeight.w800,fontSize:16))]),
      if(state=='pending')Padding(padding:const EdgeInsets.symmetric(vertical:7),child:LinearProgressIndicator(value:left/120,color:const Color(0xFF8360E0),backgroundColor:const Color(0xFFE2DDF0),minHeight:3)),
      if(error.isNotEmpty)Padding(padding:const EdgeInsets.only(bottom:6),child:Text(error,maxLines:2,style:const TextStyle(color:Color(0xFFAD4141),fontSize:12))),
      const SizedBox(height:8),FilledButton(key:const ValueKey('ludo-invite-join'),
       style:FilledButton.styleFrom(backgroundColor:Colors.white,disabledBackgroundColor:const Color(0xFFE6E7EC),foregroundColor:const Color(0xFF202936),disabledForegroundColor:const Color(0xFF8B8F99),padding:const EdgeInsets.symmetric(vertical:13),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(13))),
       onPressed:busy||state!='pending'?null:_join,
       child:Text(busy?'Katılınıyor…':state=='pending'?'Katıl':label,style:const TextStyle(fontWeight:FontWeight.w700,fontSize:16))),
     ])),
    ]))));
 }
}
class Ngelx580InviteArtwork extends StatelessWidget{
 const Ngelx580InviteArtwork({super.key});
 @override Widget build(BuildContext context)=>Container(
  decoration:const BoxDecoration(gradient:LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color(0xFF5737BD),Color(0xFF236BC0)])),
  child:Stack(alignment:Alignment.center,children:[
   Positioned(left:14,top:14,child:Transform.rotate(angle:-.18,child:const Icon(Icons.casino_rounded,size:64,color:Color(0xFFFFDD76)))),
   Positioned(right:14,bottom:10,child:Transform.rotate(angle:.2,child:const Icon(Icons.casino_rounded,size:48,color:Color(0xFF7CE5FF)))),
   const Column(mainAxisAlignment:MainAxisAlignment.center,children:[Text('NgelX',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:32)),Text('LUDO',style:TextStyle(color:Color(0xFFFFDD76),fontWeight:FontWeight.w900,fontSize:27,letterSpacing:6))]),
  ]));
}
