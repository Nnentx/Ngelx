#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
MUSIC=(ROOT/'app/lib/create_music_editor.dart').read_text(encoding='utf-8')
KOTLIN=(ROOT/'app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
MANIFEST=(ROOT/'app/android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
PUB=(ROOT/'app/pubspec.yaml').read_text(encoding='utf-8')
def need(ok,msg):
    if not ok: raise SystemExit('Build 303 native picker eksik: '+msg)
need('version: 1.0.84+303' in PUB,'sürüm')
need("defaultValue: '1.0.84'" in MAIN and "defaultValue: '303'" in MAIN,'uygulama içi sürüm')
for s in ['Future<XFile?> ngelxResimSec','Future<XFile?> ngelxVideoSec','Future<List<XFile>> ngelxCokluResimSec','Future<XFile?> ngelxDosyaSec']:
    need(s in MAIN,s)
need('"pickDocument" ->' in KOTLIN and '"pickDocuments" ->' in KOTLIN,'Android picker köprüsü')
need('ACTION_OPEN_DOCUMENT' in KOTLIN and 'copyPickedUriToCache' in KOTLIN,'SAF cache kopyası')
need('READ_MEDIA_IMAGES' in MANIFEST and 'READ_MEDIA_VIDEO' in MANIFEST and 'READ_MEDIA_AUDIO' in MANIFEST,'medya izinleri')
need('ngelxDosyaSec(tur:tur)' in MUSIC,'müzik native fallback')
need(MAIN.count('ImagePicker().pickImage(')==1,'resim picker fallback tekilleştirme')
need(MAIN.count('ImagePicker().pickVideo(')==1,'video picker fallback tekilleştirme')
need(MAIN.count('ImagePicker().pickMultiImage(')==1,'çoklu picker fallback tekilleştirme')
print('Build 303 native picker doğrulandı.')
