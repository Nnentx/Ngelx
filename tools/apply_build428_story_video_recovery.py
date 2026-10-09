#!/usr/bin/env python3
"""Build 428: bound story video initialization and make failures recoverable."""
from pathlib import Path
p=Path('app/lib/story_v66.dart')
s=p.read_text(encoding='utf-8')
def replace_one(old,new):
 global s
 count=s.count(old)
 if count!=1: raise SystemExit(f'Build428 source drift: {old[:65]} ({count})')
 s=s.replace(old,new,1)
replace_one('''      videoKontrol=x;
      await x.initialize();
      if(!mounted||nesil!=medyaNesli)''','''      videoKontrol=x;
      await x.initialize().timeout(const Duration(seconds:12));
      if(!mounted||nesil!=medyaNesli)''')
replace_one('''    }catch(_){
      if(!mounted||nesil!=medyaNesli)return;
      setState(()=>videoHata=true);
      sure.duration=const Duration(seconds:7);''','''    }catch(_){
      // Release a failed or timed-out decoder instead of leaving a spinner.
      final failed=videoKontrol;
      videoKontrol=null;
      if(failed!=null)unawaited(failed.dispose().catchError((Object _) {}));
      if(!mounted||nesil!=medyaNesli)return;
      setState(()=>videoHata=true);
      sure.duration=const Duration(seconds:7);''')
p.write_text(s,encoding='utf-8')
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '427'","defaultValue: '428'"),("defaultValue: '1.0.202'","defaultValue: '1.0.203'")]:
 if s.count(old)!=1:raise SystemExit('version source drift '+old)
 s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
assert s.count('version: 1.0.202+427')==1
p.write_text(s.replace('version: 1.0.202+427','version: 1.0.203+428',1),encoding='utf-8')
print('Build 428 story decoder timeout and recovery applied')
