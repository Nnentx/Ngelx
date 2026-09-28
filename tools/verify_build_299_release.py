#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
PUB=(ROOT/'app/pubspec.yaml').read_text(encoding='utf-8')
WORKFLOW=(ROOT/'.github/workflows/build-299-release.yml').read_text(encoding='utf-8')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit('Build 299 release kontrolü eksik: '+message)


require('version: 1.0.80+299' in PUB,'pubspec sürümü')
require("defaultValue: '1.0.80'" in MAIN and "defaultValue: '299'" in MAIN,
        'uygulama içi sürüm')
require('python3 tools/verify_v80_critical_firebase.py' in WORKFLOW,
        'V80 Firebase doğrulaması')
require('python3 tools/verify_v81_music_layers.py' in WORKFLOW,
        'V81 müzik katmanı doğrulaması')
require('flutter analyze --no-fatal-infos --no-fatal-warnings' in WORKFLOW,
        'Flutter statik analiz')
require('flutter build apk --debug' in WORKFLOW and
        'NGELX_BUILD_NUMBER="$BUILD_NUMBER"' in WORKFLOW,
        'sürüm bilgili Android APK derlemesi')
require('NgelX-1.0.80-Build-299-TEST-APK' in WORKFLOW,
        'tanımlı APK artifact adı')

print('Build 299 sürüm ve APK üretim zinciri doğrulandı.')
