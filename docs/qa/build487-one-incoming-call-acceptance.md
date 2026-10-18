# Build 487 — Tek gelen arama ekranı / tek zil kabul testleri

Status: **Cihaz testi BEKLİYOR**. Build487 1.0.262/487 QA APK; üretim dağıtımı yok.
Reference: [#102](https://github.com/Nnentx/Ngelx/issues/102), [#72](https://github.com/Nnentx/Ngelx/issues/72), [PR #107](https://github.com/Nnentx/Ngelx/pull/107).

## Kod değişikliğinin sınırları

- Yeni Android CALL bildirimi / `IncomingCallActivity470` gelen aramanın tek ekranıdır.
- Bildirim izni verilmemiş Android'de eski Flutter gelen arama bandı yedek olarak korunur.
- Native `NotificationChannel` tek sesli zil sahibidir. Eski aynı-zamanlı manuel `RingtoneManager.sound.play()` çağrısı kaldırılmıştır. Kanal ID ve kullanıcı ses/titreşim/DND tercihleri korunur.
- Mevcut cevapla, reddet, iptal, 60 saniye zil süresi, aramaya dönme, LiveKit odası, sürüklenebilir mini pencere ve Firestore yetkilerine **dokunulmadı**.
- Mevcut Build484 üretim APK'sı ve ngelxsocial.com indirme sayfası değişmez.

## İki gerçek Android telefonda manuel QA (hepsi boş — henüz doğrulanmadı)

- [ ] Android 15 (3 tuşlu) ve Android 13/14+ (jest gezinme); aynı telefonda var ise her iki gezinme biçimini test et.
- [ ] Uygulama ön plandayken çağrı: **tek gelen arama ekranı**, eski Flutter üst bandı görünmesin.
- [ ] Ana ekran dışında sohbet/feed/profil açıkken çağrı: aynı tek arama arayüzü.
- [ ] Telefon kilitliyken gelen özel sesli, özel görüntülü, grup sesli ve grup görüntülü çağrı: doğru başlık ve uygun Android tam ekran/heads-up izin davranışı.
- [ ] Bildirim izni reddedildiyse Flutter yedek cevapla/reddet bandı uygulama ön plandayken görünür; iki ayrı yüzey ortaya çıkmaz.
- [ ] Aynı room için tek/tekrarlanan FCM ve Firestore tetikleyicileri: **tek sesli zil**; 60 sn ve arama sona erince tamamen dursun.
- [ ] Android kanal sessize alınmışsa sessizlik; zil modu sessiz/titreşim, DND ve ses seviyesi ayarları korunur.
- [ ] Yanıtla/reddet/arama iptal: başka oturum açılmaz, uygun Firestore callStatus güncellenir.
- [ ] Grup çağrısına geç katılan konuk ve iki cihazda hesap değişimi: eski hesap bildirimi görünmez.
- [ ] Android geri tuşuyla aktif aramayı küçült; arka plandaki **sürüklenebilir mini pencere** aynı çağrıyı gösterir, dokunup eski odaya döner; ses/video kesilmez.
- [ ] Arama sona erdiğinde mini pencere kaybolur; cihaz yönü, uygulama arka plan/ön plan ve tekrar giriş durumlarında oturum sızıntısı yok.
- [ ] Yanıt/red sistem ekranında Android alt navigasyon ile çakışmaz.

**QA kaydı:** cihaz modeli/Android sürümü, saat ve oda senaryosu; beklenen/gerçek sonuç; sadece gerekli hata ayıklama logları. Kullanıcı/oda/token gizli verilerini paylaşma.

## Sonraki ekran işi
Canlı yayın dikey 10 konuk / küçük + / çift dokunuş kalp ve kompakt profil tasarımı [#106](https://github.com/Nnentx/Ngelx/issues/106) altında ayrıca planlandı. Önce arama QA sonra canlı yayın uygulaması.
