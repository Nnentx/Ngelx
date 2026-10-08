#!/usr/bin/env python3
"""Build 402: finish owner-profile reference layout without changing data and actions.

Runs after Build 401's visual patch, with strict anchor checks.
"""
from pathlib import Path
import re

mainfile=Path('app/lib/main.dart')
pubfile=Path('app/pubspec.yaml')
src=mainfile.read_text(encoding='utf-8')
pub=pubfile.read_text(encoding='utf-8')

def replace_one(txt,old,new,label):
    n=txt.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 anchor, found {n}: {old[:130]!r}')
    return txt.replace(old,new,1)

src=replace_one(src,"defaultValue: '401'","defaultValue: '402'","build code")
src=replace_one(src,"defaultValue: '1.0.177'","defaultValue: '1.0.178'","build name")
pub=replace_one(pub,'version: 1.0.177+401','version: 1.0.178+402','pubspec')

ps=src.index('class _ProfilPageState extends State<ProfilPage>')
pe=src.index('\nclass _ProfilEtkilesimRozeti',ps)
p=src[ps:pe]

# 1. Reference owner header: keep same avatar, change controls and name placement.
# Move name/@username into the cover's existing Stack, to the right of the avatar.
name_start=p.index('                  Row(\n                    mainAxisAlignment:MainAxisAlignment.center,\n                    mainAxisSize:MainAxisSize.min,\n                    children:[',p.index('SizedBox(\n                    height:265,'))
name_end=p.index('                  const SizedBox(height: 10),\n                  Text(bio',name_start)
name_group=p[name_start:name_end]
if "if(premiumAktif)..." not in name_group or "Text(\n                    kullanici," not in name_group:
    raise SystemExit('owner name & premium badge anchor changed')
p=p[:name_start]+p[name_end:]
name_group=name_group.replace('mainAxisAlignment:MainAxisAlignment.center,','mainAxisAlignment:MainAxisAlignment.start,',1)
name_group=name_group.replace('                  const SizedBox(height: 10),\n','')
name_group=name_group.replace('                  Row(','                          Row(',1)
name_group=name_group.replace('                    children:[','                            children:[',1)
name_group=name_group.replace('                  Text(\n                    kullanici,','                          Text(\n                    kullanici,',1)

cover_end='''                      )),
                    ]),
                  ),
                  const SizedBox(height: 4),'''
if p.count(cover_end)!=1:
    raise SystemExit(f'owner header Stack end: expected 1, found {p.count(cover_end)}')
new_cover_end="""                      )),
                      Positioned(
                        left:145,right:4,top:206,
                        child:Column(
                          crossAxisAlignment:CrossAxisAlignment.start,
                          mainAxisSize:MainAxisSize.min,
                          children:[
"""+name_group+"""                          ],
                        ),
                      ),
                    ]),
                  ),
                  const SizedBox(height: 9),"""
p=replace_one(p,cover_end,new_cover_end,'move owner title beside avatar')

# Reference profile bio and location have left-aligned editorial text.
p=replace_one(p,
    'Text(bio, textAlign: TextAlign.center, style: const TextStyle(color: Colors.black87, fontSize: 15))',
    'Align(alignment:Alignment.centerLeft,child:Text(bio,textAlign:TextAlign.start,style:const TextStyle(color:Colors.black87,fontSize:15)))',
    'left aligned biography')
p=replace_one(p,
    'Row(mainAxisAlignment:MainAxisAlignment.center,children:[const Icon(Icons.location_on_outlined',
    'Row(mainAxisAlignment:MainAxisAlignment.start,children:[const Icon(Icons.location_on_outlined',
    'profile location alignment')

# Cover image keeps last rendered bitmap during asynchronous provider refresh.
p=replace_one(p,
    'Image(image:NgelXAgImageProvider(kapakUrl),fit:BoxFit.cover,alignment:Alignment(0,kapakY))',
    'Image(image:NgelXAgImageProvider(kapakUrl),fit:BoxFit.cover,alignment:Alignment(0,kapakY),gaplessPlayback:true)',
    'cover display gapless refresh')

# 2. Four counters get rounded lilac card and separators. Values and handlers unchanged.
anchor='                          return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:['
if p.count(anchor)!=1:
    raise SystemExit(f'profile stats Row changed: {p.count(anchor)}')
sidx=p.index(anchor)
eidx=p.index('                          ]);',sidx)+len('                          ]);')
original=p[sidx:eidx]
lines=[x.strip() for x in original.splitlines() if '_beyazIstatistik(' in x]
if len(lines)!=4 or not all(x.endswith(',') for x in lines):
    raise SystemExit('Expected exact four live stat controls')
cells=[]
for i,x in enumerate(lines):
    cells.append('                              Expanded(child:'+x[:-1]+'),')
    if i<3:cells.append('                              Container(height:44,width:1,color:const Color(0xFFE4DFF1)),')
card="""                          return Container(
                            width:double.infinity,
                            padding:const EdgeInsets.symmetric(horizontal:7,vertical:9),
                            decoration:BoxDecoration(
                              color:const Color(0xFFF5F1FD),
                              border:Border.all(color:const Color(0xFFEAE3F8)),
                              borderRadius:BorderRadius.circular(20),
                            ),
                            child:Row(children:[
"""+"\n".join(cells)+"""
                            ]),
                          );"""
p=p[:sidx]+card+p[eidx:]

# 3. Buttons: show the full "Arkadaş Ekle" label even on narrow 360dp devices.
p=replace_one(p,
    'SizedBox(width:122,height:54,child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF6F1FF),foregroundColor:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18))),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),icon:const Icon(Icons.person_add_alt_1),label:const Text(\'Arkadaş Ekle\',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(fontSize:10.5,fontWeight:FontWeight.w800))))',
    """SizedBox(width:134,height:54,child:FilledButton(
                      style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF6F1FF),foregroundColor:Colors.black,padding:const EdgeInsets.symmetric(horizontal:5),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18))),
                      onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),
                      child:const Row(mainAxisAlignment:MainAxisAlignment.center,mainAxisSize:MainAxisSize.min,children:[
                        Icon(Icons.person_add_alt_1,size:17),SizedBox(width:4),
                        Flexible(child:FittedBox(fit:BoxFit.scaleDown,child:Text('Arkadaş Ekle',maxLines:1,style:TextStyle(color:Colors.black,fontSize:12,fontWeight:FontWeight.w800)))),
                      ]),
                    ))""",
    'full friend button text')

# 4. Shortcuts: label may wrap to two lines, no 1-line ellipses.
p=replace_one(p,
    """Widget _profilKisayol(IconData ikon,String yazi,{VoidCallback? tiklama})=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(15),child:SizedBox(width:58,child:Column(children:[Container(width:48,height:48,decoration:BoxDecoration(color:const Color(0xFFF3F4F7),borderRadius:BorderRadius.circular(15)),child:Icon(ikon,color:Colors.black87)),const SizedBox(height:5),Text(yazi,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:9.4,fontWeight:FontWeight.w700))])));""",
    """Widget _profilKisayol(IconData ikon,String yazi,{VoidCallback? tiklama})=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(15),child:SizedBox(width:55,child:Column(children:[Container(width:48,height:48,decoration:BoxDecoration(color:const Color(0xFFF3F4F7),borderRadius:BorderRadius.circular(15)),child:Icon(ikon,color:Colors.black87)),const SizedBox(height:5),Text(yazi,textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.visible,style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w700))])));""",
    'shortcut readable labels')

# Prevent two lines clipping inside 92px highlights/quicklinks area.
p=replace_one(p,'const SizedBox(height: 22),\n                  Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_profilKisayol(',
    'const SizedBox(height: 22),\n                  Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_profilKisayol(',
    'shortcut handler preserved check') # no-op intentional anchor check

# 5. Reference intro block: title/description on left; actual playable video at right.
intro_start=p.index('                  Container(\n                    width:double.infinity,\n                    padding:const EdgeInsets.all(15),',p.index("                  const SizedBox(height: 17),"))
intro_end=p.index('                  const SizedBox(height: 22),',intro_start)
intro_old=p[intro_start:intro_end]
if 'ProfilTanitimVideoKarti(url:tanitimVideoUrl)' not in intro_old or 'onPressed:tanitimVideosuYukle' not in intro_old:
    raise SystemExit('intro video real uploader/player missing')
intro_new="""                  Container(
                    width:double.infinity,
                    padding:const EdgeInsets.all(13),
                    decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE9E9F2))),
                    child:Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
                      Expanded(flex:5,child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                        const Row(children:[
                          Icon(Icons.video_library_rounded,color:Color(0xFF7C3AED),size:22),
                          SizedBox(width:5),
                          Expanded(child:Text('Tanıtım videosu',style:TextStyle(color:Colors.black87,fontSize:14,fontWeight:FontWeight.w900))),
                        ]),
                        const SizedBox(height:7),
                        const Text('Kendini daha iyi ifade et, hikâyeni paylaş.',style:TextStyle(color:Colors.black54,fontSize:12)),
                        const SizedBox(height:11),
                        TextButton.icon(
                          onPressed:tanitimVideosuYukle,
                          style:TextButton.styleFrom(padding:const EdgeInsets.symmetric(horizontal:5,vertical:7),backgroundColor:const Color(0xFFF2EAFD)),
                          icon:const Icon(Icons.play_circle_fill_rounded,color:Color(0xFF7C3AED),size:16),
                          label:Text(tanitimVideoUrl.isEmpty?t('addIntroVideo'):t('changeIntroVideo'),maxLines:2,style:const TextStyle(color:Color(0xFF6D35D9),fontSize:11,fontWeight:FontWeight.w800)),
                        ),
                      ])),
                      const SizedBox(width:10),
                      Expanded(flex:4,child:tanitimVideoUrl.isNotEmpty
                        ?ProfilTanitimVideoKarti(url:tanitimVideoUrl)
                        :Container(
                          height:135,
                          decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFFEAE3FA),Color(0xFFF1F5FF)]),borderRadius:BorderRadius.circular(14)),
                          child:const Center(child:Icon(Icons.play_circle_outline_rounded,color:Color(0xFF7C3AED),size:42)),
                        ),
                      ),
                    ]),
                  ),
"""
p=p[:intro_start]+intro_new+p[intro_end:]

# 6. The Highlights row only displays real stories. Improve thumbnails and empty state.
p=replace_one(p,
    "child:video?const Icon(Icons.play_arrow_rounded,color:Colors.white,size:30):(url.isEmpty?const Icon(Icons.auto_stories_rounded,color:mor):null),",
    "child:video?ClipOval(child:SizedBox(width:56,height:56,child:Stack(fit:StackFit.expand,children:[NgelXVideoKapakOnizleme(url:url),const Center(child:Icon(Icons.play_arrow_rounded,color:Colors.white,size:27))]))):(url.isEmpty?const Icon(Icons.auto_stories_rounded,color:mor):null),",
    'real video highlight cover')
p=replace_one(p,
    """Text(video?'Video':'Öne çıkan',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:11)),""",
    """Text((v['highlightTitle']??(video?'Video':'Öne çıkan')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:11)),""",
    'real highlight titles')
p=replace_one(p,
    """                        _oneCikan(Icons.add,'Yeni',hikayeYukle),
                        ...h.take(8).map((d){""",
    """                        _oneCikan(Icons.add,'Yeni',hikayeYukle),
                        if(h.isEmpty)const Padding(padding:EdgeInsets.only(top:20,left:8),child:Text('Öne çıkan hikâyelerin burada görünecek',style:TextStyle(color:Colors.black45,fontSize:12))),
                        ...h.take(8).map((d){""",
    'highlight empty state')

src=src[:ps]+p+src[pe:]

# 7. Increase only central navigation Create appearance, no navigation callback changes.
nav_start=src.index('bottomNavigationBar:akis&&temizAkis')
nav_end=src.index('            ),\n          );',nav_start)
nav=src[nav_start:nav_end]
nav=replace_one(nav,'width:38,height:30,','width:54,height:46,','create button unselected size')
nav=replace_one(nav,'width:42,height:32,','width:58,height:48,','create button selected size')
nav=replace_one(nav,'borderRadius:BorderRadius.circular(11),','borderRadius:BorderRadius.circular(24),','create button rounded default')
nav=replace_one(nav,'borderRadius:BorderRadius.circular(12),','borderRadius:BorderRadius.circular(24),','create button rounded selected')
nav=replace_one(nav,'child:const Icon(Icons.add_rounded,color:Colors.white,size:24)','child:const Icon(Icons.add_rounded,color:Colors.white,size:29)','create plus default')
nav=replace_one(nav,'child:const Icon(Icons.add_rounded,color:Colors.white,size:26)','child:const Icon(Icons.add_rounded,color:Colors.white,size:30)','create plus selected')
nav=nav.replace('height:67,','height:76,')
src=src[:nav_start]+nav+src[nav_end:]

# Existing published functionality must stay wired to the same backend.
assert "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in src
assert 'gelenKutusuIsteginiSonuclandir' in src
assert 'ngelxFotografYukle(' in src
assert 'onPressed:tanitimVideosuYukle' in src
assert 'NgelXKapakKonumlandirPage' in src
assert 'HikayeGosterPage(' in src
assert '_kaydedilenGrid()' in src
assert '_finalUretKart' in src
mainfile.write_text(src,encoding='utf-8')
pubfile.write_text(pub,encoding='utf-8')
print('Build 402 applied — reference profile layout, readable buttons, real highlight thumbnails and prominent Create. Backend preserved.')
