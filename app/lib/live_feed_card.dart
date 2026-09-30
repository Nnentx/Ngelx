part of 'main.dart';

double ngelxCanliTrendPuani(Map<String,dynamic> veri){
  final izleyici=(veri['viewerCount'] as num?)?.toDouble()??0;
  final begeni=(veri['likeCount'] as num?)?.toDouble()??0;
  final paylasim=(veri['shareCount'] as num?)?.toDouble()??0;
  final hediye=(veri['giftPoints'] as num?)?.toDouble()??0;
  final baslangic=veri['startedAt'];
  var tazelik=0.0;
  if(baslangic is Timestamp){
    final dakika=DateTime.now().difference(baslangic.toDate()).inMinutes.clamp(0,180);
    tazelik=(180-dakika)/18;
  }
  return izleyici*5+begenIyiGuvenli(begeni)*2+paylasim*4+hediye*.02+tazelik;
}

double begenIyiGuvenli(double value)=>value.isFinite?value:0;

class NgelXCanliTakipButonu extends StatefulWidget{
  final String ownerId;
  final bool compact;
  const NgelXCanliTakipButonu({super.key,required this.ownerId,this.compact=false});
  @override State<NgelXCanliTakipButonu> createState()=>_NgelXCanliTakipButonuState();
}

class _NgelXCanliTakipButonuState extends State<NgelXCanliTakipButonu>{
  bool islem=false;
  @override Widget build(BuildContext context){
    final ben=FirebaseAuth.instance.currentUser?.uid??'';
    if(ben.isEmpty||ben==widget.ownerId||widget.ownerId.isEmpty)return const SizedBox.shrink();
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(ben).snapshots(),
      builder:(_,snap){
        final takip=List<String>.from(snap.data?.data()?['following']??const[]).contains(widget.ownerId);
        return FilledButton(
          style:FilledButton.styleFrom(
            backgroundColor:takip?Colors.black54:const Color(0xFFFF1744),
            foregroundColor:Colors.white,
            padding:EdgeInsets.symmetric(horizontal:widget.compact?10:15,vertical:widget.compact?7:10),
            minimumSize:Size.zero,
            tapTargetSize:MaterialTapTargetSize.shrinkWrap,
            shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
          ),
          onPressed:islem?null:()async{
            setState(()=>islem=true);
            try{await takipDurumuDegistir(widget.ownerId,takip);}
            finally{if(mounted)setState(()=>islem=false);}
          },
          child:islem
            ?SizedBox(width:widget.compact?12:15,height:widget.compact?12:15,child:const CircularProgressIndicator(strokeWidth:2,color:Colors.white))
            :Text(takip?'Takip Ediliyor':'Takip et',style:TextStyle(fontSize:widget.compact?10:12,fontWeight:FontWeight.w900)),
        );
      },
    );
  }
}

class NgelXAkisCanliKarti extends StatelessWidget{
  final String liveId;
  final Map<String,dynamic> ilkVeri;
  final bool aktif;
  const NgelXAkisCanliKarti({super.key,required this.liveId,required this.ilkVeri,required this.aktif});

  @override Widget build(BuildContext context){
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(liveId).snapshots(),
      builder:(_,liveSnap){
        final veri=liveSnap.data?.data()??ilkVeri;
        final owner=(veri['ownerId']??'').toString();
        final canli=ngelxCanliKaydiTaze(veri);
        return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:owner.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(owner).snapshots(),
          builder:(_,profilSnap){
            final profil=profilSnap.data?.data()??<String,dynamic>{};
            final foto=(veri['coverUrl']??profil['photoUrl']??'').toString();
            final ad=(profil['displayName']??profil['username']??veri['username']??'NgelX').toString();
            final username=(profil['username']??veri['username']??'ngelx').toString().replaceFirst('@','');
            final baslik=(veri['title']??'Canlı yayın').toString();
            final izleyici=(veri['viewerCount'] as num?)?.toInt()??0;
            return GestureDetector(
              behavior:HitTestBehavior.opaque,
              onTap:canli?()=>ngelxCanliYayinaKatil(context,liveId):(){
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu canlı yayın sona erdi.')));
              },
              child:Stack(fit:StackFit.expand,children:[
                const ColoredBox(color:Color(0xFF111116)),
                if(foto.isNotEmpty)NgelXAgResmi(url:foto,fit:BoxFit.cover),
                const DecoratedBox(decoration:BoxDecoration(gradient:LinearGradient(
                  begin:Alignment.topCenter,end:Alignment.bottomCenter,
                  colors:[Color(0x33000000),Color(0x22000000),Color(0xE8000000)],
                  stops:[0,.48,1],
                ))),
                if(!canli)Center(child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:18,vertical:12),
                  decoration:BoxDecoration(color:Colors.black87,borderRadius:BorderRadius.circular(18)),
                  child:const Text('Canlı yayın sona erdi',style:TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900)),
                )),
                Positioned(
                  left:22,right:18,bottom:34,
                  child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                    Row(children:[
                      Container(
                        padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
                        decoration:BoxDecoration(color:canli?const Color(0xFFFF1744):Colors.black54,borderRadius:BorderRadius.circular(10)),
                        child:Text(canli?'● CANLI':'SONA ERDİ',style:const TextStyle(color:Colors.white,fontSize:12,fontWeight:FontWeight.w900)),
                      ),
                      const SizedBox(width:8),
                      Container(
                        padding:const EdgeInsets.symmetric(horizontal:9,vertical:6),
                        decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),
                        child:Row(mainAxisSize:MainAxisSize.min,children:[
                          const Icon(Icons.visibility_rounded,color:Colors.white,size:16),
                          const SizedBox(width:4),
                          Text('$izleyici',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
                        ]),
                      ),
                    ]),
                    const SizedBox(height:12),
                    Text(baslik,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:24,fontWeight:FontWeight.w900,height:1.08)),
                    const SizedBox(height:10),
                    Row(children:[
                      CircleAvatar(radius:19,backgroundImage:(profil['photoUrl']??'').toString().isEmpty?null:NgelXAgImageProvider((profil['photoUrl']).toString()),child:(profil['photoUrl']??'').toString().isEmpty?const Icon(Icons.person_rounded):null),
                      const SizedBox(width:9),
                      Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                        Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900)),
                        Text('@$username',style:const TextStyle(color:Colors.white70,fontSize:12,fontWeight:FontWeight.w600)),
                      ])),
                      if(canli)NgelXCanliTakipButonu(ownerId:owner),
                    ]),
                    if(canli)...[
                      const SizedBox(height:12),
                      const Row(children:[
                        Icon(Icons.touch_app_rounded,color:Colors.white70,size:18),
                        SizedBox(width:6),
                        Text('Yayına dokun ve katıl',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
                      ]),
                    ],
                  ]),
                ),
              ]),
            );
          },
        );
      },
    );
  }
}
