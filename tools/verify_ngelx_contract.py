#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app" / "lib" / "main.dart"
WORKER = ROOT / "cloudflare" / "worker" / "src" / "index.js"

app = APP.read_text(encoding="utf-8")
worker = WORKER.read_text(encoding="utf-8")

errors = []

# Every media kind sent by the Flutter app must be accepted by the R2 worker.
app_kinds = set(re.findall(r"kind\s*:\s*['\"]([^'\"]+)['\"]", app))
allowed_block = re.search(r"const ALLOWED_KINDS = new Set\(\[(.*?)\]\);", worker, re.S)
if not allowed_block:
    errors.append("R2 worker ALLOWED_KINDS bulunamadı.")
    worker_kinds = set()
else:
    worker_kinds = set(re.findall(r"['\"]([^'\"]+)['\"]", allowed_block.group(1)))
missing = sorted(app_kinds - worker_kinds)
if missing:
    errors.append("R2 worker eksik medya türleri: " + ", ".join(missing))

# New uploads must use the NgelX R2 media service only.
for forbidden in (
    "package:supabase_flutter/supabase_flutter.dart",
    "supa.Supabase.initialize(",
    "supa.Supabase.instance.client.storage",
):
    if forbidden in app:
        errors.append("Eski Supabase çalışma zamanı kodu kaldı: " + forbidden)

# The main profile avatar must directly open the photo editor.
profile_class = app.find("class _ProfilPageState")
if profile_class < 0:
    errors.append("Profil sayfası bulunamadı.")
else:
    profile_tail = app[profile_class:]
    if "onTap: fotografYukle" not in profile_tail:
        errors.append("Profil fotoğrafına dokunma fotografYukle akışına bağlı değil.")
    if "await user.updatePhotoURL(url)" not in profile_tail:
        errors.append("Profil fotoğrafı Firebase Auth photoURL ile senkronize edilmiyor.")
    if "CachedNetworkImage.evictFromCache(eski)" not in profile_tail:
        errors.append("Eski profil fotoğrafı önbellekten temizlenmiyor.")

# Contract tokens for the group experience. These guard accidental regressions.
required_group_tokens = [
    "class _GrupSohbetPageState",
    "grupAramasiBaslat",
    "grupVideoGonder",
    "grupDosyaGonder",
    "grupSesKaydiDegistir",
    "grupKonumGonder",
    "grupKalpBirak",
    "mentionOnerileri",
    "SabitlenenGrupMesajlariPage",
    "GrupMedyaPage",
    "GrupKatilmaIstekleriPage",
    "onlyAdminsCanPost",
    "newMembersSeeHistory",
    "joinApproval",
    "lastReadAt_",
    "typing_",
    "mutedFor",
    "groupPhotoUrl",
]
for token in required_group_tokens:
    if token not in app:
        errors.append("Grup özelliği sözleşmesi eksik: " + token)

# App/worker size contract for group videos and attachments.
if "80*1024*1024" in app and "videos: 80 * 1024 * 1024" not in worker:
    errors.append("Grup video boyutu app/worker arasında uyuşmuyor.")
if "30*1024*1024" in app and "'chat-files': 30 * 1024 * 1024" not in worker:
    errors.append("Grup dosya boyutu app/worker arasında uyuşmuyor.")

if errors:
    print("NgelX contract doğrulaması BAŞARISIZ:")
    for e in errors:
        print(" - " + e)
    sys.exit(1)

print("NgelX contract doğrulaması başarılı.")
print("App medya türleri:", ", ".join(sorted(app_kinds)))
print("Worker medya türleri:", ", ".join(sorted(worker_kinds)))
