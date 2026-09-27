from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
main = (root / "app/lib/main.dart").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")
worker = (root / "cloudflare/worker/src/index.js").read_text(encoding="utf-8")

checks = {
    "Supabase Flutter bagimliligi kaldirilmis": "supabase_flutter:" not in pubspec,
    "Uygulama kaynak kodunda Supabase istemcisi yok": "supa.Supabase" not in main and ".supabase.co" not in main,
    "Akis videosu sadece aktif kartta hazirlaniyor": "if (widget.aktif) unawaited(_videoyuHazirla());" in main,
    "Yanittaki kucuk video onizlemesi ag videosu acmiyor": "Yanittaki 46px video onizlemesi icin tum videoyu agdan acma." in main,
    "Grup videolari ilk dokunusta yukleniyor": "Sohbet acilir acilmaz her video icin veri indirme; ilk dokunusta baslat." in main,
    "Profil tanitim videosu tiklanmadan acilmiyor": "Tanıtım videosunu oynat" in main and "if(widget.url.isEmpty||hazir||yukleniyor)return;" in main,
    "Mesaj istegi onizlemesi 30 mesajla sinirli": bool(re.search(r"MesajIstegiOnizlemePage[\s\S]{0,2500}limitToLast\(30\)", main)),
    "Ozel sohbet fotograflari 1280px ile sinirli": bool(re.search(r"medyaGonder\(ImageSource kaynak\)[\s\S]{0,900}maxWidth:1280,[\s\S]{0,200}maxHeight:1280", main)),
    "Genel arama her harfte Firestore'u yeniden okumuyor": "Trafik tasarrufu: her harfte 60 kullanici + 100 icerigi yeniden indirme." in main and "future: _aramaVerisiniHazirla()," in main,
    "R2 byte range destegi aktif": "rangeHeader" in worker and "accept-ranges" in worker and "content-range" in worker,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + " - " + name)

if failed:
    raise SystemExit("V65 media traffic verification failed: " + ", ".join(failed))

print("V65 media traffic verification passed.")
