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
- Oyuncunun avatarına dokununca profil ve sunucudan alınan hediye kataloğu; 20/40/100 çiplik sanal Çiçek/Kalp/Taç hediyeleri. Firestore çok belgeli atomik işlemle gönderenin çipi düşer, alıcının hediye koleksiyonu artar ve oda etkinliğine eklenir. Aynı requestId tekrar ücretlenmez, fiyatlar kullanıcıdan alınmaz. Bir oda için gönderen başına en çok 30 hediye ve 3 saniye bekleme uygulanır.
- Hediye kataloğu ve alıcının koleksiyon sayısı sunucu okuma işlemiyle görüntülenir. Sıradan sohbet emoji sistemi korunur.
- Ludo içi Engelle/Engeli kaldır ve Şikâyet et paneli: sadece aynı odada bulunan gerçek oyuncular. Engelli ilişkide ücretli hediyeler reddedilir ve gönderenin bakiyesi değişmez. Şikâyet bir maç/hedef/raporlayan için tek kez, sunucu kayıtlarına `pending` olarak yazılır; **henüz bir insan moderatöre otomatik dağıtım yapılmıyor.** Bu engel genel NgelX arkadaşlık veya sohbet ilişkisini değiştirmez.
- AdMob SSV hazırlığı (sunucuda, **gerçek reklamlar henüz kapalı**): Google P-256/ECDSA-SHA256 imzası, DER doğrulaması ve orijinal query metni bozulmadan doğrulama; sabit reklam birimi, zaman ve tekil transaction id kontrolü; yalnızca kimliği doğrulanmış oyuncunun 15 dakikalık reklam oturumu için 30 sanal çip. Firestore atomik işlemle oturum kullanılır, tekrar ödüllendirme engellenir. Uygulama `ad_status` ile yalnızca sunucunun onayladığı kazancı sorgulayabilir. Sunucu `LUDO_ADMOB_AD_UNIT` ayarı olmadan `ad_session` ve SSV çağrılarını reddeder.
- Google kaynak: https://developers.google.com/admob/flutter/ssv (23 Ekim 2026 güncellemesi). Public key hizmeti `www.gstatic.com/admob/reward/verifier-keys.json` üzerinden alınır. Testler sentetik P-256 imzalarıyla çalıştı; canlı AdMob hesabında ve gerçek SSV bildirimiyle ayrıca doğrulanmalıdır.
- İsteğe bağlı mobil reklam entegrasyonu: `tools/build575_rewarded_ads.dart` ve `tools/apply_build575_ads.py` hazır. Derleme açıkça **`NGELX_ADMOB_APP_ID`** ve **`NGELX_ADMOB_REWARDED_UNIT`** olmadan AdMob SDK'yı oyuna eklemez. Kimlikler sağlanırsa Flutter `google_mobile_ads ^9.2.0`, Android manifest, oyuncuya ödüllü video düğmesi, sunucudan alınan oturum token'ının `customData` olarak kullanılması ve `ad_status` ile doğrulama bekleme akışı eklenir. **Bu isteğe bağlı yol henüz kimliklerle tam Android derlemesinde test edilmedi ve canlı kullanım izni değildir.**
- Oyundaki ses tercihi ve taş tıklama sesi, SharedPreferences ile kalıcı. Sohbet/arama sesleri etkilenmez.
- Bağlantı kesintisinde geri bağlanma düğmesi ve hatada kademeli senkronizasyon aralığı.
- Maç sonunda sadece sunucu tarafından doğrulanmış (+çip, +XP) ödül kartı.
- 320, 360, 393, 440 piksel genişliklerde Auto + çip sayacı Flutter widget testleri.
- Test sonucu: 2026-10-26 Build575 dalında hediye gönderme dahil en az 98 Node testi geçti; GitHub Actions son değişiklik için Flutter inceleme derlemesini ayrıca doğrular.

## Bu sürümde henüz **tamamlandı** denmeyecekler
1. Gerçek telefonda 320/360/393/440 genişliklerinde ekran görüntüsü karşılaştırması ve taşların referansla görsel kalite onayı. Widget testleri gerçek cihaz testi yerine geçmez.
2. Google SSV imza ve hesap kredisi sunucu tarafına kodlandı, ancak **mobil Ads SDK'nin gerçek kimliklerle derlenip doğrulanması, gerçek reklam uygulama/birim kimlikleri, izin ve gizlilik onayı, AdMob panelinde callback ayarı ve gerçek callback canlı testi** henüz eksik. Bu nedenle reklam düğmesi açılmamalı ve test imzası gerçek reklam sayılmamalı.
3. Hediye/çip aktarımı ve Ludo içi engelle/şikâyet kaydı kodlandı. Ancak gerçek cihazlarda eşzamanlı ödemenin doğrulanması, raporların moderasyon iş akışına bağlanması ve NgelX geneline uygulanacak arkadaş ekleme yetkileri hâlâ eksik. Mevcut sohbet emojileri korunur.
4. Rövanşın iki gerçek cihazda kullanıcı akışı, iki kullanıcı/çeşitli bot zorlukları ve bağlantı kesintilerinde son e2e test.
5. Zar/taş/ödül için özgün ses dosyaları, detaylı kazanma-yeme-bonus animasyonları, kalite son rötuşları ve isteğe bağlı ses sessizliği doğrulaması.
6. Bulut Ludo servisi deployment, gerekli sırlar ve cihazda doğrulanmış imzalı APK üzerine son "Güncelle" yayını. Canlıdaki Build574 ve android-update.json test süresince değişmeyecek.

## Yayın kapısı
`NgelX-BUILD575-LUDO.yml` yalnızca derleme/test amaçlıdır. Bulut oyun servisi güncellenmeden Build575'teki yeni Auto ve çip ödülü çalışmaz. CI testi + doğrulanan imza + gerçek cihaz testleri tamamlanmadan canlı güncelleme alanına sürüm kaydı açılmaz. Build574 mevcut kullanıcılar için yayınlanan sürüm olarak kalır.
