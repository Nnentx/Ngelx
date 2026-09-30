#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
live=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
pub=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")
checks={
  "version":"version: 1.0.109+328" in pub,
  "build":"defaultValue: '328'" in main,
  "heartbeat":"'lastHeartbeatAt': FieldValue.serverTimestamp()" in live and "Timer? heartbeat" in live,
  "stale filter":"ngelxCanliKaydiTaze" in main and "ngelxCanliKaydiTaze" in live,
  "share robust":"tur:'message'" in live and "basarili=0" in live and "Gönderilemedi • tekrar deneyebilirsin." in live,
  "share readable":"NgelX’te kişi ara" in live and "hintStyle:const TextStyle(color:Colors.black45" in live,
  "dropdown readable":"dropdownColor:Colors.white" in live and "ThemeData.light()" in live,
  "beauty v2":"'skinTone'" in live and "'highlightProtect'" in live and "'shadowLift'" in live,
  "exposure":"getMinExposureOffset" in live and "setExposureOffset" in live,
  "track fallback":"Yayın görüntüsü alınamadı" in live,
  "live share notification":"olayTuru=='live_share'" in main,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(("OK  " if v else "FAIL")+" "+k)
if failed:raise SystemExit("Build 328 verification failed: "+", ".join(failed))
print("Build 328 verification passed.")
