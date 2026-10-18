#!/usr/bin/env python3
"""Build513 QA: sequential, bounded, server-confirmed live gift animations.

Run AFTER Build511/512 generated source transforms. Existing immutable
Firestore events, virtual gift staging flag, money/coin policy and LiveKit
lifecycle are deliberately unchanged.
"""
from pathlib import Path

FILE=Path('app/lib/live_broadcast_studio.dart')
MARK='// Build513: sequential confirmed gift animation queue'

FIELDS=r"""
  // Build513: sequential confirmed gift animation queue.
  final List<Map<String,dynamic>> _giftQueue513=<Map<String,dynamic>>[];
  Timer? _giftQueueGap513;
  bool _giftTransitioning513=false;

  void _showNextGift513(){
    // Wait for the previous animation to fade out before showing another.
    if(!mounted || _giftVisible511!=null || _giftTransitioning513 ||
        _giftQueue513.isEmpty || yayinBitti || kapatildi)return;
    final next=_giftQueue513.removeAt(0);
    _giftQueueGap513?.cancel();
    _giftTimer511?.cancel();
    final score=(next['points'] as num?)?.toInt()??0;
    setState((){
      _giftKey511=next['eventId'].toString();
      _giftVisible511=next;
    });
    _giftTimer511=Timer(Duration(milliseconds:score>=25?3400:1750),(){
      if(!mounted)return;
      _giftTransitioning513=true;
      setState(()=>_giftVisible511=null);
      _giftQueueGap513=Timer(const Duration(milliseconds:340),(){
        _giftTransitioning513=false;
        if(mounted)_showNextGift513();
      });
    });
  }
"""

OLD_LOOP=r"""      for(final change in snap.docChanges){
        // A local gift appears with pending writes first and is confirmed
        // as modified when the server acknowledges it. Show it after ack
        // on both sender and viewer devices.
        if(change.type==DocumentChangeType.removed)continue;
        final d=change.doc;
        if(d.metadata.hasPendingWrites)continue;
        if(!_knownGiftIds511.add(d.id))continue;
        final event=d.data();
        if(event==null||event['kind']!='gift')continue;
        final pts=(event['points'] as num?)?.toInt()??0;
        if(!mounted)return;
        _giftTimer511?.cancel();
        setState((){
          _giftKey511=d.id;
          _giftVisible511={
            'emoji':(event['giftEmoji']??'🎁').toString(),
            'name':(event['giftName']??'N-Hediye').toString(),
            'sender':(event['username']??'ngelx').toString(),
            'quantity':((event['quantity'] as num?)?.toInt()??1).clamp(1,10),
            'big':pts>=25,
          };
        });
        _giftTimer511=Timer(Duration(milliseconds:pts>=25?3400:1750),(){
          if(mounted&&_giftKey511==d.id)setState(()=>_giftVisible511=null);
        });
      }"""

NEW_LOOP=r"""      // The query is newest-first; enqueue document changes oldest-first
      // so a burst from multiple viewers plays in chronological order.
      for(final change in snap.docChanges.reversed){
        if(change.type==DocumentChangeType.removed)continue;
        final d=change.doc;
        // Local writes are optimistic: never animate an unconfirmed event.
        // Both added and modified events are accepted after backend ack.
        if(d.metadata.hasPendingWrites)continue;
        if(!_knownGiftIds511.add(d.id))continue;
        final event=d.data();
        if(event==null||event['kind']!='gift')continue;
        final pts=(event['points'] as num?)?.toInt()??0;
        final data=<String,dynamic>{
          'eventId':d.id,
          'emoji':(event['giftEmoji']??'🎁').toString(),
          'name':(event['giftName']??'N-Hediye').toString(),
          'sender':(event['username']??'ngelx').toString(),
          'quantity':((event['quantity'] as num?)?.toInt()??1).clamp(1,10).toInt(),
          'big':pts>=25,
          'points':pts,
        };
        if(_giftQueue513.length<32){
          _giftQueue513.add(data);
        }else{
          // Bound memory during extreme bursts. Never discard the Firestore
          // event or change the authoritative giftCount. Summarize overflow
          // animations without claiming every gift was shown individually.
          final last=_giftQueue513.last;
          if(last['summary']==true){
            last['quantity']=((last['quantity'] as num?)?.toInt()??0)+1;
          }else{
            _giftQueue513[_giftQueue513.length-1]=<String,dynamic>{
              'eventId':'gift-burst-'+d.id,
              'emoji':'🎁','name':'Toplu hediyeler',
              'sender':'Birden çok izleyici','quantity':2,
              'big':false,'points':0,'summary':true,
            };
          }
        }
      }
      _showNextGift513();"""

def one(s,old,new,label):
    count=s.count(old)
    if count!=1:raise RuntimeError(f'Build513 {label}: expected one match; found {count}')
    return s.replace(old,new,1)

def transform(source):
    if MARK in source:return source
    a=source.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    b=source.index('\nclass _CanliOzetSatiri extends StatelessWidget',a)
    before,live,after=source[:a],source[a:b],source[b:]
    if '// Build511 QA gift event animations' not in live or '// Build512: paged read-only gift history' not in live:
        raise RuntimeError('Build513 requires both completed Build511 and Build512 transforms')
    live=one(live,'  void _watchGifts511(){',FIELDS+'\n  void _watchGifts511(){','gift queue state and runner')
    live=one(live,OLD_LOOP,NEW_LOOP,'acknowledged gift loop')
    live=one(live,'    _giftTimer511?.cancel();\n    yorum.dispose();',
        """    _giftTimer511?.cancel();
    _giftQueueGap513?.cancel();
    _giftQueue513.clear();
    yorum.dispose();""",'dispose queue timers')
    for guard in (
        'snapshots(includeMetadataChanges:true)',
        'if(d.metadata.hasPendingWrites)continue;',
        "if(!_knownGiftIds511.add(d.id))continue;",
        'snap.docChanges.reversed',
        'if(_giftQueue513.length<32)',
        "last['summary']==true",
        '_giftQueueGap513?.cancel()',
        '_giftScreen511()',
        '_giftHistory512',
        '_newCommentChip510()',
        "'giftCount'",
        "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
        '_guestRail488()',
    ):
        if guard not in live:
            raise RuntimeError('Build513 lost protected feature: '+guard)
    result=before+live+after
    if result.count(MARK)!=1:raise RuntimeError('Build513 duplicated marker')
    return result

if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    updated=transform(original)
    if updated!=original:FILE.write_text(updated,encoding='utf-8')
    print('Build513 QA: sequential acknowledged gift animations, max 32 queued slots, safe overflow summary')
