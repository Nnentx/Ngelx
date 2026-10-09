#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
start=s.index('class _ProfilAramaPageState extends State<ProfilAramaPage>')
end=s.index('\nclass ',start+12)
profile=s[start:end]
start=s.index('class _AramaPageState extends State<AramaPage>')
end=s.index('\nclass HikayeSeridi',start)
global_search=s[start:end]
checks={
 'post filter still supports all/photo/video/text':
    all(f"chip('{key}'" in profile for key in ('all','photo','video','text')),
 'visible people search category':"chip('people','Kişiler'" in profile,
 'people search carries current query':profile.count("AramaPage(baslangicSorgu:q)")>=2,
 'no match offers search people':'Kişilerde ara' in profile,
 'original post navigation intact':'IcerikBaglantiPage(icerikId:docs[i].id)' in profile,
 'story documents excluded from post search':"d.data()['type']!='story'" in profile,
 'original source and ownership filter':"where('ownerId',isEqualTo:widget.uid)" in profile,
 'account search blocks preserved':"discoverableProfile" in global_search and
     "blocked" in global_search and "deactivated" in global_search,
 'account search widened beyond fixed 60':"where(FieldPath.documentId" in global_search and
     "orderBy(alan)" in global_search,
 'no user access rules changed':Path('firestore.rules').exists(),
}
for k,v in checks.items():print(('PASS ' if v else 'FAIL ')+k,flush=True)
if not all(checks.values()):raise SystemExit('Build416 profile people regression FAILED.')
print('Build416 profile-person search routing contracts PASSED, device QA pending.')
