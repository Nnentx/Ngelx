#!/usr/bin/env python3
"""Read-only regression guards for NgelX inbox avatars and profile reads."""
from pathlib import Path

source = Path(__file__).resolve().parents[1].joinpath("app/lib/main.dart").read_text(encoding="utf-8")
media = source.split("Future<Uint8List> _ngelxAgResmiBaytlariAgdan", 1)[1].split(
    "@immutable\nclass NgelXAgImageProvider", 1
)[0]
inbox = source.split("class _MesajPageState", 1)[1].split("class ArsivSohbetlerPage", 1)[0]

checks = {
    "Image downloads share a Dio client": "_ngelxAgResmiHttp.getUri<List<int>>(" in media,
    "Identical avatar downloads are deduplicated": "_ngelxAgResmiBekleyen[url]=request;" in source,
    "Image requests do not disable HTTP caching": "'Cache-Control':'no-cache" not in media and "'Pragma':'no-cache'" not in media,
    "Inbox profile streams are reused": "stream:_profilAkisi(other)" in inbox,
    "Inbox errors have a retry action": "Kişi bilgisini yeniden yükle" in inbox,
    "Profile errors do not block opening chats": "onTap:()=>sohbetiAc(d.id,SohbetPage(chatId:d.id,digerUid:other,ad:'Kullanıcı',foto:''))" in inbox,
    "Avatar invalidation also clears requests": "_ngelxAgResmiBekleyen.clear();" in source,
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + " | " + name)
if not all(checks.values()):
    raise SystemExit(1)
print(f"PASS | {len(checks)} static regression guards")
