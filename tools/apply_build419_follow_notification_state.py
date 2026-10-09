#!/usr/bin/env python3
"""Build 419: keep committed follow/friend state independent of notification delivery.

Build 412-418 routes, request schema, privacy controls and Firestore rules
are preserved. Do not turn post-commit notification errors into UI rollbacks.
"""
from pathlib import Path
p=Path("app/lib/main.dart")
s=p.read_text(encoding="utf-8")

old="""  await batch.commit();
  await FirebaseFirestore.instance.waitForPendingWrites();
  if(!takipte)await uygulamaBildirimiGonder(toUid:hedefUid,fromUid:ben,tur:'friend',metin:'Seni takip etmeye başladı');
}"""
new="""  // Committing BOTH arrays is the authoritative follow result.
  // A notification is best-effort: do not report "follow failed" after
  // the relationship batch has already committed successfully.
  await batch.commit();
  if(!takipte){
    unawaited(uygulamaBildirimiGonder(
      toUid:hedefUid,fromUid:ben,tur:'friend',
      metin:'Seni takip etmeye başladı',
    ).catchError((_){ }));
  }
}"""
if s.count(old)!=1:
    raise SystemExit(f"Build 419 follow commit anchor drift: {s.count(old)}")
s=s.replace(old,new,1)

a=s.index("class _KullaniciProfilPageState extends State<KullaniciProfilPage>")
b=s.index("\nclass NgelXVideoKapakOnizleme",a)
v=s[a:b]
follow="""                        builder:(_,istekSnap){
                          final pendingSnap=istekSnap.data;"""
follow_new="""                        builder:(_,istekSnap){
                          // Until we have read the outgoing request, a pending
                          // follow must not briefly appear as a new 'Follow'.
                          if(me!=null&&!istekSnap.hasData){
                            if(istekSnap.hasError){
                              return const SizedBox(height:46,child:Center(
                                child:Text('Takip durumu alınamadı.',
                                  style:TextStyle(fontSize:11,color:Colors.black54))));
                            }
                            return const SizedBox(height:46,child:Center(
                              child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                          }
                          final pendingSnap=istekSnap.data;"""
if v.count(follow)!=1:
    raise SystemExit(f"Build 419 visitor outgoing follow stream drift: {v.count(follow)}")
v=v.replace(follow,follow_new,1)
friend="""                      builder:(_,istekSnap){
                        final pendingSnap=istekSnap.data;"""
friend_new="""                      builder:(_,istekSnap){
                        // Avoid showing 'Add friend' during the first pending
                        // request snapshot and on a read-permission failure.
                        if(me!=null&&!istekSnap.hasData){
                          if(istekSnap.hasError){
                            return const SizedBox(height:46,child:Center(
                              child:Text('Arkadaşlık durumu alınamadı.',
                                style:TextStyle(fontSize:11,color:Colors.black54))));
                          }
                          return const SizedBox(height:46,child:Center(
                            child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                        }
                        final pendingSnap=istekSnap.data;"""
if v.count(friend)!=1:
    raise SystemExit(f"Build 419 visitor outgoing friend stream drift: {v.count(friend)}")
v=v.replace(friend,friend_new,1)

s=s[:a]+v+s[b:]
p.write_text(s,encoding="utf-8")
print("Build 419: follow commit independent from notification; outgoing request controls await authoritative snapshots.")
