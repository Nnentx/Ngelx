#!/usr/bin/env python3
"""Build 420: never claim a pending social request was cancelled when no write succeeded.

No change to Firestore access rules, friend/follow relationship mutations, or
the notification schema. Abort when the upstream patch stack has drifted.
"""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
start=s.index('Future<void> sosyalIstekIptalEt(')
end=s.index('\nbool gidenSosyalIstekBekliyor(',start)
part=s[start:end]

def one(old,new,label):
    global part
    n=part.count(old)
    if n!=1:raise SystemExit(f'Build 420 {label}: expected 1 marker, got {n}')
    part=part.replace(old,new,1)

one("""    if(!n.exists)return;
    veri=n.data()??<String,dynamic>{};""",
"""    if(!n.exists)throw StateError('Geri çekilecek istek bildirimi bulunamadı.');
    veri=n.data()??<String,dynamic>{};""",
'notification source missing')
one("""    if(!r.exists)return;
    veri=r.data()??<String,dynamic>{};""",
"""    if(!r.exists)throw StateError('Geri çekilecek istek bulunamadı.');
    veri=r.data()??<String,dynamic>{};""",
'request source missing')
one("""  if(istekRef!=null){
    try{
      final r=await istekRef.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:6));
      if(r.exists&&r.data()?['status']=='pending'){
        batch.update(istekRef,{
          'status':'cancelled',
          'cancelledAt':FieldValue.serverTimestamp(),
          'updatedAt':FieldValue.serverTimestamp(),
        });
        degisiklik=true;
      }
    }catch(_){}
  }""",
"""  if(istekRef!=null){
    // The outgoing request is the source of truth. A failed server read
    // must bubble to the UI; silently dropping it previously produced
    // false "request cancelled" success messages.
    final r=await istekRef.get(const GetOptions(source:Source.server))
        .timeout(const Duration(seconds:6));
    if(r.exists&&r.data()?['status']=='pending'){
      batch.update(istekRef,{
        'status':'cancelled',
        'cancelledAt':FieldValue.serverTimestamp(),
        'updatedAt':FieldValue.serverTimestamp(),
      });
      degisiklik=true;
    }
  }""",
'authoritative request read')
one("""  if(degisiklik)await batch.commit().timeout(const Duration(seconds:10));
}""",
"""  if(!degisiklik){
    throw StateError('İstek artık beklemede değil veya iptal edilemedi.');
  }
  await batch.commit().timeout(const Duration(seconds:10));
}""",
'only confirm actual committed cancellation')

s=s[:start]+part+s[end:]
p.write_text(s,encoding='utf-8')
print('Build 420: request cancellation now reports success only after a committed change.')
