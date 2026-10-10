String ngelx434Aktiflik(Map<String,dynamic> v,{DateTime? now}){
  if(v['showActivityStatus']==false)return '';
  final stamp=v['lastSeenAt'];
  if(stamp is! Timestamp)return '';
  final age=(now??DateTime.now()).difference(stamp.toDate());
  if(age.isNegative&&age.inSeconds < -30)return '';
  if((v['isOnline']==true||v['online']==true)&&age.inSeconds<=120)return 'Çevrimiçi';
  if(age.inMinutes<1)return 'Az önce aktif';
  if(age.inHours<1)return '${age.inMinutes} dk önce aktif';
  if(age.inDays<1)return '${age.inHours} sa önce aktif';
  return '${age.inDays} gün önce aktif';
}
class Ngelx434AktifAvatar extends StatefulWidget{
  final String uid,photo;
  final double radius;
  final Map<String,dynamic>? initial;
  const Ngelx434AktifAvatar({super.key,required this.uid,required this.photo,this.radius=27,this.initial});
  @override State<Ngelx434AktifAvatar> createState()=>_Ngelx434AktifAvatarState();
}
class _Ngelx434AktifAvatarState extends State<Ngelx434AktifAvatar>{
  Timer? _timer;
  late Stream<DocumentSnapshot<Map<String,dynamic>>> _stream;
  void _connect(){_stream=FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots();}
  @override void initState(){super.initState();_connect();_timer=Timer.periodic(const Duration(seconds:30),(_){if(mounted)setState((){});});}
  @override void didUpdateWidget(covariant Ngelx434AktifAvatar old){super.didUpdateWidget(old);if(old.uid!=widget.uid)_connect();}
  @override void dispose(){_timer?.cancel();super.dispose();}
  @override Widget build(BuildContext context)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_stream,builder:(_,snap){
    final v=snap.data?.data()??widget.initial??<String,dynamic>{};
    final label=ngelx434Aktiflik(v),online=label=='Çevrimiçi';
    final photo=(v['photoUrl']??widget.photo).toString();
    return SizedBox(width:widget.radius*2,height:widget.radius*2+8,child:Stack(clipBehavior:Clip.none,children:[
      CircleAvatar(radius:widget.radius,backgroundColor:const Color(0xFFEFF3F8),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?const Icon(Icons.person_rounded,color:Color(0xFF61708D)):null),
      if(label.isNotEmpty)Positioned(right:-3,bottom:0,child:Semantics(label:label,child:Tooltip(message:label,child:Container(
        padding:online?const EdgeInsets.all(2):const EdgeInsets.symmetric(horizontal:4,vertical:2),
        decoration:BoxDecoration(color:online?Colors.white:const Color(0xFFEAF7ED),borderRadius:BorderRadius.circular(12)),
        child:online?const Icon(Icons.circle,color:Color(0xFF31A24C),size:14):Text(label=='Az önce aktif'?'Şimdi':label.split(' önce').first,style:const TextStyle(color:Color(0xFF287A3B),fontSize:10,fontWeight:FontWeight.w700)),
      )))),
    ]));
  });
}
String? ngelx434IstekSonucu(Map<String,dynamic> v){
  final kind=v['type'];if(kind!='friend_request'&&kind!='follow_request')return null;
  final state=v['status'];
  final result=switch(state){'accepted'=>'kabul edildi','rejected'=>'reddedildi','cancelled'=>'geri çekildi','superseded'=>'güncellendi',_=>null};
  if(result==null)return null;
  final name=(v['senderName']??v['fromName']??'Kullanıcı').toString();
  return '$name adlı kişinin ${kind=='friend_request'?'arkadaşlık':'takip'} isteği $result.';
}
