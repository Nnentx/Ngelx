#!/usr/bin/env python3
"""Build 412 visitor header, stats and intro reference. Existing business logic untouched."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
start=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
end=s.index('\nclass NgelXVideoKapakOnizleme',start);v=s[start:end]
def one(old,new,label):
 global v
 n=v.count(old)
 if n!=1:raise SystemExit(f'{label}: expected 1 match, got {n}')
 v=v.replace(old,new,1)
one("final canliAday=v['isLive']==true",
"""           final katilimHam=v['createdAt']??v['joinedAt'];
           const aylar=['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
           final katilim=katilimHam is Timestamp
             ?'${aylar[katilimHam.toDate().month-1]} ${katilimHam.toDate().year}’te katıldı'
             :'';
           final canliAday=v['isLive']==true""","join date")
a=v.index("               if(!kapaksiz)...[")
b=v.index("               if(canli&&canliId.isNotEmpty)...[",a)
header=r"""               if(kapaksiz)...[
                 const SizedBox(height:8),
                 Center(child:SizedBox(height:182,width:230,child:Stack(
                   alignment:Alignment.center,clipBehavior:Clip.none,children:[
                     Positioned(left:10,top:49,child:Container(width:62,height:62,decoration:const BoxDecoration(color:Color(0xFFF0E4FF),shape:BoxShape.circle))),
                     Positioned(right:7,top:8,child:Container(width:83,height:83,decoration:const BoxDecoration(color:Color(0xFFF4EAFF),shape:BoxShape.circle))),
                     const Positioned(left:16,top:15,child:Icon(Icons.auto_awesome_rounded,size:17,color:Color(0xFF9850F2))),
                     const Positioned(right:0,bottom:34,child:Icon(Icons.auto_awesome_rounded,size:15,color:Color(0xFF9850F2))),
                     _ziyaretciReferansAvatar(foto,(v['username']??'ngelx').toString(),canli,erisimVar,67),
                   ],
                 ))),
                 const SizedBox(height:8),
                 _ziyaretciReferansAd(v),
                 Text('@'+(v['username']??'ngelx').toString(),textAlign:TextAlign.center,
                   style:const TextStyle(color:Colors.black54,fontSize:15)),
                 const SizedBox(height:12),
                 Text((v['bio']??'').toString(),textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontSize:15)),
                 const SizedBox(height:11),
                 Wrap(alignment:WrapAlignment.center,crossAxisAlignment:WrapCrossAlignment.center,spacing:9,runSpacing:7,children:[
                   if(katilimHam is Timestamp)...[
                     const Icon(Icons.calendar_month_outlined,color:Color(0xFF68647D),size:17),
                     Text('NgelX’e katıldı: '+katilimHam.toDate().year.toString(),
                       style:const TextStyle(color:Color(0xFF68647D),fontSize:12)),
                     const Text('•',style:TextStyle(color:Colors.black45)),
                   ],
                   AktiflikDurumuYazisi(uid:uid),
                 ]),
               ] else ...[
                 SizedBox(height:246,child:Stack(clipBehavior:Clip.none,children:[
                   Positioned(left:0,right:0,top:0,height:172,child:ClipRRect(
                     borderRadius:BorderRadius.circular(20),
                     child:Image(image:NgelXAgImageProvider(profilKapak),fit:BoxFit.cover,
                       alignment:Alignment(0,kapakKonum),gaplessPlayback:true),
                   )),
                   Positioned(left:8,top:111,child:_ziyaretciReferansAvatar(
                     foto,(v['username']??'ngelx').toString(),canli,erisimVar,57)),
                   Positioned(left:138,right:0,top:181,child:Column(
                     crossAxisAlignment:CrossAxisAlignment.start,children:[
                       _ziyaretciReferansAd(v,ortala:false),
                       Text('@'+(v['username']??'ngelx').toString(),
                         maxLines:1,overflow:TextOverflow.ellipsis,
                         style:const TextStyle(color:Colors.black54,fontSize:14)),
                     ],
                   )),
                 ])),
                 const SizedBox(height:7),
                 Text((v['bio']??'').toString(),textAlign:TextAlign.start,
                   style:const TextStyle(color:Colors.black87,fontSize:15)),
                 const SizedBox(height:9),
                 Wrap(alignment:WrapAlignment.start,crossAxisAlignment:WrapCrossAlignment.center,spacing:9,runSpacing:7,children:[
                   if((v['location']??'').toString().trim().isNotEmpty)...[
                     const Icon(Icons.location_on_outlined,color:Colors.black54,size:18),
                     Text((v['location']??'').toString(),style:const TextStyle(color:Colors.black54,fontSize:12)),
                   ],
                   if(katilim.isNotEmpty)...[
                     const Icon(Icons.calendar_month_outlined,color:Colors.black54,size:18),
                     Text(katilim,style:const TextStyle(color:Colors.black54,fontSize:12)),
                   ],
                 ]),
               ],
"""
v=v[:a]+header+v[b:]
one("return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[",
"""return Container(
                         padding:const EdgeInsets.symmetric(vertical:11,horizontal:4),
                         decoration:BoxDecoration(color:const Color(0xFFF7F2FF),
                           borderRadius:BorderRadius.circular(20),
                           border:Border.all(color:const Color(0xFFE9DDFB))),
                         child:Row(children:[""","stats container")
one("""                      ]);
                    },
                  );
                },
              ),
              const SizedBox(height: 22),""",
"""                      ]));
                    },
                  );
                },
              ),
              const SizedBox(height: 15),""","stats closing")
one("""  Widget _profilSayac(BuildContext context,String sayi,String baslik,VoidCallback tiklama)=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(12),child:Padding(padding:const EdgeInsets.symmetric(horizontal:6,vertical:8),child:Column(children:[Text(sayi,style:const TextStyle(fontSize:20,fontWeight:FontWeight.w900)),Text(baslik,style:const TextStyle(color:Colors.black54,fontSize:12))])));""",
"""  Widget _profilSayac(BuildContext context,String sayi,String baslik,VoidCallback tiklama)=>
    Expanded(child:InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(12),
      child:Padding(padding:const EdgeInsets.symmetric(vertical:6),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(baslik==t('following')?Icons.person_rounded:
            baslik==t('followers')?Icons.people_rounded:
            baslik==t('interaction')?Icons.bar_chart_rounded:Icons.groups_rounded,
            color:mor,size:23),
          const SizedBox(height:5),
          Text(sayi,style:const TextStyle(fontSize:20,fontWeight:FontWeight.w900,color:Colors.black87)),
          Text(baslik,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,
            style:const TextStyle(color:Colors.black54,fontSize:10.5)),
        ]),
      ),
    ));""","four purple stats")
one("""               if((v['introVideoUrl']??'').toString().isNotEmpty) ...[
                 const SizedBox(height:14),
                 ProfilTanitimVideoKarti(url:(v['introVideoUrl']??'').toString()),
               ],""",
"""               if((v['introVideoUrl']??'').toString().isNotEmpty) ...[
                 const SizedBox(height:15),
                 Container(
                   padding:const EdgeInsets.all(11),
                   decoration:BoxDecoration(color:Colors.white,
                     borderRadius:BorderRadius.circular(19),border:Border.all(color:const Color(0xFFE6E0F0))),
                   child:Row(children:[
                     Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                       const Row(children:[
                         Icon(Icons.video_library_rounded,color:mor,size:21),
                         SizedBox(width:5),
                         Expanded(child:Text('Tanıtım videosu',
                           style:TextStyle(color:Colors.black87,fontSize:13,fontWeight:FontWeight.w900))),
                       ]),
                       const SizedBox(height:10),
                       const Text('Kendini daha iyi ifade et, hikâyeni paylaş.',
                         style:TextStyle(color:Colors.black54,fontSize:11.5,height:1.4)),
                     ])),
                     const SizedBox(width:10),
                     SizedBox(width:145,height:116,child:ClipRRect(
                       borderRadius:BorderRadius.circular(15),
                       child:ProfilTanitimVideoKarti(url:(v['introVideoUrl']??'').toString()),
                     )),
                   ]),
                 ),
               ],""","intro media preserved")
helper=r"""
  Widget _ziyaretciReferansAvatar(String foto,String handle,bool canli,bool erisimVar,double radius)=>
    Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[
      Container(padding:const EdgeInsets.all(3),
        decoration:BoxDecoration(shape:BoxShape.circle,
          border:Border.all(color:canli?const Color(0xFFFF1744):const Color(0xFF9450F4),width:3)),
        child:NgelXHikayeliAvatar(uid:uid,fotoUrl:foto,kullanici:'@$handle',radius:radius,etkin:erisimVar),
      ),
      if(canli)Positioned(bottom:-7,child:Container(
        padding:const EdgeInsets.symmetric(horizontal:10,vertical:3),
        decoration:BoxDecoration(color:const Color(0xFFFF1744),borderRadius:BorderRadius.circular(9),
          border:Border.all(color:Colors.white,width:1.5)),
        child:const Text('CANLI',style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900)),
      )),
    ]);
  Widget _ziyaretciReferansAd(Map<String,dynamic> veri,{bool ortala=true})=>Row(
    mainAxisAlignment:ortala?MainAxisAlignment.center:MainAxisAlignment.start,
    mainAxisSize:MainAxisSize.min,children:[
      Flexible(child:Text((veri['displayName']??veri['username']??'NgelX').toString(),
        maxLines:1,overflow:TextOverflow.ellipsis,
        style:TextStyle(color:Colors.black87,fontSize:ortala?26:22,fontWeight:FontWeight.w900))),
      if(veri['verified']==true)...[
        const SizedBox(width:5),const Icon(Icons.verified_rounded,size:19,color:Color(0xFF1687FF)),
      ],
      if(veri['premiumActive']==true||veri['isPremium']==true||
        (veri['plan']??'').toString().toLowerCase()=='premium')...[
        const SizedBox(width:5),const Icon(Icons.workspace_premium_rounded,size:18,color:mor),
      ],
    ],
  );

"""
i=v.index("  Widget _profilSayac(BuildContext context")
v=v[:i]+helper+v[i:]
s=s[:start]+v+s[end:];p.write_text(s,encoding='utf-8')
print('Build 412 approved visitor header, 4 purple stats, intro media card applied.')
