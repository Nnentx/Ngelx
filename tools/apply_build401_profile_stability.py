#!/usr/bin/env python3
"""Build 401: preserve Build 400 behavior while fixing invisible labels and profile reference gaps."""
from pathlib import Path

path=Path('app/lib/main.dart')
src=path.read_text(encoding='utf-8')

def exactly(hay,old,new,label):
    found=hay.count(old)
    if found!=1:
        raise SystemExit(f'{label}: expected 1 anchor, found {found}: {old[:100]!r}')
    return hay.replace(old,new,1)

# Correct the version applied by the previous Build 400 hotfix.
src=exactly(src,"defaultValue: '400'","defaultValue: '401'","build number")
src=exactly(src,"defaultValue: '1.0.176'","defaultValue: '1.0.177'","build name")
pubfile=Path('app/pubspec.yaml')
pub=pubfile.read_text(encoding='utf-8')
pub=exactly(pub,'version: 1.0.176+400','version: 1.0.177+401','pubspec')

# 1) Fix the proven white-on-white cover actions. Preserve the same actions and R2 upload.
start=src.index('  Future<void> kapakFotografiDuzenle()async{')
stop=src.index('  Future<void> tanitimVideosuYukle()',start)
cover=src[start:stop]
for old,new in [
    ("TextStyle(fontSize:19,fontWeight:FontWeight.w900)","TextStyle(color:Colors.black87,fontSize:19,fontWeight:FontWeight.w900)"),
    ("subtitle:Text('Fotoğrafı seçtikten sonra parmağınla sürükleyerek kadrajı ayarla.')",
     "subtitle:Text('Fotoğrafı seçtikten sonra parmağınla sürükleyerek kadrajı ayarla.',style:const TextStyle(color:Colors.black54))"),
    ("title:const Text('Galeriden seç')","title:const Text('Galeriden seç',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))"),
    ("title:const Text('Kapağı yeniden konumlandır')","title:const Text('Kapağı yeniden konumlandır',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))"),
]:
    cover=exactly(cover,old,new,'cover contrast')
cover=exactly(cover,
    'builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[',
    'builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[',
    'cover sheet light theme')
cover=exactly(cover,'      ])),\n    );','      ]))),\n    );','cover sheet close theme')
src=src[:start]+cover+src[stop:]

# 2) Older story viewer was using the dark app text theme in a white actions sheet.
start=src.index('class _HikayeGosterPageState extends State<HikayeGosterPage>')
stop=src.index('\nclass ',start+20)
story=src[start:stop]
story=exactly(story,
    'builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[',
    'builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[',
    'story sheet light theme')
for old,new in [
    ("title:Text(videoMu?'Video hikâye':'Fotoğraf hikâyesi'),subtitle:Text(zamanBilgisi)",
     "title:Text(videoMu?'Video hikâye':'Fotoğraf hikâyesi',style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),subtitle:Text(zamanBilgisi,style:const TextStyle(color:Colors.black54))"),
    ("title:const Text('Hikâyeyi paylaş')","title:const Text('Hikâyeyi paylaş',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))"),
    ("title:const Text('NgelX içinde özele gönder')","title:const Text('NgelX içinde özele gönder',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))"),
    ("subtitle:const Text('Yalnızca seçtiğin kişilere özel mesaj olarak gönderilir.')",
     "subtitle:const Text('Yalnızca seçtiğin kişilere özel mesaj olarak gönderilir.',style:TextStyle(color:Colors.black54))"),
    ("title:const Text('Kapat')","title:const Text('Kapat',style:TextStyle(color:Colors.black87))"),
    ("                    ])),\n                  ).whenComplete(_devam);",
     "                    ]))),\n                  ).whenComplete(_devam);"),
]:
    story=exactly(story,old,new,'story actions contrast')
src=src[:start]+story+src[stop:]

# 3) Profile controls, stats and tabs: modify ONLY the owner profile class.
start=src.index('class _ProfilPageState extends State<ProfilPage>')
stop=src.index('\nclass _ProfilEtkilesimRozeti',start)
profile=src[start:stop]

# The 'more' sheet shares the same white-on-white vulnerability.
profile=exactly(profile,
    'builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[\n        ListTile(leading:const Icon(Icons.visibility_outlined)',
    'builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[\n        ListTile(leading:const Icon(Icons.visibility_outlined)',
    'profile more sheet light theme')
profile=exactly(profile,
    "        ListTile(leading:const Icon(Icons.settings_outlined),title:Text(t('settingsTitle')),onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page()));}),\n      ])),",
    "        ListTile(leading:const Icon(Icons.settings_outlined),title:Text(t('settingsTitle')),onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page()));}),\n      ]))),",
    'profile more sheet close theme')

# Add illustrated stats without touching any Firestore counters or tap handlers.
profile=exactly(profile,
  "  Widget _beyazIstatistik(String sayi,String baslik,VoidCallback tiklama)=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(14),child:Padding(padding:const EdgeInsets.symmetric(horizontal:7,vertical:7),child:Column(children:[Text(sayi,style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)),Text(baslik,style:const TextStyle(color:Colors.black54))])));",
  """  Widget _beyazIstatistik(String sayi,String baslik,VoidCallback tiklama){
    final ikon=baslik==t('following')?Icons.person_rounded:
      baslik==t('followers')?Icons.people_rounded:
      baslik==t('interaction')?Icons.bar_chart_rounded:Icons.group_rounded;
    return InkWell(
      onTap:tiklama,borderRadius:BorderRadius.circular(14),
      child:Padding(
        padding:const EdgeInsets.symmetric(horizontal:2,vertical:7),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(ikon,color:const Color(0xFF743CF4),size:21),
          const SizedBox(height:3),
          Text(sayi,style:const TextStyle(color:Colors.black,fontSize:19,fontWeight:FontWeight.w900)),
          Text(baslik,maxLines:1,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFF707584),fontSize:11,fontWeight:FontWeight.w700)),
        ]),
      ),
    );
  }""",
  'profile stats visuals')

# Keep existing section handlers but restore the mockup tab order.
old_tabs="""                      _ProfilSekme(t('posts'),profilSekme==0,()=>setState(()=>profilSekme=0)),const SizedBox(width:12),
                      _ProfilSekme(t('reels'),profilSekme==1,()=>setState(()=>profilSekme=1)),const SizedBox(width:12),
                      _ProfilSekme(t('tagged'),profilSekme==2,()=>setState(()=>profilSekme=2)),const SizedBox(width:12),
                      _ProfilSekme('Hikayeler',profilSekme==3,()=>setState(()=>profilSekme=3)),const SizedBox(width:12),
                      _ProfilSekme(t('saved'),profilSekme==4,()=>setState(()=>profilSekme=4)),"""
new_tabs="""                      _ProfilSekme(t('posts'),profilSekme==0,()=>setState(()=>profilSekme=0)),const SizedBox(width:12),
                      _ProfilSekme(t('reels'),profilSekme==1,()=>setState(()=>profilSekme=1)),const SizedBox(width:12),
                      _ProfilSekme('Hikayeler',profilSekme==3,()=>setState(()=>profilSekme=3)),const SizedBox(width:12),
                      _ProfilSekme(t('saved'),profilSekme==4,()=>setState(()=>profilSekme=4)),const SizedBox(width:12),
                      _ProfilSekme(t('tagged'),profilSekme==2,()=>setState(()=>profilSekme=2)),"""
profile=exactly(profile,old_tabs,new_tabs,'reference tab ordering')

# Always show an explanatory intro-video card, only the stored real video is rendered.
old_intro="""                  SizedBox(width:double.infinity,child:OutlinedButton.icon(
                    onPressed:tanitimVideosuYukle,
                    icon:const Icon(Icons.video_camera_front_outlined),
                    label:Text(tanitimVideoUrl.isEmpty?t('addIntroVideo'):t('changeIntroVideo')),
                  )),
                  if(tanitimVideoUrl.isNotEmpty) ...[
                    const SizedBox(height:12),
                    ProfilTanitimVideoKarti(url:tanitimVideoUrl),
                  ],"""
new_intro="""                  Container(
                    width:double.infinity,
                    padding:const EdgeInsets.all(15),
                    decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE9E9F2))),
                    child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                      const Row(children:[
                        Icon(Icons.video_library_rounded,color:Color(0xFF7C3AED),size:23),
                        SizedBox(width:8),
                        Text('Tanıtım videosu',style:TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900)),
                      ]),
                      const SizedBox(height:7),
                      const Text('Kendini daha iyi ifade et, hikâyeni paylaş.',style:TextStyle(color:Colors.black54,fontSize:13)),
                      const SizedBox(height:12),
                      if(tanitimVideoUrl.isNotEmpty)...[
                        ProfilTanitimVideoKarti(url:tanitimVideoUrl),
                        const SizedBox(height:12),
                      ] else Container(
                        width:double.infinity,padding:const EdgeInsets.symmetric(vertical:18,horizontal:12),
                        decoration:BoxDecoration(color:const Color(0xFFF6F3FF),borderRadius:BorderRadius.circular(14)),
                        child:const Row(children:[
                          Icon(Icons.play_circle_outline,color:Color(0xFF7C3AED)),
                          SizedBox(width:10),
                          Expanded(child:Text('Henüz tanıtım videosu eklenmedi',style:TextStyle(color:Color(0xFF555066),fontSize:13))),
                        ]),
                      ),
                      const SizedBox(height:10),
                      Align(alignment:Alignment.centerLeft,child:TextButton.icon(
                        onPressed:tanitimVideosuYukle,
                        icon:const Icon(Icons.play_circle_fill_rounded,color:Color(0xFF7C3AED)),
                        label:Text(tanitimVideoUrl.isEmpty?t('addIntroVideo'):t('changeIntroVideo'),style:const TextStyle(color:Color(0xFF6D35D9),fontWeight:FontWeight.w800)),
                      )),
                    ]),
                  ),"""
profile=exactly(profile,old_intro,new_intro,'intro card')
# Keep actions while making the add-friend label readable on narrow phones.
profile=exactly(profile,
  "label:const Text('Arkadaş Ekle',style:TextStyle(fontSize:11,fontWeight:FontWeight.w800))",
  "label:const Text('Arkadaş Ekle',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(fontSize:10.5,fontWeight:FontWeight.w800))",
  'friend button text')
src=src[:start]+profile+src[stop:]

# Reference line is purple. This one small widget is shared by profile tabs.
src=exactly(src,
  "BorderSide(color:secili?mavi:Colors.transparent,width:3)",
  "BorderSide(color:secili?const Color(0xFF7C3AED):Colors.transparent,width:3)",
  'profile selected tab')

# Change ONLY the main five-tab navigation visuals; keep every destination callback intact.
start=src.index('bottomNavigationBar:akis&&temizAkis')
stop=src.index('                      destinations:[',start)
nav=src[start:stop]
for old,new in [
    ('color:Colors.black,\n                    border:Border(top:BorderSide(color:Color(0xFF161616)))',
     'color:Colors.white,\n                    border:Border(top:BorderSide(color:Color(0xFFE6E8EF)))'),
    ('BoxShadow(color:Color(0x66000000),blurRadius:18)','BoxShadow(color:Color(0x18000000),blurRadius:12)'),
    ('height:60','height:67'),
    ('backgroundColor:Colors.black','backgroundColor:Colors.white'),
    ('indicatorColor:Colors.transparent','indicatorColor:const Color(0xFFF0EAFE)'),
    ('color:s.contains(WidgetState.selected)?Colors.white:Colors.white60',
     'color:s.contains(WidgetState.selected)?const Color(0xFF7136E9):const Color(0xFF303442)'),
]:
    found=nav.count(old)
    if old=='height:60':
        if found!=2:raise SystemExit(f'nav heights expected 2 got {found}')
        nav=nav.replace(old,new)
    elif old.startswith('color:s.contains'):
        if found!=2:raise SystemExit(f'nav selected colors expected 2 got {found}')
        nav=nav.replace(old,new)
    else:
        nav=exactly(nav,old,new,'bottom nav style')
src=src[:start]+nav+src[stop:]

# Preserve stable installation identity, login, messages, and media storage.
assert "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in src
assert 'gelenKutusuIsteginiSonuclandir' in src
assert '_finalUretKart' in src
assert 'NgelXKapakKonumlandirPage' in src
path.write_text(src,encoding='utf-8')
pubfile.write_text(pub,encoding='utf-8')
print('Build 401 applied: white-sheet labels, profile reference card/tabs/stats, white navigation, preserving working flows.')
