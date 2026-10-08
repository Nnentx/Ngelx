#!/usr/bin/env python3
"""Build 411: real full-screen approved profile editor, safely updates user record."""
from pathlib import Path
p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")
anchor="class ProfilPage extends StatefulWidget {"
if src.count(anchor)!=1:raise SystemExit("Missing profile page injection point")
widget=r"""
class NgelXOnayliProfilDuzenlePage extends StatefulWidget {
  final String uid, ilkAd, ilkKullanici, ilkBio, ilkKonum, katilma, ilkGorunum, ilkKapakUrl;
  final Future<void> Function() onKapak,onFoto,onTanitim;
  const NgelXOnayliProfilDuzenlePage({
    super.key,required this.uid,required this.ilkAd,required this.ilkKullanici,
    required this.ilkBio,required this.ilkKonum,required this.katilma,
    required this.ilkGorunum,required this.ilkKapakUrl,required this.onKapak,required this.onFoto,required this.onTanitim,
  });
  @override State<NgelXOnayliProfilDuzenlePage> createState()=>_NgelXOnayliProfilDuzenlePageState();
}
class _NgelXOnayliProfilDuzenlePageState extends State<NgelXOnayliProfilDuzenlePage> {
  late final TextEditingController _ad,_kullanici,_bio,_konum;
  late String _gorunum;
  bool _kaydediliyor=false;
  @override void initState(){
    super.initState();
    _ad=TextEditingController(text:widget.ilkAd);
    _kullanici=TextEditingController(text:widget.ilkKullanici.replaceFirst('@',''));
    _bio=TextEditingController(text:widget.ilkBio);
    _konum=TextEditingController(text:widget.ilkKonum);
    _gorunum=widget.ilkGorunum=='coverless'||widget.ilkKapakUrl.isEmpty?'coverless':'cover';
  }
  @override void dispose(){
    _ad.dispose();_kullanici.dispose();_bio.dispose();_konum.dispose();
    super.dispose();
  }
  void _hata(String mesaj){
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(mesaj)));
  }
  Future<void> _kaydet(String kapak)async{
    if(_kaydediliyor)return;
    final ad=_ad.text.trim(),kullanici=_kullanici.text.trim().replaceFirst('@','').replaceAll(' ','');
    if(ad.length<2||kullanici.length<3){_hata('Geçerli ad ve kullanıcı adı gir.');return;}
    if(_gorunum=='cover'&&kapak.isEmpty){_hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.');return;}
    setState(()=>_kaydediliyor=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid).set({
        'displayName':ad,'username':kullanici,
        'bio':_bio.text.trim(),'location':_konum.text.trim(),
        'profileViewMode':_gorunum,
        'updatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:15));
      try{await FirebaseAuth.instance.currentUser?.updateDisplayName(ad);}catch(_){}
      if(mounted)Navigator.pop(context,true);
    }catch(_){
      _hata('Profil kaydedilemedi. Bağlantını kontrol edip tekrar dene.');
    }finally{
      if(mounted)setState(()=>_kaydediliyor=false);
    }
  }
  Future<void> _kapagiKaldir()async{
    if(_kaydediliyor)return;
    final onay=await showDialog<bool>(context:context,builder:(d)=>AlertDialog(
      backgroundColor:Colors.white,
      title:const Text('Kapak fotoğrafını kaldır?'),
      content:const Text('Profilin sade kapaksız görünüme geçecek. İstersen yeniden kapak ekleyebilirsin.'),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(d,false),child:const Text('Vazgeç')),
        TextButton(onPressed:()=>Navigator.pop(d,true),child:const Text('Kaldır',style:TextStyle(color:Colors.red))),
      ],
    ))??false;
    if(!onay||!mounted)return;
    setState(()=>_kaydediliyor=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid).set({
        'coverPhotoUrl':'','coverPhotoY':0.0,'profileViewMode':'coverless',
        'updatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:15));
      if(mounted)setState(()=>_gorunum='coverless');
    }catch(_){_hata('Kapak fotoğrafı kaldırılamadı.');}
    finally{if(mounted)setState(()=>_kaydediliyor=false);}
  }
  Widget _secenek(String ad,String aciklama,String mode,String cover){
    final secili=_gorunum==mode;
    return Expanded(child:InkWell(
      onTap:_kaydediliyor?null:()=>setState(()=>_gorunum=mode),
      borderRadius:BorderRadius.circular(16),
      child:Container(
        padding:const EdgeInsets.all(10),height:122,
        decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(16),
          border:Border.all(color:secili?const Color(0xFF8438F6):const Color(0xFFE4E0EB),width:secili?2:1)),
        child:Row(children:[
          Icon(secili?Icons.radio_button_checked:Icons.radio_button_unchecked,color:secili?const Color(0xFF7C3AED):Colors.black38,size:17),
          const SizedBox(width:7),
          Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisAlignment:MainAxisAlignment.center,children:[
            Container(height:39,width:55,clipBehavior:Clip.antiAlias,
              decoration:BoxDecoration(color:const Color(0xFFF1EAFE),borderRadius:BorderRadius.circular(8)),
              child:mode=='cover'&&cover.isNotEmpty?Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover):
                Icon(mode=='cover'?Icons.panorama_outlined:Icons.account_circle_rounded,color:const Color(0xFF9680DA),size:30)),
            const SizedBox(height:4),
            Text(ad,maxLines:2,style:const TextStyle(fontWeight:FontWeight.w800,fontSize:11)),
            Text(aciklama,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black45,fontSize:9)),
          ])),
        ]),
      ),
    ));
  }
  Widget _profilKucukOnizleme(String ad,String mode,String cover,String photo){
    final secili=_gorunum==mode;
    return Expanded(child:InkWell(
      onTap:()=>setState(()=>_gorunum=mode),
      borderRadius:BorderRadius.circular(15),
      child:Container(padding:const EdgeInsets.all(7),
        decoration:BoxDecoration(borderRadius:BorderRadius.circular(15),border:Border.all(color:secili?const Color(0xFF883BF8):const Color(0xFFE7E3EE),width:secili?2:1)),
        child:Column(children:[
          SizedBox(height:62,child:Stack(children:[
            if(mode=='cover'&&cover.isNotEmpty)Positioned(left:0,right:0,top:0,height:32,
              child:ClipRRect(borderRadius:BorderRadius.circular(7),child:Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover))),
            Positioned(left:10,top:mode=='cover'?20:8,
              child:CircleAvatar(radius:17,backgroundColor:const Color(0xFFE5D7FF),
                backgroundImage:photo.isNotEmpty?NgelXAgImageProvider(photo):null,
                child:photo.isEmpty?const Icon(Icons.person,color:Color(0xFF8B5CF6),size:15):null)),
            Positioned(left:49,right:0,bottom:12,child:Text(_ad.text,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:10,fontWeight:FontWeight.w800))),
          ])),
          Text(ad,style:TextStyle(color:secili?const Color(0xFF7C3AED):Colors.black54,fontSize:11,fontWeight:FontWeight.w800)),
        ]),
      ),
    ));
  }
  InputDecoration _alan(String baslik)=>InputDecoration(
    labelText:baslik,filled:true,fillColor:Colors.white,
    contentPadding:const EdgeInsets.symmetric(horizontal:14,vertical:13),
    border:OutlineInputBorder(borderRadius:BorderRadius.circular(15),borderSide:const BorderSide(color:Color(0xFFE2DDEC))),
    enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(15),borderSide:const BorderSide(color:Color(0xFFE2DDEC))),
  );
  void _onizlemeAc(String cover,String photo){
    showModalBottomSheet<void>(
      context:context,isScrollControlled:true,showDragHandle:true,backgroundColor:Colors.white,
      builder:(ctx)=>SafeArea(child:Padding(
        padding:const EdgeInsets.fromLTRB(22,6,22,30),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          const Text('Profil önizlemesi',style:TextStyle(fontSize:20,fontWeight:FontWeight.w900)),
          const SizedBox(height:12),
          if(_gorunum=='cover'&&cover.isNotEmpty)ClipRRect(borderRadius:BorderRadius.circular(17),
            child:SizedBox(height:100,width:double.infinity,child:Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover))),
          const SizedBox(height:10),
          CircleAvatar(radius:46,backgroundColor:const Color(0xFFF0E9FD),
            backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
            child:photo.isEmpty?const Icon(Icons.person,color:Color(0xFF8B5CF6),size:35):null),
          const SizedBox(height:9),
          Text(_ad.text,textAlign:TextAlign.center,style:const TextStyle(fontSize:22,fontWeight:FontWeight.w900)),
          Text('@'+_kullanici.text.replaceFirst('@',''),style:const TextStyle(color:Colors.black54)),
          const SizedBox(height:7),
          Text(_bio.text,textAlign:TextAlign.center),
          const SizedBox(height:12),
          Text(_gorunum=='cover'?'Kapaklı görünüm':'Kapaksız sade görünüm',style:const TextStyle(color:Color(0xFF7C3AED),fontWeight:FontWeight.w800)),
          const SizedBox(height:6),
          const Text('Bu önizleme henüz kaydedilmemiş değişikliklerini gösterir.',style:TextStyle(color:Colors.black45,fontSize:12),textAlign:TextAlign.center),
        ]),
      )),
    );
  }
  @override Widget build(BuildContext context){
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(
        backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0,
        title:const Text('Profili Düzenle',style:TextStyle(fontWeight:FontWeight.w900,fontSize:21)),
        centerTitle:true,
        actions:[IconButton(onPressed:_kaydediliyor?null:(){
          final doc=FirebaseFirestore.instance.collection('users').doc(widget.uid);
          doc.get().then((x)=>_kaydet((x.data()?['coverPhotoUrl']??'').toString()));
        },icon:const Icon(Icons.check_circle_rounded,color:Color(0xFF7C3AED),size:29))],
      ),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots(),
        builder:(_,snap){
          final v=snap.data?.data()??const <String,dynamic>{};
          final cover=(v['coverPhotoUrl']??'').toString();
          final photo=(v['photoUrl']??'').toString();
          final intro=(v['introVideoUrl']??'').toString();
          return SingleChildScrollView(
            padding:const EdgeInsets.fromLTRB(17,8,17,18),
            child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
              SizedBox(height:208,child:Stack(clipBehavior:Clip.none,children:[
                Positioned(top:0,left:0,right:0,height:157,child:ClipRRect(
                  borderRadius:BorderRadius.circular(20),
                  child:cover.isNotEmpty?Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover):
                    const ColoredBox(color:Color(0xFFF1EAFE),child:Center(child:Icon(Icons.landscape_rounded,color:Color(0xFFAA94D8),size:44))),
                )),
                Positioned(right:9,top:14,child:Column(children:[
                  FilledButton.icon(onPressed:_kaydediliyor?null:widget.onKapak,
                    style:FilledButton.styleFrom(backgroundColor:Colors.black.withValues(alpha:.7),foregroundColor:Colors.white),
                    icon:const Icon(Icons.camera_alt_rounded,size:16),label:const Text('Kapak fotoğrafını\ndeğiştir',style:TextStyle(fontWeight:FontWeight.w800,fontSize:10))),
                  if(cover.isNotEmpty)TextButton.icon(onPressed:_kaydediliyor?null:_kapagiKaldir,
                    style:TextButton.styleFrom(backgroundColor:Colors.black.withValues(alpha:.65),foregroundColor:Colors.white),
                    icon:const Icon(Icons.delete_outline_rounded,size:16),label:const Text('Kaldır')),
                ])),
                Positioned(left:9,top:76,child:Stack(clipBehavior:Clip.none,children:[
                  Container(padding:const EdgeInsets.all(4),decoration:const BoxDecoration(shape:BoxShape.circle,
                    gradient:LinearGradient(colors:[Color(0xFF1AC5F4),Color(0xFF913EF4)])),
                    child:CircleAvatar(radius:59,backgroundColor:Colors.white,
                      backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
                      child:photo.isEmpty?const Icon(Icons.person_rounded,color:Color(0xFF8B5CF6),size:50):null)),
                  Positioned(right:-4,bottom:-2,child:IconButton.filledTonal(onPressed:_kaydediliyor?null:widget.onFoto,
                    icon:const Icon(Icons.camera_alt_rounded),style:IconButton.styleFrom(backgroundColor:Colors.white,foregroundColor:Colors.black87))),
                ])),
              ])),
              TextField(controller:_ad,maxLength:60,decoration:_alan('Ad Soyad'),textCapitalization:TextCapitalization.words),
              const SizedBox(height:6),
              TextField(controller:_kullanici,maxLength:30,decoration:_alan('Kullanıcı adı')),
              const SizedBox(height:6),
              TextField(controller:_bio,maxLines:3,minLines:2,maxLength:160,decoration:_alan('Biyografi')),
              const SizedBox(height:6),
              Row(children:[
                Expanded(child:TextField(controller:_konum,maxLength:60,decoration:_alan('Konum'))),
                const SizedBox(width:10),
                Expanded(child:TextFormField(initialValue:widget.katilma,readOnly:true,
                  decoration:_alan('Katılma tarihi'),style:const TextStyle(fontSize:12))),
              ]),
              const SizedBox(height:12),
              Container(padding:const EdgeInsets.all(13),
                decoration:BoxDecoration(color:const Color(0xFFF7F3FF),borderRadius:BorderRadius.circular(20),
                  border:Border.all(color:const Color(0xFFECE2FB))),
                child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  const Row(children:[Icon(Icons.visibility_rounded,color:Color(0xFF7C3AED)),SizedBox(width:9),
                    Text('Profil görünümü',style:TextStyle(fontWeight:FontWeight.w900,fontSize:17))]),
                  const SizedBox(height:3),
                  const Text('Profilinin nasıl görüneceğini seç. Bu tercih herkese görünür.',style:TextStyle(color:Colors.black54,fontSize:11)),
                  const SizedBox(height:12),
                  Row(children:[
                    _secenek('Kapaklı görünüm','Kapak fotoğrafı ile', 'cover',cover),
                    const SizedBox(width:8),
                    _secenek('Kapaksız sade görünüm','Daha minimal ve temiz', 'coverless',cover),
                  ]),
                ]),
              ),
              const SizedBox(height:14),
              Container(padding:const EdgeInsets.all(13),
                decoration:BoxDecoration(border:Border.all(color:const Color(0xFFE8E3EF)),borderRadius:BorderRadius.circular(20)),
                child:Row(children:[
                  Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                    const Row(children:[Icon(Icons.video_library_rounded,color:Color(0xFF7C3AED)),SizedBox(width:5),
                      Flexible(child:Text('Tanıtım videosu',style:TextStyle(fontWeight:FontWeight.w900)))]),
                    const SizedBox(height:6),
                    const Text('Kendini daha iyi ifade et, hikâyeni paylaş.',style:TextStyle(color:Colors.black54,fontSize:11)),
                    const SizedBox(height:7),
                    TextButton.icon(onPressed:_kaydediliyor?null:widget.onTanitim,
                      icon:const Icon(Icons.play_circle_fill_rounded,color:Color(0xFF7C3AED),size:16),
                      label:Text(intro.isEmpty?'Tanıtım videosu ekle':'Tanıtım videosunu değiştir',style:const TextStyle(fontSize:10,color:Color(0xFF7C3AED),fontWeight:FontWeight.w800))),
                  ])),
                  const SizedBox(width:6),
                  SizedBox(width:119,height:104,child:ClipRRect(borderRadius:BorderRadius.circular(13),
                    child:intro.isNotEmpty?ProfilTanitimVideoKarti(url:intro):
                      const ColoredBox(color:Color(0xFFF1EAFE),child:Center(child:Icon(Icons.play_circle_outline_rounded,color:Color(0xFF8B5CF6),size:43))))),
                ]),
              ),
              const SizedBox(height:14),
              Container(padding:const EdgeInsets.all(12),decoration:BoxDecoration(
                border:Border.all(color:const Color(0xFFE8E3EF)),borderRadius:BorderRadius.circular(20)),
                child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  const Row(children:[Icon(Icons.visibility_outlined,color:Color(0xFF7C3AED)),SizedBox(width:7),
                    Text('Profili önizle',style:TextStyle(fontWeight:FontWeight.w900,fontSize:16))]),
                  const SizedBox(height:2),
                  const Text('Değişiklikleri kaydetmeden önce nasıl görüneceğini incele.',style:TextStyle(color:Colors.black54,fontSize:11)),
                  const SizedBox(height:10),
                  Row(children:[
                    _profilKucukOnizleme('Kapaklı','cover',cover,photo),
                    const SizedBox(width:10),
                    _profilKucukOnizleme('Kapaksız','coverless',cover,photo),
                  ]),
                ]),
              ),
              const SizedBox(height:19),
              Row(children:[
                Expanded(child:Container(decoration:BoxDecoration(
                  gradient:const LinearGradient(colors:[Color(0xFFA23BFF),Color(0xFF2860FF)]),
                  borderRadius:BorderRadius.circular(16)),
                  child:FilledButton.icon(onPressed:_kaydediliyor?null:()=>_kaydet(cover),
                    style:FilledButton.styleFrom(backgroundColor:Colors.transparent,shadowColor:Colors.transparent,minimumSize:const Size.fromHeight(51)),
                    icon:const Icon(Icons.check_rounded),label:Text(_kaydediliyor?'Kaydediliyor...':'Kaydet',style:const TextStyle(fontWeight:FontWeight.w900))))),
                const SizedBox(width:9),
                Expanded(child:FilledButton.icon(onPressed:()=>_onizlemeAc(cover,photo),
                  style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1EAFE),foregroundColor:const Color(0xFF7C3AED),minimumSize:const Size.fromHeight(51)),
                  icon:const Icon(Icons.visibility_outlined),label:const Text('Önizleme aç',style:TextStyle(fontWeight:FontWeight.w900)))),
              ]),
              const SizedBox(height:12),
            ]),
          );
        },
      ),
    ));
  }
}

"""
src=src.replace(anchor,widget+anchor,1)
src=src.replace("        ilkBio:bio,\n        ilkKonum:konum=='Konum eklenmedi'?'':konum,",
                "        ilkBio:bio,\n        ilkGorunum:profilGorunumu,\n        ilkKapakUrl:kapakUrl,\n        ilkKonum:konum=='Konum eklenmedi'?'':konum,",1)
p.write_text(src,encoding="utf-8")
print("Build 411 approved edit page: cover/photo actions, coverless choice, edit fields, live preview, safe profile mode saving.")
