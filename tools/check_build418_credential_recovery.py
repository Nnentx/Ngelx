#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('class _HesapDegistirPageState extends State<HesapDegistirPage>')
b=s.index('\nclass ',a+len('class _HesapDegistirPageState'))
x=s[a:b]
tests={
 'password is never trimmed':"sifre=sifre?.trim()" not in x,
 'still normalizes email only':"email.trim().toLowerCase()" in x,
 'cached password source tracked':"kayitliSifreKullanildi=true" not in x and
      "kayitliSifreKullanildi=sifre!=null&&sifre.isNotEmpty" in x,
 'bad saved credential invalidated':"if(kayitliSifreKullanildi)" in x and
      "guvenliHafiza.delete(key:sifreAnahtari(hedefEmail))" in x,
 'fresh password requested when needed':"sifre=await _sifreSor(hedefEmail)" in x,
 'only stale cached secret removed':"Kaydedilmiş şifre kabul edilmedi." in x and
      "'hatirlanan_epostalar'" in x and "uidAnahtari(hedefEmail)" in x,
 'real auth maintained':"FirebaseAuth.instance.signInWithEmailAndPassword(" in x,
 'secure local password storage maintained':"await guvenliHafiza.write(key:sifreAnahtari(hedefEmail)" in x,
 'login errors and lockout retained':"too-many-requests" in x and "network-request-failed" in x,
 'other account changes preserved':"future:_profilYukle(email)" in x and
      "Profil yükleniyor..." in x,
 'friend search categories maintained':"chip('people','Kişiler'" in s,
 'profile actions and cover preserved':"OrtakGruplarPage(digerUid:uid)" in s,
}
for name,ok in tests.items():print(('PASS ' if ok else 'FAIL ')+name,flush=True)
if not all(tests.values()):raise SystemExit('Build418 safeguard FAILED.')
print('Build418 password recovery contract PASSED; test on real accounts pending.')
