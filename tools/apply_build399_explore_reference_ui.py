#!/usr/bin/env python3
from pathlib import Path
p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")

src=src.replace("  int kategori=0;","  int kategori=-1;",1)

old="""            child:Row(children:[
              Text(t('explore'),style:const TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),
              const Spacer(),
              // Build 372: the large search field below is the single search entry point.
              IconButton(tooltip:t('filter'),onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded,color:Colors.black,size:25)),
            ]),"""
new="""            child:Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Text(t('explore'),style:const TextStyle(color:Color(0xFF080E1D),fontSize:31,fontWeight:FontWeight.w900,letterSpacing:-.7)),
                const SizedBox(height:2),
                const Text('Yeni insanları, içerikleri ve grupları keşfet',style:TextStyle(color:Color(0xFF858B9A),fontSize:13.5)),
              ])),
              IconButton(tooltip:t('search'),onPressed:_aramaAc,icon:const Icon(Icons.search_rounded,color:Colors.black,size:28)),
              IconButton(tooltip:t('notifications'),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),icon:const Icon(Icons.notifications_none_rounded,color:Colors.black,size:28)),
              IconButton(tooltip:t('filter'),onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded,color:Colors.black,size:25)),
            ]),"""
if old not in src: raise SystemExit("explore header anchor missing")
src=src.replace(old,new,1)

oldchips="""              children:[
                _kesfetSekmesi(Icons.live_tv_rounded,t('live'),0),
                _kesfetSekmesi(Icons.mic_rounded,'Sesli',1),
                _kesfetSekmesi(Icons.local_fire_department_rounded,t('trend'),2),
                _kesfetSekmesi(Icons.person_rounded,t('people'),3),
                _kesfetSekmesi(Icons.groups_rounded,t('groups'),4),
              ],"""
newchips="""              children:[
                _kesfetSekmesi(Icons.grid_view_rounded,'Tümü',-1),
                _kesfetSekmesi(Icons.wifi_tethering_rounded,t('live'),0),
                _kesfetSekmesi(Icons.mic_rounded,'Sesli',1),
                _kesfetSekmesi(Icons.local_fire_department_rounded,t('trend'),2),
                _kesfetSekmesi(Icons.person_rounded,t('people'),3),
                _kesfetSekmesi(Icons.groups_rounded,t('groups'),4),
              ],"""
if oldchips not in src: raise SystemExit("explore chips anchor missing")
src=src.replace(oldchips,newchips,1)
src=src.replace("          if(kategori==0)..._canliSliverleri(),","          if(kategori==-1)..._trendSliverleri(),\n          if(kategori==0)..._canliSliverleri(),",1)
src=src.replace("child:Text(trend?'Trend canlı yayınlar':t('liveStreams'),","child:Text(trend?'Trend canlı yayınlar':'Canlı Yayınlar',",1)

# Match approved purple-blue selected chip.
src=src.replace("gradient:kategori==index?const LinearGradient(colors:[Color(0xFF7C3AED),Color(0xFFA855F7)]):null,","gradient:kategori==index?const LinearGradient(colors:[Color(0xFF9B3EFF),Color(0xFF365BFF)]):null,",1)

p.write_text(src,encoding="utf-8")
print("Build 399 Explore reference structure applied.")
