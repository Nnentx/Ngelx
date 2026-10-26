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
swap(' Future<void> _autoSingleMove574()async{',""" void _tapAuto575(bool active){
  if(widget.watch||game.busy||!game.playing||game.seat<0)return;
  unawaited(game.perform('auto',{'enabled':!active}));
 }
 Future<void> _autoSingleMove574()async{""")
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
