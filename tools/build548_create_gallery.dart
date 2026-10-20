  Timer? _publishNoticeTimer548;
  ScaffoldFeatureController<SnackBar,SnackBarClosedReason>? _publishNotice548;
  void _dismissPublishNotice548(){
    _publishNoticeTimer548?.cancel();_publishNoticeTimer548=null;
    final notice=_publishNotice548;_publishNotice548=null;
    notice?.close();
  }
  void _showPublishNotice548(){
    _dismissPublishNotice548();
    final messenger=ScaffoldMessenger.of(context);
    messenger.hideCurrentSnackBar();
    final notice=messenger.showSnackBar(SnackBar(
      duration:const Duration(seconds:2),
      behavior:SnackBarBehavior.floating,
      content:Text(lt('Paylaşım yayınlandı ✅','Post published ✅')),
      action:SnackBarAction(label:'Akışa git',onPressed:(){
        _dismissPublishNotice548();
        final ana=context.findAncestorStateOfType<_AnaEkranState>();
        if(ana!=null&&ana.mounted)ana.setState(()=>ana.secili=0);
      }),
    ));
    _publishNotice548=notice;
    // An action can disable SnackBar's automatic timeout with accessibility.
    // Close this owned notice explicitly without changing accessibility settings.
    _publishNoticeTimer548=Timer(const Duration(seconds:2),(){
      if(identical(_publishNotice548,notice))_dismissPublishNotice548();
    });
    unawaited(notice.closed.then((_){
      if(identical(_publishNotice548,notice)){
        _publishNoticeTimer548?.cancel();_publishNoticeTimer548=null;
        _publishNotice548=null;
      }
    }));
  }
  bool _createBusy548=false;
  DateTime _createReady548=DateTime.fromMillisecondsSinceEpoch(0);
  Future<void> _createMediaAction548(Future<void> Function() action)async{
    if(_createBusy548||yukleniyor||DateTime.now().isBefore(_createReady548))return;
    _createBusy548=true;
    if(mounted)setState((){});
    try{await action();}
    finally{
      _createReady548=DateTime.now().add(const Duration(milliseconds:450));
      _createBusy548=false;if(mounted)setState((){});
    }
  }
  Future<void> genelGaleri548()=>_createMediaAction548(()async{
    try{
      final selected=await ngelxSohbetGaleriMedyaSec();
      if(selected==null||!mounted)return;
      final type=ngelxSohbetVideoMu(selected)?'video':'photo';
      if(!await _medyaBoyutuUygun(selected,type)||!mounted)return;
      setState((){tur=type;medya=selected;medyalar=<XFile>[selected];medyaYazisi='';videoBaslangicMs=0;videoBitisMs=0;});
      _taslakDegisti();
    }catch(e){if(mounted)ngelxDurumMesaji(context,_dosyaHataMetni(e),tip:'hata');}
  });
