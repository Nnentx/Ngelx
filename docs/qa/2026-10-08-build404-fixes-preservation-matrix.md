# NgelX Build 404 — Konsolide Profil / Sesli Oda / Canlı Yayın düzeltmeleri

**Talep:** 2026-10-08 videolarında not edilen eksikleri, çalışan işleri bozmadan tek pakette kodla.
**Kaynak notlar:** `docs/qa/2026-10-08-build403-profil-gercek-cihaz-video-incelemesi.md`, `docs/qa/2026-10-08-build403-sesli-odalar-telefon-video-incelemesi.md`, önceki Build 402 Canlı Yayın/Sesli kaydı.

## Build 404 kod değişiklikleri

| Bölüm | Hedefli düzeltme | Korunan sözleşme |
| --- | --- | --- |
| Sesli oda kategorileri | Seçili/seçili değil ChoiceChip için sistem temasından bağımsız açık arka plan, mor seçili vurgu ve okunur koyu yazı | Gerçek oda başlığı, kategori kodları, oda başlatma, gizlilik değerleri |
| Sesli oda ekranı | Ayrı sarı `2. kişi bekleniyor` bandını kaldır; aynı durumu konuşmacı sayacının yanında kısa, anlaşılır satırda göster | 12 sahne kapasitesi, konuşmacı rolü, mikrofon, oda mini barı, bitirme |
| Söz istekleri | Sorgu hata durumunda `Yeniden dene`; Build 403'teki 7 saniye gecikme uyarısı + boş durum korunur | Firestore speaker_requests, gerçek kabul/red, karşı kullanıcı izinleri |
| Canlı kamera | İlk açılış ve kamera değişiminde `Kamera hazırlanıyor...` açıklaması; var olan donmuş kare önizlemesi korunur | Ön/arka kamera, flaş, izinler, yayın başlat/bitir, kalite, 3-2-1 |
| Canlı yayın araçları | Filtre preset chip'lerine okunur açık arka plan, mor vurgulu seçim | Gerçek zamanlı görüntü ayarları, PK, yorum, LiveKit yayın |
| Profil video | Gerçek player 15 saniye içinde hazırlanmazsa hatayı gösterip yeniden deneme imkânı ver; loading durumuna açıklama | Gerçek video URL, oyuncu kontrolleri, süre ve profil düzenleme |
| Kaydedilenler | İlk kare hesaplanırken açıklayıcı yükleme metni; Build 403'teki 12 saniye timeout + yeniden dene korundu | Gerçek Kaydedilenler belgeleri; asıl videoyu silme yok |
| Premium | Yalnız Premium ve Cüzdan satırının mavi olması değişmedi | Diğer ayarlar ve satın alma işleyicileri |

## Tamamlanmış sayılmayan bağımlılıklar / ayrıca doğrulanacaklar
- **İki hesap/cihaz canlı testi:** Yayının keşfedilmesi, izleyici sayısı, gerçek ses/görüntü, karşı cihazda davet/yorum teslimi; yalnız statik kod analiziyle mümkün değil.
- **İki hesap/cihaz sesli test:** Oda açıkken başka kullanıcının Keşfet'te görmesi, katılması, söz istemesi, yönetici onay/ret ve iki yönde mikrofon / oda müziği duyulması.
- **Yavaş/bozuk video kaynağı:** Gri görselleri süresiz bekletmek yerine durum gösterildi; gerçek CDN, video thumbnail üretimi ve ağ süreleri ölçülmeden bütün gecikmeler çözüldü denmez.
- **Akış video player siyah kare:** Canlı/sesli oda açıkken geçişin kaynak ağ gecikmesi, decoder ve bellekle ilişkisi ölçülmeli. Bu pakette medya engine/realtime protocol değiştirilmedi.
- **Canlı yayın referans tasarımının tüm ayrıntıları:** Filtre kontrastı ve kamera durumları düzeltildi, tüm yayın ekranı baştan tasarlanmadı.
- **Sürüm**: 1.0.180+404; ancak dosya GitHub Actions başarıyla üretmeden APK hazır sayılmaz.

## Kabul kriterleri
Build 399→404 regresyon kapıları → flutter analyze → imzalı release APK → artifact checksum → Android telefonda kullanıcı videosu. Profil/kaydedilenler ve canlı/sesli işlevler baştan sona cihazda denenmeden "tamamı sorunsuz" demeyin.

**Değişikliklerin uygulama kodu doğrudan depoda değil**, CI tarafından sırasıyla uygulanan `tools/apply_build404_profile_live_voice_fixes.py` betiğinde olduğu unutulmasın; önceki 395–403 yamaları her build'de korunur.
