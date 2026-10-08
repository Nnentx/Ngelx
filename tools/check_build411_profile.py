#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
owner=s[s.index('class _ProfilPageState extends State<ProfilPage>'):s.index('class _ProfilEtkilesimRozeti')]
visitor=s[s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>'):s.index('class NgelXVideoKapakOnizleme')]
edit=s[s.index('class NgelXOnayliProfilDuzenlePage'):s.index('class ProfilPage extends StatefulWidget')]
checks={
 'owner reads per-user appearance':'profileViewMode' in owner and "veri['profileViewMode']" in owner,
 'coverless owner draws centered avatar':'_onayliKapaksizBaslik()' in owner and 'Stack(alignment:Alignment.center' in owner,
 'owner current cover layout preserved':'_sabitProfilResmi(kapakUrl)' in owner and 'kapakFotografiDuzenle' in owner,
 'visitor respects selected appearance':'final kapaksiz=gorunum' in visitor and 'if(!kapaksiz)...[' in visitor,
 'visitor cover photo uses actual user field':"v['coverPhotoUrl']" in visitor and 'NgelXAgImageProvider(profilKapak)' in visitor,
 'visitor privacy restrictions unchanged':'if (!erisimVar)' in visitor and 'profileViewPermission' in visitor,
 'visitor follow and friendship preserved':'sosyalIstekGonder' in visitor and 'OrtakGruplarPage' in visitor,
 'visitor messages preserved':'profildenMesajAc' in visitor,
 'real edit screen persisted choice':"'profileViewMode':_gorunum" in edit and 'SetOptions(merge:true)' in edit,
 'edit preview works':'_onizlemeAc' in edit and 'Kapaksız sade görünüm' in edit,
 'join date remains immutable':'readOnly:true' in edit and 'widget.katilma' in edit,
 'intro/photo/cover handlers reused':'onTanitim' in edit and 'onFoto' in edit and 'onKapak' in edit,
 'build 408 live fixes present':'ngelxCanliKaydiTaze(yayinSnap.data!' in visitor,
 'build 409 search preserved':'final gorulenMedya=<String>{};' in s,
}
for k,v in checks.items():print(('PASS ' if v else 'FAIL ')+k,flush=True)
if not all(checks.values()):raise SystemExit('Build 411 regression failed')
print('Build 411 profile contract checks passed.')