part of 'main.dart';

const ngelx565LudoUrl='https://ngelx-live-moderation.alihancaglar76.workers.dev/ludo';
const ngelx565LudoColors=[Color(0xFFE64E65),Color(0xFF22B97F),Color(0xFFF2BB35),Color(0xFF279EEB)];
String ngelx565RoomId(String text)=>RegExp(r'https://ngelxsocial\.com/ludo/([A-F0-9]{16})(?:\s|$)').firstMatch(text)?.group(1)??'';
List<int> ngelx565Legal(Map<String,dynamic> room,int seat){
  final dice=room['dice'];if(dice is! num)return [];
  final tokens=List<dynamic>.from((room['tokens'] as List)[seat]);final distance=dice.toInt()*(room['doubled']==true?2:1);
  return [for(var i=0;i<tokens.length;i++)if(tokens[i]==-1?dice==6:tokens[i]!=57&&(tokens[i] as num)+distance<=57)i];
}
Future<Map<String,dynamic>> ngelx565LudoRequest(Map<String,dynamic> body) async {
 final user=FirebaseAuth.instance.currentUser;if(user==null||user.isAnonymous)throw Exception('Oynamak için hesabına giriş yap.');
 final token=await user.getIdToken();
 try{
  final response=await Dio(BaseOptions(connectTimeout:const Duration(seconds:10),receiveTimeout:const Duration(seconds:15))).post<dynamic>(ngelx565LudoUrl,data:body,options:Options(headers:{'Authorization':'Bearer $token','content-type':'application/json'}));
  return Map<String,dynamic>.from((response.data as Map)['room'] as Map);
 }on DioException catch(e){
  final data=e.response?.data;final code=data is Map?data['error']:null;
  const errors={'room_full':'Oda dolu veya oyun başlamış.','room_not_found':'Oda bulunamadı.','room_expired':'Bu odanın süresi doldu. Yeni bir oda oluştur.','not_a_player':'Bu oyuna erişimin yok.','state_changed':'Oyun durumu değişti. Tekrar dene.','not_your_turn':'Şu an sıra sende değil.','waiting_for_players':'Diğer oyuncuların katılması bekleniyor.','slow_down':'Biraz bekleyip tekrar dene.','unauthorized':'Oturumunu kontrol edip tekrar dene.','already_left':'Bu oyundan ayrılmışsın. Yeni bir odaya katılabilirsin.'};
  throw Exception(errors[code]??'Oyun sunucusuna bağlanılamadı. Tekrar dene.');
 }
}
class Ngelx565LudoLobby extends StatefulWidget{
 const Ngelx565LudoLobby({super.key});
 @override State<Ngelx565LudoLobby> createState()=>_Ngelx565LudoLobbyState();
}
class _Ngelx565LudoLobbyState extends State<Ngelx565LudoLobby>{
 int capacity=2;bool team=false,busy=false;String mode='classic',error='';final code=TextEditingController();
 @override void dispose(){code.dispose();super.dispose();}
 Future<void> open({bool join=false})async{
  if(busy)return;setState(()=>busy=true);
  try{
   final id=code.text.trim().toUpperCase();
   if(join&&!RegExp(r'^[A-F0-9]{16}$').hasMatch(id))throw Exception('Davetindeki 16 haneli oda kodunu gir.');
   final room=await ngelx565LudoRequest(join?{'action':'join','id':id}:{'action':'create','capacity':capacity,'team':team,'mode':mode});
   if(mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:room['id'].toString(),initial:room)));
  }catch(e){if(mounted)setState(()=>error=e.toString().replaceFirst('Exception: ',''));}
  finally{if(mounted)setState(()=>busy=false);}
 }
 @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:const Color(0xFF3D2585),appBar:AppBar(title:const Text('NgelX Ludo'),backgroundColor:const Color(0xFF4F2E9B),foregroundColor:Colors.white),body:Container(decoration:const BoxDecoration(gradient:LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color(0xFF312B78),Color(0xFF8E4BBD)])),child:ListView(padding:const EdgeInsets.all(24),children:[
  const Icon(Icons.casino_rounded,size:80,color:Colors.white),const SizedBox(height:12),const Text('Birlikte Ludo oyna',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:26,fontWeight:FontWeight.w900)),const SizedBox(height:24),
  Card(child:Padding(padding:const EdgeInsets.all(18),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
   const Text('Oyun modu',style:TextStyle(fontWeight:FontWeight.w800)),Wrap(spacing:8,children:[for(final entry in {'classic':'Klasik','power':'Power'}.entries)ChoiceChip(label:Text(entry.value),selected:mode==entry.key,onSelected:busy?null:(_)=>setState(()=>mode=entry.key))]),
   const SizedBox(height:16),const Text('Oyuncular',style:TextStyle(fontWeight:FontWeight.w800)),Wrap(spacing:8,children:[ChoiceChip(label:const Text('2 kişi'),selected:capacity==2,onSelected:busy?null:(_)=>setState((){capacity=2;team=false;})),ChoiceChip(label:const Text('4 kişi'),selected:capacity==4&&!team,onSelected:busy?null:(_)=>setState((){capacity=4;team=false;})),ChoiceChip(label:const Text('2’ye 2 takım'),selected:team,onSelected:busy?null:(_)=>setState((){capacity=4;team=true;}))]),
   const SizedBox(height:16),FilledButton.icon(onPressed:busy?null:open,icon:const Icon(Icons.add_rounded),label:Text(busy?'Bağlanıyor…':'Oda oluştur')),
   const Text('Arkadaşların katıldıktan sonra oyunu sen başlatırsın.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:12)),
  ]))),const SizedBox(height:16),Card(child:Padding(padding:const EdgeInsets.all(18),child:Column(children:[TextField(controller:code,maxLength:16,textCapitalization:TextCapitalization.characters,decoration:const InputDecoration(labelText:'Oda koduyla katıl',hintText:'Davetindeki oda kodu')),SizedBox(width:double.infinity,child:OutlinedButton(onPressed:busy?null:()=>open(join:true),child:const Text('Katıl')))]))),
  if(error.isNotEmpty)Text(error,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white)),
 ])))) ;
}

class Ngelx565LudoRoom extends StatefulWidget{
 final String id;final Map<String,dynamic>? initial;
 const Ngelx565LudoRoom({super.key,required this.id,this.initial});
 @override State<Ngelx565LudoRoom> createState()=>_Ngelx565LudoRoomState();
}
class _Ngelx565LudoRoomState extends State<Ngelx565LudoRoom> with WidgetsBindingObserver{
 final roomNotifier=ValueNotifier<Map<String,dynamic>>({});Timer? poll;bool busy=false,syncing=false,allowExit=false;String error='';
 String get uid=>FirebaseAuth.instance.currentUser?.uid??'';
 Map<String,dynamic> get room=>roomNotifier.value;
 int get mySeat{for(final p in room['players']??[]){if(p['uid']==uid)return (p['seat'] as num).toInt();}return -1;}
 @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);if(widget.initial!=null)roomNotifier.value=widget.initial!;unawaited(load(join:widget.initial==null));startPoll();}
 void startPoll(){poll?.cancel();poll=Timer.periodic(const Duration(seconds:4),(_)=>unawaited(load()));}
 @override void didChangeAppLifecycleState(AppLifecycleState state){if(state==AppLifecycleState.resumed){startPoll();unawaited(load());}else poll?.cancel();}
 @override void dispose(){poll?.cancel();WidgetsBinding.instance.removeObserver(this);roomNotifier.dispose();super.dispose();}
 Future<void> load({bool join=false})async{
  if(syncing||busy||allowExit)return;syncing=true;
  try{final next=await ngelx565LudoRequest({'action':join?'join':'sync','id':widget.id});if(mounted&&(next['revision'] as num)>=(room['revision'] as num? ?? -1)){roomNotifier.value=next;setState(()=>error='');}}
  catch(e){if(mounted)setState(()=>error=e.toString().replaceFirst('Exception: ',''));}finally{syncing=false;}
 }
 Future<void> action(String action,[Map<String,dynamic> data=const {}])async{
  if(busy||room.isEmpty)return;setState(()=>busy=true);
  final body={'action':action,'id':widget.id,'revision':room['revision'],'requestId':'${DateTime.now().microsecondsSinceEpoch}_${math.Random().nextInt(1<<30)}',...data};
  try{
   final next=await ngelx565LudoRequest(body);if(mounted&&(next['revision'] as num)>=(room['revision'] as num? ?? -1)){roomNotifier.value=next;setState(()=>error='');}
  }catch(e){if(mounted)setState(()=>error=e.toString().replaceFirst('Exception: ',''));}
  finally{if(mounted){setState(()=>busy=false);if(action!='leave')unawaited(load());}}
 }
 Future<bool> leave()async{
  final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Oyundan ayrıl?'),content:const Text('Başlamış bir oyundan ayrılırsan bu turdan çekilirsin.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Ayrıl'))]))??false;
  if(!ok)return false;await action('leave');return error.isEmpty;
 }
 Future<void> controlDice()async{
  final number=await showDialog<int>(context:context,builder:(c)=>SimpleDialog(title:const Text('Zar sayısını seç'),children:[Wrap(alignment:WrapAlignment.center,children:[for(var i=1;i<=6;i++)TextButton(onPressed:()=>Navigator.pop(c,i),child:Text('$i',style:const TextStyle(fontSize:24)))])]));if(number!=null)await action('power',{'kind':'control','number':number});
 }
 Future<void> chat()async{
  final text=TextEditingController();
  await showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,builder:(c)=>Padding(padding:EdgeInsets.only(bottom:MediaQuery.viewInsetsOf(c).bottom),child:SizedBox(height:380,child:Column(children:[const Text('Oyun sohbeti',style:TextStyle(fontSize:20,fontWeight:FontWeight.w800)),Expanded(child:ValueListenableBuilder<Map<String,dynamic>>(valueListenable:roomNotifier,builder:(_,r,__)=>ListView(padding:const EdgeInsets.all(16),children:[for(final m in r['chat']??[])Text('${m['name']}: ${m['text']}',style:const TextStyle(fontSize:16))]))),Wrap(children:[for(final emoji in ['😊','🎲','👏','❤️','🎉'])TextButton(onPressed:()=>action('chat',{'text':emoji}),child:Text(emoji,style:const TextStyle(fontSize:25)))]),Padding(padding:const EdgeInsets.all(12),child:Row(children:[Expanded(child:TextField(controller:text,maxLength:180,decoration:const InputDecoration(hintText:'Mesaj yaz…',counterText:''))),IconButton(onPressed:()async{final value=text.text.trim();if(value.isNotEmpty){await action('chat',{'text':value});if(error.isEmpty)text.clear();}},icon:const Icon(Icons.send_rounded))]))]))));text.dispose();
 }
 @override Widget build(BuildContext context){
  final waiting=room['status']=='waiting',playing=room['status']=='playing',finished=room['status']=='finished',myTurn=playing&&mySeat==room['turn'];
  final players=List<dynamic>.from(room['players']??[]),seat=mySeat;
  final power=seat<0?{}:Map<String,dynamic>.from((room['power'] as List)[seat] as Map);
  return Theme(data:ThemeData.light(),child:PopScope(canPop:allowExit||room.isEmpty||finished||room['status']=='closed',onPopInvokedWithResult:(didPop,result)async{if(!didPop&&await leave()&&mounted){setState(()=>allowExit=true);WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)Navigator.pop(context);});}},child:Scaffold(backgroundColor:const Color(0xFF352471),appBar:AppBar(backgroundColor:const Color(0xFF4A2C91),foregroundColor:Colors.white,title:Text('Ludo · ${room['team']==true?'2’ye 2':room['mode']=='power'?'Power':'Klasik'}'),actions:[IconButton(tooltip:'Davet et',onPressed:waiting?()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoInvitePicker(id:widget.id))):null,icon:const Icon(Icons.person_add_alt_1_rounded))]),body:SafeArea(child:Column(children:[
   Padding(padding:const EdgeInsets.symmetric(horizontal:12,vertical:6),child:Row(children:[Expanded(child:Text('Oda: ${widget.id}',style:const TextStyle(color:Colors.white70,fontSize:12))),IconButton(tooltip:'Oda kodunu kopyala',onPressed:()=>Clipboard.setData(ClipboardData(text:widget.id)),icon:const Icon(Icons.copy_rounded,size:17,color:Colors.white70))])),
   Padding(padding:const EdgeInsets.symmetric(horizontal:8),child:Wrap(spacing:6,runSpacing:6,children:[for(final p in players)Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:5),decoration:BoxDecoration(color:ngelx565LudoColors[(p['seat'] as num).toInt()].withValues(alpha:.2),borderRadius:BorderRadius.circular(16),border:Border.all(color:p['seat']==room['turn']?Colors.white:Colors.transparent,width:2)),child:Row(mainAxisSize:MainAxisSize.min,children:[CircleAvatar(radius:13,backgroundColor:ngelx565LudoColors[(p['seat'] as num).toInt()],backgroundImage:(p['photo']??'').toString().isEmpty?null:NgelXAgImageProvider(p['photo'].toString()),child:(p['photo']??'').toString().isEmpty?const Icon(Icons.person,size:17,color:Colors.white):null),const SizedBox(width:5),SizedBox(width:75,child:Text('${p['name']}${p['left']==true?' · ayrıldı':''}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:11)))]))])),
   if(error.isNotEmpty)Padding(padding:const EdgeInsets.all(8),child:Text(error,textAlign:TextAlign.center,style:const TextStyle(color:Colors.amberAccent))),
   Expanded(child:Center(child:Padding(padding:const EdgeInsets.all(10),child:AspectRatio(aspectRatio:1,child:room.isEmpty?const Center(child:CircularProgressIndicator(color:Colors.white)):Ngelx565LudoBoard(room:room,seat:seat,enabled:myTurn&&!busy,onToken:(token)=>action('move',{'token':token})))))),
   if(waiting)...[Text('${players.length}/${room['capacity']} oyuncu · Arkadaşların bekleniyor',style:const TextStyle(color:Colors.white)),Wrap(spacing:12,children:[FilledButton.icon(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoInvitePicker(id:widget.id))),icon:const Icon(Icons.share_rounded),label:const Text('Davet et')),if(room['owner']==uid)FilledButton(onPressed:busy||players.length!=room['capacity']?null:()=>action('start'),child:const Text('Başlat'))])],
   if(playing)...[Text(myTurn?'Sıra sende':'Diğer oyuncu oynuyor',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),const SizedBox(height:5),Row(mainAxisAlignment:MainAxisAlignment.center,children:[FilledButton.icon(onPressed:myTurn&&!busy&&room['dice']==null?()=>action('roll'):null,icon:busy?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2)):const Icon(Icons.casino_rounded),label:Text(room['dice']==null?'Zar at':'Zar: ${room['dice']} · Taşını seç')),IconButton(onPressed:chat,icon:const Icon(Icons.chat_bubble_outline_rounded,color:Colors.white))]),if(room['mode']=='power')Wrap(spacing:8,children:[TextButton(onPressed:myTurn&&!busy&&room['dice']!=null&&(power['double']??0)>0?()=>action('power',{'kind':'double'}):null,child:const Text('×2 mesafe',style:TextStyle(color:Colors.white))),TextButton(onPressed:myTurn&&!busy&&room['dice']==null&&(power['control']??0)>0?controlDice:null,child:const Text('Zar seç',style:TextStyle(color:Colors.white))),TextButton(onPressed:myTurn&&!busy&&(power['shield']??0)>0?()=>action('power',{'kind':'shield'}):null,child:const Text('Kalkan',style:TextStyle(color:Colors.white)))])],
   if(finished)Padding(padding:const EdgeInsets.all(12),child:Text(room['team']==true?'🎉 ${room['winner']==0?'Kırmızı–Sarı':'Yeşil–Mavi'} takımı kazandı':'🎉 ${players.where((p)=>p['seat']==room['winner']).map((p)=>p['name']).join()} kazandı',style:const TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900))),
   if(room['status']=='closed')const Text('Oda kapatıldı',style:TextStyle(color:Colors.white)),const SizedBox(height:8),
  ])))));
 }
}

List<Offset> ngelx565Track(){
 const base=[Offset(1,6),Offset(2,6),Offset(3,6),Offset(4,6),Offset(5,6),Offset(6,5),Offset(6,4),Offset(6,3),Offset(6,2),Offset(6,1),Offset(6,0),Offset(7,0),Offset(8,0)];
 return [for(var side=0;side<4;side++)for(final point in base)ngelx565Rotate(point,side)];
}
Offset ngelx565Rotate(Offset p,int seat){for(var i=0;i<seat;i++)p=Offset(14-p.dy,p.dx);return p;}
Offset ngelx565TokenPoint(int seat,int token,int position){
 if(position<0){final p=Offset(token%2==0?1.8:4.2,token<2?1.8:4.2);return ngelx565Rotate(p,seat);}
 if(position<52)return ngelx565Track()[(position+13*seat)%52];
 return ngelx565Rotate(Offset((position-51).toDouble(),7),seat);
}
class Ngelx565LudoBoard extends StatelessWidget{
 final Map<String,dynamic> room;final int seat;final bool enabled;final ValueChanged<int> onToken;
 const Ngelx565LudoBoard({super.key,required this.room,required this.seat,required this.enabled,required this.onToken});
 @override Widget build(BuildContext context)=>LayoutBuilder(builder:(context,box){
  final cell=box.maxWidth/15,allowed=seat<0?<int>[]:ngelx565Legal(room,seat);
  final seats=[for(final p in room['players']??[])if(p['left']!=true)(p['seat'] as num).toInt()];
  return Stack(children:[Positioned.fill(child:CustomPaint(painter:Ngelx565BoardPainter())),for(final color in seats)for(var token=0;token<4;token++)...[
   Builder(builder:(_){final position=(room['tokens'] as List)[color][token] as int;final p=ngelx565TokenPoint(color,token,position);final shift=position>=0?Offset((token%2)*cell*.16,(token~/2)*cell*.16):Offset.zero;
    return AnimatedPositioned(key:ValueKey('ludo-$color-$token'),duration:const Duration(milliseconds:280),curve:Curves.easeInOut,left:(p.dx+.5)*cell-cell*.37+shift.dx,top:(p.dy+.5)*cell-cell*.37+shift.dy,width:cell*.74,height:cell*.74,child:GestureDetector(onTap:enabled&&color==seat&&allowed.contains(token)?()=>onToken(token):null,child:Container(decoration:BoxDecoration(color:ngelx565LudoColors[color],shape:BoxShape.circle,border:Border.all(color:enabled&&color==seat&&allowed.contains(token)?Colors.amberAccent:Colors.white,width:enabled&&color==seat&&allowed.contains(token)?3:1.5),boxShadow:const [BoxShadow(color:Colors.black38,blurRadius:3,offset:Offset(0,2))]),child:Center(child:Text('${token+1}',style:TextStyle(color:Colors.white,fontSize:cell*.4,fontWeight:FontWeight.w900))))));}),
  ]]);
 });
}
class Ngelx565BoardPainter extends CustomPainter{
 @override void paint(Canvas canvas,Size size){
  final c=size.width/15,p=Paint();canvas.drawRRect(RRect.fromRectAndRadius(Offset.zero&size,const Radius.circular(12)),p..color=const Color(0xFFF7F5FF));
  final bases=[const Offset(0,0),const Offset(9,0),const Offset(9,9),const Offset(0,9)];
  for(var seat=0;seat<4;seat++){final rect=Rect.fromLTWH(bases[seat].dx*c,bases[seat].dy*c,6*c,6*c);canvas.drawRect(rect,p..color=ngelx565LudoColors[seat]);canvas.drawRRect(RRect.fromRectAndRadius(rect.deflate(c*.75),Radius.circular(c*.6)),p..color=Colors.white.withValues(alpha:.85));
   for(var t=0;t<4;t++){final at=ngelx565TokenPoint(seat,t,-1);canvas.drawCircle(Offset((at.dx+.5)*c,(at.dy+.5)*c),c*.6,p..color=ngelx565LudoColors[seat].withValues(alpha:.18));}
   for(var h=1;h<=5;h++){final at=ngelx565Rotate(Offset(h.toDouble(),7),seat);canvas.drawRect(Rect.fromLTWH(at.dx*c,at.dy*c,c,c),p..color=ngelx565LudoColors[seat].withValues(alpha:.65));}
  }
  final track=ngelx565Track();const safe=[0,8,13,21,26,34,39,47];
  for(var i=0;i<track.length;i++){final at=track[i],rect=Rect.fromLTWH(at.dx*c,at.dy*c,c,c);canvas.drawRect(rect,p..color=i%13==0?ngelx565LudoColors[i~/13]:Colors.white);canvas.drawRect(rect.deflate(.3),p..color=const Color(0xFFAAA5BC)..style=PaintingStyle.stroke..strokeWidth=.5);p.style=PaintingStyle.fill;
   if(safe.contains(i)){final tp=TextPainter(text:const TextSpan(text:'★',style:TextStyle(color:Color(0xFFB2A8CC),fontSize:12)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));}
  }
  final corners=[Offset(6*c,6*c),Offset(9*c,6*c),Offset(9*c,9*c),Offset(6*c,9*c)];
  for(var i=0;i<4;i++){final path=Path()..moveTo(7.5*c,7.5*c)..lineTo(corners[(i+3)%4].dx,corners[(i+3)%4].dy)..lineTo(corners[i].dx,corners[i].dy)..close();canvas.drawPath(path,p..color=ngelx565LudoColors[i]);}
 }
 @override bool shouldRepaint(covariant Ngelx565BoardPainter old)=>false;
}

class Ngelx565LudoInvitePicker extends StatefulWidget{
 final String id;const Ngelx565LudoInvitePicker({super.key,required this.id});
 @override State<Ngelx565LudoInvitePicker> createState()=>_Ngelx565LudoInvitePickerState();
}
class _Ngelx565LudoInvitePickerState extends State<Ngelx565LudoInvitePicker>{
 late final Future<QuerySnapshot<Map<String,dynamic>>> chats;
 @override void initState(){super.initState();chats=FirebaseFirestore.instance.collection('chats').where('members',arrayContains:FirebaseAuth.instance.currentUser?.uid??'').limit(80).get();}
 Future<void> open(QueryDocumentSnapshot<Map<String,dynamic>> chat)async{
  final me=FirebaseAuth.instance.currentUser?.uid,v=chat.data();
  final draft='🎲 Ludo daveti\nhttps://ngelxsocial.com/ludo/${widget.id}\nKatıl ve birlikte oyna!';
  if(v['isGroup']==true){if(mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:chat.id,ad:(v['groupName']??'Grup').toString(),foto:(v['groupPhotoUrl']??'').toString(),draft565:draft)));}
  else{
   final members=List<String>.from(v['members']??[]);final other=members.firstWhere((u)=>u!=me,orElse:()=>'');if(other.isEmpty)return;
   final profile=await FirebaseFirestore.instance.collection('users').doc(other).get();final p=profile.data()??{};
   if(mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:chat.id,digerUid:other,ad:(p['displayName']??p['username']??'Oyuncu').toString(),foto:(p['photoUrl']??'').toString(),draft565:draft)));
  }
 }
 @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(appBar:AppBar(title:const Text('Ludo davetini gönder')),body:FutureBuilder<QuerySnapshot<Map<String,dynamic>>>(future:chats,builder:(context,s){
  if(s.hasError)return const Center(child:Text('Sohbetler yüklenemedi. Geri dönüp tekrar dene.'));if(!s.hasData)return const Center(child:CircularProgressIndicator());
  final me=FirebaseAuth.instance.currentUser?.uid,docs=s.data!.docs.where((d)=>!List<dynamic>.from(d.data()['hiddenFor']??[]).contains(me)).toList();
  if(docs.isEmpty)return const Center(child:Text('Önce bir özel sohbet veya grup oluştur.'));
  return ListView(children:[const Padding(padding:EdgeInsets.all(16),child:Text('Sohbeti seç; daveti mesaj alanında görüp Gönder’e basabilirsin.')),for(final d in docs)if(d.data()['isGroup']==true)ListTile(leading:const Icon(Icons.groups_rounded,color:mor),title:Text((d.data()['groupName']??'Grup').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d))else Builder(builder:(_){final members=List<String>.from(d.data()['members']??[]),other=members.firstWhere((u)=>u!=me,orElse:()=>'');return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:other.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(other).get(),builder:(_,u)=>ListTile(leading:const Icon(Icons.person_rounded,color:mor),title:Text((u.data?.data()?['displayName']??u.data?.data()?['username']??'Sohbet').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d)));})]);
 })));
}
class Ngelx565LudoInviteCard extends StatelessWidget{
 final String id;final bool mine;final VoidCallback onLongPress;
 const Ngelx565LudoInviteCard({super.key,required this.id,required this.mine,required this.onLongPress});
 @override Widget build(BuildContext context)=>Align(alignment:mine?Alignment.centerRight:Alignment.centerLeft,child:GestureDetector(onLongPress:onLongPress,child:Container(width:260,margin:const EdgeInsets.symmetric(vertical:6,horizontal:4),padding:const EdgeInsets.all(16),decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFF7953E8),Color(0xFF3989EE)]),borderRadius:BorderRadius.circular(22)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Row(children:[Icon(Icons.casino_rounded,color:Colors.white,size:34),SizedBox(width:10),Text('Ludo daveti',style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900))]),const SizedBox(height:8),Text('Oda: $id',style:const TextStyle(color:Colors.white70,fontSize:11)),const Text('Aynı masada birlikte oyna.',style:TextStyle(color:Colors.white)),const SizedBox(height:10),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.white,foregroundColor:mor),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:id))),child:const Text('Katıl'))]))));
}
