# NgelX Build 415 — Cihaz videosu kalan görsel düzeltmeler (09.10.2026)

## Korunan Build 412–414 özellikleri

- Kapaklı/kapaksız görünüm tercihi, gerçek profil görselleri, hikâye, profil tanıtım videosu, arkadaşlık/takip isteği ve iptal işlemleri, mesaj açma, ortak gruplar, gönderi grid'i korunur.
- Firebase/Firestore güvenlik kuralları değiştirilmez; yeni sunucu sorgusu, yetki genişletmesi veya canlı veri migrasyonu yoktur.
- Build 395–414 geçmiş regresyon testleri, Build 415 özel sözleşme testi, Firebase emulator, Flutter analiz, APK imza doğrulaması aynı CI zincirinde çalıştırılır.

## Bu pakette kodlandı

1. Ziyaretçi profilindeki **Takip / Mesaj / Arkadaşlık / Ortak gruplar** dört buton yerine daha okunaklı iki satır (her satırda iki geniş düğme, 52px yükseklik). Tüm orijinal işlem callback'leri aynıdır.
2. Kapak kadrajı ekranındaki kesilen **Kapak fotoğrafını ayarla** başlığı **Kapağı ayarla** olur; mevcut kaydetme/konum ayarlama matematiği aynıdır.
3. Profil editörü mevcut kapak URL'sini ilk Firestore snapshot yüklenene dek gösterir; kapak fotoğrafı ağdan gelirken mor küçük yükleme göstergesi ve başarısızsa kırık görsel ikonu vardır. Gerçek kayıtta kapak boşsa fotoğraf tekrar diriltilmez.
4. Arkadaşlar sayfasında bir arama varken **3 Arkadaş** gibi toplamın filtre sonucuymuş gibi görünmesi yerine **Arkadaş · Arama sonuçları** gösterilir; arama boşsa gerçek toplam kalır.

## Canlı cihaz doğrulaması bekleyenler

- Adem/Sultan/Rojin hesapları arasında arkadaşlık/takip çift taraflı tutarlılık.
- Genel aramanın tüm kayıtlı/izinli kişileri göstermesi ve arama sonucunun doğru bağlamda açılması.
- Hikâye yanıtı ve özel sohbet karşı hesap teslimi; hikâye sayaçları.
- Kapak önizlemesi ağ kaynaklı gecikmeleri ve Android küçük ekran testi.
- Çift taraflı bildirimlerin cihaz üzerinde alınması, avatar cache, diğer görsel/sekme kusurları.

**Durum:** Kaynak kod düzenlendi; otomatik test sonuçları ve gerçek telefon QA olmadan tamamlandı işareti konulmaz.
