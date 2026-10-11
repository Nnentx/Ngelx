"""Inventory unwrapped Turkish presentation literals without modifying persisted data."""
import json,sys
from pathlib import Path
from apply_build438_screen_locales import tokens,localize
rows=[]
for p in Path('app/lib').glob('*.dart'):
 src=p.read_text()
 if p.name=='main.dart':src=src[src.index('String tercihBasligi'):]
 elif not src.startswith("part of 'main.dart';"):continue
 candidates={t[1:-1] for t,_,_ in tokens(src) if t.startswith(("'",'"')) and '$' not in t and any(c in t for c in 'çğıöşüÇĞİÖŞÜ')}
 converted,_=localize(src,candidates)
 for value in candidates:
  needle='_ngelx438Ui('+json.dumps(value,ensure_ascii=False)+')'
  count=converted.count(needle)-src.count(needle)
  if count:rows.append((p.name,value,count))
output=Path(sys.argv[1] if len(sys.argv)>1 else 'tools/build441_untranslated_inventory.tsv')
output.write_text('file\ttext\toccurrences\n'+'\n'.join('\t'.join(map(str,r)) for r in sorted(rows)))
print(len(rows),'unwrapped Turkish presentation literals remain; interpolated/helper text requires separate review')
