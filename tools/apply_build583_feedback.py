"""Patch exact successful Build582 source without replacing app architecture.

CI restores artifact 12720282636 from run 40475015115 first. The optional
directory argument lets local QA keep the historical repository app untouched.
"""
from pathlib import Path
import hashlib
import math
import shutil
import struct
import sys
import wave

root = Path(__file__).resolve().parents[1]
app = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / 'app'
lib = app / 'lib'
if (lib / 'build583_feedback.dart').exists():
    assert 'version: 1.0.353+583' in (app / 'pubspec.yaml').read_text()
    print('Build583 already applied')
    raise SystemExit

expected = {
 'build565_ludo.dart':'ff1b6ebb66b1f6d2c9b27468f8ce5200f1a0269e68b45a64881de3e07ea8e74a',
 'main.dart':'f98aa070a87d778cc25776992d437f0142e34fcb10ab580146275e28a7d6591e',
 'build567_room_controller.dart':'520a179510fdb8855e983333ebddda4de2a8a28c430196ddb8140da819e3f711',
}
for name, digest in expected.items():
    assert hashlib.sha256((lib/name).read_bytes()).hexdigest() == digest, name

def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:120])
    return s.replace(old, new, 1)

s = (lib/'build565_ludo.dart').read_text()
# A light local dialog theme also styles ListTile text; room remains dark.
s = one(s, 'ThemeData ngelx567LudoTheme()=>', '''ThemeData ngelx583DialogTheme()=>ThemeData.light(useMaterial3:true).copyWith(
 colorScheme:ColorScheme.fromSeed(seedColor:const Color(0xFF7046BA)),
 dialogTheme:const DialogThemeData(backgroundColor:Color(0xFFF6F3FF),titleTextStyle:TextStyle(color:Color(0xFF27204C),fontSize:21,fontWeight:FontWeight.w900),contentTextStyle:TextStyle(color:Color(0xFF625878),fontSize:15)),
 listTileTheme:const ListTileThemeData(textColor:Color(0xFF27204C),iconColor:Color(0xFF7046BA)),
);
ThemeData ngelx567LudoTheme()=>''')
start=s.index(' Future<void> _playerCard575(')
end=s.index(' void _tapAuto575(',start)
section=s[start:end].replace('data:ngelx567LudoTheme()', 'data:ngelx583DialogTheme()')
section=section.replace('constraints:const BoxConstraints(maxHeight:360)', 'constraints:BoxConstraints(maxHeight:math.max(100,MediaQuery.sizeOf(c).height*.55))')
section=section.replace('SingleChildScrollView(child:Column', 'Scrollbar(thumbVisibility:true,child:SingleChildScrollView(child:Column')
section=one(section, '    ]))),\n    actions:', '    ])))),\n    actions:')
section=one(section, 'title:Text((e.value', "title:Text((e.value")
section=section.replace("??e.key),", "??e.key,style:const TextStyle(color:Color(0xFF27204C),fontWeight:FontWeight.w700)),")
section=section.replace("??0} çip'),", "??0} çip',style:const TextStyle(color:Color(0xFF625878))),")
old="""  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
   ok?(room['giftAlreadySent']==true?'Bu hediye daha önce gönderilmiş.':'Hediye gönderildi 🎁'):
   (game.error.isEmpty?'Hediye gönderilemedi.':game.error))));"""
section=one(section,old,"""  if(!ok||room['giftAlreadySent']==true)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
   ok?'Bu hediye daha önce gönderilmiş.':(game.error.isEmpty?'Hediye gönderilemedi.':game.error))));""")
s=s[:start]+section+s[end:]
start=s.index("   if(room['gifts'] is List")
end=s.index('   if(game.error.isNotEmpty',start)
s=s[:start]+s[end:]
# A legal stone is still the player's choice, even if only one is available.
s=one(s,'  if(mounted&&!widget.watch)unawaited(_autoSingleMove574());','  // Build583: manual play always waits for the player to touch a legal pawn.')
s=one(s,').clamp(0,10).toDouble()',').clamp(0,15).toDouble()')
s=one(s,'value:left/10,','value:left/15,')
# Both GO controls share one intent. A known rejected revision can retry once;
# an uncertain transport result or a changed lastRoll must never reroll.
start=s.index(' void _tapRoll572(bool myTurn){')
end=s.index(' void _tapPower572(',start)
s=s[:start]+''' bool _rollPending583=false;
 void _tapRoll572(bool myTurn){
  if(_rollPending583||widget.watch||(!myTurn&&!game.busy))return;
  if(room['dice']!=null){_notice572('Önce parlayan taşını seç');return;}
  _rollPending583=true;
  unawaited(()async{
   try{
    await game.waitForIdle583();
    if(!mounted||game.leaving||!game.playing||room['turn']!=game.seat||room['dice']!=null)return;
    final before=room['lastRoll'].toString();
    final ok=await game.perform('roll');
    if(!ok&&mounted&&game.lastFailureCode583=='state_changed'&&
     game.playing&&!game.leaving&&room['turn']==game.seat&&room['dice']==null&&room['lastRoll'].toString()==before){
     await game.perform('roll');
    }
   }finally{_rollPending583=false;}
  }());
 }
'''+s[end:]
s=one(s,"onRoll:()=>game.perform('roll'),busy:game.busy);","onRoll:()=>_tapRoll572(game.playing&&room['turn']==game.seat),busy:game.busy);")
# Board takes actual remaining viewport constraints, instead of a second .78 box.
s=one(s,'child:Align(alignment:Alignment.topCenter,child:AspectRatio(aspectRatio:.78,child:frame))','child:frame')
s=one(s,'children:[Padding(padding:const EdgeInsets.symmetric(horizontal:2),child:frame),', 'children:[Positioned.fill(child:Padding(padding:const EdgeInsets.symmetric(horizontal:2),child:frame)),')
s=one(s,'box.maxHeight-98','box.maxHeight-86')
s=one(s,'math.min(46.0,math.max(0.0,box.maxHeight-side-44))','math.min(43.0,math.max(0.0,box.maxHeight-side-43))')
s=one(s,"Column(mainAxisSize:MainAxisSize.min,children:[ngelx570Chip('😊 Emoji',widget.watch?null:_chat),const SizedBox(height:4),ngelx570Chip('Sohbet',widget.watch?null:_chat)])", "Row(mainAxisSize:MainAxisSize.min,children:[ngelx570Chip('😊 Emoji',widget.watch?null:_chat),const SizedBox(width:5),ngelx570Chip('Sohbet',widget.watch?null:_chat)])")
# Put effect layer after avatar widgets, in the exact same coordinate system.
start=s.index('class Ngelx567Table ')
end=s.index('class Ngelx567Dice ',start)
section=s[start:end]
section=one(section,'   }),\n  ]);','   }),\n   Positioned.fill(child:Ngelx583GiftFlight(room:room,seat:seat,side:side,left:left,top:top)),\n  ]);')
s=s[:start]+section+s[end:]
# Board handles pointer-down in one place. Per-pawn semantics retain accessibility.
start=s.index('class Ngelx565LudoBoard ')
end=s.index('Offset ngelx572StackOffset',start)
section=s[start:end]
section=one(section,'  return Stack(clipBehavior:', '''  return Listener(behavior:HitTestBehavior.opaque,onPointerDown:enabled?(event){
   final token=ngelx583HitToken(room,seat,cell,event.localPosition);
   if(token!=null)onToken(token);
  }:null,child:Stack(clipBehavior:''')
section=one(section,'onToken(token):null)]);','onToken(token):null)]));')
s=s[:start]+section+s[end:]
s=one(s,"button:widget.onTap!=null,child:GestureDetector(behavior:HitTestBehavior.opaque,onTap:widget.onTap,child:Stack(","button:widget.onTap!=null,onTap:widget.onTap,child:IgnorePointer(child:Stack(")
# Persist server's last rolled face across move/turn transition. This is display
# only: all random rolls and eligibility stay server-authoritative.
s=one(s,"if(last is Map&&last['seat']==room['turn'])return", "if(last is Map)return")
s=one(s,'var steps=1;bool captured=false;','var steps=1;bool captured=false,home=false;')
s=one(s,'if(before[i]>=0&&after[i]==-1)captured=true;', 'if(before[i]>=0&&after[i]==-1)captured=true;\n     if(before[i]!=56&&after[i]==56)home=true;')
s=one(s,'captured:captured);','captured:captured,home:home);')
s=one(s,'void move(int steps,{required bool captured})','void move(int steps,{required bool captured,bool home=false})')
s=one(s,"  if(captured)_timers.add(Timer(Duration(milliseconds:steps*190),()=>unawaited(play('capture'))));", "  if(captured||home)_timers.add(Timer(Duration(milliseconds:math.max(260,steps*190)),()=>unawaited(play(captured?'capture':'home'))));")

m=(lib/'main.dart').read_text()
m=one(m,"part 'build570_join_sound.dart';", "part 'build570_join_sound.dart';\npart 'build583_feedback.dart';")
m=one(m,'  bool _speakerBusy548=false;', '''  Ngelx570JoinSound? _joinSound583;
  final _joined583=<String>{};Timer? _joinExpiry583;
  void _joinedCall583(Set<String> ids){
    if(!mounted||bitiyor||!grupAramasi)return;
    setState(()=>_joined583.addAll(ids));_joinExpiry583?.cancel();
    _joinExpiry583=Timer(const Duration(seconds:3),(){if(mounted)setState(_joined583.clear);});
  }
  bool _speakerBusy548=false;''')
m=one(m,'  void _aramaOlaylariniBagla(lk.Room r){\n', '''  void _aramaOlaylariniBagla(lk.Room r){
    final oldJoin583=_joinSound583;_joinSound583=null;
    if(oldJoin583!=null)unawaited(oldJoin583.dispose());
    if(grupAramasi)_joinSound583=Ngelx570JoinSound(r,onJoined:_joinedCall583);
''')
m=one(m,'  Future<void> _stopLocal444()async{\n', '''  Future<void> _stopLocal444()async{
    final join583=_joinSound583;_joinSound583=null;
    if(join583!=null)await join583.dispose();
    _joinExpiry583?.cancel();_joined583.clear();
''')
m=one(m,'  @override void dispose(){\n    _peerSub548?.cancel();','''  @override void dispose(){
    _joinExpiry583?.cancel();
    final join583=_joinSound583;_joinSound583=null;
    if(join583!=null)unawaited(join583.dispose());
    _peerSub548?.cancel();''')
start=m.index('  Widget _katilimciKutusu(')
end=m.index('  // Build465: only this listener',start)
section=m[start:end]
section=one(section,'    return GestureDetector(', '''    return Ngelx583CallPresence(key:ValueKey('call-presence-${p.identity}'),participant:p,
      joined:!yerel&&_joined583.contains(p.identity),microphone:mic446,child:GestureDetector(''')
section=one(section,'    );\n  }','    ));\n  }')
m=m[:start]+section+m[end:]

j=(lib/'build570_join_sound.dart').read_text()
j=one(j,' Ngelx570JoinSound(this.room){',''' final void Function(Set<String>)? onJoined;
 Set<String> known={};
 Ngelx570JoinSound(this.room,{this.onJoined}){
  known=room.remoteParticipants.keys.toSet();''')
j=one(j,"  changed=(){if(policy.update(room.remoteParticipants.keys,connected:room.connectionState==lk.ConnectionState.connected))unawaited(_play());};",'''  changed=(){
   final current=room.remoteParticipants.keys.toSet(),added=current.difference(known);known=current;
   if(policy.update(current,connected:room.connectionState==lk.ConnectionState.connected)){
    onJoined?.call(added);unawaited(_play());
   }
  };''')
j=one(j,'player.setVolume(.65)','player.setVolume(.8)')
# A stalled injected/default request must release busy and poll gates. Mutations
# are never replayed; next sync recovers the authoritative revision.
c=(lib/'build567_room_controller.dart').read_text()
c=one(c,' Future<bool> perform(String action,', ''' String? lastFailureCode583;
 Future<void> waitForIdle583()async{
  final mutation=_mutation580;if(mutation!=null)await mutation.future;
  final syncing=_sync;if(syncing!=null)await syncing;
 }
 Future<bool> perform(String action,''')
c=one(c,"  _mutation580=Completer<void>();busy=true;error='';_notify();", "  lastFailureCode583=null;_mutation580=Completer<void>();busy=true;error='';_notify();")
c=one(c,"   if(!_disposed){\n    if(e is Ngelx567Failure", "   if(!_disposed){\n    lastFailureCode583=e is Ngelx567Failure?e.code:null;\n    if(e is Ngelx567Failure")
import re
c=re.sub(r'await request\((\{[^\n]*\})\)',r'await request(\1).timeout(const Duration(seconds:12))',c)

(lib/'build565_ludo.dart').write_text(s)
(lib/'main.dart').write_text(m)
(lib/'build570_join_sound.dart').write_text(j)
(lib/'build567_room_controller.dart').write_text(c)
shutil.copyfile(root/'tools/build583_feedback.dart',lib/'build583_feedback.dart')
pub=app/'pubspec.yaml'
pub.write_text(one(pub.read_text(),'version: 1.0.352+582','version: 1.0.353+583'))
# Own short synthesized completion cue, declared next to existing sound assets.
text=pub.read_text();text=one(text,'    - assets/ludo575_capture.wav','    - assets/ludo575_home.wav\n    - assets/ludo575_capture.wav');pub.write_text(text)
with wave.open(str(app/'assets/ludo575_home.wav'),'wb') as audio:
    rate=22050;audio.setparams((1,2,rate,0,'NONE','not compressed'))
    samples=[]
    for i in range(int(rate*.42)):
        t=i/rate;freq=(660,880,1100)[min(2,int(t/.14))]
        envelope=math.sin(math.pi*(t% .14)/.14)**2
        samples.append(struct.pack('<h',int(11000*envelope*math.sin(2*math.pi*freq*t))))
    audio.writeframes(b''.join(samples))
print('Build583 game, gift and call feedback applied')
