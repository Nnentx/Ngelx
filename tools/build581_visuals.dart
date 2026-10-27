// Build581 approved Ludo visuals. Part content is appended to build565_ludo.dart.
class Ngelx581Hero extends StatelessWidget {
 const Ngelx581Hero({super.key});
 @override Widget build(BuildContext context) => SizedBox(height:166,child:Stack(children:[
  Positioned.fill(child:DecoratedBox(decoration:const BoxDecoration(gradient:LinearGradient(colors:[Color(0xFF0E266E),Color(0xFF2923A0),Color(0xFF122B73)]),borderRadius:BorderRadius.all(Radius.circular(22))))),
  const Positioned(left:20,top:17,child:Text('LUDO',style:TextStyle(color:Color(0xFFFFDB52),fontSize:51,fontWeight:FontWeight.w900,letterSpacing:2,shadows:[Shadow(color:Color(0xFFB96100),offset:Offset(2,5),blurRadius:2)]))),
  const Positioned(left:21,bottom:25,child:Text('Arkadaşlarınla aynı masada',style:TextStyle(color:Color(0xFFD9DEFF),fontSize:12,fontWeight:FontWeight.w700))),
  Positioned(right:7,top:7,bottom:8,width:148,child:CustomPaint(painter:Ngelx581BoardArt())),
 ]));
}
class Ngelx581BoardArt extends CustomPainter {
 const Ngelx581BoardArt();
 @override void paint(Canvas canvas,Size size){
  final p=Paint();
  final board=RRect.fromRectAndRadius(Rect.fromLTWH(5,size.height*.43,size.width-10,size.height*.50),const Radius.circular(12));
  canvas.drawRRect(board,p..color=const Color(0xFFDEE9FF));
  const tile=[Color(0xFFF24B55),Color(0xFF2E8EFB),Color(0xFFFED058),Color(0xFF35B97A)];
  for(var x=0;x<6;x++){for(var y=0;y<4;y++){
   p.color=tile[((x~/3)+(y~/2)*2)%4].withValues(alpha:.9);
   canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(9+x*(size.width-18)/6,size.height*.45+y*(size.height*.46)/4,(size.width-20)/6,(size.height*.44)/4),const Radius.circular(2)),p);
  }}
  for(var i=0;i<4;i++){
   final x=24.0+i*32,y=size.height*(i.isEven ? .49 : .63);
   canvas.drawOval(Rect.fromCenter(center:Offset(x+2,y+30),width:30,height:10),p..color=Colors.black26);
   canvas.drawCircle(Offset(x,y-4),13,p..color=tile[i]);
   final path=Path()..moveTo(x-12,y+7)..lineTo(x+12,y+7)..lineTo(x+17,y+28)..lineTo(x-17,y+28)..close();
   canvas.drawPath(path,p..color=tile[i]);
   canvas.drawCircle(Offset(x-4,y-8),4,p..color=Colors.white38);
  }
  canvas.save();canvas.translate(size.width*.59,size.height*.15);canvas.rotate(-.20);
  final die=RRect.fromRectAndRadius(const Rect.fromLTWH(0,0,54,54),const Radius.circular(11));
  canvas.drawRRect(die,p..color=Colors.white);
  p.color=const Color(0xFF4E348B);
  for(final point in [const Offset(13,13),const Offset(40,13),const Offset(26,27),const Offset(13,41),const Offset(40,41)])canvas.drawCircle(point,4.6,p);
  canvas.restore();
 }
 @override bool shouldRepaint(covariant Ngelx581BoardArt old)=>false;
}
class Ngelx581QuickAction extends StatelessWidget{
 final String label;final IconData icon;final VoidCallback? action;final Key? actionKey;
 const Ngelx581QuickAction({super.key,required this.label,required this.icon,this.action,this.actionKey});
 @override Widget build(BuildContext context)=>OutlinedButton.icon(
  key:actionKey,onPressed:action,icon:Icon(icon,size:17,color:const Color(0xFFFFCF66)),
  label:Text(label,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12,fontWeight:FontWeight.w700)),
  style:OutlinedButton.styleFrom(side:const BorderSide(color:Color(0xFF8F80E9)),backgroundColor:const Color(0x992E2D89),padding:const EdgeInsets.symmetric(horizontal:7,vertical:10),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(28))));
}
class Ngelx581StatsScreen extends StatelessWidget{
 final Map<String,dynamic> stats;
 const Ngelx581StatsScreen({super.key,required this.stats});
 int _int(String key){final value=stats[key];return value is num?value.toInt():0;}
 int get _gifts {final x=stats['receivedGifts'];return x is Map?x.values.whereType<num>().fold<int>(0,(a,b)=>a+b.toInt()):0;}
 @override Widget build(BuildContext context){
  final wins=_int('wins'),losses=_int('losses'),all=wins+losses;
  // Progression matches the server's level578(xp) threshold exactly.
  final level=_int('level').clamp(1,10000),xp=_int('xp');
  final levelStart=50*level*level+50*level-100;
  final nextXp=50*(level+1)*(level+1)+50*(level+1)-100;
  final progress=((xp-levelStart)/(nextXp-levelStart)).clamp(0.0,1.0);
  final user=FirebaseAuth.instance.currentUser;
  final info=user==null?null:FirebaseFirestore.instance.collection('users').doc(user.uid).get();
  const white=Color(0xFFF9F8FF),dim=Color(0xFFBBC7F7),gold=Color(0xFFFFD658);
  return Theme(data:ngelx567LudoTheme(),child:Scaffold(
   backgroundColor:const Color(0xFF071C62),
   appBar:AppBar(title:const Text('NgelX Ludo',style:TextStyle(fontWeight:FontWeight.w900)),backgroundColor:const Color(0xFF32228F)),
   body:SafeArea(child:ListView(key:const ValueKey('ludo-stats-page'),padding:const EdgeInsets.fromLTRB(14,10,14,26),children:[
    const Ngelx581Hero(),const SizedBox(height:14),
    FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
     future:info,builder:(context,snapshot){
      final profile=snapshot.data?.data()??<String,dynamic>{};
      final name=(profile['displayName']??profile['username']??user?.displayName??'Oyuncu').toString();
      final photo=(profile['photoUrl']??user?.photoURL??'').toString();
      return Container(padding:const EdgeInsets.all(14),decoration:_ngelx581Panel(),child:Column(children:[
       Row(children:[
        CircleAvatar(radius:36,backgroundColor:const Color(0xFF7E5CEF),
         backgroundImage:photo.isEmpty?null:ResizeImage(NgelXAgImageProvider(photo),width:170),
         child:photo.isEmpty?const Icon(Icons.person_rounded,color:Colors.white,size:35):null),
        const SizedBox(width:12),
        Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
         Text(name,overflow:TextOverflow.ellipsis,maxLines:1,style:const TextStyle(color:white,fontSize:19,fontWeight:FontWeight.w900)),
         Text('Seviye ${_int('level')}',style:const TextStyle(color:dim,fontSize:15)),
        ])),
        Column(crossAxisAlignment:CrossAxisAlignment.end,children:[
         const Icon(Icons.monetization_on_rounded,color:gold,size:27),
         Text('${_int('chips')}',style:const TextStyle(color:gold,fontSize:18,fontWeight:FontWeight.w900)),
         const Text('Toplam Çip',style:TextStyle(color:dim,fontSize:10))
        ])
       ]),
       const SizedBox(height:15),
       Row(children:[const Icon(Icons.star_rounded,color:gold),const SizedBox(width:7),const Text('XP',style:TextStyle(color:white,fontWeight:FontWeight.bold)),
        const Spacer(),Text('$xp / $nextXp XP',style:const TextStyle(color:gold,fontWeight:FontWeight.w800))]),
       const SizedBox(height:7),ClipRRect(borderRadius:BorderRadius.circular(12),child:LinearProgressIndicator(value:progress,minHeight:8,color:gold,backgroundColor:const Color(0xFF383591))),
      ]));
     }),
    const SizedBox(height:12),
    LayoutBuilder(builder:(context,box){
     final width=(box.maxWidth-10)/2;
     return Wrap(spacing:10,runSpacing:10,children:[
      _stat('Çip',_int('chips'),Icons.monetization_on_rounded,gold,width),
      _stat('Elmas',_int('gems'),Icons.diamond_rounded,const Color(0xFF45DFFF),width),
      _stat('Seviye',_int('level'),Icons.stars_rounded,const Color(0xFFDF91FF),width),
      _stat('XP',_int('xp'),Icons.bolt_rounded,gold,width),
      _stat('Galibiyet',wins,Icons.emoji_events_rounded,const Color(0xFF7EF3A7),width),
      _stat('Mağlubiyet',losses,Icons.sports_martial_arts_rounded,const Color(0xFFFF7F9F),width),
      _stat('Toplanan hediye',_gifts,Icons.card_giftcard_rounded,const Color(0xFFE2A0FF),width),
      _stat('Galibiyet serisi',_int('streak'),Icons.local_fire_department_rounded,gold,width),
     ]);
    }),
    const SizedBox(height:14),
    Container(padding:const EdgeInsets.all(15),decoration:_ngelx581Panel(),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
     const Row(children:[Icon(Icons.bar_chart_rounded,color:Color(0xFF77DAFF)),SizedBox(width:9),Text('Oyun geçmişim',style:TextStyle(color:white,fontWeight:FontWeight.w900,fontSize:19))]),
     const SizedBox(height:14),
     _bar('Kazanılan oyunlar',wins,all,const Color(0xFF7EF3A7)),
     const SizedBox(height:11),
     _bar('Kaybedilen oyunlar',losses,all,const Color(0xFFFF699D)),
     const SizedBox(height:12),
     Row(children:[const Icon(Icons.casino_rounded,color:dim),const SizedBox(width:9),const Expanded(child:Text('Toplam oyun',style:TextStyle(color:white))),Text('$all',style:const TextStyle(color:white,fontWeight:FontWeight.w900,fontSize:17))]),
    ])),
    const SizedBox(height:14),
    Container(padding:const EdgeInsets.all(15),decoration:_ngelx581Panel(),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
     const Row(children:[Icon(Icons.workspace_premium_rounded,color:gold),SizedBox(width:9),Expanded(child:Text('Son başarılarım',style:TextStyle(color:white,fontWeight:FontWeight.w900,fontSize:19)))]),
     const SizedBox(height:14),
     Row(children:[
      _award('İlk Oyun','1 oyun oyna',Icons.casino_rounded,all>=1),
      _award('Galibiyet','1 oyun kazan',Icons.emoji_events_rounded,wins>=1),
      _award('Seri','2 maç üst üste',Icons.local_fire_department_rounded,_int('streak')>=2),
      _award('Usta','10 oyun kazan',Icons.lock_rounded,wins>=10),
      _award('Şampiyon','50 oyun kazan',Icons.lock_rounded,wins>=50),
     ])
    ])),
   ]))));
 }
 static BoxDecoration _ngelx581Panel()=>BoxDecoration(
  gradient:const LinearGradient(colors:[Color(0xFF3438A1),Color(0xFF39208B)]),borderRadius:BorderRadius.circular(20),
  border:Border.all(color:const Color(0xFF6C55D6),width:1.3),boxShadow:const [BoxShadow(color:Color(0x33000000),blurRadius:10,offset:Offset(0,5))]);
 Widget _stat(String title,int value,IconData icon,Color color,double width)=>Container(
  width:width,height:115,decoration:_ngelx581Panel(),padding:const EdgeInsets.all(11),
  child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
   Icon(icon,color:color,size:30),const SizedBox(height:5),
   Text(title,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:13)),
   Text('$value',style:TextStyle(color:color,fontSize:24,fontWeight:FontWeight.w900)),
  ]));
 Widget _bar(String title,int count,int total,Color color){
  final percent=total==0?0:(count*100/total).round();
  return Row(children:[
   Expanded(flex:4,child:Text(title,style:const TextStyle(color:Colors.white,fontSize:13))),
   Expanded(flex:4,child:ClipRRect(borderRadius:BorderRadius.circular(9),child:LinearProgressIndicator(value:total==0?0:count/total,minHeight:9,color:color,backgroundColor:const Color(0xFF282A85)))),
   const SizedBox(width:10),Text('$count',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),const SizedBox(width:5),
   Text('%$percent',style:const TextStyle(color:Color(0xFFB3B7EA),fontSize:12))
  ]);
 }
 Widget _award(String label,String detail,IconData icon,bool earned)=>Expanded(child:Opacity(
  opacity:earned?1:.55,child:Column(children:[
   CircleAvatar(radius:22,backgroundColor:earned?const Color(0xFFD4A23C):const Color(0xFF566092),child:Icon(icon,color:Colors.white)),
   const SizedBox(height:6),
   Text(label,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w700,fontSize:11)),
   Text(detail,textAlign:TextAlign.center,maxLines:2,style:const TextStyle(color:Color(0xFFB9C7FF),fontSize:9))
  ])));
}
