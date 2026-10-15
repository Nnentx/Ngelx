"""Build463 client-only group media and community comment reliability.
Apply after the Build462 runtime source transforms.
"""
from pathlib import Path
COMMUNITY=Path('app/lib/community450.dart')
COMMENTS=Path('app/lib/build455_widgets.dart')
MAIN=Path('app/lib/main.dart')

def one(src,old,new,label):
    if new in src:return src
    if src.count(old)!=1:raise RuntimeError(f'Build463 unexpected {label} anchor: {src.count(old)}')
    return src.replace(old,new,1)

def community(src):
    if '// Build463 normalized community gallery' not in src:
        old="""  Future<void> pick(bool video) async {
    final x = video
        ? await ImagePicker().pickVideo(source: ImageSource.gallery)
        : await ImagePicker().pickImage(source: ImageSource.gallery);
    if (x != null && mounted)
      setState(() {
        media = x;
        type = video ? 'video' : 'image';
      });
  }"""
        new="""  // Build463 normalized community gallery: stable local media staging.
  Future<void> pick(bool video) async {
    if(busy)return;
    try{
      final x=video
        ?await ngelxVideoSec(source:ImageSource.gallery)
        :await ngelxResimSec(source:ImageSource.gallery);
      if(x!=null&&mounted)setState((){media=x;type=video?'video':'image';});
    }catch(e){if(mounted)_communityError450(context,e);}
  }"""
        src=one(src,old,new,'community publish gallery')
        old="""  Future<void> image(bool isCover) async {
    final x = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (x != null && mounted) setState(() => isCover ? cover = x : photo = x);
  }"""
        new="""  Future<void> image(bool isCover) async {
    try{
      final x=await ngelxResimSec(source:ImageSource.gallery);
      if(x!=null&&mounted)setState(()=>isCover?cover=x:photo=x);
    }catch(e){if(mounted)_communityError450(context,e);}
  }"""
        src=one(src,old,new,'community cover gallery')
    src=one(src,'Ngelx455Comments(post:ref,member:member,admin:admin)',
               "Ngelx455Comments(post:ref,member:member,admin:admin,approved:value['status']=='approved')",
               'community comment status')
    return src

def comments(src):
    if '// Build463 comment approve-safe' in src:return src
    src=one(src,
        '  final bool member, admin;\n  const Ngelx455Comments({super.key, required this.post,\n    required this.member, required this.admin});',
        '  final bool member, admin, approved;\n  const Ngelx455Comments({super.key, required this.post,\n    required this.member, required this.admin, required this.approved});',
        'comments constructor')
    a=src.index('  Future<void> send() async {',src.index('class _Ngelx455CommentsState'))
    b=src.index('  Widget comment(',a)
    src=src[:a]+"""  // Build463 comment approve-safe: Firestore rejects comments on pending posts.
  // The profile read is optional, not a prerequisite to posting.
  Future<void> send() async {
    final body=input.text.trim(),me=_communityUid450;
    if(body.isEmpty||sending)return;
    if(!widget.member||!widget.approved){
      _communityError450(context,StateError('Gönderi henüz yayımlanmadığı için yorum yapılamaz.'));
      return;
    }
    final account=FirebaseAuth.instance.currentUser;
    if(account==null||account.isAnonymous||account.uid!=me){
      _communityError450(context,StateError('Yorum yazmak için hesabına giriş yap.'));
      return;
    }
    setState(()=>sending=true);
    try{
      Map<String,dynamic> profile={};
      try{
        final snap=await FirebaseFirestore.instance.collection('users').doc(me)
          .get().timeout(const Duration(seconds:5));
        profile=snap.data()??{};
      }catch(_){}
      if(_communityUid450!=me)return;
      var name=ngelx455ProfileName(profile,
        fallback:(account.displayName??'').trim().isEmpty?'Üye':account.displayName!.trim());
      name=name.trim().isEmpty?'Üye':name.trim();
      if(name.length>100)name=name.substring(0,100);
      var photo=(profile['photoUrl']??'').toString();
      if(photo.length>2048)photo='';
      var reply=replyName.trim();
      if(reply.length>100)reply=reply.substring(0,100);
      await widget.post.collection('comments').add({
        'uid':me,'name':name,'photoUrl':photo,
        'text':body,'replyTo':replyId,'replyName':reply,
        'createdAt':FieldValue.serverTimestamp(),
      });
      if(mounted){
        setState((){input.clear();replyId='';replyName='';});
        ngelx455Status(context,'Yorum gönderildi');
      }
    }catch(e){if(mounted)_communityError450(context,e);}
    finally{if(mounted)setState(()=>sending=false);}
  }
"""+src[b:]
    src=one(src,
        '        if (widget.member) Padding(padding: const EdgeInsets.fromLTRB(16, 8, 12, 12), child: Row(children: [',
        "        if(widget.member&&!widget.approved)const Padding(padding:EdgeInsets.all(14),child:Text('Bu gönderi onay bekliyor. Yorumlar yayımlanınca açılır.')),\n        if(widget.member&&widget.approved) Padding(padding: const EdgeInsets.fromLTRB(16, 8, 12, 12), child: Row(children: [",
        'pending comment UI')
    return src

def main(src):
    if '// Build463 group media diagnostic' in src:return src
    a=src.index('  Future<void> medyaGonder(ImageSource kaynak)async{')
    b=src.index('  Future<void> grupVideoGonder()async{',a)
    piece=src[a:b]
    old="""  Future<void> medyaGonder(ImageSource kaynak)async{
    final x=await ngelxResimSec(source:kaynak,imageQuality:76,maxWidth:1280);
    if(x==null)return;
    await _grupFotografiniGonder(x,kaynak);
  }"""
    new="""  // Build463 group media diagnostic: keep the verified upload URL on retry.
  String _grup463FotoDosya='';
  String _grup463FotoUrl='';
  bool _grup463FotoMesgul=false;
  Future<void> medyaGonder(ImageSource kaynak)async{
    try{
      final x=await ngelxResimSec(source:kaynak,imageQuality:76,maxWidth:1280);
      if(x!=null)await _grupFotografiniGonder(x,kaynak);
    }catch(e){
      if(mounted)ngelxDurumMesaji(context,
        'Galeri/kamera açılamadı: ${ngelxMedyaHataMetni(e)}',tip:'hata');
    }
  }"""
    piece=one(piece,old,new,'group picker')
    a2=piece.index('  Future<void> _grupFotografiniGonder(')
    piece=piece[:a2]+"""  Future<void> _grupFotografiniGonder(XFile x,ImageSource kaynak)async{
    if(_grup463FotoMesgul)return;
    _grup463FotoMesgul=true;
    try{
      String url=_grup463FotoDosya==x.path?_grup463FotoUrl:'';
      if(url.isEmpty){
        final ext=x.name.contains('.')?x.name.split('.').last.toLowerCase():'jpg';
        final yol='groups/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.$ext';
        url=await ngelxFotografYukle(
          dosya:x,kind:'groups',ext:ext,legacyPath:yol,
          onProgress:(sent,total)=>_medyaIlerlemeGuncelle('Fotoğraf yükleniyor',sent,total),
        ).timeout(const Duration(seconds:90));
        _grup463FotoDosya=x.path;
        _grup463FotoUrl=url;
      }
      final sent=await payloadGonder(
        {'type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url},'📷 Fotoğraf');
      if(!sent)throw StateError('Fotoğraf yüklendi; grup mesajı kaydedilemedi.');
      _grup463FotoDosya='';
      _grup463FotoUrl='';
    }catch(e){
      if(!mounted)return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        duration:const Duration(seconds:8),
        content:Text('Grup fotoğrafı gönderilemedi: ${ngelxMedyaHataMetni(e)}'),
        action:SnackBarAction(label:'Tekrar dene',
          onPressed:()=>unawaited(_grupFotografiniGonder(x,kaynak))),
      ));
    }finally{
      _grup463FotoMesgul=false;
      _medyaIlerlemeBitir();
    }
  }
"""
    src=src[:a]+piece+src[b:]
    a=src.index('  Future<bool> payloadGonder(');b=src.index('  Future<void> gonder()async{',a)
    piece=src[a:b]
    piece=one(piece,
        "    }catch(_){\n      if(!sessizHata&&mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gönderilemedi.')));\n      return false;",
        "    }catch(e){\n      if(!sessizHata&&mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Mesaj gönderilemedi: ${ngelxMedyaHataMetni(e)}')));\n      return false;",
        'group Firestore permission reason')
    return src[:a]+piece+src[b:]

def run():
    for file,transform in [(COMMUNITY,community),(COMMENTS,comments),(MAIN,main)]:
        src=file.read_text(encoding='utf-8')
        dst=transform(src)
        if dst!=src:file.write_text(dst,encoding='utf-8')
    print('Build463 comment, community media and group photo error/retry repairs applied.')

if __name__=='__main__':run()
