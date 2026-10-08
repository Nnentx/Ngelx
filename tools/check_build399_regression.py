#!/usr/bin/env python3
"""Build 399 regression checks with explicit failure diagnostics."""
from pathlib import Path
import sys

checks = {
 "app/pubspec.yaml": ["version: 1.0.175+399"],
 "app/lib/main.dart": [
  "defaultValue: '399'", "defaultValue: '1.0.175'",
  "Widget tumIcerigi()", "gelenKutusuIsteginiSonuclandir",
  "Grup Kur +", "grupGorunenAdi", "ngelxsocial.com",
  "Boşluk kullanılamaz", "FilteringTextInputFormatter.allow",
  "Yeni insanları, içerikleri ve grupları keşfet",
  "_kesfetSekmesi(Icons.grid_view_rounded,'Tümü',-1)", "Canlı Yayınlar",
  "Paylaş, keşfet, ilham ver", "_finalUretKart", "_finalUretArac",
  "coverPhotoUrl", "NgelXKapakKonumlandirPage",
  "Kapak Fotoğrafını", "_profilKapakIkon",
  "Daha önceki sohbet geçmişi silinmez.",
  "Bu grupta engellediğin bir kişi var", "private_chat_",
 ],
 "app/lib/story_v66.dart": ["sonrakiVideoKontrol", "dk önce"],
}
failed = []
for filename, markers in checks.items():
    path = Path(filename)
    if not path.is_file():
        failed.append(f"MISSING FILE: {filename}")
        continue
    content = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            failed.append(f"MISSING MARKER: {filename}: {marker!r}")
if failed:
    for message in failed:
        print(f"::error::{message}", flush=True)
    sys.exit(1)
print("Build 399 regression markers OK")
