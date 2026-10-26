"""Optional rewarded mobile ads assembly: intentionally disabled until real AdMob IDs.
Runs AFTER apply_build575_ludo.py and never touches NgelX screens beyond Ludo lobby.
Requires explicit NGELX_ADMOB_APP_ID and NGELX_ADMOB_REWARDED_UNIT.
"""
from pathlib import Path
import os,re,shutil

root=Path(__file__).resolve().parents[1]
app_id=os.getenv('NGELX_ADMOB_APP_ID','')
unit=os.getenv('NGELX_ADMOB_REWARDED_UNIT','')
if not app_id and not unit:
 print('Rewarded ads disabled: AdMob publisher IDs were not provided')
 raise SystemExit(0)
if not re.fullmatch(r'ca-app-pub-[0-9]{16}~[0-9]{10}',app_id):
 raise RuntimeError('AdMob App ID missing or invalid; stop before build')
if not re.fullmatch(r'ca-app-pub-[0-9]{16}/[0-9]{10}',unit):
 raise RuntimeError('AdMob rewarded Ad Unit ID missing or invalid; stop before build')
if app_id.split('~')[0]!=unit.split('/')[0]:
 raise RuntimeError('AdMob app and rewarded unit must have the same publisher')

main=root/'app/lib/main.dart'
ludo=root/'app/lib/build565_ludo.dart'
manifest=root/'app/android/app/src/main/AndroidManifest.xml'
pubspec=root/'app/pubspec.yaml'
part=root/'app/lib/build575_rewarded_ads.dart'
changes=[
(main,
 ("part 'build565_ludo.dart';",
  "part 'build565_ludo.dart';\npart 'build575_rewarded_ads.dart';")),
(main,
 ("import 'package:flutter/material.dart';",
  "import 'package:flutter/material.dart';\nimport 'package:google_mobile_ads/google_mobile_ads.dart';")),
(ludo,
 (" Future<void> _myStats575()async{",
  """ Future<void> _watchVideo575()async{
  if(busy||giftBusy575)return;
  setState(()=>giftBusy575=true);
  try{
   final message=await Ngelx575RewardedVideo(widget.request??ngelx565LudoRequest).watch();
   if(mounted)setState(()=>giftMessage575=message);
  }finally{if(mounted)setState(()=>giftBusy575=false);}
 }
 Future<void> _myStats575()async{""")),
(ludo,
 ("   OutlinedButton.icon(key:const ValueKey('ludo-profile-stats'),",
  """   OutlinedButton.icon(key:const ValueKey('ludo-rewarded-video'),
    onPressed:busy||giftBusy575?null:_watchVideo575,
    icon:const Icon(Icons.ondemand_video_rounded,size:19),
    label:const Text('Video izle (+30 çip)')),
   OutlinedButton.icon(key:const ValueKey('ludo-profile-stats'),""")),
(pubspec,
 ("  shared_preferences: ^2.5.5",
  "  shared_preferences: ^2.5.5\n  google_mobile_ads: ^9.2.0")),
(manifest,
 ("        <activity\n",
  '''        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="'''+app_id+'''" />
        <activity
''')),
]
# Validate everything before modifying anything; fail rather than corrupt sources.
originals={file:file.read_text(encoding='utf-8') for file,_ in changes}
for file,(old,new) in changes:
 if originals[file].count(old)!=1:
  raise RuntimeError(f'Build575 Ads source mismatch for {file.name}: {old[:70]}')
 pending=originals[file].replace(old,new,1)
 originals[file]=pending
for file,updated in originals.items():
 file.write_text(updated,encoding='utf-8')
shutil.copyfile(root/'tools/build575_rewarded_ads.dart',part)
print('Rewarded AdMob Flutter integration staged with caller-supplied App ID and ad unit')
