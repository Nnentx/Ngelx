from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b,n=None):
 global s
 assert a in s,a[:120]
 if n is not None:assert s.count(a)==n,(a[:80],s.count(a))
 s=s.replace(a,b)
rep("defaultValue: '1.0.210'","defaultValue: '1.0.211'",1)
rep("defaultValue: '435'","defaultValue: '436'",1)
# Fix dotted set keys: aliases belong to the selected participant, not the editor.
a=s.index('class SohbetBilgiPage');b=s.index('\nclass ',a+10);part=s[a:b]
part=part.replace("chat.data()?['nicknames']?[me]","chat.data()?['nicknames']?[uid]")
part=part.replace("'nicknames.$me':sonuc.isEmpty?FieldValue.delete():sonuc,","'nicknames':{uid:sonuc.isEmpty?FieldValue.delete():sonuc},")
part=part.replace("    await FirebaseFirestore.instance.collection('chats').doc(chatId).set({\n      'nicknames'", "    await ngelx436RequireOpen(uid);\n    await FirebaseFirestore.instance.collection('chats').doc(chatId).set({\n      'nicknames'",1)
anchor="    },SetOptions(merge:true));\n  }\n  Future<void> ozellestir"
assert anchor in part
part=part.replace(anchor,"""    },SetOptions(merge:true));
    await FirebaseFirestore.instance.collection('chats').doc(chatId).collection('messages').add({
      'senderId':me,'actorUid':me,'type':'system','systemAction':'nickname_changed',
      'targetUid':uid,'targetName':ad,'newNickname':sonuc,
      'text':sonuc.isEmpty?'$ad için takma ad kaldırıldı':'$ad için takma ad "$sonuc" olarak değiştirildi',
      'createdAt':FieldValue.serverTimestamp(),'clientCreatedAt':Timestamp.now(),
    });
  }
  Future<void> ozellestir""",1)
part=part.replace("    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;\n    final ref=FirebaseFirestore.instance.collection('chats').doc(chatId);","    final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;\n    await ngelx436RequireOpen(uid);\n    final ref=FirebaseFirestore.instance.collection('chats').doc(chatId);",1)
part=part.replace('    if(secim==null)return;\n\n    if(secim is String','    if(secim==null)return;\n    await ngelx436RequireOpen(uid);\n\n    if(secim is String',1)
part=part.replace("{'theme':secim,'backgroundVersion'","{'theme':secim,'backgroundUrl':'','backgroundUrl_$me':'','backgroundUrl_$uid':'','backgroundVersion'")
part=part.replace("(nicks[me]??'')","(nicks[uid]??'')")
part=part.replace("Center(child:AktiflikDurumuYazisi(uid:uid))","Ngelx436BlockView(other:uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():Center(child:AktiflikDurumuYazisi(uid:uid)))")
# Guard info actions and expose actual block state live.
part=part.replace("  Future<void> engelle(BuildContext context)async{","  Future<void> engelle(BuildContext context)async{\n    final me=FirebaseAuth.instance.currentUser?.uid;\n    if(me==null)return;\n    final mine=await FirebaseFirestore.instance.collection('users').doc(me).get(const GetOptions(source:Source.server));\n    if(List<String>.from(mine.data()?['blocked']??const[]).contains(uid)){await ngelxEngeliKaldir(context,uid,hedefAdi:ad);return;}")
part=part.replace("_satir(Icons.block_rounded,'Engelle',()=>engelle(context),renk:Colors.black)","Ngelx436BlockView(other:uid,builder:(mine,theirs)=>_satir(Icons.block_rounded,mine?'Engellemeyi kaldır':'Engelle',()=>engelle(context),renk:Colors.black))")
part=part.replace("_kisa(Icons.text_fields_rounded,'Takma ad',()=>takmaAd(context))","Ngelx436BlockView(other:uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():_kisa(Icons.text_fields_rounded,'Takma ad',()=>_guvenli(context,()=>takmaAd(context))))")
part=part.replace("_kisa(Icons.palette_rounded,'Özelleştir',()=>ozellestir(context))","Ngelx436BlockView(other:uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():_kisa(Icons.palette_rounded,'Özelleştir',()=>_guvenli(context,()=>ozellestir(context))))")
part=part.replace("_kisa(arkadas?Icons.people_alt_rounded:Icons.person_add_alt_1_rounded,arkadas?'Arkadaş':'Arkadaş ekle',arkadas?(){}:()=>arkadasEkle(context))","Ngelx436BlockView(other:uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():_kisa(arkadas?Icons.people_alt_rounded:Icons.person_add_alt_1_rounded,arkadas?'Arkadaş':'Arkadaş ekle',arkadas?(){}:()=>_guvenli(context,()=>arkadasEkle(context))))")
part=part.replace('  Future<void> arkadasEkle(BuildContext context)async{','''  Future<void> _guvenli(BuildContext context,Future<void> Function() action)async{
    try{await action();}catch(e){if(context.mounted)ngelxDurumMesaji(context,ngelx436Error(e),tip:'hata');}
  }
  Future<void> arkadasEkle(BuildContext context)async{
    await ngelx436RequireOpen(uid);''')
s=s[:a]+part+s[b:]
# A blocked relation is a distinct result, never an already-pending request.
rep("if(List<String>.from(benimVeri['blocked']??const[]).contains(hedefUid))return false;","if(List<String>.from(benimVeri['blocked']??const[]).contains(hedefUid))throw StateError('Engel varken istek gönderilemez.');",1)
rep("if(List<String>.from(hedefVeri['blocked']??const[]).contains(user.uid))return false;","if(List<String>.from(hedefVeri['blocked']??const[]).contains(user.uid))throw StateError('Bu hesaba istek gönderilemez.');",1)
# Canonical request is authoritative; missing notification never cancels a valid pending request.
a=s.index('    Future<bool> aktifBekleyenIstek');b=s.index('\n    if(mevcut.exists',a)
s=s[:a]+"    Future<bool> aktifBekleyenIstek(DocumentSnapshot<Map<String,dynamic>> d)async=>d.exists&&d.data()?['status']=='pending';\n"+s[b:]
# Presence always hides for blocked pairs, including profile/info/avatar routes.
rep('      final etiket=_etiket(v);','      final etiket=_etiket(v);',1)
rep("      return Text(\n        etiket,","      return Ngelx436BlockView(other:widget.uid,builder:(mine,theirs)=>(mine||theirs)?const SizedBox.shrink():Text(\n        etiket,",1)
rep("          fontWeight:online?FontWeight.w700:FontWeight.w500,\n        ),\n      );","          fontWeight:online?FontWeight.w700:FontWeight.w500,\n        ),\n      ));",1)
# Video compression runs only for oversized intro files; original remains untouched.
rep("      final boyut=await dosya.length();\n      if(boyut>35*1024*1024)throw Exception('Tanıtım videosu 35 MB’den küçük olmalı.');","""      XFile yuklenecek=dosya;
      if(await dosya.length()>35*1024*1024){
        final bilgi=await VideoCompress.compressVideo(dosya.path,quality:VideoQuality.MediumQuality,deleteOrigin:false,includeAudio:true);
        if(bilgi?.path!=null)yuklenecek=XFile(bilgi!.path!);
      }
      if(await yuklenecek.length()>35*1024*1024)throw StateError('Video sıkıştırıldıktan sonra da 35 MB sınırını aşıyor. Daha kısa bir video seç.');""",1)
anchor="kind:'profile-intros',"
a=s.index(anchor);b=s.rfind('dosya:dosya,',0,a);assert b>=0;s=s[:b]+s[b:].replace('dosya:dosya,','dosya:yuklenecek,',1)
rep("content:Text('Tanıtım videosu yüklenemedi: '+e.toString())","content:Text(e is StateError?e.message.toString():'Tanıtım videosu yüklenemedi. '+ngelx436Error(e))",1)
# Preserve retry only for transient errors; distinguish authorization failures.
rep("        }catch(_){\n          if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Silme tamamlanamadı. Bağlantı gelince tekrar denenecek.')));\n        }","        }catch(e){\n          if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(ngelx436Error(e))));\n        }",2)
rep("  }catch(_){if(!retry)rethrow;}finally{_ngelx435SilmeKilidi.remove(lock);}","""  }catch(e){
    if(e is FirebaseException&&(e.code=='permission-denied'||e.code=='invalid-argument'||e.code=='not-found'))await _ngelx435QueueChange(key,ref.path,add:false);
    if(!retry)rethrow;
  }finally{_ngelx435SilmeKilidi.remove(lock);}""",1)
# Preserve exact source values, including null, for the server's immutable cleanup manifest.
rep("'cleanupMediaUrls':ngelx435MedyaListesi(v),'mediaCleanupState':'pending',","'cleanupMediaUrls':[for(final field in ngelx435MedyaAlanlari)v.containsKey(field)?v[field]:''],'mediaCleanupState':'pending',",1)
s+='\n'+Path('tools/build436_guards.dart').read_text();p.write_text(s)
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.210+435','version: 1.0.211+436'))
print('Build436 device test fixes applied')
