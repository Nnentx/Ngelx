#!/usr/bin/env python3
"""Build 418: safe stale-password recovery for device account switching.

Keep Firebase sign-in, secure-storage API, limit of five accounts and all
profile/social code. Never trim or print passwords.
"""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class _HesapDegistirPageState extends State<HesapDegistirPage>')
b=s.index('\nclass ',a+len('class _HesapDegistirPageState'))
part=s[a:b]

old="""    var sifre=parola??await guvenliHafiza.read(key:sifreAnahtari(hedefEmail));
    sifre=sifre?.trim();
    if(sifre==null||sifre.isEmpty)sifre=await _sifreSor(hedefEmail);
    if(sifre==null||sifre.length<6)return;"""
new="""    // Passwords are case- and whitespace-sensitive. Never trim a password.
    // Track whether the value came from encrypted local quick-login cache:
    // if Firebase rejects it, remove only that stale value so the next
    // attempt asks for the current password instead of looping forever.
    var kayitliSifreKullanildi=false;
    String? sifre=parola;
    if(sifre==null){
      sifre=await guvenliHafiza.read(key:sifreAnahtari(hedefEmail));
      kayitliSifreKullanildi=sifre!=null&&sifre.isNotEmpty;
    }
    if(sifre==null||sifre.isEmpty){
      sifre=await _sifreSor(hedefEmail);
      kayitliSifreKullanildi=false;
    }
    if(sifre==null||sifre.length<6)return;"""
if part.count(old)!=1:raise SystemExit("Build 418 account switch password handling drift")
part=part.replace(old,new,1)
old="""      if(e.code=='wrong-password'||e.code=='invalid-credential'){
        mesaj='E-posta veya şifre hatalı.';
      }else if(e.code=='user-not-found'){"""
new="""      if(e.code=='wrong-password'||e.code=='invalid-credential'){
        if(kayitliSifreKullanildi){
          // The old encrypted entry is no longer valid. Remove ONLY this
          // account's cached password; keep its email, UID and other accounts.
          try{await guvenliHafiza.delete(key:sifreAnahtari(hedefEmail));}catch(_){}
          mesaj='Kaydedilmiş şifre kabul edilmedi. Geç’e yeniden dokunup güncel şifreni gir.';
        }else{
          mesaj='E-posta veya şifre hatalı.';
        }
      }else if(e.code=='user-not-found'){"""
if part.count(old)!=1:raise SystemExit('Build 418 FirebaseAuthException recovery drift')
part=part.replace(old,new,1)
s=s[:a]+part+s[b:]
p.write_text(s,encoding='utf-8')
print('Build 418: stale cached password recovery and whitespace-safe login applied.')
