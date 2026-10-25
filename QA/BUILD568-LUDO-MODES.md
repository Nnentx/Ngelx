# Build568 Ludo değişiklikleri

Temel: feat/build567-ludo-quality, 3b1884860f9ee458b0daba284bdc638cc84155ae.

- Mevcut Ludo masası korunarak makineye karşı 2/4 kişilik Klasik ve Power oyunları eklendi.
- Kolay, Orta, Zor makine hamleleri sunucuda hesaplanır. Makine sırası istemciye güvenilmeden ilerler.
- Aynı mod/kapasitedeki gerçek oyuncular otomatik eşleşir; masa dolunca otomatik başlar. İptal, süre aşımı ve eşzamanlı katılımlar ele alındı.
- Yeni oda kodları yalnızca altı rakamdır. Önceki 16 karakterli davetler çalışmaya devam eder.
- Lobiye aşağı çekerek yenileme ve yenile simgesi eklendi.
- Masa sohbetinin mesaj kutusu klavye/gezinme alanını dikkate alır. Davet listesinin altına güvenli boşluk eklendi.

## Doğrulama

- Node: 41 test geçti (oyun, yeni modlar, altı tam oyun simülasyonu ve mevcut moderasyon testleri).
- Dart: yeni arayüz ve test dosyaları format ayrıştırıcısı ile sözdizimi kontrolünden geçti.
- 17 Flutter testi ve tüm uygulamanın kod analizi geçti. APK derlemesi ve imza doğrulaması başarılı.
- Başarılı derleme: https://github.com/Nnentx/Ngelx/actions/runs/40214934625
- Doğrulanmış paket: com.nnentx.ngelx_app, sürüm 1.0.338, versionCode 568.
- APK SHA256: 76c5fc3f3643b751b04a76c59d150767874974d2ee19e8c95364dae5bfb128d8.
- Önceki uygulamanın görsel ve ses dosyaları byte düzeyinde karşılaştırıldı; mevcut Android imzası doğrulandı.
- Test edilmiş kaynak: c7f57803b8097d1b71d7b74b4978ddba7e26eb7d.
- Test edilmiş tam kaynak arşivi: NgelX-Build568-Assembled-Source, artifact 12607217256.
- Canlı sunucuya dağıtılmadı. Kullanıcının açık onayıyla feat/build568-ludo-modes dalına gönderildi.

## Derleme

`.github/workflows/NgelX-BUILD568-LUDO.yml`, doğrulanmış Build567-Assembled-Source çıktısını 40189872161 numaralı çalışmadan geri yükler ve yalnızca tools/apply_build568_ludo.py farkını uygular.
Testlerden sonra mevcut imzayla 1.0.338 / 568 inceleme APK dosyasını üretir. Otomatik sunucu dağıtımı veya güncelleme yayını yapmaz.

Sunucu kodu devreye alınmadan yeni istemcinin makine/eşleşme işlemleri kullanılamaz.
