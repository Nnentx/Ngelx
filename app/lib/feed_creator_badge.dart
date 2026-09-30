part of 'main.dart';

class NgelXIcerikUreticisiRozeti extends StatelessWidget {
  final bool kucuk;
  const NgelXIcerikUreticisiRozeti({super.key,this.kucuk=false});

  @override
  Widget build(BuildContext context){
    final h=kucuk?17.0:19.0;
    return Container(
      height:h,
      padding:EdgeInsets.symmetric(horizontal:kucuk?6:7,vertical:1),
      decoration:BoxDecoration(
        gradient:const LinearGradient(colors:[Color(0xFF00C2FF),Color(0xFF8B5CF6)]),
        borderRadius:BorderRadius.circular(999),
        boxShadow:const [BoxShadow(color:Color(0x3300B8F5),blurRadius:8,offset:Offset(0,2))],
      ),
      child:Row(mainAxisSize:MainAxisSize.min,children:[
        Icon(Icons.auto_awesome_rounded,color:Colors.white,size:kucuk?9:10),
        const SizedBox(width:4),
        Text(
          lt('İçerik Üreticisi','Content Creator'),
          maxLines:1,
          overflow:TextOverflow.ellipsis,
          style:TextStyle(color:Colors.white,fontSize:kucuk?8.3:9.2,fontWeight:FontWeight.w900,letterSpacing:.1),
        ),
      ]),
    );
  }
}

class NgelXPaylasanSatiri extends StatelessWidget {
  final String username;
  final VoidCallback? onTap;
  final bool creatorBadge;
  final String sharedByUsername;
  const NgelXPaylasanSatiri({
    super.key,
    required this.username,
    this.onTap,
    this.creatorBadge=false,
    this.sharedByUsername='',
  });

  @override
  Widget build(BuildContext context){
    return Column(
      crossAxisAlignment:CrossAxisAlignment.start,
      mainAxisSize:MainAxisSize.min,
      children:[
        if(sharedByUsername.trim().isNotEmpty)...[
          Row(mainAxisSize:MainAxisSize.min,children:[
            const Icon(Icons.repeat_rounded,color:Colors.white70,size:13),
            const SizedBox(width:4),
            Flexible(child:Text(
              '@${sharedByUsername.replaceFirst('@','')} ${lt('paylaştı','shared')}',
              maxLines:1,
              overflow:TextOverflow.ellipsis,
              style:const TextStyle(color:Colors.white70,fontSize:10.5,fontWeight:FontWeight.w700),
            )),
          ]),
          const SizedBox(height:4),
        ],
        InkWell(
          onTap:onTap,
          borderRadius:BorderRadius.circular(10),
          child:Padding(
            padding:const EdgeInsets.symmetric(vertical:2),
            child:Wrap(
              crossAxisAlignment:WrapCrossAlignment.center,
              spacing:5,
              runSpacing:5,
              children:[
                Text(
                  '@${username.replaceFirst('@','')}',
                  maxLines:1,
                  overflow:TextOverflow.ellipsis,
                  style:const TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900),
                ),
                if(creatorBadge)const NgelXIcerikUreticisiRozeti(kucuk:true),
              ],
            ),
          ),
        ),
      ],
    );
  }
}


class NgelXYorumKullaniciSatiri extends StatelessWidget{
  final String ad;final bool icerikUreticisi;final VoidCallback? onTap;
  const NgelXYorumKullaniciSatiri({super.key,required this.ad,required this.icerikUreticisi,this.onTap});
  @override Widget build(BuildContext context)=>InkWell(
    onTap:onTap,
    child:Wrap(crossAxisAlignment:WrapCrossAlignment.center,spacing:5,runSpacing:3,children:[
      Text('@$ad',style:const TextStyle(fontWeight:FontWeight.w800,color:Colors.black87,fontSize:13.5)),
      if(icerikUreticisi)const NgelXIcerikUreticisiRozeti(kucuk:true),
    ]),
  );
}

final Set<String> ngelxSilinenIcerikIdleri=<String>{};
final ValueNotifier<int> ngelxIcerikSilmeRevizyonu=ValueNotifier<int>(0);
void ngelxIcerikSilindi(String id){
  if(id.isEmpty)return;
  ngelxSilinenIcerikIdleri.add(id);
  ngelxIcerikSilmeRevizyonu.value++;
}


Widget ngelxAramaEfekti(Widget w,int efekt,{required bool rotus,required bool bulanik}){
  const m=<List<double>>[
    <double>[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
    <double>[1.03,0,0,0,5,0,1.03,0,0,5,0,0,1.02,0,4,0,0,0,1,0],
    <double>[1.02,0,0,0,8,0,1.01,0,0,7,0,0,1.00,0,6,0,0,0,1,0],
    <double>[1.05,0,0,0,9,0,1.03,0,0,7,0,0,1.01,0,5,0,0,0,1,0],
    <double>[1.08,0,0,0,5,0,1.03,0,0,2,0,0,.95,0,-1,0,0,0,1,0],
    <double>[.96,0,0,0,-1,0,1.02,0,0,1,0,0,1.09,0,4,0,0,0,1,0],
    <double>[1.07,0,0,0,2,0,1.06,0,0,2,0,0,1.07,0,2,0,0,0,1,0],
    <double>[.33,.59,.11,0,0,.33,.59,.11,0,0,.33,.59,.11,0,0,0,0,0,1,0],
  ];
  final i=efekt.clamp(0,m.length-1);
  if(i>0)w=ColorFiltered(colorFilter:ColorFilter.matrix(m[i]),child:w);
  if(rotus)w=ColorFiltered(colorFilter:const ColorFilter.matrix(<double>[
    1.025,0,0,0,6,0,1.02,0,0,6,0,0,.995,0,5,0,0,0,1,0,
  ]),child:w);
  if(bulanik)w=ImageFiltered(imageFilter:ui.ImageFilter.blur(sigmaX:4,sigmaY:4),child:w);
  return w;
}

const List<String> ngelxAramaEfektAdlari=<String>['Doğal','Clean','Soft','Glow','Sıcak','Soğuk','HD','S/B'];
