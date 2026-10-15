#!/usr/bin/env python3
"""Build462: bounded media recovery and correct cover save/display sync.

Source-only client changes following Build461, with no Firestore migrations,
production deployment, group/chat schema edits or deletion of stored media.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
LIVE=Path("app/lib/live_broadcast_studio.dart")

def only(source, old, new, name):
    count=source.count(old)
    if count != 1:
        raise ValueError(f"Build462 {name}: expected 1 anchor, got {count}")
    return source.replace(old,new,1)

def part(source,start,end,modify):
    a=source.index(start)
    b=source.index(end,a+len(start))
    return source[:a]+modify(source[a:b])+source[b:]

def owner_cover(src):
    def edit(p):
        p=only(p,
            "await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'coverPhotoUrl':url,'coverPhotoY':y,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));",
            """if(url.trim().isEmpty||Uri.tryParse(url)?.scheme!='https'){
        throw StateError('Kapak bağlantısı doğrulanamadı.');
      }
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'coverPhotoUrl':url,'coverPhotoY':y,'profileViewMode':'cover',
        'updatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));""",
            "persist covered mode after successful photo upload")
        p=only(p,"setState((){kapakUrl=url;kapakY=y;});",
             "setState((){kapakUrl=url;kapakY=y;profilGorunumu='cover';});",
             "show the newly uploaded cover without reopening app")
        p=only(p,
            "'coverPhotoUrl':'','coverPhotoY':0.0,'updatedAt':FieldValue.serverTimestamp()",
            "'coverPhotoUrl':'','coverPhotoY':0.0,'profileViewMode':'coverless','updatedAt':FieldValue.serverTimestamp()",
            "explicit removal switches to coverless")
        p=only(p,"setState((){kapakUrl='';kapakY=0;});",
             "setState((){kapakUrl='';kapakY=0;profilGorunumu='coverless';});",
             "removed cover reflects chosen layout")
        return p
    return part(src,"class _ProfilPageState extends State<ProfilPage>",
                "\nclass _ProfilEtkilesimRozeti",edit)

def editor_cover(src):
    def edit(p):
        old="onPressed:_kaydediliyor?null:widget.onKapak,"
        new="""onPressed:_kaydediliyor?null:()async{
                      await widget.onKapak();
                      if(!mounted)return;
                      try{
                        final latest=await FirebaseFirestore.instance.collection('users')
                          .doc(widget.uid).get(const GetOptions(source:Source.server))
                          .timeout(const Duration(seconds:8));
                        if(!mounted)return;
                        final data=latest.data();
                        if((data?['coverPhotoUrl']??'').toString().isNotEmpty &&
                           data?['profileViewMode']=='cover'){
                          setState(()=>_gorunum='cover');
                        }
                      }catch(_){}
                    },"""
        return only(p,old,new,"editor cover button refresh")
    return part(src,"class _NgelXOnayliProfilDuzenlePageState",
                "\nclass ProfilPage extends StatefulWidget",edit)

def intro_player(src):
    def edit(p):
        start=p.index("  Future<void> _hazirla()async{")
        end=p.index("  @override void initState()",start)
        replacement="""  // Build462: finite initialization; error must never lock the player forever.
  Future<void> _hazirla()async{
    if(widget.url.trim().isEmpty||hazir||yukleniyor)return;
    final parsed=Uri.tryParse(widget.url.trim());
    if(parsed==null||parsed.scheme!='https'||parsed.host.isEmpty){
      if(mounted)setState(()=>hata=true);
      return;
    }
    setState((){yukleniyor=true;hata=false;});
    final eski=c;
    c=null;
    if(eski!=null){
      eski.removeListener(_videoDurumu);
      try{await eski.dispose().timeout(const Duration(seconds:4));}catch(_){}
    }
    if(!mounted)return;
    final player=VideoPlayerController.networkUrl(parsed);
    c=player;
    try{
      await player.initialize().timeout(const Duration(seconds:12));
      if(!mounted||!identical(c,player))return;
      await player.setLooping(false).timeout(const Duration(seconds:3));
      await player.setVolume(sessiz?0:1).timeout(const Duration(seconds:3));
      player.addListener(_videoDurumu);
      if(!mounted||!identical(c,player))return;
      setState((){hazir=true;kontrollerGorunur=false;});
      await player.play().timeout(const Duration(seconds:5));
    }catch(_){
      if(mounted&&identical(c,player)){
        setState((){hata=true;hazir=false;});
      }
      player.removeListener(_videoDurumu);
      try{await player.dispose().timeout(const Duration(seconds:4));}catch(_){}
      if(identical(c,player))c=null;
    }finally{
      if(mounted)setState(()=>yukleniyor=false);
    }
  }
  @override void didUpdateWidget(covariant ProfilTanitimVideoKarti oldWidget){
    super.didUpdateWidget(oldWidget);
    if(oldWidget.url==widget.url)return;
    final eski=c;
    c=null;
    if(eski!=null){
      eski.removeListener(_videoDurumu);
      unawaited(eski.dispose());
    }
    kontrolZamanlayici?.cancel();
    hazir=false;
    hata=false;
    yukleniyor=false;
    kontrollerGorunur=false;
  }
"""
        p=p[:start]+replacement+p[end:]
        p=only(p,
          "    if(!mounted||x==null||!x.value.isInitialized)return;",
          """    if(!mounted||x==null)return;
    if(x.value.hasError){
      WidgetsBinding.instance.addPostFrameCallback((_){
        if(mounted&&identical(c,x)&&!hata){
          setState((){hata=true;hazir=false;});
        }
      });
      return;
    }
    if(!x.value.isInitialized)return;""",
          "report asynchronous introduction player errors")
        old="""    if(hata)return Container(
      height:150,
      decoration:BoxDecoration(color:const Color(0xFFF1F2F4),borderRadius:BorderRadius.circular(18)),
      child:const Center(child:Icon(Icons.videocam_off_rounded,color:Colors.black38,size:38)),
    );"""
        new="""    if(hata)return InkWell(
      // Build462: users can restart a controller after any playable error.
      onTap:yukleniyor?null:()=>unawaited(_hazirla()),
      child:Container(
        height:150,
        decoration:BoxDecoration(color:const Color(0xFFF1F2F4),
          borderRadius:BorderRadius.circular(18)),
        child:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(Icons.refresh_rounded,color:Color(0xFF7C3AED),size:34),
          SizedBox(height:8),
          Text('Video açılamadı. Tekrar dene',
            style:TextStyle(color:Color(0xFF7C3AED),fontWeight:FontWeight.w700)),
        ])),
      ),
    );"""
        p=only(p,old,new,"real intro player retry affordance")
        return p
    return part(src,"class _ProfilTanitimVideoKartiState",
                "\nclass ",edit)

def feed_recovery(src):
    def edit(p):
        p=only(p,"  int _ngelx460KaynakIndex=0;",
            """  int _ngelx460KaynakIndex=0;
  int _ngelx462OtomatikDeneme=0; // Build462 one-shot alternate recovery""",
            "bound alternate source retry state")
        marker="  Future<void> _videoyuTekrarDene() async {"
        helper="""  void _ngelx462DigerKaynagiDene(){
    // Switch endpoint at most once automatically. An invalid/403 source
    // remains visible as an actionable error if the alternative also fails.
    if(!mounted||!widget.aktif||_ngelx462OtomatikDeneme>=1||
       _ngelx460MedyaAdaylari.length<2)return;
    _ngelx462OtomatikDeneme++;
    WidgetsBinding.instance.addPostFrameCallback((_){
      if(mounted&&widget.aktif&&!hazirlaniyor){
        unawaited(_videoyuTekrarDene());
      }
    });
  }

"""
        p=only(p,marker,helper+marker,"bounded feed alternative method")
        p=only(p,
           "        : ngelx461VideoHataKodu(e));",
           "        : ngelx461VideoHataKodu(e));\n      _ngelx462DigerKaynagiDene();",
           "failed feed initialization switches once")
        p=only(p,
           "          setState(()=>medyaHatasi=kod);",
           "          setState(()=>medyaHatasi=kod);\n          _ngelx462DigerKaynagiDene();",
           "async player error switches once")
        p=only(p,
           "setState(()=>medyaHatasi='V461-KARE: Video görüntüsü gelmedi.');",
           """setState(()=>medyaHatasi='V461-KARE: Video görüntüsü gelmedi.');
        _ngelx462DigerKaynagiDene();""",
           "first-frame stall switches once")
        return p
    return part(src,"class _VideoKartiState extends State<VideoKarti>",
                "\nclass ",edit)

def camera_recovery(s):
    s=only(s,
        "for(final preset in <ResolutionPreset>[_onizlemeKalitesi, ResolutionPreset.medium]){",
        """final denenecek=<ResolutionPreset>[_onizlemeKalitesi];
    if(_onizlemeKalitesi!=ResolutionPreset.medium){
      denenecek.add(ResolutionPreset.medium);
    }
    for(final preset in denenecek){""",
        "avoid duplicate medium-resolution camera reopen")
    s=only(s,
        "await denenen.initialize().timeout(const Duration(seconds:8));",
        "await denenen.initialize().timeout(const Duration(seconds:6));",
        "bounded preview initialize")
    for old,new in [
       ("await eski.dispose();","await eski.dispose().timeout(const Duration(seconds:3));"),
       ("await yeni.setFocusMode(FocusMode.auto);",
        "await yeni.setFocusMode(FocusMode.auto).timeout(const Duration(seconds:2));"),
       ("await yeni.setExposureMode(ExposureMode.auto);",
        "await yeni.setExposureMode(ExposureMode.auto).timeout(const Duration(seconds:2));"),
       ("await yeni.getMinExposureOffset();",
        "await yeni.getMinExposureOffset().timeout(const Duration(seconds:2));"),
       ("await yeni.getMaxExposureOffset();",
        "await yeni.getMaxExposureOffset().timeout(const Duration(seconds:2));"),
       ("await yeni.setExposureOffset((-0.35).clamp(minExp,maxExp).toDouble());",
        "await yeni.setExposureOffset((-0.35).clamp(minExp,maxExp).toDouble()).timeout(const Duration(seconds:2));"),
    ]:
       # Only patch camera-startup path; the caller can still retry manually.
       a=s.index("  Future<void> _onizlemeyiBaslat() async {")
       b=s.index("  Future<void> _kamerayiAcKapat",a)
       frag=s[a:b]
       if old not in frag:
          raise ValueError("Build462 camera startup anchor not found: "+old)
       frag=frag.replace(old,new,1)
       s=s[:a]+frag+s[b:]
    return s

def main():
    original_main=MAIN.read_text(encoding="utf-8")
    original_live=LIVE.read_text(encoding="utf-8")
    if "Build462 one-shot alternate recovery" in original_main:
        print("Build462 already applied.")
        return
    result=owner_cover(original_main)
    result=editor_cover(result)
    result=intro_player(result)
    result=feed_recovery(result)
    new_live=camera_recovery(original_live)
    # Preservation assertions: do not accidentally erase application features.
    for required in ["class VideoKarti","class _ProfilPageState",
                     "class ProfilTanitimVideoKarti","class _NgelXOnayliProfilDuzenlePageState",
                     "class _KullaniciProfilPageState","class "]:
        if required not in result:raise ValueError("Missing preserved app feature: "+required)
    for required in ["_onizlemeyiBaslat","_kamerayiAcKapat","_kameraAyarlari"]:
        if required not in new_live:raise ValueError("Missing preserved live camera feature: "+required)
    MAIN.write_text(result,encoding="utf-8")
    LIVE.write_text(new_live,encoding="utf-8")
    print("Build462 cover save sync, intro video retry, feed alternate recovery and camera bounds applied.")

if __name__=="__main__":
    main()
