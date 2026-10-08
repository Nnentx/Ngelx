#!/usr/bin/env python3
"""Build 412: visitor follow, message, friendship, mutual groups on one row.
Only visual wrappers/styles are changed. Existing async callbacks are preserved.
"""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a);v=s[a:b]
def one(old,new,label):
 global v
 n=v.count(old)
 if n==1:
  v=v.replace(old,new,1)
  return
 import re
 pattern=r'[ \\t]*'+r'\\n[ \\t]*'.join(re.escape(line.lstrip()) for line in old.split('\\n'))
 hits=list(re.finditer(pattern,v))
 if len(hits)!=1:raise SystemExit(f'Build 412 {label}: expected 1 anchor, got {n} exact and {len(hits)} flexible')
 hit=hits[0]
 v=v[:hit.start()]+new+v[hit.end():]

marker="'Takip, içerikleri Akışında gösterir."
if v.count(marker)!=1:raise SystemExit("Explanation callout marker changed")
notice_idx=v.index(marker)
notice_start=v.rfind('Container(',0,notice_idx)
notice_end=v.index('Row(children:[',notice_idx)
if notice_start<0 or notice_end<notice_start:raise SystemExit("Explanation card limits changed")
v=v[:notice_start]+v[notice_end:]

one("""                 Row(children:[
                   Expanded(child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"""                 SizedBox(height:51,child:Row(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                   Expanded(flex:3,child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""","actions row start")
one("""                   const SizedBox(width:10),
                   Expanded(child:OutlinedButton.icon(""",
"""                   const SizedBox(width:5),
                   Expanded(flex:2,child:OutlinedButton.icon(""","message flex")
one("""                 ]),
                 const SizedBox(height:10),
                 StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"""                   const SizedBox(width:5),
                   Expanded(flex:3,child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""","friend inline")
one("""                 ),
                 const SizedBox(height:10),
                 SizedBox(width:double.infinity,child:OutlinedButton.icon(
                   onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>OrtakGruplarPage(digerUid:uid))),
                   icon:const Icon(Icons.groups_2_outlined),
                   label:const Text('Ortak gruplar'),
                 )),
""",
"""                 )),
                   const SizedBox(width:5),
                   Expanded(flex:3,child:OutlinedButton.icon(
                     style:OutlinedButton.styleFrom(foregroundColor:mor,side:const BorderSide(color:mor),
                       padding:const EdgeInsets.symmetric(horizontal:2),minimumSize:const Size(0,46)),
                     onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>OrtakGruplarPage(digerUid:uid))),
                     icon:const Icon(Icons.groups_2_outlined,size:16),
                     label:const FittedBox(fit:BoxFit.scaleDown,child:Text('Ortak gruplar',maxLines:1,
                       style:TextStyle(fontSize:11,fontWeight:FontWeight.w800))),
                   )),
                 ])),
""","group fourth inline action")
one("""                           return OutlinedButton.icon(
                             onPressed:()async{""",
"""                           return OutlinedButton.icon(
                             style:OutlinedButton.styleFrom(backgroundColor:const Color(0xFFF6F2FC),
                               foregroundColor:Colors.black87,side:BorderSide.none,
                               padding:const EdgeInsets.symmetric(horizontal:2),minimumSize:const Size(0,46)),
                             onPressed:()async{""","follow button style")
one("""                             icon:Icon(takipte?Icons.person_remove_outlined:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1)),
                             label:FittedBox(fit:BoxFit.scaleDown,child:Text(etiket,maxLines:1)),""",
"""                             icon:Icon(takipte?Icons.person_remove_outlined:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1),size:15),
                             label:FittedBox(fit:BoxFit.scaleDown,child:Text(etiket,maxLines:1,
                               style:const TextStyle(fontSize:10,fontWeight:FontWeight.w800))),""","follow label fit")
one("""                   Expanded(flex:2,child:OutlinedButton.icon(
                     onPressed:me==null?null:()=>profildenMesajAc(""",
"""                   Expanded(flex:2,child:OutlinedButton.icon(
                     style:OutlinedButton.styleFrom(foregroundColor:mor,side:const BorderSide(color:mor),
                       padding:const EdgeInsets.symmetric(horizontal:0),minimumSize:const Size(0,46)),
                     onPressed:me==null?null:()=>profildenMesajAc(""","message outline")
one("""                     icon:const Icon(Icons.message_outlined),
                     label:Text(t('message')),""",
"""                     icon:const Icon(Icons.message_outlined,size:15),
                     label:FittedBox(fit:BoxFit.scaleDown,
                       child:Text(t('message'),style:const TextStyle(fontSize:10.5,fontWeight:FontWeight.w800))),""","message label")
one("""                         return SizedBox(width:double.infinity,child:FilledButton.icon(
                           onPressed:me==null?null:()async{""",
"""                         return SizedBox(width:double.infinity,child:FilledButton.icon(
                           style:FilledButton.styleFrom(backgroundColor:mor,foregroundColor:Colors.white,
                             padding:const EdgeInsets.symmetric(horizontal:2),minimumSize:const Size(0,46)),
                           onPressed:me==null?null:()async{""","friend button style")
one("""                           icon:Icon(arkadas?Icons.people_alt_rounded:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1_rounded)),
                           label:Text(
                             arkadas?'Arkadaşsınız':(bekliyor?'Arkadaşlık isteği bekliyor':'Arkadaş ekle'),
                             maxLines:1,
                             overflow:TextOverflow.ellipsis,
                           ),""",
"""                           icon:Icon(arkadas?Icons.people_alt_rounded:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1_rounded),size:15),
                           label:FittedBox(fit:BoxFit.scaleDown,child:Text(
                             arkadas?'Arkadaşsınız':(bekliyor?'Arkadaşlık isteği bekliyor':'Arkadaş ekle'),
                             maxLines:1,style:const TextStyle(fontSize:10,fontWeight:FontWeight.w800),
                           )),""","friend label fit")

s=s[:a]+v+s[b:];p.write_text(s,encoding='utf-8')
print('Build 412 actions: all four visible inline with original follow/message/friend/group logic.')
