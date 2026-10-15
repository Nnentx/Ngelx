#!/usr/bin/env python3
"""Build460: preserve existing feed while trying alternate owned media endpoints.

No media is deleted, downloaded to CI or published. Candidate URLs are never
printed. Works after Build458 recovery and Build459 first-frame watchdog.
"""
from pathlib import Path
SOURCE=Path("app/lib/main.dart")

def exactly(s,old,new,label):
    c=s.count(old)
    if c!=1:raise ValueError(f"Build460 {label}: expected 1, found {c}")
    return s.replace(old,new,1)

def patch(s):
    if "// Build460 video fallback URLs" in s:return s
    a=s.index("class VideoKarti extends StatefulWidget")
    b=s.index("\nclass _VideoKartiState extends",a)
    widget=s[a:b]
    widget=exactly(widget,"  final String adres;",
                   "  final String adres;\n  final String alternatifAdres; // Build460 video fallback URLs",
                   "video alternate URL field")
    widget=exactly(widget,"    required this.adres,",
                   "    required this.adres,\n    this.alternatifAdres = '',",
                   "alternate constructor argument")
    s=s[:a]+widget+s[b:]
    for old,new in [
      ("adres:ngelx458VideoUrl(v['videoUrl'],v['mediaUrl']),",
       "adres:ngelx458VideoUrl(v['videoUrl'],v['mediaUrl']),\n      alternatifAdres:(v['mediaUrl']??'').toString(),"),
      ("adres:ngelx458VideoUrl(item['videoUrl'],item['mediaUrl']),",
       "adres:ngelx458VideoUrl(item['videoUrl'],item['mediaUrl']),\n                    alternatifAdres:(item['mediaUrl']??'').toString(),"),
    ]:
        s=exactly(s,old,new,"feed alternative URL input")

    a=s.index("class _VideoKartiState extends State<VideoKarti>")
    b=s.index("\nclass ",a+len("class _VideoKartiState"))
    player=s[a:b]
    player=exactly(player,"  String? medyaHatasi;",
      """  String? medyaHatasi;
  int _ngelx460KaynakIndex=0;

  List<String> get _ngelx460MedyaAdaylari {
    final urls=<String>[];
    for(final seed in <String>[widget.adres,widget.alternatifAdres]){
      final normalized=seed.trim();
      if(normalized.isEmpty)continue;
      for(final link in <String>[normalized,...ngelxMedyaUrlAdaylari(normalized)]){
        final uri=Uri.tryParse(link);
        if(uri==null||uri.scheme!='https'||uri.host.isEmpty)continue;
        if(!urls.contains(link))urls.add(link);
      }
    }
    return urls;
  }
""", "candidate algorithm")
    old="    final sonraki=VideoPlayerController.networkUrl(Uri.parse(widget.adres));"
    new="""    final candidates=_ngelx460MedyaAdaylari;
    if(candidates.isEmpty){
      if(mounted)setState(()=>medyaHatasi='Video bağlantısı bulunamadı.');
      return;
    }
    // A retry tries an alternate saved URL/owned media host instead of
    // looping forever on the same broken address.
    _ngelx460KaynakIndex=(_ngelx460KaynakIndex+1)%candidates.length;
    final sonraki=VideoPlayerController.networkUrl(
      Uri.parse(candidates[_ngelx460KaynakIndex]));"""
    player=exactly(player,old,new,"actual retry rotation")
    # The watchdog should catch a stalled controller even when it says "play".
    player=exactly(player,"if(!ilerledi && (durum.isBuffering||!durum.isPlaying||durum.hasError)){",
                        "if(!ilerledi){","watchdog progress check")
    s=s[:a]+player+s[b:]
    return s

def main():
    old=SOURCE.read_text(encoding="utf-8")
    new=patch(old)
    if new!=old:SOURCE.write_text(new,encoding="utf-8")
    print("Build460: fallback video URL candidates + 12s stalled-playback retry retained.")

if __name__=="__main__":main()
