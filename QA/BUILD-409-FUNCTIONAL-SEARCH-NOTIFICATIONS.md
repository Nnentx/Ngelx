# NgelX Build 409 — İşlevler önce, tasarım sonra

## Paket kapsamı
- Temel: Build 408 **1.0.184+408** kaynak yamaları ve testleri üzerinde devam.
- Kullanıcının önce eksikleri bitir, sonra onaylanan tasarımlara geç kararına uygun **yalnız işlevsel** iyileştirme.
- **Arama / tekrar eden video (Cemil Tugay örneği):** Build 407 çok kelimeli eşleşmesi korunuyor; eşleşen videolar alaka puanına, beraberlikte güncellik zamanına göre sıralanıyor. Birden fazla paylaşımın gerçek `sourceVideoId` / `contentHash` veya medya URL'si **aynıysa** yalnız tek sonuç gösteriliyor. Farklı medya dosyaları **başlıkları aynı diye** gizlenmiyor. Engelleme/özel gönderi filtreleri korunuyor. **Sınır:** Aramanın ilk 100 içerik örneklemesi halen var; bu, tüm arşivde indeksli arama değildir; farklı URL'lerle aynı dosyanın yeniden yüklenmesi otomatik eşit sayılmayabilir.
- **Gelen Kutusu grup istekleri:** Bildirim olay türü `type=group` ve `eventKind=group_join_request` geldiğinde de sunucudaki başvuru `status` okunarak `accepted/rejected/cancelled` sonuca göre eski "katılmak istiyor" metni güncellenir. Build 408'deki durum dinleyicisi bu olay türü ayrıntısı nedeniyle eksik kalabiliyordu; burada tamamlandı.
- **Sürüm:** `1.0.185+409`. Firestore rules **değişmedi ve yeniden dağıtılmıyor**; Build407'den bu yana zorunlu kurucu/yönetici onayı korunuyor.

## Koruma ve test
1. Build 395–408 regresyon ve emülatör kuralları.
2. `tools/apply_build409_group_notice_fix.py` ve `tools/apply_build409_search_relevance.py`.
3. `tools/check_build409_search_relevance.py`: çok kelimeli arama, gizlilik, engelleme, medya tekilleştirme, navigasyon, Bildirimler olay kimliği.
4. Flutter analyze; imzalı APK ve GitHub artifact (CI sonucu ayrı doğrulanacak).
5. Telefon smoke: Cemil Tugay araması (aynı video linki tekrar var mı, farklı video kayboldu mu?) ve daha önce onaylanan isteğin Tümü/Bildirimler metni.

## Açık kalanlar
- Tam üretime hazır gerçek Anket (sadece eski "hazırlanıyor" düğmesi var). Güvenli oy sayımı, kullanıcı başına tek oy, kurallar, oy gizliliği, UI ve cihaz testi olmadan bitti sayılmayacak.
- Videolar arası kısa siyah ekran/buffering ve geniş ölçekli sunucu indeksli arama.
- Kapaklı/kapaksız kendi ve karşı profil / Profili Düzenle onaylı bire bir tasarımları **sonraki tasarım aşamasında**.
- Renkli "Grup" rozeti ve bildirimin kişi/grup adlarını iki renkle göstermek **tasarım aşamasında**.
- Sesli odalar, PK ve ikinci telefon testleri kullanıcının isteğiyle ertelendi.

**Durum:** Kaynak regresyon testleri geçti; APK + gerçek telefon doğrulaması sonuca bağlıdır.
