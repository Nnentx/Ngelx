part of 'main.dart';

class _NgelXAyarOgesi{
  final String bolum,baslik,aciklama,anahtarlar;
  final IconData ikon;
  final Color renk;
  final WidgetBuilder sayfa;
  final bool anaListede;
  const _NgelXAyarOgesi({
    required this.bolum,
    required this.baslik,
    required this.aciklama,
    required this.ikon,
    required this.sayfa,
    this.anahtarlar='',
    this.renk=mor,
    this.anaListede=true,
  });
}

class AyarlarV258Page extends StatefulWidget{
  const AyarlarV258Page({super.key});
  @override State<AyarlarV258Page> createState()=>_AyarlarV258PageState();
}

class _AyarlarV258PageState extends State<AyarlarV258Page>{
  final arama=TextEditingController();
  String sorgu='';

  @override void dispose(){arama.dispose();super.dispose();}

  String _normalize(String x)=>x
      .replaceAll('İ','i').replaceAll('I','i').replaceAll('ı','i')
      .replaceAll('Ş','s').replaceAll('ş','s')
      .replaceAll('Ç','c').replaceAll('ç','c')
      .replaceAll('Ğ','g').replaceAll('ğ','g')
      .replaceAll('Ö','o').replaceAll('ö','o')
      .replaceAll('Ü','u').replaceAll('ü','u')
      .toLowerCase()
      .trim();

  Widget _baslik(String x)=>Padding(
    padding:const EdgeInsets.fromLTRB(12,20,12,6),
    child:Text(x,style:const TextStyle(color:Colors.black45,fontSize:12,fontWeight:FontWeight.w900,letterSpacing:.5)),
  );

  Widget _satir(BuildContext c,_NgelXAyarOgesi e,{bool aramaSonucu=false})=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:5),
    leading:Container(
      width:42,height:42,alignment:Alignment.center,
      decoration:BoxDecoration(color:e.renk.withValues(alpha:.10),borderRadius:BorderRadius.circular(14)),
      child:Icon(e.ikon,color:e.renk),
    ),
    title:Text(e.baslik,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
    subtitle:Text(
      aramaSonucu?'${e.bolum} • ${e.aciklama}':e.aciklama,
      style:const TextStyle(color:Colors.black54),
    ),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:e.sayfa)),
  );

  List<_NgelXAyarOgesi> _ogeler()=>[
    _NgelXAyarOgesi(
      bolum:'HESAP',baslik:'Hesap ve profil bilgileri',
      aciklama:'Ad, kullanıcı adı, e-posta, telefon, doğum tarihi ve şifre',
      anahtarlar:'profil ad soyad kullanıcı eposta email telefon doğum şifre parola hesap',
      ikon:Icons.manage_accounts_outlined,sayfa:(_)=>const HesapBilgileriV258Page(),
    ),
    _NgelXAyarOgesi(
      bolum:'HESAP',baslik:t('switchAccount'),aciklama:t('switchAccountSub'),
      anahtarlar:'hesap değiştir ekle çoklu hesap oturum',
      ikon:Icons.switch_account_rounded,sayfa:(_)=>const HesapDegistirPage(),
    ),
    _NgelXAyarOgesi(
      bolum:'HESAP',baslik:t('premiumWallet'),aciklama:t('premiumWalletSub'),
      anahtarlar:'premium cüzdan jeton mavi tik doğrulama satın alma ödeme',
      ikon:Icons.workspace_premium_rounded,renk:ngelxPremiumPurple,sayfa:(_)=>const NgelXPremiumPage(),
    ),

    _NgelXAyarOgesi(
      bolum:'GİZLİLİK VE GÜVENLİK',baslik:'Gizlilik',
      aciklama:'Profil, paylaşımlar, hikâyeler ve görünürlük tercihleri',
      anahtarlar:'gizlilik profil kim görür yorum hikaye ekran görüntüsü paylaşım görünürlük',
      ikon:Icons.lock_outline,sayfa:(_)=>const GizlilikMerkeziV366Page(),
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK VE GÜVENLİK',baslik:t('followFriends'),aciklama:t('followFriendsSub'),
      anahtarlar:'takip arkadaş arkadaşlık istek kabul reddet takipçi kaldır',
      ikon:Icons.people_outline,sayfa:(_)=>const ArkadaslarPage(),
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK VE GÜVENLİK',baslik:'Mesajlar ve iletişim',
      aciklama:'Kim yazabilir, mesaj istekleri, grup davetleri ve okundu bilgisi',
      anahtarlar:'mesaj kim yazabilir iletişim mesaj isteği grup daveti okundu görüldü izin',
      ikon:Icons.chat_bubble_outline,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'mesaj'),
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK VE GÜVENLİK',baslik:'Engellenen ve kısıtlanan hesaplar',
      aciklama:'Engellediğin veya etkileşimini sınırlandırdığın kişileri yönet',
      anahtarlar:'engelle engellenen kısıtla kısıtlanan kişi hesap kaldır',
      ikon:Icons.block_outlined,sayfa:(_)=>const EngellenenKisitlananV366Page(),
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK VE GÜVENLİK',baslik:'Güvenlik ve cihazlar',
      aciklama:'Şüpheli girişler, cihazlar, hesap kurtarma ve hesap işlemleri',
      anahtarlar:'güvenlik cihaz giriş şüpheli oturum kurtarma telefon eposta dondur sil',
      ikon:Icons.security_outlined,sayfa:(_)=>const GuvenlikMerkeziV366Page(),
    ),

    _NgelXAyarOgesi(
      bolum:'BİLDİRİMLER',baslik:'Bildirimler',
      aciklama:'Mesaj, arkadaşlık, etkileşim, canlı ve grup bildirimleri',
      anahtarlar:'bildirim mesaj arkadaş takip beğeni yorum canlı grup sessiz saat',
      ikon:Icons.notifications_outlined,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'bildirim'),
    ),

    _NgelXAyarOgesi(
      bolum:'İÇERİK VE MEDYA',baslik:'İçerik ve etkileşim',
      aciklama:'Yorum, etiket, bahsetme, hassas içerik ve gizli kelimeler',
      anahtarlar:'yorum etiket bahsetme hassas içerik gizli kelime filtre ilgilenmiyorum',
      ikon:Icons.tune_rounded,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'icerik'),
    ),
    _NgelXAyarOgesi(
      bolum:'İÇERİK VE MEDYA',baslik:'Medya, veri ve indirme',
      aciklama:'Reels, canlı, indirme, veri tasarrufu ve depolama seçenekleri',
      anahtarlar:'reels canlı indirme indir veri depolama wifi hd otomatik oynatma verilerim',
      ikon:Icons.video_collection_outlined,sayfa:(_)=>const MedyaVeriV366Page(),
    ),

    _NgelXAyarOgesi(
      bolum:'UYGULAMA',baslik:'Dil, çeviri ve görünüm',
      aciklama:'Uygulama dili, çeviri, altyazı ve erişilebilirlik',
      anahtarlar:'dil çeviri altyazı görünüm erişilebilirlik büyük yazı hareket',
      ikon:Icons.language_rounded,sayfa:(_)=>const UygulamaTercihleriV366Page(),
    ),
    _NgelXAyarOgesi(
      bolum:'UYGULAMA',baslik:'NgelX hakkında',
      aciklama:'Topluluk kuralları, koşullar, gizlilik ve sürüm bilgisi',
      anahtarlar:'hakkında sürüm build güncelleme topluluk kural koşul gizlilik politika',
      ikon:Icons.info_outline_rounded,sayfa:(_)=>const NgelXHakkindaV258Page(),
    ),

    _NgelXAyarOgesi(
      bolum:'YARDIM',baslik:t('support'),aciklama:t('supportSub'),
      anahtarlar:'destek yardım hata bildir sorun ekran görüntüsü iletişim',
      ikon:Icons.support_agent,sayfa:(_)=>const DestekPage(),
    ),

    _NgelXAyarOgesi(
      bolum:'GİZLİLİK',baslik:'Hikâye gizliliği',aciklama:'Hikâyeyi kim görebilir ve ekran görüntüsü seçenekleri',
      anahtarlar:'story hikaye gizlilik ekran görüntüsü',
      ikon:Icons.auto_stories_outlined,sayfa:(_)=>const TercihlerPage(baslik:'Hikâye gizliliği'),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK',baslik:'Mesaj gizliliği',aciklama:'Kim bana mesaj atabilir?',
      anahtarlar:'mesaj izin kim yazabilir herkes takip arkadaş kimse',
      ikon:Icons.forum_outlined,sayfa:(_)=>const TercihlerPage(baslik:'Mesaj izinleri'),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK',baslik:'Engellenen hesaplar',aciklama:'Engellediğin kişileri gör ve engeli kaldır',
      anahtarlar:'block engel engellenen kaldır',
      ikon:Icons.block_rounded,sayfa:(_)=>const EngellenenlerPage(),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'GİZLİLİK',baslik:'Kısıtlanan hesaplar',aciklama:'Engellemeden etkileşimi ve bildirimleri sınırla',
      anahtarlar:'restrict kısıt kısıtlanan',
      ikon:Icons.do_not_disturb_alt_rounded,sayfa:(_)=>const KisitlananlarV258Page(),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'GÜVENLİK',baslik:'Giriş yapılan cihazlar',aciklama:'Son girişleri ve cihaz bilgilerini gör',
      anahtarlar:'cihaz giriş oturum uzaktan çıkış',
      ikon:Icons.devices_outlined,sayfa:(_)=>const GirisGecmisiPage(),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'GÜVENLİK',baslik:'Hesap kurtarma',aciklama:'Kurtarma e-postası, telefon ve şifre yenileme',
      anahtarlar:'kurtarma eposta telefon şifre parola',
      ikon:Icons.health_and_safety_outlined,sayfa:(_)=>const HesapKurtarmaPage(),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'İÇERİK VE MEDYA',baslik:'İndirme ayarları',aciklama:'Paylaşımlar için varsayılan indirme tercihi',
      anahtarlar:'indir indirme download medya',
      ikon:Icons.download_outlined,sayfa:(_)=>const TercihlerPage(baslik:'İndirme izinleri'),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'İÇERİK VE MEDYA',baslik:'Veri ve depolama',aciklama:'Veri tasarrufu, otomatik oynatma ve Wi-Fi HD',
      anahtarlar:'veri depolama tasarruf wifi hd otomatik oynatma',
      ikon:Icons.data_saver_on_rounded,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'veri'),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'UYGULAMA',baslik:'Uygulama dili ve çeviri',aciklama:'Dil, otomatik çeviri ve altyazı dili',
      anahtarlar:'dil türkçe english deutsch arapça rusça çeviri altyazı',
      ikon:Icons.translate_rounded,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'dil'),anaListede:false,
    ),
    _NgelXAyarOgesi(
      bolum:'UYGULAMA',baslik:'Görünüm ve erişilebilirlik',aciklama:'Büyük yazı ve hareket azaltma tercihleri',
      anahtarlar:'görünüm erişilebilirlik büyük yazı hareket azalt',
      ikon:Icons.accessibility_new_rounded,sayfa:(_)=>const GelismisAyarlarV258Page(tur:'erisim'),anaListede:false,
    ),
  ];

  Future<void> _cikis(BuildContext context)async{
    final ok=await showDialog<bool>(
      context:context,
      builder:(c)=>AlertDialog(
        title:Text(t('logoutQuestion')),
        content:Text(t('logoutInfo')),
        actions:[
          TextButton(onPressed:()=>Navigator.pop(c,false),child:Text(t('cancel'))),
          FilledButton(onPressed:()=>Navigator.pop(c,true),child:Text(t('logout'))),
        ],
      ),
    );
    if(ok!=true)return;
    try{
      await FirebaseAuth.instance.signOut().timeout(const Duration(seconds:8));
      ngelxKokRotayaDon();
    }on TimeoutException{
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Çıkış zaman aşımına uğradı. Tekrar dene.')));
    }catch(e){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Çıkış yapılamadı: $e')));
    }
  }

  @override Widget build(BuildContext context)=>ValueListenableBuilder<String>(
    valueListenable:uygulamaDili,
    builder:(context,_,__) {
      final tum=_ogeler();
      final q=_normalize(sorgu);
      final sonuc=q.isEmpty
          ?const <_NgelXAyarOgesi>[]
          :tum.where((e)=>_normalize('${e.baslik} ${e.aciklama} ${e.anahtarlar} ${e.bolum}').contains(q)).toList();
      final bolumler=<String>[
        'HESAP',
        'GİZLİLİK VE GÜVENLİK',
        'BİLDİRİMLER',
        'İÇERİK VE MEDYA',
        'UYGULAMA',
        'YARDIM',
      ];

      return Theme(
        data:ThemeData.light().copyWith(
          scaffoldBackgroundColor:Colors.white,
          appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0),
          inputDecorationTheme:InputDecorationTheme(
            filled:true,
            fillColor:const Color(0xFFF3F4F6),
            border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none),
          ),
        ),
        child:Scaffold(
          appBar:AppBar(title:Text(t('settingsTitle'))),
          bottomNavigationBar:SizedBox(height:ngelxAltSistemRezervi(context)),
          body:ListView(
            keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag,
            padding:const EdgeInsets.fromLTRB(14,4,14,36),
            children:[
              Padding(
                padding:const EdgeInsets.fromLTRB(4,6,4,10),
                child:TextField(
                  controller:arama,
                  onChanged:(v)=>setState(()=>sorgu=v),
                  textInputAction:TextInputAction.search,
                  decoration:InputDecoration(
                    hintText:'Ayarlarda ara',
                    prefixIcon:const Icon(Icons.search_rounded,color:Colors.black54),
                    suffixIcon:sorgu.isEmpty?null:IconButton(
                      tooltip:'Aramayı temizle',
                      onPressed:(){arama.clear();setState(()=>sorgu='');FocusManager.instance.primaryFocus?.unfocus();},
                      icon:const Icon(Icons.close_rounded,color:Colors.black54),
                    ),
                  ),
                ),
              ),
              if(q.isNotEmpty)...[
                Padding(
                  padding:const EdgeInsets.fromLTRB(12,8,12,6),
                  child:Text(
                    sonuc.isEmpty?'Sonuç bulunamadı':'${sonuc.length} ayar bulundu',
                    style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w800),
                  ),
                ),
                if(sonuc.isEmpty)
                  const Padding(
                    padding:EdgeInsets.fromLTRB(12,30,12,30),
                    child:Center(child:Text('Başka bir kelimeyle ara. Örnek: mesaj, şifre, cihaz, bildirim.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black45))),
                  )
                else
                  ...sonuc.map((e)=>_satir(context,e,aramaSonucu:true)),
              ]else...[
                for(final bolum in bolumler)...[
                  _baslik(bolum),
                  ...tum.where((e)=>e.anaListede&&e.bolum==bolum).map((e)=>_satir(context,e)),
                ],
                const Divider(height:28),
                ListTile(
                  leading:const Icon(Icons.system_update,color:mor),
                  title:Text(t('appUpdates')),
                  subtitle:Text('v$ngelxVersionName • ${t("build")} $ngelxBuildNumber'),
                  trailing:const Icon(Icons.system_update_alt_rounded,color:Colors.green),
                  onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXHakkindaV258Page())),
                ),
                ListTile(
                  leading:const Icon(Icons.share,color:mavi),
                  title:Text(t('shareNgelx')),
                  subtitle:Text(t('shareNgelxSub')),
                  onTap:()async=>SharePlus.instance.share(ShareParams(text:'Ngel X ile dünyanı paylaş ✨\nhttps://ngelx.app')),
                ),
                const Divider(height:28),
                Padding(
                  padding:const EdgeInsets.fromLTRB(12,6,12,4),
                  child:Text('ÇIKIŞ VE HESAP İŞLEMLERİ',style:TextStyle(color:Colors.red.shade300,fontSize:12,fontWeight:FontWeight.w900,letterSpacing:.5)),
                ),
                ListTile(
                  leading:const Icon(Icons.logout,color:Colors.red),
                  title:Text(t('logout'),style:const TextStyle(color:Colors.red,fontWeight:FontWeight.w800)),
                  subtitle:const Text('Bu cihazdaki oturumu kapat',style:TextStyle(color:Colors.black54)),
                  onTap:()=>_cikis(context),
                ),
              ],
            ],
          ),
        ),
      );
    },
  );
}

class GizlilikMerkeziV366Page extends StatelessWidget{
  const GizlilikMerkeziV366Page({super.key});
  Widget _satir(BuildContext c,IconData icon,String title,String sub,Widget page)=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:7),
    leading:CircleAvatar(backgroundColor:const Color(0xFFF1E9FF),child:Icon(icon,color:mor)),
    title:Text(title,style:const TextStyle(fontWeight:FontWeight.w800)),
    subtitle:Text(sub),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>page)),
  );
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Gizlilik')),
      body:ListView(children:[
        _satir(context,Icons.visibility_outlined,'Profil ve paylaşımlar','Profil görünürlüğü, yorumlar, paylaşım ve gizli kelimeler',const TercihlerPage(baslik:'Gizlilik')),
        _satir(context,Icons.auto_stories_outlined,'Hikâyeler','Hikâyeyi kimlerin görebileceğini ve ekran görüntüsü tercihini yönet',const TercihlerPage(baslik:'Hikâye gizliliği')),
        _satir(context,Icons.download_outlined,'İndirme tercihi','Paylaşımların için varsayılan indirme ayarını seç',const TercihlerPage(baslik:'İndirme izinleri')),
      ]),
    ),
  );
}

class EngellenenKisitlananV366Page extends StatelessWidget{
  const EngellenenKisitlananV366Page({super.key});
  @override Widget build(BuildContext context)=>DefaultTabController(
    length:2,
    child:Theme(
      data:ThemeData.light(),
      child:Scaffold(
        backgroundColor:Colors.white,
        appBar:AppBar(
          title:const Text('Engellenen ve kısıtlananlar'),
          bottom:const TabBar(
            indicatorColor:mor,
            labelColor:mor,
            unselectedLabelColor:Colors.black54,
            tabs:[Tab(text:'Engellenen'),Tab(text:'Kısıtlanan')],
          ),
        ),
        body:const TabBarView(children:[
          _HesapDurumListesiV366(alan:'blocked',bosMetin:'Engellediğin hesap yok.',buton:'Engeli kaldır'),
          _HesapDurumListesiV366(alan:'restrictedUsers',bosMetin:'Kısıtladığın hesap yok.',buton:'Kısıtlamayı kaldır'),
        ]),
      ),
    ),
  );
}

class _HesapDurumListesiV366 extends StatefulWidget{
  final String alan,bosMetin,buton;
  const _HesapDurumListesiV366({required this.alan,required this.bosMetin,required this.buton});
  @override State<_HesapDurumListesiV366> createState()=>_HesapDurumListesiV366State();
}
class _HesapDurumListesiV366State extends State<_HesapDurumListesiV366>{
  Future<List<String>> _ids()async{
    final u=FirebaseAuth.instance.currentUser;
    if(u==null)return[];
    final d=await FirebaseFirestore.instance.collection('users').doc(u.uid).get();
    final raw=d.data()?[widget.alan];
    return raw is Iterable?raw.map((e)=>e.toString()).where((e)=>e.isNotEmpty).toList():<String>[];
  }
  Future<void> _kaldir(String id)async{
    final u=FirebaseAuth.instance.currentUser;if(u==null)return;
    await FirebaseFirestore.instance.collection('users').doc(u.uid).set(
      {widget.alan:FieldValue.arrayRemove([id])},
      SetOptions(merge:true),
    );
    if(mounted)setState((){});
  }
  @override Widget build(BuildContext context)=>FutureBuilder<List<String>>(
    future:_ids(),
    builder:(_,s){
      if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
      final ids=s.data??const <String>[];
      if(ids.isEmpty)return Center(child:Text(widget.bosMetin,style:const TextStyle(color:Colors.black54)));
      return ListView.separated(
        padding:const EdgeInsets.fromLTRB(14,14,14,36),
        itemCount:ids.length,
        separatorBuilder:(_,__)=>const Divider(height:1),
        itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),
          builder:(_,u){
            final v=u.data?.data()??<String,dynamic>{};
            final foto=(v['photoUrl']??'').toString();
            return ListTile(
              onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:ids[i]))),
              leading:CircleAvatar(
                backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),
                child:foto.isEmpty?const Icon(Icons.person):null,
              ),
              title:Text((v['displayName']??v['username']??'NgelX kullanıcısı').toString(),style:const TextStyle(fontWeight:FontWeight.w700)),
              subtitle:Text('@${v['username']??'ngelx'}'),
              trailing:TextButton(onPressed:()=>_kaldir(ids[i]),child:Text(widget.buton)),
            );
          },
        ),
      );
    },
  );
}

class GuvenlikMerkeziV366Page extends StatelessWidget{
  const GuvenlikMerkeziV366Page({super.key});
  Widget _satir(BuildContext c,IconData icon,String title,String sub,Widget page,{Color color=mor})=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:7),
    leading:CircleAvatar(backgroundColor:color.withValues(alpha:.10),child:Icon(icon,color:color)),
    title:Text(title,style:const TextStyle(fontWeight:FontWeight.w800)),
    subtitle:Text(sub),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>page)),
  );
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Güvenlik ve cihazlar')),
      body:ListView(children:[
        _satir(context,Icons.security_outlined,'Hesap güvenliği','Hesabı dondurma, silme talebi ve güvenlik seçenekleri',const HesapGuvenligiPage()),
        _satir(context,Icons.warning_amber_rounded,'Şüpheli girişler ve oturumlar','Uyarıları yönet ve gerektiğinde tüm cihazlardan çık',const GelismisAyarlarV258Page(tur:'guvenlik'),color:Colors.orange),
        _satir(context,Icons.devices_outlined,'Giriş yapılan cihazlar','Son girişleri ve cihaz bilgilerini gör',const GirisGecmisiPage()),
        _satir(context,Icons.health_and_safety_outlined,'Hesap kurtarma','Kurtarma e-postası, telefon ve şifre yenileme',const HesapKurtarmaPage()),
      ]),
    ),
  );
}

class MedyaVeriV366Page extends StatelessWidget{
  const MedyaVeriV366Page({super.key});
  Widget _satir(BuildContext c,IconData icon,String title,String sub,Widget page)=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:7),
    leading:CircleAvatar(backgroundColor:const Color(0xFFF1E9FF),child:Icon(icon,color:mor)),
    title:Text(title,style:const TextStyle(fontWeight:FontWeight.w800)),
    subtitle:Text(sub),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>page)),
  );
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Medya, veri ve indirme')),
      body:ListView(children:[
        _satir(context,Icons.video_collection_outlined,'Reels ve canlı','İndirme, yeniden paylaşım, canlı yorum ve davet tercihleri',const GelismisAyarlarV258Page(tur:'reels')),
        _satir(context,Icons.download_outlined,'İndirme ayarları','Paylaşımlar için varsayılan indirme tercihi',const TercihlerPage(baslik:'İndirme izinleri')),
        _satir(context,Icons.data_saver_on_rounded,'Veri ve depolama','Veri tasarrufu, otomatik oynatma ve Wi-Fi HD',const GelismisAyarlarV258Page(tur:'veri')),
        _satir(context,Icons.folder_copy_outlined,'Verilerim','Verilerini dışa aktar ve kayıtlarını yönet',const VerilerimV258Page()),
      ]),
    ),
  );
}

class UygulamaTercihleriV366Page extends StatelessWidget{
  const UygulamaTercihleriV366Page({super.key});
  Widget _satir(BuildContext c,IconData icon,String title,String sub,Widget page)=>ListTile(
    contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:7),
    leading:CircleAvatar(backgroundColor:const Color(0xFFF1E9FF),child:Icon(icon,color:mor)),
    title:Text(title,style:const TextStyle(fontWeight:FontWeight.w800)),
    subtitle:Text(sub),
    trailing:const Icon(Icons.chevron_right_rounded),
    onTap:()=>Navigator.push(c,MaterialPageRoute(builder:(_)=>page)),
  );
  @override Widget build(BuildContext context)=>Theme(
    data:ThemeData.light(),
    child:Scaffold(
      backgroundColor:Colors.white,
      appBar:AppBar(title:const Text('Dil, çeviri ve görünüm')),
      body:ListView(children:[
        _satir(context,Icons.translate_rounded,'Dil ve çeviri','Uygulama dili, otomatik çeviri ve altyazı dili',const GelismisAyarlarV258Page(tur:'dil')),
        _satir(context,Icons.accessibility_new_rounded,'Görünüm ve erişilebilirlik','Büyük yazı ve hareket azaltma tercihleri',const GelismisAyarlarV258Page(tur:'erisim')),
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
    return ListView.builder(itemCount:ids.length,itemBuilder:(_,i)=>FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(ids[i]).get(),builder:(_,u){final v=u.data?.data()??{},f=(v['photoUrl']??'').toString();return ListTile(onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:ids[i]))),leading:CircleAvatar(backgroundImage:f.isEmpty?null:NgelXAgImageProvider(f),child:f.isEmpty?const Icon(Icons.person):null),title:Text((v['displayName']??v['username']??'NgelX').toString()),subtitle:Text('@${v['username']??'ngelx'}'),trailing:widget.trailing(ids[i]));}));
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
    final h=await SharedPreferences.getInstance();
    await h.setBool('ngelx_auto_translate',otomatikCeviri);
    await h.setString('ngelx_caption_language',altyazi);
    ngelxIcerikDilRevizyonu.value++;
  }
  Future<void> _bool(String k,bool v)async{
    if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));
    if(k=='autoTranslate'){final h=await SharedPreferences.getInstance();await h.setBool('ngelx_auto_translate',v);ngelxIcerikDilRevizyonu.value++;}
  }
  Future<void> _str(String k,String v)async{
    if(uid!=null)await FirebaseFirestore.instance.collection('users').doc(uid).set({k:v},SetOptions(merge:true));
    if(k=='captionLanguage'){final h=await SharedPreferences.getInstance();await h.setString('ngelx_caption_language',v);ngelxIcerikDilRevizyonu.value++;}
  }
  Widget _sw(String a,String s,bool v,ValueChanged<bool> f,{bool enabled=true})=>SwitchListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20,vertical:5),title:Text(a,style:const TextStyle(fontWeight:FontWeight.w700)),subtitle:Text(s),value:v,onChanged:enabled?f:null,activeTrackColor:mavi);
  Widget _h(String x)=>Padding(padding:const EdgeInsets.fromLTRB(20,18,20,5),child:Text(x,style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w900)));
  List<Widget> _izin(String alan,String secili,ValueChanged<String> f)=>const [('all','Herkes'),('following','Takip ettiklerim'),('friends','Arkadaşlar'),('none','Kimse')].map((e)=>RadioListTile<String>(value:e.$1,groupValue:secili,title:Text(e.$2),onChanged:(v){if(v!=null){f(v);}})).toList();
  String get _baslik=>switch(widget.tur){'mesaj'=>'Mesajlar ve iletişim','icerik'=>'İçerik ve etkileşim','reels'=>'Reels ve canlı','bildirim'=>'Bildirim tercihleri','guvenlik'=>'Güvenlik uyarıları','veri'=>'Veri ve depolama','dil'=>t('languageTranslate'),'erisim'=>'Görünüm ve erişilebilirlik',_=>'Ayarlar'};

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
          ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:20),leading:const Icon(Icons.language,color:mor),title:Text(t('appLanguage'),style:const TextStyle(fontWeight:FontWeight.w800)),subtitle:Text(dilAdlari[uygulamaDili.value]??uygulamaDili.value),trailing:const Icon(Icons.chevron_right),onTap:_dilSec),
          _sw(t('autoPostTranslation'),t('autoPostTranslationSub'),otomatikCeviri,(v){setState(()=>otomatikCeviri=v);_bool('autoTranslate',v);}),
          _h(t('defaultCaptionLanguage')),
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
  @override Widget build(BuildContext context)=>ValueListenableBuilder<String>(valueListenable:uygulamaDili,builder:(context,_,__)=>Theme(data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white,appBarTheme:const AppBarTheme(backgroundColor:Colors.white,foregroundColor:Colors.black,elevation:0)),child:Scaffold(appBar:AppBar(title:Text(_baslik)),body:ListView(children:_icerik))));
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
