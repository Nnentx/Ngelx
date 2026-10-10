bool ngelx436Blocked(Map<String,dynamic> me,Map<String,dynamic> other,String mine,String theirs)=>
  (me['blocked'] is Iterable&&(me['blocked'] as Iterable).contains(theirs))||
  (other['blocked'] is Iterable&&(other['blocked'] as Iterable).contains(mine));
Future<void> ngelx436RequireOpen(String other)async{
  final mine=FirebaseAuth.instance.currentUser?.uid;
  if(mine==null)throw StateError('Önce giriş yap.');
  final db=FirebaseFirestore.instance;
  final docs=await Future.wait([db.collection('users').doc(mine).get(const GetOptions(source:Source.server)),db.collection('users').doc(other).get(const GetOptions(source:Source.server))]).timeout(const Duration(seconds:10));
  if(ngelx436Blocked(docs[0].data()??{},docs[1].data()??{},mine,other))throw StateError('Engel varken bu işlem yapılamaz.');
}
String ngelx436Error(Object e){
  if(e is FirebaseException){
    if(e.code=='permission-denied')return 'İşlem izni reddedildi. İşlem tamamlanmadı.';
    if(e.code=='resource-exhausted')return 'Sunucu işlem sınırına ulaştı. Daha sonra tekrar dene.';
    if(e.code=='unavailable'||e.code=='deadline-exceeded')return 'Sunucuya ulaşılamadı. Bağlantı gelince tekrar denenecek.';
    return 'İşlem tamamlanamadı (${e.code}).';
  }
  if(e is TimeoutException)return 'Sunucudan onay alınamadı. Sonuç yeniden kontrol edilecek.';
  if(e is StateError)return e.message.toString();
  return 'İşlem tamamlanamadı. Tekrar dene.';
}
class Ngelx436BlockView extends StatelessWidget{
  final String other;
  final Widget Function(bool mine,bool theirs) builder;
  const Ngelx436BlockView({super.key,required this.other,required this.builder});
  @override Widget build(BuildContext context){
    final mine=FirebaseAuth.instance.currentUser?.uid;
    if(mine==null)return builder(true,true);
    final db=FirebaseFirestore.instance;
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:db.collection('users').doc(mine).snapshots(),builder:(_,a)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:db.collection('users').doc(other).snapshots(),builder:(_,b){
      if(!a.hasData||!b.hasData)return const SizedBox.shrink();
      bool has(dynamic list,String id)=>list is Iterable&&list.contains(id);
      return builder(has(a.data?.data()?['blocked'],other),has(b.data?.data()?['blocked'],mine));
    }));
  }
}
