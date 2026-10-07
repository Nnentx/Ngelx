#!/usr/bin/env python3
from pathlib import Path

path = Path("app/lib/main.dart")
src = path.read_text(encoding="utf-8")

src = src.replace("defaultValue: '397'", "defaultValue: '398'", 1)
src = src.replace("defaultValue: '1.0.173'", "defaultValue: '1.0.174'", 1)

login_start = src.index("class _GirisPageState extends State<GirisPage>")
login_end = src.index("\nclass _NgelXRenkliBaslik", login_start)
login = src[login_start:login_end]

login = login.replace("minimumSize:const Size.fromHeight(56),","minimumSize:const Size.fromHeight(50),",1)
login = login.replace("contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:19),","contentPadding:const EdgeInsets.symmetric(horizontal:18,vertical:16),",1)
login = login.replace("padding:const EdgeInsets.fromLTRB(24,14,24,28),","padding:const EdgeInsets.fromLTRB(24,10,24,16),",1)
login = login.replace(
    "const SizedBox(height:36),\n                  Center(child:Image.asset('assets/ngelx_logo.png',width:104,height:104,fit:BoxFit.contain)),",
    "const SizedBox(height:20),\n                  Center(child:Image.asset('assets/ngelx_logo.png',width:82,height:82,fit:BoxFit.contain)),",
    1,
)
login = login.replace(
    "const Center(child:Text('ngelxsocial.com',style:TextStyle(color:Color(0xFF7682A2),fontSize:13.5,fontWeight:FontWeight.w600,letterSpacing:.1))),\n                  const SizedBox(height:24),",
    "const Center(child:Text('ngelxsocial.com',style:TextStyle(color:Color(0xFF7682A2),fontSize:12.5,fontWeight:FontWeight.w600,letterSpacing:.1))),\n                  const SizedBox(height:16),",
    1,
)
login = login.replace(
    "style:const TextStyle(color:Color(0xFF68738F),fontSize:15.5,fontWeight:FontWeight.w500)",
    "style:const TextStyle(color:Color(0xFF68738F),fontSize:14.5,fontWeight:FontWeight.w500)",
    1,
)
login = login.replace("height:54,","height:48,",1)
login = login.replace(
    "const SizedBox(height:24),\n                  Row(children:[\n                    ozellik(",
    "const SizedBox(height:18),\n                  Row(children:[\n                    ozellik(",
    1,
)
login = login.replace(
    "                  ]),\n                  const SizedBox(height:24),\n                  TextField(",
    "                  ]),\n                  const SizedBox(height:18),\n                  TextField(",
    1,
)
login = login.replace("const SizedBox(height:13),\n                  TextField(","const SizedBox(height:10),\n                  TextField(",1)
login = login.replace("height:58,","height:54,",1)
login = login.replace("const SizedBox(height:20),\n                  Row(children:[","const SizedBox(height:14),\n                  Row(children:[",1)
login = login.replace("const SizedBox(height:14),\n                  Row(children:[","const SizedBox(height:10),\n                  Row(children:[",1)
login = login.replace("const SizedBox(height:17),\n                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[","const SizedBox(height:10),\n                  Row(mainAxisAlignment:MainAxisAlignment.center,children:[",1)
login = login.replace(
    "lt('Google ile giriş bağlantısı hazırlanıyor.','Google sign-in is being prepared.')",
    "lt('Google ile giriş henüz aktif değil.','Google sign-in is not active yet.')",
)
login = login.replace(
    "lt('Apple ile giriş bağlantısı hazırlanıyor.','Apple sign-in is being prepared.')",
    "lt('Apple ile giriş henüz aktif değil.','Apple sign-in is not active yet.')",
)

src = src[:login_start] + login + src[login_end:]

story_class = src.index("class _HikayeGosterPageState extends State<HikayeGosterPage>")
story_end = src.index("\nclass HesapDegistirPage", story_class)
story = src[story_class:story_end]

old_time = r'''  String get zamanBilgisi{
    final olusma=widget.createdAt is Timestamp?(widget.createdAt as Timestamp).toDate():null;
    final bitis=widget.expiresAt is Timestamp?(widget.expiresAt as Timestamp).toDate():null;
    String iki(int n)=>n.toString().padLeft(2,'0');
    String saat(DateTime d)=>'${iki(d.hour)}:${iki(d.minute)}';
    String tarihSaat(DateTime d)=>'${iki(d.day)}.${iki(d.month)} ${saat(d)}';
    String baslangic='Başladı: az önce';
    if(olusma!=null){
      baslangic='Başladı: ${saat(olusma)}';
    }
    if(bitis==null)return baslangic;
    final kalan=bitis.difference(DateTime.now());
    final bitisEtiketi=olusma!=null&&olusma.day==bitis.day&&olusma.month==bitis.month&&olusma.year==bitis.year
      ?saat(bitis)
      :tarihSaat(bitis);
    if(kalan.isNegative)return '$baslangic • Bitti: $bitisEtiketi';
    final kalanYazi=kalan.inHours>=1?'${kalan.inHours} sa kaldı':'${kalan.inMinutes.clamp(1,59)} dk kaldı';
    return '$baslangic • Biter: $bitisEtiketi • $kalanYazi';
  }
'''
new_time = r'''  String get zamanBilgisi{
    final olusma=widget.createdAt is Timestamp?(widget.createdAt as Timestamp).toDate():null;
    if(olusma==null)return 'Az önce';
    final fark=DateTime.now().difference(olusma);
    if(fark.isNegative||fark.inMinutes<1)return 'Az önce';
    if(fark.inHours<1)return '${fark.inMinutes} dk önce';
    if(fark.inHours<24)return '${fark.inHours} sa önce';
    return '${fark.inDays} gün önce';
  }

  String get sonaErmeBilgisi{
    final bitis=widget.expiresAt is Timestamp?(widget.expiresAt as Timestamp).toDate():null;
    if(bitis==null)return '';
    final kalan=bitis.difference(DateTime.now());
    if(kalan.isNegative)return 'Süresi doldu';
    if(kalan.inHours>=1)return '${kalan.inHours} saat sonra sona erecek';
    return '${kalan.inMinutes.clamp(1,59)} dk sonra sona erecek';
  }
'''
if old_time not in story:
    raise SystemExit("legacy story time block not found")
story = story.replace(old_time,new_time,1)
story = story.replace(
    "subtitle:Text(zamanBilgisi)",
    "subtitle:Text(sonaErmeBilgisi.isEmpty?zamanBilgisi:'$zamanBilgisi • $sonaErmeBilgisi')",
    1,
)

src = src[:story_class] + story + src[story_end:]

path.write_text(src,encoding="utf-8")
print("Build 398 login + story polish patch applied.")
