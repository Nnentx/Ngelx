from pathlib import Path
TAG='// Build549 quota-aware call recovery'
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError(f'Build549 unique anchor {a[:100]!r}: {s.count(a)}')
 return s.replace(a,b,1)
def main_source(s):
 if TAG in s:return s
 s=once(s,"import 'build548_policy.dart';","import 'build548_policy.dart';\nimport 'build549_call_policy.dart';")
 s=once(s,"part 'build548_widgets.dart';","part 'build548_widgets.dart';\npart 'build549_call_recovery.dart';")
 # One shared monotonic gate spans foreground/background surfaces.
 old="      if(DateTime.now().second%30==0&&!bitiyor)unawaited(FirebaseFirestore.instance.runTransaction((tx)async{final d=await tx.get(widget.aramaRef);if(d.data()?['callRoomName']==widget.roomName&&const {'ringing','active'}.contains(d.data()?['callStatus']))tx.set(widget.aramaRef,{'callHeartbeatAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}).timeout(const Duration(seconds:8)).catchError((_){ }));"
 s=once(s,old,"      if(!bitiyor)unawaited(ngelx549Heartbeat(widget.aramaRef,widget.roomName,alive:()=>_alive444&&oda!=null&&!kucultuluyor));")
 a=s.index('class _NgelXAramaPageState ');b=s.index('\nclass GrupBilgiPage ',a);call=s[a:b]
 call=once(call,'    });\n    final arkaPlan=ngelxArkaPlanAramayiGeriAl(widget.roomName);',"    },onError:(Object error){debugPrint('Call status unavailable: $error');});\n    final arkaPlan=ngelxArkaPlanAramayiGeriAl(widget.roomName);")
 call=once(call,'  String? hata,bitisDurumu;','  bool _callQuota549=false;\n  String? hata,bitisDurumu;')
 call=once(call,'        final current=await widget.aramaRef.get();\n        final call=current.data();','        final call=initial444.data();')
 call=once(call,'    if(!_alive444||_connectInFlight444)return;', '    if(!_alive444||_connectInFlight444)return;\n    _callQuota549=false;')
 call=once(call,'if(_alive444&&yeniden&&!rejoinBlocked535&&yenidenBaglanmaDenemesi<3)', 'if(_alive444&&yeniden&&!rejoinBlocked535&&!ngelx549Quota(e)&&yenidenBaglanmaDenemesi<3)')
 call=once(call,"hata=e.toString().replaceFirst('Exception: ','');", "_callQuota549=ngelx549Quota(e);hata=ngelx549CallError(e);")
 call=once(call,"TextButton(onPressed:openAppSettings,child:const Text('Kamera / mikrofon izinlerini aç')),", "if(!_callQuota549)TextButton(onPressed:openAppSettings,child:const Text('Kamera / mikrofon izinlerini aç')),")
 s=s[:a]+call+s[b:]
 s=once(s,"if(mounted)ngelxDurumMesaji(context,'Önceki ayrılma kaydı gönderilemedi. Bağlantını kontrol edip tekrar dene.',tip:'hata');", "if(mounted)ngelxDurumMesaji(context,ngelx549LastLeaveError!=null?ngelx549CallError(ngelx549LastLeaveError!):'Önceki ayrılma kaydı henüz tamamlanamadı. Lütfen tekrar dene.',tip:'uyari');")
 # The pending-leave preflight's server read previously escaped all UI catches.
 a=s.index('  Future<void> aktifGrupAramasinaKatil(');b=s.index('\n  Future<void> aramaBaslat(',a);join=s[a:b]
 pos=join.index('    if(!await ngelx542PrepareManualJoin')
 join=join[:pos]+'    try{\n'+join[pos:]
 end=join.rfind('\n  }');join=join[:end]+"\n    }catch(error){if(mounted)ngelxDurumMesaji(context,ngelx549CallError(error),tip:'uyari');}"+join[end:]
 join=once(join,"    }catch(_){\n      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Aktif aramaya katılınamadı.')));", "    }catch(error){\n      if(mounted)ngelxDurumMesaji(context,ngelx549CallError(error),tip:'uyari');")
 s=s[:a]+join+s[b:]
 s=once(s,"final metin=e.code=='permission-denied'", "final metin=ngelx549Quota(e)?ngelx549CallError(e):e.code=='permission-denied'")
 return s+'\n'+TAG+'\n'
def incoming_source(s):
 if TAG in s:return s
 s=once(s,'  bool _verifyingMissing469=false;', '  final Set<String> _dismissed549={};\n  bool _verifyingMissing469=false;')
 s=once(s,'      _account455=user?.uid;', '      _dismissed549.clear();\n      _account455=user?.uid;')
 s=once(s,"          final v=d.data(),t=v['callCreatedAt'];", "          final v=d.data(),t=v['callCreatedAt'];\n          if(_dismissed549.contains((v['callRoomName']??'').toString()))return false;")
 # Stream quota errors are not call-end events. Keep RTC ownership intact.
 a=s.index('  Future<void> _action(');b=s.index('\n}\nfinal ngelx448Incoming',a)
 s=s[:a]+Path('tools/build549_incoming_action.dart').read_text().rstrip()+s[b:]
 return s+'\n'+TAG+'\n'
def pending_source(s):
 if TAG in s:return s
 s=once(s,'  while(_leaveInFlight542.contains(key))', "  final retryAfter=_leaveRetryAfter549[key];\n  if(retryAfter!=null&&DateTime.now().isBefore(retryAfter))throw FirebaseException(plugin:'cloud_firestore',code:'resource-exhausted');\n  while(_leaveInFlight542.contains(key))")
 s=once(s,'  }finally{_leaveInFlight542.remove(key);}', "  }catch(error){\n    if(ngelx549Quota(error)){\n      _leaveRetryAfter549[key]=DateTime.now().add(const Duration(minutes:2));\n      ngelx549LastLeaveError=error;\n    }\n    rethrow;\n  }finally{_leaveInFlight542.remove(key);}")
 s=s.replace('await prefs.remove(key);','await prefs.remove(key);_leaveRetryAfter549.remove(key);')
 s=once(s,"try{await _ngelx542AttemptLeave(key,prefs);}catch(error){debugPrint('Pending self-leave retained: $error');}", "try{await _ngelx542AttemptLeave(key,prefs);}catch(error){debugPrint('Pending self-leave retained: $error');if(ngelx549Quota(error))break;}")
 s=once(s,"  final key='pending_call_leave_542_${uid}_$room';\n  if(prefs.containsKey(key)){", "  final key='pending_call_leave_542_${uid}_$room';\n  ngelx549LastLeaveError=null;\n  if(prefs.containsKey(key)){")
 s=once(s,'try{await _ngelx542AttemptLeave(key,prefs);}catch(_){return false;}', 'try{await _ngelx542AttemptLeave(key,prefs);}catch(error){ngelx549LastLeaveError=error;return false;}')
 return s+'\n'+TAG+'\n'
def overlay_source(s):
 if TAG in s:return s
 a=s.index('          unawaited(FirebaseFirestore.instance.runTransaction((tx)async{',s.index('class _Ngelx445CallOverlayState'))
 b=s.index('        }\n      }\n    });',a)
 s=s[:a]+"          unawaited(ngelx549Heartbeat(detail.ref,name,alive:()=>FirebaseAuth.instance.currentUser?.uid==detail.uid&&_ngelxArkaPlanAramaOdalari.containsKey(name)));\n"+s[b:]
 return s+'\n'+TAG+'\n'
if __name__=='__main__':
 for name,fn in [('main.dart',main_source),('build448_incoming_calls.dart',incoming_source),('build542_pending_leave.dart',pending_source),('build445_inbox_model.dart',overlay_source)]:
  p=Path('app/lib')/name;p.write_text(fn(p.read_text()))
 for name in ['call_policy','call_recovery']:(Path('app/lib')/('build549_'+name+'.dart')).write_text(Path('tools/build549_'+name+'.dart').read_text())
