# NgelX Build 406 — Son 8 Hata Tek Paket

- Kaynak: Build 405 tek telefon video kayıtları (45115.mp4, 45117.mp4, 45121.mp4), gelen kutusu bildirimi (45118.jpg), davet ekranları (45119.jpg, 45120.jpg), `QA/BUILD-405-FINAL-SINGLE-DEVICE-SCOPE.md`.
- Branch: `work/build-406-final-eight-fixes`.
- Build hedefi: **1.0.182+406**.
- Kod uygulama yöntemi: önce mevcut 395–405 CI yamaları, ardından `tools/apply_build406_final_eight.py`. Yeni APK kaynakları çalışma dalındaki uygulama dosyalarında doğrudan değil, doğrulanan CI çalışma kopyasında oluşturulur.

## Sekiz başlık — kod işi

1. **P1 Canlı Yayın / son özeti:** `_CanliOzetSatiri` etiket ve değerlerinin siyah yazı renklere sahip olmasını sağla. Build 405'teki tek kalıcı özet katmanı, onay ve Keşfet'e dönüş değişmeyecek.
2. **P1 Gelen Kutusu / Bildirimler:** Gerçek `fromUid` ile kişiyi Firestore'dan çöz; görünen ad veya kullanıcı adını, gerçek profil resmini kullan. Var olan gönderici bilgisi yoksa belirsiz/kayıp hesap yedeği göster. Eski istek metinlerine isim ekle; tekrar eden isim yazma. Kabul/ret, bildirim zamanı ve okundu durumu aynı.
3. **P2 Gruplar / Davet:** Geçerli, hala aktif grup koduyla `Gruba katıl` doğrudan `autojoin` olacak. `joinApproval` gerçek davet bağlantısında bekleme zorunluluğu olmayacak. Firestore `validInvite`, geçerli chat code, revoked/active/expiresAt, 60 kişi sınırı ve banned listesi korunacak. Açık keşif onaylı katılım yolu değişmeyecek. Bu işlem Firebase kurallarının canlı ortama yayınlanmasını da gerektirir.
4. **P2 Profil / tanıtım videosu:** URL değişince `ValueKey(url)` ile eski oynatıcı/kapak controller'ını düşür ve gerçek yeni player oluştur. Başarılı upload bildirimi, dosya, `mm:ss` süre ve geri dönüş korunacak.
5. **P2 Profil / avatar & kapak:** Mevcut URL için tekrar tekrar yeni provider nesneleri yerine profil kapsamlı kararlı provider cache kullan. Yeni URL olunca yenisi çözülür. Kalıcı yükleme kusuru ölçülmeden tamamen bitti denmez.
6. **P2 Akış / medya geçişi:** Medya önizleme yuvalarında koyu boş ekran yerine açıklayıcı/video önizleme durumu kullan. Bu görsel iyileştirme, tüm ağ/decoder kaynaklı tam ekran Akış siyah spinner gecikmelerini tek başına giderdiğini kanıtlamaz; tek cihazda ayrı smoke gerekir.
7. **P3 Kaydedilenler:** Profil kısayol genişliğini artır, kısa etikette tek satırlı orantılı yazı kullan. Gerçek Kaydedilenler içeriği/kayıt kaldırma işleyicileri değişmeyecek.
8. **P3 Gizlilik:** `Gizli hesap` + `Profilimi kimler görüntüleyebilir?` izinlerinin birlikte nasıl etkili olduğunu açıkla, stored privacy ayarlarını değiştirme.

## Güvenlik, regresyon ve teslim
- Python koruma kontrolleri: 399–406, `tools/check_build406_regression.py`.
- Firebase Firestore emulator birim testleri: `tools/firestore_rules_test.mjs` içinde onaylı grupta geçerli aktif linkle `autojoin` mümkün olmalı; yalnız `pending` kendi kendine üyelik yaratamaz.
- APK: Flutter analyze + imzalı release + sha256 + artifact (önceki paket kimliğini ve çalışan işlevleri koru).
- Firebase üretim kurallarını **yalnız yukarıdaki testler ve başarılı APK CI sonucundan sonra** ayrı `deploy-rules` job'uyla uygula; servis kimliği yoksa iş başarısız olduğu açıkça bildirilecek.
- **İkinci telefon/iki hesap gerçek bağlantı testleri isteğe bağlı beklemede**: live ses, karşı izleyici/yorum, sesli oda, PK, davet teslimi. Başarılı diye işaretlenmez.
- **Gerçek cihaz kontrolü gerekli**: Canlı özet metin/sayı, gelen kutusu gerçek gönderen, profil yeni video & Kaydedilenler, geçerli davet linki. Kod/CI başarısı cihaz uçtan uca onayı değildir.

## Durum
Başlangıç kaydı: Kod yaması ve otomasyon pipeline'ı oluşturuldu, CI sonuçları takip ediliyor. Derleme başarılı olmadan hiçbir maddeye telefonda tamamlandı statüsü verilmeyecek.
