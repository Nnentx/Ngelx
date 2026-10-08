#!/usr/bin/env python3
"""Build 404 -- UI, loading and error states only. Run after Build 403 patch."""
from pathlib import Path
def rep(s,a,b,k):
 n=s.count(a)
 if n!=1: raise SystemExit(f'{k}: expected one match, found {n}: {a[:95]!r}')
 return s.replace(a,b,1)
def get(f): return Path(f).read_text(encoding='utf-8')
def save(f,s): Path(f).write_text(s,encoding='utf-8')

p='app/lib/main.dart';m=get(p)
m=rep(m,"defaultValue: '403'","defaultValue: '404'",'version code')
m=rep(m,"defaultValue: '1.0.179'","defaultValue: '1.0.180'",'version name')
q='app/pubspec.yaml'
save(q,rep(get(q),'version: 1.0.179+403','version: 1.0.180+404','pubspec'))

i=m.index('class _NgelXVideoKapakOnizlemeState')
j=m.index('\nclass MedyaOnizleme extends StatelessWidget',i)
s=m[i:j]
s=rep(s,'return const ColoredBox(color:Color(0xFFE9ECF2),child:Center(child:SizedBox(width:22,height:22,child:CircularProgressIndicator(strokeWidth:2,color:Colors.black26))));',
"""return const ColoredBox(color:Color(0xFFF0EDFA),child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
  SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFF8655E6))),
  SizedBox(height:7),Text('Video hazırlanıyor',textAlign:TextAlign.center,style:TextStyle(color:Color(0xFF655B74),fontSize:10,fontWeight:FontWeight.w600)),
])));""",'thumbnail loading label')
m=m[:i]+s+m[j:]

i=m.index('class _ProfilTanitimVideoKartiState')
j=m.index('\nclass ',i+20)
s=m[i:j]
s=rep(s,'await x.initialize();','await x.initialize().timeout(const Duration(seconds:15));','intro timed initialization')
s=rep(s,
"""    if(hata)return Container(
      height:150,
      decoration:BoxDecoration(color:const Color(0xFFF1F2F4),borderRadius:BorderRadius.circular(18)),
      child:const Center(child:Icon(Icons.videocam_off_rounded,color:Colors.black38,size:38)),
    );""",
"""    if(hata)return InkWell(
      onTap:(){final eski=c;c=null;if(eski!=null)unawaited(eski.dispose());setState(()=>hata=false);unawaited(_hazirla());},
      borderRadius:BorderRadius.circular(18),
      child:Container(height:150,
        decoration:BoxDecoration(color:const Color(0xFFF1F2F4),borderRadius:BorderRadius.circular(18)),
        child:const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(Icons.refresh_rounded,color:Color(0xFF7544DB),size:34),SizedBox(height:8),
          Text('Video yüklenemedi • Tekrar dene',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:11)),
        ])),
      ),
    );""",'intro retry')
s=rep(s,
"""Center(child:yukleniyor
            ?const CircularProgressIndicator(color:Colors.white)
            :const Column(""",
"""Center(child:yukleniyor
            ?const Column(mainAxisSize:MainAxisSize.min,children:[
              CircularProgressIndicator(color:Colors.white),
              SizedBox(height:9),
              Text('Tanıtım videosu hazırlanıyor',textAlign:TextAlign.center,style:TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
            ])
            :const Column(""",'intro pending label')
m=m[:i]+s+m[j:]
save(p,m)

p='app/lib/audio_live_rooms.dart';a=get(p)
a=rep(a,
"""label:Text(x,style:TextStyle(color:kategori==x?const Color(0xFF5B2CA2):Colors.black87,fontWeight:FontWeight.w700)),
  selected:kategori==x,selectedColor:const Color(0xFFEFE5FF),
  onSelected:(_)=>setState(()=>kategori=x),""",
"""label:Text(x,style:TextStyle(color:kategori==x?const Color(0xFF5825AB):const Color(0xFF27223A),fontWeight:FontWeight.w800)),
  selected:kategori==x,
  backgroundColor:const Color(0xFFF7F5FB),selectedColor:const Color(0xFFE8DAFF),
  disabledColor:const Color(0xFFF2F2F5),
  side:BorderSide(color:kategori==x?const Color(0xFF8452D8):const Color(0xFFDDD7E8)),
  checkmarkColor:const Color(0xFF5825AB),
  onSelected:(_)=>setState(()=>kategori=x),""",'category high contrast')

# Replace separate yellow waiting band with concise status inside room summary.
i=a.index('    if(sahibiyim&&aktifKisiSayisi<2&&yalnizlikBasladi!=null&&!bitti)')
j=a.index('    Expanded(child:ListView(',i)
if '2. kişi bekleniyor' not in a[i:j]:raise SystemExit('waiting band changed')
a=a[:i]+a[j:]
needle="Text('"+'$'+'{sp.length}'+"/12 konuşmacı',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700))"
a=rep(a,needle,needle+""",
if(sahibiyim&&aktifKisiSayisi<2&&yalnizlikBasladi!=null&&!bitti)...[
 const SizedBox(height:7),
 const Row(children:[Icon(Icons.group_add_outlined,size:15,color:Color(0xFF7354A3)),SizedBox(width:5),
   Flexible(child:Text('2. kişi bekleniyor • Davet edebilirsin',
     style:TextStyle(fontSize:11,color:Color(0xFF7354A3),fontWeight:FontWeight.w700)))]),
]""",'waiting state in room summary')

a=rep(a,
"""if(s.hasError)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:36),SizedBox(height:8),Text('İstekler yüklenemedi.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bağlantını kontrol edip tekrar dene.',style:TextStyle(color:Colors.black45))])));""",
"""if(s.hasError)return Center(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
 const Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:36),const SizedBox(height:8),
 const Text('İstekler yüklenemedi.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
 const SizedBox(height:3),const Text('Bağlantını kontrol edip tekrar dene.',style:TextStyle(color:Colors.black45)),
 const SizedBox(height:12),
 OutlinedButton.icon(onPressed:(){Navigator.pop(c);unawaited(istekler());},
   icon:const Icon(Icons.refresh_rounded),label:const Text('Yeniden dene')),
])));""",'speech request network retry')
save(p,a)

p='app/lib/live_broadcast_studio.dart';l=get(p)
l=rep(l,'const Center(child:CircularProgressIndicator(color:Colors.white)),',
"""const Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
 CircularProgressIndicator(color:Colors.white),
 SizedBox(height:10),Text('Kamera hazırlanıyor...',style:TextStyle(color:Colors.white,fontSize:12,fontWeight:FontWeight.w800)),
])),""",'switching camera message')
l=rep(l,
'return const ColoredBox(color: Color(0xFF151515), child: Center(child: CircularProgressIndicator(color: Colors.white)));',
"""return const ColoredBox(color: Color(0xFF151515), child: Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
 CircularProgressIndicator(color: Colors.white),
 SizedBox(height:11),Text('Kamera hazırlanıyor...',style:TextStyle(color:Colors.white70,fontSize:12,fontWeight:FontWeight.w700)),
])));""",'initial camera message')
l=rep(l,
"""label:Text(p.ad),selected:p.ad==presetAdi,
                onSelected:(_){setSheet(()=>presetAdi=p.ad);""",
"""label:Text(p.ad,style:TextStyle(color:p.ad==presetAdi?const Color(0xFF542A99):Colors.black87,fontWeight:FontWeight.w800)),
                selected:p.ad==presetAdi,
                backgroundColor:const Color(0xFFF8F7FC),selectedColor:const Color(0xFFEDE2FF),
                side:BorderSide(color:p.ad==presetAdi?const Color(0xFF8B55D9):const Color(0xFFDDD7E8)),
                checkmarkColor:const Color(0xFF542A99),
                onSelected:(_){setSheet(()=>presetAdi=p.ad);""",'live preset contrast')
save(p,l)
print('Build 404 patch applied: no auth, media ownership, Firestore schema or LiveKit changes.')
