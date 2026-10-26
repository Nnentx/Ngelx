"""Apply feedback to exact Build579 assembled sources; keep historical app baseline.

Run after restoring NgelX-Build579-Assembled-Source from CI 40386052388.
"""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
lib=root/'app/lib'
p=lib/'build565_ludo.dart'
s=p.read_text()
if 'class Ngelx580InviteContacts' in s:
    assert 'Future<void> setAuto580' in (lib/'build567_room_controller.dart').read_text(),'Partial Build580 controller'
    assert "const gameActions=" in (lib/'build566_transport.dart').read_text(),'Partial Build580 transport'
    assert (lib/'main.dart').read_text().count('inviteToken:ngelx580InviteToken(metin)')==2,'Partial Build580 chat integration'
    assert 'version: 1.0.350+580' in (root/'app/pubspec.yaml').read_text(),'Partial Build580 version'
    print('Build580 already applied');raise SystemExit(0)
assert hashlib.sha256(p.read_bytes()).hexdigest()=='9868c46c1da3fb2b2e71722f4a3c8f9fdeb940f54c96eccdb14af825b9669d20','Restore exact Build579 source first'
def swap(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:100])
    s=s.replace(a,b,1)

# Keep query-bearing invitations recognizable by the existing chat renderer.
swap(r"(?:\s|$)').firstMatch(text)",r"(?:[?\s]|$)').firstMatch(text)")
# Preserve readable server failures rather than reporting every rejection as a network error.
swap("'already_left':'Bu oyundan ayrılmışsın. Yeni bir odaya katılabilirsin.'", "'already_left':'Bu oyundan ayrılmışsın. Yeni bir odaya katılabilirsin.','invite_expired':'Davetin süresi doldu. Yeni davet iste.','invite_used':'Bu davete zaten katılındı.','not_available':'Bu masa artık davet kabul etmiyor.'")

# Muting is enforced at the effect player, including delayed/loading audio.
swap(' Future<void> _restoreSound575()async{\n  final p=await SharedPreferences.getInstance();', ' int _soundPreferenceEpoch580=0;\n Future<void> _restoreSound575()async{\n  final epoch=_soundPreferenceEpoch580;\n  final p=await SharedPreferences.getInstance();\n  if(epoch!=_soundPreferenceEpoch580)return;')
swap('  final next=!_soundOn575;', '  _soundPreferenceEpoch580++;final next=!_soundOn575;')
swap("_soundOn575=p.getBool('ngelx_ludo_sound')??true;_soundReady575=true;", "_soundOn575=p.getBool('ngelx_ludo_sound')??true;_effects575.setEnabled(_soundOn575);_soundReady575=true;")
swap('  if(!next)_effects575.stop();','  _effects575.setEnabled(next);')
swap('final List<Timer> _timers=[];bool _disposed=false;int _epoch=0;', '''final List<Timer> _timers=[];bool _disposed=false,_enabled=false;int _epoch=0;
 void setEnabled(bool enabled){_enabled=enabled;if(!enabled)stop();}''')
swap('if(_disposed)return;final epoch=_epoch;','if(_disposed||!_enabled)return;final epoch=_epoch;')
swap('if(_disposed||epoch!=_epoch)return;','if(_disposed||!_enabled||epoch!=_epoch)return;')
swap("if(!_disposed&&epoch==_epoch)unawaited(player.play().catchError((_){ }));", "if(!_disposed&&_enabled&&epoch==_epoch)unawaited(player.play().catchError((_){ }));")
swap(' void move(int steps,{required bool captured}){',' void move(int steps,{required bool captured}){\n  if(!_enabled||_disposed)return;')
swap('for(final player in _players.values){unawaited(player.stop());}', 'for(final player in _players.values){unawaited(player.setVolume(0).catchError((_){ }));unawaited(player.stop().catchError((_){ }));}')
swap('milliseconds:i*150','milliseconds:i*190')
swap('milliseconds:steps*150','milliseconds:steps*190')

# A press while a mutation is in progress is queued, rather than silently dropped.
swap("  if(widget.watch||game.busy||!game.playing||game.seat<0)return;\n  unawaited(game.perform('auto',{'enabled':!active}));", "  if(widget.watch||!game.playing||game.seat<0)return;\n  unawaited(game.setAuto580(!active));")
swap('if(_asking||_singleMoveInFlight574', 'if(game.pendingAuto580!=null||_asking||_singleMoveInFlight574')
swap("final auto=autoSeats is Map&&autoSeats[seat.toString()]==true;", "final auto=game.pendingAuto580??(autoSeats is Map&&autoSeats[seat.toString()]==true);")
swap('child:Container(width:46,height:47,','child:Container(width:52,height:52,')
swap("Text('Auto',style:const TextStyle(fontSize:10", "Text(enabled?'Kapat':'Auto',style:const TextStyle(fontSize:11")
swap("Text(enabled?'Kapat':'Auto',style:const TextStyle(fontSize:11,color:Colors.white,fontWeight:FontWeight.w900))", "SizedBox(height:16,child:FittedBox(fit:BoxFit.scaleDown,child:Text(enabled?'Kapat':'Auto',maxLines:1,style:const TextStyle(fontSize:11,color:Colors.white,fontWeight:FontWeight.w900))))")

# Avoid rebuilding a static board painter and every stationary pawn on every poll.
swap('final messages=room[\'chat\'] as List? ?? [];', "_observeVictory580();\n  final messages=room['chat'] as List? ?? [];")
swap('  if(mounted&&!_chatOpen)setState((){});', '  final visual580=room.toString();\n  if(mounted&&(!_chatOpen)&&(game.busy!=_lastBusy580||game.error!=_lastError580||visual580!=_lastVisual580||game.pendingAuto580!=_lastAuto580)){\n   _lastBusy580=game.busy;_lastError580=game.error;_lastVisual580=visual580;_lastAuto580=game.pendingAuto580;setState((){});\n  }')
swap(' int _connectionFailures575=0;', " int _connectionFailures575=0;\n bool _lastBusy580=false;bool? _lastAuto580;String _lastError580='',_lastVisual580='';\n bool _victory580=false,_victorySeen580=false;Timer? _victoryTimer580;")
swap(' void _changed(){', ''' void _observeVictory580(){
  if(_victorySeen580||widget.watch||game.detached||game.seat<0||room['status']!='finished'||room['winner']==null)return;
  _victorySeen580=true;_victory580=true;
  _victoryTimer580=Timer(const Duration(seconds:4),(){if(mounted)setState(()=>_victory580=false);});
 }
 void _changed(){''')
swap(' @override void dispose(){_effects575.dispose();', ' @override void dispose(){_victoryTimer580?.cancel();_effects575.dispose();')
swap('  if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();', '  _observeVictory580();if(widget.initial==null)unawaited(game.sync(join:true));_startPoll();')
# Full-screen overlay covers the whole Scaffold, including the app bar.
swap('return Theme(data:ngelx567LudoTheme(),child:PopScope(', 'return Theme(data:ngelx567LudoTheme(),child:Stack(children:[PopScope(')
swap('  )));\n }\n}\nWidget _roomLabel567', "  )),if(_victory580)Positioned.fill(child:Ngelx580Victory(name:_winner567(room))) ]));\n }\n}\nWidget _roomLabel567")
swap('maxWidth:math.min(320,area.maxWidth-34)', 'maxWidth:math.min(380,area.maxWidth-20)')
swap('width:265,child:FittedBox(fit:BoxFit.scaleDown,child:SizedBox(width:265', 'width:300,child:FittedBox(fit:BoxFit.scaleDown,child:SizedBox(width:300')
swap("'Oda dolduğunda kurucu Başlat’a dokunur.", "'En az iki oyuncu katılınca kurucu Başlat’a dokunur. Takımlı oyun dört kişiyle başlar.")
swap("fontSize:10,letterSpacing:1)))]));", "fontSize:14,fontWeight:FontWeight.w800,letterSpacing:2)))]));")
swap('radius:compact?17:22,','radius:compact?23:28,')
swap('SizedBox(width:capacity==4?48:90,child:Text(', 'SizedBox(width:capacity==4?70:115,child:Text(')
swap('maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:_ludoInk567,fontSize:10,fontWeight:FontWeight.w800)', 'maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:_ludoInk567,fontSize:14,fontWeight:FontWeight.w800)')
swap('width:compact?34:44,height:compact?34:44','width:compact?46:56,height:compact?46:56')
swap("fontSize:10,fontWeight:FontWeight.w800))]))]),", "fontSize:13,fontWeight:FontWeight.w800))]))]),")
swap('fontWeight:FontWeight.w900,fontSize:11,letterSpacing:1', 'fontWeight:FontWeight.w800,fontSize:20,letterSpacing:3')
swap("players.length<capacity?'${capacity-players.length} oyuncu daha bekleniyor':owner?", "players.length<(room['team']==true?4:2)?'${(room['team']==true?4:2)-players.length} oyuncu daha bekleniyor':owner?")
swap("${p['level'] is num?'Lv.${p['level']}  ':''}", "Lv.${p['level'] is num?p['level']:1}  ")

# The painted foot CENTER (not the bitmap bottom) belongs at the socket center.
swap('double ngelx578PawnTop(double floor,double size)=>floor-size*.94;', 'double ngelx578PawnTop(double floor,double size)=>floor-size*.89;')
swap('center:Offset(size.width*.5,size.height*.94)', 'center:Offset(size.width*.5,size.height*.89)')
swap('math.min(1800,math.max(210,(widget.position-from).abs()*160))','math.min(2400,math.max(260,(widget.position-from).abs()*190))')
# Cache the unchanged sprite draw while the position animates.
swap('@override Widget build(BuildContext context)=>AnimatedBuilder(animation:motion,builder:(_,__){', '@override Widget build(BuildContext context)=>AnimatedBuilder(animation:motion,child:RepaintBoundary(child:CustomPaint(painter:Ngelx570SpritePainter(widget.seat,widget.highlight,sprite))),builder:(_,pawn){')
swap("child:CustomPaint(painter:Ngelx570SpritePainter(widget.seat,widget.highlight,sprite)))));", "child:pawn)));")
# Protection is visible independently of move selection; do not add a move hint.
swap('final bool highlight;final Offset stackOffset;final int stackCount;', 'final bool highlight;final Offset stackOffset;final int stackCount;final bool protected580;')
swap('required this.stackCount,this.onTap});','required this.stackCount,this.onTap,this.protected580=false});')
swap("key:ValueKey('ludo-$color-$token'),seat:color", "protected580:room['shields'] is Map&&(room['shields'] as Map)[color.toString()]==true,key:ValueKey('ludo-$color-$token'),seat:color")
swap('child:pawn)));', "child:Stack(clipBehavior:Clip.none,children:[Positioned.fill(child:pawn!),if(widget.protected580)Positioned(right:-2,top:-2,child:const Icon(Icons.shield_rounded,color:Color(0xFF9AF4FF),size:16))]))));")
swap("if(kind!='control'){final ok=await game.perform('power',{'kind':kind});_notice572(ok?(kind=='shield'?'Kalkan etkinleştirildi':'Çift hareket etkinleştirildi'):game.error);return;}", "if(kind!='control'){final ok=await game.perform('power',{'kind':kind});_notice572(ok?(kind=='shield'?'Kalkan etkinleştirildi · taşlarında kalkan işareti var':'Çift hareket etkinleştirildi'):game.error);return;}")
# Explicit receipt for collecting any power; keep authoritative game rules.
swap("   _recentPickup575=receipt;", "   if(_recentPickup575!=null&&receipt!=_recentPickup575&&pickup['seat']==game.seat){\n    WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)_notice572('${pickup['kind']=='shield'?'Kalkan':pickup['kind']=='control'?'Zar seç':'Çift'} alındı · güçlerine eklendi');});\n   }\n   _recentPickup575=receipt;")
swap("   if(_recentPickup575!=null&&receipt!=_recentPickup575&&pickup['seat']==game.seat){", "   if(_pickupReady580&&receipt!=_recentPickup575&&pickup['seat']==game.seat){")
swap(' int _connectionFailures575=0;', ' bool _pickupReady580=false;\n int _connectionFailures575=0;')
swap('  _observeVictory580();if(widget.initial==null)', '  _pickupReady580=widget.initial!=null;\n  final initialPickup580=room[\'pickup\'];\n  if(initialPickup580 is Map)_recentPickup575=\'${initialPickup580["seat"]}:${initialPickup580["cell"]}:${initialPickup580["at"]}\';\n  _observeVictory580();if(widget.initial==null)')
swap('  final visual580=room.toString();', '  _pickupReady580=true;\n  final visual580=room.toString();')

# New invite card and searchable white recipient picker replace only these views.
a=s.index('class Ngelx565LudoInvitePicker extends StatefulWidget')
b=s.index('\nBoxDecoration ngelx570Bevel',a)
s=s[:a]+(root/'tools/build580_invites.dart').read_text()+s[b:]
a=s.index('class Ngelx567WaitingPanel extends StatelessWidget')
b=s.index('class Ngelx567Table extends StatelessWidget',a)
s=s[:a]+(root/'tools/build580_waiting.dart').read_text()+'\n'+s[b:]
s+='\n'+(root/'tools/build580_victory.dart').read_text()
p.write_text(s)

# Queued Auto changes must survive an in-flight manual action and CAS conflicts.
p=lib/'build567_room_controller.dart';c=p.read_text()
c="import 'dart:async';\n"+c
c=c.replace("joined==room['capacity']", "joined>=(room['team']==true||room['matchmaking']==true?room['capacity'] as num:2)")
c=c.replace(' Future<void>? _sync;', ''' Future<void>? _sync;
 Completer<void>? _mutation580;bool? pendingAuto580;bool _autoChanging580=false;
 Future<void> setAuto580(bool enabled)async{
  if(_disposed||leaving||detached||!playing||seat<0)return;
  pendingAuto580=enabled;_notify();if(_autoChanging580)return;
  _autoChanging580=true;
  try{
   while(pendingAuto580!=null&&!_disposed&&!leaving&&!detached){
    final pending=_mutation580;if(pending!=null)await pending.future;
    if(_disposed||leaving||detached)return;
    final desired=pendingAuto580;bool ok=false;
    for(var attempt=0;attempt<3;attempt++){
     if(_disposed||leaving||detached)return;
     ok=await perform('auto',{'enabled':desired});
     if(ok||error.isNotEmpty)break;
    }
    if(pendingAuto580==desired){pendingAuto580=null;break;}
   }
  }finally{_autoChanging580=false;pendingAuto580=null;_notify();}
 }
''')
c=c.replace("  busy=true;error='';_notify();", "  _mutation580=Completer<void>();busy=true;error='';_notify();",1)
c=c.replace('  finally{busy=false;_notify();}', '  finally{busy=false;final done=_mutation580;_mutation580=null;done?.complete();_notify();}',1)
p.write_text(c)

p=lib/'build566_transport.dart';c=p.read_text()
needle="    if(!RegExp(r'^(?:[0-9]{6}|[A-F0-9]{16})$').hasMatch('${room['id']}')||room['revision'] is! num)throw const FormatException('Oyun yanıtı doğrulanamadı.');"
assert needle in c
c=c.replace(needle,'''    const gameActions={'create','bot','match','join','sync','start','roll','move','auto','chat','power','leave','watch','watch_leave','rematch','invite_join'};
    if(gameActions.contains(payload['action'])){
     if(!RegExp(r'^(?:[0-9]{6}|[A-F0-9]{16})$').hasMatch('${room['id']}')||room['revision'] is! num)throw const FormatException('Oyun yanıtı doğrulanamadı.');
    }else if({'wallet','daily_reward','chest_reward'}.contains(payload['action'])){
     if(['chips','gems','xp','level'].any((key)=>room[key] is! num))throw const FormatException('Cüzdan yanıtı doğrulanamadı.');
    }else if({'invite_create','invite_status'}.contains(payload['action'])){
     if(!{'pending','joined','expired'}.contains(room['status'])||room['expiresAt'] is! num)throw const FormatException('Davet yanıtı doğrulanamadı.');
    }else if(payload['action']=='gift_catalog'&&room['gifts'] is! Map){
     throw const FormatException('Hediye yanıtı doğrulanamadı.');
    }''')
p.write_text(c)

p=lib/'main.dart';m=p.read_text()
old='id:ludo565,mine:ben,onLongPress:()=>mesajMenusu(d)'
assert m.count(old)==2
m=m.replace(old,"id:ludo565,mine:ben,inviteToken:ngelx580InviteToken(metin),sentAt:ngelx580MessageTime(v),onLongPress:()=>mesajMenusu(d)")
needle='    final t=mesaj.text.trim();if(t.isEmpty||mesajGonderiliyor)return;'
assert m.count(needle)==1;m=m.replace(needle,needle.replace('final t=','var t='))
needle='      Map<String,String> preview=<String,String>{};\n      try{\n        preview=await fetchGroupLinkPreview(t)'
assert m.count(needle)==1;m=m.replace(needle,"      t=await ngelx580PrepareInvite(t);\n      Map<String,String> preview=<String,String>{};\n      try{\n        preview=t.startsWith('🎲 Ludo daveti\\n')?<String,String>{}:await fetchGroupLinkPreview(t)")
needle='    final t=ngelxMesajBaglantilariniAyir(hamMetin);';assert m.count(needle)==1
m=m.replace(needle,needle.replace('final t=','var t='))
needle='    final gonderilenMetin=t;\n    mesaj.clear();';assert m.count(needle)==1
m=m.replace(needle,"""    try{t=await ngelx580PrepareInvite(t);}catch(e){
     if(mounted){setState(()=>gonderiliyor=false);ngelxDurumMesaji(context,'Davet hazırlanamadı. Tekrar dene.',tip:'uyari');}return;
    }
    final gonderilenMetin=t;
    mesaj.clear();""")
p.write_text(m)
p=root/'app/pubspec.yaml';p.write_text(p.read_text().replace('version: 1.0.349+579','version: 1.0.350+580'))
print('Build580 feedback patch applied to exact Build579 source')
