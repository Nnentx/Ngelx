# Build 483 — Topluluk Yetki Düzeltmesi: Yayın Öncesi ve Geri Alma

**Durum (2026-10-17):** Aday kurallar Firestore emülatöründe doğrulandı. **Canlı güvenlik kuralları yayımlanmadı.** Aşağıdaki liste, yetkili Ngel X bakım ekibi için operasyon kontrol listesidir; çalışan uygulamayı ve kullanıcı verilerini değiştirmek üzere otomatik bir tetikleyici değildir.

## Kaynak ve doğrulanmış sürümler

- Uygulama: kurulu kalması gereken **Build 482**; Flutter uygulaması, kameralar, sohbetler, çağrılar, galeri ve gizlilik ekranları bu çalışma kapsamında değiştirilmedi.
- Test edilen kural dalı: `qa/ngelx-build483-community-permissions-20261017`.
- Taslak inceleme: [PR #93](https://github.com/Nnentx/Ngelx/pull/93).
- Başarılı test / salt-okunur yedekleme: [GitHub Actions #39057850591](https://github.com/Nnentx/Ngelx/actions/runs/39057850591).
- Yedek: `NgelX-Build483-READ-ONLY-Rollback-Backup`, artifact **12110232635**. **7 gün süreli; 2026-10-24 tarihinde silinmeden önce güvenli, erişimi kısıtlı uzun ömürlü depoya aktarılması gerekir.**
- 2026-10-17 tarihinde okunan üretim kural dosyasının SHA-256 ilk 16 karakteri: `0307f035ad68f047`. Test edilen topluluk-only aday: `56bf091f7940bd4f`. Bunlar **tam hash değildir**; tam değerler yedek `release-metadata.json` içindedir.
- Mevcut kurallar için o anda kaydedilen immutable ruleset: `projects/ngelx-44eed/rulesets/87d4781e-f7cf-40c4-8f73-3e7e059ba285`. Yayın zamanı aktif ruleset farklıysa işlem durdurulmalı.

## Yayın ön koşulları

- [ ] Canlı Firebase projesinin **`ngelx-44eed`** olduğu yetkili yönetici tarafından doğrulandı.
- [ ] Üretim kurallarının değişmez önceki sürüm kimliği, tam SHA-256 değeri ve tam dosyası **yetkili depoya** yedeklendi; GitHub'ın süreli artifact'ı tek kopya değil.
- [ ] Projeye erişen diğer geliştiricilerin o sırada eşzamanlı Firebase kural yayını yapmayacağı teyit edildi.
- [ ] Build 483 aday kurallarının tam SHA-256 değeri, başarısı kanıtlanan emülatör adayıyla eşleşiyor.
- [ ] `tools/apply_build483_community_permissions.py` dışındaki üretim `chats`, `users`, medya, Authentication ve Storage kuralları **değişmiyor**.
- [ ] Emülatörde `build450`, `build455`, `build456`, `build472`, `build483` testleri; ayrıca `test_build483_release_safety.py` içindeki yayın/geri alma testleri başarılı.
- [ ] Geri alma planı ve canlı cihaz kabul kontrolü hazır; yetkili operatör gerçekten yayın yapmayı onayladı.

## Yetkili dağıtım prosedürü

1. Ayrılmış, erişim kontrollü bir bakım ortamında bu daldaki sabit sürümü alın. `build483-rollback/previous.rules`, `candidate.rules` ve `release-metadata.json` dosyalarını artifact'tan geri yükleyin ve dosyaların tam SHA-256 doğrulamasını yapın.
2. İlgili Firestore release nesnesinin hâlâ yedekte belirtilen immutable ruleset'i işaret ettiğini ve kurallarının aynı tam SHA-256 değerine sahip olduğunu **salt okunur** kontrol edin. Fark varsa işlemi **iptal edin**, yedeği zorlayarak yayınlamayın.
3. Önce `tools/release_build483_production_rules.py stage` ile mevcut sürümü yeniden okuyup yeni geri alma dosyalarını oluşturun. Aynı adayın kurallarını Firebase emülatöründe test edin.
4. Üretim Firebase Rules API'sine yalnızca doğrulanan **tek `cloud.firestore` release pointer** güncellemesi uygulayan, proje kimliği ve SHA korumalı `tools/release_build483_production_rules.py publish` yordamını ancak yetkili yayın ortamında kullanın. Bu adım **mevcut sohbete bağlı araçlar üzerinden otomatik uygulanmamalı**. Tüm `firebase deploy` komutuyla başka hizmetleri veya yanlış kural dosyasını dağıtmayın.
5. Güncellenen aktif immutable ruleset'i ve kural içerik hash'ini yeniden okuyun. Okunan değer adayla uyuşmazsa yayımlanan sürümü bekletmeden önceki immutable ruleset'e geri çevirin. `publish` akışındaki otomatik rollback başarısızsa üretim işlemlerini durdurup elle müdahale edin.

## Canlı cihaz kabul kontrolü (önce test topluluğunda)

- [ ] Kurucu: topluluk profil fotoğrafını değiştir; küçük kare görsel güncellensin, kapak korunmalı.
- [ ] Kurucu: bir üyeyi yönetici yap / geri al; veritabanındaki rol ve ekrandaki rozet eşleşsin.
- [ ] Kurucu: moderatör yap / geri al, sustur / geri al; yetkisiz kullanıcı aynı yazmaları gerçekleştiremesin.
- [ ] Kurucu: özel topluluk, üyelik onayı, gönderi onayı, ad/açıklama/kurallar ve durdur/yeniden aç.
- [ ] Yönetici/moderatör: yalnızca kendi rolüne izinli moderasyon işlemleri çalışsın; başkasına kurucu yetkisi verilmesin.
- [ ] Gönderi: yorum kapat/aç, yavaşlat, sabitle, raporla; yetkisiz üyeler reddedilsin.
- [ ] Üye daveti: isimler görünür kalsın; davet bağlantısı / yeni sohbet oluşturma etkilenmesin.
- [ ] Regresyon: özel sohbet mesajı gönderme/alma, geçmiş mesajlar, medya galerisi, aramalar, kamera, profil, bildirimler ve Ayarlar/gizlilik düzgün çalışsın.
- [ ] Gerçek fotoğraf yüklemesi için Firebase Storage yetkisi ayrı kontrol edilmeli; Firestore testi Storage erişimini doğrulamaz.
- [ ] Başarı/başarısızlık durumunda uygulama hata kayıtları incelensin, gizli bilgileri/log tokenlarını paylaşmayın.

## Geri alma ve sınırlamalar

- Mevcut kuralların önceden kaydedilmiş immutable ruleset kimliğiyle `cloud.firestore` release'inin önceki sürümüne geri döndürülmesi, kural geri alma prosedürüdür. İlgili değişmez kuralların tam SHA'sı yeniden doğrulanmalıdır.
- **Bu yedek kullanıcı verisi yedeği değildir.** Kullanıcı dokümanlarının silinmesi, topluluğu tamamen silme, Firebase Storage nesneleri veya Auth hesaplarına müdahale kapsamında değildir.
- Firebase güvenlik kuralı testleri gerçek cihaz, belirli topluluk verisi ve Storage izinlerinin doğrulanması yerine geçmez.
- Canlı yayından önce yukarıdaki kontroller tamamlanmazsa **yayınlama; Build 482'yi kullanmaya devam et**.
