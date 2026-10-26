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
- Taslak oyun ekonomisi: gerçek oyuncuya karşı ilk galibiyet +150 çip, +90 XP; makineye karşı ilk galibiyet +35 çip, +35 XP; galibiyet serisi için gerçek oyuncu maçında +20'şer çip (en fazla +100), bot maçında +10'ar çip (en fazla +50). Mağlubiyet +15 XP, her 200 XP seviye artışı. Sunucudaki miktarlar ürün ekonomisine göre ayarlanabilir; gerçek para değildir.

## Sonraki kod eklemeleri (GitHub PR #190 taslak, henüz üretimde değil)
- Günlük hediye: her UTC gününde bir kez, sunucuda CAS ile çip bakiyesi artar ve seri tutulur.
- Ödül sandığı: sekiz saatlik sunucu bekleme süresi, çip ve XP ödülü, çifte tahsilat engeli.
- "Puanlarım": kullanıcıya özel okunur bakiyeler; çip, elmas, XP, seviye, maç/galibiyet/mağlubiyet ve seri. Başkasının hesabına bakarak kredi kazanmak mümkün değildir.
- Rövanş: biten maçtaki eski oyuncular için tek yeni oda, tam dolunca maç başlatma.
- Oyundaki ses tercihi ve taş tıklama sesi, SharedPreferences ile kalıcı. Sohbet/arama sesleri etkilenmez.
- Bağlantı kesintisinde geri bağlanma düğmesi ve hatada kademeli senkronizasyon aralığı.
- Maç sonunda sadece sunucu tarafından doğrulanmış (+çip, +XP) ödül kartı.
- 320, 360, 393, 440 piksel genişliklerde Auto + çip sayacı Flutter widget testleri.
- Test sonucu: 2026-10-26 Build575 dalı sunucu testleri 75/75 geçti; Android sürüm incelemesi ayrıca doğrulanacaktır.

## Bu sürümde henüz **tamamlandı** denmeyecekler
1. Gerçek telefonda 320/360/393/440 genişliklerinde ekran görüntüsü karşılaştırması ve taşların referansla görsel kalite onayı. Widget testleri gerçek cihaz testi yerine geçmez.
2. Gerçek reklam SDK'sı ve sağlayıcının sunucu doğrulamasıyla (SSV) ödüllü video; izlenmeyen, iptal edilen veya doğrulanmamış reklamlara çip verilmemeli.
3. Ücretli oyuncudan oyuncuya hediye transferi, hediye/emoji fiyatları, arkadaş ekleme/engelleme/şikayet paneli ve sunucu kontrollü muhasebe. Mevcut sohbet emojileri korunur.
4. Rövanşın iki gerçek cihazda kullanıcı akışı, iki kullanıcı/çeşitli bot zorlukları ve bağlantı kesintilerinde son e2e test.
5. Zar/taş/ödül için özgün ses dosyaları, detaylı kazanma-yeme-bonus animasyonları, kalite son rötuşları ve isteğe bağlı ses sessizliği doğrulaması.
6. Bulut Ludo servisi deployment, gerekli sırlar ve cihazda doğrulanmış imzalı APK üzerine son "Güncelle" yayını. Canlıdaki Build574 ve android-update.json test süresince değişmeyecek.

## Yayın kapısı
`NgelX-BUILD575-LUDO.yml` yalnızca derleme/test amaçlıdır. Bulut oyun servisi güncellenmeden Build575'teki yeni Auto ve çip ödülü çalışmaz. CI testi + doğrulanan imza + gerçek cihaz testleri tamamlanmadan canlı güncelleme alanına sürüm kaydı açılmaz. Build574 mevcut kullanıcılar için yayınlanan sürüm olarak kalır.
