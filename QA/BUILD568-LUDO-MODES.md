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
- Flutter arayüz testleri ve APK derlemesi henüz doğrulanmadı.
- Canlı sunucuya dağıtılmadı. GitHub gönderimi otomatik onay denetimi tarafından durduruldu.

## Derleme

`.github/workflows/NgelX-BUILD568-LUDO.yml`, doğrulanmış Build567-Assembled-Source çıktısını 40189872161 numaralı çalışmadan geri yükler ve yalnızca tools/apply_build568_ludo.py farkını uygular.
Testlerden sonra mevcut imzayla 1.0.338 / 568 inceleme APK dosyasını üretir. Otomatik sunucu dağıtımı veya güncelleme yayını yapmaz.

Sunucu kodu devreye alınmadan yeni istemcinin makine/eşleşme işlemleri kullanılamaz.
