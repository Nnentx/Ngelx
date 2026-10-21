  Set<String> _moderators553=<String>{};
  Timestamp? _myCommentMute553;
  bool get _canModerate553=>widget.yayinSahibi||_moderators553.contains(FirebaseAuth.instance.currentUser?.uid);
  Future<void> _viewerAction553(String uid,String action)async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null||uid.isEmpty||uid==widget.ownerId||uid==me)return;
    if(action=='remove'){
      final yes=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
        title:const Text('Yayından çıkarılsın mı?'),
        content:const Text('Bu kişi bu canlı yayına yeniden giremeyecek.'),
        actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
          FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Çıkar'))]))??false;
      if(!yes)return;
    }
    try{
      final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
      await FirebaseFirestore.instance.runTransaction((tx)async{
        final v=(await tx.get(ref)).data()??<String,dynamic>{};
        final host=v['ownerId']==me;
        final mods=List<String>.from(v['moderatorUids553']??const[]);
        if(!host&&(!mods.contains(me)||action!='remove'||mods.contains(uid)))throw StateError('forbidden');
        if(action=='moderator'||action=='unmoderator'){
          if(!host)throw StateError('forbidden');
          tx.update(ref,{'moderatorUids553':action=='moderator'?FieldValue.arrayUnion([uid]):FieldValue.arrayRemove([uid])});
        }else if(action=='mute5'||action=='unmuteComment'){
          if(!host)throw StateError('forbidden');
          final until=Map<String,dynamic>.from(v['commentMuteUntil553']??const{});
          if(action=='mute5')until[uid]=Timestamp.fromDate(DateTime.now().add(const Duration(minutes:5)));
          else until.remove(uid);
          tx.update(ref,{'commentMuteUntil553':until,'mutedUsers':FieldValue.arrayRemove([uid])});
        }else if(action=='remove'){
          tx.update(ref,{'bannedUsers':FieldValue.arrayUnion([uid])});
        }else{throw StateError('invalid_action');}
      },maxAttempts:3).timeout(const Duration(seconds:12));
      if(mounted)ngelxDurumMesaji(context,
        action=='moderator'?'Moderatör seçildi.':action=='unmoderator'?'Moderatör yetkisi kaldırıldı.':
        action=='mute5'?'Yorumlar 5 dakika susturuldu.':action=='unmuteComment'?'Yorum susturması kaldırıldı.':'Bu yayından çıkarıldı.',tip:'basari');
    }catch(_){if(mounted)ngelxDurumMesaji(context,'İşlem sunucuda doğrulanamadı. Yeniden dene.',tip:'hata');}
  }
  Widget _commentMuteBanner553()=>ValueListenableBuilder<int>(valueListenable:_clock448,builder:(_,__,___){
    final until=_myCommentMute553;
    final seconds=until==null?0:until.toDate().difference(DateTime.now()).inSeconds;
    if(seconds<=0)return const SizedBox.shrink();
    return Padding(padding:const EdgeInsets.all(6),child:Text(
      'Yorum susturması: ${seconds~/60}:${(seconds%60).toString().padLeft(2,'0')}',
      style:const TextStyle(color:Colors.amber,fontWeight:FontWeight.w700)));
  });
