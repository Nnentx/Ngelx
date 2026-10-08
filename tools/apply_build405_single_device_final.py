#!/usr/bin/env python3
"""Build 405: final single-device fixes after 404. Never synthesize media or users."""
from pathlib import Path

def read(path): return Path(path).read_text(encoding="utf-8")
def save(path, contents): Path(path).write_text(contents, encoding="utf-8")
def one(contents, old, new, label):
    count=contents.count(old)
    if count!=1: raise SystemExit(f"{label}: expected exactly 1 anchor, found {count}")
    return contents.replace(old,new,1)

# Version bump, without changing Firebase, account identity, or saved content.
main=read("app/lib/main.dart")
main=one(main,"defaultValue: '404'","defaultValue: '405'","build number")
main=one(main,"defaultValue: '1.0.180'","defaultValue: '1.0.181'","build name")
pub=one(read("app/pubspec.yaml"),"version: 1.0.180+404","version: 1.0.181+405","pubspec")

# The owner-only button navigates to the friends list, not an add-friend flow.
start=main.index("class _ProfilPageState extends State<ProfilPage>")
end=main.index("\nclass _ProfilEtkilesimRozeti",start)
profile=main[start:end]
profile=one(profile,"'Arkadaş Ekle'","'Arkadaşlar'","owner profile truthful friends CTA")
# Two-line shortcuts stay aligned even if the Kaydedilenler label wraps.
old="Text(yazi,textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.visible,style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w700))"
new="SizedBox(height:28,child:Center(child:Text(yazi,textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w700))))"
profile=one(profile,old,new,"owner shortcut equal height")
main=main[:start]+profile+main[end:]
save("app/lib/main.dart",main)
save("app/pubspec.yaml",pub)

# The story countdown must not run while a photo/video is still initializing.
path="app/lib/story_v66.dart"
story=read(path)
story=one(story,
"""      await x.initialize();
      if(!mounted||sonrakiVideoKontrol!=x||sonrakiVideoIndex!=index){""",
"""      await x.initialize().timeout(const Duration(seconds:12));
      if(!mounted||sonrakiVideoKontrol!=x||sonrakiVideoIndex!=index){""",
"story next video preload timeout")
story=one(story,
"""    if(adres.isEmpty||Uri.tryParse(adres)?.hasScheme!=true||!_videoMu(v,adres)){
      final eski=sonrakiVideoKontrol;""",
"""    if(adres.isNotEmpty&&Uri.tryParse(adres)?.hasScheme==true&&!_videoMu(v,adres)&&mounted){
      unawaited(precacheImage(NgelXAgImageProvider(adres),context).catchError((Object _){ }));
    }
    if(adres.isEmpty||Uri.tryParse(adres)?.hasScheme!=true||!_videoMu(v,adres)){
      final eski=sonrakiVideoKontrol;""",
"next image prefetch")
story=one(story,
"""    if(!videoMu){
      if(onceki!=null)unawaited(onceki.dispose());
      sure.duration=const Duration(seconds:7);
      if(mounted)setState((){});
      sure.forward(from:0);
      unawaited(_sonrakiniHazirla());
      return;
    }""",
"""    if(!videoMu){
      if(onceki!=null)unawaited(onceki.dispose());
      sure.duration=const Duration(seconds:7);
      if(mounted)setState((){});
      try{
        await precacheImage(NgelXAgImageProvider(medyaAdresi),context)
          .timeout(const Duration(seconds:12));
        if(!mounted||nesil!=medyaNesli)return;
        setState(()=>videoHata=false);
        sure.forward(from:0);
        unawaited(_sonrakiniHazirla());
      }catch(_){
        if(!mounted||nesil!=medyaNesli)return;
        setState(()=>videoHata=true);
      }
      return;
    }""",
"story photo wait before countdown")
story=one(story,
"""      await x.initialize();
      if(!mounted||nesil!=medyaNesli){await x.dispose();return;}""",
"""      await x.initialize().timeout(const Duration(seconds:12));
      if(!mounted||nesil!=medyaNesli){await x.dispose();return;}""",
"story current video timeout")
story=one(story,
"""      setState(()=>videoHata=true);
      sure.duration=const Duration(seconds:7);
      sure.forward(from:0);
      unawaited(_sonrakiniHazirla());""",
"""      setState(()=>videoHata=true);
      sure.stop();
      unawaited(_sonrakiniHazirla());""",
"story errored video must wait for retry")
story=one(story,
"""    if(!mounted||yukleniyor||belge==null)return;
    if(!sure.isAnimating)sure.forward();""",
"""    if(!mounted||yukleniyor||belge==null)return;
    if(videoHata||(videoMu&&!videoHazir))return;
    if(!sure.isAnimating)sure.forward();""",
"story resume not while loading")
story=one(story,
"""    if(!videoMu){
      return NgelXAgResmi(
        url:url,
        fit:BoxFit.contain,
        placeholder:const Center(child:CircularProgressIndicator(color:Colors.white)),
        error:const Center(child:Icon(Icons.broken_image_outlined,color:Colors.white54,size:60)),
      );
    }
    if(videoHata)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Icon(Icons.videocam_off_outlined,color:Colors.white54,size:62),
      SizedBox(height:10),
      Text('Video hikâye açılamadı',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
    ]));
    if(!videoHazir||videoKontrol==null)return const Center(child:CircularProgressIndicator(color:Colors.white));""",
"""    if(videoHata)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Icon(videoMu?Icons.videocam_off_outlined:Icons.broken_image_outlined,color:Colors.white70,size:54),
      const SizedBox(height:10),
      Text(videoMu?'Video hikâye açılamadı':'Fotoğraf hikâye açılamadı',
        style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
      const SizedBox(height:12),
      OutlinedButton.icon(
        style:OutlinedButton.styleFrom(foregroundColor:Colors.white),
        onPressed:(){setState(()=>videoHata=false);unawaited(_aktifHikayeyiBaslat());},
        icon:const Icon(Icons.refresh_rounded),
        label:const Text('Tekrar dene'),
      ),
    ]));
    if(!videoMu){
      return NgelXAgResmi(
        url:url,
        fit:BoxFit.contain,
        placeholder:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          CircularProgressIndicator(color:Colors.white),
          SizedBox(height:10),
          Text('Hikâye yükleniyor...',style:TextStyle(color:Colors.white70)),
        ])),
        error:Center(child:TextButton.icon(
          onPressed:(){setState(()=>videoHata=false);unawaited(_aktifHikayeyiBaslat());},
          icon:const Icon(Icons.refresh_rounded),
          label:const Text('Tekrar dene'),
        )),
      );
    }
    if(!videoHazir||videoKontrol==null)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      CircularProgressIndicator(color:Colors.white),
      SizedBox(height:10),
      Text('Video hazırlanıyor...',style:TextStyle(color:Colors.white70)),
    ]));""",
"story media retry/loading UI")
save(path,story)

# Host stream end is ONE persistent view, not a modal behind an existing overlay.
path="app/lib/live_broadcast_studio.dart"
live=read(path)
live=one(live,"  bool yayinBitti=false;","  bool yayinBitti=false;\n  bool bitisOzetiHazir=false;","live end-ready state")
live=one(live,
"""    await widget.oda.disconnect();
    await widget.oda.dispose();
    if (geriDon && mounted) Navigator.pop(context);""",
"""    await widget.oda.disconnect();
    await widget.oda.dispose();
    if(mounted)setState(()=>bitisOzetiHazir=true);
    if (geriDon && mounted) Navigator.pop(context);""",
"end ready after stream clean up")
start=live.index("  Future<bool> _geri() async {")
end=live.index("  Future<Map<String, dynamic>> _aktifProfil() async {",start)
if "Canlı yayın özeti" not in live[start:end]: raise SystemExit("existing live summary anchor changed")
live=live[:start]+"""  Future<bool> _geri() async {
    // After the stream ends, only the explicit return button may dismiss summary.
    if(kapatildi||yayinBitti)return false;
    await _klavyeyiKapat();
    if(widget.yayinSahibi){
      final onay=await showDialog<bool>(
        context:context,
        builder:(_)=>AlertDialog(
          title:const Text('Yayın bitsin mi?'),
          content:const Text('Canlı yayın tüm izleyiciler için sona erecek.'),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('Devam et')),
            FilledButton(onPressed:()=>Navigator.pop(context,true),child:const Text('Yayını bitir')),
          ],
        ),
      )??false;
      if(!onay||!mounted)return false;
      await _bitir(geriDon:false);
      return false; // Avoid WillPopScope and manual button popping twice.
    }
    await _bitir(geriDon:false);
    return true;
  }

"""+live[end:]
start=live.index("          if(yayinBitti)Positioned.fill(child:ColoredBox(")
end=live.index("\n        ]),\n      ),\n    );\n  }\n}",start)
live=live[:start]+"          if(yayinBitti)Positioned.fill(child:_bitisEkrani()),"+live[end:]
needle="  @override\n  Widget build(BuildContext context) {\n    final track = _goruntu();"
if live.count(needle)!=1: raise SystemExit("live build insertion anchor changed")
widget="""  Widget _bitisEkrani(){
    final m=(saniye~/60).toString().padLeft(2,'0');
    final s=(saniye%60).toString().padLeft(2,'0');
    return ColoredBox(
      color:const Color(0xF2111111),
      child:SafeArea(child:Center(child:SingleChildScrollView(
        padding:const EdgeInsets.all(22),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          const Icon(Icons.stop_circle_rounded,color:Color(0xFFFF1744),size:68),
          const SizedBox(height:13),
          const Text('CANLI YAYIN SONA ERDİ',textAlign:TextAlign.center,
            style:TextStyle(color:Colors.white,fontSize:22,fontWeight:FontWeight.w900)),
          const SizedBox(height:8),
          Text(bitisMesaji,textAlign:TextAlign.center,
            style:const TextStyle(color:Colors.white70,fontSize:13)),
          const SizedBox(height:17),
          if(!bitisOzetiHazir)
            const Padding(padding:EdgeInsets.all(20),
              child:CircularProgressIndicator(color:Colors.white)),
          if(bitisOzetiHazir&&widget.yayinSahibi)
            Container(
              padding:const EdgeInsets.all(17),
              decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(20)),
              child:Column(mainAxisSize:MainAxisSize.min,children:[
                const Text('Canlı yayın özeti',
                  style:TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900)),
                const SizedBox(height:11),
                _CanliOzetSatiri(ikon:Icons.schedule_rounded,etiket:'Süre',deger:m+':'+s),
                _CanliOzetSatiri(ikon:Icons.visibility_rounded,etiket:'En yüksek izleyici',deger:'$maxIzleyici'),
                _CanliOzetSatiri(ikon:Icons.favorite_rounded,etiket:'Beğeni',deger:'$sonToplamKalp'),
                _CanliOzetSatiri(ikon:Icons.chat_bubble_rounded,etiket:'Yorum',deger:'$sonYorumSayisi'),
                _CanliOzetSatiri(ikon:Icons.card_giftcard_rounded,etiket:'Hediye puanı',deger:'$sonHediyePuani'),
              ]),
            ),
          const SizedBox(height:17),
          FilledButton.icon(
            style:FilledButton.styleFrom(backgroundColor:Colors.white,
              foregroundColor:Colors.black,minimumSize:const Size(220,50)),
            onPressed:bitisOzetiHazir?()=>Navigator.pop(context):null,
            icon:const Icon(Icons.explore_rounded),
            label:const Text('Keşfet’e dön',style:TextStyle(fontWeight:FontWeight.w900)),
          ),
        ]),
      ))),
    );
  }

"""
live=live.replace(needle,widget+needle,1)
save(path,live)
print("Build 405 patch: live persistent summary, story media retry/timing, profile final CTA/spacing.")
