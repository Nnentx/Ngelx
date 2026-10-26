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
- Oyuncunun avatarına dokununca profil ve sunucudan alınan, telefon ekranında kaydırılabilir **16 çeşit hediye kataloğu** (gül, kalp, taç, kahve, beğeni, domates, pizza, su kovası, saat, alev, horoz, terlik, tava, pompa, yumurta ve balon; 10–100 çip arası). Firestore çok belgeli atomik işlemle gönderenin çipi düşer, alıcının hediye koleksiyonu artar ve oda etkinliğine eklenir. Aynı requestId tekrar ücretlenmez, fiyatlar kullanıcıdan alınmaz. Bir oda için gönderen başına en çok 30 hediye ve 3 saniye bekleme uygulanır.
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

## Build575 son görsel ve güvenlik eklemeleri
- Oyun sonunda kazanan kişi için kupa + yıldızlı kompakt ve kısa süren animasyon; mağlup olan için yanlışlıkla zafer efekti gösterilmez. Orijinal tahta yerleşimi aynı kalır.
- Bloklanan oyuncunun sohbet mesajları ve hediye gönderim geçmişi sadece bloklayan kişinin **oyun görünümünden** gizlenir; diğer oyuncuların ve kayıtlı odanın içeriği değiştirilmez. Engeli kaldırınca yeniden görünür.
- 320 px küçük telefon genişliğinde kazanma/kaybetme widget kontrolü ve sunucuda kişisel engelleme filtre testi.
- Google AdMob SSV: doğrulanmış ödül sorgulaması ve gerçek kimliklerle **isteğe bağlı** Flutter Mobile Ads entegrasyonu; gerekli publisher değerleri yokken reklam kapalı kalır.
- Node regresyon testleri: oyun, ödül ekonomisi, hediye aktarımı, sosyal engelleme ve güvenli reklam doğrulaması dahil 99/99 (son GitHub eyleminde).
- Android inceleme ve tasarım testi ayrı CI'da yürütülür; son sürüm için başarılı bitiş ve fiziksel cihaz onayı beklenir.

- Güvenli reklam oturumu: aynı kullanıcı 15 dakikalık oturum açıkken yeni token üretemez, tekrar dokunma aynı token'ı döndürür; günlük 20 oturum denemesi sınırı Firestore CAS ile tutulur ve gerçek ödül alınınca token tüketilir. Sahte yerel reklam tamamlama mesajları bakiye değiştiremez.
- GitHub Actions son kod değişikliklerini seri denemelerle inceler; eskimiş denemeler iptal edilir, Flutter paket/analiz/widget adımları ayrı ve süre sınırlıdır.

## Son Android derleme ve reklam smoke kontrolleri (26.10.2026)
- Widget suite'in gerçek tahtayı açıp dokunmaya çalışan avatar testi Flutter test runner'ı uzun süre kilitledi. Bu test yerine avatar `GestureDetector` hit-area ve `onPlayerTap` bağlantıları derleme öncesi sabit kaynak sözleşmesiyle doğrulanır. Gerçek avatar tıklaması iki fiziksel telefonla test edilmelidir.
- İzleyici/masaya oturmamış hesap yanlışlıkla galibiyet kupası alamaz (`!widget.watch`, `seat>=0`).
- AdMob rewarded video gösterilmeden önce SSV `customData` ayarının tamamlanması **beklenir**; bu işlem yarış koşuluyla eksik callback üretmemelidir.
- CI, imzalı ve reklamsız Build575 inceleme APK'sını artefakt olarak kaydettikten sonra ayrık adımda **yalnızca Google demo/test AdMob App ID ve Rewarded Unit ID ile** mobil SDK ve Dart derleme denetimi yapar. Demo kimlikleri hiçbir yayınlanacak APK içinde kullanılmaz. Bu denetim başarısı canlı Ads hesabının bağlı olduğu anlamına gelmez.
- En güncel Android ve reklam smoke test sonuçları, CI'nin `NgelX-BUILD575-LUDO.yml` çıktısı tamamlandığında doğrulanır; bitmemiş işler başarılı ilan edilmez.

## Bu sürümde henüz **tamamlandı** denmeyecekler
1. Gerçek telefonda 320/360/393/440 genişliklerinde ekran görüntüsü karşılaştırması ve taşların referansla görsel kalite onayı. Widget testleri gerçek cihaz testi yerine geçmez.
2. Google SSV imza ve hesap kredisi sunucu tarafına kodlandı, ancak **mobil Ads SDK'nin gerçek kimliklerle derlenip doğrulanması, gerçek reklam uygulama/birim kimlikleri, izin ve gizlilik onayı, AdMob panelinde callback ayarı ve gerçek callback canlı testi** henüz eksik. Bu nedenle reklam düğmesi açılmamalı ve test imzası gerçek reklam sayılmamalı.
3. Hediye/çip aktarımı ve Ludo içi engelle/şikâyet kaydı kodlandı. Ancak gerçek cihazlarda eşzamanlı ödemenin doğrulanması, moderatör API'sinin gerçek yetkili hesaplarla işletime alınması, operasyon ekranının hazırlanması ve inceleme iş akışının onaylanması ve NgelX geneline uygulanacak arkadaş ekleme yetkileri hâlâ eksik. Mevcut sohbet emojileri korunur.
4. Rövanşın iki gerçek cihazda kullanıcı akışı, iki kullanıcı/çeşitli bot zorlukları ve bağlantı kesintilerinde son e2e test.
5. Zar/taş/ödül için özgün ses dosyaları, detaylı kazanma-yeme-bonus animasyonları, kalite son rötuşları ve isteğe bağlı ses sessizliği doğrulaması.
6. Bulut Ludo servisi deployment, gerekli sırlar ve cihazda doğrulanmış imzalı APK üzerine son "Güncelle" yayını. Canlıdaki Build574 ve android-update.json test süresince değişmeyecek.

## Moderatör inceleme altyapısı (yeni, henüz üretimde değil)
- Şikâyetler artık **iki Firestore kaydına tek atomik CAS işlemle** yazılır: gerçek şikâyet (`report575_<SHA256>`) ve günlük özel inceleme sırası (`moderation_queue575_YYYY-MM-DD`). Kayıt düşüp listede kaybolma durumu engellenir.
- `moderation_queue` aksiyonu yalnızca sunucuda `LUDO_MODERATOR_UIDS` allowlist'inde bulunan ve Firebase oturumu doğrulanmış moderatör UID'sine açıktır. Eksik/boş allowlist halinde erişim **tamamen kapalıdır**. Her sayfa 50 kayıt içerir, eski kayıtlar sayfalanabilir (günlük indeks en fazla 500).
- `moderation_resolve` aksiyonu `pending` raporu, sorumlu moderatör UID'si ve zaman damgasıyla `reviewed`, `dismissed` veya `actioned` durumlarından birine bir kez CAS ile geçirir. Bu durumlar sadece **kayıt durumudur**; oyuncuya otomatik ceza/hesap yasaklama uygulanmaz.
- Mevcut bildirim/şikâyet paneli kullanıcı içindir; moderatörün gerçek operasyon arayüzü, özel Firebase UID konfigürasyonu ve canlı moderasyon süreç onayı hâlâ gereklidir. Üretime geçilmeden bu hizmet kurallarına ayrı gözden geçirme yapılmalı.
- Cloudflare Workers deploy **yapılmadan** `NgelX-BUILD575-WORKER-DRYRUN.yml` ile yeni sunucu JS bağımlılıklarının paketlenmesi ve endpoint testleri doğrulanır.

## Yayın için kalan 4 ana kontrol (26 Ekim 2026)
1. **Son Build575 Android inceleme çıktısı:** `NgelX-BUILD575-LUDO.yml` backend, Flutter analiz, küçük ekran widget, geçerli imza ve release APK/artefakt aşamalarından tamamen başarıyla çıkmalı. AdMob demo-ID smoke aşaması ayrıca başarılı olmalı. Yalnızca önceki bir commit'in APK'sına güvenilmez.
2. **İki gerçek telefon:** farklı iki Firebase hesabıyla 2/4 kişi ve takım, Auto aç/kapat, rövanş, hediye fiyatı ve alıcıya teslim, sohbet/engelle/şikâyet, ağ kaybı-geri dönüş, dar ekran ve kupa/taş animasyonu tek tek denenmeli. Bot modu ayrı kontrol edilmeli.
3. **Canlı sunucu:** son `ludo565.mjs`, `index.mjs` ve server bağımlılıkları imzalı APK'dan **önce** Cloudflare'a dağıtılmalı; `/health`, Firebase kimlik doğrulama, Firestore CAS/gift ve Google SSV callback bağlantısı test edilmeli. Build574'ün kullandığı endpoint'in mevcut işlevleri bozulmamalı.
4. **AdMob + moderasyon + yayın:** gerçek AdMob App ID/Rewarded Unit ID ve SSV URL onaylanmalı; kullanıcı izin/gizlilik uyumluluğu tamamlanmalı; `pending` Ludo şikâyetlerinin gerçek moderatör iş akışı sağlanmalı. Demo reklam kimlikleri üretim APK'sına girmemeli. Ancak bundan sonra web güncelleme manifestine yeni sürüm girilebilir.

**Not:** Kodun hazır olması, gerçek telefon/servis erişimi gerektiren bu maddelerin tamamlandığı anlamına gelmez. Son APK dağıtımı dışındaki aşamalar kullanıcının mevcut Build574 uygulamasını etkilememelidir.

## Maç ödülü yeniden bağlanma ve Firestore CAS doğrulaması
- Bağlantı kesilip aynı biten maça dönülürse ilk seferde sunucunun onayladığı **çip/XP/seri/galibiyet** `reward` makbuzu cüzdan belgesindeki `matchRewards` alanından tekrar okunur. Tekrar görüntüleme **yeni ödeme üretmez**.
- Sunucunun önceki Build575 kodundan kalan eski makbuzlarda `matchRewards` bulunmayabilir; geriye dönük destek yine eski ödemeyi korur, hayali bir kazanç bilgisi oluşturmaz. `receipts` idempotency kontrolü korunmuştur.
- Makbuz geçmişi, zaten bitmiş odanın 48 saatlik takip süresiyle birlikte temizlenir; diğer oyuncunun veya izleyicinin cüzdanına paylaşılmaz. Günlük hediye ve sandık alımı araya girse de asıl maç makbuzu sabit kalır.
- Mock cüzdan testlerine ek olarak, gerçek `ludoStore565` Firestore REST `documents:commit` isteği iki kayıt (reklam oturumu) ve üç kayıt (hediye/SSV) için kontrol edilir. `updateTime` / `exists:false` CAS koşulu, doğru Firebase proje yolu, Authorization ve 409 tekrar deneme davranışı test edilir. Canlı Firestore işlem denemesi yine ayrı kabul testidir.
- Son kaynak üzerinde **119/119 sunucu testi geçti** (26 Ekim 2026, GitHub Actions 40330155671); yeni Android inceleme derlemesi halen test akışında olduğundan buradan yayına hazır sonucu çıkarılmaz.

## Yayın kapısı
`NgelX-BUILD575-LUDO.yml` yalnızca derleme/test amaçlıdır. Bulut oyun servisi güncellenmeden Build575'teki yeni Auto ve çip ödülü çalışmaz. CI testi + doğrulanan imza + gerçek cihaz testleri tamamlanmadan canlı güncelleme alanına sürüm kaydı açılmaz. Build574 mevcut kullanıcılar için yayınlanan sürüm olarak kalır.
