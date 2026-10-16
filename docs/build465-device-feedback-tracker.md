# NgelX Build465 — cihaz geri bildirimi / 15 madde

**Referans kurulum:** v1.0.240, Build465, PR #64, `qa/ngelx-build465-install-20261016`.
**Bu çalışma:** `qa/ngelx-build465-feedback-fixes-20261016`.
**Durum:** QA taslağı; üretim yayını yapılmadı. **Kodlandı ≠ cihazda doğrulandı.**

| # | Kullanıcı isteği | QA dalındaki durum | Doğrulama |
|---|---|---|---|
| 1 | Sesli grup araması fotoğrafı tam görünen kare | Yerel, yuvarlak köşeli tam resim patch'i hazır | Flutter + cihaz bekliyor |
| 2 | Katılımcı sesini susturup geri açabilme | **Yerel dinleme** için subscribe/unsubscribe patch'i hazır; başka kişinin mikrofonunu uzaktan açma iddiası yok | 2 katılımcılı gerçek arama bekliyor |
| 3 | Fotoğrafa yanıtın küçük alıntı görseli | Paylaşılan görsel altındaki 60 px yanıt önizlemesi patch'i hazır | Flutter + cihaz bekliyor |
| 4 | Mesaj fotoğrafları yuvarlatılmış ve kırpılmadan görünmeli | Var olan Build453/454 doğal oranlı `BoxFit.contain` + yuvarlatılmış kenar **korundu**, geri alım yapılmadı | Dikey/yatay farklı fotoğraflar ile test |
| 5 | Yazılı mesaj alıntı görünümü Messenger gibi | Var olan alıntı bileşeni incelendi; tasarımın son rötuşları açık | Açık |
| 6 | Büyütülen fotoğraf Android alt tuşlarına taşmasın | SafeArea/boyut patch'i hazır | Android cihaz bekliyor |
| 7 | Grup fotoğrafı kalbi sağa kaymasın | Rozet fotoğraf genişliğine sabit patch'i hazır | Cihaz bekliyor |
| 8 | Özel fotoğraf kalbi yakına hizalansın | Rozet fotoğraf genişliğine sabit patch'i hazır | Cihaz bekliyor |
| 9 | Grup mesaj/emojisi/profil boşlukları Messenger gibi | Kod ve ekran görüntüsü incelendi, görsel ince ayar açık | Açık |
| 10 | Özel sohbetin alt alanı gruptaki gibi olsun | Kamera/galeri doğrudan, emoji alanı içte, alt boşluk tek kez olacak şekilde patch hazır | Dar ekran/klavye testi bekliyor |
| 11 | Gelen arama zili ve yinelenen Reddet/Cevapla paneli | Android bildirim izni + yeni zil kanalı; başlık tıklaması doğrulanmış sohbete gidiyor, tekrarlı sheet kaldırıldı | Android 13+/izin/sessiz mod/ses testi bekliyor |
| 12 | Arama ekranları Messenger videosunu referans alsın | Kısmi avatar ve ses menüsü; tam ekran/mini pencere/görünüm refaktörü açık | Açık |
| 13 | Büyütülen video alt sistem çubuğuna taşmasın | SafeArea/boyut patch'i hazır | Dikey/yatay video cihaz testi bekliyor |
| 14 | Grup/özel sohbete girince son mesajlar altta görünsün | Eski scroll offset korunmuyor; açılış sonuna yerleştiriliyor; kullanıcı dokununca bırakıyor | Cihaz ve Flutter bekliyor |
| 15 | Gelen Kutusu “Kişi bilgisi yükleniyor…” takılmasın (Issue #65) | Per-UID sınırlı zamanlayıcıyla yeniden deneme + manuel yenileme patch'i hazır | Gerçek kopma/geri gelme testi bekliyor |

## Düzeltme kaynakları
- `tools/apply_build465_inbox_recovery.py`
- `tools/apply_build465_safe_media.py`
- `tools/apply_build465_reaction_alignment.py`
- `tools/apply_build465_chat_initial_scroll.py`
- `tools/apply_build465_private_composer.py`
- `tools/apply_build465_call_participants.py`
- `tools/apply_build465_photo_reply_layout.py`
- `tools/apply_build465_ringtone_channel.py`
- `app/lib/build454_widgets.dart` (ikinci yanıt panelini kaldıran chat açılışı)
- `app/android/app/src/main/AndroidManifest.xml` (Android 13+ bildirim izni)
- `.github/workflows/NgelX-BUILD465-INSTALL-QA.yml` ve `NgelX-BUILD465-FEEDBACK-UNIT.yml`.

## Kabul koşulları
1. Tüm kaynak üretme patch'leri çakışmadan uygulanmalı.
2. `flutter analyze` hata vermemeli; Flutter widget ve Firestore emulator testleri geçmeli.
3. Build465 kurulum kimliği/imzası korunmalı; üretim verisi/kuralları değiştirilmemeli.
4. Android cihazda grup ve özel sohbet, dikey/yatay fotoğraf/video, zayıf ağ, zil izni, 2+ kişilik sesli arama senaryoları tamamlanmalı.
5. **CI veya APK çıktı diye kullanıcıya hatanın kesin düzeldiği söylenmemeli**; cihaz onayı ve ekran görüntüsü/test kaydı gerekli.
