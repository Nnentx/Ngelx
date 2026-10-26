"""Build573: apply reference layout to verified Build572 source."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'app/lib/build565_ludo.dart'
s=p.read_text(encoding='utf-8')
def swap(old,new):
 global s
 if s.count(old)!=1:raise RuntimeError('Build573 mismatch: '+old[:90]+' count='+str(s.count(old)))
 s=s.replace(old,new,1)
swap('stackOffset:ngelx572StackOffset(room,color,token),','stackOffset:ngelx572StackOffset(room,color,token),stackCount:ngelx573PawnCount(room,color,token),')
swap('class _MovingPawn567 extends StatefulWidget {',"""int ngelx573PawnCount(Map<String,dynamic> room,int seat,int token){
 final tokens=room['tokens'] as List,pos=(tokens[seat][token] as num).toInt();
 if(pos<0)return 1;
 String key(int s,int x)=>x<51?'track-${(s*13+x)%52}':'finish-$s-$x';
 final target=key(seat,pos);
 var count=0;
 for(final player in room['players'] as List? ?? []){
  if(player['left']==true)continue;
  final s=(player['seat'] as num).toInt();
  for(final value in tokens[s])if(value is num&&value>=0&&key(s,value.toInt())==target)count++;
 }
 return count.clamp(1,4).toInt();
}
class _MovingPawn567 extends StatefulWidget {""")
swap('final double cell;final bool highlight;final Offset stackOffset;final VoidCallback? onTap;','final double cell;final bool highlight;final Offset stackOffset;final int stackCount;final VoidCallback? onTap;')
swap('required this.highlight,required this.stackOffset,this.onTap','required this.highlight,required this.stackOffset,required this.stackCount,this.onTap')
swap('if(shared.length==2)return Offset(order==0?-.18:.18,0);\n return Offset(order.isEven?-.16:.16,order<2?-.15:.15);','if(shared.length==2)return Offset(order==0?-.23:.23,0);\n return Offset(order.isEven?-.23:.23,order<2?-.20:.20);')
swap('final size=c*1.24,limit=c*15-size;\n  final x=((p.dx+.5+widget.stackOffset.dx)*c-size*.5).clamp(0.0,limit).toDouble();\n  final y=((p.dy+.5+widget.stackOffset.dy)*c-size*.71-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.13).clamp(0.0,limit).toDouble();',
"""final size=c*(widget.position<0?1.04:widget.stackCount>1?.49:.91),limit=c*15-size;
  final x=((p.dx+.5+widget.stackOffset.dx)*c-size*.5).clamp(0.0,limit).toDouble();
  final y=((p.dy+.5+widget.stackOffset.dy)*c-size*.51-math.sin((motion.value*(widget.position-from).abs()%1)*math.pi)*c*.075).clamp(0.0,limit).toDouble();""")
swap('final side=math.min(box.maxWidth,math.max(60.0,box.maxHeight-76)),left=(box.maxWidth-side)/2,top=(box.maxHeight-side)/2;',"""final side=math.min(box.maxWidth,math.max(60.0,box.maxHeight-98)),left=(box.maxWidth-side)/2;
  final top=math.min(46.0,math.max(0.0,box.maxHeight-side-44));""")
swap('final width=math.min(180.0,side*.61)','final width=math.min(180.0,side*.55)')
swap('top:isTop?top-46:top+side-2,width:width,height:44','top:isTop?top-43:top+side-2,width:width,height:42')
swap('Container(width:40,height:40,padding:const EdgeInsets.all(2)','Container(width:38,height:38,padding:const EdgeInsets.all(2)')
swap("child:Text(isMine?'Sen':'${p['name']}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white,fontWeight:FontWeight.w900,fontSize:11))", """child:Text("${p['level'] is num?'Lv.${p['level']}  ':''}${isMine?'Sen':p['name']}",maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:isTurn?_ludoGold567:Colors.white,fontWeight:FontWeight.w900,fontSize:10))""")
swap("@override Widget build(BuildContext context)=>DecoratedBox(decoration:const BoxDecoration(gradient:RadialGradient(center:Alignment(-.4,-.6),radius:1.5,colors:[Color(0xFF4447A0),Color(0xFF303373),Color(0xFF1D2259)])),child:child);", """@override Widget build(BuildContext context)=>DecoratedBox(decoration:const BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFF213D69),Color(0xFF164A70),Color(0xFF122A51)])),child:Stack(children:[const Positioned.fill(child:IgnorePointer(child:CustomPaint(painter:_LudoBackdropPainter573()))),child]));""")
swap('class Ngelx567GameButton extends StatelessWidget {',"""class _LudoBackdropPainter573 extends CustomPainter {
 const _LudoBackdropPainter573();
 @override void paint(Canvas canvas,Size size){
  final p=Paint(),wave=Path()..moveTo(0,size.height*.1)..quadraticBezierTo(size.width*.45,size.height*.06,size.width,size.height*.16)..lineTo(size.width,size.height*.64)..quadraticBezierTo(size.width*.4,size.height*.73,0,size.height*.65)..close();
  canvas.drawPath(wave,p..shader=const LinearGradient(colors:[Color(0xFF28698A),Color(0xFF1D477E),Color(0xFF153C64)]).createShader(Offset.zero&size));p.shader=null;
  for(var i=0;i<17;i++){
   final x=i.isEven?0.0:size.width,y=size.height*(.03+i*.061),r=18.0+(i%4)*9.0;
   canvas.drawCircle(Offset(x,y),r,p..color=Color.lerp(const Color(0xFF184B44),const Color(0xFF216849),(i%3)/3)!);
   canvas.drawCircle(Offset(x+(i.isEven?14:-14),y-10),r*.7,p..color=const Color(0x663AA16B));
  }
 }
 @override bool shouldRepaint(covariant _LudoBackdropPainter573 old)=>false;
}
class Ngelx567GameButton extends StatelessWidget {""")
swap('class Ngelx570Logo extends StatelessWidget {',"""class Ngelx573WalletBar extends StatelessWidget{
 final Map<String,dynamic> room;const Ngelx573WalletBar({super.key,required this.room});
 Widget badge(IconData icon,Color color,dynamic amount,String title)=>Expanded(child:Tooltip(message:title,child:Container(height:33,margin:const EdgeInsets.symmetric(horizontal:4),padding:const EdgeInsets.symmetric(horizontal:8),decoration:ngelx570Bevel(const Color(0xFF161D65),19),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[Icon(icon,color:color,size:19),const SizedBox(width:7),Text(amount is num?amount.toInt().toString():'—',style:const TextStyle(color:Colors.white,fontSize:13,fontWeight:FontWeight.w900))]))));
 @override Widget build(BuildContext context)=>Row(children:[badge(Icons.diamond_rounded,const Color(0xFFC360FF),room['gems'],'Elmas bakiyesi'),badge(Icons.monetization_on_rounded,const Color(0xFFFFD441),room['chips'],'Çip bakiyesi')]);
}
class Ngelx570Logo extends StatelessWidget {""")
swap('toolbarHeight:MediaQuery.sizeOf(context).height<650?56:74','toolbarHeight:MediaQuery.sizeOf(context).height<650?48:62')
swap('body:_LudoBackdrop567(child:SafeArea(bottom:true,child:LayoutBuilder(builder:(context,box){','body:_LudoBackdrop567(child:SafeArea(bottom:true,child:Column(children:[Ngelx573WalletBar(room:room),Expanded(child:LayoutBuilder(builder:(context,box){')
swap('   }))),\n  )));\n }\n}\nWidget _roomLabel567','   }))])),\n  )));\n }\n}\nWidget _roomLabel567')
swap('children:[Center(child:AspectRatio(aspectRatio:.85,child:frame))','children:[Center(child:AspectRatio(aspectRatio:1,child:frame))')
swap('Padding(padding:const EdgeInsets.symmetric(horizontal:4),child:Center(child:AspectRatio(aspectRatio:.85,child:frame)))','Padding(padding:const EdgeInsets.symmetric(horizontal:2),child:Align(alignment:Alignment.topCenter,child:AspectRatio(aspectRatio:1,child:frame)))')
swap('return Padding(padding:const EdgeInsets.fromLTRB(14,6,14,12)','return Padding(padding:const EdgeInsets.fromLTRB(10,3,10,7)')
start=s.index('   ]else if(active)...[',s.index(' Widget _footer(){'))
end=s.index("   ]else...[Text(room['matchmaking']",start)
s=s[:start]+"""   ]else if(active)...[
    Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
     Column(mainAxisSize:MainAxisSize.min,children:[Ngelx570Clock(paused:_chatOpen,deadline:(room['deadline'] as num?)?.toInt()??0,active:myTurn),const SizedBox(height:2),const Text('Sıra sende',style:TextStyle(fontSize:9,color:Colors.white70))]),
     const SizedBox(width:12),GestureDetector(key:const ValueKey('ludo-main-dice'),behavior:HitTestBehavior.opaque,onTap:widget.watch?null:()=>_tapRoll572(myTurn),child:Container(padding:const EdgeInsets.all(6),decoration:ngelx570Bevel(const Color(0xFF211D55),14),child:Ngelx567Dice(value:ngelx570ShownDice(room),size:54,busy:game.busy&&myTurn))),
     const SizedBox(width:12),Expanded(child:Column(children:[SizedBox(height:30,width:double.infinity,child:ngelx570Chip('İyi oyunlar',widget.watch?null:()=>game.perform('chat',{'text':'İyi oyunlar!'}))),const SizedBox(height:5),SizedBox(height:30,width:double.infinity,child:ngelx570Chip('Güzel hamle',widget.watch?null:()=>game.perform('chat',{'text':'Güzel hamle!'})))])),
    ]),const SizedBox(height:8),
    Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
     Column(mainAxisSize:MainAxisSize.min,children:[ngelx570Chip('😊 Emoji',widget.watch?null:_chat),const SizedBox(height:4),ngelx570Chip('Sohbet',widget.watch?null:_chat)]),
     if(room['mode']=='power'&&!widget.watch)...[const SizedBox(width:7),for(final item in [('control','Zar seç'),('double','Çift'),('shield','Kalkan')])Expanded(child:Ngelx570Power(kind:item.$1,label:item.$2,count:(inventory[item.$1] as num?)?.toInt()??0,onTap:()=>_tapPower572(item.$1,(inventory[item.$1] as num?)?.toInt()??0,myTurn)))]
     else Expanded(child:Text(widget.watch?'İZLEYİCİ':'KLASİK LUDO',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800,fontSize:11))),
    ]),
"""+s[end:]
swap('SizedBox(width:62,height:59,child:Stack','SizedBox(width:54,height:49,child:Stack')
swap('Positioned(right:0,top:0,child:Container(padding:const EdgeInsets.all(4)','Positioned(right:0,top:0,child:Container(padding:const EdgeInsets.all(3)')
p.write_text(s,encoding='utf-8')
pub=root/'app/pubspec.yaml';y=pub.read_text()
assert 'version: 1.0.342+572' in y
pub.write_text(y.replace('version: 1.0.342+572','version: 1.0.343+573',1))
print('Build573 Ludo design installed into verified Build572 source')
