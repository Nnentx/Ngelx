#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
live=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
pub=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

checks={
  "version":"version: 1.0.110+329" in pub,
  "build":"defaultValue: '329'" in main,
  "reconnect credentials":"participantToken" in live and "serverUrl" in live,
  "three reconnect attempts":"for(var deneme=1;deneme<=3;deneme++)" in live,
  "viewer end state":"CANLI YAYIN SONA ERDİ" in live and "endReason':'host_ended'" in live,
  "camera off state":"Canlı yayın ses ve yorumlarla devam ediyor." in live and "'cameraEnabled':yeni" in live,
  "heartbeat guard":"connectionState==lk.ConnectionState.disconnected" in live,
  "friends followers":"profilVeri['followers']" in live and "profilVeri['friends']" in live,
  "visibility notifications":"gizlilik=='Arkadaşlar'" in live and "gizlilik=='Takipçiler'" in live,
  "ended notification title":"Canlı yayın sona erdi" in main and "_bildirimBasligiDurumlu" in main,
  "ended notification tap":"Bu canlı yayın bitti." in main and "canliHedefi" in main,
  "blocked notification filter":"gonderenVeri['blocked']" in main and "ayar['blocked']" in main,
}

failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(("OK  " if v else "FAIL")+" "+k)
if failed:raise SystemExit("Build 329 verification failed: "+", ".join(failed))
print("Build 329 verification passed.")
