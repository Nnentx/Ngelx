from pathlib import Path

root=Path(__file__).resolve().parents[1]
main=(root/'app/lib/main.dart').read_text(encoding='utf-8')
pub=(root/'app/pubspec.yaml').read_text(encoding='utf-8')

checks=[
    "version: 1.0.104+323" in pub,
    "defaultValue: '1.0.104'" in main,
    "defaultValue: '323'" in main,
    "Canlı yayın ön hazırlık" in main,
    "_onizlemeyiHazirla" in main,
    "setCameraPosition" in main,
    "'filterIndex': filtre" in main,
    "'retouch': rotus" in main,
    "class _CanliHazirlikButonu" in main,
    "StreamSubscription<DocumentSnapshot<Map<String, dynamic>>>? yayinAboneligi" in main,
    "ngelxAramaEfekti(" in main,
]
if not all(checks):
    raise SystemExit('Build 323 verification failed')
if main.count("class CanliHazirlikPage extends StatefulWidget") != 1:
    raise SystemExit('CanliHazirlikPage duplicated')
if main.count("class CanliYayinPage extends StatefulWidget") != 1:
    raise SystemExit('CanliYayinPage duplicated')
print('Build 323 live preflight verification OK')
