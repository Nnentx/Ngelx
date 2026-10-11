"""Render shared profiles as white cards; apply after other Build438 patches."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
if 'class Ngelx438ProfileCard' not in s:
    start=s.index('Future<void> ngelxKisiyeProfilGonder({')
    end=s.index('\nFuture',start+1)
    part=s[start:end]
    old='    chat.get().timeout(const Duration(seconds:8)),\n'
    assert part.count(old)==1
    part=part.replace(old,old+"    FirebaseFirestore.instance.collection('users').doc(profilUid).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8)),\n")
    old="  final sohbet=sonuc[2].data()??<String,dynamic>{};"
    part=part.replace(old,old+"""
  final profile438=sonuc[3].data();
  if(profile438==null||profile438['deactivated']==true)throw StateError('profile-unavailable');
  if(List<String>.from(benim['blocked']??const[]).contains(profilUid)
    ||List<String>.from(profile438['blocked']??const[]).contains(ben.uid))throw StateError('blocked');
  if(profile438['profileShareFriendsOnly']==true&&ben.uid!=profilUid
    &&!List<String>.from(benim['friends']??const[]).contains(profilUid))throw StateError('profile-share-permission');
""")
    old="'profileUid':profilUid,'profileName':profilAdi,"
    assert part.count(old)==1
    part=part.replace(old,"""'profileUid':profilUid,
    'profileName':(profile438['displayName']??profile438['username']??profilAdi).toString(),
    'profileUsername':(profile438['username']??'').toString(),
    'profilePhotoUrl':(profile438['photoUrl']??'').toString(),""")
    s=s[:start]+part+s[end:]
    old='            else if(shared)\n              IgnorePointer(child:NgelXPaylasilanIcerikKarti(mesaj:v,benim:false))'
    assert s.count(old)==1
    s=s.replace(old,"            else if(sharedProfile)\n              Ngelx438ProfileCard(message:v)\n"+old)
    s += '''
class Ngelx438ProfileCard extends StatelessWidget{
  final Map<String,dynamic> message;
  const Ngelx438ProfileCard({super.key,required this.message});
  @override Widget build(BuildContext context){
    final name=(message['profileName']??'NgelX kullanıcısı').toString().trim();
    final username=(message['profileUsername']??'').toString().trim().replaceFirst(RegExp(r'^@+'),'');
    final photo=(message['profilePhotoUrl']??'').toString().trim();
    final fallback=const Icon(Icons.person_rounded,color:Color(0xFF8257E5),size:28);
    return Container(
      width:double.infinity,padding:const EdgeInsets.all(12),
      decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(16),border:Border.all(color:const Color(0xFFE9E1FA))),
      child:Row(children:[
        ClipOval(child:SizedBox(width:48,height:48,child:ColoredBox(color:const Color(0xFFF3EDFF),child:photo.isEmpty?fallback:NgelXAgResmi(imageUrl:photo,width:48,height:48,fit:BoxFit.cover,errorWidget:(_,__,___)=>fallback)))),
        const SizedBox(width:10),
        Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
          const Text('NgelX profili',style:TextStyle(color:Color(0xFF8257E5),fontSize:11,fontWeight:FontWeight.w700)),
          Text(name.isEmpty?'NgelX kullanıcısı':name,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF171923),fontSize:14,fontWeight:FontWeight.w800)),
          if(username.isNotEmpty)Text('@$username',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:12)),
          const SizedBox(height:4),
          const Text('Profili aç',style:TextStyle(color:Color(0xFF8257E5),fontSize:12,fontWeight:FontWeight.w700)),
        ])),
        const Icon(Icons.chevron_right_rounded,color:Color(0xFF8257E5)),
      ]),
    );
  }
}
'''
    p.write_text(s)
