  Future<void> _viewerJoinPanel497(BuildContext context,String uid,String? status)async{
    var camera548=cameraPreferred;var busy548=false;
    final previewKey=GlobalKey<Ngelx548GuestPreviewState>();
    final invited=status=='invited',pending=status=='pending',accepted=status=='accepted';
    final joined=accepted&&connected548;
    final action=invited?'accept':pending||joined?'reject':accepted?'connect548':'request';
    final label=invited?'Daveti kabul et':joined?'Konukluktan ayrıl':pending?'İsteği iptal et':accepted?'Yayına bağlan':'Katılma isteği gönder';
    await showModalBottomSheet<void>(context:context,isScrollControlled:true,useSafeArea:true,
      isDismissible:true,showDragHandle:true,backgroundColor:const Color(0xFF211D2F),
      builder:(sheet)=>StatefulBuilder(builder:(sheet,refresh)=>SingleChildScrollView(child:Padding(
        padding:EdgeInsets.fromLTRB(20,8,20,20+MediaQuery.viewInsetsOf(sheet).bottom),
        child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.stretch,children:[
          Text(invited?'Yayın daveti':joined?'Konuk olarak bağlı':'Nasıl katılmak istersin?',
            style:const TextStyle(color:Colors.white,fontSize:21,fontWeight:FontWeight.w800)),
          const SizedBox(height:10),
          Text(joined?'Ayrıldığında izleyici olarak kalırsın. Kamera ve mikrofon yayından kesilir.':pending?
            'İsteğin yayıncıya gönderildi; onay bekleniyor.':'Sesli veya görüntülü katılımı sen seç. Onayından önce sesin ve görüntün yayına gitmez.',
            style:const TextStyle(color:Colors.white70,fontSize:13)),
          if(!joined&&!pending)...[
            const SizedBox(height:14),
            Row(children:[
              Expanded(child:ChoiceChip(label:const Text('Sesli'),avatar:const Icon(Icons.mic),selected:!camera548,
                onSelected:busy548?null:(_)=>refresh(()=>camera548=false))),
              const SizedBox(width:12),
              Expanded(child:ChoiceChip(label:const Text('Görüntülü'),avatar:const Icon(Icons.videocam),selected:camera548,
                onSelected:busy548?null:(_)=>refresh(()=>camera548=true))),
            ]),
            const SizedBox(height:10),Ngelx548GuestPreview(key:previewKey,video:camera548),
          ],
          const SizedBox(height:14),
          FilledButton(onPressed:busy548?null:()async{
            refresh(()=>busy548=true);
            await previewKey.currentState?.stop548();
            if(!sheet.mounted)return;
            Navigator.pop(sheet);
            if(joined)onLeaving548?.call();
            if(!joined&&!pending)onCameraPreference?.call(camera548);
            if(action!='connect548'&&context.mounted)await ngelx448GuestAction(context,liveId,ownerUid,uid,action,video:camera548);
          },child:Text(busy548?'Hazırlanıyor…':label)),
          if(invited)TextButton(onPressed:busy548?null:()async{
            refresh(()=>busy548=true);await previewKey.currentState?.stop548();
            if(sheet.mounted)Navigator.pop(sheet);
            if(context.mounted)await ngelx448GuestAction(context,liveId,ownerUid,uid,'reject');
          },child:const Text('Daveti reddet')),
        ])))));
  }
