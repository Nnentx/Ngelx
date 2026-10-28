part of 'main.dart';

// Resolve enlarged targets once at board level. Inactive pawns cannot intercept
// touches, and overlapping targets always select the nearest legal piece.
int? ngelx583HitToken(Map<String,dynamic> room,int seat,double cell,Offset tap){
 if(seat<0||cell<=0)return null;
 final turns=(3-seat+4)%4;
 int? nearest;var distance=double.infinity;
 for(final token in ngelx565Legal(room,seat)){
  final position=(room['tokens'][seat][token] as num).toInt();
  final point=ngelx565Rotate(ngelx565TokenPoint(seat,token,position),turns);
  final shift=ngelx572StackOffset(room,seat,token);
  final size=ngelx578PawnSize(cell,position,ngelx573PawnCount(room,seat,token));
  final center=Offset((point.dx+.5+shift.dx)*cell,
   ngelx578FootY((point.dy+.5+shift.dy)*cell,cell,position)-size*.39);
  final d=(center-tap).distance;
  if(d<=math.max(24.0,cell*.85)&&d<distance){nearest=token;distance=d;}
 }
 return nearest;
}

class Ngelx583GiftQueue {
 final _seen=<String>{};final pending=<Map<String,dynamic>>[];
 bool _ready=false;
 void observe(dynamic raw,int now){
  if(raw is! List){_ready=true;return;}
  final current=<String>{};
  for(final item in raw.whereType<Map>()){
   final at=(item['at'] as num?)?.toInt();if(at==null)continue;
   final key='${item['from']}:${item['to']}:${item['kind']}:$at';
   current.add(key);
   if(_ready&&!_seen.contains(key)&&now-at>=-2000&&now-at<8000&&pending.length<6){
    pending.add(Map<String,dynamic>.from(item));
   }
  }
  _seen.addAll(current);
  // Server retains twelve receipts; bound local memory while preserving overlap.
  if(_seen.length>96){_seen.removeWhere((key)=>!current.contains(key));}
  _ready=true;
 }
}

class Ngelx583GiftFlight extends StatefulWidget {
 final Map<String,dynamic> room;final int seat;final double side,left,top;
 const Ngelx583GiftFlight({super.key,required this.room,required this.seat,
  required this.side,required this.left,required this.top});
 @override State<Ngelx583GiftFlight> createState()=>_Ngelx583GiftFlightState();
}
class _Ngelx583GiftFlightState extends State<Ngelx583GiftFlight> with SingleTickerProviderStateMixin{
 final queue=Ngelx583GiftQueue();Map<String,dynamic>? gift;
 late final AnimationController motion=AnimationController(vsync:this,duration:const Duration(milliseconds:1600))
  ..addStatusListener((status){if(status==AnimationStatus.completed&&mounted){setState(()=>gift=null);_next();}});
 @override void initState(){super.initState();queue.observe(widget.room['gifts'],DateTime.now().millisecondsSinceEpoch);}
 @override void didUpdateWidget(covariant Ngelx583GiftFlight old){
  super.didUpdateWidget(old);queue.observe(widget.room['gifts'],DateTime.now().millisecondsSinceEpoch);_next();
 }
 void _next(){
  if(gift!=null||queue.pending.isEmpty)return;
  gift=queue.pending.removeAt(0);motion.forward(from:0);
 }
 Offset _avatar(String uid){
  final players=(widget.room['players'] as List? ?? []).whereType<Map>();
  final player=players.where((p)=>p['uid']==uid).firstOrNull;
  final seat=(player?['seat'] as num?)?.toInt()??0;
  final visual=(seat+(widget.seat<0?0:(3-widget.seat+4)%4))%4;
  return Offset(widget.left+((visual==0||visual==3)?24:widget.side-24),
   (visual<2)?widget.top-20:widget.top+widget.side+20);
 }
 @override void dispose(){motion.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>IgnorePointer(child:AnimatedBuilder(animation:motion,builder:(_,__) {
  final event=gift;if(event==null)return const SizedBox.shrink();
  final t=Curves.easeInOutCubic.transform(motion.value);
  final from=_avatar('${event['from']}'),to=_avatar('${event['to']}');
  final center=Offset.lerp(from,to,t)!-Offset(0,math.sin(t*math.pi)*widget.side*.22);
  return Stack(clipBehavior:Clip.none,children:[Positioned(left:(center.dx-64).clamp(0.0,math.max(0.0,widget.side-128)),top:center.dy-40,width:128,
   child:Opacity(opacity:motion.value<.85?1:((1-motion.value)/.15).clamp(0.0,1.0),
    child:Column(mainAxisSize:MainAxisSize.min,children:[
     Transform.scale(scale:1+math.sin(t*math.pi)*.6,child:Text('${event['emoji']??'🎁'}',textAlign:TextAlign.center,style:const TextStyle(fontSize:46))),
     Container(padding:const EdgeInsets.symmetric(horizontal:6,vertical:4),decoration:BoxDecoration(color:const Color(0xEF20163D),borderRadius:BorderRadius.circular(10)),
      child:Text('${event['fromName']??'Oyuncu'} → ${event['toName']??'Oyuncu'}',maxLines:2,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w700))),
    ])))]);
 }));
}

// LiveKit participant notifications update each tile independently from the
// room's throttled layout refresh. Join highlight expires without another event.
class Ngelx583CallPresence extends StatefulWidget {
 final lk.Participant participant;final bool joined,microphone;final Widget child;
 const Ngelx583CallPresence({super.key,required this.participant,required this.joined,required this.microphone,required this.child});
 @override State<Ngelx583CallPresence> createState()=>_Ngelx583CallPresenceState();
}
class _Ngelx583CallPresenceState extends State<Ngelx583CallPresence> with SingleTickerProviderStateMixin{
 late final AnimationController pulse=AnimationController(vsync:this,duration:const Duration(milliseconds:550));
 Timer? expiry;bool joined=false;
 void _changed(){
  final speaking=widget.participant.isSpeaking&&widget.microphone;
  if(speaking||joined){if(!pulse.isAnimating)pulse.repeat(reverse:true);}
  else{pulse.stop();pulse.value=0;}
  if(mounted)setState((){});
 }
 void _join(){
  if(!widget.joined||joined)return;joined=true;expiry?.cancel();
  expiry=Timer(const Duration(seconds:3),(){if(mounted){joined=false;_changed();}});
 }
 @override void initState(){super.initState();widget.participant.addListener(_changed);_join();_changed();}
 @override void didUpdateWidget(covariant Ngelx583CallPresence old){
  super.didUpdateWidget(old);
  if(!identical(old.participant,widget.participant)){old.participant.removeListener(_changed);widget.participant.addListener(_changed);}
  if(!old.joined&&widget.joined)_join();_changed();
 }
 @override void dispose(){expiry?.cancel();widget.participant.removeListener(_changed);pulse.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>AnimatedBuilder(animation:pulse,child:widget.child,builder:(_,child){
  final speaking=widget.participant.isSpeaking&&widget.microphone;
  return Stack(fit:StackFit.expand,children:[child!,if(joined||speaking)Positioned.fill(child:IgnorePointer(child:DecoratedBox(
   decoration:BoxDecoration(borderRadius:BorderRadius.circular(24),border:Border.all(color:(joined?const Color(0xFFFFD768):const Color(0xFF23DC7A)).withValues(alpha:.65+.35*pulse.value),width:3.5))))),
   if(joined)Positioned(left:10,top:10,right:38,child:IgnorePointer(child:Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:5),decoration:BoxDecoration(color:const Color(0xFF554017),borderRadius:BorderRadius.circular(10)),child:const Text('Aramaya katıldı',style:TextStyle(color:Color(0xFFFFE9A3),fontSize:11,fontWeight:FontWeight.w800))))),
   if(speaking)Positioned(right:18,bottom:18,child:IgnorePointer(child:Row(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.center,children:[for(var i=0;i<4;i++)Container(width:3,height:5+(i.isEven?pulse.value:1-pulse.value)*14,margin:const EdgeInsets.symmetric(horizontal:1),color:const Color(0xFF5AFFA0))]))),
  ]);
 });
}
