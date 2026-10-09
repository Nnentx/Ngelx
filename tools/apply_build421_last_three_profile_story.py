#!/usr/bin/env python3
"""Build 421: video QA three remaining improvements, display-only changes.

Keep all profile gestures, cover mode, social actions, story expiry records,
media playback and Firestore rules unchanged. Strict anchors fail closed.
"""
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

def modify_between(start_marker,end_marker,changes):
    global s
    a=s.index(start_marker)
    b=s.index(end_marker,a+len(start_marker))
    part=s[a:b]
    for label,old,new in changes:
        n=part.count(old)
        if n!=1:
            raise SystemExit(f'Build421 {label}: expected 1 anchor, got {n}')
        part=part.replace(old,new,1)
    s=s[:a]+part+s[b:]

# (1) Narrow the header only when coverless, not the approved covered view.
modify_between(
  'class _ProfilPageState extends State<ProfilPage>',
  '\nclass _ProfilEtkilesimRozeti',
  [
    ('owner no-cover avatar box',
     'SizedBox(height:174,width:210,child:Stack(alignment:Alignment.center,children:[',
     'SizedBox(height:152,width:194,child:Stack(alignment:Alignment.center,children:['),
    ('owner decorative bubble left',
     'Positioned(left:8,top:50,child:Container(width:58,height:58,',
     'Positioned(left:10,top:45,child:Container(width:51,height:51,'),
    ('owner decorative bubble right',
     'Positioned(right:7,top:10,child:Container(width:76,height:76,',
     'Positioned(right:7,top:9,child:Container(width:66,height:66,'),
    ('owner avatar size',
     'kullanici:kullanici,radius:70,etkin:false',
     'kullanici:kullanici,radius:59,etkin:false'),
    ('owner camera offset',
     'Positioned(right:21,bottom:7,child:InkWell(',
     'Positioned(right:15,bottom:3,child:InkWell('),
    ('owner no-cover displayName',
     'style:const TextStyle(fontSize:27,color:Colors.black,fontWeight:FontWeight.w900)',
     'style:const TextStyle(fontSize:25,color:Colors.black,fontWeight:FontWeight.w900)'),
  ],
)

# (2) Visitor coverless date becomes the SAME month/year label already shown
# in the covered view and on the owner's page.
modify_between(
  'class _KullaniciProfilPageState extends State<KullaniciProfilPage>',
  '\nclass NgelXVideoKapakOnizleme',
  [
    ('visitor no-cover initial top gap',
     """               if(kapaksiz)...[
                  const SizedBox(height:8),""",
     """               if(kapaksiz)...[
                  const SizedBox(height:4),"""),
    ('visitor no-cover avatar box',
     'Center(child:SizedBox(height:182,width:230,child:Stack(',
     'Center(child:SizedBox(height:156,width:205,child:Stack('),
    ('visitor decorative bubble left',
     'Positioned(left:10,top:49,child:Container(width:62,height:62,',
     'Positioned(left:10,top:39,child:Container(width:53,height:53,'),
    ('visitor decorative bubble right',
     'Positioned(right:7,top:8,child:Container(width:83,height:83,',
     'Positioned(right:7,top:8,child:Container(width:70,height:70,'),
    ('visitor no-cover avatar size',
     'canli,erisimVar,67),',
     'canli,erisimVar,57),'),
    ('visitor avatar/name gap',
     """                  const SizedBox(height:8),
                  _ziyaretciReferansAd(v),""",
     """                  const SizedBox(height:5),
                  _ziyaretciReferansAd(v),"""),
    ('visitor name/bio gap',
     """                  const SizedBox(height:12),
                  Text((v['bio']??'').toString(),textAlign:TextAlign.center""",
     """                  const SizedBox(height:8),
                  Text((v['bio']??'').toString(),textAlign:TextAlign.center"""),
    ('visitor bio/metadata gap',
     """                  const SizedBox(height:11),
                  Wrap(alignment:WrapAlignment.center""",
     """                  const SizedBox(height:8),
                  Wrap(alignment:WrapAlignment.center"""),
    ('visitor full join date',
     """                      Text('NgelX’e katıldı: '+katilimHam.toDate().year.toString(),
                        style:const TextStyle(color:Color(0xFF68647D),fontSize:12)),""",
     """                      Text(katilim,
                        style:const TextStyle(color:Color(0xFF68647D),fontSize:12)),"""),
  ],
)

# (3) The story viewer already receives the saved createdAt and expiresAt.
# Show both exact local timestamps and remaining time without altering data.
a=s.index('class _HikayeGosterPageState extends State<HikayeGosterPage>')
b=s.index('\nclass HesapDegistirPage',a)
story=s[a:b]
marker='  Future<void> _yanitGonder(String ham,{bool tepki=false})async{'
if story.count(marker)!=1:
    raise SystemExit('Build421 story reply helper anchor changed')
helpers="""  String _hikayeTamTarih(DateTime tarih){
    String iki(int n)=>n.toString().padLeft(2,'0');
    return '${iki(tarih.day)}.${iki(tarih.month)}.${tarih.year} ${iki(tarih.hour)}:${iki(tarih.minute)}';
  }

  String get hikayeBaslangicZamani{
    final ham=widget.createdAt;
    if(ham is! Timestamp)return 'Paylaşım zamanı henüz bilinmiyor';
    return 'Paylaşıldı: ${_hikayeTamTarih(ham.toDate())}';
  }

  String get hikayeBitisZamani{
    final ham=widget.expiresAt;
    if(ham is! Timestamp)return 'Bitiş zamanı henüz bilinmiyor';
    final tarih=ham.toDate();
    final kalan=tarih.difference(DateTime.now());
    if(kalan<=Duration.zero)return 'Bitti: ${_hikayeTamTarih(tarih)}';
    final saat=kalan.inHours;
    final dakika=kalan.inMinutes.remainder(60);
    final kalanYazi=saat>0?'${saat} sa ${dakika} dk kaldı'
      :'${kalan.inMinutes.clamp(1,59)} dk kaldı';
    return 'Biter: ${_hikayeTamTarih(tarih)} · $kalanYazi';
  }

"""
story=story.replace(marker,helpers+marker,1)

anchor="""              ]),
              const Spacer(),
              if(!benim&&widget.ownerUid.isNotEmpty) ...["""
widget="""              ]),
              const SizedBox(height:7),
              Align(alignment:Alignment.centerLeft,child:Container(
                padding:const EdgeInsets.symmetric(horizontal:10,vertical:7),
                decoration:BoxDecoration(
                  color:Colors.black.withValues(alpha:.42),
                  borderRadius:BorderRadius.circular(10)),
                child:AnimatedBuilder(
                  animation:sure,
                  builder:(_,__)=>Column(
                    crossAxisAlignment:CrossAxisAlignment.start,
                    mainAxisSize:MainAxisSize.min,children:[
                      Text(hikayeBaslangicZamani,maxLines:1,
                        overflow:TextOverflow.ellipsis,
                        style:const TextStyle(color:Colors.white,fontSize:11)),
                      const SizedBox(height:2),
                      Text(hikayeBitisZamani,maxLines:2,
                        style:const TextStyle(color:Colors.white70,
                          fontSize:11,fontWeight:FontWeight.w600)),
                    ]),
                ),
              )),
              const Spacer(),
              if(!benim&&widget.ownerUid.isNotEmpty) ...["""
if story.count(anchor)!=1:
    raise SystemExit(f'Build421 visible story dates anchor changed: {story.count(anchor)}')
story=story.replace(anchor,widget,1)
s=s[:a]+story+s[b:]

p.write_text(s,encoding='utf-8')
print('Build421 coverless sizing, month/year join date, exact story start/end and time remaining applied.')
