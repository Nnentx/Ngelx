#!/usr/bin/env python3
"""Build521 QA: retry staging virtual gifts with the SAME immutable event ID.

This adds no production Firebase rules or LiveKit changes and does not create
coins, debits, balances, or a payment backend. The existing staging feature
flag remains OFF in signed QA builds. Apply AFTER Build511 through Build516.
"""
from pathlib import Path

FILE=Path('app/lib/live_broadcast_studio.dart')
MARK="// Build521: stable gift request ID across uncertain acknowledgements"

def once(src,old,new,label):
    count=src.count(old)
    if count!=1:raise RuntimeError(f"Build521 {label}: expected one anchor, got {count}")
    return src.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    a=src.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    b=src.index('\nclass _CanliOzetSatiri extends StatelessWidget',a)
    left,live,right=src[:a],src[a:b],src[b:]
    for required in (
      "// Build511 QA gift event animations",
      "// Build513: sequential confirmed gift animation queue",
      "// Build512: paged read-only gift history",
      "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
      "      final giftDoc=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').doc();",
      "'quantity': adet,",
      "'points': puan*adet,",
    ):
        if required not in live:raise RuntimeError("Build521 parent not generated: "+required)
    live=once(live,"  bool _giftPrimed511=false;",
      """  bool _giftPrimed511=false;
  // Build521: stable gift request ID across uncertain acknowledgements.
  String? _pendingGiftId521;
  String? _pendingGiftSignature521;""",
      "pending event state")
    start=live.index('  Future<void> _hediyeGonder(')
    stop=live.index('  Future<void> _giftHistory512()',start)
    # Build512 inserts gift history directly before _hediyePaneli(). The
    # send method itself ends immediately before the following helper.
    sending=live[start:stop]
    old="""      final giftDoc=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').doc();
      await giftDoc.set({"""
    new="""      // One user intention retains one unique document ID after an ambiguous
      // network failure. Same action can be retried without double-counting.
      // A deliberate new send after success receives a NEW random ID.
      final signature='${widget.belgeId}|${user.uid}|$ad|$adet';
      final gifts=FirebaseFirestore.instance.collection('live_streams')
          .doc(widget.belgeId).collection('comments');
      final reusable=_pendingGiftSignature521==signature?_pendingGiftId521:null;
      final giftDoc=reusable==null?gifts.doc():gifts.doc(reusable);
      _pendingGiftSignature521=signature;
      _pendingGiftId521=giftDoc.id;
      final alreadyCommitted=await FirebaseFirestore.instance.runTransaction<bool>((tx)async{
        final current=await tx.get(giftDoc);
        if(current.exists){
          final saved=current.data()??<String,dynamic>{};
          // Only this exact authored event may complete an uncertain retry.
          // A collision or a modified record fails closed.
          if(saved['kind']!='gift'||saved['uid']!=user.uid||
             saved['giftName']!=ad||saved['quantity']!=adet||
             saved['points']!=puan*adet){
            throw StateError('virtual_gift_event_mismatch');
          }
          return true;
        }
        tx.set(giftDoc,{"""
    sending=once(sending,old,new,"unique Firestore gift doc")
    oldEnd="""        'createdAt': FieldValue.serverTimestamp(),
      });
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$emoji $ad ×$adet gönderildi')));"""
    newEnd="""        'createdAt': FieldValue.serverTimestamp(),
        });
        return false;
      },maxAttempts:4);
      // The transaction read+create also makes two concurrent retries share
      // one logical result; security rules still forbid editing a gift event.
      _pendingGiftId521=null;
      _pendingGiftSignature521=null;
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text(alreadyCommitted
          ?'$emoji $ad ×$adet daha önce kaydedilmiş; tekrar sayılmadı'
          :'$emoji $ad ×$adet gönderildi')));"""
    sending=once(sending,oldEnd,newEnd,"final transaction and acknowledgment")
    sending=once(sending,
      "const SnackBar(content: Text('Hediye gönderilemedi.'))",
      "const SnackBar(content: Text('Hediye doğrulanamadı. Aynı hediyeyi tekrar deneyebilirsin.'))",
      "unconfirmed retry instructions")
    live=live[:start]+sending+live[stop:]
    if "collection('comments').add(" in sending:raise RuntimeError("unexpected additive write")
    if live.count(MARK)!=1:raise RuntimeError("Build521 duplicate marker")
    return left+live+right

if __name__=='__main__':
    previous=FILE.read_text(encoding='utf-8')
    newer=transform(previous)
    if previous!=newer:FILE.write_text(newer,encoding='utf-8')
    print("Build521 staging-only virtual gifts: immutable transaction, retry reuses one ID; production gifts OFF")
