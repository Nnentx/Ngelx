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
    (name:'Toplanan hediye',value:stats['receivedGifts'] is Map?(stats['receivedGifts'] as Map).values.whereType<num>().fold<int>(0,(sum,count)=>sum+count.toInt()):0),
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
  if(mounted)setState((){_soundOn575=p.getBool('ngelx_ludo_sound')??true;_soundReady575=true;});
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
# Translate gift transaction results without pretending a network failure occurred.
swap("errors[code]??'Oyun bağlantısı kurulamadı. Tekrar dene.'",
"""ngelx575GiftError(code)??errors[code]??'Oyun bağlantısı kurulamadı. Tekrar dene.'""")
swap('class Ngelx573WalletBar extends StatelessWidget{',
"""String? ngelx575GiftError(dynamic raw){
 switch(raw){
  case 'insufficient_chips':return 'Hediye için yeterli çipin yok.';
  case 'gift_slow_down':return 'Yeni hediye göndermek için birkaç saniye bekle.';
  case 'gift_room_limit':return 'Bu masadaki hediye sınırına ulaştın.';
  case 'cannot_gift_self':return 'Kendine hediye gönderemezsin.';
  case 'invalid_gift':return 'Bu hediye artık kullanılamıyor.';
  case 'gift_player_unavailable':return 'Bu oyuncuya şu anda hediye gönderilemiyor.';
  case 'gift_store_unavailable':return 'Hediye sistemi geçici olarak kullanılamıyor.';
  default:return null;
 }
}
class Ngelx573WalletBar extends StatelessWidget{""")

# Win/lose visual feedback stays inside the existing end-of-match footer.
swap('class Ngelx573WalletBar extends StatelessWidget{',"""class Ngelx575VictoryBanner extends StatelessWidget {
 final bool won;
 const Ngelx575VictoryBanner({super.key,required this.won});
 @override Widget build(BuildContext context)=>TweenAnimationBuilder<double>(
  tween:Tween<double>(begin:.88,end:1),
  duration:const Duration(milliseconds:750),
  curve:Curves.elasticOut,
  builder:(context,value,child)=>Transform.scale(scale:value,child:child),
  child:Container(
   key:const ValueKey('ludo-result-celebration'),
   width:double.infinity,padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
   decoration:BoxDecoration(borderRadius:BorderRadius.circular(17),
    gradient:LinearGradient(colors:won?
     [const Color(0xFF6541D8),const Color(0xFF2D358D)]:
     [const Color(0xFF373B69),const Color(0xFF232B56)]),
    border:Border.all(color:won?const Color(0xFFFFDE72):const Color(0xFF8184B6),width:1.4),
    boxShadow:[BoxShadow(color:(won?const Color(0xFFFFC85D):Colors.black)
     .withValues(alpha:.2),blurRadius:13,offset:const Offset(0,3))]),
   child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
    Icon(won?Icons.emoji_events_rounded:Icons.sports_esports_rounded,
     size:25,color:won?const Color(0xFFFFDA62):Colors.white70),
    const SizedBox(width:9),
    Flexible(child:Text(won?'Tebrikler, kazandın!':'Oyun sona erdi',
     maxLines:2,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,
     style:const TextStyle(color:Colors.white,fontSize:15,fontWeight:FontWeight.w900))),
    if(won)...[const SizedBox(width:6),
      const Icon(Icons.auto_awesome_rounded,size:18,color:Color(0xFFFFE594))],
   ])));
}
class Ngelx573WalletBar extends StatelessWidget{""")
swap("Text(game.detached?'Bu masadan ayrıldın':room['status']=='closed'?'Masa kapandı':_winner567(room),style:const TextStyle(color:_ludoGold567,fontWeight:FontWeight.w900,fontSize:17)),",
"""if(!widget.watch&&!game.detached&&game.seat>=0&&room['status']=='finished')...[
    Ngelx575VictoryBanner(won:room['winner']!=null&&
      (room['team']==true?game.seat%2==room['winner']:game.seat==room['winner'])),
    const SizedBox(height:7),
   ],
   Text(game.detached?'Bu masadan ayrıldın':room['status']=='closed'?'Masa kapandı':_winner567(room),
    textAlign:TextAlign.center,style:const TextStyle(color:_ludoGold567,fontWeight:FontWeight.w900,fontSize:17)),""")
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
  Map<String,dynamic> items={};bool alreadyBlocked575=false;
  try{
   if(!isMine&&!bot){
    final myWallet=await (widget.request??ngelx565LudoRequest)({'action':'wallet'});
    alreadyBlocked575=(myWallet['blockedUsers'] is List)&&
      (myWallet['blockedUsers'] as List).contains(theirId);
    final result=await (widget.request??ngelx565LudoRequest)({'action':'gift_catalog'});
    if(result['gifts'] is Map)items=Map<String,dynamic>.from(result['gifts'] as Map);
   }
  }catch(_){if(!mounted)return;}
  if(!mounted)return;
  final selected=await showDialog<String>(context:context,builder:(c)=>Theme(
   data:ngelx567LudoTheme(),child:AlertDialog(
    title:Text(nickname),
    content:ConstrainedBox(constraints:const BoxConstraints(maxHeight:360),
     child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,
     crossAxisAlignment:CrossAxisAlignment.start,children:[
     Text('Seviye ${(person['level'] as num?)?.toInt()??1}'),
     const SizedBox(height:8),
     if(bot)const Text('Makine oyuncusu'),
     if(isMine)const Text('Kendi oyuncu profilin'),
     if(!isMine&&!bot&&items.isEmpty)const Text('Hediye listesi şu anda açılamıyor.'),
     if(alreadyBlocked575)const Text('Bu oyuncu Ludo içinde engellendi.',style:TextStyle(color:Color(0xFFD34D66))),
     if(!isMine&&!bot)for(final e in items.entries)
      ListTile(contentPadding:EdgeInsets.zero,
       leading:Text((e.value is Map?e.value['emoji']:null)?.toString()??'🎁',
        style:const TextStyle(fontSize:26)),
       title:Text((e.value is Map?e.value['label']:null)?.toString()??e.key),
       subtitle:Text('${(e.value is Map?e.value['chips']:null)??0} çip'),
       onTap:alreadyBlocked575?null:()=>Navigator.pop(c,e.key)),
    ]))),
    actions:[
      if(!isMine&&!bot)...[
       TextButton(onPressed:()=>Navigator.pop(c,'__report575'),
        child:const Text('Şikayet et')),
       TextButton(onPressed:()=>Navigator.pop(c,'__block575'),
        child:Text(alreadyBlocked575?'Engeli kaldır':'Engelle')),
      ],
      TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Kapat'))])));
  if(!mounted||selected==null)return;
  if(selected=='__block575'){
   try{
    final response=await (widget.request??ngelx565LudoRequest)({
      'action':'block','id':widget.id,'to':theirId,'blocked':!alreadyBlocked575});
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content:Text(response['blocked']==true?'Ludo içinde engellendi.':'Ludo engeli kaldırıldı.')));
   }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(
     SnackBar(content:Text('Engel işlemi başarısız: $e')));}
   return;
  }
  if(selected=='__report575'){
   final reason=await showDialog<String>(context:context,builder:(c)=>SimpleDialog(
    title:const Text('Şikayet nedeni'),children:[
     for(final entry in [('spam','Spam'),('harassment','Rahatsız etme'),
      ('cheating','Hile şüphesi'),('other','Diğer')])
      SimpleDialogOption(onPressed:()=>Navigator.pop(c,entry.$1),child:Text(entry.$2)),
    ]));
   if(reason==null)return;
   try{
    final response=await (widget.request??ngelx565LudoRequest)({
     'action':'report','id':widget.id,'to':theirId,'reason':reason});
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
     content:Text(response['submitted']==true?'Ludo şikayetin kaydedildi.':
      'Bu oyuncuyu bu maç için zaten şikayet ettin.')));
   }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(
     SnackBar(content:Text('Şikayet gönderilemedi: $e')));}
   return;
  }
  // Paid gifts require explicit confirmation of the server-catalog price.
  // Only the server can charge the wallet; clients never supply a price.
  final gift=items[selected];
  if(gift is! Map||gift['chips'] is! num)return;
  final price=(gift['chips'] as num).toInt();
  if(price<=0)return;
  final label=gift['label']?.toString()??selected;
  final confirmed=await showDialog<bool>(context:context,builder:(c)=>Theme(
   data:ngelx567LudoTheme(),child:AlertDialog(
    key:const ValueKey('ludo-gift-confirmation'),
    title:const Text('Hediye gönderilsin mi?'),
    content:Text('$nickname adlı oyuncuya $label göndermek için $price çip harcanacak.'),
    actions:[
     TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
     FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Gönder')),
    ])))??false;
  if(!mounted||!confirmed)return;
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
# Rounded, resolution-independent pawns replace the old narrow sprite rendering.
start=s.index('class _PawnPainter567 extends CustomPainter {')
end=s.index('class Ngelx565BoardPainter',start)
s=s[:start]+'''class _PawnPainter567 extends CustomPainter {
 final Color color;final bool highlight;const _PawnPainter567(this.color,this.highlight);
 @override void paint(Canvas canvas,Size size){
  final w=size.width,h=size.height;
  final dark=Color.lerp(color,Colors.black,.42)!,light=Color.lerp(color,Colors.white,.65)!;
  final base=Rect.fromLTWH(w*.18,h*.68,w*.64,h*.23);
  canvas.drawOval(base.shift(Offset(w*.025,h*.055)),Paint()..color=Colors.black.withValues(alpha:.34)..maskFilter=const MaskFilter.blur(BlurStyle.normal,1.6));
  if(highlight)canvas.drawOval(base.inflate(w*.06),Paint()..color=_ludoGold567.withValues(alpha:.8));
  final body=Path()..moveTo(w*.37,h*.35)..cubicTo(w*.38,h*.49,w*.29,h*.58,w*.23,h*.72)..cubicTo(w*.19,h*.91,w*.81,h*.91,w*.77,h*.72)..cubicTo(w*.71,h*.58,w*.62,h*.49,w*.63,h*.35)..close();
  canvas.drawOval(base,Paint()..color=dark);
  canvas.drawPath(body,Paint()..shader=LinearGradient(begin:Alignment.centerLeft,end:Alignment.centerRight,colors:[dark,light,color,dark],stops:const [0,.25,.58,1]).createShader(Offset.zero&size));
  canvas.drawArc(Rect.fromLTWH(w*.22,h*.66,w*.56,h*.17),0,math.pi,false,Paint()..color=light.withValues(alpha:.8)..style=PaintingStyle.stroke..strokeWidth=w*.035);
  final head=Rect.fromCircle(center:Offset(w*.5,h*.29),radius:w*.235);
  canvas.drawCircle(Offset(w*.5,h*.29),w*.235,Paint()..shader=RadialGradient(center:const Alignment(-.4,-.5),radius:1,colors:[light,color,dark],stops:const [0,.5,1]).createShader(head));
  canvas.drawOval(Rect.fromLTWH(w*.36,h*.14,w*.13,h*.085),Paint()..color=Colors.white.withValues(alpha:.75));
 }
 @override bool shouldRepaint(covariant _PawnPainter567 old)=>old.color!=color||old.highlight!=highlight;
}
''' +s[end:]
start=s.index('class Ngelx570SpritePainter extends CustomPainter {')
end=s.index('\nint? ngelx570ShownDice',start)
s=s[:start]+'''class Ngelx570SpritePainter extends CustomPainter {
 final int seat;final bool highlight;final ui.Image? image;
 const Ngelx570SpritePainter(this.seat,this.highlight,this.image);
 @override void paint(Canvas canvas,Size size){
  final atlas=image;
  if(atlas==null){_PawnPainter567(ngelx565LudoColors[seat],highlight).paint(canvas,size);return;}
  // Actual opaque pawn bounds in the generated 1254px atlas, plus four pixels of margin.
  // Preserve the original image proportions; never stretch the pawn into a square.
  const bounds=[Rect.fromLTWH(178,85,315,499),Rect.fromLTWH(757,84,316,501),
    Rect.fromLTWH(177,676,318,501),Rect.fromLTWH(755,676,318,501)];
  final b=bounds[seat],sx=atlas.width/1254,sy=atlas.height/1254;
  final src=Rect.fromLTWH(b.left*sx,b.top*sy,b.width*sx,b.height*sy);
  final height=size.height*.96,width=height*b.width/b.height;
  final dst=Rect.fromLTWH((size.width-width)/2,size.height*.01,width,height);
  final base=Rect.fromCenter(center:Offset(size.width*.5,size.height*.94),width:width*.9,height:size.height*.08);
  canvas.drawOval(base,Paint()..color=Colors.black.withValues(alpha:.27)..maskFilter=const MaskFilter.blur(BlurStyle.normal,1.3));
  if(highlight)canvas.drawOval(base.inflate(size.width*.04),Paint()..style=PaintingStyle.stroke..strokeWidth=1.5..color=_ludoGold567);
  canvas.drawImageRect(atlas,src,dst,Paint()..isAntiAlias=true..filterQuality=FilterQuality.high);
 }
 @override bool shouldRepaint(covariant Ngelx570SpritePainter old)=>old.seat!=seat||old.highlight!=highlight||old.image!=image;
}
''' +s[end:]
# The bundled bitmap is the selected original 3D asset; no automatic palette recoloring.
swap("rootBundle.load('assets/ludo570_pawns.png')","rootBundle.load('assets/ludo577_pawns.png')")
# Reuse the decoded native image synchronously when another game/board is opened.
# This avoids redundant completed-Future listeners and first-frame fallback redraws.
swap('unawaited(ngelx570PawnSprite().then((value){if(mounted)setState(()=>sprite=value);}).catchError((_){ }));',
     'if(sprite==null)unawaited(ngelx570PawnSprite().then((value){if(mounted)setState(()=>sprite=value);}).catchError((_){ }));')
# Do not start a delayed one-piece move while the user is confirming departure.
swap('if(_singleMoveInFlight574||!mounted||game.busy||game.leaving||',
     'if(_asking||_singleMoveInFlight574||!mounted||game.busy||game.leaving||')
swap("if(!mounted||game.busy||game.leaving||room['revision']!=revision||",
     "if(_asking||!mounted||game.busy||game.leaving||room['revision']!=revision||")
# Media effects are driven by accepted room-state changes, including bot/Auto moves.
swap(' void _soundTap575(){if(_soundOn575)unawaited(SystemSound.play(SystemSoundType.click));}', ''' final _effects575=Ngelx575Effects();
 String? _soundTokens575,_soundDice575,_soundStatus575;bool _soundReady575=false;
 void _soundTap575(){} // Actual sounds follow successful server transitions.
 void _observeSound575(){
  final tokens=room['tokens'];if(tokens is! List)return;
  final signature=tokens.toString(),dice=room['lastRoll']?.toString(),status=room['status']?.toString();
  if(_soundTokens575!=null&&_soundOn575&&_soundReady575){
   if(status=='finished'&&_soundStatus575!='finished'){_effects575.play('win');}
   else if(signature!=_soundTokens575){
    final before=RegExp(r'-?\\d+').allMatches(_soundTokens575!).map((m)=>int.parse(m[0]!)).toList();
    final after=tokens.expand((row)=>row as List).whereType<num>().map((n)=>n.toInt()).toList();
    var steps=1;bool captured=false;
    for(var i=0;i<math.min(before.length,after.length);i++){
     if(before[i]>=0&&after[i]==-1)captured=true;
     if(after[i]>before[i])steps=math.max(steps,after[i]-math.max(0,before[i]));
    }
    _effects575.move(steps.clamp(1,12).toInt(),captured:captured);
   }else if(dice!=null&&dice!=_soundDice575){_effects575.play('dice');}
  }
  _soundTokens575=signature;_soundDice575=dice;_soundStatus575=status;
 }
''')
swap(' void _changed(){',' void _changed(){\n  _observeSound575();')
swap('  setState(()=>_soundOn575=next);','  setState(()=>_soundOn575=next);\n  if(!next)_effects575.stop();')
swap('@override void dispose(){chatExpiry?.cancel();poll?.cancel();','@override void dispose(){_effects575.dispose();chatExpiry?.cancel();poll?.cancel();')
s=s.replace('unawaited(SystemSound.play(SystemSoundType.click));',"_effects575.play('capture');")
s+='''
class Ngelx575Effects {
 final Map<String,AudioPlayer> _players={};
 final List<Timer> _timers=[];bool _disposed=false;int _epoch=0;
 Future<void> play(String kind)async{
  if(_disposed)return;final epoch=_epoch;
  try{
   final player=_players.putIfAbsent(kind,()=>AudioPlayer(handleAudioSessionActivation:false,handleInterruptions:false));
   if(player.audioSource==null)await player.setAsset('assets/ludo575_$kind.wav');
   if(_disposed||epoch!=_epoch)return;
   await player.setVolume(.7);await player.seek(Duration.zero);
   if(!_disposed&&epoch==_epoch)unawaited(player.play().catchError((_){ }));
  }catch(_){ } // Audio failure must never block the game.
 }
 void move(int steps,{required bool captured}){
  for(final timer in _timers){timer.cancel();}_timers.clear();
  for(var i=0;i<steps;i++){
   _timers.add(Timer(Duration(milliseconds:i*150),()=>unawaited(play('step'))));
  }
  if(captured)_timers.add(Timer(Duration(milliseconds:steps*150),()=>unawaited(play('capture'))));
 }
 void stop(){_epoch++;for(final timer in _timers){timer.cancel();}_timers.clear();for(final player in _players.values){unawaited(player.stop());}}
 void dispose(){_disposed=true;stop();for(final player in _players.values){unawaited(player.dispose());}}
}
'''
s=s.replace('else{poll?.cancel();}}', 'else{_effects575.stop();poll?.cancel();}}')
# Bundle original synthesized effects; no platform click-sound dependency.
import math,struct,wave
assets=root/'app/assets';assets.mkdir(parents=True,exist_ok=True)
for kind,notes in {'step':[(700,.045),(480,.035)],'dice':[(900,.04),(640,.04),(1100,.04),(500,.06)],'capture':[(880,.08),(660,.08),(440,.12)],'win':[(523.25,.13),(659.25,.13),(783.99,.13),(1046.5,.3)]}.items():
 with wave.open(str(assets/f'ludo575_{kind}.wav'),'wb') as out:
  out.setparams((1,2,22050,0,'NONE','not compressed'))
  for frequency,duration in notes:
   count=int(22050*duration)
   out.writeframes(b''.join(struct.pack('<h',int(14000*math.sin(2*math.pi*frequency*i/22050)*min(1,i/100)*((count-i)/count)**2)) for i in range(count)))
pubspec=root/'app/pubspec.yaml'
manifest=pubspec.read_text()
for kind in ['step','dice','capture','win']:
 manifest+=f'    - assets/ludo575_{kind}.wav\n'
pubspec.write_text(manifest)

import shutil
shutil.copyfile(root/'tools/assets/ludo577_pawns.png',root/'app/assets/ludo577_pawns.png')
manifest=pubspec.read_text()
if('    - assets/ludo577_pawns.png\n') not in manifest:
 pubspec.write_text(manifest+'    - assets/ludo577_pawns.png\n')
controller=root/'app/lib/build567_room_controller.dart'
control=controller.read_text()
assert control.count('for(var attempt=0;attempt<2;attempt++)')==1
assert control.count("if(attempt==0&&e is Ngelx567Failure&&e.code=='state_changed')")==1
control=control.replace('for(var attempt=0;attempt<2;attempt++)','for(var attempt=0;attempt<4;attempt++)',1)
control=control.replace("if(attempt==0&&e is Ngelx567Failure&&e.code=='state_changed')","if(attempt<3&&e is Ngelx567Failure&&e.code=='state_changed')",1)
controller.write_text(control)

# Build578: place the visible foot on the cell/socket center, rather than centering the image.
swap("final size=c*(widget.position<0?1.13:widget.stackCount > 1 ? 0.52 : 0.98),limit=c*15-size;",
     "final size=ngelx578PawnSize(c,widget.position,widget.stackCount);")
swap("final x=((p.dx+.5+widget.stackOffset.dx)*c-size*.5).clamp(0.0,limit).toDouble();",
     "final x=ngelx578PawnLeft((p.dx+.5+widget.stackOffset.dx)*c,size);")
swap("final y=((p.dy+.5+widget.stackOffset.dy)*c-size*.51-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.075).clamp(0.0,limit).toDouble();",
     "final y=ngelx578PawnTop(ngelx578FootY((p.dy+.5+widget.stackOffset.dy)*c,c,widget.position),size)-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.075;")
swap('class _MovingPawn567 extends StatefulWidget {',"""double ngelx578PawnSize(double cell,int position,int count)=>cell*(position<0?1.26:count>1?.52:1.18);
double ngelx578PawnTop(double floor,double size)=>floor-size*.94;
double ngelx578FootY(double center,double cell,int position)=>center+(position<0?0:cell*.28);
double ngelx578PawnLeft(double center,double size)=>center-size*.5;
class _MovingPawn567 extends StatefulWidget {""")
swap('child:ClipRRect(borderRadius:BorderRadius.circular(4),child:RepaintBoundary(',
     'child:ClipRRect(clipBehavior:Clip.none,borderRadius:BorderRadius.circular(4),child:RepaintBoundary(')
# Client single-choice assistance must not submit a manual move that cancels server Auto.
swap('  final choices=ngelx565Legal(room,game.seat);',"""  final autoSeats578=room['autoSeats'];
  if(autoSeats578 is Map&&autoSeats578[game.seat.toString()]==true)return;
  final choices=ngelx565Legal(room,game.seat);""")
swap("   if(_asking||!mounted||game.busy||game.leaving||room['revision']!=revision||room['turn']!=game.seat||room['dice']==null)return;", """   final autoNow578=room['autoSeats'];
   if(_asking||(autoNow578 is Map&&autoNow578[game.seat.toString()]==true)){
    _singleMoveRevision574=null;return;
   }
   if(!mounted||game.busy||game.leaving||room['revision']!=revision||room['turn']!=game.seat||room['dice']==null)return;""")
swap('poll=Timer.periodic(Duration(seconds:widget.watch?4:1),(tick){', 'poll=Timer.periodic(const Duration(milliseconds:500),(tick){')
swap("  if(_chatOpen&&tick.tick%3!=0)return;\n  final gap=math.min(8,1<<_connectionFailures575);", """  final seats578=room['autoSeats'];
  final auto578=seats578 is Map&&seats578[game.seat.toString()]==true;
  if(_chatOpen&&!auto578&&tick.tick%6!=0)return;
  final pace578=widget.watch?8:(auto578||room['botGame']==true?1:2);
  final gap=pace578*math.min(8,1<<_connectionFailures575);""")

p.write_text(s,encoding='utf-8')
pub=root/'app/pubspec.yaml'
version=pub.read_text(encoding='utf-8')
assert 'version: 1.0.344+574' in version
pub.write_text(version.replace('version: 1.0.344+574','version: 1.0.348+578',1),encoding='utf-8')
print('Build575 frontend ready: persistent Auto on/off, updated painted pawn depth, existing NgelX layout retained')
