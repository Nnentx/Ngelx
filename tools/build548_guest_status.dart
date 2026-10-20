  Widget _guestStatus546(){
    if(widget.yayinSahibi||_guestStage546.isEmpty)return const SizedBox.shrink();
    Widget toggle(IconData icon,String label,bool enabled,VoidCallback action)=>IconButton(
      tooltip:label,onPressed:_guestMediaBusy546||_guestConnecting448?null:action,
      style:IconButton.styleFrom(backgroundColor:enabled?Colors.white:Colors.white12,
        foregroundColor:enabled?const Color(0xFF211D2F):Colors.white),icon:Icon(icon,size:21));
    return Padding(padding:const EdgeInsets.only(bottom:7),child:Container(
      padding:const EdgeInsets.symmetric(horizontal:10,vertical:7),
      decoration:BoxDecoration(color:const Color(0xDC211D2F),borderRadius:BorderRadius.circular(15)),
      child:Column(mainAxisSize:MainAxisSize.min,children:[
        Row(children:[Icon(_guestActive448?Icons.check_circle:Icons.sync,color:_guestActive448?Colors.greenAccent:Colors.white70,size:16),
          const SizedBox(width:6),Expanded(child:Text(_guestStage546,maxLines:2,style:const TextStyle(color:Colors.white,fontSize:11)))]),
        if(_guestActive448)Row(mainAxisAlignment:MainAxisAlignment.center,children:[
          toggle(_guestMicWanted546&&!_guestAudioMuted489?Icons.mic:Icons.mic_off,'Mikrofon',_guestMicWanted546&&!_guestAudioMuted489,()=>unawaited(_guestToggle546(false))),
          const SizedBox(width:10),toggle(_guestCameraWanted546?Icons.videocam:Icons.videocam_off,'Kamera',_guestCameraWanted546,()=>unawaited(_guestToggle546(true))),
          if(_guestCameraWanted546)IconButton(tooltip:'Kamerayı çevir',onPressed:_guestMediaBusy546?null:()=>unawaited(_guestFlip548()),icon:const Icon(Icons.cameraswitch,color:Colors.white,size:21)),
        ])else if(_guestWanted448&&!_guestConnecting448&&_guestConsent548)TextButton(
          onPressed:(){_guestRetries546=0;unawaited(_guestSync448(true));},child:const Text('Tekrar bağlan')),
      ])));
  }
