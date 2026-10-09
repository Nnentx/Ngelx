#!/usr/bin/env python3
"""Build 423 generated-source regression guard; device tests still required."""
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('class _MesajPageState extends State<MesajPage>')
b=s.index('\nclass ArsivSohbetlerPage',a)
inbox=s[a:b]
visitor=s[s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>'):s.index('\nclass NgelXVideoKapakOnizleme')]
checks={
    'request list hides legacy duplicate pending sender/type rows':'gorulen.add(from' in inbox,
    'request tab always starts without stale scroll':'ValueKey("ngelx-requests-"+filtre)' in inbox,
    'request sender names legible':'style:const TextStyle(color:Color(0xFF142138),fontSize:15' in inbox,
    'green group kind label':"const Text('Grup',style:TextStyle(color:Color(0xFF138A55)" in inbox,
    'notification red live label':"const Color(0xFFDA233B)" in inbox,
    'notification purple voice label':"const Color(0xFF844AED)" in inbox,
    'real live five tab red badges':"_bildirimAkisi(ben,200)" in inbox and "_sohbetAkisi(ben,200)" in inbox and "const Color(0xFFE62D48)" in inbox,
    'friendship request dialog explicit light theme':"showModalBottomSheet<bool>(" in visitor and visitor.count('builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(')>=2,
    'accept and reject buttons visible':visitor.count("title:const Text('Kabul et',style:TextStyle(color:Colors.black87")>=2 and visitor.count("title:const Text('Reddet',style:TextStyle(color:Colors.black87")>=2,
    'keeps story reply and feed':"class _HikayeGosterPageState" in s and 'class _VideoAkisiState' in s,
    'new version exists':"defaultValue: '423'" in s and 'version: 1.0.198+423' in Path('app/pubspec.yaml').read_text(),
}
for name,ok in checks.items():
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)
if not all(checks.values()):raise SystemExit('Build 423 generated-source protection failed')
print('Build 423 static regression checks passed, device QA still pending')
