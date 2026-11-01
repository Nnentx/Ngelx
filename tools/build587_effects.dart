part of 'main.dart';

Future<bool> _ngelx587ConfirmDemotion(BuildContext context,String name)async=>
 await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
  title:const Text('Yöneticilikten al'),content:Text('$name adlı kişinin yönetici yetkileri kaldırılsın mı?'),
  actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
   FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Yetkileri kaldır'))]))??false;

/// Price stays beside the single-tap action; the server owns the charge.
class Ngelx587GiftShelf extends StatelessWidget {
 final Map<String,dynamic> items;final bool blocked;final ValueChanged<String> onSend;
 const Ngelx587GiftShelf({super.key,required this.items,required this.blocked,required this.onSend});
 @override Widget build(BuildContext context)=>SizedBox(height:156,child:Scrollbar(child:ListView.separated(
  key:const ValueKey('ludo-gift-shelf'),scrollDirection:Axis.horizontal,
  itemCount:items.length,separatorBuilder:(_,__)=>const SizedBox(width:10),
  itemBuilder:(_,i){final entry=items.entries.elementAt(i),gift=entry.value is Map?entry.value as Map:const {};
   return SizedBox(width:106,child:Material(color:Colors.white,borderRadius:BorderRadius.circular(20),
    child:InkWell(key:ValueKey('ludo-gift-${entry.key}'),borderRadius:BorderRadius.circular(20),
     onTap:blocked?null:()=>onSend(entry.key),child:Container(
      decoration:BoxDecoration(borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE5DBF5))),
      padding:const EdgeInsets.symmetric(horizontal:7,vertical:10),child:Column(children:[
       Ngelx587GiftArt(kind:entry.key,size:60),const SizedBox(height:8),
       Text('${gift['label']??entry.key}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF27204C),fontWeight:FontWeight.w700)),
       const SizedBox(height:4),Text('${gift['chips']??0} çip',style:const TextStyle(color:Color(0xFF625878),fontSize:12,fontWeight:FontWeight.w600)),
      ])))));
  })));
}

class Ngelx587GiftArt extends StatelessWidget {
 final String kind;final double size;
 const Ngelx587GiftArt({super.key,required this.kind,this.size=60});
 @override Widget build(BuildContext context){
  final (icon,colors)=switch(kind){
   'heart'=>(Icons.favorite_rounded,const [Color(0xFFFF789F),Color(0xFFE31C60)]),
   'rose'||'flower'=>(Icons.local_florist_rounded,const [Color(0xFFFF7792),Color(0xFFBD174B)]),
   'crown'=>(Icons.workspace_premium_rounded,const [Color(0xFFFFDF85),Color(0xFFD88A10)]),
   'coffee'=>(Icons.coffee_rounded,const [Color(0xFFE5BE98),Color(0xFF976344)]),
   'like'||'thumbs_up'=>(Icons.thumb_up_rounded,const [Color(0xFF86CEFF),Color(0xFF397AE2)]),
   'tomato'=>(Icons.eco_rounded,const [Color(0xFFFF8D74),Color(0xFFE63B35)]),
   'pizza'=>(Icons.local_pizza_rounded,const [Color(0xFFFFD28E),Color(0xFFE58C31)]),
   'bucket'=>(Icons.water_drop_rounded,const [Color(0xFF8CE5F6),Color(0xFF379EC6)]),
   'clock'=>(Icons.schedule_rounded,const [Color(0xFFB6CAFF),Color(0xFF657AD0)]),
   'flame'=>(Icons.local_fire_department_rounded,const [Color(0xFFFFD56D),Color(0xFFF36531)]),
   'rooster'=>(Icons.pets_rounded,const [Color(0xFFF1CDA1),Color(0xFFB27B4E)]),
   'slipper'=>(Icons.hiking_rounded,const [Color(0xFFABDFC7),Color(0xFF388E80)]),
   'pan'=>(Icons.soup_kitchen_rounded,const [Color(0xFFB1BFCE),Color(0xFF526275)]),
   'plunger'=>(Icons.cleaning_services_rounded,const [Color(0xFFBEA5E1),Color(0xFF7958AC)]),
   'egg'=>(Icons.egg_rounded,const [Color(0xFFFFEAD0),Color(0xFFD7AA74)]),
   'balloon'=>(Icons.celebration_rounded,const [Color(0xFFFFA5D1),Color(0xFFD24F9C)]),
   _=>(Icons.card_giftcard_rounded,const [Color(0xFFC4A3FF),Color(0xFF7650CB)]),
  };
  return Container(width:size,height:size,decoration:BoxDecoration(
   borderRadius:BorderRadius.circular(size*.29),gradient:LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:colors),
   border:Border.all(color:Colors.white.withValues(alpha:.7)),
   boxShadow:[BoxShadow(color:colors.last.withValues(alpha:.25),blurRadius:12,offset:const Offset(0,5))]),
   child:Icon(icon,size:size*.58,color:Colors.white,shadows:const [Shadow(color:Color(0x33000000),blurRadius:3,offset:Offset(0,2))]));
 }
}

/// React only to fresh receipts. Historical hearts never replay on entering.
class Ngelx587Hearts extends StatefulWidget {
 final Map<String,dynamic> room;
 const Ngelx587Hearts({super.key,required this.room});
 @override State<Ngelx587Hearts> createState()=>_Ngelx587HeartsState();
}
class _Ngelx587HeartsState extends State<Ngelx587Hearts> with SingleTickerProviderStateMixin {
 final seen=<String>{};int bursts=0;
 late final AnimationController motion=AnimationController(vsync:this,duration:const Duration(milliseconds:2400))
  ..addStatusListener((s){if(s==AnimationStatus.completed&&bursts>0){bursts--;motion.forward(from:0);}});
 Iterable<Map> _events()=>[
  ...(widget.room['chat'] as List? ?? []).whereType<Map>().where((e)=>e['text']=='❤️'),
  ...(widget.room['gifts'] as List? ?? []).whereType<Map>().where((e)=>e['kind']=='heart'),
 ];
 String _key(Map e)=>'${e['uid']??e['from']}:${e['to']}:${e['at']}';
 @override void initState(){super.initState();seen.addAll(_events().map(_key));}
 @override void didUpdateWidget(covariant Ngelx587Hearts old){
  super.didUpdateWidget(old);final now=DateTime.now().millisecondsSinceEpoch;
  for(final e in _events()){
   if(!seen.add(_key(e)))continue;
   final at=(e['at'] as num?)?.toInt()??0;
   if(now-at<8000&&now-at>=-2000){if(!motion.isAnimating)motion.forward(from:0);else bursts=math.min(2,bursts+1);}
  }
  if(seen.length>96){final current=_events().map(_key).toSet();seen.removeWhere((k)=>!current.contains(k));}
 }
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>IgnorePointer(child:RepaintBoundary(child:AnimatedBuilder(animation:motion,builder:(_,__)=>
  motion.isAnimating?CustomPaint(painter:_Ngelx587HeartsPainter(motion.value),size:Size.infinite):const SizedBox.shrink())));
}
class _Ngelx587HeartsPainter extends CustomPainter {
 final double progress;_Ngelx587HeartsPainter(this.progress);
 @override void paint(Canvas canvas,Size size){
  for(var i=0;i<14;i++){
   final t=((progress-i*.023)/.67).clamp(0.0,1.0);if(t<=0||t>=1)continue;
   final x=size.width*(.10+(i*7%13)/16)+math.sin(t*5+i)*17;
   final y=size.height*(.88-.62*Curves.easeOut.transform(t));
   final radius=10.0+(i%4)*3,alpha=math.sin(t*math.pi)*.85;
   final path=Path()..moveTo(0,radius*.9)..cubicTo(-radius*1.8,-radius*.2,-radius,-radius*1.4,0,-radius*.45)
    ..cubicTo(radius,-radius*1.4,radius*1.8,-radius*.2,0,radius*.9)..close();
   canvas.save();canvas.translate(x,y);canvas.rotate(math.sin(t*4+i)*.22);
   canvas.drawPath(path,Paint()..color=Color(i.isEven?0xFFFF487F:0xFFFF9DBA).withValues(alpha:alpha));canvas.restore();
  }
 }
 @override bool shouldRepaint(_Ngelx587HeartsPainter old)=>old.progress!=progress;
}

/// Shared PK presentation: a full-width pink/cyan score ribbon and clock.
class Ngelx587PkRibbon extends StatelessWidget {
 final int selfScore,opponentScore,remaining;final String selfName,opponentName;
 const Ngelx587PkRibbon({super.key,required this.selfScore,required this.opponentScore,required this.remaining,required this.selfName,required this.opponentName});
 @override Widget build(BuildContext context){
  final a=math.max(0,selfScore),b=math.max(0,opponentScore),ratio=a+b==0 ? .5 : a/(a+b);
  final seconds=remaining.clamp(0,180),clock='${(seconds~/60).toString().padLeft(2,'0')}:${(seconds%60).toString().padLeft(2,'0')}';
  return Column(mainAxisSize:MainAxisSize.min,children:[
   Semantics(label:'PK $selfName $a puan, $opponentName $b puan',child:SizedBox(height:24,child:LayoutBuilder(builder:(_,box)=>Stack(children:[
    const Positioned.fill(child:ColoredBox(color:Color(0xFF18BDD9))),
    AnimatedContainer(duration:const Duration(milliseconds:400),curve:Curves.easeOutCubic,width:box.maxWidth*ratio,height:24,color:const Color(0xFFFF3689)),
    Positioned(left:10,top:1,child:Text('$a',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:17))),
    Positioned(right:10,top:1,child:Text('$b',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:17))),
    const Center(child:Icon(Icons.sports_mma_rounded,color:Colors.white,size:21)),
   ])))),
   Container(padding:const EdgeInsets.symmetric(horizontal:14,vertical:6),
    decoration:const BoxDecoration(color:Color(0xC9252430),borderRadius:BorderRadius.vertical(bottom:Radius.circular(15))),
    child:Row(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.sports_mma_rounded,color:Color(0xFFFF669F),size:16),const SizedBox(width:7),
     Text(clock,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800,fontSize:15,fontFeatures:[ui.FontFeature.tabularFigures()]))])),
  ]);
 }
}

class Ngelx587PkClash extends StatefulWidget {
 const Ngelx587PkClash({super.key});
 @override State<Ngelx587PkClash> createState()=>_Ngelx587PkClashState();
}
class _Ngelx587PkClashState extends State<Ngelx587PkClash> with SingleTickerProviderStateMixin {
 late final AnimationController motion=AnimationController(vsync:this,duration:const Duration(milliseconds:1500))..forward();
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>IgnorePointer(child:AnimatedBuilder(animation:motion,builder:(_,__){
  final t=motion.value;if(t>=1)return const SizedBox.shrink();
  final entrance=Curves.easeOutBack.transform((t/.4).clamp(0.0,1.0));
  return Opacity(opacity:t<.75?1:((1-t)/.25).clamp(0.0,1.0),child:SizedBox(height:120,child:Stack(alignment:Alignment.center,children:[
   Container(width:100+25*t,height:100+25*t,decoration:BoxDecoration(shape:BoxShape.circle,
    gradient:RadialGradient(colors:[const Color(0xFFFFDF88).withValues(alpha:.8),Colors.transparent]))),
   for(final left in [true,false])Transform.translate(offset:Offset((left?-1:1)*(70-42*entrance),0),child:Transform.rotate(angle:left?-.35:.35,
    child:Container(width:64,height:64,decoration:BoxDecoration(shape:BoxShape.circle,
     gradient:LinearGradient(colors:left?const [Color(0xFFFF83BB),Color(0xFFE31D72)]:const [Color(0xFF7AEEFF),Color(0xFF05AFCB)]),
     border:Border.all(color:Colors.white,width:2),boxShadow:const [BoxShadow(color:Color(0x66FFE49D),blurRadius:20)]),
     child:const Icon(Icons.sports_mma_rounded,color:Colors.white,size:35)))),
   const Icon(Icons.bolt_rounded,color:Color(0xFFFFF1B9),size:36),
  ])));
 }));
}
