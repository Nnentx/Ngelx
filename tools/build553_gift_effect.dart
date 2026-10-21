import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Original NgelX vector effects. No network, audio, or hit-test interception.
class Ngelx553GiftEffect extends StatefulWidget {
  final String kind, sender;
  final int quantity;
  const Ngelx553GiftEffect({super.key,required this.kind,required this.sender,required this.quantity});
  @override State<Ngelx553GiftEffect> createState()=>_Ngelx553GiftEffectState();
}
class _Ngelx553GiftEffectState extends State<Ngelx553GiftEffect> with SingleTickerProviderStateMixin {
  late final AnimationController _animation=AnimationController(vsync:this,duration:const Duration(seconds:7))..forward();
  @override void dispose(){_animation.dispose();super.dispose();}
  @override Widget build(BuildContext context){
    final reduced=MediaQuery.disableAnimationsOf(context);
    return IgnorePointer(child:Semantics(label:'${widget.sender}: ${widget.kind} hediyesi, ${widget.quantity} adet',
      child:AnimatedBuilder(animation:_animation,builder:(_,__) {
        final t=reduced ? 0.5 : _animation.value;
        final opacity=reduced?1.0:math.min(1.0,math.min(t*8,(1-t)*8)).clamp(0.0,1.0).toDouble();
        return Opacity(opacity:opacity,child:SizedBox(width:double.infinity,height:350,child:Stack(alignment:Alignment.center,children:[
          Positioned.fill(child:CustomPaint(painter:_GiftPainter553(t,widget.kind))),
          Positioned(left:24,right:24,bottom:12,child:Container(
            padding:const EdgeInsets.symmetric(horizontal:16,vertical:10),
            decoration:BoxDecoration(color:const Color(0xDD151023),borderRadius:BorderRadius.circular(24),border:Border.all(color:const Color(0xFFFFD881))),
            child:Column(mainAxisSize:MainAxisSize.min,children:[
              Text('${widget.kind} ×${widget.quantity}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFFFFD881),fontSize:22,fontWeight:FontWeight.w900)),
              Text('${widget.sender} gönderdi',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:13)),
            ]))),
        ])));
      })));
  }
}
class _GiftPainter553 extends CustomPainter {
  final double t;final String kind;
  _GiftPainter553(this.t,this.kind);
  @override void paint(Canvas c,Size s){
    final center=Offset(s.width/2,s.height*.42);
    final radius=math.min(s.width*.31,110.0);
    final glow=Paint()..shader=RadialGradient(colors:[const Color(0x776D46FF),Colors.transparent]).createShader(Rect.fromCircle(center:center,radius:radius*1.8));
    c.drawCircle(center,radius*1.8,glow);
    for(var i=0;i<54;i++){
      final angle=i*2.39996+t*math.pi*(i%2==0?1:-1);
      final distance=radius*(.3+(i%13)/10);
      final p=center+Offset(math.cos(angle)*distance,math.sin(angle)*distance*.8);
      c.drawCircle(p,1.2+(i%3)*.7,Paint()..color=Color.lerp(const Color(0xFFFFE3A3),const Color(0xFFB6A2FF),(i%7)/6)!.withValues(alpha:.8));
    }
    if(kind=='Aslan'){
      c.save();c.translate(center.dx,center.dy+math.sin(t*math.pi*6)*5);
      for(var i=0;i<18;i++){
        final a=i*math.pi/9;final p=Offset(math.cos(a)*radius*.61,math.sin(a)*radius*.61);
        c.drawOval(Rect.fromCenter(center:p,width:radius*.68,height:radius*.73),Paint()..color=i%2==0?const Color(0xFFB55F21):const Color(0xFFDC8B31));
      }
      c.drawOval(Rect.fromCenter(center:Offset.zero,width:radius*1.15,height:radius*1.3),Paint()..color=const Color(0xFFFFCF70));
      for(final side in [-1.0,1.0]){
        c.drawCircle(Offset(side*radius*.43,-radius*.48),radius*.2,Paint()..color=const Color(0xFFF4B95B));
        final eye=Offset(side*radius*.23,-radius*.12);
        c.drawOval(Rect.fromCenter(center:eye,width:radius*.14,height:radius*.10),Paint()..color=const Color(0xFF2B1822));
        c.drawCircle(Offset(side*radius*.16,radius*.28),radius*.22,Paint()..color=const Color(0xFFFFE8B4));
      }
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromCenter(center:Offset(0,radius*.2),width:radius*.22,height:radius*.15),Radius.circular(radius*.06)),Paint()..color=const Color(0xFF492526));
      final mouth=Path()..moveTo(0,radius*.28)..quadraticBezierTo(-radius*.04,radius*.47,-radius*.22,radius*.4)..moveTo(0,radius*.28)..quadraticBezierTo(radius*.04,radius*.47,radius*.22,radius*.4);
      c.drawPath(mouth,Paint()..color=const Color(0xFF492526)..style=PaintingStyle.stroke..strokeWidth=3);
      c.restore();
    }else{
      c.save();c.translate(center.dx,center.dy);c.rotate(t*math.pi*.7);
      for(var i=0;i<4;i++){
        c.drawOval(Rect.fromCenter(center:Offset.zero,width:radius*(1.5+i*.22),height:radius*(.5+i*.1)),Paint()..color=Color.lerp(const Color(0xFF9F7AFF),const Color(0xFF4DE3FF),i/3)!.withValues(alpha:.65)..style=PaintingStyle.stroke..strokeWidth=3);
        c.rotate(math.pi/4);
      }
      c.drawCircle(Offset.zero,radius*.34,Paint()..shader=const RadialGradient(colors:[Color(0xFFFFFFFF),Color(0xFFD3ACFF),Color(0xFF6A39C4)]).createShader(Rect.fromCircle(center:Offset.zero,radius:radius*.34)));
      c.restore();
    }
  }
  @override bool shouldRepaint(covariant _GiftPainter553 old)=>old.t!=t||old.kind!=kind;
}
