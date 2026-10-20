  // Build546: explicit local preferences; never let a reconnect unmute a user.
  bool _guestMicWanted546=true,_guestCameraWanted546=true;
  bool _guestMediaBusy546=false;
  String _guestStage546='';
  int _guestRetries546=0;
  Timer? _guestRetry546;
  final _guestTiming546=Stopwatch();
  bool _guestAlive546(String uid)=>mounted&&!kapatildi&&!yayinBitti&&
    FirebaseAuth.instance.currentUser?.uid==uid;
  void _guestStageSet546(String value){if(mounted)setState(()=>_guestStage546=value);}
  int _guestMediaEpoch546=0;
  Future<void> _guestMicApply546(String uid,bool enabled)async{
    final local=widget.oda.localParticipant;if(local==null)throw StateError('guest_media_missing');
    final epoch=_guestMediaEpoch546;
    await local.setMicrophoneEnabled(enabled).then((_)async{
      if(enabled&&(!_guestAlive546(uid)||!_guestWanted448||_guestAudioMuted489||epoch!=_guestMediaEpoch546)){
        await local.setMicrophoneEnabled(false);
      }
    }).timeout(const Duration(seconds:8));
  }
  Future<void> _guestCameraApply546(String uid,bool enabled)async{
    final local=widget.oda.localParticipant;if(local==null)throw StateError('guest_media_missing');
    final epoch=_guestMediaEpoch546;
    await local.setCameraEnabled(enabled,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0)).then((_)async{
      if(enabled&&(!_guestAlive546(uid)||!_guestWanted448||!_guestCameraWanted546||epoch!=_guestMediaEpoch546)){
        await local.setCameraEnabled(false);
      }
    }).timeout(const Duration(seconds:8));
  }
  Future<void> _guestStopMedia546()async{
    _guestMediaEpoch546++;
    // Start both shutdowns immediately; one device failure must not skip the other.
    await Future.wait([
      ()async{try{await widget.oda.localParticipant?.setMicrophoneEnabled(false).timeout(const Duration(seconds:3));}catch(_){} }(),
      ()async{try{await widget.oda.localParticipant?.setCameraEnabled(false).timeout(const Duration(seconds:3));}catch(_){} }(),
    ]);
  }
  Future<({bool allowed,bool muted,String room})> _guestVerify546(String uid)async{
    final values=await Future.wait([
      FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).get(const GetOptions(source:Source.server)),
      ngelx448GuestRef(widget.belgeId,uid).get(const GetOptions(source:Source.server)),
    ]).timeout(const Duration(seconds:8));
    final live=values[0].data()??<String,dynamic>{};
    final guest=values[1].data()??<String,dynamic>{};
    final room=(live['roomName']??'').toString();
    final allowed=ngelx546GuestAuthorized(expectedUid:uid,currentUid:FirebaseAuth.instance.currentUser?.uid,
      expectedOwner:widget.ownerId,room:room,currentRoom:widget.oda.name,
      live:live['active']==true,owner:live['ownerId'] as String?,host:guest['hostUid'] as String?,
      guest:guest['guestUid'] as String?,status:guest['status'] as String?);
    return (allowed:allowed,muted:List<String>.from(live['guestAudioMutedUids']??const[]).contains(uid),room:room);
  }
  Future<void> _guestSync448(bool accepted)async{
    final wasWanted=_guestWanted448;
    _guestWanted448=accepted;
    if(!accepted){
      _guestRetry546?.cancel();_guestRetries546=0;
      // Do this even while a pending network operation is still in flight.
      unawaited(_guestStopMedia546());
    }else if(!wasWanted){_guestRetries546=0;}
    if(_guestConnecting448||!mounted||kapatildi||yayinBitti||accepted&&_guestActive448)return;
    if(!accepted){
      await _guestStopMedia546();
      if(mounted)setState((){_guestActive448=false;_guestStage546='';});
      return;
    }
    final uid=FirebaseAuth.instance.currentUser?.uid;if(uid==null)return;
    _guestConnecting448=true;_guestRetry546?.cancel();_guestTiming546..reset()..start();
    _guestStageSet546('Konuk bağlantısı doğrulanıyor…');
    try{
      var state=await _guestVerify546(uid);
      if(!_guestAlive546(uid)||!_guestWanted448)return;
      if(!state.allowed){_guestWanted448=false;await _guestStopMedia546();_guestStageSet546('Konuk izni artık geçerli değil.');return;}
      _guestAudioMuted489=state.muted;
      final permissions=widget.oda.localParticipant?.permissions;
      final reusable=ngelx546CanReuse(connected:widget.oda.connectionState==lk.ConnectionState.connected,
        canPublish:permissions?.canPublish==true,
        sources:permissions?.canPublishSources.map((s)=>s.name).toList()??const[],
        microphone:_guestMicWanted546&&!state.muted,camera:_guestCameraWanted546);
      if(!reusable){
        _guestStageSet546('Konuk bağlantısı kuruluyor…');
        final token=await NgelXLiveKitSource441().fetch(lk.TokenRequestOptions(roomName:state.room,participantIdentity:uid));
        if(!_guestAlive546(uid)||!_guestWanted448)return;
        // Keep watching until the new token is ready; disconnect only if required.
        _liveServer453=token.serverUrl;_liveToken453=token.participantToken;
        await widget.oda.disconnect().timeout(const Duration(seconds:8));
        if(!_guestAlive546(uid)||!_guestWanted448)return;
        await widget.oda.connect(_liveServer453,_liveToken453).then((_)async{
          if(!_guestAlive546(uid)){try{await widget.oda.disconnect();}catch(_){} }
          else if(!_guestWanted448){await _guestStopMedia546();}
        }).timeout(const Duration(seconds:15));
        if(!_guestAlive546(uid)||!_guestWanted448)return;
        state=await _guestVerify546(uid);
        if(!state.allowed){_guestWanted448=false;await _guestStopMedia546();return;}
        _guestAudioMuted489=state.muted;
      }
      if(!_guestAlive546(uid)||!_guestWanted448)return;
      _guestStageSet546('Mikrofon hazırlanıyor…');
      await _guestMicApply546(uid,_guestMicWanted546&&!_guestAudioMuted489);
      if(!_guestAlive546(uid)||!_guestWanted448){await _guestStopMedia546();return;}
      // A slow/failing camera must not hold back a successfully published mic.
      if(mounted)setState((){_guestActive448=true;_guestStage546=_guestCameraWanted546?'Ses hazır · kamera hazırlanıyor…':'Yayındasın · kamera kapalı';});
      try{
        await _guestCameraApply546(uid,_guestCameraWanted546);
        if(!_guestAlive546(uid)||!_guestWanted448){await _guestStopMedia546();return;}
        _guestStageSet546(_guestCameraWanted546?'Konuk bağlantısı hazır':'Yayındasın · kamera kapalı');
      }catch(_){
        // Timeout can complete late: shut down the camera instead of enabling it later.
        _guestCameraWanted546=false;
        try{await widget.oda.localParticipant?.setCameraEnabled(false);}catch(_){}
        _guestStageSet546('Ses hazır · kamera açılamadı, yeniden açabilirsin.');
      }
      _guestRetries546=0;
      debugPrint('Guest546 admission complete in ${_guestTiming546.elapsedMilliseconds}ms; reused=$reusable');
    }catch(_){
      await _guestStopMedia546();
      if(mounted)setState(()=>_guestActive448=false);
      if(_guestAlive546(uid)&&ngelx546ShouldRetry(_guestRetries546,_guestWanted448,true)){
        final delay=1<<_guestRetries546;_guestRetries546++;
        _guestStageSet546('Bağlantı yeniden deneniyor ($_guestRetries546/3)…');
        _guestRetry546=Timer(Duration(seconds:delay),(){if(_guestAlive546(uid)&&_guestWanted448)unawaited(_guestSync448(true));});
      }else if(_guestAlive546(uid)){
        _guestStageSet546('Bağlantı kurulamadı. Tekrar bağlan düğmesini kullan.');
      }
    }finally{
      if(mounted)setState(()=>_guestConnecting448=false);else _guestConnecting448=false;
      _guestTiming546.stop();
      if(_guestAlive546(uid)&&!_guestWanted448){await _guestStopMedia546();if(mounted)setState(()=>_guestActive448=false);}
    }
  }
  Future<void> _guestToggle546(bool camera)async{
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null||!_guestActive448||_guestConnecting448||_guestMediaBusy546)return;
    setState(()=>_guestMediaBusy546=true);
    try{
      final state=await _guestVerify546(uid);
      if(!_guestAlive546(uid)||!_guestWanted448||!state.allowed){await _guestSync448(false);return;}
      _guestAudioMuted489=state.muted;
      if(camera){
        final next=!_guestCameraWanted546;
        if(next&&!(await Permission.camera.request()).isGranted)return;
        if(!_guestAlive546(uid)||!_guestWanted448)return;
        _guestCameraWanted546=next;
        await _guestCameraApply546(uid,next);
      }else{
        if(state.muted){_guestStageSet546('Yayıncı mikrofonunu sessize aldı.');return;}
        final next=!_guestMicWanted546;
        await _guestMicApply546(uid,next);
        _guestMicWanted546=next;
      }
      if(!_guestAlive546(uid)||!_guestWanted448){await _guestStopMedia546();return;}
    }catch(_){await _guestStopMedia546();_guestMicWanted546=false;_guestCameraWanted546=false;_guestStageSet546('Konuk ayarı değiştirilemedi. Tekrar dene.');}
    finally{if(mounted)setState(()=>_guestMediaBusy546=false);}
  }
  Widget _guestStatus546(){
    if(widget.yayinSahibi||(!_guestWanted448&&!_guestActive448&&_guestStage546.isEmpty))return const SizedBox.shrink();
    return Container(key:const ValueKey('guest-status546'),margin:const EdgeInsets.symmetric(horizontal:12,vertical:4),padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
      decoration:BoxDecoration(color:const Color(0xDD151C2B),borderRadius:BorderRadius.circular(14)),
      child:Column(mainAxisSize:MainAxisSize.min,children:[
        Text(_guestStage546,style:const TextStyle(color:Colors.white,fontSize:12),textAlign:TextAlign.center),
        if(_guestActive448)Row(mainAxisSize:MainAxisSize.min,children:[
          IconButton(tooltip:_guestAudioMuted489?'Yayıncı tarafından sessizde':'Konuk mikrofonu',onPressed:_guestMediaBusy546||_guestConnecting448?null:()=>unawaited(_guestToggle546(false)),
            icon:Icon(_guestMicWanted546&&!_guestAudioMuted489?Icons.mic:Icons.mic_off,color:Colors.white)),
          IconButton(tooltip:'Konuk kamerası',onPressed:_guestMediaBusy546||_guestConnecting448?null:()=>unawaited(_guestToggle546(true)),
            icon:Icon(_guestCameraWanted546?Icons.videocam:Icons.videocam_off,color:Colors.white)),
        ])else if(_guestWanted448&&!_guestConnecting448)TextButton(
          onPressed:(){_guestRetries546=0;unawaited(_guestSync448(true));},child:const Text('Tekrar bağlan')),
      ]));
  }
