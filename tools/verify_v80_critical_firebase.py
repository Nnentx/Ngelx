#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("V80 kritik Firebase kontrolü eksik: " + message)


require("Future<String> _ngelxMedyaYayininiDogrula" in MAIN,
        "yüklenen medya yayın doğrulaması")
require("HttpHeaders.rangeHeader:'bytes=0-63'" in MAIN,
        "düşük trafikli medya okuma kontrolü")
require(MAIN.count("return await _ngelxMedyaYayininiDogrula(url);") >= 6,
        "bütün medya taşıma yollarında yayın doğrulaması")

private_start = MAIN.index(
    "Future<void> medyaGonder(ImageSource kaynak)",
    MAIN.index("class _SohbetPageState"),
)
private_end = MAIN.index("Future<void> videoGonder", private_start)
private = MAIN[private_start:private_end]
require("await batch.commit().timeout(const Duration(seconds:20));" in private,
        "özel fotoğraf mesajında Firestore commit beklenmesi")
require("unawaited(batch.commit()" not in private,
        "erken başarılı sayılan özel fotoğraf batch yazımının kaldırılması")

story_start = MAIN.index("Future<void> hikayeYukle()")
story_end = MAIN.index("Future<void> hikayeyiAc()", story_start)
story = MAIN[story_start:story_end]
require("final url=video" in story and "ngelxMedyaYukleDosya(" in story,
        "video hikâyesinde dosya tabanlı yükleme")
require("ngelxMedyaYukleBytes(" in story,
        "fotoğraf hikâyesinde güvenli PNG normalizasyonu")

require("class NgelXYorumYazici extends StatelessWidget" in MAIN,
        "yorum yazıcısının canlı listeden ayrılması")
require("MediaQuery.sizeOf(context).height * .72" in MAIN and
        "MediaQuery.viewInsetsOf(context).bottom" in MAIN,
        "klavye değişiminde yorum listesinin yeniden çizilmemesi")
require("NgelXVideoKapakOnizleme(url:widget.url)" in MAIN,
        "tanıtım videosunda gerçek video kapağı")
require("if(cevrilecekMetin.isEmpty){" in MAIN and
        "final altyaziSonucu=await ngelxGercekAltyaziOlustur" in MAIN,
        "açıklamasız videoda konuşmadan çeviri üretimi")

print("V80 kritik Firebase/medya/yorum düzeltmeleri doğrulandı.")
