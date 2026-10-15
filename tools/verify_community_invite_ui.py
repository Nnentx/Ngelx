#!/usr/bin/env python3
"""Read-only regression guards for community invitation and member menus."""
from pathlib import Path

root=Path(__file__).resolve().parents[1]
text=(root/"app/lib/build456_widgets.dart").read_text(encoding="utf-8")
members=text.split("class _Ngelx456MembersState",1)[1].split("Future<void> ngelx456Invite(",1)[0]
picker=text.split("class _Ngelx456ChatPickerState",1)[1].split("Future<void> ngelx456SendInvite(",1)[0]
checks={
    "Role tabs fit without horizontal scrolling": "Kurucu/Yönetici" in members
        and "SingleChildScrollView(\n              scrollDirection: Axis.horizontal," not in members,
    "Founder sorts before admin": "ngelx456RoleOrder(v,a).compareTo(ngelx456RoleOrder(v,b))" in members,
    "Member menu is readable on white background": "'Üye işlemleri'" in members
        and "ThemeData.light()" in members
        and "color:ngelx456Ink" in members,
    "Member menu supports profile and message": "'profile':'Profili gör'" in members
        and "'message':'Mesaj gönder'" in members,
    "Member profile errors are retryable": "Üyeyi yeniden yükle" in members,
    "Invitation picker has distinct heading": "'Topluluğa davet et'" in picker,
    "Invitation picker has readable names": "color:ngelx456Ink,fontSize:15" in picker,
    "Invitation picker has selection checkboxes": "CheckboxListTile(" in picker
        and "selected.contains(uid)" in picker,
    "Invitation flow retains send action": "sohbete gönder" in picker,
    "Invitation flow retains retry action": "Kişiyi yeniden yükle" in picker,
}
for name,passed in checks.items():
    print(("PASS" if passed else "FAIL")+" | "+name)
if not all(checks.values()):
    raise SystemExit(1)
print("All "+str(len(checks))+" static community UI checks passed.")
