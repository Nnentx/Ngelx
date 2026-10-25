from pathlib import Path
import math,struct,wave,base64,hashlib
ROOT=Path(__file__).resolve().parents[1]
for source,target in [('build570_ludo.dart','build565_ludo.dart'),('build570_call_lifecycle.dart','build446_call_lifecycle.dart'),('build570_join_policy.dart','build570_join_policy.dart'),('build570_join_sound.dart','build570_join_sound.dart')]:
 (ROOT/'app/lib'/target).write_bytes((ROOT/'tools'/source).read_bytes())
p=ROOT/'app/lib/main.dart';s=p.read_text()
s=s.replace("import 'dart:ui' as ui;", "import 'dart:ui' as ui;\nimport 'build570_join_policy.dart';",1)
s=s.replace("part 'build565_ludo.dart';", "part 'build565_ludo.dart';\npart 'build570_join_sound.dart';",1)
p.write_text(s)
asset=ROOT/'app/assets/ludo570_pawns.png';asset.write_bytes(base64.b64decode((ROOT/'tools/build570_pawns.b64').read_text()))
assert hashlib.sha256(asset.read_bytes()).hexdigest()=='a5f009ba877b678bdd48131bac27f1b61800f7b7d3578f82dc3ed6894f80c5d8'
# Gentle 0.36-second two-note join chime; no session activation or call audio routing changes.
with wave.open(str(ROOT/'app/assets/call_join570.wav'),'wb') as out:
 out.setparams((1,2,24000,0,'NONE','not compressed'))
 samples=[]
 for i in range(8640):
  t=i/24000;f=660 if t<.17 else 880;local=t if t<.17 else t-.17
  env=min(1,local/.015)*max(0,1-local/.19)**2
  samples.append(struct.pack('<h',int(11000*env*math.sin(2*math.pi*f*t))))
 out.writeframes(b''.join(samples))
p=ROOT/'app/pubspec.yaml';s=p.read_text()
for name in ['ludo570_pawns.png','call_join570.wav']:
 if '    - assets/'+name not in s:s=s.replace('  assets:\n','  assets:\n    - assets/'+name+'\n',1)
s=s.replace('version: 1.0.339+569','version: 1.0.340+570');p.write_text(s)
# Performance delta applies to the verified baseline, not a wholesale main.dart replacement.
import re
(ROOT/'app/lib/build570_perf.dart').write_bytes((ROOT/'tools/build570_perf.dart').read_bytes())
p=ROOT/'app/lib/main.dart';s=p.read_text().replace("import 'build570_join_policy.dart';", "import 'build570_join_policy.dart';\nimport 'build570_perf.dart';",1)
a=s.index('void _ngelx464BellegeAl(');b=s.index('bool _ngelx464GuvenilirMedyaHost',a)
s=s[:a]+"void _ngelx464BellegeAl(String url,Uint8List bytes){ngelx570CachePut(_ngelxAgResmiBellek,url,bytes,maxEntries:_ngelxAgResmiBellekSiniri);}\n"+s[b:]
a=s.index('Future<Uint8List> _ngelx464ResmiGetir(');b=s.index('@immutable\nclass NgelXAgImageProvider',a)
s=s[:a]+s[a:b].replace('ui.instantiateImageCodec(bytes)','ui.instantiateImageCodec(bytes,targetWidth:32,allowUpscaling:false)')+s[b:]
pattern=r'(backgroundImage:\s*(?:\w+\.isEmpty\s*\?\s*null\s*:\s*)?)NgelXAgImageProvider\((\w+)\)'
s,count=re.subn(pattern,r'\1ResizeImage(NgelXAgImageProvider(\2),width:384)',s)
print('Bounded avatar decode sites:',count)
a=s.index('  void _aramaSureBaslat(');b=s.index('  Future<void> _izinleriIste()',a)
s=s[:a]+s[a:b].replace('if(mounted)setState((){});','if(mounted&&!kucultuluyor)setState((){});')+s[b:]
p.write_text(s)
