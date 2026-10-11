"""Build441: own archive recovery, uncapped highlights and production token guard."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
assert '// Build441 play readiness' not in s
start=s.index('class _ArsivSohbetlerPageState');end=s.index('class MesajIstekleriPage',start)
v=s[start:end]
v=v.replace('List<DocumentSnapshot<Map<String,dynamic>>>','List<NgelXArchiveRecord441>').replace('<DocumentSnapshot<Map<String,dynamic>>>[]','<NgelXArchiveRecord441>[]')
v=v.replace("final ids=<String>{...manuel};", "final ids=<String>{...manuel};\n    final dismissed=Set<String>.from(List<String>.from(user.data()?['dismissedArchiveChats']??const[]));\n    final metadata=<String,Map<String,dynamic>>{};")
v=v.replace("ids.addAll(kayitlar.docs.map((e)=>(e.data()['chatId']??e.id).toString()).where((e)=>e.isNotEmpty));", "for(final e in kayitlar.docs){final id=(e.data()['chatId']??e.id).toString();if(id.isNotEmpty){ids.add(id);metadata[id]=e.data();}}")
v=v.replace('final docs=<NgelXArchiveRecord441>[];', 'ids.removeAll(dismissed);\n    final docs=<NgelXArchiveRecord441>[];')
v=v.replace('docs.add(d);', "docs.add(NgelXArchiveRecord441(id,d.exists?d.data()??{}:metadata[id]??{},available:d.exists));")
v=v.replace('}catch(_){_arsivKismi=true;}\n    }));', "}on FirebaseException catch(e){\n        if(e.code=='permission-denied'){docs.add(NgelXArchiveRecord441(id,metadata[id]??{},available:false));}\n        else{_arsivKismi=true;}\n      }catch(_){_arsivKismi=true;}\n    }));")
v=v.replace('if(!d.exists)return false;', 'if(!d.available)return true;')
a=v.index('  Future<void> eskiSohbetiSil');b=v.index('  @override Widget build',a)
v=v[:a]+'''  Future<void> eskiSohbetiSil(String id)async{
    if(FirebaseAuth.instance.currentUser?.uid!=widget.uid)return;
    try{
      final batch=FirebaseFirestore.instance.batch();
      batch.set(FirebaseFirestore.instance.collection('users').doc(widget.uid),{
        'archivedChats':FieldValue.arrayRemove([id]),
        'dismissedArchiveChats':FieldValue.arrayUnion([id]),
      },SetOptions(merge:true));
      batch.delete(ngelxGroupArchiveRef(widget.uid,id));
      await batch.commit().timeout(const Duration(seconds:12));
      if(mounted&&FirebaseAuth.instance.currentUser?.uid==widget.uid)_arsivYenile();
    }catch(_){if(mounted)ngelxDurumMesaji(context,_ngelx438Ui('Arşivden çıkarılamadı. Bağlantını kontrol edip tekrar dene.'),tip:'hata');}
  }

'''+v[b:]
v=v.replace("final members=List<String>.from(v['members']??const[]);", """if(!d.available)return ListTile(
                leading:const CircleAvatar(child:Icon(Icons.archive_outlined)),
                title:Text((v['groupName']??t('archivedChats')).toString()),
                subtitle:Text(_ngelx438Ui('Bu sohbet artık erişilebilir değil. Arşiv kaydını kaldırabilirsin.')),
                trailing:IconButton(tooltip:_ngelx438Ui('Arşivden kaldır'),onPressed:()=>eskiSohbetiSil(d.id),icon:const Icon(Icons.delete_outline_rounded)),
              );
              final members=List<String>.from(v['members']??const[]);""")
s=s[:start]+v+s[end:]
s=s.replace(".where('ownerId',isEqualTo:aktifKullanici!.uid).where('type',isEqualTo:'story').limit(100).snapshots(),\n                    builder:(_,hs)",".where('ownerId',isEqualTo:aktifKullanici!.uid).where('highlighted',isEqualTo:true).limit(30).snapshots(),\n                    builder:(_,hs)",1)
s=s.replace("final h=(hs.data?.docs??[]).where((d)=>d.data()['highlighted']==true).toList()", "if(hs.hasError)return Center(child:Text(_ngelx438Ui('Öne çıkanlar yüklenemedi. Bağlantını kontrol et.')));\n                      final h=(hs.data?.docs??[]).where((d)=>d.data()['type']=='story').toList()",1)
s+='''
// Build441 play readiness
class NgelXArchiveRecord441 {
  final String id;
  final Map<String,dynamic> value;
  final bool available;
  const NgelXArchiveRecord441(this.id,this.value,{required this.available});
  Map<String,dynamic> data()=>value;
}
const ngelxPlayRelease441=bool.fromEnvironment('NGELX_PLAY_RELEASE');
const ngelxLiveKitEndpoint441=String.fromEnvironment('NGELX_LIVEKIT_TOKEN_URL');
Future<lk.TokenSourceResponse> ngelxLiveKitToken441(lk.TokenRequestOptions options)async{
  if(ngelxLiveKitEndpoint441.isEmpty){
    if(ngelxPlayRelease441)throw StateError('Production calling endpoint is not configured');
    return lk.DevelopmentTokenSource(id:liveKitTestSunucuId).fetch(options).timeout(const Duration(seconds:12));
  }
  final uri=Uri.parse(ngelxLiveKitEndpoint441);
  if(uri.scheme!='https'||uri.host.isEmpty||uri.userInfo.isNotEmpty)throw StateError('Invalid calling endpoint');
  final user=FirebaseAuth.instance.currentUser;
  if(user==null||user.isAnonymous)throw StateError('Sign in to call');
  final idToken=await user.getIdToken().timeout(const Duration(seconds:10));
  if(idToken==null)throw StateError('Session unavailable');
  final result=await lk.EndpointTokenSource(url:uri,headers:{'Authorization':'Bearer $idToken'}).fetch(options).timeout(const Duration(seconds:12));
  if(FirebaseAuth.instance.currentUser?.uid!=user.uid)throw StateError('Session changed');
  return result;
}
class NgelXLiveKitSource441 {
  Future<lk.TokenSourceResponse> fetch(lk.TokenRequestOptions options)=>ngelxLiveKitToken441(options);
}
'''
s=s.replace('lk.DevelopmentTokenSource(id:liveKitTestSunucuId);','NgelXLiveKitSource441();').replace('lk.DevelopmentTokenSource(id: liveKitTestSunucuId);','NgelXLiveKitSource441();')
p.write_text(s)
for p in Path('app/lib').glob('*.dart'):
 if p.name=='main.dart' or not p.read_text().startswith("part of 'main.dart';"):continue
 v=p.read_text().replace('lk.DevelopmentTokenSource(id:liveKitTestSunucuId)','NgelXLiveKitSource441()').replace('lk.DevelopmentTokenSource(id: liveKitTestSunucuId)','NgelXLiveKitSource441()')
 if p.name=='story_v66.dart':
  v=v.replace('int aktif=0;', 'int aktif=0;\n  final Map<String,bool> _highlight441={};').replace("final oneCikan=veri['highlighted']==true;","final oneCikan=_highlight441[storyId]??(veri['highlighted']==true);")
  v=v.replace("await d.reference.set({'highlighted':!oneCikan,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));", "await d.reference.set({'highlighted':!oneCikan,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).timeout(const Duration(seconds:12));\n        final saved=await d.reference.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10));\n        if(saved.data()?['highlighted']!=!oneCikan)throw StateError('Highlight not persisted');\n        _highlight441[d.id]=!oneCikan;")
 p.write_text(v)
print('Build441 archive, highlight and production call guard applied')
