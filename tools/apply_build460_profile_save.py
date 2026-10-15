#!/usr/bin/env python3
"""Build460: mode-only edits must preserve legacy international usernames.

Run after Build459 source transforms. This does not write production Firestore
or change any account/media data; it changes client-side save behavior only.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")

def patch(s):
    if "// Build460 identity-preserving mode save" in s:
        return s
    a=s.index("class _NgelXOnayliProfilDuzenlePageState")
    b=s.index("\nclass ProfilPage extends StatefulWidget",a)
    editor=s[a:b]
    start=editor.index("  Future<void> _kaydet(String kapak)async{")
    end=editor.index("  Future<void> _kapagiKaldir()async{",start)
    prior=editor[start:end]
    guards=[
        "Geçerli ad ve kullanıcı adı gir.",
        "profileViewMode",
        "usernameLower",
        "Kapaklı görünüm için önce bir kapak fotoğrafı ekle.",
    ]
    if any(x not in prior for x in guards):
        raise ValueError("Build460: unknown editor save implementation; refusing unsafe rewrite")

    updated="""  Future<void> _kaydet(String kapak)async{
    if(_kaydediliyor)return;
    // Build460 identity-preserving mode save; do not revalidate legacy username
    // (including names containing Turkish characters) when unchanged.
    final priorAd=widget.ilkAd.trim();
    final priorUsername=widget.ilkKullanici.trim().replaceFirst('@','');
    final typedAd=_ad.text.trim();
    final typedUsername=_kullanici.text.trim().replaceFirst('@','');
    final ad=typedAd.isEmpty?priorAd:typedAd;
    final kullanici=typedUsername.isEmpty?priorUsername:typedUsername;
    final changeName=ad!=priorAd;
    final changeUsername=kullanici!=priorUsername;

    if(changeName&&ad.length<2){
      _hata('Ad en az 2 karakter olmalı.');
      return;
    }
    if(changeUsername&&!RegExp(r'^[a-zA-Z0-9._]{3,20}$').hasMatch(kullanici)){
      _hata('Yeni kullanıcı adı 3-20 karakter ve İngilizce harf, rakam, nokta veya alt çizgi içermeli.');
      return;
    }
    if(_gorunum=='cover'&&kapak.isEmpty){
      _hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.',kapakUyarisi:true);
      return;
    }
    final kayit=<String,dynamic>{
      'profileViewMode':_gorunum,
      'updatedAt':FieldValue.serverTimestamp(),
    };
    if(changeName)kayit['displayName']=ad;
    if(changeUsername){
      kayit['username']=kullanici;
      kayit['usernameLower']=kullanici.toLowerCase();
    }
    if(_bio.text.trim()!=widget.ilkBio.trim())kayit['bio']=_bio.text.trim();
    if(_konum.text.trim()!=widget.ilkKonum.trim())kayit['location']=_konum.text.trim();
    setState(()=>_kaydediliyor=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid)
        .set(kayit,SetOptions(merge:true)).timeout(const Duration(seconds:15));
      if(changeName){
        try{await FirebaseAuth.instance.currentUser?.updateDisplayName(ad);}catch(_){}
      }
      if(mounted)Navigator.pop(context,true);
    }catch(_){
      _hata('Profil kaydedilemedi. Bağlantını kontrol edip tekrar dene.');
    }finally{
      if(mounted)setState(()=>_kaydediliyor=false);
    }
  }
"""
    editor=editor[:start]+updated+editor[end:]
    return s[:a]+editor+s[b:]

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=patch(before)
    if after!=before:MAIN.write_text(after,encoding="utf-8")
    print("Build460: legacy username preserved on cover-mode-only saves.")

if __name__=="__main__":main()
