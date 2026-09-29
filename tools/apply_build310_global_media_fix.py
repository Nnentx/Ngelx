#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "app/lib/main.dart"
PUB_PATH = ROOT / "app/pubspec.yaml"

main = MAIN_PATH.read_text(encoding="utf-8")
pub = PUB_PATH.read_text(encoding="utf-8")

if "version: 1.0.91+310" in pub and "defaultValue: '310'" in main:
    print("Build 310 already applied.")
    raise SystemExit(0)

def one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Build 310 patch failed: {label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)

# 1) Photo helper must always go through byte normalization.
start = main.find("Future<String> ngelxFotografYukle({")
end = main.find("Future<void> ngelxMedyaSil(", start)
if start < 0 or end < 0:
    raise SystemExit("Build 310 patch failed: ngelxFotografYukle block not found")

helper = r'''Future<String> ngelxFotografYukle({
  required XFile dosya,
  required String kind,
  required String legacyPath,
  String? ext,
  void Function(int sent,int total)? onProgress,
}) async {
  final ad=dosya.name.trim();
  final hamExt=(ext??(ad.contains('.')?ad.split('.').last:'jpg')).toLowerCase();
  final temizExt=_ngelxUzantiTemizle(hamExt);
  try{
    final bytes=await dosya.readAsBytes();
    if(bytes.isEmpty)throw Exception('Seçilen fotoğraf boş görünüyor.');
    // Tüm fotoğraflar ortak byte hattından geçer. Bu hat gerçek baytları
    // yeniden kodlayıp PNG olarak yükler; galeri JPG adı verip HEIC/WEBP
    // baytı döndürse bile profil, grup, hikâye, sohbet ve akışta açılabilir.
    return await ngelxMedyaYukleBytes(
      bytes:bytes,
      kind:kind,
      ext:temizExt,
      legacyPath:legacyPath,
      onProgress:onProgress,
    );
  }catch(e){
    throw Exception('Fotoğraf yüklenemedi: '+_ngelxKisaHata(e));
  }
}

'''
main = main[:start] + helper + main[end:]

# 2) Private-chat photos also need the image normalization path.
pattern = re.compile(
    r"bool _ngelxFotoKind\(String kind\)=>const <String>\{\s*"
    r"'photos','profiles','stories','groups','chat-images','chat-backgrounds','support'\s*"
    r"\}\.contains\(kind\);"
)
replacement = """bool _ngelxFotoKind(String kind)=>const <String>{
  'photos','profiles','stories','groups','chats','chat-images','chat-backgrounds','support','thumbnails'
}.contains(kind);"""
main, n = pattern.subn(replacement, main, count=1)
if n != 1:
    raise SystemExit(f"Build 310 patch failed: photo-kind set expected 1 match, got {n}")

# 3) Feed photos: use the same primary/backup host fallback when this older
# CachedNetworkImage form is still present. Some later sources already contain it.
feed_pattern = re.compile(
    r"itemBuilder:\s*\(_\s*,\s*i\)\s*=>\s*CachedNetworkImage\(\s*"
    r"imageUrl\s*:\s*fotoListesi\[i\]\s*,\s*"
    r"fit\s*:\s*BoxFit\.contain\s*,\s*"
    r"placeholder\s*:\s*\(_\s*,\s*__\)\s*=>\s*const Center\(child:CircularProgressIndicator\(color\s*:\s*mavi\)\)\s*,\s*"
    r"errorWidget\s*:\s*\(_\s*,\s*__\s*,\s*___\)\s*=>\s*ngelxMedyaHataGorunumu\(fotoListesi\[i\]\)\s*,\s*"
    r"\)\s*,",
    re.S,
)
feed_new = """itemBuilder:(_,i)=>NgelXAgResmi(
                url:fotoListesi[i],
                fit:BoxFit.contain,
                placeholder:const Center(child:CircularProgressIndicator(color:mavi)),
                error:ngelxMedyaHataGorunumu(fotoListesi[i]),
              ),"""
main, feed_n = feed_pattern.subn(feed_new, main, count=1)
if feed_n == 0:
    # Do not fail if this source already uses the fallback in the feed.
    g0 = main.find("class _GorselYaziKartiState")
    g1 = main.find("\nclass ", g0 + 10) if g0 >= 0 else -1
    region = main[g0:(g1 if g1 > g0 else len(main))] if g0 >= 0 else ""
    if "fotoListesi[i]" not in region or "NgelXAgResmi(" not in region:
        raise SystemExit("Build 310 patch failed: feed media fallback form could not be located")

# 4) Version/build.
main = one(main, "defaultValue: '1.0.90'", "defaultValue: '1.0.91'", "runtime version")
main = one(main, "defaultValue: '309'", "defaultValue: '310'", "runtime build")
pub = one(pub, "version: 1.0.90+309", "version: 1.0.91+310", "pubspec version")

MAIN_PATH.write_text(main, encoding="utf-8")
PUB_PATH.write_text(pub, encoding="utf-8")

print("Build 310 global media fix applied.")
