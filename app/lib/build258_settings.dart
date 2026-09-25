part of 'main.dart';

class AyarlarV258Page extends StatelessWidget{
  const AyarlarV258Page({super.key});
  Widget _baslik(String x)=>Padding(padding:const EdgeInsets.fromLTRB(12,20,12,5),child:Text(x,style:const TextStyle(color:Colors.black45,fontSize:12,fontWeight:FontWeight.w900,letterSpacing:.5)));
  Widget _satir(BuildContext c,IconData i,String a,String s,Widget p,{Color renk=mor})=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:5),
    leading:Container(width:42,height:42,alignment:Alignment.center,decoration:BoxDecoration(color:renk.withValues(alpha:.10),borderRadius:BorderRadius.circular(14)),child:Icon(i,color:renk)),
    title:Text(a,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
    subtitle:Text(s,style:const TextStyle(color:Colors.black54)),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>p)),
  );
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),
    child:Scaffold(
      appBar:AppBar(title:const Text('Ayarlar ve gizlilik')),
      body:ListView(padding:const EdgeInsets.fromLTRB(14,4,14,30),children:[
        _baslik('HESAP'),
        _satir(context,Icons.manage_accounts_outlined,'Hesap ve profil bilgileri','Ad, kullanıcı adı, e-posta, telefon, doğum tarihi ve şifre',const HesapBilgileriV258Page()),
        _satir(context,Icons.switch_account_rounded,t('switchAccount'),t('switchAccountSub'),const HesapDegistirPage()),
        _satir(context,Icons.workspace_premium_rounded,t('premiumWallet'),t('premiumWalletSub'),const NgelXPremiumPage(),renk:ngelxPremiumPurple),

        _baslik('GİZLİLİK'),
        _satir(context,Icons.lock_outline,t('privacy'),t('privacySub'),const TercihlerPage(baslik:'Gizlilik')),
        _satir(context,Icons.people_outline,t('followFriends'),t('followFriendsSub'),const ArkadaslarPage()),
        _satir(context,Icons.block_outlined,t('blockedAccounts'),t('blockedAccountsSub'),const EngellenenlerPage()),
        _satir(context,Icons.do_not_disturb_alt_rounded,'Kısıtlanan hesaplar','Engellemeden etkileşim ve bildirimleri sınırla',const KisitlananlarV258Page()),
        _satir(context,Icons.volume_off_outlined,'Sessize alınan hesaplar','Takipten çıkmadan içeriklerini azalt',const SessizeAlinanlarV258Page()),
        _satir(context,Icons.chat_bubble_outline,'Mesaj ve grup izinleri','Mesaj istekleri, grup davetleri ve okundu bilgisi',const GelismisAyarlarV258Page(tur:'mesaj')),
        _satir(context,Icons.auto_stories_outlined,t('storyPrivacy'),t('storyPrivacySub'),const TercihlerPage(baslik:'Hikâye gizliliği')),

        _baslik('İÇERİK VE ETKİLEŞİM'),
        _satir(context,Icons.tune_rounded,'İçerik ve etkileşim','Yorum, etiket, bahsetme, hassas içerik ve gizli kelimeler',const GelismisAyarlarV258Page(tur:'icerik')),
        _satir(context,Icons.video_collection_outlined,'Reels ve canlı','İndirme, yeniden paylaşım, canlı yorum ve davet izinleri',const GelismisAyarlarV258Page(tur:'reels')),
        _satir(context,Icons.download_outlined,t('downloadPermissions'),t('downloadPermissionsSub'),const TercihlerPage(baslik:'İndirme izinleri')),

        _baslik('BİLDİRİMLER'),
        _satir(context,Icons.notifications_outlined,'Bildirim tercihleri','Mesaj, arkadaşlık, etkileşim, canlı, grup ve sessiz saatler',const GelismisAyarlarV258Page(tur:'bildirim')),

        _baslik('GÜVENLİK'),
        _satir(context,Icons.security_outlined,t('accountSecurity'),t('accountSecuritySub'),const HesapGuvenligiPage()),
        _satir(context,Icons.warning_amber_rounded,'Güvenlik uyarıları','Şüpheli girişleri ve tüm cihazlardan çıkışı yönet',const GelismisAyarlarV258Page(tur:'guvenlik')),
        _satir(context,Icons.devices_outlined,t('devices'),t('devicesSub'),const GirisGecmisiPage()),
        _satir(context,Icons.health_and_safety_outlined,'Hesap kurtarma','Kurtarma e-postası, telefon ve şifre yenileme',const HesapKurtarmaPage()),

        _baslik('VERİ VE UYGULAMA'),
        _satir(context,Icons.folder_copy_outlined,'Verilerim','Verilerini dışa aktar, geçmişleri ve kaydedilenleri yönet',const VerilerimV258Page()),
        _satir(context,Icons.data_saver_on_rounded,'Veri ve depolama','Veri tasarrufu, otomatik oynatma ve Wi-Fi HD',const GelismisAyarlarV258Page(tur:'veri')),
        _satir(context,Icons.language_rounded,'Dil ve çeviri','Uygulama dili, otomatik çeviri ve altyazı dili',const GelismisAyarlarV258Page(tur:'dil')),
        _satir(context,Icons.accessibility_new_rounded,'Görünüm ve erişilebilirlik','Büyük yazı ve hareket azaltma tercihleri',const GelismisAyarlarV258Page(tur:'erisim')),

        _baslik('DESTEK VE HAKKINDA'),
        _satir(context,Icons.support_agent,t('support'),t('supportSub'),const DestekPage()),
        _satir(context,Icons.info_outline_rounded,'NgelX hakkında','Topluluk kuralları, gizlilik, koşullar ve sürüm bilgisi',const NgelXHakkindaV258Page()),

        const Divider(height:28),
        ListTile(leading:const Icon(Icons.system_update,color:mor),title:Text(t('appUpdates')),subtitle:Text('v$ngelxVersionName • ${t("build")} $ngelxBuildNumber'),trailing:const Icon(Icons.system_update_alt_rounded,color:Colors.green)),
        ListTile(leading:const Icon(Icons.share,color:mavi),title:Text(t('shareNgelx')),subtitle:Text(t('shareNgelxSub')),onTap:()async=>SharePlus.instance.share(ShareParams(text:'Ngel X ile dünyanı paylaş ✨\nhttps://ngelx.app'))),
        const Divider(),
        ListTile(leading:const Icon(Icons.logout,color:Colors.red),title:Text(t('logout'),style:const TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),onTap:()async{
          final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:Text(t('logoutQuestion')),content:Text(t('logoutInfo')),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:Text(t('cancel'))),FilledButton(onPressed:()=>Navigator.pop(c,true),child:Text(t('logout')))]));
          if(ok==true){try{await FirebaseAuth.instance.signOut().timeout(const Duration(seconds:8));ngelxKokRotayaDon();}on TimeoutException{if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Çıkış zaman aşımına uğradı. Tekrar dene.')));}catch(e){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Çıkış yapılamadı: $e')));}}
        }),
      ]),
    ),
  );
}

class HesapBilgileriV258Page extends StatefulWidget{
  const HesapBilgileriV258Page({super.key});
  @override State<HesapBilgileriV258Page> createState()=>_HesapBilgileriV258PageState();
}
class _HesapBilgileriV258PageState extends State<HesapBilgileriV258Page>{
  final ad=TextEditingController(),kullanici=TextEditingController(),bio=TextEditingController(),telefon=TextEditingController(),dogum=TextEditingController();
  bool yukleniyor=true,kaydediliyor=false;
  @override void initState(){super.initState();_yukle();}
  @override void dispose(){ad.dispose();kullanici.dispose();bio.dispose();telefon.dispose();dogum.dispose();super.dispose();}
  Future<void> _yukle()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null){if(mounted)setState(()=>yukleniyor=false);return;}
    try{final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get(),v=d.data()??<String,dynamic>{};ad.text=(v['displayName']??u.displayName??'').toString();kullanici.text=(v['username']??'').toString();bio.text=(v['bio']??'').toString();telefon.text=(v['phone']??v['phoneNumber']??'').toString();dogum.text=(v['birthDate']??'').toString();}
    finally{if(mounted)setState(()=>yukleniyor=false);}
  }
  Future<void> _kaydet()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null||kaydediliyor)return;
    final a=ad.text.trim(),k=kullanici.text.trim().toLowerCase().replaceFirst('@','');
    if(a.length<2||!RegExp(r'^[a-z0-9_.]{3,30}$').hasMatch(k)){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Adı ve kullanıcı adını kontrol et.')));return;}
    setState(()=>kaydediliyor=true);
    try{
      final q=await FirebaseFirestore.instance.collection('users').where('username',isEqualTo:k).limit(2).get().timeout(const Duration(seconds:10));
      if(q.docs.any((x)=>x.id!=u.uid)){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu kullanıcı adı kullanılıyor.')));return;}
      await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'displayName':a,'username':k,'bio':bio.text.trim(),'phone':telefon.text.trim(),'birthDate':dogum.text.trim(),'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).timeout(const Duration(seconds:12));
      try{await u.updateDisplayName(a);}catch(_){}
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Hesap bilgileri kaydedildi ✅')));
    }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Kaydedilemedi: $e')));}
    finally{if(mounted)setState(()=>kaydediliyor=false);}
  }
  Future<void> _sifre()async{final e=FirebaseAuth.instance.currentUser?.email;if(e==null)return;try{await FirebaseAuth.instance.sendPasswordResetEmail(email:e);if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Şifre değiştirme bağlantısı e-postana gönderildi.')));}catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Bağlantı gönderilemedi: $e')));}}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none))),child:Scaffold(
    appBar:AppBar(title:const Text('Hesap ve profil bilgileri')),
    body:yukleniyor?const Center(child:CircularProgressIndicator(color:mor)):ListView(padding:const EdgeInsets.all(20),children:[
      TextField(controller:ad,maxLength:50,decoration:const InputDecoration(labelText:'Ad ve soyad',prefixIcon:Icon(Icons.badge_outlined))),
      TextField(controller:kullanici,maxLength:30,autocorrect:false,enableSuggestions:false,decoration:const InputDecoration(labelText:'Kullanıcı adı',prefixText:'@',prefixIcon:Icon(Icons.alternate_email))),
      TextField(controller:bio,maxLines:3,maxLength:160,decoration:const InputDecoration(labelText:'Biyografi',prefixIcon:Icon(Icons.notes_rounded))),
      TextField(enabled:false,decoration:InputDecoration(labelText:'E-posta',prefixIcon:const Icon(Icons.email_outlined),hintText:FirebaseAuth.instance.currentUser?.email??'')),
      TextField(controller:telefon,keyboardType:TextInputType.phone,decoration:const InputDecoration(labelText:'Telefon',prefixIcon:Icon(Icons.phone_outlined))),
      TextField(controller:dogum,inputFormatters:const [NgelXBirthDateFormatter()],keyboardType:TextInputType.number,decoration:const InputDecoration(labelText:'Doğum tarihi',hintText:'GG/AA/YYYY',prefixIcon:Icon(Icons.cake_outlined))),
      const SizedBox(height:14),
      FilledButton.icon(onPressed:kaydediliyor?null:_kaydet,icon:const Icon(Icons.save_outlined),label:Text(kaydediliyor?'Kaydediliyor...':'Değişiklikleri kaydet')),
      OutlinedButton.icon(onPressed:_sifre,icon:const Icon(Icons.lock_reset_rounded),label:const Text('Şifremi değiştir')),
      OutlinedButton.icon(onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const HesapKurtarmaPage())),icon:const Icon(Icons.health_and_safety_outlined),label:const Text('Hesap kurtarma seçenekleri')),
    ]),
  ));
}

class KisitlananlarV258Page extends StatefulWidget{
  const KisitlananlarV258Page({super.key});
  @override State<KisitlananlarV258Page> createState()=>_KisitlananlarV258PageState();
}
class _KisitlananlarV258PageState extends State<KisitlananlarV258Page>{
  Future<List<String>> _getir()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return[];final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();return List<String>.from(d.data()?['restrictedUsers']??const[]);}
  Future<void> _kaldir(String id)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'restrictedUsers':FieldValue.arrayRemove([id])},SetOptions(merge:true));if(mounted)setState((){});}
  @override Widget build(BuildContext context)=>_NgelXUserArrayPage(
    baslik:'Kısıtlanan hesaplar',alan:'restrictedUsers',bosMetin:'Kısıtladığın hesap yok.',
    trailing:(id)=>TextButton(onPressed:()=>_kaldir(id),child:const Text('Kaldır')),
  );
}

class SessizeAlinanlarV258Page extends StatefulWidget{
  const SessizeAlinanlarV258Page({super.key});
  @override State<SessizeAlinanlarV258Page> createState()=>_SessizeAlinanlarV258PageState();
}
class _SessizeAlinanlarV258PageState extends State<SessizeAlinanlarV258Page>{
  Future<void> _kaldir(String id)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'mutedUsers':FieldValue.arrayRemove([id])},SetOptions(merge:true));if(mounted)setState((){});}
  @override Widget build(BuildContext context)=>_NgelXUserArrayPage(
    baslik:'Sessize alınan hesaplar',alan:'mutedUsers',bosMetin:'Sessize aldığın hesap yok.',
    trailing:(id)=>TextButton(onPressed:()=>_kaldir(id),child:const Text('Sesi aç')),
  );
}

class _NgelXUserArrayPage extends StatefulWidget{
  final String baslik,alan,bosMetin;
  final Widget Function(String id) trailing;
  const _NgelXUserArrayPage({required this.baslik,required this.alan,required this.bosMetin,required this.trailing});
  @override State<_NgelXUserArrayPage> createState()=>_NgelXUserArrayPageState();
}
class _NgelXUserArrayPageState extends State<_NgelXUserArrayPage>{
  Future<List<String>> _ids()async{final u=FirebaseAuth.instance.currentUser;if(u==null)return[];final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();return List<String>.from(d.data()?[widget.alan]??const[]);}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:Text(widget.baslik)),body:FutureBuilder<List<String>>(future:_ids(),builder:(_,s){
    if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
    final ids=s.data??[];if(ids.isEmpty)return Center(child:Text(widget.bosMetin,style:const TextStyle(color:Colors.black54)));
    return ListView.builder(itemCount:ids.length,itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),builder:(_,u){final v=u.data?.data()??{},f=(v['photoUrl']??'').toString();return ListTile(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:ids[i]))),leading:CircleAvatar(backgroundImage:f.isEmpty?null:CachedNetworkImageProvider(f),child:f.isEmpty?const Icon(Icons.person):null),title:Text((v['displayName']??v['username']??'NgelX').toString()),subtitle:Text('@${v['username']??'ngelx'}'),trailing:widget.trailing(ids[i]));}));
  })));
}

class GelismisAyarlarV258Page extends StatefulWidget{
  final String tur;
  const GelismisAyarlarV258Page({super.key,required this.tur});
  @override State<GelismisAyarlarV258Page> createState()=>_GelismisAyarlarV258PageState();
}
class _GelismisAyarlarV258PageState extends State<GelismisAyarlarV258Page>{
  bool mesajIstek=true,grupDavet=true,okundu=true,etiketOnay=false,uygunsuzFiltre=true;
  bool reelsIndir=true,reelsPaylas=true,canliYorum=true,canliDavet=true;
  bool bildirim=true,mesajBildirim=true,arkadasBildirim=true,etkilesimBildirim=true,canliBildirim=true,grupBildirim=true,sessizSaat=false;
  bool supheliGiris=true,veriTasarruf=false,otomatikOynat=true,wifiHd=false,otomatikCeviri=true,hareketAzalt=false,buyukYazi=false;
  String bahsetme='all',etiket='all',hassas='standard',altyazi='tr';
  String? get uid=>FirebaseAuth.instance.currentUser?.uid;
  @override void initState(){super.initState();_yukle();}
  Future<void> _yukle()async{
    if(uid==null)return;final d=await FirebaseFirestore.instance.collection('users').doc(uid).get(),v=d.data()??<String,dynamic>{};if(!mounted)return;
    setState((){
      mesajIstek=v['allowMessageRequests']!=false;grupDavet=v['allowGroupInvites']!=false;okundu=v['globalReadReceipts']!=false;
      etiketOnay=v['reviewTagsBeforeProfile']==true;uygunsuzFiltre=v['offensiveCommentFilter']!=false;bahsetme=(v['mentionPermission']??'all').toString();etiket=(v['tagPermission']??'all').toString();hassas=(v['sensitiveContentLevel']??'standard').toString();
      reelsIndir=v['allowReelsDownload']!=false;reelsPaylas=v['allowReelsReshare']!=false;canliYorum=v['allowLiveComments']!=false;canliDavet=v['allowLiveInvites']!=false;
      bildirim=v['notificationsEnabled']!=false;mesajBildirim=v['messageNotifications']!=false;arkadasBildirim=v['friendNotifications']!=false;etkilesimBildirim=v['interactionNotifications']!=false;canliBildirim=v['liveNotifications']!=false;grupBildirim=v['groupNotifications']!=false;sessizSaat=v['quietHoursEnabled']==true;
      supheliGiris=v['suspiciousLoginAlerts']!=false;veriTasarruf=v['dataSaver']==true;otomatikOynat=v['autoplayVideos']!=false;wifiHd=v['wifiOnlyHd']==true;otomatikCeviri=v['autoTranslate']!=false;altyazi=(v['captionLanguage']??uygulamaDili.value).toString();hareketAzalt=v['reduceMotion']==true;buyukYazi=v['largeText']==true;
    });
  }
  Future<void> _bool(String k,bool v)async{if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));}
  Future<void> _str(String k,String v)async{if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));}
  Widget _sw(String a,String s,bool v,ValueChanged<bool> f,{bool enabled=true})=>SwitchListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20,vertical:5),title:Text(a,style:const TextStyle(fontWeight:FontWeight.w700)),subtitle:Text(s),value:v,onChanged:enabled?f:null,activeTrackColor:mavi);
  Widget _h(String x)=>Padding(padding:const EdgeInsets.fromLTRB(20,18,20,5),child:Text(x,style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w900)));
  List<Widget> _izin(String alan,String secili,ValueChanged<String> f)=>const [('all','Herkes'),('following','Takip ettiklerim'),('friends','Arkadaşlar'),('none','Kimse')].map((e)=>RadioListTile<String>(value:e.$1,groupValue:secili,title:Text(e.$2),onChanged:(v){if(v!=null){f(v);}})).toList();
  String get _baslik=>switch(widget.tur){'mesaj'=>'Mesaj ve grup izinleri','icerik'=>'İçerik ve etkileşim','reels'=>'Reels ve canlı','bildirim'=>'Bildirim tercihleri','guvenlik'=>'Güvenlik uyarıları','veri'=>'Veri ve depolama','dil'=>'Dil ve çeviri','erisim'=>'Görünüm ve erişilebilirlik',_=>'Ayarlar'};

  Future<void> _dilSec()async{
    final sec=await showModalBottomSheet<String>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:dilAdlari.entries.map((e)=>ListTile(leading:uygulamaDili.value==e.key?const Icon(Icons.check_circle,color:mor):const Icon(Icons.language),title:Text(e.value),onTap:()=>Navigator.pop(c,e.key))).toList())));
    if(sec!=null){await diliDegistir(sec);if(mounted)setState((){});}
  }
  Future<void> _tumCihazlardanCik()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Tüm cihazlardan çıkış yapılsın mı?'),content:const Text('NgelX açık olan diğer cihazlara çıkış talimatı gönderilecek ve bu cihazdaki oturum da kapanacak.'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Tümünden çık'))]))??false;
    if(!ok)return;
    final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get(),ham=List<dynamic>.from(d.data()?['loginHistory']??const[]),ids=ham.whereType<Map>().map((x)=>(x['deviceId']??'').toString()).where((x)=>x.isNotEmpty).toSet().toList();
    await FirebaseFirestore.instance.collection('users').doc(u.uid).set({'revokedDeviceIds':FieldValue.arrayUnion(ids),'allSessionsRevokedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    await FirebaseAuth.instance.signOut().timeout(const Duration(seconds:8));
    ngelxKokRotayaDon();
  }

  List<Widget> get _icerik{
    switch(widget.tur){
      case 'mesaj':
        return [
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.chat_bubble_outline,color:mor),title:const Text('Kim mesaj atabilir?',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:const Text('Herkes / Takip ettiklerim / Arkadaşlar / Kimse'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Mesaj izinleri')))),
          _sw('Mesaj istekleri','Takip etmediğin kişiler mesaj isteği gönderebilir',mesajIstek,(v){setState(()=>mesajIstek=v);_bool('allowMessageRequests',v);}),
          _sw('Grup davetleri','Diğer kullanıcılar seni gruplara davet edebilir',grupDavet,(v){setState(()=>grupDavet=v);_bool('allowGroupInvites',v);}),
          _sw('Okundu bilgisi','Mesajları okuduğunda Görüldü bilgisi gösterilir',okundu,(v){setState(()=>okundu=v);_bool('globalReadReceipts',v);}),
        ];
      case 'icerik':
        return [
          _h('Kim senden bahsedebilir?'),
          ..._izin('mentionPermission',bahsetme,(v){setState(()=>bahsetme=v);_str('mentionPermission',v);}),
          _h('Kim seni etiketleyebilir?'),
          ..._izin('tagPermission',etiket,(v){setState(()=>etiket=v);_str('tagPermission',v);}),
          _sw('Etiketleri önce onayla','Etiketlenen içerik profilinde görünmeden önce onay iste',etiketOnay,(v){setState(()=>etiketOnay=v);_bool('reviewTagsBeforeProfile',v);}),
          _sw('Uygunsuz yorum filtresi','Saldırgan ifadeleri otomatik gizlemeye yardımcı olur',uygunsuzFiltre,(v){setState(()=>uygunsuzFiltre=v);_bool('offensiveCommentFilter',v);}),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.visibility_off_outlined,color:mor),title:const Text('Gizli kelimeler'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const TercihlerPage(baslik:'Gizlilik')))),
          _h('Hassas içerik seviyesi'),
          for(final e in const [('less','Daha az'),('standard','Standart'),('more','Daha fazla')])RadioListTile<String>(value:e.$1,groupValue:hassas,title:Text(e.$2),onChanged:(v){if(v!=null){setState(()=>hassas=v);_str('sensitiveContentLevel',v);}}),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.restart_alt_rounded,color:mor),title:const Text('“İlgilenmiyorum” geçmişini temizle'),onTap:()async{if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({'notInterestedIds':<String>[]},SetOptions(merge:true));if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Geçmiş temizlendi.')));}),
        ];
      case 'reels':
        return [
          _sw('Reels indirilebilsin','Yeni Reels paylaşımlarında indirmeye izin ver',reelsIndir,(v){setState(()=>reelsIndir=v);_bool('allowReelsDownload',v);}),
          _sw('Reels yeniden paylaşılabilsin','İçeriklerinin yeniden paylaşılmasına izin ver',reelsPaylas,(v){setState(()=>reelsPaylas=v);_bool('allowReelsReshare',v);}),
          const Divider(),
          _sw('Canlı yayın yorumları','Canlı yayınlarında izleyiciler yorum yapabilsin',canliYorum,(v){setState(()=>canliYorum=v);_bool('allowLiveComments',v);}),
          _sw('Canlı yayın davetleri','Diğer kullanıcılar canlı yayına davet gönderebilsin',canliDavet,(v){setState(()=>canliDavet=v);_bool('allowLiveInvites',v);}),
        ];
      case 'bildirim':
        return [
          _sw('Tüm bildirimler','Uygulama bildirimlerini aç veya kapat',bildirim,(v){setState(()=>bildirim=v);_bool('notificationsEnabled',v);}),
          const Divider(),
          _sw('Mesajlar','Yeni mesaj bildirimleri',mesajBildirim,(v){setState(()=>mesajBildirim=v);_bool('messageNotifications',v);},enabled:bildirim),
          _sw('Arkadaşlık ve takip','İstek ve kabul bildirimleri',arkadasBildirim,(v){setState(()=>arkadasBildirim=v);_bool('friendNotifications',v);},enabled:bildirim),
          _sw('Beğeni ve yorumlar','Paylaşımlarındaki etkileşimler',etkilesimBildirim,(v){setState(()=>etkilesimBildirim=v);_bool('interactionNotifications',v);},enabled:bildirim),
          _sw('Canlı yayınlar','Takip ettiğin hesapların canlı yayınları',canliBildirim,(v){setState(()=>canliBildirim=v);_bool('liveNotifications',v);},enabled:bildirim),
          _sw('Gruplar','Grup etkinlikleri ve davetler',grupBildirim,(v){setState(()=>grupBildirim=v);_bool('groupNotifications',v);},enabled:bildirim),
          _sw('Sessiz saatler','22:00–08:00 arasında sesli bildirimleri azalt',sessizSaat,(v){setState(()=>sessizSaat=v);_bool('quietHoursEnabled',v);},enabled:bildirim),
        ];
      case 'guvenlik':
        return [
          _sw('Şüpheli giriş uyarıları','Yeni veya alışılmadık bir cihaz algılandığında uyarı oluştur',supheliGiris,(v){setState(()=>supheliGiris=v);_bool('suspiciousLoginAlerts',v);}),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.devices_outlined,color:mor),title:const Text('Giriş yapılan cihazlar',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:const Text('Aktif cihazları gör ve uzaktan çıkış yap'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GirisGecmisiPage()))),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.health_and_safety_outlined,color:mor),title:const Text('Hesap kurtarma'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const HesapKurtarmaPage()))),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.logout_rounded,color:Colors.red),title:const Text('Tüm cihazlardan çıkış yap',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),onTap:_tumCihazlardanCik),
        ];
      case 'veri':
        return [
          _sw('Veri tasarrufu','Mobil veride daha düşük veri tüketimi kullan',veriTasarruf,(v){setState(()=>veriTasarruf=v);_bool('dataSaver',v);}),
          _sw('Videoları otomatik oynat','Akışta videolar görünür olduğunda otomatik başlat',otomatikOynat,(v){setState(()=>otomatikOynat=v);_bool('autoplayVideos',v);}),
          _sw('HD yalnızca Wi‑Fi ile','HD medyayı mobil veride sınırla',wifiHd,(v){setState(()=>wifiHd=v);_bool('wifiOnlyHd',v);}),
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.folder_copy_outlined,color:mor),title:const Text('Verilerim'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const VerilerimV258Page()))),
        ];
      case 'dil':
        return [
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.language,color:mor),title:const Text('Uygulama dili',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:Text(dilAdlari[uygulamaDili.value]??uygulamaDili.value),trailing:const Icon(Icons.chevron_right),onTap:_dilSec),
          _sw('Otomatik gönderi çevirisi','Farklı dillerdeki metinler için çeviri seçeneğini göster',otomatikCeviri,(v){setState(()=>otomatikCeviri=v);_bool('autoTranslate',v);}),
          _h('Varsayılan altyazı dili'),
          for(final e in dilAdlari.entries)RadioListTile<String>(value:e.key,groupValue:altyazi,title:Text(e.value),onChanged:(v){if(v!=null){setState(()=>altyazi=v);_str('captionLanguage',v);}}),
        ];
      case 'erisim':
        return [
          _sw('Hareketleri azalt','Yoğun animasyon ve geçişleri azaltmayı tercih et',hareketAzalt,(v){setState(()=>hareketAzalt=v);_bool('reduceMotion',v);}),
          _sw('Daha büyük yazı','NgelX arayüzünde daha büyük metin tercih et',buyukYazi,(v){setState(()=>buyukYazi=v);_bool('largeText',v);}),
        ];
      default:return const [ListTile(title:Text('Ayar bulunamadı.'))];
    }
  }
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:Text(_baslik)),body:ListView(children:_icerik)));
}

class VerilerimV258Page extends StatefulWidget{
  const VerilerimV258Page({super.key});
  @override State<VerilerimV258Page> createState()=>_VerilerimV258PageState();
}
class _VerilerimV258PageState extends State<VerilerimV258Page>{
  bool aktar=false;
  dynamic _temiz(dynamic v){if(v is Timestamp)return v.toDate().toUtc().toIso8601String();if(v is DateTime)return v.toUtc().toIso8601String();if(v is Map)return v.map((k,e)=>MapEntry(k.toString(),_temiz(e)));if(v is Iterable)return v.map(_temiz).toList();return v;}
  Future<void> _disa()async{
    final u=FirebaseAuth.instance.currentUser;if(u==null||aktar)return;setState(()=>aktar=true);
    try{
      final p=await FirebaseFirestore.instance.collection('users').doc(u.uid).get(),g=await FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:u.uid).limit(500).get(),dir=await getApplicationDocumentsDirectory();
      final f=File('${dir.path}/ngelx_verilerim_${DateTime.now().millisecondsSinceEpoch}.json');
      await f.writeAsString(const JsonEncoder.withIndent('  ').convert({'exportedAt':DateTime.now().toUtc().toIso8601String(),'account':_temiz(p.data()??{}),'posts':g.docs.map((x)=>{'id':x.id,'data':_temiz(x.data())}).toList()}));
      await SharePlus.instance.share(ShareParams(files:[XFile(f.path)],text:'NgelX verilerim'));
    }catch(e){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Veriler hazırlanamadı: $e')));}
    finally{if(mounted)setState(()=>aktar=false);}
  }
  Future<void> _sil(String alan,String ad)async{final u=FirebaseAuth.instance.currentUser;if(u==null)return;await FirebaseFirestore.instance.collection('users').doc(u.uid).set({alan:<dynamic>[]},SetOptions(merge:true));if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('$ad temizlendi.')));}
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Verilerim')),body:ListView(padding:const EdgeInsets.all(18),children:[
    ListTile(leading:const Icon(Icons.download_rounded,color:mor),title:const Text('NgelX verilerimi dışa aktar',style:TextStyle(fontWeight:FontWeight.w800)),subtitle:const Text('Profil bilgilerin ve kendi paylaşımların JSON dosyası olarak hazırlanır.'),trailing:aktar?const SizedBox(width:22,height:22,child:CircularProgressIndicator(strokeWidth:2)):const Icon(Icons.chevron_right),onTap:aktar?null:_disa),
    const Divider(),
    ListTile(leading:const Icon(Icons.search_rounded,color:mor),title:const Text('Arama geçmişini temizle'),onTap:()=>_sil('searchHistory','Arama geçmişi')),
    ListTile(leading:const Icon(Icons.play_circle_outline,color:mor),title:const Text('İzleme geçmişini temizle'),onTap:()=>_sil('watchHistory','İzleme geçmişi')),
    ListTile(leading:const Icon(Icons.bookmark_border,color:mor),title:const Text('Kaydedilenler'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const KaydedilenlerPage()))),
    ListTile(leading:const Icon(Icons.devices_outlined,color:mor),title:const Text('Hesap hareketleri ve cihazlar'),trailing:const Icon(Icons.chevron_right),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const GirisGecmisiPage()))),
  ])));
}

class NgelXHakkindaV258Page extends StatelessWidget{
  const NgelXHakkindaV258Page({super.key});
  Future<void> _m(BuildContext c,String a,String b)=>showDialog<void>(context:c,builder:(x)=>AlertDialog(title:Text(a),content:Text(b),actions:[TextButton(onPressed:()=>Navigator.pop(x),child:const Text('Kapat'))]));
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('NgelX hakkında')),body:ListView(padding:const EdgeInsets.all(18),children:[
    const Center(child:Logo(kucuk:true)),const SizedBox(height:8),Center(child:Text('v$ngelxVersionName • Yapı $ngelxBuildNumber',style:const TextStyle(color:Colors.black54))),const Divider(height:30),
    ListTile(title:const Text('Topluluk kuralları'),trailing:const Icon(Icons.chevron_right),onTap:()=>_m(context,'Topluluk kuralları','Taciz, tehdit, dolandırıcılık, yasa dışı içerik ve mahremiyet ihlallerine izin verilmez.')),
    ListTile(title:const Text('Gizlilik özeti'),trailing:const Icon(Icons.chevron_right),onTap:()=>_m(context,'Gizlilik','Görünürlük, mesaj, hikâye, etiket ve etkinlik tercihlerini Ayarlar ve gizlilik bölümünden yönetebilirsin.')),
    ListTile(title:const Text('Kullanım koşulları'),trailing:const Icon(Icons.chevron_right),onTap:()=>_m(context,'Kullanım koşulları','NgelX kullanırken yürürlükteki yasalara, topluluk kurallarına ve başkalarının haklarına uymalısın.')),
    ListTile(title:const Text('Telif hakkı'),trailing:const Icon(Icons.chevron_right),onTap:()=>_m(context,'Telif hakkı','Yalnızca paylaşma hakkına sahip olduğun içerikleri yüklemelisin.')),
    ListTile(title:const Text('Açık kaynak lisansları'),trailing:const Icon(Icons.chevron_right),onTap:()=>showLicensePage(context:context,applicationName:'NgelX',applicationVersion:'$ngelxVersionName+$ngelxBuildNumber')),
  ])));
}
