"""Apply final device feedback after the existing Build445 pipeline."""
from pathlib import Path

def change(text, old, new):
    assert text.count(old) == 1, (old[:90], text.count(old))
    return text.replace(old, new, 1)

p=Path('app/lib/build445_inbox_model.dart');s=p.read_text()
s=change(s,'builder:(_)=>const YuklePage()', 'builder:(_)=>const Scaffold(backgroundColor:Colors.white,body:ProfilPage())')
s=change(s,'  String? _opening;', '''  String? _opening;
  Timer? _noteClock;
  @override void initState(){super.initState();_noteClock=Timer.periodic(const Duration(seconds:30),(_){if(mounted)setState((){});});}
  @override void dispose(){_noteClock?.cancel();super.dispose();}
  Future<void> _editNote(Map<String,dynamic> profile)async{
    if(_opening!=null)return;
    final expiry=profile['inboxNoteExpiresAt'];
    final active=expiry is Timestamp&&expiry.toDate().isAfter(DateTime.now());
    final controller=TextEditingController(text:active?(profile['inboxNote']??'').toString():'');
    final value=await showModalBottomSheet<String>(context:context,isScrollControlled:true,backgroundColor:Colors.white,
      builder:(c)=>Padding(padding:EdgeInsets.fromLTRB(20,20,20,20+MediaQuery.viewInsetsOf(c).bottom),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        TextField(controller:controller,autofocus:true,maxLength:50,maxLines:2,decoration:const InputDecoration(hintText:'Bir not yaz…',counterText:'')),
        TextButton(onPressed:()=>Navigator.pop(c,controller.text.trim()),child:const Text('Paylaş')),
      ]))));
    // The controller remains alive until the closing route animation finishes.
    await Future<void>.delayed(const Duration(milliseconds:350));controller.dispose();
    if(value==null||!mounted||FirebaseAuth.instance.currentUser?.uid!=widget.uid)return;
    setState(()=>_opening=widget.uid);
    try{
      await FirebaseFirestore.instance.collection('users').doc(widget.uid).update({
        'inboxNote':value,'inboxNoteExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(hours:24))),
      }).timeout(const Duration(seconds:10));
    }catch(_){if(mounted)ngelxDurumMesaji(context,'Not kaydedilemedi. Tekrar dene.',tip:'hata');}
    finally{if(mounted)setState(()=>_opening=null);}
  }''')
s=change(s,'SizedBox(height:108,child:ListView.builder(', 'SizedBox(height:86,child:ListView.builder(')
a=s.index('                  SizedBox(height:24,child:note.isEmpty?null:Align(')
b=s.index('                  Stack(clipBehavior:',a)
s=s[:a]+'''                  const SizedBox(height:14),
'''+s[b:]
anchor="                      child:CircleAvatar(radius:23,backgroundColor:const Color(0xFFF1EDF9),backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),child:photo.isEmpty?const Icon(Icons.person_outline,color:mor):null)),\n"
s=change(s,anchor,anchor+'''                    if(note.isNotEmpty)Positioned(top:-12,left:0,right:0,child:Transform.translate(offset:Offset.zero,child:Container(
                      padding:const EdgeInsets.symmetric(horizontal:5,vertical:3),
                      decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(12),border:Border.all(color:const Color(0xFFE9E6EE)),boxShadow:const[BoxShadow(color:Color(0x18000000),blurRadius:3)]),
                      child:Text(note,maxLines:2,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontSize:9)),
                    ))),
''')
old="if(self)Positioned(right:0,bottom:0,child:Container(width:18,height:18,decoration:BoxDecoration(color:mor,shape:BoxShape.circle,border:Border.all(color:Colors.white,width:2)),child:const Icon(Icons.add,color:Colors.white,size:13))),"
new="if(self)Positioned(right:-7,bottom:-7,child:GestureDetector(behavior:HitTestBehavior.opaque,onTap:()=>_editNote(p),child:Padding(padding:const EdgeInsets.all(7),child:Container(width:18,height:18,decoration:BoxDecoration(color:mor,shape:BoxShape.circle,border:Border.all(color:Colors.white,width:2)),child:const Icon(Icons.add,color:Colors.white,size:13))))),"
s=change(s,old,new);p.write_text(s)

p=Path('app/lib/main.dart');s=p.read_text()
a=s.index('class _YeniYuklePageState');b=s.index('class ',a+30)
region=s[a:b]
region=change(region,'child:ColoredBox(\n        color:Colors.white,','child:Material(\n        color:Colors.white,\n        textStyle:const TextStyle(color:Colors.black87,fontSize:14,decoration:TextDecoration.none),')
s=s[:a]+region+s[b:]
# Keep member permissions and selection UI; make loading and failures visible.
s=change(s,'  Future<void> uyeEkle(List<String> mevcut)async{','''  bool _adding446=false;
  Future<void> uyeEkle(List<String> mevcut)async{
    if(_adding446)return;
    setState(()=>_adding446=true);
    ngelxDurumMesaji(context,'Kişiler yükleniyor…');
    try{_uyeProfilCache.clear();await _uyeEkle446(mevcut);}
    catch(_){if(mounted)ngelxDurumMesaji(context,'Kişiler yüklenemedi. Tekrar dene.',tip:'hata');}
    finally{if(mounted)setState(()=>_adding446=false);}
  }
  Future<void> _uyeEkle446(List<String> mevcut)async{''')
a=s.index('  Future<void> _uyeEkle446');b=s.index('  Future<void> ',a+40)
region=s[a:b].replace('await ref.get();','await ref.get().timeout(const Duration(seconds:10));').replace("doc(me).get();","doc(me).get().timeout(const Duration(seconds:10));").replace('await Future.wait(izinli.map(_uyeGetir));','await Future.wait(izinli.map(_uyeGetir)).timeout(const Duration(seconds:10));')
s=s[:a]+region+s[b:];p.write_text(s)

p=Path('app/lib/story_v66.dart');s=p.read_text()
s=change(s,"(segments.first=='stories'||segments.first=='videos')", "(segments.first=='stories'||segments.first=='videos'||segments.first=='photos')")
s=change(s,"!dosya.fullPath.startsWith('stories/'+uid+'/')", "!ownR2Key(dosya.fullPath)")
s=change(s,"if(api.isEmpty||!raw.startsWith(api+'/media/')){", "if(api.isEmpty||!{Uri.parse(api).origin,Uri.parse(_ngelxMediaApiBuild).origin,Uri.parse(_ngelxMediaApiBackup).origin,Uri.parse(_ngelxMediaApiLegacyPrimary).origin,Uri.parse(_ngelxMediaApiLegacyBackup).origin}.contains(Uri.parse(raw).origin)){")
s=change(s,'final current=await ref.get();','final current=await ref.get().timeout(const Duration(seconds:10));')
s=change(s,'await dosya.delete();','await dosya.delete().timeout(const Duration(seconds:12));')
p.write_text(s)
print('Build446 final device feedback applied; original tabs, call flow and permissions preserved')
