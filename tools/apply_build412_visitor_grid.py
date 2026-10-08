#!/usr/bin/env python3
"""Build 412: approved 3-column post grid with like/comment counters."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a);v=s[a:b]
def one(old,new,label):
 global v
 n=v.count(old)
 if n==0 and v.count(old.strip())==1:
  old=old.strip()
  n=1
 if n!=1:raise SystemExit(f'Build 412 {label}: expected one anchor, got {n}')
 v=v.replace(old,new,1)
one("childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6",
    "childAspectRatio: .98, crossAxisSpacing: 6, mainAxisSpacing: 6","square media tiles")
one("""                         return GestureDetector(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:docs[i].id))),child:MedyaOnizleme(tur: tur, url: url, thumbnailUrl: (x['thumbnailUrl'] ?? '').toString(), yazi: (x['description'] ?? '').toString(), arkaPlan: const Color(0xFFF0F1F4)));""",
"""                         return GestureDetector(
                           onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:docs[i].id))),
                           child:ClipRRect(borderRadius:BorderRadius.circular(13),
                             child:Stack(fit:StackFit.expand,children:[
                               MedyaOnizleme(tur:tur,url:url,thumbnailUrl:(x['thumbnailUrl']??'').toString(),
                                 yazi:(x['description']??'').toString(),arkaPlan:const Color(0xFFF0F1F4)),
                               Positioned(left:5,right:5,bottom:5,child:Container(
                                 padding:const EdgeInsets.symmetric(horizontal:3,vertical:5),
                                 decoration:BoxDecoration(color:Colors.black.withValues(alpha:.67),
                                   borderRadius:BorderRadius.circular(13)),
                                 child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                                   Row(mainAxisSize:MainAxisSize.min,children:[
                                     const Icon(Icons.favorite_rounded,color:Colors.white,size:13),
                                     const SizedBox(width:3),
                                     Text(((x['likeCount'] as num?)?.toInt()??0).toString(),
                                       style:const TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w800)),
                                   ]),
                                   Row(mainAxisSize:MainAxisSize.min,children:[
                                     const Icon(Icons.mode_comment_rounded,color:Colors.white,size:13),
                                     const SizedBox(width:3),
                                     Text(((x['commentCount'] as num?)?.toInt()??0).toString(),
                                       style:const TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w800)),
                                   ]),
                                 ]),
                               )),
                             ]),
                           ),
                         );""","post grid overlays without changing tap action")
s=s[:a]+v+s[b:];p.write_text(s,encoding='utf-8')
print('Build 412 visitor grid: square rounded thumbnails, dynamic likes/comments and original post open action.')
