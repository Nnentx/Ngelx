"""Build572: visual reference, touch feedback, clipped/overlapping pawns and live Power locations.
Applies to the verified Build571 assembled source, never to unrelated NgelX modules.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'app/lib/build565_ludo.dart'
s=p.read_text()

def replace(old,new,expected=1):
 global s
 actual=s.count(old)
 if actual!=expected:raise RuntimeError(f'Build572 source mismatch: expected {expected}, got {actual}: {old[:110]}')
 s=s.replace(old,new)

replace("return Stack(children:[Positioned.fill(child:CustomPaint(painter:Ngelx565BoardPainter(turns:turns,power:room['mode']=='power')))",
        "return Stack(clipBehavior:Clip.none,children:[Positioned.fill(child:CustomPaint(painter:Ngelx565BoardPainter(turns:turns,power:room['mode']=='power',powerTiles:room['powerTiles'] is Map?Map<String,dynamic>.from(room['powerTiles'] as Map):null)))")
replace("for(final color in seats)for(var token=0;token<4;token++)_MovingPawn567(",
        "for(final color in seats)for(var token=0;token<4;token++)_MovingPawn567(stackOffset:ngelx572StackOffset(room,color,token),")
replace("class _MovingPawn567 extends StatefulWidget {",
"""Offset ngelx572StackOffset(Map<String,dynamic> room,int seat,int token){
 final tokens=room['tokens'] as List;
 final position=(tokens[seat][token] as num).toInt();
 if(position<0)return Offset.zero;
 String key(int s,int pos)=>pos<51?'track-${(s*13+pos)%52}':'finish-$s-$pos';
 final mine=key(seat,position);
 final players=room['players'] as List? ?? [];
 final shared=<String>[];
 for(final player in players){
  if(player['left']==true)continue;
  final s=(player['seat'] as num).toInt();
  for(var i=0;i<4;i++){final pos=(tokens[s][i] as num).toInt();if(pos>=0&&key(s,pos)==mine)shared.add('$s-$i');}
 }
 if(shared.length<2)return Offset.zero;
 final order=shared.indexOf('$seat-$token');
 if(shared.length==2)return Offset(order==0?-.18:.18,0);
 return Offset(order.isEven?-.16:.16,order<2?-.15:.15);
}
class _MovingPawn567 extends StatefulWidget {""")
replace("final double cell;final bool highlight;final VoidCallback? onTap;",
        "final double cell;final bool highlight;final Offset stackOffset;final VoidCallback? onTap;")
replace("required this.cell,required this.turns,required this.highlight,this.onTap",
        "required this.cell,required this.turns,required this.highlight,required this.stackOffset,this.onTap")
old="return Positioned(left:(p.dx+.5)*c-c*.56,top:(p.dy+.5)*c-c*.8624-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.17,width:c*1.12,height:c*1.12"
new="""final size=c*1.24,limit=c*15-size;
  final x=((p.dx+.5+widget.stackOffset.dx)*c-size*.5).clamp(0.0,limit).toDouble();
  final y=((p.dy+.5+widget.stackOffset.dy)*c-size*.71-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.13).clamp(0.0,limit).toDouble();
  return Positioned(left:x,top:y,width:size,height:size"""
replace(old,new)

replace("final int turns;final bool power;\n const Ngelx565BoardPainter({this.turns=0,this.power=false});",
"final int turns;final bool power;final Map<String,dynamic>? powerTiles;\n const Ngelx565BoardPainter({this.turns=0,this.power=false,this.powerTiles});")
replace("const pickup=[2,5,10,15,18,23,28,31,36,41,44,49];",
"""const pickup=[2,5,10,15,18,23,28,31,36,41,44,49];
  final tiles=powerTiles??{for(var i=0;i<pickup.length;i)'${pickup[i]}':['control','double','shield'][i%3]};""")
replace("else if(power&&pickup.contains(i)){","else if(power&&tiles.containsKey('$i')){")
replace("Ngelx570PowerPainter(['control','double','shield'][pickup.indexOf(i)%3])",
        "Ngelx570PowerPainter(tiles['$i'].toString())")
replace("old.turns!=turns||old.power!=power;","old.turns!=turns||old.power!=power||!mapEquals(old.powerTiles,powerTiles);")

replace("top:isTop?top-40:top+side+4,width:width,height:36",
        "top:isTop?top-46:top+side-2,width:width,height:44")
replace("Container(width:34,height:34,padding:const EdgeInsets.all(2)",
        "Container(width:40,height:40,padding:const EdgeInsets.all(2)")
replace("final width=math.min(180.0,side*.57)",
        "final width=math.min(180.0,side*.61)")
replace("Flexible(child:Text(isMine?'Sen':'${p['name']}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white70,fontWeight:FontWeight.w800,fontSize:11)))",
        "Flexible(child:Container(padding:const EdgeInsets.symmetric(horizontal:6,vertical:4),decoration:BoxDecoration(color:const Color(0xEE141340),borderRadius:BorderRadius.circular(14),border:Border.all(color:ngelx565LudoColors[color])),child:Text(isMine?'Sen':'${p['name']}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white,fontWeight:FontWeight.w900,fontSize:11))))")

replace("appBar:AppBar(leading:IconButton(key:const ValueKey('ludo-back')",
        "appBar:AppBar(toolbarHeight:74,centerTitle:true,leading:IconButton(key:const ValueKey('ludo-back')")
replace("title:const Ngelx570Logo(),actions:[Center(child:",
        "title:Column(mainAxisSize:MainAxisSize.min,children:[Text(ngelx572ModeTitle(room),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFFFFD763),fontSize:13,fontWeight:FontWeight.w900,shadows:[Shadow(color:Colors.black54,offset:Offset(0,2),blurRadius:3)])),const Ngelx570Logo()]),actions:[Center(child:")
replace("class Ngelx570Logo extends StatelessWidget {",
"""String ngelx572ModeTitle(Map<String,dynamic> room){
 if(room['botGame']==true)return 'MAKİNEYE KARŞI';
 final mode=room['mode']=='power'?'POWER':'KLASİK';
 return '$mode • ${room['capacity']??2} KİŞİ';
}
class Ngelx570Logo extends StatelessWidget {""")
replace("Color(0xFFFFD83C),Color(0xFF42E6FF)",
        "Color(0xFFF94C53),Color(0xFFFFD83C),Color(0xFF40E990),Color(0xFF42E6FF)")
replace("style:const TextStyle(fontSize:25,fontWeight:FontWeight.w900",
        "style:const TextStyle(fontSize:28,fontWeight:FontWeight.w900")

replace("GestureDetector(onTap:myTurn&&!game.busy&&room['dice']==null?()=>game.perform('roll'):null,child:Container(padding:const EdgeInsets.all(7)",
        "GestureDetector(key:const ValueKey('ludo-main-dice'),behavior:HitTestBehavior.opaque,onTap:widget.watch?null:()=>_tapRoll572(myTurn),child:Container(padding:const EdgeInsets.all(8)")
replace("Ngelx567Dice(value:ngelx570ShownDice(room),size:52",
        "Ngelx567Dice(value:ngelx570ShownDice(room),size:56")
replace("onTap:myTurn&&!game.busy&&(inventory[item.$1]??0)>0&&(item.$1!='control'||room['dice']==null)&&(item.$1!='double'||room['dice']!=null)?()=>_power(item.$1):null",
        "onTap:()=>_tapPower572(item.$1,(inventory[item.$1] as num?)?.toInt()??0,myTurn)")
replace(" Future<void> _power(String kind)async{",
""" void _notice572(String message){
  if(!mounted)return;
  ScaffoldMessenger.of(context).hideCurrentSnackBar();
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(message),duration:const Duration(seconds:2)));
 }
 void _tapRoll572(bool myTurn){
  if(game.busy){_notice572('Hamle işleniyor');return;}
  if(!myTurn){_notice572('Sıra sende değil');return;}
  if(room['dice']!=null){_notice572('Önce parlayan taşını seç');return;}
  unawaited(game.perform('roll'));
 }
 void _tapPower572(String kind,int count,bool myTurn){
  if(game.busy){_notice572('Hamle işleniyor');return;}
  if(!myTurn){_notice572('Bu güç sıra sendeyken kullanılabilir');return;}
  if(count<=0){_notice572('Bu güçten kalmadı; tahtadan toplayabilirsin');return;}
  if(kind=='control'&&room['dice']!=null){_notice572('Zar seçme hakkını zar atmadan önce kullan');return;}
  if(kind=='double'&&(room['dice']==null||room['doubled']==true)){_notice572('Çift gücünü zar attıktan sonra kullan');return;}
  unawaited(_power(kind));
 }
 Future<void> _power(String kind)async{""")
replace("if(kind!='control'){await game.perform('power',{'kind':kind});return;}",
        "if(kind!='control'){final ok=await game.perform('power',{'kind':kind});_notice572(ok?(kind=='shield'?'Kalkan etkinleştirildi':'Çift hareket etkinleştirildi'):game.error);return;}")
replace("if(value!=null)await game.perform('power',{'kind':'control','number':value});",
        "if(value!=null){final ok=await game.perform('power',{'kind':'control','number':value});if(!ok)_notice572(game.error);}")
p.write_text(s)
pub=root/'app/pubspec.yaml'
content=pub.read_text()
assert 'version: 1.0.341+571' in content
pub.write_text(content.replace('version: 1.0.341+571','version: 1.0.342+572',1))
print('Build572 applied; Android app remains unchanged outside Ludo part and version.')
