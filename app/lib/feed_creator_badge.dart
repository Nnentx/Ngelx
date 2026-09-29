part of 'main.dart';

class NgelXIcerikUreticisiRozeti extends StatelessWidget {
  final bool kucuk;
  const NgelXIcerikUreticisiRozeti({super.key,this.kucuk=false});

  @override
  Widget build(BuildContext context){
    final h=kucuk?20.0:22.0;
    return Container(
      height:h,
      padding:EdgeInsets.symmetric(horizontal:kucuk?7:8,vertical:2),
      decoration:BoxDecoration(
        gradient:const LinearGradient(colors:[Color(0xFF00C2FF),Color(0xFF8B5CF6)]),
        borderRadius:BorderRadius.circular(999),
        boxShadow:const [BoxShadow(color:Color(0x3300B8F5),blurRadius:8,offset:Offset(0,2))],
      ),
      child:Row(mainAxisSize:MainAxisSize.min,children:[
        Icon(Icons.auto_awesome_rounded,color:Colors.white,size:kucuk?11:12),
        const SizedBox(width:4),
        Text(
          lt('İçerik Üreticisi','Content Creator'),
          maxLines:1,
          overflow:TextOverflow.ellipsis,
          style:TextStyle(color:Colors.white,fontSize:kucuk?9.5:10.5,fontWeight:FontWeight.w900,letterSpacing:.1),
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
    this.creatorBadge=true,
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
              spacing:7,
              runSpacing:5,
              children:[
                Text(
                  '@${username.replaceFirst('@','')}',
                  maxLines:1,
                  overflow:TextOverflow.ellipsis,
                  style:const TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900),
                ),
                if(creatorBadge)const NgelXIcerikUreticisiRozeti(),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
