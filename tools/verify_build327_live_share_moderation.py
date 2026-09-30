#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
live=(ROOT/"app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
pub=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

checks={
  "version":"version: 1.0.108+327" in pub,
  "build number":"defaultValue: '327'" in main,
  "internal share":"Canlı yayını NgelX’te paylaş" in live and "'liveShare':true" in live,
  "chat schema":"collection('chats').doc(chatId)" in live and "unread_$hedefUid" in live,
  "live notification":"olayTuru:'live_share'" in live,
  "viewer list":"Future<void> _izleyiciListesiniAc()" in live and "_aktifIzleyiciler()" in live,
  "profile header":"Widget _yayinBasligi()" in live and "KullaniciProfilPage(uid:widget.ownerId)" in live,
  "connection badge":"Widget _baglantiRozeti()" in live and "ConnectionQuality.poor" in live,
  "reconnect ui":"Bağlantı yeniden kuruluyor" in live,
  "comment controls":"'commentsEnabled': true" in live and "'slowModeSeconds': 0" in live,
  "comment moderation":"Future<void> _yorumYonet" in live and "pinnedComment" in live and "mutedUsers" in live,
  "safer exposure":"parlaklik:-.015" in live and "b-=.005" in live,
  "keyboard dismiss":"onTapOutside:(_)=>FocusScope.of(context).unfocus()" in live,
  "compact toast":"width:230" in live,
}

failed=[name for name,ok in checks.items() if not ok]
for name,ok in checks.items():
    print(("OK  " if ok else "FAIL")+" "+name)
if failed:
    raise SystemExit("Build 327 verification failed: "+", ".join(failed))
print("Build 327 verification passed.")
