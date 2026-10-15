#!/usr/bin/env python3
"""Build460: unblock profile view-mode saving without mutating unchanged identity.

Applied to CI-generated app/lib/main.dart after the Build459 transform. Existing
user data, URLs, friends, messages, groups and production rules stay untouched.
"""
from pathlib import Path
SOURCE=Path("app/lib/main.dart")

def exactly(s,old,new,label):
    count=s.count(old)
    if count!=1:raise ValueError(f"Build460 {label}: expected 1 anchor, found {count}")
    return s.replace(old,new,1)

def patch(s):
    if "// Build460 save only fields actually edited" in s:return s
    a=s.index("class _NgelXOnayliProfilDuzenlePageState")
    b=s.index("\nclass ProfilPage extends StatefulWidget",a)
    x=s[a:b]
    old="""    final ad=_ad.text.trim(),kullanici=_kullanici.text.trim().replaceFirst('@','').replaceAll(' ','');
    if(ad.length<2||kullanici.length<3){_hata('Geçerli ad ve kullanıcı adı gir.');return;}
    if(_gorunum=='cover'&&kapak.isEmpty){_hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.');return;}
    setState(()=>_kaydediliyor=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid).set({
        'displayName':ad,'username':kullanici,
        'bio':_bio.text.trim(),'location':_konum.text.trim(),
        'profileViewMode':_gorunum,
        'updatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:15));
      try{await FirebaseAuth.instance.currentUser?.updateDisplayName(ad);}catch(_){}
      if(mounted)Navigator.pop(context,true);"""
    new="""    // Build460 save only fields actually edited. A cover-mode change must never
    // rewrite or revalidate an unchanged legacy username/display name.
    final typedAd=_ad.text.trim();
    final typedUsername=_kullanici.text.trim().replaceFirst('@','').replaceAll(' ','');
    final priorAd=widget.ilkAd.trim();
    final priorUsername=widget.ilkKullanici.trim().replaceFirst('@','').replaceAll(' ','');
    final ad=typedAd.isEmpty?priorAd:typedAd;
    final kullanici=typedUsername.isEmpty?priorUsername:typedUsername;
    final identityChanged=ad!=priorAd||kullanici!=priorUsername;
    if(identityChanged&&(ad.length<2||kullanici.length<3)){
      _hata('Ad en az 2, kullanıcı adı en az 3 karakter olmalı.');
      return;
    }
    if(_gorunum=='cover'&&kapak.isEmpty){
      _hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.');
      return;
    }
    final kayit=<String,dynamic>{
      'profileViewMode':_gorunum,
      'updatedAt':FieldValue.serverTimestamp(),
    };
    if(ad!=priorAd)kayit['displayName']=ad;
    if(kullanici!=priorUsername)kayit['username']=kullanici;
    if(_bio.text.trim()!=widget.ilkBio.trim())kayit['bio']=_bio.text.trim();
    if(_konum.text.trim()!=widget.ilkKonum.trim())kayit['location']=_konum.text.trim();
    setState(()=>_kaydediliyor=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid)
        .set(kayit,SetOptions(merge:true)).timeout(const Duration(seconds:15));
      if(ad!=priorAd){
        try{await FirebaseAuth.instance.currentUser?.updateDisplayName(ad);}catch(_){}
      }
      if(mounted)Navigator.pop(context,true);"""
    x=exactly(x,old,new,"editor form save")
    return s[:a]+x+s[b:]

def main():
    before=SOURCE.read_text(encoding="utf-8")
    after=patch(before)
    if after!=before:SOURCE.write_text(after,encoding="utf-8")
    print("Build460: profile display modes can save without rewriting unchanged identity.")

if __name__=="__main__": main()
