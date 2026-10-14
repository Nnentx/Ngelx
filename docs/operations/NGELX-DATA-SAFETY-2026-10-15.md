# NgelX veri güvenliği ve kurtarma kontrol kaydı — 15 Ekim 2026

## Durum: KORUMA MODU (henüz tam yedek doğrulanmadı)
- Üretim Firestore ve Cloudflare R2 verilerine bu inceleme sırasında erişilmedi; yeni veri silme, üretim kuralı dağıtımı veya APK build'i yapılmadı.
- Ana dalda `.github/workflows/NgelX-APPROVED-DAILY-RETENTION.yml` zamanlanmış tetikleyicisi kaldırıldı ve `retention` işi `if: ${{ false }}` ile kapatıldı. Değişiklik commit'i: `ad7978108835bfcaba50c6b3a436fabec15be8e6`.
- Bu durdurma **yalnız GitHub Actions'daki günlük işi** kapsar. Daha önce dağıtılmış Firebase Functions/Cloudflare Worker, R2 lifecycle kuralları veya telefon uygulamasında çalışan silme fonksiyonlarının durumunu kanıtlamaz.
- Build 457 test APK'sı ayrı `work/build-457-device-recovery` dalında başarılı koşudan çıktı; canlı Firebase kuralları bu CI koşusunda dağıtılmadı.

## 14 Ekim 2026 günlük temizlik kaydı
- GitHub Actions `38574620026`: 330 Firestore kaydı tarandı; 85 veritabanı kaydı silindi, 11 medya içeren mesaj temizleme sürecine alındı (`queued`), 2 kayıt değişim nedeniyle korunmuş görünüyor.
- R2 arka uç medya temizliği `read budget` sınırına takılıp durdu. Bu log **bu koşunun başarıyla nesne sildiğini göstermiyor**; farklı bir yerde silme gerçekleşmediği sonucunu da çıkaramayız.
- Değişiklikleri kullanıcılara ait özel veriler olmadan yalnız toplu sayımlarla raporla. Hangi kayıtların silindiği ve geri yüklenebilirlik üretim erişimi ve yedek geçmişiyle doğrulanmalıdır.
- `tools/retention437_cleanup.py` mantığı eski sohbet mesajları için 14 gün eşiği ve seçili bildirim, arama geçmişi ve talep durumları için başka eşikler içerir. Süresi doldu diye otomatik olarak tekrar çalıştırma.

## Devreye alma kilidi
1. Otomatik silmeyi ve medya objesi kalıcı silmelerini, aşağıdaki yedek/doğrulama tamamlanana kadar tekrar açma.
2. Yalnız kuru çalıştırma (read-only preview) gerçekleştir; `--apply`, `firebase deploy`, `r2 object delete` veya `gcloud firestore import` çalıştırma.
3. Yetkili kullanıcının talep ettiği hesap/içerik silme ve hukuki saklama süreleri ayrı iş akışı olarak ele alınmalı; bu operasyonel durdurma böyle taleplerin mevzuata uygun işlenmesini kalıcı olarak iptal etmek için kullanılmamalıdır.

## Firebase Firestore geri yükleme kontrolü
- Gerçek proje: `ngelx-44eed`. Firebase/Google Cloud yönetici erişimi gereklidir; `google-services.json` bunun yerine geçmez.
- Google Cloud Console'da Firestore Databases -> Scheduled backups altında etkin plan ve elde bulunan gerçek yedekler kontrol edilmeli. Başarılı **tamamlanmış** yedek adı, oluşturulma zamanı, veritabanı ve saklama süresi kaydedilmeli.
- Firestore zamanlanmış yedekleme planını ilk kez etkinleştirmek ya da değiştirmek ücretli Blaze planı ve uygun IAM yetkisi gerektirir; ücret ve saklama süresi proje sahibince kontrol edilmeli.
- Yerinde overwrite/geri yükleme yapma. Önce **ayrı bir test veritabanına** geri yükle; sayım, belge yapısı, referans bütünlüğü ve bir iki kayıt üzerinden denetle. Gerçek kullanıcı verilerini public GitHub/CI artefaktına koyma.
- Kaynak: https://firebase.google.com/docs/firestore/backups

## R2 medya güvenliği
- `ngelx-media` kovasının object lifecycle kurallarını, erişim kontrolünü, varsa ayrı medya yedeğini ve silme günlüklerini incele.
- Firestore yedekleri R2 fotoğraf/video nesnelerini içermez; ayrı geri kazanım planı zorunludur.
- Object Lock / bucket lock yanlış yapılandırılırsa kullanıcının geçerli silme talepleri ile çatışabilir; yalnız kapsamı ve süreleri doğrulanan prefix'lerde kullan. Tek başına kopya yedek sayılmaz.
- Mevcut R2 envanterinin sayımını ve değişmeyen nesne örneklerinin ETag/hash doğrulamasını yap. Farklı koruma alanında ikinci kopya ve test geri yükleme olmadan "medya yedeklendi" deme.
- Kaynaklar:
  - https://developers.cloudflare.com/r2/buckets/object-lifecycles/
  - https://developers.cloudflare.com/r2/buckets/bucket-locks/

## 85 silinen kayıt / 11 medya kuyruğu araştırması
- Zaman aralığı: 14 Ekim 2026, ilgili günlük GitHub Action.
- Yalnız yönetici erişimiyle `_retention437_cursors`, mesajlardaki `retentionExpired`, `mediaCleanupState` ve varsa kalıcı medya iş kayıtlarını salt okunur incele.
- `queued=11` kesin olarak 11 R2 dosyasının silindiği anlamına gelmez.
- Önce mevcut yedeklerden restore seçeneğini doğrula; canlı Firestore'a doğrudan kayıp kayıt yazma. Restorasyon öncesi veri tutarlılığı ve kullanıcı/erişim etkilerini değerlendir.

## Yeniden otomatik temizliğe dönme koşulları
- [ ] Firestore son başarılı yedeği ve geri yükleme testi kanıtlandı.
- [ ] Cloudflare R2 ayrı kopyası ve en az bir nesne geri yükleme testi kanıtlandı.
- [ ] Üretim Firebase/Worker/R2 silme tetikleyicileri envanteri çıkarıldı.
- [ ] 85 kayıt ve 11 kuyruktaki medyanın durumları sınıflandırıldı.
- [ ] Bekleyen veri silme talepleri ile mevzuata uygun saklama politikası tasarlandı.
- [ ] Silme kuralının sadece doğru verileri etkileyeceği test edildi; proje sahibi yeniden etkinleştirmeyi açıkça onayladı.

Bu doküman bir **hazırlık/kayıt dosyasıdır**, gerçek yedek alındığının kanıtı değildir.
