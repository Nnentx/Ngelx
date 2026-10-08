#!/usr/bin/env python3
"""Build 403: visual and loading-state hotfix; applied after Build 402."""
from pathlib import Path
def one(s,a,b,k):
    n=s.count(a)
    if n!=1: raise SystemExit(f'{k}: expected one anchor, found {n}: {a[:90]}')
    return s.replace(a,b,1)
def read(p):return Path(p).read_text(encoding='utf-8')
def write(p,s):Path(p).write_text(s,encoding='utf-8')

p='app/lib/main.dart';s=read(p)
s=one(s,"defaultValue: '402'","defaultValue: '403'",'build code')
s=one(s,"defaultValue: '1.0.178'","defaultValue: '1.0.179'",'build name')
# Actual duration from playable video, not invented sample duration.
i=s.index('class _ProfilTanitimVideoKartiState');j=s.index('\nclass ',i+10);c=s[i:j]
c=one(c,'Center(child:AspectRatio(aspectRatio:videoOrani,child:VideoPlayer(x))),',
"""Center(child:AspectRatio(aspectRatio:videoOrani,child:VideoPlayer(x))),
              if(x.value.duration>Duration.zero)
                Positioned(top:8,left:8,child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:8,vertical:5),
                  decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),
                  child:Text(x.value.duration.inMinutes.toString().padLeft(2,'0')+':'+
                    (x.value.duration.inSeconds%60).toString().padLeft(2,'0'),
                    style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w900)),
                )),""",'real intro duration')
s=s[:i]+c+s[j:]
# Never leave a video tile spinning indefinitely; permit manual retry.
i=s.index('class NgelXVideoKapakOnizleme extends StatefulWidget');j=s.index('\nclass MedyaOnizleme extends StatelessWidget',i);c=s[i:j]
c=one(c,'await x.initialize();await x.seekTo(Duration.zero);',
      'await x.initialize().timeout(const Duration(seconds:12));await x.seekTo(Duration.zero);','thumbnail timeout')
c=one(c,'if(hata)return const ColoredBox(color:Color(0xFFE9ECF2),child:Center(child:Icon(Icons.video_library_outlined,size:42,color:Colors.black38)));',
"""if(hata)return Material(color:const Color(0xFFE9ECF2),child:InkWell(
  onTap:(){final eski=c;if(eski!=null)unawaited(eski.dispose());c=null;setState((){hata=false;hazir=false;});unawaited(kur());},
  child:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
    Icon(Icons.refresh_rounded,size:32,color:Color(0xFF7C3AED)),
    SizedBox(height:5),
    Text('Tekrar dene',style:TextStyle(color:Colors.black54,fontSize:10)),
  ])),
));""",'thumbnail retry')
s=s[:i]+c+s[j:]
i=s.index('class KaydedilenlerPage extends StatelessWidget');j=s.index('\nclass Logo extends StatelessWidget',i);c=s[i:j]
c=one(c,"thumbnailUrl: (veri['thumbnailUrl'] ?? '').toString()",
"""thumbnailUrl: (() {for(final k in const ['thumbnailUrl','coverUrl','posterUrl','imageUrl']){
 final v=(veri[k]??'').toString().trim();if(v.isNotEmpty)return v;
}return '';})()""",'saved thumbnail metadata')
s=s[:i]+c+s[j:]
write(p,s)
p='app/pubspec.yaml';write(p,one(read(p),'version: 1.0.178+402','version: 1.0.179+403','pubspec'))
# Selectively blue; no other settings row changes.
p='app/lib/build258_settings.dart';s=read(p)
s=one(s,'ikon:Icons.workspace_premium_rounded,renk:ngelxPremiumPurple,sayfa:(_)=>const NgelXPremiumPage(),',
      'ikon:Icons.workspace_premium_rounded,renk:const Color(0xFF2368E8),sayfa:(_)=>const NgelXPremiumPage(),','premium blue icon')
s=one(s,"Widget _satir(BuildContext c,_NgelXAyarOgesi e,{bool aramaSonucu=false})=>ListTile(",
"""Widget _satir(BuildContext c,_NgelXAyarOgesi e,{bool aramaSonucu=false})=>Container(
    decoration:BoxDecoration(
      color:e.baslik==t('premiumWallet')?const Color(0xFFEAF2FF):Colors.transparent,
      borderRadius:BorderRadius.circular(18),
    ),child:ListTile(""",'premium only background')
s=one(s,'title:Text(e.baslik,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),',
      "title:Text(e.baslik,style:TextStyle(color:e.baslik==t('premiumWallet')?const Color(0xFF1350B6):Colors.black87,fontWeight:FontWeight.w800)),",'premium only title')
s=one(s,'    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:e.sayfa)),\n  );',
      '    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:e.sayfa)),\n  ));','premium card close')
write(p,s)
# Sesli oda requests: show non-destructive timeout guidance, no new participant actions.
p='app/lib/audio_live_rooms.dart';s=read(p)
s=one(s,'  Future<void> istekler()async{\n    if(!yoneticiyim)return;',
      '  Future<void> istekler()async{\n    if(!yoneticiyim)return;\n    final istekBeklemeSiniri=Future<void>.delayed(const Duration(seconds:7));','request delay')
s=one(s,'if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));',
"""if(s.connectionState==ConnectionState.waiting&&!s.hasData)return FutureBuilder<void>(
  future:istekBeklemeSiniri,
  builder:(_,bekleme)=>bekleme.connectionState==ConnectionState.done
    ?Center(child:Padding(padding:const EdgeInsets.all(20),child:Column(mainAxisSize:MainAxisSize.min,children:[
      const Icon(Icons.wifi_find_rounded,color:mor,size:34),
      const SizedBox(height:9),
      const Text('İstekler hâlâ yükleniyor',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
      const SizedBox(height:5),
      const Text('Bağlantı yavaş olabilir. Söz istekleri silinmedi.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)),
      const SizedBox(height:10),
      OutlinedButton.icon(onPressed:(){Navigator.pop(c);unawaited(istekler());},icon:const Icon(Icons.refresh_rounded),label:const Text('Yeniden dene')),
    ])))
    :const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      CircularProgressIndicator(color:mor),SizedBox(height:11),
      Text('Söz istekleri yükleniyor...',style:TextStyle(color:Colors.black54)),
    ])),
);""",'request waiting fallback')
s=one(s,"Text('Bekleyen söz isteği yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))",
      "Text('Henüz söz isteği yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))",'request empty state')
s=one(s,
"Wrap(spacing:8,children:['Sohbet','Müzik','Teknoloji','Spor','Gündem'].map((x)=>ChoiceChip(label:Text(x),selected:kategori==x,onSelected:(_)=>setState(()=>kategori=x))).toList())",
"""Wrap(spacing:8,runSpacing:8,children:['Sohbet','Müzik','Teknoloji','Spor','Gündem'].map((x)=>ChoiceChip(
  label:Text(x,style:TextStyle(color:kategori==x?const Color(0xFF5B2CA2):Colors.black87,fontWeight:FontWeight.w700)),
  selected:kategori==x,selectedColor:const Color(0xFFEFE5FF),
  onSelected:(_)=>setState(()=>kategori=x),
)).toList())""",'voice category theme')
s=one(s, "    ),const SizedBox(height:22),\n    FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(54)),onPressed:baslatiliyor?null:baslat,",
"""    ),
    const SizedBox(height:9),
    Text(gizlilik=='public'?'Bu odayı herkes Keşfet üzerinden bulabilir.':
      gizlilik=='followers'?'Bu oda takipçilerin için görünür.':'Bu oda yalnız arkadaşların için görünür.',
      style:const TextStyle(color:Colors.black54,fontSize:12)),
    const SizedBox(height:18),
    FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:mor,minimumSize:const Size.fromHeight(54)),onPressed:baslatiliyor?null:baslat,""",
'voice privacy explanation')
write(p,s)
# Live preparation: same studio sliders, just collapsible by default.
p='app/lib/live_broadcast_studio.dart';s=read(p)
s=one(s,
"""            Container(
              padding:const EdgeInsets.fromLTRB(14,14,14,10),
              decoration:BoxDecoration(color:const Color(0xFFF7F8FA),borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE8EBEF))),
              child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(children:[
                  const Icon(Icons.auto_awesome_rounded,color:Color(0xFF7C4DFF)),""",
"""            Container(
              padding:const EdgeInsets.fromLTRB(6,2,6,4),
              decoration:BoxDecoration(color:const Color(0xFFF7F8FA),borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE8EBEF))),
              child:ExpansionTile(
                initiallyExpanded:false,
                iconColor:const Color(0xFF7C4DFF),
                title:const Text('Görüntü Stüdyosu',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
                subtitle:const Text('Efektler ve ışık ayarları',style:TextStyle(color:Colors.black54,fontSize:12)),
                children:[Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(children:[
                  const Icon(Icons.auto_awesome_rounded,color:Color(0xFF7C4DFF)),""",
'live studio header')
s=one(s,
"""                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.',style:TextStyle(color:Colors.black54)),
                ),
              ]),
            ),
            Row(children: [""",
"""                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.',style:TextStyle(color:Colors.black54)),
                ),
              ])],
            ),
            ),
            const SizedBox(height:12),
            const Padding(padding:EdgeInsets.fromLTRB(2,0,2,8),child:Text('Yayın kalitesi ve kimler izleyebilir',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
            Row(children: [""",
'live studio footer')
write(p,s)
print('Build 403 patch applied; Firestore, LiveKit, share and media upload semantics unchanged.')
