#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN_PATH=ROOT/"app/lib/main.dart"
PUB_PATH=ROOT/"app/pubspec.yaml"

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f"Build 296 patch failed: {label}: {n} matches")
    return text.replace(old,new,1)

def between(text,start,end,new,label):
    a=text.find(start); b=text.find(end,a)
    if a<0 or b<0:
        raise SystemExit(f"Build 296 patch failed: {label}")
    return text[:a]+new+text[b:]

main=MAIN_PATH.read_text(encoding="utf-8")

new_social=r'''Future<bool> sosyalIstekGonder({
  required String hedefUid,
  required String tur,
  required String metin,
}) async {
  final user=FirebaseAuth.instance.currentUser;
  if(user==null||user.isAnonymous||hedefUid.isEmpty||hedefUid==user.uid)return false;
  final kilit='__USER_UID__|$hedefUid|$tur';
  if(!_sosyalIstekIslemleri.add(kilit))return false;
  try{
    Map<String,dynamic> p=<String,dynamic>{};
    try{
      final cached=await FirebaseFirestore.instance.collection('users').doc(user.uid)
          .get(const GetOptions(source:Source.cache));
      p=cached.data()??<String,dynamic>{};
    }catch(_){}

    final sonuc=await Future.wait<dynamic>([
      FirebaseFirestore.instance.collection('users').doc(user.uid)
          .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8)),
      FirebaseFirestore.instance.collection('users').doc(hedefUid)
          .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8)),
      FirebaseFirestore.instance.collection('notifications')
          .where('fromUid',isEqualTo:user.uid)
          .where('toUid',isEqualTo:hedefUid)
          .limit(20).get().timeout(const Duration(seconds:8)),
    ]);
    final benimVeri=(sonuc[0] as DocumentSnapshot<Map<String,dynamic>>).data()??<String,dynamic>{};
    final hedefVeri=(sonuc[1] as DocumentSnapshot<Map<String,dynamic>>).data()??<String,dynamic>{};
    final pairIstekler=sonuc[2] as QuerySnapshot<Map<String,dynamic>>;
    p=<String,dynamic>{...p,...benimVeri};

    final zatenIliski=tur=='follow_request'
      ? List<String>.from(benimVeri['following']??const[]).contains(hedefUid)
        ||List<String>.from(hedefVeri['followers']??const[]).contains(user.uid)
      : tur=='friend_request'
        ? List<String>.from(benimVeri['friends']??const[]).contains(hedefUid)
          ||List<String>.from(hedefVeri['friends']??const[]).contains(user.uid)
        : false;
    if(zatenIliski)return false;

    if(pairIstekler.docs.any((d)=>d.data()['type']==tur&&d.data()['status']=='pending'))return false;

    final emailAdi=(user.email??'').split('@').first.trim();
    final ad=(p['displayName']??p['username']??user.displayName??(emailAdi.isNotEmpty?emailAdi:'NgelX kullanıcısı')).toString();
    final foto=(p['photoUrl']??user.photoURL??'').toString();
    await FirebaseFirestore.instance.collection('notifications').add({
      'toUid':hedefUid,'fromUid':user.uid,'type':tur,
      'senderName':ad,'photoUrl':foto,'text':metin,
      'status':'pending','read':false,
      'createdAt':FieldValue.serverTimestamp(),
      'clientCreatedAt':Timestamp.now(),
    }).timeout(const Duration(seconds:10));
    return true;
  }finally{
    _sosyalIstekIslemleri.remove(kilit);
  }
}

'''.replace("__USER_UID__", "$"+"{user.uid}")

main=between(main,"Future<bool> sosyalIstekGonder({","Future<void> sosyalIstekIptalEt",new_social,"social request function")

main=one(main,
"if(ben==null||gonderen.isEmpty||veri['status']!='pending')return;\n\n    String benimAd='NgelX kullanıcısı',benimFoto='';",
"""if(ben==null||gonderen.isEmpty||veri['status']!='pending')return;

    final ayniBekleyen=<QueryDocumentSnapshot<Map<String,dynamic>>>[];
    try{
      final q=await FirebaseFirestore.instance.collection('notifications')
          .where('toUid',isEqualTo:ben)
          .where('fromUid',isEqualTo:gonderen)
          .limit(20).get().timeout(const Duration(seconds:6));
      for(final istek in q.docs){
        final x=istek.data();
        if((x['type']??'').toString()==tur&&x['status']=='pending')ayniBekleyen.add(istek);
      }
    }catch(_){}
    if(!ayniBekleyen.any((x)=>x.reference.path==belge.reference.path))ayniBekleyen.add(belge);

    String benimAd='NgelX kullanıcısı',benimFoto='';""","duplicate request lookup")

main=one(main,
"""    final toplu=FirebaseFirestore.instance.batch();
    toplu.update(belge.reference,{
      'status':kabul?'accepted':'rejected',
      'read':true,
      'answeredAt':FieldValue.serverTimestamp(),
    });
""",
"""    final toplu=FirebaseFirestore.instance.batch();
    for(final istek in ayniBekleyen){
      toplu.update(istek.reference,{
        'status':kabul?'accepted':'rejected',
        'read':true,
        'answeredAt':FieldValue.serverTimestamp(),
      });
    }
""","resolve duplicates")

main=one(main,
"""final foto = (v['photoUrl'] ?? '').toString();
          final arkadaslar = Set<String>.from(List<dynamic>.from(benimVerim['friends'] ?? []));
          final gizli = v['privateAccount'] == true;""",
"""final foto = (v['photoUrl'] ?? '').toString();
          final arkadaslar = Set<String>.from(List<dynamic>.from(benimVerim['friends'] ?? []));
          if(me!=null&&List<String>.from(v['friends']??const[]).contains(me))arkadaslar.add(uid);
          final gizli = v['privateAccount'] == true;""","bilateral profile friendship")

main=one(main,
"final takipte=List<String>.from(benSnap.data?.data()?['following']??const[]).contains(uid);",
"""final benimTakipEttiklerim=List<String>.from(benSnap.data?.data()?['following']??const[]);
                      final hedefTakipcileri=List<String>.from(v['followers']??const[]);
                      final takipte=benimTakipEttiklerim.contains(uid)||(me!=null&&hedefTakipcileri.contains(me));""","bilateral follow button")

main=one(main,
"final gidenAkis=me==null?null:FirebaseFirestore.instance.collection('notifications').where('fromUid',isEqualTo:me).limit(100).snapshots();",
"""final gidenAkis=me==null?null:FirebaseFirestore.instance.collection('notifications')
                          .where('fromUid',isEqualTo:me)
                          .where('toUid',isEqualTo:uid)
                          .limit(20).snapshots();""","pair follow stream")

main=one(main,
"final arkadas=List<String>.from(benSnap.data?.data()?['friends']??const[]).contains(uid);",
"""final benimArkadaslarim=List<String>.from(benSnap.data?.data()?['friends']??const[]);
                    final hedefArkadaslari=List<String>.from(v['friends']??const[]);
                    final arkadas=benimArkadaslarim.contains(uid)||(me!=null&&hedefArkadaslari.contains(me));""","bilateral friend button")

main=one(main,
"stream:me==null?null:FirebaseFirestore.instance.collection('notifications').where('fromUid',isEqualTo:me).limit(100).snapshots(),",
"""stream:me==null?null:FirebaseFirestore.instance.collection('notifications')
                        .where('fromUid',isEqualTo:me)
                        .where('toUid',isEqualTo:uid)
                        .limit(20).snapshots(),""","pair friend stream")

main=one(main,
"""            await sosyalIstekGonder(
              hedefUid:hedefUid,
              tur:'follow_request',
              metin:'Yeni takip isteğin var',
            );
            if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takip isteği gönderildi.')));""",
"""            final gonderildi=await sosyalIstekGonder(
              hedefUid:hedefUid,
              tur:'follow_request',
              metin:'Yeni takip isteğin var',
            );
            if(!gonderildi){
              final gercek=await FirebaseFirestore.instance.collection('users').doc(me)
                  .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
              final zatenTakipte=List<String>.from(gercek.data()?['following']??const[]).contains(hedefUid);
              if(mounted){
                setState((){
                  gonderilenTakipIstekleri.remove(hedefUid);
                  if(zatenTakipte)takipEdilenler.add(hedefUid);
                });
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
                  zatenTakipte?'Bu hesabı zaten takip ediyorsun.':'Takip isteğin zaten bekliyor.',
                )));
              }
              return;
            }
            if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Takip isteği gönderildi.')));""","explore follow result")

main=one(main,
"""      await sosyalIstekGonder(
        hedefUid:hedefUid,
        tur:'friend_request',
        metin:'Yeni arkadaşlık isteğin var',
      );
      if(!mounted)return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arkadaşlık isteği gönderildi.')));""",
"""      final gonderildi=await sosyalIstekGonder(
        hedefUid:hedefUid,
        tur:'friend_request',
        metin:'Yeni arkadaşlık isteğin var',
      );
      if(!gonderildi){
        final gercek=await FirebaseFirestore.instance.collection('users').doc(me)
            .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        final zatenArkadas=List<String>.from(gercek.data()?['friends']??const[]).contains(hedefUid);
        if(mounted){
          setState((){
            gonderilenArkadaslikIstekleri.remove(hedefUid);
            if(zatenArkadas)arkadaslar.add(hedefUid);
          });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(
            zatenArkadas?'Zaten arkadaşsınız.':'Arkadaşlık isteğin zaten bekliyor.',
          )));
        }
        return;
      }
      if(!mounted)return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Arkadaşlık isteği gönderildi.')));""","explore friend result")

main=one(main,"defaultValue: '1.0.76'","defaultValue: '1.0.77'","version name")
main=one(main,"defaultValue: '295'","defaultValue: '296'","build number")
MAIN_PATH.write_text(main,encoding="utf-8")

pub=PUB_PATH.read_text(encoding="utf-8")
pub=one(pub,"version: 1.0.76+295","version: 1.0.77+296","pubspec")
PUB_PATH.write_text(pub,encoding="utf-8")
print("Build 296 social relation patch prepared.")
