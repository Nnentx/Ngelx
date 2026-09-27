from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
main = (root / "app/lib/main.dart").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")
worker = (root / "cloudflare/worker/src/index.js").read_text(encoding="utf-8")

checks = {
    "Supabase Flutter bagimliligi kaldirilmis": "supabase_flutter:" not in pubspec,
    "Uygulama kaynak kodunda Supabase istemcisi yok": "supa.Supabase" not in main and ".supabase.co" not in main,
    "Akis videosu sadece aktif kartta hazirlaniyor": bool(re.search(r"if\s*\(widget\.aktif\)\s*\{[\s\S]{0,220}unawaited\(_videoyuHazirla\(\)\)", main)),
    "Akis sesi sadece aktif kartta hazirlaniyor": "Trafik tasarrufu: komsu akis kartlarinda medya ve kullanici durumunu onceden indirme." in main and bool(re.search(r"if\s*\(widget\.aktif\)[\s\S]{0,260}unawaited\(_aktifSesiHazirla\(\)\)", main)),
    "Komsu akis karti medya ve durum verisini onceden indirmiyor": "Trafik tasarrufu: komsu akis kartlarinda medya ve kullanici durumunu onceden indirme." in main and "widget.aktif\n              ?PageView.builder" in main,
    "Like ve yorum sayaclari alt koleksiyonlari indirmiyor": "stream: ref.collection('comments').snapshots()" not in main and bool(re.search(r"class CanliSayacButonu[\s\S]{0,1800}final parent=ref\.parent;[\s\S]{0,1800}stream:parent\.snapshots\(\)", main)),
    "Akis meta bilgisi sadece aktif kartta dinleniyor": "required this.aktif" in main and "if (!aktif||icerikId.isEmpty) return const SizedBox.shrink();" in main,
    "Yanittaki kucuk video onizlemesi ag videosu acmiyor": "Yanittaki 46px video onizlemesi icin tum videoyu agdan acma." in main,
    "Grup videolari ilk dokunusta yukleniyor": "Sohbet acilir acilmaz her video icin veri indirme; ilk dokunusta baslat." in main,
    "Profil tanitim videosu tiklanmadan acilmiyor": "Tanıtım videosunu oynat" in main and "if(widget.url.isEmpty||hazir||yukleniyor)return;" in main,
    "Mesaj istegi onizlemesi 30 mesajla sinirli": bool(re.search(r"MesajIstegiOnizlemePage[\s\S]{0,2500}limitToLast\(30\)", main)),
    "Ozel sohbet fotograflari 1280px ile sinirli": bool(re.search(r"medyaGonder\(ImageSource kaynak\)[\s\S]{0,900}maxWidth:1280,[\s\S]{0,200}maxHeight:1280", main)),
    "Genel arama her harfte Firestore'u yeniden okumuyor": "Trafik tasarrufu: her harfte 60 kullanici + 100 icerigi yeniden indirme." in main and "future: _aramaVerisiniHazirla()," in main,
    "Hikaye yuzeyleri yalnizca story belgelerini sorguluyor": "collection('videos').where('type',isEqualTo:'story').limit(30).snapshots()" in main and "where('ownerId',isEqualTo:uid).where('type',isEqualTo:'story').limit(30).get()" in main,
    "Degistirilen profil videosu ve ozel sohbet arka plani temizleniyor": "final eski=tanitimVideoUrl;" in main and "ngelxMedyaSil(eski)" in main and "final eskiArkaPlan=(onceki.data()?['backgroundUrl_$me']??'').toString();" in main and "ngelxMedyaSil(eskiArkaPlan)" in main,
    "R2 byte range destegi aktif": "rangeHeader" in worker and "accept-ranges" in worker and "content-range" in worker,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + " - " + name)

if failed:
    raise SystemExit("V65 media traffic verification failed: " + ", ".join(failed))

print("V65 media traffic verification passed.")
