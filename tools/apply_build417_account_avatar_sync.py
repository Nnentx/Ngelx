#!/usr/bin/env python3
"""Build 417: account-switch card stability and live fallback friends avatars.

Preserves account credentials, auth handling, all social callbacks,
profile appearance and Firestore rules. Fail closed on source drift.
"""
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

def patch_section(a,b,edits):
    global s
    start=s.index(a)
    end=s.index(b,start+len(a))
    segment=s[start:end]
    for label,old,new in edits:
        n=segment.count(old)
        if n!=1:raise SystemExit(f'Build417 {label}: expected 1 marker, got {n}')
        segment=segment.replace(old,new,1)
    s=s[:start]+segment+s[end:]

patch_section(
    'class _HesapDegistirPageState extends State<HesapDegistirPage>',
    '\nclass ',
    [
      ('profile request cache declaration',
       "  bool islem=false;\n\n  String sifreAnahtari",
       """  bool islem=false;
  // Keep one request per email while the account list rebuilds.
  // A user-triggered retry invalidates only the corresponding entry.
  final Map<String,Future<Map<String,dynamic>>> _profilIstekleri={};

  Future<Map<String,dynamic>> _profilYukle(String email)=>
    _profilIstekleri.putIfAbsent(email.trim().toLowerCase(),
      ()=>_profil(email));

  String sifreAnahtari"""),
      ('reset profile cache before accounts refresh',
       "  Future<void> _yukle()async{\n    final h=await SharedPreferences.getInstance();",
       """  Future<void> _yukle()async{
    _profilIstekleri.clear();
    final h=await SharedPreferences.getInstance();"""),
      ('when account uid absent show data load issue not fake name',
       "    if(uid.isEmpty)return <String,dynamic>{'email':email};",
       """    if(uid.isEmpty)return <String,dynamic>{
      'email':email,'profilHatasi':true,
    };"""),
      ('when remote read fails surface retry',
       """    }catch(_){
      return <String,dynamic>{'email':email,'uid':uid};
    }
  }

  Future<String?> _sifreSor""",
       """    }catch(_){
      final aktif=FirebaseAuth.instance.currentUser;
      final ayni=aktif?.uid==uid;
      return <String,dynamic>{
        'email':email,'uid':uid,'profilHatasi':true,
        if(ayni&&aktif?.displayName!=null)'displayName':aktif!.displayName,
        if(ayni&&aktif?.photoURL!=null)'photoUrl':aktif!.photoURL,
      };
    }
  }

  Future<String?> _sifreSor"""),
      ('use stable per-email profile future',
       "          ...hesaplar.map((email)=>FutureBuilder<Map<String,dynamic>>(\n            future:_profil(email),",
       """          ...hesaplar.map((email)=>FutureBuilder<Map<String,dynamic>>(
            future:_profilYukle(email),"""),
      ('show honest avatar loading state',
       """            builder:(_,s){
              final v=s.data??<String,dynamic>{};
              final foto=(v['photoUrl']??'').toString();
              final ad=(v['displayName']??v['username']??email).toString();
              final bu=aktif==email.toLowerCase();""",
       """            builder:(_,s){
              final bu=aktif==email.toLowerCase();
              if(!s.hasData&&s.connectionState==ConnectionState.waiting){
                return NgelXPremiumCard(
                  margin:const EdgeInsets.only(bottom:10),
                  padding:const EdgeInsets.symmetric(horizontal:12,vertical:10),
                  child:Row(children:[
                    const SizedBox(width:46,height:46,
                      child:Center(child:CircularProgressIndicator(
                        strokeWidth:2,color:ngelxPremiumPurple))),
                    const SizedBox(width:11),
                    Expanded(child:Column(
                      crossAxisAlignment:CrossAxisAlignment.start,children:[
                        const Text('Profil yükleniyor...',
                          style:TextStyle(fontWeight:FontWeight.w800)),
                        Text(email,maxLines:1,overflow:TextOverflow.ellipsis,
                          style:const TextStyle(color:ngelxPremiumMuted,fontSize:11.5)),
                      ])),
                  ]),
                );
              }
              final v=s.data??<String,dynamic>{'profilHatasi':true};
              final bilgiEksik=v['profilHatasi']==true||s.hasError;
              final foto=(v['photoUrl']??'').toString();
              final ad=(v['displayName']??v['username']??
                (bilgiEksik?'Profil bilgisi alınamadı':'NgelX kullanıcısı')).toString();"""),
      ('retry one profile instead of repeated automatic fetches',
       """                  if(bu)
                    Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),decoration:BoxDecoration(color:const Color(0xFFE7F9EF),borderRadius:BorderRadius.circular(12)),child:const Text('Bu hesap',style:TextStyle(color:Color(0xFF0A8F48),fontSize:10,fontWeight:FontWeight.w900)))
                  else""",
       """                  if(bilgiEksik)
                    IconButton(
                      tooltip:'Profil bilgisini yeniden yükle',
                      icon:const Icon(Icons.refresh_rounded,color:ngelxPremiumPurple),
                      onPressed:()=>setState(()=>
                        _profilIstekleri.remove(email.trim().toLowerCase())),
                    ),
                  if(bu)
                    Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),decoration:BoxDecoration(color:const Color(0xFFE7F9EF),borderRadius:BorderRadius.circular(12)),child:const Text('Bu hesap',style:TextStyle(color:Color(0xFF0A8F48),fontSize:10,fontWeight:FontWeight.w900)))
                  else"""),
    ],
)

patch_section(
 'class _ArkadaslarPageState extends State<ArkadaslarPage>',
 '\nclass ',
 [
   ('friends live fallback data',
    """    if(bilinen!=null)return satir(bilinen);
    return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      future:FirebaseFirestore.instance.collection('users').doc(id).get(),
      builder:(_,snap){
        if(snap.connectionState==ConnectionState.waiting)return const SizedBox(height:72,child:Center(child:LinearProgressIndicator(minHeight:1,color:mor)));
        return satir(snap.data?.data()??<String,dynamic>{});
      },
    );""",
    """    if(bilinen!=null)return satir(bilinen);
    // Friends outside the initial discovery page should receive live updates
    // too, especially after a profile photo / display-name edit.
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(id).snapshots(),
      builder:(_,snap){
        if(snap.hasError){
          return const ListTile(
            leading:Icon(Icons.info_outline,color:mor),
            title:Text('Arkadaş profili yüklenemedi.'));
        }
        if(!snap.hasData){
          return const SizedBox(height:72,child:Center(
            child:LinearProgressIndicator(minHeight:1,color:mor)));
        }
        if(!snap.data!.exists)return const SizedBox.shrink();
        return satir(snap.data!.data()??<String,dynamic>{});
      },
    );"""),
 ],
)

patch_section(
 'class _ProfilPageState extends State<ProfilPage>',
 '\nclass _ProfilEtkilesimRozeti',
 [
   ('prevent a signed-out profile load from overwriting new session',
    """          .doc(user.uid)
          .get();

      final veri = belge.data();""",
    """          .doc(user.uid)
          .get();

      if(!mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
      final veri = belge.data();"""),
   ('guard obsolete catch from replacing current profile UI',
    """    } catch (_) {
      if (mounted) setState(() => yukleniyor = false);
    }
  }

  Future<void> fotografYukle()""",
    """    } catch (_) {
      if(mounted&&FirebaseAuth.instance.currentUser?.uid==user.uid){
        setState(()=>yukleniyor=false);
      }
    }
  }

  Future<void> fotografYukle()"""),
 ],
)

p.write_text(s,encoding='utf-8')
print('Build 417 profile switching cards, live friend avatar refresh and auth race guards applied.')
