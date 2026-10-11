"""List remaining direct Turkish Text literals after the Build438 generators.

This is a lower-bound inventory: interpolated strings, helper-fed strings and
Turkish strings without distinctive Turkish characters need a separate review.
User-authored content is never translated by this audit.
"""
import csv
import sys
from pathlib import Path
from apply_build438_screen_locales import tokens

writer=csv.writer(sys.stdout,delimiter='\t')
writer.writerow(['source','line','literal'])
for path in sorted(Path('app/lib').glob('*.dart')):
    source=path.read_text()
    if path.name!='main.dart' and not source.startswith("part of 'main.dart';"):
        continue
    stream=tokens(source)
    for i,(token,start,end) in enumerate(stream[:-2]):
        if token!='Text' or stream[i+1][0]!='(': continue
        text=stream[i+2][0]
        if not text.startswith("'") or '$' in text: continue
        if any(c in text for c in 'şğıçöüŞĞİÇÖÜ'):
            writer.writerow([str(path),source.count('\n',0,start)+1,text[1:-1]])
