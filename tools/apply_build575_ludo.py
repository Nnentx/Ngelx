"""Build575 additive Ludo Auto UI + premium pawn finishing.
Runs only on verified Build574 assembled source. Fails closed on mismatched anchors.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'app/lib/build565_ludo.dart'
s=p.read_text(encoding='utf-8')
def swap(old,new):
 global s
 count=s.count(old)
 if count!=1:raise RuntimeError(f'Build575 mismatch ({count}): {old[:120]}')
 s=s.replace(old,new,1)

swap('class Ngelx573WalletBar extends StatelessWidget{',"""class Ngelx575AutoBadge extends StatelessWidget {
 final bool enabled;final VoidCallback? onPressed;
 const Ngelx575AutoBadge({super.key,required this.enabled,required this.onPressed});
 @override Widget build(BuildContext context)=>Semantics(
  label:enabled?'Auto açık, kapatmak için dokun':'Auto kapalı, açmak için dokun',
  button:true,child:Tooltip(message:enabled?'Otomatikten çık':'Otomatik oyna',
   child:InkWell(key:const ValueKey('ludo-auto-toggle'),onTap:onPressed,borderRadius:BorderRadius.circular(30),
    child:Container(width:46,height:47,decoration:BoxDecoration(shape:BoxShape.circle,
      color:enabled?const Color(0xFF0F564B):const Color(0xFF1A285B),
      border:Border.all(color:enabled?const Color(0xFF50F0A1):const Color(0xFF38D6EE),width:2),
      boxShadow:[BoxShadow(color:(enabled?const Color(0xFF50F0A1):const Color(0xFF38D6EE)).withValues(alpha:.27),blurRadius:6)]),
      child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
       Icon(enabled?Icons.check_circle:Icons.autorenew_rounded,color:enabled?const Color(0xFF5CF7AB):Colors.white,size:19),
       Text('Auto',style:const TextStyle(fontSize:10,color:Colors.white,fontWeight:FontWeight.w900))])))));
}
class Ngelx573WalletBar extends StatelessWidget{""")
swap('class Ngelx573WalletBar extends StatelessWidget{',"""class Ngelx575AnimatedBalance extends StatelessWidget{
 final dynamic amount;
 const Ngelx575AnimatedBalance({super.key,required this.amount});
 @override Widget build(BuildContext context){
  final n=amount is num?(amount as num).toDouble():null;
  if(n==null)return const Text('—',style:TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900));
  return TweenAnimationBuilder<double>(
   tween:Tween<double>(begin:0,end:n),duration:const Duration(milliseconds:900),
   curve:Curves.easeOutCubic,
   builder:(_,value,__)=>
    Text(value.round().toString(),style:const TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900)));
 }
}
class Ngelx573WalletBar extends StatelessWidget{""")
swap("Text(amount is num?amount.toInt().toString():'—',style:const TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900))","Ngelx575AnimatedBalance(amount:amount)")
swap("int capacity=2;bool team=false,busy=false,joining=false;String play='friends',difficulty='medium',mode='classic',error='';",
"""int capacity=2;bool team=false,busy=false,joining=false,giftBusy575=false;
 String giftMessage575='';String play='friends',difficulty='medium',mode='classic',error='';""")
swap(' Future<void> refresh()async{',""" Future<void> _myStats575()async{
  try{
   final stats=await (widget.request??ngelx565LudoRequest)({'action':'wallet'});
   if(!mounted)return;
   final entries=<({String name,dynamic value})>[
    (name:'Çip',value:stats['chips']),(name:'Elmas',value:stats['gems']),
    (name:'Seviye',value:stats['level']),(name:'XP',value:stats['xp']),
    (name:'Galibiyet',value:stats['wins']),(name:'Mağlubiyet',value:stats['losses']),
    (name:'Galibiyet serisi',value:stats['streak'])];
   await showDialog<void>(context:context,builder:(c)=>Theme(
    data:ngelx567LudoTheme(),child:AlertDialog(title:const Text('Ludo istatistiklerim'),
     content:Column(mainAxisSize:MainAxisSize.min,children:[
       for(final entry in entries)Padding(
        padding:const EdgeInsets.symmetric(vertical:5),
        child:Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
         Text(entry.name,style:const TextStyle(color:Color(0xFF453C69),fontWeight:FontWeight.w700)),
         const SizedBox(width:12),
         Text('${entry.value is num?entry.value.toInt():0}',
          style:const TextStyle(color:Color(0xFF5C42AF),fontWeight:FontWeight.w900)),
        ]))]),
     actions:[TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Kapat'))])));
  }catch(e){if(mounted)setState(()=>giftMessage575='İstatistikler alınamadı: $e');}
 }
 Future<void> refresh()async{""")
swap(' Future<void> refresh()async{',""" Future<void> _claim575(String action)async{
  if(busy||giftBusy575)return;
  setState(()=>giftBusy575=true);
  try{
   final reward=await (widget.request??ngelx565LudoRequest)({'action':action});
   final claimed=reward['claimed']==true;
   final count=(reward['chipReward'] as num?)?.toInt()??0;
   if(mounted)setState(()=>giftMessage575=claimed?'+$count çip kazandın! 🎁':'Bu ödülü zaten topladın; daha sonra yeniden dene.');
  }catch(e){if(mounted)setState(()=>giftMessage575=e.toString().replaceFirst('Exception: ',''));}
  finally{if(mounted)setState(()=>giftBusy575=false);}
 }
 Future<void> refresh()async{""")
swap("const Center(child:Text('Arkadaşlarınla aynı masada',style:TextStyle(color:Colors.white70,fontSize:14))),const SizedBox(height:25),",
"""const Center(child:Text('Arkadaşlarınla aynı masada',style:TextStyle(color:Colors.white70,fontSize:14))),
  const SizedBox(height:12),
  Wrap(alignment:WrapAlignment.center,spacing:8,runSpacing:4,children:[
   OutlinedButton.icon(key:const ValueKey('ludo-daily-gift'),onPressed:busy||giftBusy575?null:()=>_claim575('daily_reward'),
    icon:const Icon(Icons.card_giftcard_rounded,size:19),label:const Text('Günlük hediye')),
   OutlinedButton.icon(key:const ValueKey('ludo-timed-chest'),onPressed:busy||giftBusy575?null:()=>_claim575('chest_reward'),
    icon:const Icon(Icons.inventory_2_rounded,size:19),label:const Text('Ödül sandığı')),
   OutlinedButton.icon(key:const ValueKey('ludo-profile-stats'),onPressed:busy?null:_myStats575,
    icon:const Icon(Icons.person_outline_rounded,size:19),label:const Text('Puanlarım')),
  ]),
  if(giftMessage575.isNotEmpty)Padding(padding:const EdgeInsets.only(top:4),child:Text(giftMessage575,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFFFFE28D),fontWeight:FontWeight.w700,fontSize:12))),
  const SizedBox(height:15),""")
swap("bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;",
"""bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;bool _soundOn575=true;""")
swap('  if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();',
"""  if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();unawaited(_restoreSound575());""")
swap(' void _startPoll(){',""" Future<void> _restoreSound575()async{
  final p=await SharedPreferences.getInstance();
  if(mounted)setState(()=>_soundOn575=p.getBool('ngelx_ludo_sound')??true);
 }
 Future<void> _toggleSound575()async{
  final next=!_soundOn575;
  setState(()=>_soundOn575=next);
  final p=await SharedPreferences.getInstance();
  await p.setBool('ngelx_ludo_sound',next);
 }
 void _soundTap575(){if(_soundOn575)unawaited(SystemSound.play(SystemSoundType.click));}
 void _startPoll(){""")
swap("onToken:(token)=>game.perform('move',{'token':token}),",
"""onToken:(token){_soundTap575();unawaited(game.perform('move',{'token':token}));},""")
swap("IconButton(tooltip:'Oda kodunu kopyala',",
"""IconButton(key:const ValueKey('ludo-sound-toggle'),
    tooltip:_soundOn575?'Oyun sesini kapat':'Oyun sesini aç',
    onPressed:_toggleSound575,
    icon:Icon(_soundOn575?Icons.volume_up_rounded:Icons.volume_off_rounded,size:19)),
    IconButton(tooltip:'Oda kodunu kopyala',""")
swap("bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;bool _soundOn575=true;",
"""bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;bool _soundOn575=true;
 int? _earnedChips575,_earnedXp575;String? _recentPickup575;""")
swap("  if(mounted&&!_chatOpen)setState((){});\n  if(mounted&&!widget.watch)unawaited(_autoSingleMove574());",
"""  final reward=room['reward'];
  if(reward is Map&&reward['matchId']==widget.id){
   _earnedChips575=(reward['chips'] as num?)?.toInt();
   _earnedXp575=(reward['xp'] as num?)?.toInt();
  }
  final pickup=room['pickup']??room['bonusPickup'];
  if(pickup is Map){
   final receipt='${pickup['seat']}:${pickup['cell']}:${pickup['at']}';
   if(_recentPickup575!=null&&receipt!=_recentPickup575&&_soundOn575){
    unawaited(SystemSound.play(SystemSoundType.click));
   }
   _recentPickup575=receipt;
  }
  if(mounted&&!_chatOpen)setState((){});
  if(mounted&&!widget.watch)unawaited(_autoSingleMove574());""")
swap("Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close),",
"""if(_earnedChips575!=null||_earnedXp575!=null)Padding(
    padding:const EdgeInsets.symmetric(vertical:7),
    child:Container(key:const ValueKey('ludo-verified-match-reward'),
     padding:const EdgeInsets.symmetric(horizontal:12,vertical:9),
     decoration:BoxDecoration(
       borderRadius:BorderRadius.circular(14),
       gradient:const LinearGradient(colors:[Color(0xFF204D79),Color(0xFF2C317A)]),
       border:Border.all(color:const Color(0xFFFFDC72),width:1.4)),
     child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
       const Icon(Icons.emoji_events_rounded,color:Color(0xFFFFD85A),size:20),
       const SizedBox(width:8),
       if(_earnedChips575!=null)Text('+${_earnedChips575!} çip',
         style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:13)),
       if(_earnedXp575!=null)...[const SizedBox(width:10),
        Text('+${_earnedXp575!} XP',
         style:const TextStyle(color:Color(0xFF9AFFE6),fontWeight:FontWeight.w900,fontSize:13))],
     ]))),
   Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close),""")
swap("int? _earnedChips575,_earnedXp575;String? _recentPickup575;",
"""int? _earnedChips575,_earnedXp575;String? _recentPickup575;
 int _connectionFailures575=0;""")
swap("  final reward=room['reward'];",
"""  if(game.error.isNotEmpty){_connectionFailures575=math.min(4,_connectionFailures575+1);}
  else{_connectionFailures575=0;}
  final reward=room['reward'];""")
swap("void _startPoll(){poll?.cancel();poll=Timer.periodic(Duration(seconds:widget.watch?4:1),(tick){if(_chatOpen&&tick.tick%3!=0)return;if(!game.terminal)unawaited(game.sync());});}",
"""void _startPoll(){poll?.cancel();poll=Timer.periodic(Duration(seconds:widget.watch?4:1),(tick){
  if(_chatOpen&&tick.tick%3!=0)return;
  final gap=math.min(8,1<<_connectionFailures575);
  if(tick.tick%gap!=0)return;
  if(!game.terminal&&!game.busy)unawaited(game.sync());
 });}""")
swap("if(game.error.isNotEmpty)TextButton.icon(onPressed:()=>game.sync(),icon:const Icon(Icons.refresh),label:Text(game.error)),",
"""if(game.error.isNotEmpty)Padding(padding:const EdgeInsets.only(bottom:5),
    child:OutlinedButton.icon(key:const ValueKey('ludo-reconnect'),
     onPressed:game.busy?null:()=>unawaited(game.sync()),
     icon:const Icon(Icons.wifi_off_rounded,size:17),
     label:const Text('Bağlantıyı yenile'),
     style:OutlinedButton.styleFrom(foregroundColor:const Color(0xFFFFE9AC)))),""")
# Player card: the already-visible table portraits become tappable without moving any board tile.
swap("final ValueChanged<int> onToken;final VoidCallback onRoll;",
"""final ValueChanged<int> onToken;final VoidCallback onRoll;
 final ValueChanged<Map<String,dynamic>>? onPlayerTap;""")
swap("required this.onToken,required this.onRoll,required this.busy});",
"""required this.onToken,required this.onRoll,required this.busy,this.onPlayerTap});""")
swap("Container(width:38,height:38,padding:const EdgeInsets.all(2)",
"""GestureDetector(key:ValueKey('ludo-player-${p['uid']}'),
  onTap:onPlayerTap==null?null:()=>onPlayerTap!(Map<String,dynamic>.from(p as Map)),
  child:Container(width:38,height:38,padding:const EdgeInsets.all(2)""")
swap("size:20,color:Colors.white):null)),const SizedBox(width:5),",
"size:20,color:Colors.white):null))),const SizedBox(width:5),")
swap("onToken:(token){_soundTap575();unawaited(game.perform('move',{'token':token}));},",
"""onPlayerTap:widget.watch?null:_playerCard575,
    onToken:(token){_soundTap575();unawaited(game.perform('move',{'token':token}));},""")
swap(' Future<void> _autoSingleMove574()async{',""" Future<void> _playerCard575(Map<String,dynamic> person)async{
  if(_chatOpen||game.busy)return;
  final theirId=person['uid']?.toString()??'',isMine=theirId==game.uid,bot=person['bot']==true;
  final nickname=person['name']?.toString()??'Oyuncu';
  Map<String,dynamic> items={};
  try{
   if(!isMine&&!bot){
    final result=await (widget.request??ngelx565LudoRequest)({'action':'gift_catalog'});
    if(result['gifts'] is Map)items=Map<String,dynamic>.from(result['gifts'] as Map);
   }
  }catch(_){if(!mounted)return;}
  if(!mounted)return;
  final selected=await showDialog<String>(context:context,builder:(c)=>Theme(
   data:ngelx567LudoTheme(),child:AlertDialog(
    title:Text(nickname),
    content:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
     Text('Seviye ${(person['level'] as num?)?.toInt()??1}'),
     const SizedBox(height:8),
     if(bot)const Text('Makine oyuncusu'),
     if(isMine)const Text('Kendi oyuncu profilin'),
     if(!isMine&&!bot&&items.isEmpty)const Text('Hediye listesi şu anda açılamıyor.'),
     if(!isMine&&!bot)for(final e in items.entries)
      ListTile(contentPadding:EdgeInsets.zero,
       leading:Text((e.value is Map?e.value['emoji']:null)?.toString()??'🎁',
        style:const TextStyle(fontSize:26)),
       title:Text((e.value is Map?e.value['label']:null)?.toString()??e.key),
       subtitle:Text('${(e.value is Map?e.value['chips']:null)??0} çip'),
       onTap:()=>Navigator.pop(c,e.key)),
    ]),
    actions:[TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Kapat'))])));
  if(!mounted||selected==null)return;
  final ok=await game.perform('gift',{'to':theirId,'kind':selected});
  if(!mounted)return;
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
   ok?(room['giftAlreadySent']==true?'Bu hediye daha önce gönderilmiş.':'Hediye gönderildi 🎁'):
   (game.error.isEmpty?'Hediye gönderilemedi.':game.error))));
 }
 Future<void> _autoSingleMove574()async{""")
swap("if(game.error.isNotEmpty)Padding(padding:const EdgeInsets.only(bottom:5),",
"""if(room['gifts'] is List&&(room['gifts'] as List).isNotEmpty)Padding(
    padding:const EdgeInsets.only(bottom:5),
    child:Text('${(room['gifts'] as List).last['emoji']??'🎁'} ${(room['gifts'] as List).last['fromName']??'Oyuncu'} → ${(room['gifts'] as List).last['toName']??'Oyuncu'}',
     maxLines:1,overflow:TextOverflow.ellipsis,
     style:const TextStyle(fontSize:11,color:Color(0xFFFFE28D),fontWeight:FontWeight.w800))),
   if(game.error.isNotEmpty)Padding(padding:const EdgeInsets.only(bottom:5),""")
swap(' Future<void> _autoSingleMove574()async{',""" void _tapAuto575(bool active){
  if(widget.watch||game.busy||!game.playing||game.seat<0)return;
  unawaited(game.perform('auto',{'enabled':!active}));
 }
 bool _rematching575=false;
 Future<void> _rematch575()async{
  if(_rematching575||widget.watch)return;
  _rematching575=true;
  try{
   final fresh=await (widget.request??ngelx565LudoRequest)({'action':'rematch','id':widget.id});
   if(!mounted)return;
   Navigator.of(context).pushReplacement(MaterialPageRoute(builder:(_)=>Ngelx565LudoRoom(
    id:fresh['id'].toString(),initial:fresh,request:widget.request,userId:widget.userId)));
  }catch(e){
   if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
    content:Text('Rövanş oluşturulamadı: $e')));
  }finally{_rematching575=false;}
 }
 Future<void> _autoSingleMove574()async{""")
swap("Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close),",
"""if(!widget.watch&&!game.detached&&room['status']=='finished'&&room['botGame']!=true)...[
    Ngelx567GameButton(label:'Rövanş',onPressed:game.busy?null:_rematch575),
    const SizedBox(height:8),
   ],
   Ngelx567GameButton(label:'Lobiye dön',gold:true,onPressed:_close),""")
swap("final inventory=seat<0?<String,dynamic>{}:Map<String,dynamic>.from((room['power'] as List)[seat] as Map);",
"""final inventory=seat<0?<String,dynamic>{}:Map<String,dynamic>.from((room['power'] as List)[seat] as Map);
  final autoSeats=room['autoSeats'];
  final auto=autoSeats is Map&&autoSeats[seat.toString()]==true;""")
swap("Column(mainAxisSize:MainAxisSize.min,children:[Ngelx570Clock(paused:_chatOpen,deadline:(room['deadline'] as num?)?.toInt()??0,active:myTurn),const SizedBox.shrink()]),",
"""if(!widget.watch)...[Ngelx575AutoBadge(enabled:auto,onPressed:()=>_tapAuto575(auto)),const SizedBox(width:5)],
     Column(mainAxisSize:MainAxisSize.min,children:[Ngelx570Clock(paused:_chatOpen,deadline:(room['deadline'] as num?)?.toInt()??0,active:myTurn),const SizedBox.shrink()]),""")
swap("final src=Rect.fromLTWH((seat%2)*w+w*.095,(seat~/2)*h+h*.035,w*.81,h*.91);",
"""final src=Rect.fromLTWH((seat%2)*w+w*.065,(seat~/2)*h+h*.025,w*.87,h*.94);""")
swap("final dst=Offset.zero&size;\n  canvas.drawImageRect(atlas,src,dst,Paint()..filterQuality=FilterQuality.high..isAntiAlias=true);",
"""final dst=Offset.zero&size;
  canvas.drawOval(Rect.fromLTWH(size.width*.20,size.height*.79,size.width*.60,size.height*.15),
    Paint()..color=Colors.black.withValues(alpha:.34)..maskFilter=const MaskFilter.blur(BlurStyle.normal,2.3));
  canvas.drawImageRect(atlas,src,dst,Paint()..filterQuality=FilterQuality.high..isAntiAlias=true);""")
swap('widget.stackCount > 1 ? 0.49 : 0.98','widget.stackCount > 1 ? 0.52 : 0.98')
p.write_text(s,encoding='utf-8')
pub=root/'app/pubspec.yaml'
version=pub.read_text(encoding='utf-8')
assert 'version: 1.0.344+574' in version
pub.write_text(version.replace('version: 1.0.344+574','version: 1.0.345+575',1),encoding='utf-8')
print('Build575 frontend ready: persistent Auto on/off, updated painted pawn depth, existing NgelX layout retained')
