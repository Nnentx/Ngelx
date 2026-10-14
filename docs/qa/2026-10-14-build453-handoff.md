# NgelX Build 453 — birleşik düzeltme ve test kaydı

Tarih: 14 Ekim 2026 (Europe/Istanbul).
Android sürümü: 1.0.228 / 453.
Test edilen kaynak: `a556df09ea156e51e2838d4e84cbe859b29360c3`.
Derleme: https://github.com/Nnentx/Ngelx/actions/runs/38521285091

## Paketteki değişiklikler

- Canlı yayın yorum alanı klavye ve araç paneli değişirken odağını ve taslağını korur; gönderim sırasında yazılan yeni taslak silinmez.
- Yayıncı/izleyici alanları, daha kısa araç ve konuk panelleri; üst üste yükselen ve süre sonunda kaybolan, sayısı sınırlı kalpler.
- Konuk kabulü/çıkarılması ve yeniden bağlantı sırasında güncel sunucu erişim bilgisi ve izinleri kullanılır.
- Özel ve grup sohbetlerinde fotoğrafın oranı korunur; önizleme büyütülür ve ekran ölçüsüne göre bellek yükü sınırlandırılır.
- Gelen kutusundaki avatarlar, canlı/aktif alanı ve mesaj metinleri büyütülür; gereksiz profil abonelikleri ve canlı sorguları azaltılır.
- Arama bildirimi, çağrı kaydı tamamlandığında gönderilir. Tekrarlanan uyarılar mevcut zil bildirimini değiştirmez.
- Cihaz kayıt işlemi sürerken hesap değişirse yeni hesap için kayıt yeniden başlatılır. Bildirim anahtarı alma süresi 8 saniyeyle sınırlıdır. Başarısız kayıt için 30 saniye arayla en fazla iki ek tur denenir; ek turlar aynı hesabın açık ve uygulamanın ön planda olduğu durumda çalışır.
- Başarılı cihaz kaydı, bildirim ayarları tanılama hatasından bağımsızdır. Geçersiz cihaz anahtarları kaldırılır ve eksik kayıtlar başarılı bildirim teslimi sayılmaz.

## Doğrulama

- Kaynak uygulama aşamaları ve mevcut koruma kontrolleri CI'da geçti.
- Flutter analiz, canlı yorum/kalp, küçük ekran ve mevcut davranış testleri geçti.
- Sunucu token yetkilendirme ve Firestore kural testleri geçti.
- Güncel ücretsiz arama bildirim sunucusunun 23 testi yerel olarak geçti; dağıtım CI'da başarılı.
- Mevcut Android imza anahtarı, APK çıktısının imzası ve 1.0.228 / 453 sürümü doğrulandı. Derleme 38521285091 başarılı. İndirilen APK ayrıca SHA256 ile doğrulandı: `26bb70f762b36a98c2f995af0674e5970435f4fcdc816cfefa06a3446f0e973a` (147447625 bayt). Dosya kullanıcıya doğrudan teslim edildi. GitHub release oluşturma adımı HTTP 403 (Resource not accessible by integration) nedeniyle başarısız; bu, başarılı derleme çıktısını etkilemedi.

## Açık işler ve cihaz kabulü

1. Her iki test telefonuna da bu paketi kurup açın; bildirim izni ve zil sesi açık olmalı. Özel/grup aramasında uygulama açık, arka planda ve ekran kilitliyken zili doğrulayın. Kabul/ret sonrası zil durmalı, tekrar bildirim gelmemeli.
2. Hesap A'dan çıkıp B'ye girerken bildirim kaydı kesintiye uğramamalı. Geçici bağlantı hatasından sonra uygulamayı yeniden başlatmadan kayıt yenilenmeli.
3. İki telefonla konuk isteği, kabul, mikrofon/kamera, çıkarma ve bağlantı kesilip dönme davranışını doğrulayın. Gerçek ses/görüntü teslimi henüz doğrulanmadı.
4. Yayıncı/izleyici yorum alanını klavyeyle açıp kapatın; taslak, odak ve görünür yorum satırlarını kontrol edin. Hızlı kalp basımlarında kalpler çoğalıp kaybolmalı.
5. Özel/grup sohbetine yatay ve dikey fotoğraf gönderin; görüntü kırpılmadan okunabilir büyüklükte görünmeli.
6. Sayfa ve klavye gecikmesi gerçek cihazda ölçülmeli. Sorgu azaltmaları tek başına gecikmenin tamamen düzeldiğini kanıtlamaz.
7. Topluluk `posts` indeksi açık: COLLECTION kapsamında `status ASCENDING`, `createdAt DESCENDING`. Son indeks işlemi HTTP 403 ile başarısız; Firebase sahibi indeks oluşturmalı veya mevcut dağıtım hesabına indeks yönetim yetkisi vermeli. İndeks READY olarak doğrulanmadı.

Önceki tüm ürün kapsamı korunur. Otomatik test sonuçları fiziksel iki telefon testlerinin yerine geçmez.