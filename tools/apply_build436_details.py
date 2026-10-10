from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b,n=1):
 global s
 assert s.count(a)==n,(a[:120],s.count(a));s=s.replace(a,b)
rep("takma=(uid==null?'':(nicks[uid]??'').toString()).trim(),","takma=(nicks[widget.digerUid]??'').toString().trim(),")
rep("return p>0?'Sen'+raw.substring(p):raw;","return p>0?('Sen'+raw.substring(p)).replaceFirst(' değiştirdi',' değiştirdin').replaceFirst(' kaldırdı',' kaldırdın').replaceFirst(' sıfırladı',' sıfırladın'):raw;")
# Block again must be idempotent, including other entry points.
rep("  String hedefAd='Bu kullanıcı',hedefFoto='';","""  final mine=await FirebaseFirestore.instance.collection('users').doc(u.uid).get(const GetOptions(source:Source.server));
  if(List<String>.from(mine.data()?['blocked']??const[]).contains(hedefUid)){
    if(context.mounted)ngelxDurumMesaji(context,'Bu hesap zaten engellenmiş.',tip:'uyari');
    return;
  }
  String hedefAd='Bu kullanıcı',hedefFoto='';""")
# A tombstone stays in its original position with sender-specific text in groups.
rep("Text('Bu mesaj silindi',style:TextStyle(color:Color(0xFF777B80)","Text((v['deletedBy']??'')==uid?'Bu mesajı sildin':'Bu mesaj silindi',style:TextStyle(color:Color(0xFF777B80)")
# Eligibility has the same three relationship routes for profile, info and list labels.
rep("final etiket=_etiket(v);","final etiket=_etiket(v);")
rep("return Ngelx436BlockView(other:widget.uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():Text(","return Ngelx436PresenceAccess(other:widget.uid,target:v,child:Text(")
# Presence access widget owns the block checks and requires actual mutual chat history.
s+='''
class Ngelx436PresenceAccess extends StatelessWidget{
  final String other;final Map<String,dynamic> target;final Widget child;
  const Ngelx436PresenceAccess({super.key,required this.other,required this.target,required this.child});
  @override Widget build(BuildContext context){
    final mine=FirebaseAuth.instance.currentUser?.uid;
    if(mine==null||target['showActivityStatus']==false)return const SizedBox.shrink();
    if(mine==other)return child;
    final db=FirebaseFirestore.instance;
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:db.collection('users').doc(mine).snapshots(),builder:(_,snap){
      final me=snap.data?.data();if(me==null||ngelx436Blocked(me,target,mine,other))return const SizedBox.shrink();
      bool has(Map<String,dynamic> v,String key,String id)=>v[key] is Iterable&&(v[key] as Iterable).contains(id);
      if(has(me,'friends',other)||has(me,'following',other)||has(me,'followers',other)||has(target,'friends',mine)||has(target,'following',mine)||has(target,'followers',mine))return child;
      final ids=<String>[mine,other]..sort();
      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:db.collection('chats').doc(ids.join('_')).collection('messages').where('senderId',whereIn:[mine,other]).limit(100).snapshots(),builder:(_,messages){
        final senders=<String>{};
        for(final d in messages.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[]){if(d.data()['type']!='system')senders.add((d.data()['senderId']??'').toString());}
        return senders.contains(mine)&&senders.contains(other)?child:const SizedBox.shrink();
      });
    });
  }
}
'''
# Avatar online/last-seen must also respect both block directions and privacy.
rep("final label=ngelx434Aktiflik(v),online=label=='Çevrimiçi';","final label=ngelx434Aktiflik(v),online=label=='Çevrimiçi';")
rep("if(label.isNotEmpty)Positioned(right:-3,bottom:0,child:Semantics(label:label,child:Tooltip", "if(label.isNotEmpty)Positioned(right:-3,bottom:0,child:Ngelx436PresenceAccess(other:widget.uid,target:v,child:Semantics(label:label,child:Tooltip")
rep("      )))),\n    ]));","      ))))),\n    ]));")
p.write_text(s)
from build436_rules import patch_rules
p=Path('firestore.rules');p.write_text(patch_rules(p.read_text()))
print('Build436 relationship, deletion and block details applied')

p=Path('tools/firestore_rules_test.mjs');text=p.read_text();anchor="  console.log('Firestore rules testleri başarılı.');";assert anchor in text;p.write_text(text.replace(anchor,Path('tools/build436_rules_test.mjs').read_text()+'\n'+anchor))
