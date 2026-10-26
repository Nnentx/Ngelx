# NgelX Ludo Build 575 — İki Android Telefonla Son Kabul Kontrolü

**Durum:** TEST PLANI. Kontroller gerçek telefonlarda uygulanmış ya da canlı sürüm onaylanmış değildir.
**Hedef:** Build 574 üzerinde çalışan NgelX uygulamasını, Build 575 yayınından önce koruyarak test etmek.

## Ön koşullar
- CI `NgelX-BUILD575-LUDO.yml` son commit için başarılı; imzası korunmuş **REVIEW** APK artefaktı test cihazına kurulmuş olmalı.
- `NgelX-BUILD575-WORKER-DRYRUN.yml` başarılı; ayrıca **gerçek** oyun sunucusu doğrulanmış bir test ortamına dağıtılmış olmalı. Dry-run canlı deploy değildir.
- İki ayrı fiziksel Android telefon / iki farklı gerçek Firebase oyuncu hesabı ve stabil ağ ile ikinci aşamada kesintili bağlantı.
- Build 574 kullanan başka hesabın eski davranışı bozulmamalı. Mevcut Güncelle manifesti deney sırasında değişmeyecek.
- Gerçek AdMob App/Ad Unit kimlikleri, SSV URL ayarı, izin ve mahremiyet kontrolleri sağlanmadıysa reklam özelliği **devre dışı** tutulur. Resmî Google test kimlikleri yalnızca derleme smoke testinde kullanılır.

## Gerçek cihaz senaryoları
| # | Adım | Beklenen sonuç | Sonuç |
|---|---|---|---|
| 01 | Telefon A klasik 2 kişilik oda açar, Telefon B kodla katılır | Tek oda, iki farklı UID, aynı tahta ve revizyon | ☐ |
| 02 | 2 kişi zar atar, taş sürer, rakip taşını yer, koruma karesi denenir | Senkron görüntü, geçerli hamle, doğru tur sırası | ☐ |
| 03 | Sırası gelen kişi 10 saniye işlem yapmaz | Auto devreye girer, hamleler otomatik sürer | ☐ |
| 04 | Auto açıkken oyuncu düğmeye dokunur | Auto kapanır, oyuncu yeniden manuel oynar | ☐ |
| 05 | Telefon A bağlantıyı keser ve geri açar | Tekrar bağlanır, zar/taşlar iki telefonda tutarlı | ☐ |
| 06 | Power modunda shield, double, control ve ödül karoları | Sunucu onaylı güç ve görsel tepki doğru | ☐ |
| 07 | 4 kişilik normal ve iki takımlı mod | Aynı odada dört ayrı hesapla gerçek kullanıcı testi; doğru takım galibiyeti | ☐ |
| 08 | Bitiş, kupa animasyonu, çip/XP ve tekrar aynı sonucu çekme | Ödül bir kez işlenir; izleyici kazanan gibi görünmez | ☐ |
| 09 | Rövanş daveti, iki oyuncunun kabulü | Ortak yeni maç, eskisi bozulmaz | ☐ |
| 10 | Günlük hediye ve sandık iki kez peş peşe talep edilir | Tek ödül, zaman sınırı uygulanır | ☐ |
| 11 | Telefon A, B'ye ücretli hediye gönderir | Gönderenin çipi bir kez düşer, B'nin koleksiyonuna bir kez eklenir | ☐ |
| 12 | Aynı hediye isteği bağlantı kopunca yeniden gönderilir | Aynı requestId ikinci kez tahsil edilmez | ☐ |
| 13 | Telefon B, A'yı engeller | B'nin sohbet/hediye bildirimi gizlenir, engelli hediye için çip düşmez | ☐ |
| 14 | Oyuncu spam/rahatsız etme şikâyeti gönderir | Sunucuda pending kayıt ve moderatör kuyruğu; normal oyuncu kuyruğu okuyamaz | ☐ |
| 15 | Moderatör yetkili hesabıyla raporu görüntüler ve karar verir | Sadece sunucu UID allowlist hesabı erişir; işlem günlüğü kaydedilir | ☐ |
| 16 | Sahte/iptal edilmiş ödüllü reklam bildirimi | Çip eklenmez. Gerçek reklam ancak canlı Google SSV onayı sonrası çip kazandırır | ☐ |
| 17 | 320, 360, 393, 440 px ve yatay ekran | Taşlar, hediye profili, sohbet, Auto ve sonuç ekranları taşmaz | ☐ |
| 18 | NgelX uygulamasının diğer ekranları, topluluk ve arama | Build 574'ün mevcut ana işlevleri bozulmaz | ☐ |
| 19 | Güncelleme imzası ve önceki Build 574 üzerine Android kurulumu | Veri kaybı yok, Android güncellemeyi kabul ediyor | ☐ |

## Kritik hata sayılacak durumlar
- Oynanmayan veya doğrulanmamış reklamdan çip elde edilmesi; aynı işlemle iki kez para/çip düşmesi ya da ödül verilmesi.
- Gerçek UID dışındaki oyuncuya ait cüzdanın erişilebilir olması; moderatör rolü olmadan gizli raporların görünmesi.
- Oda revizyonlarının ayrışması, 4 kişi/2v2 oyununun bozulması veya bağlantı yenilemenin oda değiştirmesi.
- Build 574'e güncelleme yapılamaması, APK imzasının değişmesi, normal NgelX ekranlarının kaybolması.

## Yayına geçiş kararı
Gerçek cihaz ve canlı Worker testleri tamamlanmadan bu dosyadaki boş kutular **başarılı varsayılmaz**. Rapor moderasyonunda izinli Firebase UID konfigürasyonu, gerçek AdMob gereklilikleri ve Cloudflare dağıtımı tamamlanmış olmalıdır. Son onaydan sonra `Nnentx/ngelx-web/android-update.json` güncellenebilir; bundan önce mevcut **1.0.344 / Build 574** sürümü korunmalıdır.

Referans: `QA/BUILD575-LUDO-SCOPE.md`, GitHub PR #190 ve iki Build 575 CI iş akışı.
