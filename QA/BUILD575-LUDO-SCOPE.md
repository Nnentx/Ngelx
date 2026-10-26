# NgelX Ludo — Build 575 başlangıç paketi ve kalite sözleşmesi

## Temel kural
Build 574 (NgelX 1.0.344) ekran düzeni, Duyurular -> Ludo bağlantısı, 2/4 kişi, takım oyunu, makine, sohbet, davetler, Power, +1 konum yenilemesi ve ana uygulama ekranları değişmeyecek.
Yeni kod, testli Build574 paketinin üstüne `tools/apply_build575_ludo.py` ile uygulanır. Bu daldaki `app/lib/main.dart`, eski kaynak sürüm olduğundan doğrudan değiştirilmez.

## Başlanan ve kodlanan özellikler (henüz üretimde değil)
- Süre dolunca server tarafından otomatik moda geçiş; sonraki hamleler server'dan, geçerli zar ve taş kurallarından; akıllı rakip yeme / güvenli kare seçimi.
- Auto rozetine basılınca mod kapanır, yeni hamle süresi verilir. Manuel hamle de Auto'yu kapatır. Rakibin Auto'su değiştirilemez.
- Oyun ekranında küçük Auto düğmesi; izleyiciler için gizli. Mevcut dizilim, Power/kalkan/dice/davet paneli korunur.
- Üstte sunucudan gelen çip ve elmas bakiyesinde sayı değişim animasyonu.
- Premium taş atlası daha dolu kırpılır, yumuşak gölge eklenir, aynı karedeki taşlar ayrıştırılır.
- Sunucu doğrulamadan oyuncu galibiyet/mağlubiyet çip, XP, seviye ve galibiyet serisi güncellemesi. Ödüller kullanıcı başına/maç başına idempotent, Firestore CAS ile kaydedilir.
- Taslak oyun ekonomisi: gerçek oyuncuya karşı galibiyet +150 çip, +90 XP; makineye karşı galibiyet +35 çip, +35 XP; mağlubiyet +15 XP; her 200 XP seviye artışı. Bunlar ürün ekonomisi için ayarlanabilir değerlerdir, gerçek para değildir.

## Bu sürümde henüz **tamamlandı** denmeyecekler
1. Gerçek telefonda 320/360/393/440 genişliklerinde ekran görüntüsü kıyaslaması, taşların görsel onayı.
2. Gerçek reklam SDK'sı ve sağlayıcı sunucu doğrulamasıyla ödüllü video; yalnızca izleme sonucu/onaylandıysa çip verme, video kapatılınca asla vermeme.
3. Günlük hediye, kazanılan eşya sandığı, hediye/emoji gönderme ve hediye fiyatlarının gerçek hesaptan düşülmesi; tüm ödüller sunucu doğrulamalı.
4. Rövanş odası ve aynı oyunculara yeniden davet; canlı maçtan bağımsız.
5. Oyun içi ses aç/kapat ve zar/taş/ödül efektleri; var olan sohbet ve canlı ses kanalları korunmalı.
6. Wi-Fi kesintisi ve geri dönüş senaryoları, iki kullanıcı ve makine maçında çifte hareket/ödül kontrolleri.
7. Kazanma, rakip taşı yeme ve bonus toplama için daha zengin efektler, referans görsellerle kalite son rötuşları.
8. Backend server dağıtımı ve imzalı APK'nin Android gerçek cihazda testinden **sonra** `ngelx-web/android-update.json` sürüm güncellemesi.

## Yayın kapısı
`NgelX-BUILD575-LUDO.yml` yalnızca derleme/test amaçlıdır. Bulut oyun servisi güncellenmeden Build575'teki yeni Auto ve çip ödülü çalışmaz. CI testi + doğrulanan imza + gerçek cihaz testleri tamamlanmadan canlı güncelleme alanına sürüm kaydı açılmaz. Build574 mevcut kullanıcılar için yayınlanan sürüm olarak kalır.
