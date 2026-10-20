from pathlib import Path

TAG = '// Build550 bounded Firestore usage'


def once(source, old, new):
    if source.count(old) != 1:
        raise RuntimeError(f'Build550 expected unique anchor: {old[:100]!r}')
    return source.replace(old, new, 1)


def live_source(s):
    if TAG in s:
        return s
    s = once(s, '  int heartbeatTik=0;', '''  int heartbeatTik=0;
  final _totals550=Ngelx550LiveTotals();
  final _reactionTotal550=ValueNotifier<int>(0);
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _totalsSub550;
  bool _totalsReady550=false,_heartbeatBusy550=false;
  DateTime? _heartbeatRetry550;''')
    anchor = "    widget.oda.addListener(_yenile);"
    s = once(s, anchor, '''    if(widget.yayinSahibi){
      _totalsSub550=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId)
        .collection('comments').snapshots(includeMetadataChanges:true).listen((snapshot){
          for(final change in snapshot.docChanges){
            _totals550.apply(change.doc.id,change.type==DocumentChangeType.removed?null:change.doc.data());
          }
          _totalsReady550=!snapshot.metadata.isFromCache&&!snapshot.metadata.hasPendingWrites;
        },onError:(Object error){_totalsReady550=false;});
    }
''' + anchor)
    s = once(s, "        _reactionCounts453[d.doc.id]=count;", "        if(d.type==DocumentChangeType.removed){_reactionCounts453.remove(d.doc.id);}else{_reactionCounts453[d.doc.id]=count;}")
    s = once(s, '      _reactionsReady453=true;', '''      _reactionsReady453=true;
      _reactionTotal550.value=_reactionCounts453.values.fold<int>(0,(a,b)=>a+b);''')
    a = s.index('    if(pkAktifYerel||heartbeatTik%3==0){', s.index('  Future<void> _heartbeatYaz()'))
    b = s.index('    try{\n      if(kapatildi)return;', a)
    s = s[:a] + '''    if(_reactionsReady453)yama['likeCount']=_reactionTotal550.value;
    if(_totalsReady550){
      yama['commentCount']=_totals550.comments;
      yama['giftPoints']=_totals550.points;
      yama['giftCount']=_totals550.gifts;
    }
''' + s[b:]
    s = once(s, "    heartbeatTik++;", '''    if(_heartbeatBusy550||_heartbeatRetry550!=null&&DateTime.now().isBefore(_heartbeatRetry550!))return;
    _heartbeatBusy550=true;
    heartbeatTik++;''')
    s = once(s, "      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).update(yama);\n    }catch(_){}", """      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).update(yama);
    }catch(error){
      if(ngelx549Quota(error))_heartbeatRetry550=DateTime.now().add(const Duration(minutes:2));
    }finally{_heartbeatBusy550=false;}""")
    # Reuse the existing reaction subscription for immediate UI counters.
    s = once(s, "stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),\n                  builder:(_,likesSnap)", "stream:_liveStream448,\n                  builder:(_,likesSnap)")
    s = once(s, """return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').snapshots(),
                      builder:(_,reactionSnap){
                        final liveLikes=reactionSnap.data?.docs.fold<int>(0,
                          (sum,d)=>sum+((d.data()['count'] as num?)?.toInt()??1));
                        final likes=liveLikes??storedLikes;""", """return ValueListenableBuilder<int>(
                      valueListenable:_reactionTotal550,
                      builder:(_,liveLikes,__){
                        final likes=_reactionsReady453?liveLikes:storedLikes;""")
    # Sharing the stable live stream also prevents duplicate policy listeners.
    for prefix in ['_guestAudioPolicySub489=', 'canliDurumAboneligi=']:
        s = once(s, prefix + "FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots().listen(", prefix + '_liveStream448.listen(')
    s = once(s, '    _reactionSub453?.cancel();', '''    _reactionSub453?.cancel();
    _totalsSub550?.cancel();
    _reactionTotal550.dispose();''')
    s = once(s, '    heartbeat=null;\n    if (widget.yayinSahibi) {', '''    heartbeat=null;
    await _totalsSub550?.cancel();_totalsSub550=null;
    if (widget.yayinSahibi) {''')
    # Keep the one-off end-of-broadcast reconciliation. It is not periodic and
    # gives the final summary authoritative totals after pending writes settle.
    return s + '\n' + TAG + '\n'


def pk_source(s):
    if TAG in s:
        return s
    s = once(s, '  Timer? _timer;', '''  Timer? _timer;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _ownSub550;
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _invitesSub550;
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _invites550=[];
  bool _ownReady550=false;
  void _cancelWatches550(){
    _ownSub550?.cancel();_ownSub550=null;
    _invitesSub550?.cancel();_invitesSub550=null;
  }''')
    s = once(s, '_timer?.cancel();unawaited(_drop());}});', '_timer?.cancel();_cancelWatches550();unawaited(_drop());}});')
    s = once(s, '    _timer=Timer.periodic', '''    _ownSub550=_ref.snapshots().listen((snapshot){
      if(_disposed||FirebaseAuth.instance.currentUser?.uid!=_sessionUid)return;
      _own=snapshot.data()??{};_ownReady550=true;unawaited(_sync());
    },onError:(Object error){_ownReady550=false;unawaited(_drop());});
    if(_host){
      _invitesSub550=_db.collection('calls').where('members',arrayContains:_sessionUid).snapshots().listen((snapshot){
        if(_disposed||FirebaseAuth.instance.currentUser?.uid!=_sessionUid)return;
        _invites550=snapshot.docs;unawaited(_sync());
      },onError:(Object error){_invites550=[];});
    }
    _timer=Timer.periodic''')
    s = once(s, '    super.initState();_sessionUid=', '    super.initState();if(widget.ended)return;_sessionUid=')
    s = once(s, '  Future<void> _drop()async{', '''  @override void didUpdateWidget(covariant Ngelx541AudioPk oldWidget){
    super.didUpdateWidget(oldWidget);
    if(widget.ended&&!oldWidget.ended){_timer?.cancel();_cancelWatches550();unawaited(_drop());}
  }
  Future<void> _drop()async{''')
    s = once(s, "      final own=(await _ref.get(const GetOptions(source:Source.server))).data()??<String,dynamic>{};\n      if(_disposed)return;\n      _own=own;", "      if(!_ownReady550||_disposed)return;\n      final own=_own;")
    s = once(s, "        final q=await _db.collection('calls').where('members',arrayContains:_sessionUid).get(const GetOptions(source:Source.server));\n        final candidates=q.docs.where", "        final candidates=_invites550.where")
    s = once(s, '_disposed=true;_timer?.cancel();_auth?.cancel();', '_disposed=true;_timer?.cancel();_auth?.cancel();_cancelWatches550();')
    return s + '\n' + TAG + '\n'


def apply(root=Path('app/lib')):
    main=root/'main.dart'
    s=main.read_text()
    if "import 'build550_live_totals.dart';" not in s:
        s=once(s,"import 'build549_call_policy.dart';", "import 'build549_call_policy.dart';\nimport 'build550_live_totals.dart';")
        main.write_text(s)
    for name,fn in [('live_broadcast_studio.dart',live_source),('build541_audio_pk.dart',pk_source)]:
        path=root/name
        path.write_text(fn(path.read_text()))
    (root/'build550_live_totals.dart').write_text(Path('tools/build550_live_totals.dart').read_text())


if __name__=='__main__':
    import sys
    apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path('app/lib'))
