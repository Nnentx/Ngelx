class Ngelx580Victory extends StatefulWidget{
 final String name;const Ngelx580Victory({super.key,required this.name});
 @override State<Ngelx580Victory> createState()=>_Ngelx580VictoryState();
}
class _Ngelx580VictoryState extends State<Ngelx580Victory> with SingleTickerProviderStateMixin{
 late final AnimationController motion=AnimationController(vsync:this,duration:const Duration(seconds:4))..forward();
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>Material(key:const ValueKey('ludo-fullscreen-victory'),color:const Color(0xF522174C),child:SafeArea(child:Stack(children:[
  Positioned.fill(child:RepaintBoundary(child:CustomPaint(painter:_Ngelx580Confetti(motion)))),
  Center(child:Padding(padding:const EdgeInsets.all(28),child:Column(mainAxisSize:MainAxisSize.min,children:[
   TweenAnimationBuilder<double>(tween:Tween(begin:.3,end:1),duration:const Duration(milliseconds:850),curve:Curves.elasticOut,builder:(_,value,child)=>Transform.scale(scale:value,child:child),child:const Icon(Icons.emoji_events_rounded,size:112,color:Color(0xFFFFDC68))),
   const SizedBox(height:26),Text(widget.name,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontSize:34,fontWeight:FontWeight.w900,height:1.2)),
   const SizedBox(height:14),const Text('TEBRİKLER!',style:TextStyle(color:Color(0xFFFFDC68),fontSize:17,fontWeight:FontWeight.w800,letterSpacing:4)),
  ]))),
 ])));
}
class _Ngelx580Confetti extends CustomPainter{
 final Animation<double> motion;_Ngelx580Confetti(this.motion):super(repaint:motion);
 @override void paint(Canvas canvas,Size size){
  const colors=[Color(0xFFFFDA66),Color(0xFF60E7FF),Color(0xFFFF86C8),Color(0xFF97FFBF)];
  final p=Paint();
  for(var i=0;i<64;i++){
   final x=((i*73)%101)/101*size.width,y=((motion.value*1.6+i*.071)%1)*(size.height+40)-20;
   canvas.save();canvas.translate(x,y);canvas.rotate(i+motion.value*8);canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-3,-6,6,12),const Radius.circular(1.5)),p..color=colors[i%4]);canvas.restore();
  }
 }
 @override bool shouldRepaint(covariant _Ngelx580Confetti old)=>old.motion!=motion;
}
