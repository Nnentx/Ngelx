import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:supabase_flutter/supabase_flutter.dart' as supa;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:image_picker/image_picker.dart';
import 'package:video_player/video_player.dart';
import 'package:share_plus/share_plus.dart';
import 'package:gal/gal.dart';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:file_selector/file_selector.dart';
import 'package:just_audio/just_audio.dart';
import 'package:livekit_client/livekit_client.dart' as lk;
import 'package:device_info_plus/device_info_plus.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    await Firebase.initializeApp();
    await supa.Supabase.initialize(
      url: 'https://ptteuuwktcvzuhrkacuv.supabase.co',
      anonKey: 'sb_publishable_kcV2-0Y3irQoWpbNwEtj1w_WGkGESZZ',
    );
    final hafiza = await SharedPreferences.getInstance();
    uygulamaDili.value = hafiza.getString('uygulama_dili') ?? 'tr';
    runApp(const NgelXApp());
  } catch (e) {
    runApp(BaslangicHataApp(hata: e.toString()));
  }
}

class BaslangicHataApp extends StatelessWidget {
  final String hata; const BaslangicHataApp({super.key,required this.hata});
  @override Widget build(BuildContext context)=>MaterialApp(debugShowCheckedModeBanner:false,home:Scaffold(backgroundColor:Colors.white,body:SafeArea(child:Center(child:Padding(padding:const EdgeInsets.all(28),child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:70),const SizedBox(height:18),const Text('NgelX başlatılamadı',style:TextStyle(color:Colors.black,fontSize:24,fontWeight:FontWeight.w900)),const SizedBox(height:9),const Text('İnternet bağlantısını ve Firebase ayarlarını kontrol et.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:16)),const SizedBox(height:12),Text(hata,maxLines:4,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Colors.redAccent,fontSize:12)),const SizedBox(height:20),FilledButton.icon(onPressed:()=>main(),icon:const Icon(Icons.refresh),label:const Text('Tekrar dene'))]))))));
}

const mor = Color(0xFF8B5CF6);
const mavi = Color(0xFF22D3EE);
const panel = Color(0xFF17171F);
final uygulamaDili = ValueNotifier<String>('tr');
const dilAdlari = {'tr':'Türkçe','en':'English','de':'Deutsch','ar':'العربية','ru':'Русский'};
const ceviriler = <String, Map<String,String>>{
  'welcome': {'tr':'Tekrar hoş geldin','en':'Welcome back','de':'Willkommen zurück','ar':'مرحباً بعودتك','ru':'С возвращением'},
  'tagline': {'tr':'İzle, keşfet ve kendi dünyanı paylaş.','en':'Watch, discover and share your world.','de':'Ansehen, entdecken und deine Welt teilen.','ar':'شاهد واكتشف وشارك عالمك.','ru':'Смотри, открывай и делись своим миром.'},
  'email': {'tr':'E-posta adresi','en':'Email address','de':'E-Mail-Adresse','ar':'البريد الإلكتروني','ru':'Электронная почта'},
  'password': {'tr':'Şifre','en':'Password','de':'Passwort','ar':'كلمة المرور','ru':'Пароль'},
  'remember': {'tr':'Beni hatırla','en':'Remember me','de':'Angemeldet bleiben','ar':'تذكرني','ru':'Запомнить меня'},
  'forgot': {'tr':'Şifremi unuttum','en':'Forgot password','de':'Passwort vergessen','ar':'نسيت كلمة المرور','ru':'Забыли пароль'},
  'login': {'tr':'Giriş Yap','en':'Sign in','de':'Anmelden','ar':'تسجيل الدخول','ru':'Войти'},
  'guest': {'tr':'Misafir olarak keşfet','en':'Explore as guest','de':'Als Gast entdecken','ar':'استكشف كضيف','ru':'Войти как гость'},
  'noAccount': {'tr':'Hesabın yok mu?','en':'Don’t have an account?','de':'Noch kein Konto?','ar':'ليس لديك حساب؟','ru':'Нет аккаунта?'},
  'createAccount': {'tr':'Hesap oluştur','en':'Create account','de':'Konto erstellen','ar':'إنشاء حساب','ru':'Создать аккаунт'},
  'resetTitle': {'tr':'Şifreni yenile','en':'Reset your password','de':'Passwort zurücksetzen','ar':'إعادة تعيين كلمة المرور','ru':'Сбросить пароль'},
  'resetInfo': {'tr':'E-posta adresini yaz. Sana güvenli şifre yenileme bağlantısı göndereceğiz.','en':'Enter your email. We will send you a secure password reset link.','de':'Gib deine E-Mail ein. Wir senden dir einen sicheren Link.','ar':'أدخل بريدك الإلكتروني وسنرسل رابطاً آمناً.','ru':'Введите почту — мы отправим безопасную ссылку.'},
  'sendReset': {'tr':'Bağlantı gönder','en':'Send reset link','de':'Link senden','ar':'إرسال الرابط','ru':'Отправить ссылку'},
  'backLogin': {'tr':'Giriş ekranına dön','en':'Back to sign in','de':'Zurück zur Anmeldung','ar':'العودة لتسجيل الدخول','ru':'Вернуться ко входу'},
  'newAccount': {'tr':'Yeni hesap','en':'New account','de':'Neues Konto','ar':'حساب جديد','ru':'Новый аккаунт'},
  'fullName': {'tr':'Ad ve soyad','en':'Full name','de':'Vor- und Nachname','ar':'الاسم الكامل','ru':'Имя и фамилия'},
  'username': {'tr':'Kullanıcı adı','en':'Username','de':'Benutzername','ar':'اسم المستخدم','ru':'Имя пользователя'},
  'emailAgain': {'tr':'E-posta adresini tekrar yaz','en':'Enter email again','de':'E-Mail wiederholen','ar':'أعد إدخال البريد الإلكتروني','ru':'Повторите почту'},
  'password8': {'tr':'Şifre (en az 8 karakter)','en':'Password (at least 8 characters)','de':'Passwort (mindestens 8 Zeichen)','ar':'كلمة المرور (8 أحرف على الأقل)','ru':'Пароль (минимум 8 символов)'},
  'passwordAgain': {'tr':'Şifreyi tekrar yaz','en':'Enter password again','de':'Passwort wiederholen','ar':'أعد إدخال كلمة المرور','ru':'Повторите пароль'},
  'birthDate': {'tr':'Doğum tarihi (GG/AA/YYYY)','en':'Birth date (DD/MM/YYYY)','de':'Geburtsdatum (TT/MM/JJJJ)','ar':'تاريخ الميلاد (يوم/شهر/سنة)','ru':'Дата рождения (ДД/ММ/ГГГГ)'},
  'phone': {'tr':'Telefon numarası','en':'Phone number','de':'Telefonnummer','ar':'رقم الهاتف','ru':'Номер телефона'},
  'phoneOptional': {'tr':'Şimdilik zorunlu değil, boş bırakabilirsin.','en':'Optional for now; you can leave it blank.','de':'Derzeit optional; kann leer bleiben.','ar':'اختياري حالياً ويمكن تركه فارغاً.','ru':'Пока необязательно; можно оставить пустым.'},
  'terms': {'tr':'Kullanım Koşulları ve Gizlilik Politikasını kabul ediyorum.','en':'I accept the Terms of Use and Privacy Policy.','de':'Ich akzeptiere Nutzungsbedingungen und Datenschutzrichtlinie.','ar':'أوافق على شروط الاستخدام وسياسة الخصوصية.','ru':'Я принимаю Условия использования и Политику конфиденциальности.'},
  'creating': {'tr':'Hesap oluşturuluyor...','en':'Creating account...','de':'Konto wird erstellt...','ar':'جارٍ إنشاء الحساب...','ru':'Создание аккаунта...'},
  'weak': {'tr':'Zayıf','en':'Weak','de':'Schwach','ar':'ضعيفة','ru':'Слабый'},
  'medium': {'tr':'Orta','en':'Medium','de':'Mittel','ar':'متوسطة','ru':'Средний'},
  'strong': {'tr':'Güçlü','en':'Strong','de':'Stark','ar':'قوية','ru':'Сильный'},
  'flow': {'tr':'Akış','en':'Feed','de':'Feed','ar':'الرئيسية','ru':'Лента'},
  'explore': {'tr':'Keşfet','en':'Explore','de':'Entdecken','ar':'استكشف','ru':'Обзор'},
  'create': {'tr':'Üret','en':'Create','de':'Erstellen','ar':'إنشاء','ru':'Создать'},
  'chat': {'tr':'Sohbet','en':'Chat','de':'Chat','ar':'الدردشة','ru':'Чат'},
  'me': {'tr':'Ben','en':'Me','de':'Ich','ar':'أنا','ru':'Я'},
};
String t(String anahtar) => ceviriler[anahtar]?[uygulamaDili.value] ?? ceviriler[anahtar]?['tr'] ?? anahtar;
Future<void> diliDegistir(String dil) async {uygulamaDili.value=dil;final h=await SharedPreferences.getInstance();await h.setString('uygulama_dili',dil);}

Future<void> uygulamaBildirimiGonder({required String toUid,required String fromUid,required String tur,required String metin,String? belgeId}) async {
  if(toUid==fromUid)return;
  final hedef=await FirebaseFirestore.instance.collection('users').doc(toUid).get();
  final ayar=hedef.data()??{};
  if(ayar['notificationsEnabled']==false)return;
  if(tur=='message'&&ayar['messageNotifications']==false)return;
  if(tur=='interaction'&&ayar['interactionNotifications']==false)return;
  if(tur=='friend'&&ayar['friendNotifications']==false)return;
  await FirebaseFirestore.instance.collection('notifications').add({
    'toUid':toUid,'fromUid':fromUid,'type':tur,'text':metin,
    if(belgeId!=null)'sourceId':belgeId,
    'read':false,'createdAt':FieldValue.serverTimestamp(),
  });
}

Future<void> takipDurumuDegistir(String hedefUid,bool takipte)async{
  final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||hedefUid.isEmpty||ben==hedefUid)return;
  final batch=FirebaseFirestore.instance.batch();
  batch.set(FirebaseFirestore.instance.collection('users').doc(ben),{'following':takipte?FieldValue.arrayRemove([hedefUid]):FieldValue.arrayUnion([hedefUid])},SetOptions(merge:true));
  batch.set(FirebaseFirestore.instance.collection('users').doc(hedefUid),{'followers':takipte?FieldValue.arrayRemove([ben]):FieldValue.arrayUnion([ben])},SetOptions(merge:true));
  await batch.commit();
  if(!takipte)await uygulamaBildirimiGonder(toUid:hedefUid,fromUid:ben,tur:'friend',metin:'Seni takip etmeye başladı');
}

Future<void> icerikAracMenusu(BuildContext context,String icerikId,{Future<void> Function(double)? hizDegistir})async{
  if(icerikId.isEmpty)return;
  final belge=await FirebaseFirestore.instance.collection('videos').doc(icerikId).get();
  bool altyazi=belge.data()?['captionsEnabled']==true;
  if(!context.mounted)return;
  await showModalBottomSheet(context:context,backgroundColor:Colors.white,shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),builder:(c)=>StatefulBuilder(builder:(c,setPencere)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
    Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.black26,borderRadius:BorderRadius.circular(8))),
    const Text('İçerik araçları',style:TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),
    ListTile(leading:const Icon(Icons.translate_rounded,color:mor),title:const Text('Dil ve çeviri',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text('Seçili dil: ${dilAdlari[uygulamaDili.value]}',style:const TextStyle(color:Colors.black54)),onTap:()async{final sec=await showDialog<String>(context:c,builder:(d)=>SimpleDialog(title:const Text('İçerik dili'),children:dilAdlari.entries.map((e)=>SimpleDialogOption(onPressed:()=>Navigator.pop(d,e.key),child:Text(e.value))).toList()));if(sec!=null){await diliDegistir(sec);if(c.mounted)Navigator.pop(c);}}),
    SwitchListTile(secondary:const Icon(Icons.closed_caption_rounded,color:Colors.blue),title:const Text('Otomatik altyazı',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:const Text('Konuşmaları yazı olarak göster',style:TextStyle(color:Colors.black54)),value:altyazi,onChanged:(v)async{await FirebaseFirestore.instance.collection('videos').doc(icerikId).set({'captionsEnabled':v},SetOptions(merge:true));setPencere(()=>altyazi=v);}),
    if(hizDegistir!=null)ListTile(leading:const Icon(Icons.speed_rounded,color:Colors.orange),title:const Text('Oynatma hızı',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Wrap(spacing:7,children:[.5,1.0,1.5,2.0].map((x)=>ActionChip(label:Text('${x}x'),onPressed:()async{await hizDegistir(x);if(c.mounted)Navigator.pop(c);})).toList())),
    ListTile(leading:const Icon(Icons.info_outline_rounded,color:Colors.black54),title:const Text('İçerik bilgileri',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text('İçerik kimliği: $icerikId',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black45))),
    ListTile(leading:const Icon(Icons.flag_outlined,color:Colors.redAccent),title:const Text('Bildir / Şikâyet et',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w700)),onTap:(){Navigator.pop(c);sikayetEt(context,hedefTuru:'paylasim',hedefId:icerikId,hedefUid:'');}),
  ]))));
}

Future<void> girisKaydiEkle(User user) async {
  try {
    final bilgi=await DeviceInfoPlugin().androidInfo;
    final cihaz='${bilgi.manufacturer} ${bilgi.model}'.trim();
    final onceki=await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    final oncekiCihaz=(onceki.data()?['lastLoginDevice']??'').toString();
    await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
      'lastLoginAt':FieldValue.serverTimestamp(),
      'lastLoginDevice':cihaz,
      'loginHistory':FieldValue.arrayUnion([{
        'device':cihaz,
        'platform':'Android ${bilgi.version.release}',
        'at':DateTime.now().toUtc().toIso8601String(),
      }]),
    },SetOptions(merge:true));
    if(oncekiCihaz.isNotEmpty&&oncekiCihaz!=cihaz&&(onceki.data()?['notificationsEnabled']!=false)){
      await FirebaseFirestore.instance.collection('notifications').add({'toUid':user.uid,'type':'security','text':'Yeni cihazdan giriş yapıldı: $cihaz','device':cihaz,'read':false,'createdAt':FieldValue.serverTimestamp()});
    }
  } catch (_) {}
}

Future<bool> misafirEngeli(BuildContext context) async {
  if (FirebaseAuth.instance.currentUser?.isAnonymous != true) return false;
  await showDialog<void>(context: context, builder: (ctx) => AlertDialog(
    title: const Text('Ngel X’e katıl ✨'),
    content: const Text('Bu özelliği kullanabilmek için ücretsiz hesap oluşturman gerekiyor.'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Gezmeye devam et')),
      TextButton(onPressed: () async { await FirebaseAuth.instance.signOut(); if (ctx.mounted) Navigator.of(ctx).pushAndRemoveUntil(MaterialPageRoute(builder: (_) => const GirisPage()), (_) => false); }, child: const Text('Giriş yap')),
      FilledButton(onPressed: () async { await FirebaseAuth.instance.signOut(); if (ctx.mounted) Navigator.of(ctx).pushAndRemoveUntil(MaterialPageRoute(builder: (_) => const KayitPage()), (_) => false); }, child: const Text('Şimdi kayıt ol')),
    ],
  ));
  return true;
}

Future<void> sikayetEt(BuildContext context,{required String hedefTuru,required String hedefId,String? hedefUid}) async {
  final bildiren=FirebaseAuth.instance.currentUser;
  if(bildiren==null||bildiren.isAnonymous){await misafirEngeli(context);return;}
  final neden=await showModalBottomSheet<String>(context:context,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[const ListTile(title:Text('Şikâyet nedenini seç',style:TextStyle(fontWeight:FontWeight.bold))),for(final n in ['Spam veya yanıltıcı','Taciz veya zorbalık','Nefret söylemi','Çıplaklık veya cinsel içerik','Şiddet veya tehlikeli davranış','Başkasını taklit ediyor'])ListTile(title:Text(n),onTap:()=>Navigator.pop(c,n)),const SizedBox(height:12)])));
  if(neden==null||!context.mounted)return;
  try{await FirebaseFirestore.instance.collection('reports').add({'reporterUid':bildiren.uid,'targetType':hedefTuru,'targetId':hedefId,'targetUid':hedefUid,'reason':neden,'status':'pending','createdAt':FieldValue.serverTimestamp()});if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Şikâyetin incelemeye gönderildi.')));}catch(e){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Şikâyet gönderilemedi: $e')));}
}

Future<void> kullaniciyiEngelle(BuildContext context,String hedefUid) async {
  final u=FirebaseAuth.instance.currentUser;if(u==null||u.isAnonymous)return;
  final tamam=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Kullanıcı engellensin mi?'),content:const Text('Birbirinizin profilini ve içeriklerini göremez, mesaj gönderemezsiniz.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),style:FilledButton.styleFrom(backgroundColor:Colors.red),child:const Text('Engelle'))]))??false;
  if(!tamam)return;
  try{await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'blocked':FieldValue.arrayUnion([hedefUid])},SetOptions(merge:true));if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Kullanıcı engellendi.')));}catch(e){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Engelleme tamamlanamadı: $e')));}
}

class NgelXApp extends StatelessWidget {
  const NgelXApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<String>(valueListenable: uygulamaDili, builder: (_, dil, __) => MaterialApp(
      key: ValueKey('ngelx_app_$dil'),
      debugShowCheckedModeBanner: false,
      title: 'NgelX',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF08080D),
        colorScheme: const ColorScheme.dark(
          primary: mor,
          secondary: mavi,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: panel,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(18),
            borderSide: BorderSide.none,
          ),
        ),
      ),
      home: UygulamaDurumKapisi(child:FirebaseAuth.instance.currentUser == null
          ? GirisPage(key: ValueKey('giris_$dil'))
          : AnaEkran(key: ValueKey('ana_$dil'))),
      builder: (context, child) => Directionality(textDirection: dil=='ar' ? TextDirection.rtl : TextDirection.ltr, child: child!),
    ));
  }
}

class UygulamaDurumKapisi extends StatefulWidget {final Widget child;const UygulamaDurumKapisi({super.key,required this.child});@override State<UygulamaDurumKapisi> createState()=>_UygulamaDurumKapisiState();}
class _UygulamaDurumKapisiState extends State<UygulamaDurumKapisi>{late Future<DocumentSnapshot<Map<String,dynamic>>> durum;@override void initState(){super.initState();yenile();}void yenile()=>durum=FirebaseFirestore.instance.collection('app_config').doc('status').get().timeout(const Duration(seconds:8));@override Widget build(BuildContext context)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:durum,builder:(context,s){if(s.connectionState==ConnectionState.waiting)return const Scaffold(backgroundColor:Colors.white,body:Center(child:CircularProgressIndicator()));if(s.hasError)return widget.child;final v=s.data?.data()??{};if(v['maintenance']!=true)return widget.child;return Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,body:SafeArea(child:Center(child:Padding(padding:const EdgeInsets.all(30),child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.engineering_outlined,size:88,color:mor),const SizedBox(height:20),const Text('Kısa bir bakımdayız',style:TextStyle(fontSize:28,fontWeight:FontWeight.w900)),const SizedBox(height:12),Text((v['message']??'Ngel X’i daha iyi hale getiriyoruz. Biraz sonra tekrar dene.').toString(),textAlign:TextAlign.center,style:const TextStyle(fontSize:16,color:Colors.black54)),const SizedBox(height:24),FilledButton.icon(onPressed:()=>setState(yenile),icon:const Icon(Icons.refresh),label:const Text('Tekrar dene'))]))))));});}

class GirisPage extends StatefulWidget {
  const GirisPage({super.key});

  @override
  State<GirisPage> createState() => _GirisPageState();
}

class _GirisPageState extends State<GirisPage> {
  final email = TextEditingController();
  final sifre = TextEditingController();
  final guvenliHafiza = const FlutterSecureStorage();
  bool gizli = true;
  bool beniHatirla = true;
  bool yukleniyor = false;
  List<String> kayitliEpostalar=[];
  List<String> epostaOnerileri=[];

  String sifreAnahtari(String adres)=>'ngelx_sifre_${adres.trim().toLowerCase()}';

  @override
  void initState() {
    super.initState();
    email.addListener(epostaDegisti);
    kayitliEpostayiGetir();
  }

  @override void dispose(){email.removeListener(epostaDegisti);email.dispose();sifre.dispose();super.dispose();}

  void epostaDegisti(){
    final arama=email.text.trim().toLowerCase();
    final yeni=arama.length<2?<String>[]:kayitliEpostalar.where((e)=>e.toLowerCase().startsWith(arama)&&e.toLowerCase()!=arama).take(5).toList();
    if(mounted&&yeni.join('|')!=epostaOnerileri.join('|'))setState(()=>epostaOnerileri=yeni);
  }

  Future<void> oneriyiSec(String adres) async {
    email.text=adres;
    sifre.text=await guvenliHafiza.read(key:sifreAnahtari(adres))??'';
    if(mounted)setState((){epostaOnerileri=[];beniHatirla=sifre.text.isNotEmpty;});
  }

  Future<void> kayitliEpostayiGetir() async {
    final hafiza = await SharedPreferences.getInstance();
    final kayitli = hafiza.getString('hatirlanan_eposta');
    kayitliEpostalar=hafiza.getStringList('hatirlanan_epostalar')??<String>[];
    if(kayitli!=null&&!kayitliEpostalar.contains(kayitli)){kayitliEpostalar.insert(0,kayitli);await hafiza.setStringList('hatirlanan_epostalar',kayitliEpostalar);}
    var kayitliSifre=kayitli==null?null:await guvenliHafiza.read(key:sifreAnahtari(kayitli));
    kayitliSifre??=await guvenliHafiza.read(key:'hatirlanan_sifre');
    if (!mounted) return;
    if (kayitli != null) email.text = kayitli;
    if (kayitliSifre != null) sifre.text = kayitliSifre;
    setState(()=>beniHatirla=kayitli!=null&&kayitliSifre!=null);
  }

  Future<void> hatirlamayiDegistir(bool deger) async {
    setState(()=>beniHatirla=deger);
    if(!deger){
      final adres=email.text.trim();final hafiza=await SharedPreferences.getInstance();
      kayitliEpostalar.removeWhere((e)=>e.toLowerCase()==adres.toLowerCase());
      await hafiza.setStringList('hatirlanan_epostalar',kayitliEpostalar);
      await hafiza.remove('hatirlanan_eposta');
      await guvenliHafiza.delete(key:sifreAnahtari(adres));
      await guvenliHafiza.delete(key:'hatirlanan_sifre');
    }
  }

  Future<void> girisYap() async {
    if (!email.text.contains('@') || sifre.text.length < 6) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Geçerli e-posta ve en az 6 karakterli şifre gir.')),
      );
      return;
    }
    final hafiza=await SharedPreferences.getInstance();
    final denemeAnahtari='giris_deneme_${email.text.trim().toLowerCase()}';
    final kilitAnahtari='giris_kilit_${email.text.trim().toLowerCase()}';
    final kilitBitis=hafiza.getInt(kilitAnahtari)??0;
    final simdi=DateTime.now().millisecondsSinceEpoch;
    if(kilitBitis>simdi){
      final saniye=((kilitBitis-simdi)/1000).ceil();
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Çok fazla hatalı deneme yapıldı. $saniye saniye sonra tekrar dene.')));
      return;
    }
    setState(() => yukleniyor = true);
    try {
      final sonuc = await FirebaseAuth.instance.signInWithEmailAndPassword(
        email: email.text.trim(),
        password: sifre.text,
      );
      await sonuc.user?.reload();
      if (FirebaseAuth.instance.currentUser?.emailVerified != true) {
        await FirebaseAuth.instance.currentUser?.sendEmailVerification();
        await FirebaseAuth.instance.signOut();
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('E-posta adresin henüz doğrulanmamış. Yeni doğrulama bağlantısı gönderildi; gelen kutunu kontrol et.')));
        return;
      }
      final profilBelgesi=await FirebaseFirestore.instance.collection('users').doc(sonuc.user!.uid).get();
      final profilVerisi=profilBelgesi.data()??{};
      if(profilVerisi['deactivated']==true&&mounted){
        final silmeTalebi=profilVerisi['deletionRequestedAt']!=null;
        final yenidenAc=await showDialog<bool>(context:context,barrierDismissible:false,builder:(c)=>AlertDialog(title:Text(silmeTalebi?'Hesap silme talebi var':'Hesap dondurulmuş'),content:Text(silmeTalebi?'Hesabın 30 günlük silme sürecinde. Şimdi geri açmak ister misin?':'Hesabını yeniden etkinleştirmek ister misin?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Hesabı geri aç'))]));
        if(yenidenAc!=true){await FirebaseAuth.instance.signOut();return;}
        await FirebaseFirestore.instance.collection('users').doc(sonuc.user!.uid).set({'deactivated':false,'deletionRequestedAt':FieldValue.delete(),'deletionScheduledFor':FieldValue.delete()},SetOptions(merge:true));
      }
      await girisKaydiEkle(FirebaseAuth.instance.currentUser!);
      await hafiza.remove(denemeAnahtari);
      await hafiza.remove(kilitAnahtari);
      if (beniHatirla) {
        final adres=email.text.trim();
        kayitliEpostalar.removeWhere((e)=>e.toLowerCase()==adres.toLowerCase());
        kayitliEpostalar.insert(0,adres);
        if(kayitliEpostalar.length>8)kayitliEpostalar=kayitliEpostalar.take(8).toList();
        await hafiza.setString('hatirlanan_eposta',adres);
        await hafiza.setStringList('hatirlanan_epostalar',kayitliEpostalar);
        await guvenliHafiza.write(key:sifreAnahtari(adres),value:sifre.text);
      } else {
        await hafiza.remove('hatirlanan_eposta');
        await guvenliHafiza.delete(key:'hatirlanan_sifre');
      }
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const AnaEkran()),
      );
    } on FirebaseAuthException catch (e) {
      if (!mounted) return;
      var mesaj='Giriş yapılamadı: ${e.message ?? e.code}';
      if(e.code=='invalid-credential'||e.code=='wrong-password'||e.code=='user-not-found'){
        final deneme=(hafiza.getInt(denemeAnahtari)??0)+1;
        if(deneme>=5){
          await hafiza.setInt(kilitAnahtari,DateTime.now().add(const Duration(minutes:1)).millisecondsSinceEpoch);
          await hafiza.remove(denemeAnahtari);
          mesaj='Çok fazla hatalı deneme yapıldı. Güvenliğin için giriş 1 dakika durduruldu.';
        }else{
          await hafiza.setInt(denemeAnahtari,deneme);
          mesaj='E-posta veya şifre yanlış. ${5-deneme} deneme hakkın kaldı.';
        }
      }
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(mesaj)));
    } finally {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  Future<void> misafirGirisi() async {
    setState(() => yukleniyor = true);
    try {
      await FirebaseAuth.instance.signInAnonymously();
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const AnaEkran()),
      );
    } on FirebaseAuthException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Misafir girişi başarısız: ${e.message ?? e.code}')),
      );
    } finally {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData.light().copyWith(
        colorScheme: ColorScheme.fromSeed(seedColor: mor),
        scaffoldBackgroundColor: Colors.white,
        inputDecorationTheme: InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none)),
      ),
      child: Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Align(alignment: Alignment.centerRight, child: PopupMenuButton<String>(initialValue: uygulamaDili.value, onSelected: diliDegistir, itemBuilder:(_)=>dilAdlari.entries.map((e)=>PopupMenuItem(value:e.key,child:Text(e.value))).toList(), child:Container(padding:const EdgeInsets.symmetric(horizontal:13,vertical:7),decoration:BoxDecoration(color:const Color(0xFFF3F4F6),borderRadius:BorderRadius.circular(18),border:Border.all(color:Colors.black12)),child:Row(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.language,size:18,color:Colors.black87),const SizedBox(width:7),Text(uygulamaDili.value.toUpperCase(),style:const TextStyle(color:Colors.black87))])))),
              const SizedBox(height: 45),
              const Logo(),
              const SizedBox(height: 55),
              Text(
                t('welcome'),
                style: const TextStyle(
                  fontSize: 31,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                t('tagline'),
                style: const TextStyle(color: Colors.black54),
              ),
              const SizedBox(height: 32),
              TextField(
                controller: email,
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  prefixIcon: const Icon(Icons.alternate_email),
                  hintText: t('email'),
                ),
              ),
              if(epostaOnerileri.isNotEmpty) Container(
                margin:const EdgeInsets.only(top:6),
                decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(14),border:Border.all(color:Colors.black12),boxShadow:const [BoxShadow(color:Colors.black12,blurRadius:10)]),
                child:Column(mainAxisSize:MainAxisSize.min,children:epostaOnerileri.map((adres)=>ListTile(dense:true,leading:const Icon(Icons.account_circle_outlined),title:Text(adres),onTap:()=>oneriyiSec(adres))).toList()),
              ),
              const SizedBox(height: 14),
              TextField(
                controller: sifre,
                obscureText: gizli,
                decoration: InputDecoration(
                  prefixIcon: const Icon(Icons.lock_outline),
                  hintText: t('password'),
                  suffixIcon: IconButton(
                    onPressed: () {
                      setState(() => gizli = !gizli);
                    },
                    icon: Icon(
                      gizli
                          ? Icons.visibility_off_outlined
                          : Icons.visibility_outlined,
                    ),
                  ),
                ),
              ),
              CheckboxListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(t('remember')),
                value: beniHatirla,
                onChanged: (v) => hatirlamayiDegistir(v ?? false),
                controlAffinity: ListTileControlAffinity.leading,
              ),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => SifreYenilePage(baslangicEposta: email.text.trim()))),
                  child: Text(t('forgot')),
                ),
              ),
              RenkliButon(
                yazi: yukleniyor ? '...' : t('login'),
                tiklama: yukleniyor ? () {} : girisYap,
              ),
              const SizedBox(height: 18),
              OutlinedButton.icon(
                onPressed: yukleniyor ? null : misafirGirisi,
                icon: const Icon(Icons.person_outline),
                label: Text(t('guest')),
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size.fromHeight(54),
                ),
              ),
              const SizedBox(height: 22),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(t('noAccount'), style: const TextStyle(color: Colors.black54)),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const KayitPage(),
                        ),
                      );
                    },
                    child: Text(t('createAccount')),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      ),
    );
  }
}

class SifreYenilePage extends StatefulWidget {
  final String baslangicEposta;
  const SifreYenilePage({super.key, this.baslangicEposta = ''});
  @override State<SifreYenilePage> createState() => _SifreYenilePageState();
}

class _SifreYenilePageState extends State<SifreYenilePage> {
  late final TextEditingController email;
  bool yukleniyor=false;
  @override void initState(){super.initState();email=TextEditingController(text:widget.baslangicEposta);}
  @override void dispose(){email.dispose();super.dispose();}
  Future<void> gonder() async {
    final adres=email.text.trim();
    if(!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(adres)){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Geçerli bir e-posta adresi yaz.')));return;}
    setState(()=>yukleniyor=true);
    try{await FirebaseAuth.instance.sendPasswordResetEmail(email:adres).timeout(const Duration(seconds:20));if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Şifre yenileme bağlantısı gönderildi. E-posta kutunu kontrol et.')));}
    on TimeoutException{if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('İşlem zaman aşımına uğradı. İnternet bağlantını kontrol et.')));}
    on FirebaseAuthException catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Bağlantı gönderilemedi: ${e.message ?? e.code}')));}
    catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Beklenmeyen bir hata oluştu. Tekrar dene.')));}
    finally{if(mounted)setState(()=>yukleniyor=false);}
  }
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(colorScheme:ColorScheme.fromSeed(seedColor:mor),scaffoldBackgroundColor:Colors.white,inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none))),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,title:Text(t('resetTitle'))),body:SafeArea(child:SingleChildScrollView(padding:const EdgeInsets.all(24),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[const Logo(),const SizedBox(height:36),Text(t('resetTitle'),style:const TextStyle(fontSize:28,fontWeight:FontWeight.w900)),const SizedBox(height:10),Text(t('resetInfo'),style:const TextStyle(color:Colors.black54)),const SizedBox(height:28),TextField(controller:email,keyboardType:TextInputType.emailAddress,decoration:InputDecoration(prefixIcon:const Icon(Icons.alternate_email),hintText:t('email'))),const SizedBox(height:22),RenkliButon(yazi:yukleniyor?'...':t('sendReset'),tiklama:yukleniyor?(){}:gonder),const SizedBox(height:12),TextButton(onPressed:()=>Navigator.pop(context),child:Text(t('backLogin')))])))));
}

class KayitPage extends StatefulWidget {
  const KayitPage({super.key});

  @override
  State<KayitPage> createState() => _KayitPageState();
}

class _KayitPageState extends State<KayitPage> {
  final kullanici = TextEditingController();
  final adSoyad = TextEditingController();
  final email = TextEditingController();
  final emailTekrar = TextEditingController();
  final sifre = TextEditingController();
  final sifreTekrar = TextEditingController();
  final dogumTarihi = TextEditingController();
  final telefon = TextEditingController();
  bool yukleniyor = false;
  bool sifreGizli = true;
  bool sifreTekrarGizli = true;
  bool kosullarKabul = false;

  int get sifrePuani {final s=sifre.text;var p=0;if(s.length>=8)p++;if(RegExp(r'[A-Z]').hasMatch(s)&&RegExp(r'[a-z]').hasMatch(s))p++;if(RegExp(r'\d').hasMatch(s))p++;if(RegExp(r'[^A-Za-z0-9]').hasMatch(s))p++;return p;}

  String? dogumKontrol(String metin){final m=RegExp(r'^(\d{2})/(\d{2})/(\d{4})$').firstMatch(metin);if(m==null)return 'Doğum tarihini GG/AA/YYYY biçiminde yaz. Örnek: 12/07/1994';final g=int.parse(m.group(1)!),a=int.parse(m.group(2)!),y=int.parse(m.group(3)!);try{final d=DateTime(y,a,g);final bugun=DateTime.now();if(d.day!=g||d.month!=a||d.year!=y||d.isAfter(bugun))return 'Geçerli bir doğum tarihi yaz.';var yas=bugun.year-y;if(bugun.month<a||(bugun.month==a&&bugun.day<g))yas--;if(yas<13)return 'Ngel X hesabı oluşturmak için en az 13 yaşında olmalısın.';if(yas>120)return 'Geçerli bir doğum tarihi yaz.';}catch(_){return 'Geçerli bir doğum tarihi yaz.';}return null;}

  Future<void> hesapOlustur() async {
    String? hata;
    const yasakliAdlar={'admin','administrator','ngelx','support','destek','moderator','root','official','resmi'};
    if(adSoyad.text.trim().split(RegExp(r'\s+')).length<2)hata='Adını ve soyadını eksiksiz yaz.';
    else if(!RegExp(r'^[a-zA-Z0-9_.]{3,20}$').hasMatch(kullanici.text.trim()))hata='Kullanıcı adı 3-20 karakter olmalı; yalnızca harf, sayı, nokta ve alt çizgi kullanılabilir.';
    else if(yasakliAdlar.contains(kullanici.text.trim().toLowerCase()))hata='Bu kullanıcı adı güvenlik nedeniyle kullanılamaz.';
    else if(!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email.text.trim()))hata='Geçerli bir e-posta adresi yaz.';
    else if(email.text.trim().toLowerCase()!=emailTekrar.text.trim().toLowerCase())hata='E-posta adresleri birbiriyle eşleşmiyor.';
    else if(sifre.text.length<8)hata='Şifre en az 8 karakter olmalı.';
    else if(sifrePuani<4)hata='Daha güçlü bir şifre seç: büyük-küçük harf, sayı ve özel karakter kullan.';
    else if(sifre.text!=sifreTekrar.text)hata='Şifreler birbiriyle eşleşmiyor.';
    else if(!kosullarKabul)hata='Devam etmek için Kullanım Koşulları ve Gizlilik Politikasını kabul et.';
    else hata=dogumKontrol(dogumTarihi.text.trim());
    final tel=telefon.text.replaceAll(RegExp(r'\D'),'');
    if(hata==null&&telefon.text.trim().isNotEmpty&&(tel.length<10||tel.length>15))hata='Telefon numarasını geçerli yaz veya alanı boş bırak.';
    if(hata!=null){ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hata)));return;}
    final yerelHafiza=await SharedPreferences.getInstance();
    final sonKayit=yerelHafiza.getInt('son_kayit_deneme')??0;
    final simdi=DateTime.now().millisecondsSinceEpoch;
    if(simdi-sonKayit<10000){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Lütfen tekrar denemeden önce 10 saniye bekle.')));return;}
    await yerelHafiza.setInt('son_kayit_deneme',simdi);
    setState(() => yukleniyor = true);
    User? yeniKullanici;
    try {
      final kullaniciKucuk=kullanici.text.trim().toLowerCase();
      final sonuc = await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: email.text.trim().toLowerCase(),
        password: sifre.text,
      ).timeout(const Duration(seconds:20));
      final yeni=sonuc.user!;
      yeniKullanici=yeni;
      final alinmis=await FirebaseFirestore.instance.collection('users').where('usernameLower',isEqualTo:kullaniciKucuk).limit(1).get().timeout(const Duration(seconds:20));
      if(alinmis.docs.isNotEmpty){
        await yeniKullanici?.delete();
        yeniKullanici=null;
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu kullanıcı adı alınmış. Başka bir kullanıcı adı seç.')));
        return;
      }
      await yeni.updateDisplayName(adSoyad.text.trim());
      await FirebaseFirestore.instance.collection('users').doc(yeni.uid).set({
        'username': kullanici.text.trim(),
        'usernameLower': kullaniciKucuk,
        'displayName': adSoyad.text.trim(),
        'email': email.text.trim().toLowerCase(),
        'birthDate': dogumTarihi.text.trim(),
        'phone': telefon.text.trim(),
        'emailVerified': false,
        'bio': 'NgelX dünyasına yeni katıldı ✦',
        'createdAt': FieldValue.serverTimestamp(),
      });
      await yeni.sendEmailVerification();
      await FirebaseAuth.instance.signOut();
      if (!mounted) return;
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const GirisPage()),
        (_) => false,
      );
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Doğrulama bağlantısı e-posta adresine gönderildi. E-postanı doğruladıktan sonra giriş yapabilirsin.')));
    } on FirebaseAuthException catch (e) {
      if (!mounted) return;
      final mesaj = e.code == 'email-already-in-use'
          ? 'Bu e-posta zaten kullanılıyor.'
          : 'Kayıt başarısız: ${e.message ?? e.code}';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(mesaj)));
    } on FirebaseException catch (e) {
      try { await yeniKullanici?.delete(); } catch (_) {}
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Profil kaydedilemedi: ${e.message ?? e.code}')));
    } on TimeoutException {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('İşlem zaman aşımına uğradı. İnternet bağlantını kontrol edip tekrar dene.')));
    } catch (e) {
      try { await yeniKullanici?.delete(); } catch (_) {}
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Hesap oluşturulamadı: $e')));
    } finally {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  @override void dispose(){for(final c in [kullanici,adSoyad,email,emailTekrar,sifre,sifreTekrar,dogumTarihi,telefon]){c.dispose();}super.dispose();}

  @override
  Widget build(BuildContext context) {
    return Theme(data:ThemeData.light().copyWith(colorScheme:ColorScheme.fromSeed(seedColor:mor),scaffoldBackgroundColor:Colors.white,inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none))),child:Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: Text(t('newAccount')),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(24, 24, 24, 110),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Logo(),
            const SizedBox(height: 35),
            TextField(
              controller: adSoyad,
              textCapitalization: TextCapitalization.words,
              decoration: InputDecoration(prefixIcon: const Icon(Icons.badge_outlined), hintText: t('fullName')),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: kullanici,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.person_outline),
                hintText: t('username'),
              ),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: email,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.alternate_email),
                hintText: t('email'),
              ),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: emailTekrar,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(prefixIcon: const Icon(Icons.alternate_email), hintText: t('emailAgain')),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: sifre,
              obscureText: sifreGizli,
              onChanged: (_) => setState((){}),
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.lock_outline),
                hintText: t('password8'),
                suffixIcon: IconButton(onPressed:()=>setState(()=>sifreGizli=!sifreGizli),icon:Icon(sifreGizli?Icons.visibility_off_outlined:Icons.visibility_outlined)),
              ),
            ),
            if(sifre.text.isNotEmpty) Padding(padding:const EdgeInsets.only(top:8),child:Row(children:[Expanded(child:LinearProgressIndicator(value:sifrePuani/4,color:sifrePuani>=4?Colors.green:sifrePuani>=2?Colors.orange:Colors.red,backgroundColor:Colors.black12)),const SizedBox(width:10),Text(sifrePuani>=4?t('strong'):sifrePuani>=2?t('medium'):t('weak'))])),
            const SizedBox(height: 14),
            TextField(
              controller: sifreTekrar,
              obscureText: sifreTekrarGizli,
              decoration: InputDecoration(prefixIcon: const Icon(Icons.lock_outline), hintText: t('passwordAgain'),suffixIcon:IconButton(onPressed:()=>setState(()=>sifreTekrarGizli=!sifreTekrarGizli),icon:Icon(sifreTekrarGizli?Icons.visibility_off_outlined:Icons.visibility_outlined))),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: dogumTarihi,
              keyboardType: TextInputType.datetime,
              maxLength: 10,
              decoration: InputDecoration(prefixIcon: const Icon(Icons.cake_outlined), hintText: t('birthDate'), counterText: ''),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: telefon,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(prefixIcon: const Icon(Icons.phone_outlined), hintText: t('phone'), helperText: t('phoneOptional')),
            ),
            CheckboxListTile(contentPadding:EdgeInsets.zero,value:kosullarKabul,onChanged:(v)=>setState(()=>kosullarKabul=v??false),controlAffinity:ListTileControlAffinity.leading,title:Text(t('terms'))),
            const SizedBox(height: 24),
            RenkliButon(
              yazi: yukleniyor ? t('creating') : t('createAccount'),
              tiklama: yukleniyor ? () {} : hesapOlustur,
            ),
          ],
        ),
      ),
      ),
    ));
  }
}

class AnaEkran extends StatefulWidget {
  const AnaEkran({super.key});

  @override
  State<AnaEkran> createState() => _AnaEkranState();
}

class _AnaEkranState extends State<AnaEkran> {
  int secili = 0;

  @override
  Widget build(BuildContext context) {
    final sayfalar = [
      VideoAkisi(gorunur: secili == 0),
      KesfetPage(gorunur: secili == 1),
      const YuklePage(),
      const MesajPage(),
      const ProfilPage(),
    ];
    return Scaffold(
      body: IndexedStack(
        index: secili,
        children: sayfalar,
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: Color(0xFF101016),
          border: Border(top: BorderSide(color: Color(0xFF292936))),
          boxShadow: [BoxShadow(color: Colors.black54, blurRadius: 18)],
        ),
        child: NavigationBar(
          height: 76,
          selectedIndex: secili,
          backgroundColor: Colors.transparent,
          indicatorColor: const Color(0xFF22D3EE),
          labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
          onDestinationSelected: (i) async {
            if (i != 0 && await misafirEngeli(context)) return;
            if (mounted) setState(() => secili = i);
          },
          destinations: [
            NavigationDestination(icon: const Icon(Icons.play_circle_outline), selectedIcon: const Icon(Icons.play_circle_fill, color: Colors.black), label: t('flow')),
            NavigationDestination(icon: const Icon(Icons.explore_outlined), selectedIcon: const Icon(Icons.explore, color: Colors.black), label: t('explore')),
            NavigationDestination(icon: const Icon(Icons.add_box_outlined, size: 31), selectedIcon: const Icon(Icons.add_box, color: Colors.black, size: 34), label: t('create')),
            NavigationDestination(icon: const Badge(child: Icon(Icons.forum_outlined)), selectedIcon: const Icon(Icons.forum, color: Colors.black), label: t('chat')),
            NavigationDestination(icon: const Icon(Icons.person_outline), selectedIcon: const Icon(Icons.person, color: Colors.black), label: t('me')),
          ],
        ),
      ),
    );
  }
}

class VideoAkisi extends StatefulWidget {
  final bool gorunur;
  const VideoAkisi({super.key, required this.gorunur});

  @override
  State<VideoAkisi> createState() => _VideoAkisiState();
}

class _VideoAkisiState extends State<VideoAkisi> {
  int aktif = 0;
  bool takipSekmesi = false;
  Set<String> takipEdilenler = {};
  Set<String> engellenenler = {};

  @override
  void initState() {
    super.initState();
    takipListesiniGetir();
  }

  Future<void> takipListesiniGetir() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;
    final d = await FirebaseFirestore.instance.collection('users').doc(uid).get();
    if (!mounted) return;
    setState(() {
      takipEdilenler = Set<String>.from(List<dynamic>.from(d.data()?['following'] ?? []));
      engellenenler = Set<String>.from(List<dynamic>.from(d.data()?['blocked'] ?? []));
    });
  }

  static const ornekVideolar = [
    {
      'id': 'ornek_1',
      'videoUrl': 'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4',
      'username': 'ngelx_1',
      'ownerId': '',
      'type': 'video',
    },
    {
      'id': 'ornek_2',
      'videoUrl': 'https://flutter.github.io/assets-for-api-docs/assets/videos/butterfly.mp4',
      'username': 'ngelx_2',
      'ownerId': '',
      'type': 'video',
    },
    {
      'id': 'ornek_3',
      'videoUrl': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
      'username': 'ngelx_3',
      'ownerId': '',
      'type': 'video',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
          stream: FirebaseFirestore.instance
              .collection('videos')
              .orderBy('createdAt', descending: true)
              .limit(20)
              .snapshots(),
          builder: (context, snapshot) {
            final yuklenenler = (snapshot.data?.docs ?? []).map((belge) {
              final veri = belge.data();
              return {
                'id': belge.id,
                'videoUrl': (veri['videoUrl'] ?? '').toString(),
                'username': (veri['username'] ?? 'ngelx').toString(),
                'ownerId': (veri['ownerId'] ?? '').toString(),
                'type': (veri['type'] ?? 'video').toString(),
                'mediaUrl': (veri['mediaUrl'] ?? veri['videoUrl'] ?? '').toString(),
                'audioUrl': (veri['audioUrl'] ?? '').toString(),
                'description': (veri['description'] ?? '').toString(),
                'allowDownload': (veri['allowDownload'] ?? true).toString(),
              };
            }).where((v) => v['type'] != 'story' && !engellenenler.contains(v['ownerId'])).toList();
            final filtreli = takipSekmesi ? yuklenenler.where((v) => takipEdilenler.contains(v['ownerId'])).toList() : yuklenenler;
            final videolar = takipSekmesi ? filtreli : [...filtreli, ...ornekVideolar];
            if (videolar.isEmpty) return const Center(child: Padding(padding: EdgeInsets.all(30), child: Text('Takip ettiğin kişilerin paylaşımları burada görünecek.', textAlign: TextAlign.center)));
            return PageView.builder(
              scrollDirection: Axis.vertical,
              itemCount: videolar.length,
              onPageChanged: (i) => setState(() => aktif = i),
              itemBuilder: (_, i) {
                final item = videolar[i];
                final tur = item['type'] ?? 'video';
                if (tur == 'video') {
                  return VideoKarti(
                    adres: item['videoUrl'] ?? item['mediaUrl'] ?? '',
                    videoId: item['id']!,
                    kullaniciAdi: item['username']!,
                    ownerId: item['ownerId']!,
                    indirilebilir: item['allowDownload'] != 'false',
                    aktif: widget.gorunur && aktif == i,
                  );
                }
                return GorselYaziKarti(
                  veri: item,
                  aktif: widget.gorunur && aktif == i,
                );
              },
            );
          },
        ),
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(17),
            child: Row(
              children: [
                const Logo(kucuk: true),
                const Spacer(),
                GestureDetector(onTap: () => setState(() { takipSekmesi = true; aktif = 0; }), child: Text('Takip', style: TextStyle(color: takipSekmesi ? Colors.white : Colors.white60, fontWeight: takipSekmesi ? FontWeight.bold : FontWeight.normal, decoration: takipSekmesi ? TextDecoration.underline : null, decorationColor: mavi, decorationThickness: 3))),
                const SizedBox(width: 17),
                GestureDetector(onTap: () => setState(() { takipSekmesi = false; aktif = 0; }), child: Text('Sana Özel', style: TextStyle(color: takipSekmesi ? Colors.white60 : Colors.white, fontWeight: takipSekmesi ? FontWeight.normal : FontWeight.bold, decoration: takipSekmesi ? null : TextDecoration.underline, decorationColor: mor, decorationThickness: 3))),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AramaPage())),
                  icon: const Icon(Icons.search_rounded, size: 31),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class AramaPage extends StatefulWidget {
  const AramaPage({super.key});
  @override
  State<AramaPage> createState() => _AramaPageState();
}

class _AramaPageState extends State<AramaPage> {
  final ara = TextEditingController();
  String sorgu = '';
  Set<String> engellenenler={};

  @override void initState(){super.initState();engellenenleriGetir();}
  Future<void> engellenenleriGetir()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();if(mounted)setState(()=>engellenenler=Set<String>.from(List<dynamic>.from(d.data()?['blocked']??const[])));}

  @override
  void dispose() { ara.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0D0D14),
        titleSpacing: 0,
        title: TextField(
          controller: ara,
          autofocus: true,
          onChanged: (v) => setState(() => sorgu = v.trim().toLowerCase()),
          decoration: InputDecoration(hintText: 'Kullanıcı, video, etiket ara', prefixIcon: const Icon(Icons.search), suffixIcon: sorgu.isEmpty ? null : IconButton(onPressed: () { ara.clear(); setState(() => sorgu = ''); }, icon: const Icon(Icons.cancel))),
        ),
        actions: [TextButton(onPressed: () => FocusScope.of(context).unfocus(), child: const Text('Ara', style: TextStyle(color: mavi, fontWeight: FontWeight.bold)))],
      ),
      body: sorgu.isEmpty
          ? const Center(child: Column(mainAxisSize: MainAxisSize.min, children: [Icon(Icons.manage_search_rounded, size: 75, color: mavi), SizedBox(height: 12), Text('NgelX’te istediğini ara', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)), SizedBox(height: 6), Text('Kullanıcılar, açıklamalar ve etiketler', style: TextStyle(color: Colors.white38))]))
          : FutureBuilder<List<QuerySnapshot<Map<String, dynamic>>>>(
              future: Future.wait([
                FirebaseFirestore.instance.collection('users').limit(60).get(),
                FirebaseFirestore.instance.collection('videos').limit(100).get(),
              ]),
              builder: (_, snap) {
                if (!snap.hasData) return const Center(child: CircularProgressIndicator(color: mavi));
                bool eslesir(String metin) => metin.toLowerCase().split(RegExp(r'[^a-z0-9ığüşöç]+')).any((kelime) => kelime.startsWith(sorgu));
                final kullanicilar = snap.data![0].docs.where((d) { final v=d.data(); return !engellenenler.contains(d.id)&&v['deactivated']!=true&&eslesir('${v['username'] ?? ''} ${v['displayName'] ?? ''}'); }).toList();
                final icerikler = snap.data![1].docs.where((d) { final v=d.data(); return !engellenenler.contains((v['ownerId']??'').toString())&&v['type'] != 'story' && '${v['description'] ?? ''} ${v['username'] ?? ''}'.toLowerCase().contains(sorgu); }).toList();
                if (kullanicilar.isEmpty && icerikler.isEmpty) return const Center(child: Text('Sonuç bulunamadı.'));
                return ListView(children: [
                  if (kullanicilar.isNotEmpty) const Padding(padding: EdgeInsets.fromLTRB(18, 20, 18, 8), child: Text('Kullanıcılar', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: mavi))),
                  ...kullanicilar.map((d) { final v=d.data(); final foto=(v['photoUrl'] ?? '').toString(); return ListTile(onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => KullaniciProfilPage(uid: d.id))), leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : NetworkImage(foto), child: foto.isEmpty ? const Text('N') : null), title: Text((v['displayName'] ?? v['username'] ?? 'NgelX').toString()), subtitle: Text('@${v['username'] ?? 'ngelx'}'), trailing: const Icon(Icons.chevron_right)); }),
                  if (icerikler.isNotEmpty) const Padding(padding: EdgeInsets.fromLTRB(18, 20, 18, 8), child: Text('Paylaşımlar', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: mor))),
                  ...icerikler.map((d) { final v=d.data(); final tur=(v['type'] ?? 'video').toString(); final item=<String,String>{'id':d.id,'type':tur,'videoUrl':(v['videoUrl']??'').toString(),'mediaUrl':(v['mediaUrl']??'').toString(),'audioUrl':(v['audioUrl']??'').toString(),'description':(v['description']??'').toString(),'username':(v['username']??'ngelx').toString(),'ownerId':(v['ownerId']??'').toString(),'allowDownload':(v['allowDownload']??true).toString()}; return ListTile(onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => Scaffold(body: SafeArea(child: tur=='video' ? VideoKarti(adres:item['videoUrl']!,videoId:item['id']!,kullaniciAdi:item['username']!,ownerId:item['ownerId']!,indirilebilir:item['allowDownload']!='false',aktif:true) : GorselYaziKarti(veri:item,aktif:true))))), leading: Icon(tur == 'video' ? Icons.videocam : tur == 'photo' ? Icons.photo : Icons.text_fields, color: mor), title: Text((v['description'] ?? 'NgelX paylaşımı').toString(), maxLines: 2, overflow: TextOverflow.ellipsis), subtitle: Text('@${v['username'] ?? 'ngelx'}')); }),
                ]);
              },
            ),
    );
  }
}

class HikayeSeridi extends StatelessWidget {
  const HikayeSeridi({super.key});

  Future<List<Map<String, dynamic>>> gorunebilirHikayeler(List<QueryDocumentSnapshot<Map<String, dynamic>>> belgeler) async {
    final ben = FirebaseAuth.instance.currentUser?.uid;
    if (ben == null) return [];
    final benimBelgem = await FirebaseFirestore.instance.collection('users').doc(ben).get();
    final arkadaslar = Set<String>.from(List<dynamic>.from(benimBelgem.data()?['friends'] ?? []));
    final simdi = DateTime.now();
    final adaylar = belgeler.map((d) => d.data()).where((v) {
      final bitis = v['expiresAt'];
      return v['type'] == 'story' && bitis is Timestamp && bitis.toDate().isAfter(simdi);
    }).toList();
    final sonuc = <Map<String, dynamic>>[];
    for (final h in adaylar) {
      final sahibi = (h['ownerId'] ?? '').toString();
      if (sahibi.isEmpty || sahibi == ben) { sonuc.add(h); continue; }
      final sahipBelgesi = await FirebaseFirestore.instance.collection('users').doc(sahibi).get();
      final profil = sahipBelgesi.data() ?? {};
      if (profil['deactivated'] == true) continue;
      if (profil['friendsOnlyStory'] != false && !arkadaslar.contains(sahibi)) continue;
      sonuc.add(h);
    }
    return sonuc;
  }

  void ac(BuildContext context, Map<String, dynamic> veri) {
    showDialog(
      context: context,
      barrierColor: Colors.black,
      builder: (_) => Dialog.fullscreen(
        backgroundColor: Colors.black,
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.network(veri['mediaUrl'] ?? '', fit: BoxFit.contain),
            const Positioned(
              top: 45,
              left: 18,
              right: 18,
              child: LinearProgressIndicator(value: 1, color: mavi),
            ),
            Positioned(
              top: 62,
              left: 20,
              child: Text('@${veri['username'] ?? 'ngelx'}', style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
            Positioned(
              top: 48,
              right: 14,
              child: IconButton(icon: const Icon(Icons.close, size: 30), onPressed: () => Navigator.pop(context)),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 82,
      child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
        stream: FirebaseFirestore.instance.collection('videos').limit(80).snapshots(),
        builder: (_, snap) {
          if (!snap.hasData) return const SizedBox.shrink();
          return FutureBuilder<List<Map<String, dynamic>>>(
            future: gorunebilirHikayeler(snap.data!.docs),
            builder: (_, gorunur) {
              final hikayeler = gorunur.data ?? [];
              if (hikayeler.isEmpty) return const SizedBox.shrink();
              return ListView.separated(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            scrollDirection: Axis.horizontal,
            itemCount: hikayeler.length,
            separatorBuilder: (_, __) => const SizedBox(width: 10),
            itemBuilder: (_, i) {
              final h = hikayeler[i];
              return GestureDetector(
                onTap: () => ac(context, h),
                child: Container(
                  width: 70,
                  padding: const EdgeInsets.all(3),
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: LinearGradient(colors: [mavi, mor, Colors.pinkAccent]),
                    boxShadow: [BoxShadow(color: mor, blurRadius: 12)],
                  ),
                  child: CircleAvatar(
                    backgroundColor: panel,
                    backgroundImage: NetworkImage((h['mediaUrl'] ?? '').toString()),
                  ),
                ),
              );
            },
              );
            },
          );
        },
      ),
    );
  }
}

Future<void> kendiPaylasiminiSil(BuildContext context, String id, Map<String, dynamic> veri) async {
  final uid = FirebaseAuth.instance.currentUser?.uid;
  if (uid == null || id.isEmpty || uid != (veri['ownerId'] ?? '').toString()) return;
  final onay = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
    title: const Text('Bu paylaşımı silmek istiyor musun?'),
    content: const Text('Paylaşım profilinden, Akıştan ve Keşfetten tamamen kaldırılacak.'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Vazgeç')),
      TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Sil', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold))),
    ],
  ));
  if (onay != true) return;
  final ref = FirebaseFirestore.instance.collection('videos').doc(id);
  final likes = await ref.collection('likes').get();
  final comments = await ref.collection('comments').get();
  final batch = FirebaseFirestore.instance.batch();
  for (final x in likes.docs) { batch.delete(x.reference); }
  for (final x in comments.docs) { batch.delete(x.reference); }
  batch.delete(ref);
  await batch.commit();
  for (final raw in [(veri['mediaUrl'] ?? '').toString(), (veri['videoUrl'] ?? '').toString(), (veri['audioUrl'] ?? '').toString()]) {
    if (raw.isEmpty) continue;
    try { final parts = Uri.parse(raw).pathSegments; final i = parts.indexOf('ngelx-media'); if (i >= 0 && i + 1 < parts.length) await supa.Supabase.instance.client.storage.from('ngelx-media').remove([parts.sublist(i + 1).join('/')]); } catch (_) {}
  }
  if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Paylaşım tüm alanlardan silindi.')));
}

Future<void> kendiPaylasimMenusu(BuildContext context, String id, Map<String, dynamic> veri) async {
  if (FirebaseAuth.instance.currentUser?.uid != (veri['ownerId'] ?? '').toString()) return;
  await showModalBottomSheet(context: context, backgroundColor: panel, builder: (ctx) => SafeArea(child: Column(mainAxisSize: MainAxisSize.min, children: [
    Container(width: 42, height: 4, margin: const EdgeInsets.all(12), decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(8))),
    ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, id, veri); }),
  ])));
}

class GorselYaziKarti extends StatefulWidget {
  final Map<String, String> veri;
  final bool aktif;
  const GorselYaziKarti({super.key, required this.veri, required this.aktif});

  @override
  State<GorselYaziKarti> createState() => _GorselYaziKartiState();
}

class _GorselYaziKartiState extends State<GorselYaziKarti> {
  AudioPlayer? oynatici;
  bool begenildi = false;
  bool kaydedildi = false;
  bool indiriliyor = false;
  int begeniSayisi = 0;
  int yorumSayisi = 0;

  String get icerikId => widget.veri['id'] ?? '';
  bool get indirilebilir => widget.veri['allowDownload'] != 'false' || FirebaseAuth.instance.currentUser?.uid == widget.veri['ownerId'];

  @override
  void initState() {
    super.initState();
    etkilesimleriGetir();
    final ses = widget.veri['audioUrl'] ?? '';
    if (ses.isNotEmpty) {
      oynatici = AudioPlayer();
      oynatici!.setUrl(ses).then((_) {
        oynatici!.setLoopMode(LoopMode.one);
        if (widget.aktif) oynatici!.play();
      });
    }
  }

  Future<void> etkilesimleriGetir() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || icerikId.isEmpty) return;
    final ref = FirebaseFirestore.instance.collection('videos').doc(icerikId);
    final sonuclar = await Future.wait([
      ref.collection('likes').doc(user.uid).get(),
      ref.collection('likes').count().get(),
      ref.collection('comments').count().get(),
      FirebaseFirestore.instance.collection('users').doc(user.uid).collection('saved').doc(icerikId).get(),
    ]);
    if (!mounted) return;
    setState(() {
      begenildi = (sonuclar[0] as DocumentSnapshot).exists;
      begeniSayisi = (sonuclar[1] as AggregateQuerySnapshot).count ?? 0;
      yorumSayisi = (sonuclar[2] as AggregateQuerySnapshot).count ?? 0;
      kaydedildi = (sonuclar[3] as DocumentSnapshot).exists;
    });
  }

  Future<void> icerigiKaydet() async {
    if (await misafirEngeli(context)) return;
    final user=FirebaseAuth.instance.currentUser;if(user==null||icerikId.isEmpty)return;
    final ref=FirebaseFirestore.instance.collection('users').doc(user.uid).collection('saved').doc(icerikId);
    final yeni=!kaydedildi;setState(()=>kaydedildi=yeni);
    try{if(yeni){await ref.set({'contentId':icerikId,'type':widget.veri['type']??'photo','savedAt':FieldValue.serverTimestamp()});}else{await ref.delete();}if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(yeni?'Kaydedilenlere eklendi ✅':'Kaydedilenlerden kaldırıldı.')));}catch(e){if(mounted)setState(()=>kaydedildi=!yeni);}
  }

  Future<void> begeniyiDegistir() async {
    if (await misafirEngeli(context)) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || icerikId.isEmpty) return;
    final ref = FirebaseFirestore.instance.collection('videos').doc(icerikId).collection('likes').doc(user.uid);
    final yeni = !begenildi;
    setState(() {
      begenildi = yeni;
      begeniSayisi += yeni ? 1 : -1;
      if (begeniSayisi < 0) begeniSayisi = 0;
    });
    if (yeni) {
      await ref.set({'userId': user.uid, 'createdAt': FieldValue.serverTimestamp()});
    } else {
      await ref.delete();
    }
  }

  void yorumlariAc() {
    if (icerikId.isEmpty) return;
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(25))),
      builder: (_) => Yorumlar(videoId: icerikId),
    ).whenComplete(etkilesimleriGetir);
  }

  Future<void> fotografiKaydet() async {
    if (await misafirEngeli(context)) return;
    final foto = widget.veri['mediaUrl'] ?? '';
    if (foto.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Bu yazı Kaydet düğmesiyle koleksiyonuna eklenebilir.')));
      return;
    }
    if (indiriliyor) return;
    setState(() => indiriliyor = true);
    File? gecici;
    try {
      if (!await Gal.hasAccess()) await Gal.requestAccess();
      final klasor = await getTemporaryDirectory();
      gecici = File('${klasor.path}/ngelx_${DateTime.now().millisecondsSinceEpoch}.jpg');
      await Dio().download(foto, gecici.path);
      await Gal.putImage(gecici.path);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Fotoğraf galeriye kaydedildi ✅')));
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Fotoğraf kaydedilemedi. Galeri iznini aç.')));
    } finally {
      if (gecici != null && await gecici.exists()) await gecici.delete();
      if (mounted) setState(() => indiriliyor = false);
    }
  }

  Future<void> paylas() async {
    final foto = widget.veri['mediaUrl'] ?? '';
    final yazi = widget.veri['description'] ?? '';
    await SharePlus.instance.share(ShareParams(text: foto.isEmpty ? 'NgelX paylaşımı: $yazi' : 'NgelX paylaşımı: $yazi\n$foto'));
  }

  Future<void> uzunBasmaMenusu() async {
    final sahibi = FirebaseAuth.instance.currentUser?.uid == widget.veri['ownerId'];
    await showModalBottomSheet(
      context: context,
      backgroundColor: panel,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
      builder: (ctx) => SafeArea(child: Column(mainAxisSize: MainAxisSize.min, children: [
        Container(width: 42, height: 4, margin: const EdgeInsets.all(12), decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(9))),
        if (indirilebilir) ListTile(leading: const Icon(Icons.download_rounded, color: mavi), title: const Text('İndir'), onTap: () { Navigator.pop(ctx); fotografiKaydet(); }),
        ListTile(leading: const Icon(Icons.heart_broken_outlined), title: const Text('İlgilenmiyorum'), onTap: () { Navigator.pop(ctx); ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Benzer içerikler azaltılacak.'))); }),
        ListTile(leading: const Icon(Icons.flag_outlined, color: Colors.orange), title: const Text('Bildir / Şikâyet et'), onTap: () { Navigator.pop(ctx); sikayetEt(context,hedefTuru:'paylasim',hedefId:icerikId,hedefUid:(widget.veri['ownerId']??'').toString()); }),
        if(!sahibi) ListTile(leading:const Icon(Icons.block,color:Colors.red),title:const Text('Kullanıcıyı engelle',style:TextStyle(color:Colors.red)),onTap:(){Navigator.pop(ctx);kullaniciyiEngelle(context,(widget.veri['ownerId']??'').toString());}),
        if (sahibi) ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, icerikId, widget.veri); }),
      ])),
    );
  }

  @override
  void didUpdateWidget(covariant GorselYaziKarti oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.aktif) {
      oynatici?.play();
    } else {
      oynatici?.pause();
    }
  }

  @override
  void dispose() {
    oynatici?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final foto = widget.veri['mediaUrl'] ?? '';
    final yazi = widget.veri['description'] ?? '';
    return GestureDetector(
      onLongPress: uzunBasmaMenusu,
      child: Container(
        color: const Color(0xFF09090F),
        child: Stack(
        fit: StackFit.expand,
        children: [
          if (foto.isNotEmpty)
            Image.network(foto, fit: BoxFit.contain)
          else
            Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(35),
              decoration: const BoxDecoration(
                gradient: LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Color(0xFF16213E), Color(0xFF47256D)]),
              ),
              child: Text(yazi, textAlign: TextAlign.center, style: const TextStyle(fontSize: 29, height: 1.3, fontWeight: FontWeight.w800)),
            ),
          const DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.black54, Colors.transparent, Colors.black87]),
            ),
          ),
          Positioned(
            left: 20,
            bottom: 28,
            right: 82,
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('@${widget.veri['username'] ?? 'ngelx'}', style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold)),
              if (foto.isNotEmpty && yazi.isNotEmpty) ...[const SizedBox(height: 8), Text(yazi)],
              if ((widget.veri['audioUrl'] ?? '').isNotEmpty) ...[const SizedBox(height: 8), const Row(children: [Icon(Icons.music_note, size: 18), Text(' Fotoğraflı müzik')])],
            ]),
          ),
          Positioned(
            right: 15,
            bottom: 25,
            child: Column(children: [
              IslemButonu(ikon: begenildi ? Icons.favorite : Icons.favorite_border, yazi: '$begeniSayisi', renk: begenildi ? Colors.pinkAccent : Colors.white, tiklama: begeniyiDegistir),
              IslemButonu(ikon: Icons.mode_comment_outlined, yazi: '$yorumSayisi', tiklama: yorumlariAc),
              IslemButonu(ikon: kaydedildi ? Icons.bookmark : Icons.bookmark_border, yazi: kaydedildi ? 'Kaydedildi' : 'Kaydet', renk: kaydedildi ? mavi : Colors.white, tiklama: icerigiKaydet),
              IslemButonu(ikon: Icons.menu_rounded, yazi: 'Araçlar', tiklama: () => icerikAracMenusu(context,icerikId)),
              IslemButonu(ikon: Icons.send_outlined, yazi: 'Paylaş', tiklama: paylas),
            ]),
          ),
          ],
        ),
      ),
    );
  }
}

class VideoKarti extends StatefulWidget {
  final String adres;
  final String videoId;
  final String kullaniciAdi;
  final String ownerId;
  final bool aktif;
  final bool indirilebilir;

  const VideoKarti({
    super.key,
    required this.adres,
    required this.videoId,
    required this.kullaniciAdi,
    required this.ownerId,
    required this.aktif,
    this.indirilebilir = true,
  });

  @override
  State<VideoKarti> createState() => _VideoKartiState();
}

class _VideoKartiState extends State<VideoKarti> with WidgetsBindingObserver {
  late final VideoPlayerController kontrol;
  bool hazir = false;
  bool begenildi = false;
  bool kaydedildi = false;
  int begeniSayisi = 0;
  int yorumSayisi = 0;
  bool duraklatildi = false;
  bool indiriliyor = false;
  String profilFoto = '';

  String get videoId => widget.videoId;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);

    kontrol = VideoPlayerController.networkUrl(
      Uri.parse(widget.adres),
    );

    etkilesimleriGetir();
    profilFotosunuGetir();

    kontrol.initialize().then((_) {
      kontrol.setLooping(true);

      if (widget.aktif) {
        kontrol.play();
      }

      if (mounted) {
        setState(() => hazir = true);
      }
    });
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state != AppLifecycleState.resumed && hazir) kontrol.pause();
    if (state == AppLifecycleState.resumed && widget.aktif && !duraklatildi && hazir) {
      kontrol.play();
    }
  }

  Future<void> profilFotosunuGetir() async {
    if (widget.ownerId.isEmpty) return;
    final belge = await FirebaseFirestore.instance
        .collection('users')
        .doc(widget.ownerId)
        .get();
    if (!mounted) return;
    setState(() => profilFoto = (belge.data()?['photoUrl'] ?? '').toString());
  }

  Future<void> etkilesimleriGetir() async {
    final kullanici = FirebaseAuth.instance.currentUser;
    if (kullanici == null) return;
    final video = FirebaseFirestore.instance.collection('videos').doc(videoId);
    final sonuclar = await Future.wait([
      video.collection('likes').doc(kullanici.uid).get(),
      video.collection('likes').count().get(),
      video.collection('comments').count().get(),
      FirebaseFirestore.instance.collection('users').doc(kullanici.uid).collection('saved').doc(videoId).get(),
    ]);
    if (!mounted) return;
    setState(() {
      begenildi = (sonuclar[0] as DocumentSnapshot).exists;
      begeniSayisi = (sonuclar[1] as AggregateQuerySnapshot).count ?? 0;
      yorumSayisi = (sonuclar[2] as AggregateQuerySnapshot).count ?? 0;
      kaydedildi = (sonuclar[3] as DocumentSnapshot).exists;
    });
  }

  Future<void> videoyuKaydet() async {
    if(await misafirEngeli(context))return;final u=FirebaseAuth.instance.currentUser;if(u==null||videoId.isEmpty)return;
    final ref=FirebaseFirestore.instance.collection('users').doc(u.uid).collection('saved').doc(videoId),yeni=!kaydedildi;setState(()=>kaydedildi=yeni);
    try{if(yeni){await ref.set({'contentId':videoId,'type':'video','savedAt':FieldValue.serverTimestamp()});}else{await ref.delete();}if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(yeni?'Kaydedilenlere eklendi ✅':'Kaydedilenlerden kaldırıldı.')));}catch(e){if(mounted)setState(()=>kaydedildi=!yeni);}
  }

  Future<void> begeniyiDegistir() async {
    if (await misafirEngeli(context)) return;
    final kullanici = FirebaseAuth.instance.currentUser;
    if (kullanici == null) return;
    final video = FirebaseFirestore.instance.collection('videos').doc(videoId);
    final begeni = video.collection('likes').doc(kullanici.uid);
    final yeniDurum = !begenildi;
    setState(() {
      begenildi = yeniDurum;
      begeniSayisi += yeniDurum ? 1 : -1;
      if (begeniSayisi < 0) begeniSayisi = 0;
    });
    if (yeniDurum) {
      await begeni.set({
        'userId': kullanici.uid,
        'createdAt': FieldValue.serverTimestamp(),
      });
    } else {
      await begeni.delete();
    }
  }

  Future<void> videoyuPaylas() async {
    await SharePlus.instance.share(
      ShareParams(
        text: 'NgelX videosu: ${widget.adres}',
        title: 'NgelX videosunu paylaş',
      ),
    );
  }

  Future<void> videoyuGaleriyeKaydet() async {
    if (await misafirEngeli(context)) return;
    if (indiriliyor) return;
    setState(() => indiriliyor = true);
    File? geciciDosya;
    try {
      if (!await Gal.hasAccess()) {
        await Gal.requestAccess();
      }
      final klasor = await getTemporaryDirectory();
      geciciDosya = File(
        '${klasor.path}/ngelx_${DateTime.now().millisecondsSinceEpoch}.mp4',
      );
      await Dio().download(widget.adres, geciciDosya.path);
      await Gal.putVideo(geciciDosya.path);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Video galeriye kaydedildi ✅')),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Video kaydedilemedi. Fotoğraf ve video iznini aç.'),
        ),
      );
    } finally {
      if (geciciDosya != null && await geciciDosya.exists()) {
        await geciciDosya.delete();
      }
      if (mounted) setState(() => indiriliyor = false);
    }
  }

  Future<void> paylasanProfiliAc() async {
    if (widget.ownerId.isEmpty) return;
    final belge = await FirebaseFirestore.instance.collection('users').doc(widget.ownerId).get();
    if (!mounted) return;
    final v = belge.data() ?? {};
    final aktifUid = FirebaseAuth.instance.currentUser?.uid;
    final kendiBelgesi = aktifUid == null ? null : await FirebaseFirestore.instance.collection('users').doc(aktifUid).get();
    bool takipte = List<dynamic>.from(kendiBelgesi?.data()?['following'] ?? []).contains(widget.ownerId);
    if (!mounted) return;
    showModalBottomSheet(
      context: context,
      backgroundColor: panel,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
      builder: (ctx) => StatefulBuilder(builder: (ctx, pencereState) => Padding(
        padding: const EdgeInsets.all(28),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 92, height: 92, padding: const EdgeInsets.all(4), decoration: const BoxDecoration(shape: BoxShape.circle, gradient: LinearGradient(colors: [mavi, mor])), child: CircleAvatar(backgroundImage: (v['photoUrl'] ?? '').toString().isEmpty ? null : NetworkImage(v['photoUrl']), child: (v['photoUrl'] ?? '').toString().isEmpty ? const Text('N', style: TextStyle(fontSize: 35, fontWeight: FontWeight.bold)) : null)),
          const SizedBox(height: 14),
          Text((v['displayName'] ?? widget.kullaniciAdi).toString(), style: const TextStyle(fontSize: 23, fontWeight: FontWeight.bold)),
          Text('@${v['username'] ?? widget.kullaniciAdi}', style: const TextStyle(color: Colors.white54)),
          const SizedBox(height: 12),
          Text((v['bio'] ?? 'NgelX kullanıcısı').toString(), textAlign: TextAlign.center),
          if (aktifUid != null && aktifUid != widget.ownerId) ...[
            const SizedBox(height: 18),
            RenkliButon(yazi: takipte ? 'Takibi Bırak' : 'Takip Et', tiklama: () async {
              await takipDurumuDegistir(widget.ownerId,takipte);
              pencereState(() => takipte = !takipte);
            }),
          ],
        ]),
      )),
    );
  }

  Future<void> uzunBasmaMenusu() async {
    final sahibi = FirebaseAuth.instance.currentUser?.uid == widget.ownerId;
    await showModalBottomSheet(
      context: context,
      backgroundColor: panel,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
      builder: (ctx) => SafeArea(child: Padding(
        padding: const EdgeInsets.fromLTRB(14, 12, 14, 22),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 42, height: 4, margin: const EdgeInsets.only(bottom: 12), decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(9))),
          if (widget.indirilebilir || sahibi) ListTile(leading: const Icon(Icons.download_rounded, color: mavi), title: const Text('İndir'), onTap: () { Navigator.pop(ctx); videoyuGaleriyeKaydet(); }),
          ListTile(leading: const Icon(Icons.heart_broken_outlined), title: const Text('İlgilenmiyorum'), onTap: () { Navigator.pop(ctx); ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Benzer içerikler azaltılacak.'))); }),
          ListTile(leading: const Icon(Icons.flag_outlined, color: Colors.orange), title: const Text('Bildir / Şikâyet et'), onTap: () { Navigator.pop(ctx); sikayetEt(context,hedefTuru:'video',hedefId:videoId,hedefUid:widget.ownerId); }),
          if(!sahibi) ListTile(leading:const Icon(Icons.block,color:Colors.red),title:const Text('Kullanıcıyı engelle',style:TextStyle(color:Colors.red)),onTap:(){Navigator.pop(ctx);kullaniciyiEngelle(context,widget.ownerId);}),
          if (sahibi) ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, videoId, {'ownerId': widget.ownerId, 'videoUrl': widget.adres}); }),
          const Divider(),
          const Align(alignment: Alignment.centerLeft, child: Padding(padding: EdgeInsets.all(10), child: Text('Video hızı', style: TextStyle(fontWeight: FontWeight.bold)))),
          Wrap(spacing: 9, children: [.5, 1.0, 1.5, 2.0].map((hiz) => ActionChip(label: Text('${hiz}x'), onPressed: () { kontrol.setPlaybackSpeed(hiz); Navigator.pop(ctx); })).toList()),
        ]),
      )),
    );
  }

  @override
  void didUpdateWidget(covariant VideoKarti oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (!hazir) return;

    if (widget.aktif) {
      if (!duraklatildi) kontrol.play();
    } else {
      kontrol.pause();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    kontrol.dispose();
    super.dispose();
  }

  void yorumlariAc() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(25),
        ),
      ),
      builder: (_) => Yorumlar(videoId: videoId),
    ).whenComplete(etkilesimleriGetir);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onLongPress: uzunBasmaMenusu,
      onTap: () {
        if (!hazir) return;

        setState(() {
          if (kontrol.value.isPlaying) {
            kontrol.pause();
            duraklatildi = true;
          } else {
            kontrol.play();
            duraklatildi = false;
          }
        });
      },
      onDoubleTap: () {
        if (!begenildi) begeniyiDegistir();
      },
      child: Stack(
        fit: StackFit.expand,
        children: [
          Container(color: Colors.black),
          if (hazir)
            FittedBox(
              fit: BoxFit.cover,
              child: SizedBox(
                width: kontrol.value.size.width,
                height: kontrol.value.size.height,
                child: VideoPlayer(kontrol),
              ),
            )
          else
            const Center(
              child: CircularProgressIndicator(color: mavi),
            ),
          const DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black54,
                  Colors.transparent,
                  Colors.black87,
                ],
              ),
            ),
          ),
          if (hazir && duraklatildi)
            const Center(
              child: Icon(
                Icons.play_arrow_rounded,
                size: 92,
                color: Colors.white70,
              ),
            ),
          Positioned(
            left: 18,
            right: 85,
            bottom: 25,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '@${widget.kullaniciAdi}',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Anı yakala, kendi hikâyeni paylaş ✨',
                ),
                const SizedBox(height: 8),
                const Row(
                  children: [
                    Icon(Icons.graphic_eq, size: 17),
                    SizedBox(width: 6),
                    Text('NgelX • Özgün ses'),
                  ],
                ),
              ],
            ),
          ),
          Positioned(
            right: 14,
            bottom: 20,
            child: Column(
              children: [
                GestureDetector(
                  onTap: paylasanProfiliAc,
                  child: CircleAvatar(
                    radius: 27,
                    backgroundColor: mavi,
                    child: CircleAvatar(
                      radius: 23,
                      backgroundColor: panel,
                      backgroundImage: profilFoto.isEmpty ? null : NetworkImage(profilFoto),
                      child: profilFoto.isNotEmpty ? null : const Text(
                        'N',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
                IslemButonu(
                  ikon: begenildi
                      ? Icons.favorite
                      : Icons.favorite_border,
                  yazi: '$begeniSayisi',
                  renk: begenildi
                      ? Colors.pinkAccent
                      : Colors.white,
                  tiklama: begeniyiDegistir,
                ),
                IslemButonu(
                  ikon: Icons.mode_comment_outlined,
                  yazi: '$yorumSayisi',
                  tiklama: yorumlariAc,
                ),
                IslemButonu(
                  ikon: kaydedildi
                      ? Icons.bookmark
                      : Icons.bookmark_border,
                  yazi: kaydedildi ? 'Kaydedildi' : 'Kaydet',
                  renk: kaydedildi ? mavi : Colors.white,
                  tiklama: videoyuKaydet,
                ),
                IslemButonu(ikon:Icons.menu_rounded,yazi:'Araçlar',tiklama:()=>icerikAracMenusu(context,videoId,hizDegistir:(x)async=>kontrol.setPlaybackSpeed(x))),
                IslemButonu(
                  ikon: Icons.send_outlined,
                  yazi: 'Paylaş',
                  tiklama: videoyuPaylas,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class IslemButonu extends StatelessWidget {
  final IconData ikon;
  final String yazi;
  final VoidCallback tiklama;
  final Color renk;

  const IslemButonu({
    super.key,
    required this.ikon,
    required this.yazi,
    required this.tiklama,
    this.renk = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: tiklama,
      child: Padding(
        padding: const EdgeInsets.only(top: 16),
        child: Column(
          children: [
            Icon(ikon, size: 33, color: renk),
            const SizedBox(height: 3),
            Text(
              yazi,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class Yorumlar extends StatefulWidget {
  final String videoId;
  const Yorumlar({super.key, required this.videoId});

  @override
  State<Yorumlar> createState() => _YeniYorumlarState();
}

class _YeniYorumlarState extends State<Yorumlar> {
  final yorum = TextEditingController();
  bool gonderiliyor = false;
  String? yanitlananId;
  String? yanitlananKullanici;
  final Set<String> acikYanitlar = {};

  CollectionReference<Map<String, dynamic>> get ref => FirebaseFirestore.instance.collection('videos').doc(widget.videoId).collection('comments');

  String zamanYaz(dynamic ham) {
    if (ham is! Timestamp) return 'Şimdi';
    final fark = DateTime.now().difference(ham.toDate());
    if (fark.inSeconds < 45) return 'Şimdi';
    if (fark.inMinutes < 60) return '${fark.inMinutes} dk önce';
    if (fark.inHours < 24) return '${fark.inHours} sa önce';
    if (fark.inDays == 1) return 'Dün';
    if (fark.inDays < 30) return '${fark.inDays} gün önce';
    return '${ham.toDate().day}.${ham.toDate().month}.${ham.toDate().year}';
  }

  Future<void> gonder() async {
    if (await misafirEngeli(context)) return;
    final metin = yorum.text.trim();
    final user = FirebaseAuth.instance.currentUser;
    if (metin.isEmpty || user == null || gonderiliyor) return;
    setState(() => gonderiliyor = true);
    try {
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final p = profil.data() ?? {};
      await ref.add({
        'userId': user.uid,
        'username': (p['username'] ?? user.displayName ?? 'ngelx').toString(),
        'photoUrl': (p['photoUrl'] ?? '').toString(),
        'text': metin,
        'parentId': yanitlananId ?? '',
        'replyToUsername': yanitlananKullanici ?? '',
        'likedBy': <String>[],
        'createdAt': FieldValue.serverTimestamp(),
      });
      yorum.clear();
      setState(() { yanitlananId = null; yanitlananKullanici = null; });
    } finally {
      if (mounted) setState(() => gonderiliyor = false);
    }
  }

  Future<void> yorumBegen(String id, List<dynamic> begenenler) async {
    if (await misafirEngeli(context)) return;
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;
    await ref.doc(id).update({'likedBy': begenenler.contains(uid) ? FieldValue.arrayRemove([uid]) : FieldValue.arrayUnion([uid])});
  }

  @override
  void dispose() { yorum.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData.light().copyWith(
        scaffoldBackgroundColor: Colors.white,
        dividerColor: const Color(0xFFE5E7EB),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFFF4F5F7),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
        ),
      ),
      child: SafeArea(
      child: SizedBox(
        height: MediaQuery.of(context).size.height * .72,
        child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
          stream: ref.snapshots(),
          builder: (_, snap) {
            final List<QueryDocumentSnapshot<Map<String, dynamic>>> tumu =
                snap.data?.docs.toList() ??
                <QueryDocumentSnapshot<Map<String, dynamic>>>[];
            tumu.sort((a, b) {
              final at = a.data()['createdAt']; final bt = b.data()['createdAt'];
              if (at is! Timestamp) return -1; if (bt is! Timestamp) return 1;
              return at.compareTo(bt);
            });
            final ana = tumu.where((d) => (d.data()['parentId'] ?? '').toString().isEmpty).toList();
            return Column(children: [
              Container(width: 42, height: 4, margin: const EdgeInsets.only(top: 9), decoration: BoxDecoration(color: Colors.black26, borderRadius: BorderRadius.circular(9))),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 12),
                child: Row(children: [const Spacer(), Text('${tumu.length} yorum', style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900)), const Spacer(), IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close))]),
              ),
              const Divider(height: 1),
              Expanded(
                child: snap.connectionState == ConnectionState.waiting
                    ? const Center(child: CircularProgressIndicator(color: mavi))
                    : ana.isEmpty
                        ? const Center(child: Text('İlk yorumu sen yaz ✨'))
                        : ListView.builder(
                            padding: const EdgeInsets.fromLTRB(14, 8, 14, 18),
                            itemCount: ana.length,
                            itemBuilder: (_, i) {
                              final d = ana[i]; final v = d.data();
                              final yanitlar = tumu.where((x) => (x.data()['parentId'] ?? '') == d.id).toList();
                              return YorumKarti(
                                id: d.id,
                                veri: v,
                                zaman: zamanYaz(v['createdAt']),
                                yanitlar: yanitlar,
                                acik: acikYanitlar.contains(d.id),
                                zamanYaz: zamanYaz,
                                begen: yorumBegen,
                                yanitla: () => setState(() { yanitlananId = d.id; yanitlananKullanici = (v['username'] ?? 'ngelx').toString(); }),
                                yanitlariAc: () => setState(() { acikYanitlar.contains(d.id) ? acikYanitlar.remove(d.id) : acikYanitlar.add(d.id); }),
                              );
                            },
                          ),
              ),
              if (yanitlananId != null)
                Container(color: mor.withValues(alpha: .15), padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 7), child: Row(children: [Expanded(child: Text('@$yanitlananKullanici kullanıcısına yanıt veriyorsun', style: const TextStyle(color: mavi))), IconButton(onPressed: () => setState(() { yanitlananId = null; yanitlananKullanici = null; }), icon: const Icon(Icons.close, size: 18))])),
              Padding(
                padding: EdgeInsets.fromLTRB(12, 8, 12, MediaQuery.of(context).viewInsets.bottom + 10),
                child: Row(children: [
                  IconButton(onPressed: () => yorum.text += ' 😊', icon: const Icon(Icons.emoji_emotions_outlined, color: mor)),
                  Expanded(child: TextField(controller: yorum, onSubmitted: (_) => gonder(), decoration: InputDecoration(hintText: yanitlananId == null ? 'Yorum ekle...' : 'Yanıt yaz...', contentPadding: const EdgeInsets.symmetric(horizontal: 17, vertical: 12)))),
                  IconButton(onPressed: gonderiliyor ? null : gonder, icon: gonderiliyor ? const SizedBox(width: 21, height: 21, child: CircularProgressIndicator(strokeWidth: 2, color: mavi)) : const Icon(Icons.send_rounded, color: mavi)),
                ]),
              ),
            ]);
          },
        ),
      ),
    ),
    );
  }
}

class YorumKarti extends StatelessWidget {
  final String id;
  final Map<String, dynamic> veri;
  final String zaman;
  final List<QueryDocumentSnapshot<Map<String, dynamic>>> yanitlar;
  final bool acik;
  final String Function(dynamic) zamanYaz;
  final Future<void> Function(String, List<dynamic>) begen;
  final VoidCallback yanitla;
  final VoidCallback yanitlariAc;
  const YorumKarti({super.key, required this.id, required this.veri, required this.zaman, required this.yanitlar, required this.acik, required this.zamanYaz, required this.begen, required this.yanitla, required this.yanitlariAc});

  Widget satir(String yorumId, Map<String, dynamic> v, String zaman, {bool yanit = false}) {
    final ad = (v['username'] ?? 'ngelx').toString();
    final metin = (v['text'] ?? v['message'] ?? v['content'] ?? '').toString().trim();
    final foto = (v['photoUrl'] ?? '').toString();
    final liked = List<dynamic>.from(v['likedBy'] ?? []);
    final uid = FirebaseAuth.instance.currentUser?.uid;
    final secili = uid != null && liked.contains(uid);
    return Padding(
      padding: EdgeInsets.fromLTRB(yanit ? 52 : 0, 9, 0, 4),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        CircleAvatar(radius: yanit ? 16 : 21, backgroundImage: foto.isEmpty ? null : NetworkImage(foto), child: foto.isEmpty ? Text(ad.isEmpty ? 'N' : ad[0].toUpperCase()) : null),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('@$ad', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black87)),
          if ((v['replyToUsername'] ?? '').toString().isNotEmpty)
            Text.rich(TextSpan(children: [TextSpan(text: '@${v['replyToUsername']}  ', style: const TextStyle(color: mavi, fontWeight: FontWeight.w700)), TextSpan(text: metin.isEmpty ? 'Mesaj içeriği bulunamadı' : metin)]), style: const TextStyle(color: Colors.black87, fontSize: 15, height: 1.3))
          else
            Text(metin.isEmpty ? 'Mesaj içeriği bulunamadı' : metin, maxLines: null, softWrap: true, style: const TextStyle(color: Colors.black87, fontSize: 15, height: 1.3)),
          const SizedBox(height: 5),
          Row(children: [Text(zaman, style: const TextStyle(color: Colors.black45, fontSize: 12)), const SizedBox(width: 18), if (!yanit) GestureDetector(onTap: yanitla, child: const Text('Yanıtla', style: TextStyle(color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12)))]),
        ])),
        GestureDetector(onTap: () => begen(yorumId, liked), child: Column(children: [Icon(secili ? Icons.favorite : Icons.favorite_border, color: secili ? Colors.pinkAccent : Colors.black45, size: 22), if (liked.isNotEmpty) Text('${liked.length}', style: const TextStyle(fontSize: 11, color: Colors.black45))])),
      ]),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      satir(id, veri, zaman),
      if (yanitlar.isNotEmpty) GestureDetector(onTap: yanitlariAc, child: Padding(padding: const EdgeInsets.only(left: 54, top: 5, bottom: 3), child: Text(acik ? 'Yanıtları gizle' : '${yanitlar.length} yanıtı görüntüle', style: const TextStyle(color: mavi, fontWeight: FontWeight.bold, fontSize: 12)))),
      if (acik) ...yanitlar.map((d) => satir(d.id, d.data(), zamanYaz(d.data()['createdAt']), yanit: true)),
    ]);
  }
}

class EskiYorumlar extends StatefulWidget {
  final String videoId;

  const EskiYorumlar({super.key, required this.videoId});

  @override
  State<EskiYorumlar> createState() => _YorumlarState();
}

class _YorumlarState extends State<EskiYorumlar> {
  final yorum = TextEditingController();
  bool gonderiliyor = false;

  CollectionReference<Map<String, dynamic>> get yorumlar =>
      FirebaseFirestore.instance
          .collection('videos')
          .doc(widget.videoId)
          .collection('comments');

  Future<void> yorumGonder() async {
    final metin = yorum.text.trim();
    final kullanici = FirebaseAuth.instance.currentUser;
    if (metin.isEmpty || kullanici == null || gonderiliyor) return;
    setState(() => gonderiliyor = true);
    try {
      final profil = await FirebaseFirestore.instance
          .collection('users')
          .doc(kullanici.uid)
          .get();
      final veri = profil.data() ?? {};
      final kullaniciAdi = (veri['username'] ?? kullanici.displayName ?? 'ngelx').toString();
      await yorumlar.add({
        'userId': kullanici.uid,
        'username': kullaniciAdi,
        'text': metin,
        'createdAt': FieldValue.serverTimestamp(),
      });
      yorum.clear();
    } finally {
      if (mounted) setState(() => gonderiliyor = false);
    }
  }

  @override
  void dispose() {
    yorum.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SizedBox(
        height: 430,
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                'Yorumlar',
                style: TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Expanded(
              child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                stream: yorumlar.orderBy('createdAt', descending: true).snapshots(),
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  final belgeler = snapshot.data?.docs ?? [];
                  if (belgeler.isEmpty) {
                    return const Center(child: Text('İlk yorumu sen yaz.'));
                  }
                  return ListView.builder(
                    itemCount: belgeler.length,
                    itemBuilder: (_, i) {
                      final veri = belgeler[i].data();
                      final ad = (veri['username'] ?? 'ngelx').toString();
                      final metin = (veri['text'] ?? '').toString();
                      return ListTile(
                        leading: CircleAvatar(
                          child: Text(ad.isEmpty ? 'N' : ad[0].toUpperCase()),
                        ),
                        title: Text('@$ad'),
                        subtitle: Text(metin),
                      );
                    },
                  );
                },
              ),
            ),
            Padding(
              padding: EdgeInsets.all(12),
              child: TextField(
                controller: yorum,
                onSubmitted: (_) => yorumGonder(),
                decoration: InputDecoration(
                  hintText: 'Yorum yaz...',
                  suffixIcon: IconButton(
                    onPressed: gonderiliyor ? null : yorumGonder,
                    icon: gonderiliyor
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.send),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

const liveKitTestSunucuId = 'ngelx-g49q1h';

class KesfetPage extends StatelessWidget {
  final bool gorunur;
  const KesfetPage({super.key, required this.gorunur});

  Future<void> _yayinIzle(BuildContext context, Map<String, dynamic> veri, String belgeId) async {
    if (await misafirEngeli(context)) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    try {
      final kaynak = lk.DevelopmentTokenSource(id: liveKitTestSunucuId);
      final kimlik = '${user.uid}-${DateTime.now().millisecondsSinceEpoch}';
      final cevap = await kaynak.fetch(lk.TokenRequestOptions(
        roomName: (veri['roomName'] ?? '').toString(),
        participantIdentity: kimlik,
        participantName: (user.displayName?.isNotEmpty == true ? user.displayName : 'NgelX izleyicisi'),
      ));
      final oda = lk.Room(roomOptions: lk.RoomOptions(adaptiveStream: true, dynacast: true));
      await oda.connect(cevap.serverUrl, cevap.participantToken);
      if (!context.mounted) {
        await oda.disconnect();
        await oda.dispose();
        return;
      }
      Navigator.push(context, MaterialPageRoute(builder: (_) => CanliYayinPage(
        oda: oda,
        belgeId: belgeId,
        baslik: (veri['title'] ?? 'NgelX canlı yayını').toString(),
        yayinSahibi: false,
      )));
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Canlı yayına bağlanılamadı: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: CustomScrollView(slivers: [
          const SliverToBoxAdapter(child: Padding(
            padding: EdgeInsets.fromLTRB(18, 14, 18, 8),
            child: Row(children: [Text('Keşfet', style: TextStyle(color: Colors.black, fontSize: 30, fontWeight: FontWeight.w900)), Spacer(), Icon(Icons.search_rounded, color: Colors.black, size: 29), SizedBox(width: 16), Icon(Icons.tune_rounded, color: Colors.black, size: 27)]),
          )),
          SliverToBoxAdapter(child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 12),
            child: TextField(style: const TextStyle(color: Colors.black87), decoration: InputDecoration(hintText: 'Kişi, grup veya içerik ara', hintStyle: const TextStyle(color: Colors.black45), prefixIcon: const Icon(Icons.search, color: Colors.black45), filled: true, fillColor: const Color(0xFFF4F5F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(22), borderSide: BorderSide.none))),
          )),
          SliverToBoxAdapter(child: SizedBox(height: 52, child: ListView(padding: const EdgeInsets.symmetric(horizontal: 16), scrollDirection: Axis.horizontal, children: [
            _kesfetSekmesi(Icons.live_tv_rounded, 'Canlı', true),
            _kesfetSekmesi(Icons.local_fire_department_rounded, 'Trend', false),
            _kesfetSekmesi(Icons.person_rounded, 'Kişiler', false),
            _kesfetSekmesi(Icons.groups_rounded, 'Gruplar', false),
          ]))),
          const SliverToBoxAdapter(child: Padding(
            padding: EdgeInsets.fromLTRB(16, 14, 16, 10),
            child: Row(children: [Text('Canlı yayınlar', style: TextStyle(color: Colors.black, fontSize: 21, fontWeight: FontWeight.w900)), Spacer(), Text('Tümünü gör ›', style: TextStyle(color: Colors.black45, fontWeight: FontWeight.w700))]),
          )),
          SliverToBoxAdapter(child: SizedBox(
            height: 205,
            child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: FirebaseFirestore.instance.collection('live_streams').where('active', isEqualTo: true).snapshots(),
              builder: (_, snap) {
                final yayinlar = snap.data?.docs ?? [];
                if (yayinlar.isEmpty) {
                  return Container(
                    margin: const EdgeInsets.symmetric(horizontal: 16),
                    decoration: BoxDecoration(color: const Color(0xFFFFF0F2), borderRadius: BorderRadius.circular(20), border: Border.all(color: const Color(0xFFFF1744).withOpacity(.25))),
                    child: const Center(child: Text('Şu anda canlı yayın yok. İlk yayını sen başlat ✨', style: TextStyle(color: Colors.black54))),
                  );
                }
                return ListView.separated(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  scrollDirection: Axis.horizontal,
                  itemCount: yayinlar.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 10),
                  itemBuilder: (_, i) {
                    final y = yayinlar[i].data();
                    return GestureDetector(
                      onTap: () => _yayinIzle(context, y, yayinlar[i].id),
                      child: Container(
                        width: 245,
                        decoration: BoxDecoration(
                          color: const Color(0xFF2A2630),
                          image: (y['coverUrl'] ?? '').toString().isEmpty ? null : DecorationImage(image: NetworkImage((y['coverUrl']).toString()), fit: BoxFit.cover),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: const Color(0xFFFF1744), width: 2),
                          boxShadow: const [BoxShadow(color: Color(0x22000000), blurRadius: 12, offset: Offset(0, 5))],
                        ),
                        child: Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(borderRadius: BorderRadius.circular(18), gradient: const LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.transparent, Color(0xDD000000)])),
                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Row(children: [
                            Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6), decoration: BoxDecoration(color: const Color(0xFFFF1744), borderRadius: BorderRadius.circular(9)), child: const Text('● CANLI', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900))),
                            Spacer(),
                            Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5), decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(9)), child: Row(children: [const Icon(Icons.visibility, size: 16, color: Colors.white), const SizedBox(width: 4), Text('${y['viewerCount'] ?? 0}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))])),
                          ]),
                          const Spacer(),
                          Text((y['title'] ?? 'Canlı yayın').toString(), maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 18)),
                          const SizedBox(height: 5),
                          Text('@${(y['username'] ?? 'ngelx')}', style: const TextStyle(color: Colors.white70)),
                        ])),
                      ),
                    );
                  },
                );
              },
            ),
          )),
          const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.fromLTRB(16, 20, 16, 10), child: Text('Trendler', style: TextStyle(color: Colors.black, fontSize: 21, fontWeight: FontWeight.w900)))),
          SliverToBoxAdapter(child: SizedBox(height: 48, child: ListView(padding: const EdgeInsets.symmetric(horizontal: 16), scrollDirection: Axis.horizontal, children: const [
            _TrendEtiketi(Icons.directions_run_rounded, '#spor', Color(0xFFFFEEF1), Colors.red),
            _TrendEtiketi(Icons.music_note_rounded, '#müzik', Color(0xFFF1EAFE), mor),
            _TrendEtiketi(Icons.computer_rounded, '#teknoloji', Color(0xFFE7FAFA), Color(0xFF00AFC1)),
            _TrendEtiketi(Icons.flight_takeoff_rounded, '#seyahat', Color(0xFFEAF2FF), Colors.blue),
          ]))),
          const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.fromLTRB(16, 20, 16, 8), child: Row(children: [Text('Trend içerikler', style: TextStyle(color: Colors.black, fontSize: 21, fontWeight: FontWeight.w900)), Spacer(), Text('Tümünü gör ›', style: TextStyle(color: Colors.black45))]))),
          SliverPadding(padding: const EdgeInsets.all(6), sliver: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: FirebaseFirestore.instance.collection('videos').orderBy('createdAt', descending: true).limit(60).snapshots(),
              builder: (_, snap) {
                final belgeler = (snap.data?.docs ?? []).where((d) {
                  final v = d.data();
                  if (v['type'] == 'story') return false;
                  final begeni = (v['likeCount'] as num?)?.toInt() ?? 0;
                  final izlenme = (v['viewCount'] as num?)?.toInt() ?? 0;
                  return v['isTrending'] == true || begeni >= 50 || izlenme >= 500;
                }).toList();
                if (belgeler.isEmpty) return const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.all(28), child: Center(child: Text('Trend içerikler burada görünecek ✨', style: TextStyle(color: Colors.black54)))));
                return SliverGrid(
                  delegate: SliverChildBuilderDelegate((_, i) {
                    final v = belgeler[i].data();
                    final tur = (v['type'] ?? 'video').toString();
                    final url = (v['mediaUrl'] ?? v['videoUrl'] ?? '').toString();
                    return GestureDetector(
                      onTap: () {
                        final item = <String, String>{
                          'id': belgeler[i].id, 'type': tur, 'videoUrl': (v['videoUrl'] ?? '').toString(),
                          'mediaUrl': url, 'audioUrl': (v['audioUrl'] ?? '').toString(),
                          'description': (v['description'] ?? '').toString(), 'username': (v['username'] ?? 'ngelx').toString(),
                          'ownerId': (v['ownerId'] ?? '').toString(), 'allowDownload': (v['allowDownload'] ?? true).toString(),
                        };
                        Navigator.push(context, MaterialPageRoute(builder: (_) => Scaffold(body: SafeArea(child: tur == 'video' ? VideoKarti(adres: item['videoUrl']!, videoId: item['id']!, kullaniciAdi: item['username']!, ownerId: item['ownerId']!, indirilebilir: item['allowDownload'] != 'false', aktif: true) : GorselYaziKarti(veri: item, aktif: true)))));
                      },
                      onLongPress: () => kendiPaylasimMenusu(context, belgeler[i].id, v),
                      child: MedyaOnizleme(tur: tur, url: url, yazi: (v['description'] ?? '').toString(), arkaPlan: i.isEven ? const Color(0xFF292348) : const Color(0xFF16343B)),
                    );
                  }, childCount: belgeler.length),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6),
                );
              },
            )),
          const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.fromLTRB(16, 20, 16, 8), child: Row(children: [Text('Kişileri keşfet', style: TextStyle(color: Colors.black, fontSize: 21, fontWeight: FontWeight.w900)), Spacer(), Text('Tümünü gör ›', style: TextStyle(color: Colors.black45))]))),
          SliverToBoxAdapter(child: SizedBox(height: 145, child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
            stream: FirebaseFirestore.instance.collection('users').limit(12).snapshots(),
            builder: (_, snap) => ListView.separated(
              padding: const EdgeInsets.symmetric(horizontal: 16), scrollDirection: Axis.horizontal,
              itemCount: snap.data?.docs.length ?? 0, separatorBuilder: (_, __) => const SizedBox(width: 14),
              itemBuilder: (_, i) { final d = snap.data!.docs[i]; return _kisiKarti(context, d.id, d.data()); },
            ),
          ))),
          const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.fromLTRB(16, 16, 16, 8), child: Row(children: [Text('Grupları keşfet', style: TextStyle(color: Colors.black, fontSize: 21, fontWeight: FontWeight.w900)), Spacer(), Text('Tümünü gör ›', style: TextStyle(color: Colors.black45))]))),
          SliverToBoxAdapter(child: SizedBox(height: 130, child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
            stream: FirebaseFirestore.instance.collection('groups').limit(12).snapshots(),
            builder: (_, snap) { final gruplar = (snap.data?.docs ?? []).where((d) { final ad = (d.data()['name'] ?? '').toString().toLowerCase(); return !ad.contains('oyun') && !ad.contains('game'); }).toList(); return ListView.separated(
              padding: const EdgeInsets.symmetric(horizontal: 16), scrollDirection: Axis.horizontal,
              itemCount: gruplar.length, separatorBuilder: (_, __) => const SizedBox(width: 12),
              itemBuilder: (_, i) => _grupKarti(context, gruplar[i].id, gruplar[i].data()),
            ); },
          ))),
          const SliverToBoxAdapter(child: SizedBox(height: 90)),
        ]),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: FilledButton.icon(
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0xFFFF1744),
          minimumSize: const Size(230, 54),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
          elevation: 12,
        ),
        onPressed: () async {
          if (await misafirEngeli(context)) return;
          if (context.mounted) Navigator.push(context, MaterialPageRoute(builder: (_) => const CanliHazirlikPage()));
        },
        icon: const Icon(Icons.videocam_rounded),
        label: const Text('Canlı yayın başlat', style: TextStyle(fontWeight: FontWeight.w800)),
      ),
    );
  }

  Widget _kesfetSekmesi(IconData ikon, String yazi, bool secili) => Container(
    margin: const EdgeInsets.only(right: 10),
    padding: const EdgeInsets.symmetric(horizontal: 20),
    decoration: BoxDecoration(gradient: secili ? const LinearGradient(colors: [Color(0xFF7C3AED), Color(0xFFA855F7)]) : null, color: secili ? null : const Color(0xFFF2F3F6), borderRadius: BorderRadius.circular(22)),
    child: Row(children: [Icon(ikon, size: 18, color: secili ? Colors.white : Colors.black54), const SizedBox(width: 7), Text(yazi, style: TextStyle(color: secili ? Colors.white : Colors.black87, fontWeight: FontWeight.w700))]),
  );

  Widget _kisiKarti(BuildContext context, String uid, Map<String, dynamic> v) {
    final foto = (v['photoUrl'] ?? '').toString();
    final ad = (v['displayName'] ?? v['username'] ?? 'Kullanıcı').toString();
    return SizedBox(width: 105, child: Column(children: [
      Stack(children: [CircleAvatar(radius: 38, backgroundColor: const Color(0xFFF0E8FF), backgroundImage: foto.isEmpty ? null : NetworkImage(foto), child: foto.isEmpty ? Text(ad.substring(0, 1).toUpperCase(), style: const TextStyle(color: mor, fontSize: 24, fontWeight: FontWeight.bold)) : null), const Positioned(right: 2, bottom: 2, child: CircleAvatar(radius: 7, backgroundColor: Color(0xFF23D160)))]),
      const SizedBox(height: 5), Text(ad, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.black, fontWeight: FontWeight.w800)),
      const SizedBox(height: 4), SizedBox(height: 30, child: FilledButton(style: FilledButton.styleFrom(backgroundColor: mor, padding: const EdgeInsets.symmetric(horizontal: 12)), onPressed: () async {await takipDurumuDegistir(uid,false);if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takip edildi ✅')));}, child: const Text('Takip et', style: TextStyle(fontSize: 11)))),
    ]));
  }

  Widget _grupKarti(BuildContext context, String id, Map<String, dynamic> v) {
    final ad = (v['name'] ?? 'Topluluk').toString();
    final sayi = (v['memberCount'] ?? 0).toString();
    return Container(width: 245, padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: const Color(0xFFF6F3FF), borderRadius: BorderRadius.circular(18)), child: Row(children: [
      Container(width: 65, height: 65, decoration: BoxDecoration(color: const Color(0xFFE9DDFF), borderRadius: BorderRadius.circular(14)), child: const Icon(Icons.groups_rounded, color: mor, size: 34)),
      const SizedBox(width: 10), Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [Text(ad, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.black, fontWeight: FontWeight.w900)), Text('$sayi üye', style: const TextStyle(color: Colors.black45, fontSize: 12)), const SizedBox(height: 6), SizedBox(height: 30, child: FilledButton(style: FilledButton.styleFrom(backgroundColor: mor), onPressed: () async { final uid = FirebaseAuth.instance.currentUser?.uid; if (uid != null) await FirebaseFirestore.instance.collection('groups').doc(id).set({'members': FieldValue.arrayUnion([uid]), 'memberCount': FieldValue.increment(1)}, SetOptions(merge: true)); }, child: const Text('Katıl', style: TextStyle(fontSize: 12))))]))
    ]));
  }
}

class _TrendEtiketi extends StatelessWidget {
  final IconData ikon; final String yazi; final Color arkaPlan; final Color renk;
  const _TrendEtiketi(this.ikon, this.yazi, this.arkaPlan, this.renk);
  @override Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(right: 10), padding: const EdgeInsets.symmetric(horizontal: 16),
    decoration: BoxDecoration(color: arkaPlan, borderRadius: BorderRadius.circular(18)),
    child: Row(children: [Icon(ikon, color: renk, size: 20), const SizedBox(width: 7), Text(yazi, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700))]),
  );
}

class CanliHazirlikPage extends StatefulWidget {
  const CanliHazirlikPage({super.key});
  @override
  State<CanliHazirlikPage> createState() => _CanliHazirlikPageState();
}

class _CanliHazirlikPageState extends State<CanliHazirlikPage> {
  final baslik = TextEditingController();
  bool baglaniyor = false;
  bool mikrofon = true;
  bool kamera = true;

  @override
  void dispose() {
    baslik.dispose();
    super.dispose();
  }

  Future<void> baslat() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.isAnonymous || baglaniyor) return;
    if (baslik.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('En az 3 karakterlik yayın başlığı yaz.')));
      return;
    }
    setState(() => baglaniyor = true);
    lk.Room? oda;
    try {
      final odaAdi = 'ngelx_${user.uid}_${DateTime.now().millisecondsSinceEpoch}';
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();
      final kaynak = lk.DevelopmentTokenSource(id: liveKitTestSunucuId);
      final cevap = await kaynak.fetch(lk.TokenRequestOptions(
        roomName: odaAdi,
        participantIdentity: user.uid,
        participantName: ad,
        participantAttributes: const {'role': 'host'},
      ));
      oda = lk.Room(roomOptions: lk.RoomOptions(adaptiveStream: true, dynacast: true));
      await oda.connect(cevap.serverUrl, cevap.participantToken);
      final yerelKatilimci = oda.localParticipant;
      if (yerelKatilimci == null) throw Exception('Canlı yayın katılımcısı hazırlanamadı.');
      if (kamera) await yerelKatilimci.setCameraEnabled(true);
      if (mikrofon) await yerelKatilimci.setMicrophoneEnabled(true);
      final belge = await FirebaseFirestore.instance.collection('live_streams').add({
        'roomName': odaAdi,
        'ownerId': user.uid,
        'username': ad,
        'title': baslik.text.trim(),
        'active': true,
        'startedAt': FieldValue.serverTimestamp(),
      });
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => CanliYayinPage(
        oda: oda!,
        belgeId: belge.id,
        baslik: baslik.text.trim(),
        yayinSahibi: true,
      )));
    } catch (e) {
      if (oda != null) {
        await oda.disconnect();
        await oda.dispose();
      }
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Yayın başlatılamadı: $e')));
    } finally {
      if (mounted) setState(() => baglaniyor = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Canlı yayın hazırla')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(22),
          children: [
            Container(
              height: 290,
              decoration: BoxDecoration(
                gradient: const LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Color(0xFF102C43), Color(0xFF301331)]),
                borderRadius: BorderRadius.circular(28),
              ),
              child: const Center(child: Icon(Icons.videocam_rounded, size: 82, color: Colors.white38)),
            ),
            const SizedBox(height: 20),
            TextField(controller: baslik, maxLength: 100, decoration: const InputDecoration(prefixIcon: Icon(Icons.edit_rounded), hintText: 'Yayın başlığı yaz')),
            SwitchListTile(value: kamera, onChanged: (v) => setState(() => kamera = v), secondary: const Icon(Icons.videocam_rounded), title: const Text('Kamera')),
            SwitchListTile(value: mikrofon, onChanged: (v) => setState(() => mikrofon = v), secondary: const Icon(Icons.mic_rounded), title: const Text('Mikrofon')),
            const ListTile(leading: Icon(Icons.public_rounded), title: Text('Herkese açık'), subtitle: Text('Keşfet bölümünde görünecek')),
            const SizedBox(height: 16),
            FilledButton.icon(
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744), minimumSize: const Size.fromHeight(58), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22))),
              onPressed: baglaniyor ? null : baslat,
              icon: baglaniyor ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.sensors_rounded),
              label: Text(baglaniyor ? 'Bağlanıyor...' : 'Canlı yayına başla', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
            ),
            const SizedBox(height: 10),
            const Text('İlk kullanımda kamera ve mikrofon izni istenir.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white54)),
          ],
        ),
      ),
    );
  }
}

class CanliYayinPage extends StatefulWidget {
  final lk.Room oda;
  final String belgeId;
  final String baslik;
  final bool yayinSahibi;
  const CanliYayinPage({super.key, required this.oda, required this.belgeId, required this.baslik, required this.yayinSahibi});
  @override
  State<CanliYayinPage> createState() => _CanliYayinPageState();
}

class _CanliYayinPageState extends State<CanliYayinPage> {
  final yorum = TextEditingController();
  Timer? sayac;
  int saniye = 0;
  bool mikrofonAcik = true;
  bool kameraAcik = true;
  bool kapatildi = false;

  @override
  void initState() {
    super.initState();
    widget.oda.addListener(_yenile);
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => saniye++);
    });
  }

  void _yenile() {
    if (mounted) setState(() {});
  }

  lk.VideoTrack? _goruntu() {
    if (widget.yayinSahibi) {
      for (final p in widget.oda.localParticipant?.videoTrackPublications ?? <lk.LocalTrackPublication>[]) {
        if (!p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
      }
    } else {
      for (final katilimci in widget.oda.remoteParticipants.values) {
        for (final p in katilimci.videoTrackPublications) {
          if (p.subscribed && !p.muted && p.track is lk.VideoTrack) return p.track as lk.VideoTrack;
        }
      }
    }
    return null;
  }

  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;
    if (widget.yayinSahibi) {
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'active': false, 'endedAt': FieldValue.serverTimestamp()}, SetOptions(merge: true));
    }
    await widget.oda.disconnect();
    await widget.oda.dispose();
    if (geriDon && mounted) Navigator.pop(context);
  }

  Future<bool> _geri() async {
    if (widget.yayinSahibi) {
      final onay = await showDialog<bool>(context: context, builder: (_) => AlertDialog(
        title: const Text('Yayın bitsin mi?'),
        content: const Text('Canlı yayın tüm izleyiciler için kapanacak.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Devam et')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Yayını bitir')),
        ],
      )) ?? false;
      if (!onay) return false;
    }
    await _bitir(geriDon: false);
    return true;
  }

  Future<void> _yorumGonder() async {
    final metin = yorum.text.trim();
    final user = FirebaseAuth.instance.currentUser;
    if (metin.isEmpty || user == null) return;
    yorum.clear();
    final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').add({
      'uid': user.uid,
      'username': (profil.data()?['username'] ?? 'ngelx').toString(),
      'text': metin,
      'createdAt': FieldValue.serverTimestamp(),
    });
  }

  @override
  void dispose() {
    sayac?.cancel();
    yorum.dispose();
    widget.oda.removeListener(_yenile);
    if (!kapatildi) _bitir(geriDon: false);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final track = _goruntu();
    final dakika = (saniye ~/ 60).toString().padLeft(2, '0');
    final sn = (saniye % 60).toString().padLeft(2, '0');
    return WillPopScope(
      onWillPop: _geri,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(children: [
          Positioned.fill(child: track == null ? const Center(child: CircularProgressIndicator()) : lk.VideoTrackRenderer(track, fit: lk.VideoViewFit.cover)),
          Positioned.fill(child: DecoratedBox(decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.black54, Colors.transparent, Colors.black.withOpacity(.8)])))),
          SafeArea(child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(children: [
              Row(children: [
                Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8), decoration: BoxDecoration(color: const Color(0xFFFF1744), borderRadius: BorderRadius.circular(14)), child: const Text('● CANLI', style: TextStyle(fontWeight: FontWeight.w900))),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('$dakika:$sn')),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('👁 ${widget.oda.remoteParticipants.length}')),
                const Spacer(),
                IconButton(onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.close_rounded, size: 31)),
              ]),
              const Spacer(),
              Align(alignment: Alignment.centerLeft, child: Container(
                constraints: const BoxConstraints(maxWidth: 330, maxHeight: 210),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(color: Colors.black38, borderRadius: BorderRadius.circular(18)),
                child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                  stream: FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').orderBy('createdAt', descending: true).limit(20).snapshots(),
                  builder: (_, snap) {
                    final yorumlar = snap.data?.docs ?? [];
                    if (yorumlar.isEmpty) return Text(widget.baslik, style: const TextStyle(fontWeight: FontWeight.w800));
                    return ListView.builder(reverse: true, shrinkWrap: true, itemCount: yorumlar.length, itemBuilder: (_, i) {
                      final y = yorumlar[i].data();
                      return Padding(padding: const EdgeInsets.symmetric(vertical: 3), child: Text('@${y['username'] ?? 'ngelx'}  ${y['text'] ?? ''}'));
                    });
                  },
                ),
              )),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(child: TextField(controller: yorum, onSubmitted: (_) => _yorumGonder(), decoration: InputDecoration(hintText: 'Yorum yaz...', filled: true, fillColor: Colors.black54, suffixIcon: IconButton(onPressed: _yorumGonder, icon: const Icon(Icons.send_rounded))))),
                const SizedBox(width: 8),
                if (widget.yayinSahibi) ...[
                  IconButton.filled(onPressed: () async { mikrofonAcik = !mikrofonAcik; await widget.oda.localParticipant?.setMicrophoneEnabled(mikrofonAcik); if (mounted) setState(() {}); }, icon: Icon(mikrofonAcik ? Icons.mic : Icons.mic_off)),
                  const SizedBox(width: 6),
                  IconButton.filled(onPressed: () async { kameraAcik = !kameraAcik; await widget.oda.localParticipant?.setCameraEnabled(kameraAcik); if (mounted) setState(() {}); }, icon: Icon(kameraAcik ? Icons.videocam : Icons.videocam_off)),
                  const SizedBox(width: 6),
                  FilledButton(style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF1744)), onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, child: const Text('Bitir')),
                ] else
                  IconButton.filled(onPressed: () {}, icon: const Icon(Icons.favorite_rounded, color: Colors.redAccent)),
              ]),
            ]),
          )),
        ]),
      ),
    );
  }
}

class EskiKesfetPage extends StatelessWidget {
  const EskiKesfetPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(18),
            child: Row(
              children: [
                Text(
                  'Keşfet',
                  style: TextStyle(
                    fontSize: 29,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                Spacer(),
                Icon(Icons.search),
              ],
            ),
          ),
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(5),
              itemCount: 18,
              gridDelegate:
                  const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                childAspectRatio: 0.7,
                crossAxisSpacing: 5,
                mainAxisSpacing: 5,
              ),
              itemBuilder: (_, i) {
                return Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    color: i.isEven
                        ? const Color(0xFF292348)
                        : const Color(0xFF16343B),
                  ),
                  child: const Icon(
                    Icons.play_arrow,
                    color: Colors.white38,
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class YuklePage extends StatefulWidget {
  const YuklePage({super.key});

  @override
  State<YuklePage> createState() => _YeniYuklePageState();
}

class _YeniYuklePageState extends State<YuklePage> {
  String tur = 'video';
  bool yukleniyor = false;
  bool indirmeyeIzin = true;
  bool yorumlaraIzin = true;
  bool yenidenPaylasimaIzin = true;
  bool otomatikAltyazi = false;
  bool ortakGonderi = false;
  String gizlilik = 'Herkes';
  String kalite = 'HD';
  XFile? medya;
  XFile? muzik;
  final aciklama = TextEditingController();
  final konum = TextEditingController();
  final etiketler = TextEditingController();

  @override
  void initState() {
    super.initState();
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid != null) {
      FirebaseFirestore.instance.collection('users').doc(uid).get().then((d) {
        if (mounted) setState(() => indirmeyeIzin = d.data()?['defaultAllowDownload'] != false);
      });
    }
  }

  Future<void> medyaSec() async {
    XFile? secilen;
    if (tur == 'video') {
      secilen = await ImagePicker().pickVideo(source: ImageSource.gallery);
    } else if (tur == 'photo') {
      secilen = await ImagePicker().pickImage(source: ImageSource.gallery, imageQuality: 85, maxWidth: 1600);
    }
    if (secilen != null && mounted) setState(() => medya = secilen);
  }

  Future<void> kamerayiAc({required bool video}) async {
    final secilen = video
        ? await ImagePicker().pickVideo(source: ImageSource.camera, maxDuration: const Duration(minutes: 10))
        : await ImagePicker().pickImage(source: ImageSource.camera, imageQuality: 90, maxWidth: 2160);
    if (secilen != null && mounted) {
      setState(() {
        tur = video ? 'video' : 'photo';
        medya = secilen;
      });
    }
  }

  Future<void> kameraSecimi() async {
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: panel,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
      builder: (c) => SafeArea(child: Padding(
        padding: const EdgeInsets.all(22),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Kamerayla oluştur', style: TextStyle(fontSize: 21, fontWeight: FontWeight.w900)),
          const SizedBox(height: 18),
          Row(children: [
            Expanded(child: _buyukSecenek(Icons.photo_camera_rounded, 'Fotoğraf çek', () { Navigator.pop(c); kamerayiAc(video: false); })),
            const SizedBox(width: 12),
            Expanded(child: _buyukSecenek(Icons.videocam_rounded, 'Video çek', () { Navigator.pop(c); kamerayiAc(video: true); })),
          ]),
        ]),
      )),
    );
  }

  Future<void> taslakKaydet() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    await FirebaseFirestore.instance.collection('users').doc(user.uid).collection('drafts').add({
      'type': tur,
      'description': aciklama.text.trim(),
      'location': konum.text.trim(),
      'tags': etiketler.text.trim(),
      'privacy': gizlilik,
      'quality': kalite,
      'createdAt': FieldValue.serverTimestamp(),
    });
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Taslak kaydedildi ✓')));
  }

  Future<void> muzikSec() async {
    const sesTurleri = XTypeGroup(
      label: 'Müzik',
      extensions: ['mp3', 'm4a', 'aac', 'wav', 'ogg'],
    );
    final sonuc = await openFile(acceptedTypeGroups: [sesTurleri]);
    if (sonuc != null && mounted) setState(() => muzik = sonuc);
  }

  Future<String> xDosyasiYukle(XFile dosya, String klasor) async {
    final user = FirebaseAuth.instance.currentUser!;
    final boyut = await dosya.length();
    if (boyut > 50 * 1024 * 1024) throw Exception('Dosya 50 MB’den küçük olmalı');
    final uzanti = dosya.name.contains('.') ? dosya.name.split('.').last.toLowerCase() : (tur == 'video' ? 'mp4' : 'jpg');
    final yol = '$klasor/${user.uid}/${DateTime.now().microsecondsSinceEpoch}.$uzanti';
    await supa.Supabase.instance.client.storage.from('ngelx-media').uploadBinary(yol, await dosya.readAsBytes());
    return supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);
  }

  Future<void> yayinla() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || yukleniyor) return;
    if (tur != 'text' && medya == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Önce galeriden bir dosya seç.')));
      return;
    }
    if (tur == 'text' && aciklama.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Paylaşmak istediğin yazıyı gir.')));
      return;
    }
    setState(() => yukleniyor = true);
    try {
      String medyaUrl = '';
      String sesUrl = '';
      if (medya != null) medyaUrl = await xDosyasiYukle(medya!, tur == 'video' ? 'videos' : 'photos');
      if (tur == 'photo' && muzik != null) {
        if (await muzik!.length() > 15 * 1024 * 1024) throw Exception('Müzik 15 MB’den küçük olmalı');
        final uzanti = muzik!.name.contains('.') ? muzik!.name.split('.').last.toLowerCase() : 'mp3';
        final yol = 'music/${user.uid}/${DateTime.now().microsecondsSinceEpoch}.$uzanti';
        await supa.Supabase.instance.client.storage.from('ngelx-media').uploadBinary(yol, await muzik!.readAsBytes());
        sesUrl = supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);
      }
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final adi = (profil.data()?['username'] ?? 'ngelx').toString();
      await FirebaseFirestore.instance.collection('videos').add({
        'ownerId': user.uid,
        'username': adi,
        'type': tur,
        'videoUrl': tur == 'video' ? medyaUrl : '',
        'mediaUrl': medyaUrl,
        'audioUrl': sesUrl,
        'description': aciklama.text.trim().isEmpty ? 'NgelX ile paylaşıldı ✨' : aciklama.text.trim(),
        'allowDownload': indirmeyeIzin,
        'allowComments': yorumlaraIzin,
        'allowReshare': yenidenPaylasimaIzin,
        'autoCaptions': otomatikAltyazi,
        'collab': ortakGonderi,
        'privacy': gizlilik,
        'quality': kalite,
        'location': konum.text.trim(),
        'tags': etiketler.text.trim(),
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (!mounted) return;
      setState(() { medya = null; muzik = null; aciklama.clear(); });
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Paylaşım yayınlandı ✅ Akışta ve profilinde görünecek.')));
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Yüklenemedi: $e')));
    } finally {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(22),
        children: [
          const Text('Yeni içerik üret', textAlign: TextAlign.center, style: TextStyle(fontSize: 27, fontWeight: FontWeight.w900)),
          const SizedBox(height: 8),
          const Text('Fikrini seç, düzenle ve paylaş', textAlign: TextAlign.center, style: TextStyle(color: Colors.white54)),
          const SizedBox(height: 24),
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(color: panel, borderRadius: BorderRadius.circular(22)),
            child: Row(children: [
              _turButonu('video', Icons.videocam_rounded, 'Video'),
              _turButonu('photo', Icons.photo_rounded, 'Fotoğraf'),
              _turButonu('text', Icons.text_fields_rounded, 'Yazı'),
            ]),
          ),
          const SizedBox(height: 14),
          SizedBox(height: 92, child: ListView(scrollDirection: Axis.horizontal, children: [
            _hizliUret(Icons.camera_alt_rounded, 'Kamera', kameraSecimi),
            _hizliUret(Icons.auto_stories_rounded, 'Hikâye', () => setState(() => tur = 'photo')),
            _hizliUret(Icons.movie_creation_rounded, 'Reels', () => setState(() => tur = 'video')),
            _hizliUret(Icons.wifi_tethering_rounded, 'Canlı', () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CanliHazirlikPage()))),
            _hizliUret(Icons.poll_rounded, 'Anket', () => setState(() => tur = 'text')),
          ])),
          const SizedBox(height: 25),
          if (tur != 'text')
            OutlinedButton.icon(
              style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(70), side: const BorderSide(color: mavi), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20))),
              onPressed: medyaSec,
              icon: Icon(tur == 'video' ? Icons.video_library : Icons.photo_library, size: 30),
              label: Text(medya == null ? (tur == 'video' ? 'Galeriden video seç' : 'Galeriden fotoğraf seç') : 'Seçildi: ${medya!.name}', overflow: TextOverflow.ellipsis),
            ),
          if (tur == 'photo') ...[
            const SizedBox(height: 14),
            OutlinedButton.icon(onPressed: muzikSec, icon: const Icon(Icons.music_note), label: Text(muzik == null ? 'Müzik ekle (isteğe bağlı)' : 'Müzik: ${muzik!.name}', overflow: TextOverflow.ellipsis)),
          ],
          const SizedBox(height: 18),
          TextField(
            controller: aciklama,
            maxLines: tur == 'text' ? 8 : 3,
            maxLength: tur == 'text' ? 500 : 180,
            decoration: InputDecoration(labelText: tur == 'text' ? 'Ne düşünüyorsun?' : 'Açıklama yaz', prefixIcon: const Icon(Icons.edit_note_rounded)),
          ),
          Row(children: [
            Expanded(child: TextField(controller: konum, decoration: const InputDecoration(labelText: 'Konum ekle', prefixIcon: Icon(Icons.location_on_outlined)))),
            const SizedBox(width: 10),
            Expanded(child: TextField(controller: etiketler, decoration: const InputDecoration(labelText: 'Kişi / #etiket', prefixIcon: Icon(Icons.alternate_email)))),
          ]),
          const SizedBox(height: 18),
          _bolumBasligi('Düzenle'),
          Wrap(spacing: 8, runSpacing: 8, children: [
            _arac(Icons.crop_rounded, 'Kırp'), _arac(Icons.tune_rounded, 'Filtre'),
            _arac(Icons.auto_fix_high_rounded, 'Efekt'), _arac(Icons.speed_rounded, 'Hız'),
            _arac(Icons.text_fields_rounded, 'Metin'), _arac(Icons.emoji_emotions_outlined, 'GIF / çıkartma'),
            _arac(Icons.grid_view_rounded, 'Kolaj'), _arac(Icons.image_rounded, 'Kapak'),
            _arac(Icons.record_voice_over_rounded, 'Seslendirme'), _arac(Icons.compare_rounded, 'Önce / sonra'),
          ]),
          const SizedBox(height: 20),
          _bolumBasligi('Yayın ayarları'),
          DropdownButtonFormField<String>(
            value: gizlilik,
            decoration: const InputDecoration(labelText: 'Kimler görebilir?', prefixIcon: Icon(Icons.visibility_outlined)),
            items: const ['Herkes', 'Arkadaşlar', 'Yakın arkadaşlar', 'Yalnızca ben'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => gizlilik = v ?? 'Herkes'),
          ),
          const SizedBox(height: 10),
          SegmentedButton<String>(
            segments: const [ButtonSegment(value: 'Veri tasarrufu', label: Text('Veri tasarrufu')), ButtonSegment(value: 'HD', label: Text('HD'))],
            selected: {kalite},
            onSelectionChanged: (v) => setState(() => kalite = v.first),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            activeThumbColor: mavi,
            title: const Text('İçeriğimin indirilmesine izin ver', style: TextStyle(fontWeight: FontWeight.bold)),
            subtitle: const Text('Kapalıysa yalnızca sen indirebilirsin.', style: TextStyle(color: Colors.white38)),
            value: indirmeyeIzin,
            onChanged: (v) => setState(() => indirmeyeIzin = v),
          ),
          SwitchListTile(contentPadding: EdgeInsets.zero, title: const Text('Yorumlara izin ver'), value: yorumlaraIzin, onChanged: (v) => setState(() => yorumlaraIzin = v)),
          SwitchListTile(contentPadding: EdgeInsets.zero, title: const Text('Yeniden paylaşıma izin ver'), value: yenidenPaylasimaIzin, onChanged: (v) => setState(() => yenidenPaylasimaIzin = v)),
          SwitchListTile(contentPadding: EdgeInsets.zero, title: const Text('Otomatik altyazı'), value: otomatikAltyazi, onChanged: (v) => setState(() => otomatikAltyazi = v)),
          SwitchListTile(contentPadding: EdgeInsets.zero, title: const Text('Ortak gönderi'), value: ortakGonderi, onChanged: (v) => setState(() => ortakGonderi = v)),
          const SizedBox(height: 16),
          Row(children: [
            Expanded(child: OutlinedButton.icon(onPressed: taslakKaydet, icon: const Icon(Icons.bookmark_add_outlined), label: const Text('Taslak kaydet'))),
            const SizedBox(width: 10),
            Expanded(child: OutlinedButton.icon(onPressed: () {}, icon: const Icon(Icons.schedule_rounded), label: const Text('Zamanla'))),
          ]),
          const SizedBox(height: 12),
          if (yukleniyor) const Center(child: Column(children: [CircularProgressIndicator(color: mavi), SizedBox(height: 10), Text('İçerik yayınlanıyor...')])) else RenkliButon(yazi: 'NgelX’te Yayınla', tiklama: yayinla),
          const SizedBox(height: 12),
          const Text('Video ve fotoğraf en fazla 50 MB, müzik en fazla 15 MB.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white38, fontSize: 12)),
        ],
      ),
    );
  }

  Widget _bolumBasligi(String yazi) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Text(yazi, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
  );

  Widget _arac(IconData ikon, String yazi) => ActionChip(
    avatar: Icon(ikon, size: 18, color: mavi),
    label: Text(yazi),
    onPressed: () => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$yazi aracı açıldı'))),
  );

  Widget _hizliUret(IconData ikon, String yazi, VoidCallback tiklama) => Padding(
    padding: const EdgeInsets.only(right: 10),
    child: InkWell(
      borderRadius: BorderRadius.circular(18),
      onTap: tiklama,
      child: Container(
        width: 82,
        padding: const EdgeInsets.symmetric(vertical: 12),
        decoration: BoxDecoration(color: panel, borderRadius: BorderRadius.circular(18)),
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(ikon, color: mavi), const SizedBox(height: 6), Text(yazi, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold))]),
      ),
    ),
  );

  Widget _buyukSecenek(IconData ikon, String yazi, VoidCallback tiklama) => InkWell(
    borderRadius: BorderRadius.circular(20),
    onTap: tiklama,
    child: Container(
      padding: const EdgeInsets.symmetric(vertical: 24),
      decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(20)),
      child: Column(children: [Icon(ikon, color: mavi, size: 34), const SizedBox(height: 8), Text(yazi, style: const TextStyle(fontWeight: FontWeight.bold))]),
    ),
  );

  Widget _turButonu(String deger, IconData ikon, String yazi) {
    final secili = tur == deger;
    return Expanded(child: GestureDetector(
      onTap: () => setState(() { tur = deger; medya = null; muzik = null; }),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(gradient: secili ? const LinearGradient(colors: [mavi, mor]) : null, borderRadius: BorderRadius.circular(17)),
        child: Column(children: [Icon(ikon, color: secili ? Colors.black : Colors.white60), const SizedBox(height: 5), Text(yazi, style: TextStyle(color: secili ? Colors.black : Colors.white60, fontWeight: FontWeight.bold))]),
      ),
    ));
  }
}

class EskiYuklePage extends StatefulWidget {
  const EskiYuklePage({super.key});

  @override
  State<EskiYuklePage> createState() => _YuklePageState();
}

class _YuklePageState extends State<EskiYuklePage> {
  bool yukleniyor = false;
  String durum = '';

  Future<void> videoSec() async {
    final dosya = await ImagePicker().pickVideo(
      source: ImageSource.gallery,
    );

    if (dosya == null || !mounted) return;
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    final boyut = await dosya.length();
    if (boyut > 50 * 1024 * 1024) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Video 50 MB’den küçük olmalı.')),
      );
      return;
    }

    setState(() {
      yukleniyor = true;
      durum = 'Video yükleniyor...';
    });
    try {
      final zaman = DateTime.now().millisecondsSinceEpoch;
      final uzanti = dosya.name.contains('.')
          ? dosya.name.split('.').last.toLowerCase()
          : 'mp4';
      final yol = 'videos/${user.uid}/$zaman.$uzanti';
      final baytlar = await dosya.readAsBytes();
      await supa.Supabase.instance.client.storage
          .from('ngelx-media')
          .uploadBinary(yol, baytlar);
      final url = supa.Supabase.instance.client.storage
          .from('ngelx-media')
          .getPublicUrl(yol);
      final profil = await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .get();
      final kullaniciAdi = (profil.data()?['username'] ?? 'ngelx').toString();
      await FirebaseFirestore.instance.collection('videos').add({
        'ownerId': user.uid,
        'username': kullaniciAdi,
        'videoUrl': url,
        'storagePath': yol,
        'description': 'NgelX ile paylaşıldı ✨',
        'createdAt': FieldValue.serverTimestamp(),
      });
      if (!mounted) return;
      setState(() => durum = 'Video yayınlandı! Akışta görebilirsin.');
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Video başarıyla yayınlandı.')),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => durum = 'Yükleme başarısız. Tekrar dene.');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e')),
      );
    } finally {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.video_call_outlined,
                size: 75,
                color: mavi,
              ),
              const SizedBox(height: 20),
              const Text(
                'Yeni içerik üret',
                style: TextStyle(
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Galerinden 50 MB’den küçük bir video seç.',
                style: TextStyle(color: Colors.white54),
              ),
              const SizedBox(height: 25),
              if (yukleniyor)
                const CircularProgressIndicator(color: mavi)
              else
                RenkliButon(
                  yazi: 'Videoyu Seç ve Yayınla',
                  tiklama: videoSec,
                ),
              if (durum.isNotEmpty) ...[
                const SizedBox(height: 18),
                Text(durum, textAlign: TextAlign.center),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class MesajPage extends StatefulWidget {
  const MesajPage({super.key});
  @override State<MesajPage> createState()=>_MesajPageState();
}

class _MesajPageState extends State<MesajPage> {
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;
  Set<String> engellenenler={};
  Set<String> sessizSohbetler={};
  final sohbetAra=TextEditingController();
  String sohbetSorgu='';
  String filtre='Tümü';

  Future<void> tercihleriGetir() async {
    final ben=uid;if(ben==null)return;
    final d=await FirebaseFirestore.instance.collection('users').doc(ben).get();
    if(!mounted)return;
    setState((){
      engellenenler=Set<String>.from(List<dynamic>.from(d.data()?['blocked']??const[]));
      sessizSohbetler=Set<String>.from(List<dynamic>.from(d.data()?['mutedChats']??const[]));
    });
  }

  @override void initState(){super.initState();tercihleriGetir();}
  @override void dispose(){sohbetAra.dispose();super.dispose();}

  Future<void> sessizeAl(String chatId,bool sessiz) async {
    final ben=uid;if(ben==null)return;
    await FirebaseFirestore.instance.collection('users').doc(ben).set({'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true));
    if(mounted)setState(()=>sessiz?sessizSohbetler.add(chatId):sessizSohbetler.remove(chatId));
  }

  Future<void> sohbetMenusu(BuildContext context,String id) async {
    final sessiz=sessizSohbetler.contains(id);
    await showModalBottomSheet(context:context,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      ListTile(leading:Icon(sessiz?Icons.notifications_active_outlined:Icons.notifications_off_outlined),title:Text(sessiz?'Sessizi kaldır':'Sessize al'),onTap:(){Navigator.pop(c);sessizeAl(id,!sessiz);}),
      ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:const Text('Sohbeti listemden kaldır',style:TextStyle(color:Colors.red)),onTap:(){Navigator.pop(c);sohbetSil(context,id);}),
    ])));
  }

  Future<void> sohbetSil(BuildContext context,String id) async {
    final ben=uid;if(ben==null)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sohbet kaldırılsın mı?'),content:const Text('Bu sohbet yalnızca senin gelen kutundan kaldırılacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),TextButton(onPressed:()=>Navigator.pop(c,true),child:const Text('KALDIR',style:TextStyle(color:Colors.red)))]))??false;
    if(ok)await FirebaseFirestore.instance.collection('chats').doc(id).set({'hiddenFor':FieldValue.arrayUnion([ben])},SetOptions(merge:true));
  }

  @override Widget build(BuildContext context){
    final ben=uid;
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),child:ColoredBox(color:Colors.white,child:SafeArea(child:Column(children:[
      Padding(padding:const EdgeInsets.fromLTRB(18,14,10,8),child:Row(children:[const Text('Gelen Kutusu',style:TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),const SizedBox(width:8),const Icon(Icons.done_all_rounded,color:Color(0xFF27C66F)),const Spacer(),IconButton(tooltip:'Arşiv',onPressed:(){},icon:const Icon(Icons.archive_outlined,color:Colors.black54)),IconButton(tooltip:'Grup oluştur',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GrupOlusturPage())),icon:const Icon(Icons.group_add_rounded,color:mor,size:29)),IconButton(tooltip:'Yeni sohbet',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const YeniSohbetPage())),icon:const Icon(Icons.person_add_alt_1,color:mavi,size:29))])),
      Padding(padding:const EdgeInsets.fromLTRB(16,4,16,10),child:TextField(controller:sohbetAra,onChanged:(v)=>setState(()=>sohbetSorgu=v.trim().toLowerCase()),style:const TextStyle(color:Colors.black87),decoration:InputDecoration(hintText:'Sohbetlerde ara',hintStyle:const TextStyle(color:Colors.black45),prefixIcon:const Icon(Icons.search,color:Colors.black45),filled:true,fillColor:const Color(0xFFF3F4F7),border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none)))),
      SizedBox(height:46,child:ListView(padding:const EdgeInsets.symmetric(horizontal:16),scrollDirection:Axis.horizontal,children:['Tümü','Okunmamış','Arkadaşlar','Gruplar'].map((f)=>Padding(padding:const EdgeInsets.only(right:9),child:ChoiceChip(label:Text(f),selected:filtre==f,selectedColor:mor,labelStyle:TextStyle(color:filtre==f?Colors.white:Colors.black87,fontWeight:FontWeight.w700),backgroundColor:const Color(0xFFF1F2F5),side:BorderSide.none,onSelected:(_)=>setState(()=>filtre=f)))).toList())),
      StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:ben==null?null:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).snapshots(),builder:(_,s){final okunmamis=(s.data?.docs??[]).where((d)=>d.data()['read']!=true).length;return Container(margin:const EdgeInsets.fromLTRB(16,8,16,5),decoration:BoxDecoration(color:const Color(0xFFF5EFFF),borderRadius:BorderRadius.circular(20)),child:ListTile(leading:const CircleAvatar(backgroundColor:Color(0xFFE5D5FF),child:Icon(Icons.favorite,color:mor)),title:const Text('Aktivite',style:TextStyle(color:Colors.black,fontWeight:FontWeight.w900)),subtitle:const Text('Beğeniler, yorumlar ve güvenlik bildirimleri',style:TextStyle(color:Colors.black54)),trailing:okunmamis==0?const Icon(Icons.chevron_right,color:Colors.black45):Badge(label:Text('$okunmamis'),child:const Icon(Icons.chevron_right,color:Colors.black45)),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()))));}),
      Container(margin:const EdgeInsets.fromLTRB(16,5,16,8),decoration:BoxDecoration(color:const Color(0xFFEDF7FF),borderRadius:BorderRadius.circular(20)),child:ListTile(leading:const CircleAvatar(backgroundColor:Color(0xFFD8ECFF),child:Icon(Icons.chat_bubble_rounded,color:Colors.blue)),title:const Text('Mesaj İstekleri',style:TextStyle(color:Colors.black,fontWeight:FontWeight.w900)),subtitle:const Text('Seni takip etmeyenlerden gelen mesajlar',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black45),onTap:(){})),
      Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:ben==null?null:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).snapshots(),
        builder:(_,s){
          final docs=(s.data?.docs??[]).where((d){final v=d.data();if(List<String>.from(v['hiddenFor']??const[]).contains(ben))return false;final grup=v['isGroup']==true||List<String>.from(v['members']??const[]).length>2;final unread=(v['unread_$ben']??0) as int;if(filtre=='Okunmamış'&&unread==0)return false;if(filtre=='Gruplar'&&!grup)return false;if(filtre=='Arkadaşlar'&&grup)return false;final son=(v['lastMessage']??'').toString().toLowerCase();return sohbetSorgu.isEmpty||son.contains(sohbetSorgu);}).toList();
          if(docs.isEmpty)return const Center(child:Text('Bu bölümde henüz sohbet yok.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)));
          return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){
            final d=docs[i],v=d.data(),members=List<String>.from(v['members']??[]);
            final grup=v['isGroup']==true||members.length>2;
            if(grup){final ad=(v['groupName']??'Grup sohbeti').toString(),foto=(v['groupPhotoUrl']??'').toString(),unread=(v['unread_$ben']??0) as int;return ListTile(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:d.id,ad:ad,foto:foto))),onLongPress:()=>sohbetMenusu(context,d.id),leading:CircleAvatar(backgroundColor:const Color(0xFFE9DDFF),backgroundImage:foto.isEmpty?null:NetworkImage(foto),child:foto.isEmpty?const Icon(Icons.groups,color:mor):null),title:Text(ad,style:TextStyle(color:Colors.black87,fontWeight:unread>0?FontWeight.w900:FontWeight.w700)),subtitle:Text((v['lastMessage']??'Grup oluşturuldu').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)),trailing:unread>0?Badge(label:Text('$unread')):null);}
            final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');
            if(engellenenler.contains(other))return const SizedBox.shrink();
            return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(other).get(),builder:(_,u){
              final p=u.data?.data()??{};
              if(p['deactivated']==true||List<String>.from(p['blocked']??const[]).contains(ben))return const SizedBox.shrink();
              final unread=(v['unread_$ben']??0) as int;
              final sessiz=sessizSohbetler.contains(d.id);
              return ListTile(
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:d.id,digerUid:other,ad:(p['displayName']??p['username']??'NgelX').toString(),foto:(p['photoUrl']??'').toString()))),
                onLongPress:()=>sohbetMenusu(context,d.id),
                leading:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:NetworkImage(p['photoUrl'])),
                title:Text((p['displayName']??p['username']??'NgelX').toString(),style:TextStyle(fontWeight:unread>0?FontWeight.w900:FontWeight.w700,color:Colors.black87)),
                subtitle:Text((v['lastMessage']??'Yeni sohbet').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)),
                trailing:Wrap(crossAxisAlignment:WrapCrossAlignment.center,children:[if(sessiz)const Icon(Icons.volume_off,size:18,color:Colors.black38),if(unread>0)Badge(label:Text('$unread'))]),
              );
            });
          });
        },
      )),
    ]))));
  }
}
class GrupOlusturPage extends StatefulWidget{const GrupOlusturPage({super.key});@override State<GrupOlusturPage> createState()=>_GrupOlusturPageState();}
class _GrupOlusturPageState extends State<GrupOlusturPage>{
  final ad=TextEditingController(),arama=TextEditingController();final Set<String> secilen={};String sorgu='';XFile? foto;bool kaydediliyor=false;
  @override void dispose(){ad.dispose();arama.dispose();super.dispose();}
  Future<void> olustur()async{final u=FirebaseAuth.instance.currentUser;if(u==null||kaydediliyor)return;if(ad.text.trim().length<2){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup adı en az 2 karakter olmalı.')));return;}if(secilen.length<2){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('En az 2 kişi seç.')));return;}setState(()=>kaydediliyor=true);try{String fotoUrl='';if(foto!=null){final yol='groups/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';await supa.Supabase.instance.client.storage.from('ngelx-media').uploadBinary(yol,await foto!.readAsBytes());fotoUrl=supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);}final ref=FirebaseFirestore.instance.collection('chats').doc();await ref.set({'isGroup':true,'groupName':ad.text.trim(),'groupPhotoUrl':fotoUrl,'members':[u.uid,...secilen],'admins':[u.uid],'createdBy':u.uid,'createdAt':FieldValue.serverTimestamp(),'updatedAt':FieldValue.serverTimestamp(),'lastMessage':'Grup oluşturuldu','hiddenFor':<String>[]});if(mounted)Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:ref.id,ad:ad.text.trim(),foto:fotoUrl)));}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Grup oluşturulamadı: $e')));}finally{if(mounted)setState(()=>kaydediliyor=false);}}
  @override Widget build(BuildContext context){final me=FirebaseAuth.instance.currentUser?.uid;return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Yeni grup',style:TextStyle(fontWeight:FontWeight.w900)),actions:[TextButton(onPressed:kaydediliyor?null:olustur,child:const Text('Oluştur',style:TextStyle(fontWeight:FontWeight.w900)))]),body:Column(children:[
  Padding(padding:const EdgeInsets.all(18),child:Row(children:[GestureDetector(onTap:()async{final x=await ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:85);if(x!=null&&mounted)setState(()=>foto=x);},child:CircleAvatar(radius:34,backgroundColor:const Color(0xFFE9DDFF),child:foto==null?const Icon(Icons.add_a_photo,color:mor):const Icon(Icons.check,color:mor))),const SizedBox(width:14),Expanded(child:TextField(controller:ad,maxLength:50,style:const TextStyle(color:Colors.black87),decoration:const InputDecoration(labelText:'Grup adı',hintText:'Grubuna bir ad ver')))])),
    Padding(padding:const EdgeInsets.symmetric(horizontal:18),child:TextField(controller:arama,onChanged:(v)=>setState(()=>sorgu=v.toLowerCase()),style:const TextStyle(color:Colors.black87),decoration:const InputDecoration(prefixIcon:Icon(Icons.search),hintText:'Gruba kişi ekle'))),
    Padding(padding:const EdgeInsets.fromLTRB(18,12,18,5),child:Align(alignment:Alignment.centerLeft,child:Text('${secilen.length} kişi seçildi',style:const TextStyle(color:mor,fontWeight:FontWeight.bold)))),
    Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').snapshots(),builder:(_,s){final docs=(s.data?.docs??[]).where((d){final v=d.data();final isim=(v['displayName']??v['username']??'').toString().toLowerCase();return d.id!=me&&v['deactivated']!=true&&(sorgu.isEmpty||isim.contains(sorgu));}).toList();return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){final d=docs[i],v=d.data(),isim=(v['displayName']??v['username']??'Kullanıcı').toString(),pf=(v['photoUrl']??'').toString(),secili=secilen.contains(d.id);return CheckboxListTile(value:secili,onChanged:(x)=>setState(()=>x==true?secilen.add(d.id):secilen.remove(d.id)),secondary:CircleAvatar(backgroundImage:pf.isEmpty?null:NetworkImage(pf),child:pf.isEmpty?const Icon(Icons.person):null),title:Text(isim,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text('@${v['username']??'ngelx'}',style:const TextStyle(color:Colors.black54)),activeColor:mor);});})),
  ])));}
}

class GrupSohbetPage extends StatefulWidget{final String chatId,ad,foto;const GrupSohbetPage({super.key,required this.chatId,required this.ad,this.foto=''});@override State<GrupSohbetPage> createState()=>_GrupSohbetPageState();}
class _GrupSohbetPageState extends State<GrupSohbetPage>{final mesaj=TextEditingController();String? get uid=>FirebaseAuth.instance.currentUser?.uid;@override void dispose(){mesaj.dispose();super.dispose();}
  Future<void> gonder()async{final t=mesaj.text.trim(),ben=uid;if(t.isEmpty||ben==null)return;mesaj.clear();final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId),d=await ref.get(),uyeler=List<String>.from(d.data()?['members']??const[]);await ref.collection('messages').add({'senderId':ben,'text':t,'type':'text','createdAt':FieldValue.serverTimestamp()});final g=<String,dynamic>{'lastMessage':t,'updatedAt':FieldValue.serverTimestamp()};for(final x in uyeler){if(x!=ben)g['unread_$x']=FieldValue.increment(1);}await ref.set(g,SetOptions(merge:true));}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:Row(children:[CircleAvatar(backgroundColor:const Color(0xFFE9DDFF),backgroundImage:widget.foto.isEmpty?null:NetworkImage(widget.foto),child:widget.foto.isEmpty?const Icon(Icons.groups,color:mor):null),const SizedBox(width:10),Expanded(child:Text(widget.ad,style:const TextStyle(fontWeight:FontWeight.w800)))]),actions:[IconButton(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId))),icon:const Icon(Icons.info_outline,color:mor))]),body:Column(children:[Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(widget.chatId).collection('messages').orderBy('createdAt',descending:true).snapshots(),builder:(_,s)=>ListView(reverse:true,padding:const EdgeInsets.all(12),children:(s.data?.docs??[]).map((d){final v=d.data(),ben=v['senderId']==uid,metin=(v['text']??v['message']??v['content']??'').toString();return Align(alignment:ben?Alignment.centerRight:Alignment.centerLeft,child:Container(constraints:const BoxConstraints(maxWidth:280),margin:const EdgeInsets.all(4),padding:const EdgeInsets.all(12),decoration:BoxDecoration(color:ben?const Color(0xFF7C3AED):const Color(0xFFF0F1F4),borderRadius:BorderRadius.circular(18)),child:Text(metin.isEmpty?'Mesaj içeriği bulunamadı':metin,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:16))));}).toList()))),Padding(padding:EdgeInsets.fromLTRB(8,7,8,MediaQuery.of(context).viewInsets.bottom+8),child:Row(children:[IconButton(onPressed:(){},icon:const Icon(Icons.add_circle_outline,color:mor)),Expanded(child:TextField(controller:mesaj,onSubmitted:(_)=>gonder(),decoration:const InputDecoration(hintText:'Gruba mesaj yaz...'))),IconButton(onPressed:gonder,icon:const Icon(Icons.send_rounded,color:mor))]))])));
}

class GrupBilgiPage extends StatelessWidget{final String chatId;const GrupBilgiPage({super.key,required this.chatId});@override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Grup bilgileri')),body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(chatId).snapshots(),builder:(_,s){final v=s.data?.data()??{},uyeler=List<String>.from(v['members']??const[]),yoneticiler=List<String>.from(v['admins']??const[]),ben=FirebaseAuth.instance.currentUser?.uid,yonetici=yoneticiler.contains(ben);return ListView(padding:const EdgeInsets.all(18),children:[CircleAvatar(radius:50,backgroundColor:const Color(0xFFE9DDFF),backgroundImage:(v['groupPhotoUrl']??'').toString().isEmpty?null:NetworkImage(v['groupPhotoUrl']),child:(v['groupPhotoUrl']??'').toString().isEmpty?const Icon(Icons.groups,color:mor,size:48):null),const SizedBox(height:10),Text((v['groupName']??'Grup').toString(),textAlign:TextAlign.center,style:const TextStyle(color:Colors.black,fontSize:25,fontWeight:FontWeight.w900)),Text('${uyeler.length} üye',textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54)),if(yonetici)ListTile(leading:const Icon(Icons.edit,color:mor),title:const Text('Grup adını ve fotoğrafını düzenle'),onTap:()async{final c=TextEditingController(text:(v['groupName']??'').toString());final yeni=await showDialog<String>(context:context,builder:(x)=>AlertDialog(title:const Text('Grup adını düzenle'),content:TextField(controller:c,maxLength:50),actions:[TextButton(onPressed:()=>Navigator.pop(x),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(x,c.text.trim()),child:const Text('Kaydet'))]));c.dispose();if(yeni!=null&&yeni.length>=2)await FirebaseFirestore.instance.collection('chats').doc(chatId).update({'groupName':yeni});}),const Divider(),const Text('Üyeler',style:TextStyle(color:Colors.black,fontSize:18,fontWeight:FontWeight.w900)),...uyeler.map((id)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(id).get(),builder:(_,u){final p=u.data?.data()??{},isim=(p['displayName']??p['username']??'Kullanıcı').toString();return ListTile(leading:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:NetworkImage(p['photoUrl'])),title:Text(isim),subtitle:Text(yoneticiler.contains(id)?'Yönetici':'Üye'),trailing:yonetici&&id!=ben?IconButton(onPressed:()=>FirebaseFirestore.instance.collection('chats').doc(chatId).update({'members':FieldValue.arrayRemove([id])}),icon:const Icon(Icons.person_remove,color:Colors.red)):null);})),const Divider(),ListTile(leading:const Icon(Icons.exit_to_app,color:Colors.red),title:const Text('Gruptan ayrıl',style:TextStyle(color:Colors.red)),onTap:()async{if(ben!=null){await FirebaseFirestore.instance.collection('chats').doc(chatId).update({'members':FieldValue.arrayRemove([ben]),'admins':FieldValue.arrayRemove([ben])});if(context.mounted)Navigator.popUntil(context,(r)=>r.isFirst);}})]);})));}

class YeniSohbetPage extends StatefulWidget {
  const YeniSohbetPage({super.key});
  @override State<YeniSohbetPage> createState()=>_YeniSohbetPageState();
}
class _YeniSohbetPageState extends State<YeniSohbetPage>{
  final arama=TextEditingController();
  String sorgu='';
  Set<String> engellenenler={};
  @override void initState(){super.initState();engellenenleriGetir();}
  Future<void> engellenenleriGetir()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();if(mounted)setState(()=>engellenenler=Set<String>.from(List<dynamic>.from(d.data()?['blocked']??const[])));}
  @override void dispose(){arama.dispose();super.dispose();}
  TextSpan vurgula(String metin){final q=sorgu.toLowerCase(),m=metin.toLowerCase(),i=q.isEmpty?-1:m.indexOf(q);if(i<0)return TextSpan(text:metin,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600));return TextSpan(children:[TextSpan(text:metin.substring(0,i),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600)),TextSpan(text:metin.substring(i,i+q.length),style:const TextStyle(color:Colors.blue,fontWeight:FontWeight.w900)),TextSpan(text:metin.substring(i+q.length),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600))]);}
  @override
  Widget build(BuildContext context) {
    final me = FirebaseAuth.instance.currentUser?.uid;
    final beyazTema = ThemeData.light().copyWith(
      scaffoldBackgroundColor: Colors.white,
      appBarTheme: const AppBarTheme(backgroundColor: Colors.white, foregroundColor: Colors.black, elevation: 0),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFFF1F3F5),
        prefixIconColor: Colors.black54,
        hintStyle: const TextStyle(color: Colors.black45),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
      ),
    );
    return Theme(
      data: beyazTema,
      child: Scaffold(
        appBar: AppBar(title: const Text('Yeni sohbet', style: TextStyle(fontWeight: FontWeight.bold))),
        body: Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(18, 8, 18, 14),
            child: TextField(
              controller: arama,
              onChanged: (v) => setState(() => sorgu = v.trim().toLowerCase()),
              style: const TextStyle(color: Colors.black87),
              decoration: const InputDecoration(prefixIcon: Icon(Icons.search), hintText: 'Kişi veya kullanıcı adı ara'),
            ),
          ),
          Expanded(
            child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: FirebaseFirestore.instance.collection('users').snapshots(),
              builder: (_, s) {
                final docs = (s.data?.docs ?? []).where((d) {
                  if (d.id == me || engellenenler.contains(d.id)) return false;
                  final v = d.data();
                  if(v['deactivated']==true||List<String>.from(v['blocked']??const[]).contains(me))return false;
                  return true;
                }).toList();
                if (s.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator(color: mavi));
                }
                if (docs.isEmpty) {
                  return const Center(child: Text('Aramana uygun kişi bulunamadı.', style: TextStyle(color: Colors.black54)));
                }
                return ListView.separated(
                  itemCount: docs.length,
                  separatorBuilder: (_, __) => const Divider(height: 1, indent: 82, color: Color(0xFFE5E7EB)),
                  itemBuilder: (_, i) {
                    final d = docs[i], v = d.data();
                    final foto = (v['photoUrl'] ?? '').toString();
                    final ad = (v['displayName'] ?? v['username'] ?? 'NgelX').toString();
                    final ids = me==null?<String>[d.id]:<String>[me,d.id]..sort();
                    final chatId=ids.join('_');
                    return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('chats').doc(chatId).get(),builder:(_,chat){final last=(chat.data?.data()?['lastMessage']??'').toString();final adEslesir=ad.toLowerCase().contains(sorgu)||(v['username']??'').toString().toLowerCase().contains(sorgu);final mesajEslesir=last.toLowerCase().contains(sorgu);if(sorgu.isNotEmpty&&!adEslesir&&!mesajEslesir)return const SizedBox.shrink();return InkWell(
                      onTap: () {
                        if (me == null) return;
                        Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => SohbetPage(chatId: chatId, digerUid: d.id, ad: ad, foto: foto)));
                        FirebaseFirestore.instance.collection('chats').doc(chatId).set({
                          'members': ids,
                          'updatedAt': FieldValue.serverTimestamp(),
                          'hiddenFor': FieldValue.arrayRemove([me]),
                        }, SetOptions(merge: true));
                      },
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                        leading: CircleAvatar(
                          radius: 27,
                          backgroundColor: const Color(0xFFE5E7EB),
                          backgroundImage: foto.isEmpty ? null : NetworkImage(foto),
                          child: foto.isEmpty ? const Icon(Icons.person, color: Colors.black45) : null,
                        ),
                        title: RichText(text:vurgula(ad)),
                        subtitle: Text(last.isNotEmpty?last:'@${v['username'] ?? 'ngelx'}',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:mesajEslesir&&sorgu.isNotEmpty?Colors.blue:Colors.black54,fontWeight:mesajEslesir&&sorgu.isNotEmpty?FontWeight.bold:FontWeight.normal)),
                        trailing: const Icon(Icons.chevron_right, color: Colors.blue),
                      ),
                    );});
                  },
                );
              },
            ),
          ),
        ]),
      ),
    );
  }
}

class SohbetPage extends StatefulWidget {final String chatId,digerUid,ad,foto;const SohbetPage({super.key,required this.chatId,required this.digerUid,required this.ad,this.foto=''});@override State<SohbetPage> createState()=>_SohbetPageState();}
class _SohbetPageState extends State<SohbetPage> {
  final mesaj=TextEditingController();
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;

  Future<String?> mesajEngeli() async {
    final ben=uid;
    if(ben==null)return 'Mesaj göndermek için giriş yap.';
    try {
      final sonuc=await Future.wait([
        FirebaseFirestore.instance.collection('users').doc(ben).get(),
        FirebaseFirestore.instance.collection('users').doc(widget.digerUid).get(),
      ]);
      final benim=sonuc[0].data()??{};
      final diger=sonuc[1].data()??{};
      final benimEngellediklerim=List<String>.from(benim['blocked']??const[]);
      final onunEngelledikleri=List<String>.from(diger['blocked']??const[]);
      if(benimEngellediklerim.contains(widget.digerUid)||onunEngelledikleri.contains(ben))return 'Engellenen hesaplar arasında mesaj gönderilemez.';
      if(diger['deactivated']==true)return 'Bu hesap şu anda kullanılamıyor.';
      final arkadaslar=List<String>.from(diger['friends']??const[]);
      if(diger['friendsOnlyMessages']!=false&&!arkadaslar.contains(ben))return 'Bu kullanıcı yalnızca arkadaşlarından mesaj kabul ediyor.';
      return null;
    } catch (_) {
      return 'Mesaj izni kontrol edilemedi. İnternet bağlantını kontrol et.';
    }
  }

  Future<void> gonder() async {
    final t=mesaj.text.trim();
    if(t.isEmpty||uid==null)return;
    final engel=await mesajEngeli();
    if(engel!=null){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(engel)));return;}
    mesaj.clear();
    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    try {
      await ref.set({'members':[uid,widget.digerUid],'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      await ref.collection('messages').add({'senderId':uid,'text':t,'type':'text','createdAt':FieldValue.serverTimestamp()});
      await ref.set({'lastMessage':t,'updatedAt':FieldValue.serverTimestamp(),'unread_${widget.digerUid}':FieldValue.increment(1)},SetOptions(merge:true));
      await uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:uid!,tur:'message',metin:'Yeni bir mesajın var',belgeId:widget.chatId);
    } catch(e) {
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Mesaj gönderilemedi: $e')));
    }
  }

  Future<void> medyaGonder(ImageSource kaynak) async {
    if(uid==null)return;
    final engel=await mesajEngeli();
    if(engel!=null){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(engel)));return;}
    final x=await ImagePicker().pickImage(source:kaynak,imageQuality:82);
    if(x==null)return;
    try {
      final yol='chats/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.jpg';
      await supa.Supabase.instance.client.storage.from('ngelx-media').upload(yol,File(x.path));
      final url=supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);
      final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
      await ref.set({'members':[uid,widget.digerUid]},SetOptions(merge:true));
      await ref.collection('messages').add({'senderId':uid,'text':'','type':'photo','mediaUrl':url,'createdAt':FieldValue.serverTimestamp()});
      await ref.set({'lastMessage':'📷 Fotoğraf','updatedAt':FieldValue.serverTimestamp(),'unread_${widget.digerUid}':FieldValue.increment(1)},SetOptions(merge:true));
      await uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:uid!,tur:'message',metin:'Yeni bir fotoğraf mesajın var',belgeId:widget.chatId);
    } catch(e) {
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Medya gönderilemedi.')));
    }
  }

  void bilgi()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetBilgiPage(uid:widget.digerUid,ad:widget.ad,foto:widget.foto,chatId:widget.chatId)));

  @override
  void initState(){
    super.initState();
    if(uid!=null)FirebaseFirestore.instance.collection('chats').doc(widget.chatId).set({'unread_$uid':0},SetOptions(merge:true));
  }

  @override
  void dispose(){mesaj.dispose();super.dispose();}

  @override
  Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(
    appBar:AppBar(
      leading:const BackButton(color:Colors.blue),
      title:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.digerUid))),child:Row(children:[CircleAvatar(radius:18,backgroundImage:widget.foto.isEmpty?null:NetworkImage(widget.foto)),const SizedBox(width:9),Expanded(child:Text(widget.ad))])),
      actions:[
        IconButton(onPressed:()=>ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli arama başlatılıyor…'))),icon:const Icon(Icons.call,color:Colors.blue)),
        IconButton(onPressed:()=>ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Görüntülü arama başlatılıyor…'))),icon:const Icon(Icons.videocam,color:Colors.blue)),
        IconButton(onPressed:bilgi,icon:const Icon(Icons.info,color:Colors.blue)),
      ],
    ),
    body:Column(children:[
      Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('chats').doc(widget.chatId).collection('messages').orderBy('createdAt',descending:true).snapshots(),
        builder:(_,s)=>ListView(reverse:true,padding:const EdgeInsets.all(12),children:(s.data?.docs??[]).map((d){final v=d.data(),ben=v['senderId']==uid,photo=v['type']=='photo';final metin=(v['text']??v['message']??v['content']??'').toString().trim();return Align(alignment:ben?Alignment.centerRight:Alignment.centerLeft,child:Container(constraints:const BoxConstraints(maxWidth:280),margin:const EdgeInsets.all(4),padding:EdgeInsets.all(photo?4:12),decoration:BoxDecoration(color:ben?const Color(0xFF1687FF):const Color(0xFFF0F1F4),borderRadius:BorderRadius.circular(18)),child:photo?ClipRRect(borderRadius:BorderRadius.circular(15),child:Image.network((v['mediaUrl']??'').toString(),width:220,fit:BoxFit.cover)):Text(metin.isEmpty?'Mesaj içeriği bulunamadı':metin,softWrap:true,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:16,height:1.3))));}).toList()),
      )),
      Padding(
        padding:EdgeInsets.fromLTRB(4,7,4,MediaQuery.of(context).viewInsets.bottom+8),
        child:Row(children:[
          IconButton(onPressed:()=>medyaGonder(ImageSource.camera),icon:const Icon(Icons.camera_alt,color:Colors.blue)),
          IconButton(onPressed:()=>medyaGonder(ImageSource.gallery),icon:const Icon(Icons.photo_library,color:Colors.blue)),
          Expanded(child:TextField(controller:mesaj,onSubmitted:(_)=>gonder(),decoration:const InputDecoration(hintText:'Mesaj'))),
          IconButton(onPressed:()=>mesaj.text+=' 😊',icon:const Icon(Icons.emoji_emotions,color:Colors.blue)),
          IconButton(onPressed:gonder,icon:const Icon(Icons.send,color:Colors.blue)),
        ]),
      ),
    ]),
  ));
}

class SohbetBilgiPage extends StatelessWidget{final String uid,ad,foto,chatId;const SohbetBilgiPage({super.key,required this.uid,required this.ad,required this.foto,required this.chatId});@override Widget build(BuildContext context)=>Scaffold(appBar:AppBar(),body:ListView(padding:const EdgeInsets.all(20),children:[CircleAvatar(radius:55,backgroundImage:foto.isEmpty?null:NetworkImage(foto)),const SizedBox(height:12),Text(ad,textAlign:TextAlign.center,style:const TextStyle(fontSize:27,fontWeight:FontWeight.bold)),const SizedBox(height:20),Wrap(alignment:WrapAlignment.spaceEvenly,children:[_kisa(Icons.person,'Profil',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uid)))),_kisa(Icons.text_fields,'Takma ad',()=>_bilgi(context,'Takma ad yalnızca bu özel sohbette görünür.')),_kisa(Icons.search,'Arama',()=>_bilgi(context,'Sohbet araması açıldı.')),_kisa(Icons.palette,'Özelleştir',()=>_bilgi(context,'Sohbet temasını seç.'))]),const Divider(height:40),_satir(Icons.photo_library,'Medya, dosya ve bağlantılar'),_satir(Icons.push_pin,'Sabitlenmiş mesajlar'),const Divider(),_satir(Icons.notifications_off,'Sessize al'),_satir(Icons.volume_up,'Bildirimler ve sesler'),_satir(Icons.do_not_disturb_alt,'Kısıtla'),_satir(Icons.block,'Engelle',renk:Colors.red),_satir(Icons.delete_forever,'Sohbeti sil',renk:Colors.red),_satir(Icons.report,'Şikâyet et',renk:Colors.red)]));Widget _kisa(IconData i,String t,VoidCallback f)=>InkWell(onTap:f,child:SizedBox(width:78,child:Column(children:[CircleAvatar(backgroundColor:Colors.blue.withValues(alpha:.15),child:Icon(i,color:Colors.blue)),const SizedBox(height:5),Text(t,textAlign:TextAlign.center)])));Widget _satir(IconData i,String t,{Color? renk})=>ListTile(leading:Icon(i,color:renk),title:Text(t,style:TextStyle(color:renk)));void _bilgi(BuildContext c,String t)=>ScaffoldMessenger.of(c).showSnackBar(SnackBar(content:Text(t)));}

class AktivitePage extends StatelessWidget {
  const AktivitePage({super.key});

  IconData _ikon(String tur){switch(tur){case 'like':return Icons.favorite_rounded;case 'comment':return Icons.mode_comment_rounded;case 'message':return Icons.chat_bubble_rounded;case 'security':return Icons.shield_rounded;case 'follow_request':return Icons.person_add_alt_1_rounded;case 'friend_accepted':return Icons.people_rounded;default:return Icons.notifications_rounded;}}
  Color _renk(String tur){switch(tur){case 'like':return const Color(0xFFFF3B73);case 'comment':return Colors.blue;case 'security':return Colors.orange;case 'follow_request':return mor;default:return const Color(0xFF20B86A);}}

  Future<void> _aktiviteAc(BuildContext context, QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final v=d.data();await d.reference.set({'read':true},SetOptions(merge:true));if(!context.mounted)return;
    final from=(v['fromUid']??'').toString(),tur=(v['type']??'').toString();
    if(from.isNotEmpty&&(tur=='follow_request'||tur=='friend_accepted'||tur=='like'||tur=='comment')){Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:from)));return;}
    if(tur=='message'&&from.isNotEmpty){final p=await FirebaseFirestore.instance.collection('users').doc(from).get();if(!context.mounted)return;final ids=[FirebaseAuth.instance.currentUser!.uid,from]..sort();Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:(v['sourceId']??v['chatId']??v['belgeId']??ids.join('_')).toString(),digerUid:from,ad:(p.data()?['displayName']??p.data()?['username']??'Kullanıcı').toString(),foto:(p.data()?['photoUrl']??'').toString())));}
  }

  Future<void> istegiSonuclandir(BuildContext context, QueryDocumentSnapshot<Map<String, dynamic>> belge, bool kabul) async {
    final ben = FirebaseAuth.instance.currentUser?.uid;
    final gonderen = (belge.data()['fromUid'] ?? '').toString();
    if (ben == null || gonderen.isEmpty || belge.data()['status'] != 'pending') return;
    final toplu = FirebaseFirestore.instance.batch();
    toplu.update(belge.reference, {'status': kabul ? 'accepted' : 'rejected', 'read': true, 'answeredAt': FieldValue.serverTimestamp()});
    if (kabul) {
      final gonderenBelgesi = await FirebaseFirestore.instance.collection('users').doc(gonderen).get();
      final kabulBildirimiAcik = gonderenBelgesi.data()?['notificationsEnabled'] != false && gonderenBelgesi.data()?['friendNotifications'] != false;
      toplu.set(FirebaseFirestore.instance.collection('users').doc(ben), {
        'friends': FieldValue.arrayUnion([gonderen]),
        'followers': FieldValue.arrayUnion([gonderen]),
      }, SetOptions(merge: true));
      toplu.set(FirebaseFirestore.instance.collection('users').doc(gonderen), {
        'friends': FieldValue.arrayUnion([ben]),
        'following': FieldValue.arrayUnion([ben]),
      }, SetOptions(merge: true));
      if(kabulBildirimiAcik) {
        toplu.set(FirebaseFirestore.instance.collection('notifications').doc('friend_accepted_' + ben + '_' + gonderen), {
          'toUid': gonderen,
          'fromUid': ben,
          'type': 'friend_accepted',
          'text': 'Arkadaşlık isteğin kabul edildi',
          'read': false,
          'createdAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true));
      }
    }
    await toplu.commit();
    if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(kabul ? 'Arkadaşlık isteği kabul edildi ✅' : 'İstek reddedildi.')));
  }

  @override
  Widget build(BuildContext context) {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),dividerColor:const Color(0xFFE8E9ED)),child:Scaffold(
      backgroundColor:Colors.white,
      appBar: AppBar(title: const Text('Aktivite',style:TextStyle(fontWeight:FontWeight.w900)),actions:[IconButton(tooltip:'Tümünü okundu yap',onPressed:()async{if(uid==null)return;final q=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:uid).get();final b=FirebaseFirestore.instance.batch();for(final d in q.docs){b.set(d.reference,{'read':true},SetOptions(merge:true));}await b.commit();},icon:const Icon(Icons.done_all_rounded,color:Color(0xFF20B86A)))]),
      body: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
        stream: uid == null ? null : FirebaseFirestore.instance.collection('notifications').where('toUid', isEqualTo: uid).snapshots(),
        builder: (_, s) {
          if(s.hasError)return const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:52),SizedBox(height:10),Text('Aktiviteler yüklenemedi',style:TextStyle(color:Colors.black,fontWeight:FontWeight.w800)),Text('İnternet bağlantını kontrol edip tekrar dene.',style:TextStyle(color:Colors.black54))]));
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final docs = (s.data?.docs ?? []).toList()
            ..sort((a, b) {
              final at = a.data()['createdAt'];
              final bt = b.data()['createdAt'];
              final ad = at is Timestamp ? at.toDate() : DateTime.fromMillisecondsSinceEpoch(0);
              final bd = bt is Timestamp ? bt.toDate() : DateTime.fromMillisecondsSinceEpoch(0);
              return bd.compareTo(ad);
            });
          if (docs.isEmpty) return const Center(child: Column(mainAxisSize:MainAxisSize.min,children:[CircleAvatar(radius:36,backgroundColor:Color(0xFFF1E9FF),child:Icon(Icons.notifications_none_rounded,color:mor,size:38)),SizedBox(height:13),Text('Henüz yeni aktivite yok',style:TextStyle(color:Colors.black,fontSize:18,fontWeight:FontWeight.w900)),Text('Beğeni, yorum ve güvenlik bildirimleri burada görünür.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54))]));
          return ListView.separated(padding:const EdgeInsets.fromLTRB(12,8,12,24),separatorBuilder:(_,__)=>const Divider(height:1,indent:72),itemCount:docs.length,itemBuilder:(_,i){final d=docs[i];
            final v = d.data();
            final tur=(v['type']??'').toString(),okundu=v['read']==true,foto=(v['photoUrl']??'').toString();
            final bekliyor = v['type'] == 'follow_request' && v['status'] == 'pending';
            return Container(decoration:BoxDecoration(color:okundu?Colors.white:const Color(0xFFF8F4FF),borderRadius:BorderRadius.circular(17)),child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
              leading: Stack(children:[CircleAvatar(radius:26,backgroundColor:_renk(tur).withOpacity(.13),backgroundImage:foto.isEmpty?null:NetworkImage(foto),child:foto.isEmpty?Icon(_ikon(tur),color:_renk(tur)):null),if(!okundu)const Positioned(right:0,top:0,child:CircleAvatar(radius:5,backgroundColor:Color(0xFF7C3AED)))]),
              title: Text((v['text'] ?? v['message'] ?? v['content'] ?? 'Yeni bildirim').toString(), style: TextStyle(color:Colors.black87,fontWeight:okundu?FontWeight.w600:FontWeight.w900)),
              subtitle: Text(zamanKisa(v['createdAt']),style:const TextStyle(color:Colors.black45)),
              trailing: bekliyor ? Wrap(children: [
                IconButton(onPressed: () => istegiSonuclandir(context, d, true), icon: const Icon(Icons.check, color: Colors.green)),
                IconButton(onPressed: () => istegiSonuclandir(context, d, false), icon: const Icon(Icons.close, color: Colors.red)),
              ]) : (v['status'] == 'accepted' ? const Icon(Icons.people, color: Colors.green) : null),
              onTap: () => _aktiviteAc(context,d),
            ));
          });
        },
      ),
    ));
  }
}
String zamanKisa(dynamic t){if(t is! Timestamp)return 'Şimdi';final f=DateTime.now().difference(t.toDate());if(f.inMinutes<1)return 'Şimdi';if(f.inHours<1)return '${f.inMinutes} dk önce';if(f.inDays<1)return '${f.inHours} sa önce';return '${f.inDays} gün önce';}

class KullaniciProfilPage extends StatelessWidget {
  final String uid;
  const KullaniciProfilPage({super.key, required this.uid});

  @override
  Widget build(BuildContext context) {
    final me = FirebaseAuth.instance.currentUser?.uid;
    final hedef = FirebaseFirestore.instance.collection('users').doc(uid).get();
    final benim = me == null ? Future.value(null) : FirebaseFirestore.instance.collection('users').doc(me).get();
    return Scaffold(
      appBar: AppBar(title: const Text('NgelX Profili')),
      body: FutureBuilder<List<DocumentSnapshot<Map<String, dynamic>>?>>(
        future: Future.wait([hedef, benim]),
        builder: (_, s) {
          if (!s.hasData) return const Center(child: CircularProgressIndicator(color: mavi));
          final v = s.data![0]?.data() ?? <String, dynamic>{};
          final benimVerim = s.data![1]?.data() ?? <String, dynamic>{};
          final foto = (v['photoUrl'] ?? '').toString();
          final arkadaslar = Set<String>.from(List<dynamic>.from(benimVerim['friends'] ?? []));
          final gizli = v['privateAccount'] == true;
          final erisimVar = me == uid || !gizli || arkadaslar.contains(uid);
          return ListView(
            padding: const EdgeInsets.all(22),
            children: [
              Center(child: CircleAvatar(radius: 55, backgroundImage: foto.isEmpty ? null : NetworkImage(foto), child: foto.isEmpty ? const Text('N', style: TextStyle(fontSize: 40)) : null)),
              const SizedBox(height: 12),
              Text((v['displayName'] ?? v['username'] ?? 'NgelX').toString(), textAlign: TextAlign.center, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
              Text('@' + (v['username'] ?? 'ngelx').toString(), textAlign: TextAlign.center, style: const TextStyle(color: Colors.white54)),
              const SizedBox(height: 16),
              Text((v['bio'] ?? '').toString(), textAlign: TextAlign.center),
              const SizedBox(height: 22),
              if (me != uid) Row(children: [
                Expanded(child: FilledButton(
                  onPressed: arkadaslar.contains(uid) ? null : () async {
                    if (me == null) return;
                    final istekId = 'friend_request_' + me + '_' + uid;
                    final istek = FirebaseFirestore.instance.collection('notifications').doc(istekId);
                    final onceki = await istek.get();
                    if (onceki.data()?['status'] == 'pending') {
                      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Arkadaşlık isteğin zaten bekliyor.')));
                      return;
                    }
                    await istek.set({'toUid': uid, 'fromUid': me, 'type': 'follow_request', 'text': 'Yeni arkadaşlık isteğin var', 'status': 'pending', 'read': false, 'createdAt': FieldValue.serverTimestamp()});
                    if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Takip isteği gönderildi ✅')));
                  },
                  child: Text(arkadaslar.contains(uid) ? 'Arkadaşsınız' : 'Takip isteği gönder'),
                )),
                const SizedBox(width: 10),
                IconButton(
                  onPressed: () async {
                    if (me == null) return;
                    final ids = [me, uid]..sort();
                    final id = ids.join('_');
                    await FirebaseFirestore.instance.collection('chats').doc(id).set({'members': ids, 'updatedAt': FieldValue.serverTimestamp()}, SetOptions(merge: true));
                    if (context.mounted) Navigator.push(context, MaterialPageRoute(builder: (_) => SohbetPage(chatId: id, digerUid: uid, ad: (v['displayName'] ?? v['username'] ?? 'NgelX').toString(),foto:foto)));
                  },
                  icon: const Icon(Icons.message, color: mavi),
                ),
              ]),
              const SizedBox(height: 20),
              if (!erisimVar)
                Container(
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(color: panel, borderRadius: BorderRadius.circular(20)),
                  child: const Column(children: [
                    Icon(Icons.lock_outline, size: 48, color: mor),
                    SizedBox(height: 12),
                    Text('Bu hesap gizli', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    SizedBox(height: 7),
                    Text('Paylaşımları görmek için arkadaşlık isteğinin kabul edilmesi gerekiyor.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white60)),
                  ]),
                )
              else
                StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                  stream: FirebaseFirestore.instance.collection('videos').where('ownerId', isEqualTo: uid).snapshots(),
                  builder: (_, p) {
                    final docs = (p.data?.docs ?? []).where((d) => d.data()['type'] != 'story').toList();
                    return GridView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: docs.length,
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6),
                      itemBuilder: (_, i) {
                        final x = docs[i].data();
                        final tur = (x['type'] ?? 'video').toString();
                        final url = (x['mediaUrl'] ?? x['videoUrl'] ?? '').toString();
                        return MedyaOnizleme(tur: tur, url: url, yazi: (x['description'] ?? '').toString(), arkaPlan: panel);
                      },
                    );
                  },
                ),
            ],
          );
        },
      ),
    );
  }
}

class MedyaOnizleme extends StatelessWidget {
  final String tur, url, yazi;
  final Color arkaPlan;
  const MedyaOnizleme({super.key, required this.tur, required this.url, required this.yazi, required this.arkaPlan});
  @override Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(13),
    child: ColoredBox(
      color: arkaPlan,
      child: tur == 'photo' && url.isNotEmpty
          ? Image.network(url, fit: BoxFit.cover, errorBuilder: (_, __, ___) => const SizedBox.expand())
          : tur == 'video' && url.isNotEmpty
              ? VideoIlkKare(url: url)
              : Padding(padding: const EdgeInsets.all(9), child: Center(child: Text(yazi, maxLines: 6, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center))),
    ),
  );
}

class VideoIlkKare extends StatefulWidget {
  final String url;
  const VideoIlkKare({super.key, required this.url});
  @override State<VideoIlkKare> createState() => _VideoIlkKareState();
}
class _VideoIlkKareState extends State<VideoIlkKare> {
  late final VideoPlayerController kontrol;
  bool hazir = false;
  @override void initState() {
    super.initState();
    kontrol = VideoPlayerController.networkUrl(Uri.parse(widget.url));
    kontrol.initialize().then((_) async { await kontrol.seekTo(Duration.zero); await kontrol.pause(); if (mounted) setState(() => hazir = true); }).catchError((_){ });
  }
  @override void dispose() { kontrol.dispose(); super.dispose(); }
  @override Widget build(BuildContext context) => Stack(
    fit: StackFit.expand,
    children: [
      if (hazir) FittedBox(fit: BoxFit.cover, child: SizedBox(width: kontrol.value.size.width, height: kontrol.value.size.height, child: VideoPlayer(kontrol))),
      if (!hazir) const Center(child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white54)),
      const Center(child: Icon(Icons.play_arrow_rounded, size: 48, color: Colors.white)),
    ],
  );
}

class HikayeGosterPage extends StatefulWidget {final String url,kullanici;const HikayeGosterPage({super.key,required this.url,required this.kullanici});@override State<HikayeGosterPage> createState()=>_HikayeGosterPageState();}
class _HikayeGosterPageState extends State<HikayeGosterPage> with SingleTickerProviderStateMixin {
  late final AnimationController sure;
  @override void initState(){super.initState();sure=AnimationController(vsync:this,duration:const Duration(seconds:5))..addStatusListener((s){if(s==AnimationStatus.completed&&mounted)Navigator.pop(context);})..forward();}
  @override void dispose(){sure.dispose();super.dispose();}
  @override Widget build(BuildContext context){return Scaffold(
    backgroundColor:Colors.black,
    body:GestureDetector(
      onLongPressStart:(_)=>sure.stop(),
      onLongPressEnd:(_)=>sure.forward(),
      child:Stack(fit:StackFit.expand,children:[
        Image.network(widget.url,fit:BoxFit.contain),
        SafeArea(child:Padding(padding:const EdgeInsets.all(14),child:Column(children:[
          AnimatedBuilder(animation:sure,builder:(_,__)=>LinearProgressIndicator(value:sure.value,color:mavi,backgroundColor:Colors.white24)),
          const SizedBox(height:10),
          Row(children:[const CircleAvatar(radius:17,backgroundColor:mor,child:Text('N')),const SizedBox(width:9),Text(widget.kullanici,style:const TextStyle(fontWeight:FontWeight.bold)),const Spacer(),IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close,size:31))]),
        ]))),
      ]),
    ),
  );}
}

class AyarlarPage extends StatelessWidget {
  const AyarlarPage({super.key});
  @override Widget build(BuildContext context){final misafir=FirebaseAuth.instance.currentUser?.isAnonymous==true;return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),cardTheme:const CardThemeData(color:Colors.white,elevation:0,margin:EdgeInsets.symmetric(vertical:4)),dividerColor:Color(0xFFE5E7EB)),child:Scaffold(appBar:AppBar(title:const Text('Ayarlar ve gizlilik')),body:SafeArea(child:ListView(padding:const EdgeInsets.fromLTRB(14,8,14,24),children:[
    if(!misafir)...[
      _ayar(context,Icons.lock_outline,'Gizlilik','Paylaşımlarını ve hesabını kimler görebilir'),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.people_outline,color:mor),title:const Text('Takip ve arkadaşlık',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('İstekleri kabul et, reddet ve arkadaşlarını yönet',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()))),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.block_outlined,color:mor),title:const Text('Engellenen hesaplar',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('Engellediğin kişileri gör ve engeli kaldır',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const EngellenenlerPage()))),
      _ayar(context,Icons.chat_bubble_outline,'Mesaj izinleri','Kimlerin mesaj gönderebileceğini seç'),
      _ayar(context,Icons.auto_stories_outlined,'Hikâye gizliliği','Görüntüleme ve ekran görüntüsü izinleri'),
      _ayar(context,Icons.notifications_outlined,'Bildirimler','Aktivite ve mesaj bildirimleri'),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.security_outlined,color:mor),title:const Text('Hesap güvenliği',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('Hesabı dondur, silme talebi oluştur',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const HesapGuvenligiPage()))),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.devices_outlined,color:mor),title:const Text('Giriş yapılan cihazlar',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('Son girişleri ve cihaz bilgilerini gör',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GirisGecmisiPage()))),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.support_agent,color:mor),title:const Text('Destek ve hata bildir',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('Açıklama ve ekran görüntüsü gönder',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const DestekPage()))),
      _ayar(context,Icons.download_outlined,'İndirme izinleri','Varsayılan paylaşım indirme ayarı'),
    ],
    const Divider(),
    ListTile(leading:const Icon(Icons.system_update,color:mor),title:const Text('Uygulama güncellemeleri'),subtitle:const Text('V17 • Geliştiriliyor'),trailing:const Icon(Icons.build_circle,color:Colors.orange)),
    ListTile(leading:const Icon(Icons.share,color:mavi),title:const Text('Ngel X’i paylaş'),subtitle:const Text('Uygulama bağlantısını paylaş veya kopyala'),onTap:()async=>SharePlus.instance.share(ShareParams(text:'Ngel X ile dünyanı paylaş ✨'))),
    const Divider(),
    ListTile(leading:const Icon(Icons.logout,color:Colors.red),title:const Text('Çıkış yap',style:TextStyle(color:Colors.red)),onTap:()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const GirisPage()),(_)=>false);})
  ]))));}
  Widget _ayar(BuildContext c,IconData i,String t,String s)=>Card(child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>TercihlerPage(baslik:t))),leading:Icon(i,color:mor),title:Text(t,style:const TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:Text(s,style:const TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87)));
}

class HesapGuvenligiPage extends StatefulWidget {const HesapGuvenligiPage({super.key});@override State<HesapGuvenligiPage> createState()=>_HesapGuvenligiPageState();}
class _HesapGuvenligiPageState extends State<HesapGuvenligiPage>{
  bool yukleniyor=false;
  Future<bool> onay(String baslik,String aciklama,String dugme)async=>await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:Text(baslik),content:Text(aciklama),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),style:FilledButton.styleFrom(backgroundColor:Colors.red),child:Text(dugme))]))??false;
  Future<void> dondur()async{if(!await onay('Hesap dondurulsun mu?','Hesabın geçici olarak kapatılacak. Giriş yaparak hesabını yeniden açabilirsin.','Hesabı dondur'))return;await isle({'deactivated':true,'deactivatedAt':FieldValue.serverTimestamp()});}
  Future<void> silmeTalebi()async{if(!await onay('Hesap silme talebi oluşturulsun mu?','Hesabın hemen kapanacak ve 30 gün sonra kalıcı silinmek üzere işaretlenecek. Bu sürede giriş yaparak talebi iptal edebilirsin.','Silme talebi oluştur'))return;await isle({'deactivated':true,'deletionRequestedAt':FieldValue.serverTimestamp(),'deletionScheduledFor':Timestamp.fromDate(DateTime.now().add(const Duration(days:30)))});}
  Future<void> isle(Map<String,dynamic> veri)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;setState(()=>yukleniyor=true);try{await FirebaseFirestore.instance.collection('users').doc(u.uid).set(veri,SetOptions(merge:true));await FirebaseAuth.instance.signOut();if(mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const GirisPage()),(_)=>false);}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('İşlem tamamlanamadı: $e')));}finally{if(mounted)setState(()=>yukleniyor=false);}}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Hesap güvenliği')),body:SafeArea(child:ListView(padding:const EdgeInsets.all(18),children:[const ListTile(leading:Icon(Icons.verified_user_outlined,color:Colors.green),title:Text('E-posta doğrulaması'),subtitle:Text('Hesabın doğrulanmış e-posta ile korunur.')),const Divider(),ListTile(enabled:!yukleniyor,leading:const Icon(Icons.pause_circle_outline,color:Colors.orange),title:const Text('Hesabı dondur'),subtitle:const Text('Geri dönene kadar profilini geçici olarak gizle'),onTap:dondur),ListTile(enabled:!yukleniyor,leading:const Icon(Icons.delete_forever_outlined,color:Colors.red),title:const Text('Hesap silme talebi',style:TextStyle(color:Colors.red)),subtitle:const Text('30 günlük geri alma süresiyle kapat'),onTap:silmeTalebi),if(yukleniyor)const Padding(padding:EdgeInsets.all(20),child:Center(child:CircularProgressIndicator()))]))));
}

class GirisGecmisiPage extends StatelessWidget {
  const GirisGecmisiPage({super.key});
  @override Widget build(BuildContext context){
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Giriş yapılan cihazlar')),body:uid==null?const Center(child:Text('Oturum bulunamadı.')):FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(uid).get(),builder:(context,s){
      if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());
      final ham=List<dynamic>.from(s.data?.data()?['loginHistory']??const []);
      final kayitlar=ham.whereType<Map>().toList().reversed.take(10).toList();
      if(kayitlar.isEmpty)return const Center(child:Text('Henüz cihaz kaydı yok.'));
      return ListView.separated(padding:const EdgeInsets.all(16),itemCount:kayitlar.length,separatorBuilder:(_,__)=>const Divider(),itemBuilder:(_,i){final k=kayitlar[i],tarih=DateTime.tryParse((k['at']??'').toString())?.toLocal();return ListTile(leading:const CircleAvatar(child:Icon(Icons.phone_android)),title:Text((k['device']??'Android cihaz').toString()),subtitle:Text('${k['platform']??'Android'}${tarih==null?'':' • ${tarih.day.toString().padLeft(2,'0')}/${tarih.month.toString().padLeft(2,'0')}/${tarih.year} ${tarih.hour.toString().padLeft(2,'0')}:${tarih.minute.toString().padLeft(2,'0')}'}'));});
    })));
  }
}

class EngellenenlerPage extends StatefulWidget {const EngellenenlerPage({super.key});@override State<EngellenenlerPage> createState()=>_EngellenenlerPageState();}
class _EngellenenlerPageState extends State<EngellenenlerPage>{
  Future<List<String>> getir()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return[];final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();return List<String>.from(d.data()?['blocked']??const[]);}
  Future<void> kaldir(String uid)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'blocked':FieldValue.arrayRemove([uid])},SetOptions(merge:true));if(mounted)setState((){});}
/* Eski sıkıştırılmış görünüm devre dışı.
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Engellenen hesaplar')),body:FutureBuilder<List<String>>(future:getir(),builder:(context,s){if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());final ids=s.data??[];if(ids.isEmpty)return const Center(child:Text('Engellediğin hesap yok.'));return ListView.separated(padding:const EdgeInsets.all(14),itemCount:ids.length,separatorBuilder:(_,__)=>const Divider(),itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),builder:(_,p){final v=p.data?.data()??{},foto=(v['photoUrl']??'').toString();return ListTile(leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NetworkImage(foto),child:foto.isEmpty?const Icon(Icons.person):null),title:Text((v['displayName']??v['username']??'Ngel X kullanıcısı').toString()),subtitle:Text('@${v['username']??'ngelx'}'),trailing:TextButton(onPressed:()=>kaldir(ids[i]),child:const Text('Engeli kaldır')));});});}));
*/
  @override
  Widget build(BuildContext context) => Theme(
    data: ThemeData.light(),
    child: Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(title: const Text('Engellenen hesaplar')),
      body: FutureBuilder<List<String>>(
        future: getir(),
        builder: (context, s) {
          if (s.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
          final ids = s.data ?? [];
          if (ids.isEmpty) return const Center(child: Text('Engellediğin hesap yok.'));
          return ListView.separated(
            padding: const EdgeInsets.all(14),
            itemCount: ids.length,
            separatorBuilder: (_, __) => const Divider(),
            itemBuilder: (_, i) => FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
              future: FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),
              builder: (_, p) {
                final v = p.data?.data() ?? {};
                final foto = (v['photoUrl'] ?? '').toString();
                return ListTile(
                  leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : NetworkImage(foto), child: foto.isEmpty ? const Icon(Icons.person) : null),
                  title: Text((v['displayName'] ?? v['username'] ?? 'Ngel X kullanıcısı').toString()),
                  subtitle: Text('@${v['username'] ?? 'ngelx'}'),
                  trailing: TextButton(onPressed: () => kaldir(ids[i]), child: const Text('Engeli kaldır')),
                );
              },
            ),
          );
        },
      ),
    ),
  );
}

class DestekPage extends StatefulWidget {const DestekPage({super.key});@override State<DestekPage> createState()=>_DestekPageState();}
class _DestekPageState extends State<DestekPage>{
  final aciklama=TextEditingController();String kategori='Uygulama hatası';XFile? ekran;bool gonderiliyor=false;
  @override void dispose(){aciklama.dispose();super.dispose();}
  Future<void> ekranSec()async{final x=await ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:75,maxWidth:1440);if(x!=null&&mounted)setState(()=>ekran=x);}
  Future<void> gonder()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;if(aciklama.text.trim().length<10){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sorunu en az 10 karakterle açıkla.')));return;}setState(()=>gonderiliyor=true);try{String ekranUrl='';if(ekran!=null){final yol='support/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';await supa.Supabase.instance.client.storage.from('ngelx-media').upload(yol,File(ekran!.path));ekranUrl=supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);}await FirebaseFirestore.instance.collection('support_requests').add({'uid':u.uid,'email':u.email,'category':kategori,'description':aciklama.text.trim(),'screenshotUrl':ekranUrl,'status':'open','createdAt':FieldValue.serverTimestamp()});if(!mounted)return;aciklama.clear();setState(()=>ekran=null);ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Destek talebin gönderildi.')));}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Talep gönderilemedi: $e')));}finally{if(mounted)setState(()=>gonderiliyor=false);}}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none))),child:Scaffold(appBar:AppBar(title:const Text('Destek ve hata bildir')),body:SafeArea(child:ListView(padding:const EdgeInsets.all(20),children:[DropdownButtonFormField<String>(initialValue:kategori,items:['Uygulama hatası','Hesap ve giriş','Güvenlik','Ödeme ve kazanç','Öneri','Diğer'].map((x)=>DropdownMenuItem(value:x,child:Text(x))).toList(),onChanged:(v)=>setState(()=>kategori=v??kategori),decoration:const InputDecoration(labelText:'Konu')),const SizedBox(height:14),TextField(controller:aciklama,minLines:5,maxLines:10,maxLength:1000,decoration:const InputDecoration(labelText:'Sorunu veya isteğini anlat')),const SizedBox(height:12),OutlinedButton.icon(onPressed:gonderiliyor?null:ekranSec,icon:const Icon(Icons.add_photo_alternate_outlined),label:Text(ekran==null?'Ekran görüntüsü ekle':'Ekran görüntüsü seçildi')),const SizedBox(height:20),RenkliButon(yazi:gonderiliyor?'Gönderiliyor...':'Destek talebini gönder',tiklama:gonderiliyor?(){}:gonder)]))));
}

class TercihlerPage extends StatefulWidget {final String baslik;const TercihlerPage({super.key,required this.baslik});@override State<TercihlerPage> createState()=>_TercihlerPageState();}
class _TercihlerPageState extends State<TercihlerPage> {
  bool hesapGizli=false, mesajArkadas=true, hikayeArkadas=true, ekranGoruntusu=false, bildirim=true, mesajBildirimi=true, arkadasBildirimi=true, etkilesimBildirimi=true, indirme=true;
  String? get uid => FirebaseAuth.instance.currentUser?.uid;

  @override
  void initState(){super.initState();yukle();}

  Future<void> yukle() async {
    if(uid==null)return;
    final d=await FirebaseFirestore.instance.collection('users').doc(uid).get(),v=d.data()??{};
    if(mounted)setState((){
      hesapGizli=v['privateAccount']==true;
      mesajArkadas=v['friendsOnlyMessages']!=false;
      hikayeArkadas=v['friendsOnlyStory']!=false;
      ekranGoruntusu=v['allowStoryScreenshot']==true;
      bildirim=v['notificationsEnabled']!=false;
      mesajBildirimi=v['messageNotifications']!=false;
      arkadasBildirimi=v['friendNotifications']!=false;
      etkilesimBildirimi=v['interactionNotifications']!=false;
      indirme=v['defaultAllowDownload']!=false;
    });
  }

  Future<void> kaydet(String k,bool v) async {
    if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));
  }

  Widget satir(String t,String s,bool v,ValueChanged<bool> f,{bool etkin=true})=>SwitchListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:22,vertical:8),
    title:Text(t,style:TextStyle(color:etkin?Colors.black87:Colors.black38,fontWeight:FontWeight.w600)),
    subtitle:Text(s,style:TextStyle(color:etkin?Colors.black54:Colors.black26)),
    value:v,onChanged:etkin?f:null,activeThumbColor:Colors.white,activeTrackColor:mavi,
  );

  List<Widget> get secenekler {
    switch(widget.baslik){
      case 'Gizlilik':
        return [satir('Gizli hesap','Yeni takipçiler onay bekler',hesapGizli,(v){setState(()=>hesapGizli=v);kaydet('privateAccount',v);})];
      case 'Mesaj izinleri':
        return [satir('Yalnızca arkadaşlardan mesaj','Yabancılardan gelen mesajları engelle',mesajArkadas,(v){setState(()=>mesajArkadas=v);kaydet('friendsOnlyMessages',v);})];
      case 'Hikâye gizliliği':
        return [
          satir('Hikâyeyi arkadaşlar görsün','Hikâyeni yalnızca arkadaşlarına göster',hikayeArkadas,(v){setState(()=>hikayeArkadas=v);kaydet('friendsOnlyStory',v);}),
          satir('Hikâyede ekran görüntüsü','İzin verirsen arkadaşların ekran görüntüsü alabilir',ekranGoruntusu,(v){setState(()=>ekranGoruntusu=v);kaydet('allowStoryScreenshot',v);}),
        ];
      case 'Bildirimler':
        return [
          satir('Tüm bildirimler','Uygulama bildirimlerini tek dokunuşla aç veya kapat',bildirim,(v){setState(()=>bildirim=v);kaydet('notificationsEnabled',v);}),
          const Divider(),
          satir('Mesajlar','Yeni mesaj ve fotoğraf bildirimleri',mesajBildirimi,(v){setState(()=>mesajBildirimi=v);kaydet('messageNotifications',v);},etkin:bildirim),
          satir('Arkadaşlık','İstek ve kabul bildirimleri',arkadasBildirimi,(v){setState(()=>arkadasBildirimi=v);kaydet('friendNotifications',v);},etkin:bildirim),
          satir('Beğeni ve yorumlar','Paylaşımlarındaki etkileşimler',etkilesimBildirimi,(v){setState(()=>etkilesimBildirimi=v);kaydet('interactionNotifications',v);},etkin:bildirim),
        ];
      case 'İndirme izinleri':
        return [satir('Varsayılan indirme izni','Yeni paylaşımların indirilebilsin',indirme,(v){setState(()=>indirme=v);kaydet('defaultAllowDownload',v);})];
      default:
        return const [ListTile(leading:Icon(Icons.people,color:mavi),title:Text('Arkadaşlık isteklerini Aktivite ekranından yönet.',style:TextStyle(color:Colors.black87)))];
    }
  }

  @override
  Widget build(BuildContext context)=>Theme(
    data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),dividerColor:const Color(0xFFE5E7EB)),
    child:Scaffold(appBar:AppBar(title:Text(widget.baslik)),body:SafeArea(child:ListView(children:secenekler))),
  );
}

class ArkadaslarPage extends StatelessWidget {const ArkadaslarPage({super.key});@override Widget build(BuildContext context){final uid=FirebaseAuth.instance.currentUser?.uid;return Scaffold(appBar:AppBar(title:const Text('Arkadaşlar')),body:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:uid==null?null:FirebaseFirestore.instance.collection('users').doc(uid).get(),builder:(_,s){final ids=List<String>.from(s.data?.data()?['friends']??[]);if(ids.isEmpty)return const Center(child:Text('Henüz arkadaşın yok.'));return ListView(children:ids.map((id)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(id).get(),builder:(_,u){final v=u.data?.data()??{},foto=(v['photoUrl']??'').toString();return ListTile(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:id))),onLongPress:()async{final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Arkadaşlıktan çıkarılsın mı?'),content:Text('${v['displayName']??v['username']??'Bu kişi'} arkadaşlıktan çıkarılsın mı?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),TextButton(onPressed:()=>Navigator.pop(c,true),child:const Text('ARKADAŞLIKTAN ÇIKAR',style:TextStyle(color:Colors.red,fontWeight:FontWeight.bold)))]));if(ok==true&&uid!=null){await FirebaseFirestore.instance.collection('users').doc(uid).update({'friends':FieldValue.arrayRemove([id])});await FirebaseFirestore.instance.collection('users').doc(id).update({'friends':FieldValue.arrayRemove([uid])});}},leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NetworkImage(foto)),title:Text((v['displayName']??v['username']??'NgelX').toString()),subtitle:Text('@${v['username']??'ngelx'}'),trailing:const Icon(Icons.chevron_right));})).toList());}));}}

class ProfilPage extends StatefulWidget {
  const ProfilPage({super.key});

  @override
  State<ProfilPage> createState() => _ProfilPageState();
}

class _ProfilPageState extends State<ProfilPage> {
  String ad = 'NgelX Kullanıcısı';
  String kullanici = '@ngelx';
  String bio = 'NgelX dünyasına hoş geldin ✦';
  String fotoUrl = '';
  String konum = 'Konum eklenmedi';
  String katilim = 'Yeni katıldı';
  bool yukleniyor = true;
  bool fotoYukleniyor = false;
  int takipSayisi = 0;
  int takipciSayisi = 0;
  int arkadasSayisi = 0;

  User? get aktifKullanici => FirebaseAuth.instance.currentUser;

  @override
  void initState() {
    super.initState();
    profiliGetir();
  }

  Future<void> profiliGetir() async {
    final user = aktifKullanici;
    if (user == null) return;

    try {
      final belge = await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .get();

      final veri = belge.data();

      if (veri != null && mounted) {
        final hamKullanici = (veri['username'] ?? 'ngelx').toString();

        final following = List<dynamic>.from(veri['following'] ?? []);
        final followers = List<dynamic>.from(veri['followers'] ?? []);
        final friends = List<dynamic>.from(veri['friends'] ?? []);
        final tarih = veri['createdAt'] ?? veri['joinedAt'];
        setState(() {
          ad = (veri['displayName'] ?? user.displayName ?? hamKullanici).toString();
          kullanici = '@${hamKullanici.isEmpty ? 'ngelx' : hamKullanici}';
          bio = (veri['bio'] ?? 'NgelX dünyasına hoş geldin ✦').toString();
          fotoUrl = (veri['photoUrl'] ?? '').toString();
          konum = (veri['location'] ?? 'Konum eklenmedi').toString();
          if (tarih is Timestamp) {
            const aylar = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
            final d = tarih.toDate(); katilim = '${aylar[d.month-1]} ${d.year}’te katıldı';
          }
          takipSayisi = following.length;
          takipciSayisi = followers.length;
          arkadasSayisi = friends.length;
          yukleniyor = false;
        });
      } else if (mounted) {
        setState(() {
          ad = user.isAnonymous
              ? 'NgelX Misafir'
              : (user.displayName ?? 'NgelX Kullanıcısı');
          kullanici = user.isAnonymous ? '@misafir' : '@ngelx';
          yukleniyor = false;
        });
      }
    } catch (_) {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  Future<void> fotografYukle() async {
    final user = aktifKullanici;
    if (user == null || user.isAnonymous || fotoYukleniyor) return;
    final dosya = await ImagePicker().pickImage(
      source: ImageSource.gallery,
      imageQuality: 82,
      maxWidth: 1080,
    );
    if (dosya == null || !mounted) return;
    setState(() => fotoYukleniyor = true);
    try {
      final uzanti = dosya.name.contains('.')
          ? dosya.name.split('.').last.toLowerCase()
          : 'jpg';
      final yol = 'profiles/${user.uid}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      await supa.Supabase.instance.client.storage
          .from('ngelx-media')
          .uploadBinary(yol, await dosya.readAsBytes());
      final url = supa.Supabase.instance.client.storage
          .from('ngelx-media')
          .getPublicUrl(yol);
      await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .set({
        'photoUrl': url,
        'updatedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
      if (!mounted) return;
      setState(() => fotoUrl = url);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Profil fotoğrafı kaydedildi.')),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Fotoğraf yüklenemedi: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => fotoYukleniyor = false);
    }
  }

  Future<void> hikayeYukle() async {
    final user = aktifKullanici;
    if (user == null || user.isAnonymous) return;
    final dosya = await ImagePicker().pickImage(source: ImageSource.gallery, imageQuality: 84, maxWidth: 1440);
    if (dosya == null || !mounted) return;
    setState(() => fotoYukleniyor = true);
    try {
      final uzanti = dosya.name.contains('.') ? dosya.name.split('.').last.toLowerCase() : 'jpg';
      final yol = 'stories/${user.uid}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      await supa.Supabase.instance.client.storage.from('ngelx-media').uploadBinary(yol, await dosya.readAsBytes());
      final url = supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(yol);
      await FirebaseFirestore.instance.collection('videos').add({
        'ownerId': user.uid,
        'username': kullanici.replaceFirst('@', ''),
        'type': 'story',
        'mediaUrl': url,
        'createdAt': FieldValue.serverTimestamp(),
        'expiresAt': Timestamp.fromDate(DateTime.now().add(const Duration(hours: 24))),
      });
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hikâyen 24 saat boyunca yayında ✨')));
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Hikâye yüklenemedi: $e')));
    } finally {
      if (mounted) setState(() => fotoYukleniyor = false);
    }
  }

  Future<void> hikayeyiAc() async {
    final user = aktifKullanici;
    if (user == null) return;
    final sonuc = await FirebaseFirestore.instance.collection('videos').where('ownerId', isEqualTo: user.uid).get();
    final simdi = DateTime.now();
    final aktif = sonuc.docs.where((d) {
      final v = d.data();
      final bitis = v['expiresAt'];
      return v['type'] == 'story' && bitis is Timestamp && bitis.toDate().isAfter(simdi);
    }).toList();
    if (!mounted) return;
    if (aktif.isEmpty) {
      await hikayeYukle();
      return;
    }
    final veri = aktif.last.data();
    Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(url:(veri['mediaUrl']??'').toString(),kullanici:kullanici)));
  }

  Future<void> duzenle() async {
    final user = aktifKullanici;

    if (user == null || user.isAnonymous) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Profili kaydetmek için normal hesap oluşturmalısın.'),
        ),
      );
      return;
    }

    final adKontrol = TextEditingController(text: ad);
    final kullaniciKontrol = TextEditingController(
      text: kullanici.replaceFirst('@', ''),
    );
    final bioKontrol = TextEditingController(text: bio);
    final konumKontrol = TextEditingController(text: konum == 'Konum eklenmedi' ? '' : konum);

    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: panel,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(26)),
      ),
      builder: (ctx) {
        bool kaydediliyor = false;

        return StatefulBuilder(
          builder: (ctx, pencereState) {
            return Padding(
              padding: EdgeInsets.fromLTRB(
                20,
                25,
                20,
                MediaQuery.of(ctx).viewInsets.bottom + 25,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Profilini düzenle',
                    style: TextStyle(
                      fontSize: 23,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  TextField(
                    controller: adKontrol,
                    decoration: const InputDecoration(
                      labelText: 'Görünen ad',
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: kullaniciKontrol,
                    decoration: const InputDecoration(
                      prefixText: '@',
                      labelText: 'Kullanıcı adı',
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: bioKontrol,
                    maxLength: 80,
                    decoration: const InputDecoration(
                      labelText: 'Biyografi',
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(controller: konumKontrol, maxLength: 60, decoration: const InputDecoration(labelText: 'Konum', prefixIcon: Icon(Icons.location_on_outlined))),
                  const SizedBox(height: 12),
                  RenkliButon(
                    yazi: kaydediliyor ? 'Kaydediliyor...' : 'Kaydet',
                    tiklama: () async {
                      if (kaydediliyor) return;

                      final yeniAd = adKontrol.text.trim();
                      final yeniKullanici = kullaniciKontrol.text
                          .trim()
                          .replaceAll(' ', '');

                      if (yeniAd.length < 2 || yeniKullanici.length < 3) {
                        ScaffoldMessenger.of(ctx).showSnackBar(
                          const SnackBar(
                            content: Text('Geçerli ad ve kullanıcı adı gir.'),
                          ),
                        );
                        return;
                      }

                      pencereState(() => kaydediliyor = true);

                      await FirebaseFirestore.instance
                          .collection('users')
                          .doc(user.uid)
                          .set({
                        'displayName': yeniAd,
                        'username': yeniKullanici,
                        'bio': bioKontrol.text.trim(),
                        'location': konumKontrol.text.trim(),
                        'email': user.email,
                        'updatedAt': FieldValue.serverTimestamp(),
                      }, SetOptions(merge: true));

                      await user.updateDisplayName(yeniAd);

                      if (!mounted || !ctx.mounted) return;

                      setState(() {
                        ad = yeniAd;
                        kullanici = '@$yeniKullanici';
                        bio = bioKontrol.text.trim();
                        konum = konumKontrol.text.trim().isEmpty ? 'Konum eklenmedi' : konumKontrol.text.trim();
                      });

                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Profil Firebase’e kaydedildi.')),
                      );
                    },
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Future<void> cikisYap() async {
    final onay = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Çıkış yapılsın mı?'),
        content: const Text('Tekrar giriş yapman gerekecek.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Vazgeç'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Çıkış Yap'),
          ),
        ],
      ),
    );

    if (onay != true || !mounted) return;

    await FirebaseAuth.instance.signOut();

    if (!mounted) return;

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const GirisPage()),
      (_) => false,
    );
  }

  Map<String,String> icerikHaritasi(QueryDocumentSnapshot<Map<String,dynamic>> d){final v=d.data();return {'id':d.id,'type':(v['type']??'video').toString(),'videoUrl':(v['videoUrl']??'').toString(),'mediaUrl':(v['mediaUrl']??v['videoUrl']??'').toString(),'audioUrl':(v['audioUrl']??'').toString(),'description':(v['description']??'').toString(),'username':(v['username']??'ngelx').toString(),'ownerId':(v['ownerId']??'').toString(),'allowDownload':(v['allowDownload']??true).toString()};}

  void icerigiAc(QueryDocumentSnapshot<Map<String,dynamic>> d){final item=icerikHaritasi(d),tur=item['type'];Navigator.push(context,MaterialPageRoute(builder:(_)=>Scaffold(body:SafeArea(child:tur=='video'?VideoKarti(adres:item['videoUrl']!,videoId:item['id']!,kullaniciAdi:item['username']!,ownerId:item['ownerId']!,indirilebilir:item['allowDownload']!='false',aktif:true):GorselYaziKarti(veri:item,aktif:true)))));}

  Future<void> icerikMenusu(QueryDocumentSnapshot<Map<String,dynamic>> d) async {await showModalBottomSheet(context:context,backgroundColor:panel,builder:(ctx)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.white24,borderRadius:BorderRadius.circular(8))),ListTile(leading:const Icon(Icons.edit,color:mavi),title:const Text('Açıklamayı düzenle'),onTap:(){Navigator.pop(ctx);icerikDuzenle(d);}),ListTile(leading:const Icon(Icons.push_pin_outlined,color:mor),title:const Text('Profilde sabitle'),onTap:(){d.reference.set({'pinned':true},SetOptions(merge:true));Navigator.pop(ctx);}),ListTile(leading:const Icon(Icons.delete_forever,color:Colors.red),title:const Text('PAYLAŞIMI SİL',style:TextStyle(color:Colors.red,fontWeight:FontWeight.bold)),onTap:(){Navigator.pop(ctx);icerikSil(d);})])));}

  Future<void> icerikDuzenle(QueryDocumentSnapshot<Map<String,dynamic>> d) async {final c=TextEditingController(text:(d.data()['description']??'').toString());final ok=await showDialog<bool>(context:context,builder:(ctx)=>AlertDialog(title:const Text('Paylaşımı düzenle'),content:TextField(controller:c,maxLength:500,maxLines:4),actions:[TextButton(onPressed:()=>Navigator.pop(ctx,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(ctx,true),child:const Text('Kaydet'))]));if(ok==true)await d.reference.update({'description':c.text.trim(),'updatedAt':FieldValue.serverTimestamp()});c.dispose();}

  Future<void> icerikSil(QueryDocumentSnapshot<Map<String,dynamic>> d) async {
    final ok=await showDialog<bool>(context:context,builder:(ctx)=>AlertDialog(title:const Text('Bu paylaşımı silmek istiyor musun?'),content:const Text('Paylaşım profilinden ve akıştan tamamen kaldırılacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(ctx,false),child:const Text('Vazgeç')),TextButton(onPressed:()=>Navigator.pop(ctx,true),child:const Text('Sil',style:TextStyle(color:Colors.red,fontWeight:FontWeight.bold)))]));
    if(ok!=true)return;
    final likes=await d.reference.collection('likes').get();
    final comments=await d.reference.collection('comments').get();
    final batch=FirebaseFirestore.instance.batch();
    for(final x in likes.docs){batch.delete(x.reference);}for(final x in comments.docs){batch.delete(x.reference);}batch.delete(d.reference);await batch.commit();
    final v=d.data();
    for(final raw in [(v['mediaUrl']??'').toString(),(v['videoUrl']??'').toString(),(v['audioUrl']??'').toString()]){if(raw.isEmpty)continue;try{final parts=Uri.parse(raw).pathSegments;final i=parts.indexOf('ngelx-media');if(i>=0&&i+1<parts.length)await supa.Supabase.instance.client.storage.from('ngelx-media').remove([parts.sublist(i+1).join('/')]);}catch(_){}}
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Paylaşım profilinden ve akıştan silindi.')));
  }

  @override
  Widget build(BuildContext context) {
    if (yukleniyor) {
      return const Center(
        child: CircularProgressIndicator(color: mavi),
      );
    }

    return Theme(
      data: ThemeData.light().copyWith(scaffoldBackgroundColor: Colors.white),
      child: ColoredBox(color: Colors.white, child: SafeArea(
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(18, 12, 18, 8),
              child: Column(
                children: [
                  Row(
                    children: [
                      const Text('NgelX', style: TextStyle(color: Colors.black, fontSize: 29, fontWeight: FontWeight.w900)),
                      const Spacer(),
                      IconButton(onPressed:(){},icon:const Icon(Icons.search_rounded,color:Colors.black,size:28)),
                      IconButton(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),icon:const Badge(label:Text('3'),child:Icon(Icons.notifications_none_rounded,color:Colors.black,size:28))),
                      IconButton(tooltip: 'Ayarlar ve gizlilik',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarPage())),icon:const Icon(Icons.settings_outlined,color:Colors.black,size:28)),
                    ],
                  ),
                  const SizedBox(height: 18),
                  GestureDetector(
                    onTap: hikayeyiAc,
                    onLongPress: fotografYukle,
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        Container(
                          width: 126,
                          height: 126,
                          padding: const EdgeInsets.all(4),
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: LinearGradient(colors: [mavi, mor]),
                          ),
                          child: CircleAvatar(
                            backgroundColor: const Color(0xFFF0E8FF),
                            backgroundImage: fotoUrl.isEmpty ? null : NetworkImage(fotoUrl),
                            child: fotoUrl.isNotEmpty
                                ? null
                                : Text(
                                    ad.isEmpty ? 'N' : ad[0].toUpperCase(),
                                    style: const TextStyle(
                                      color: mor,
                                      fontSize: 45,
                                      fontWeight: FontWeight.w900,
                                    ),
                                  ),
                          ),
                        ),
                        if (fotoYukleniyor)
                          const CircularProgressIndicator(color: Colors.white),
                        Positioned(
                          right: 0,
                          bottom: 0,
                          child: GestureDetector(
                            onTap: fotografYukle,
                            child: Container(
                              padding: const EdgeInsets.all(9),
                              decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 10)]),
                              child: const Icon(Icons.photo_camera_rounded, color: Colors.black, size: 20),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    ad,
                    style: const TextStyle(
                      color: Colors.black,
                      fontSize: 23,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  Text(
                    kullanici,
                    style: const TextStyle(color: Colors.black54, fontSize: 15),
                  ),
                  const SizedBox(height: 10),
                  Text(bio, textAlign: TextAlign.center, style: const TextStyle(color: Colors.black87, fontSize: 15)),
                  const SizedBox(height: 8),
                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[const Icon(Icons.location_on_outlined,color:Colors.black54,size:18),const SizedBox(width:4),Flexible(child:Text(konum,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54))),const SizedBox(width:13),const Icon(Icons.calendar_month_outlined,color:Colors.black54,size:18),const SizedBox(width:4),Flexible(child:Text(katilim,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)))]),
                  const SizedBox(height: 18),
                  StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:aktifKullanici!.uid).snapshots(),builder:(_,s){final g=(s.data?.docs??[]).where((d)=>d.data()['type']!='story').length;return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[_beyazIstatistik('$g','Gönderi'),_beyazIstatistik('$takipciSayisi','Takipçi'),_beyazIstatistik('$takipSayisi','Takip')]);}),
                  const SizedBox(height: 17),
                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[SizedBox(width:235,height:50,child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1F2F6),foregroundColor:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:duzenle,icon:const Icon(Icons.edit_outlined),label:Text(aktifKullanici?.isAnonymous==true?'Hesap Oluştur':'Profili Düzenle',style:const TextStyle(fontWeight:FontWeight.w800)))),const SizedBox(width:10),SizedBox(width:52,height:50,child:FilledButton(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1ECFF),foregroundColor:Colors.black,padding:EdgeInsets.zero,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),child:const Icon(Icons.person_add_alt_1)))]),
                  const SizedBox(height: 22),
                  Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_profilKisayol(Icons.bookmark_border_rounded,'Kaydedilenler',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const KaydedilenlerPage()))),_profilKisayol(Icons.history_rounded,'Arşiv'),_profilKisayol(Icons.add_circle_outline_rounded,'Hikâyeler',tiklama:hikayeyiAc),_profilKisayol(Icons.event_outlined,'Etkinlikler'),_profilKisayol(Icons.lock_outline_rounded,'Gizlilik',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Gizlilik')))),_profilKisayol(Icons.settings_outlined,'Ayarlar',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarPage())))]),
                  const SizedBox(height: 20),
                  Container(padding:const EdgeInsets.symmetric(horizontal:16,vertical:13),decoration:BoxDecoration(gradient:const LinearGradient(colors:[Color(0xFFF2E8FF),Color(0xFFF9F4FF)]),borderRadius:BorderRadius.circular(18)),child:const Row(children:[CircleAvatar(backgroundColor:Color(0xFFD9B8FF),child:Icon(Icons.workspace_premium_rounded,color:mor)),SizedBox(width:11),Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('NgelX+',style:TextStyle(color:Colors.black,fontSize:19,fontWeight:FontWeight.w900)),Text('Daha fazla özellik, daha fazla özgürlük',style:TextStyle(color:Colors.black54))])),Icon(Icons.chevron_right,color:Colors.black54)])),
                  const SizedBox(height: 18),
                  SizedBox(height:92,child:ListView(scrollDirection:Axis.horizontal,children:[_oneCikan(Icons.add,'Yeni',hikayeYukle),_oneCikan(Icons.person,'Ben',hikayeyiAc),_oneCikan(Icons.wb_sunny_outlined,'Günlük',hikayeyiAc),_oneCikan(Icons.people_outline,'Dostlar',hikayeyiAc),_oneCikan(Icons.flight_takeoff,'Seyahat',hikayeyiAc),_oneCikan(Icons.restaurant_outlined,'Yemek',hikayeyiAc),_oneCikan(Icons.favorite_border,'Anılar',hikayeyiAc)])),
                  const SizedBox(height: 14),
                  const Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_ProfilSekme('Gönderiler',true),_ProfilSekme('Reels',false),_ProfilSekme('Etiketlenenler',false),_ProfilSekme('Beğenilenler',false)]),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: aktifKullanici == null ? null : FirebaseFirestore.instance.collection('videos').where('ownerId', isEqualTo: aktifKullanici!.uid).snapshots(),
              builder: (_, snap) {
                final paylasimlar = (snap.data?.docs ?? []).where((d) => d.data()['type'] != 'story').toList();
                if (paylasimlar.isEmpty) return const Padding(padding: EdgeInsets.all(35), child: Center(child: Text('Henüz paylaşımın yok. Üret bölümünden ilk içeriğini yayınla ✨', textAlign: TextAlign.center, style: TextStyle(color: Colors.black54))));
                return GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  padding: const EdgeInsets.all(6),
                  itemCount: paylasimlar.length,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6),
                  itemBuilder: (_, i) {
                    final belge = paylasimlar[i];
                    final v = belge.data();
                    final tur = (v['type'] ?? 'video').toString();
                    final url = (v['mediaUrl'] ?? v['videoUrl'] ?? '').toString();
                    return GestureDetector(onTap:()=>icerigiAc(belge),onLongPress:()=>icerikMenusu(belge),child:MedyaOnizleme(
                      tur: tur,
                      url: url,
                      yazi: (v['description'] ?? '').toString(),
                      arkaPlan: i.isEven ? const Color(0xFF28233F) : const Color(0xFF173036),
                    ));
                  },
                );
              },
            ),
          ),
        ],
      ),
    )),
    );
  }

  Widget _beyazIstatistik(String sayi,String baslik)=>Column(children:[Text(sayi,style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)),Text(baslik,style:const TextStyle(color:Colors.black54))]);
  Widget _profilKisayol(IconData ikon,String yazi,{VoidCallback? tiklama})=>InkWell(onTap:tiklama,child:SizedBox(width:55,child:Column(children:[Container(width:48,height:48,decoration:BoxDecoration(color:const Color(0xFFF3F4F7),borderRadius:BorderRadius.circular(15)),child:Icon(ikon,color:Colors.black87)),const SizedBox(height:5),Text(yazi,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w600))])));
  Widget _oneCikan(IconData ikon,String yazi,VoidCallback tiklama)=>Padding(padding:const EdgeInsets.only(right:13),child:InkWell(onTap:tiklama,child:Column(children:[Container(width:62,height:62,decoration:BoxDecoration(color:const Color(0xFFF1F3F7),shape:BoxShape.circle,border:Border.all(color:const Color(0xFFDDE0E7),width:2)),child:Icon(ikon,color:mor)),const SizedBox(height:5),Text(yazi,style:const TextStyle(color:Colors.black87,fontSize:11))])));
}

class _ProfilSekme extends StatelessWidget{final String yazi;final bool secili;const _ProfilSekme(this.yazi,this.secili);@override Widget build(BuildContext context)=>Container(padding:const EdgeInsets.only(bottom:10),decoration:BoxDecoration(border:Border(bottom:BorderSide(color:secili?mavi:Colors.transparent,width:3))),child:Text(yazi,style:TextStyle(color:secili?Colors.black:Colors.black45,fontWeight:FontWeight.w800)));}

class KaydedilenlerPage extends StatelessWidget {
  const KaydedilenlerPage({super.key});
  @override
  Widget build(BuildContext context) {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    return Theme(
      data: ThemeData.light(),
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(title: const Text('Kaydedilenler', style: TextStyle(fontWeight: FontWeight.w900))),
        body: uid == null
            ? const Center(child: Text('Kaydedilenleri görmek için giriş yap.'))
            : StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                stream: FirebaseFirestore.instance.collection('users').doc(uid).collection('saved').orderBy('savedAt', descending: true).snapshots(),
                builder: (_, s) {
                  if (s.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: mor));
                  final docs = s.data?.docs ?? [];
                  if (docs.isEmpty) return const Center(child: Text('Henüz kaydedilen içerik yok'));
                  return GridView.builder(
                    padding: const EdgeInsets.all(8),
                    itemCount: docs.length,
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6),
                    itemBuilder: (_, i) => FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
                      future: FirebaseFirestore.instance.collection('videos').doc((docs[i].data()['contentId'] ?? docs[i].id).toString()).get(),
                      builder: (_, v) {
                        final veri = v.data?.data() ?? {};
                        final tur = (veri['type'] ?? 'text').toString();
                        final url = (veri['mediaUrl'] ?? veri['videoUrl'] ?? '').toString();
                        return GestureDetector(
                          onLongPress: () => docs[i].reference.delete(),
                          child: MedyaOnizleme(tur: tur, url: url, yazi: (veri['description'] ?? '').toString(), arkaPlan: const Color(0xFFF0F1F4)),
                        );
                      },
                    ),
                  );
                },
              ),
      ),
    );
  }
}

class Logo extends StatelessWidget {
  final bool kucuk;

  const Logo({super.key, this.kucuk = false});

  @override
  Widget build(BuildContext context) {
    final boyut = kucuk ? 40.0 : 70.0;
    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: kucuk
          ? MainAxisAlignment.start
          : MainAxisAlignment.center,
      children: [
        SizedBox(
          width: boyut,
          height: boyut,
          child: Stack(clipBehavior: Clip.none, children: [
            Container(decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(kucuk ? 13 : 22),
              gradient: const LinearGradient(begin:Alignment.topLeft,end:Alignment.bottomRight,colors:[Color(0xFF102238),Color(0xFF131027),Color(0xFF21103B)]),
              border: Border.all(color: const Color(0xFF713CFF), width: 1.4),
              boxShadow: const [BoxShadow(color:mavi,blurRadius:18,spreadRadius:-5),BoxShadow(color:mor,blurRadius:20,spreadRadius:-7)],
            )),
            Positioned.fill(child: CustomPaint(painter: const _YorungeCizici())),
            Center(child:Text('N',style:TextStyle(color:Colors.white,fontSize:kucuk?25:44,fontWeight:FontWeight.w900,fontStyle:FontStyle.italic,height:1,shadows:const[Shadow(color:Colors.white54,blurRadius:8)]))),
            Positioned(right:kucuk?-3:-5,top:kucuk?-5:-7,child:Icon(Icons.auto_awesome_rounded,color:Colors.white,size:kucuk?13:20,shadows:const[Shadow(color:mor,blurRadius:10)])),
          ]),
        ),
        const SizedBox(width: 10),
        Row(mainAxisSize:MainAxisSize.min,children:[
          Text('Ngel',style:TextStyle(color:Colors.white,fontSize:kucuk?23:39,fontWeight:FontWeight.w900,letterSpacing:-1,shadows:const[Shadow(color:mor,blurRadius:12)])),
          ShaderMask(shaderCallback:(r)=>const LinearGradient(colors:[mavi,Color(0xFF4D8CFF),mor]).createShader(r),child:Text('X',style:TextStyle(color:Colors.white,fontSize:kucuk?25:42,fontWeight:FontWeight.w900,fontStyle:FontStyle.italic,letterSpacing:-2))),
        ]),
      ],
    );
  }
}

class _YorungeCizici extends CustomPainter {
  const _YorungeCizici();
  @override void paint(Canvas canvas, Size size) {
    final boya=Paint()..style=PaintingStyle.stroke..strokeWidth=size.width*.075..strokeCap=StrokeCap.round..shader=const LinearGradient(colors:[mavi,Color(0xFF4F8BFF),mor]).createShader(Offset.zero&size);
    canvas.save();canvas.translate(size.width/2,size.height/2);canvas.rotate(-.32);canvas.translate(-size.width/2,-size.height/2);
    canvas.drawArc(Rect.fromCenter(center:Offset(size.width/2,size.height*.58),width:size.width*1.18,height:size.height*.42),.18,2.7,false,boya);
    canvas.drawArc(Rect.fromCenter(center:Offset(size.width/2,size.height*.58),width:size.width*1.18,height:size.height*.42),3.45,2.35,false,boya);
    canvas.restore();
  }
  @override bool shouldRepaint(covariant CustomPainter oldDelegate)=>false;
}

class RenkliButon extends StatelessWidget {
  final String yazi;
  final VoidCallback tiklama;

  const RenkliButon({
    super.key,
    required this.yazi,
    required this.tiklama,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: tiklama,
      child: Ink(
        height: 54,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(18),
          gradient: const LinearGradient(
            colors: [mavi, mor],
          ),
        ),
        child: Center(
          child: Text(
            yazi,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}

class Istatistik extends StatelessWidget {
  final String sayi;
  final String yazi;
  final VoidCallback? tiklama;

  const Istatistik(this.sayi, this.yazi, {super.key,this.tiklama});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap:tiklama,child:Column(
      children: [
        Text(
          sayi,
          style: const TextStyle(
            fontSize: 19,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          yazi,
          style: const TextStyle(color: Colors.white54),
        ),
      ],
    ));
  }
}

class BosEkran extends StatelessWidget {
  final IconData ikon;
  final String baslik;
  final String aciklama;

  const BosEkran({
    super.key,
    required this.ikon,
    required this.baslik,
    required this.aciklama,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(ikon, size: 65, color: mavi),
            const SizedBox(height: 18),
            Text(
              baslik,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 7),
            Text(
              aciklama,
              style: const TextStyle(color: Colors.white54),
            ),
          ],
        ),
      ),
    );
  }
}
