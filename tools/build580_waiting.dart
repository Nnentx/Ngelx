class Ngelx567WaitingPanel extends StatelessWidget {
 final Map<String,dynamic> room;final String uid;final bool canStart,busy,compact;final VoidCallback onInvite,onStart;
 const Ngelx567WaitingPanel({super.key,required this.room,required this.uid,required this.canStart,required this.busy,required this.onInvite,required this.onStart,this.compact=false});
 @override Widget build(BuildContext context){
  final players=List<dynamic>.from(room['players']??[]).where((p)=>p['left']!=true).toList();
  final capacity=(room['capacity'] as num? ?? 2).toInt(),requiredPlayers=room['team']==true?4:2;
  final id='${room['id']??''}',owner=room['owner']==uid,random=room['matchmaking']==true;
  return Container(key:const ValueKey('ludo-waiting-panel'),decoration:BoxDecoration(
   borderRadius:BorderRadius.circular(20),gradient:const LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFFB8B4FF),Color(0xFF7C74D5)]),
   border:Border.all(color:const Color(0xFFD2CFFF),width:2),boxShadow:const [BoxShadow(color:Color(0x990C082E),blurRadius:28,offset:Offset(0,10))]),
   child:Column(mainAxisSize:MainAxisSize.min,children:[
    Padding(padding:EdgeInsets.symmetric(vertical:compact?9:13,horizontal:8),child:Text(random?'Rakip aranıyor…':'Arkadaşlarla · ${room['mode']=='power'?'Power':'Klasik'}',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:compact?17:20))),
    Container(margin:const EdgeInsets.fromLTRB(9,0,9,10),padding:EdgeInsets.all(compact?10:14),decoration:BoxDecoration(color:const Color(0xFFF0EFFF),borderRadius:BorderRadius.circular(15)),
     child:Column(mainAxisSize:MainAxisSize.min,children:[
      Row(crossAxisAlignment:CrossAxisAlignment.start,children:[for(var i=0;i<capacity;i++)Expanded(child:Padding(padding:const EdgeInsets.symmetric(horizontal:2),child:
       i<players.length?Column(mainAxisSize:MainAxisSize.min,children:[
        CircleAvatar(radius:compact?23:28,backgroundColor:ngelx565LudoColors[(players[i]['seat'] as num).toInt()],
         backgroundImage:(players[i]['photo']??'').toString().isEmpty?null:ResizeImage(NgelXAgImageProvider(players[i]['photo'].toString()),width:192),
         child:(players[i]['photo']??'').toString().isEmpty?const Icon(Icons.person_rounded,color:Colors.white):null),
        const SizedBox(height:6),Text(players[i]['uid']==uid?'Sen':'${players[i]['name']}',textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:_ludoInk567,fontSize:14,fontWeight:FontWeight.w800)),
        Text('Lv.${players[i]['level']??1}',style:const TextStyle(color:Color(0xFF74658F),fontSize:11,fontWeight:FontWeight.w600)),
       ]):InkWell(onTap:random?null:onInvite,borderRadius:BorderRadius.circular(12),child:Column(mainAxisSize:MainAxisSize.min,children:[
        Container(width:compact?46:56,height:compact?46:56,decoration:BoxDecoration(shape:BoxShape.circle,gradient:const LinearGradient(colors:[Color(0xFF91DEFF),Color(0xFF5285DF)]),border:Border.all(color:Colors.white,width:2)),child:Icon(random?Icons.search_rounded:Icons.person_add_alt_1_rounded,color:Colors.white,size:25)),
        const SizedBox(height:6),Text(random?'Aranıyor…':'Davet et',textAlign:TextAlign.center,maxLines:2,style:const TextStyle(color:Color(0xFF7065AD),fontSize:13,fontWeight:FontWeight.w800)),
       ]))))]),
      SizedBox(height:compact?10:16),
      Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:9),decoration:BoxDecoration(color:const Color(0xFFE0DEFA),borderRadius:BorderRadius.circular(24)),child:Row(children:[
       const Icon(Icons.meeting_room_rounded,color:Color(0xFF8270C6),size:20),const SizedBox(width:6),
       Expanded(child:Text(id,key:const ValueKey('ludo-waiting-code'),textAlign:TextAlign.center,maxLines:1,style:TextStyle(color:const Color(0xFF4C4077),fontWeight:FontWeight.w800,fontSize:id.length>6?14:21,letterSpacing:id.length>6?1:3))),
       IconButton(tooltip:'Oda kodunu kopyala',onPressed:()=>Clipboard.setData(ClipboardData(text:id)),icon:const Icon(Icons.copy_rounded,size:21,color:Color(0xFF8270C6)),constraints:const BoxConstraints(minWidth:36,minHeight:36),padding:const EdgeInsets.all(5)),
      ])),
      Padding(padding:EdgeInsets.symmetric(vertical:compact?8:13),child:Text(players.length<requiredPlayers?'${requiredPlayers-players.length} oyuncu daha bekleniyor':owner?'Masa hazır. Oyunu başlatabilirsin.':'Kurucunun başlatması bekleniyor',textAlign:TextAlign.center,style:TextStyle(color:const Color(0xFF74658F),fontSize:compact?12:13,fontWeight:FontWeight.w700))),
      if(!random)Row(children:[Expanded(child:Ngelx567GameButton(label:'Davet et',icon:Icons.person_add_alt_1_rounded,onPressed:busy?null:onInvite)),const SizedBox(width:10),Expanded(child:Ngelx567GameButton(key:const ValueKey('ludo-start'),label:'Başlat',gold:true,onPressed:canStart?onStart:null))]),
     ])),
   ]));
 }
}
