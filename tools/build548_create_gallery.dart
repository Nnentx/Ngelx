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
