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
        return Opacity(opacity:opacity,child:SizedBox(width:double.infinity,height:math.min(MediaQuery.sizeOf(context).height*.62,520.0),child:Stack(alignment:Alignment.center,children:[
          Positioned.fill(child:CustomPaint(painter:_GiftPainter553(t,widget.kind))),
          Positioned.fill(bottom:72,child:Transform.translate(
            offset:Offset(0,reduced?0:math.sin(t*math.pi*5)*5),
            child:Transform.rotate(angle:widget.kind=='Aslan'?0:(t-.5)*(widget.kind=='Evren' ? 0.8 : 0.28),
              child:Transform.scale(scale:reduced?1:
                .78+.22*Curves.easeOutCubic.transform((t/.22).clamp(0.0,1.0)),
                child:Image.asset(widget.kind=='Aslan'?'assets/gifts553/lion.webp':'assets/gifts553/galaxy.webp',
                  fit:BoxFit.contain,filterQuality:FilterQuality.medium))))),
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
    if(kind!='Aslan'){
      c.save();c.translate(center.dx,center.dy);c.rotate(t*math.pi*.7);
      for(var i=0;i<(kind=='Evren'?7:3);i++){
        c.drawOval(Rect.fromCenter(center:Offset.zero,width:radius*(1.5+i*.22),height:radius*(.5+i*.1)),Paint()..color=Color.lerp(const Color(0xFF9F7AFF),const Color(0xFF4DE3FF),i/3)!.withValues(alpha:.65)..style=PaintingStyle.stroke..strokeWidth=3);
        c.rotate(math.pi/4);
      }
      c.drawCircle(Offset.zero,radius*.34,Paint()..shader=const RadialGradient(colors:[Color(0xFFFFFFFF),Color(0xFFD3ACFF),Color(0xFF6A39C4)]).createShader(Rect.fromCircle(center:Offset.zero,radius:radius*.34)));
      c.restore();
    }
  }
  @override bool shouldRepaint(covariant _GiftPainter553 old)=>old.t!=t||old.kind!=kind;
}
