# NgelX Build 402 — Profil referans düzeltmesi ve koruma planı

Kaynak: 2026-10-08 Build 401 gerçek cihaz video incelemesi (`docs/qa/2026-10-08-build401-cihaz-video-incelemesi.md`) ve kullanıcının paylaştığı Ben sayfası referans görseli.

## Bu sürümün hedefli değişiklikleri
1. Profil resmini bozmadan isim ve @kullanıcı adını avatarın sağına al; mevcut kapak fotoğrafı, kadraj ve kamera işlemlerini koru.
2. Dört gerçek zamanlı istatistik sayısını tek, açık mor, yuvarlatılmış ve üç dikey ayırıcılı kartla göster. Tıklama/yönlendirme yollarını değiştirme.
3. Arkadaş Ekle etiketini dar telefonda gizleme: buton boyutu, yazı ölçekleme ve minik ikon.
4. Kaydedilenler dahil profil kısayollarındaki metinleri gerektiğinde iki satır göster.
5. Profil tanıtım videosu alanını referanstaki sol metin + sağ gerçek video oynatıcı şeklinde düzenle. Var olan oynatıcı ve medya adresi korunur; olmayan videoya sahte içerik gösterilmez.
6. Gerçek öne çıkan video hikâyeler için video kapak küçük resmi kullan; kayıtlı başlık varsa göster, veri boşken açıklayıcı boş durum göster.
7. Alt orta Üret butonunu büyüt, mor-mavi gradienti koru, aynı navigasyon callback'ini kullan.
8. Kapak resmi ağdan tekrar çizilirken önceki görüntünün kalmasını destekleyen `gaplessPlayback` etkinleştirildi.

## Kesin koruma sözleşmesi
- Firebase giriş/oturum, Firestore profil verisi, R2 kapak yüklemesi `kind:'profiles'`, fotoğraf kadrajı ve kapak kaldırma koduna dokunma.
- Profil fotoğrafı, doğrulanmış hesap/premium durumu, arkadaş/ortak noktalar, hesap gizliliği, takip ve etkileşim sayaçlarını koru.
- Profil kaydetme, tanıtım videosu oynatma, hikâye yayınlama/izleme/arşivleme, Kaydedilenler/Etiketlenenler/Reels ve üç sütunlu gönderi grid akışını koru.
- Gelen Kutusu / grup arama / profil arama / kamera / Üret / Akış / yorum / beğeni gibi başka alanların backend mantığını değiştirme.
- Beş ana alt menü sekmesinin kendi yönlendirmeleri aynı kalır, yalnız Üret butonunun boyutu değişir.
- Referans ekranındaki örnek şehir/hesap/metin/fotoğraf verilerini kullanıcı hesabına koyma. Öne çıkanlar yalnız gerçekten işaretlenmiş hikâyelerden üretilir.

## Henüz tamamlandı sayılmayacak
- Build 402 kodu GitHub CI'da regresyon, Flutter analiz, imza ve APK derleme adımlarından geçmelidir.
- Gerçek cihazda avatar/isim hiza ve uzun ad taşmaları, 320/360/400 dp ekranlar, buton etiketleri, hikâye küçük resimleri, gerçek tanıtım videosunun oynatma kontrolü, orta Üret butonunun tıklanması yeniden denenmeli.
- Uygulama açılırken ağdan görsel geç yüklenmesi ve yorum paneli yükleme süreleri ölçümsüz şekilde tamamen çözüldü denmemeli.

## Kod/CI
- Kod düzeltmesi: `tools/apply_build402_profile_reference_polish.py`
- Koruma testi: `tools/check_build402_profile_regression.py`
- CI workflow: `.github/workflows/NgelX-BUILD-402-PROFILE-REFERENCE-POLISH.yml`
