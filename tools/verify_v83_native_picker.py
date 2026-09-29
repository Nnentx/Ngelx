#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
MUSIC=(ROOT/'app/lib/create_music_editor.dart').read_text(encoding='utf-8')
KOTLIN=(ROOT/'app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
MANIFEST=(ROOT/'app/android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
PUB=(ROOT/'app/pubspec.yaml').read_text(encoding='utf-8')

def need(ok,msg):
    if not ok:
        raise SystemExit('V83 native picker eksik: '+msg)

need('version: 1.0.82+301' in PUB,'Build 301 sürümü')
need("defaultValue: '1.0.82'" in MAIN and "defaultValue: '301'" in MAIN,'uygulama içi sürüm')
need('Future<XFile?> ngelxResimSec' in MAIN,'resim seçim köprüsü')
need('Future<XFile?> ngelxVideoSec' in MAIN,'video seçim köprüsü')
need('Future<List<XFile>> ngelxCokluResimSec' in MAIN,'çoklu foto seçim köprüsü')
need('Future<XFile?> ngelxDosyaSec' in MAIN,'dosya/müzik seçim köprüsü')
need("'pickDocument'" in MAIN and "'pickDocuments'" in MAIN,'Dart native picker çağrıları')
need('"pickDocument" ->' in KOTLIN and '"pickDocuments" ->' in KOTLIN,'Android native picker metotları')
need('ACTION_OPEN_DOCUMENT' in KOTLIN and 'copyPickedUriToCache' in KOTLIN,'Android SAF ve cache kopyası')
need('READ_MEDIA_IMAGES' in MANIFEST and 'READ_MEDIA_VIDEO' in MANIFEST and 'READ_MEDIA_AUDIO' in MANIFEST,'Android medya izinleri')
need('android.intent.action.OPEN_DOCUMENT' in MANIFEST,'Android belge seçici görünürlüğü')
need('ngelxDosyaSec(tur:tur)' in MUSIC,'müzik dosyası native fallback')
need(MAIN.count('ImagePicker().pickImage(')==1,'doğrudan resim picker sadece fallback helper içinde')
need(MAIN.count('ImagePicker().pickVideo(')==1,'doğrudan video picker sadece fallback helper içinde')
need(MAIN.count('ImagePicker().pickMultiImage(')==1,'doğrudan çoklu picker sadece fallback helper içinde')
print('V83 Build 301 native Android picker doğrulandı.')
