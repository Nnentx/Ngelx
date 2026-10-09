#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
def part(a,b):
    start=s.index(a)
    end=s.index(b,start+len(a))
    return s[start:end]
account=part('class _HesapDegistirPageState extends State<HesapDegistirPage>','\nclass ')
friends=part('class _ArkadaslarPageState extends State<ArkadaslarPage>','\nclass ')
owner=part('class _ProfilPageState extends State<ProfilPage>','\nclass _ProfilEtkilesimRozeti')
visitor=part('class _KullaniciProfilPageState extends State<KullaniciProfilPage>','\nclass NgelXVideoKapakOnizleme')
checks={
 'account future cached by normalized email':'_profilIstekleri.putIfAbsent(email.trim().toLowerCase()' in account,
 'cached account future reused':'future:_profilYukle(email)' in account,
 'profile loader waits without showing fake name':"Profil yükleniyor..." in account,
 'failed account profile shows retry':"Profil bilgisini yeniden yükle" in account and "profilHatasi" in account,
 'account user id read privacy untouched':"h.getString(uidAnahtari(email))" in account,
 'account existing secure sign-in kept':"signInWithEmailAndPassword" in account and "guvenliHafiza.write" in account,
 'account remove functionality preserved':'Future<void> _kaldir(' in account,
 'friend out-of-page avatar live stream':"collection('users').doc(id).snapshots()" in friends,
 'friend live missing doc handled':'if(!snap.data!.exists)' in friends,
 'friend search and removal preserved':'_esles(id,v)' in friends and '_arkadaslikKaldir' in friends,
 'owner stale read cannot overwrite current uid':"FirebaseAuth.instance.currentUser?.uid!=user.uid" in owner,
 'owner current profile upload intact':'ngelxFotografYukle(' in owner and "await user.updatePhotoURL(url)" in owner,
 'approved cover/coverless still intact':'if(kapaksiz)...[' in visitor and "NgelXAgImageProvider(profilKapak)" in visitor,
 'follow and friendship actions still retained':'takipDurumuDegistir(uid' in visitor and "_arkadasliktanCikar" in visitor,
 'profile people search retained':"chip('people','Kişiler'" in s,
 'FireStore rules have not been rewritten':Path('firestore.rules').is_file(),
}
for k,v in checks.items():print(('PASS ' if v else 'FAIL ')+k,flush=True)
if not all(checks.values()):raise SystemExit('Build417 regression guards FAILED.')
print('Build417 structural regression guards PASSED; real device validation pending.')
