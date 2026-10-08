#!/usr/bin/env python3
from pathlib import Path
p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")
src=src.replace("defaultValue: '398'","defaultValue: '399'",1)
src=src.replace("defaultValue: '1.0.174'","defaultValue: '1.0.175'",1)

# Registration: compact logo + username without spaces.
ks=src.index("class _KayitPageState extends State<KayitPage>")
ke=src.index("\nclass ",ks+20)
k=src[ks:ke]
k=k.replace("""            const Logo(),
            const SizedBox(height: 35),""","""            const SizedBox(height:4),
            Center(child:SizedBox(width:112,height:112,child:FittedBox(fit:BoxFit.contain,child:Logo()))),
            const SizedBox(height:14),""",1)
k=k.replace("""            TextField(
              controller: kullanici,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.person_outline),
                hintText: t('username'),
              ),
            ),""","""            TextField(
              controller:kullanici,
              autocorrect:false,
              enableSuggestions:false,
              textCapitalization:TextCapitalization.none,
              inputFormatters:[
                FilteringTextInputFormatter.allow(RegExp(r'[a-zA-Z0-9_.]')),
                LengthLimitingTextInputFormatter(20),
              ],
              onChanged:(v){
                final temiz=v.replaceAll(RegExp(r'\\s+'),'');
                if(temiz!=v)kullanici.value=TextEditingValue(text:temiz,selection:TextSelection.collapsed(offset:temiz.length));
              },
              decoration:InputDecoration(
                prefixIcon:const Icon(Icons.person_outline),
                hintText:t('username'),
                helperText:lt('Boşluk kullanılamaz • harf, sayı, nokta ve _','No spaces • letters, numbers, dot and _'),
              ),
            ),""",1)
src=src[:ks]+k+src[ke:]

# Profile cover fields/load.
ps=src.index("class _ProfilPageState extends State<ProfilPage>")
pe=src.index("\nclass _ProfilEtkilesimRozeti",ps)
prof=src[ps:pe]
prof=prof.replace("""  String fotoUrl = '';
  String tanitimVideoUrl = '';""","""  String fotoUrl = '';
  String kapakUrl = '';
  double kapakY = 0;
  bool kapakYukleniyor=false;
  String tanitimVideoUrl = '';""",1)
prof=prof.replace("""          fotoUrl = (veri['photoUrl'] ?? user.photoURL ?? '').toString();
          tanitimVideoUrl = (veri['introVideoUrl'] ?? '').toString();""","""          fotoUrl = (veri['photoUrl'] ?? user.photoURL ?? '').toString();
          kapakUrl = (veri['coverPhotoUrl'] ?? '').toString();
          kapakY = ((veri['coverPhotoY'] as num?)?.toDouble() ?? 0).clamp(-1.0,1.0);
          tanitimVideoUrl = (veri['introVideoUrl'] ?? '').toString();""",1)

method=r'''
  Future<void> kapakFotografiDuzenle()async{
    final user=aktifKullanici;
    if(user==null||user.isAnonymous||kapakYukleniyor)return;
    final secim=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const ListTile(title:Text('Kapak fotoğrafı',style:TextStyle(fontSize:19,fontWeight:FontWeight.w900)),subtitle:Text('Fotoğrafı seçtikten sonra parmağınla sürükleyerek kadrajı ayarla.')),
        ListTile(leading:const Icon(Icons.photo_library_rounded,color:mor),title:const Text('Galeriden seç'),onTap:()=>Navigator.pop(c,'pick')),
        if(kapakUrl.isNotEmpty)ListTile(leading:const Icon(Icons.tune_rounded,color:mor),title:const Text('Kapağı yeniden konumlandır'),onTap:()=>Navigator.pop(c,'reposition')),
        if(kapakUrl.isNotEmpty)ListTile(leading:const Icon(Icons.delete_outline_rounded,color:Colors.red),title:const Text('Kapak fotoğrafını kaldır',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'remove')),
      ])),
    );
    if(secim==null)return;
    if(secim=='remove'){
      final eski=kapakUrl;
      setState(()=>kapakYukleniyor=true);
      try{
        await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'coverPhotoUrl':'','coverPhotoY':0.0,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
        if(mounted)setState((){kapakUrl='';kapakY=0;});
        if(eski.isNotEmpty)unawaited(ngelxMedyaSil(eski).catchError((_){ }));
      }finally{if(mounted)setState(()=>kapakYukleniyor=false);}
      return;
    }
    if(secim=='reposition'){
      final y=await Navigator.push<double>(context,MaterialPageRoute(builder:(_)=>NgelXKapakKonumlandirPage(imageUrl:kapakUrl,initialY:kapakY)));
      if(y==null||!mounted)return;
      setState(()=>kapakY=y);
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'coverPhotoY':y,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      return;
    }
    final dosya=await ngelxResimSec(source:ImageSource.gallery,imageQuality:88,maxWidth:1920);
    if(dosya==null||!mounted)return;
    final y=await Navigator.push<double>(context,MaterialPageRoute(builder:(_)=>NgelXKapakKonumlandirPage(localFile:File(dosya.path),initialY:0)));
    if(y==null||!mounted)return;
    setState(()=>kapakYukleniyor=true);
    try{
      final uzanti=dosya.name.contains('.')?dosya.name.split('.').last.toLowerCase():'jpg';
      final eski=kapakUrl;
      final url=await ngelxFotografYukle(dosya:dosya,kind:'profile-covers',ext:uzanti,legacyPath:'profile-covers/${user.uid}/${DateTime.now().millisecondsSinceEpoch}.$uzanti');
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'coverPhotoUrl':url,'coverPhotoY':y,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      if(!mounted)return;
      setState((){kapakUrl=url;kapakY=y;});
      if(eski.isNotEmpty&&eski!=url)unawaited(ngelxMedyaSil(eski).catchError((_){ }));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kapak fotoğrafı yüklenemedi: $e')));
    }finally{if(mounted)setState(()=>kapakYukleniyor=false);}
  }

'''
at=prof.index("  Future<void> tanitimVideosuYukle()")
prof=prof[:at]+method+prof[at:]
src=src[:ps]+prof+src[pe:]

# Cover crop/position editor.
insert=src.index("class ProfilPage extends StatefulWidget")
page=r'''
class NgelXKapakKonumlandirPage extends StatefulWidget{
  final File? localFile;
  final String imageUrl;
  final double initialY;
  const NgelXKapakKonumlandirPage({super.key,this.localFile,this.imageUrl='',this.initialY=0});
  @override State<NgelXKapakKonumlandirPage> createState()=>_NgelXKapakKonumlandirPageState();
}
class _NgelXKapakKonumlandirPageState extends State<NgelXKapakKonumlandirPage>{
  late double y;
  @override void initState(){super.initState();y=widget.initialY.clamp(-1.0,1.0);}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(
    backgroundColor:Colors.white,
    appBar:AppBar(title:const Text('Kapak fotoğrafını ayarla',style:TextStyle(fontWeight:FontWeight.w900)),actions:[TextButton(onPressed:()=>Navigator.pop(context,y),child:const Text('Kaydet',style:TextStyle(fontWeight:FontWeight.w900)))]),
    body:SafeArea(child:Column(children:[
      const Padding(padding:EdgeInsets.all(16),child:Text('Fotoğrafı yukarı-aşağı sürükle. Kapak yüksekliği sabit kalır; sadece görünen kadraj değişir.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54))),
      GestureDetector(
        onVerticalDragUpdate:(d)=>setState(()=>y=(y+d.delta.dy/120).clamp(-1.0,1.0)),
        child:Container(
          margin:const EdgeInsets.symmetric(horizontal:16),height:190,width:double.infinity,
          clipBehavior:Clip.antiAlias,
          decoration:BoxDecoration(color:const Color(0xFFF0F1F5),borderRadius:BorderRadius.circular(22)),
          child:widget.localFile!=null
            ?Image.file(widget.localFile!,fit:BoxFit.cover,alignment:Alignment(0,y))
            :NgelXAgResmi(url:widget.imageUrl,fit:BoxFit.cover,alignment:Alignment(0,y)),
        ),
      ),
      const SizedBox(height:16),
      Row(mainAxisAlignment:MainAxisAlignment.center,children:[
        IconButton(onPressed:()=>setState(()=>y=(y-.1).clamp(-1.0,1.0)),icon:const Icon(Icons.keyboard_arrow_up_rounded)),
        Text('Kadraj ${(y*100).round()}%',style:const TextStyle(fontWeight:FontWeight.w800)),
        IconButton(onPressed:()=>setState(()=>y=(y+.1).clamp(-1.0,1.0)),icon:const Icon(Icons.keyboard_arrow_down_rounded)),
      ]),
    ])),
  ));
}

'''
src=src[:insert]+page+src[insert:]

p.write_text(src,encoding="utf-8")
print("Build 399 registration + profile cover foundations applied.")
