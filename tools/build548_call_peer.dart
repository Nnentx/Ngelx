  String? _peerUid548;
  String _peerName548='Bağlanıyor…',_peerPhoto548='';
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _peerSub548;
  String get _callTitle548=>grupAramasi?widget.baslik:_peerName548;
  String get _callPhoto548=>grupAramasi?widget.foto:_peerPhoto548;
  void _syncPeer548(Map<String,dynamic> chat){
    if(grupAramasi||chat['callRoomName']!=widget.roomName)return;
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null)return;
    final peer=ngelx548PeerUid(List<String>.from(chat['members']??const[]),me);
    if(peer==_peerUid548)return;
    _peerSub548?.cancel();_peerUid548=peer;
    if(mounted)setState((){_peerName548='Kişi';_peerPhoto548='';});
    if(peer==null)return;
    _peerSub548=FirebaseFirestore.instance.collection('users').doc(peer).snapshots().listen((snapshot){
      if(!mounted||bitiyor||FirebaseAuth.instance.currentUser?.uid!=me||_peerUid548!=peer)return;
      final profile=snapshot.data()??<String,dynamic>{};
      setState((){
        _peerName548=(profile['displayName']??profile['username']??'Kişi').toString();
        _peerPhoto548=(profile['photoUrl']??'').toString();
      });
      _registerPip543();
    },onError:(_){ });
  }
  bool _speakerBusy548=false;
