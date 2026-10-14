# Build 454 — kişi isimleri yerine NgelX görünmesi

Tarih: 14 Ekim 2026, Europe/Istanbul.
Kanıt: 47210.jpg ve 47211.jpg, kullanıcı tarafından gönderilen ekranlar. 47212.jpg önceki test konuşması ekranıdır.

## Bildirim ve gözlem
Kullanıcı: kişilerin isimleri gözükmüyor, hepsinde NgelX yazıyor.
Gelen Kutusu / Mesajlar listesinde farklı avatarları olan birden fazla özel sohbetin başlığı NgelX. Aynı ekranda özlem engin ve Efsane Kaptan gibi gerçek isimler de görünüyor; dolayısıyla bütün satırların bozuk olduğu ekranla doğrulanmıyor.
Üst avatar şeridinde Selma, ADEM ve Ahsen isimleri okunabiliyor. Ahsen avatarı ile eşleşen sohbet satırında NgelX yazıyor.
Özel sohbet üst başlığında NgelX ve genel kişi avatarı görülüyor; listede görünen kişi avatarı ile başlığın profil bilgileri tutarlı değil.

## Beklenen davranış
Özel sohbet listesi ve sohbet üst başlığı karşıdaki kişinin doğru görünen adını ve profil fotoğrafını göstermeli. Yükleme sırasında marka adı kalıcı kişi adı gibi gösterilmemeli. Profil adı değişiklikleri ve hesap geçişleri doğru kişi bilgisine yansımalı.

## Toplu düzeltmede incelenecekler
Karşı taraf UID seçimi, profil ad alanlarının önceliği, eksik profil için varsayılan NgelX metni, profil önbelleğinin UID/hesap kapsamı ve hesap geçişinde abonelik temizliği. Bunlar araştırma başlıklarıdır; kök neden henüz doğrulanmadı.
Mevcut yapı korunacak. Bu aşamada kod değişikliği veya yeni APK yapılmadı.
