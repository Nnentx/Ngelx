# Build 426 — 45504.mp4 / 45509.jpg: Hikâye bağlantıları ve kullanıcı adı

**Tarih:** 2026-10-09. Kaynak kanıt: sohbet ekranı `45509.jpg`; önceki test videosu `45504.mp4` (~59 sn).

## Gözlemler
- **Geçti, korunacak:** Build 425 hikâye yanıtı ve emoji tepkisi gönderebiliyor. 45504 videosunun sonlarında "Yanıtın gönderildi", "Tepkin gönderildi" ve karşı özel sohbet ekranında hikâyeye referanslı mesaj kartları görülüyor. Sadece karşı sohbetin ekranda görülmesi, uzun dönem teslim güvencesi değildir.
- **Yeni istek:** Özel sohbetteki resimli `Hikâye yanıtı` ve `Hikâye tepkisi` kartlarına dokununca ilgili hikâye açılmalı. Şu an `story_reply` türü için `onTap` tanımlı değil.
- **Görsel hata:** 45504 videosunda hikâye üst şeridindeki `@ASLANKARDEŞ` ismi dar sütunda iki satıra bölünüyor. Yanındaki Takiptesin/ses/menü/kapat düğmeleri kullanılabilir yatay alanı tüketiyor. İsim tek satırda, uzunluk yetmezse `...` ile gösterilmeli; işlem düğmeleri ikinci satırda olmalı.
- **Performans gözlemi:** Önceki kullanıcının mesajına göre sohbet ve hikâye yanıtında gecikme var; ağ süresi kesin ölçülmedi.

## Kod düzeltmesi
1. `_SohbetPageState` içindeki `story_reply` balonuna özel tıklama eylemi; Firestore'dan ilgili videonun `ownerId`, `storyId`, bitiş süresi kontrolüyle `NgelXHikayeSeriPage(initialStoryId)` açılır. Süresi dolmuş/silinmişse açıklayıcı mesaj gösterilir.
2. `story_v66.dart` hikâye serisi üst şeridinde tek satır/ellipsis kullanıcı adı ve ikinci satıra alınmış aksiyonlar.
3. Zaten cihazda açılmış aktif hikâye snapshot'ını yanıt sahibini doğrulamak için kullanma; gereksiz ikinci video belgesi GET isteği kaldırıldı, engel/mesaj izinleri değişmedi.
4. Mesaj kaydı başarılı olduktan sonraki sohbet önizleme güncellemesi arka planda çalışır; 8 sn timeout yüzünden gönderildi sinyalinin bekletilmesi önlenir.
5. Statik regresyon, Firebase emülatör testleri, Flutter analiz ve APK derleme CI.

## Cihaz QA bekleyen
- İki kullanıcıya ait hikâye yanıtı ve emoji kartlarından açılış; doğru hikâyeye, doğru sahibine gitmesi.
- Süresi dolmuş/silinmiş hikâye kartında düzgün uyarı ve gizlilik.
- Uzun `@ASLANKARDEŞ` başlığının foto ve video hikâyelerinde tek satırda görünmesi.
- Özel sohbet açılış süresi ve hikâyeye yanıt toplam süresi telefon üzerinde önce/sonra ölçülmeli. Bu kod değişikliği tüm mesaj açılışı gecikmesini kanıtlanmış şekilde düzeltmez.
- Çalışan hikâye yanıtı teslimi ve emoji tepkileri bozulmamalı.

**Not:** Work test kaydı ve kod değişiklikleri GitHub'da tutuluyor; telefon testi bitmeden tüm sorunlar kapandı denmemeli.
