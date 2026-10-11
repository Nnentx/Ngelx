from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
if '// Build440 device QA' in s: raise SystemExit('Build440 already applied')
def replace(old,new,count=1):
 global s
 assert s.count(old)>=count,old[:100]
 s=s.replace(old,new,count)
s="import 'build440_behavior.dart';\n"+s
replace('Set<String> sabitSohbetler={};','Set<String> sabitSohbetler={};\n  Map<String,int> sabitZamanlar440={};\n  int _tercihSurumu440=0;')
replace('final ben=uid;if(ben==null)return;\n    final d=await FirebaseFirestore.instance.collection(\'users\').doc(ben).get();',"final ben=uid;if(ben==null)return;\n    final version=++_tercihSurumu440;\n    final d=await FirebaseFirestore.instance.collection('users').doc(ben).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10));")
replace('if(!mounted||uid!=ben)return;\n    setState((){\n      engellenenler=', 'if(!mounted||uid!=ben||version!=_tercihSurumu440)return;\n    setState((){\n      engellenenler=')
replace("sabitSohbetler=Set<String>.from(List<dynamic>.from(veri['pinnedChats']??const[]));", "sabitSohbetler=Set<String>.from(List<dynamic>.from(veri['pinnedChats']??const[]));\n      sabitZamanlar440=Map<String,dynamic>.from(veri['pinnedChatAt']??const{}).map((k,v)=>MapEntry(k,v is Timestamp?v.millisecondsSinceEpoch:v is num?v.toInt():0));")
replace("try{\n      await FirebaseFirestore.instance.collection('users').doc(ben).set({alan:ekle?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true)).timeout(const Duration(seconds:12));", "try{\n      ++_tercihSurumu440;\n      final now=DateTime.now().millisecondsSinceEpoch;\n      await FirebaseFirestore.instance.collection('users').doc(ben).set({alan:ekle?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId]),if(alan=='pinnedChats')'pinnedChatAt':{chatId:ekle?now:FieldValue.delete()}},SetOptions(merge:true)).timeout(const Duration(seconds:12));\n      if(alan=='pinnedChats'){if(ekle){sabitZamanlar440[chatId]=now;}else{sabitZamanlar440.remove(chatId);}}")
replace("final ap=pinned(a),bp=pinned(b);\n              if(ap!=bp)return ap?-1:1;\n              return (b['time'] as int).compareTo(a['time'] as int);", "final ap=pinned(a),bp=pinned(b);\n              if(ap!=bp)return ap?-1:1;\n              if(ap&&bp)return ngelx440PinCompare((a['doc'] as DocumentSnapshot).id,(b['doc'] as DocumentSnapshot).id,sabitSohbetler,sabitZamanlar440,a['time'] as int,b['time'] as int);\n              return (b['time'] as int).compareTo(a['time'] as int);")
# Update preferences immediately after navigating back from archive.
replace("onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>ArsivSohbetlerPage(uid:ben)));}", "onTap:()async{Navigator.pop(c);await Navigator.push(context,MaterialPageRoute(builder:(_)=>ArsivSohbetlerPage(uid:ben)));if(mounted)await tercihleriGetir();}") if "onTap:(){Navigator.pop(c);Navigator.push(context,MaterialPageRoute(builder:(_)=>ArsivSohbetlerPage(uid:ben)));}" in s else None
# Legacy discovery is optional; permission-denied is not a network failure.
a=s.index('class _ArsivSohbetlerPageState');b=s.index('class ',a+40);part=s[a:b]
part=part.replace("}catch(_){_arsivKismi=true;}","}on FirebaseException catch(e){if(e.code!='permission-denied')_arsivKismi=true;}catch(_){_arsivKismi=true;}",2)
s=s[:a]+part+s[b:]
# Live story surfaces expire without needing a database write.
replace('final docs=s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[];\n      if(docs.isEmpty)return _profilBosDurum(Icons.auto_stories_outlined',"final docs=(s.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]).where((d)=>ngelx440StoryActive(d.data(),DateTime.now())).toList();\n      if(docs.isEmpty)return _profilBosDurum(Icons.auto_stories_outlined")
a=s.index('Widget _profilHikayeGridFinal()');b=s.index('Widget ',a+40);part=s[a:b].replace('StreamBuilder<QuerySnapshot<Map<String,dynamic>>>','NgelXStorySnapshotBuilder');s=s[:a]+part+s[b:]
# Current story strip also rebuilds at its next expiry.
a=s.index('class HikayeSeridi');b=s.index('class ',a+25);part=s[a:b].replace("child:StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(\n        stream:FirebaseFirestore.instance.collection('videos').where('type'","child:NgelXStorySnapshotBuilder(\n        stream:FirebaseFirestore.instance.collection('videos').where('type'").replace("child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(\n        stream:FirebaseFirestore.instance.collection('videos').where('type'","child:NgelXStorySnapshotBuilder(\n        stream:FirebaseFirestore.instance.collection('videos').where('type'");s=s[:a]+part+s[b:]
# Hide ended/stale banners; room heartbeat is written by the connected client.
s=s.replace("((tv['callStatus']??'').toString()=='ringing'||(tv['callStatus']??'').toString()=='active')&&(tv['callRoomName']??'').toString().isNotEmpty", "ngelx440CallJoinable(tv,DateTime.now())")
s=s.replace("((veri['callStatus']??'').toString()=='ringing'||(veri['callStatus']??'').toString()=='active')&&(veri['callRoomName']??'').toString().isNotEmpty", "ngelx440CallJoinable(veri,DateTime.now())")
# Always persist call type when settling its history row.
a=s.index('Future<void> bitir({bool geriDon=true})');b=s.index('@override void dispose()',a);part=s[a:b].replace("'callStatus':finalDurum,", "'callStatus':finalDurum,\n              'callVideo':widget.goruntulu,")
# Settle chat + message atomically under a room guard, before optional system log.
start=part.index('            await widget.aramaRef.set({');end=part.index("            await widget.aramaRef.collection('messages').doc('call_end_'",start)
part=part[:start]+'''            await FirebaseFirestore.instance.runTransaction((tx)async{
              final latest=await tx.get(widget.aramaRef);
              if(latest.data()?['callRoomName']!=widget.roomName)return;
              tx.set(widget.aramaRef,{'callStatus':finalDurum,'callVideo':widget.goruntulu,'callParticipants':FieldValue.arrayRemove([me]),'callEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
              final id=(latest.data()?['callMessageId']??'').toString();
              if(id.isNotEmpty&&latest.data()?['callStartedBy']==me)tx.set(widget.aramaRef.collection('messages').doc(id),{'callStatus':finalDurum,'callVideo':widget.goruntulu,'callEndedAt':FieldValue.serverTimestamp(),'durationSeconds':sureSaniye},SetOptions(merge:true));
            }).timeout(const Duration(seconds:10));
'''+part[end:]
part=part.replace('final d=await widget.aramaRef.get();','final d=await widget.aramaRef.get().timeout(const Duration(seconds:8));')
part=part.replace('}catch(_){}\n\n    await ngelxArkaPlanAramayiTemizle',"}catch(_){if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(_ngelx438Ui('Arama kapandı. Sunucu kaydı güncellenemedi; yeniden dene.'))));}\n\n    await ngelxArkaPlanAramayiTemizle")
s=s[:a]+part+s[b:]
# Heartbeat while connected, stop with existing duration timer on disposal.
replace('if(mounted)setState((){});\n    });\n  }\n\n  Future<void> _izinleriIste()', "if(mounted)setState((){});\n      if(DateTime.now().second%30==0&&!bitiyor)unawaited(FirebaseFirestore.instance.runTransaction((tx)async{final d=await tx.get(widget.aramaRef);if(d.data()?['callRoomName']==widget.roomName&&const {'ringing','active'}.contains(d.data()?['callStatus']))tx.set(widget.aramaRef,{'callHeartbeatAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}).timeout(const Duration(seconds:8)).catchError((_){ }));\n    });\n  }\n\n  Future<void> _izinleriIste()")
s=s.replace("final goruntulu=v['callVideo']==true;\n      final durum=(v['callStatus']??'ringing').toString();", "final sameCall=grupVerisi?['callRoomName']==v['callRoomName']&&v['callRoomName']!=null;\n      final callData=sameCall?(grupVerisi??<String,dynamic>{}):v;\n      final goruntulu=callData['callVideo']==true||(v['text']??'').toString().startsWith('Görüntülü');\n      final storedStatus=(v['callStatus']??'ringing').toString();\n      var durum=storedStatus;\n      if(sameCall){durum=(grupVerisi?['callStatus']??storedStatus).toString();}else if(const {'ringing','active'}.contains(storedStatus)){durum='ended';}")
s=s.replace('super.initState();tercihleriGetir();_eskiGruplariIzle438();','super.initState();unawaited(tercihleriGetir().catchError((_){ }));_eskiGruplariIzle438();')
s+='\n// Build440 device QA\n';p.write_text(s)
Path('app/lib/build440_behavior.dart').write_text(Path('tools/build440_behavior.dart').read_text())
print('Build440 device fixes applied')
