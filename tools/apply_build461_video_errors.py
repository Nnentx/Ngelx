#!/usr/bin/env python3
"""Build461: classify video playback failures without leaking URLs or tokens.

After Build460 source transform, include async player errors in the UI rather
than leaving the first frame black. No Firestore/R2 writes or cloud deployment.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")


def one(s,old,new,label):
    count=s.count(old)
    if count!=1:raise ValueError(f"Build461 {label}: expected one anchor, got {count}")
    return s.replace(old,new,1)


def patch(s):
    if "// Build461 video error report" in s:return s
    a=s.index("class _VideoKartiState extends State<VideoKarti>")
    b=s.index("\nclass ",a+len("class _VideoKartiState"))
    player=s[a:b]
    helper="""// Build461 video error report: only non-sensitive categories are shown.
  // Never include signed URLs, personal IDs or raw platform exception strings.
String ngelx461VideoHataKodu(Object hata) {
    final t=hata.toString().toLowerCase();
    if(t.contains('403')||t.contains('unauthorized')||t.contains('permission')){
      return 'V461-403: Video erişim izni reddedildi.';
    }
    if(t.contains('404')||t.contains('not found')){
      return 'V461-404: Video dosyası bulunamadı.';
    }
    if(t.contains('codec')||t.contains('unsupported')||t.contains('format')){
      return 'V461-FORMAT: Video biçimi oynatılamıyor.';
    }
    if(t.contains('socket')||t.contains('host')||t.contains('network')||
        t.contains('timeout')||t.contains('source error')){
      return 'V461-AG: Video ağına erişilemiyor.';
    }
    return 'V461-PLAYER: Video açılamadı.';
  }

"""
    player=one(player,"  void _kesimKontrol(){",
      """"""  void _kesimKontrol(){
    // Errors may arrive after initialize() succeeded. Previous versions
    // ignored these listener errors, showing a black frame indefinitely.
    if(kontrol.value.hasError&&medyaHatasi==null&&mounted){
      final kod=ngelx461VideoHataKodu(
        kontrol.value.errorDescription??'unknown');
      WidgetsBinding.instance.addPostFrameCallback((_){
        if(mounted&&medyaHatasi==null)setState(()=>medyaHatasi=kod);
      });
      return;
    }""",
      "async playback error listener")

    old="""if(mounted)setState(()=>medyaHatasi=e is TimeoutException ? 'Video yüklemesi zaman aşımına uğradı.' : 'Video oynatılamadı.');"""
    new="""if(mounted)setState(()=>medyaHatasi=e is TimeoutException
        ? 'V461-SURE: Video yüklemesi zaman aşımı.'
        : _ngelx461VideoHataKodu(e));"""
    player=one(player,old,new,"typed video initialization error")
    player=one(player,"medyaHatasi='Video görüntüsü yüklenemedi.';",
               "medyaHatasi='V461-KARE: Video görüntüsü gelmedi.';",
               "first frame timeout category")
    result=s[:a]+player+s[b:]
    marker="class VideoKarti extends StatefulWidget"
    if result.count(marker)!=1:raise ValueError("Build461 video pure-category anchor")
    result=result.replace(marker,helper+marker,1)
    return result


def main():
    before=MAIN.read_text(encoding="utf-8")
    after=patch(before)
    if after!=before:MAIN.write_text(after,encoding="utf-8")
    print("Build461: classify video errors without URL/token logging; async player error visible.")


if __name__=="__main__":
    main()
