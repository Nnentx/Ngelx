from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'app/lib/build565_ludo.dart'
p.write_bytes((ROOT/'tools/build568_ludo.dart').read_bytes())
p=ROOT/'app/lib/main.dart';s=p.read_text();a=s.index('  Future<void> _yeniOlusturMenusu()');b=s.index('  Future<void> sohbetiAc',a);chunk=s[a:b]
chunk=chunk.replace('showDragHandle:true,','showDragHandle:true,\n      isScrollControlled:true,\n      useSafeArea:true,')
chunk=chunk.replace('child:Padding(\n            padding:', 'child:SingleChildScrollView(child:Padding(\n            padding:')
chunk=chunk.replace('            ]),\n          ),','            ]),\n          )),')
p.write_text(s[:a]+chunk+s[b:])
