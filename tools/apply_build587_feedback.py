"""Apply device feedback to the exact reviewed Build586 assembled source."""
from pathlib import Path
import hashlib,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
app=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'app'
if 'version: 1.0.357+587' in (app/'pubspec.yaml').read_text():
 assert (app/'lib/build587_effects.dart').read_bytes()==(root/'tools/build587_effects.dart').read_bytes()
 print('Build587 already applied');raise SystemExit
expected={'lib/build565_ludo.dart': '1074b2bf78d4eedfcd4eb7fcc56b976196594504ec9a2c4c0429a2f7041a7e37', 'lib/build583_feedback.dart': 'aad7a2f7c9a978fa1beac4fc2985d8ad06198eea3810cae873c46d037f5f5abb', 'lib/main.dart': 'e0a152f15a56e93393b3b2381498a615df6c7a3841cbd49ca5d653c2d17ab5cf', 'lib/live_pk.dart': '429f40240295e63ac0dac309cf3bfd8fec13bd0d18aae4f14888d852bce99624', 'lib/live_broadcast_studio.dart': '4020b6071ae91029bb05affd00d16548229676c8c32ee33f100f2705d0eb4d86', 'pubspec.yaml': '2e0d55cb9ed2caa0a542abe8e9c674724535f104e874b1ac70052a8b30b1011f'}
for path,digest in expected.items():
 assert hashlib.sha256((app/path).read_bytes()).hexdigest()==digest, f'Wrong Build586 input: {path}'
patch=root/'tools/build587_app.patch'
subprocess.run(['patch','--batch','--dry-run','-p1','-d',str(app),'-i',str(patch)],check=True)
subprocess.run(['patch','--batch','-p1','-d',str(app),'-i',str(patch)],check=True)
shutil.copyfile(root/'tools/build587_effects.dart',app/'lib/build587_effects.dart')
print('Build587: one accepted roll, horizontal instant gifts, compact chat, hearts, member roles and PK reference layout')
