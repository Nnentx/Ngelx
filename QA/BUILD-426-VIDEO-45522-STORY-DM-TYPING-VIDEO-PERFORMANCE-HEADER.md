# NgelX Build 426 — cihaz QA videosu 45522.mp4

**Kayıt zamanı:** 2026-10-09. **Dosya:** Kullanıcının bu konuşmada yüklediği `45522.mp4`. **Süre:** 55,54 saniye (1080×2392, HEVC, ~24,17 fps). **Kapsam:** Hikâye görüntüleme, yazılı yanıt, emoji tepki, klavye, özel sohbet, özel sohbetten hikâye açma, video oynatma ve hikâye başlığı.

## Kanıtlı gözlemler

1. **00:02–00:11 — hikâye emoji ve yazılı yanıtı.** Hikâye açık, ❤️ emoji tepkisi ve yazılı yanıt işlemleri başarı bildirimi gösteriyor. Önceki 45407/45490 “gönderilemedi” hatası bu örnekte görülmüyor. İşlem sırasında yanıtın beklemesi ve klavyenin ekranda kalması gözlemleniyor; kullanıcının yavaşlık şikâyeti dikkate alınmalı.
2. **00:16–00:25 — hikâyede uzun yanıt yazma.** Metin yazılırken ekrandaki video/fotoğraf ve klavye yeniden yerleşiyor; uzun metin oluşturma, öneri/emoji paneline geçiş ve mesaj gönderme gibi hızlı etkileşimlerde kullanıcı belirgin takılma bildirdi. Video karelerinden sürekli FPS ya da milisaniye düzeyinde giriş gecikmesi **kesin** ölçülemiyor. Bu alan öncelikli cihaz profil testi gerektiriyor.
3. **00:27–00:30 — özel sohbet ekranı.** Hikâyeye yazılan metin ve emoji tepkileri, hikâye resimli kartlar olarak özel sohbet içinde görünüyor. **Geçti / korunmalı:** Mesaj gönderme, görsel hikâye kartları, karşı hesap sohbetindeki görünüm.
4. **00:30–00:32, 00:36–00:39 ve 00:45–00:47 — sohbetten hikâye/video açma.** Sohbet içindeki hikâye kartına dokununca hikâye serisi açılıyor. Özellikle ~00:46'da siyah zemin ve “Video hazırlanıyor...” yüklemesi, ardından videonun görünmesi gözleniyor. **Geçti:** karttan hikâyeye geçiş; **geçmedi/performans:** geçiş ve video hazırlama sırasında hissedilir gecikme.
5. **Hikâye üst kontrolleri — “Takiptesin” düğmesi.** Fotoğraf/video hikâyesinin üstündeki kullanıcı adı ve avatar satırından aşağıda ayrı bir satırda duruyor ve içerik alanına doğru kayıyor. Kullanıcı, takip durumunun hikâyenin fotoğraf/video ortasına neredeyse yaklaşmasından rahatsız. **Düzelt:** Düğme üst başlıkla aynı bantta/dengeli hizada ve yeterli boşlukla durmalı; medyayı örtmemeli. Uzun kullanıcı adı (örn. @ASLANKARDEŞ) tek satırlı/ellipsis olarak korunmalı.
6. **00:32–00:54 — video oynatma ve sohbet geçişleri.** Oynatma sırasında arka arkaya hikâye/sohbet aç-kapat yapılınca gecikme hissediliyor. Video denetleyicisinin dispose/reinitialize ve ön yükleme akışları incelenmeli; bunların kesin kök neden olduğu **henüz kanıtlanmadı**.

## Öncelikli düzeltme gereksinimleri

- **Yüksek / Performans:** Hikâye yanıt girişindeki klavye gecikmesi, uzun mesaj yazımı ve emoji seçiminde gereksiz widget rebuild, hikâye oynatma denetleyici yükü ve senkron network beklentileri profillensin. Yazılı mesaj, emoji tepkisi, gönderim hata/başarı sinyalleri bozulmasın.
- **Yüksek / Video geçişi:** Özel sohbet hikâye kartından doğru hikâyeye dokunma -> oynatma zamanı, siyah ara ekran, tekrar açılışta video controller hazırlama ve medya önbelleği cihaz profili ile ölçülsün. Aynı video tekrar açıldığında gereksiz yüklemeyi azaltmayı değerlendir. Medya gizliliğini/expiry kontrollerini kaldırma.
- **Orta / Hikâye üst başlığı:** “Takiptesin” fotoğraf/video üzerine düşmeyecek; başlık alanında dengeli üst konumda olacak. “Takip Et / İstek gönderildi” diğer durumları da düzeni koruyacak.
- **Orta / Sohbet:** Mesaj yazma ve sohbetten hikâye açma sırasında gereksiz ekran kararması ve input gecikmesi ölçülsün. Kullanıcı özel sohbetin de yavaşladığını ayrıca bildirdi; video doğrudan özel sohbet klavyesinde uzun yazma testi içermediğinden otomatik “başarısız” ilan edilmemeli.

## Geçenleri koru

Build 425/426 hikâye yanıtlarının özel sohbete düşmesi, emoji tepkileri, hikâye kartına tıklayarak hikâyeyi açma, hikâye gönderim izinleri/mahremiyet kontrolleri, uzun kullanıcı adının tek satır olması.

**Durum:** Yalnızca test raporu kaydedildi. Bu rapor kendi başına kod değişikliği veya performans düzeltmesi yapmaz. Build 426 performans ve düğme yerleşimi için açık QA maddeleri olarak tutulmalı. Gerçek cihazda ölçerek tekrar doğrula.
