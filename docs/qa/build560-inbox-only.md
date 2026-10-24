# Ngel — Gelen Kutusu tasarım güncellemesi / Build560

Bu çalışma, doğrulanmış Build558 ve daha önce verilen dört hesap kimliğinin bulunduğu `9be616728072d82f300430ea30e13fa9f03650ed` tabanında hazırlandı. Güncelleme yalnızca Gelen Kutusu sunumuyla sınırlıdır. Ayrı Build559 hesap/e-posta çalışması bu pakete eklenmedi.

## Uygulanan kaynak değişiklikleri

| Kaynak | İşlem |
| --- | --- |
| `app/lib/main.dart` — yalnızca `MesajPage` bölümü | Kalıcı uzun arama alanı kaldırıldı. Mevcut arama ikonu, başlığın yanında kısa alan açıyor. Kapatma, sorguyu temizleyip normal başlığı geri getiriyor. Mevcut denetleyici, arama filtresi ve yeni sohbet + geri çağrısı kullanılıyor. Sekmelerin veri/sayaç hesabı korunarak yatay kaydırılabilir sunuma bağlandı. |
| `app/lib/build445_inbox_model.dart` — yalnızca profil şeridi sunumu | Görünen not baloncukları ve ayrılan 54+6 piksel boşluk kaldırıldı. Profiller kompaktlaştırıldı; isim satır yüksekliği belirlenerek taşma önlendi. Fotoğraf, isim, aktiflik, renkli halka ve tıklamalar gerçek verilerle korunuyor. Kendi + düğmesinde düzenleme; basılı tutmada mevcut not okuma/silme ekranı erişilebilir. |
| `app/lib/build560_inbox.dart` — yeni sunum bileşenleri | Çakışmayan başlık/arama satırı, mevcut görünümü koruyan sekme butonu, dar ekranda yatay sekme sırası ve kompakt profil şeridi. Normal profil şeridi 124 piksel yüksekliğinde, hücreler 90 piksel genişliğinde. |

Çok kısa yatay veya klavyeli ekranlarda profil şeridi geçici olarak görünmez yapılarak arama sonuçlarına alan bırakılır. Verisi, durumu ve gerçek zamanlı abonelikleri korunur. Büyük yazı boyutlarında şerit yüksekliği uyarlanır.

Not verileri ve mevcut okuma/düzenleme/silme yöntemleri silinmedi. Sohbet listesi, bildirim/istek işleme, filtreleme, sayaç hesapları ve gerçek zamanlı sorguların mevcut kodu korundu. Veritabanı, giriş/kayıt, mesaj gönderme/alma, grup işlemleri, profil ayarları, API/servisler, diğer sayfalar ve alt navigasyon değiştirilmedi. Sahte kullanıcı veya sohbet verisi uygulamaya eklenmedi.

## Depodaki destek dosyaları

Tarihsel ham uygulama kaynakları Git içinde topluca değiştirilmedi. Mevcut üretim zincirinin sonunda yalnızca gerekli kaynak farkını uygulayan dosyalar eklendi:

- `tools/apply_build560_inbox.py`
- `tools/build560_inbox.patch`
- `tools/build560_manifest.json`
- `tools/build560_inbox.dart`
- `tools/test_build560_inbox.py`
- `tools/build560_widget_test.dart`
- `.github/workflows/NgelX-BUILD560-INBOX.yml`
- `docs/qa/build560-inbox-only.md`

## Kontroller

Son test kaynağı: `ea467a88dac48cdcb1e94606d4475dfa4758e558`.

- Yeni 10 arayüz testi ve önceki 6 regresyon testi geçti.
- 280, 320, 360, 393, 430 ve 600 piksel genişlikte başlık/arama ayrılığı, açma-yazma-kapatma ve + işlevi kontrol edildi.
- İki kat yazı ölçeği, beş sekmeye yatay erişim/sayaçlar, profil kaydırma/tıklama ve kısa ekran uyumu kontrol edildi.
- Tam Flutter uygulama analizi hata vermeden geçti; mevcut uyarı/bilgi borcu temizlenmiş sayılmıyor.
- Kaynak kapsamı testi, Gelen Kutusu dışındaki sayfaları; sohbet/bildirim liste ve sorgularını; not işlemlerini ve ilgisiz arama yardımcılarını önce/sonra birebir karşılaştırıyor.
- İlk uygulama, tekrar uygulama ve kaynak kaymasına karşı ret kontrolü geçti. Veritabanı kuralları ve uygulama ayarı test dosyaları değişmedi.
- Profil testindeki örnek kişiler yalnızca test ortamındadır; uygulamadaki gerçek kullanıcıların yerine geçirilmez.

Derleme: https://github.com/Nnentx/Ngelx/actions/runs/40078881350

APK başarıyla derlendi ve indirildikten sonra doğrulandı:

- Paket: `com.nnentx.ngelx_app`, sürüm `1.0.330`, yapı `560`.
- Mevcut güncelleme imzası eşleşti: SHA256 `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`.
- ARM64 uygulama ve Flutter çalışma zamanı dosyaları mevcut.
- ZIP arşiv özetleri GitHub artifact kayıtlarıyla, APK özeti derleme çıktısındaki özetle eşleşti; ZIP bütünlük kontrolü geçti.
- Değişen iki kaynak ve yeni sunum dosyası, onaylanan yama/yardımcı dosyayla eşleşti. Diğer **54 Dart dosyası** Build558 UID tabanıyla birebir aynı. Arşivdeki `firestore.rules` da aynı kaldı.
- APK boyutu: 47.506.943 bayt.
- APK SHA256: `3fa1d07ab8ac00cebfb864bb1ec25a70a7c4c70ff52272004a032ddb63834471`.

Gerçek telefonda son kabul kontrolü henüz yapılmadı. Üretime dağıtım, mağazada yayın veya sunucu ayarı değişikliği yapılmadı.
