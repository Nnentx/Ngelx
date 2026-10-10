from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b,count=None):
 global s
 assert a in s,a[:140]
 if count is not None:assert s.count(a)==count,(a[:90],s.count(a))
 s=s.replace(a,b)
rep("defaultValue: '1.0.209'","defaultValue: '1.0.210'",1)
rep("defaultValue: '434'","defaultValue: '435'",1)
rep("import 'dart:async';","import 'dart:async';\nimport 'package:crypto/crypto.dart' as crypto;",1)
# Shared files get an app-owned, URL-specific temporary directory. Eviction
# cannot touch unrelated downloads or another message with the same filename.
rep("      final dir=await getTemporaryDirectory();\n      final ad=(v['fileName']??'NgelX_dosya').toString().replaceAll(RegExp(r'[\\\\/:*?\"<>|]'),'_');\n      final yol=dir.path+'/'+ad;\n      await Dio().download(url,yol);","      final ad=(v['fileName']??'NgelX_dosya').toString();\n      final yol=await ngelx435PaylasimDosyasi(url,ad);",1)
rep("      final dir=await getTemporaryDirectory();\n      final ad=(v['fileName']??'NgelX_dosya').toString().replaceAll(RegExp(r'[\\\\/:*?\"<>|]'),'_');\n      final yol='${dir.path}/$ad';\n      await Dio().download(url,yol);","      final ad=(v['fileName']??'NgelX_dosya').toString();\n      final yol=await ngelx435PaylasimDosyasi(url,ad);",1)
# Preserve UI and relationship behavior; replace just the two deletion bodies.
start=0
for _ in range(2):
 a=s.index('        final eskiMedya=<String>{',start)
 b=s.index('\n      }',s.index('        for(final url in eskiMedya)',a))
 s=s[:a]+"""        try{
          await ngelx435MesajiSil(d.reference);
          if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj silindi.')));
        }catch(_){
          if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Silme tamamlanamadı. Bağlantı gelince tekrar denenecek.')));
        }"""+s[b:]
 start=a+500
rep("        if(benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red)","        ListTile(leading:const Icon(Icons.delete_outline),title:const Text('Benden sil'),onTap:()=>Navigator.pop(c,'hide435')),\n        if(benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red)",1)
rep("    else if(fazla=='delete'){","    else if(fazla=='hide435'){\n      try{await ngelx435BendenSil(d.reference,v);if(mounted)setState((){});}catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gizlenemedi. Tekrar dene.')));}\n    }\n    else if(fazla=='delete'){",1)
rep("                _mesajMenuSatir(c,Icons.forward_rounded,'İlet'","                _mesajMenuSatir(c,Icons.delete_outline,'Benden sil','Yalnızca senden gizle','hide435'),\n                _mesajMenuSatir(c,Icons.forward_rounded,'İlet'",1)
rep("    }else if(sec=='delete'){","    }else if(sec=='hide435'){\n      try{await ngelx435BendenSil(d.reference,v);if(mounted)setState((){});}catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gizlenemedi. Tekrar dene.')));}\n    }else if(sec=='delete'){",1)
# Stable message identity ensures cached URLs are evicted when a tombstone arrives.
rep('  Widget mesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{QueryDocumentSnapshot<Map<String,dynamic>>? onceki,Map<String,dynamic>? grupVerisi,bool sonMesaj=false}){',"""  Widget mesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{QueryDocumentSnapshot<Map<String,dynamic>>? onceki,Map<String,dynamic>? grupVerisi,bool sonMesaj=false})=>Ngelx435MesajGorunumu(key:ValueKey('message435-'+d.reference.path),data:d.data(),builder:()=>_mesajKarti435(d,onceki:onceki,grupVerisi:grupVerisi,sonMesaj:sonMesaj));
  Widget _mesajKarti435(QueryDocumentSnapshot<Map<String,dynamic>> d,{QueryDocumentSnapshot<Map<String,dynamic>>? onceki,Map<String,dynamic>? grupVerisi,bool sonMesaj=false}){""",1)
rep('  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{double fontSize=16,bool goruldu=false,String quickReaction=\'❤️\'}){',"""  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{double fontSize=16,bool goruldu=false,String quickReaction='❤️'})=>Ngelx435MesajGorunumu(key:ValueKey('message435-'+d.reference.path),data:d.data(),builder:()=>_ozelMesajKarti435(d,fontSize:fontSize,goruldu:goruldu,quickReaction:quickReaction));
  Widget _ozelMesajKarti435(QueryDocumentSnapshot<Map<String,dynamic>> d,{double fontSize=16,bool goruldu=false,String quickReaction='❤️'}){""",1)
for cls in ['class _GrupSohbetPageState extends State<GrupSohbetPage>{','class _SohbetPageState extends State<SohbetPage> {']:
 a=s.index(cls);b=s.index('\nclass ',a+len(cls));part=s[a:b]
 part=part.replace(cls,cls+'\n  Timer? _cleanup435Timer;')
 anchor='    super.initState();';assert anchor in part
 part=part.replace(anchor,anchor+"\n    unawaited(ngelx435SilmeTekrar(widget.chatId));\n    _cleanup435Timer=Timer.periodic(const Duration(seconds:30),(_)=>unawaited(ngelx435SilmeTekrar(widget.chatId)));",1)
 anchor='super.dispose();';assert anchor in part
 part=part.replace(anchor,'_cleanup435Timer?.cancel();super.dispose();',1)
 s=s[:a]+part+s[b:]
s+='\n'+Path('tools/build435_message_cleanup.dart').read_text();p.write_text(s)
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.209+434','version: 1.0.210+435'))
p.write_text(p.read_text().replace('  cached_network_image:', '  crypto: ^3.0.6\n  cached_network_image:'))
from build435_rules import patch_rules
p=Path('firestore.rules');p.write_text(patch_rules(p.read_text()))
p=Path('tools/firestore_rules_test.mjs');v=p.read_text();v=v.replace("  console.log('Firestore rules testleri başarılı.');",Path('tools/build435_rules_test.mjs').read_text()+"\n  console.log('Firestore rules testleri başarılı.');");p.write_text(v)
print('Build435 cleanup applied')
