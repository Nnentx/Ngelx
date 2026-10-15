#!/usr/bin/env python3
"""Build458 bounded Akis video playback with a genuine controller retry.

Changes generated app/lib/main.dart after previous Build457 transforms only.
Does not mutate server/media records or upload/download user content.
"""
from pathlib import Path

SOURCE=Path("app/lib/main.dart")

def patch(s):
    if "// Build458 feed retry" in s:
        return s
    a=s.index("class _VideoKartiState extends State<VideoKarti>")
    b=s.index("\nclass ",a+len("class _VideoKartiState"))
    frag=s[a:b]

    def once(old,new,label):
        nonlocal frag
        if frag.count(old)!=1:
            raise ValueError(f"Build458 {label} anchor count {frag.count(old)}")
        frag=frag.replace(old,new,1)

    once("late final VideoPlayerController kontrol;",
         "late VideoPlayerController kontrol; // Build458 feed retry",
         "mutable recoverable controller")

    once("  Future<void> _videoyuHazirla() async {",
         """  Future<void> _videoyuTekrarDene() async {
    if(hazirlaniyor || !mounted)return;
    _otomatikKaydirmaIptal();
    final eski=kontrol;
    eski.removeListener(_kesimKontrol);
    final sonraki=VideoPlayerController.networkUrl(Uri.parse(widget.adres));
    kontrol=sonraki;
    sonraki.addListener(_kesimKontrol);
    if(mounted)setState(() {
      hazir=false;
      medyaHatasi=null;
      duraklatildi=false;
    });
    try{await eski.dispose().timeout(const Duration(seconds:4));}catch(_){}
    if(mounted && widget.aktif)await _videoyuHazirla();
  }

  Future<void> _videoyuHazirla() async {""",
         "retry controller method")

    once("await kontrol.initialize();",
         "await kontrol.initialize().timeout(const Duration(seconds:12));",
         "bounded video init")

    once("if(mounted)setState(()=>medyaHatasi=e.toString());",
         "if(mounted)setState(()=>medyaHatasi=e is TimeoutException ? 'Video yüklemesi zaman aşımına uğradı.' : 'Video oynatılamadı.');",
         "non-leaking error reason")

    once("if (medyaHatasi != null)\n            ngelxMedyaHataGorunumu(widget.adres)",
         """if (medyaHatasi != null)
            Stack(fit:StackFit.expand,children:[
              ngelxMedyaHataGorunumu(widget.adres),
              Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const SizedBox(height:56),
                OutlinedButton.icon(
                  onPressed:hazirlaniyor?null:()=>unawaited(_videoyuTekrarDene()),
                  icon:const Icon(Icons.refresh_rounded),
                  label:const Text('Videoyu yeniden dene'),
                  style:OutlinedButton.styleFrom(foregroundColor:Colors.white,
                    backgroundColor:Colors.black87),
                ),
              ])),
            ])""",
         "visible real retry")
    return s[:a]+frag+s[b:]

def main():
    before=SOURCE.read_text(encoding="utf-8")
    after=patch(before)
    if after!=before: SOURCE.write_text(after,encoding="utf-8")
    print("Build458: Akis video 12s timeout, error and true replay retry applied.")

if __name__=="__main__":
    main()
