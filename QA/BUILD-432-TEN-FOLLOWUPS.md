# Build432 — yükleme regresyonu ve 10 ek madde

45651.mp4 cihaz testi Build431'in bildirim ve mesaj isteği kartında kalıcı yükleme gösterdiğini ortaya koydu. Build431 cihaz doğrulaması başarısızdır; CI başarısı bu sorunu yakalamamıştı.

Ana düzeltme: ortak Firestore sorgularına son snapshot/error sonucunu yeni dinleyicilere aktaran, tek upstream dinleyici kullanan ve ekran kapanınca kapanan cache eklendi. İlk sonuç 15 saniyede gelmezse hata görünür; yenileme yeniden bağlanır. Bir sorguya sonradan eklenen anahtarlı StreamBuilder testi bu cihaz senaryosunu tekrar üretir.

|46 listesindeki no|Bu paketle yapılan ek değişiklik|
|---|---|
|6|Mesaj istekleri ekranı kalıcı kullanıcı/sohbet stream'i; açıklamalı boş durum, yerinde yenileme/hata düğmesi.|
|10|Sayaç, liste ve mesaj isteği kartı tek 200-kayıt sohbet sorgusunu paylaşır. Kullanıcı get hataları cache'ten çıkar; 12 saniye sınırı var.|
|12|Hikâye videosu ilk hazırlığı 12 yerine 30 saniye; devam eden ön yükleme beklenir. Hikâye kayıt sorgusu 15 saniye sınırlandırıldı.|
|13|Video hata dinleyicisi ve 20 saniyelik buffering sınırı; başarısız controller kapanır, mevcut Tekrar dene görünür. Buffering sırasında hikâye ilerlemesi durur.|
|18|Aynı sonraki video halen hazırlanırken yeni controller kurulmaz; sonraki hikâyeye geçiş o hazırlığı kullanır.|
|25|Profil araması 220ms debounce; retained stream, hata/yenileme ve ekran kapanışında iptal.|
|26|Arşiv stateful retained stream; ilk sonuç zaman aşımı ve aynı ekranda retry. Her rebuild'de sorgu oluşturulmaz.|
|28|Arşiv/arama owner, deleted/isDeleted/removed ve hiddenFor filtreleri; silinen yerel ID de hariç. Kaydedilmemiş expired hikâye arşiv sayılmaz.|
|29|Ziyaretçi profilinin birleşik kullanıcı yüklemesi rebuild'lerde korunur; işlem, UID veya oturum değişiminde temizlenir. Hata ekranı ve retry eklendi.|
|45|Profil arama ve arşiv yerel silme revizyonunu dinler; eski Firestore snapshot'ı varken de silinen içerik hemen gizlenir. Arşiv star update silinmiş belgeyi yeniden yaratmaz. Mesaj medyası cache temizliği bu maddede hâlâ açık.|

Kod ve otomatik test hedefleri bunlardır. Gerçek telefon performansı ve tüm 46 maddenin tamamlanması iddia edilmez. Story DM teslimi, profil zili, request transaction ve sahiplik doğrulamalı medya silme korunur. Firestore erişim kuralları değiştirilmez.

Doğrulama: kaynak zinciri + kaynak koruma kontrolleri, Flutter analizi, eski 12 davranış testi + 6 yeni test, Firestore emulator ve imzalı APK. Flutter analizi, 18 davranış testi ve Firestore emulator testleri Actions 38047626631 içinde geçti. İmzalı APK üretimi ve v2 imza doğrulaması geçti. İş akışı başarılı: https://github.com/Nnentx/Ngelx/actions/runs/38047626631 . Sürüm 1.0.207+432. APK dosyası NgelX-Build432.apk; 145052542 bayt. APK SHA256: 67b3388ce626f190602100d5cc2886da1b07ece9dca83eedf79d49e9f840b64d. Artifact ZIP SHA256: 5294f07722993c552cc1975844f6b41f0c1a040e36a333575a66b59f4645e6a7. İndirilen ZIP ve APK hash değerleri doğrulandı. Telefon testi bekleniyor.
