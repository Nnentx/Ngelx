part of 'main.dart';

const ngelx565LudoUrl='https://oyun.ngelxsocial.com/ludo';
const ngelx565LudoColors=[Color(0xFF16D52E),Color(0xFFFFD500),Color(0xFF05B8F5),Color(0xFFF43B27)];
String ngelx565RoomId(String text)=>RegExp(r'https://ngelxsocial\.com/ludo/((?:[0-9]{6}|[A-F0-9]{16}))(?:\s|$)').firstMatch(text)?.group(1)??'';
List<int> ngelx565Legal(Map<String,dynamic> room,int seat){
  final dice=room['dice'];if(dice is! num)return [];
  final tokens=List<dynamic>.from((room['tokens'] as List)[seat]);final distance=dice.toInt()*(room['doubled']==true?2:1);
  return [for(var i=0;i<tokens.length;i++)if(tokens[i]==-1?dice==6:tokens[i]!=56&&(tokens[i] as num)+distance<=56)i];
}
final _ngelx566LudoTransport=Ngelx566LudoTransport();
Future<Map<String,dynamic>> ngelx565LudoRequest(Map<String,dynamic> body) async {
 final user=FirebaseAuth.instance.currentUser;if(user==null||user.isAnonymous)throw Exception('Oynamak için hesabına giriş yap.');
 final token=await user.getIdToken().timeout(const Duration(seconds:12));
 if(token==null)throw Exception('Oturumunu kontrol edip tekrar dene.');
 final payload=_ngelx566LudoTransport.prepare(body);
 try{
  Map<String,dynamic> room;
  try{room=await _ngelx566LudoTransport.request(payload,token:token);}
  on DioException catch(e){
   if(e.response?.statusCode!=401)rethrow;
   final fresh=await user.getIdToken(true);if(fresh==null)rethrow;
   room=await _ngelx566LudoTransport.request(payload,token:fresh);
  }
  if(FirebaseAuth.instance.currentUser?.uid!=user.uid)throw Exception('Oturum değişti. Tekrar giriş yap.');
  return room;
 }on DioException catch(e){
  final data=e.response?.data;final code=data is Map?data['error']:null;
  const errors={'room_full':'Oda dolu veya oyun başlamış.','room_not_found':'Oda bulunamadı.','room_expired':'Bu odanın süresi doldu. Yeni bir oda oluştur.','not_a_player':'Bu oyuna erişimin yok.','state_changed':'Oyun durumu değişti. Tekrar dene.','not_your_turn':'Şu an sıra sende değil.','waiting_for_players':'Diğer oyuncuların katılması bekleniyor.','slow_down':'Biraz bekleyip tekrar dene.','unauthorized':'Oturumunu kontrol edip tekrar dene.','already_left':'Bu oyundan ayrılmışsın. Yeni bir odaya katılabilirsin.'};
  debugPrint('Ludo566: ${e.type.name}, HTTP ${e.response?.statusCode}, ${code??'connection'}');
  throw Ngelx567Failure(code?.toString()??'connection',errors[code]??'Oyun bağlantısı kurulamadı. Tekrar dene.');
 }on FormatException {throw Exception('Oyun yanıtı doğrulanamadı. Tekrar dene.');}
}

const _ludoInk567=Color(0xFF27204C);
const _ludoGold567=Color(0xFFFFD95B);
ThemeData ngelx567LudoTheme()=>ThemeData(brightness:Brightness.dark,useMaterial3:true,
 colorScheme:ColorScheme.fromSeed(seedColor:const Color(0xFF9D83FF),brightness:Brightness.dark),
 scaffoldBackgroundColor:const Color(0xFF372474),
 appBarTheme:const AppBarTheme(backgroundColor:Colors.transparent,foregroundColor:Colors.white,elevation:0),
 dialogTheme:const DialogThemeData(backgroundColor:Color(0xFFF6F3FF),titleTextStyle:TextStyle(color:_ludoInk567,fontSize:21,fontWeight:FontWeight.w900),contentTextStyle:TextStyle(color:Color(0xFF625878),fontSize:15)),
 textButtonTheme:TextButtonThemeData(style:TextButton.styleFrom(foregroundColor:const Color(0xFF7046BA))),
 inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF6F3FF),labelStyle:const TextStyle(color:Color(0xFF72628F)),hintStyle:const TextStyle(color:Color(0xFF988DA9)),border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none)),
);
class _LudoBackdrop567 extends StatelessWidget {
 final Widget child;
 const _LudoBackdrop567({required this.child});
 @override Widget build(BuildContext context)=>DecoratedBox(decoration:const BoxDecoration(gradient:RadialGradient(center:Alignment(-.4,-.6),radius:1.5,colors:[Color(0xFF4447A0),Color(0xFF303373),Color(0xFF1D2259)])),child:child);
}
class Ngelx567GameButton extends StatelessWidget {
 final String label;final VoidCallback? onPressed;final IconData? icon;final bool gold,busy;
 const Ngelx567GameButton({super.key,required this.label,this.onPressed,this.icon,this.gold=false,this.busy=false});
 @override Widget build(BuildContext context){
  final enabled=onPressed!=null;
  return Container(decoration:BoxDecoration(borderRadius:BorderRadius.circular(15),gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:!enabled?[const Color(0xFF79728F),const Color(0xFF5A546F)]:gold?[const Color(0xFFFFEF91),const Color(0xFFFFC438)]:[const Color(0xFF91B8FF),const Color(0xFF566DE4)]),border:Border.all(color:enabled?(gold?const Color(0xFFFFEEA1):const Color(0xFFBACBFF)):const Color(0xFF9890AD)),boxShadow:[BoxShadow(color:Colors.black.withValues(alpha:.22),blurRadius:9,offset:const Offset(0,4))]),
   child:FilledButton(onPressed:onPressed,style:FilledButton.styleFrom(backgroundColor:Colors.transparent,disabledBackgroundColor:Colors.transparent,foregroundColor:gold?_ludoInk567:Colors.white,disabledForegroundColor:const Color(0xFFE5DFEF),shadowColor:Colors.transparent,padding:const EdgeInsets.symmetric(horizontal:14,vertical:13),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14))),child:Row(mainAxisAlignment:MainAxisAlignment.center,mainAxisSize:MainAxisSize.min,children:[if(busy)...[const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)),const SizedBox(width:7)]else if(icon!=null)...[Icon(icon,size:19),const SizedBox(width:7)],Flexible(child:Text(label,textAlign:TextAlign.center,style:const TextStyle(fontSize:15,fontWeight:FontWeight.w900)))])));
 }
}

class Ngelx565LudoLobby extends StatefulWidget {
 final Ngelx567Request? request;final String? userId;
 const Ngelx565LudoLobby({super.key,this.request,this.userId});
 @override State<Ngelx565LudoLobby> createState()=>_Ngelx565LudoLobbyState();
}
class _Ngelx565LudoLobbyState extends State<Ngelx565LudoLobby> {
 int capacity=2;bool team=false,busy=false,joining=false;String play='friends',difficulty='medium',mode='classic',error='';final code=TextEditingController();
 @override void dispose(){code.dispose();super.dispose();}
 Future<void> open({bool watch=false})async{
  if(busy)return;FocusScope.of(context).unfocus();setState((){busy=true;error='';});
  try{
   final text=code.text.trim().toUpperCase(),link=ngelx565RoomId(code.text.trim());
   final id=link.isNotEmpty?link:text.replaceAll(RegExp(r'\s'), '');
   if(joining&&!RegExp(r'^(?:[0-9]{6}|[A-F0-9]{16})$').hasMatch(id))throw const Ngelx567Failure('invalid_code','Davetindeki oda kodunu gir veya davet bağlantısını yapıştır.');
   final room=await (widget.request??ngelx565LudoRequest)(joining?{'action':watch?'watch':'join','id':id}:{'action':play=='bot'?'bot':play=='random'?'match':'create','capacity':capacity,'team':play=='friends'&&team,'mode':mode,'difficulty':difficulty});
   if(mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:room['id'].toString(),initial:room,request:widget.request,userId:widget.userId,watch:watch)));
  }catch(e){if(mounted)setState(()=>error=e.toString().replaceFirst('Exception: ',''));}
  finally{if(mounted)setState(()=>busy=false);}
 }
 Future<void> refresh()async{if(busy)return;setState(()=>error='');await Future<void>.delayed(const Duration(milliseconds:350));}
 Widget option(String title,String sub,bool selected,VoidCallback tap,{IconData? icon})=>Expanded(child:InkWell(onTap:busy?null:tap,borderRadius:BorderRadius.circular(18),child:AnimatedContainer(duration:const Duration(milliseconds:180),padding:const EdgeInsets.symmetric(vertical:17,horizontal:9),decoration:BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:selected?[const Color(0xFF9CD9FF),const Color(0xFF5864E3)]:[const Color(0xFF8B8DE1),const Color(0xFF6353AE)]),borderRadius:BorderRadius.circular(18),border:Border.all(color:selected?_ludoGold567:const Color(0xFFABA2EA),width:selected?2.5:1),boxShadow:const [BoxShadow(color:Color(0x33000000),blurRadius:6,offset:Offset(0,3))]),child:Column(children:[if(icon!=null)Icon(icon,color:selected?_ludoGold567:Colors.white,size:30),const SizedBox(height:5),Text(title,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:17)),Text(sub,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontSize:11)),if(selected)const Icon(Icons.check_circle_rounded,size:19,color:_ludoGold567)]))));
 @override Widget build(BuildContext context)=>Theme(data:ngelx567LudoTheme(),child:Scaffold(extendBodyBehindAppBar:false,appBar:AppBar(title:const Text('NgelX Ludo',style:TextStyle(fontWeight:FontWeight.w900)),actions:[IconButton(tooltip:'Yenile',onPressed:refresh,icon:const Icon(Icons.refresh_rounded))]),body:_LudoBackdrop567(child:Padding(padding:EdgeInsets.only(bottom:MediaQuery.viewPaddingOf(context).bottom),child:RefreshIndicator(onRefresh:refresh,color:_ludoGold567,child:ListView(physics:const AlwaysScrollableScrollPhysics(),padding:const EdgeInsets.fromLTRB(24,14,24,28),children:[
  const Center(child:Text('LUDO',style:TextStyle(color:_ludoGold567,fontSize:42,letterSpacing:4,fontWeight:FontWeight.w900,shadows:[Shadow(color:Color(0xFF36215F),offset:Offset(0,4),blurRadius:1)]))),
  const Center(child:Text('Arkadaşlarınla aynı masada',style:TextStyle(color:Colors.white70,fontSize:14))),const SizedBox(height:25),
  const Text('Nasıl oynamak istersin?',textAlign:TextAlign.center,style:TextStyle(fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:14),
  for(final item in [('friends',Icons.groups_rounded,'Arkadaşlarla oyna','Oda oluştur veya kodla katıl'),('bot',Icons.smart_toy_rounded,'Makineye karşı oyna','Bilgisayara karşı pratik yap'),('random',Icons.shuffle_rounded,'Rastgele rakiple oyna','Otomatik eşleş, hemen başla')])Padding(padding:const EdgeInsets.only(bottom:10),child:Material(color:play==item.$1?const Color(0xFF6577DE):const Color(0xFF7862B6),borderRadius:BorderRadius.circular(18),child:ListTile(shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18),side:BorderSide(color:play==item.$1?_ludoGold567:Colors.white24,width:2)),leading:Icon(item.$2,color:_ludoGold567,size:30),title:Text(item.$3,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),subtitle:Text(item.$4,style:const TextStyle(color:Colors.white70,fontSize:12)),trailing:play==item.$1?const Icon(Icons.check_circle,color:_ludoGold567):null,onTap:busy?null:()=>setState((){play=item.$1;joining=false;team=false;error='';})))),const SizedBox(height:12),
  if(play=='friends')Row(children:[Expanded(child:Ngelx567GameButton(label:'Oda oluştur',gold:!joining,onPressed:busy?null:()=>setState(()=>joining=false))),const SizedBox(width:12),Expanded(child:Ngelx567GameButton(label:'Odaya katıl',gold:joining,onPressed:busy?null:()=>setState(()=>joining=true)))]),const SizedBox(height:22),
  Container(padding:const EdgeInsets.all(18),decoration:BoxDecoration(gradient:const LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFF7B67C2),Color(0xFF63439F)]),borderRadius:BorderRadius.circular(24),border:Border.all(color:const Color(0xFFAB98EE),width:1.5),boxShadow:const [BoxShadow(color:Color(0x440F0B30),blurRadius:18,offset:Offset(0,9))]),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
   if(joining)...[
    const Text('Birlikte oynamaya katıl',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:21,fontWeight:FontWeight.w900)),const SizedBox(height:14),
    TextField(key:const ValueKey('ludo-room-code'),controller:code,style:const TextStyle(color:_ludoInk567,fontWeight:FontWeight.w800),keyboardType:TextInputType.number,decoration:const InputDecoration(labelText:'6 haneli oda kodu',prefixIcon:Icon(Icons.link_rounded,color:Color(0xFF7860AD)))),
    const SizedBox(height:20),Ngelx567GameButton(label:busy?'Katılınıyor…':'Katıl',gold:true,busy:busy,onPressed:busy?null:open),const SizedBox(height:10),Ngelx567GameButton(label:'İzleyici olarak gir',icon:Icons.visibility_rounded,onPressed:busy?null:()=>open(watch:true)),
   ]else...[
    const Text('Oyun modunu seç',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:15),
    Row(crossAxisAlignment:CrossAxisAlignment.start,children:[option('Klasik','Klasik Ludo',mode=='classic',()=>setState(()=>mode='classic'),icon:Icons.casino_rounded),const SizedBox(width:13),option('Power','Özel güçlerle oyna',mode=='power',()=>setState(()=>mode='power'),icon:Icons.auto_awesome_rounded)]),const SizedBox(height:23),
    const Text('Oyuncuları seç',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:13),
    Row(children:[option('2 kişi','Karşılıklı',capacity==2,()=>setState((){capacity=2;team=false;})),const SizedBox(width:10),option('4 kişi','Herkes tek',capacity==4&&!team,()=>setState((){capacity=4;team=false;})),if(play=='friends')const SizedBox(width:10),if(play=='friends')option('2V2','Takım kur',team,()=>setState((){capacity=4;team=true;}))]),const SizedBox(height:23),
    if(play=='bot')...[const Text('Zorluk',textAlign:TextAlign.center,style:TextStyle(fontSize:20,fontWeight:FontWeight.w900)),const SizedBox(height:12),Row(children:[for(final item in [('easy','Kolay'),('medium','Orta'),('hard','Zor')])option(item.$2,'',difficulty==item.$1,()=>setState(()=>difficulty=item.$1))]),const SizedBox(height:16)],
    if(play=='friends')const Row(mainAxisAlignment:MainAxisAlignment.center,children:[Icon(Icons.groups_rounded,size:17,color:Colors.white60),SizedBox(width:6),Flexible(child:Text('Davetini özel sohbete veya grubuna gönder',style:TextStyle(color:Colors.white70,fontSize:11)))]),const SizedBox(height:15),
    Ngelx567GameButton(label:busy?'Masa hazırlanıyor…':play=='bot'?'Oyuna başla':play=='random'?'Rakip bul':'Oda oluştur',gold:true,busy:busy,onPressed:busy?null:open),
   ],
   if(error.isNotEmpty)Padding(padding:const EdgeInsets.only(top:16),child:Text(error,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFFFFE39A),fontWeight:FontWeight.w600))),
  ])),const SizedBox(height:18),Text(play=='friends'?'Oda dolduğunda kurucu Başlat’a dokunur. Zar at, taşını seç ve dört taşını da eve ulaştır.':play=='bot'?'Makine otomatik oynar. Sıra sana geldiğinde zar at ve taşını seç.':'Uygun oyuncular bulunduğunda oyun otomatik başlar. Aramayı masadan iptal edebilirsin.',textAlign:TextAlign.center,style:TextStyle(color:Colors.white60,fontSize:12,height:1.5)),
 ]))))));
}

class Ngelx565LudoRoom extends StatefulWidget {
 final bool watch;final String id;final Map<String,dynamic>? initial;final String? userId;
 final Ngelx567Request? request;final VoidCallback? onInvite;
 const Ngelx565LudoRoom({super.key,required this.id,this.watch=false,this.initial,this.userId,this.request,this.onInvite});
 @override State<Ngelx565LudoRoom> createState()=>_Ngelx565LudoRoomState();
}
class _Ngelx565LudoRoomState extends State<Ngelx565LudoRoom> with WidgetsBindingObserver {
 late final Ngelx567RoomController game;
 bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;
 Map<String,dynamic> get room=>game.room;
 @override void initState(){
  super.initState();WidgetsBinding.instance.addObserver(this);
  final uid=widget.userId??FirebaseAuth.instance.currentUser?.uid??'';
  game=Ngelx567RoomController(id:widget.id,uid:uid,request:(body)=>(widget.request??ngelx565LudoRequest)(widget.watch?{...body,'action':body['action']=='leave'?'watch_leave':'watch'}:body),initial:widget.initial,accountMatches:widget.userId!=null?null:()=>FirebaseAuth.instance.currentUser?.uid==uid)..addListener(_changed);
  if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();
 }
 void _changed(){
  final messages=room['chat'] as List? ?? [];
  if(messages.isNotEmpty){final m=messages.last;final key='${m['uid']}:${m['at']}';
   if(key!=chatKey){chatKey=key;chatExpiry?.cancel();
    if(DateTime.now().millisecondsSinceEpoch-(m['at'] as num).toInt()<5000){chatBubble='${m['name']}: ${m['text']}';chatExpiry=Timer(const Duration(seconds:3),(){if(mounted){chatBubble=null;if(!_chatOpen)setState((){});}});}
   }
  }
  if(mounted&&!_chatOpen)setState((){});
 }
 void _startPoll(){poll?.cancel();poll=Timer.periodic(Duration(seconds:widget.watch?4:1),(tick){if(_chatOpen&&tick.tick%3!=0)return;if(!game.terminal)unawaited(game.sync());});}
 @override void didChangeAppLifecycleState(AppLifecycleState state){if(state==AppLifecycleState.resumed){_startPoll();unawaited(game.sync());}else{poll?.cancel();}}
 @override void dispose(){chatExpiry?.cancel();poll?.cancel();WidgetsBinding.instance.removeObserver(this);game.removeListener(_changed);game.dispose();super.dispose();}
 Future<void> _close()async{
  if(!mounted)return;poll?.cancel();setState(()=>_canClose=true);
  await WidgetsBinding.instance.endOfFrame;
  if(mounted)Navigator.of(context).pop();
 }
 Future<void> _askLeave()async{
  if(_asking||game.leaving)return;
  if(widget.watch){await game.perform('leave');await _close();return;}
  if(game.terminal||room.isEmpty){await _close();return;}
  if(game.busy)return;
  _asking=true;
  try{
   final answer=await showDialog<bool>(context:context,builder:(c)=>Theme(data:ngelx567LudoTheme(),child:AlertDialog(title:Text(game.waiting?'Masadan ayrıl?':'Oyundan ayrıl?'),content:Text(game.waiting?(game.owner?'Kurduğun masa kapanacak.':'Bu masadan çıkacaksın.'):'Bu oyundan çekileceksin. Diğer oyuncular devam edebilir.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(key:const ValueKey('confirm-ludo-leave'),style:FilledButton.styleFrom(backgroundColor:const Color(0xFF7354C9),foregroundColor:Colors.white),onPressed:()=>Navigator.pop(c,true),child:const Text('Ayrıl'))])));
   if(answer!=true||!mounted)return;poll?.cancel();
   final left=await game.leave();if(!mounted)return;
   if(left){await _close();}else{
    _startPoll();
    final close=await showDialog<bool>(context:context,builder:(c)=>Theme(data:ngelx567LudoTheme(),child:AlertDialog(title:const Text('Ayrılma doğrulanamadı'),content:const Text('Bağlantı nedeniyle masadan ayrılma henüz doğrulanamadı. Yeniden deneyebilir veya yalnızca bu ekranı kapatabilirsin.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Yeniden dene')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Ekranı kapat'))])));
    if(close==true&&mounted)await _close();
   }
  }finally{_asking=false;}
 }
 void _invite(){
  if(widget.onInvite!=null){widget.onInvite!();return;}
  Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoInvitePicker(id:widget.id)));
 }
 Future<void> _power(String kind)async{
  if(kind!='control'){await game.perform('power',{'kind':kind});return;}
  final value=await showDialog<int>(context:context,builder:(c)=>Theme(data:ngelx567LudoTheme(),child:SimpleDialog(title:const Text('Zar sayısını seç'),children:[Wrap(alignment:WrapAlignment.center,children:[for(var i=1;i<=6;i++)IconButton(onPressed:()=>Navigator.pop(c,i),icon:Ngelx567Dice(value:i,size:40))])])));
  if(value!=null)await game.perform('power',{'kind':'control','number':value});
 }
 Future<void> _chat()async{
  if(_chatOpen||widget.watch)return;setState(()=>_chatOpen=true);
  try{await showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,backgroundColor:const Color(0xFF302B67),builder:(c)=>Theme(data:ngelx567LudoTheme(),child:Padding(padding:EdgeInsets.only(bottom:math.max(MediaQuery.viewInsetsOf(c).bottom,MediaQuery.viewPaddingOf(c).bottom)),child:SizedBox(height:(MediaQuery.sizeOf(c).height-MediaQuery.viewInsetsOf(c).bottom-MediaQuery.viewPaddingOf(c).bottom-90).clamp(160.0,370.0),child:Ngelx570ChatPanel(game:game)))));}
  finally{if(mounted)setState(()=>_chatOpen=false);}
 }
 Widget _footer(){
  final active=game.playing,seat=game.seat,myTurn=active&&seat==room['turn']&&!widget.watch;
  final inventory=seat<0?<String,dynamic>{}:Map<String,dynamic>.from((room['power'] as List)[seat] as Map);
  return Padding(padding:const EdgeInsets.fromLTRB(14,6,14,12),child:Column(mainAxisSize:MainAxisSize.min,children:[
   if(game.error.isNotEmpty)TextButton.icon(onPressed:()=>game.sync(),icon:const Icon(Icons.refresh),label:Text(game.error)),
   if(game.terminal)...[
    Text(game.detached?'Bu masadan ayrıldın':room['status']=='closed'?'Masa kapandı':_winner567(room),style:const TextStyle(color:_ludoGold567,fontWeight:FontWeight.w900,fontSize:17)),const SizedBox(height:8),Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close),
   ]else if(active)...[
    Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
     Ngelx570Clock(paused:_chatOpen,deadline:(room['deadline'] as num?)?.toInt()??0,active:myTurn),const SizedBox(width:12),
     GestureDetector(onTap:myTurn&&!game.busy&&room['dice']==null?()=>game.perform('roll'):null,child:Container(padding:const EdgeInsets.all(7),decoration:ngelx570Bevel(const Color(0xFF211D55),14),child:Ngelx567Dice(value:ngelx570ShownDice(room),size:52,busy:game.busy&&myTurn))),
     const SizedBox(width:12),Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(widget.watch?'Oyunu izliyorsun':myTurn?'Sıra sende':'Rakibin oynuyor',style:const TextStyle(color:_ludoGold567,fontWeight:FontWeight.w900,fontSize:15)),Text(myTurn?(room['dice']==null?'Zara dokun':'Parlayan taşını seç'):'Hamleleri takip et',style:const TextStyle(color:Colors.white70,fontSize:11))])),
    ]),const SizedBox(height:9),
    Row(children:[Expanded(child:ngelx570Chip('İyi oyunlar',widget.watch?null:()=>game.perform('chat',{'text':'İyi oyunlar!'}))),const SizedBox(width:8),Expanded(child:ngelx570Chip('Güzel hamle',widget.watch?null:()=>game.perform('chat',{'text':'Güzel hamle!'})))]),const SizedBox(height:9),
    Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
     Column(children:[ngelx570Chip('😊 Emoji',widget.watch?null:_chat),const SizedBox(height:5),Tooltip(message:'Emoji ve sohbet',child:ngelx570Chip('Sohbet',widget.watch?null:_chat))]),
     if(room['mode']=='power'&&!widget.watch)...[const SizedBox(width:10),for(final item in [('control','Zar seç'),('double','Çift'),('shield','Kalkan')])Expanded(child:Ngelx570Power(kind:item.$1,label:item.$2,count:(inventory[item.$1] as num?)?.toInt()??0,onTap:myTurn&&!game.busy&&(inventory[item.$1]??0)>0&&(item.$1!='control'||room['dice']==null)&&(item.$1!='double'||room['dice']!=null)?()=>_power(item.$1):null))]
     else Expanded(child:Text(widget.watch?'İZLEYİCİ':'KLASİK LUDO',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white54,fontWeight:FontWeight.w800,letterSpacing:2,fontSize:11))),
    ]),
   ]else...[Text(room['matchmaking']==true?'${game.joined}/${room['capacity']??2} oyuncu · Rakip aranıyor…':'${game.joined}/${room['capacity']??2} oyuncu',style:const TextStyle(color:Colors.white70)),if(room['matchmaking']==true)Ngelx567GameButton(label:'Vazgeç',onPressed:_askLeave),IconButton(tooltip:'Emoji ve sohbet',onPressed:_chat,icon:const Icon(Icons.chat_bubble_outline_rounded))],
  ]));
 }
 @override Widget build(BuildContext context){
  final players=List<Map<String,dynamic>>.from((room['players'] as List? ?? []).map((p)=>Map<String,dynamic>.from(p as Map)));
  return Theme(data:ngelx567LudoTheme(),child:PopScope(canPop:_canClose,onPopInvokedWithResult:(didPop,result){if(!didPop)unawaited(_askLeave());},child:Scaffold(extendBodyBehindAppBar:false,
   appBar:AppBar(leading:IconButton(key:const ValueKey('ludo-back'),tooltip:'Masadan ayrıl',onPressed:game.leaving?null:_askLeave,icon:const Icon(Icons.arrow_back_rounded)),title:const Ngelx570Logo(),actions:[Center(child:Padding(padding:const EdgeInsets.only(right:10),child:Row(children:[const Icon(Icons.visibility_rounded,size:16,color:Colors.white70),const SizedBox(width:4),Text('${room['spectatorCount']??0}',style:const TextStyle(fontSize:12))]))),IconButton(tooltip:'Oda kodunu kopyala',onPressed:()=>Clipboard.setData(ClipboardData(text:widget.id)),icon:const Icon(Icons.copy_rounded,size:20))]),
   body:_LudoBackdrop567(child:SafeArea(bottom:true,child:LayoutBuilder(builder:(context,box){
    final sideways=box.maxWidth>box.maxHeight*1.3&&box.maxWidth>550;
    final frame=Ngelx567Table(room:room,seat:game.seat,uid:game.uid,enabled:game.playing&&game.seat==room['turn']&&!game.busy&&!game.leaving,onToken:(token)=>game.perform('move',{'token':token}),onRoll:()=>game.perform('roll'),busy:game.busy);
    final wait=game.waiting&&!game.detached&&!widget.watch?Ngelx567WaitingPanel(room:room,uid:game.uid,canStart:game.canStart,busy:game.busy,onInvite:_invite,onStart:()=>game.perform('start'),compact:box.maxHeight<500):null;
    if(sideways)return Row(children:[Expanded(child:Padding(padding:const EdgeInsets.all(10),child:Stack(alignment:Alignment.center,children:[Center(child:AspectRatio(aspectRatio:.85,child:frame)),if(wait!=null)SizedBox(width:265,child:FittedBox(fit:BoxFit.scaleDown,child:SizedBox(width:265,child:wait)))]))),SizedBox(width:245,child:ListView(padding:const EdgeInsets.only(top:12),children:[_roomLabel567(widget.id),_footer()]))]);
    return Column(children:[_roomLabel567(widget.id),Expanded(child:LayoutBuilder(builder:(_,area)=>Stack(alignment:Alignment.center,children:[Padding(padding:const EdgeInsets.symmetric(horizontal:4),child:Center(child:AspectRatio(aspectRatio:.85,child:frame))),if(wait!=null)ConstrainedBox(constraints:BoxConstraints(maxWidth:math.min(320,area.maxWidth-34),maxHeight:area.maxHeight-8),child:SingleChildScrollView(child:wait)),if(room.isEmpty)const Center(child:CircularProgressIndicator(color:_ludoGold567)),if(chatBubble!=null)Positioned(left:16,right:16,bottom:8,child:IgnorePointer(child:Container(padding:const EdgeInsets.all(12),decoration:BoxDecoration(color:const Color(0xF022173F),borderRadius:BorderRadius.circular(16)),child:Text(chatBubble!,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w700)))))]))),if(players.isEmpty&&room.isEmpty)const Text('Masaya bağlanılıyor…',style:TextStyle(color:Colors.white70)),_footer()]);
   }))),
  )));
 }
}
Widget _roomLabel567(String id)=>Padding(padding:const EdgeInsets.symmetric(horizontal:18,vertical:5),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[const Icon(Icons.lock_outline_rounded,size:12,color:Colors.white38),const SizedBox(width:5),Flexible(child:Text('ODA · $id',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white54,fontSize:10,letterSpacing:1)))]));
String _winner567(Map<String,dynamic> room){
 final win=room['winner'];if(room['team']==true)return win==0?'Yeşil–Mavi takımı kazandı!':'Sarı–Kırmızı takımı kazandı!';
 for(final p in room['players']??[]){if(p['seat']==win)return '🎉 ${p['name']} kazandı!';}
 return 'Oyun tamamlandı';
}

class Ngelx567WaitingPanel extends StatelessWidget {
 final Map<String,dynamic> room;final String uid;final bool canStart,busy,compact;final VoidCallback onInvite,onStart;
 const Ngelx567WaitingPanel({super.key,required this.room,required this.uid,required this.canStart,required this.busy,required this.onInvite,required this.onStart,this.compact=false});
 @override Widget build(BuildContext context){
  final players=List<dynamic>.from(room['players']??[]).where((p)=>p['left']!=true).toList(),capacity=(room['capacity'] as num? ?? 2).toInt(),owner=room['owner']==uid;
  final id='${room['id']??''}';
  return Container(key:const ValueKey('ludo-waiting-panel'),decoration:BoxDecoration(borderRadius:BorderRadius.circular(20),gradient:const LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFFB8B4FF),Color(0xFF7C74D5)]),border:Border.all(color:const Color(0xFFD2CFFF),width:2),boxShadow:const [BoxShadow(color:Color(0x990C082E),blurRadius:28,offset:Offset(0,10))]),child:Column(mainAxisSize:MainAxisSize.min,children:[
   Padding(padding:EdgeInsets.symmetric(vertical:compact?7:11),child:Text(room['matchmaking']==true?'Rakip aranıyor…':'Arkadaşlarla · ${room['mode']=='power'?'Power':'Klasik'}',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:compact?15:18))),
   Container(margin:const EdgeInsets.fromLTRB(9,0,9,10),padding:EdgeInsets.all(compact?10:15),decoration:BoxDecoration(color:const Color(0xFFF0EFFF),borderRadius:BorderRadius.circular(15)),child:Column(mainAxisSize:MainAxisSize.min,children:[
    Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[for(var i=0;i<capacity;i++)i<players.length?Column(mainAxisSize:MainAxisSize.min,children:[CircleAvatar(radius:compact?17:22,backgroundColor:ngelx565LudoColors[(players[i]['seat'] as num).toInt()],backgroundImage:(players[i]['photo']??'').toString().isEmpty?null:NgelXAgImageProvider(players[i]['photo'].toString()),child:(players[i]['photo']??'').toString().isEmpty?const Icon(Icons.person_rounded,color:Colors.white):null),const SizedBox(height:3),SizedBox(width:capacity==4?48:90,child:Text(players[i]['uid']==uid?'Sen':'${players[i]['name']}',textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:_ludoInk567,fontSize:10,fontWeight:FontWeight.w800)))])
     :InkWell(onTap:room['matchmaking']==true?null:onInvite,child:Column(mainAxisSize:MainAxisSize.min,children:[Container(width:compact?34:44,height:compact?34:44,decoration:BoxDecoration(shape:BoxShape.circle,gradient:const LinearGradient(colors:[Color(0xFF91DEFF),Color(0xFF5285DF)]),border:Border.all(color:Colors.white,width:2)),child:Icon(room['matchmaking']==true?Icons.search_rounded:Icons.person_add_alt_1_rounded,color:Colors.white,size:22)),const SizedBox(height:3),Text(room['matchmaking']==true?'Aranıyor…':'Davet et',style:const TextStyle(color:Color(0xFF7065AD),fontSize:10,fontWeight:FontWeight.w800))]))]),
    SizedBox(height:compact?8:14),Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:8),decoration:BoxDecoration(color:const Color(0xFFE0DEFA),borderRadius:BorderRadius.circular(24)),child:Row(children:[const Icon(Icons.meeting_room_rounded,color:Color(0xFF8270C6),size:18),const SizedBox(width:6),Expanded(child:Text(id,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFF4C4077),fontWeight:FontWeight.w900,fontSize:11,letterSpacing:1))),InkWell(onTap:()=>Clipboard.setData(ClipboardData(text:id)),child:const Icon(Icons.copy_rounded,size:17,color:Color(0xFF8270C6)))])),
    Padding(padding:EdgeInsets.symmetric(vertical:compact?7:12),child:Text(players.length<capacity?'${capacity-players.length} oyuncu daha bekleniyor':owner?'Masa hazır. Oyunu başlatabilirsin.':'Kurucunun başlatması bekleniyor',textAlign:TextAlign.center,style:TextStyle(color:const Color(0xFF74658F),fontSize:compact?10:12,fontWeight:FontWeight.w700))),
    if(room['matchmaking']!=true)Row(children:[Expanded(child:Ngelx567GameButton(label:'Davet et',icon:Icons.person_add_alt_1_rounded,onPressed:busy?null:onInvite)),const SizedBox(width:10),Expanded(child:Ngelx567GameButton(key:const ValueKey('ludo-start'),label:'Başlat',gold:true,onPressed:canStart?onStart:null))]),
   ])),
  ]));
 }
}
class Ngelx567Table extends StatelessWidget {
 final Map<String,dynamic> room;final int seat;final String uid;final bool enabled,busy;final ValueChanged<int> onToken;final VoidCallback onRoll;
 const Ngelx567Table({super.key,required this.room,required this.seat,required this.uid,required this.enabled,required this.onToken,required this.onRoll,required this.busy});
 @override Widget build(BuildContext context)=>LayoutBuilder(builder:(_,box){
  final side=math.min(box.maxWidth,math.max(60.0,box.maxHeight-76)),left=(box.maxWidth-side)/2,top=(box.maxHeight-side)/2;
  final turns=seat<0?0:(3-seat+4)%4,playing=room['status']=='playing';
  final players=List<dynamic>.from(room['players']??[]).where((p)=>p['left']!=true).toList();
  return Stack(clipBehavior:Clip.none,children:[
   Positioned(left:left,top:top,width:side,height:side,child:Container(decoration:BoxDecoration(borderRadius:BorderRadius.circular(6),border:Border.all(color:const Color(0xFF675CB0),width:2),boxShadow:const [BoxShadow(color:Color(0x770D082D),blurRadius:24,offset:Offset(0,10))]),child:ClipRRect(borderRadius:BorderRadius.circular(4),child:RepaintBoundary(child:Ngelx565LudoBoard(room:room,seat:seat,enabled:enabled,onToken:onToken))))),
   for(final p in players)Builder(builder:(_){
    final color=(p['seat'] as num).toInt(),visual=(color+turns)%4,isLeft=visual==0||visual==3,isTop=visual==0||visual==1,isTurn=playing&&room['turn']==color,isMine=p['uid']==uid;
    final width=math.min(180.0,side*.57),photo='${p['photo']??''}';
    final lastRoll=room['lastRoll'] as Map?;
    final shownDice=(room['dice'] as num?)?.toInt() ?? (lastRoll!=null && lastRoll['seat']==color ? (lastRoll['value'] as num?)?.toInt() : null);
    return Positioned(left:isLeft?left:left+side-width,top:isTop?top-40:top+side+4,width:width,height:36,child:Row(mainAxisAlignment:isLeft?MainAxisAlignment.start:MainAxisAlignment.end,children:[
     if(!isLeft&&isTurn)...[GestureDetector(onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:shownDice,size:32,busy:busy&&isMine)),const SizedBox(width:6)],
     Container(width:34,height:34,padding:const EdgeInsets.all(2),decoration:BoxDecoration(shape:BoxShape.circle,color:isTurn?_ludoGold567:ngelx565LudoColors[color],boxShadow:[BoxShadow(color:(isTurn?_ludoGold567:Colors.black).withValues(alpha:.25),blurRadius:8)]),child:CircleAvatar(backgroundColor:const Color(0xFF8273AB),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?Icon(p['bot']==true?Icons.smart_toy_rounded:Icons.person_rounded,size:20,color:Colors.white):null)),const SizedBox(width:5),
     Flexible(child:Text(isMine?'Sen':'${p['name']}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white70,fontWeight:FontWeight.w800,fontSize:11))),
     if(isLeft&&isTurn)...[const SizedBox(width:6),GestureDetector(key:isMine?const ValueKey('ludo-dice'):null,onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:shownDice,size:32,busy:busy&&isMine))],
    ]));
   }),
  ]);
 });
}
class Ngelx567Dice extends StatelessWidget {
 final int? value;final double size;final bool busy;
 const Ngelx567Dice({super.key,this.value,this.size=48,this.busy=false});
 @override Widget build(BuildContext context)=>Semantics(label:value==null?'Zar at':'Zar: $value',child:Container(width:size,height:size,decoration:BoxDecoration(borderRadius:BorderRadius.circular(size*.23),boxShadow:const [BoxShadow(color:Color(0x660E0D2C),blurRadius:6,offset:Offset(0,3))]),child:CustomPaint(painter:_DicePainter567(value,busy))));
}
class _DicePainter567 extends CustomPainter {
 final int? value;final bool busy;const _DicePainter567(this.value,this.busy);
 @override void paint(Canvas canvas,Size size){
  final rect=Offset.zero&size,r=RRect.fromRectAndRadius(rect.deflate(1),Radius.circular(size.width*.2));
  canvas.drawRRect(r,Paint()..shader=const LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Colors.white,Color(0xFFF4F2FF),Color(0xFFAFA7D0)]).createShader(rect));
  canvas.drawRRect(r,Paint()..style=PaintingStyle.stroke..strokeWidth=1.5..color=const Color(0xFFE8DFFF));
  if(busy){final p=Paint()..color=const Color(0xFF7B61C3)..style=PaintingStyle.stroke..strokeWidth=3;canvas.drawArc(rect.deflate(size.width*.25),-.8,4.5,false,p);return;}
  if(value==null){final tp=TextPainter(text:TextSpan(text:'GO',style:TextStyle(fontFamily:'Roboto',color:const Color(0xFF5D458E),fontSize:size.width*.58,fontWeight:FontWeight.w900)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));return;}
  const positions={1:[4],2:[0,8],3:[0,4,8],4:[0,2,6,8],5:[0,2,4,6,8],6:[0,2,3,5,6,8]};
  for(final n in positions[value]??[]){final at=Offset(size.width*(.25+(n%3)*.25),size.height*(.25+(n~/3)*.25));canvas.drawCircle(at,size.width*.075,Paint()..color=const Color(0xFF27243E));canvas.drawCircle(at-Offset(size.width*.012,size.width*.014),size.width*.035,Paint()..color=const Color(0xFF555066));}
 }
 @override bool shouldRepaint(covariant _DicePainter567 old)=>old.value!=value||old.busy!=busy;
}

List<Offset> ngelx565Track(){
 const base=[Offset(1,6),Offset(2,6),Offset(3,6),Offset(4,6),Offset(5,6),Offset(6,5),Offset(6,4),Offset(6,3),Offset(6,2),Offset(6,1),Offset(6,0),Offset(7,0),Offset(8,0)];
 return [for(var side=0;side<4;side++)for(final point in base)ngelx565Rotate(point,side)];
}
Offset ngelx565Rotate(Offset p,int seat){for(var i=0;i<seat;i++)p=Offset(14-p.dy,p.dx);return p;}
Offset ngelx565TokenPoint(int seat,int token,int position){
 if(position<0)return ngelx565Rotate(Offset(token%2==0?1.5:3.5,token<2?1.5:3.5),seat);
 if(position<51)return ngelx565Track()[(position+13*seat)%52];
 return ngelx565Rotate(Offset((position-50).toDouble(),7),seat);
}
Offset ngelx567MovingPoint(int seat,int token,int from,int to,double t){
 if(from>=0&&to>from&&to-from<=12){final p=from+(to-from)*t;final low=p.floor().clamp(from,to).toInt();final high=(low+1).clamp(from,to).toInt();return Offset.lerp(ngelx565TokenPoint(seat,token,low),ngelx565TokenPoint(seat,token,high),p-low)!;}
 return Offset.lerp(ngelx565TokenPoint(seat,token,from),ngelx565TokenPoint(seat,token,to),t)!;
}
class Ngelx565LudoBoard extends StatelessWidget {
 final Map<String,dynamic> room;final int seat;final bool enabled;final ValueChanged<int> onToken;
 const Ngelx565LudoBoard({super.key,required this.room,required this.seat,required this.enabled,required this.onToken});
 @override Widget build(BuildContext context)=>LayoutBuilder(builder:(_,box){
  final cell=box.maxWidth/15,turns=seat<0?0:(3-seat+4)%4,allowed=seat<0?<int>[]:ngelx565Legal(room,seat);
  final seats=[for(final p in room['players']??[])if(p['left']!=true)(p['seat'] as num).toInt()];
  return Stack(children:[Positioned.fill(child:CustomPaint(painter:Ngelx565BoardPainter(turns:turns,power:room['mode']=='power'))),for(final color in seats)for(var token=0;token<4;token++)_MovingPawn567(key:ValueKey('ludo-$color-$token'),seat:color,token:token,position:((room['tokens'] as List)[color][token] as num).toInt(),cell:cell,turns:turns,highlight:enabled&&color==seat&&allowed.contains(token),onTap:enabled&&color==seat&&allowed.contains(token)?()=>onToken(token):null)]);
 });
}
class _MovingPawn567 extends StatefulWidget {
 final int seat,token,position,turns;final double cell;final bool highlight;final VoidCallback? onTap;
 const _MovingPawn567({super.key,required this.seat,required this.token,required this.position,required this.cell,required this.turns,required this.highlight,this.onTap});
 @override State<_MovingPawn567> createState()=>_MovingPawn567State();
}
class _MovingPawn567State extends State<_MovingPawn567> with SingleTickerProviderStateMixin {
 late final AnimationController motion;late int from;ui.Image? sprite;
 @override void initState(){super.initState();sprite=_loadedPawn570;from=widget.position;motion=AnimationController(vsync:this,duration:const Duration(milliseconds:180))..value=1;unawaited(ngelx570PawnSprite().then((value){if(mounted)setState(()=>sprite=value);}).catchError((_){ }));}
 @override void didUpdateWidget(covariant _MovingPawn567 old){super.didUpdateWidget(old);if(old.position!=widget.position){from=old.position;motion.duration=Duration(milliseconds:math.min(1800,math.max(210,(widget.position-from).abs()*160)));motion.forward(from:0);}}
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>AnimatedBuilder(animation:motion,builder:(_,__){
  final p=ngelx565Rotate(ngelx567MovingPoint(widget.seat,widget.token,from,widget.position,motion.value),widget.turns),c=widget.cell;
  return Positioned(left:(p.dx+.5)*c-c*.56,top:(p.dy+.5)*c-c*.8624-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.17,width:c*1.12,height:c*1.12,child:Semantics(label:'${widget.token+1}. taş',button:widget.onTap!=null,child:GestureDetector(behavior:HitTestBehavior.opaque,onTap:widget.onTap,child:CustomPaint(painter:Ngelx570SpritePainter(widget.seat,widget.highlight,sprite)))));
 });
}
class _PawnPainter567 extends CustomPainter {
 final Color color;final bool highlight;const _PawnPainter567(this.color,this.highlight);
 @override void paint(Canvas canvas,Size size){
  final w=size.width,h=size.height,rect=Offset.zero&size;
  if(highlight)canvas.drawCircle(Offset(w*.5,h*.62),w*.47,Paint()..shader=RadialGradient(colors:[_ludoGold567.withValues(alpha:.65),_ludoGold567.withValues(alpha:0)]).createShader(rect));
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.52,h*.87),width:w*.68,height:h*.2),Paint()..color=Colors.black.withValues(alpha:.22));
  final dark=Color.lerp(color,Colors.black,.55)!,light=Color.lerp(color,Colors.white,.72)!;
  final body=Path()..moveTo(w*.39,h*.32)..cubicTo(w*.43,h*.48,w*.31,h*.6,w*.24,h*.75)..quadraticBezierTo(w*.5,h*.91,w*.76,h*.75)..cubicTo(w*.69,h*.6,w*.57,h*.48,w*.61,h*.32)..close();
  final shader=LinearGradient(colors:[dark,light,color,dark],stops:const [0,.23,.48,1]).createShader(rect);
  canvas.drawPath(body,Paint()..shader=shader);
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.77),width:w*.66,height:h*.21),Paint()..shader=shader);
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.73),width:w*.57,height:h*.12),Paint()..color=light.withValues(alpha:.65));
  canvas.drawCircle(Offset(w*.5,h*.27),w*.24,Paint()..shader=RadialGradient(center:const Alignment(-.45,-.5),colors:[Color.lerp(color,Colors.white,.7)!,color,dark],stops:const [0,.55,1]).createShader(Rect.fromCircle(center:Offset(w*.5,h*.27),radius:w*.22)));
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.43,h*.21),width:w*.12,height:h*.07),Paint()..color=Colors.white.withValues(alpha:.6));
  if(highlight)canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.81),width:w*.77,height:h*.23),Paint()..style=PaintingStyle.stroke..strokeWidth=1.5..color=_ludoGold567);
 }
 @override bool shouldRepaint(covariant _PawnPainter567 old)=>old.color!=color||old.highlight!=highlight;
}
class Ngelx565BoardPainter extends CustomPainter {
 final int turns;final bool power;
 const Ngelx565BoardPainter({this.turns=0,this.power=false});
 void tile(Canvas canvas,Rect rect,Color color){
  final p=Paint();canvas.drawRect(rect,p..color=Color.lerp(color,Colors.black,.35)!);
  canvas.drawRect(rect.deflate(.7),p..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.white,.18)!,color,Color.lerp(color,Colors.black,.08)!]).createShader(rect));p.shader=null;
  canvas.drawLine(rect.topLeft+const Offset(1,1),rect.topRight+const Offset(-1,1),p..color=Colors.white.withValues(alpha:.65)..strokeWidth=1.2);
 }
 void star(Canvas canvas,Offset center,double radius,Color color){final path=Path();for(var j=0;j<10;j++){final angle=-math.pi/2+j*math.pi/5,r=j.isEven?radius:radius*.46,at=center+Offset(math.cos(angle)*r,math.sin(angle)*r);if(j==0){path.moveTo(at.dx,at.dy);}else{path.lineTo(at.dx,at.dy);}}canvas.drawPath(path..close(),Paint()..color=color);}
 @override void paint(Canvas canvas,Size size){
  final c=size.width/15,paint=Paint();canvas.save();canvas.translate(size.width/2,size.height/2);canvas.rotate(turns*math.pi/2);canvas.translate(-size.width/2,-size.height/2);
  canvas.drawRect(Offset.zero&size,paint..color=const Color(0xFFCED9EE));
  const bases=[Offset(0,0),Offset(9,0),Offset(9,9),Offset(0,9)];
  for(var seat=0;seat<4;seat++){
   final color=ngelx565LudoColors[seat],base=Rect.fromLTWH(bases[seat].dx*c,bases[seat].dy*c,6*c,6*c);
   final outer=RRect.fromRectAndRadius(base.deflate(.5),Radius.circular(c*.12));
   canvas.drawRRect(outer,paint..color=Colors.white..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.white,.4)!,color,Color.lerp(color,Colors.black,.18)!]).createShader(base));paint.shader=null;
   canvas.drawRRect(outer.deflate(2),paint..style=PaintingStyle.stroke..strokeWidth=1.8..color=Color.lerp(color,Colors.white,.48)!);paint.style=PaintingStyle.fill;
   final home=base.deflate(c*.88),inner=RRect.fromRectAndRadius(home,Radius.circular(c*.23));
   canvas.drawRRect(inner,paint..color=Colors.white..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.black,.48)!,Color.lerp(color,Colors.black,.16)!]).createShader(home));paint.shader=null;
   canvas.drawRRect(inner.deflate(1),paint..style=PaintingStyle.stroke..strokeWidth=2..color=Color.lerp(color,Colors.black,.25)!);paint.style=PaintingStyle.fill;
   canvas.drawLine(home.bottomLeft+Offset(c*.2,0),home.bottomRight-Offset(c*.2,0),paint..color=Colors.white.withValues(alpha:.28)..strokeWidth=1.5);
   for(var token=0;token<4;token++){final at=ngelx565TokenPoint(seat,token,-1),center=Offset((at.dx+.5)*c,(at.dy+.5)*c);canvas.drawCircle(center,c*.44,paint..color=Colors.black.withValues(alpha:.19));}
   for(var h=1;h<=5;h++){final at=ngelx565Rotate(Offset(h.toDouble(),7),seat);tile(canvas,Rect.fromLTWH(at.dx*c,at.dy*c,c,c),color);}
  }
  final track=ngelx565Track();const safe=[0,8,13,21,26,34,39,47];const pickup=[2,5,10,15,18,23,28,31,36,41,44,49];
  for(var i=0;i<52;i++){
   final at=track[i],rect=Rect.fromLTWH(at.dx*c,at.dy*c,c,c);tile(canvas,rect,i%13==0?ngelx565LudoColors[i~/13]:const Color(0xFFF1F5FD));
   if(safe.contains(i))star(canvas,rect.center,c*.34,i%13==0?Color.lerp(ngelx565LudoColors[i~/13],Colors.black,.4)!:const Color(0xFF899AB6));
   else if(power&&[4,17,30,43].contains(i)){
    canvas.drawRRect(RRect.fromRectAndRadius(rect.deflate(c*.1),Radius.circular(c*.12)),paint..color=Colors.white..shader=LinearGradient(colors:const [Color(0xFFFFF4A3),Color(0xFFFFBD18)],begin:Alignment.topLeft,end:Alignment.bottomRight).createShader(rect));paint.shader=null;
    final tp=TextPainter(text:TextSpan(text:'+1',style:TextStyle(fontFamily:'Roboto',color:const Color(0xFF9C5100),fontSize:c*.51,fontWeight:FontWeight.w900)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));
   }else if(power&&pickup.contains(i)){
    canvas.drawCircle(rect.center,c*.42,paint..color=Colors.white..shader=const RadialGradient(center:Alignment(-.3,-.4),colors:[Colors.white,Color(0xFF63D9FF),Color(0xFF2953BB)]).createShader(rect));paint.shader=null;
    canvas.save();canvas.translate(rect.left+c*.08,rect.top+c*.08);canvas.rotate(-turns*math.pi/2);if(turns!=0){canvas.restore();canvas.save();canvas.translate(rect.center.dx,rect.center.dy);canvas.rotate(-turns*math.pi/2);canvas.translate(-c*.42,-c*.42);}
    Ngelx570PowerPainter(['control','double','shield'][pickup.indexOf(i)%3]).paint(canvas,Size(c*.84,c*.84));canvas.restore();
   }
  }
  final corners=[Offset(6*c,6*c),Offset(9*c,6*c),Offset(9*c,9*c),Offset(6*c,9*c)];
  for(var i=0;i<4;i++){final path=Path()..moveTo(7.5*c,7.5*c)..lineTo(corners[(i+3)%4].dx,corners[(i+3)%4].dy)..lineTo(corners[i].dx,corners[i].dy)..close();canvas.drawPath(path,paint..color=ngelx565LudoColors[i]);canvas.drawPath(path,paint..style=PaintingStyle.stroke..strokeWidth=.7..color=Colors.black26);paint.style=PaintingStyle.fill;}
  canvas.restore();
 }
 @override bool shouldRepaint(covariant Ngelx565BoardPainter old)=>old.turns!=turns||old.power!=power;
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
 @override Widget build(BuildContext context)=>Theme(data:ngelx567LudoTheme(),child:Scaffold(appBar:AppBar(title:const Text('Ludo davetini gönder')),body:FutureBuilder<QuerySnapshot<Map<String,dynamic>>>(future:chats,builder:(context,s){
  if(s.hasError)return const Center(child:Text('Sohbetler yüklenemedi. Geri dönüp tekrar dene.'));if(!s.hasData)return const Center(child:CircularProgressIndicator());
  final me=FirebaseAuth.instance.currentUser?.uid,docs=s.data!.docs.where((d)=>!List<dynamic>.from(d.data()['hiddenFor']??[]).contains(me)).toList();
  if(docs.isEmpty)return const Center(child:Text('Önce bir özel sohbet veya grup oluştur.'));
  return ListView(padding:EdgeInsets.only(bottom:math.max(MediaQuery.viewPaddingOf(context).bottom,MediaQuery.paddingOf(context).bottom)+40),children:[const Padding(padding:EdgeInsets.all(16),child:Text('Sohbeti seç; daveti mesaj alanında görüp Gönder’e basabilirsin.')),for(final d in docs)if(d.data()['isGroup']==true)ListTile(leading:const Icon(Icons.groups_rounded,color:mor),title:Text((d.data()['groupName']??'Grup').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d))else Builder(builder:(_){final members=List<String>.from(d.data()['members']??[]),other=members.firstWhere((u)=>u!=me,orElse:()=>'');return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:other.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(other).get(),builder:(_,u)=>ListTile(leading:const Icon(Icons.person_rounded,color:mor),title:Text((u.data?.data()?['displayName']??u.data?.data()?['username']??'Sohbet').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d)));})]);
 })));
}
class Ngelx565LudoInviteCard extends StatelessWidget{
 final String id;final bool mine;final VoidCallback onLongPress;
 const Ngelx565LudoInviteCard({super.key,required this.id,required this.mine,required this.onLongPress});
 @override Widget build(BuildContext context)=>Align(alignment:mine?Alignment.centerRight:Alignment.centerLeft,child:GestureDetector(onLongPress:onLongPress,child:Container(width:260,margin:const EdgeInsets.symmetric(vertical:6,horizontal:4),padding:const EdgeInsets.all(16),decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFF7953E8),Color(0xFF3989EE)]),borderRadius:BorderRadius.circular(22)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Row(children:[Icon(Icons.casino_rounded,color:Colors.white,size:34),SizedBox(width:10),Text('Ludo daveti',style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900))]),const SizedBox(height:8),Text('Oda: $id',style:const TextStyle(color:Colors.white70,fontSize:11)),const Text('Aynı masada birlikte oyna.',style:TextStyle(color:Colors.white)),const SizedBox(height:10),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.white,foregroundColor:mor),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:id))),child:const Text('Katıl'))]))));
}

BoxDecoration ngelx570Bevel(Color color,double radius)=>BoxDecoration(
 gradient:LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.white,.22)!,color,Color.lerp(color,Colors.black,.35)!]),
 borderRadius:BorderRadius.circular(radius),border:Border.all(color:Color.lerp(color,Colors.white,.5)!,width:1.4),
 boxShadow:[const BoxShadow(color:Color(0x88080A2D),blurRadius:7,offset:Offset(0,4)),BoxShadow(color:color.withValues(alpha:.25),blurRadius:10)]);
class Ngelx570Logo extends StatelessWidget {
 const Ngelx570Logo({super.key});
 @override Widget build(BuildContext context)=>FittedBox(fit:BoxFit.scaleDown,child:Text.rich(TextSpan(children:[const TextSpan(text:'NgelX ',style:TextStyle(color:Colors.white)),TextSpan(text:'Ludo',style:TextStyle(foreground:Paint()..shader=const LinearGradient(colors:[Color(0xFFFFD83C),Color(0xFF42E6FF)]).createShader(const Rect.fromLTWH(0,0,90,30))))]),style:const TextStyle(fontSize:25,fontWeight:FontWeight.w900,shadows:[Shadow(color:Color(0xFF11113C),offset:Offset(0,3),blurRadius:2)])));
}
Widget ngelx570Chip(String label,VoidCallback? tap)=>Opacity(opacity:tap==null ? .55 : 1,child:InkWell(onTap:tap,borderRadius:BorderRadius.circular(18),child:Container(padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),decoration:ngelx570Bevel(const Color(0xFF383387),18),child:Text(label,maxLines:1,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800,fontSize:11)))));
class Ngelx570Clock extends StatefulWidget {
 final int deadline;final bool active,paused;
 const Ngelx570Clock({super.key,required this.deadline,required this.active,this.paused=false});
 @override State<Ngelx570Clock> createState()=>_Ngelx570ClockState();
}
class _Ngelx570ClockState extends State<Ngelx570Clock>{
 Timer? tick;
 @override void initState(){super.initState();tick=Timer.periodic(const Duration(milliseconds:250),(_){if(mounted&&!widget.paused)setState((){});});}
 @override void dispose(){tick?.cancel();super.dispose();}
 @override Widget build(BuildContext context){final left=((widget.deadline-DateTime.now().millisecondsSinceEpoch)/1000).clamp(0,10).toDouble();return SizedBox(width:58,height:58,child:Stack(alignment:Alignment.center,children:[Container(decoration:BoxDecoration(shape:BoxShape.circle,color:const Color(0xFF171947),boxShadow:[BoxShadow(color:const Color(0xFF00CFFF).withValues(alpha:widget.active ? .6 : .15),blurRadius:12)])),SizedBox.expand(child:CircularProgressIndicator(value:left/10,strokeWidth:6,backgroundColor:const Color(0xFF292660),color:widget.active?const Color(0xFF4EEBFF):const Color(0xFF6F75AD))),Text('${left.ceil()}',style:const TextStyle(fontSize:22,color:Colors.white,fontWeight:FontWeight.w900))]));}
}
class Ngelx570Power extends StatelessWidget {
 final String kind,label;final int count;final VoidCallback? onTap;
 const Ngelx570Power({super.key,required this.kind,required this.label,required this.count,this.onTap});
 @override Widget build(BuildContext context)=>Tooltip(message:'$label: $count adet',child:InkWell(onTap:onTap,borderRadius:BorderRadius.circular(30),child:Column(mainAxisSize:MainAxisSize.min,children:[SizedBox(width:62,height:59,child:Stack(clipBehavior:Clip.none,children:[Positioned(left:1,right:4,top:3,bottom:0,child:Container(decoration:BoxDecoration(shape:BoxShape.circle,gradient:const RadialGradient(center:Alignment(-.4,-.5),colors:[Colors.white,Color(0xFF64E7FF),Color(0xFF1687DF),Color(0xFF183E9D)],stops:[0,.15,.65,1]),border:Border.all(color:const Color(0xFFC6F7FF),width:1.8),boxShadow:const [BoxShadow(color:Color(0x883ADDFF),blurRadius:7)]),child:CustomPaint(painter:Ngelx570PowerPainter(kind)))),Positioned(right:0,top:0,child:Container(padding:const EdgeInsets.all(4),constraints:const BoxConstraints(minWidth:21),decoration:BoxDecoration(shape:BoxShape.circle,gradient:const LinearGradient(colors:[Color(0xFFFF7663),Color(0xFFD81E24)]),border:Border.all(color:const Color(0xFFFFB08D))),child:Text('$count',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:12))))])),const SizedBox(height:3),Text(label,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800,fontSize:10))])));
}
class Ngelx570PowerPainter extends CustomPainter {
 final String kind;const Ngelx570PowerPainter(this.kind);
 @override void paint(Canvas canvas,Size size){
  final w=size.width;
  if(kind=='shield'){
   canvas.save();canvas.translate(w*.12,w*.06);canvas.scale(.7);_PawnPainter567(const Color(0xFFF33926),false).paint(canvas,size);canvas.restore();
   final shield=Path()..moveTo(w*.58,w*.40)..lineTo(w*.87,w*.45)..lineTo(w*.82,w*.73)..lineTo(w*.69,w*.88)..lineTo(w*.56,w*.73)..close();
   canvas.drawPath(shield,Paint()..shader=const LinearGradient(colors:[Color(0xFFE3FFFF),Color(0xFF006ADB)]).createShader(Offset.zero&size));canvas.drawPath(shield,Paint()..style=PaintingStyle.stroke..strokeWidth=2..color=Colors.white);
  }else{
   canvas.save();canvas.translate(w*.21,w*.25);canvas.rotate(.14);_DicePainter567(kind=='control'?5:6,false).paint(canvas,Size(w*.59,w*.59));canvas.restore();
   if(kind=='control'){canvas.save();canvas.translate(w*.08,w*.42);canvas.rotate(-.22);_DicePainter567(3,false).paint(canvas,Size(w*.40,w*.40));canvas.restore();}
   else{canvas.drawCircle(Offset(w*.51,w*.28),w*.1,Paint()..shader=const RadialGradient(center:Alignment(-.4,-.5),colors:[Colors.white,Colors.red,Color(0xFF9B1520)]).createShader(Rect.fromCircle(center:Offset(w*.51,w*.28),radius:w*.11)));}
  }
 }
 @override bool shouldRepaint(covariant Ngelx570PowerPainter old)=>old.kind!=kind;
}

ui.Image? _loadedPawn570;Future<ui.Image>? _pawn570;
Future<ui.Image> ngelx570PawnSprite()=>_pawn570??=()async{final bytes=await rootBundle.load('assets/ludo570_pawns.png');final codec=await ui.instantiateImageCodec(bytes.buffer.asUint8List());final frame=await codec.getNextFrame();codec.dispose();_loadedPawn570=frame.image;return frame.image;}();
class Ngelx570SpritePainter extends CustomPainter {
 final int seat;final bool highlight;final ui.Image? image;
 const Ngelx570SpritePainter(this.seat,this.highlight,this.image);
 @override void paint(Canvas canvas,Size size){
  if(highlight)canvas.drawOval(Rect.fromLTWH(0,size.height*.65,size.width,size.height*.35),Paint()..color=_ludoGold567.withValues(alpha:.7));
  final atlas=image;if(atlas==null){_PawnPainter567(ngelx565LudoColors[seat],highlight).paint(canvas,size);return;}
  final w=atlas.width/2,h=atlas.height/2;canvas.drawImageRect(atlas,Rect.fromLTWH((seat%2)*w,(seat~/2)*h,w,h),Offset.zero&size,Paint()..filterQuality=FilterQuality.high);
 }
 @override bool shouldRepaint(covariant Ngelx570SpritePainter old)=>old.seat!=seat||old.highlight!=highlight||old.image!=image;
}

int? ngelx570ShownDice(Map<String,dynamic> room){final dice=room['dice'];if(dice is num)return dice.toInt();final last=room['lastRoll'];if(last is Map&&last['seat']==room['turn'])return (last['value'] as num?)?.toInt();return null;}

class Ngelx570ChatPanel extends StatefulWidget {
 final Ngelx567RoomController game;const Ngelx570ChatPanel({super.key,required this.game});
 @override State<Ngelx570ChatPanel> createState()=>_Ngelx570ChatPanelState();
}
class _Ngelx570ChatPanelState extends State<Ngelx570ChatPanel>{
 final input=TextEditingController();bool sending=false;
 @override void dispose(){input.dispose();super.dispose();}
 Future<void> send([String? emoji])async{final text=emoji??input.text.trim();if(text.isEmpty||sending||widget.game.busy)return;setState(()=>sending=true);final sent=await widget.game.perform('chat',{'text':text});if(!mounted)return;if(sent){Navigator.pop(context);}else{setState(()=>sending=false);}}
 @override Widget build(BuildContext context)=>Column(children:[const Text('Masa sohbeti',style:TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900)),Expanded(child:AnimatedBuilder(animation:widget.game,builder:(_,__){final messages=widget.game.room['chat'] as List? ?? [];return ListView.builder(padding:const EdgeInsets.all(12),itemCount:messages.length,itemBuilder:(_,i)=>Padding(padding:const EdgeInsets.only(bottom:8),child:Text('${messages[i]['name']}: ${messages[i]['text']}',style:const TextStyle(color:Colors.white,fontSize:14))));})),Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[for(final emoji in ['😊','🎲','👏','❤️','🎉'])IconButton(onPressed:sending?null:()=>send(emoji),icon:Text(emoji,style:const TextStyle(fontSize:24)))]),Padding(padding:const EdgeInsets.fromLTRB(12,0,12,10),child:Row(children:[Expanded(child:TextField(key:const ValueKey('ludo-chat-input'),controller:input,maxLength:180,style:const TextStyle(color:_ludoInk567),decoration:const InputDecoration(hintText:'Mesaj yaz…',counterText:''),onSubmitted:(_)=>send())),IconButton(onPressed:sending?null:send,icon:const Icon(Icons.send_rounded,color:_ludoGold567))]))]);
}
