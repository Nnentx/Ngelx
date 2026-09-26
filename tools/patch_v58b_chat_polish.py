from pathlib import Path
import re

MAIN=Path("app/lib/main.dart")
PUBSPEC=Path("app/pubspec.yaml")
s=MAIN.read_text(encoding="utf-8")
changes=[]

def once(old,new,label,required=True):
    global s
    n=s.count(old)
    if n==0:
        if required: raise SystemExit(f"[V58B] target missing: {label}")
        return
    s=s.replace(old,new,1)
    changes.append(label)

once(
"""class _UygulamaDurumKapisiState extends State<UygulamaDurumKapisi> with WidgetsBindingObserver{
  late Future<DocumentSnapshot<Map<String,dynamic>>> durum;
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);yenile();unawaited(_presence(true));unawaited(_uzakCikisKontrol());}
  @override void dispose(){WidgetsBinding.instance.removeObserver(this);unawaited(_presence(false));super.dispose();}""",
"""class _UygulamaDurumKapisiState extends State<UygulamaDurumKapisi> with WidgetsBindingObserver{
  late Future<DocumentSnapshot<Map<String,dynamic>>> durum;
  Timer? _presenceHeartbeat;
  void _presenceBaslat(){
    _presenceHeartbeat?.cancel();
    unawaited(_presence(true));
    _presenceHeartbeat=Timer.periodic(const Duration(seconds:45),(_)=>unawaited(_presence(true)));
  }
  void _presenceDurdur(){
    _presenceHeartbeat?.cancel();
    _presenceHeartbeat=null;
    unawaited(_presence(false));
  }
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);yenile();_presenceBaslat();unawaited(_uzakCikisKontrol());}
  @override void dispose(){WidgetsBinding.instance.removeObserver(this);_presenceDurdur();super.dispose();}""",
"presence heartbeat lifecycle",
)

once(
"""  @override void didChangeAppLifecycleState(AppLifecycleState state){
    if(state==AppLifecycleState.resumed){unawaited(_presence(true));unawaited(_uzakCikisKontrol());}
    if(state==AppLifecycleState.inactive||state==AppLifecycleState.paused||state==AppLifecycleState.detached||state==AppLifecycleState.hidden)unawaited(_presence(false));
  }""",
"""  @override void didChangeAppLifecycleState(AppLifecycleState state){
    if(state==AppLifecycleState.resumed){_presenceBaslat();unawaited(_uzakCikisKontrol());}
    if(state==AppLifecycleState.inactive||state==AppLifecycleState.paused||state==AppLifecycleState.detached||state==AppLifecycleState.hidden)_presenceDurdur();
  }""",
"presence lifecycle state",
)

s=s.replace("if(v['isOnline']==true)return '● Çevrimiçi';","if(ngelxPresenceOnline(v))return '● Çevrimiçi';")
s=s.replace("final online=v['isOnline']==true;","final online=ngelxPresenceOnline(v);")
s=s.replace("online=p['isOnline']==true||p['online']==true","online=ngelxPresenceOnline(p)")
changes.append("fresh online status")

once(
"""      builder:(_,s){
        final ham=s.data?.data()?['nicknames'],
          nicks=ham is Map?Map<String,dynamic>.from(ham):<String,dynamic>{},
          takma=(uid==null?'':(nicks[uid]??'').toString()).trim(),
          gorunenAd=takma.isNotEmpty?takma:widget.ad;""",
"""      builder:(_,s){
        final cv=s.data?.data()??<String,dynamic>{};
        final ham=cv['nicknames'],
          nicks=ham is Map?Map<String,dynamic>.from(ham):<String,dynamic>{},
          takma=(uid==null?'':(nicks[uid]??'').toString()).trim(),
          gorunenAd=takma.isNotEmpty?takma:widget.ad;
        final typingAt=cv['typing_\${widget.digerUid}'];
        final yaziyor=cv['typing_\${widget.digerUid}']==true&&typingAt is Timestamp&&DateTime.now().difference(typingAt.toDate()).inSeconds<=6;""",
"private typing state",
)
once(
"""                Text(gorunenAd,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:ngelxPrivateBlueInk,fontSize:16,fontWeight:FontWeight.w900)),
                AktiflikDurumuYazisi(uid:widget.digerUid),""",
"""                Text(gorunenAd,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:ngelxPrivateBlueInk,fontSize:16,fontWeight:FontWeight.w900)),
                if(yaziyor)
                  const Text('Yazıyor…',style:TextStyle(color:ngelxPrivateBlue,fontSize:12,fontWeight:FontWeight.w800))
                else
                  AktiflikDurumuYazisi(uid:widget.digerUid),""",
"private typing label",
)

once(
"""        return Padding(
          padding:const EdgeInsets.only(left:2,bottom:5),
          child:Row(mainAxisSize:MainAxisSize.min,children:[
            CircleAvatar(radius:10,backgroundColor:ngelxGroupGreenSoft,backgroundImage:pf.isEmpty?null:CachedNetworkImageProvider(pf),child:pf.isEmpty?const Icon(Icons.person,size:11,color:ngelxGroupGreen):null),
            const SizedBox(width:6),
            Flexible(child:Text(isim,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF187A3D),fontSize:11.3,fontWeight:FontWeight.w900))),
          ]),
        );""",
"""        return InkWell(
          onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:gonderen))),
          borderRadius:BorderRadius.circular(14),
          child:Padding(
            padding:const EdgeInsets.only(left:2,bottom:5,right:6,top:2),
            child:Row(mainAxisSize:MainAxisSize.min,children:[
              CircleAvatar(radius:10,backgroundColor:ngelxGroupGreenSoft,backgroundImage:pf.isEmpty?null:CachedNetworkImageProvider(pf),child:pf.isEmpty?const Icon(Icons.person,size:11,color:ngelxGroupGreen):null),
              const SizedBox(width:6),
              Flexible(child:Text(isim,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF187A3D),fontSize:11.3,fontWeight:FontWeight.w900))),
            ]),
          ),
        );""",
"group sender profile tap",
)

once(
"""    final yaziRengi=ben?Colors.white:const Color(0xFF211B2C);
    final tepkiSayilari=<String,int>{};""",
"""    final yaziRengi=ben?Colors.white:const Color(0xFF211B2C);
    final sadeMedya=tur=='photo'||tur=='video'||tur=='gif';
    final tepkiSayilari=<String,int>{};""",
"group plain media flag",
)
s=s.replace(
"padding:sadeceEmoji?const EdgeInsets.symmetric(horizontal:3,vertical:2):EdgeInsets.all((tur=='photo'||tur=='gif')?4:9),",
"padding:sadeceEmoji?const EdgeInsets.symmetric(horizontal:3,vertical:2):(sadeMedya?EdgeInsets.zero:const EdgeInsets.all(9)),",
1,
)
s=s.replace(
"gradient:sadeceEmoji?null:(ben?const LinearGradient(colors:[Color(0xFF14AE52),Color(0xFF078B3B)],begin:Alignment.topLeft,end:Alignment.bottomRight):null),",
"gradient:(sadeceEmoji||sadeMedya)?null:(ben?const LinearGradient(colors:[Color(0xFF14AE52),Color(0xFF078B3B)],begin:Alignment.topLeft,end:Alignment.bottomRight):null),",
1,
)
s=s.replace(
"color:sadeceEmoji?Colors.transparent:(ben?null:const Color(0xFFDDF3E4).withValues(alpha:.98)),",
"color:(sadeceEmoji||sadeMedya)?Colors.transparent:(ben?null:const Color(0xFFDDF3E4).withValues(alpha:.98)),",
1,
)
s=s.replace(
"border:sadeceEmoji?null:(ben?null:Border.all(color:const Color(0xFFCBE7D4))),",
"border:(sadeceEmoji||sadeMedya)?null:(ben?null:Border.all(color:const Color(0xFFCBE7D4))),",
1,
)
s=s.replace(
"boxShadow:sadeceEmoji?null:(yeniBlok?const [BoxShadow(color:Color(0x0C000000),blurRadius:8,offset:Offset(0,3))]:null),",
"boxShadow:(sadeceEmoji||sadeMedya)?null:(yeniBlok?const [BoxShadow(color:Color(0x0C000000),blurRadius:8,offset:Offset(0,3))]:null),",
1,
)
changes.append("plain group media bubbles")

once(
"""                Slider(
                  value:opacity,min:.10,max:.55,
                  onChanged:(x)=>ref.set({'backgroundOpacity_'+uid:x},SetOptions(merge:true)),
                ),""",
"""                Slider(
                  value:opacity,min:.10,max:.55,
                  onChanged:(x)async{
                    if(!await ngelxCanManageGroup(widget.chatId,uid)){
                      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup arka planını yalnızca kurucu ve yöneticiler değiştirebilir.')));
                      return;
                    }
                    await ref.set({'backgroundOpacity':x},SetOptions(merge:true));
                  },
                ),""",
"group background opacity manager gate",
)

s=s.replace("'onlyAdminsCanAddMembers':false,","'onlyAdminsCanAddMembers':true,")
changes.append("new group member-add default")

p=PUBSPEC.read_text(encoding="utf-8")
p2,n=re.subn(r"(?m)^version:\s+\S+\s*$","version: 1.0.59+278",p,count=1)
if n!=1: raise SystemExit("[V58B] pubspec version line missing")
PUBSPEC.write_text(p2,encoding="utf-8")
MAIN.write_text(s,encoding="utf-8")
print("[V58B] patched:",", ".join(changes))
print("[V58B] version: 1.0.59+278")
