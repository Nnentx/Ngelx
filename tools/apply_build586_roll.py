"""One GO gesture includes existing opening attempts; server dice/rules unchanged."""
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
app=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'app'
pub=app/'pubspec.yaml'
if 'version: 1.0.356+586' in pub.read_text():
    print('Build586 already applied');raise SystemExit
assert 'version: 1.0.355+585' in pub.read_text()
def one(s,old,new):
    assert s.count(old)==1,(s.count(old),old[:100])
    return s.replace(old,new,1)
p=app/'lib/build565_ludo.dart';s=p.read_text()
a=s.index(' bool _rollPending583=false;');b=s.index(' void _tapPower572(',a)
s=s[:a]+''' bool _rollPending583=false;
 int? _rollFace586;
 bool get _canRoll586=>mounted&&!widget.watch&&!_asking&&!_chatOpen&&
  WidgetsBinding.instance.lifecycleState!=AppLifecycleState.paused&&
  WidgetsBinding.instance.lifecycleState!=AppLifecycleState.inactive&&
  WidgetsBinding.instance.lifecycleState!=AppLifecycleState.hidden&&
  WidgetsBinding.instance.lifecycleState!=AppLifecycleState.detached&&
  !game.leaving&&!game.detached&&game.playing&&game.seat>=0&&
  room['turn']==game.seat&&room['dice']==null;
 void _tapRoll572(bool myTurn){
  if(_rollPending583||widget.watch||(!myTurn&&!game.busy))return;
  if(room['dice']!=null){_notice572('Önce parlayan taşını seç');return;}
  setState((){_rollPending583=true;_rollFace586=null;});
  unawaited(()async{
   try{
    // Accept a gesture during a pending mutation/poll, then use its fresh state.
    await game.waitForIdle583();
    for(var opening=0;opening<3&&_canRoll586;opening++){
     final beforeOpening=(room['openingRolls'] as num?)?.toInt()??0;
     final beforeRoll=room['lastRoll'].toString();
     var ok=false;
     for(var conflict=0;conflict<3&&_canRoll586;conflict++){
      final receipt=room['lastRoll'].toString();
      ok=await game.perform('roll');
      if(ok)break;
      // A rejected revision is safe to retry; a changed roll is never replayed.
      if(game.lastFailureCode583!='state_changed'||!_canRoll586||
         room['lastRoll'].toString()!=receipt)break;
      await game.waitForIdle583();
     }
     if(!ok||!mounted||room['lastRoll'].toString()==beforeRoll)break;
     final last=room['lastRoll'];
     final face=last is Map&&last['seat']==game.seat?(last['value'] as num?)?.toInt():null;
     if(face!=null)setState(()=>_rollFace586=face);
     final count=(room['openingRolls'] as num?)?.toInt()??0;
     final tokens=game.seat<0?null:(room['tokens'] as List)[game.seat];
     final continueOpening=_canRoll586&&face!=6&&count==beforeOpening+1&&count<=2&&
        tokens is List&&tokens.every((token)=>token==-1);
     final receipt=last.toString();
     // Also show the final no-move result after the server passes the turn.
     if(face!=null&&room['dice']==null)await Future<void>.delayed(const Duration(milliseconds:360));
     if(!continueOpening||!_canRoll586||room['lastRoll'].toString()!=receipt||
        room['openingRolls']!=count)break;
     await game.waitForIdle583();
    }
   }finally{
    if(mounted)setState((){_rollPending583=false;_rollFace586=null;});
   }
  }());
 }
'''+s[b:]
s=one(s,'(tick){\n  final seats578=', '(tick){\n  if(_rollPending583)return;\n  final seats578=')
s=one(s,"onRoll:()=>_tapRoll572(game.playing&&room['turn']==game.seat),busy:game.busy);",
      "onRoll:()=>_tapRoll572(game.playing&&room['turn']==game.seat),busy:game.busy,rollPending586:_rollPending583,rollFace586:_rollFace586);")
s=one(s,'final ValueChanged<Map<String,dynamic>>? onPlayerTap;\n const Ngelx567Table',
      'final ValueChanged<Map<String,dynamic>>? onPlayerTap;final bool rollPending586;final int? rollFace586;\n const Ngelx567Table')
s=one(s,'required this.busy,this.onPlayerTap});',
      'required this.busy,this.onPlayerTap,this.rollPending586=false,this.rollFace586});')
s=one(s,"final shownDice=(room['dice'] as num?)?.toInt();",
      "final shownDice=(room['dice'] as num?)?.toInt()??(isMine?rollFace586:null);\n    Widget rollControl586()=>GestureDetector(key:isMine?const ValueKey('ludo-dice'):null,behavior:HitTestBehavior.opaque,onTap:isMine&&(enabled||busy)&&!rollPending586&&room['dice']==null?onRoll:null,child:SizedBox(width:48,height:42,child:Center(child:Ngelx567Dice(value:shownDice,size:32,busy:isMine&&(busy||rollPending586&&rollFace586==null)))));")
s=one(s,"GestureDetector(onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:shownDice,size:32,busy:busy&&isMine))",'rollControl586()')
s=one(s,"GestureDetector(key:isMine?const ValueKey('ludo-dice'):null,onTap:isMine&&enabled&&!busy&&room['dice']==null?onRoll:null,child:Ngelx567Dice(value:shownDice,size:32,busy:busy&&isMine))",'rollControl586()')
s=one(s,'if(!isLeft&&isTurn)...[','if(!isLeft&&(isTurn||isMine&&rollPending586))...[')
s=one(s,'if(isLeft&&isTurn)...[','if(isLeft&&(isTurn||isMine&&rollPending586))...[')
p.write_text(s)
pub.write_text(one(pub.read_text(),'version: 1.0.355+585','version: 1.0.356+586'))
print('Build586: one GO gesture, queued taps, opening-result feedback and larger hit area')
