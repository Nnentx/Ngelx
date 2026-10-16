#!/usr/bin/env python3
"""Read-only regression checks on fully generated Build457 Flutter source."""
from pathlib import Path

src=Path(__file__).resolve().parents[1].joinpath("app/lib/main.dart").read_text(encoding="utf-8")
start=src.index("Future<Uint8List> _ngelxAgResmiBaytlari456(String rawUrl) async {")
end=src.index("@immutable\nclass NgelXAgImageProvider",start)
media=src[start:end]
inbox=src.split("class _MesajPageState",1)[1].split("class ArsivSohbetlerPage",1)[0]
checks={
  "Reuse one avatar HTTP client": "_ngelx457AvatarHttp.getUri<List<int>>(" in media,
  "Retain Build456 shared request cache": "_ngelx456ImageRequests.putIfAbsent(" in src,
  "Retain bounded image cache": "_ngelx456ImageBudget=24*1024*1024" in src,
  "Avoid forced HTTP cache bypass": "'Cache-Control':'no-cache" not in media and "'Pragma':'no-cache'" not in media,
  "Retain private media access token fallback": "HttpHeaders.authorizationHeader:'Bearer $token'" in media,
  "Retain UID-bound inbox identity": "inbox-uid457-" in inbox or "inbox-person-" in inbox,
  "Retain inbox profile retry action": "Kişi bilgisi yüklenemedi" in inbox and "Icons.refresh_rounded" in inbox,
}
for label,passed in checks.items():
    print(("PASS" if passed else "FAIL")+" | "+label)
if not all(checks.values()):
    raise SystemExit(1)
print(f"PASS | {len(checks)} generated-source regression checks")
