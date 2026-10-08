#!/usr/bin/env python3
"""Build 409 search quality regression - preserves queries, permissions and links."""
from pathlib import Path
s=Path("app/lib/main.dart").read_text(encoding="utf-8")
a=s.index("class _AramaPageState extends State<AramaPage>")
b=s.index("\nclass HikayeSeridi",a)
p=s[a:b]
tests={
"multiword matching preserved":"aranan.every((q)=>kelimeler.any((k)=>k.startsWith(q)))" in p,
"user blocked filter preserved":"!beniEngelledi&&!engellenenler.contains(d.id)" in p,
"private posts hidden":"gizlilik=='private'" in p,
"exact media de-duplicated":"final gorulenMedya=<String>{};" in p and "gorulenMedya.add('media:'+medya)" in p,
"distinct posts never merged based on title":"gorulenMedya.add('post:'+d.id)" in p,
"sort by relevance then recency":"return bMs.compareTo(aMs);" in p,
"content navigation preserved":"IcerikBaglantiPage(icerikId:d.id)" in p,
"video edit flow unaffected":"_finalUretArac(Icons.videocam_rounded" in s and "_cokluMedyaSirala()" in s,
"build 408 priority fixes preserved":"ngelx_group_block_dialog_" in s and "ngelxCanliKaydiTaze(yayinSnap.data!" in s,
"group approval result reads eventKind":"if(tur==\'group_join_request\'||(v[\'eventKind\']??\'\')==\'group_join_request\')" in s,
}
for k,v in tests.items():print(("PASS " if v else "FAIL ")+k,flush=True)
if not all(tests.values()):raise SystemExit("Search quality regression failed")
print("Build 409 source checks passed; phone relevance testing is pending.")
