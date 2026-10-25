from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def apply():
 p=ROOT/'app/lib/build565_ludo.dart'
 if not p.exists():raise RuntimeError('Restore tested Build567 assembled source first')
 p.write_bytes((ROOT/'tools/build568_ludo.dart').read_bytes())
 for name in ['main.dart','build566_transport.dart']:
  p=ROOT/'app/lib'/name;s=p.read_text().replace('[A-F0-9]{16}', '(?:[0-9]{6}|[A-F0-9]{16})')
  if name=='build566_transport.dart':s=s.replace("body['action']!='create'", "!['create','bot','match'].contains(body['action'])")
  p.write_text(s)
 print('Build568 Ludo delta applied; other application files preserved')
if __name__=='__main__':apply()
