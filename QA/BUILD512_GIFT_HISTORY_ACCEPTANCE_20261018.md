# Build512 QA kabul planı — 18 Ekim 2026

> **Durum: test adayı, kabul edilmedi.** `main` / çalışan Build484 / indirme sitesi / production Firebase ve LiveKit dokunulmayacak.

## Kaynak
- Kullanıcı videosundaki dokuz maddelik ana takip: [#138](https://github.com/Nnentx/Ngelx/issues/138)
- Hediyeler ve yorumlar: [#137](https://github.com/Nnentx/Ngelx/issues/137)
- Kod: [Build511 PR #140](https://github.com/Nnentx/Ngelx/pull/140) → [Build512 PR #141](https://github.com/Nnentx/Ngelx/pull/141)

## Laboratuvar koşulu
- **Yalnız izole Firestore Emulator / staging Firebase projesi** üzerinde dene; kullanıcıların gerçek verilerini değiştirme.
- Sanal hediye gönderimi varsayılan **KAPALI**: `bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)`.
- Sadece izole test yapılandırmasında test edilecek build için `--dart-define=NGELX_VIRTUAL_GIFT_STAGING=true` kullanılabilir. Bu, staging'i otomatik doğrulamaz: gerçek Firebase servis ayarının da staging olduğundan emin ol.
- Gerçek para, coin bakiyesi, mağaza ödemesi veya tahsilatı **yok**.
- Gerçek Android cihaz testleri, işletim sistemi izinleri ve uzun yayın kabulü yapılmadı.

## İstenen QA senaryoları
- [ ] Normal QA APK'da `Gül` veya `Elmas` gönderimi **yasak**, açıklayıcı uyarı çıkar; production Firestore'a yeni hediye yazılmaz.
- [ ] Staging'de Gül ×1, ×5, ×10 (tek işleme tek ID) gönder; her olayın `quantity`, `points`, `uid`, `userId`, `createdAt` alanı doğrulansın.
- [ ] Miktar 0/11, değiştirilmiş puan, sahte kullanıcı, başka yayına gönderim ve sona ermiş yayına gönderim reddedilsin.
- [ ] Aynı hediye olay ID'sini tekrar yazma, değiştirme veya silme engellensin.
- [ ] Alıcı yayında emoji büyüyerek belirsin; yüksek puanlı hediyede büyük animasyon, düşükte küçük; süre sonunda kaybolsun.
- [ ] Anlık animasyondan sayaç artmasın. Gönderi doğrulanmış Firestore olaylarından host heartbeat ile hesaplanarak `giftCount` tutarlı kalsın.
- [ ] Yorum listesinde `Gül ×5`, gönderen ve hediye gösterilsin; normal yorum ve moderasyon bozulmasın.
- [ ] 🎁 sayaç dokunulunca hediye geçmişi açılsın; her kayıtta gönderen, tür, adet ve yerel tarih/saat görülsün.
- [ ] 50 canlı olayın içinde ve dışında hediye bulunacak test verileriyle `Daha eski hediyeleri getir` butonu sınansın; 50'si yorum olan sayfadan da önceki sayfaya geçilsin.
- [ ] 1.000'den çok yorum bulunan yayında bellek, ağ veri hacmi, geç açılma ve ardışık sayfalama ölçülsün.
- [ ] Android küçük ekran, klavye açık/kapalı, Android 3 tuş/jest, yayıncı/izleyici iki rol ve iki telefon.
- [ ] Ağ kopması, tekrar bağlanma, hediye olayının pending/ack geçişi; aynı animasyon iki kere oynamasın.
- [ ] Yayın bitince animasyon timer'ı ve Firestore listener kapanmalı, pop-up ekranın üzerinde kalmamalı.
- [ ] CI imzalı APK artifact, SHA256, Flutter analyze, emulator test sonuçları kaydedilsin; **geçti** denmeden gerçek telefon doğrulansın.

## Bilinen kapsam sınırları
- Hediye geçmişi açık `comments` akışından 50'şer olay tarıyor; bu aşamada yalnız hediyeler için ayrı sorgu indeksi yok.
- Gönderim sunucu ödeme defterine bağlı değil; yalnız sanal test akışı. İdempotency + resmi bakiye defteri ve mağaza politikaları olmadan parasal hediye sistemi açılmayacak.
- Mevcut hediye animasyonu emoji temelli Flutter UI; yüksek yoğunlukta kuyruk/öncelik doğrulaması yapılmadı.
- Build509 gerçek sistem genelinde yüzen LiveKit video, Build510 100 yorumdan daha eski sayfalama ve canlı 10 konuk fiziksel QA ayrıca açık.

## Üretime geçiş engeli
**Gerçek cihaz QA + server güvenliği + kullanıcı açık onayı olmadan hiçbir merge, release, dağıtım veya prod veri/rule güncellemesi yapılmayacak.**
