# NgelX Build 421 — Son üç görüntüleme düzeltmesi (09.10.2026)

## Amaç ve eski çalışan kodun korunması

Build 420 üzerinden devam edilir; Build 395–420 yamaları **aynı sırayla** uygulanır. Kapaklı profiller, gerçek fotoğraf değiştirme, mesaj, takip, arkadaşlık, gönderiler, hikâye yükleme/24 saat kuralı, hikâye oynatma ve Firestore güvenlik kuralları değişmez. Yalnızca aşağıdaki üç **görüntüleme** sorunu düzeltilir.

## Son üç düzeltme

1. **Kapaksız profil oranları:** Sahibin ortadaki avatarının üst bölümündeki 174×210 alanı 152×194 yapıldı; dekoratif daireler ve avatar yarıçapı uyumlu biçimde küçültüldü. Ziyaretçi kapaksız profilinde avatar bölgesi 182×230 yerine 156×205; başlık/biyografi boşlukları azaltıldı. Kamera, hikâye, arama, ayarlar ve diğer düğmeler aynen korunur. Kapaklı başlık oranları değiştirilmez.
2. **Katılım tarihi:** Ziyaretçinin kapaksız profilinde yalnız `NgelX’e katıldı: 2026` gösterilmesi kaldırılır; kapaklı profilde kullanılan, doğru ay ve yıl içeren `Eylül 2026 tarihinde katıldı` benzeri **aynı tarih metni** kullanılır. Profil sahibinin tarih biçimi de aynı kalır.
3. **Hikâye başlangıç/bitiş:** Hikâye izleyicisinde veritabanından zaten gelen `createdAt` ve `expiresAt` değerleri, kullanıcının yerel saatine dönüştürülüp tam tarih ve saatle gösterilir. Bitiş zamanı ve kalan saat/dakika, oynatma ilerlemesi devam ederken yenilenir. Tarih alanı yoksa gerçek olmayan saat uydurulmaz; bilinmediği açıkça belirtilir. İçeriklerin 24 saatlik son kullanma süreleri değiştirilmez.

## Telefonla doğrulanması gerekenler

- Adem, Rojin ve Sultan hesaplarının sahibi/ziyaretçi kapaksız profil üst düzeni, küçük ekranlarda avatar ve kamera tıklaması.
- Kapaklı profilin daha önce onaylanmış tasarımı, takip/arkadaşlık/mesaj eylemleri ve gönderi grid'i aynen kalmalı.
- Aynı hesapta kapaklı ve kapaksız ziyaretçi ekranlarının katılım tarihleri tam olarak aynı olmalı.
- Yeni foto/video hikâyesi: paylaşım saati, bitiş tarihi/saati, kalan zaman; tarih geçişi ve süresi dolmuş hikâye; hikâye oynatma ve mesaj yanıtı.
- Gerçek iki hesap arasında takip/arkadaşlık ve bildirim senkronizasyonu hâlâ cihaz testi gerektiriyor.

## Durum

Kod değişiklikleri Build 421 dalındadır. Kaynak kontrolleri ve Firebase emulator / Flutter analyze / imzalı APK otomasyonundan geçmeden **tamamlandı** sayılmaz; ayrıca cihaz testleri gerekiyor.
