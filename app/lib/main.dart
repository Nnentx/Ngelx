import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:supabase_flutter/supabase_flutter.dart' as supa;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:image_picker/image_picker.dart';
import 'package:video_player/video_player.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:share_plus/share_plus.dart';
import 'package:gal/gal.dart';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:file_selector/file_selector.dart';
import 'package:just_audio/just_audio.dart';
import 'package:livekit_client/livekit_client.dart' as lk;
import 'package:device_info_plus/device_info_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:record/record.dart' as rec;

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
const ngelxWebAdresi = 'https://ngelxsocial.com';
const _ngelxMediaApiBuild = String.fromEnvironment('NGELX_MEDIA_API', defaultValue: 'https://ngelx-media.alihancaglar76.workers.dev');
String? _ngelxMediaApiCache;
DateTime? _ngelxMediaApiCacheZamani;

Future<void> ngelxOverlayKapanisiniBekle() async {
  await Future<void>.delayed(const Duration(milliseconds: 360));
}

bool ngelxEskiSupabaseMedya(String url) =>
    url.contains('.supabase.co/storage/v1/object/');

Widget ngelxMedyaHataGorunumu(String url) => Container(
  color: const Color(0xFF09090F),
  alignment: Alignment.center,
  padding: const EdgeInsets.all(28),
  child: Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      const Icon(Icons.cloud_off_rounded, color: Colors.white54, size: 54),
      const SizedBox(height: 12),
      Text(
        ngelxEskiSupabaseMedya(url)
            ? 'Bu eski medya Supabase kotası nedeniyle geçici olarak açılamıyor.'
            : 'Medya şu anda yüklenemedi.',
        textAlign: TextAlign.center,
        style: const TextStyle(color: Colors.white70, fontSize: 15, fontWeight: FontWeight.w700),
      ),
      if (ngelxEskiSupabaseMedya(url)) ...[
        const SizedBox(height: 7),
        const Text(
          'Yeni yüklemeler Cloudflare R2 üzerinden devam ediyor.',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.white38, fontSize: 12),
        ),
      ],
    ],
  ),
);


String _ngelxUzantiTemizle(String value) {
  final v = value.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
  return v.isEmpty ? 'bin' : (v.length > 8 ? v.substring(0, 8) : v);
}

String _ngelxContentType(String ext) {
  switch (_ngelxUzantiTemizle(ext)) {
    case 'jpg':
    case 'jpeg':
      return 'image/jpeg';
    case 'png':
      return 'image/png';
    case 'webp':
      return 'image/webp';
    case 'gif':
      return 'image/gif';
    case 'mp4':
      return 'video/mp4';
    case 'mov':
      return 'video/quicktime';
    case 'mp3':
      return 'audio/mpeg';
    case 'm4a':
      return 'audio/mp4';
    case 'aac':
      return 'audio/aac';
    case 'wav':
      return 'audio/wav';
    case 'ogg':
      return 'audio/ogg';
    default:
      return 'application/octet-stream';
  }
}

Future<String> ngelxMediaApiAdresi() async {
  if (_ngelxMediaApiBuild.trim().isNotEmpty) return _ngelxMediaApiBuild.trim().replaceAll(RegExp(r'/+$'), '');
  final simdi = DateTime.now();
  if (_ngelxMediaApiCache != null &&
      _ngelxMediaApiCacheZamani != null &&
      simdi.difference(_ngelxMediaApiCacheZamani!).inMinutes < 10) {
    return _ngelxMediaApiCache!;
  }
  try {
    final d = await FirebaseFirestore.instance.collection('app_config').doc('media').get().timeout(const Duration(seconds: 5));
    _ngelxMediaApiCache = (d.data()?['uploadApi'] ?? '').toString().trim().replaceAll(RegExp(r'/+$'), '');
  } catch (_) {
    _ngelxMediaApiCache ??= '';
  }
  _ngelxMediaApiCacheZamani = simdi;
  return _ngelxMediaApiCache ?? '';
}

Future<String> ngelxMedyaYukleBytes({
  required Uint8List bytes,
  required String kind,
  required String ext,
  required String legacyPath,
  String? contentType,
}) async {
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) throw Exception('Medya yüklemek için giriş yapmalısın.');
  final api = await ngelxMediaApiAdresi();
  final temizExt = _ngelxUzantiTemizle(ext);
  final tur = contentType ?? _ngelxContentType(temizExt);

  if (api.isNotEmpty) {
    final uri = Uri.parse('$api/upload').replace(queryParameters: {'kind': kind, 'ext': temizExt});
    Object? sonHata;
    for (var deneme = 0; deneme < 3; deneme++) {
      final istemci = HttpClient()..connectionTimeout = const Duration(seconds: 12);
      try {
        final token = await user.getIdToken(deneme > 0);
        if (token == null || token.isEmpty) throw Exception('Güvenli medya oturumu oluşturulamadı.');
        final istek = await istemci.postUrl(uri).timeout(const Duration(seconds: 15));
        istek.persistentConnection = false;
        istek.headers.set(HttpHeaders.authorizationHeader, 'Bearer $token');
        istek.headers.set(HttpHeaders.contentTypeHeader, tur);
        istek.headers.set('X-NgelX-Client', 'android-v53');
        istek.contentLength = bytes.length;
        istek.add(bytes);
        final cevap = await istek.close().timeout(const Duration(seconds: 35));
        final govde = await utf8.decoder.bind(cevap).join().timeout(const Duration(seconds: 15));
        if (cevap.statusCode >= 200 && cevap.statusCode < 300) {
          final veri = govde.isEmpty ? const <String,dynamic>{} : jsonDecode(govde);
          final url = veri is Map ? (veri['url'] ?? '').toString() : '';
          if (url.isEmpty) throw Exception('Medya sunucusu geçerli URL döndürmedi.');
          return url;
        }
        sonHata = HttpException('Medya sunucusu HTTP ${cevap.statusCode}: $govde', uri: uri);
        if (cevap.statusCode < 500 && cevap.statusCode != 408 && cevap.statusCode != 429 && cevap.statusCode != 401) {
          throw sonHata;
        }
      } on SocketException catch (e) {
        sonHata = e;
      } on TimeoutException catch (e) {
        sonHata = e;
      } on HttpException catch (e) {
        sonHata = e;
      } catch (e) {
        sonHata = e;
        if (deneme >= 2) rethrow;
      } finally {
        istemci.close(force: true);
      }
      if (deneme < 2) {
        await Future<void>.delayed(Duration(milliseconds: deneme == 0 ? 700 : 1600));
      }
    }
    throw Exception('Medya sunucusuna bağlanılamadı. Bağlantı otomatik olarak 3 kez denendi. ${sonHata ?? ''}');
  }

  await supa.Supabase.instance.client.storage
      .from('ngelx-media')
      .uploadBinary(
        legacyPath,
        bytes,
        fileOptions: supa.FileOptions(contentType: tur),
      )
      .timeout(const Duration(seconds: 25));
  return supa.Supabase.instance.client.storage.from('ngelx-media').getPublicUrl(legacyPath);
}

Future<void> ngelxMedyaSil(String rawUrl) async {
  if (rawUrl.trim().isEmpty) return;
  final api = await ngelxMediaApiAdresi();
  if (api.isNotEmpty && rawUrl.startsWith('$api/media/')) {
    try {
      final user = FirebaseAuth.instance.currentUser;
      final token = await user?.getIdToken();
      if (token == null || token.isEmpty) return;
      final uri = Uri.parse(rawUrl);
      final key = Uri.decodeComponent(uri.path.substring('/media/'.length));
      await Dio().delete(
        '$api/object',
        queryParameters: {'key': key},
        options: Options(headers: {'Authorization': 'Bearer $token'}, sendTimeout: const Duration(seconds: 12), receiveTimeout: const Duration(seconds: 12)),
      );
      return;
    } catch (_) {
      return;
    }
  }
  try {
    final parts = Uri.parse(rawUrl).pathSegments;
    final i = parts.indexOf('ngelx-media');
    if (i >= 0 && i + 1 < parts.length) {
      await supa.Supabase.instance.client.storage.from('ngelx-media').remove([parts.sublist(i + 1).join('/')]);
    }
  } catch (_) {}
}

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
  if(List<String>.from(ayar['restrictedUsers']??const[]).contains(fromUid))return;
  if(ayar['notificationsEnabled']==false)return;
  if(tur=='message'&&ayar['messageNotifications']==false)return;
  if(tur=='interaction'&&ayar['interactionNotifications']==false)return;
  if(tur=='friend'&&ayar['friendNotifications']==false)return;
  if(tur=='message'&&belgeId!=null&&List<String>.from(ayar['mutedChats']??const[]).contains(belgeId)){
    final ham=(ayar['mutedChatUntil'] is Map)?(ayar['mutedChatUntil'] as Map)[belgeId]:null;
    final bitis=DateTime.tryParse((ham??'').toString());
    if(bitis==null||bitis.isAfter(DateTime.now().toUtc()))return;
  }
  final gonderen=await FirebaseFirestore.instance.collection('users').doc(fromUid).get();
  final gonderenVeri=gonderen.data()??{};
  final gonderenAdi=(gonderenVeri['displayName']??gonderenVeri['username']??'NgelX kullanıcısı').toString();
  final gonderenFoto=(gonderenVeri['photoUrl']??'').toString();
  await FirebaseFirestore.instance.collection('notifications').add({
    'toUid':toUid,'fromUid':fromUid,'type':tur,
    'senderName':gonderenAdi,'photoUrl':gonderenFoto,
    'text':'$gonderenAdi $metin',
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

Future<void> tepkiMenusu(BuildContext context,String icerikId) async {
  final user=FirebaseAuth.instance.currentUser;
  if(user==null||user.isAnonymous||icerikId.isEmpty){await misafirEngeli(context);return;}
  final tepki=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),builder:(c)=>SafeArea(child:Padding(padding:const EdgeInsets.symmetric(horizontal:16,vertical:22),child:Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:['❤️','👍','😂','😮','😢','😡'].map((e)=>InkWell(onTap:()=>Navigator.pop(c,e),borderRadius:BorderRadius.circular(30),child:Padding(padding:const EdgeInsets.all(7),child:Text(e,style:const TextStyle(fontSize:29))))).toList()))));
  if(tepki==null)return;
  try{
    await FirebaseFirestore.instance.collection('videos').doc(icerikId).collection('likes').doc(user.uid).set({'userId':user.uid,'reaction':tepki,'createdAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('$tepki tepkin kaydedildi.')));
  }catch(e){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Tepki kaydedilemedi: $e')));}
}

Future<void> icerikAracMenusu(BuildContext context,String icerikId,{Future<void> Function(double)? hizDegistir,double mevcutHiz=1.0})async{
  if(icerikId.isEmpty)return;
  final belge=await FirebaseFirestore.instance.collection('videos').doc(icerikId).get();
  final hafiza=await SharedPreferences.getInstance(),altyaziVar=(belge.data()?['captionText']??belge.data()?['captions']??'').toString().trim().isNotEmpty;
  bool altyazi=hafiza.getBool('content_caption_$icerikId')??false;
  String icerikDili=hafiza.getString('content_language_$icerikId')??uygulamaDili.value;
  if(!context.mounted)return;
  await showModalBottomSheet(context:context,backgroundColor:Colors.white,shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),builder:(c)=>StatefulBuilder(builder:(c,setPencere)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
    Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.black26,borderRadius:BorderRadius.circular(8))),
    const Text('İçerik araçları',style:TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),
    ListTile(leading:const Icon(Icons.translate_rounded,color:mor),title:const Text('Dil ve çeviri',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text('Bu içerik için: ${dilAdlari[icerikDili]}',style:const TextStyle(color:Colors.black54)),onTap:()async{final sec=await showDialog<String>(context:c,builder:(d)=>Theme(data:ThemeData.light(),child:SimpleDialog(backgroundColor:Colors.white,title:const Text('İçerik dili',style:TextStyle(color:Colors.black87)),children:dilAdlari.entries.map((e)=>SimpleDialogOption(onPressed:()=>Navigator.pop(d,e.key),child:Row(children:[if(e.key==icerikDili)const Icon(Icons.check,color:mor),if(e.key==icerikDili)const SizedBox(width:8),Text(e.value,style:const TextStyle(color:Colors.black87))]))).toList())));if(sec!=null){await hafiza.setString('content_language_$icerikId',sec);setPencere(()=>icerikDili=sec);}}),
    SwitchListTile(secondary:const Icon(Icons.closed_caption_rounded,color:Colors.blue),title:const Text('Altyazı',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text(altyaziVar?'Konuşmaları yazı olarak göster':'Bu içerik için altyazı henüz yok',style:const TextStyle(color:Colors.black54)),value:altyazi&&altyaziVar,onChanged:altyaziVar?(v)async{await hafiza.setBool('content_caption_$icerikId',v);setPencere(()=>altyazi=v);}:null),
    if(hizDegistir!=null)ListTile(
      leading:const Icon(Icons.speed_rounded,color:Colors.orange),
      title:const Text('Oynatma hızı',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
      subtitle:Wrap(spacing:7,children:[.5,1.0,1.5,2.0].map((x){
        final secili=(x-mevcutHiz).abs()<.01;
        return ChoiceChip(
          label:Text('${x}x'),
          selected:secili,
          selectedColor:mor,
          backgroundColor:const Color(0xFFF1F2F5),
          side:BorderSide.none,
          labelStyle:TextStyle(color:secili?Colors.white:Colors.black87,fontWeight:FontWeight.w800),
          onSelected:(_)async{await hizDegistir(x);if(c.mounted)Navigator.pop(c);},
        );
      }).toList()),
    ),
    ListTile(leading:const Icon(Icons.info_outline_rounded,color:Colors.black54),title:const Text('İçerik bilgileri',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),subtitle:Text('İçerik kimliği: $icerikId',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black45))),
    ListTile(leading:const Icon(Icons.flag_outlined,color:Colors.redAccent),title:const Text('Bildir / Şikâyet et',style:TextStyle(color:Colors.redAccent,fontWeight:FontWeight.w700)),onTap:(){Navigator.pop(c);sikayetEt(context,hedefTuru:'paylasim',hedefId:icerikId,hedefUid:'');}),
  ]))));
}

Future<String> cihazKurulumKimligi()async{
  final hafiza=await SharedPreferences.getInstance();
  var id=hafiza.getString('ngelx_device_install_id');
  if(id==null||id.isEmpty){
    id='d'+DateTime.now().microsecondsSinceEpoch.toString()+'_'+Object().hashCode.toString();
    await hafiza.setString('ngelx_device_install_id',id);
  }
  return id;
}

Future<void> girisKaydiEkle(User user) async {
  try {
    final bilgi=await DeviceInfoPlugin().androidInfo;
    final cihaz='${bilgi.manufacturer} ${bilgi.model}'.trim();
    final deviceId=await cihazKurulumKimligi();
    final onceki=await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    final oncekiCihaz=(onceki.data()?['lastLoginDevice']??'').toString();
    await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
      'lastLoginAt':FieldValue.serverTimestamp(),
      'lastLoginDevice':cihaz,
      'lastLoginDeviceId':deviceId,
      'revokedDeviceIds':FieldValue.arrayRemove([deviceId]),
      'loginHistory':FieldValue.arrayUnion([{
        'deviceId':deviceId,
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
  final neden=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[const ListTile(title:Text('Şikâyet nedenini seç',style:TextStyle(color:Colors.black,fontWeight:FontWeight.bold))),for(final n in ['Spam veya yanıltıcı','Taciz veya zorbalık','Nefret söylemi','Çıplaklık veya cinsel içerik','Şiddet veya tehlikeli davranış','Başkasını taklit ediyor'])ListTile(title:Text(n,style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,n)),const SizedBox(height:12)]))));
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
      home: StreamBuilder<User?>(
        stream:FirebaseAuth.instance.authStateChanges(),
        initialData:FirebaseAuth.instance.currentUser,
        builder:(_,auth)=>UygulamaDurumKapisi(
          child:auth.data==null
            ? GirisPage(key:ValueKey('giris_$dil'))
            : AnaEkran(key:ValueKey('ana_$dil')),
        ),
      ),
      onGenerateRoute:(settings){
        final uri=Uri.tryParse(settings.name??'');
        if(uri!=null){
          if(uri.pathSegments.length>=2&&uri.pathSegments.first=='p')return MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:uri.pathSegments[1]));
          if(uri.pathSegments.length>=2&&uri.pathSegments.first=='u')return MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uri.pathSegments[1]));
          if(uri.host=='p'&&uri.pathSegments.isNotEmpty)return MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:uri.pathSegments.first));
          if(uri.host=='u'&&uri.pathSegments.isNotEmpty)return MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uri.pathSegments.first));
        }
        return null;
      },
      builder: (context, child) => Directionality(textDirection: dil=='ar' ? TextDirection.rtl : TextDirection.ltr, child: child!),
    ));
  }
}

class IcerikBaglantiPage extends StatelessWidget {
  final String icerikId;
  const IcerikBaglantiPage({super.key,required this.icerikId});
  @override Widget build(BuildContext context)=>Scaffold(backgroundColor:const Color(0xFF09090F),appBar:AppBar(title:const Text('NgelX paylaşımı')),body:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('videos').doc(icerikId).get(),builder:(_,s){if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mavi));if(s.hasError)return Center(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.cloud_off_rounded,size:55,color:Colors.redAccent),const SizedBox(height:12),const Text('İçerik yüklenemedi.'),TextButton(onPressed:()=>Navigator.pop(context),child:const Text('Akışa dön'))])));if(s.data?.exists!=true)return const Center(child:Text('Bu paylaşım kaldırılmış veya artık kullanılamıyor.'));final v={'id':icerikId,...?s.data?.data()};final tur=(v['type']??'video').toString();return tur=='video'?VideoKarti(adres:(v['videoUrl']??v['mediaUrl']??'').toString(),videoId:icerikId,kullaniciAdi:(v['username']??'ngelx').toString(),ownerId:(v['ownerId']??'').toString(),indirilebilir:v['allowDownload']!=false,aktif:true):GorselYaziKarti(veri:v.map((k,e)=>MapEntry(k,e?.toString()??'')),aktif:true); }));
}

class UygulamaDurumKapisi extends StatefulWidget {final Widget child;const UygulamaDurumKapisi({super.key,required this.child});@override State<UygulamaDurumKapisi> createState()=>_UygulamaDurumKapisiState();}
class _UygulamaDurumKapisiState extends State<UygulamaDurumKapisi> with WidgetsBindingObserver{
  late Future<DocumentSnapshot<Map<String,dynamic>>> durum;
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);yenile();unawaited(_presence(true));unawaited(_uzakCikisKontrol());}
  @override void dispose(){WidgetsBinding.instance.removeObserver(this);unawaited(_presence(false));super.dispose();}
  void yenile()=>durum=FirebaseFirestore.instance.collection('app_config').doc('status').get().timeout(const Duration(seconds:8));
  Future<void> _uzakCikisKontrol()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null||u.isAnonymous)return;
    try{
      final id=await cihazKurulumKimligi();
      final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();
      final iptal=List<String>.from(d.data()?['revokedDeviceIds']??const[]);
      if(iptal.contains(id))await FirebaseAuth.instance.signOut();
    }catch(_){}
  }
  Future<void> _presence(bool online)async{
    final u=FirebaseAuth.instance.currentUser;if(u==null||u.isAnonymous)return;
    try{await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'isOnline':online,'lastSeenAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}catch(_){}
  }
  @override void didChangeAppLifecycleState(AppLifecycleState state){
    if(state==AppLifecycleState.resumed){unawaited(_presence(true));unawaited(_uzakCikisKontrol());}
    if(state==AppLifecycleState.inactive||state==AppLifecycleState.paused||state==AppLifecycleState.detached||state==AppLifecycleState.hidden)unawaited(_presence(false));
  }
  @override Widget build(BuildContext context)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
    future:durum,
    builder:(context,s){
      if(s.connectionState==ConnectionState.waiting)return const Scaffold(backgroundColor:Colors.white,body:Center(child:CircularProgressIndicator()));
      if(s.hasError)return widget.child;
      final v=s.data?.data()??{};
      if(v['maintenance']!=true)return widget.child;
      return Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,body:SafeArea(child:Center(child:Padding(padding:const EdgeInsets.all(30),child:Column(mainAxisSize:MainAxisSize.min,children:[
        const Icon(Icons.engineering_outlined,size:88,color:mor),const SizedBox(height:20),
        const Text('Kısa bir bakımdayız',style:TextStyle(fontSize:28,fontWeight:FontWeight.w900)),const SizedBox(height:12),
        Text((v['message']??'Ngel X’i daha iyi hale getiriyoruz. Biraz sonra tekrar dene.').toString(),textAlign:TextAlign.center,style:const TextStyle(fontSize:16,color:Colors.black54)),const SizedBox(height:24),
        FilledButton.icon(onPressed:()=>setState(yenile),icon:const Icon(Icons.refresh),label:const Text('Tekrar dene')),
      ]))))));
    },
  );
}

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

  Future<void> _girisArkaPlanIsleri({
    required User user,
    required SharedPreferences hafiza,
    required String denemeAnahtari,
    required String kilitAnahtari,
    required String adres,
    required String parola,
    required bool hatirla,
  }) async {
    try{
      await hafiza.remove(denemeAnahtari);
      await hafiza.remove(kilitAnahtari);
      if(hatirla){
        kayitliEpostalar.removeWhere((e)=>e.toLowerCase()==adres.toLowerCase());
        kayitliEpostalar.insert(0,adres);
        if(kayitliEpostalar.length>8)kayitliEpostalar=kayitliEpostalar.take(8).toList();
        await hafiza.setString('hatirlanan_eposta',adres);
        await hafiza.setStringList('hatirlanan_epostalar',kayitliEpostalar);
        await guvenliHafiza.write(key:sifreAnahtari(adres),value:parola);
      }else{
        await hafiza.remove('hatirlanan_eposta');
        await guvenliHafiza.delete(key:'hatirlanan_sifre');
      }
    }catch(_){}
    unawaited(girisKaydiEkle(user));
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
      final profilGelecek=FirebaseFirestore.instance.collection('users').doc(sonuc.user!.uid).get();
      await sonuc.user?.reload();
      if (FirebaseAuth.instance.currentUser?.emailVerified != true) {
        await FirebaseAuth.instance.currentUser?.sendEmailVerification();
        await FirebaseAuth.instance.signOut();
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('E-posta adresin henüz doğrulanmamış. Yeni doğrulama bağlantısı gönderildi; gelen kutunu kontrol et.')));
        return;
      }
      final profilBelgesi=await profilGelecek;
      final profilVerisi=profilBelgesi.data()??{};
      if(profilVerisi['deactivated']==true&&mounted){
        final silmeTalebi=profilVerisi['deletionRequestedAt']!=null;
        final yenidenAc=await showDialog<bool>(context:context,barrierDismissible:false,builder:(c)=>AlertDialog(title:Text(silmeTalebi?'Hesap silme talebi var':'Hesap dondurulmuş'),content:Text(silmeTalebi?'Hesabın 30 günlük silme sürecinde. Şimdi geri açmak ister misin?':'Hesabını yeniden etkinleştirmek ister misin?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Hesabı geri aç'))]));
        if(yenidenAc!=true){await FirebaseAuth.instance.signOut();return;}
        await FirebaseFirestore.instance.collection('users').doc(sonuc.user!.uid).set({'deactivated':false,'deletionRequestedAt':FieldValue.delete(),'deletionScheduledFor':FieldValue.delete()},SetOptions(merge:true));
      }
      final aktifKullanici=FirebaseAuth.instance.currentUser!;
      final adres=email.text.trim();
      final parola=sifre.text;
      final hatirla=beniHatirla;
      unawaited(_girisArkaPlanIsleri(
        user:aktifKullanici,
        hafiza:hafiza,
        denemeAnahtari:denemeAnahtari,
        kilitAnahtari:kilitAnahtari,
        adres:adres,
        parola:parola,
        hatirla:hatirla,
      ));
      if (!mounted) return;
      setState(()=>yukleniyor=false);
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
              const SizedBox(height: 40),
              const _NgelXRenkliBaslik(),
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

class _NgelXRenkliBaslik extends StatelessWidget {
  const _NgelXRenkliBaslik();

  @override
  Widget build(BuildContext context) {
    final dil = uygulamaDili.value.toLowerCase();
    const parcalar = <String, List<String>>{
      'tr': ['Tekrar', 'hoş geldin'],
      'en': ['Welcome', 'back'],
      'de': ['Willkommen', 'zurück'],
      'ar': ['مرحباً', 'بعودتك'],
      'ru': ['С', 'возвращением'],
    };
    final secili = parcalar[dil] ?? parcalar['tr']!;
    final rtl = dil == 'ar';

    return Align(
      alignment: rtl ? Alignment.centerRight : Alignment.centerLeft,
      child: FittedBox(
        fit: BoxFit.scaleDown,
        alignment: rtl ? Alignment.centerRight : Alignment.centerLeft,
        child: Directionality(
          textDirection: rtl ? TextDirection.rtl : TextDirection.ltr,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                secili[0],
                style: const TextStyle(
                  fontSize: 34,
                  fontWeight: FontWeight.w900,
                  color: Color(0xFF07142E),
                  height: 1.05,
                  letterSpacing: -1.1,
                ),
              ),
              const SizedBox(width: 8),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  ShaderMask(
                    blendMode: BlendMode.srcIn,
                    shaderCallback: (bounds) => const LinearGradient(
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                      colors: [
                        Color(0xFF079BF6),
                        Color(0xFF1767F7),
                        Color(0xFF7A45F4),
                      ],
                    ).createShader(bounds),
                    child: Text(
                      secili[1],
                      style: const TextStyle(
                        fontSize: 34,
                        fontWeight: FontWeight.w900,
                        color: Colors.white,
                        height: 1.05,
                        letterSpacing: -1.1,
                      ),
                    ),
                  ),
                  const SizedBox(height: 3),
                  Container(
                    width: 62,
                    height: 4,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      gradient: const LinearGradient(
                        colors: [Color(0xFF5FE0EC), Color(0xFF9B72F7)],
                      ),
                    ),
                  ),
                ],
              ),
            ],
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
  String? acilanAramaId;

  Widget gelenAramaKatmani(){
    final ben=FirebaseAuth.instance.currentUser?.uid;
    if(ben==null||FirebaseAuth.instance.currentUser?.isAnonymous==true)return const SizedBox.shrink();
    return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(60).snapshots(),
      builder:(context,s){
        final adaylar=(s.data?.docs??[]).where((d){
          final v=d.data();
          if((v['callStartedBy']??'').toString()==ben||v['callStatus']!='ringing')return false;
          final t=v['callCreatedAt'];
          if(t is Timestamp&&DateTime.now().difference(t.toDate()).inMinutes>3)return false;
          return (v['callRoomName']??'').toString().isNotEmpty;
        }).toList()
          ..sort((a,b){
            final at=a.data()['callCreatedAt'],bt=b.data()['callCreatedAt'];
            final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
            return bm.compareTo(am);
          });
        if(adaylar.isEmpty)return const SizedBox.shrink();
        final d=adaylar.first,v=d.data(),from=(v['callStartedBy']??'').toString(),grup=v['isGroup']==true,goruntulu=v['callVideo']==true;
        return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          future:grup||from.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(from).get(),
          builder:(_,u){
            final p=u.data?.data()??<String,dynamic>{};
            final baslik=grup?(v['callTitle']??v['groupName']??'Grup araması').toString():(p['displayName']??p['username']??'NgelX kullanıcısı').toString();
            final foto=grup?(v['groupPhotoUrl']??'').toString():(p['photoUrl']??'').toString();
            return SafeArea(
              child:Align(
                alignment:Alignment.topCenter,
                child:Container(
                  margin:const EdgeInsets.fromLTRB(12,10,12,0),
                  padding:const EdgeInsets.all(12),
                  decoration:BoxDecoration(
                    color:Colors.white,
                    borderRadius:BorderRadius.circular(22),
                    boxShadow:const [BoxShadow(color:Color(0x33000000),blurRadius:24,offset:Offset(0,8))],
                  ),
                  child:Row(children:[
                    CircleAvatar(
                      radius:24,
                      backgroundColor:const Color(0xFFE9DDFF),
                      backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),
                      child:foto.isEmpty?Icon(grup?Icons.groups:Icons.person,color:mor):null,
                    ),
                    const SizedBox(width:11),
                    Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
                      Text(baslik,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black,fontWeight:FontWeight.w900,fontSize:16)),
                      Text(goruntulu?'Gelen görüntülü arama':'Gelen sesli arama',style:const TextStyle(color:Colors.black54,fontSize:12)),
                    ])),
                    IconButton.filled(
                      style:IconButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),
                      tooltip:'Reddet',
                      onPressed:()async{
                        await d.reference.set({'callStatus':'rejected','callEndedBy':ben,'callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
                        final mesajId=(v['callMessageId']??'').toString();
                        if(mesajId.isNotEmpty){
                          unawaited(d.reference.collection('messages').doc(mesajId).set({'callStatus':'rejected','callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).catchError((_){ }));
                        }
                      },
                      icon:const Icon(Icons.call_end_rounded),
                    ),
                    const SizedBox(width:8),
                    IconButton.filled(
                      style:IconButton.styleFrom(backgroundColor:Colors.green,foregroundColor:Colors.white),
                      tooltip:'Cevapla',
                      onPressed:()async{
                        if(acilanAramaId==d.id)return;
                        setState(()=>acilanAramaId=d.id);
                        try{
                          await d.reference.set({'callStatus':'active','callParticipants':FieldValue.arrayUnion([ben]),'callAnsweredAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
                          final mesajId=(v['callMessageId']??'').toString();
                          if(mesajId.isNotEmpty){
                            unawaited(d.reference.collection('messages').doc(mesajId).set({'callStatus':'active','callAnsweredAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).catchError((_){ }));
                          }
                          if(!context.mounted)return;
                          await Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXAramaPage(
                            roomName:(v['callRoomName']??'').toString(),
                            baslik:baslik,
                            foto:foto,
                            goruntulu:goruntulu,
                            aramaRef:d.reference,
                          )));
                        }finally{
                          if(mounted)setState(()=>acilanAramaId=null);
                        }
                      },
                      icon:Icon(goruntulu?Icons.videocam_rounded:Icons.call_rounded),
                    ),
                  ]),
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _aktifSayfa() {
    switch (secili) {
      case 0: return const VideoAkisi(gorunur: true);
      case 1: return const KesfetPage(gorunur: true);
      case 2: return const YuklePage();
      case 3: return const MesajPage();
      case 4: return const ProfilPage();
      default: return const VideoAkisi(gorunur: true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body:Stack(children:[
        Positioned.fill(child:KeyedSubtree(key:ValueKey('ngelx_tab_$secili'),child:_aktifSayfa())),
        Positioned.fill(child:IgnorePointer(
          ignoring:false,
          child:gelenAramaKatmani(),
        )),
      ]),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          border: Border(top: BorderSide(color: Color(0xFFE7E9EE))),
          boxShadow: [BoxShadow(color: Color(0x1A000000), blurRadius: 18)],
        ),
        child: NavigationBarTheme(
          data:NavigationBarThemeData(
            height:76,
            backgroundColor:Colors.white,
            indicatorColor:const Color(0xFFE9DDFF),
            indicatorShape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
            labelTextStyle:WidgetStateProperty.resolveWith((s)=>TextStyle(color:s.contains(WidgetState.selected)?mor:Colors.black54,fontSize:11,fontWeight:s.contains(WidgetState.selected)?FontWeight.w900:FontWeight.w600)),
            iconTheme:WidgetStateProperty.resolveWith((s)=>IconThemeData(color:s.contains(WidgetState.selected)?mor:Colors.black54,size:s.contains(WidgetState.selected)?28:25)),
          ),
          child:NavigationBar(
          height: 76,
          selectedIndex: secili,
          backgroundColor: Colors.transparent,
          labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
          onDestinationSelected: (i) async {
            if (i != 0 && await misafirEngeli(context)) return;
            if (mounted) setState(() => secili = i);
          },
          destinations: [
            NavigationDestination(icon: const Icon(Icons.play_circle_outline), selectedIcon: const Icon(Icons.play_circle_fill), label: t('flow')),
            NavigationDestination(icon: const Icon(Icons.explore_outlined), selectedIcon: const Icon(Icons.explore), label: t('explore')),
            NavigationDestination(icon: const Icon(Icons.add_box_outlined, size: 30), selectedIcon: const Icon(Icons.add_box, size: 32), label: t('create')),
            NavigationDestination(icon: const Badge(child: Icon(Icons.forum_outlined)), selectedIcon: const Icon(Icons.forum), label: t('chat')),
            NavigationDestination(icon: const Icon(Icons.person_outline), selectedIcon: const Icon(Icons.person), label: t('me')),
          ],
        ),
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
  final PageController akisKontrol = PageController();
  int aktif = 0;
  bool takipSekmesi = false;
  Set<String> takipEdilenler = {};
  Set<String> arkadaslar = {};
  Set<String> engellenenler = {};
  Set<String> gizlenenIcerikler = {};

  @override
  void initState() {
    super.initState();
    takipListesiniGetir();
  }

  @override
  void dispose() {
    akisKontrol.dispose();
    super.dispose();
  }

  Future<void> takipListesiniGetir() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;
    final d = await FirebaseFirestore.instance.collection('users').doc(uid).get();
    if (!mounted) return;
    setState(() {
      takipEdilenler = Set<String>.from(List<dynamic>.from(d.data()?['following'] ?? []));
      arkadaslar = Set<String>.from(List<dynamic>.from(d.data()?['friends'] ?? []));
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
            final yuklenenler = (snapshot.data?.docs ?? []).map<Map<String,dynamic>>((belge) {
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
                'privacy':(veri['privacy']??'Herkes').toString(),
                'visibleTo':List<String>.from(veri['visibleTo']??const[]),
                'hiddenFor':List<String>.from(veri['hiddenFor']??const[]),
              };
            }).where((v){
              final me=FirebaseAuth.instance.currentUser?.uid,owner=v['ownerId']?.toString()??'',privacy=v['privacy']?.toString()??'Herkes';
              if(v['type']=='story'||engellenenler.contains(owner)||gizlenenIcerikler.contains(v['id']))return false;
              if(me!=null&&(v['hiddenFor'] as List<String>).contains(me))return false;
              if(me==owner)return true;
              if(privacy=='Yalnızca ben')return false;
              if(privacy=='Arkadaşlar')return me!=null&&arkadaslar.contains(owner);
              if(privacy=='Yakın arkadaşlar')return me!=null&&(v['visibleTo'] as List<String>).contains(me);
              return true;
            }).toList();
            final filtreli = takipSekmesi ? yuklenenler.where((v) => takipEdilenler.contains(v['ownerId'])).toList() : yuklenenler;
            final videolar = takipSekmesi ? filtreli : <Map<String,dynamic>>[...filtreli, ...ornekVideolar.map((e)=>Map<String,dynamic>.from(e))];
            if (videolar.isEmpty) return const Center(child: Padding(padding: EdgeInsets.all(30), child: Text('Takip ettiğin kişilerin paylaşımları burada görünecek.', textAlign: TextAlign.center)));
            return GestureDetector(
    behavior: HitTestBehavior.translucent,
    onHorizontalDragEnd: (detay) {
      final hiz = detay.primaryVelocity ?? 0;
      if (hiz < -250 && aktif < videolar.length - 1) {
        akisKontrol.nextPage(
          duration: const Duration(milliseconds: 260),
          curve: Curves.easeOut,
        );
      } else if (hiz > 250 && aktif > 0) {
        akisKontrol.previousPage(
          duration: const Duration(milliseconds: 260),
          curve: Curves.easeOut,
        );
      }
    },
    child: PageView.builder(
              controller: akisKontrol,
              scrollDirection: Axis.vertical,
              itemCount: videolar.length,
              onPageChanged: (i) => setState(() => aktif = i),
              itemBuilder: (_, i) {
                final item = videolar[i];
                final tur = (item['type'] ?? 'video').toString();
                if (tur == 'video') {
                  return VideoKarti(
                    adres: (item['videoUrl'] ?? item['mediaUrl'] ?? '').toString(),
                    videoId: (item['id'] ?? '').toString(),
                    kullaniciAdi: (item['username'] ?? 'ngelx').toString(),
                    ownerId: (item['ownerId'] ?? '').toString(),
                    indirilebilir: item['allowDownload']?.toString() != 'false',
                    aktif: widget.gorunur && aktif == i,
                  );
                }
                final kartVeri=<String,String>{
                  'id':(item['id']??'').toString(),
                  'type':tur,
                  'videoUrl':(item['videoUrl']??'').toString(),
                  'mediaUrl':(item['mediaUrl']??item['videoUrl']??'').toString(),
                  'audioUrl':(item['audioUrl']??'').toString(),
                  'description':(item['description']??'').toString(),
                  'username':(item['username']??'ngelx').toString(),
                  'ownerId':(item['ownerId']??'').toString(),
                  'allowDownload':(item['allowDownload']??true).toString(),
                };
                return GorselYaziKarti(
                  veri: kartVeri,
                  aktif: widget.gorunur && aktif == i,
                );
              },
            ),
          );
          },
        ),
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(17),
            child: Row(
              children: [
                const Logo(kucuk: true, koyuZemin: true),
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
                  ...kullanicilar.map((d) { final v=d.data(); final foto=(v['photoUrl'] ?? '').toString(); return ListTile(onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => KullaniciProfilPage(uid: d.id))), leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto), child: foto.isEmpty ? const Text('N') : null), title: Text((v['displayName'] ?? v['username'] ?? 'NgelX').toString()), subtitle: Text('@${v['username'] ?? 'ngelx'}'), trailing: const Icon(Icons.chevron_right)); }),
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
            CachedNetworkImage(imageUrl: (veri['mediaUrl'] ?? '').toString(), fit: BoxFit.contain),
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
        stream: FirebaseFirestore.instance.collection('videos').limit(30).snapshots(),
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
                    backgroundImage: CachedNetworkImageProvider((h['mediaUrl'] ?? '').toString()),
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

Future<void> kendiPaylasiminiSil(
  BuildContext context,
  String id,
  Map<String, dynamic> veri,
) async {
  await ngelxOverlayKapanisiniBekle();
  if (!context.mounted) return;
  final uid = FirebaseAuth.instance.currentUser?.uid;
  if (uid == null || id.isEmpty || uid != (veri['ownerId'] ?? '').toString()) return;

  final onay = await showDialog<bool>(
    context: context,
    builder: (ctx) => AlertDialog(
      title: const Text('Bu paylaşımı silmek istiyor musun?'),
      content: const Text('Paylaşım profilinden, Akıştan ve Keşfetten tamamen kaldırılacak.'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Vazgeç')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Sil', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold))),
      ],
    ),
  );
  if (onay != true) return;
  await ngelxOverlayKapanisiniBekle();
  if (!context.mounted) return;

  final ref = FirebaseFirestore.instance.collection('videos').doc(id);
  try {
    await ref.delete();
  } catch (e) {
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Paylaşım silinemedi: $e')));
    }
    return;
  }

  try {
    final likes = await ref.collection('likes').get();
    for (final x in likes.docs) {
      try { await x.reference.delete(); } catch (_) {}
    }
  } catch (_) {}

  try {
    final comments = await ref.collection('comments').get();
    for (final x in comments.docs) {
      try { await x.reference.delete(); } catch (_) {}
    }
  } catch (_) {}

  for (final raw in [
    (veri['mediaUrl'] ?? '').toString(),
    (veri['videoUrl'] ?? '').toString(),
    (veri['audioUrl'] ?? '').toString(),
  ]) {
    if (raw.isEmpty) continue;
    unawaited(ngelxMedyaSil(raw).catchError((_){ }));
  }

  if (context.mounted) {
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Paylaşım tamamen silindi ✅')));
  }
}

Future<void> kendiPaylasimMenusu(BuildContext context, String id, Map<String, dynamic> veri) async {
  if (FirebaseAuth.instance.currentUser?.uid != (veri['ownerId'] ?? '').toString()) return;
  await showModalBottomSheet(context: context, backgroundColor: panel, builder: (ctx) => SafeArea(child: Column(mainAxisSize: MainAxisSize.min, children: [
    Container(width: 42, height: 4, margin: const EdgeInsets.all(12), decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(8))),
    ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, id, veri); }),
  ])));
}


String ngelxIcerikLink(String id) => '$ngelxWebAdresi/p/$id';

Future<void> ngelxIcerikGizle(BuildContext context, String id, {bool ilgilenmiyorum = false}) async {
  final u = FirebaseAuth.instance.currentUser;
  if (u == null || id.isEmpty) return;
  if (u.isAnonymous) {
    await misafirEngeli(context);
    return;
  }
  try {
    final alan = ilgilenmiyorum ? 'notInterestedIds' : 'hiddenContent';
    await FirebaseFirestore.instance.collection('users').doc(u.uid).set({
      alan: FieldValue.arrayUnion([id]),
    }, SetOptions(merge: true));
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(ilgilenmiyorum
            ? 'Benzer içerikler azaltılacak.'
            : 'İçerik akışından gizlendi.'),
      ));
    }
  } catch (e) {
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('İşlem tamamlanamadı: $e')),
      );
    }
  }
}

Future<void> ngelxKisiyeIcerikGonder({required User ben,required String hedefUid,required String icerikId,required String aciklama}) async {
  final ids=<String>[ben.uid,hedefUid]..sort();
  final chatId=ids.join('_');
  final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
  final metin=['NgelX paylaşımı ✨',if(aciklama.trim().isNotEmpty)aciklama.trim(),ngelxIcerikLink(icerikId),'NgelX: $ngelxWebAdresi'].join('\n');
  await chat.set({'members':ids,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
  await chat.collection('messages').add({'senderId':ben.uid,'text':metin,'type':'shared_content','contentId':icerikId,'createdAt':FieldValue.serverTimestamp()});
  await chat.set({'lastMessage':'🔗 NgelX paylaşımı','updatedAt':FieldValue.serverTimestamp(),'unread_$hedefUid':FieldValue.increment(1)},SetOptions(merge:true));
  await uygulamaBildirimiGonder(toUid:hedefUid,fromUid:ben.uid,tur:'message',metin:'Sana bir NgelX paylaşımı gönderdi',belgeId:chatId);
}

Future<void> ngelxOzeldenPaylas(
  BuildContext context, {
  required String icerikId,
  required String aciklama,
}) async {
  if (await misafirEngeli(context)) return;
  final ben = FirebaseAuth.instance.currentUser;
  if (ben == null) return;

  final benim = await FirebaseFirestore.instance.collection('users').doc(ben.uid).get();
  final engellenen = Set<String>.from(List<dynamic>.from(benim.data()?['blocked'] ?? const []));
  if (!context.mounted) return;

  String sorgu = '';
  final secilenler=<String>{};
  bool gonderiliyor=false;
  await showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
    ),
    builder: (sheetContext) => StatefulBuilder(
      builder: (sheetContext, setSheet) => Theme(
        data: ThemeData.light(),
        child: SafeArea(
          child: SizedBox(
            height: MediaQuery.of(sheetContext).size.height * .72,
            child: Column(
              children: [
                Container(
                  width: 42,
                  height: 4,
                  margin: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.black26,
                    borderRadius: BorderRadius.circular(9),
                  ),
                ),
                const Text(
                  'NgelX içinde özele gönder',
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 20,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(14),
                  child: TextField(
                    onChanged: (v) => setSheet(() => sorgu = v.trim().toLowerCase()),
                    decoration: InputDecoration(
                      hintText: 'Kişi ara',
                      prefixIcon: const Icon(Icons.search),
                      filled: true,
                      fillColor: const Color(0xFFF3F4F6),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(22),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                ),
                Expanded(
                  child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                    stream: FirebaseFirestore.instance.collection('users').limit(100).snapshots(),
                    builder: (_, snap) {
                      if (snap.connectionState == ConnectionState.waiting) {
                        return const Center(child: CircularProgressIndicator(color: mor));
                      }
                      final docs = (snap.data?.docs ?? []).where((d) {
                        if (d.id == ben.uid || engellenen.contains(d.id)) return false;
                        final v = d.data();
                        if (v['deactivated'] == true) return false;
                        if (List<String>.from(v['blocked'] ?? const []).contains(ben.uid)) return false;
                        final ad = '${v['displayName'] ?? ''} ${v['username'] ?? ''}'.toLowerCase();
                        return sorgu.isEmpty || ad.contains(sorgu);
                      }).toList();

                      if (docs.isEmpty) {
                        return const Center(
                          child: Text('Kişi bulunamadı.', style: TextStyle(color: Colors.black54)),
                        );
                      }

                      return ListView.builder(
                        itemCount: docs.length,
                        itemBuilder: (_, i) {
                          final d = docs[i];
                          final v = d.data();
                          final foto = (v['photoUrl'] ?? '').toString();
                          final ad = (v['displayName'] ?? v['username'] ?? 'Kullanıcı').toString();
                          return ListTile(
                            leading: CircleAvatar(
                              backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto),
                              child: foto.isEmpty ? const Icon(Icons.person) : null,
                            ),
                            title: Text(ad, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w800)),
                            subtitle: Text('@${v['username'] ?? 'ngelx'}', style: const TextStyle(color: Colors.black54)),
                            trailing: Checkbox(value:secilenler.contains(d.id),activeColor:mor,onChanged:(_)=>setSheet((){secilenler.contains(d.id)?secilenler.remove(d.id):secilenler.add(d.id);})),
                            onTap:()=>setSheet((){secilenler.contains(d.id)?secilenler.remove(d.id):secilenler.add(d.id);}),
                          );
                        },
                      );
                    },
                  ),
                ),
                SafeArea(top:false,child:Padding(padding:const EdgeInsets.fromLTRB(14,8,14,12),child:SizedBox(width:double.infinity,height:52,child:FilledButton.icon(onPressed:secilenler.isEmpty||gonderiliyor?null:()async{setSheet(()=>gonderiliyor=true);try{for(final uid in secilenler){await ngelxKisiyeIcerikGonder(ben:ben,hedefUid:uid,icerikId:icerikId,aciklama:aciklama);}if(!icerikId.startsWith('ornek_'))await FirebaseFirestore.instance.collection('videos').doc(icerikId).set({'shareCount':FieldValue.increment(secilenler.length)},SetOptions(merge:true));if(sheetContext.mounted)Navigator.pop(sheetContext);if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('${secilenler.length} kişiye gönderildi ✅')));}catch(e){setSheet(()=>gonderiliyor=false);if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Gönderilemedi, tekrar dene: $e')));}},icon:gonderiliyor?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2)):const Icon(Icons.send_rounded),label:Text(secilenler.isEmpty?'Göndermek için kişi seç':'${secilenler.length} kişiye gönder'))))),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

Future<void> ngelxPaylasimMenusu(
  BuildContext context, {
  required String icerikId,
  required String aciklama,
}) async {
  final link = ngelxIcerikLink(icerikId);
  final metin = [
    'NgelX’te bunu gördüm ✨',
    if (aciklama.trim().isNotEmpty) aciklama.trim(),
    '',
    'İçeriğe bak: $link',
    'NgelX: $ngelxWebAdresi',
  ].join('\n');

  await showModalBottomSheet<void>(
    context: context,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
    ),
    builder: (c) => Theme(
      data: ThemeData.light(),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 42,
              height: 4,
              margin: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(9),
              ),
            ),
            const ListTile(
              title: Text(
                'Paylaş',
                style: TextStyle(color: Colors.black, fontSize: 20, fontWeight: FontWeight.w900),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.forum_rounded, color: mor),
              title: const Text(
                'NgelX içinde özele gönder',
                style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w800),
              ),
              onTap: () {
                Navigator.pop(c);
                ngelxOzeldenPaylas(context, icerikId: icerikId, aciklama: aciklama);
              },
            ),
            ListTile(
              leading: const Icon(Icons.share_rounded, color: Color(0xFF20B86A)),
              title: const Text(
                'WhatsApp / diğer uygulamalar',
                style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w800),
              ),
              subtitle: const Text(ngelxWebAdresi, style: TextStyle(color: Colors.black54)),
              onTap: () async {
                Navigator.pop(c);
                await SharePlus.instance.share(
                  ShareParams(text: metin, title: 'NgelX paylaşımı'),
                );
                if (!icerikId.startsWith('ornek_')) {
                  await FirebaseFirestore.instance.collection('videos').doc(icerikId).set(
                    {'shareCount': FieldValue.increment(1)},
                    SetOptions(merge: true),
                  );
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.link_rounded, color: Colors.blue),
              title: const Text(
                'Bağlantıyı kopyala',
                style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w800),
              ),
              subtitle: Text(link, style: const TextStyle(color: Colors.black54)),
              onTap: () async {
                await Clipboard.setData(ClipboardData(text: link));
                if (c.mounted) Navigator.pop(c);
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('NgelX bağlantısı kopyalandı ✅')),
                  );
                }
              },
            ),
          ],
        ),
      ),
    ),
  );
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
  bool kalpAnimasyonu = false;
  bool begeniIsleniyor = false;
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

  Future<void> ciftTikBegen() async {
    if (!begenildi) await begeniyiDegistir();
    if (!mounted) return;
    setState(() => kalpAnimasyonu = true);
    await Future.delayed(const Duration(milliseconds: 520));
    if (mounted) setState(() => kalpAnimasyonu = false);
  }

  Future<void> begeniyiDegistir() async {
    if(begeniIsleniyor)return;
    if(await misafirEngeli(context))return;
    final user=FirebaseAuth.instance.currentUser;
    if(user==null||icerikId.isEmpty)return;
    final video=FirebaseFirestore.instance.collection('videos').doc(icerikId);
    final ref=video.collection('likes').doc(user.uid);
    begeniIsleniyor=true;
    final yeni=!begenildi;
    setState((){
      begenildi=yeni;
      begeniSayisi+=yeni?1:-1;
      if(begeniSayisi<0)begeniSayisi=0;
    });
    try{
      final batch=FirebaseFirestore.instance.batch();
      if(yeni){
        batch.set(ref,{'userId':user.uid,'createdAt':FieldValue.serverTimestamp()});
        batch.set(video,{'likeCount':FieldValue.increment(1)},SetOptions(merge:true));
      }else{
        batch.delete(ref);
        batch.set(video,{'likeCount':FieldValue.increment(-1)},SetOptions(merge:true));
      }
      await batch.commit();
      final hedefUid=(widget.veri['ownerId']??'').toString();
      if(yeni&&hedefUid.isNotEmpty&&hedefUid!=user.uid){
        unawaited(uygulamaBildirimiGonder(
          toUid:hedefUid,fromUid:user.uid,tur:'interaction',
          metin:'Gönderini beğendi',belgeId:icerikId,
        ).catchError((_){ }));
      }
    }catch(e){
      if(mounted)setState((){
        begenildi=!yeni;
        begeniSayisi+=yeni?-1:1;
      });
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Beğeni kaydedilemedi: $e')));
    }finally{
      begeniIsleniyor=false;
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
    await ngelxPaylasimMenusu(
      context,
      icerikId: icerikId,
      aciklama: (widget.veri['description'] ?? '').toString(),
    );
    await etkilesimleriGetir();
  }

  Future<void> uzunBasmaMenusu() async {
    final sahibi = FirebaseAuth.instance.currentUser?.uid == widget.veri['ownerId'];
    await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) => Theme(
        data: ThemeData.light(),
        child: SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(width: 42, height: 4, margin: const EdgeInsets.all(12), decoration: BoxDecoration(color: Colors.black26, borderRadius: BorderRadius.circular(9))),
              if (indirilebilir) ListTile(leading: const Icon(Icons.download_rounded, color: mavi), title: const Text('İndir'), onTap: () { Navigator.pop(ctx); fotografiKaydet(); }),
              ListTile(leading: const Icon(Icons.heart_broken_outlined, color: Colors.black87), title: const Text('İlgilenmiyorum'), subtitle: const Text('Benzer içerikleri azalt'), onTap: () { Navigator.pop(ctx); ngelxIcerikGizle(context, icerikId, ilgilenmiyorum: true); }),
              ListTile(leading: const Icon(Icons.visibility_off_outlined, color: Colors.black87), title: const Text('İçeriği gizle'), onTap: () { Navigator.pop(ctx); ngelxIcerikGizle(context, icerikId); }),
              ListTile(leading: const Icon(Icons.link_rounded, color: Colors.blue), title: const Text('Bağlantıyı kopyala'), onTap: () async { await Clipboard.setData(ClipboardData(text: ngelxIcerikLink(icerikId))); if (ctx.mounted) Navigator.pop(ctx); }),
              ListTile(leading: const Icon(Icons.flag_outlined, color: Colors.orange), title: const Text('Bildir / Şikâyet et'), onTap: () { Navigator.pop(ctx); sikayetEt(context, hedefTuru: 'paylasim', hedefId: icerikId, hedefUid: (widget.veri['ownerId'] ?? '').toString()); }),
              if (!sahibi) ListTile(leading: const Icon(Icons.block, color: Colors.red), title: const Text('Kullanıcıyı engelle', style: TextStyle(color: Colors.red)), onTap: () { Navigator.pop(ctx); kullaniciyiEngelle(context, (widget.veri['ownerId'] ?? '').toString()); }),
              if (sahibi) ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, icerikId, widget.veri); }),
            ],
          ),
        ),
      ),
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
      onDoubleTap: ciftTikBegen,
      child: Container(
        color: const Color(0xFF09090F),
        child: Stack(
        fit: StackFit.expand,
        children: [
          if (foto.isNotEmpty)
            CachedNetworkImage(
              imageUrl: foto,
              fit: BoxFit.contain,
              errorWidget: (_, __, ___) => ngelxMedyaHataGorunumu(foto),
            )
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
          if (kalpAnimasyonu)
            const Center(child: KalpPatlama()),
          Positioned(
            left: 20,
            bottom: 28,
            right: 82,
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('@${widget.veri['username'] ?? 'ngelx'}', style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold)),
              if (foto.isNotEmpty && yazi.isNotEmpty) ...[const SizedBox(height: 8), Text(yazi)],
              if ((widget.veri['audioUrl'] ?? '').isNotEmpty) ...[const SizedBox(height: 8), const Row(children: [Icon(Icons.music_note, size: 18), Text(' Fotoğraflı müzik')])],
    const SizedBox(height: 8),
    AkisMetaSatiri(icerikId: icerikId, yorumlariAc: yorumlariAc),
            ]),
          ),
          Positioned(
            right: 15,
            bottom: 25,
            child: Column(children: [
              CanliSayacButonu(ref: FirebaseFirestore.instance.collection('videos').doc(icerikId).collection('likes'), ikon: begenildi ? Icons.favorite : Icons.favorite_border, renk: begenildi ? const Color(0xFFE6003C) : Colors.white, tiklama: begeniyiDegistir, uzunBasma:()async{await tepkiMenusu(context,icerikId);if(mounted)setState(()=>begenildi=true);}),
              CanliSayacButonu(ref: FirebaseFirestore.instance.collection('videos').doc(icerikId).collection('comments'), ikon: Icons.mode_comment_outlined, tiklama: yorumlariAc),
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
  bool sessiz = false;
  bool kalpAnimasyonu = false;
  bool begeniIsleniyor = false;
  String? medyaHatasi;
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
    }).catchError((e) {
      if (mounted) {
        setState(() => medyaHatasi = e.toString());
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

  Future<void> ciftTikBegenVideo() async {
    if (!begenildi) await begeniyiDegistir();
    if (!mounted) return;
    setState(() => kalpAnimasyonu = true);
    await Future.delayed(const Duration(milliseconds: 520));
    if (mounted) setState(() => kalpAnimasyonu = false);
  }

  void sesiDegistir() {
    if (!hazir) return;
    setState(() => sessiz = !sessiz);
    kontrol.setVolume(sessiz ? 0 : 1);
  }

  Future<void> begeniyiDegistir() async {
    if (begeniIsleniyor) return;
    if (await misafirEngeli(context)) return;
    final kullanici=FirebaseAuth.instance.currentUser;
    if(kullanici==null)return;
    final video=FirebaseFirestore.instance.collection('videos').doc(videoId);
    final begeni=video.collection('likes').doc(kullanici.uid);
    final yeniDurum=!begenildi;
    begeniIsleniyor=true;
    setState((){
      begenildi=yeniDurum;
      begeniSayisi+=yeniDurum?1:-1;
      if(begeniSayisi<0)begeniSayisi=0;
    });
    try{
      final batch=FirebaseFirestore.instance.batch();
      if(yeniDurum){
        batch.set(begeni,{'userId':kullanici.uid,'createdAt':FieldValue.serverTimestamp()});
        batch.set(video,{'likeCount':FieldValue.increment(1)},SetOptions(merge:true));
      }else{
        batch.delete(begeni);
        batch.set(video,{'likeCount':FieldValue.increment(-1)},SetOptions(merge:true));
      }
      await batch.commit();
      if(yeniDurum&&widget.ownerId.isNotEmpty&&widget.ownerId!=kullanici.uid){
        unawaited(uygulamaBildirimiGonder(
          toUid:widget.ownerId,fromUid:kullanici.uid,tur:'interaction',
          metin:'Videonu beğendi',belgeId:videoId,
        ).catchError((_){ }));
      }
    }catch(e){
      if(mounted)setState((){
        begenildi=!yeniDurum;
        begeniSayisi+=yeniDurum?-1:1;
      });
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Beğeni kaydedilemedi: $e')));
    }finally{
      begeniIsleniyor=false;
    }
  }


  Future<void> videoyuPaylas() async {
    await ngelxPaylasimMenusu(
      context,
      icerikId: videoId,
      aciklama: 'NgelX videosu • @${widget.kullaniciAdi}',
    );
    await etkilesimleriGetir();
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
        const SnackBar(content: Text('Video kaydedilemedi. Fotoğraf ve video iznini aç.')),
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
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => KullaniciProfilPage(uid: widget.ownerId),
      ),
    );
  }

  Future<void> uzunBasmaMenusu() async {
    final sahibi = FirebaseAuth.instance.currentUser?.uid == widget.ownerId;
    await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) => Theme(
        data: ThemeData.light(),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(14, 12, 14, 22),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(width: 42, height: 4, margin: const EdgeInsets.only(bottom: 12), decoration: BoxDecoration(color: Colors.black26, borderRadius: BorderRadius.circular(9))),
                if (widget.indirilebilir || sahibi) ListTile(leading: const Icon(Icons.download_rounded, color: mavi), title: const Text('İndir'), onTap: () { Navigator.pop(ctx); videoyuGaleriyeKaydet(); }),
                ListTile(leading: const Icon(Icons.heart_broken_outlined, color: Colors.black87), title: const Text('İlgilenmiyorum'), subtitle: const Text('Benzer içerikleri azalt'), onTap: () { Navigator.pop(ctx); ngelxIcerikGizle(context, videoId, ilgilenmiyorum: true); }),
                ListTile(leading: const Icon(Icons.visibility_off_outlined, color: Colors.black87), title: const Text('İçeriği gizle'), onTap: () { Navigator.pop(ctx); ngelxIcerikGizle(context, videoId); }),
                ListTile(leading: const Icon(Icons.link_rounded, color: Colors.blue), title: const Text('Bağlantıyı kopyala'), onTap: () async { await Clipboard.setData(ClipboardData(text: ngelxIcerikLink(videoId))); if (ctx.mounted) Navigator.pop(ctx); }),
                ListTile(leading: const Icon(Icons.flag_outlined, color: Colors.orange), title: const Text('Bildir / Şikâyet et'), onTap: () { Navigator.pop(ctx); sikayetEt(context, hedefTuru: 'video', hedefId: videoId, hedefUid: widget.ownerId); }),
                if (!sahibi) ListTile(leading: const Icon(Icons.block, color: Colors.red), title: const Text('Kullanıcıyı engelle', style: TextStyle(color: Colors.red)), onTap: () { Navigator.pop(ctx); kullaniciyiEngelle(context, widget.ownerId); }),
                if (sahibi) ListTile(leading: const Icon(Icons.delete_forever, color: Colors.red), title: const Text('PAYLAŞIMI SİL', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)), onTap: () { Navigator.pop(ctx); kendiPaylasiminiSil(context, videoId, {'ownerId': widget.ownerId, 'videoUrl': widget.adres}); }),
                const Divider(),
                const Align(alignment: Alignment.centerLeft, child: Padding(padding: EdgeInsets.all(10), child: Text('Video hızı', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)))),
                Wrap(spacing: 9, children: [.5, 1.0, 1.5, 2.0].map((hiz) => ActionChip(label: Text('${hiz}x'), onPressed: () { kontrol.setPlaybackSpeed(hiz); Navigator.pop(ctx); })).toList()),
              ],
            ),
          ),
        ),
      ),
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
      onDoubleTap: ciftTikBegenVideo,
      child: Stack(
        fit: StackFit.expand,
        children: [
          Container(color: Colors.black),
          if (medyaHatasi != null)
            ngelxMedyaHataGorunumu(widget.adres)
          else if (hazir)
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
if (kalpAnimasyonu)
  const Center(child: KalpPatlama()),
Positioned(
  top: 88,
  right: 16,
  child: Material(
    color: Colors.black45,
    shape: const CircleBorder(),
    child: IconButton(
      onPressed: sesiDegistir,
      icon: Icon(
        sessiz ? Icons.volume_off_rounded : Icons.volume_up_rounded,
        color: Colors.white,
        size: 22,
      ),
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
      const SizedBox(height: 8),
      AkisMetaSatiri(icerikId: videoId, yorumlariAc: yorumlariAc),
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
                      backgroundImage: profilFoto.isEmpty ? null : CachedNetworkImageProvider(profilFoto),
                      child: profilFoto.isNotEmpty ? null : const Text(
                        'N',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
                CanliSayacButonu(
        ref: FirebaseFirestore.instance.collection('videos').doc(videoId).collection('likes'),
        ikon: begenildi ? Icons.favorite : Icons.favorite_border,
        renk: begenildi ? const Color(0xFFE6003C) : Colors.white,
        tiklama: begeniyiDegistir,
        uzunBasma:()async{await tepkiMenusu(context,videoId);if(mounted)setState(()=>begenildi=true);},
      ),
                CanliSayacButonu(
        ref: FirebaseFirestore.instance.collection('videos').doc(videoId).collection('comments'),
        ikon: Icons.mode_comment_outlined,
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
                IslemButonu(ikon:Icons.menu_rounded,yazi:'Araçlar',tiklama:()=>icerikAracMenusu(context,videoId,mevcutHiz:kontrol.value.playbackSpeed,hizDegistir:(x)async=>kontrol.setPlaybackSpeed(x))),
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



String akisKisaZaman(dynamic ham) {
  if (ham is! Timestamp) return 'Şimdi';
  final fark = DateTime.now().difference(ham.toDate());
  if (fark.inSeconds < 45) return 'Şimdi';
  if (fark.inMinutes < 60) return '${fark.inMinutes} dk önce';
  if (fark.inHours < 24) return '${fark.inHours} sa önce';
  if (fark.inDays == 1) return 'Dün';
  if (fark.inDays < 7) return '${fark.inDays} gün önce';
  final d = ham.toDate();
  return '${d.day}.${d.month}.${d.year}';
}

class KalpPatlama extends StatelessWidget {
  const KalpPatlama({super.key});
  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: TweenAnimationBuilder<double>(
        tween: Tween(begin: .55, end: 1.15),
        duration: const Duration(milliseconds: 420),
        curve: Curves.easeOutBack,
        builder: (_, value, child) => Transform.scale(
          scale: value,
          child: Opacity(
            opacity: (1.25 - value).clamp(0.0, 1.0).toDouble(),
            child: child,
          ),
        ),
        child: const Icon(
          Icons.favorite_rounded,
          size: 112,
          color: const Color(0xFFFF2D55),
          shadows: [Shadow(color: Colors.black45, blurRadius: 18)],
        ),
      ),
    );
  }
}

class AkisMetaSatiri extends StatelessWidget {
  final String icerikId;
  final VoidCallback yorumlariAc;
  const AkisMetaSatiri({
    super.key,
    required this.icerikId,
    required this.yorumlariAc,
  });

  @override
  Widget build(BuildContext context) {
    if (icerikId.isEmpty || icerikId.startsWith('ornek_')) {
      return const SizedBox.shrink();
    }
    final ref = FirebaseFirestore.instance.collection('videos').doc(icerikId);
    return StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream: ref.snapshots(),
      builder: (_, belge) {
        final zaman = akisKisaZaman(belge.data?.data()?['createdAt']);
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              zaman,
              style: const TextStyle(
                color: Colors.white60,
                fontSize: 11,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(height: 4),
            StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: ref.collection('comments').snapshots(),
              builder: (_, snap) {
                final sayi=snap.data?.docs.length??0;
                if(sayi==0)return const SizedBox.shrink();
                return GestureDetector(
                  onTap: yorumlariAc,
                  child: Text(
                    sayi==1?'Yorumu gör':'$sayi yorumun tümünü gör',
                    style:const TextStyle(color:Colors.white70,fontSize:11,fontWeight:FontWeight.w700),
                  ),
                );
              },
            ),
          ],
        );
      },
    );
  }
}


class CanliSayacButonu extends StatelessWidget {
  final CollectionReference<Map<String, dynamic>> ref;
  final IconData ikon;
  final VoidCallback tiklama;
  final Color renk;
  final VoidCallback? uzunBasma;

  const CanliSayacButonu({
    super.key,
    required this.ref,
    required this.ikon,
    required this.tiklama,
    this.uzunBasma,
    this.renk = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: ref.snapshots(),
      builder: (_, snap) => IslemButonu(
        ikon: ikon,
        yazi: '${snap.data?.docs.length ?? 0}',
        renk: renk,
        tiklama: tiklama,
        uzunBasma: uzunBasma,
      ),
    );
  }
}

class CanliEtkilesimOzet extends StatelessWidget {
  final String icerikId;
  final VoidCallback yorumlariAc;

  const CanliEtkilesimOzet({
    super.key,
    required this.icerikId,
    required this.yorumlariAc,
  });

  @override
  Widget build(BuildContext context) {
    final ref = FirebaseFirestore.instance.collection('videos').doc(icerikId);
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
          stream: ref.collection('likes').snapshots(),
          builder: (_, snap) => Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.favorite_rounded, size: 16, color: Colors.white),
              const SizedBox(width: 5),
              Text(
                '${snap.data?.docs.length ?? 0} beğeni',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(width: 13),
        Expanded(
          child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
            stream: ref.collection('comments').snapshots(),
            builder: (_, snap) {
              final sayi = snap.data?.docs.length ?? 0;
              return GestureDetector(
                onTap: yorumlariAc,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.mode_comment_outlined, size: 16, color: Colors.white),
                        const SizedBox(width: 5),
                        Text(
                          '$sayi yorum',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                    if (sayi > 0) ...[
                      const SizedBox(height: 4),
                      const Text(
                        'Yorumları gör',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 12,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}


class IslemButonu extends StatelessWidget {
  final IconData ikon;
  final String yazi;
  final VoidCallback tiklama;
  final Color renk;
  final VoidCallback? uzunBasma;

  const IslemButonu({
    super.key,
    required this.ikon,
    required this.yazi,
    required this.tiklama,
    this.uzunBasma,
    this.renk = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: tiklama,
      onLongPress: uzunBasma,
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
  bool gizliKelimeFiltresi=true;
  List<String> gizliKelimeListesi=[];
  String? yanitlananId;
  String? yanitlananKullanici;
  final Set<String> acikYanitlar = {};
  bool enCokBegenilen = false;

  CollectionReference<Map<String, dynamic>> get ref => FirebaseFirestore.instance.collection('videos').doc(widget.videoId).collection('comments');

  @override void initState(){
    super.initState();
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid!=null)FirebaseFirestore.instance.collection('users').doc(uid).get().then((d){
      final v=d.data()??<String,dynamic>{};
      if(mounted)setState((){
        gizliKelimeFiltresi=v['hiddenWordsFilter']!=false;
        gizliKelimeListesi=List<String>.from(v['hiddenWords']??const[]);
      });
    });
  }

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
    final metin=yorum.text.trim();
    final user=FirebaseAuth.instance.currentUser;
    if(metin.isEmpty||user==null||gonderiliyor)return;

    String icerikSahibi='';
    try{
      final video=await FirebaseFirestore.instance.collection('videos').doc(widget.videoId).get();
      final vv=video.data()??<String,dynamic>{};
      icerikSahibi=(vv['ownerId']??'').toString();
      final izin=(vv['commentAudience']??'Herkes').toString();
      if(user.uid!=icerikSahibi){
        if(vv['allowComments']==false||izin=='Kimse'){
          if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu gönderide yorumlar kapalı.')));
          return;
        }
        if(izin!='Herkes'){
          final sahipBelgesi=await FirebaseFirestore.instance.collection('users').doc(icerikSahibi).get();
          final sv=sahipBelgesi.data()??<String,dynamic>{};
          if(izin=='Arkadaşlar'&&!List<String>.from(sv['friends']??const[]).contains(user.uid)){
            if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu gönderiye yalnızca arkadaşlar yorum yapabilir.')));
            return;
          }
          if(izin=='Takip ettiklerim'&&!List<String>.from(sv['following']??const[]).contains(user.uid)){
            if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu gönderiye yalnızca içerik sahibinin takip ettiği kişiler yorum yapabilir.')));
            return;
          }
        }
      }
    }catch(_){}

    setState(()=>gonderiliyor=true);
    final yanitId=yanitlananId;
    final yanitKullanici=yanitlananKullanici;
    try{
      final profil=await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final p=profil.data()??<String,dynamic>{};
      final yorumRef=ref.doc();
      final videoRef=FirebaseFirestore.instance.collection('videos').doc(widget.videoId);
      final batch=FirebaseFirestore.instance.batch();
      batch.set(yorumRef,{
        'userId':user.uid,
        'username':(p['username']??user.displayName??'ngelx').toString(),
        'photoUrl':(p['photoUrl']??'').toString(),
        'text':metin,
        'parentId':yanitId??'',
        'replyToUsername':yanitKullanici??'',
        'likedBy':<String>[],
        'createdAt':FieldValue.serverTimestamp(),
      });
      batch.set(videoRef,{'commentCount':FieldValue.increment(1)},SetOptions(merge:true));
      await batch.commit();

      yorum.clear();
      if(mounted)setState((){
        yanitlananId=null;
        yanitlananKullanici=null;
        gonderiliyor=false;
      });

      if(yanitId!=null&&yanitId.isNotEmpty){
        unawaited(ref.doc(yanitId).get().then((anaYorum)async{
          final hedefUid=(anaYorum.data()?['userId']??'').toString();
          if(hedefUid.isEmpty||hedefUid==user.uid)return;
          await uygulamaBildirimiGonder(
            toUid:hedefUid,
            fromUid:user.uid,
            tur:'interaction',
            metin:'Yorumuna yanıt verdi',
            belgeId:widget.videoId,
          );
        }).catchError((_){ }));
      }else if(icerikSahibi.isNotEmpty&&icerikSahibi!=user.uid){
        unawaited(uygulamaBildirimiGonder(
          toUid:icerikSahibi,
          fromUid:user.uid,
          tur:'interaction',
          metin:'Gönderine yorum yaptı',
          belgeId:widget.videoId,
        ).catchError((_){ }));
      }
    }catch(e){
      if(mounted){
        setState(()=>gonderiliyor=false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Yorum gönderilemedi, tekrar dene: $e')));
      }
    }
  }

  Future<void> yorumBegen(String id, List<dynamic> _) async {
    if (await misafirEngeli(context)) return;
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;

    final yorumRef = ref.doc(id);
    final likeRef = yorumRef.collection('likes').doc(uid);

    try {
      final varMi = await likeRef.get();
      if (varMi.exists) {
        await likeRef.delete();
        await yorumRef.set({'likeCount': FieldValue.increment(-1)}, SetOptions(merge:true));
      } else {
        await likeRef.set({
          'uid': uid,
          'createdAt': FieldValue.serverTimestamp(),
        });
        await yorumRef.set({'likeCount': FieldValue.increment(1)}, SetOptions(merge:true));

        final yorumBelgesi = await yorumRef.get();
        final yorumSahibi = (yorumBelgesi.data()?['userId'] ?? '').toString();
        if (yorumSahibi.isNotEmpty && yorumSahibi != uid) {
          await uygulamaBildirimiGonder(
            toUid: yorumSahibi,
            fromUid: uid,
            tur: 'like',
            metin: 'Yorumunu beğendi',
            belgeId: widget.videoId,
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Yorum beğenilemedi: $e')),
        );
      }
    }
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
              return bt.compareTo(at);
            });
            final ana = tumu.where((d) => (d.data()['parentId'] ?? '').toString().isEmpty).toList();
            if (enCokBegenilen) {
              ana.sort((a, b) {
                final al = (a.data()['likeCount'] as num?)?.toInt() ?? 0;
                final bl = (b.data()['likeCount'] as num?)?.toInt() ?? 0;
                return bl.compareTo(al);
              });
            }
            return Column(children: [
              Container(width: 42, height: 4, margin: const EdgeInsets.only(top: 9), decoration: BoxDecoration(color: Colors.black26, borderRadius: BorderRadius.circular(9))),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 12),
                child: Row(children: [const Spacer(), Text('${tumu.length} yorum', style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900)), const Spacer(), PopupMenuButton<bool>(tooltip:'Yorum sıralaması',initialValue:enCokBegenilen,onSelected:(v)=>setState(()=>enCokBegenilen=v),itemBuilder:(_)=>const [PopupMenuItem(value:false,child:Text('En yeni')),PopupMenuItem(value:true,child:Text('En çok beğenilen'))],icon:const Icon(Icons.sort_rounded)), IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close))]),
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
                                videoId: widget.videoId,
                                id: d.id,
                                veri: v,
                                zaman: zamanYaz(v['createdAt']),
                                yanitlar: yanitlar,
                                acik: acikYanitlar.contains(d.id),
                                zamanYaz: zamanYaz,
                                begen: yorumBegen,
                                yanitla: () => setState(() { yanitlananId = d.id; yanitlananKullanici = (v['username'] ?? 'ngelx').toString(); }),
                                yanitlariAc: () => setState(() { acikYanitlar.contains(d.id) ? acikYanitlar.remove(d.id) : acikYanitlar.add(d.id); }),
                                gizliKelimeFiltresi:gizliKelimeFiltresi,
                                gizliKelimeListesi:gizliKelimeListesi,
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
  final String videoId;
  final String id;
  final Map<String, dynamic> veri;
  final String zaman;
  final List<QueryDocumentSnapshot<Map<String, dynamic>>> yanitlar;
  final bool acik;
  final String Function(dynamic) zamanYaz;
  final Future<void> Function(String, List<dynamic>) begen;
  final VoidCallback yanitla;
  final VoidCallback yanitlariAc;
  final bool gizliKelimeFiltresi;
  final List<String> gizliKelimeListesi;

  const YorumKarti({
    super.key,
    required this.videoId,
    required this.id,
    required this.veri,
    required this.zaman,
    required this.yanitlar,
    required this.acik,
    required this.zamanYaz,
    required this.begen,
    required this.yanitla,
    required this.yanitlariAc,
    this.gizliKelimeFiltresi=true,
    this.gizliKelimeListesi=const[],
  });

  Widget satir(
    BuildContext context,
    String yorumId,
    Map<String, dynamic> v,
    String zaman, {
    bool yanit = false,
  }) {
    final ad = (v['username'] ?? 'ngelx').toString();
    final metin = (v['text'] ?? v['message'] ?? v['content'] ?? '').toString().trim();
    final gizlenecek=gizliKelimeFiltresi&&metin.isNotEmpty&&gizliKelimeListesi.any((x)=>x.trim().isNotEmpty&&metin.toLowerCase().contains(x.toLowerCase()));
    final gosterilecekMetin=gizlenecek?'Gizli kelime filtresi nedeniyle gizlendi.':metin;
    final foto = (v['photoUrl'] ?? '').toString();
    final profilUid = (v['userId'] ?? '').toString();
    final aktifUid = FirebaseAuth.instance.currentUser?.uid;

    Future<void> yorumMenusu() async {
      final benim = aktifUid == profilUid;
      final videoBelgesi = await FirebaseFirestore.instance.collection('videos').doc(videoId).get();
      final icerikSahibi = (videoBelgesi.data()?['ownerId'] ?? '').toString();
      final silebilir = benim || (aktifUid != null && aktifUid == icerikSahibi);
      if (!context.mounted) return;
      final secim = await showModalBottomSheet<String>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(26))),
        builder: (c) => Theme(data:ThemeData.light(),child:SafeArea(child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.black26,borderRadius:BorderRadius.circular(8))),
          Padding(
            padding:const EdgeInsets.symmetric(horizontal:10,vertical:4),
            child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
              for(final e in const ['❤️','😂','😮','😢','😡','👍'])
                InkWell(onTap:()=>Navigator.pop(c,'reaction:'+e),child:Text(e,style:const TextStyle(fontSize:27))),
            ]),
          ),
          if (benim) ListTile(leading:const Icon(Icons.edit_outlined),title:const Text('Düzenle'),onTap:()=>Navigator.pop(c,'edit')),
          if (silebilir) ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:Text(benim?'Yorumu sil':'Gönderimden kaldır',style:const TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'delete')),
          ListTile(leading:const Icon(Icons.copy_outlined),title:const Text('Kopyala'),onTap:()=>Navigator.pop(c,'copy')),
          if (!benim) ListTile(leading:const Icon(Icons.flag_outlined,color:Colors.orange),title:const Text('Şikâyet et'),onTap:()=>Navigator.pop(c,'report')),
          if (!benim) ListTile(leading:const Icon(Icons.block,color:Colors.red),title:const Text('Kullanıcıyı engelle',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'block')),
        ]))),
      );
      if (secim == null || !context.mounted) return;
      await ngelxOverlayKapanisiniBekle();
      if (!context.mounted) return;
      final yorumRef = FirebaseFirestore.instance.collection('videos').doc(videoId).collection('comments').doc(yorumId);
      if (secim.startsWith('reaction:')) {
        final emoji=secim.substring(9);
        if(aktifUid!=null){
          final alan='reactions.'+aktifUid;
          final mevcut=Map<String,dynamic>.from(v['reactions']??const{});
          if((mevcut[aktifUid]??'').toString()==emoji)await yorumRef.update({alan:FieldValue.delete()});
          else await yorumRef.set({alan:emoji},SetOptions(merge:true));
        }
      } else if (secim == 'copy') {
        await Clipboard.setData(ClipboardData(text: metin));
        if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yorum kopyalandı.')));
      } else if (secim == 'report') {
        await sikayetEt(context, hedefTuru:'yorum', hedefId:'$videoId/$yorumId', hedefUid:profilUid);
      } else if (secim == 'block') {
        await kullaniciyiEngelle(context, profilUid);
      } else if (secim == 'delete') {
        final onay = await showDialog<bool>(context:context,builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(backgroundColor:Colors.white,surfaceTintColor:Colors.white,title:const Text('Yorum silinsin mi?',style:TextStyle(color:Colors.black87)),content:const Text('Bu işlem geri alınamaz.',style:TextStyle(color:Colors.black54)),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Sil'))]))) ?? false;
        if (onay) {
          try {
            final videoRef=FirebaseFirestore.instance.collection('videos').doc(videoId);
            final yorumlarRef=videoRef.collection('comments');
            final altYanitlar=await yorumlarRef.where('parentId',isEqualTo:yorumId).get();
            final hedefler=<DocumentReference<Map<String,dynamic>>>[yorumRef,...altYanitlar.docs.map((e)=>e.reference)];
            for(final hedef in hedefler){
              final begeniler=await hedef.collection('likes').get();
              final batch=FirebaseFirestore.instance.batch();
              for(final b in begeniler.docs){batch.delete(b.reference);}
              batch.delete(hedef);
              await batch.commit();
            }
            await videoRef.set({'commentCount':FieldValue.increment(-hedefler.length)},SetOptions(merge:true));
          } catch(e) {
            if(context.mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Yorum silinemedi: $e')));
          }
        }
      } else if (secim == 'edit') {
        final kontrol = TextEditingController(text:metin);
        final kaydet = await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Yorumu düzenle'),content:TextField(controller:kontrol,maxLines:4,maxLength:500,autofocus:true),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Kaydet'))])) ?? false;
        final yeni = kontrol.text.trim(); kontrol.dispose();
        if (kaydet && yeni.isNotEmpty) {
          try { await yorumRef.update({'text':yeni,'updatedAt':FieldValue.serverTimestamp()}); } catch(e) { if(context.mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Yorum güncellenemedi: $e'))); }
        }
      }
    }

    void profilAc() {
      if (profilUid.isEmpty) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => KullaniciProfilPage(uid: profilUid)),
      );
    }

    final yorumBelgeRef = FirebaseFirestore.instance
        .collection('videos')
        .doc(videoId)
        .collection('comments')
        .doc(yorumId);

    Future<void> hizliKalp() async {
      final uid=FirebaseAuth.instance.currentUser?.uid;
      if(uid==null)return;
      try{
        await yorumBelgeRef.set({'reactions.$uid':'❤️'},SetOptions(merge:true));
        final likeRef=yorumBelgeRef.collection('likes').doc(uid);
        final mevcut=await likeRef.get();
        if(!mevcut.exists){
          final batch=FirebaseFirestore.instance.batch();
          batch.set(likeRef,{'uid':uid,'createdAt':FieldValue.serverTimestamp()});
          batch.set(yorumBelgeRef,{'likeCount':FieldValue.increment(1)},SetOptions(merge:true));
          await batch.commit();
        }
      }catch(_){
        if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('❤️ tepki eklenemedi.')),
        );
      }
    }

    final likeStream = yorumBelgeRef.collection('likes').snapshots();

    return GestureDetector(
      onLongPress: yorumMenusu,
      onDoubleTap: hizliKalp,
      child: Padding(
      padding: EdgeInsets.fromLTRB(yanit ? 52 : 0, 9, 0, 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          GestureDetector(
            onTap: profilAc,
            child: CircleAvatar(
              radius: yanit ? 16 : 21,
              backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto),
              child: foto.isEmpty ? Text(ad.isEmpty ? 'N' : ad[0].toUpperCase()) : null,
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GestureDetector(
                  onTap: profilAc,
                  child: Text('@$ad', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black87)),
                ),
                if ((v['replyToUsername'] ?? '').toString().isNotEmpty)
                  Text.rich(
                    TextSpan(
                      children: [
                        TextSpan(text: '@${v['replyToUsername']}  ', style: const TextStyle(color: mor, fontWeight: FontWeight.w700)),
                        TextSpan(text: gosterilecekMetin.isEmpty ? 'Mesaj içeriği bulunamadı' : gosterilecekMetin),
                      ],
                    ),
                    style: const TextStyle(color: Colors.black87, fontSize: 15, height: 1.3),
                  )
                else
                  Text(
                    gosterilecekMetin.isEmpty ? 'Mesaj içeriği bulunamadı' : gosterilecekMetin,
                    maxLines: null,
                    softWrap: true,
                    style: const TextStyle(color: Colors.black87, fontSize: 15, height: 1.3),
                  ),
                if (v['reactions'] is Map && (v['reactions'] as Map).isNotEmpty) ...[
                  const SizedBox(height:6),
                  Wrap(spacing:5,runSpacing:5,children:(){
                    final m=Map<String,dynamic>.from(v['reactions'] as Map);
                    final say=<String,int>{};
                    for(final x in m.values){final e=x.toString();say[e]=(say[e]??0)+1;}
                    return say.entries.map((e)=>Container(
                      padding:const EdgeInsets.symmetric(horizontal:7,vertical:3),
                      decoration:BoxDecoration(color:const Color(0xFFF3F4F6),borderRadius:BorderRadius.circular(12)),
                      child:Text(e.value>1?e.key+' '+e.value.toString():e.key),
                    )).toList();
                  }()),
                ],
                const SizedBox(height: 5),
                Row(
                  children: [
                    Text(zaman, style: const TextStyle(color: Colors.black45, fontSize: 12)),
                    const SizedBox(width: 18),
                    if (!yanit)
                      GestureDetector(
                        onTap: yanitla,
                        child: const Text('Yanıtla', style: TextStyle(color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12)),
                      ),
                  ],
                ),
              ],
            ),
          ),
          StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
            stream: likeStream,
            builder: (_, snap) {
              final docs = snap.data?.docs ?? const [];
              final secili = aktifUid != null && docs.any((d) => d.id == aktifUid);
              final sayi = docs.length;
              return GestureDetector(
                onTap: () => begen(yorumId, const []),
                child: Column(
                  children: [
                    Icon(
                      secili ? Icons.favorite : Icons.favorite_border,
                      color: secili ? const Color(0xFFFF2D55) : Colors.black45,
                      size: 22,
                    ),
                    if (sayi > 0)
                      Text('$sayi', style: const TextStyle(fontSize: 11, color: Colors.black45)),
                  ],
                ),
              );
            },
          ),
          IconButton(
            tooltip: 'Yorum seçenekleri',
            onPressed: yorumMenusu,
            icon: const Icon(Icons.more_vert_rounded, color: Colors.black45, size: 21),
            padding: const EdgeInsets.only(left: 2),
            constraints: const BoxConstraints(minWidth: 34, minHeight: 34),
          ),
        ],
      )),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        satir(context, id, veri, zaman),
        if (yanitlar.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(left: 52),
            child: TextButton(
              onPressed: yanitlariAc,
              child: Text(acik ? 'Yanıtları gizle' : '${yanitlar.length} yanıtı görüntüle'),
            ),
          ),
        if (acik)
          ...yanitlar.map(
            (d) => satir(
              context,
              d.id,
              d.data(),
              zamanYaz(d.data()['createdAt']),
              yanit: true,
            ),
          ),
      ],
    );
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
            child: Row(children: [const Logo(kucuk: true), const Spacer(), const Icon(Icons.search_rounded, color: Colors.black, size: 27), const SizedBox(width: 14), const Icon(Icons.tune_rounded, color: Colors.black, size: 25)]),
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
              stream: FirebaseFirestore.instance.collection('live_streams').where('active', isEqualTo: true).limit(20).snapshots(),
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
                          image: (y['coverUrl'] ?? '').toString().isEmpty ? null : DecorationImage(image: CachedNetworkImageProvider((y['coverUrl']).toString()), fit: BoxFit.cover),
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
              stream: FirebaseFirestore.instance.collection('videos').orderBy('createdAt', descending: true).limit(30).snapshots(),
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
                      child: MedyaOnizleme(tur: tur, url: url, thumbnailUrl: (v['thumbnailUrl'] ?? '').toString(), yazi: (v['description'] ?? '').toString(), arkaPlan: i.isEven ? const Color(0xFF292348) : const Color(0xFF16343B)),
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
      Stack(children: [CircleAvatar(radius: 38, backgroundColor: const Color(0xFFF0E8FF), backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto), child: foto.isEmpty ? Text(ad.substring(0, 1).toUpperCase(), style: const TextStyle(color: mor, fontSize: 24, fontWeight: FontWeight.bold)) : null), const Positioned(right: 2, bottom: 2, child: CircleAvatar(radius: 7, backgroundColor: Color(0xFF23D160)))]),
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
  String yorumKitlesi = 'Herkes';
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
      secilen = await ImagePicker().pickImage(source: ImageSource.gallery, imageQuality: 78, maxWidth: 1280);
    }
    if (secilen != null && mounted) setState(() => medya = secilen);
  }

  Future<void> kamerayiAc({required bool video}) async {
    final secilen = video
        ? await ImagePicker().pickVideo(source: ImageSource.camera, maxDuration: const Duration(minutes: 10))
        : await ImagePicker().pickImage(source: ImageSource.camera, imageQuality: 82, maxWidth: 1440);
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
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(28))),
      builder: (c) => Theme(data:ThemeData.light(),child:SafeArea(child: Padding(
        padding: const EdgeInsets.all(22),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Kamerayla oluştur', style: TextStyle(color:Colors.black87,fontSize: 21, fontWeight: FontWeight.w900)),
          const SizedBox(height: 18),
          Row(children: [
            Expanded(child: _buyukSecenek(Icons.photo_camera_rounded, 'Fotoğraf çek', () { Navigator.pop(c); kamerayiAc(video: false); })),
            const SizedBox(width: 12),
            Expanded(child: _buyukSecenek(Icons.videocam_rounded, 'Video çek', () { Navigator.pop(c); kamerayiAc(video: true); })),
          ]),
        ]),
      ))),
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
      'commentAudience': yorumKitlesi,
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
    return ngelxMedyaYukleBytes(
      bytes: await dosya.readAsBytes(),
      kind: klasor == 'videos' ? 'videos' : 'photos',
      ext: uzanti,
      legacyPath: yol,
    );
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
      const kapakUrl = '';
      if (medya != null) {
        medyaUrl = await xDosyasiYukle(medya!, tur == 'video' ? 'videos' : 'photos');
      }
      if (tur == 'photo' && muzik != null) {
        if (await muzik!.length() > 15 * 1024 * 1024) throw Exception('Müzik 15 MB’den küçük olmalı');
        final uzanti = muzik!.name.contains('.') ? muzik!.name.split('.').last.toLowerCase() : 'mp3';
        final yol = 'music/${user.uid}/${DateTime.now().microsecondsSinceEpoch}.$uzanti';
        sesUrl = await ngelxMedyaYukleBytes(
          bytes: await muzik!.readAsBytes(),
          kind: 'music',
          ext: uzanti,
          legacyPath: yol,
        );
      }
      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final adi = (profil.data()?['username'] ?? 'ngelx').toString();
      await FirebaseFirestore.instance.collection('videos').add({
        'ownerId': user.uid,
        'username': adi,
        'type': tur,
        'videoUrl': tur == 'video' ? medyaUrl : '',
        'mediaUrl': medyaUrl,
        'thumbnailUrl': '',
        'audioUrl': sesUrl,
        'description': aciklama.text.trim().isEmpty ? 'NgelX ile paylaşıldı ✨' : aciklama.text.trim(),
        'allowDownload': indirmeyeIzin,
        'allowComments': yorumlaraIzin,
        'commentAudience': yorumKitlesi,
        'allowReshare': yenidenPaylasimaIzin,
        'autoCaptions': otomatikAltyazi,
        'collab': ortakGonderi,
        'privacy': gizlilik,
        'visibleTo':gizlilik=='Yakın arkadaşlar'?List<String>.from(profil.data()?['closeFriends']??const[]):<String>[],
        'hiddenFor':<String>[],
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
    return Theme(
      data: ThemeData.light().copyWith(
        scaffoldBackgroundColor: Colors.white,
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFFF3F5F8),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(18),
            borderSide: BorderSide.none,
          ),
        ),
      ),
      child: ColoredBox(
        color: Colors.white,
        child: SafeArea(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(22,22,22,110),
        children: [
          const Text('Yeni içerik üret', textAlign: TextAlign.center, style: TextStyle(color: Colors.black, fontSize: 27, fontWeight: FontWeight.w900)),
          const SizedBox(height: 8),
          const Text('Fikrini seç, düzenle ve paylaş', textAlign: TextAlign.center, style: TextStyle(color: Colors.black54)),
          const SizedBox(height: 24),
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(color: const Color(0xFFF3F5F8), borderRadius: BorderRadius.circular(22)),
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
          ])),
          const SizedBox(height: 25),
          if (tur != 'text')
            Row(children:[
              Expanded(child:OutlinedButton.icon(
                style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(70), side: const BorderSide(color: mavi), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20))),
                onPressed: medyaSec,
                icon: Icon(tur == 'video' ? Icons.video_library : Icons.photo_library, size: 28),
                label: Text(medya == null ? 'Galeriden seç' : 'Seçildi: ${medya!.name}', maxLines:2, overflow: TextOverflow.ellipsis),
              )),
              const SizedBox(width:10),
              Expanded(child:OutlinedButton.icon(
                style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(70), side: const BorderSide(color: mor), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20))),
                onPressed:()=>kamerayiAc(video:tur=='video'),
                icon:Icon(tur=='video'?Icons.videocam_rounded:Icons.photo_camera_rounded,size:28),
                label:Text(tur=='video'?'Video çek':'Fotoğraf çek'),
              )),
            ]),
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
            subtitle: const Text('Kapalıysa yalnızca sen indirebilirsin.', style: TextStyle(color: Colors.black54)),
            value: indirmeyeIzin,
            onChanged: (v) => setState(() => indirmeyeIzin = v),
          ),
          SwitchListTile(contentPadding: EdgeInsets.zero, title: const Text('Yorumlara izin ver'), value: yorumlaraIzin, onChanged: (v) => setState(() => yorumlaraIzin = v)),
          if(yorumlaraIzin)DropdownButtonFormField<String>(
            initialValue:yorumKitlesi,
            decoration:const InputDecoration(labelText:'Kimler yorum yapabilir?',prefixIcon:Icon(Icons.mode_comment_outlined)),
            items:const ['Herkes','Arkadaşlar','Takip ettiklerim','Kimse'].map((e)=>DropdownMenuItem(value:e,child:Text(e))).toList(),
            onChanged:(v)=>setState(()=>yorumKitlesi=v??'Herkes'),
          ),
          if(yorumlaraIzin)const SizedBox(height:10),
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
          if (yukleniyor)
            const Center(child:Column(children:[CircularProgressIndicator(color:mor),SizedBox(height:10),Text('İçerik yayınlanıyor...',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))]))
          else
            Container(
              decoration:BoxDecoration(
                gradient:const LinearGradient(colors:[Color(0xFF22D3EE),Color(0xFF7C3AED)]),
                borderRadius:BorderRadius.circular(18),
                boxShadow:const [BoxShadow(color:Color(0x33000000),blurRadius:12,offset:Offset(0,5))],
              ),
              child:FilledButton.icon(
                style:FilledButton.styleFrom(
                  minimumSize:const Size.fromHeight(58),
                  backgroundColor:Colors.transparent,
                  shadowColor:Colors.transparent,
                  foregroundColor:Colors.white,
                  shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
                ),
                onPressed:yayinla,
                icon:const Icon(Icons.publish_rounded,color:Colors.white),
                label:const Text('NgelX’te Yayınla',style:TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900)),
              ),
            ),
          const SizedBox(height: 12),
          const Text('Video ve fotoğraf en fazla 50 MB, müzik en fazla 15 MB.', textAlign: TextAlign.center, style: TextStyle(color: Colors.black45, fontSize: 12)),
        ],
      ),
    )));
  }

  Widget _bolumBasligi(String yazi) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Text(yazi, style: const TextStyle(color: Colors.black87, fontSize: 18, fontWeight: FontWeight.w900)),
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
        decoration: BoxDecoration(color: const Color(0xFFF3F5F8), borderRadius: BorderRadius.circular(18)),
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(ikon, color: mavi), const SizedBox(height: 6), Text(yazi, style: const TextStyle(color: Colors.black87, fontSize: 12, fontWeight: FontWeight.bold))]),
      ),
    ),
  );

  Widget _buyukSecenek(IconData ikon, String yazi, VoidCallback tiklama) => InkWell(
    borderRadius: BorderRadius.circular(20),
    onTap: tiklama,
    child: Container(
      padding: const EdgeInsets.symmetric(vertical: 24),
      decoration: BoxDecoration(color: const Color(0xFFF3F5F8), borderRadius: BorderRadius.circular(20)),
      child: Column(children: [Icon(ikon, color: mavi, size: 34), const SizedBox(height: 8), Text(yazi, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.bold))]),
    ),
  );

  Widget _turButonu(String deger, IconData ikon, String yazi) {
    final secili = tur == deger;
    return Expanded(child: GestureDetector(
      onTap: () => setState(() { tur = deger; medya = null; muzik = null; }),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(gradient: secili ? const LinearGradient(colors: [mavi, mor]) : null, color: secili ? null : const Color(0xFFF3F5F8), borderRadius: BorderRadius.circular(17)),
        child: Column(children: [Icon(ikon, color: secili ? Colors.black : Colors.black54), const SizedBox(height: 5), Text(yazi, style: TextStyle(color: secili ? Colors.black : Colors.black54, fontWeight: FontWeight.bold))]),
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
      final url = await ngelxMedyaYukleBytes(
        bytes: baytlar,
        kind: 'videos',
        ext: uzanti,
        legacyPath: yol,
      );
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
  Set<String> arsivSohbetler={};
  Set<String> sabitSohbetler={};
  Set<String> arkadaslar={};
  final sohbetAra=TextEditingController();
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _kullaniciCache={};
  Future<DocumentSnapshot<Map<String,dynamic>>> _kullaniciGetir(String id)=>
      _kullaniciCache.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('users').doc(id).get());
  String sohbetSorgu='';
  String filtre='Tümü';

  Future<void> tercihleriGetir() async {
    final ben=uid;if(ben==null)return;
    final d=await FirebaseFirestore.instance.collection('users').doc(ben).get();
    final veri=d.data()??<String,dynamic>{},sessiz=Set<String>.from(List<dynamic>.from(veri['mutedChats']??const[])),sureler=Map<String,dynamic>.from(veri['mutedChatUntil']??{}),suresiDolan=<String>[];
    for(final id in sessiz){final tarih=DateTime.tryParse((sureler[id]??'').toString());if(tarih!=null&&tarih.isBefore(DateTime.now().toUtc()))suresiDolan.add(id);}
    if(suresiDolan.isNotEmpty){sessiz.removeAll(suresiDolan);final guncelle=<String,dynamic>{'mutedChats':FieldValue.arrayRemove(suresiDolan)};for(final id in suresiDolan)guncelle['mutedChatUntil.$id']=FieldValue.delete();await d.reference.update(guncelle);}
    if(!mounted)return;
    setState((){
      engellenenler=Set<String>.from(List<dynamic>.from(veri['blocked']??const[]));
      sessizSohbetler=sessiz;
      arsivSohbetler=Set<String>.from(List<dynamic>.from(veri['archivedChats']??const[]));
      sabitSohbetler=Set<String>.from(List<dynamic>.from(veri['pinnedChats']??const[]));
      arkadaslar=Set<String>.from(List<dynamic>.from(veri['friends']??const[]));
    });
  }

  @override void initState(){super.initState();tercihleriGetir();}
  @override void dispose(){sohbetAra.dispose();super.dispose();}

  Future<void> sessizeAl(String chatId,bool sessiz) async {
    final ben=uid;if(ben==null)return;
    await FirebaseFirestore.instance.collection('users').doc(ben).set({'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true));
    if(!sessiz)await FirebaseFirestore.instance.collection('users').doc(ben).update({'mutedChatUntil.$chatId':FieldValue.delete()});
    if(mounted)setState(()=>sessiz?sessizSohbetler.add(chatId):sessizSohbetler.remove(chatId));
  }

  Future<void> sessizeAlMenusu(String chatId) async {
    final secim=await showModalBottomSheet<Duration?>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      const ListTile(title:Text('Bildirimleri sessize al',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
      for(final e in const [('1 saat',Duration(hours:1)),('8 saat',Duration(hours:8)),('1 hafta',Duration(days:7)),('Süresiz',Duration(days:36500))])
        ListTile(title:Text(e.$1,style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,e.$2)),
      TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Vazgeç')),
    ]))));
    if(secim==null)return;
    final ben=uid;if(ben==null)return;
    final kullanici=FirebaseFirestore.instance.collection('users').doc(ben);
    await kullanici.set({'mutedChats':FieldValue.arrayUnion([chatId])},SetOptions(merge:true));
    await kullanici.update({'mutedChatUntil.$chatId':DateTime.now().add(secim).toUtc().toIso8601String()});
    if(mounted)setState(()=>sessizSohbetler.add(chatId));
  }

  Future<void> tumunuOkunduYap() async {
    final ben=uid;if(ben==null)return;
    final q=await FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).get();
    final batch=FirebaseFirestore.instance.batch();
    for(final d in q.docs){if((d.data()['unread_$ben']??0)!=0)batch.set(d.reference,{'unread_$ben':0},SetOptions(merge:true));}
    final bildirimler=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).get();
    for(final d in bildirimler.docs){if(d.data()['read']!=true)batch.update(d.reference,{'read':true});}
    await batch.commit();
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Tüm bildirimler okundu olarak işaretlendi.')));
  }

  Future<void> sohbetiAc(String chatId,Widget sayfa) async {
    // Okundu yazısı ekran geçişini asla bekletmez. Ağ/kural hatası olsa bile
    // sohbet anında açılır; sayaç yazısı arka planda en fazla 5 sn denenir.
    if(!mounted)return;
    final ben=uid;
    if(ben!=null){
      unawaited(
        FirebaseFirestore.instance.collection('chats').doc(chatId).set(
          {'unread_$ben':0},
          SetOptions(merge:true),
        ).timeout(const Duration(seconds:5)).catchError((_){ }),
      );
    }
    await Navigator.push(context,MaterialPageRoute(builder:(_)=>sayfa));
  }

  Future<void> sohbetTercihi(String alan,String chatId,bool ekle) async {
    final ben=uid;if(ben==null)return;
    await FirebaseFirestore.instance.collection('users').doc(ben).set({alan:ekle?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true));
    if(!mounted)return;
    setState((){final hedef=alan=='archivedChats'?arsivSohbetler:sabitSohbetler;ekle?hedef.add(chatId):hedef.remove(chatId);});
  }

  Future<void> sohbetMenusu(BuildContext context,String id) async {
    final sessiz=sessizSohbetler.contains(id);
    await showModalBottomSheet(context:context,backgroundColor:Colors.white,showDragHandle:true,shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      ListTile(leading:Icon(sabitSohbetler.contains(id)?Icons.push_pin:Icons.push_pin_outlined,color:mor),title:Text(sabitSohbetler.contains(id)?'Sabitlemeyi kaldır':'Sohbeti sabitle'),onTap:(){Navigator.pop(c);sohbetTercihi('pinnedChats',id,!sabitSohbetler.contains(id));}),
      ListTile(leading:const Icon(Icons.archive_outlined,color:Colors.blue),title:const Text('Arşivle'),onTap:(){Navigator.pop(c);sohbetTercihi('archivedChats',id,true);}),
      ListTile(leading:Icon(sessiz?Icons.notifications_active_outlined:Icons.notifications_off_outlined),title:Text(sessiz?'Sessizi kaldır':'Sessize al'),onTap:(){Navigator.pop(c);sessiz?sessizeAl(id,false):sessizeAlMenusu(id);}),
      ListTile(leading:const Icon(Icons.mark_chat_read_outlined,color:Colors.green),title:const Text('Okundu olarak işaretle'),onTap:()async{Navigator.pop(c);final ben=uid;if(ben!=null)await FirebaseFirestore.instance.collection('chats').doc(id).set({'unread_$ben':0},SetOptions(merge:true));}),
      ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:const Text('Sohbeti listemden kaldır',style:TextStyle(color:Colors.red)),onTap:(){Navigator.pop(c);sohbetSil(context,id);}),
    ]))));
  }

  Future<void> sohbetSil(BuildContext context,String id) async {
    final ben=uid;if(ben==null)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sohbet kaldırılsın mı?'),content:const Text('Bu sohbet yalnızca senin gelen kutundan kaldırılacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),TextButton(onPressed:()=>Navigator.pop(c,true),child:const Text('KALDIR',style:TextStyle(color:Colors.red)))]))??false;
    if(ok)await FirebaseFirestore.instance.collection('chats').doc(id).set({'hiddenFor':FieldValue.arrayUnion([ben])},SetOptions(merge:true));
  }

  @override Widget build(BuildContext context){
    final ben=uid;
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),child:ColoredBox(color:Colors.white,child:SafeArea(child:Column(children:[
      Padding(
        padding:const EdgeInsets.fromLTRB(18,14,8,8),
        child:Row(children:[
          Expanded(
            child:FittedBox(
              fit:BoxFit.scaleDown,
              alignment:Alignment.centerLeft,
              child:Row(mainAxisSize:MainAxisSize.min,children:[
                const Text('Gelen Kutusu',style:TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),
                const SizedBox(width:2),
                IconButton(constraints:const BoxConstraints.tightFor(width:36),padding:EdgeInsets.zero,tooltip:'Tümünü okundu yap',onPressed:ben==null?null:tumunuOkunduYap,icon:const Icon(Icons.done_all_rounded,color:Color(0xFF27C66F))),
              ]),
            ),
          ),
          IconButton(constraints:const BoxConstraints.tightFor(width:38),padding:EdgeInsets.zero,tooltip:'Arşiv',onPressed:ben==null?null:()async{await Navigator.push(context,MaterialPageRoute(builder:(_)=>ArsivSohbetlerPage(uid:ben)));await tercihleriGetir();},icon:const Icon(Icons.archive_outlined,color:Colors.black54)),
          IconButton(constraints:const BoxConstraints.tightFor(width:38),padding:EdgeInsets.zero,tooltip:'Grup oluştur',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GrupOlusturPage())),icon:const Icon(Icons.group_add_rounded,color:mor,size:27)),
          IconButton(constraints:const BoxConstraints.tightFor(width:38),padding:EdgeInsets.zero,tooltip:'Yeni sohbet',onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const YeniSohbetPage())),icon:const Icon(Icons.person_add_alt_1,color:mavi,size:27)),
        ]),
      ),
      Padding(padding:const EdgeInsets.fromLTRB(16,4,16,10),child:TextField(controller:sohbetAra,onChanged:(v)=>setState(()=>sohbetSorgu=v.trim().toLowerCase()),style:const TextStyle(color:Colors.black87),decoration:InputDecoration(hintText:'Sohbetlerde ara',hintStyle:const TextStyle(color:Colors.black45),prefixIcon:const Icon(Icons.search,color:Colors.black45),filled:true,fillColor:const Color(0xFFF3F4F7),border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none)))),
      Padding(padding:const EdgeInsets.symmetric(horizontal:8),child:Row(children:['Tümü','Okunmamış','Arkadaşlar','Gruplar'].map((f)=>Expanded(child:Padding(padding:const EdgeInsets.symmetric(horizontal:2),child:ChoiceChip(labelPadding:const EdgeInsets.symmetric(horizontal:2),label:Center(child:FittedBox(fit:BoxFit.scaleDown,child:Text(f,maxLines:1))),selected:filtre==f,selectedColor:mor,labelStyle:TextStyle(color:filtre==f?Colors.white:Colors.black87,fontWeight:FontWeight.w700),backgroundColor:const Color(0xFFF1F2F5),side:BorderSide.none,onSelected:(_)=>setState(()=>filtre=f))))).toList())),
      StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:ben==null?null:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:ben).limit(60).snapshots(),builder:(_,s){final okunmamis=(s.data?.docs??[]).where((d)=>d.data()['read']!=true).length;return Container(margin:const EdgeInsets.fromLTRB(16,8,16,5),decoration:BoxDecoration(color:const Color(0xFFF5EFFF),borderRadius:BorderRadius.circular(20)),child:ListTile(leading:const CircleAvatar(backgroundColor:Color(0xFFE5D5FF),child:Icon(Icons.favorite,color:mor)),title:const Text('Aktivite',style:TextStyle(color:Colors.black,fontWeight:FontWeight.w900)),subtitle:const Text('Beğeniler, yorumlar ve güvenlik bildirimleri',style:TextStyle(color:Colors.black54)),trailing:okunmamis==0?const Icon(Icons.chevron_right,color:Colors.black45):Badge(label:Text('$okunmamis'),child:const Icon(Icons.chevron_right,color:Colors.black45)),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()))));}),
      Container(margin:const EdgeInsets.fromLTRB(16,5,16,8),decoration:BoxDecoration(color:const Color(0xFFEDF7FF),borderRadius:BorderRadius.circular(20)),child:ListTile(leading:const CircleAvatar(backgroundColor:Color(0xFFD8ECFF),child:Icon(Icons.chat_bubble_rounded,color:Colors.blue)),title:const Text('Mesaj İstekleri',style:TextStyle(color:Colors.black,fontWeight:FontWeight.w900)),subtitle:const Text('Seni takip etmeyenlerden gelen mesajlar',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black45),onTap:ben==null?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>MesajIstekleriPage(uid:ben))))),
      Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:ben==null?null:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:ben).limit(60).snapshots(),
        builder:(_,s){
          final docs=(s.data?.docs??[]).where((d){final v=d.data();if(List<String>.from(v['hiddenFor']??const[]).contains(ben)||arsivSohbetler.contains(d.id))return false;final members=List<String>.from(v['members']??const[]),grup=v['isGroup']==true||members.length>2;final unread=(v['unread_$ben']??0) as int;if(filtre=='Okunmamış'&&unread==0)return false;if(filtre=='Gruplar'&&!grup)return false;if(!grup){final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');final gelenIstek=v['requestRecipientUid']==ben&&v['requestAccepted_$ben']!=true&&!arkadaslar.contains(other);if(gelenIstek)return false;if(filtre=='Arkadaşlar'&&!arkadaslar.contains(other))return false;}else if(filtre=='Arkadaşlar')return false;final son='${v['groupName']??''} ${v['lastMessage']??''}'.toLowerCase();return sohbetSorgu.isEmpty||son.contains(sohbetSorgu);}).toList()..sort((a,b){final ap=sabitSohbetler.contains(a.id),bp=sabitSohbetler.contains(b.id);if(ap!=bp)return ap?-1:1;final at=a.data()['updatedAt'] as Timestamp?,bt=b.data()['updatedAt'] as Timestamp?;return (bt?.millisecondsSinceEpoch??0).compareTo(at?.millisecondsSinceEpoch??0);});
          if(docs.isEmpty)return const Center(child:Text('Bu bölümde henüz sohbet yok.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)));
          return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){
            final d=docs[i],v=d.data(),members=List<String>.from(v['members']??[]);
            final grup=v['isGroup']==true||members.length>2;
            if(grup){final ad=(v['groupName']??'Grup sohbeti').toString(),foto=(v['groupPhotoUrl']??'').toString(),unread=(v['unread_$ben']??0) as int;return ListTile(onTap:()=>sohbetiAc(d.id,GrupSohbetPage(chatId:d.id,ad:ad,foto:foto)),onLongPress:()=>sohbetMenusu(context,d.id),leading:CircleAvatar(backgroundColor:const Color(0xFFE9DDFF),backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups,color:mor):null),title:Text(ad,style:TextStyle(color:Colors.black87,fontWeight:unread>0?FontWeight.w900:FontWeight.w700)),subtitle:Text((v['lastMessage']??'Grup oluşturuldu').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)),trailing:Wrap(crossAxisAlignment:WrapCrossAlignment.center,children:[if(sabitSohbetler.contains(d.id))const Icon(Icons.push_pin,size:16,color:mor),if(sessizSohbetler.contains(d.id))const Icon(Icons.volume_off,size:18,color:Colors.black38),if(unread>0)Badge(label:Text('$unread'))]));}
            final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');
            if(engellenenler.contains(other))return const SizedBox.shrink();
            return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:_kullaniciGetir(other),builder:(_,u){
              final p=u.data?.data()??{};
              if(p['deactivated']==true||List<String>.from(p['blocked']??const[]).contains(ben))return const SizedBox.shrink();
              final hamTakmalar=v['nicknames'],takmalar=hamTakmalar is Map?Map<String,dynamic>.from(hamTakmalar):<String,dynamic>{},takma=(ben==null?'':(takmalar[ben]??'').toString()).trim(),profilAdi=(p['displayName']??p['username']??'NgelX').toString(),gorunenAd=takma.isNotEmpty?takma:profilAdi;
              final aranan='$gorunenAd ${p['displayName']??''} ${p['username']??''} ${v['lastMessage']??''}'.toLowerCase();
              if(sohbetSorgu.isNotEmpty&&!aranan.contains(sohbetSorgu))return const SizedBox.shrink();
              final unread=(v['unread_$ben']??0) as int;
              final sessiz=sessizSohbetler.contains(d.id);
              return ListTile(
                onTap:()=>sohbetiAc(d.id,SohbetPage(chatId:d.id,digerUid:other,ad:gorunenAd,foto:(p['photoUrl']??'').toString())),
                onLongPress:()=>sohbetMenusu(context,d.id),
                leading:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:CachedNetworkImageProvider(p['photoUrl'])),
                title:Text(gorunenAd,style:TextStyle(fontWeight:unread>0?FontWeight.w900:FontWeight.w700,color:Colors.black87)),
                subtitle:Text((v['lastMessage']??'Yeni sohbet').toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54)),
                trailing:Wrap(crossAxisAlignment:WrapCrossAlignment.center,children:[if(sabitSohbetler.contains(d.id))const Icon(Icons.push_pin,size:16,color:mor),if(sessiz)const Icon(Icons.volume_off,size:18,color:Colors.black38),if(unread>0)Badge(label:Text('$unread'))]),
              );
            });
          });
        },
      )),
    ]))));
  }
}

class ArsivSohbetlerPage extends StatefulWidget {
  final String uid;
  const ArsivSohbetlerPage({super.key, required this.uid});
  @override State<ArsivSohbetlerPage> createState() => _ArsivSohbetlerPageState();
}

class _ArsivSohbetlerPageState extends State<ArsivSohbetlerPage> {
  Future<List<String>> arsivGetir() async {
    final d = await FirebaseFirestore.instance.collection('users').doc(widget.uid).get();
    return List<String>.from(d.data()?['archivedChats'] ?? const []);
  }

  Future<void> geriAl(String id) async {
    await FirebaseFirestore.instance.collection('users').doc(widget.uid).set(
      {'archivedChats': FieldValue.arrayRemove([id])}, SetOptions(merge: true));
    if (mounted) setState(() {});
  }

  @override Widget build(BuildContext context) => Theme(
    data: ThemeData.light(),
    child: Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(title: const Text('Arşivlenen sohbetler', style: TextStyle(fontWeight: FontWeight.w900))),
      body: FutureBuilder<List<String>>(
        future: arsivGetir(),
        builder: (_, s) {
          final ids = s.data ?? [];
          if (s.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: mor));
          if (ids.isEmpty) return const Center(child: Text('Arşivlenmiş sohbetin yok.', style: TextStyle(color: Colors.black54)));
          return ListView.separated(
            padding: const EdgeInsets.all(12), itemCount: ids.length,
            separatorBuilder: (_, __) => const Divider(),
            itemBuilder: (_, i) => FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              future: FirebaseFirestore.instance.collection('chats').doc(ids[i]).get(),
              builder: (_, c) {
                final v = c.data?.data() ?? <String,dynamic>{};
                final members = List<String>.from(v['members'] ?? const []);
                final grup = v['isGroup'] == true || members.length > 2;
                if (grup) return ListTile(
                  leading: const CircleAvatar(backgroundColor: Color(0xFFE9DDFF), child: Icon(Icons.groups, color: mor)),
                  title: Text((v['groupName'] ?? 'Grup sohbeti').toString()), subtitle: Text((v['lastMessage'] ?? '').toString()),
                  trailing: IconButton(tooltip: 'Arşivden çıkar', onPressed: () => geriAl(ids[i]), icon: const Icon(Icons.unarchive_outlined, color: mor)),
                );
                final other = members.firstWhere((x) => x != widget.uid, orElse: () => widget.uid);
                return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  future: FirebaseFirestore.instance.collection('users').doc(other).get(),
                  builder: (_, u) {
                    final p = u.data?.data() ?? <String,dynamic>{};
                    final foto = (p['photoUrl'] ?? '').toString();
                    return ListTile(
                      leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto)),
                      title: Text((p['displayName'] ?? p['username'] ?? 'NgelX').toString(), style: const TextStyle(fontWeight: FontWeight.w800)),
                      subtitle: Text((v['lastMessage'] ?? '').toString()),
                      trailing: IconButton(tooltip: 'Arşivden çıkar', onPressed: () => geriAl(ids[i]), icon: const Icon(Icons.unarchive_outlined, color: mor)),
                    );
                  },
                );
              },
            ),
          );
        },
      ),
    ),
  );
}

class MesajIstekleriPage extends StatelessWidget {
  final String uid;
  const MesajIstekleriPage({super.key, required this.uid});
  @override Widget build(BuildContext context) => Theme(
    data: ThemeData.light(),
    child: Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(title: const Text('Mesaj istekleri', style: TextStyle(fontWeight: FontWeight.w900))),
      body: FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        future: FirebaseFirestore.instance.collection('users').doc(uid).get(),
        builder: (_, me) {
          final arkadaslar = Set<String>.from(List<dynamic>.from(me.data?.data()?['friends'] ?? const []));
          return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream: FirebaseFirestore.instance.collection('chats').where('members', arrayContains: uid).limit(60).snapshots(),
            builder: (_, s) {
              final docs = (s.data?.docs ?? []).where((d) {
                final v=d.data(), m=List<String>.from(v['members'] ?? const []);
                if(v['isGroup']==true || m.length!=2) return false;
                final other=m.firstWhere((x)=>x!=uid,orElse:()=>uid);
                final hedef=(v['requestRecipientUid']??uid).toString();
                return hedef==uid && !arkadaslar.contains(other) && v['requestAccepted_$uid']!=true && v['requestRejected_$uid']!=true;
              }).toList();
              if(docs.isEmpty) return const Center(child: Text('Yeni mesaj isteğin yok.', style: TextStyle(color: Colors.black54)));
              return ListView.builder(
                padding: const EdgeInsets.all(12), itemCount: docs.length,
                itemBuilder: (_, i) {
                  final d=docs[i], v=d.data(), m=List<String>.from(v['members'] ?? const []);
                  final other=m.firstWhere((x)=>x!=uid,orElse:()=>uid);
                  return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                    future: FirebaseFirestore.instance.collection('users').doc(other).get(),
                    builder: (_, u) {
                      final p=u.data?.data() ?? <String,dynamic>{}, foto=(p['photoUrl'] ?? '').toString();
                      final ad=(p['displayName'] ?? p['username'] ?? 'NgelX').toString();
                      Future<void> kabul()async{await d.reference.set({'requestAccepted_$uid':true,'requestRejected_$uid':false},SetOptions(merge:true));if(context.mounted)Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:d.id,digerUid:other,ad:ad,foto:foto)));}
                      return Card(child: ListTile(
                        onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>MesajIstegiOnizlemePage(chatId:d.id,digerUid:other,ad:ad,foto:foto,uid:uid))),
                        leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto)),
                        title: Text(ad, style: const TextStyle(fontWeight: FontWeight.w800)),
                        subtitle: Text((v['lastMessage'] ?? 'Mesaj isteği').toString()),
                        trailing: TextButton(onPressed:kabul,child:const Text('Kabul et')),
                      ));
                    },
                  );
                },
              );
            },
          );
        },
      ),
    ),
  );
}

class MesajIstegiOnizlemePage extends StatelessWidget{
  final String chatId,digerUid,ad,foto,uid;
  const MesajIstegiOnizlemePage({super.key,required this.chatId,required this.digerUid,required this.ad,required this.foto,required this.uid});
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:Text(ad)),body:Column(children:[
    Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(chatId).collection('messages').orderBy('createdAt').limitToLast(100).snapshots(),builder:(_,s)=>ListView(padding:const EdgeInsets.all(16),children:(s.data?.docs??[]).map((d){final v=d.data(),metin=(v['text']??'').toString(),photo=v['type']=='photo';return Align(alignment:v['senderId']==uid?Alignment.centerRight:Alignment.centerLeft,child:Container(margin:const EdgeInsets.symmetric(vertical:4),padding:EdgeInsets.all(photo?4:12),constraints:const BoxConstraints(maxWidth:280),decoration:BoxDecoration(color:const Color(0xFFF0F1F4),borderRadius:BorderRadius.circular(18)),child:photo?ClipRRect(borderRadius:BorderRadius.circular(15),child:Image.network((v['mediaUrl']??'').toString())):Text(metin)));}).toList()))),
    SafeArea(top:false,child:Padding(padding:const EdgeInsets.all(12),child:Row(children:[Expanded(child:OutlinedButton(onPressed:()async{await FirebaseFirestore.instance.collection('chats').doc(chatId).set({'requestRejected_$uid':true,'hiddenFor':FieldValue.arrayUnion([uid])},SetOptions(merge:true));if(context.mounted)Navigator.pop(context);},child:const Text('Reddet'))),const SizedBox(width:8),Expanded(child:OutlinedButton(style:OutlinedButton.styleFrom(foregroundColor:Colors.red),onPressed:()async{await kullaniciyiEngelle(context,digerUid);await FirebaseFirestore.instance.collection('chats').doc(chatId).set({'requestRejected_$uid':true,'hiddenFor':FieldValue.arrayUnion([uid])},SetOptions(merge:true));if(context.mounted)Navigator.pop(context);},child:const Text('Engelle'))),const SizedBox(width:8),Expanded(child:FilledButton(onPressed:()async{await FirebaseFirestore.instance.collection('chats').doc(chatId).set({'requestAccepted_$uid':true},SetOptions(merge:true));if(context.mounted)Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:chatId,digerUid:digerUid,ad:ad,foto:foto)));},child:const Text('Kabul et')))]))),
  ])));
}

class GrupOlusturPage extends StatefulWidget{const GrupOlusturPage({super.key});@override State<GrupOlusturPage> createState()=>_GrupOlusturPageState();}
class _GrupOlusturPageState extends State<GrupOlusturPage>{
  final ad=TextEditingController(),arama=TextEditingController();
  final Set<String> secilen={};
  final List<QueryDocumentSnapshot<Map<String,dynamic>>> adaylar=[];
  String sorgu='';
  String? yuklemeHatasi;
  XFile? foto;
  bool kaydediliyor=false,izinlerYukleniyor=true;
  String? _olusturulanGrupId;

  @override void initState(){super.initState();izinliKisileriGetir();}
  @override void dispose(){ad.dispose();arama.dispose();super.dispose();}

  Future<void> izinliKisileriGetir()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null){if(mounted)setState(()=>izinlerYukleniyor=false);return;}
    try{
      final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get().timeout(const Duration(seconds:8));
      final v=d.data()??<String,dynamic>{};
      final ids=<String>{...List<String>.from(v['following']??const[]),...List<String>.from(v['friends']??const[])}..remove(u.uid);
      final liste=ids.toList();
      final sorgular=<Future<QuerySnapshot<Map<String,dynamic>>>>[];
      for(int i=0;i<liste.length;i+=30){
        final son=(i+30<liste.length)?i+30:liste.length;
        final parca=liste.sublist(i,son);
        if(parca.isEmpty)continue;
        sorgular.add(FirebaseFirestore.instance.collection('users')
          .where(FieldPath.documentId,whereIn:parca)
          .get()
          .timeout(const Duration(seconds:8)));
      }
      final sonuclar=await Future.wait(sorgular).timeout(const Duration(seconds:12));
      final bulunan=<QueryDocumentSnapshot<Map<String,dynamic>>>[
        for(final q in sonuclar)...q.docs.where((x)=>x.data()['deactivated']!=true),
      ];
      if(mounted)setState((){adaylar..clear()..addAll(bulunan);izinlerYukleniyor=false;yuklemeHatasi=null;});
    }catch(e){
      if(mounted)setState((){izinlerYukleniyor=false;yuklemeHatasi='Kişiler yüklenemedi. İnternet bağlantını kontrol edip tekrar dene.';});
    }
  }
  Future<void> olustur()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null||kaydediliyor)return;
    final grupAdi=ad.text.trim();
    if(grupAdi.length<2){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup adı en az 2 karakter olmalı.')));return;}
    if(grupAdi.length>16){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup adı en fazla 16 karakter olabilir.')));return;}
    if(secilen.isEmpty){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup için en az 1 kişi seç.')));return;}
    if(secilen.length>59){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yönetici dahil grupta en fazla 60 üye olabilir.')));return;}
    setState(()=>kaydediliyor=true);
    try{
      String fotoUrl='';
      bool fotoAtlandi=false;
      if(foto!=null){
        try{
          final bytes=await foto!.readAsBytes().timeout(const Duration(seconds:8));
          final yol='groups/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';
          fotoUrl=await ngelxMedyaYukleBytes(
            bytes: bytes,
            kind: 'groups',
            ext: 'jpg',
            legacyPath: yol,
          ).timeout(const Duration(seconds:12));
        }catch(_){
          fotoAtlandi=true;
          fotoUrl='';
        }
      }
      _olusturulanGrupId??=FirebaseFirestore.instance.collection('chats').doc().id;
      final ref=FirebaseFirestore.instance.collection('chats').doc(_olusturulanGrupId);
      await ref.set({
        'isGroup':true,
        'groupName':grupAdi,
        'groupPhotoUrl':fotoUrl,
        'members':[u.uid,...secilen],
        'admins':[u.uid],
        'moderators':<String>[],
        'createdBy':u.uid,
        'createdAt':FieldValue.serverTimestamp(),
        'updatedAt':FieldValue.serverTimestamp(),
        'lastMessage':'Grup oluşturuldu',
        'hiddenFor':<String>[],
        'maxMembers':60,
        'onlyAdminsCanEdit':true,
      }).timeout(const Duration(seconds:12));
      // Sohbet ekranını, grup belgesi Firestore'a kesin olarak yazıldıktan sonra aç.
      // Böylece messages alt koleksiyonu için üyelik kuralı ilk açılışta yarış durumuna girmez.
      if(mounted){
        if(fotoAtlandi)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Medya hizmeti kullanılamıyor. Grup fotoğrafsız oluşturuldu.')));
        Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:ref.id,ad:grupAdi,foto:fotoUrl)));
      }
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup oluşturulamadı. Lütfen tekrar dene.')));
    }finally{
      if(mounted)setState(()=>kaydediliyor=false);
    }
  }
  @override Widget build(BuildContext context){return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Yeni grup',style:TextStyle(fontWeight:FontWeight.w900)),actions:[TextButton(onPressed:kaydediliyor?null:olustur,child:const Text('Oluştur',style:TextStyle(fontWeight:FontWeight.w900)))]),body:Column(children:[
  Padding(padding:const EdgeInsets.all(18),child:Row(children:[GestureDetector(onTap:()async{final x=await ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:78,maxWidth:1024);if(x!=null&&mounted)setState(()=>foto=x);},child:CircleAvatar(radius:34,backgroundColor:const Color(0xFFE9DDFF),backgroundImage:foto==null?null:FileImage(File(foto!.path)),child:foto==null?const Icon(Icons.add_a_photo,color:mor):null)),const SizedBox(width:14),Expanded(child:TextField(controller:ad,maxLength:16,onChanged:(_)=>setState((){}),style:const TextStyle(color:Colors.black87),decoration:InputDecoration(labelText:'Grup adı',hintText:'Grubuna bir ad ver',counterText:'${ad.text.characters.length}/16 karakter')))])),
    Padding(padding:const EdgeInsets.symmetric(horizontal:18),child:TextField(controller:arama,onChanged:(v)=>setState(()=>sorgu=v.toLowerCase()),style:const TextStyle(color:Colors.black87),decoration:const InputDecoration(prefixIcon:Icon(Icons.search),hintText:'Gruba kişi ekle'))),
    Padding(padding:const EdgeInsets.fromLTRB(18,12,18,5),child:Align(alignment:Alignment.centerLeft,child:Text('${secilen.length} kişi seçildi • ${secilen.length+1}/60 üye',style:const TextStyle(color:mor,fontWeight:FontWeight.bold)))),
    Expanded(
      child:izinlerYukleniyor
        ? const Center(child:CircularProgressIndicator(color:mor))
        : yuklemeHatasi!=null
          ? Center(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
              const Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:42),
              const SizedBox(height:10),
              Text(yuklemeHatasi!,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54)),
              const SizedBox(height:12),
              OutlinedButton.icon(onPressed:(){setState(()=>izinlerYukleniyor=true);izinliKisileriGetir();},icon:const Icon(Icons.refresh),label:const Text('Yeniden dene')),
            ])))
          : Builder(builder:(_){
              final docs=adaylar.where((d){
                final v=d.data();
                final isim='${v['displayName']??''} ${v['username']??''}'.toLowerCase();
                return sorgu.isEmpty||isim.contains(sorgu);
              }).toList();
              if(docs.isEmpty)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Text('Gruba ekleyebileceğin takip veya arkadaş bulunamadı.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54))));
              return ListView.builder(
                itemCount:docs.length,
                itemBuilder:(_,i){
                  final d=docs[i],v=d.data(),isim=(v['displayName']??v['username']??'Kullanıcı').toString(),pf=(v['photoUrl']??'').toString(),secili=secilen.contains(d.id);
                  return CheckboxListTile(
                    value:secili,
                    onChanged:(x){
                      if(x==true&&!secili&&secilen.length>=59){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yönetici dahil en fazla 60 üye eklenebilir.')));return;}
                      setState(()=>x==true?secilen.add(d.id):secilen.remove(d.id));
                    },
                    secondary:CircleAvatar(backgroundImage:pf.isEmpty?null:CachedNetworkImageProvider(pf),child:pf.isEmpty?const Icon(Icons.person):null),
                    title:Text(isim,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
                    subtitle:Text('@${v['username']??'ngelx'}',style:const TextStyle(color:Colors.black54)),
                    activeColor:mor,
                  );
                },
              );
            }),
    ),
  ])));}
}

class GrupSohbetPage extends StatefulWidget{final String chatId,ad,foto;const GrupSohbetPage({super.key,required this.chatId,required this.ad,this.foto=''});@override State<GrupSohbetPage> createState()=>_GrupSohbetPageState();}
class _GrupSohbetPageState extends State<GrupSohbetPage>{
  final mesaj=TextEditingController(),liste=ScrollController();
  final List<Map<String,String>> mentionOnerileri=[];
  final Set<String> etiketlenenUidler={};
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _uyeProfilCache={};
  Timer? mentionZamanlayici,_mesajBeklemeZamanlayici;
  List<Map<String,String>>? _mentionUyeleri;
  late Stream<QuerySnapshot<Map<String,dynamic>>> _mesajAkisi;
  late final Stream<DocumentSnapshot<Map<String,dynamic>>> _grupAkisi;
  bool aramaBaslatiliyor=false,mesajGonderiliyor=false,_okunduYaziliyor=false,_ilkMesajKaydirma=true,_mesajBeklemeBitti=false;
  DateTime? _sonOkunduKontrolu;
  String? yanitlananMesajId,yanitlananMetin;
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;
  DocumentReference<Map<String,dynamic>> get chatRef=>FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
  Future<DocumentSnapshot<Map<String,dynamic>>> _uyeGetir(String id)=>_uyeProfilCache.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('users').doc(id).get());
  @override void initState(){
    super.initState();
    _grupAkisi=chatRef.snapshots();
    // Bütün grup geçmişini her açılışta indirmek uygulamayı kilitliyordu.
    // En yeni 100 mesaj ilk ekran için yeterli; eski içerikler medya ve arama
    // sayfalarından ayrıca alınır.
    _mesajAkisiniYenile();
    unawaited(_okunduIsaretle());
  }
  void _mesajAkisiniYenile(){
    _mesajBeklemeZamanlayici?.cancel();
    _mesajBeklemeBitti=false;
    _mesajAkisi=chatRef.collection('messages').orderBy('createdAt').limitToLast(100).snapshots();
    _mesajBeklemeZamanlayici=Timer(const Duration(seconds:2),(){
      if(mounted)setState(()=>_mesajBeklemeBitti=true);
    });
  }
  @override void dispose(){mentionZamanlayici?.cancel();_mesajBeklemeZamanlayici?.cancel();mesaj.dispose();liste.dispose();super.dispose();}
  Future<void> _okunduIsaretle()async{
    final ben=uid;
    if(ben==null||_okunduYaziliyor)return;
    final simdi=DateTime.now();
    if(_sonOkunduKontrolu!=null&&simdi.difference(_sonOkunduKontrolu!).inMilliseconds<1200)return;
    _sonOkunduKontrolu=simdi;
    _okunduYaziliyor=true;
    try{
      final d=await chatRef.get().timeout(const Duration(seconds:5));
      final okunmamis=(d.data()?['unread_$ben'] as num?)?.toInt()??0;
      if(okunmamis>0)await chatRef.set({'unread_$ben':0},SetOptions(merge:true)).timeout(const Duration(seconds:5));
    }catch(_){
    }finally{
      _okunduYaziliyor=false;
    }
  }
  void sonaGit(){WidgetsBinding.instance.addPostFrameCallback((_){
    if(!mounted||!liste.hasClients)return;
    final hedef=liste.position.maxScrollExtent;
    if(_ilkMesajKaydirma){
      _ilkMesajKaydirma=false;
      if(hedef>0)liste.jumpTo(hedef);
      return;
    }
    if(hedef-liste.position.pixels>320)return;
    if((liste.position.pixels-hedef).abs()<2)return;
    liste.animateTo(hedef,duration:const Duration(milliseconds:180),curve:Curves.easeOut);
  });}

  Future<Map<String,dynamic>?> mesajGonderimVerisi()async{
    final ben=uid;if(ben==null)return null;
    final d=await chatRef.get();
    final v=d.data()??<String,dynamic>{};
    final uyeler=List<String>.from(v['members']??const[]);
    final yoneticiler=List<String>.from(v['admins']??const[]);
    if(!uyeler.contains(ben)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Artık bu grubun üyesi değilsin.')));
      return null;
    }
    if(v['onlyAdminsCanPost']==true&&!yoneticiler.contains(ben)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu grupta yalnızca yöneticiler mesaj gönderebilir.')));
      return null;
    }
    return v;
  }
  Future<bool> payloadGonder(Map<String,dynamic> veri,String sonMesaj)async{
    final ben=uid;if(ben==null)return false;
    try{
      final grupVerisi=await mesajGonderimVerisi();
      if(grupVerisi==null)return false;
      final uyeler=List<String>.from(grupVerisi['members']??const[]);
      final mesajRef=chatRef.collection('messages').doc();
      final batch=FirebaseFirestore.instance.batch();
      batch.set(mesajRef,{
        'senderId':ben,
        'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
        ...veri,
      });
      final g=<String,dynamic>{'lastMessage':sonMesaj,'updatedAt':FieldValue.serverTimestamp(),'hiddenFor':FieldValue.arrayRemove(uyeler)};
      for(final x in uyeler){if(x!=ben)g['unread_$x']=FieldValue.increment(1);}
      batch.set(chatRef,g,SetOptions(merge:true));
      await batch.commit();
      final etiketler=List<String>.from(veri['mentions']??const[]);
      if(etiketler.isNotEmpty){
        final profil=await FirebaseFirestore.instance.collection('users').doc(ben).get();
        final ad=(profil.data()?['displayName']??profil.data()?['username']??'Bir kullanıcı').toString();
        for(final hedef in etiketler.toSet()){
          if(hedef==ben||!uyeler.contains(hedef))continue;
          unawaited(uygulamaBildirimiGonder(
            toUid:hedef,fromUid:ben,tur:'message',
            metin:'$ad grupta senden bahsetti',
            belgeId:widget.chatId,
          ).catchError((_){ }));
        }
      }
      return true;
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gönderilemedi.')));
      return false;
    }
  }
  Future<void> gonder()async{
    final t=mesaj.text.trim();if(t.isEmpty||mesajGonderiliyor)return;
    final etiketler=etiketlenenUidler.toList(),yanitId=yanitlananMesajId,yanitMetin=yanitlananMetin;
    setState(()=>mesajGonderiliyor=true);
    final tamam=await payloadGonder({
      'text':t,'type':'text',
      if(etiketler.isNotEmpty)'mentions':etiketler,
      if(yanitId!=null)'replyToId':yanitId,
      if(yanitMetin!=null&&yanitMetin.isNotEmpty)'replyToText':yanitMetin,
    },t);
    if(tamam){
      mesaj.clear();etiketlenenUidler.clear();
      if(mounted)setState((){yanitlananMesajId=null;yanitlananMetin=null;});
    }
    if(mounted)setState(()=>mesajGonderiliyor=false);
  }
  Future<void> medyaGonder(ImageSource kaynak)async{final x=await ImagePicker().pickImage(source:kaynak,imageQuality:76,maxWidth:1280);if(x==null)return;try{final yol='groups/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.jpg';final url=await ngelxMedyaYukleBytes(bytes:await x.readAsBytes(),kind:'groups',ext:'jpg',legacyPath:yol).timeout(const Duration(seconds:12));await payloadGonder({'type':'photo','mediaUrl':url},'📷 Fotoğraf');}catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Fotoğraf gönderilemedi.')));}}
  Future<void> gifGonder()async{const tur=XTypeGroup(label:'GIF',extensions:['gif']);final x=await openFile(acceptedTypeGroups:[tur]);if(x==null)return;try{final yol='groups/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.gif';final bytes=await x.readAsBytes().timeout(const Duration(seconds:8));final url=await ngelxMedyaYukleBytes(bytes:bytes,kind:'gifs',ext:'gif',legacyPath:yol,contentType:'image/gif').timeout(const Duration(seconds:12));await payloadGonder({'type':'gif','mediaUrl':url},'GIF');}catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('GIF gönderilemedi.')));}}

  Future<void> emojiSec()async{final e=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Padding(padding:const EdgeInsets.all(18),child:Wrap(spacing:14,runSpacing:14,children:['😀','😊','😂','😍','🥰','😎','😭','😡','👍','👏','🙏','❤️','🔥','🎉','✨','💯','🤔','😴','🙌','🤝'].map((x)=>InkWell(onTap:()=>Navigator.pop(c,x),child:Text(x,style:const TextStyle(fontSize:30)))).toList()))));if(e!=null){final t=mesaj.text;mesaj.text='$t$e';mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}}

  Future<void> mentionAra(String deger)async{
    mentionZamanlayici?.cancel();
    final parca=deger.split(RegExp(r'\s+')).last;
    if(!parca.startsWith('@')){
      if(mentionOnerileri.isNotEmpty&&mounted)setState(()=>mentionOnerileri.clear());
      return;
    }
    final ara=parca.substring(1).toLowerCase();
    mentionZamanlayici=Timer(const Duration(milliseconds:260),()async{
      try{
        var uyeler=_mentionUyeleri;
        if(uyeler==null){
          final grup=await chatRef.get();
          final ids=List<String>.from(grup.data()?['members']??const[]).take(60).toList();
          final belgeler=await Future.wait(ids.map(_uyeGetir));
          uyeler=<Map<String,String>>[];
          for(int i=0;i<belgeler.length;i++){
            final v=belgeler[i].data()??<String,dynamic>{};
            final kullanici=(v['username']??'').toString().trim();
            final ad=(v['displayName']??kullanici).toString().trim();
            if(kullanici.isNotEmpty)uyeler.add({'uid':ids[i],'username':kullanici,'name':ad.isEmpty?kullanici:ad});
          }
          _mentionUyeleri=uyeler;
        }
        if(!mounted)return;
        final sonuc=<Map<String,String>>[];
        if('herkes'.contains(ara))sonuc.add({'uid':'all','username':'herkes','name':'Herkes'});
        for(final u in uyeler){
          if(sonuc.length>=6)break;
          final kullanici=(u['username']??'').toLowerCase(),ad=(u['name']??'').toLowerCase();
          if(ara.isEmpty||kullanici.contains(ara)||ad.contains(ara))sonuc.add(u);
        }
        if(mounted)setState((){mentionOnerileri..clear()..addAll(sonuc);});
      }catch(_){}
    });
  }
  Future<void> mentionEkle(String kullanici,String? hedefUid)async{
    final metin=mesaj.text,sonBosluk=metin.lastIndexOf(RegExp(r'\s'));
    mesaj.text='${sonBosluk<0?'':metin.substring(0,sonBosluk+1)}@$kullanici ';
    mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);
    if(hedefUid=='all'){
      final grup=await chatRef.get();
      etiketlenenUidler.addAll(List<String>.from(grup.data()?['members']??const[]));
    }else if(hedefUid!=null&&hedefUid.isNotEmpty){
      etiketlenenUidler.add(hedefUid);
    }
    if(mounted)setState(()=>mentionOnerileri.clear());
  }

  Future<void> grupKalpBirak(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final ben=uid;if(ben==null)return;
    try{
      await d.reference.set({'reactions.$ben':'❤️'},SetOptions(merge:true));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('❤️ tepki eklenemedi.')));
    }
  }

  Future<void> mesajMenusu(QueryDocumentSnapshot<Map<String,dynamic>> d)async{final v=d.data(),ben=v['senderId']==uid,metin=(v['text']??'').toString();final grup=await chatRef.get(),yonetici=List<String>.from(grup.data()?['admins']??const[]).contains(uid);final sec=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[Wrap(spacing:12,children:['❤️','👍','😂','😮','😢','😡'].map((e)=>TextButton(onPressed:()=>Navigator.pop(c,'reaction:$e'),child:Text(e,style:const TextStyle(fontSize:24)))).toList()),ListTile(leading:const Icon(Icons.reply),title:const Text('Yanıtla',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'reply')),if(metin.isNotEmpty)ListTile(leading:const Icon(Icons.copy),title:const Text('Kopyala',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'copy')),if(ben&&metin.isNotEmpty)ListTile(leading:const Icon(Icons.edit),title:const Text('Düzenle',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'edit')),if(yonetici)ListTile(leading:Icon(v['pinned']==true?Icons.push_pin:Icons.push_pin_outlined,color:mor),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle',style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'pin')),if(ben||yonetici)ListTile(leading:const Icon(Icons.delete,color:Colors.red),title:const Text('Herkesten sil',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'delete')),if(!ben)ListTile(leading:const Icon(Icons.flag_outlined),title:const Text('Şikâyet et',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'report'))]))));if(sec==null)return;await ngelxOverlayKapanisiniBekle();if(!mounted)return;if(sec.startsWith('reaction:')){await d.reference.set({'reactions.${uid!}':sec.substring(9)},SetOptions(merge:true));}else if(sec=='copy'){await Clipboard.setData(ClipboardData(text:metin));}else if(sec=='reply'){if(mounted)setState((){yanitlananMesajId=d.id;yanitlananMetin=metin.isEmpty?(v['type']=='gif'?'GIF':'Medya'):metin;});}else if(sec=='pin'){await d.reference.set({'pinned':v['pinned']!=true,'pinnedAt':FieldValue.serverTimestamp(),'pinnedBy':uid},SetOptions(merge:true));}else if(sec=='delete'){final ok=await showDialog<bool>(context:context,builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(backgroundColor:Colors.white,surfaceTintColor:Colors.white,title:const Text('Mesaj silinsin mi?',style:TextStyle(color:Colors.black87)),content:const Text('Mesaj gruptan kalıcı olarak kaldırılacak.',style:TextStyle(color:Colors.black54)),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Sil'))])))??false;if(ok)await d.reference.delete();}else if(sec=='report'){if(mounted)await sikayetEt(context,hedefTuru:'grup_mesaji',hedefId:'${widget.chatId}/${d.id}',hedefUid:v['senderId']?.toString());}else if(sec=='edit'){final c=TextEditingController(text:metin);final ok=await showDialog<bool>(context:context,builder:(x)=>AlertDialog(backgroundColor:Colors.white,title:const Text('Mesajı düzenle'),content:TextField(controller:c,maxLines:5,maxLength:2000),actions:[TextButton(onPressed:()=>Navigator.pop(x,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(x,true),child:const Text('Kaydet'))]))??false;if(ok&&c.text.trim().isNotEmpty)await d.reference.update({'text':c.text.trim(),'editedAt':FieldValue.serverTimestamp()});c.dispose();}}

  Future<void> ekMenusu()async{
    final secim=await showModalBottomSheet<String>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:SafeArea(
          child:Wrap(children:[
            ListTile(leading:const Icon(Icons.camera_alt,color:mor),title:const Text('Kamera',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'camera')),
            ListTile(leading:const Icon(Icons.photo_library,color:mor),title:const Text('Galeri',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'gallery')),
            ListTile(leading:const Icon(Icons.gif_box_outlined,color:mor),title:const Text('GIF',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),onTap:()=>Navigator.pop(c,'gif')),
          ]),
        ),
      ),
    );
    if(!mounted||secim==null)return;
    // Alt sayfa tamamen kapanmadan kamera/galeri Activity'sini başlatmak,
    // Android'de Flutter route ağacının sökülmesiyle çakışıp _dependents.isEmpty
    // assertion'ına neden olabiliyor. Kapanış animasyonundan sonra başlat.
    await Future<void>.delayed(const Duration(milliseconds:320));
    if(!mounted)return;
    if(secim=='camera')await medyaGonder(ImageSource.camera);
    else if(secim=='gallery')await medyaGonder(ImageSource.gallery);
    else if(secim=='gif')await gifGonder();
  }
  Future<void> grupArkaPlanMenusu()async{
    final me=uid;if(me==null)return;
    final secim=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(leading:const Icon(Icons.photo_library_outlined,color:mor),title:const Text('Arka plan seç',style:TextStyle(fontWeight:FontWeight.w700)),onTap:()=>Navigator.pop(c,'gallery')),
        ListTile(leading:const Icon(Icons.opacity_rounded,color:mor),title:const Text('Görünürlük'),trailing:Wrap(spacing:4,children:[
          TextButton(onPressed:()=>Navigator.pop(c,'opacity:20'),child:const Text('Az')),
          TextButton(onPressed:()=>Navigator.pop(c,'opacity:35'),child:const Text('Orta')),
          TextButton(onPressed:()=>Navigator.pop(c,'opacity:50'),child:const Text('Çok')),
        ])),
        ListTile(leading:const Icon(Icons.hide_image_outlined,color:Colors.red),title:const Text('Arka planı kaldır',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'remove')),
      ]))),
    );
    if(secim==null||!mounted)return;
    if(secim.startsWith('opacity:')){final oran=(int.tryParse(secim.substring(8))??35)/100;await chatRef.set({'backgroundOpacity_$me':oran},SetOptions(merge:true));return;}
    if(secim=='remove'){await chatRef.set({'backgroundUrl_$me':''},SetOptions(merge:true));return;}
    final x=await ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:78,maxWidth:1440);if(x==null)return;
    try{
      final yol='chat-backgrounds/'+me+'/'+widget.chatId+'_'+DateTime.now().millisecondsSinceEpoch.toString()+'.jpg';
      final url=await ngelxMedyaYukleBytes(bytes:await x.readAsBytes(),kind:'chat-backgrounds',ext:'jpg',legacyPath:yol);
      await chatRef.set({'backgroundUrl_$me':url,'backgroundOpacity_$me':.35},SetOptions(merge:true));
    }catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arka plan yüklenemedi.')));}
  }

  Future<void> aramaBaslat(bool goruntulu)async{
    final ben=uid;
    if(ben==null||aramaBaslatiliyor)return;
    setState(()=>aramaBaslatiliyor=true);
    final grupAdi=widget.ad;
    final odaAdi='group_${widget.chatId}_${DateTime.now().millisecondsSinceEpoch}';
    try{
      unawaited(chatRef.set({
        'callStatus':'ringing',
        'callRoomName':odaAdi,
        'callStartedBy':ben,
        'callVideo':goruntulu,
        'callTitle':grupAdi,
        'callGroup':true,
        'callParticipants':<String>[ben],
        'callCreatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:10)).catchError((_){ }));
      unawaited(chatRef.get().timeout(const Duration(seconds:10)).then((grup){
        final uyeler=List<String>.from(grup.data()?['members']??const[]);
        for(final uye in uyeler){
          if(uye==ben)continue;
          unawaited(uygulamaBildirimiGonder(toUid:uye,fromUid:ben,tur:'call',metin:goruntulu?'$grupAdi grubunda görüntülü arama başlattı':'$grupAdi grubunda sesli arama başlattı',belgeId:widget.chatId).catchError((_){ }));
        }
      }).catchError((_){ }));
      if(!mounted)return;
      setState(()=>aramaBaslatiliyor=false);
      await Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXAramaPage(
        roomName:odaAdi,baslik:grupAdi,foto:widget.foto,goruntulu:goruntulu,aramaRef:chatRef,
      )));
    }catch(_){
      if(!mounted)return;
      setState(()=>aramaBaslatiliyor=false);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arama açılamadı.')));
    }
  }


  Widget mesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d){
    final v=d.data(),gonderen=(v['senderId']??v['fromUid']??v['uid']??'').toString(),ben=gonderen==uid;
    final metin=(v['text']??v['message']??v['content']??'').toString(),tur=(v['type']??'text').toString(),media=(v['mediaUrl']??'').toString();
    final saat=mesajSaati(v['createdAt']??v['clientCreatedAt']),yanit=(v['replyToText']??'').toString();
    final hamTepkiler=v['reactions'],tepkiler=hamTepkiler is Map?Map<String,dynamic>.from(hamTepkiler):<String,dynamic>{};
    if(tur=='poll')return const SizedBox.shrink();
    if(tur=='system')return Center(child:Container(margin:const EdgeInsets.symmetric(vertical:5),padding:const EdgeInsets.symmetric(horizontal:10,vertical:5),decoration:BoxDecoration(color:Colors.white.withValues(alpha:.84),borderRadius:BorderRadius.circular(13)),child:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black54,fontSize:11.5,fontWeight:FontWeight.w600))));
    final gonderenBasligi=!ben?(gonderen.isEmpty?null:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:_uyeGetir(gonderen),builder:(_,u){final p=u.data?.data()??{},pf=(p['photoUrl']??'').toString();return Padding(padding:const EdgeInsets.only(bottom:5),child:Row(mainAxisSize:MainAxisSize.min,children:[CircleAvatar(radius:9,backgroundImage:pf.isEmpty?null:CachedNetworkImageProvider(pf),child:pf.isEmpty?const Icon(Icons.person,size:11):null),const SizedBox(width:5),Flexible(child:Text((p['displayName']??p['username']??'Üye').toString(),overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF6F4BC0),fontSize:11.5,fontWeight:FontWeight.w800)))]));})):null;
    final kutuRengi=ben?const Color(0xFF7651C9):const Color(0xFFF4F4F7),yaziRengi=ben?Colors.white:Colors.black87;
    return Align(alignment:ben?Alignment.centerRight:Alignment.centerLeft,child:GestureDetector(
      behavior:HitTestBehavior.opaque,onLongPress:()=>mesajMenusu(d),onDoubleTap:()=>grupKalpBirak(d),
      onTap:(tur=='photo'||tur=='gif')&&media.isNotEmpty?()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:media))):null,
      child:Container(constraints:const BoxConstraints(maxWidth:286),margin:const EdgeInsets.symmetric(vertical:3,horizontal:1),padding:EdgeInsets.all((tur=='photo'||tur=='gif')?4:10),decoration:BoxDecoration(color:kutuRengi,borderRadius:BorderRadius.circular(16)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        if(gonderenBasligi!=null)gonderenBasligi,
        if(yanit.isNotEmpty)Container(width:double.infinity,margin:const EdgeInsets.only(bottom:7),padding:const EdgeInsets.symmetric(horizontal:8,vertical:6),decoration:BoxDecoration(color:ben?Colors.white.withValues(alpha:.13):Colors.white,borderRadius:BorderRadius.circular(10)),child:Row(children:[Container(width:3,height:28,decoration:BoxDecoration(color:ben?Colors.white70:mor,borderRadius:BorderRadius.circular(4))),const SizedBox(width:7),Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('Yanıt',style:TextStyle(color:ben?Colors.white70:const Color(0xFF6F4BC0),fontSize:10.5,fontWeight:FontWeight.w800)),Text(yanit,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:12.5))]))])),
        if((tur=='photo'||tur=='gif')&&media.isNotEmpty)IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(13),child:CachedNetworkImage(imageUrl:media,width:236,fit:BoxFit.cover,errorWidget:(_,__,___)=>const SizedBox(width:236,height:116,child:Center(child:Icon(Icons.broken_image_outlined))))))else Text(metin.isEmpty?(tur=='gif'?'GIF':'Mesaj'):metin,style:TextStyle(color:yaziRengi,fontSize:15.2,height:1.28,fontWeight:FontWeight.w500)),
        if(tepkiler.isNotEmpty)Padding(padding:const EdgeInsets.only(top:4),child:Wrap(spacing:2,children:tepkiler.values.map((e)=>Text(e.toString(),style:const TextStyle(fontSize:15))).toList())),
        if(v['editedAt']!=null||saat.isNotEmpty)Align(alignment:Alignment.centerRight,child:Padding(padding:const EdgeInsets.only(top:3),child:Text([if(v['editedAt']!=null)'düzenlendi',if(saat.isNotEmpty)saat].join(' · '),style:TextStyle(fontSize:9.5,color:ben?Colors.white70:Colors.black45)))),
      ])),
    ));
  }

  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),
    child:Scaffold(
      appBar:AppBar(
        backgroundColor:const Color(0xFFF4EEFF),surfaceTintColor:Colors.transparent,elevation:0,titleSpacing:0,
        title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_grupAkisi,builder:(_,s){
          final v=s.data?.data()??{},ad=(v['groupName']??widget.ad).toString(),foto=(v['groupPhotoUrl']??widget.foto).toString(),uyeSayisi=List<String>.from(v['members']??const[]).length;
          return InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId))),child:Row(children:[
            CircleAvatar(radius:18,backgroundColor:const Color(0xFFE3D5FF),backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups,color:mor,size:20):null),
            const SizedBox(width:8),
            Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
              Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:16.5,fontWeight:FontWeight.w900,color:Colors.black87)),
              Text(uyeSayisi.toString()+' üye',style:const TextStyle(fontSize:11,color:Colors.black54,fontWeight:FontWeight.w600)),
            ])),
          ]));
        }),
        actions:[
          IconButton(constraints:const BoxConstraints.tightFor(width:39),tooltip:'Sesli arama',onPressed:aramaBaslatiliyor?null:()=>aramaBaslat(false),icon:aramaBaslatiliyor?const SizedBox(width:17,height:17,child:CircularProgressIndicator(strokeWidth:2)):const Icon(Icons.call_rounded,color:Color(0xFF7651C9))),
          IconButton(constraints:const BoxConstraints.tightFor(width:39),tooltip:'Görüntülü arama',onPressed:aramaBaslatiliyor?null:()=>aramaBaslat(true),icon:const Icon(Icons.videocam_rounded,color:Color(0xFF7651C9))),
          PopupMenuButton<String>(icon:const Icon(Icons.more_vert_rounded,color:Color(0xFF7651C9)),onSelected:(x){if(x=='background')grupArkaPlanMenusu();else Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId)));},itemBuilder:(_)=>const [
            PopupMenuItem(value:'info',child:Row(children:[Icon(Icons.info_outline),SizedBox(width:10),Text('Grup bilgileri')])),
            PopupMenuItem(value:'background',child:Row(children:[Icon(Icons.wallpaper_rounded),SizedBox(width:10),Text('Arka plan')])),
          ]),
        ],
      ),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_grupAkisi,builder:(_,tema){
        final tv=tema.data?.data()??<String,dynamic>{},arkaPlanUrl=(tv['backgroundUrl_$uid']??'').toString();
        final opaklik=(tv['backgroundOpacity_$uid'] is num?(tv['backgroundOpacity_$uid'] as num).toDouble():.35).clamp(.10,.65).toDouble();
        return Container(decoration:BoxDecoration(color:Colors.white,image:arkaPlanUrl.isEmpty?null:DecorationImage(image:CachedNetworkImageProvider(arkaPlanUrl),fit:BoxFit.cover,opacity:opaklik)),child:Column(children:[
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:_mesajAkisi,builder:(_,s){
            if(s.hasError)return Center(child:OutlinedButton.icon(onPressed:(){setState(()=>_mesajAkisiniYenile());},icon:const Icon(Icons.refresh),label:const Text('Yeniden dene')));
            final docs=<QueryDocumentSnapshot<Map<String,dynamic>>>[...?s.data?.docs].where((d)=>(d.data()['type']??'').toString()!='poll').toList()..sort((a,b){final ad=a.data(),bd=b.data(),av=ad['createdAt']??ad['clientCreatedAt'],bv=bd['createdAt']??bd['clientCreatedAt'];final ams=av is Timestamp?av.millisecondsSinceEpoch:0,bms=bv is Timestamp?bv.millisecondsSinceEpoch:0;return ams.compareTo(bms);});
            if(s.hasData){if(docs.isNotEmpty&&docs.last.data()['senderId']!=uid)unawaited(_okunduIsaretle());sonaGit();}
            if(docs.isEmpty){if(s.connectionState==ConnectionState.waiting&&!_mesajBeklemeBitti)return const Center(child:CircularProgressIndicator(color:mor,strokeWidth:2));return const Center(child:Text('İlk mesajı yaz.',style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w600)));}
            return ListView.builder(controller:liste,keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag,padding:const EdgeInsets.fromLTRB(10,12,10,8),itemCount:docs.length,itemBuilder:(_,i)=>RepaintBoundary(key:ValueKey(docs[i].id),child:mesajKarti(docs[i])));
          })),
          if(mentionOnerileri.isNotEmpty)Container(color:Colors.white.withValues(alpha:.96),child:Column(mainAxisSize:MainAxisSize.min,children:mentionOnerileri.map((u)=>ListTile(dense:true,visualDensity:VisualDensity.compact,leading:CircleAvatar(radius:14,backgroundColor:const Color(0xFFEDE4FF),child:Icon(u['uid']=='all'?Icons.groups_rounded:Icons.person,size:16,color:mor)),title:Text(u['uid']=='all'?'@herkes':(u['name']??'Üye')+'  @'+(u['username']??''),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w700)),onTap:()=>mentionEkle(u['username']??'',u['uid']))).toList())),
          if(yanitlananMetin!=null)Container(margin:const EdgeInsets.fromLTRB(10,4,10,0),padding:const EdgeInsets.fromLTRB(10,6,4,6),decoration:BoxDecoration(color:Colors.white.withValues(alpha:.96),borderRadius:BorderRadius.circular(14),border:Border.all(color:const Color(0xFFE7DDF8))),child:Row(children:[Container(width:3,height:30,decoration:BoxDecoration(color:mor,borderRadius:BorderRadius.circular(3))),const SizedBox(width:8),Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Text('Yanıt',style:TextStyle(color:Color(0xFF6F4BC0),fontSize:11,fontWeight:FontWeight.w900)),Text(yanitlananMetin!,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:12.5))])),IconButton(onPressed:()=>setState((){yanitlananMesajId=null;yanitlananMetin=null;}),icon:const Icon(Icons.close_rounded,size:19),visualDensity:VisualDensity.compact)])),
          SafeArea(top:false,child:Padding(padding:const EdgeInsets.fromLTRB(7,6,7,8),child:Row(children:[
            IconButton(tooltip:'Ekle',onPressed:ekMenusu,icon:const Icon(Icons.add_circle_rounded,color:Color(0xFF7651C9),size:29)),
            Expanded(child:TextField(controller:mesaj,onChanged:mentionAra,onSubmitted:(_)=>gonder(),maxLength:2000,buildCounter:(_, {required currentLength,required isFocused,maxLength})=>null,decoration:InputDecoration(hintText:'Mesaj yaz...',filled:true,fillColor:Colors.white.withValues(alpha:.97),contentPadding:const EdgeInsets.symmetric(horizontal:15,vertical:10),border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none),enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:const BorderSide(color:Color(0xFFE6E6EA))),focusedBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:const BorderSide(color:Color(0xFFB9A2EA)))))),
            IconButton(tooltip:'Emoji',onPressed:emojiSec,icon:const Icon(Icons.emoji_emotions_outlined,color:Color(0xFF7651C9))),
            IconButton(tooltip:'Gönder',onPressed:mesajGonderiliyor?null:gonder,icon:const Icon(Icons.send_rounded,color:Color(0xFF7651C9))),
          ]))),
        ]));
      }),
    ),
  );
}

class TamEkranMedyaPage extends StatelessWidget{final String url;const TamEkranMedyaPage({super.key,required this.url});@override Widget build(BuildContext context)=>Scaffold(backgroundColor:Colors.black,appBar:AppBar(backgroundColor:Colors.black,foregroundColor:Colors.white),body:Center(child:InteractiveViewer(minScale:.5,maxScale:5,child:Image.network(url,fit:BoxFit.contain,errorBuilder:(_,__,___)=>const Text('Medya açılamadı.',style:TextStyle(color:Colors.white))))));}

class GrupMedyaPage extends StatelessWidget{
  final String chatId;const GrupMedyaPage({super.key,required this.chatId});
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Medya ve bağlantılar')),body:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(chatId).collection('messages').orderBy('createdAt',descending:true).snapshots(),builder:(_,s){if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));final docs=(s.data?.docs??[]).where((d){final t=(d.data()['type']??'').toString();return t=='photo'||t=='gif'||t=='shared_content';}).toList();if(docs.isEmpty)return const Center(child:Text('Henüz medya veya bağlantı paylaşılmadı.',style:TextStyle(color:Colors.black54)));return GridView.builder(padding:const EdgeInsets.all(8),itemCount:docs.length,gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:3,crossAxisSpacing:6,mainAxisSpacing:6),itemBuilder:(_,i){final v=docs[i].data(),t=(v['type']??'').toString(),url=(v['mediaUrl']??'').toString();if(t=='shared_content')return InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:(v['contentId']??'').toString()))),child:Container(color:const Color(0xFFF0E8FF),child:const Icon(Icons.link_rounded,color:mor,size:38)));return InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:url))),child:ClipRRect(borderRadius:BorderRadius.circular(10),child:Image.network(url,fit:BoxFit.cover,errorBuilder:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F1F4),child:Icon(Icons.broken_image_outlined)))));});})));
}

class SabitlenenGrupMesajlariPage extends StatelessWidget{
  final String chatId;const SabitlenenGrupMesajlariPage({super.key,required this.chatId});
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Sabitlenmiş mesajlar')),body:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(chatId).collection('messages').where('pinned',isEqualTo:true).snapshots(),builder:(_,s){if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));final docs=s.data?.docs??[];if(docs.isEmpty)return const Center(child:Text('Sabitlenmiş mesaj yok.',style:TextStyle(color:Colors.black54)));return ListView.separated(padding:const EdgeInsets.all(12),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),itemBuilder:(_,i){final v=docs[i].data(),tur=(v['type']??'text').toString(),metin=(v['text']??'').toString(),url=(v['mediaUrl']??'').toString();return ListTile(leading:Icon(tur=='photo'||tur=='gif'?Icons.photo:Icons.push_pin,color:mor),title:Text(metin.isEmpty?tur=='gif'?'GIF':'Fotoğraf':metin,maxLines:3,overflow:TextOverflow.ellipsis),subtitle:Text(mesajSaati(v['createdAt'])),onTap:url.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:url))));});})));
}

class NgelXAramaPage extends StatefulWidget{
  final String roomName,baslik,foto;final bool goruntulu;final DocumentReference<Map<String,dynamic>> aramaRef;
  const NgelXAramaPage({super.key,required this.roomName,required this.baslik,this.foto='',required this.goruntulu,required this.aramaRef});
  @override State<NgelXAramaPage> createState()=>_NgelXAramaPageState();
}
class _NgelXAramaPageState extends State<NgelXAramaPage>{
  lk.Room? oda;
  StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? aramaDurumAboneligi;
  bool baglaniyor=true,mikrofon=true,kamera=true,hoparlor=true,bitiyor=false,bulanik=false,rotus=false;
  int efekt=0;
  String? hata;

  @override void initState(){
    super.initState();
    aramaDurumAboneligi=widget.aramaRef.snapshots().listen((d){
      final durum=(d.data()?['callStatus']??'').toString();
      if((durum=='ended'||durum=='rejected'||durum=='missed')&&!bitiyor){
        unawaited(_uzaktanBitirildi(durum));
      }
    });
    baglan();
  }
  void _odaDegisti(){if(mounted)setState((){});}

  Future<void> _uzaktanBitirildi(String durum)async{
    if(bitiyor)return;
    bitiyor=true;
    final r=oda;oda=null;
    if(r!=null){
      r.removeListener(_odaDegisti);
      try{await r.disconnect();}catch(_){}
      try{await r.dispose();}catch(_){}
    }
    if(!mounted)return;
    final belge=await widget.aramaRef.get();
    final mesajId=(belge.data()?['callMessageId']??'').toString();
    if(mesajId.isNotEmpty){
      unawaited(widget.aramaRef.collection('messages').doc(mesajId).set({'callStatus':durum,'callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).catchError((_){ }));
    }
    if(!mounted)return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content:Text(durum=='rejected'?'Arama reddedildi.':durum=='missed'?'Arama cevaplanmadı.':'Arama sona erdi.'),
    ));
    Navigator.maybePop(context);
  }

  Future<void> _izinleriIste()async{
    final mikrofonIzni=await Permission.microphone.request();
    if(!mikrofonIzni.isGranted)throw Exception('Mikrofon izni verilmedi.');
    if(widget.goruntulu){
      final kameraIzni=await Permission.camera.request();
      if(!kameraIzni.isGranted)throw Exception('Kamera izni verilmedi.');
    }
  }

  Future<void> baglan()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null){if(mounted)setState((){baglaniyor=false;hata='Arama için giriş yapman gerekiyor.';});return;}
    lk.Room? r;
    try{
      await _izinleriIste();
      final kaynak=lk.DevelopmentTokenSource(id:liveKitTestSunucuId);
      final cevap=await kaynak.fetch(lk.TokenRequestOptions(
        roomName:widget.roomName,
        participantIdentity:u.uid,
        participantName:u.displayName?.isNotEmpty==true?u.displayName!:'NgelX kullanıcısı',
      )).timeout(const Duration(seconds:12));
      r=lk.Room(roomOptions:lk.RoomOptions(adaptiveStream:true,dynacast:true));
      r.addListener(_odaDegisti);
      await r.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:18));
      oda=r;
      final yerel=r.localParticipant;
      if(yerel==null)throw Exception('Arama katılımcısı hazırlanamadı.');
      await yerel.setMicrophoneEnabled(true);
      if(widget.goruntulu)await yerel.setCameraEnabled(true);
      await lk.AudioManager.instance.setSpeakerOutputPreferred(true,force:widget.goruntulu);
      hoparlor=true;
      unawaited(widget.aramaRef.set({
        'callStatus':'active',
        'callParticipants':FieldValue.arrayUnion([u.uid]),
        'callConnectedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true)).timeout(const Duration(seconds:10)).catchError((_){ }));
      unawaited(widget.aramaRef.get().then((d){
        final mesajId=(d.data()?['callMessageId']??'').toString();
        if(mesajId.isNotEmpty)return widget.aramaRef.collection('messages').doc(mesajId).set({'callStatus':'active','callConnectedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      }).catchError((_){ }));
      if(mounted)setState(()=>baglaniyor=false);
    }catch(e){
      if(r!=null){
        r.removeListener(_odaDegisti);
        try{await r.disconnect();}catch(_){}
        try{await r.dispose();}catch(_){}
      }
      oda=null;
      if(mounted)setState((){baglaniyor=false;hata=e.toString().replaceFirst('Exception: ','');});
    }
  }

  lk.VideoTrack? _katilimciVideosu(lk.Participant? p){
    if(p==null)return null;
    for(final pub in p.videoTrackPublications){
      final track=pub.track;
      if(track is lk.VideoTrack&&!pub.muted)return track;
    }
    return null;
  }
  lk.VideoTrack? get _yerelVideo=>_katilimciVideosu(oda?.localParticipant);
  lk.VideoTrack? get _uzakVideo{
    final r=oda;if(r==null)return null;
    for(final p in r.remoteParticipants.values){
      final track=_katilimciVideosu(p);
      if(track!=null)return track;
    }
    return null;
  }

  Future<void> mikrofonDegistir()async{
    final yeni=!mikrofon;
    try{await oda?.localParticipant?.setMicrophoneEnabled(yeni);if(mounted)setState(()=>mikrofon=yeni);}
    catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Mikrofon değiştirilemedi: $e')));}
  }
  Future<void> kameraDegistir()async{
    final yeni=!kamera;
    try{await oda?.localParticipant?.setCameraEnabled(yeni);if(mounted)setState(()=>kamera=yeni);}
    catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kamera değiştirilemedi: $e')));}
  }
  Future<void> hoparlorDegistir()async{
    final yeni=!hoparlor;
    try{
      await lk.AudioManager.instance.setSpeakerOutputPreferred(yeni,force:yeni&&widget.goruntulu);
      if(mounted)setState(()=>hoparlor=yeni);
    }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Ses çıkışı değiştirilemedi: $e')));}
  }

  Future<void> bitir({bool geriDon=true})async{
    if(bitiyor)return;bitiyor=true;
    try{
      await widget.aramaRef.set({'callStatus':'ended','callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      final d=await widget.aramaRef.get();
      final mesajId=(d.data()?['callMessageId']??'').toString();
      if(mesajId.isNotEmpty)await widget.aramaRef.collection('messages').doc(mesajId).set({'callStatus':'ended','callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    }catch(_){}
    final r=oda;oda=null;
    if(r!=null){
      r.removeListener(_odaDegisti);
      try{await r.disconnect();}catch(_){}
      try{await r.dispose();}catch(_){}
    }
    if(geriDon&&mounted)Navigator.pop(context);
  }

  @override void dispose(){
    aramaDurumAboneligi?.cancel();
    final r=oda;
    if(r!=null){
      r.removeListener(_odaDegisti);
      if(!bitiyor){unawaited(r.disconnect());unawaited(r.dispose());}
    }
    super.dispose();
  }

  Widget _efektliVideo(lk.VideoTrack track){
    Widget w=lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover);
    if(efekt==1)w=ColorFiltered(colorFilter:const ColorFilter.mode(Color(0x33FF8A00),BlendMode.softLight),child:w);
    if(efekt==2)w=ColorFiltered(colorFilter:const ColorFilter.mode(Color(0x332C7BFF),BlendMode.softLight),child:w);
    if(efekt==3)w=ColorFiltered(
      colorFilter:const ColorFilter.matrix(<double>[
        0.2126,0.7152,0.0722,0,0,
        0.2126,0.7152,0.0722,0,0,
        0.2126,0.7152,0.0722,0,0,
        0,0,0,1,0,
      ]),
      child:w,
    );
    if(rotus)w=ColorFiltered(colorFilter:const ColorFilter.mode(Color(0x22FFFFFF),BlendMode.screen),child:w);
    if(bulanik)w=ImageFiltered(imageFilter:ui.ImageFilter.blur(sigmaX:5,sigmaY:5),child:w);
    return w;
  }

  Future<void> efektSec()async{
    final x=await showModalBottomSheet<int>(
      context:context,
      backgroundColor:const Color(0xFF191919),
      showDragHandle:true,
      builder:(c)=>SafeArea(child:Padding(
        padding:const EdgeInsets.all(18),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          const Text('Efektler',style:TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900)),
          const SizedBox(height:16),
          Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
            for(final e in const [('Hiçbiri',0),('Sıcak',1),('Soğuk',2),('S/B',3)])
              InkWell(
                onTap:()=>Navigator.pop(c,e.$2),
                child:Column(children:[
                  CircleAvatar(
                    radius:30,
                    backgroundColor:e.$2==efekt?mor:Colors.white24,
                    child:Icon(e.$2==0?Icons.block:e.$2==3?Icons.filter_b_and_w:Icons.auto_awesome,color:Colors.white),
                  ),
                  const SizedBox(height:6),
                  Text(e.$1,style:const TextStyle(color:Colors.white)),
                ]),
              ),
          ]),
        ]),
      )),
    );
    if(x!=null&&mounted)setState(()=>efekt=x);
  }

  Future<void> aramaAyarlari()async{
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:const Color(0xFF1F1F1F),
      showDragHandle:true,
      builder:(c)=>SafeArea(child:Padding(
        padding:const EdgeInsets.fromLTRB(18,4,18,22),
        child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
          const Center(child:Chip(label:Text('🔒 Güvenli bağlantı'))),
          const SizedBox(height:12),
          const Text('Kişiler',style:TextStyle(color:Colors.white54,fontSize:16,fontWeight:FontWeight.w800)),
          const ListTile(contentPadding:EdgeInsets.zero,leading:CircleAvatar(child:Icon(Icons.person)),title:Text('Sen',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800))),
          ListTile(contentPadding:EdgeInsets.zero,leading:const CircleAvatar(child:Icon(Icons.person_outline)),title:Text(widget.baslik,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800))),
          const SizedBox(height:8),
          const Text('Arama ayarları',style:TextStyle(color:Colors.white54,fontSize:16,fontWeight:FontWeight.w800)),
          ListTile(
            contentPadding:EdgeInsets.zero,
            leading:const Icon(Icons.volume_up,color:Colors.white),
            title:const Text('Ses çıkışı',style:TextStyle(color:Colors.white)),
            subtitle:Text(hoparlor?'Hoparlör':'Ahize',style:const TextStyle(color:Colors.white54)),
            onTap:hoparlorDegistir,
          ),
          ListTile(
            contentPadding:EdgeInsets.zero,
            leading:const Icon(Icons.warning_amber_rounded,color:Colors.white),
            title:const Text('Teknik sorun',style:TextStyle(color:Colors.white)),
            onTap:()=>Navigator.pop(c),
          ),
        ]),
      )),
    );
  }

  bool get grupAramasi=>widget.roomName.startsWith('group_');

  String _katilimciAdi(lk.Participant p,{bool yerel=false}){
    if(yerel)return 'Sen';
    final ad=p.name.toString().trim();
    if(ad.isNotEmpty&&ad!='null')return ad;
    final kimlik=p.identity.toString().trim();
    return kimlik.isEmpty?'NgelX kullanıcısı':kimlik;
  }

  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){
    final ad=_katilimciAdi(p,yerel:yerel);
    final track=_katilimciVideosu(p);
    final ilk=ad.trim().isEmpty?'N':ad.trim()[0].toUpperCase();
    return Container(
      clipBehavior:Clip.antiAlias,
      decoration:BoxDecoration(color:const Color(0xFF25212E),borderRadius:BorderRadius.circular(22)),
      child:Stack(fit:StackFit.expand,children:[
        if(widget.goruntulu&&track!=null)
          _efektliVideo(track)
        else
          Center(child:CircleAvatar(
            radius:44,
            backgroundColor:const Color(0xFFE9DDFF),
            child:Text(ilk,style:const TextStyle(color:mor,fontSize:34,fontWeight:FontWeight.w900)),
          )),
        Positioned(
          left:10,right:10,bottom:10,
          child:Container(
            padding:const EdgeInsets.symmetric(horizontal:10,vertical:7),
            decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(13)),
            child:Row(children:[
              Expanded(child:Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800))),
              if(yerel)const Icon(Icons.person_pin_circle_rounded,color:Colors.white70,size:17),
            ]),
          ),
        ),
      ]),
    );
  }

  Widget _grupAramaAlani(){
    final r=oda;
    if(r==null){
      return Expanded(child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const CircularProgressIndicator(color:Colors.white),
        const SizedBox(height:14),
        Text(baglaniyor?'Grup aramasına bağlanılıyor…':'Katılımcılar bekleniyor…',style:const TextStyle(color:Colors.white70)),
      ])));
    }
    final yerel=r.localParticipant;
    final katilimcilar=<({lk.Participant p,bool yerel})>[
      if(yerel!=null)(p:yerel,yerel:true),
      ...r.remoteParticipants.values.map((p)=>(p:p,yerel:false)),
    ];
    final sutun=katilimcilar.length<=1?1:2;
    return Expanded(child:Column(children:[
      Padding(
        padding:const EdgeInsets.fromLTRB(16,10,16,8),
        child:Row(children:[
          Expanded(child:Text(widget.baslik,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:21,fontWeight:FontWeight.w900))),
          Container(
            padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
            decoration:BoxDecoration(color:Colors.white12,borderRadius:BorderRadius.circular(14)),
            child:Text('${katilimcilar.length} kişi',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
          ),
        ]),
      ),
      Expanded(child:GridView.builder(
        padding:const EdgeInsets.fromLTRB(12,6,12,12),
        itemCount:katilimcilar.length,
        gridDelegate:SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount:sutun,
          crossAxisSpacing:10,
          mainAxisSpacing:10,
          childAspectRatio:katilimcilar.length<=2?1.05:.82,
        ),
        itemBuilder:(_,i)=>_katilimciKutusu(katilimcilar[i].p,yerel:katilimcilar[i].yerel),
      )),
    ]));
  }

  Widget _videoAlani(){
    final uzak=_uzakVideo,yerel=_yerelVideo,ana=uzak??yerel;
    return Expanded(child:Stack(children:[
      Positioned.fill(
        child:ana!=null
          ? _efektliVideo(ana)
          : Container(
              margin:const EdgeInsets.all(14),
              decoration:BoxDecoration(color:Colors.white10,borderRadius:BorderRadius.circular(22)),
              child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const Icon(Icons.person_rounded,color:Colors.white30,size:76),
                const SizedBox(height:12),
                Text(baglaniyor?'Bağlanıyor…':'Karşı tarafın görüntüsü bekleniyor…',style:const TextStyle(color:Colors.white70)),
              ])),
            ),
      ),
      Positioned(top:14,left:14,child:IconButton.filledTonal(onPressed:aramaAyarlari,icon:const Icon(Icons.settings_rounded))),
      if(uzak!=null&&yerel!=null)
        Positioned(
          right:20,top:20,width:108,height:154,
          child:ClipRRect(borderRadius:BorderRadius.circular(18),child:_efektliVideo(yerel)),
        ),
      Positioned(
        left:18,right:18,bottom:16,
        child:Column(children:[
          CircleAvatar(radius:38,backgroundColor:Colors.black26,backgroundImage:widget.foto.isEmpty?null:CachedNetworkImageProvider(widget.foto),child:widget.foto.isEmpty?const Icon(Icons.person,color:Colors.white,size:36):null),
          const SizedBox(height:8),
          Text(widget.baslik,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontSize:26,fontWeight:FontWeight.w900,shadows:[Shadow(blurRadius:8,color:Colors.black54)])),
          Text(baglaniyor?'Aranıyor…':'Görüntülü arama',style:const TextStyle(color:Colors.white70,fontSize:16)),
        ]),
      ),
    ]));
  }

  Widget _sesliAlani()=>Expanded(child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
    CircleAvatar(radius:62,backgroundColor:const Color(0xFFE9DDFF),backgroundImage:widget.foto.isEmpty?null:CachedNetworkImageProvider(widget.foto),child:widget.foto.isEmpty?const Icon(Icons.call_rounded,color:mor,size:62):null),
    const SizedBox(height:18),
    Text(widget.baslik,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontSize:27,fontWeight:FontWeight.w900)),
    const SizedBox(height:7),
    Text(baglaniyor?'Bağlanıyor…':'Sesli arama',style:const TextStyle(color:Colors.white70,fontSize:16)),
  ])));

  @override Widget build(BuildContext context)=>PopScope(
    canPop:true,
    onPopInvokedWithResult:(didPop,__){if(didPop)bitir(geriDon:false);},
    child:Scaffold(
      backgroundColor:const Color(0xFF16121F),
      body:SafeArea(child:Column(children:[
        if(hata!=null)
          Expanded(child:Center(child:Padding(padding:const EdgeInsets.all(28),child:Column(mainAxisSize:MainAxisSize.min,children:[
            const Icon(Icons.call_end_rounded,color:Colors.redAccent,size:66),
            const SizedBox(height:16),
            const Text('Arama bağlantısı kurulamadı',style:TextStyle(color:Colors.white,fontSize:21,fontWeight:FontWeight.w900)),
            const SizedBox(height:10),
            SelectableText(hata!,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70)),
            const SizedBox(height:18),
            FilledButton.icon(onPressed:(){setState((){hata=null;baglaniyor=true;});baglan();},icon:const Icon(Icons.refresh),label:const Text('Tekrar dene')),
            TextButton(onPressed:openAppSettings,child:const Text('Kamera / mikrofon izinlerini aç')),
          ]))))
        else if(grupAramasi)_grupAramaAlani()
        else if(widget.goruntulu)_videoAlani()
        else _sesliAlani(),
        if(hata==null&&widget.goruntulu)Padding(
          padding:const EdgeInsets.fromLTRB(10,10,10,2),
          child:Wrap(spacing:8,runSpacing:8,alignment:WrapAlignment.center,children:[
            FilterChip(
              label:const Text('✨ Rötuş'),
              selected:rotus,
              onSelected:(v)=>setState(()=>rotus=v),
              selectedColor:Colors.white,
              backgroundColor:Colors.white24,
              labelStyle:TextStyle(color:rotus?Colors.black:Colors.white),
            ),
            FilterChip(
              label:const Text('◌ Bulanıklaştır'),
              selected:bulanik,
              onSelected:(v)=>setState(()=>bulanik=v),
              selectedColor:Colors.white,
              backgroundColor:Colors.white24,
              labelStyle:TextStyle(color:bulanik?Colors.black:Colors.white),
            ),
            ActionChip(
              label:const Text('☺ Efektler'),
              onPressed:efektSec,
              backgroundColor:Colors.white24,
              labelStyle:const TextStyle(color:Colors.white),
            ),
          ]),
        ),
        if(hata==null)Padding(
          padding:const EdgeInsets.fromLTRB(12,18,12,8),
          child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
            _aramaTus(mikrofon?Icons.mic:Icons.mic_off,mikrofonDegistir,mikrofon),
            _aramaTus(hoparlor?Icons.volume_up:Icons.volume_off,hoparlorDegistir,hoparlor),
            if(widget.goruntulu)_aramaTus(kamera?Icons.videocam:Icons.videocam_off,kameraDegistir,kamera),
          ]),
        ),
        FloatingActionButton.large(heroTag:null,backgroundColor:Colors.red,onPressed:()=>bitir(),child:const Icon(Icons.call_end,color:Colors.white,size:34)),
        const SizedBox(height:26),
      ])),
    ),
  );

  Widget _aramaTus(IconData ikon,Future<void> Function() onTap,bool acik)=>IconButton.filled(
    style:IconButton.styleFrom(backgroundColor:acik?Colors.white24:Colors.white,foregroundColor:acik?Colors.white:Colors.black),
    onPressed:()=>onTap(),
    icon:Icon(ikon),iconSize:29,padding:const EdgeInsets.all(16),
  );
}

class GrupBilgiPage extends StatefulWidget{final String chatId;const GrupBilgiPage({super.key,required this.chatId});@override State<GrupBilgiPage> createState()=>_GrupBilgiPageState();}
class _GrupBilgiPageState extends State<GrupBilgiPage>{
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _uyeProfilCache={};
  DocumentReference<Map<String,dynamic>> get ref=>FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
  String? get ben=>FirebaseAuth.instance.currentUser?.uid;
  Future<DocumentSnapshot<Map<String,dynamic>>> _uyeGetir(String id)=>
      _uyeProfilCache.putIfAbsent(id,()=>FirebaseFirestore.instance.collection('users').doc(id).get());
  Future<void> sistemMesaji(String text)async{await ref.collection('messages').add({'senderId':'system','type':'system','text':text,'createdAt':FieldValue.serverTimestamp()});await ref.set({'lastMessage':text,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}
  Future<void> adiDuzenle(String mevcut)async{
    final c=TextEditingController(text:mevcut.length>16?mevcut.substring(0,16):mevcut);
    final yeni=await showDialog<String>(
      context:context,
      builder:(x)=>Theme(
        data:ThemeData.light(),
        child:AlertDialog(
          backgroundColor:Colors.white,
          surfaceTintColor:Colors.white,
          title:const Text('Grup adını düzenle',style:TextStyle(color:Colors.black87)),
          content:TextField(
            controller:c,
            maxLength:16,
            style:const TextStyle(color:Colors.black87),
            decoration:const InputDecoration(
              helperText:'En fazla 16 karakter',
              helperStyle:TextStyle(color:Colors.black54),
              counterStyle:TextStyle(color:Colors.black54),
            ),
          ),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(x),child:const Text('Vazgeç')),
            FilledButton(onPressed:()=>Navigator.pop(x,c.text.trim()),child:const Text('Kaydet')),
          ],
        ),
      ),
    );
    await ngelxOverlayKapanisiniBekle();
    c.dispose();
    if(yeni==null)return;
    if(!mounted)return;
    final temiz=yeni.trim();
    if(temiz.length<2||temiz.length>16){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup adı 2–16 karakter arasında olmalı.')));
      return;
    }
    await ref.update({'groupName':temiz});
    await sistemMesaji('Grup adı “$temiz” olarak değiştirildi.');
  }
  Future<void> fotografDuzenle()async{
    final secim=await showModalBottomSheet<String>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
          const ListTile(title:Text('Grup fotoğrafını değiştir',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
          ListTile(leading:const Icon(Icons.camera_alt_rounded,color:mor),title:const Text('Fotoğraf çek',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'camera')),
          ListTile(leading:const Icon(Icons.photo_library_rounded,color:mor),title:const Text('Galeriden seç',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'gallery')),
          ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:const Text('Mevcut fotoğrafı kaldır',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'remove')),
        ])),
      ),
    );
    if(secim==null)return;
    await ngelxOverlayKapanisiniBekle();
    if(!mounted)return;

    try{
      final mevcut=await ref.get();
      final eski=(mevcut.data()?['groupPhotoUrl']??'').toString();

      if(secim=='remove'){
        await ref.update({'groupPhotoUrl':'','updatedAt':FieldValue.serverTimestamp()});
        if(eski.isNotEmpty)unawaited(ngelxMedyaSil(eski).catchError((_){ }));
        await sistemMesaji('Yönetici grup fotoğrafını kaldırdı.');
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup fotoğrafı kaldırıldı.')));
        return;
      }

      final x=await ImagePicker().pickImage(
        source:secim=='camera'?ImageSource.camera:ImageSource.gallery,
        imageQuality:82,
        maxWidth:1280,
      );
      if(x==null)return;

      final uzanti=x.name.contains('.')?x.name.split('.').last.toLowerCase():'jpg';
      final yol='groups/${widget.chatId}/avatar_${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      final url=await ngelxMedyaYukleBytes(
        bytes:await x.readAsBytes(),
        kind:'groups',
        ext:uzanti,
        legacyPath:yol,
      );
      await ref.update({'groupPhotoUrl':url,'updatedAt':FieldValue.serverTimestamp()});
      if(eski.isNotEmpty&&eski!=url)unawaited(ngelxMedyaSil(eski).catchError((_){ }));
      await sistemMesaji('Yönetici grup fotoğrafını değiştirdi.');
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup fotoğrafı kaydedildi.')));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Grup fotoğrafı değiştirilemedi: $e')));
    }
  }

  Future<void> uyeIslemi(String id,String isim,bool admin)async{
    final sec=await showModalBottomSheet<String>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
          ListTile(title:Text(isim,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
          ListTile(
            leading:Icon(admin?Icons.person_remove_alt_1:Icons.admin_panel_settings,color:mor),
            title:Text(admin?'Yöneticilikten çıkar':'Yönetici yap',style:const TextStyle(color:Colors.black87)),
            onTap:()=>Navigator.pop(c,admin?'demote':'promote'),
          ),
          ListTile(leading:const Icon(Icons.person_remove,color:Colors.red),title:const Text('Gruptan çıkar',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'remove')),
        ])),
      ),
    );
    if(sec==null)return;
    if(sec=='promote'){
      await ref.update({'admins':FieldValue.arrayUnion([id])});
      await sistemMesaji('$isim yönetici yapıldı.');
    }else if(sec=='demote'){
      await ref.update({'admins':FieldValue.arrayRemove([id])});
      await sistemMesaji('$isim artık yönetici değil.');
    }else{
      final ok=await showDialog<bool>(
        context:context,
        builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(
          backgroundColor:Colors.white,
          title:Text('$isim gruptan çıkarılsın mı?',style:const TextStyle(color:Colors.black87)),
          content:const Text('Bu işlemden sonra kullanıcı gruba mesaj gönderemez.',style:TextStyle(color:Colors.black87)),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
            FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Çıkar')),
          ],
        )),
      )??false;
      if(ok){
        await ref.update({'members':FieldValue.arrayRemove([id]),'admins':FieldValue.arrayRemove([id])});
        await sistemMesaji('$isim gruptan çıkarıldı.');
      }
    }
  }
  Future<void> uyeEkle(List<String> mevcut)async{
    final me=ben;
    if(me==null)return;
    if(mevcut.length>=60){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu grup 60 üyelik üst sınıra ulaştı.')));
      return;
    }
    final p=await FirebaseFirestore.instance.collection('users').doc(me).get();
    final izinli=<String>{
      ...List<String>.from(p.data()?['friends']??const[]),
      ...List<String>.from(p.data()?['following']??const[]),
    }..removeAll(mevcut);
    if(izinli.isEmpty){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Eklenebilecek arkadaş veya takip edilen kişi bulunamadı.')));
      return;
    }

    final belgeler=await Future.wait(izinli.map(_uyeGetir));
    final adaylar=<DocumentSnapshot<Map<String,dynamic>>>[];
    for(final d in belgeler){
      if(d.exists&&d.data()?['deactivated']!=true)adaylar.add(d);
    }
    adaylar.sort((a,b){
      final av=a.data()??<String,dynamic>{},bv=b.data()??<String,dynamic>{};
      final aa=(av['displayName']??av['username']??'').toString().toLowerCase();
      final ba=(bv['displayName']??bv['username']??'').toString().toLowerCase();
      return aa.compareTo(ba);
    });
    if(!mounted)return;

    final secilen=<String>{};
    final onay=await showModalBottomSheet<bool>(
      context:context,
      isScrollControlled:true,
      backgroundColor:Colors.white,
      showDragHandle:true,
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:StatefulBuilder(builder:(c,setP)=>SafeArea(child:SizedBox(
          height:MediaQuery.sizeOf(c).height*.72,
          child:Column(children:[
            ListTile(
              title:const Text('Gruba üye ekle',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
              subtitle:Text('${mevcut.length+secilen.length}/60 üye',style:const TextStyle(color:Colors.black54)),
            ),
            Expanded(child:adaylar.isEmpty
              ? const Center(child:Text('Eklenebilecek kişi bulunamadı.',style:TextStyle(color:Colors.black54)))
              : ListView.builder(
                  itemCount:adaylar.length,
                  itemBuilder:(_,i){
                    final d=adaylar[i],v=d.data()??<String,dynamic>{};
                    final ad=(v['displayName']??v['username']??'Kullanıcı').toString();
                    final foto=(v['photoUrl']??'').toString();
                    return CheckboxListTile(
                      value:secilen.contains(d.id),
                      onChanged:(x){
                        if(x==true&&mevcut.length+secilen.length>=60){
                          ScaffoldMessenger.of(c).showSnackBar(const SnackBar(content:Text('Grupta en fazla 60 üye olabilir.')));
                          return;
                        }
                        setP(()=>x==true?secilen.add(d.id):secilen.remove(d.id));
                      },
                      secondary:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto)),
                      title:Text(ad,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
                      subtitle:Text('@${v['username']??'ngelx'}',style:const TextStyle(color:Colors.black54)),
                    );
                  },
                ),
            ),
            Padding(
              padding:EdgeInsets.fromLTRB(12,12,12,12+MediaQuery.paddingOf(c).bottom),
              child:SizedBox(
                width:double.infinity,
                child:FilledButton(
                  onPressed:secilen.isEmpty?null:()=>Navigator.pop(c,true),
                  child:Text('${secilen.length} kişiyi ekle'),
                ),
              ),
            ),
          ]),
        ))),
      ),
    )??false;
    if(!onay||secilen.isEmpty)return;
    await ref.update({
      'members':FieldValue.arrayUnion(secilen.toList()),
      'hiddenFor':FieldValue.arrayRemove(secilen.toList()),
    });
    _uyeProfilCache.clear();
    await sistemMesaji('${secilen.length} yeni üye gruba eklendi.');
  }
  Future<void> ayril(List<String> uyeler,List<String> admins)async{final me=ben;if(me==null)return;if(admins.length==1&&admins.contains(me)&&uyeler.length>1){await showDialog<void>(context:context,builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(backgroundColor:Colors.white,title:const Text('Önce yönetici belirle',style:TextStyle(color:Colors.black87)),content:const Text('Gruptan ayrılmadan önce başka bir üyeyi yönetici yapmalısın.',style:TextStyle(color:Colors.black87)),actions:[FilledButton(onPressed:()=>Navigator.pop(c),child:const Text('Tamam'))])));return;}final sonKisi=uyeler.length==1;final ok=await showDialog<bool>(context:context,builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(backgroundColor:Colors.white,title:Text(sonKisi?'Grup silinsin mi?':'Gruptan ayrılmak istiyor musun?',style:const TextStyle(color:Colors.black87)),content:Text(sonKisi?'Grupta yalnızca sen kaldın. Grup sohbeti listenden kaldırılacak.':'Mesaj geçmişine erişimin sona erecek.',style:const TextStyle(color:Colors.black87)),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:Text(sonKisi?'Grubu sil':'Ayrıl'))])))??false;if(!ok)return;if(sonKisi)await ref.set({'members':FieldValue.arrayRemove([me]),'admins':FieldValue.arrayRemove([me]),'groupDeleted':true,'deletedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));else{await sistemMesaji('Bir üye gruptan ayrıldı.');await ref.update({'members':FieldValue.arrayRemove([me]),'admins':FieldValue.arrayRemove([me])});}if(mounted)Navigator.popUntil(context,(r)=>r.isFirst);}
  Future<void> ayarDegistir(String alan,bool deger)async{await ref.set({alan:deger},SetOptions(merge:true));}
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(
        backgroundColor:Colors.white,
        surfaceTintColor:Colors.transparent,
        elevation:0,
        title:const Text('Grup bilgileri',style:TextStyle(fontWeight:FontWeight.w900)),
      ),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:ref.snapshots(),
        builder:(_,s){
          if(!s.hasData)return const Center(child:CircularProgressIndicator(color:mor));
          final v=s.data?.data()??<String,dynamic>{};
          final uyeler=List<String>.from(v['members']??const[]);
          final yoneticiler=List<String>.from(v['admins']??const[]);
          final yonetici=yoneticiler.contains(ben);
          final foto=(v['groupPhotoUrl']??'').toString();
          final ad=(v['groupName']??'Grup').toString();

          return ListView(
            padding:EdgeInsets.fromLTRB(16,14,16,28+MediaQuery.paddingOf(context).bottom),
            children:[
              GestureDetector(
                onTap:yonetici?fotografDuzenle:null,
                child:Center(
                  child:Stack(
                    clipBehavior:Clip.none,
                    children:[
                      CircleAvatar(
                        radius:48,
                        backgroundColor:const Color(0xFFE9DDFF),
                        backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),
                        child:foto.isEmpty?const Icon(Icons.groups,color:mor,size:44):null,
                      ),
                      if(yonetici)
                        const Positioned(
                          right:-2,bottom:-2,
                          child:CircleAvatar(
                            radius:15,
                            backgroundColor:mor,
                            child:Icon(Icons.camera_alt_rounded,color:Colors.white,size:16),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height:9),
              Text(ad,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:23,fontWeight:FontWeight.w900)),
              Text(uyeler.length.toString()+' üye',textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54,fontSize:13,fontWeight:FontWeight.w600)),

              if(yonetici)...[
                const SizedBox(height:13),
                Row(
                  children:[
                    Expanded(child:OutlinedButton.icon(onPressed:()=>adiDuzenle(ad),icon:const Icon(Icons.edit_rounded,size:18),label:const Text('Ad'))),
                    const SizedBox(width:7),
                    Expanded(child:OutlinedButton.icon(onPressed:fotografDuzenle,icon:const Icon(Icons.photo_camera_rounded,size:18),label:const Text('Fotoğraf'))),
                    const SizedBox(width:7),
                    Expanded(child:OutlinedButton.icon(onPressed:uyeler.length>=60?null:()=>uyeEkle(uyeler),icon:const Icon(Icons.person_add_alt_1_rounded,size:18),label:const Text('Ekle'))),
                  ],
                ),
              ],

              const SizedBox(height:18),
              Row(
                children:[
                  const Expanded(child:Text('Sohbet üyeleri',style:TextStyle(color:Colors.black87,fontSize:18,fontWeight:FontWeight.w900))),
                  Text(uyeler.length.toString()+'/60',style:const TextStyle(color:Colors.black45,fontWeight:FontWeight.w700)),
                ],
              ),
              const SizedBox(height:3),
              ...uyeler.map((id)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                future:_uyeGetir(id),
                builder:(_,u){
                  final p=u.data?.data()??<String,dynamic>{};
                  final isim=(p['displayName']??p['username']??'Kullanıcı').toString();
                  final pf=(p['photoUrl']??'').toString();
                  final admin=yoneticiler.contains(id);
                  return ListTile(
                    dense:true,
                    visualDensity:VisualDensity.compact,
                    contentPadding:EdgeInsets.zero,
                    onTap:yonetici&&id!=ben?()=>uyeIslemi(id,isim,admin):null,
                    leading:CircleAvatar(
                      radius:20,
                      backgroundImage:pf.isEmpty?null:CachedNetworkImageProvider(pf),
                      child:pf.isEmpty?const Icon(Icons.person,size:19):null,
                    ),
                    title:Text(isim,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontWeight:FontWeight.w700)),
                    subtitle:admin?const Text('Yönetici',style:TextStyle(color:mor,fontSize:11.5,fontWeight:FontWeight.w700)):null,
                    trailing:yonetici&&id!=ben?const Icon(Icons.more_horiz_rounded,size:20):null,
                  );
                },
              )),

              const Divider(height:24),
              ListTile(
                dense:true,
                contentPadding:EdgeInsets.zero,
                leading:const Icon(Icons.photo_library_outlined,color:mor),
                title:const Text('Medya ve bağlantılar',style:TextStyle(fontWeight:FontWeight.w700)),
                trailing:const Icon(Icons.chevron_right),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupMedyaPage(chatId:widget.chatId))),
              ),
              ListTile(
                dense:true,
                contentPadding:EdgeInsets.zero,
                leading:const Icon(Icons.push_pin_outlined,color:mor),
                title:const Text('Sabitlenen mesajlar',style:TextStyle(fontWeight:FontWeight.w700)),
                trailing:const Icon(Icons.chevron_right),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:widget.chatId))),
              ),

              if(yonetici)...[
                const Divider(height:24),
                const Text('İzinler',style:TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900)),
                SwitchListTile(
                  dense:true,contentPadding:EdgeInsets.zero,
                  title:const Text('Sadece yöneticiler yazsın'),
                  value:v['onlyAdminsCanPost']==true,
                  onChanged:(x)=>ayarDegistir('onlyAdminsCanPost',x),
                ),
                SwitchListTile(
                  dense:true,contentPadding:EdgeInsets.zero,
                  title:const Text('Yeni üyeler geçmişi görsün'),
                  value:v['newMembersSeeHistory']!=false,
                  onChanged:(x)=>ayarDegistir('newMembersSeeHistory',x),
                ),
                SwitchListTile(
                  dense:true,contentPadding:EdgeInsets.zero,
                  title:const Text('Katılma isteğini onayla'),
                  value:v['joinApproval']==true,
                  onChanged:(x)=>ayarDegistir('joinApproval',x),
                ),
              ],

              const Divider(height:24),
              ListTile(
                dense:true,
                contentPadding:EdgeInsets.zero,
                leading:const Icon(Icons.exit_to_app_rounded,color:Colors.red),
                title:Text(uyeler.length==1?'Grubu sil':'Gruptan ayrıl',style:const TextStyle(color:Colors.red,fontWeight:FontWeight.w700)),
                onTap:()=>ayril(uyeler,yoneticiler),
              ),
            ],
          );
        },
      ),
    ),
  );
}

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
              stream: FirebaseFirestore.instance.collection('users').limit(100).snapshots(),
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
                      },
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                        leading: CircleAvatar(
                          radius: 27,
                          backgroundColor: const Color(0xFFE5E7EB),
                          backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto),
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
  final mesaj=TextEditingController(),liste=ScrollController();
  final List<Map<String,String>> mentionOnerileri=[];
  late final Stream<DocumentSnapshot<Map<String,dynamic>>> _chatAkisi;
  late final Stream<QuerySnapshot<Map<String,dynamic>>> _mesajAkisi;
  bool _okunduYaziliyor=false;
  bool _ilkMesajKaydirma=true;
  DateTime? _sonYaziyorGonderim;
  DateTime? _mesajHazirlikZamani;
  String? _mesajHazirlikEngeli;
  Map<String,dynamic> _mesajHazirlikSohbet=<String,dynamic>{};
  Map<String,dynamic> _mesajHazirlikDiger=<String,dynamic>{};
  bool _mesajHazirlikSohbetMevcut=false;
  bool gonderiliyor=false,aramaBaslatiliyor=false,yaziyorGonderildi=false;
  final rec.AudioRecorder _sesKaydedici=rec.AudioRecorder();
  bool sesKaydediliyor=false;
  DateTime? sesKaydiBaslangic;
  Timer? yaziyorZamanlayici,sureliMesajZamanlayici;
  bool gizliKelimeFiltresi=true;
  List<String> gizliKelimeListesi=[];
  String? yanitMesajId,yanitMetin,yanitGonderenUid;
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;

  Future<({String? engel,Map<String,dynamic> sohbet,Map<String,dynamic> diger,bool sohbetMevcut})> mesajGonderimHazirligi({bool zorla=false}) async {
    final ben=uid;
    if(ben==null)return (engel:'Mesaj göndermek için giriş yap.',sohbet:<String,dynamic>{},diger:<String,dynamic>{},sohbetMevcut:false);
    final simdi=DateTime.now();
    if(!zorla&&_mesajHazirlikZamani!=null&&simdi.difference(_mesajHazirlikZamani!).inSeconds<15){
      return (engel:_mesajHazirlikEngeli,sohbet:_mesajHazirlikSohbet,diger:_mesajHazirlikDiger,sohbetMevcut:_mesajHazirlikSohbetMevcut);
    }
    try{
      final sonuc=await Future.wait([
        FirebaseFirestore.instance.collection('users').doc(ben).get().timeout(const Duration(seconds:8)),
        FirebaseFirestore.instance.collection('users').doc(widget.digerUid).get().timeout(const Duration(seconds:8)),
        FirebaseFirestore.instance.collection('chats').doc(widget.chatId).get().timeout(const Duration(seconds:8)),
      ]);
      final benim=sonuc[0].data()??<String,dynamic>{};
      final diger=sonuc[1].data()??<String,dynamic>{};
      final sohbet=sonuc[2].data()??<String,dynamic>{};
      String? engel;
      final benimEngellediklerim=List<String>.from(benim['blocked']??const[]);
      final onunEngelledikleri=List<String>.from(diger['blocked']??const[]);
      if(benimEngellediklerim.contains(widget.digerUid)||onunEngelledikleri.contains(ben))engel='Engellenen hesaplar arasında mesaj gönderilemez.';
      else if(diger['deactivated']==true)engel='Bu hesap şu anda kullanılamıyor.';
      else{
        final arkadaslar=List<String>.from(diger['friends']??const[]);
        final takipEttikleri=List<String>.from(diger['following']??const[]);
        final kabulEdildi=sohbet['requestAccepted_$ben']==true||sohbet['requestAccepted_${widget.digerUid}']==true;
        final izin=(diger['messagePermission']??(diger['friendsOnlyMessages']!=false?'friends':'all')).toString();
        if(!kabulEdildi){
          if(izin=='none')engel='Bu kullanıcı yeni özel mesaj kabul etmiyor.';
          else if(izin=='friends'&&!arkadaslar.contains(ben))engel='Bu kullanıcı yalnızca arkadaşlarından mesaj kabul ediyor.';
          else if(izin=='following'&&!takipEttikleri.contains(ben))engel='Bu kullanıcı yalnızca takip ettiği hesaplardan mesaj kabul ediyor.';
        }
      }
      _mesajHazirlikZamani=simdi;
      _mesajHazirlikEngeli=engel;
      _mesajHazirlikSohbet=sohbet;
      _mesajHazirlikDiger=diger;
      _mesajHazirlikSohbetMevcut=sonuc[2].exists;
      return (engel:engel,sohbet:sohbet,diger:diger,sohbetMevcut:sonuc[2].exists);
    }catch(_){
      return (engel:'Mesaj izni kontrol edilemedi. İnternet bağlantını kontrol et.',sohbet:<String,dynamic>{},diger:<String,dynamic>{},sohbetMevcut:false);
    }
  }

  Future<String?> mesajEngeli()async=>(await mesajGonderimHazirligi()).engel;

  void sureliMesajTakvimi(Iterable<QueryDocumentSnapshot<Map<String,dynamic>>> docs){
    sureliMesajZamanlayici?.cancel();
    DateTime? enYakin;
    final simdi=DateTime.now();
    for(final d in docs){
      final x=d.data()['expiresAt'];
      if(x is! Timestamp)continue;
      final tarih=x.toDate();
      if(tarih.isAfter(simdi)&&(enYakin==null||tarih.isBefore(enYakin)))enYakin=tarih;
    }
    if(enYakin==null)return;
    final bekleme=enYakin.difference(simdi)+const Duration(milliseconds:150);
    sureliMesajZamanlayici=Timer(bekleme,(){if(mounted)setState((){});});
  }

  Future<void> _okunduGuncelle()async{
    final ben=uid;
    if(ben==null||_okunduYaziliyor)return;
    _okunduYaziliyor=true;
    try{
      final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
      final d=await ref.get();
      if(!d.exists)return;
      final veri=d.data()??<String,dynamic>{};
      final okunmamis=(veri['unread_$ben'] as num?)?.toInt()??0;
      if(okunmamis<=0)return;
      final izin=veri['readReceipts_$ben']!=false;
      await ref.set({
        'unread_$ben':0,
        if(izin)'lastReadAt_$ben':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));
    }catch(_){
    }finally{
      _okunduYaziliyor=false;
    }
  }

  void mesajDegisti(String deger){
    mentionAra(deger);
    final ben=uid;if(ben==null)return;
    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    yaziyorZamanlayici?.cancel();
    if(deger.trim().isEmpty){
      if(yaziyorGonderildi){
        yaziyorGonderildi=false;
        unawaited(ref.set({'typing_$ben':false},SetOptions(merge:true)));
      }
      return;
    }
    final simdi=DateTime.now();
    if(!yaziyorGonderildi){
      yaziyorGonderildi=true;
      _sonYaziyorGonderim=simdi;
      unawaited(ref.get().then((d){
        if(d.data()?['typingIndicator_$ben']!=false){
          return ref.set({'typing_$ben':true,'typingAt_$ben':FieldValue.serverTimestamp()},SetOptions(merge:true));
        }
      }).catchError((_){ }));
    }else if(_sonYaziyorGonderim==null||simdi.difference(_sonYaziyorGonderim!).inSeconds>=4){
      _sonYaziyorGonderim=simdi;
      unawaited(ref.set({'typingAt_$ben':FieldValue.serverTimestamp()},SetOptions(merge:true)).catchError((_){ }));
    }
    yaziyorZamanlayici=Timer(const Duration(seconds:2),(){
      yaziyorGonderildi=false;
      unawaited(ref.set({'typing_$ben':false},SetOptions(merge:true)));
    });
  }

  Future<void> gonder() async {
    final t=mesaj.text.trim();
    final ben=uid;
    if(t.isEmpty||ben==null||gonderiliyor)return;
    setState(()=>gonderiliyor=true);

    final hazirlik=await mesajGonderimHazirligi();
    if(hazirlik.engel!=null){
      if(mounted){
        setState(()=>gonderiliyor=false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hazirlik.engel!)));
      }
      return;
    }

    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    final sureHam=hazirlik.sohbet['disappearingSeconds'];
    final sure=sureHam is num?sureHam.toInt():0;
    final simdi=DateTime.now();
    final clientCreatedAt=Timestamp.fromDate(simdi);
    final bitis=sure>0?Timestamp.fromDate(simdi.add(Duration(seconds:sure))):null;
    final arkadas=List<String>.from(hazirlik.diger['friends']??const[]).contains(ben);
    final cevapId=yanitMesajId,cevapMetin=yanitMetin,cevapUid=yanitGonderenUid;
    final mesajRef=ref.collection('messages').doc();
    final batch=FirebaseFirestore.instance.batch();

    batch.set(ref,{
      'members':[ben,widget.digerUid],
      'lastMessage':t,
      'updatedAt':FieldValue.serverTimestamp(),
      'unread_${widget.digerUid}':FieldValue.increment(1),
      if(!hazirlik.sohbetMevcut&&!arkadas)'requestSenderUid':ben,
      if(!hazirlik.sohbetMevcut&&!arkadas)'requestRecipientUid':widget.digerUid,
    },SetOptions(merge:true));
    batch.set(mesajRef,{
      'senderId':ben,
      'text':t,
      'type':'text',
      'createdAt':FieldValue.serverTimestamp(),
      'clientCreatedAt':clientCreatedAt,
      if(bitis!=null)'expiresAt':bitis,
      if(cevapId!=null)'replyToId':cevapId,
      if(cevapMetin!=null)'replyText':cevapMetin,
      if(cevapUid!=null)'replySenderId':cevapUid,
    });

    try{
      // Sunucu yazmayı kabul etmeden alanı temizleme. Böylece başarısız bir
      // mesaj gönderilmiş gibi görünmez ve art arda dokunma kopya üretmez.
      await batch.commit().timeout(const Duration(seconds:12));
      mesaj.clear();
      yaziyorZamanlayici?.cancel();
      yaziyorGonderildi=false;
      _mesajHazirlikSohbetMevcut=true;
      _mesajHazirlikSohbet={
        ...hazirlik.sohbet,
        'lastMessage':t,
        'updatedAt':clientCreatedAt,
      };
      if(mounted)setState((){
        yanitMesajId=null;
        yanitMetin=null;
        yanitGonderenUid=null;
      });
      unawaited(ref.set({'typing_$ben':false},SetOptions(merge:true)).catchError((_){ }));
      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir mesajın var',belgeId:widget.chatId).catchError((_){ }));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj gönderilemedi. Bağlantını kontrol edip tekrar dene.')));
    }finally{
      if(mounted)setState(()=>gonderiliyor=false);
    }
  }

  Future<void> medyaGonder(ImageSource kaynak) async {
    final ben=uid;
    if(ben==null)return;
    final hazirlik=await mesajGonderimHazirligi();
    if(hazirlik.engel!=null){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hazirlik.engel!)));
      return;
    }
    final x=await ImagePicker().pickImage(source:kaynak,imageQuality:78);
    if(x==null)return;
    try{
      final yol='chats/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.jpg';
      final url=await ngelxMedyaYukleBytes(
        bytes: await x.readAsBytes(),
        kind: 'chats',
        ext: 'jpg',
        legacyPath: yol,
      ).timeout(const Duration(seconds:12));
      final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
      final sureHam=hazirlik.sohbet['disappearingSeconds'];
      final sure=sureHam is num?sureHam.toInt():0;
      final simdi=DateTime.now(),clientCreatedAt=Timestamp.fromDate(simdi);
      final bitis=sure>0?Timestamp.fromDate(simdi.add(Duration(seconds:sure))):null;
      final arkadas=List<String>.from(hazirlik.diger['friends']??const[]).contains(ben);
      final mesajRef=ref.collection('messages').doc();
      final batch=FirebaseFirestore.instance.batch();
      batch.set(ref,{
        'members':[ben,widget.digerUid],
        'lastMessage':'📷 Fotoğraf',
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_${widget.digerUid}':FieldValue.increment(1),
        if(!hazirlik.sohbetMevcut&&!arkadas)'requestSenderUid':ben,
        if(!hazirlik.sohbetMevcut&&!arkadas)'requestRecipientUid':widget.digerUid,
      },SetOptions(merge:true));
      batch.set(mesajRef,{
        'senderId':ben,'text':'','type':'photo','mediaUrl':url,
        'createdAt':FieldValue.serverTimestamp(),'clientCreatedAt':clientCreatedAt,
        if(bitis!=null)'expiresAt':bitis,
      });
      _mesajHazirlikSohbetMevcut=true;
      _mesajHazirlikSohbet={...hazirlik.sohbet,'lastMessage':'📷 Fotoğraf','updatedAt':clientCreatedAt};
      unawaited(batch.commit().timeout(const Duration(seconds:12)).catchError((e){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Fotoğraf gönderilemedi. Tekrar dene.')));
      }));
      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir fotoğraf mesajın var',belgeId:widget.chatId).catchError((_){ }));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Medya hizmeti şu anda kullanılamıyor. Yazılı mesaj göndermeye devam edebilirsin.')));
    }
  }

  Future<bool> ekMesajGonder(Map<String,dynamic> veri,String sonMesaj,{String bildirim='Yeni bir mesajın var'})async{
    final ben=uid;
    if(ben==null)return false;
    final hazirlik=await mesajGonderimHazirligi();
    if(hazirlik.engel!=null){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(hazirlik.engel!)));
      return false;
    }
    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    final simdi=DateTime.now(),clientCreatedAt=Timestamp.fromDate(simdi);
    final arkadas=List<String>.from(hazirlik.diger['friends']??const[]).contains(ben);
    final mesajRef=ref.collection('messages').doc();
    final batch=FirebaseFirestore.instance.batch();
    batch.set(ref,{
      'members':[ben,widget.digerUid],
      'lastMessage':sonMesaj,
      'updatedAt':FieldValue.serverTimestamp(),
      'unread_${widget.digerUid}':FieldValue.increment(1),
      if(!hazirlik.sohbetMevcut&&!arkadas)'requestSenderUid':ben,
      if(!hazirlik.sohbetMevcut&&!arkadas)'requestRecipientUid':widget.digerUid,
    },SetOptions(merge:true));
    batch.set(mesajRef,{
      'senderId':ben,
      'createdAt':FieldValue.serverTimestamp(),
      'clientCreatedAt':clientCreatedAt,
      ...veri,
    });
    try{
      await batch.commit().timeout(const Duration(seconds:15));
      _mesajHazirlikSohbetMevcut=true;
      _mesajHazirlikSohbet={...hazirlik.sohbet,'lastMessage':sonMesaj,'updatedAt':clientCreatedAt};
      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:bildirim,belgeId:widget.chatId).catchError((_){ }));
      return true;
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Gönderilemedi. Bağlantını kontrol edip tekrar dene.')));
      return false;
    }
  }

  Future<void> dosyaGonder()async{
    final x=await openFile();
    if(x==null)return;
    try{
      final boyut=await x.length();
      if(boyut>30*1024*1024)throw Exception('Dosya 30 MB’den küçük olmalı.');
      final ad=x.name.isEmpty?'dosya':x.name;
      final uzanti=ad.contains('.')?ad.split('.').last.toLowerCase():'bin';
      final url=await ngelxMedyaYukleBytes(
        bytes:await x.readAsBytes(),
        kind:'chat-files',
        ext:uzanti,
        legacyPath:'chat-files/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}_$ad',
      ).timeout(const Duration(seconds:30));
      await ekMesajGonder({'type':'file','fileUrl':url,'fileName':ad,'fileSize':boyut},'📎 $ad',bildirim:'Sana bir dosya gönderdi');
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Dosya gönderilemedi: $e')));
    }
  }

  Future<void> dosyayiPaylas(Map<String,dynamic> v)async{
    final url=(v['fileUrl']??'').toString();
    if(url.isEmpty)return;
    try{
      final dir=await getTemporaryDirectory();
      final ad=(v['fileName']??'NgelX_dosya').toString().replaceAll(RegExp(r'[\\/:*?"<>|]'),'_');
      final yol='${dir.path}/$ad';
      await Dio().download(url,yol);
      await SharePlus.instance.share(ShareParams(files:[XFile(yol)],text:'NgelX dosyası: $ad'));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Dosya açılamadı.')));
    }
  }

  Future<void> konumGonder()async{
    final c=TextEditingController();
    final sonuc=await showDialog<String>(
      context:context,
      builder:(d)=>Theme(data:ThemeData.light(),child:AlertDialog(
        backgroundColor:Colors.white,
        title:const Text('Konum paylaş'),
        content:TextField(controller:c,autofocus:true,maxLength:160,decoration:const InputDecoration(prefixIcon:Icon(Icons.location_on_outlined),hintText:'Konum veya adres yaz')),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(d),child:const Text('Vazgeç')),
          FilledButton(onPressed:()=>Navigator.pop(d,c.text.trim()),child:const Text('Gönder')),
        ],
      )),
    );
    final metin=sonuc?.trim()??'';
    c.dispose();
    if(metin.isEmpty)return;
    await ekMesajGonder({'type':'location','text':metin,'locationText':metin},'📍 $metin',bildirim:'Sana bir konum gönderdi');
  }

  Future<void> sesKaydiDegistir()async{
    if(sesKaydediliyor){
      try{
        final yol=await _sesKaydedici.stop();
        final baslangic=sesKaydiBaslangic;
        if(mounted)setState(()=>sesKaydediliyor=false);
        sesKaydiBaslangic=null;
        if(yol==null||yol.isEmpty)return;
        final dosya=File(yol);
        if(!await dosya.exists())return;
        final bytes=await dosya.readAsBytes();
        if(bytes.isEmpty)return;
        final sure=baslangic==null?1:DateTime.now().difference(baslangic).inSeconds.clamp(1,600);
        final url=await ngelxMedyaYukleBytes(
          bytes:bytes,
          kind:'chat-audio',
          ext:'m4a',
          legacyPath:'chat-audio/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.m4a',
          contentType:'audio/mp4',
        ).timeout(const Duration(seconds:30));
        await ekMesajGonder({'type':'audio','audioUrl':url,'durationSeconds':sure},'🎤 Sesli mesaj',bildirim:'Sana sesli mesaj gönderdi');
        try{await dosya.delete();}catch(_){}
      }catch(e){
        if(mounted)setState(()=>sesKaydediliyor=false);
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Ses kaydı gönderilemedi: $e')));
      }
      return;
    }
    try{
      if(!await _sesKaydedici.hasPermission()){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli mesaj için mikrofon izni gerekli.')));
        return;
      }
      final dir=await getTemporaryDirectory();
      final yol='${dir.path}/ngelx_voice_${DateTime.now().millisecondsSinceEpoch}.m4a';
      await _sesKaydedici.start(
        const rec.RecordConfig(encoder:rec.AudioEncoder.aacLc,bitRate:96000,sampleRate:44100),
        path:yol,
      );
      sesKaydiBaslangic=DateTime.now();
      if(mounted)setState(()=>sesKaydediliyor=true);
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Ses kaydı başlatılamadı: $e')));
    }
  }

  Future<void> mesajTepkiDegistir(QueryDocumentSnapshot<Map<String,dynamic>> d,String emoji)async{
    final ben=uid;if(ben==null)return;
    final mevcut=Map<String,dynamic>.from(d.data()['reactions']??const{});
    final alan='reactions.'+ben;
    if((mevcut[ben]??'').toString()==emoji)await d.reference.update({alan:FieldValue.delete()});
    else await d.reference.set({alan:emoji},SetOptions(merge:true));
  }

  Future<void> mesajKalpBirak(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final ben=uid;if(ben==null)return;
    try{
      await d.reference.set({'reactions.$ben':'❤️'},SetOptions(merge:true));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Tepki eklenemedi.')));
    }
  }

  Future<String?> mesajTepkisiSec()async=>showModalBottomSheet<String>(
    context:context,backgroundColor:Colors.white,showDragHandle:true,
    builder:(c)=>SafeArea(child:Padding(
      padding:const EdgeInsets.all(18),
      child:Wrap(spacing:14,runSpacing:14,children:
        ['❤️','😂','😮','😢','😡','👍','👏','🔥','🎉','🙏','😍','🤔']
          .map((e)=>InkWell(onTap:()=>Navigator.pop(c,e),child:Padding(padding:const EdgeInsets.all(8),child:Text(e,style:const TextStyle(fontSize:30))))).toList(),
      ),
    )),
  );

  Future<void> mesajHatirlat(QueryDocumentSnapshot<Map<String,dynamic>> d,String metin)async{
    final ben=uid;if(ben==null)return;
    final sec=await showModalBottomSheet<Duration>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const ListTile(title:Text('Hatırlatma ayarla',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))),
        for(final e in const [('1 saat',Duration(hours:1)),('4 saat',Duration(hours:4)),('Yarın',Duration(days:1)),('1 hafta',Duration(days:7))])
          ListTile(title:Text(e.$1,style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,e.$2)),
      ]))),
    );
    if(sec==null)return;
    await FirebaseFirestore.instance.collection('users').doc(ben).collection('messageReminders').add({
      'chatId':widget.chatId,'messageId':d.id,'text':metin,
      'remindAt':Timestamp.fromDate(DateTime.now().add(sec)),
      'createdAt':FieldValue.serverTimestamp(),
    });
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hatırlatma kaydedildi.')));
  }

  Widget _mesajAksiyon(IconData i,String t,VoidCallback f,{bool etkin=true})=>Opacity(
    opacity:etkin?1:.35,
    child:InkWell(
      onTap:etkin?f:null,
      borderRadius:BorderRadius.circular(16),
      child:SizedBox(width:78,child:Padding(
        padding:const EdgeInsets.symmetric(vertical:8),
        child:Column(children:[
          Icon(i,color:const Color(0xFF1836D8),size:29),
          const SizedBox(height:6),
          Text(t,maxLines:2,textAlign:TextAlign.center,style:const TextStyle(fontSize:12,color:Colors.black87)),
        ]),
      )),
    ),
  );

  Future<void> mesajMenusu(QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final v=d.data(),benim=v['senderId']==uid,metin=(v['text']??v['message']??v['content']??'').toString();
    final sec=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,isScrollControlled:true,showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
      builder:(c)=>SafeArea(child:Padding(
        padding:const EdgeInsets.fromLTRB(12,0,12,14),
        child:Column(mainAxisSize:MainAxisSize.min,children:[
          Container(
            margin:const EdgeInsets.fromLTRB(6,2,6,12),
            padding:const EdgeInsets.symmetric(horizontal:4,vertical:7),
            decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(28),boxShadow:const [BoxShadow(color:Color(0x22000000),blurRadius:18,offset:Offset(0,5))]),
            child:Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
              for(final e in const ['❤️','😂','😮','😢','😡','👍'])
                InkWell(onTap:()=>Navigator.pop(c,'reaction:'+e),child:Padding(padding:const EdgeInsets.symmetric(horizontal:4,vertical:5),child:Text(e,style:const TextStyle(fontSize:25)))),
              InkWell(onTap:()=>Navigator.pop(c,'reaction_more'),child:const CircleAvatar(radius:16,backgroundColor:Color(0xFFF1F2F4),child:Icon(Icons.add,color:Colors.black87))),
            ]),
          ),
          Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[
            _mesajAksiyon(Icons.reply_rounded,'Yanıtla',()=>Navigator.pop(c,'reply')),
            _mesajAksiyon(Icons.copy_rounded,'Kopyala',()=>Navigator.pop(c,'copy'),etkin:metin.isNotEmpty),
            _mesajAksiyon(Icons.schedule_rounded,'Hatırlatma ayarla',()=>Navigator.pop(c,'remind')),
            _mesajAksiyon(Icons.more_horiz_rounded,'Daha fazla',()=>Navigator.pop(c,'more')),
          ]),
        ]),
      )),
    );
    if(sec==null)return;
    await ngelxOverlayKapanisiniBekle();
    if(!mounted)return;
    if(sec.startsWith('reaction:')){await mesajTepkiDegistir(d,sec.substring(9));return;}
    if(sec=='reaction_more'){final e=await mesajTepkisiSec();if(e!=null)await mesajTepkiDegistir(d,e);return;}
    if(sec=='copy'&&metin.isNotEmpty){await Clipboard.setData(ClipboardData(text:metin));return;}
    if(sec=='reply'){
      final tur=(v['type']??'text').toString();
      setState((){
        yanitMesajId=d.id;
        yanitMetin=metin.trim().isNotEmpty?metin.trim():(tur=='photo'?'📷 Fotoğraf':tur=='shared_content'?'NgelX paylaşımı':'Mesaj');
        yanitGonderenUid=(v['senderId']??'').toString();
      });
      return;
    }
    if(sec=='remind'){await mesajHatirlat(d,metin);return;}
    if(sec!='more')return;

    final fazla=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        if(benim&&metin.isNotEmpty)ListTile(leading:const Icon(Icons.edit_outlined),title:const Text('Düzenle',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'edit')),
        ListTile(leading:Icon(v['pinned']==true?Icons.push_pin:Icons.push_pin_outlined,color:Colors.blue),title:Text(v['pinned']==true?'Sabitlemeyi kaldır':'Mesajı sabitle',style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'pin')),
        if(benim)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:const Text('Herkesten sil',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'delete')),
        if(!benim)ListTile(leading:const Icon(Icons.flag_outlined),title:const Text('Şikâyet et',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'report')),
      ]))),
    );
    if(fazla==null)return;
    await ngelxOverlayKapanisiniBekle();
    if(!mounted)return;
    if(fazla=='pin')await d.reference.set({'pinned':v['pinned']!=true,'pinnedAt':FieldValue.serverTimestamp(),'pinnedBy':uid},SetOptions(merge:true));
    else if(fazla=='delete'){
      final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
        backgroundColor:Colors.white,title:const Text('Mesaj silinsin mi?'),content:const Text('Mesaj sohbetten kalıcı olarak kaldırılacak.'),
        actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:()=>Navigator.pop(c,true),child:const Text('Sil'))],
      ))??false;
      if(ok)await d.reference.delete();
    }else if(fazla=='report'){
      if(mounted)await sikayetEt(context,hedefTuru:'mesaj',hedefId:widget.chatId+'/'+d.id,hedefUid:widget.digerUid);
    }else if(fazla=='edit'){
      final x=TextEditingController(text:metin);
      final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
        backgroundColor:Colors.white,title:const Text('Mesajı düzenle'),content:TextField(controller:x,maxLength:2000,maxLines:5),
        actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Kaydet'))],
      ))??false;
      if(ok&&x.text.trim().isNotEmpty)await d.reference.update({'text':x.text.trim(),'editedAt':FieldValue.serverTimestamp()});
      x.dispose();
    }
  }


  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{double fontSize=16,bool goruldu=false,String quickReaction='❤️'}){
    final v=d.data(),ben=v['senderId']==uid,tur=(v['type']??'text').toString();
    final photo=tur=='photo',shared=tur=='shared_content',audio=tur=='audio',file=tur=='file',location=tur=='location',call=tur=='call',storyReply=tur=='story_reply';
    final metin=(v['text']??v['message']??v['content']??'').toString().trim(),saat=mesajSaati(v['createdAt']??v['clientCreatedAt']);
    final gizlenecek=gizliKelimeFiltresi&&metin.isNotEmpty&&gizliKelimeListesi.any((x)=>x.trim().isNotEmpty&&metin.toLowerCase().contains(x.toLowerCase()));
    final gosterilecekMetin=gizlenecek?'Gizli kelime filtresi nedeniyle gizlendi.':metin;
    final tepkiler=Map<String,dynamic>.from(v['reactions']??{});
    final sayilar=<String,int>{};
    for(final x in tepkiler.values){final e=x.toString();sayilar[e]=(sayilar[e]??0)+1;}
    return Align(
      alignment:ben?Alignment.centerRight:Alignment.centerLeft,
      child:GestureDetector(
        behavior:HitTestBehavior.opaque,
        onLongPress:()=>mesajMenusu(d),
        onDoubleTap:()=>mesajTepkiDegistir(d,quickReaction),
        onTap:photo
          ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:(v['mediaUrl']??'').toString())))
          : shared
            ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:(v['contentId']??'').toString())))
            : file
              ? ()=>dosyayiPaylas(v)
              : location
                ? ()async{await Clipboard.setData(ClipboardData(text:(v['locationText']??v['text']??'').toString()));if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Konum metni kopyalandı.')));}
                : null,
        child:Container(
          constraints:const BoxConstraints(maxWidth:290),
          margin:const EdgeInsets.symmetric(horizontal:4,vertical:5),
          padding:EdgeInsets.all(photo?4:12),
          decoration:BoxDecoration(color:ben?const Color(0xFF1687FF):const Color(0xFFF0F1F4),borderRadius:BorderRadius.circular(20)),
          child:Column(crossAxisAlignment:CrossAxisAlignment.end,mainAxisSize:MainAxisSize.min,children:[
            if((v['replyText']??'').toString().trim().isNotEmpty)
              Container(
                width:double.infinity,
                margin:const EdgeInsets.only(bottom:8),
                padding:const EdgeInsets.symmetric(horizontal:10,vertical:8),
                decoration:BoxDecoration(
                  color:ben?Colors.white.withValues(alpha:.16):Colors.white,
                  borderRadius:BorderRadius.circular(12),
                  border:Border(left:BorderSide(color:ben?Colors.white:const Color(0xFF1836D8),width:3)),
                ),
                child:Text((v['replyText']??'').toString(),maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:12.5,fontWeight:FontWeight.w600)),
              ),
            if(photo)
              IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(16),child:CachedNetworkImage(imageUrl:(v['mediaUrl']??'').toString(),width:230,fit:BoxFit.cover)))
            else if(shared)
              IgnorePointer(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(children:[Icon(Icons.play_circle_fill_rounded,color:ben?Colors.white:mavi),const SizedBox(width:7),Text('NgelX paylaşımı',style:TextStyle(color:ben?Colors.white:Colors.black87,fontWeight:FontWeight.w900))]),
                const SizedBox(height:8),Text(metin,maxLines:4,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white70:Colors.black54)),
              ]))
            else if(storyReply)
              Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
                ClipRRect(borderRadius:BorderRadius.circular(12),child:CachedNetworkImage(imageUrl:(v['storyUrl']??'').toString(),width:62,height:82,fit:BoxFit.cover,errorWidget:(_,__,___)=>const SizedBox(width:62,height:82,child:Icon(Icons.auto_stories)))),
                const SizedBox(width:10),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text(v['reaction']==true?'Hikâye tepkisi':'Hikâye yanıtı',style:TextStyle(color:ben?Colors.white70:Colors.black54,fontSize:11,fontWeight:FontWeight.w700)),
                  const SizedBox(height:4),
                  Text(metin.isEmpty?'Hikâyeye yanıt verdi':metin,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:fontSize,fontWeight:FontWeight.w800)),
                ])),
              ])
            else if(audio)
              NgelXSesliMesaj(url:(v['audioUrl']??'').toString(),benim:ben,durationSeconds:(v['durationSeconds'] as num?)?.toInt()??0)
            else if(file)
              Row(children:[
                Icon(Icons.insert_drive_file_rounded,color:ben?Colors.white:const Color(0xFF1836D8),size:34),
                const SizedBox(width:9),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text((v['fileName']??'Dosya').toString(),maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white:Colors.black87,fontWeight:FontWeight.w800)),
                  Text('Dokun: aç / paylaş',style:TextStyle(color:ben?Colors.white70:Colors.black54,fontSize:11)),
                ])),
              ])
            else if(location)
              Row(children:[
                Icon(Icons.location_on_rounded,color:ben?Colors.white:Colors.redAccent,size:34),
                const SizedBox(width:9),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text('Konum',style:TextStyle(color:ben?Colors.white70:Colors.black54,fontSize:11,fontWeight:FontWeight.w700)),
                  Text((v['locationText']??metin).toString(),style:TextStyle(color:ben?Colors.white:Colors.black87,fontWeight:FontWeight.w800)),
                  Text('Dokun: adresi kopyala',style:TextStyle(color:ben?Colors.white70:Colors.black54,fontSize:10)),
                ])),
              ])
            else if(call)
              Builder(builder:(_){
                final goruntulu=v['callVideo']==true,durum=(v['callStatus']??'ringing').toString();
                final baslik=(durum=='rejected'||durum=='missed')
                  ? (goruntulu?'Cevapsız görüntülü arama':'Cevapsız sesli arama')
                  : (goruntulu?'Görüntülü arama':'Sesli arama');
                return Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                  Row(children:[
                    CircleAvatar(backgroundColor:durum=='rejected'||durum=='missed'?Colors.redAccent:Colors.green,child:Icon(goruntulu?Icons.videocam_rounded:Icons.call_rounded,color:Colors.white)),
                    const SizedBox(width:10),
                    Expanded(child:Text(baslik,style:TextStyle(color:ben?Colors.white:Colors.black87,fontWeight:FontWeight.w900))),
                  ]),
                  const SizedBox(height:9),
                  FilledButton.tonal(onPressed:()=>aramaBaslat(goruntulu),child:const Text('Geri ara')),
                ]);
              })
            else Text(gosterilecekMetin.isEmpty?'Mesaj içeriği bulunamadı':gosterilecekMetin,softWrap:true,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:fontSize,height:1.3,fontStyle:gizlenecek?FontStyle.italic:FontStyle.normal)),
            if(v['editedAt']!=null)Text('düzenlendi',style:TextStyle(fontSize:9,color:ben?Colors.white60:Colors.black38)),
            if(sayilar.isNotEmpty)Padding(
              padding:const EdgeInsets.only(top:7),
              child:Wrap(spacing:5,runSpacing:5,children:sayilar.entries.map((e)=>Container(
                padding:const EdgeInsets.symmetric(horizontal:7,vertical:3),
                decoration:BoxDecoration(color:ben?Colors.white.withValues(alpha:.18):Colors.white,borderRadius:BorderRadius.circular(14)),
                child:Text(e.value>1?e.key+' '+e.value.toString():e.key,style:const TextStyle(fontSize:15)),
              )).toList()),
            ),
            if(saat.isNotEmpty)Padding(padding:const EdgeInsets.only(top:4),child:Row(mainAxisSize:MainAxisSize.min,children:[
              Text(saat,style:TextStyle(fontSize:10,color:ben?Colors.white70:Colors.black45)),
              if(goruldu)...[
                const SizedBox(width:5),
                Text('Görüldü',style:TextStyle(fontSize:10,color:ben?Colors.white70:Colors.blueGrey)),
              ],
            ])),
          ]),
        ),
      ),
    );
  }

  Widget sohbetUstBilgi()=>Padding(
    padding:const EdgeInsets.fromLTRB(12,8,12,18),
    child:Column(children:[
      FilledButton.tonal(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.digerUid))),child:const Text('Profili Gör')),
      const SizedBox(height:12),
      const Row(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.start,children:[
        Icon(Icons.lock_rounded,size:15,color:Colors.black45),
        SizedBox(width:6),
        Flexible(child:Text(
          'Bu sohbet güvenli bağlantı üzerinden çalışır. Mesaj ve medya içeriklerini yalnızca bu sohbette paylaştığın kişiler görebilir.',
          textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:13,height:1.35),
        )),
      ]),
    ]),
  );

  Future<void> emojiSec()async{final e=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Padding(padding:const EdgeInsets.all(18),child:Wrap(spacing:14,runSpacing:14,children:['😀','😊','😂','😍','🥰','😎','😭','😡','👍','👏','🙏','❤️','🔥','🎉','✨','💯','🤔','😴','🙌','🤝'].map((x)=>InkWell(onTap:()=>Navigator.pop(c,x),child:Text(x,style:const TextStyle(fontSize:30)))).toList()))));if(e!=null){mesaj.text='${mesaj.text}$e';mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}}

  Future<void> mentionAra(String deger)async{
    final parca=deger.split(RegExp(r'\s+')).last;
    if(!parca.startsWith('@')){if(mentionOnerileri.isNotEmpty&&mounted)setState(()=>mentionOnerileri.clear());return;}
    final ara=parca.substring(1).toLowerCase(),sonuc=<Map<String,String>>[];
    if('herkes'.contains(ara))sonuc.add({'uid':'all','username':'herkes','name':'Herkes'});
    try{
      final d=await FirebaseFirestore.instance.collection('users').doc(widget.digerUid).get(),v=d.data()??<String,dynamic>{};
      final kullanici=(v['username']??'').toString().trim(),ad=(v['displayName']??kullanici).toString().trim(),aranan='$kullanici $ad'.toLowerCase();
      if(kullanici.isNotEmpty&&(ara.isEmpty||aranan.contains(ara)))sonuc.add({'uid':widget.digerUid,'username':kullanici,'name':ad.isEmpty?kullanici:ad});
    }catch(_){}
    if(mounted)setState((){mentionOnerileri..clear()..addAll(sonuc.take(5));});
  }
  void mentionEkle(String kullanici){final metin=mesaj.text,sonBosluk=metin.lastIndexOf(RegExp(r'\s'));mesaj.text='${sonBosluk<0?'':metin.substring(0,sonBosluk+1)}@$kullanici ';mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);setState(()=>mentionOnerileri.clear());}

  Future<void> aramaBaslat(bool goruntulu)async{
    final ben=uid;
    if(ben==null||aramaBaslatiliyor)return;
    setState(()=>aramaBaslatiliyor=true);
    final odaAdi='chat_${widget.chatId}_${DateTime.now().millisecondsSinceEpoch}';
    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    try{
      final mesajRef=ref.collection('messages').doc();
      final aramaVerisi=<String,dynamic>{
        'callStatus':'ringing',
        'callRoomName':odaAdi,
        'callStartedBy':ben,
        'callVideo':goruntulu,
        'callTitle':widget.ad,
        'callParticipants':<String>[ben],
        'callCreatedAt':FieldValue.serverTimestamp(),
        'callMessageId':mesajRef.id,
        'members':<String>[ben,widget.digerUid],
        'lastMessage':goruntulu?'📹 Görüntülü arama':'📞 Sesli arama',
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_${widget.digerUid}':FieldValue.increment(1),
      };
      final batch=FirebaseFirestore.instance.batch();
      batch.set(ref,aramaVerisi,SetOptions(merge:true));
      batch.set(mesajRef,{
        'senderId':ben,
        'type':'call',
        'text':'',
        'callVideo':goruntulu,
        'callStatus':'ringing',
        'roomName':odaAdi,
        'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
      });
      await batch.commit().timeout(const Duration(seconds:10));
      if(!mounted)return;
      unawaited(uygulamaBildirimiGonder(
        toUid:widget.digerUid,
        fromUid:ben,
        tur:'call',
        metin:goruntulu?'Görüntülü arama':'Sesli arama',
        belgeId:widget.chatId,
      ).catchError((_){ }));
      setState(()=>aramaBaslatiliyor=false);
      await Navigator.push(
        context,
        MaterialPageRoute(builder:(_)=>NgelXAramaPage(
          roomName:odaAdi,
          baslik:widget.ad,
          foto:widget.foto,
          goruntulu:goruntulu,
          aramaRef:ref,
        )),
      );
    }on TimeoutException{
      if(!mounted)return;
      setState(()=>aramaBaslatiliyor=false);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arama bağlantısı kurulamadı. İnternetini kontrol edip tekrar dene.')));
    }catch(_){
      if(!mounted)return;
      setState(()=>aramaBaslatiliyor=false);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arama başlatılamadı. Lütfen tekrar dene.')));
    }
  }

  void bilgi()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetBilgiPage(uid:widget.digerUid,ad:widget.ad,foto:widget.foto,chatId:widget.chatId)));

  @override
  void initState(){
    super.initState();
    final sohbetRef=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
    _chatAkisi=sohbetRef.snapshots();
    _mesajAkisi=sohbetRef.collection('messages').orderBy('createdAt').limitToLast(100).snapshots();
    unawaited(mesajGonderimHazirligi());
    if(uid!=null){
      unawaited(_okunduGuncelle());
      FirebaseFirestore.instance.collection('users').doc(uid).get().then((d){
        final v=d.data()??<String,dynamic>{};
        if(mounted)setState((){
          gizliKelimeFiltresi=v['hiddenWordsFilter']!=false;
          gizliKelimeListesi=List<String>.from(v['hiddenWords']??const[]);
        });
      });
    }
  }

  @override
  void dispose(){
    yaziyorZamanlayici?.cancel();
    sureliMesajZamanlayici?.cancel();
    final ben=uid;
    if(ben!=null)unawaited(FirebaseFirestore.instance.collection('chats').doc(widget.chatId).set({'typing_$ben':false},SetOptions(merge:true)));
    if(sesKaydediliyor)unawaited(_sesKaydedici.cancel());
    unawaited(_sesKaydedici.dispose());
    mesaj.dispose();liste.dispose();super.dispose();
  }
  void sonaGit(){WidgetsBinding.instance.addPostFrameCallback((_){
    if(!mounted||!liste.hasClients)return;
    final hedef=liste.position.maxScrollExtent;
    if(_ilkMesajKaydirma){
      _ilkMesajKaydirma=false;
      if(hedef>0)liste.jumpTo(hedef);
      return;
    }
    if(hedef-liste.position.pixels>320)return;
    if((liste.position.pixels-hedef).abs()<2)return;
    liste.animateTo(hedef,duration:const Duration(milliseconds:180),curve:Curves.easeOut);
  });}

  @override
  Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(
    appBar:AppBar(
      leading:const BackButton(color:Colors.blue),
      title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,s){
        final ham=s.data?.data()?['nicknames'],nicks=ham is Map?Map<String,dynamic>.from(ham):<String,dynamic>{},takma=(uid==null?'':(nicks[uid]??'').toString()).trim(),gorunenAd=takma.isNotEmpty?takma:widget.ad;
        return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),
          builder:(_,u){
            final p=u.data?.data()??<String,dynamic>{};
            String durum='';
            if(p['showActivityStatus']!=false){
              if(p['isOnline']==true)durum='Şu an aktif';
              else if(p['lastSeenAt'] is Timestamp){
                final fark=DateTime.now().difference((p['lastSeenAt'] as Timestamp).toDate());
                if(fark.inMinutes<60)durum='${fark.inMinutes.clamp(1,59)} dk önce aktifti';
                else if(fark.inHours<24)durum='${fark.inHours} saat önce aktifti';
                else durum='${fark.inDays} gün önce aktifti';
              }
            }
            return InkWell(
              onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.digerUid))),
              child:Row(children:[
                CircleAvatar(radius:20,backgroundImage:widget.foto.isEmpty?null:CachedNetworkImageProvider(widget.foto),child:widget.foto.isEmpty?const Icon(Icons.person):null),
                const SizedBox(width:9),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
                  Text(gorunenAd,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:16,fontWeight:FontWeight.w900)),
                  if(durum.isNotEmpty)Text(durum,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:11,color:Colors.black54,fontWeight:FontWeight.w500)),
                ])),
              ]),
            );
          },
        );
      }),
      actions:[
        IconButton(
          tooltip:'Sesli arama',
          onPressed:aramaBaslatiliyor?null:()=>aramaBaslat(false),
          icon:aramaBaslatiliyor
            ? const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2))
            : const Icon(Icons.call,color:Colors.blue),
        ),
        IconButton(
          tooltip:'Görüntülü arama',
          onPressed:aramaBaslatiliyor?null:()=>aramaBaslat(true),
          icon:const Icon(Icons.videocam,color:Colors.blue),
        ),
        IconButton(onPressed:bilgi,icon:const Icon(Icons.info,color:Colors.blue)),
      ],
    ),
    body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,tema){final veri=tema.data?.data()??<String,dynamic>{},ham=veri['theme_$uid'];final arkaPlan=ham is int?Color(ham):Colors.white,arkaPlanUrl=(veri['backgroundUrl_$uid']??'').toString(),hizliEmoji=(veri['quickEmoji_$uid']??'👍').toString(),arkaPlanOpaklik=(veri['backgroundOpacity_$uid'] is num?(veri['backgroundOpacity_$uid'] as num).toDouble():.30).clamp(.05,.85).toDouble(),mesajYaziBoyutu=(veri['messageFontSize_$uid'] is num?(veri['messageFontSize_$uid'] as num).toDouble():16.0).clamp(12.0,22.0).toDouble();return Container(decoration:BoxDecoration(color:arkaPlan,image:arkaPlanUrl.isEmpty?null:DecorationImage(image:CachedNetworkImageProvider(arkaPlanUrl),fit:BoxFit.cover,opacity:arkaPlanOpaklik)),child:Column(children:[
      Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:_mesajAkisi,
        builder:(_,s){
          final tumDocs=s.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[];
          final simdi=DateTime.now();
          final docs=tumDocs.where((d){
            final x=d.data()['expiresAt'];
            return x is! Timestamp||x.toDate().isAfter(simdi);
          }).toList();
          sureliMesajTakvimi(docs);
          final okunmamis=(veri['unread_$uid'] as num?)?.toInt()??0;
          if(uid!=null&&s.hasData&&okunmamis>0)unawaited(_okunduGuncelle());
          if(s.hasData)sonaGit();
          QueryDocumentSnapshot<Map<String,dynamic>>? sonBenim;
          for(final d in docs){if(d.data()['senderId']==uid)sonBenim=d;}
          final digerOkuma=veri['readReceipts_${widget.digerUid}']!=false?veri['lastReadAt_${widget.digerUid}']:null;
          return ListView.builder(
            controller:liste,
            padding:const EdgeInsets.all(12),
            itemCount:docs.length+1,
            itemBuilder:(_,i){
              if(i==0)return sohbetUstBilgi();
              final d=docs[i-1];
              bool goruldu=false;
              if(sonBenim?.id==d.id&&digerOkuma is Timestamp&&d.data()['createdAt'] is Timestamp){
                goruldu=digerOkuma.millisecondsSinceEpoch>=(d.data()['createdAt'] as Timestamp).millisecondsSinceEpoch;
              }
              return ozelMesajKarti(d,fontSize:mesajYaziBoyutu,goruldu:goruldu,quickReaction:hizliEmoji);
            },
          );
        },
      )),
      Builder(builder:(_){
        final yaziyor=veri['typing_${widget.digerUid}']==true;
        final at=veri['typingAt_${widget.digerUid}'];
        final taze=at is Timestamp&&DateTime.now().difference(at.toDate()).inSeconds<6;
        if(!yaziyor||!taze)return const SizedBox.shrink();
        return Padding(
          padding:const EdgeInsets.fromLTRB(18,4,18,2),
          child:Align(alignment:Alignment.centerLeft,child:Text('${widget.ad} yazıyor…',style:const TextStyle(color:Colors.black54,fontSize:12,fontStyle:FontStyle.italic))),
        );
      }),
      if(mentionOnerileri.isNotEmpty)Container(color:Colors.white.withValues(alpha:.96),child:Column(mainAxisSize:MainAxisSize.min,children:mentionOnerileri.map((u)=>ListTile(dense:true,leading:CircleAvatar(radius:15,child:Icon(u['uid']=='all'?Icons.groups:Icons.person,size:17)),title:Text(u['name']??'Kullanıcı'),subtitle:Text('@${u['username']??''}'),onTap:()=>mentionEkle(u['username']??''))).toList())),
      if(yanitMetin!=null)Container(
        margin:const EdgeInsets.fromLTRB(10,4,10,2),
        padding:const EdgeInsets.fromLTRB(12,8,4,8),
        decoration:BoxDecoration(color:Colors.white.withValues(alpha:.94),borderRadius:BorderRadius.circular(14),border:const Border(left:BorderSide(color:Color(0xFF1836D8),width:3))),
        child:Row(children:[
          const Icon(Icons.reply_rounded,color:Color(0xFF1836D8),size:20),const SizedBox(width:8),
          Expanded(child:Text(yanitMetin!,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600))),
          IconButton(onPressed:()=>setState((){yanitMesajId=null;yanitMetin=null;yanitGonderenUid=null;}),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
        ]),
      ),
      SafeArea(top:false,child:Padding(
        padding:const EdgeInsets.fromLTRB(4,7,4,8),
        child:Row(children:[
          IconButton(
            tooltip:'Ekle',
            onPressed:()async{
              final secim=await showModalBottomSheet<String>(
                context:context,backgroundColor:Colors.white,showDragHandle:true,
                builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
                  ListTile(leading:const Icon(Icons.bookmark_rounded,color:Color(0xFF1836D8)),title:const Text('Kaydedilenler',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'saved')),
                  ListTile(leading:const Icon(Icons.attach_file_rounded,color:Color(0xFF1836D8)),title:const Text('Dosyalar',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'file')),
                  ListTile(leading:const Icon(Icons.sports_esports_rounded,color:Color(0xFF1836D8)),title:const Text('Oyun',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'game')),
                  ListTile(leading:const Icon(Icons.location_on_rounded,color:Color(0xFF1836D8)),title:const Text('Konum',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'location')),
                  const Divider(),
                  ListTile(leading:const Icon(Icons.camera_alt_outlined,color:Colors.blue),title:const Text('Kamera',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'camera')),
                  ListTile(leading:const Icon(Icons.photo_library_outlined,color:Colors.blue),title:const Text('Fotoğraf',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'gallery')),
                ]))),
              );
              if(!mounted||secim==null)return;
              await Future<void>.delayed(const Duration(milliseconds:320));
              if(!mounted)return;
              if(secim=='camera'||secim=='gallery')await medyaGonder(secim=='camera'?ImageSource.camera:ImageSource.gallery);
              else if(secim=='saved')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const KaydedilenlerPage()));
              else if(secim=='file')await dosyaGonder();
              else if(secim=='game')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXMiniOyunPage()));
              else if(secim=='location')await konumGonder();
            },
            icon:const Icon(Icons.add_circle,color:Color(0xFF1836D8),size:29),
          ),
          IconButton(onPressed:()=>medyaGonder(ImageSource.camera),icon:const Icon(Icons.camera_alt,color:Color(0xFF1836D8))),
          IconButton(onPressed:()=>medyaGonder(ImageSource.gallery),icon:const Icon(Icons.photo_library,color:Color(0xFF1836D8))),
          IconButton(
            tooltip:sesKaydediliyor?'Kaydı bitir ve gönder':'Sesli mesaj',
            onPressed:sesKaydiDegistir,
            icon:Icon(sesKaydediliyor?Icons.stop_circle_rounded:Icons.mic_rounded,color:sesKaydediliyor?Colors.red:const Color(0xFF1836D8)),
          ),
          Expanded(child:TextField(
            controller:mesaj,onChanged:mesajDegisti,onSubmitted:(_)=>gonder(),
            decoration:InputDecoration(
              hintText:sesKaydediliyor?'Ses kaydı alınıyor…':'Mesaj',filled:true,fillColor:sesKaydediliyor?const Color(0xFFFFEEF0):const Color(0xFFF3F4F6),
              contentPadding:const EdgeInsets.symmetric(horizontal:16,vertical:10),
              border:OutlineInputBorder(borderRadius:BorderRadius.circular(24),borderSide:BorderSide.none),
            ),
          )),
          IconButton(tooltip:'Emoji seç',onPressed:emojiSec,icon:const Icon(Icons.emoji_emotions,color:Color(0xFF1836D8))),
          ValueListenableBuilder<TextEditingValue>(
            valueListenable:mesaj,
            builder:(_,v,__){
              if(v.text.trim().isEmpty)return IconButton(
                tooltip:'Hızlı emoji gönder',
                onPressed:(){mesaj.text=hizliEmoji;gonder();},
                icon:Text(hizliEmoji,style:const TextStyle(fontSize:27)),
              );
              return IconButton(
                onPressed:gonderiliyor?null:gonder,
                icon:gonderiliyor?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2)):const Icon(Icons.send,color:Color(0xFF1836D8)),
              );
            },
          ),
        ]),
      )),
    ]));}),
  ));
}

class NgelXSesliMesaj extends StatefulWidget{
  final String url;
  final bool benim;
  final int durationSeconds;
  const NgelXSesliMesaj({super.key,required this.url,required this.benim,this.durationSeconds=0});
  @override State<NgelXSesliMesaj> createState()=>_NgelXSesliMesajState();
}
class _NgelXSesliMesajState extends State<NgelXSesliMesaj>{
  final AudioPlayer oynatici=AudioPlayer();
  bool hazirlaniyor=false;
  Future<void> degistir()async{
    if(widget.url.isEmpty||hazirlaniyor)return;
    if(oynatici.playing){await oynatici.pause();return;}
    try{
      if(oynatici.duration==null){
        if(mounted)setState(()=>hazirlaniyor=true);
        await oynatici.setUrl(widget.url);
      }
      if(oynatici.processingState==ProcessingState.completed)await oynatici.seek(Duration.zero);
      await oynatici.play();
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sesli mesaj oynatılamadı.')));
    }finally{
      if(mounted)setState(()=>hazirlaniyor=false);
    }
  }
  @override void dispose(){unawaited(oynatici.dispose());super.dispose();}
  @override Widget build(BuildContext context)=>StreamBuilder<PlayerState>(
    stream:oynatici.playerStateStream,
    builder:(_,snap){
      final playing=snap.data?.playing==true;
      return Row(children:[
        IconButton.filledTonal(
          onPressed:hazirlaniyor?null:degistir,
          icon:hazirlaniyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2)):Icon(playing?Icons.pause_rounded:Icons.play_arrow_rounded),
        ),
        const SizedBox(width:6),
        Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
          Text('Sesli mesaj',style:TextStyle(color:widget.benim?Colors.white:Colors.black87,fontWeight:FontWeight.w900)),
          if(widget.durationSeconds>0)Text('${widget.durationSeconds} sn',style:TextStyle(color:widget.benim?Colors.white70:Colors.black54,fontSize:11)),
        ])),
        Icon(Icons.graphic_eq_rounded,color:widget.benim?Colors.white70:const Color(0xFF1836D8)),
      ]);
    },
  );
}

class NgelXMiniOyunPage extends StatefulWidget{
  const NgelXMiniOyunPage({super.key});
  @override State<NgelXMiniOyunPage> createState()=>_NgelXMiniOyunPageState();
}
class _NgelXMiniOyunPageState extends State<NgelXMiniOyunPage>{
  int puan=0,hamle=0;
  final hedefler=const ['🎯','⭐','💎','🔥','⚡','🎉'];
  void vur(){setState((){puan++;hamle=(hamle+1)%hedefler.length;});}
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('NgelX Mini Oyun')),
      body:SafeArea(child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const Text('Hedefe dokun',style:TextStyle(fontSize:25,fontWeight:FontWeight.w900)),
        const SizedBox(height:8),
        Text('Puan: $puan',style:const TextStyle(fontSize:18,color:Colors.black54)),
        const SizedBox(height:38),
        InkWell(onTap:vur,borderRadius:BorderRadius.circular(80),child:Container(
          width:150,height:150,alignment:Alignment.center,
          decoration:BoxDecoration(shape:BoxShape.circle,color:const Color(0xFFF1E9FF),border:Border.all(color:mor,width:4)),
          child:Text(hedefler[hamle],style:const TextStyle(fontSize:64)),
        )),
        const SizedBox(height:30),
        OutlinedButton.icon(onPressed:()=>setState(()=>puan=0),icon:const Icon(Icons.refresh),label:const Text('Sıfırla')),
      ]))),
    ),
  );
}

class SohbetBilgiPage extends StatelessWidget{
  final String uid,ad,foto,chatId;
  const SohbetBilgiPage({super.key,required this.uid,required this.ad,required this.foto,required this.chatId});

  Future<void> takmaAd(BuildContext context)async{final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;final chat=await FirebaseFirestore.instance.collection('chats').doc(chatId).get(),c=TextEditingController(text:(chat.data()?['nicknames']?[me]??'').toString());if(!context.mounted)return;final sonuc=await showDialog<String>(context:context,builder:(x)=>AlertDialog(backgroundColor:Colors.white,title:const Text('Takma ad'),content:TextField(controller:c,maxLength:30,decoration:const InputDecoration(hintText:'Bu sohbette görünecek ad')),actions:[TextButton(onPressed:()=>Navigator.pop(x),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(x,c.text.trim()),child:const Text('Kaydet'))]));c.dispose();if(sonuc!=null)await FirebaseFirestore.instance.collection('chats').doc(chatId).update({'nicknames.$me':sonuc});}
  Future<void> ozellestir(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
    final secim=await showModalBottomSheet<Object>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,isScrollControlled:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const ListTile(title:Text('Sohbeti özelleştir',style:TextStyle(fontWeight:FontWeight.w900)),subtitle:Text('Bu görünüm yalnızca sende görünür.')),
        const ListTile(title:Text('Arka plan rengi',style:TextStyle(fontWeight:FontWeight.w700))),
        Wrap(spacing:16,runSpacing:16,children:[
          Colors.white,const Color(0xFFFFF4F7),const Color(0xFFF4F0FF),const Color(0xFFEFF8FF),const Color(0xFFF1FFF5)
        ].map((x)=>InkWell(onTap:()=>Navigator.pop(c,x.toARGB32()),child:CircleAvatar(radius:25,backgroundColor:x,child:const Icon(Icons.check,color:Colors.black26)))).toList()),
        const SizedBox(height:12),
        ListTile(leading:const Icon(Icons.photo_library_outlined,color:mor),title:const Text('Galeriden özel fotoğraf / logo seç'),onTap:()=>Navigator.pop(c,'gallery')),
        ListTile(leading:const Icon(Icons.camera_alt_outlined,color:mor),title:const Text('Kameradan arka plan çek'),onTap:()=>Navigator.pop(c,'camera')),
        ListTile(leading:const Icon(Icons.hide_image_outlined,color:Colors.red),title:const Text('Özel fotoğrafı kaldır',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'removeImage')),
        const Divider(height:28),
        const ListTile(leading:Icon(Icons.opacity_rounded,color:mor),title:Text('Arka plan görünürlüğü',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:Text('Fotoğrafın sohbetin arkasında ne kadar belirgin olacağını seç.')),
        Wrap(spacing:8,children:[
          ActionChip(label:const Text('Hafif'),onPressed:()=>Navigator.pop(c,'opacity:15')),
          ActionChip(label:const Text('Normal'),onPressed:()=>Navigator.pop(c,'opacity:30')),
          ActionChip(label:const Text('Belirgin'),onPressed:()=>Navigator.pop(c,'opacity:50')),
          ActionChip(label:const Text('Güçlü'),onPressed:()=>Navigator.pop(c,'opacity:70')),
        ]),
        const Divider(height:28),
        const ListTile(leading:Icon(Icons.text_fields_rounded,color:mor),title:Text('Mesaj yazı boyutu',style:TextStyle(fontWeight:FontWeight.w800))),
        Wrap(spacing:8,children:[
          ActionChip(label:const Text('Küçük'),onPressed:()=>Navigator.pop(c,'font:14')),
          ActionChip(label:const Text('Normal'),onPressed:()=>Navigator.pop(c,'font:16')),
          ActionChip(label:const Text('Büyük'),onPressed:()=>Navigator.pop(c,'font:18')),
        ]),
        const Divider(height:28),
        const ListTile(leading:Icon(Icons.emoji_emotions_outlined,color:mor),title:Text('Hızlı gönderme emojisi',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:Text('Mesaj kutusu boşken sağdaki tek dokunuş emojisini seç.')),
        Padding(padding:const EdgeInsets.fromLTRB(16,0,16,8),child:Wrap(spacing:12,runSpacing:12,children:
          ['👍','❤️','😂','😍','🔥','👏','🙏','🎉','😮','😢','😡','💯'].map((e)=>InkWell(
            onTap:()=>Navigator.pop(c,'quickEmoji:'+e),
            borderRadius:BorderRadius.circular(28),
            child:Container(width:48,height:48,alignment:Alignment.center,decoration:BoxDecoration(color:const Color(0xFFF4F4F6),borderRadius:BorderRadius.circular(24)),child:Text(e,style:const TextStyle(fontSize:25))),
          )).toList(),
        )),
        const Divider(height:24),
        ListTile(leading:const Icon(Icons.restart_alt_rounded,color:Colors.red),title:const Text('Özelleştirmeyi sıfırla',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),subtitle:const Text('Arka plan, yazı boyutu ve hızlı emojiyi varsayılana döndür.'),onTap:()=>Navigator.pop(c,'reset')),
        const SizedBox(height:10),
      ])))),
    );
    if(secim==null)return;
    final ref=FirebaseFirestore.instance.collection('chats').doc(chatId);

    if(secim is String&&secim.startsWith('quickEmoji:')){
      final emoji=secim.substring('quickEmoji:'.length);
      await ref.set({'quickEmoji_$me':emoji},SetOptions(merge:true));
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Hızlı emoji '+emoji+' olarak ayarlandı.')));
      return;
    }
    if(secim is String&&secim.startsWith('opacity:')){
      final oran=(double.tryParse(secim.substring(8))??30)/100;
      await ref.set({'backgroundOpacity_$me':oran},SetOptions(merge:true));
      return;
    }
    if(secim is String&&secim.startsWith('font:')){
      final boyut=double.tryParse(secim.substring(5))??16;
      await ref.set({'messageFontSize_$me':boyut},SetOptions(merge:true));
      return;
    }
    if(secim=='reset'){
      await ref.set({
        'theme_$me':Colors.white.toARGB32(),
        'backgroundUrl_$me':'',
        'backgroundOpacity_$me':.30,
        'messageFontSize_$me':16.0,
        'quickEmoji_$me':'👍',
      },SetOptions(merge:true));
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sohbet özelleştirmeleri sıfırlandı.')));
      return;
    }
    if(secim is int){
      await ref.set({'theme_$me':secim},SetOptions(merge:true));
      return;
    }
    if(secim=='removeImage'){
      if(!context.mounted)return;
      final onay=await showDialog<bool>(context:context,builder:(d)=>Theme(
        data:ThemeData.light().copyWith(dialogTheme:const DialogThemeData(backgroundColor:Colors.white)),
        child:AlertDialog(
          backgroundColor:Colors.white,surfaceTintColor:Colors.white,
          title:const Text('Özel fotoğraf kaldırılsın mı?',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          content:const Text('Sohbet arka planındaki özel fotoğraf kaldırılacak. İstersen daha sonra yeniden seçebilirsin.',style:TextStyle(color:Colors.black87,height:1.35)),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(d,false),child:const Text('Vazgeç',style:TextStyle(color:mor))),
            FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(d,true),child:const Text('Kaldır')),
          ],
        ),
      ))??false;
      if(!onay)return;
      await ref.set({'backgroundUrl_$me':''},SetOptions(merge:true));
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Özel sohbet arka planı kaldırıldı.')));
      return;
    }

    final kaynak=secim=='camera'?ImageSource.camera:ImageSource.gallery;
    final x=await ImagePicker().pickImage(source:kaynak,imageQuality:76,maxWidth:1280);if(x==null)return;
    try{
      final yol='chat-backgrounds/'+me+'/'+chatId+'_'+DateTime.now().millisecondsSinceEpoch.toString()+'.jpg';
      final url=await ngelxMedyaYukleBytes(
        bytes: await x.readAsBytes(),
        kind: 'chat-backgrounds',
        ext: 'jpg',
        legacyPath: yol,
      );
      await ref.set({'backgroundUrl_$me':url},SetOptions(merge:true));
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Özel sohbet arka planın kaydedildi.')));
    }catch(e){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Arka plan yüklenemedi: '+e.toString())));
    }
  }
  Future<void> sureliMesajlar(BuildContext context,int mevcut)async{
    final secim=await showModalBottomSheet<int>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const ListTile(
          leading:Icon(Icons.timer_outlined,color:mor),
          title:Text('Süreli mesajlar',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
          subtitle:Text('Yeni mesajlar seçilen sürenin sonunda sohbet görünümünden kaybolur.',style:TextStyle(color:Colors.black54)),
        ),
        for(final e in const [('Kapalı',0),('24 saat',86400),('7 gün',604800),('30 gün',2592000)])
          ListTile(
            leading:Icon(mevcut==e.$2?Icons.radio_button_checked:Icons.radio_button_off,color:mevcut==e.$2?mor:Colors.black38),
            title:Text(e.$1),
            onTap:()=>Navigator.pop(c,e.$2),
          ),
      ]))),
    );
    if(secim==null)return;
    await FirebaseFirestore.instance.collection('chats').doc(chatId).set({'disappearingSeconds':secim},SetOptions(merge:true));
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(secim==0?'Süreli mesajlar kapatıldı.':'Süreli mesajlar ayarlandı.')));
  }

  Future<void> sessizeAl(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
    final ref=FirebaseFirestore.instance.collection('users').doc(me),d=await ref.get(),v=d.data()??<String,dynamic>{},sessiz=List<String>.from(v['mutedChats']??const[]).contains(chatId);
    if(!context.mounted)return;
    final secim=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
      const ListTile(leading:Icon(Icons.notifications_off_outlined,color:mor),title:Text('Sohbet bildirimlerini sessize al',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),subtitle:Text('Mesajlar gelmeye devam eder; yalnızca bu sohbetin bildirimi kapanır.',style:TextStyle(color:Colors.black54))),
      if(sessiz)ListTile(leading:const Icon(Icons.notifications_active_outlined,color:Colors.green),title:const Text('Sessizi kaldır'),onTap:()=>Navigator.pop(c,'unmute')),
      if(!sessiz)...[
        for(final e in const [('1 saat','1h'),('8 saat','8h'),('1 hafta','7d'),('Süresiz','forever')])ListTile(title:Text(e.$1),onTap:()=>Navigator.pop(c,e.$2)),
      ],
      TextButton(onPressed:()=>Navigator.pop(c),child:const Text('Vazgeç')),
    ]))));
    if(secim==null)return;
    if(secim=='unmute'){
      await ref.set({'mutedChats':FieldValue.arrayRemove([chatId]),'mutedChatUntil':{chatId:FieldValue.delete()}},SetOptions(merge:true));
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sohbet bildirimlerinin sesi açıldı.')));
      return;
    }
    final g=<String,dynamic>{'mutedChats':FieldValue.arrayUnion([chatId])};
    if(secim=='forever')g['mutedChatUntil.$chatId']=FieldValue.delete();
    else{
      final sure=secim=='1h'?const Duration(hours:1):secim=='8h'?const Duration(hours:8):const Duration(days:7);
      g['mutedChatUntil.$chatId']=DateTime.now().add(sure).toUtc().toIso8601String();
    }
    await ref.set(g,SetOptions(merge:true));
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(secim=='forever'?'Sohbet süresiz sessize alındı.':'Sohbet seçilen süre boyunca sessize alındı.')));
  }
  Future<void> kisitla(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
    final ref=FirebaseFirestore.instance.collection('users').doc(me),d=await ref.get(),v=d.data()??<String,dynamic>{},kisitli=List<String>.from(v['restrictedUsers']??const[]).contains(uid);
    if(!context.mounted)return;
    final onay=await showDialog<bool>(context:context,builder:(c)=>Theme(
      data:ThemeData.light().copyWith(dialogTheme:const DialogThemeData(backgroundColor:Colors.white)),
      child:AlertDialog(
        backgroundColor:Colors.white,
        surfaceTintColor:Colors.white,
        title:Text(kisitli?'Kısıtlamayı kaldır':'$ad kısıtlansın mı?',style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
        content:Text(kisitli?'Bu kişinin bildirimleri tekrar normal şekilde gelebilir.':'Bu kişiden gelen etkileşim ve mesaj bildirimleri sessizce kısıtlanır. Engelleme değildir; sohbet tamamen kapanmaz.',style:const TextStyle(color:Colors.black87,height:1.35)),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç',style:TextStyle(color:mor))),
          FilledButton(onPressed:()=>Navigator.pop(c,true),child:Text(kisitli?'Kısıtlamayı kaldır':'Kısıtla',style:const TextStyle(color:Colors.white))),
        ],
      ),
    ))??false;
    if(!onay)return;
    await ref.set({'restrictedUsers':kisitli?FieldValue.arrayRemove([uid]):FieldValue.arrayUnion([uid])},SetOptions(merge:true));
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(kisitli?'Kısıtlama kaldırıldı.':'Kullanıcı kısıtlandı. Bildirimleri sessizce filtrelenecek.')));
  }
  Future<void> engelle(BuildContext context)async{
    final ok=await showDialog<bool>(context:context,builder:(c)=>Theme(
      data:ThemeData.light().copyWith(dialogTheme:const DialogThemeData(backgroundColor:Colors.white)),
      child:AlertDialog(
        backgroundColor:Colors.white,
        surfaceTintColor:Colors.white,
        title:Text('$ad engellensin mi?',style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
        content:const Text('Bu kullanıcı sana mesaj gönderemez ve profilini göremez.',style:TextStyle(color:Colors.black87,height:1.35)),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç',style:TextStyle(color:mor))),
          FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(c,true),child:const Text('Engelle')),
        ],
      ),
    ))??false;
    if(ok&&context.mounted)await kullaniciyiEngelle(context,uid);
  }
  Future<void> sohbetiSil(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>Theme(
      data:ThemeData.light().copyWith(dialogTheme:const DialogThemeData(backgroundColor:Colors.white)),
      child:AlertDialog(
        backgroundColor:Colors.white,
        surfaceTintColor:Colors.white,
        title:const Text('Sohbet silinsin mi?',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
        content:const Text('Bu sohbet yalnızca senin sohbet listenden kaldırılacak. Karşı tarafın sohbeti silinmeyecek.',style:TextStyle(color:Colors.black87,height:1.35)),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç',style:TextStyle(color:mor))),
          FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(c,true),child:const Text('Sohbeti sil')),
        ],
      ),
    ))??false;
    if(!ok)return;
    await FirebaseFirestore.instance.collection('chats').doc(chatId).set({'hiddenFor':FieldValue.arrayUnion([me])},SetOptions(merge:true));
    if(context.mounted)Navigator.popUntil(context,(r)=>r.isFirst);
  }

  Future<void> arkadasEkle(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null||me==uid)return;
    final benim=await FirebaseFirestore.instance.collection('users').doc(me).get();
    final arkadaslar=List<String>.from(benim.data()?['friends']??const[]);
    if(arkadaslar.contains(uid)){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Zaten arkadaşsınız.')));return;}
    final istekId='friend_request_${me}_$uid',istek=FirebaseFirestore.instance.collection('notifications').doc(istekId),onceki=await istek.get();
    if(onceki.data()?['status']=='pending'){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arkadaşlık isteğin zaten bekliyor.')));return;}
    await istek.set({'toUid':uid,'fromUid':me,'type':'friend_request','text':'Yeni arkadaşlık isteğin var','status':'pending','read':false,'createdAt':FieldValue.serverTimestamp()});
    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arkadaşlık isteği gönderildi.')));
  }
  Future<void> kisiyiPaylas()async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    final hedef=await FirebaseFirestore.instance.collection('users').doc(uid).get(),hv=hedef.data()??<String,dynamic>{};
    if(hv['profileShareFriendsOnly']==true&&me!=uid){
      final benim=me==null?null:await FirebaseFirestore.instance.collection('users').doc(me).get();
      if(!List<String>.from(benim?.data()?['friends']??const[]).contains(uid))return;
    }
    final link='$ngelxWebAdresi/u/$uid';
    await SharePlus.instance.share(ShareParams(title:'NgelX profili',subject:'NgelX • $ad',text:'NgelX’te $ad profilini görüntüle\n$link'));
  }

  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light().copyWith(
      scaffoldBackgroundColor:Colors.white,
      appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0,surfaceTintColor:Colors.white),
      dividerColor:const Color(0xFFECEDEF),
    ),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(
        leading:const BackButton(),
        title:const SizedBox.shrink(),
        actions:[PopupMenuButton<String>(
          icon:const Icon(Icons.more_vert_rounded),
          onSelected:(v){if(v=='share')kisiyiPaylas();if(v=='report')sikayetEt(context,hedefTuru:'kullanici',hedefId:uid,hedefUid:uid);},
          itemBuilder:(_)=>const [
            PopupMenuItem(value:'share',child:Row(children:[Icon(Icons.share_outlined),SizedBox(width:10),Text('Kişiyi paylaş')])),
            PopupMenuItem(value:'report',child:Row(children:[Icon(Icons.flag_outlined),SizedBox(width:10),Text('Şikâyet et')])),
          ],
        )],
      ),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('chats').doc(chatId).snapshots(),
        builder:(_,s){
          final me=FirebaseAuth.instance.currentUser?.uid,ham=s.data?.data()?['nicknames'],nicks=ham is Map?Map<String,dynamic>.from(ham):<String,dynamic>{},takma=(me==null?'':(nicks[me]??'').toString()).trim(),gorunenAd=takma.isNotEmpty?takma:ad;
          return ListView(
            padding:const EdgeInsets.fromLTRB(20,8,20,28),
            children:[
              Center(child:CircleAvatar(radius:58,backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,size:48):null)),
              const SizedBox(height:16),
              Text(gorunenAd,textAlign:TextAlign.center,style:const TextStyle(fontSize:29,fontWeight:FontWeight.w900,color:Colors.black)),
              const SizedBox(height:24),
              FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                future:me==null?null:FirebaseFirestore.instance.collection('users').doc(me).get(),
                builder:(_,u){
                  final arkadas=me!=null&&List<String>.from(u.data?.data()?['friends']??const[]).contains(uid);
                  return Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
                    _kisa(arkadas?Icons.people_alt_rounded:Icons.person_add_alt_1_rounded,arkadas?'Arkadaş':'Arkadaş ekle',arkadas?(){}:()=>arkadasEkle(context)),
                    _kisa(Icons.person_rounded,'Profil',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uid)))),
                    _kisa(Icons.text_fields_rounded,'Takma ad',()=>takmaAd(context)),
                    _kisa(Icons.search_rounded,'Arama',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:chatId)))),
                    _kisa(Icons.palette_rounded,'Özelleştir',()=>ozellestir(context)),
                  ]);
                },
              ),
              const SizedBox(height:30),
              _bolum('Sohbet bilgisi'),
              _satir(Icons.photo_library_outlined,'Medya, dosya ve bağlantılar',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupMedyaPage(chatId:chatId)))),
              _satir(Icons.push_pin_outlined,'Sabitlenmiş mesajlar',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:chatId)))),
              _satir(
                Icons.timer_outlined,
                'Süreli mesajlar',
                ()=>sureliMesajlar(context,(s.data?.data()?['disappearingSeconds'] is num?(s.data!.data()!['disappearingSeconds'] as num).toInt():0)),
                alt:(s.data?.data()?['disappearingSeconds']??0)==0?'Kapalı':'Yeni mesajlar otomatik kaybolur',
              ),
              if(me!=null)SwitchListTile(
                contentPadding:const EdgeInsets.symmetric(horizontal:8),
                secondary:const Icon(Icons.done_all_rounded,color:Colors.black),
                title:const Text('Okundu bilgisi',style:TextStyle(color:Colors.black87,fontSize:17)),
                subtitle:const Text('Mesajları okuduğunda karşı tarafa Görüldü bilgisi gösterilir.',style:TextStyle(color:Colors.black45,fontSize:13)),
                value:s.data?.data()?['readReceipts_$me']!=false,
                onChanged:(x)=>FirebaseFirestore.instance.collection('chats').doc(chatId).set({'readReceipts_$me':x},SetOptions(merge:true)),
              ),
              if(me!=null)SwitchListTile(
                contentPadding:const EdgeInsets.symmetric(horizontal:8),
                secondary:const Icon(Icons.more_horiz_rounded,color:Colors.black),
                title:const Text('Yazma göstergesi',style:TextStyle(color:Colors.black87,fontSize:17)),
                subtitle:const Text('Mesaj yazarken karşı taraf “yazıyor” bilgisini görebilir.',style:TextStyle(color:Colors.black45,fontSize:13)),
                value:s.data?.data()?['typingIndicator_$me']!=false,
                onChanged:(x)=>FirebaseFirestore.instance.collection('chats').doc(chatId).set({'typingIndicator_$me':x,if(!x)'typing_$me':false},SetOptions(merge:true)),
              ),
              const SizedBox(height:18),
              _bolum('İşlemler'),
              _satir(Icons.notifications_off_outlined,'Sessize al',()=>sessizeAl(context),alt:'Bu sohbetin bildirimlerini yönet'),
              _satir(Icons.notifications_outlined,'Bildirimler ve sesler',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Bildirimler'))),alt:'Mesaj bildirim ayarları'),
              _satir(Icons.share_outlined,'Kişiyi paylaş',kisiyiPaylas),
              const SizedBox(height:18),
              _bolum('Gizlilik ve destek'),
              _satir(Icons.shield_outlined,'Mesaj izinleri',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Mesaj izinleri')))),
              _satir(Icons.do_not_disturb_alt_rounded,'Kısıtla',()=>kisitla(context)),
              _satir(Icons.block_rounded,'Engelle',()=>engelle(context),renk:Colors.black),
              _satir(Icons.delete_outline_rounded,'Sohbeti sil',()=>sohbetiSil(context),alt:'Yalnızca senin sohbet listenden kaldırır',renk:Colors.red),
            ],
          );
        },
      ),
    ),
  );
  Widget _bolum(String t)=>Padding(padding:const EdgeInsets.fromLTRB(8,4,8,8),child:Text(t,style:const TextStyle(color:Colors.black54,fontSize:16,fontWeight:FontWeight.w800)));
  Widget _kisa(IconData i,String t,VoidCallback f)=>Expanded(child:InkWell(borderRadius:BorderRadius.circular(18),onTap:f,child:Padding(padding:const EdgeInsets.symmetric(horizontal:2,vertical:4),child:Column(children:[CircleAvatar(radius:25,backgroundColor:const Color(0xFFF0F1F3),child:Icon(i,color:Colors.black,size:25)),const SizedBox(height:7),Text(t,maxLines:2,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontSize:12.5,height:1.1))]))));
  Widget _satir(IconData i,String t,VoidCallback f,{String? alt,Color? renk})=>ListTile(
    onTap:f,
    contentPadding:const EdgeInsets.symmetric(horizontal:8,vertical:6),
    leading:Icon(i,color:renk??Colors.black,size:29),
    title:Text(t,style:TextStyle(color:renk??Colors.black87,fontSize:17,fontWeight:FontWeight.w500)),
    subtitle:alt==null?null:Text(alt,style:const TextStyle(color:Colors.black45,fontSize:13)),
    trailing:const Icon(Icons.chevron_right_rounded,color:Colors.black38),
  );
}

class SohbetMesajAramaPage extends StatefulWidget{
  final String chatId;const SohbetMesajAramaPage({super.key,required this.chatId});
  @override State<SohbetMesajAramaPage> createState()=>_SohbetMesajAramaPageState();
}
class _SohbetMesajAramaPageState extends State<SohbetMesajAramaPage>{
  String sorgu='';
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Sohbette ara')),body:Column(children:[Padding(padding:const EdgeInsets.all(12),child:TextField(autofocus:true,onChanged:(v)=>setState(()=>sorgu=v.trim().toLowerCase()),decoration:const InputDecoration(prefixIcon:Icon(Icons.search),hintText:'Mesaj yazısı ara'))),Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('chats').doc(widget.chatId).collection('messages').orderBy('createdAt',descending:true).snapshots(),builder:(_,s){final docs=(s.data?.docs??[]).where((d)=>(d.data()['text']??'').toString().toLowerCase().contains(sorgu)&&sorgu.isNotEmpty).toList();if(sorgu.isEmpty)return const Center(child:Text('Aramak istediğin kelimeyi yaz.',style:TextStyle(color:Colors.black54)));if(docs.isEmpty)return const Center(child:Text('Eşleşen mesaj bulunamadı.',style:TextStyle(color:Colors.black54)));return ListView.separated(padding:const EdgeInsets.all(12),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),itemBuilder:(_,i)=>ListTile(leading:const Icon(Icons.chat_bubble_outline,color:Colors.blue),title:Text((docs[i].data()['text']??'').toString()),subtitle:Text(mesajSaati(docs[i].data()['createdAt']))));}))])));
}

class AktivitePage extends StatelessWidget {
  const AktivitePage({super.key});

  IconData _ikon(String tur){switch(tur){case 'like':case 'interaction':return Icons.favorite_rounded;case 'comment':return Icons.mode_comment_rounded;case 'message':return Icons.chat_bubble_rounded;case 'security':return Icons.shield_rounded;case 'friend':case 'follow_request':case 'friend_request':return Icons.person_add_alt_1_rounded;case 'friend_accepted':return Icons.people_rounded;case 'follow_accepted':return Icons.person_rounded;default:return Icons.notifications_rounded;}}
  Color _renk(String tur){switch(tur){case 'like':case 'interaction':return const Color(0xFFFF3B73);case 'comment':return Colors.blue;case 'security':return Colors.orange;case 'friend':case 'follow_request':case 'friend_request':return mor;default:return const Color(0xFF20B86A);}}

  Widget _bildirimBasligi(Map<String,dynamic> v,bool okundu){
    final tam=(v['text']??v['message']??v['content']??'Yeni bildirim').toString();
    String ad=(v['senderName']??v['fromName']??'').toString().trim(),eylem=tam;
    if(ad.isEmpty){
      const anahtarlar=[' Gönderine',' Gönderini',' Yorumunu',' Sana bir',' Yeni bir',' Arkadaşlık'];
      for(final a in anahtarlar){final i=tam.indexOf(a);if(i>0){ad=tam.substring(0,i);eylem=tam.substring(i).trimLeft();break;}}
    }else if(tam.toLowerCase().startsWith(ad.toLowerCase())){eylem=tam.substring(ad.length).trimLeft();}
    if(ad.isEmpty)return Text(tam,style:TextStyle(color:Colors.black87,fontWeight:okundu?FontWeight.w500:FontWeight.w700));
    return Text.rich(TextSpan(children:[TextSpan(text:'$ad ',style:const TextStyle(fontWeight:FontWeight.w900)),TextSpan(text:eylem,style:TextStyle(fontWeight:okundu?FontWeight.w400:FontWeight.w600))]),style:const TextStyle(color:Colors.black87));
  }

  Future<void> _aktiviteAc(BuildContext context, QueryDocumentSnapshot<Map<String,dynamic>> d)async{
    final v=d.data();await d.reference.set({'read':true},SetOptions(merge:true));if(!context.mounted)return;
    final from=(v['fromUid']??v['senderId']??v['senderUid']??v['userId']??'').toString(),tur=(v['type']??'').toString();
    final kaynak=(v['sourceId']??v['chatId']??v['belgeId']??v['postId']??v['contentId']??'').toString();
    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:kaynak)));return;}
    if(from.isNotEmpty&&(tur=='friend'||tur=='follow_request'||tur=='friend_request'||tur=='friend_accepted'||tur=='follow_accepted')){Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:from)));return;}
    if(tur=='call'&&kaynak.isNotEmpty){final ref=FirebaseFirestore.instance.collection('calls').doc(kaynak),arama=await ref.get(),a=arama.data();if(!context.mounted)return;if(a==null||a['status']=='ended'){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu arama sona ermiş.')));return;}final p=await FirebaseFirestore.instance.collection('users').doc(from).get();if(!context.mounted)return;final baslik=a['group']==true?(a['title']??'Grup araması').toString():(p.data()?['displayName']??p.data()?['username']??'NgelX araması').toString();final foto=a['group']==true?'':(p.data()?['photoUrl']??'').toString();Navigator.push(context,MaterialPageRoute(builder:(_)=>NgelXAramaPage(roomName:(a['roomName']??'').toString(),baslik:baslik,foto:foto,goruntulu:a['video']==true,aramaRef:ref)));return;}
    if(tur=='message'&&from.isNotEmpty){final p=await FirebaseFirestore.instance.collection('users').doc(from).get();if(!context.mounted)return;final ids=[FirebaseAuth.instance.currentUser!.uid,from]..sort();Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:(v['sourceId']??v['chatId']??v['belgeId']??ids.join('_')).toString(),digerUid:from,ad:(p.data()?['displayName']??p.data()?['username']??'Kullanıcı').toString(),foto:(p.data()?['photoUrl']??'').toString())));}
  }

  Future<void> istegiSonuclandir(BuildContext context, QueryDocumentSnapshot<Map<String, dynamic>> belge, bool kabul) async {
    final ben=FirebaseAuth.instance.currentUser?.uid;
    final veri=belge.data();
    final gonderen=(veri['fromUid']??'').toString();
    final tur=(veri['type']??'').toString();
    final eskiArkadaslik=belge.id.startsWith('friend_request_')||(veri['text']??'').toString().toLowerCase().contains('arkadaşlık');
    final arkadaslikIstegi=tur=='friend_request'||eskiArkadaslik;
    final takipIstegi=tur=='follow_request'&&!arkadaslikIstegi;
    if(ben==null||gonderen.isEmpty||veri['status']!='pending')return;

    final toplu=FirebaseFirestore.instance.batch();
    toplu.update(belge.reference,{
      'status':kabul?'accepted':'rejected',
      'read':true,
      'answeredAt':FieldValue.serverTimestamp(),
    });

    if(kabul&&takipIstegi){
      toplu.set(
        FirebaseFirestore.instance.collection('users').doc(ben),
        {'followers':FieldValue.arrayUnion([gonderen])},
        SetOptions(merge:true),
      );
      toplu.set(
        FirebaseFirestore.instance.collection('users').doc(gonderen),
        {'following':FieldValue.arrayUnion([ben])},
        SetOptions(merge:true),
      );
      toplu.set(
        FirebaseFirestore.instance.collection('notifications').doc('follow_accepted_'+ben+'_'+gonderen),
        {
          'toUid':gonderen,'fromUid':ben,'type':'follow_accepted',
          'text':'Takip isteğin kabul edildi','read':false,
          'createdAt':FieldValue.serverTimestamp(),
        },
        SetOptions(merge:true),
      );
    }

    if(kabul&&arkadaslikIstegi){
      toplu.set(
        FirebaseFirestore.instance.collection('users').doc(ben),
        {'friends':FieldValue.arrayUnion([gonderen])},
        SetOptions(merge:true),
      );
      toplu.set(
        FirebaseFirestore.instance.collection('users').doc(gonderen),
        {'friends':FieldValue.arrayUnion([ben])},
        SetOptions(merge:true),
      );
      final ids=[ben,gonderen]..sort();
      toplu.set(
        FirebaseFirestore.instance.collection('friendships').doc(ids.join('_')),
        {'members':ids,'since':FieldValue.serverTimestamp()},
        SetOptions(merge:true),
      );
      toplu.set(
        FirebaseFirestore.instance.collection('notifications').doc('friend_accepted_'+ben+'_'+gonderen),
        {
          'toUid':gonderen,'fromUid':ben,'type':'friend_accepted',
          'text':'Arkadaşlık isteğin kabul edildi','read':false,
          'createdAt':FieldValue.serverTimestamp(),
        },
        SetOptions(merge:true),
      );
    }

    await toplu.commit();
    if(context.mounted){
      final ad=takipIstegi?'Takip isteği':'Arkadaşlık isteği';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(kabul?'$ad kabul edildi.':'$ad reddedildi.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),dividerColor:const Color(0xFFE8E9ED)),child:Scaffold(
      backgroundColor:Colors.white,
      appBar: AppBar(title: const Text('Aktivite',style:TextStyle(fontWeight:FontWeight.w900)),actions:[IconButton(tooltip:'Tümünü okundu yap',onPressed:()async{if(uid==null)return;final q=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:uid).get();final b=FirebaseFirestore.instance.batch();for(final d in q.docs){b.set(d.reference,{'read':true},SetOptions(merge:true));}await b.commit();},icon:const Icon(Icons.done_all_rounded,color:Color(0xFF20B86A)))]),
      body: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
        stream: uid == null ? null : FirebaseFirestore.instance.collection('notifications').where('toUid', isEqualTo: uid).limit(100).snapshots(),
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
            final bekliyor = (v['type'] == 'follow_request' || v['type'] == 'friend_request') && v['status'] == 'pending';
            return Container(decoration:BoxDecoration(color:okundu?Colors.white:const Color(0xFFF8F4FF),borderRadius:BorderRadius.circular(17)),child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
              leading: Stack(children:[CircleAvatar(radius:26,backgroundColor:_renk(tur).withOpacity(.13),backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?Icon(_ikon(tur),color:_renk(tur)):null),if(!okundu)const Positioned(right:0,top:0,child:CircleAvatar(radius:5,backgroundColor:Color(0xFF7C3AED)))]),
              title: _bildirimBasligi(v,okundu),
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
String mesajSaati(dynamic t){if(t is! Timestamp)return '';final d=t.toDate().toLocal();final s=d.minute.toString().padLeft(2,'0');return '${d.hour}:$s';}

Future<void> profilZiyaretKaydet(String hedefUid)async{
  final me=FirebaseAuth.instance.currentUser?.uid;
  if(me==null||me==hedefUid)return;
  try{
    final simdi=DateTime.now().toLocal();
    final gun=simdi.year.toString().padLeft(4,'0')+simdi.month.toString().padLeft(2,'0')+simdi.day.toString().padLeft(2,'0');
    final hafiza=await SharedPreferences.getInstance();
    final anahtar='profile_view_'+hedefUid+'_'+gun;
    if(hafiza.getBool(anahtar)==true)return;
    await FirebaseFirestore.instance.collection('profile_view_stats').doc(hedefUid).collection('days').doc(gun).set({
      'count':FieldValue.increment(1),
      'day':gun,
      'updatedAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
    await hafiza.setBool(anahtar,true);
  }catch(_){}
}

class ProfilZiyaretTrendPage extends StatelessWidget{
  const ProfilZiyaretTrendPage({super.key});
  @override Widget build(BuildContext context){
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light(),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Profil ziyaret eğilimleri',style:TextStyle(fontWeight:FontWeight.w900))),
      body:uid==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('profile_view_stats').doc(uid).collection('days').orderBy(FieldPath.documentId,descending:true).limit(30).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final docs=s.data?.docs??[];
          if(docs.isEmpty)return const Center(child:Text('Henüz profil ziyaret verisi yok.',style:TextStyle(color:Colors.black54)));
          final max=docs.fold<int>(1,(m,d){final n=((d.data()['count'] as num?)?.toInt()??0);return n>m?n:m;});
          return ListView.separated(
            padding:const EdgeInsets.all(18),itemCount:docs.length,separatorBuilder:(_,__)=>const SizedBox(height:10),
            itemBuilder:(_,i){
              final v=docs[i].data(),n=((v['count'] as num?)?.toInt()??0),gun=(v['day']??docs[i].id).toString();
              return Row(children:[
                SizedBox(width:82,child:Text(gun,style:const TextStyle(color:Colors.black54,fontSize:12))),
                Expanded(child:ClipRRect(borderRadius:BorderRadius.circular(8),child:LinearProgressIndicator(value:n/max,minHeight:14,backgroundColor:const Color(0xFFF0F1F4),color:mor))),
                const SizedBox(width:10),SizedBox(width:38,child:Text(n.toString(),textAlign:TextAlign.right,style:const TextStyle(fontWeight:FontWeight.w900))),
              ]);
            },
          );
        },
      ),
    ));
  }
}

class ProfilTanitimVideoKarti extends StatefulWidget{
  final String url;
  const ProfilTanitimVideoKarti({super.key,required this.url});
  @override State<ProfilTanitimVideoKarti> createState()=>_ProfilTanitimVideoKartiState();
}
class _ProfilTanitimVideoKartiState extends State<ProfilTanitimVideoKarti>{
  VideoPlayerController? c;
  bool hazir=false;
  @override void initState(){super.initState();_hazirla();}
  Future<void> _hazirla()async{
    if(widget.url.isEmpty)return;
    final x=VideoPlayerController.networkUrl(Uri.parse(widget.url));
    c=x;
    try{await x.initialize();if(mounted)setState(()=>hazir=true);}catch(_){}
  }
  @override void dispose(){c?.dispose();super.dispose();}
  @override Widget build(BuildContext context){
    final x=c;
    if(!hazir||x==null)return Container(height:180,decoration:BoxDecoration(color:const Color(0xFFF1F2F4),borderRadius:BorderRadius.circular(18)),child:const Center(child:CircularProgressIndicator(color:mor)));
    return ClipRRect(
      borderRadius:BorderRadius.circular(18),
      child:AspectRatio(
        aspectRatio:x.value.aspectRatio==0?16/9:x.value.aspectRatio,
        child:Stack(fit:StackFit.expand,children:[
          VideoPlayer(x),
          Center(child:IconButton.filledTonal(
            onPressed:(){setState((){x.value.isPlaying?x.pause():x.play();});},
            icon:Icon(x.value.isPlaying?Icons.pause_rounded:Icons.play_arrow_rounded,size:36),
          )),
        ]),
      ),
    );
  }
}

class OrtakGruplarPage extends StatelessWidget{
  final String digerUid;
  const OrtakGruplarPage({super.key,required this.digerUid});
  @override Widget build(BuildContext context){
    final me=FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light(),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Ortak gruplar',style:TextStyle(fontWeight:FontWeight.w900))),
      body:me==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('chats').where('members',arrayContains:me).limit(60).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final docs=(s.data?.docs??[]).where((d){
            final v=d.data(),uyeler=List<String>.from(v['members']??const[]);
            return v['isGroup']==true&&uyeler.contains(digerUid);
          }).toList();
          if(docs.isEmpty)return const Center(child:Text('Ortak grubunuz yok.',style:TextStyle(color:Colors.black54)));
          return ListView.separated(
            padding:const EdgeInsets.all(12),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),
            itemBuilder:(_,i){
              final d=docs[i],v=d.data(),foto=(v['groupPhotoUrl']??'').toString(),ad=(v['groupName']??'Grup').toString();
              return ListTile(
                leading:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups):null),
                title:Text(ad,style:const TextStyle(fontWeight:FontWeight.w800)),
                subtitle:Text(List<String>.from(v['members']??const[]).length.toString()+' üye'),
                trailing:const Icon(Icons.chevron_right),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupSohbetPage(chatId:d.id,ad:ad,foto:foto))),
              );
            },
          );
        },
      ),
    ));
  }
}

class KullaniciProfilPage extends StatelessWidget {
  final String uid;
  final bool ziyaretciOnizleme;
  const KullaniciProfilPage({super.key, required this.uid,this.ziyaretciOnizleme=false});

  Future<void> profiliPaylas(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    final hedef=await FirebaseFirestore.instance.collection('users').doc(uid).get();
    final hv=hedef.data()??<String,dynamic>{};
    if(hv['profileShareFriendsOnly']==true&&me!=uid){
      final benim=me==null?null:await FirebaseFirestore.instance.collection('users').doc(me).get();
      final arkadaslar=List<String>.from(benim?.data()?['friends']??const[]);
      if(!arkadaslar.contains(uid)){
        if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu kullanıcı profilinin yalnızca arkadaşları tarafından paylaşılmasına izin veriyor.')));
        return;
      }
    }
    final ad=(hv['displayName']??hv['username']??'NgelX kullanıcısı').toString();
    final link='$ngelxWebAdresi/u/$uid';
    await SharePlus.instance.share(ShareParams(title:'NgelX profili',subject:'NgelX • $ad',text:'NgelX’te $ad profilini görüntüle\n$link'));
  }

  @override
  Widget build(BuildContext context) {
    final me = FirebaseAuth.instance.currentUser?.uid;
    if(!ziyaretciOnizleme)unawaited(profilZiyaretKaydet(uid));
    final hedef = FirebaseFirestore.instance.collection('users').doc(uid).get();
    final benim = me == null ? Future.value(null) : FirebaseFirestore.instance.collection('users').doc(me).get();
    return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(
      backgroundColor:Colors.white,
      appBar: AppBar(
        title:Text(ziyaretciOnizleme?'Profil önizleme':'Profil',style:const TextStyle(fontWeight:FontWeight.w900)),
        actions:[IconButton(tooltip:'Profili paylaş',onPressed:()=>profiliPaylas(context),icon:const Icon(Icons.share_outlined))],
      ),
      body: FutureBuilder<List<DocumentSnapshot<Map<String, dynamic>>?>>(
        future: Future.wait([hedef, benim]),
        builder: (_, s) {
          if (!s.hasData) return const Center(child: CircularProgressIndicator(color: mavi));
          final v = s.data![0]?.data() ?? <String, dynamic>{};
          final benimVerim = s.data![1]?.data() ?? <String, dynamic>{};
          final foto = (v['photoUrl'] ?? '').toString();
          final arkadaslar = Set<String>.from(List<dynamic>.from(benimVerim['friends'] ?? []));
          final takip = Set<String>.from(List<dynamic>.from(benimVerim['following'] ?? []));
          final gizli = v['privateAccount'] == true;
          final profilIzni=(v['profileViewPermission']??'all').toString();
          final beniTakipEdiyor=me!=null&&List<String>.from(v['followers']??const[]).contains(me);
          final izinVar=profilIzni=='all'||(profilIzni=='followers'&&beniTakipEdiyor)||(profilIzni=='friends'&&arkadaslar.contains(uid));
          final erisimVar = ziyaretciOnizleme
              ? (profilIzni=='all'&&!gizli)
              : (me==uid||(izinVar&&(!gizli||beniTakipEdiyor||arkadaslar.contains(uid))));
          return ListView(
            padding: const EdgeInsets.all(22),
            children: [
              Center(child:GestureDetector(
                onTap:!erisimVar?null:()async{
                  try{
                    final q=await FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).limit(100).get();
                    final simdi=DateTime.now();
                    final hikayeler=q.docs.where((d){
                      final x=d.data(),bitis=x['expiresAt'];
                      return x['type']=='story'&&bitis is Timestamp&&bitis.toDate().isAfter(simdi);
                    }).toList()..sort((a,b){
                      final at=a.data()['createdAt'],bt=b.data()['createdAt'];
                      final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
                      return bm.compareTo(am);
                    });
                    if(!context.mounted)return;
                    if(hikayeler.isEmpty){
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Aktif hikâye yok.')));
                      return;
                    }
                    final d=hikayeler.first,x=d.data();
                    Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(
                      url:(x['mediaUrl']??'').toString(),
                      kullanici:'@'+(v['username']??'ngelx').toString(),
                      fotoUrl:foto,
                      ownerUid:uid,
                      storyId:d.id,
                      createdAt:x['createdAt'],
                      expiresAt:x['expiresAt'],
                    )));
                  }catch(_){
                    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye açılamadı.')));
                  }
                },
                child:Container(
                  padding:const EdgeInsets.all(3),
                  decoration:const BoxDecoration(shape:BoxShape.circle,gradient:LinearGradient(colors:[Color(0xFF22D3EE),Color(0xFF8B5CF6)])),
                  child:CircleAvatar(radius:55,backgroundColor:Colors.white,backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Text('N',style:TextStyle(fontSize:40)):null),
                ),
              )),
              const SizedBox(height: 12),
              Text((v['displayName'] ?? v['username'] ?? 'NgelX').toString(), textAlign: TextAlign.center, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
              Text('@' + (v['username'] ?? 'ngelx').toString(), textAlign: TextAlign.center, style: const TextStyle(color: Colors.black54)),
              const SizedBox(height: 16),
              Text((v['bio'] ?? '').toString(), textAlign: TextAlign.center),
              const SizedBox(height: 10),
              Wrap(alignment:WrapAlignment.center,spacing:12,runSpacing:6,children:[
                if((v['createdAt']??v['joinedAt']) is Timestamp)
                  Text('NgelX’e katıldı: '+((v['createdAt']??v['joinedAt']) as Timestamp).toDate().year.toString(),style:const TextStyle(color:Colors.black54,fontSize:12)),
                if(v['showActivityStatus']!=false)
                  Text(v['isOnline']==true?'● Çevrimiçi':(v['lastSeenAt'] is Timestamp?'Son görülme: '+zamanKisa(v['lastSeenAt']):'Çevrimdışı'),style:TextStyle(color:v['isOnline']==true?Colors.green:Colors.black54,fontSize:12,fontWeight:v['isOnline']==true?FontWeight.w700:FontWeight.w400)),
              ]),
              if((v['introVideoUrl']??'').toString().isNotEmpty) ...[
                const SizedBox(height:14),
                ProfilTanitimVideoKarti(url:(v['introVideoUrl']??'').toString()),
              ],
              const SizedBox(height: 14),
              FutureBuilder<QuerySnapshot<Map<String,dynamic>>>(
                future:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).get(),
                builder:(_,etk){
                  final paylasimlar=(etk.data?.docs??[]).where((d)=>d.data()['type']!='story');
                  final toplam=paylasimlar.fold<int>(0,(n,d){
                    final x=d.data();
                    return n+
                      ((x['likeCount'] as num?)?.toInt()??0)+
                      ((x['commentCount'] as num?)?.toInt()??0)+
                      ((x['shareCount'] as num?)?.toInt()??0);
                  });
                  return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                    _profilSayac(context,'${List<dynamic>.from(v['following']??const[]).length}','Takip',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:uid,alan:'following',baslik:'Takip')))),
                    _profilSayac(context,'${List<dynamic>.from(v['followers']??const[]).length}','Takipçi',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:uid,alan:'followers',baslik:'Takipçiler')))),
                    _profilSayac(context,'$toplam','Etkileşim',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>EtkilesimOzetiPage(uid:uid)))),
                    _profilSayac(context,'${List<dynamic>.from(v['friends']??const[]).length}','Arkadaşlar',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:uid,alan:'friends',baslik:'Arkadaşlar')))),
                  ]);
                },
              ),
              const SizedBox(height: 22),
              if (me != uid && !ziyaretciOnizleme) ...[
                Row(children:[
                  Expanded(child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                    stream:me==null?null:FirebaseFirestore.instance.collection('users').doc(me).snapshots(),
                    builder:(_,benSnap){
                      final takipte=List<String>.from(benSnap.data?.data()?['following']??const[]).contains(uid);
                      final istekRef=me==null?null:FirebaseFirestore.instance.collection('notifications').doc('follow_request_'+me+'_'+uid);
                      return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                        stream:istekRef?.snapshots(),
                        builder:(_,istekSnap){
                          final bekliyor=istekSnap.data?.data()?['status']=='pending';
                          final etiket=takipte?'Takiptesin':(gizli?(bekliyor?'İstek gönderildi':'Takip isteği gönder'):'Takip et');
                          return OutlinedButton.icon(
                            onPressed:(bekliyor&&!takipte)?null:()async{
                              if(me==null)return;
                              if(takipte){
                                final gorunenAd=(v['displayName']??v['username']??'Bu kişi').toString();
                                final onay=await showDialog<bool>(context:context,builder:(d)=>AlertDialog(
                                  backgroundColor:Colors.white,surfaceTintColor:Colors.white,
                                  title:const Text('Takipten çıkılsın mı?',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                                  content:Text('$gorunenAd artık takip ettiklerin arasında görünmeyecek.',style:const TextStyle(color:Colors.black87)),
                                  actions:[
                                    TextButton(onPressed:()=>Navigator.pop(d,false),child:const Text('Vazgeç')),
                                    FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(d,true),child:const Text('Takipten çık')),
                                  ],
                                ))??false;
                                if(!onay)return;
                                await takipDurumuDegistir(uid,true);
                                if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takipten çıktın.')));
                                return;
                              }

                              if(gizli){
                                await istekRef!.set({
                                  'toUid':uid,'fromUid':me,'type':'follow_request',
                                  'text':'Yeni takip isteğin var','status':'pending',
                                  'read':false,'createdAt':FieldValue.serverTimestamp(),
                                },SetOptions(merge:true));
                                if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takip isteği gönderildi.')));
                                return;
                              }

                              try{
                                await takipDurumuDegistir(uid,false);
                                if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Artık bu hesabı takip ediyorsun.')));
                              }catch(e){
                                if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Takip işlemi tamamlanamadı: $e')));
                              }
                            },
                            icon:Icon(takipte?Icons.person_remove_outlined:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1)),
                            label:Text(etiket),
                          );
                        },
                      );
                    },
                  )),
                  const SizedBox(width:10),
                  Expanded(child:OutlinedButton.icon(onPressed:()async{if(me==null)return;final ids=[me,uid]..sort();final id=ids.join('_');Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:id,digerUid:uid,ad:(v['displayName']??v['username']??'NgelX').toString(),foto:foto)));},icon:const Icon(Icons.message_outlined),label:const Text('Mesaj'))),
                ]),
                const SizedBox(height:10),
                StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  stream:me==null?null:FirebaseFirestore.instance.collection('notifications').doc('friend_request_'+me+'_'+uid).snapshots(),
                  builder:(_,istekSnap){
                    final bekliyor=istekSnap.data?.data()?['status']=='pending';
                    return SizedBox(width:double.infinity,child:FilledButton(
                      onPressed:(arkadaslar.contains(uid)||bekliyor)?null:()async{
                        if(me==null)return;
                        final ref=FirebaseFirestore.instance.collection('notifications').doc('friend_request_'+me+'_'+uid);
                        await ref.set({
                          'toUid':uid,'fromUid':me,'type':'friend_request',
                          'text':'Yeni arkadaşlık isteğin var','status':'pending',
                          'read':false,'createdAt':FieldValue.serverTimestamp(),
                        },SetOptions(merge:true));
                        if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arkadaşlık isteği gönderildi.')));
                      },
                      child:Text(arkadaslar.contains(uid)?'Arkadaşsınız':(bekliyor?'Arkadaşlık isteği gönderildi':'Arkadaşlık isteği gönder')),
                    ));
                  },
                ),
                const SizedBox(height:10),
                SizedBox(width:double.infinity,child:OutlinedButton.icon(
                  onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>OrtakGruplarPage(digerUid:uid))),
                  icon:const Icon(Icons.groups_2_outlined),
                  label:const Text('Ortak gruplar'),
                )),
                if(arkadaslar.contains(uid))FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  future:() { final ids=[me!,uid]..sort(); return FirebaseFirestore.instance.collection('friendships').doc(ids.join('_')).get(); }(),
                  builder:(_,fs){
                    final since=fs.data?.data()?['since'];
                    if(since is! Timestamp)return const SizedBox.shrink();
                    final gun=DateTime.now().difference(since.toDate()).inDays;
                    return Padding(
                      padding:const EdgeInsets.only(top:10),
                      child:Container(
                        width:double.infinity,padding:const EdgeInsets.all(12),
                        decoration:BoxDecoration(color:const Color(0xFFF7F4FF),borderRadius:BorderRadius.circular(14)),
                        child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                          const Icon(Icons.favorite_outline_rounded,color:mor,size:19),const SizedBox(width:7),
                          Text(gun<1?'Arkadaşlığınız bugün başladı':'$gun gündür arkadaşsınız',style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700)),
                        ]),
                      ),
                    );
                  },
                ),
              ],
              const SizedBox(height: 20),
              if (!erisimVar)
                Container(
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(color: const Color(0xFFF3F4F7), borderRadius: BorderRadius.circular(20)),
                  child: const Column(children: [
                    Icon(Icons.lock_outline, size: 48, color: mor),
                    SizedBox(height: 12),
                    Text('Bu profil sınırlı', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    SizedBox(height: 7),
                    Text('Bu kullanıcının profil görüntüleme veya gizlilik ayarları nedeniyle paylaşımlar görünmüyor.', textAlign: TextAlign.center, style: TextStyle(color: Colors.black54)),
                  ]),
                )
              else
                Column(children:[const Padding(padding:EdgeInsets.only(bottom:12),child:Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_ProfilSekme('Gönderiler',true),_ProfilSekme('Reels',false),_ProfilSekme('Etiketlenenler',false)])),StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
                  stream: FirebaseFirestore.instance.collection('videos').where('ownerId', isEqualTo: uid).limit(100).snapshots(),
                  builder: (_, p) {
                    final docs = (p.data?.docs ?? []).where((d){
                      final x=d.data();
                      if(x['type']=='story')return false;
                      if(me==uid)return true;
                      final hidden=List<String>.from(x['hiddenFor']??const[]);
                      if(me!=null&&hidden.contains(me))return false;
                      final privacy=(x['privacy']??'Herkes').toString();
                      if(privacy=='Yalnızca ben')return false;
                      if(privacy=='Arkadaşlar')return arkadaslar.contains(uid);
                      if(privacy=='Yakın arkadaşlar')return me!=null&&List<String>.from(x['visibleTo']??const[]).contains(me);
                      return true;
                    }).toList()
                      ..sort((a,b){
                        final ap=a.data()['pinned']==true,bp=b.data()['pinned']==true;
                        if(ap!=bp)return ap?-1:1;
                        final at=a.data()['createdAt'],bt=b.data()['createdAt'];
                        final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
                        return bm.compareTo(am);
                      });
                    return GridView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: docs.length,
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: .72, crossAxisSpacing: 6, mainAxisSpacing: 6),
                      itemBuilder: (_, i) {
                        final x = docs[i].data();
                        final tur = (x['type'] ?? 'video').toString();
                        final url = (x['mediaUrl'] ?? x['videoUrl'] ?? '').toString();
                        return GestureDetector(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:docs[i].id))),child:MedyaOnizleme(tur: tur, url: url, thumbnailUrl: (x['thumbnailUrl'] ?? '').toString(), yazi: (x['description'] ?? '').toString(), arkaPlan: const Color(0xFFF0F1F4)));
                      },
                    );
                  },
                )]),
            ],
          );
        },
      ),
    ));
  }

  Widget _profilSayac(BuildContext context,String sayi,String baslik,VoidCallback tiklama)=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(12),child:Padding(padding:const EdgeInsets.symmetric(horizontal:6,vertical:8),child:Column(children:[Text(sayi,style:const TextStyle(fontSize:20,fontWeight:FontWeight.w900)),Text(baslik,style:const TextStyle(color:Colors.black54,fontSize:12))])));
}

class MedyaOnizleme extends StatelessWidget {
  final String tur, url, yazi, thumbnailUrl;
  final Color arkaPlan;
  const MedyaOnizleme({
    super.key,
    required this.tur,
    required this.url,
    required this.yazi,
    required this.arkaPlan,
    this.thumbnailUrl = '',
  });

  @override
  Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(13),
    child: ColoredBox(
      color: arkaPlan,
      child: tur == 'photo' && url.isNotEmpty
          ? CachedNetworkImage(
              imageUrl: url,
              fit: BoxFit.cover,
              placeholder: (_, __) => const Center(child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black26)),
              errorWidget: (_, __, ___) => const Center(child: Icon(Icons.broken_image_outlined, color: Colors.black38)),
            )
          : tur == 'video'
              ? Stack(
                  fit: StackFit.expand,
                  children: [
                    if (thumbnailUrl.isNotEmpty)
                      CachedNetworkImage(
                        imageUrl: thumbnailUrl,
                        fit: BoxFit.cover,
                        placeholder: (_, __) => const ColoredBox(color: Color(0xFFE9ECF2)),
                        errorWidget: (_, __, ___) => const ColoredBox(color: Color(0xFFE9ECF2)),
                      )
                    else
                      const ColoredBox(
                        color: Color(0xFFE9ECF2),
                        child: Center(child: Icon(Icons.video_library_outlined, size: 42, color: Colors.black38)),
                      ),
                    const Center(
                      child: DecoratedBox(
                        decoration: BoxDecoration(color: Colors.black45, shape: BoxShape.circle),
                        child: Padding(
                          padding: EdgeInsets.all(8),
                          child: Icon(Icons.play_arrow_rounded, size: 34, color: Colors.white),
                        ),
                      ),
                    ),
                  ],
                )
              : Padding(
                  padding: const EdgeInsets.all(9),
                  child: Center(
                    child: Text(
                      yazi,
                      maxLines: 6,
                      overflow: TextOverflow.ellipsis,
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
    ),
  );
}

// V46: compatibility widget. It deliberately does not open the original MP4.
class VideoIlkKare extends StatelessWidget {
  final String url;
  const VideoIlkKare({super.key, required this.url});
  @override
  Widget build(BuildContext context) => const Stack(
    fit: StackFit.expand,
    children: [
      ColoredBox(color: Color(0xFFE9ECF2)),
      Center(child: Icon(Icons.play_arrow_rounded, size: 48, color: Colors.black45)),
    ],
  );
}

class HikayeGosterPage extends StatefulWidget {
  final String url,kullanici,fotoUrl,ownerUid,storyId;
  final dynamic createdAt,expiresAt;
  const HikayeGosterPage({
    super.key,
    required this.url,
    required this.kullanici,
    this.fotoUrl='',
    this.ownerUid='',
    this.storyId='',
    this.createdAt,
    this.expiresAt,
  });
  @override State<HikayeGosterPage> createState()=>_HikayeGosterPageState();
}
class _HikayeGosterPageState extends State<HikayeGosterPage> with SingleTickerProviderStateMixin {
  late final AnimationController sure;
  final cevap=TextEditingController();
  bool gonderiliyor=false,sessiz=false;

  @override void initState(){
    super.initState();
    sure=AnimationController(vsync:this,duration:const Duration(seconds:7))
      ..addStatusListener((s){if(s==AnimationStatus.completed&&mounted)Navigator.pop(context);})
      ..forward();
  }
  @override void dispose(){cevap.dispose();sure.dispose();super.dispose();}

  String get zamanBilgisi{
    final olusma=widget.createdAt is Timestamp?(widget.createdAt as Timestamp).toDate():null;
    final bitis=widget.expiresAt is Timestamp?(widget.expiresAt as Timestamp).toDate():null;
    String baslangic='Az önce';
    if(olusma!=null){
      final fark=DateTime.now().difference(olusma);
      if(fark.inMinutes<60)baslangic='${fark.inMinutes.clamp(1,59)} dk önce';
      else if(fark.inHours<24)baslangic='${fark.inHours} sa önce';
      else baslangic='${fark.inDays} gün önce';
    }
    if(bitis==null)return baslangic;
    final kalan=bitis.difference(DateTime.now());
    if(kalan.isNegative)return '$baslangic • Süresi doldu';
    if(kalan.inHours>=1)return '$baslangic • ${kalan.inHours} sa kaldı';
    return '$baslangic • ${kalan.inMinutes.clamp(1,59)} dk kaldı';
  }

  Future<void> _yanitGonder(String ham,{bool tepki=false})async{
    final ben=FirebaseAuth.instance.currentUser;
    final hedef=widget.ownerUid.trim();
    final metin=ham.trim();
    if(ben==null||metin.isEmpty||gonderiliyor)return;
    if(hedef.isEmpty){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye sahibine ulaşılamadı.')));
      return;
    }
    if(hedef==ben.uid){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu kendi hikâyen.')));
      return;
    }
    setState(()=>gonderiliyor=true);
    sure.stop();
    try{
      final ids=<String>[ben.uid,hedef]..sort();
      final chatId=ids.join('_');
      final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
      final mesajRef=chat.collection('messages').doc();
      final batch=FirebaseFirestore.instance.batch();
      batch.set(chat,{
        'members':ids,
        'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedef':FieldValue.increment(1),
      },SetOptions(merge:true));
      batch.set(mesajRef,{
        'senderId':ben.uid,
        'text':metin,
        'type':'story_reply',
        'storyId':widget.storyId,
        'storyUrl':widget.url,
        'storyOwnerId':hedef,
        'reaction':tepki,
        'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
      });
      if(widget.storyId.isNotEmpty){
        final story=FirebaseFirestore.instance.collection('videos').doc(widget.storyId);
        batch.set(story,{
          'replyCount':FieldValue.increment(1),
          if(tepki)'reactionCount':FieldValue.increment(1),
        },SetOptions(merge:true));
      }
      await batch.commit().timeout(const Duration(seconds:12));
      unawaited(uygulamaBildirimiGonder(
        toUid:hedef,fromUid:ben.uid,tur:'message',
        metin:tepki?'$metin hikâyene tepki verdi':'Hikâyene yanıt verdi',
        belgeId:chatId,
      ).catchError((_){ }));
      cevap.clear();
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(tepki?'Tepkin gönderildi.':'Yanıtın gönderildi.')));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hikâye yanıtı gönderilemedi. Tekrar dene.')));
    }finally{
      if(mounted){
        setState(()=>gonderiliyor=false);
        sure.forward();
      }
    }
  }

  @override Widget build(BuildContext context){
    final benim=FirebaseAuth.instance.currentUser?.uid==widget.ownerUid;
    return Scaffold(
      backgroundColor:Colors.black,
      body:GestureDetector(
        onLongPressStart:(_)=>sure.stop(),
        onLongPressEnd:(_)=>sure.forward(),
        child:Stack(fit:StackFit.expand,children:[
          CachedNetworkImage(
            imageUrl:widget.url,
            fit:BoxFit.contain,
            placeholder:(_,__)=>const Center(child:CircularProgressIndicator(color:Colors.white)),
            errorWidget:(_,__,___)=>const Center(child:Icon(Icons.broken_image_outlined,color:Colors.white54,size:60)),
          ),
          Positioned.fill(child:IgnorePointer(child:DecoratedBox(decoration:BoxDecoration(
            gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Colors.black54,Colors.transparent,Colors.black54],stops:[0,.35,1]),
          )))),
          SafeArea(child:Padding(
            padding:const EdgeInsets.fromLTRB(14,10,14,12),
            child:Column(children:[
              AnimatedBuilder(animation:sure,builder:(_,__)=>ClipRRect(borderRadius:BorderRadius.circular(8),child:LinearProgressIndicator(value:sure.value,minHeight:3,color:Colors.white,backgroundColor:Colors.white24))),
              const SizedBox(height:10),
              Row(children:[
                CircleAvatar(radius:20,backgroundColor:mor,backgroundImage:widget.fotoUrl.isEmpty?null:CachedNetworkImageProvider(widget.fotoUrl),child:widget.fotoUrl.isEmpty?Text(widget.kullanici.replaceFirst('@','').isEmpty?'N':widget.kullanici.replaceFirst('@','')[0].toUpperCase()):null),
                const SizedBox(width:9),
                Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  Text(widget.kullanici,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:16)),
                  Text(zamanBilgisi,style:const TextStyle(color:Colors.white70,fontSize:12)),
                ])),
                IconButton(tooltip:'Hikâye seçenekleri',onPressed:()=>showModalBottomSheet<void>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
                  ListTile(leading:const Icon(Icons.info_outline),title:Text(zamanBilgisi)),
                  ListTile(leading:const Icon(Icons.close),title:const Text('Kapat'),onTap:()=>Navigator.pop(c)),
                ]))),icon:const Icon(Icons.more_horiz,color:Colors.white,size:28)),
                IconButton(tooltip:sessiz?'Sesi aç':'Sesi kapat',onPressed:()=>setState(()=>sessiz=!sessiz),icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:29)),
                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close,color:Colors.white,size:32)),
              ]),
              const Spacer(),
              if(!benim&&widget.ownerUid.isNotEmpty) ...[
                Row(children:[
                  Expanded(child:TextField(
                    controller:cevap,
                    onTap:()=>sure.stop(),
                    onSubmitted:(v)=>_yanitGonder(v),
                    style:const TextStyle(color:Colors.white),
                    decoration:InputDecoration(
                      hintText:'Mesaj gönder',
                      hintStyle:const TextStyle(color:Colors.white70),
                      filled:true,fillColor:Colors.black45,
                      contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:12),
                      border:OutlineInputBorder(borderRadius:BorderRadius.circular(28),borderSide:BorderSide.none),
                      suffixIcon:gonderiliyor?const Padding(padding:EdgeInsets.all(13),child:SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white))):IconButton(onPressed:()=>_yanitGonder(cevap.text),icon:const Icon(Icons.send_rounded,color:Colors.white)),
                    ),
                  )),
                  const SizedBox(width:8),
                  for(final e in const ['❤️','😂','😮'])
                    InkWell(
                      onTap:gonderiliyor?null:()=>_yanitGonder(e,tepki:true),
                      borderRadius:BorderRadius.circular(28),
                      child:Padding(padding:const EdgeInsets.symmetric(horizontal:7,vertical:8),child:Text(e,style:const TextStyle(fontSize:29))),
                    ),
                ]),
              ] else
                Container(
                  padding:const EdgeInsets.symmetric(horizontal:14,vertical:9),
                  decoration:BoxDecoration(color:Colors.black45,borderRadius:BorderRadius.circular(18)),
                  child:const Text('Hikâyen',style:TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
                ),
            ]),
          )),
        ]),
      ),
    );
  }
}

class AyarlarPage extends StatelessWidget {
  const AyarlarPage({super.key});
  @override Widget build(BuildContext context){final misafir=FirebaseAuth.instance.currentUser?.isAnonymous==true;return Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),cardTheme:const CardThemeData(color:Colors.white,elevation:0,margin:EdgeInsets.symmetric(vertical:4)),dividerColor:Color(0xFFE5E7EB)),child:Scaffold(appBar:AppBar(title:const Text('Ayarlar ve gizlilik')),body:SafeArea(child:ListView(padding:const EdgeInsets.fromLTRB(14,8,14,24),children:[
    if(!misafir)...[
      _ayar(context,Icons.lock_outline,'Gizlilik','Paylaşımlarını ve hesabını kimler görebilir'),
      ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),leading:const Icon(Icons.people_outline,color:mor),title:const Text('Takip ve arkadaşlık',style:TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:const Text('İstekleri kabul et, reddet ve arkadaşlarını yönet',style:TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage()))),
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
    ListTile(leading:const Icon(Icons.system_update,color:mor),title:const Text('Uygulama güncellemeleri'),subtitle:const Text('V42 • Geliştiriliyor'),trailing:const Icon(Icons.build_circle,color:Colors.orange)),
    ListTile(leading:const Icon(Icons.share,color:mavi),title:const Text('Ngel X’i paylaş'),subtitle:const Text('Uygulama bağlantısını paylaş veya kopyala'),onTap:()async=>SharePlus.instance.share(ShareParams(text:'Ngel X ile dünyanı paylaş ✨\nhttps://ngelx.app'))),
    const Divider(),
    ListTile(leading:const Icon(Icons.logout,color:Colors.red),title:const Text('Çıkış yap',style:TextStyle(color:Colors.red)),onTap:()async{final onay=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Çıkış yapılsın mı?'),content:const Text('Tekrar giriş yapman gerekecek.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Çıkış yap'))]));if(onay==true){await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const GirisPage()),(_)=>false);}})
  ]))));}
  Widget _ayar(BuildContext c,IconData i,String t,String s)=>Card(child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:7),onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>TercihlerPage(baslik:t))),leading:Icon(i,color:mor),title:Text(t,style:const TextStyle(fontWeight:FontWeight.bold,color:Colors.black87)),subtitle:Text(s,style:const TextStyle(color:Colors.black54)),trailing:const Icon(Icons.chevron_right,color:Colors.black87)));
}

class HesapKurtarmaPage extends StatefulWidget{
  const HesapKurtarmaPage({super.key});
  @override State<HesapKurtarmaPage> createState()=>_HesapKurtarmaPageState();
}

class _HesapKurtarmaPageState extends State<HesapKurtarmaPage>{
  final email=TextEditingController(),telefon=TextEditingController();
  bool yukleniyor=true,kaydediliyor=false;

  @override void initState(){super.initState();_yukle();}
  @override void dispose(){email.dispose();telefon.dispose();super.dispose();}

  Future<void> _yukle()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null){if(mounted)setState(()=>yukleniyor=false);return;}
    final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();
    final v=d.data()??<String,dynamic>{};
    email.text=(v['recoveryEmail']??'').toString();
    telefon.text=(v['recoveryPhone']??v['phone']??'').toString();
    if(mounted)setState(()=>yukleniyor=false);
  }

  Future<String?> _sifreSor()async{
    final kontrol=TextEditingController();
    final x=await showDialog<String>(
      context:context,
      builder:(d)=>Theme(
        data:ThemeData.light(),
        child:AlertDialog(
          backgroundColor:Colors.white,
          surfaceTintColor:Colors.white,
          title:const Text('Kimliğini doğrula',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          content:TextField(controller:kontrol,obscureText:true,decoration:const InputDecoration(labelText:'Mevcut şifre')),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(d),child:const Text('Vazgeç')),
            FilledButton(onPressed:()=>Navigator.pop(d,kontrol.text),child:const Text('Doğrula')),
          ],
        ),
      ),
    );
    kontrol.dispose();
    return x;
  }

  Future<void> kaydet()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null||kaydediliyor)return;
    final re=email.text.trim().toLowerCase();
    final tel=telefon.text.trim();
    if(re.isNotEmpty&&(!re.contains('@')||!re.contains('.'))){
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Geçerli bir kurtarma e-postası yaz.')));
      return;
    }
    final sifre=await _sifreSor();
    if(sifre==null||sifre.isEmpty)return;
    setState(()=>kaydediliyor=true);
    try{
      final hesapEmail=u.email;
      if(hesapEmail==null||hesapEmail.isEmpty)throw Exception('Bu hesapta doğrulanabilir e-posta bulunamadı.');
      await u.reauthenticateWithCredential(EmailAuthProvider.credential(email:hesapEmail,password:sifre));
      await FirebaseFirestore.instance.collection('users').doc(u.uid).set({
        'recoveryEmail':re,
        'recoveryPhone':tel,
        'recoveryUpdatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Kurtarma seçenekleri kaydedildi.')));
    }on FirebaseAuthException catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
        e.code=='wrong-password'||e.code=='invalid-credential'?'Şifre doğrulanamadı.':'Doğrulama başarısız: '+(e.message??e.code)
      )));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kaydedilemedi: '+e.toString())));
    }finally{
      if(mounted)setState(()=>kaydediliyor=false);
    }
  }

  Future<void> sifreBaglantisi()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u?.email==null)return;
    try{
      await FirebaseAuth.instance.sendPasswordResetEmail(email:u!.email!);
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Şifre yenileme bağlantısı hesap e-postana gönderildi.')));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Bağlantı gönderilemedi: '+e.toString())));
    }
  }

  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light().copyWith(
      scaffoldBackgroundColor:Colors.white,
      appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),
    ),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Hesap kurtarma')),
      body:yukleniyor
        ? const Center(child:CircularProgressIndicator(color:mor))
        : ListView(padding:const EdgeInsets.all(20),children:[
            ListTile(contentPadding:EdgeInsets.zero,leading:const Icon(Icons.alternate_email_rounded,color:mor),title:const Text('Hesap e-postası'),subtitle:Text(FirebaseAuth.instance.currentUser?.email??'E-posta yok')),
            const SizedBox(height:12),
            TextField(controller:email,keyboardType:TextInputType.emailAddress,decoration:const InputDecoration(labelText:'Kurtarma e-postası')),
            const SizedBox(height:14),
            TextField(controller:telefon,keyboardType:TextInputType.phone,decoration:const InputDecoration(labelText:'Kurtarma telefonu')),
            const SizedBox(height:20),
            FilledButton.icon(onPressed:kaydediliyor?null:kaydet,icon:const Icon(Icons.shield_outlined),label:Text(kaydediliyor?'Doğrulanıyor...':'Kurtarma bilgilerini kaydet')),
            const SizedBox(height:10),
            OutlinedButton.icon(onPressed:sifreBaglantisi,icon:const Icon(Icons.lock_reset_rounded),label:const Text('Şifre yenileme bağlantısı gönder')),
          ]),
    ),
  );
}

class HesapGuvenligiPage extends StatefulWidget {const HesapGuvenligiPage({super.key});@override State<HesapGuvenligiPage> createState()=>_HesapGuvenligiPageState();}
class _HesapGuvenligiPageState extends State<HesapGuvenligiPage>{
  bool yukleniyor=false;
  Future<bool> onay(String baslik,String aciklama,String dugme)async=>await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:Text(baslik),content:Text(aciklama),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),style:FilledButton.styleFrom(backgroundColor:Colors.red),child:Text(dugme))]))??false;
  Future<void> dondur()async{if(!await onay('Hesap dondurulsun mu?','Hesabın geçici olarak kapatılacak. Giriş yaparak hesabını yeniden açabilirsin.','Hesabı dondur'))return;await isle({'deactivated':true,'deactivatedAt':FieldValue.serverTimestamp()});}
  Future<void> silmeTalebi()async{if(!await onay('Hesap silme talebi oluşturulsun mu?','Hesabın hemen kapanacak ve 30 gün sonra kalıcı silinmek üzere işaretlenecek. Bu sürede giriş yaparak talebi iptal edebilirsin.','Silme talebi oluştur'))return;await isle({'deactivated':true,'deletionRequestedAt':FieldValue.serverTimestamp(),'deletionScheduledFor':Timestamp.fromDate(DateTime.now().add(const Duration(days:30)))});}
  Future<void> isle(Map<String,dynamic> veri)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;setState(()=>yukleniyor=true);try{await FirebaseFirestore.instance.collection('users').doc(u.uid).set(veri,SetOptions(merge:true));await FirebaseAuth.instance.signOut();if(mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const GirisPage()),(_)=>false);}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('İşlem tamamlanamadı: $e')));}finally{if(mounted)setState(()=>yukleniyor=false);}}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Hesap güvenliği')),body:SafeArea(child:ListView(padding:const EdgeInsets.all(18),children:[
    const ListTile(leading:Icon(Icons.verified_user_outlined,color:Colors.green),title:Text('E-posta doğrulaması'),subtitle:Text('Hesabın doğrulanmış e-posta ile korunur.')),
    ListTile(leading:const Icon(Icons.health_and_safety_outlined,color:mor),title:const Text('Hesap kurtarma seçenekleri'),subtitle:const Text('Kurtarma e-postası, telefon ve şifre yenileme'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const HesapKurtarmaPage()))),
    const Divider(),
    ListTile(enabled:!yukleniyor,leading:const Icon(Icons.pause_circle_outline,color:Colors.orange),title:const Text('Hesabı dondur'),subtitle:const Text('Geri dönene kadar profilini geçici olarak gizle'),onTap:dondur),
    ListTile(enabled:!yukleniyor,leading:const Icon(Icons.delete_forever_outlined,color:Colors.red),title:const Text('Hesap silme talebi',style:TextStyle(color:Colors.red)),subtitle:const Text('30 günlük geri alma süresiyle kapat'),onTap:silmeTalebi),
    if(yukleniyor)const Padding(padding:EdgeInsets.all(20),child:Center(child:CircularProgressIndicator())),
  ]))));
}

class GirisGecmisiPage extends StatefulWidget{
  const GirisGecmisiPage({super.key});
  @override State<GirisGecmisiPage> createState()=>_GirisGecmisiPageState();
}
class _GirisGecmisiPageState extends State<GirisGecmisiPage>{
  String? mevcutId;
  @override void initState(){super.initState();cihazKurulumKimligi().then((x){if(mounted)setState(()=>mevcutId=x);});}

  Future<void> cihazdanCik(String deviceId,String ad)async{
    final u=FirebaseAuth.instance.currentUser;if(u==null)return;
    final ok=await showDialog<bool>(
      context:context,
      builder:(c)=>Theme(
        data:ThemeData.light(),
        child:AlertDialog(
          backgroundColor:Colors.white,surfaceTintColor:Colors.white,
          title:const Text('Bu cihazdaki oturum kapatılsın mı?',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          content:Text(ad+' cihazı NgelX yeniden açıldığında oturumdan çıkarılacak.',style:const TextStyle(color:Colors.black87)),
          actions:[
            TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
            FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(c,true),child:const Text('Oturumu kapat')),
          ],
        ),
      ),
    )??false;
    if(!ok)return;
    await FirebaseFirestore.instance.collection('users').doc(u.uid).set({
      'revokedDeviceIds':FieldValue.arrayUnion([deviceId]),
    },SetOptions(merge:true));
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Cihaza çıkış talimatı gönderildi.')));
  }

  @override Widget build(BuildContext context){
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(
      data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),
      child:Scaffold(
        appBar:AppBar(title:const Text('Giriş yapılan cihazlar')),
        body:uid==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:FirebaseFirestore.instance.collection('users').doc(uid).snapshots(),
          builder:(context,s){
            if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());
            final ham=List<dynamic>.from(s.data?.data()?['loginHistory']??const[]);
            final ters=ham.whereType<Map>().toList().reversed.toList();
            final gorulen=<String>{},kayitlar=<Map>[];
            for(final k in ters){
              final id=(k['deviceId']??'').toString();
              final anahtar=id.isEmpty?((k['device']??'').toString()+'|'+(k['platform']??'').toString()):id;
              if(gorulen.add(anahtar))kayitlar.add(k);
              if(kayitlar.length>=10)break;
            }
            final iptal=Set<String>.from(List<String>.from(s.data?.data()?['revokedDeviceIds']??const[]));
            if(kayitlar.isEmpty)return const Center(child:Text('Henüz cihaz kaydı yok.'));
            return ListView.separated(
              padding:const EdgeInsets.all(16),
              itemCount:kayitlar.length,
              separatorBuilder:(_,__)=>const Divider(),
              itemBuilder:(_,i){
                final k=kayitlar[i];
                final id=(k['deviceId']??'').toString();
                final tarih=DateTime.tryParse((k['at']??'').toString())?.toLocal();
                final buCihaz=id.isNotEmpty&&id==mevcutId;
                final iptalEdildi=id.isNotEmpty&&iptal.contains(id);
                final ad=(k['device']??'Android cihaz').toString();
                final tarihYazi=tarih==null?'':' • '+tarih.day.toString().padLeft(2,'0')+'/'+tarih.month.toString().padLeft(2,'0')+'/'+tarih.year.toString()+' '+tarih.hour.toString().padLeft(2,'0')+':'+tarih.minute.toString().padLeft(2,'0');
                return ListTile(
                  leading:CircleAvatar(child:Icon(buCihaz?Icons.smartphone_rounded:Icons.phone_android)),
                  title:Row(children:[Expanded(child:Text(ad)),if(buCihaz)const Chip(label:Text('Bu cihaz'),visualDensity:VisualDensity.compact)]),
                  subtitle:Text((k['platform']??'Android').toString()+tarihYazi+(iptalEdildi?'\nÇıkış talimatı bekliyor':'')),
                  trailing:(!buCihaz&&id.isNotEmpty&&!iptalEdildi)
                    ? TextButton(onPressed:()=>cihazdanCik(id,ad),child:const Text('Çıkış yap',style:TextStyle(color:Colors.red)))
                    : null,
                );
              },
            );
          },
        ),
      ),
    );
  }
}

class EngellenenlerPage extends StatefulWidget {const EngellenenlerPage({super.key});@override State<EngellenenlerPage> createState()=>_EngellenenlerPageState();}
class _EngellenenlerPageState extends State<EngellenenlerPage>{
  Future<List<String>> getir()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return[];final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();return List<String>.from(d.data()?['blocked']??const[]);}
  Future<void> kaldir(String uid)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'blocked':FieldValue.arrayRemove([uid])},SetOptions(merge:true));if(mounted)setState((){});}
/* Eski sıkıştırılmış görünüm devre dışı.
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:const Text('Engellenen hesaplar')),body:FutureBuilder<List<String>>(future:getir(),builder:(context,s){if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());final ids=s.data??[];if(ids.isEmpty)return const Center(child:Text('Engellediğin hesap yok.'));return ListView.separated(padding:const EdgeInsets.all(14),itemCount:ids.length,separatorBuilder:(_,__)=>const Divider(),itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),builder:(_,p){final v=p.data?.data()??{},foto=(v['photoUrl']??'').toString();return ListTile(leading:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person):null),title:Text((v['displayName']??v['username']??'Ngel X kullanıcısı').toString()),subtitle:Text('@${v['username']??'ngelx'}'),trailing:TextButton(onPressed:()=>kaldir(ids[i]),child:const Text('Engeli kaldır')));});});}));
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
                  leading: CircleAvatar(backgroundImage: foto.isEmpty ? null : CachedNetworkImageProvider(foto), child: foto.isEmpty ? const Icon(Icons.person) : null),
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
  Future<void> gonder()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;if(aciklama.text.trim().length<10){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Sorunu en az 10 karakterle açıkla.')));return;}setState(()=>gonderiliyor=true);try{String ekranUrl='';if(ekran!=null){final yol='support/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';ekranUrl=await ngelxMedyaYukleBytes(bytes:await ekran!.readAsBytes(),kind:'support',ext:'jpg',legacyPath:yol);}await FirebaseFirestore.instance.collection('support_requests').add({'uid':u.uid,'email':u.email,'category':kategori,'description':aciklama.text.trim(),'screenshotUrl':ekranUrl,'status':'open','createdAt':FieldValue.serverTimestamp()});if(!mounted)return;aciklama.clear();setState(()=>ekran=null);ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Destek talebin gönderildi.')));}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Talep gönderilemedi: $e')));}finally{if(mounted)setState(()=>gonderiliyor=false);}}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none))),child:Scaffold(appBar:AppBar(title:const Text('Destek ve hata bildir')),body:SafeArea(child:ListView(padding:const EdgeInsets.all(20),children:[DropdownButtonFormField<String>(initialValue:kategori,items:['Uygulama hatası','Hesap ve giriş','Güvenlik','Ödeme ve kazanç','Öneri','Diğer'].map((x)=>DropdownMenuItem(value:x,child:Text(x))).toList(),onChanged:(v)=>setState(()=>kategori=v??kategori),decoration:const InputDecoration(labelText:'Konu')),const SizedBox(height:14),TextField(controller:aciklama,minLines:5,maxLines:10,maxLength:1000,decoration:const InputDecoration(labelText:'Sorunu veya isteğini anlat')),const SizedBox(height:12),OutlinedButton.icon(onPressed:gonderiliyor?null:ekranSec,icon:const Icon(Icons.add_photo_alternate_outlined),label:Text(ekran==null?'Ekran görüntüsü ekle':'Ekran görüntüsü seçildi')),const SizedBox(height:20),RenkliButon(yazi:gonderiliyor?'Gönderiliyor...':'Destek talebini gönder',tiklama:gonderiliyor?(){}:gonder)]))));
}

class TercihlerPage extends StatefulWidget {final String baslik;const TercihlerPage({super.key,required this.baslik});@override State<TercihlerPage> createState()=>_TercihlerPageState();}
class _TercihlerPageState extends State<TercihlerPage> {
  bool hesapGizli=false, profilArama=true, aktiflik=true, profilPaylasArkadas=false, yorumArkadas=false, gizliKelimeler=true, mesajArkadas=true, hikayeArkadas=true, ekranGoruntusu=false, bildirim=true, mesajBildirimi=true, arkadasBildirimi=true, etkilesimBildirimi=true, indirme=true;
  String mesajIzni='friends';
  String profilGoruntuleme='all';
  List<String> gizliKelimeListesi=[];
  String? get uid => FirebaseAuth.instance.currentUser?.uid;

  @override
  void initState(){super.initState();yukle();}

  Future<void> yukle() async {
    if(uid==null)return;
    final d=await FirebaseFirestore.instance.collection('users').doc(uid).get(),v=d.data()??{};
    if(mounted)setState((){
      hesapGizli=v['privateAccount']==true;
      profilGoruntuleme=(v['profileViewPermission']??'all').toString();
      profilArama=v['discoverableProfile']!=false;
      aktiflik=v['showActivityStatus']!=false;
      profilPaylasArkadas=v['profileShareFriendsOnly']==true;
      yorumArkadas=v['friendsOnlyComments']==true;
      gizliKelimeler=v['hiddenWordsFilter']!=false;
      gizliKelimeListesi=List<String>.from(v['hiddenWords']??const[]);
      mesajArkadas=v['friendsOnlyMessages']!=false;
      mesajIzni=(v['messagePermission']??(mesajArkadas?'friends':'all')).toString();
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
  Future<void> kaydetMetin(String k,String v)async{
    if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));
  }
  Future<void> gizliKelimeYonet()async{
    final kontrol=TextEditingController();
    await showModalBottomSheet<void>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,isScrollControlled:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:StatefulBuilder(builder:(c,setP)=>SafeArea(child:Padding(
        padding:EdgeInsets.fromLTRB(18,6,18,MediaQuery.of(c).viewInsets.bottom+18),
        child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
          const Text('Gizli kelimeler',style:TextStyle(color:Colors.black87,fontSize:20,fontWeight:FontWeight.w900)),
          const SizedBox(height:6),
          const Text('Bu kelimeleri içeren yorum ve özel mesajlar sende gizlenir.',style:TextStyle(color:Colors.black54)),
          const SizedBox(height:14),
          if(gizliKelimeListesi.isNotEmpty)Wrap(spacing:7,runSpacing:7,children:gizliKelimeListesi.map((x)=>InputChip(
            label:Text(x),onDeleted:()async{
              gizliKelimeListesi.remove(x);
              await FirebaseFirestore.instance.collection('users').doc(uid!).set({'hiddenWords':gizliKelimeListesi},SetOptions(merge:true));
              if(mounted)setState((){});setP((){});
            },
          )).toList()),
          const SizedBox(height:12),
          Row(children:[
            Expanded(child:TextField(controller:kontrol,maxLength:30,decoration:const InputDecoration(hintText:'Kelime veya ifade ekle'))),
            const SizedBox(width:8),
            FilledButton(onPressed:()async{
              final x=kontrol.text.trim().toLowerCase();
              if(x.isEmpty||gizliKelimeListesi.contains(x))return;
              gizliKelimeListesi.add(x);kontrol.clear();
              await FirebaseFirestore.instance.collection('users').doc(uid!).set({'hiddenWords':gizliKelimeListesi,'hiddenWordsFilter':true},SetOptions(merge:true));
              if(mounted)setState(()=>gizliKelimeler=true);setP((){});
            },child:const Text('Ekle')),
          ]),
        ]),
      )))),
    );
    kontrol.dispose();
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
        return [
          satir('Gizli hesap','Yeni takipçiler onay bekler',hesapGizli,(v){setState(()=>hesapGizli=v);kaydet('privateAccount',v);}),
          const Padding(padding:EdgeInsets.fromLTRB(22,14,22,4),child:Text('Profili kimler görüntüleyebilir?',style:TextStyle(fontWeight:FontWeight.w900))),
          for(final e in const [('all','Herkes'),('followers','Takipçilerim'),('friends','Arkadaşlarım')])
            RadioListTile<String>(
              value:e.$1,groupValue:profilGoruntuleme,
              title:Text(e.$2),
              onChanged:(v)async{if(v==null)return;setState(()=>profilGoruntuleme=v);await kaydetMetin('profileViewPermission',v);},
            ),
          satir('Profil aramalarında görün','Kullanıcılar seni adınla bulabilsin',profilArama,(v){setState(()=>profilArama=v);kaydet('discoverableProfile',v);}),
          satir('Aktiflik durumunu göster','Arkadaşların son görülme bilgini görebilsin',aktiflik,(v){setState(()=>aktiflik=v);kaydet('showActivityStatus',v);}),
          satir('Profil paylaşımını arkadaşlarla sınırla','Profil bağlantını yalnızca arkadaşların paylaşabilsin',profilPaylasArkadas,(v){setState(()=>profilPaylasArkadas=v);kaydet('profileShareFriendsOnly',v);}),
          satir('Yorumları arkadaşlarla sınırla','Yalnızca arkadaşların yorum yapabilsin',yorumArkadas,(v){setState(()=>yorumArkadas=v);kaydet('friendsOnlyComments',v);}),
          satir('Gizli kelime filtresi','Seçtiğin kelimeleri içeren yorum ve mesajları gizle',gizliKelimeler,(v){setState(()=>gizliKelimeler=v);kaydet('hiddenWordsFilter',v);}),
          ListTile(
            contentPadding:const EdgeInsets.symmetric(horizontal:22,vertical:6),
            leading:const Icon(Icons.visibility_off_outlined,color:mor),
            title:const Text('Gizli kelimeleri yönet',style:TextStyle(fontWeight:FontWeight.w700)),
            subtitle:Text(gizliKelimeListesi.isEmpty?'Henüz kelime eklenmedi':gizliKelimeListesi.length.toString()+' kelime / ifade'),
            trailing:const Icon(Icons.chevron_right),
            onTap:gizliKelimeYonet,
          ),
          const Divider(),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:22,vertical:6),leading:const Icon(Icons.block_outlined,color:mor),title:const Text('Engellenen hesaplar',style:TextStyle(fontWeight:FontWeight.w700)),subtitle:const Text('Engellediğin hesapları yönet'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const EngellenenlerPage()))),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:22,vertical:6),leading:const Icon(Icons.history_toggle_off_rounded,color:mor),title:const Text('Takip isteği geçmişi',style:TextStyle(fontWeight:FontWeight.w700)),subtitle:const Text('Gönderdiğin bekleyen, kabul edilen ve reddedilen istekler'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TakipIstegiGecmisiPage()))),
        ];
      case 'Mesaj izinleri':
        return [
          const Padding(padding:EdgeInsets.fromLTRB(22,16,22,8),child:Text('Kim mesaj atabilir?',style:TextStyle(fontSize:18,fontWeight:FontWeight.w900))),
          for(final e in const [('all','Herkes','Mesaj istekleri dahil herkes yazabilir'),('following','Takip ettiklerim','Yalnızca senin takip ettiğin hesaplar'),('friends','Arkadaşlar','Yalnızca arkadaşların'),('none','Kimse','Yeni özel mesaj kabul etme')])
            RadioListTile<String>(
              value:e.$1,groupValue:mesajIzni,
              title:Text(e.$2,style:const TextStyle(fontWeight:FontWeight.w700)),
              subtitle:Text(e.$3),
              onChanged:(v)async{
                if(v==null)return;
                setState(()=>mesajIzni=v);
                await kaydetMetin('messagePermission',v);
                await kaydet('friendsOnlyMessages',v=='friends');
              },
            ),
        ];
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

class ArkadaslarPage extends StatelessWidget {
  const ArkadaslarPage({super.key});
  @override Widget build(BuildContext context) {
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(
      data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),
      child:Scaffold(
        backgroundColor:Colors.white,
        appBar:AppBar(title:const Text('Arkadaşlar',style:TextStyle(fontWeight:FontWeight.w900))),
        body:FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          future:uid==null?null:FirebaseFirestore.instance.collection('users').doc(uid).get(),
          builder:(_,s){
            final ids=List<String>.from(s.data?.data()?['friends']??[]);
            if(ids.isEmpty)return const Center(child:Text('Henüz arkadaşın yok.',style:TextStyle(color:Colors.black54)));
            return ListView(children:ids.map((id)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              future:FirebaseFirestore.instance.collection('users').doc(id).get(),
              builder:(_,u){
                final v=u.data?.data()??<String,dynamic>{},foto=(v['photoUrl']??'').toString();
                return ListTile(
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:id))),
                  onLongPress:()async{
                    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
                      title:const Text('Arkadaşlıktan çıkarılsın mı?'),
                      content:Text('${v['displayName']??v['username']??'Bu kişi'} arkadaşlıktan çıkarılsın mı?'),
                      actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),TextButton(onPressed:()=>Navigator.pop(c,true),child:const Text('ARKADAŞLIKTAN ÇIKAR',style:TextStyle(color:Colors.red,fontWeight:FontWeight.bold)))]));
                    if(ok==true&&uid!=null){
                      await FirebaseFirestore.instance.collection('users').doc(uid).update({'friends':FieldValue.arrayRemove([id])});
                      await FirebaseFirestore.instance.collection('users').doc(id).update({'friends':FieldValue.arrayRemove([uid])});
                    }
                  },
                  leading:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person):null),
                  title:Text((v['displayName']??v['username']??'NgelX').toString(),style:const TextStyle(fontWeight:FontWeight.w800)),
                  subtitle:Text('@${v['username']??'ngelx'}'),trailing:const Icon(Icons.chevron_right),
                );
              },
            )).toList());
          },
        ),
      ),
    );
  }
}

class TakipIstegiGecmisiPage extends StatelessWidget{
  const TakipIstegiGecmisiPage({super.key});
  String durum(Map<String,dynamic> v){
    switch((v['status']??'pending').toString()){
      case 'accepted':return 'Kabul edildi';
      case 'rejected':return 'Reddedildi';
      default:return 'Bekliyor';
    }
  }
  Color durumRengi(Map<String,dynamic> v){
    switch((v['status']??'pending').toString()){
      case 'accepted':return Colors.green;
      case 'rejected':return Colors.red;
      default:return Colors.orange;
    }
  }
  @override Widget build(BuildContext context){
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light(),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Takip isteği geçmişi',style:TextStyle(fontWeight:FontWeight.w900))),
      body:uid==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('notifications').where('fromUid',isEqualTo:uid).limit(100).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final docs=(s.data?.docs??[]).where((d)=>d.data()['type']=='follow_request').toList()
            ..sort((a,b){
              final at=a.data()['createdAt'],bt=b.data()['createdAt'];
              final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
              return bm.compareTo(am);
            });
          if(docs.isEmpty)return const Center(child:Text('Gönderilmiş takip isteğin yok.',style:TextStyle(color:Colors.black54)));
          return ListView.separated(
            padding:const EdgeInsets.all(12),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),
            itemBuilder:(_,i){
              final v=docs[i].data(),hedef=(v['toUid']??'').toString();
              return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                future:FirebaseFirestore.instance.collection('users').doc(hedef).get(),
                builder:(_,u){
                  final p=u.data?.data()??<String,dynamic>{},foto=(p['photoUrl']??'').toString(),ad=(p['displayName']??p['username']??'NgelX kullanıcısı').toString();
                  return ListTile(
                    onTap:hedef.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:hedef))),
                    leading:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person):null),
                    title:Text(ad,style:const TextStyle(fontWeight:FontWeight.w800)),
                    subtitle:Text(zamanKisa(v['createdAt'])),
                    trailing:Text(durum(v),style:TextStyle(color:durumRengi(v),fontWeight:FontWeight.w800)),
                  );
                },
              );
            },
          );
        },
      ),
    ));
  }
}

class KullaniciListesiPage extends StatefulWidget{
  final String uid,alan,baslik;
  const KullaniciListesiPage({super.key,required this.uid,required this.alan,required this.baslik});
  @override State<KullaniciListesiPage> createState()=>_KullaniciListesiPageState();
}
class _KullaniciListesiPageState extends State<KullaniciListesiPage>{
  String arama='';
  String? get me=>FirebaseAuth.instance.currentUser?.uid;

  Future<void> takipciyiKaldir(String hedefUid,String ad)async{
    final benim=me;if(benim==null||widget.uid!=benim||widget.alan!='followers')return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(
      backgroundColor:Colors.white,surfaceTintColor:Colors.white,
      title:const Text('Takipçi kaldırılsın mı?',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
      content:Text(ad+' seni artık takip etmeyecek. Bu kişiye bildirim gönderilmez.',style:const TextStyle(color:Colors.black87)),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),
        FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),onPressed:()=>Navigator.pop(c,true),child:const Text('Takipçiyi kaldır')),
      ],
    ))??false;
    if(!ok)return;
    final batch=FirebaseFirestore.instance.batch();
    batch.set(FirebaseFirestore.instance.collection('users').doc(benim),{'followers':FieldValue.arrayRemove([hedefUid])},SetOptions(merge:true));
    batch.set(FirebaseFirestore.instance.collection('users').doc(hedefUid),{'following':FieldValue.arrayRemove([benim])},SetOptions(merge:true));
    await batch.commit();
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takipçi kaldırıldı.')));
  }

  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:Text(widget.baslik,style:const TextStyle(fontWeight:FontWeight.w900))),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final ids=List<String>.from(s.data?.data()?[widget.alan]??const[]);
          if(ids.isEmpty)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.people_outline,size:54,color:mor),const SizedBox(height:12),Text(widget.baslik+' listesi boş.',style:const TextStyle(color:Colors.black54))]));
          return Column(children:[
            Padding(
              padding:const EdgeInsets.fromLTRB(12,10,12,6),
              child:TextField(
                onChanged:(v)=>setState(()=>arama=v.trim().toLowerCase()),
                decoration:InputDecoration(
                  hintText:'Kişi ara',
                  prefixIcon:const Icon(Icons.search_rounded),
                  filled:true,fillColor:const Color(0xFFF3F4F6),
                  border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none),
                ),
              ),
            ),
            Expanded(child:ListView.builder(
              padding:const EdgeInsets.all(12),itemCount:ids.length,
              itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),
                builder:(_,u){
                  final v=u.data?.data()??<String,dynamic>{},foto=(v['photoUrl']??'').toString(),ad=(v['displayName']??v['username']??'NgelX').toString(),kullanici=(v['username']??'ngelx').toString();
                  final metin=(ad+' '+kullanici).toLowerCase();
                  if(arama.isNotEmpty&&!metin.contains(arama))return const SizedBox.shrink();
                  final kaldirabilir=me==widget.uid&&widget.alan=='followers'&&ids[i]!=me;
                  return ListTile(
                    onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:ids[i]))),
                    leading:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person):null),
                    title:Text(ad,style:const TextStyle(fontWeight:FontWeight.w800)),
                    subtitle:Text('@'+kullanici),
                    trailing:kaldirabilir?PopupMenuButton<String>(
                      onSelected:(x){if(x=='remove')takipciyiKaldir(ids[i],ad);},
                      itemBuilder:(_)=>const [PopupMenuItem(value:'remove',child:Text('Takipçiyi kaldır',style:TextStyle(color:Colors.red)))],
                    ):const Icon(Icons.chevron_right),
                  );
                },
              ),
            )),
          ]);
        },
      ),
    ),
  );
}


class EtkilesimOzetiPage extends StatelessWidget{
  final String uid;
  const EtkilesimOzetiPage({super.key,required this.uid});
  int puan(Map<String,dynamic> v)=>((v['likeCount'] as num?)?.toInt()??0)+((v['commentCount'] as num?)?.toInt()??0)+((v['shareCount'] as num?)?.toInt()??0);
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Etkileşim',style:TextStyle(fontWeight:FontWeight.w900))),
      body:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).limit(100).snapshots(),
        builder:(_,s){
          final d=(s.data?.docs??[]).where((x)=>x.data()['type']!='story').toList();
          final eksik=d.where((x)=>x.data()['likeCount']==null||x.data()['commentCount']==null).toList();
          if(eksik.isNotEmpty){
            return FutureBuilder<void>(
              future:Future.wait(eksik.map((x)async{
                final v=x.data();
                final sonuc=await Future.wait([
                  if(v['likeCount']==null)x.reference.collection('likes').count().get(),
                  if(v['commentCount']==null)x.reference.collection('comments').count().get(),
                ]);
                int i=0;
                final guncelle=<String,dynamic>{};
                if(v['likeCount']==null)guncelle['likeCount']=(sonuc[i++] as AggregateQuerySnapshot).count??0;
                if(v['commentCount']==null)guncelle['commentCount']=(sonuc[i++] as AggregateQuerySnapshot).count??0;
                if(guncelle.isNotEmpty)await x.reference.set(guncelle,SetOptions(merge:true));
              })),
              builder:(_,geri){
                if(geri.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator(color:mor));
                return const SizedBox.shrink();
              },
            );
          }
          int begeni=0,yorum=0,paylasim=0;
          for(final x in d){final v=x.data();begeni+=((v['likeCount'] as num?)?.toInt()??0);yorum+=((v['commentCount'] as num?)?.toInt()??0);paylasim+=((v['shareCount'] as num?)?.toInt()??0);}
          final benim=FirebaseAuth.instance.currentUser?.uid==uid;
          final top=[...d]..sort((a,b)=>puan(b.data()).compareTo(puan(a.data())));
          return ListView(padding:const EdgeInsets.all(20),children:[
            const Text('İçerik istatistikleri',style:TextStyle(fontSize:22,fontWeight:FontWeight.w900)),
            const SizedBox(height:18),
            Row(children:[_kart(Icons.favorite_rounded,'Beğeni',begeni,Colors.red),_kart(Icons.comment_rounded,'Yorum',yorum,Colors.blue)]),
            const SizedBox(height:12),
            Row(children:[_kart(Icons.send_rounded,'Paylaşım',paylasim,mor),_kart(Icons.grid_view_rounded,'Gönderi',d.length,Colors.orange)]),
            if(benim)...[
              const SizedBox(height:24),
              ListTile(
                contentPadding:EdgeInsets.zero,
                leading:const CircleAvatar(backgroundColor:Color(0xFFF1E9FF),child:Icon(Icons.query_stats_rounded,color:mor)),
                title:const Text('Profil ziyaret eğilimleri',style:TextStyle(fontWeight:FontWeight.w800)),
                subtitle:const Text('Günlük ziyaret sayılarındaki değişimi gör'),
                trailing:const Icon(Icons.chevron_right),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ProfilZiyaretTrendPage())),
              ),
              const SizedBox(height:16),
              const Text('En çok etkileşim alan gönderiler',style:TextStyle(fontSize:18,fontWeight:FontWeight.w900)),
              const SizedBox(height:8),
              if(top.isEmpty)const Text('Henüz gönderi yok.',style:TextStyle(color:Colors.black54)),
              ...top.take(5).map((x){
                final v=x.data(),aciklama=(v['description']??'Gönderi').toString();
                return ListTile(
                  contentPadding:EdgeInsets.zero,
                  leading:CircleAvatar(backgroundColor:const Color(0xFFF1F2F4),child:Text((puan(v)).toString(),style:const TextStyle(fontWeight:FontWeight.w900))),
                  title:Text(aciklama.isEmpty?'Gönderi':aciklama,maxLines:1,overflow:TextOverflow.ellipsis),
                  subtitle:Text('Toplam etkileşim: '+puan(v).toString()),
                  trailing:const Icon(Icons.chevron_right),
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:x.id))),
                );
              }),
            ],
          ]);
        },
      ),
    ),
  );
  Widget _kart(IconData i,String t,int n,Color c)=>Expanded(child:Container(margin:const EdgeInsets.all(5),padding:const EdgeInsets.all(18),decoration:BoxDecoration(color:c.withValues(alpha:.10),borderRadius:BorderRadius.circular(20)),child:Column(children:[Icon(i,color:c),const SizedBox(height:8),Text(n.toString(),style:const TextStyle(fontSize:24,fontWeight:FontWeight.w900)),Text(t,style:const TextStyle(color:Colors.black54))])));
}

class ProfilAramaPage extends StatefulWidget{
  final String uid;
  const ProfilAramaPage({super.key,required this.uid});
  @override State<ProfilAramaPage> createState()=>_ProfilAramaPageState();
}
class _ProfilAramaPageState extends State<ProfilAramaPage>{
  String q='';
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:TextField(autofocus:true,onChanged:(v)=>setState(()=>q=v.trim().toLowerCase()),decoration:const InputDecoration(hintText:'Profilde ara',prefixIcon:Icon(Icons.search)))),
      body:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.uid).limit(100).snapshots(),
        builder:(_,s){
          final docs=(s.data?.docs??[]).where((d){final v=d.data();return v['type']!='story'&&(q.isEmpty||(v['description']??'').toString().toLowerCase().contains(q));}).toList();
          if(docs.isEmpty)return const Center(child:Text('Eşleşen paylaşım bulunamadı.',style:TextStyle(color:Colors.black54)));
          return ListView.separated(
            padding:const EdgeInsets.all(14),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),
            itemBuilder:(_,i){
              final v=docs[i].data();
              return ListTile(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:docs[i].id))),leading:const CircleAvatar(backgroundColor:Color(0xFFF1E9FF),child:Icon(Icons.grid_view,color:mor)),title:Text((v['description']??'Adsız paylaşım').toString(),maxLines:2,overflow:TextOverflow.ellipsis),trailing:const Icon(Icons.chevron_right));
            },
          );
        },
      ),
    ),
  );
}

class HikayeArsiviPage extends StatelessWidget{
  const HikayeArsiviPage({super.key});
  @override Widget build(BuildContext context){
    final uid=FirebaseAuth.instance.currentUser?.uid;
    return Theme(data:ThemeData.light(),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Hikâye arşivi',style:TextStyle(fontWeight:FontWeight.w900))),
      body:uid==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
        stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:uid).limit(100).snapshots(),
        builder:(_,s){
          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
          final docs=(s.data?.docs??[]).where((d)=>d.data()['type']=='story').toList()
            ..sort((a,b){
              final at=a.data()['createdAt'],bt=b.data()['createdAt'];
              final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
              return bm.compareTo(am);
            });
          if(docs.isEmpty)return const Center(child:Text('Henüz arşivlenmiş hikâyen yok.',style:TextStyle(color:Colors.black54)));
          return ListView.separated(
            padding:const EdgeInsets.all(12),itemCount:docs.length,separatorBuilder:(_,__)=>const Divider(),
            itemBuilder:(_,i){
              final d=docs[i],v=d.data(),url=(v['mediaUrl']??'').toString(),oneCikan=v['highlighted']==true;
              return ListTile(
                leading:ClipRRect(borderRadius:BorderRadius.circular(10),child:url.isEmpty?const SizedBox(width:54,height:54,child:Icon(Icons.image_not_supported_outlined)):CachedNetworkImage(imageUrl:url,width:54,height:54,fit:BoxFit.cover)),
                title:Text(zamanKisa(v['createdAt']),style:const TextStyle(fontWeight:FontWeight.w800)),
                subtitle:Text(oneCikan?'Öne çıkanlarda gösteriliyor':'Arşivde'),
                trailing:IconButton(
                  tooltip:oneCikan?'Öne çıkandan kaldır':'Öne çıkar',
                  onPressed:()=>d.reference.set({'highlighted':!oneCikan},SetOptions(merge:true)),
                  icon:Icon(oneCikan?Icons.star_rounded:Icons.star_border_rounded,color:oneCikan?Colors.amber:mor),
                ),
                onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(
                  url:url,kullanici:'Hikâyem',ownerUid:uid,storyId:d.id,createdAt:v['createdAt'],expiresAt:v['expiresAt'],
                ))),
              );
            },
          );
        },
      ),
    ));
  }
}

class ProfilBolumuPage extends StatelessWidget{final String baslik,aciklama;final IconData ikon;const ProfilBolumuPage({super.key,required this.baslik,required this.aciklama,required this.ikon});@override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:Text(baslik,style:const TextStyle(fontWeight:FontWeight.w900))),body:Center(child:Padding(padding:const EdgeInsets.all(28),child:Column(mainAxisSize:MainAxisSize.min,children:[CircleAvatar(radius:38,backgroundColor:const Color(0xFFF1E9FF),child:Icon(ikon,color:mor,size:38)),const SizedBox(height:14),Text(aciklama,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54,fontSize:16))])))));}

class IcerikGizlemePage extends StatelessWidget{
  final String videoId;
  const IcerikGizlemePage({super.key,required this.videoId});
  @override Widget build(BuildContext context){
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null)return const Scaffold(body:Center(child:Text('Oturum bulunamadı.')));
    final videoRef=FirebaseFirestore.instance.collection('videos').doc(videoId);
    return Theme(data:ThemeData.light(),child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('İçeriği kimlerden gizle?',style:TextStyle(fontWeight:FontWeight.w900))),
      body:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:videoRef.snapshots(),
        builder:(_,videoSnap){
          final hidden=Set<String>.from(List<String>.from(videoSnap.data?.data()?['hiddenFor']??const[]));
          return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('users').doc(me).snapshots(),
            builder:(_,userSnap){
              final uv=userSnap.data?.data()??<String,dynamic>{};
              final ids=<String>{...List<String>.from(uv['friends']??const[]),...List<String>.from(uv['followers']??const[])}.toList();
              if(ids.isEmpty)return const Center(child:Text('Gizleyebileceğin arkadaş veya takipçi yok.',style:TextStyle(color:Colors.black54)));
              return ListView.builder(
                padding:const EdgeInsets.all(12),itemCount:ids.length,
                itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),
                  builder:(_,p){
                    final v=p.data?.data()??<String,dynamic>{},foto=(v['photoUrl']??'').toString(),ad=(v['displayName']??v['username']??'NgelX').toString(),secili=hidden.contains(ids[i]);
                    return CheckboxListTile(
                      value:secili,
                      onChanged:(x)=>videoRef.set({'hiddenFor':x==true?FieldValue.arrayUnion([ids[i]]):FieldValue.arrayRemove([ids[i]])},SetOptions(merge:true)),
                      secondary:CircleAvatar(backgroundImage:foto.isEmpty?null:CachedNetworkImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person):null),
                      title:Text(ad,style:const TextStyle(fontWeight:FontWeight.w700)),
                      subtitle:Text('@'+(v['username']??'ngelx').toString()),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    ));
  }
}

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
  String tanitimVideoUrl = '';
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
          tanitimVideoUrl = (veri['introVideoUrl'] ?? '').toString();
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

    final secim = await showModalBottomSheet<String>(
      context: context,
      backgroundColor: Colors.white,
      showDragHandle: true,
      builder: (c) => Theme(
        data: ThemeData.light(),
        child: SafeArea(
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const ListTile(
              title: Text('Profil fotoğrafı', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w900)),
            ),
            ListTile(
              leading: const Icon(Icons.camera_alt_rounded, color: mor),
              title: const Text('Fotoğraf çek', style: TextStyle(color: Colors.black87)),
              onTap: () => Navigator.pop(c, 'camera'),
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_rounded, color: mor),
              title: const Text('Galeriden seç', style: TextStyle(color: Colors.black87)),
              onTap: () => Navigator.pop(c, 'gallery'),
            ),
            if (fotoUrl.isNotEmpty)
              ListTile(
                leading: const Icon(Icons.delete_outline_rounded, color: Colors.red),
                title: const Text('Profil fotoğrafını kaldır', style: TextStyle(color: Colors.red)),
                onTap: () => Navigator.pop(c, 'remove'),
              ),
          ]),
        ),
      ),
    );
    if (secim == null) return;
    await ngelxOverlayKapanisiniBekle();
    if (!mounted) return;

    if (secim == 'remove') {
      final eski = fotoUrl;
      setState(() => fotoYukleniyor = true);
      try {
        await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
          'photoUrl': '',
          'updatedAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true));
        if (!mounted) return;
        setState(() => fotoUrl = '');
        if (eski.isNotEmpty) {
          unawaited(ngelxMedyaSil(eski).catchError((_){ }));
        }
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Profil fotoğrafı kaldırıldı.')),
        );
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Profil fotoğrafı kaldırılamadı: $e')),
          );
        }
      } finally {
        if (mounted) setState(() => fotoYukleniyor = false);
      }
      return;
    }

    XFile? dosya;
    try {
      dosya = await ImagePicker().pickImage(
        source: secim == 'camera' ? ImageSource.camera : ImageSource.gallery,
        imageQuality: 82,
        maxWidth: 1080,
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Kamera/Galeri açılamadı: $e')),
        );
      }
      return;
    }
    if (dosya == null || !mounted) return;

    setState(() => fotoYukleniyor = true);
    try {
      final uzanti = dosya.name.contains('.')
          ? dosya.name.split('.').last.toLowerCase()
          : 'jpg';
      final yol = 'profiles/${user.uid}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      final eski = fotoUrl;
      final url = await ngelxMedyaYukleBytes(
        bytes: await dosya.readAsBytes(),
        kind: 'profiles',
        ext: uzanti,
        legacyPath: yol,
      );
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
        'photoUrl': url,
        'updatedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
      if (!mounted) return;
      setState(() => fotoUrl = url);
      if (eski.isNotEmpty && eski != url) {
        unawaited(ngelxMedyaSil(eski).catchError((_){ }));
      }
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Profil fotoğrafı kaydedildi.')),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Profil fotoğrafı yüklenemedi: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => fotoYukleniyor = false);
    }
  }

  Future<void> tanitimVideosuYukle()async{
    final user=aktifKullanici;if(user==null||user.isAnonymous)return;
    final secim=await showModalBottomSheet<String>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(leading:const Icon(Icons.video_library_outlined,color:mor),title:Text(tanitimVideoUrl.isEmpty?'Tanıtım videosu seç':'Tanıtım videosunu değiştir',style:const TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(c,'pick')),
        if(tanitimVideoUrl.isNotEmpty)ListTile(leading:const Icon(Icons.delete_outline,color:Colors.red),title:const Text('Tanıtım videosunu kaldır',style:TextStyle(color:Colors.red)),onTap:()=>Navigator.pop(c,'remove')),
      ]))),
    );
    if(secim==null)return;
    if(secim=='remove'){
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'introVideoUrl':''},SetOptions(merge:true));
      if(mounted)setState(()=>tanitimVideoUrl='');
      return;
    }
    final dosya=await ImagePicker().pickVideo(source:ImageSource.gallery,maxDuration:const Duration(seconds:30));
    if(dosya==null)return;
    if(mounted)setState(()=>fotoYukleniyor=true);
    try{
      final yol='profile-intros/'+user.uid+'/'+DateTime.now().millisecondsSinceEpoch.toString()+'.mp4';
      final url=await ngelxMedyaYukleBytes(
        bytes: await dosya.readAsBytes(),
        kind: 'profile-intros',
        ext: 'mp4',
        legacyPath: yol,
      );
      await FirebaseFirestore.instance.collection('users').doc(user.uid).set({'introVideoUrl':url,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      if(mounted){setState(()=>tanitimVideoUrl=url);ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Profil tanıtım videosu kaydedildi.')));}
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Tanıtım videosu yüklenemedi: '+e.toString())));
    }finally{if(mounted)setState(()=>fotoYukleniyor=false);}
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
      final url = await ngelxMedyaYukleBytes(
        bytes: await dosya.readAsBytes(),
        kind: 'stories',
        ext: uzanti,
        legacyPath: yol,
      );
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
    final belge = aktif.last;
    final veri = belge.data();
    Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(url:(veri['mediaUrl']??'').toString(),kullanici:kullanici,fotoUrl:fotoUrl,ownerUid:user.uid,storyId:belge.id,createdAt:veri['createdAt'],expiresAt:veri['expiresAt'])));
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
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(26)),
      ),
      builder: (ctx) {
        bool kaydediliyor = false;

        return Theme(
          data:ThemeData.light(),
          child:StatefulBuilder(
          builder: (ctx, pencereState) {
            return SafeArea(
              top:false,
              child:SingleChildScrollView(child:Padding(
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
                        const SnackBar(content: Text('Profilin güncellendi ✓')),
                      );
                    },
                  ),
                ],
              ),
            )),
            );
          },
        ));
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

  Future<void> icerikMenusu(QueryDocumentSnapshot<Map<String,dynamic>> d) async {
    final sabit=d.data()['pinned']==true;
    await showModalBottomSheet(
      context:context,backgroundColor:Colors.white,showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
      builder:(ctx)=>Theme(data:ThemeData.light(),child:SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(leading:const Icon(Icons.edit,color:mavi),title:const Text('Açıklamayı düzenle'),onTap:(){Navigator.pop(ctx);icerikDuzenle(d);}),
        ListTile(
          leading:const Icon(Icons.visibility_off_outlined,color:Colors.orange),
          title:const Text('Belirli kişilerden gizle'),
          onTap:(){Navigator.pop(ctx);Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikGizlemePage(videoId:d.id)));},
        ),
        ListTile(
          leading:Icon(sabit?Icons.push_pin:Icons.push_pin_outlined,color:mor),
          title:Text(sabit?'Sabitlemeyi kaldır':'Profilde sabitle'),
          onTap:()async{
            if(!sabit){
              final u=aktifKullanici;if(u==null)return;
              final q=await FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:u.uid).get();
              final sayi=q.docs.where((x)=>x.data()['type']!='story'&&x.data()['pinned']==true).length;
              if(sayi>=3){
                if(ctx.mounted)Navigator.pop(ctx);
                if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Profilde en fazla 3 gönderi sabitleyebilirsin.')));
                return;
              }
            }
            await d.reference.set({'pinned':!sabit,'pinnedAt':!sabit?FieldValue.serverTimestamp():null},SetOptions(merge:true));
            if(ctx.mounted)Navigator.pop(ctx);
          },
        ),
        ListTile(leading:const Icon(Icons.delete_forever,color:Colors.red),title:const Text('PAYLAŞIMI SİL',style:TextStyle(color:Colors.red,fontWeight:FontWeight.bold)),onTap:(){Navigator.pop(ctx);icerikSil(d);}),
      ]))),
    );
  }

  Future<void> icerikDuzenle(QueryDocumentSnapshot<Map<String,dynamic>> d) async {final c=TextEditingController(text:(d.data()['description']??'').toString());final ok=await showDialog<bool>(context:context,builder:(ctx)=>AlertDialog(title:const Text('Paylaşımı düzenle'),content:TextField(controller:c,maxLength:500,maxLines:4),actions:[TextButton(onPressed:()=>Navigator.pop(ctx,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(ctx,true),child:const Text('Kaydet'))]));if(ok==true)await d.reference.update({'description':c.text.trim(),'updatedAt':FieldValue.serverTimestamp()});c.dispose();}

  Future<void> icerikSil(QueryDocumentSnapshot<Map<String,dynamic>> d) async {
    await ngelxOverlayKapanisiniBekle();
    if(!mounted)return;

    final ok=await showDialog<bool>(
      context:context,
      builder:(ctx)=>AlertDialog(
        backgroundColor:Colors.white,
        surfaceTintColor:Colors.white,
        title:const Text('Bu paylaşımı silmek istiyor musun?'),
        content:const Text('Paylaşım profilinden ve akıştan tamamen kaldırılacak.'),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(ctx,false),child:const Text('Vazgeç')),
          FilledButton(
            style:FilledButton.styleFrom(backgroundColor:Colors.red),
            onPressed:()=>Navigator.pop(ctx,true),
            child:const Text('Sil'),
          ),
        ],
      ),
    )??false;
    if(!ok)return;
    await ngelxOverlayKapanisiniBekle();
    if(!mounted)return;

    try{
      final v=d.data();
      final likes=await d.reference.collection('likes').get();
      final comments=await d.reference.collection('comments').get();
      final batch=FirebaseFirestore.instance.batch();
      for(final x in likes.docs){batch.delete(x.reference);}
      for(final x in comments.docs){
        final altLikes=await x.reference.collection('likes').get();
        for(final l in altLikes.docs){batch.delete(l.reference);}
        batch.delete(x.reference);
      }
      batch.delete(d.reference);
      await batch.commit();

      for(final raw in <String>[
        (v['mediaUrl']??'').toString(),
        (v['videoUrl']??'').toString(),
        (v['audioUrl']??'').toString(),
      ]){
        if(raw.isEmpty)continue;
        unawaited(ngelxMedyaSil(raw).catchError((_){ }));
      }
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Paylaşım silindi.')),
      );
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content:Text('Paylaşım silinemedi: $e')),
      );
    }
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
                      const Spacer(),
                      IconButton(tooltip:'Profil önizleme',onPressed:aktifKullanici==null?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:aktifKullanici!.uid,ziyaretciOnizleme:true))),icon:const Icon(Icons.visibility_outlined,color:Colors.black,size:27)),
                      IconButton(onPressed:aktifKullanici==null?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>ProfilAramaPage(uid:aktifKullanici!.uid))),icon:const Icon(Icons.search_rounded,color:Colors.black,size:28)),
                      StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:aktifKullanici!.uid).limit(100).snapshots(),builder:(_,s){final sayi=(s.data?.docs??[]).where((d)=>d.data()['read']!=true).length;return IconButton(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage())),icon:sayi==0?const Icon(Icons.notifications_none_rounded,color:Colors.black,size:28):Badge(label:Text(sayi>99?'99+':'$sayi'),child:const Icon(Icons.notifications_none_rounded,color:Colors.black,size:28)));}),
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
                            backgroundImage: fotoUrl.isEmpty ? null : CachedNetworkImageProvider(fotoUrl),
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
                  StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:aktifKullanici!.uid).limit(100).snapshots(),
                    builder:(_,s){
                      final paylasimlar=(s.data?.docs??[]).where((d)=>d.data()['type']!='story');
                      final etkilesim=paylasimlar.fold<int>(0,(toplam,d){final v=d.data();return toplam+((v['likeCount'] as num?)?.toInt()??0)+((v['commentCount'] as num?)?.toInt()??0)+((v['shareCount'] as num?)?.toInt()??0);});
                      return Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
                        _beyazIstatistik('$takipSayisi','Takip',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'following',baslik:'Takip')))),
                        _beyazIstatistik('$takipciSayisi','Takipçi',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciListesiPage(uid:aktifKullanici!.uid,alan:'followers',baslik:'Takipçiler')))),
                        _beyazIstatistik('$etkilesim','Etkileşim',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>EtkilesimOzetiPage(uid:aktifKullanici!.uid)))),
                        _beyazIstatistik('$arkadasSayisi','Arkadaşlar',()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage()))),
                      ]);
                    },
                  ),
                  const SizedBox(height: 17),
                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[SizedBox(width:235,height:50,child:FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1F2F6),foregroundColor:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:duzenle,icon:const Icon(Icons.edit_outlined),label:Text(aktifKullanici?.isAnonymous==true?'Hesap Oluştur':'Profili Düzenle',style:const TextStyle(fontWeight:FontWeight.w800)))),const SizedBox(width:10),SizedBox(width:52,height:50,child:FilledButton(style:FilledButton.styleFrom(backgroundColor:const Color(0xFFF1ECFF),foregroundColor:Colors.black,padding:EdgeInsets.zero,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(17))),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ArkadaslarPage())),child:const Icon(Icons.person_add_alt_1)))]),
                  const SizedBox(height: 12),
                  SizedBox(width:double.infinity,child:OutlinedButton.icon(
                    onPressed:tanitimVideosuYukle,
                    icon:const Icon(Icons.video_camera_front_outlined),
                    label:Text(tanitimVideoUrl.isEmpty?'Profil tanıtım videosu ekle':'Tanıtım videosunu değiştir'),
                  )),
                  if(tanitimVideoUrl.isNotEmpty) ...[
                    const SizedBox(height:12),
                    ProfilTanitimVideoKarti(url:tanitimVideoUrl),
                  ],
                  const SizedBox(height: 22),
                  Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_profilKisayol(Icons.bookmark_border_rounded,'Kaydedilenler',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const KaydedilenlerPage()))),_profilKisayol(Icons.history_rounded,'Arşiv',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const HikayeArsiviPage()))),_profilKisayol(Icons.add_circle_outline_rounded,'Hikâyeler',tiklama:hikayeyiAc),_profilKisayol(Icons.event_outlined,'Etkinlikler',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const ProfilBolumuPage(baslik:'Etkinlikler',aciklama:'Yaklaşan ve katıldığın etkinlikler burada görünecek.',ikon:Icons.event_outlined)))),_profilKisayol(Icons.lock_outline_rounded,'Gizlilik',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Gizlilik')))),_profilKisayol(Icons.settings_outlined,'Ayarlar',tiklama:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarPage())))]),
                  const SizedBox(height: 20),
                  SizedBox(height:92,child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                    stream:aktifKullanici==null?null:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:aktifKullanici!.uid).limit(100).snapshots(),
                    builder:(_,hs){
                      final h=(hs.data?.docs??[]).where((d)=>d.data()['type']=='story'&&d.data()['highlighted']==true).toList()
                        ..sort((a,b){
                          final at=a.data()['createdAt'],bt=b.data()['createdAt'];
                          final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
                          return bm.compareTo(am);
                        });
                      return ListView(scrollDirection:Axis.horizontal,children:[
                        _oneCikan(Icons.add,'Yeni',hikayeYukle),
                        ...h.take(8).map((d){
                          final v=d.data(),url=(v['mediaUrl']??'').toString();
                          return Padding(
                            padding:const EdgeInsets.only(right:10),
                            child:InkWell(
                              onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>HikayeGosterPage(url:url,kullanici:kullanici,fotoUrl:fotoUrl,ownerUid:aktifKullanici?.uid??'',storyId:d.id,createdAt:v['createdAt'],expiresAt:v['expiresAt']))),
                              child:SizedBox(width:70,child:Column(children:[
                                CircleAvatar(radius:28,backgroundColor:const Color(0xFFF1E9FF),backgroundImage:url.isEmpty?null:CachedNetworkImageProvider(url),child:url.isEmpty?const Icon(Icons.auto_stories_rounded,color:mor):null),
                                const SizedBox(height:5),
                                const Text('Öne çıkan',maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:Colors.black54,fontSize:11)),
                              ])),
                            ),
                          );
                        }),
                      ]);
                    },
                  )),
                  const SizedBox(height: 14),
                  const Row(mainAxisAlignment:MainAxisAlignment.spaceAround,children:[_ProfilSekme('Gönderiler',true),_ProfilSekme('Reels',false),_ProfilSekme('Etiketlenenler',false),_ProfilSekme('Beğenilenler',false)]),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: aktifKullanici == null ? null : FirebaseFirestore.instance.collection('videos').where('ownerId', isEqualTo: aktifKullanici!.uid).limit(100).snapshots(),
              builder: (_, snap) {
                final paylasimlar = (snap.data?.docs ?? []).where((d) => d.data()['type'] != 'story').toList()
                  ..sort((a,b){
                    final ap=a.data()['pinned']==true,bp=b.data()['pinned']==true;
                    if(ap!=bp)return ap?-1:1;
                    final at=a.data()['createdAt'],bt=b.data()['createdAt'];
                    final am=at is Timestamp?at.millisecondsSinceEpoch:0,bm=bt is Timestamp?bt.millisecondsSinceEpoch:0;
                    return bm.compareTo(am);
                  });
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
                    return GestureDetector(
            onTap:()=>icerigiAc(belge),
            onLongPress:()=>icerikMenusu(belge),
            child:Stack(
              fit:StackFit.expand,
              children:[
                MedyaOnizleme(
                  tur: tur,
                  url: url,
                  thumbnailUrl: (v['thumbnailUrl'] ?? '').toString(),
                  yazi: (v['description'] ?? '').toString(),
                  arkaPlan: i.isEven ? const Color(0xFF28233F) : const Color(0xFF173036),
                ),
                Positioned(
                  left:6,
                  right:6,
                  bottom:6,
                  child:_ProfilEtkilesimRozeti(likeCount:(v['likeCount'] as num?)?.toInt()??0,commentCount:(v['commentCount'] as num?)?.toInt()??0),
                ),
              ],
            ),
          );
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

  Widget _beyazIstatistik(String sayi,String baslik,VoidCallback tiklama)=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(14),child:Padding(padding:const EdgeInsets.symmetric(horizontal:7,vertical:7),child:Column(children:[Text(sayi,style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)),Text(baslik,style:const TextStyle(color:Colors.black54))])));
  Widget _profilKisayol(IconData ikon,String yazi,{VoidCallback? tiklama})=>InkWell(onTap:tiklama,borderRadius:BorderRadius.circular(15),child:SizedBox(width:58,child:Column(children:[Container(width:48,height:48,decoration:BoxDecoration(color:const Color(0xFFF3F4F7),borderRadius:BorderRadius.circular(15)),child:Icon(ikon,color:Colors.black87)),const SizedBox(height:5),Text(yazi,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:9.4,fontWeight:FontWeight.w700))])));
  Widget _oneCikan(IconData ikon,String yazi,VoidCallback tiklama)=>Padding(padding:const EdgeInsets.only(right:13),child:InkWell(onTap:tiklama,child:Column(children:[Container(width:62,height:62,decoration:BoxDecoration(color:const Color(0xFFF1F3F7),shape:BoxShape.circle,border:Border.all(color:const Color(0xFFDDE0E7),width:2)),child:Icon(ikon,color:mor)),const SizedBox(height:5),Text(yazi,style:const TextStyle(color:Colors.black87,fontSize:11))])));
}


class _ProfilEtkilesimRozeti extends StatelessWidget {
  final int likeCount, commentCount;
  const _ProfilEtkilesimRozeti({required this.likeCount, required this.commentCount});

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
    decoration: BoxDecoration(
      color: Colors.black.withValues(alpha: .62),
      borderRadius: BorderRadius.circular(12),
    ),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.favorite_rounded, color: Colors.white, size: 15),
            const SizedBox(width: 4),
            Text('$likeCount', style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w800)),
          ],
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.mode_comment_rounded, color: Colors.white, size: 15),
            const SizedBox(width: 4),
            Text('$commentCount', style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w800)),
          ],
        ),
      ],
    ),
  );
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
                stream: FirebaseFirestore.instance.collection('users').doc(uid).collection('saved').orderBy('savedAt', descending: true).limit(100).snapshots(),
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
                        if(v.connectionState==ConnectionState.done&&v.data?.exists==false){Future.microtask(()=>docs[i].reference.delete());return const SizedBox.shrink();}
                        final veri = v.data?.data() ?? {};
                        final tur = (veri['type'] ?? 'text').toString();
                        final url = (veri['mediaUrl'] ?? veri['videoUrl'] ?? '').toString();
                        return GestureDetector(
                          onTap: () { final id=(docs[i].data()['contentId']??docs[i].id).toString(); Navigator.push(context,MaterialPageRoute(builder:(_)=>IcerikBaglantiPage(icerikId:id))); },
                          onLongPress: () => docs[i].reference.delete(),
                          child: MedyaOnizleme(tur: tur, url: url, thumbnailUrl: (veri['thumbnailUrl'] ?? '').toString(), yazi: (veri['description'] ?? '').toString(), arkaPlan: const Color(0xFFF0F1F4)),
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
  final bool koyuZemin;

  const Logo({
    super.key,
    this.kucuk = false,
    this.koyuZemin = false,
  });

  @override
  Widget build(BuildContext context) {
    if (kucuk) {
      final yaziRengi =
koyuZemin ? Colors.white : const Color(0xFF07142E);
      return SizedBox(
        height: 30,
        child: Row(
mainAxisSize: MainAxisSize.min,
children: [
  ClipRect(
    child: Align(
      alignment: Alignment.centerLeft,
      widthFactor: .47,
      child: Image.asset(
        'assets/ngelx_logo_horizontal.png',
        height: 29,
        fit: BoxFit.contain,
      ),
    ),
  ),
  const SizedBox(width: 4),
  Text.rich(
    TextSpan(
      children: [
        TextSpan(
          text: 'Ngel',
          style: TextStyle(
            color: yaziRengi,
            fontSize: 18,
            fontWeight: FontWeight.w900,
            letterSpacing: -1,
          ),
        ),
        const TextSpan(
          text: 'X',
          style: TextStyle(
            color: Color(0xFF19C7F2),
            fontSize: 19,
            fontWeight: FontWeight.w900,
            letterSpacing: -1,
          ),
        ),
      ],
    ),
  ),
],
        ),
      );
    }

    return Center(
      child: Image.asset(
        'assets/ngelx_logo.png',
        width: 165,
        height: 165,
        fit: BoxFit.contain,
      ),
    );
  }
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
