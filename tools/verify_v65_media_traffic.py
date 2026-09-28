from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
main=(root/"app/lib/main.dart").read_text(encoding="utf-8")
pubspec=(root/"app/pubspec.yaml").read_text(encoding="utf-8")
worker=(root/"cloudflare/worker/src/index.js").read_text(encoding="utf-8")
checks={
"V72+ surumu":any(v in pubspec for v in ("version: 1.0.72+291", "version: 1.0.73+292", "version: 1.0.74+293", "version: 1.0.75+294", "version: 1.0.76+295", "version: 1.0.77+296", "version: 1.0.78+297")),
"Supabase Flutter yok":"supabase_flutter:" not in pubspec,
"Arama cache":"Trafik tasarrufu: her harfte 60 kullanici + 100 icerigi yeniden indirme." in main and "future: _aramaVerisiniHazirla()," in main,
"Foto lazy":"widget.aktif\n              ?PageView.builder" in main,
"Akis meta lazy":"if (!aktif||icerikId.isEmpty) return const SizedBox.shrink();" in main,
"Video lazy":"Future<void> _videoyuHazirla() async" in main and "if(widget.aktif&&!oldWidget.aktif)" in main,
"Muzik lazy":"if(widget.audioUrl.isEmpty||!widget.aktif||muzikOynatici!=null)return;" in main,
"Mesaj istegi 30":bool(re.search(r"MesajIstegiOnizlemePage[\s\S]{0,3000}limitToLast\(30\)",main)),
"Sohbet foto 1280":bool(re.search(r"medyaGonder\(ImageSource kaynak\)[\s\S]{0,1100}maxWidth:1280,[\s\S]{0,260}maxHeight:1280",main)),
"Grup video lazy":"Sohbet acilir acilmaz her video icin veri indirme; ilk dokunusta baslat." in main,
"Profil intro lazy":"Tanıtım videosunu oynat" in main,
"Hikaye filtre":"collection('videos').where('type',isEqualTo:'story').limit(30).snapshots()" in main,
"Medya temizleme":"ngelxMedyaSil(eskiArkaPlan)" in main and "ngelxMedyaSil(eski)" in main,
"R2 range":"rangeHeader" in worker and "accept-ranges" in worker and "content-range" in worker,
}
bad=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(("PASS" if v else "FAIL")+" - "+k)
if bad: raise SystemExit("V72 traffic verification failed: "+", ".join(bad))
print("V72 combined traffic verification passed.")
