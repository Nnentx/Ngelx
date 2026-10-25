part of 'main.dart';

class Ngelx565NoticeRow extends StatefulWidget{
 const Ngelx565NoticeRow({super.key});
 @override State<Ngelx565NoticeRow> createState()=>_Ngelx565NoticeRowState();
}
class _Ngelx565NoticeRowState extends State<Ngelx565NoticeRow>{
 int seen=0;
 String get key=>'notices565_seen_${FirebaseAuth.instance.currentUser?.uid??'guest'}';
 @override void initState(){super.initState();unawaited(_load());}
 Future<void> _load()async{final prefs=await SharedPreferences.getInstance();if(mounted)setState(()=>seen=prefs.getInt(key)??0);}
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:ngelx564Updater,builder:(context,_){
  final latest=math.max(565,ngelx564Updater.release?.build??0);
  return ListTile(key:const ValueKey('ngelx-announcements565'),contentPadding:const EdgeInsets.symmetric(horizontal:20,vertical:5),leading:Container(width:52,height:52,decoration:const BoxDecoration(shape:BoxShape.circle,gradient:LinearGradient(colors:[mor,Color(0xFF258AFF)])),child:const Icon(Icons.campaign_rounded,color:Colors.white,size:29)),title:const Text('NgelX Duyurular',style:TextStyle(color:Color(0xFF101827),fontWeight:FontWeight.w800,fontSize:16)),subtitle:const Text('Ludo ve uygulama güncellemeleri',style:TextStyle(color:Color(0xFF606875),fontSize:12.5)),trailing:seen<latest?const Badge(label:Text('1'),backgroundColor:mor):const Icon(Icons.chevron_right_rounded,color:mor),onTap:()async{
   final prefs=await SharedPreferences.getInstance();await prefs.setInt(key,latest);if(!context.mounted)return;setState(()=>seen=latest);await Navigator.push(context,MaterialPageRoute(builder:(_)=>const Ngelx565AnnouncementsPage()));
  });
 });
}
class Ngelx565AnnouncementsPage extends StatelessWidget{
 const Ngelx565AnnouncementsPage({super.key});
 static Future<void> update(BuildContext context)async{
  if(!ngelx564Updater.busy)await ngelx564Updater.check();
  if(context.mounted)await showDialog<void>(context:context,barrierDismissible:false,builder:(_)=>const Ngelx564UpdateDialog());
 }
 @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:const Color(0xFFF6F3FC),appBar:AppBar(title:const Text('NgelX Duyurular'),backgroundColor:Colors.white),body:ListView(padding:const EdgeInsets.all(18),children:[
  Container(padding:const EdgeInsets.all(22),decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFF7947DE),Color(0xFF328FEF)]),borderRadius:BorderRadius.circular(24)),child:const Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Icon(Icons.campaign_rounded,color:Colors.white,size:36),SizedBox(height:14),Text('NgelX’te yenilikler',style:TextStyle(color:Colors.white,fontSize:25,fontWeight:FontWeight.w900)),SizedBox(height:6),Text('Oyunlar ve uygulama güncellemeleri burada.',style:TextStyle(color:Colors.white70,fontSize:15))])),const SizedBox(height:18),
  Ngelx565AnnouncementCard(icon:Icons.casino_rounded,title:'Ludo’da buluşalım',text:'2 veya 4 kişi oyna, 2’ye 2 takım kur. Oda davetini özel sohbete veya grubuna gönder.',button:'Ludo oyna',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const Ngelx565LudoLobby()))),const SizedBox(height:16),
  Ngelx565AnnouncementCard(icon:Icons.system_update_rounded,title:'Uygulama güncellemesi',text:'NgelX $ngelxVersionName · Yapı $ngelxBuildNumber\nYeni sürümü buradan kontrol edip güncelleyebilirsin.',button:'Güncelle',onPressed:()=>update(context)),
 ])));
}
class Ngelx565AnnouncementCard extends StatelessWidget{
 final IconData icon;final String title,text,button;final VoidCallback onPressed;
 const Ngelx565AnnouncementCard({super.key,required this.icon,required this.title,required this.text,required this.button,required this.onPressed});
 @override Widget build(BuildContext context)=>Container(padding:const EdgeInsets.all(20),decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE9DFF9))),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Icon(icon,size:34,color:mor),const SizedBox(height:12),Text(title,style:const TextStyle(color:Color(0xFF151323),fontSize:21,fontWeight:FontWeight.w900)),const SizedBox(height:8),Text(text,style:const TextStyle(color:Color(0xFF6B667B),fontSize:15,height:1.4)),const SizedBox(height:16),FilledButton(onPressed:onPressed,style:FilledButton.styleFrom(backgroundColor:mor),child:Text(button))]));
}
