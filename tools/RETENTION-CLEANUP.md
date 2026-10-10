# Sunucu hikâye saklama temizliği

Bu araç yalnız süresi dolmuş ve kaydedilmemiş hikâyeleri seçer. `archivedAt`, `highlighted=true` veya `saved=true` olanları korur. Paylaşımlar, profil medyası ve canlı yayınlar bu otomatik işlem kapsamına dahil değildir.

Varsayılan çağrı önizlemedir:

```sh
python tools/retention_cleanup.py --limit 100
```

Firebase Admin application default credentials gerekir. Uygulamanın google-services.json dosyası bu yetkiyi sağlamaz. GitHub read-only preview mevcut Firebase Admin kimliği ile başarılı çalıştı ve 50 süresi dolmuş kaydedilmemiş hikâye adayı buldu. --apply çalıştırılmadı; canlı veri silinmedi. Deployed Worker kimlik türetme yöntemi çözüldü. Medya sahipliği önizlemesi 50 adayın tamamını tanımlanamaz bulduğu için güvenli biçimde atladı (verified=0, unverifiable=50). Otomatik silme etkinleştirilmedi.

Silme modunda ek olarak `firebase-admin` ve `boto3` Python paketleri, `NGELX_MEDIA_ORIGIN`, `NGELX_R2_BUCKET`, `NGELX_R2_ENDPOINT`, `NGELX_R2_ACCESS_KEY_ID`, `NGELX_R2_SECRET_ACCESS_KEY` sunucu ortam değişkenleri gerekir. Anahtarları depoya yazmayın.

```sh
python tools/retention_cleanup.py --apply --limit 100
```

R2 yolunun kayıt sahibine ait olması ve R2 object metadata uid değerinin aynı kullanıcı olması şarttır. Tanımlanamayan eski medyalar silinmeden atlanır. Eşzamanlı kaydetme işlemleri sürüm kontrolünü kaybederse temizlik durur. Firestore işleminde içerik ve dayanıklı `_retention_cleanup_jobs` kaydı birlikte taşınır; medya hatalarında iş kaydı korunur ve sonraki çalışmada yeniden denenir. Başarılı iş, alt kayıtları ve iş kaydını temizler. Bu koleksiyon istemcilere açılmamalıdır; mevcut default deny korunur.

Yerel doğrulama:

```sh
python -m unittest discover -s tools -p test_retention_cleanup.py
```

Altı seçim/yol güvenliği testi geçti. Firebase okuma entegrasyonu doğrulandı. R2 silme entegrasyonu, eski URL sahiplik eşlemesi ve zamanlanmış sunucu kurulumu henüz doğrulanmadı. `--verify-media` yalnız metadata okur; hiçbir kayıt veya nesne silmez. Sahipsiz medya için bütün veritabanı referanslarını doğrulayan ayrı tarama gereklidir; bu araç keyfi R2 nesnelerini silmez.
