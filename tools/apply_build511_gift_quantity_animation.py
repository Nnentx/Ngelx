#!/usr/bin/env python3
"""Build511 staging-only gift UI. No real money, purchases, or coin ledger."""
from pathlib import Path
FILE=Path('app/lib/live_broadcast_studio.dart')
MARK='// Build511 QA gift event animations'
METHOD=r"""
  // Build511 QA gift event animations.
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _gifts511;
  Timer? _giftTimer511;
  final Set<String> _knownGiftIds511=<String>{};
  bool _giftPrimed511=false;
  String? _giftKey511;
  Map<String,dynamic>? _giftVisible511;
  int sonHediyeAdedi511=0;

  void _watchGifts511(){
    _gifts511=FirebaseFirestore.instance.collection('live_streams')
        .doc(widget.belgeId).collection('comments')
        .orderBy('createdAt',descending:true).limit(50)
        .snapshots(includeMetadataChanges:true).listen((snap){
      if(!_giftPrimed511){
        if(snap.metadata.isFromCache)return;
        _giftPrimed511=true;
        _knownGiftIds511.addAll(snap.docs.map((d)=>d.id));
        return;
      }
      for(final change in snap.docChanges){
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
      }
      if(_knownGiftIds511.length>250){
        _knownGiftIds511.clear();
        _knownGiftIds511.addAll(snap.docs.map((d)=>d.id));
      }
    },onError:(_){});
  }

  Widget _giftScreen511(){
    final gift=_giftVisible511;
    final big=gift?['big']==true;
    return IgnorePointer(ignoring:true,child:AnimatedSwitcher(
      duration:const Duration(milliseconds:320),
      transitionBuilder:(child,a)=>FadeTransition(opacity:a,
        child:ScaleTransition(scale:Tween<double>(begin:.6,end:1)
          .animate(CurvedAnimation(parent:a,curve:Curves.easeOutBack)),child:child)),
      child:gift==null?const SizedBox.shrink():Container(
        key:ValueKey<String>(_giftKey511??'gift'),
        constraints:BoxConstraints(maxWidth:big?320:220),
        padding:EdgeInsets.all(big?19:11),
        decoration:BoxDecoration(color:const Color(0xE02D1E52),
          borderRadius:BorderRadius.circular(22),
          border:Border.all(color:const Color(0xFFFFCD69),width:big?2:1)),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Text(gift['emoji'].toString(),style:TextStyle(fontSize:big?87:45)),
          Text(gift['name'].toString()+' ×'+gift['quantity'].toString(),
            style:TextStyle(fontSize:big?19:14,color:Colors.white,fontWeight:FontWeight.w900)),
          Text(gift['sender'].toString()+' gönderdi',
            maxLines:1,overflow:TextOverflow.ellipsis,
            style:const TextStyle(color:Colors.white70,fontSize:12)),
        ]),
      ),
    ));
  }
"""
def one(s,a,b,name):
    count=s.count(a)
    if count!=1:raise RuntimeError(f'Build511 {name}: {count} matches')
    return s.replace(a,b,1)

def transform(src):
    if MARK in src:return src
    first=src.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    last=src.index('\nclass _CanliOzetSatiri extends StatelessWidget',first)
    before,part,after=src[:first],src[first:last],src[last:]
    if 'Build510: manual livestream comment scrolling' not in part:
        raise RuntimeError('Build511 runs after Build510 comment UI')
    part=one(part,'  final yorum = TextEditingController();',
             '  final yorum = TextEditingController();\n'+METHOD,'methods')
    part=one(part,'    super.initState();',
             '    super.initState();\n    _watchGifts511();','init gift subscription')
    part=one(part,'    yorum.dispose();',
             '    _gifts511?.cancel();\n    _giftTimer511?.cancel();\n    yorum.dispose();','cleanup')
    if "yama['giftPoints']=gifts.docs.fold<int>(" in part:
        # Build453 replaces the heartbeat counters with aggregate gift docs.
        # Count their quantity separately from N-Puan; do not count animations.
        oldStats="yama['giftPoints']=gifts.docs.fold<int>(0,(a,d)=>a+((d.data()['points'] as num?)?.toInt()??0));"
        newStats=oldStats+"\n        yama['giftCount']=gifts.docs.fold<int>(0,(a,d)=>a+(((d.data()['quantity'] as num?)?.toInt()??1).clamp(1,10).toInt()));"
        part=one(part,oldStats,newStats,'Build453 counted virtual gifts')
    else:
        part=one(part,'        var kalp=0,hediye=0,yorumSayisi=0;',
                 '        var kalp=0,hediye=0,yorumSayisi=0,hediyeAdedi511=0;','legacy live count')
        part=one(part,"          if(v['kind']=='gift')hediye+=(v['points'] as num?)?.toInt()??0;",
                 """          if(v['kind']=='gift'){
            hediye+=(v['points'] as num?)?.toInt()??0;
            hediyeAdedi511+=((v['quantity'] as num?)?.toInt()??1).clamp(1,10).toInt();
          }""",'legacy count event quantity')
        part=one(part,"        yama['giftPoints']=hediye;",
                 "        yama['giftPoints']=hediye;\n        yama['giftCount']=hediyeAdedi511;",'legacy live document tally')
    part=one(part,'      var hediyePuani = 0;',
             '      var hediyePuani = 0;\n      var hediyeAdedi511=0;','end count')
    part=one(part,"          if (data['kind'] == 'gift') hediyePuani += (data['points'] as num?)?.toInt() ?? 0;",
             """          if (data['kind'] == 'gift'){
            hediyePuani+=(data['points'] as num?)?.toInt()??0;
            hediyeAdedi511+=((data['quantity'] as num?)?.toInt()??1).clamp(1,10).toInt();
          }""",'end count events')
    part=one(part,'      sonHediyePuani=hediyePuani;',
             '      sonHediyePuani=hediyePuani;\n      sonHediyeAdedi511=hediyeAdedi511;','end count state')
    part=one(part,"        'giftPoints': hediyePuani,",
             "        'giftPoints': hediyePuani,\n        'giftCount': hediyeAdedi511,",'end count field')
    part=one(part,"            _CanliOzetSatiri(ikon:Icons.card_giftcard_rounded,etiket:'Hediye puanı',deger:'$sonHediyePuani'),",
             """            _CanliOzetSatiri(ikon:Icons.card_giftcard_rounded,etiket:'Hediye adedi',deger:'$sonHediyeAdedi511'),
            _CanliOzetSatiri(ikon:Icons.stars_rounded,etiket:'Hediye puanı',deger:'$sonHediyePuani'),""",'summary count')
    part=one(part,'  Future<void> _hediyeGonder(String ad, String emoji, int puan) async {',
             '  Future<void> _hediyeGonder(String ad, String emoji, int puan,{int adet=1}) async {','gift amount')
    part=one(part,'    if (hediyeGonderiliyor) return;',
             '''    if (hediyeGonderiliyor||adet<1||adet>10) return;
    // Stage-only gate: the QA APK must never write a new gift event to
    // production Firestore unless an explicitly isolated test setup enables it.
    const stagingEnabled=bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false);
    if(!stagingEnabled){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Sanal hediyeler yalnız test ortamında kullanılabilir.')));
      return;
    }''','send bounds and stage-only safety gate')
    gift_start=part.index('  Future<void> _hediyeGonder(')
    gift_end=part.index('  Future<void> _hediyePaneli() async {',gift_start)
    sending=part[gift_start:gift_end]
    sending=one(sending,"      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({",
             """      final giftDoc=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').doc();
      await giftDoc.set({""",'unique id per gift send')
    part=part[:gift_start]+sending+part[gift_end:]
    part=one(part,"        'text': '$emoji $ad',",
             "        'text': '$emoji $ad ×$adet',",'gift text')
    part=one(part,"        'giftEmoji': emoji,\n        'points': puan,",
             "        'giftEmoji': emoji,\n        'quantity': adet,\n        'points': puan*adet,",'quantity in event')
    part=one(part,"Text('$emoji $ad gönderildi • +$puan N-Puan')",
             "Text('$emoji $ad ×$adet gönderildi')",'sent confirmation')
    part=one(part,"      {'ad': 'Gül', 'emoji': '🌹', 'puan': 1},",
             """      {'ad': 'Gül', 'emoji': '🌹', 'puan': 1},
      {'ad': 'Kalp', 'emoji': '❤️', 'puan': 3},
      {'ad': 'Elmas', 'emoji': '💎', 'puan': 15},
      {'ad': 'Ayıcık', 'emoji': '🧸', 'puan': 25},""",'gift catalog')
    part=one(part,"    await showModalBottomSheet<void>(\n      context: context,\n      backgroundColor: const Color(0xFF15151B),",
             """    int amount511=1;
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled:true,
      backgroundColor: const Color(0xFF15151B),""",'gift sheet amount')
    part=one(part,'      builder: (c) => SafeArea(child: Padding(',
             '      builder: (c) => StatefulBuilder(builder:(c,setGiftAmount)=>SafeArea(child: SingleChildScrollView(child:Padding(','stateful count selector')
    part=one(part,"          const Text('Canlı yayını destekle • hediyeler N-Puan kazandırır', style: TextStyle(color: Colors.white60)),",
             """          const Text('QA sanal hediye · gerçek para/coin ödemesi yok',style:TextStyle(color:Colors.white60)),
          Row(children:[
            const Text('Adet',style:TextStyle(color:Colors.white)),
            const Spacer(),
            IconButton(onPressed:amount511<=1?null:()=>setGiftAmount(()=>amount511--),
              icon:const Icon(Icons.remove_circle_outline,color:Colors.white)),
            Text('$amount511',style:const TextStyle(color:Colors.white)),
            IconButton(onPressed:amount511>=10?null:()=>setGiftAmount(()=>amount511++),
              icon:const Icon(Icons.add_circle_outline,color:Colors.white)),
          ]),""",'amount controls')
    part=one(part,"await _hediyeGonder(h['ad'] as String, h['emoji'] as String, h['puan'] as int);",
             "await _hediyeGonder(h['ad'] as String, h['emoji'] as String, h['puan'] as int,adet:amount511);",'send selected amount')
    a=part.index('  Future<void> _hediyePaneli() async {')
    b=part.index('  Future<void> _kalpDegistir() async {',a)
    sheet=one(part[a:b],"      )),\n    );\n  }","      )))),\n    );\n  }",'StatefulBuilder close')
    part=part[:a]+sheet+part[b:]
    # Keep Dart's interpolation in the existing comment renderer.
    dollar=chr(36)
    old=dollar+"{y['giftName']??'N-Hediye'} +"+dollar+"{y['points']??0} N"
    new=dollar+"{y['giftName']??'N-Hediye'} ×"+dollar+"{y['quantity']??1}"
    if old in part:
        part=one(part,old,new,'legacy comment gift quantities')
    elif "final message=y['kind']=='join'" not in part:
        raise RuntimeError("Build511 generated comment text for virtual gifts missing")
    part=one(part,'          if(yayinBitti)Positioned.fill(child:ColoredBox(',
             '          if(!yayinBitti)Positioned.fill(child:Center(child:_giftScreen511())),\n          if(yayinBitti)Positioned.fill(child:ColoredBox(','gift overlay')
    part=one(part,"                const Spacer(),\n                if(!widget.yayinSahibi)IconButton(",
             """                StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
                  builder:(_,s){
                    final n=(s.data?.data()?['giftCount'] as num?)?.toInt()??0;
                    return Text('🎁 $n',style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800));
                  }),
                const Spacer(),
                if(!widget.yayinSahibi)IconButton(""",'gift total badge')
    for required in ('_newCommentChip510()','_yorumYonet(d.id,y)',
                     '_guestRail488()','_kalpDegistir()',
                     "'giftCount'","_giftScreen511()"):
        if required not in part:raise RuntimeError('Build511 protected feature missing '+required)
    result=before+part+after
    if result.count(MARK)!=1:raise RuntimeError('Build511 marker duplicate')
    return result

if __name__=='__main__':
    orig=FILE.read_text(encoding='utf-8')
    new=transform(orig)
    if new!=orig:FILE.write_text(new,encoding='utf-8')
    print('Build511 QA: gift quantity, count, animation; no coin/payment ledger')
