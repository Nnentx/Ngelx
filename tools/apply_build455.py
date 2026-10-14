"""Apply Build455 after the verified Build454 source-generation chain."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def replace(path, old, new):
    target = root / path
    source = target.read_text()
    if old not in source:
        raise RuntimeError(f"Build455 source anchor missing: {path}: {old[:70]}")
    target.write_text(source.replace(old, new))

replace('app/lib/main.dart', "part 'build454_widgets.dart';", "part 'build454_widgets.dart';\npart 'build455_widgets.dart';")
replace('app/lib/main.dart', "profilAdi=(p['displayName']??p['username']??'NgelX').toString()", "profilAdi=ngelx455ProfileName(p, fallback:'Kişi bilgisi yükleniyor…')")
replace('app/lib/main.dart', "takma=(ben==null?'':(takmalar[ben]??'').toString()).trim()", "takma=(takmalar[other]??'').toString().trim()")
replace('app/lib/main.dart', "title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,s){", "title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),builder:(_,profile455){return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,s){")
# Close this additional builder only at the private-chat title boundary.
path = root / 'app/lib/main.dart'
source = path.read_text()
start = source.index("title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),builder:(_,profile455)")
end = source.index('actions:', start)
section = source[start:end]
section = section.replace('gorunenAd=takma.isNotEmpty?takma:widget.ad;', "gorunenAd=takma.isNotEmpty?takma:ngelx455ProfileName(profile455.data?.data()??{},fallback:widget.ad=='NgelX'?'Kişi bilgisi yükleniyor…':widget.ad);\n        final photo455=(profile455.data?.data()?['photoUrl']??widget.foto).toString();")
section = section.replace('widget.foto.isEmpty', 'photo455.isEmpty').replace('NgelXAgImageProvider(widget.foto)', 'NgelXAgImageProvider(photo455)')
last = section.rfind('}),')
if last < 0: raise RuntimeError('Build455 private title closure missing')
section = section[:last] + '});}),' + section[last+3:]
path.write_text(source[:start]+section+source[end:])

replace('app/lib/community450.dart', 'fontSize: 11)', 'fontSize: 13)')
replace('app/lib/community450.dart', 'fontSize: 11,', 'fontSize: 13,')
replace('app/lib/community450.dart', 'fontSize: 12)', 'fontSize: 14)')
replace('app/lib/community450.dart', 'padding:const EdgeInsets.all(16),margin:const EdgeInsets.only(bottom:16)', 'padding:const EdgeInsets.symmetric(horizontal:12,vertical:9),margin:const EdgeInsets.only(bottom:10)')
replace('app/lib/community450.dart', "Text(_stage454,style:const TextStyle(color:Color(0xFF43326C),fontWeight:FontWeight.w700)),const SizedBox(height:10)", "Text(_stage454,style:const TextStyle(color:Color(0xFF6744C8),fontSize:12,fontWeight:FontWeight.w700)),const SizedBox(height:6)")
replace('app/lib/community450.dart', "style:const TextStyle(color:Color(0xFF43326C))", "style:const TextStyle(color:Color(0xFF6744C8),fontSize:12,fontWeight:FontWeight.w600)")
replace('app/lib/community450.dart', "ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(pending?'Gönderin yönetici onayına gönderildi.':'Gönderin paylaşıldı.')))", "ngelx455Status(context,pending?'Yönetici onayına gönderildi':type=='video'?'Video paylaşıldı':type=='image'?'Fotoğraf paylaşıldı':'Gönderi paylaşıldı')")
print('Build455 profile names and compact upload presentation applied')
