"""Build574 incremental Ludo: one-legal-piece autoplay, dynamic +1, gloss, quieter controls.
Only touches app/lib/build565_ludo.dart and the Flutter build version.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'app/lib/build565_ludo.dart'
s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 n=s.count(old)
 if n!=1:raise RuntimeError(f'Build574 source mismatch: expected one, found {n}: {old[:110]}')
 s=s.replace(old,new,1)

# The room listener receives every authoritative server revision, including selected dice.
change("bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;",
"""bool _chatOpen=false;Timer? poll;Timer? chatExpiry;String? chatKey;String? chatBubble;bool _canClose=false,_asking=false;
 bool _singleMoveInFlight574=false;int? _singleMoveRevision574;""")
change("  if(mounted&&!_chatOpen)setState((){});\n }\n void _startPoll(){",
"""  if(mounted&&!_chatOpen)setState((){});
  if(mounted&&!widget.watch)unawaited(_autoSingleMove574());
 }
 Future<void> _autoSingleMove574()async{
  if(_singleMoveInFlight574||!mounted||game.busy||game.leaving||!game.playing||game.seat<0||room['turn']!=game.seat||room['dice']==null)return;
  final choices=ngelx565Legal(room,game.seat);
  if(choices.length!=1)return; // Two or more legal pieces always require the player's selection.
  final revision=(room['revision'] as num?)?.toInt();
  if(revision==null||revision==_singleMoveRevision574)return;
  _singleMoveRevision574=revision;
  _singleMoveInFlight574=true;
  try{
   await Future<void>.delayed(const Duration(milliseconds:380));
   if(!mounted||game.busy||game.leaving||room['revision']!=revision||room['turn']!=game.seat||room['dice']==null)return;
   final latest=ngelx565Legal(room,game.seat);
   if(latest.length!=1||latest.first!=choices.first)return;
   final ok=await game.perform('move',{'token':choices.single});
   if(!ok)_singleMoveRevision574=null; // Network failure: re-attempt on next room sync.
  }finally{_singleMoveInFlight574=false;}
 }
 void _startPoll(){""")
# No noisy snack bar for tapping while opponent plays.
change("if(!myTurn){_notice572('Sıra sende değil');return;}","if(!myTurn)return;")
change("const SizedBox(height:2),const Text('Sıra sende',style:TextStyle(fontSize:9,color:Colors.white70))","const SizedBox.shrink()")
# +1 positions must come from the same server room as power placements.
change("powerTiles:room['powerTiles'] is Map?Map<String,dynamic>.from(room['powerTiles'] as Map):null)",
"""powerTiles:room['powerTiles'] is Map?Map<String,dynamic>.from(room['powerTiles'] as Map):null,
   bonusTiles:room['bonusTiles'] is List?(room['bonusTiles'] as List).whereType<num>().map((n)=>n.toInt()).toList():null)""")
change("final int turns;final bool power;final Map<String,dynamic>? powerTiles;\n const Ngelx565BoardPainter({this.turns=0,this.power=false,this.powerTiles});",
"""final int turns;final bool power;final Map<String,dynamic>? powerTiles;final List<int>? bonusTiles;
 const Ngelx565BoardPainter({this.turns=0,this.power=false,this.powerTiles,this.bonusTiles});""")
change("else if(power&&[4,17,30,43].contains(i)){",
       "else if(power&&(bonusTiles??const <int>[4,17,30,43]).contains(i)){")
change("old.turns!=turns||old.power!=power||!mapEquals(old.powerTiles,powerTiles);",
       "old.turns!=turns||old.power!=power||!mapEquals(old.powerTiles,powerTiles)||!listEquals(old.bonusTiles,bonusTiles);")
# Existing glossy source atlas stays in use; crop its wide transparent border
# so a pawn fills the grid square while still never exceeding its own hitbox.
change("final w=atlas.width/2,h=atlas.height/2;canvas.drawImageRect(atlas,Rect.fromLTWH((seat%2)*w,(seat~/2)*h,w,h),Offset.zero&size,Paint()..filterQuality=FilterQuality.high);",
"""final w=atlas.width/2,h=atlas.height/2;
  final src=Rect.fromLTWH((seat%2)*w+w*.095,(seat~/2)*h+h*.035,w*.81,h*.91);
  final dst=Offset.zero&size;
  canvas.drawImageRect(atlas,src,dst,Paint()..filterQuality=FilterQuality.high..isAntiAlias=true);
  if(highlight)canvas.drawRRect(RRect.fromRectAndRadius(dst.deflate(size.width*.01),Radius.circular(size.width*.16)),Paint()..style=PaintingStyle.stroke..strokeWidth=size.width*.035..color=const Color(0xFFFFE77B));""")
# Larger pawn is still bounded to one board cell. Home sockets have slightly more room.
change("final size=c*(widget.position<0?1.04:widget.stackCount > 1 ? 0.49 : 0.91)",
       "final size=c*(widget.position<0?1.13:widget.stackCount > 1 ? 0.49 : 0.98)")
# Clearer score bar; the plus is a visual affordance, never fabricated purchases/balances.
change("Text(amount is num?amount.toInt().toString():'—',style:const TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900))",
       "Text(amount is num?amount.toInt().toString():'—',style:const TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900)),const Spacer(),const Icon(Icons.add_circle_outline_rounded,color:Color(0xFF8FCCFF),size:17)")
# Attach small Messenger-style + to real usable power buttons without changing their action.
change("Positioned(right:0,top:0,child:Container(padding:const EdgeInsets.all(3)",
       "Positioned(right:0,bottom:1,child:Container(width:17,height:17,decoration:BoxDecoration(shape:BoxShape.circle,color:const Color(0xFF114992),border:Border.all(color:const Color(0xFF76E5FF),width:1.1)),child:const Icon(Icons.add_rounded,color:Colors.white,size:13))),Positioned(right:0,top:0,child:Container(padding:const EdgeInsets.all(3)")
# Tile shading, with shadows confined to their own squares and no hitbox changes.
change("canvas.drawRect(rect.deflate(.7),p..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color.lerp(color,Colors.white,.18)!,color,Color.lerp(color,Colors.black,.08)!]).createShader(rect));p.shader=null;",
"""canvas.drawRRect(RRect.fromRectAndRadius(rect.deflate(.7),Radius.circular(rect.width*.075)),
   p..shader=LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,stops:const [0,.47,1],colors:[Color.lerp(color,Colors.white,.38)!,color,Color.lerp(color,Colors.black,.16)!]).createShader(rect));p.shader=null;""")
p.write_text(s,encoding='utf-8')
pub=root/'app/pubspec.yaml'
b=pub.read_text(encoding='utf-8')
assert 'version: 1.0.343+573' in b
pub.write_text(b.replace('version: 1.0.343+573','version: 1.0.344+574',1),encoding='utf-8')
print('Build574 Ludo frontend updated; existing NgelX screens and Android identity unchanged')
