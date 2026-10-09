#!/usr/bin/env python3
"""Build 426: message story-card jump, nonwrapping story name, fast replies.

Patch generated Flutter sources AFTER all previous Build 395-425 steps. Keep
privacy checks, delivery, and the entire existing chat/story data model.
"""
from pathlib import Path

def one(s,old,new,label):
    n=s.count(old)
    if n!=1:raise SystemExit(f'Build426 source drift: {label} ({n} matches)')
    return s.replace(old,new,1)

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

# A story_reply bubble is a real navigable story link, not inert text.
old="""        onTap:sesliOdaPaylasimi
          ? ()=>ngelxSesliPaylasimMesajiniAc(context,v)
          : canliPaylasimi"""
new="""        onTap:sesliOdaPaylasimi
          ? ()=>ngelxSesliPaylasimMesajiniAc(context,v)
          : storyReply
          ? ()=>_hikayeYanitKartiAc(v)
          : canliPaylasimi"""
s=one(s,old,new,'private-message story bubble tap')

entry="  Widget sohbetUstBilgi()=>Padding("
handler="""  Future<void> _hikayeYanitKartiAc(Map<String,dynamic> mesajVerisi)async{
    final id=(mesajVerisi['storyId']??'').toString().trim();
    final kayitliSahip=(mesajVerisi['storyOwnerId']??'').toString().trim();
    if(id.isEmpty||kayitliSahip.isEmpty){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Bu mesajın hikâye bağlantısı bulunamadı.')));
      return;
    }
    try{
      // Do not trust the sender-controlled message: validate against the
      // actual story and expiry before navigating to the private viewer.
      final kayit=await FirebaseFirestore.instance.collection('videos').doc(id)
        .get(const GetOptions(source:Source.server))
        .timeout(const Duration(seconds:10));
      if(!mounted)return;
      final v=kayit.data();
      if(v==null||!ngelxHikayeAktif(v)){
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('Bu hikâye silinmiş veya süresi dolmuş.')));
        return;
      }
      final gercekSahip=(v['ownerId']??'').toString().trim();
      if(gercekSahip.isEmpty||gercekSahip!=kayitliSahip){
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('Hikâye bağlantısı doğrulanamadı.')));
        return;
      }
      final ad=(v['username']??(gercekSahip==widget.digerUid?widget.ad:'')).toString().trim();
      final foto=(v['ownerPhotoUrl']??(gercekSahip==widget.digerUid?widget.foto:'')).toString().trim();
      await Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXHikayeSeriPage(
        ownerUid:gercekSahip,initialStoryId:id,
        kullanici:ad.isEmpty?'Hikâye':ad,fotoUrl:foto,
      )));
    }on FirebaseException catch(e){
      debugPrint('ngelx_story_card_open: '+e.code);
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Hikâye şu anda açılamıyor.')));
    }on TimeoutException{
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Hikâye açılırken bağlantı zaman aşımına uğradı.')));
    }catch(e){
      debugPrint('ngelx_story_card_open: '+e.runtimeType.toString());
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Hikâye açılamadı. Tekrar dene.')));
    }
  }

"""
s=one(s,entry,handler+entry,'private-message story open action')
s=one(s,"defaultValue: '425'","defaultValue: '426'",'app build number')
s=one(s,"defaultValue: '1.0.200'","defaultValue: '1.0.201'",'app build name')
p.write_text(s,encoding='utf-8')

p=Path('app/lib/story_v66.dart')
s=p.read_text(encoding='utf-8')
old="""              Row(children:[
                GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:CircleAvatar(radius:20,backgroundColor:mor,backgroundImage:widget.fotoUrl.isEmpty?null:NgelXAgImageProvider(widget.fotoUrl),child:widget.fotoUrl.isEmpty?Text(widget.kullanici.replaceFirst('@','').isEmpty?'N':widget.kullanici.replaceFirst('@','')[0].toUpperCase()):null),
                ),
                const SizedBox(width:9),
                Expanded(child:GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                    Text(widget.kullanici,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:16)),
                    Text(zamanBilgisi,style:const TextStyle(color:Colors.white70,fontSize:12)),
                  ]),
                )),
                _takipButonu(),
                if(videoMu)IconButton(onPressed:_sesDegistir,icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:_secenekler,icon:const Icon(Icons.more_horiz_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.white,size:32)),
              ]),
              const Spacer(),"""
new="""              // Build426: long names like @ASLANKARDEŞ must never split.
              // Put follow/audio/menu on a separate line to preserve width.
              Row(children:[
                GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:CircleAvatar(radius:20,backgroundColor:mor,backgroundImage:widget.fotoUrl.isEmpty?null:NgelXAgImageProvider(widget.fotoUrl),child:widget.fotoUrl.isEmpty?Text(widget.kullanici.replaceFirst('@','').isEmpty?'N':widget.kullanici.replaceFirst('@','')[0].toUpperCase()):null),
                ),
                const SizedBox(width:9),
                Expanded(child:GestureDetector(
                  onTap:widget.ownerUid.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerUid))),
                  child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
                    Text(widget.kullanici,maxLines:1,softWrap:false,overflow:TextOverflow.ellipsis,
                      style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:16)),
                    Text(zamanBilgisi,maxLines:1,overflow:TextOverflow.ellipsis,
                      style:const TextStyle(color:Colors.white70,fontSize:12)),
                  ]),
                )),
                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.white,size:32)),
              ]),
              Row(mainAxisAlignment:MainAxisAlignment.end,children:[
                _takipButonu(),
                if(videoMu)IconButton(onPressed:_sesDegistir,icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:_secenekler,icon:const Icon(Icons.more_horiz_rounded,color:Colors.white,size:28)),
              ]),
              const Spacer(),"""
s=one(s,old,new,'nonwrapping story header with actions below')

# Active story is already loaded in memory by _yukle. Avoid a redundant
# network read before every reply. Still validate owner and expiry.
old="""      var hedef=widget.ownerUid.trim();
      // The story record, not a possibly stale UI avatar, determines who
      // receives this private response across account switches.
      if(storyId.isNotEmpty){
        final story=await db.collection('videos').doc(storyId)
          .get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:10));
        if(!story.exists)throw StateError('Hikâye artık bulunamıyor.');
        final gercekSahip=(story.data()?['ownerId']??'').toString().trim();
        if(gercekSahip.isNotEmpty)hedef=gercekSahip;
      }"""
new="""      // The displayed series item is a Firestore snapshot that _yukle already
      // retrieved. Avoid an unnecessary second server round trip per reaction.
      final seciliHikaye=belge;
      if(seciliHikaye==null||!ngelxHikayeAktif(seciliHikaye.data())){
        throw StateError('Hikâye artık bulunamıyor veya süresi dolmuş.');
      }
      final hedef=(seciliHikaye.data()['ownerId']??'').toString().trim();
      if(hedef.isEmpty||hedef!=widget.ownerUid.trim()){
        throw StateError('Hikâye sahibi doğrulanamadı.');
      }"""
s=one(s,old,new,'use authenticated loaded story snapshot')

# After the message itself has been safely stored, don't keep the story
# keyboard/progress spinner waiting for an optional preview update.
old="""      asama='sohbet-onizleme';
      try{
        await chat.update({
          'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
          'lastSenderId':ben.uid,
          'updatedAt':FieldValue.serverTimestamp(),
          'unread_$hedef':FieldValue.increment(1),
        }).timeout(const Duration(seconds:8));
      }catch(e){
        debugPrint('ngelx_story_reply_preview: '+e.runtimeType.toString());
      }"""
new="""      // Preview is best effort; success UI is tied to message commit only.
      unawaited(chat.update({
        'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
        'lastSenderId':ben.uid,
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedef':FieldValue.increment(1),
      }).timeout(const Duration(seconds:8)).catchError((Object e){
        debugPrint('ngelx_story_reply_preview: '+e.runtimeType.toString());
      }));"""
s=one(s,old,new,'nonblocking preview after message commit')
p.write_text(s,encoding='utf-8')

p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
s=one(s,'version: 1.0.200+425','version: 1.0.201+426','pubspec version')
p.write_text(s,encoding='utf-8')

print('Build426: story cards open active story, expired links explain; username never wraps; reply preview is nonblocking.')
