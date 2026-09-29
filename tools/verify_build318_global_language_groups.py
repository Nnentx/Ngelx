#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
GROUP=(ROOT/"app/lib/group_quality.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok: raise SystemExit("Build 318 verification failed: "+msg)

req("version: 1.0.99+318" in PUB,"pubspec version")
req("defaultValue: '1.0.99'" in MAIN and "defaultValue: '318'" in MAIN,"runtime version")
req("String lt(String tr,String en" in MAIN,"global UI language helper")
for token in [
    "lt('Grup ayarları','Group settings')",
    "lt('Bildirimleri sessize al','Mute notifications')",
    "lt('Kimler mesaj gönderebilir?','Who can send messages?')",
    "lt('Kimler kişi ekleyebilir?','Who can add people?')",
    "lt('Sohbet üyelerini gör','View chat members')",
    "lt('Davetler ve istekler','Invites and requests')",
    "lt('Sohbet bilgileri','Chat information')",
]:
    req(token in MAIN,token)
req("showGroupStickerPicker(context,lang:uygulamaDili.value)" in MAIN,"sticker sheet gets app language")
req("showGroupMessageInfo(lang:uygulamaDili.value," in MAIN,"message info gets app language")
req("showGroupForwardSheet(lang:uygulamaDili.value," in MAIN,"forward sheet gets app language")
req("String _gl(String lang,String tr,String en)" in GROUP,"group helper language helper")
req("_gl(lang,'Çıkartmalar','Stickers')" in GROUP,"sticker localization")
req("_gl(lang,'Mesaj bilgisi','Message info')" in GROUP,"message info localization")
req("_gl(lang,'Mesajı ilet','Forward message')" in GROUP,"forward localization")
print("Build 318 global group language verification passed.")
