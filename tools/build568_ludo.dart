part of 'main.dart';

const ngelx565LudoUrl='https://oyun.ngelxsocial.com/ludo';
const ngelx565LudoColors=[Color(0xFF27CF78),Color(0xFFFFCD36),Color(0xFF35BFF6),Color(0xFFFA526B)];
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
 @override Widget build(BuildContext context)=>DecoratedBox(decoration:const BoxDecoration(gradient:RadialGradient(center:Alignment(-.4,-.6),radius:1.5,colors:[Color(0xFF7551B9),Color(0xFF412B83),Color(0xFF28205C)])),child:child);
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
 Future<void> open()async{
  if(busy)return;FocusScope.of(context).unfocus();setState((){busy=true;error='';});
  try{
   final text=code.text.trim().toUpperCase(),link=ngelx565RoomId(code.text.trim());
   final id=link.isNotEmpty?link:text.replaceAll(RegExp(r'\s'), '');
   if(joining&&!RegExp(r'^(?:[0-9]{6}|[A-F0-9]{16})$').hasMatch(id))throw const Ngelx567Failure('invalid_code','Davetindeki oda kodunu gir veya davet bağlantısını yapıştır.');
   final room=await (widget.request??ngelx565LudoRequest)(joining?{'action':'join','id':id}:{'action':play=='bot'?'bot':play=='random'?'match':'create','capacity':capacity,'team':play=='friends'&&team,'mode':mode,'difficulty':difficulty});
   if(mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:room['id'].toString(),initial:room,request:widget.request,userId:widget.userId)));
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
    const SizedBox(height:20),Ngelx567GameButton(label:busy?'Katılınıyor…':'Katıl',gold:true,busy:busy,onPressed:busy?null:open),
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
 final String id;final Map<String,dynamic>? initial;final String? userId;
 final Ngelx567Request? request;final VoidCallback? onInvite;
 const Ngelx565LudoRoom({super.key,required this.id,this.initial,this.userId,this.request,this.onInvite});
 @override State<Ngelx565LudoRoom> createState()=>_Ngelx565LudoRoomState();
}
class _Ngelx565LudoRoomState extends State<Ngelx565LudoRoom> with WidgetsBindingObserver {
 late final Ngelx567RoomController game;
 Timer? poll;bool _canClose=false,_asking=false;
 Map<String,dynamic> get room=>game.room;
 @override void initState(){
  super.initState();WidgetsBinding.instance.addObserver(this);
  final uid=widget.userId??FirebaseAuth.instance.currentUser?.uid??'';
  game=Ngelx567RoomController(id:widget.id,uid:uid,request:widget.request??ngelx565LudoRequest,initial:widget.initial,accountMatches:widget.userId!=null?null:()=>FirebaseAuth.instance.currentUser?.uid==uid)..addListener(_changed);
  if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();
 }
 void _changed(){if(mounted)setState((){});}
 void _startPoll(){poll?.cancel();poll=Timer.periodic(const Duration(seconds:4),(_){if(!game.terminal)unawaited(game.sync());});}
 @override void didChangeAppLifecycleState(AppLifecycleState state){if(state==AppLifecycleState.resumed){_startPoll();unawaited(game.sync());}else{poll?.cancel();}}
 @override void dispose(){poll?.cancel();WidgetsBinding.instance.removeObserver(this);game.removeListener(_changed);game.dispose();super.dispose();}
 Future<void> _close()async{
  if(!mounted)return;poll?.cancel();setState(()=>_canClose=true);
  await WidgetsBinding.instance.endOfFrame;
  if(mounted)Navigator.of(context).pop();
 }
 Future<void> _askLeave()async{
  if(_asking||game.leaving)return;
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
  final input=TextEditingController();
  await showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,backgroundColor:const Color(0xFF49377C),builder:(c)=>Theme(data:ngelx567LudoTheme(),child:Padding(padding:EdgeInsets.only(bottom:math.max(MediaQuery.viewInsetsOf(c).bottom,MediaQuery.viewPaddingOf(c).bottom)),child:SizedBox(height:math.min(370.0,MediaQuery.sizeOf(c).height-MediaQuery.viewInsetsOf(c).bottom-MediaQuery.viewPaddingOf(c).bottom-90),child:AnimatedBuilder(animation:game,builder:(_,__)=>Column(children:[const Text('Masa sohbeti',style:TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900)),Expanded(child:ListView(padding:const EdgeInsets.all(16),children:[for(final m in room['chat']??[])Padding(padding:const EdgeInsets.only(bottom:9),child:Text('${m['name']}: ${m['text']}',style:const TextStyle(color:Colors.white,fontSize:15)))])),Wrap(children:[for(final emoji in ['😊','🎲','👏','❤️','🎉'])IconButton(onPressed:game.busy?null:()=>game.perform('chat',{'text':emoji}),icon:Text(emoji,style:const TextStyle(fontSize:26)))]),Padding(padding:const EdgeInsets.all(12),child:Row(children:[Expanded(child:TextField(controller:input,maxLength:180,style:const TextStyle(color:_ludoInk567),decoration:const InputDecoration(hintText:'Mesaj yaz…',counterText:''))),IconButton(onPressed:game.busy?null:()async{final value=input.text.trim();if(value.isNotEmpty&&await game.perform('chat',{'text':value}))input.clear();},icon:const Icon(Icons.send_rounded,color:_ludoGold567))]))]))))));input.dispose();
 }
 Widget _footer(){
  final active=game.playing,seat=game.seat,myTurn=active&&seat==room['turn'];
  final inventory=seat<0?<String,dynamic>{}:Map<String,dynamic>.from((room['power'] as List)[seat] as Map);
  return Container(padding:const EdgeInsets.fromLTRB(16,10,16,12),decoration:const BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0x00372A77),Color(0xCC291D60)])),child:Column(mainAxisSize:MainAxisSize.min,children:[
   if(game.error.isNotEmpty)Container(margin:const EdgeInsets.only(bottom:9),padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),decoration:BoxDecoration(color:const Color(0xFF6B3C6C),borderRadius:BorderRadius.circular(13)),child:Row(children:[const Icon(Icons.info_outline,color:_ludoGold567,size:18),const SizedBox(width:8),Expanded(child:Text(game.error,style:const TextStyle(color:Colors.white,fontSize:12))),if(!game.terminal)IconButton(onPressed:()=>game.sync(),icon:const Icon(Icons.refresh_rounded,color:Colors.white,size:20))])),
   if(game.leaving)const Padding(padding:EdgeInsets.all(12),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2,color:_ludoGold567)),SizedBox(width:10),Text('Masadan ayrılınıyor…',style:TextStyle(color:Colors.white))]))
   else if(game.terminal)...[
    Text(game.detached?'Bu masadan ayrıldın':room['status']=='closed'?'Masa kapandı':_winner567(room),textAlign:TextAlign.center,style:const TextStyle(color:_ludoGold567,fontSize:17,fontWeight:FontWeight.w900)),const SizedBox(height:10),SizedBox(width:220,child:Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close)),
   ]else...[
    if(active)Row(children:[
     Container(width:42,height:42,decoration:BoxDecoration(shape:BoxShape.circle,border:Border.all(color:myTurn?_ludoGold567:Colors.white24,width:2)),alignment:Alignment.center,child:Text('${math.max(0,(((room['deadline'] as num?)??0)-DateTime.now().millisecondsSinceEpoch)~/1000)}',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900))),const SizedBox(width:10),
     Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(myTurn?'Sıra sende':'Rakibin oynuyor',style:const TextStyle(color:_ludoGold567,fontSize:16,fontWeight:FontWeight.w900)),Text(myTurn?(room['dice']==null?'Zara dokun':'Parlayan taşını seç'):'Sıranı bekle',style:const TextStyle(color:Colors.white70,fontSize:12))])),
    ])else Text(room['matchmaking']==true?'${game.joined}/${room['capacity']??2} oyuncu · Rakip aranıyor…':'${game.joined}/${room['capacity']??2} oyuncu · Arkadaşlarını davet et',style:const TextStyle(color:Colors.white70,fontSize:12)),
    if(game.waiting&&room['matchmaking']==true)Padding(padding:const EdgeInsets.only(top:10),child:Ngelx567GameButton(label:'Vazgeç',onPressed:_askLeave)),
    const SizedBox(height:10),Row(children:[IconButton(tooltip:'Emoji ve sohbet',onPressed:room.isEmpty?null:_chat,icon:const Icon(Icons.chat_bubble_outline_rounded,color:Colors.white)),
     if(room['mode']=='power')...[for(final item in [('control',Icons.casino_rounded,'Zar seç'),('double',Icons.double_arrow_rounded,'×2 mesafe'),('shield',Icons.shield_rounded,'Kalkan')])Expanded(child:Tooltip(message:item.$3,child:InkWell(onTap:active&&myTurn&&!game.busy&&(inventory[item.$1]??0)>0&&(item.$1!='control'||room['dice']==null)&&(item.$1!='double'||room['dice']!=null)?()=>_power(item.$1):null,borderRadius:BorderRadius.circular(30),child:Column(children:[Container(width:39,height:39,decoration:BoxDecoration(shape:BoxShape.circle,gradient:LinearGradient(colors:(inventory[item.$1]??0)>0?[const Color(0xFFADE5FF),const Color(0xFF5377DA)]:[const Color(0xFF777188),const Color(0xFF514B64)]),border:Border.all(color:Colors.white54),boxShadow:const [BoxShadow(color:Colors.black26,blurRadius:5,offset:Offset(0,2))]),child:Icon(item.$2,color:Colors.white,size:22)),Text('${inventory[item.$1]??0}',style:const TextStyle(color:_ludoGold567,fontSize:11,fontWeight:FontWeight.w800))])))),
     ]else const Expanded(child:Text('KLASİK',textAlign:TextAlign.center,style:TextStyle(color:Colors.white38,fontSize:11,letterSpacing:2))),
     IconButton(tooltip:'Arkadaş davet et',onPressed:game.waiting&&room['matchmaking']!=true?_invite:null,icon:Icon(Icons.person_add_alt_1_rounded,color:game.waiting?Colors.white:Colors.white24)),
    ]),
   ],
  ]));
 }
 @override Widget build(BuildContext context){
  final players=List<Map<String,dynamic>>.from((room['players'] as List? ?? []).map((p)=>Map<String,dynamic>.from(p as Map)));
  return Theme(data:ngelx567LudoTheme(),child:PopScope(canPop:_canClose,onPopInvokedWithResult:(didPop,result){if(!didPop)unawaited(_askLeave());},child:Scaffold(extendBodyBehindAppBar:false,
   appBar:AppBar(leading:IconButton(key:const ValueKey('ludo-back'),tooltip:'Masadan ayrıl',onPressed:game.leaving?null:_askLeave,icon:const Icon(Icons.arrow_back_rounded)),title:Text(room['team']==true?'Ludo · 2V2':room['mode']=='power'?'Ludo · Power':'Ludo · Klasik',style:const TextStyle(fontWeight:FontWeight.w900,fontSize:18)),actions:[IconButton(tooltip:'Oda kodunu kopyala',onPressed:()=>Clipboard.setData(ClipboardData(text:widget.id)),icon:const Icon(Icons.copy_rounded,size:20))]),
   body:_LudoBackdrop567(child:SafeArea(bottom:true,child:LayoutBuilder(builder:(context,box){
    final sideways=box.maxWidth>box.maxHeight*1.3&&box.maxWidth>550;
    final frame=Ngelx567Table(room:room,seat:game.seat,uid:game.uid,enabled:game.playing&&game.seat==room['turn']&&!game.busy&&!game.leaving,onToken:(token)=>game.perform('move',{'token':token}),onRoll:()=>game.perform('roll'),busy:game.busy);
    final wait=game.waiting&&!game.detached?Ngelx567WaitingPanel(room:room,uid:game.uid,canStart:game.canStart,busy:game.busy,onInvite:_invite,onStart:()=>game.perform('start'),compact:box.maxHeight<500):null;
    if(sideways)return Row(children:[Expanded(child:Padding(padding:const EdgeInsets.all(10),child:Stack(alignment:Alignment.center,children:[Center(child:AspectRatio(aspectRatio:.85,child:frame)),if(wait!=null)SizedBox(width:265,child:FittedBox(fit:BoxFit.scaleDown,child:SizedBox(width:265,child:wait)))]))),SizedBox(width:245,child:ListView(padding:const EdgeInsets.only(top:12),children:[_roomLabel567(widget.id),_footer()]))]);
    return Column(children:[_roomLabel567(widget.id),Expanded(child:LayoutBuilder(builder:(_,area)=>Stack(alignment:Alignment.center,children:[Padding(padding:const EdgeInsets.symmetric(horizontal:12),child:Center(child:AspectRatio(aspectRatio:.85,child:frame))),if(wait!=null)ConstrainedBox(constraints:BoxConstraints(maxWidth:math.min(320,area.maxWidth-34),maxHeight:area.maxHeight-8),child:SingleChildScrollView(child:wait)),if(room.isEmpty)const Center(child:CircularProgressIndicator(color:_ludoGold567))]))),if(players.isEmpty&&room.isEmpty)const Text('Masaya bağlanılıyor…',style:TextStyle(color:Colors.white70)),_footer()]);
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
  final side=math.min(box.maxWidth,math.max(60.0,box.maxHeight-80)),left=(box.maxWidth-side)/2,top=(box.maxHeight-side)/2;
  final turns=seat<0?0:(3-seat+4)%4,playing=room['status']=='playing';
  final players=List<dynamic>.from(room['players']??[]).where((p)=>p['left']!=true).toList();
  return Stack(clipBehavior:Clip.none,children:[
   Positioned(left:left,top:top,width:side,height:side,child:Container(decoration:BoxDecoration(borderRadius:BorderRadius.circular(13),border:Border.all(color:const Color(0xFFCFB6FF),width:2),boxShadow:const [BoxShadow(color:Color(0x770D082D),blurRadius:24,offset:Offset(0,10))]),child:ClipRRect(borderRadius:BorderRadius.circular(10),child:Ngelx565LudoBoard(room:room,seat:seat,enabled:enabled,onToken:onToken)))),
   for(final p in players)Builder(builder:(_){
    final color=(p['seat'] as num).toInt(),visual=(color+turns)%4,isLeft=visual==0||visual==3,isTop=visual==0||visual==1,isTurn=playing&&room['turn']==color,isMine=p['uid']==uid;
    final width=math.min(180.0,side*.57),photo='${p['photo']??''}';
    return Positioned(left:isLeft?left:left+side-width,top:isTop?top-40:top+side+4,width:width,height:36,child:Row(mainAxisAlignment:isLeft?MainAxisAlignment.start:MainAxisAlignment.end,children:[
     if(!isLeft&&isTurn)...[GestureDetector(onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:(room['dice'] as num?)?.toInt(),size:32,busy:busy&&isMine)),const SizedBox(width:6)],
     Container(width:34,height:34,padding:const EdgeInsets.all(2),decoration:BoxDecoration(shape:BoxShape.circle,color:isTurn?_ludoGold567:ngelx565LudoColors[color],boxShadow:[BoxShadow(color:(isTurn?_ludoGold567:Colors.black).withValues(alpha:.25),blurRadius:8)]),child:CircleAvatar(backgroundColor:const Color(0xFF8273AB),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?Icon(p['bot']==true?Icons.smart_toy_rounded:Icons.person_rounded,size:20,color:Colors.white):null)),const SizedBox(width:5),
     Flexible(child:Text(isMine?'Sen':'${p['name']}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white70,fontWeight:FontWeight.w800,fontSize:11))),
     if(isLeft&&isTurn)...[const SizedBox(width:6),GestureDetector(key:isMine?const ValueKey('ludo-dice'):null,onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:(room['dice'] as num?)?.toInt(),size:32,busy:busy&&isMine))],
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
  if(value==null){final tp=TextPainter(text:TextSpan(text:'?',style:TextStyle(color:const Color(0xFF5D458E),fontSize:size.width*.58,fontWeight:FontWeight.w900)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));return;}
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
 late final AnimationController motion;late int from;
 @override void initState(){super.initState();from=widget.position;motion=AnimationController(vsync:this,duration:const Duration(milliseconds:420))..value=1;}
 @override void didUpdateWidget(covariant _MovingPawn567 old){super.didUpdateWidget(old);if(old.position!=widget.position){from=old.position;motion.duration=Duration(milliseconds:math.min(1000,math.max(280,(widget.position-from).abs()*105)));motion.forward(from:0);}}
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>AnimatedBuilder(animation:motion,builder:(_,__){
  final p=ngelx565Rotate(ngelx567MovingPoint(widget.seat,widget.token,from,widget.position,motion.value),widget.turns),c=widget.cell;
  return Positioned(left:(p.dx+.5)*c-c*.56,top:(p.dy+.5)*c-c*.8624,width:c*1.12,height:c*1.12,child:Semantics(label:'${widget.token+1}. taş',button:widget.onTap!=null,child:GestureDetector(behavior:HitTestBehavior.opaque,onTap:widget.onTap,child:CustomPaint(painter:_PawnPainter567(ngelx565LudoColors[widget.seat],widget.highlight)))));
 });
}
class _PawnPainter567 extends CustomPainter {
 final Color color;final bool highlight;const _PawnPainter567(this.color,this.highlight);
 @override void paint(Canvas canvas,Size size){
  final w=size.width,h=size.height,rect=Offset.zero&size;
  if(highlight)canvas.drawCircle(Offset(w*.5,h*.62),w*.47,Paint()..shader=RadialGradient(colors:[_ludoGold567.withValues(alpha:.65),_ludoGold567.withValues(alpha:0)]).createShader(rect));
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.52,h*.87),width:w*.68,height:h*.2),Paint()..color=Colors.black.withValues(alpha:.22));
  final dark=Color.lerp(color,Colors.black,.28)!,light=Color.lerp(color,Colors.white,.45)!;
  final body=Path()..moveTo(w*.39,h*.32)..cubicTo(w*.43,h*.48,w*.31,h*.6,w*.24,h*.75)..quadraticBezierTo(w*.5,h*.91,w*.76,h*.75)..cubicTo(w*.69,h*.6,w*.57,h*.48,w*.61,h*.32)..close();
  final shader=LinearGradient(colors:[light,color,dark],stops:const [0,.43,1]).createShader(rect);
  canvas.drawPath(body,Paint()..shader=shader);
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.77),width:w*.66,height:h*.21),Paint()..shader=shader);
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.73),width:w*.57,height:h*.12),Paint()..color=light.withValues(alpha:.65));
  canvas.drawCircle(Offset(w*.5,h*.27),w*.21,Paint()..shader=RadialGradient(center:const Alignment(-.45,-.5),colors:[Color.lerp(color,Colors.white,.7)!,color,dark],stops:const [0,.55,1]).createShader(Rect.fromCircle(center:Offset(w*.5,h*.27),radius:w*.22)));
  canvas.drawOval(Rect.fromCenter(center:Offset(w*.43,h*.21),width:w*.12,height:h*.07),Paint()..color=Colors.white.withValues(alpha:.6));
  if(highlight)canvas.drawOval(Rect.fromCenter(center:Offset(w*.5,h*.81),width:w*.77,height:h*.23),Paint()..style=PaintingStyle.stroke..strokeWidth=1.5..color=_ludoGold567);
 }
 @override bool shouldRepaint(covariant _PawnPainter567 old)=>old.color!=color||old.highlight!=highlight;
}
class Ngelx565BoardPainter extends CustomPainter {
 final int turns;final bool power;
 const Ngelx565BoardPainter({this.turns=0,this.power=false});
 @override void paint(Canvas canvas,Size size){
  final c=size.width/15,paint=Paint()..isAntiAlias=true;
  canvas.save();canvas.translate(size.width/2,size.height/2);canvas.rotate(turns*math.pi/2);canvas.translate(-size.width/2,-size.height/2);
  canvas.drawRect(Offset.zero&size,paint..color=const Color(0xFFFAF8F1));
  const bases=[Offset(0,0),Offset(9,0),Offset(9,9),Offset(0,9)];
  for(var seat=0;seat<4;seat++){
   final color=ngelx565LudoColors[seat],base=Rect.fromLTWH(bases[seat].dx*c,bases[seat].dy*c,6*c,6*c);
   canvas.drawRect(base,paint..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.white,.15)!,color,Color.lerp(color,Colors.black,.1)!]).createShader(base));paint.shader=null;
   final inner=RRect.fromRectAndRadius(base.deflate(c*.73),Radius.circular(c*.52));canvas.drawShadow(Path()..addRRect(inner),Colors.black.withValues(alpha:.16),c*.18,false);
   canvas.drawRRect(inner,paint..color=Color.lerp(color,Colors.white,.87)!);
   canvas.drawRRect(inner.deflate(.7),paint..style=PaintingStyle.stroke..strokeWidth=1..color=Colors.white.withValues(alpha:.75));paint.style=PaintingStyle.fill;
   for(var token=0;token<4;token++){
    final point=ngelx565TokenPoint(seat,token,-1),center=Offset((point.dx+.5)*c,(point.dy+.5)*c),socket=Rect.fromCircle(center:center,radius:c*.57);
    canvas.drawCircle(center,c*.57,paint..shader=RadialGradient(center:const Alignment(0,.4),colors:[color.withValues(alpha:.12),color.withValues(alpha:.25)]).createShader(socket));paint.shader=null;
    canvas.drawArc(socket,-math.pi*.1,math.pi*1.2,false,paint..style=PaintingStyle.stroke..strokeWidth=.8..color=color.withValues(alpha:.24));paint.style=PaintingStyle.fill;
   }
   for(var h=1;h<=5;h++){final at=ngelx565Rotate(Offset(h.toDouble(),7),seat),rect=Rect.fromLTWH(at.dx*c,at.dy*c,c,c);canvas.drawRect(rect,paint..color=Color.lerp(color,Colors.white,.28)!);canvas.drawRect(rect.deflate(.3),paint..style=PaintingStyle.stroke..strokeWidth=.45..color=Color.lerp(color,Colors.black,.15)!);paint.style=PaintingStyle.fill;}
  }
  final track=ngelx565Track();const safe=[0,8,13,21,26,34,39,47];
  for(var i=0;i<52;i++){
   final at=track[i],rect=Rect.fromLTWH(at.dx*c,at.dy*c,c,c);canvas.drawRect(rect,paint..color=i%13==0?ngelx565LudoColors[i~/13]:const Color(0xFFFFFEF9));
   canvas.drawRect(rect.deflate(.25),paint..style=PaintingStyle.stroke..strokeWidth=.5..color=const Color(0xFFB7B5C9));paint.style=PaintingStyle.fill;
   if(safe.contains(i)){
    final tp=TextPainter(text:TextSpan(text:'★',style:TextStyle(color:i%13==0?Colors.white:const Color(0xFFA8A0C4),fontSize:c*.65,fontWeight:FontWeight.w900)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));
   }else if(power&&[4,17,30,43].contains(i)){
    canvas.drawRRect(RRect.fromRectAndRadius(rect.deflate(c*.12),Radius.circular(c*.15)),paint..color=const Color(0xFFFFD558));
    final tp=TextPainter(text:TextSpan(text:'+1',style:TextStyle(color:const Color(0xFF97651C),fontSize:c*.45,fontWeight:FontWeight.w900)),textDirection:TextDirection.ltr)..layout();tp.paint(canvas,rect.center-Offset(tp.width/2,tp.height/2));
   }
  }
  final corners=[Offset(6*c,6*c),Offset(9*c,6*c),Offset(9*c,9*c),Offset(6*c,9*c)];
  for(var i=0;i<4;i++){final path=Path()..moveTo(7.5*c,7.5*c)..lineTo(corners[(i+3)%4].dx,corners[(i+3)%4].dy)..lineTo(corners[i].dx,corners[i].dy)..close();canvas.drawPath(path,paint..color=ngelx565LudoColors[i]);}
  canvas.drawCircle(Offset(7.5*c,7.5*c),c*.32,paint..color=Colors.white.withValues(alpha:.25));
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
  return ListView(padding:EdgeInsets.only(bottom:MediaQuery.viewPaddingOf(context).bottom+24),children:[const Padding(padding:EdgeInsets.all(16),child:Text('Sohbeti seç; daveti mesaj alanında görüp Gönder’e basabilirsin.')),for(final d in docs)if(d.data()['isGroup']==true)ListTile(leading:const Icon(Icons.groups_rounded,color:mor),title:Text((d.data()['groupName']??'Grup').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d))else Builder(builder:(_){final members=List<String>.from(d.data()['members']??[]),other=members.firstWhere((u)=>u!=me,orElse:()=>'');return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:other.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(other).get(),builder:(_,u)=>ListTile(leading:const Icon(Icons.person_rounded,color:mor),title:Text((u.data?.data()?['displayName']??u.data?.data()?['username']??'Sohbet').toString()),trailing:const Icon(Icons.chevron_right),onTap:()=>open(d)));})]);
 })));
}
class Ngelx565LudoInviteCard extends StatelessWidget{
 final String id;final bool mine;final VoidCallback onLongPress;
 const Ngelx565LudoInviteCard({super.key,required this.id,required this.mine,required this.onLongPress});
 @override Widget build(BuildContext context)=>Align(alignment:mine?Alignment.centerRight:Alignment.centerLeft,child:GestureDetector(onLongPress:onLongPress,child:Container(width:260,margin:const EdgeInsets.symmetric(vertical:6,horizontal:4),padding:const EdgeInsets.all(16),decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFF7953E8),Color(0xFF3989EE)]),borderRadius:BorderRadius.circular(22)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Row(children:[Icon(Icons.casino_rounded,color:Colors.white,size:34),SizedBox(width:10),Text('Ludo daveti',style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900))]),const SizedBox(height:8),Text('Oda: $id',style:const TextStyle(color:Colors.white70,fontSize:11)),const Text('Aynı masada birlikte oyna.',style:TextStyle(color:Colors.white)),const SizedBox(height:10),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.white,foregroundColor:mor),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(id:id))),child:const Text('Katıl'))]))));
}
