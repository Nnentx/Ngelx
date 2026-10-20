#!/usr/bin/env python3
"""Incremental Build543 transforms after the verified Build542 pipeline; no deployment."""
from pathlib import Path
TAG='// Build543 community and system PiP'
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError('Build543 anchor mismatch '+a[:110]+': '+str(s.count(a)))
 return s.replace(a,b,1)
def main(s):
 s=once(s,"part 'build542_pending_leave.dart';", "part 'build542_pending_leave.dart';\npart 'build543_pip_participants.dart';\npart 'build543_community_admin.dart';\npart 'build543_group_call_join.dart';")
 s=once(s,'ngelx542GroupTrailing(v,','ngelx542GroupTrailing(d.id,v,')
 s=once(s,'const Ngelx541GlobalCallStrip()]','const Ngelx541GlobalCallStrip(),const Ngelx543GlobalPip()]')
 a=s.index('class _NgelXAramaPageState');b=s.index('class GrupBilgiPage',a)
 body=s[a:b]
 body=once(body,'  Future<void> _stopLocal444()async{','  Future<void> _stopLocal444()async{\n    Ngelx543PipCall.clear(widget.roomName);')
 body=once(body,'      oda=r;','      oda=r;\n      _registerPip543();')
 body=once(body,'      oda=arkaPlan.room;','      oda=arkaPlan.room;\n      _registerPip543();')
 a1=body.index('  Future<void> _aramaEkraniniKucult()async{');b1=body.index('  @override Widget build',a1)
 minimize=body[a1:b1]
 minimize=once(minimize,'      oda=null;','      Ngelx543PipCall.clear(widget.roomName);\n      oda=null;')
 body=body[:a1]+minimize+body[b1:]
 body=once(body,'  @override void dispose(){','  @override void dispose(){\n    Ngelx543PipCall.clear(widget.roomName);')
 a1=body.index('  Widget _ngelx520PipVideo(){');b1=body.index('  Widget _efektliVideo',a1)
 body=body[:a1]+'''  void _registerPip543(){
    Ngelx543PipCall.bind(oda,widget.roomName,widget.baslik,(action)async{
      if(!mounted||bitiyor||oda==null)return;
      if(action=='end'){await bitir();}
      else if(action=='microphone'){await mikrofonDegistir();}
      else if(action=='speaker'){await hoparlorDegistir();}
    });
  }
  Widget _ngelx520PipVideo(){
    final room=oda;
    return room==null?const ColoredBox(color:Colors.black):Ngelx543MiniCall(room:room,title:widget.baslik);
  }

'''+body[b1:]
 s=s[:a]+body+s[b:]
 return s

def bridge(s):
 s=once(s,'        active.value=call.arguments as bool;', '        active.value=call.arguments as bool;\n        if(!active.value)unawaited(Ngelx543PipCall.restoreAfterExpand());')
 return once(s,"      if(call.method=='pipMode520'&&call.arguments is bool){", """      if(call.method=='background543'){
        await Ngelx543PipCall.background();return;
      }
      if(call.method=='pipAction543'&&call.arguments is String){
        try{await Ngelx543PipCall.action(call.arguments as String);}catch(_){}
        return;
      }
      if(call.method=='pipMode520'&&call.arguments is bool){""")

def behavior(s):
 a=s.index("  final stamp=data['callHeartbeatAt']");b=s.index('\n}',a)
 return s[:a]+'''  // A previous call's heartbeat can survive into a newly started call.
  // Select the newest server timestamp, never let that stale field mask creation.
  final stamps=<Timestamp>[for(final key in ['callCreatedAt','callConnectedAt','callHeartbeatAt'])if(data[key] is Timestamp)data[key] as Timestamp];
  if(stamps.isEmpty)return false;
  stamps.sort((a,b)=>b.compareTo(a));
  final stamp=stamps.first;
  final age=now.difference(stamp.toDate());
  return age>=const Duration(seconds:-30)&&age<const Duration(minutes:2);
'''+s[b:]

def dashboard(s):
 a=s.index('class _Ngelx456DashboardState');b=s.index('  Widget card(',a)
 body=s[a:b]
 body=once(body,"      'Üyelik istekleri': root", "      if(_communityAdmin450(widget.value)) 'Üyelik istekleri': root")
 a1=body.index('    final values = await Future.wait(')
 body=body[:a1]+'''    final result=<String,int>{};
    await Future.wait(queries.entries.map((entry)async{
      try{result[entry.key]=(await entry.value.count().get().timeout(const Duration(seconds:12))).count??0;}
      catch(_){result[entry.key]=-1;}
    }));
    return result;
  }

'''
 s=s[:a]+body+s[b:]
 s=once(s,"s.hasError ? '—' : (s.data?[key] ?? '…').toString();", "s.hasError||s.data?[key]==-1 ? '—' : (s.data?[key] ?? '…').toString();")
 s=once(s,"          TextButton.icon(\n            onPressed: () => setState(() => counts = load()),", """          if(s.data?.values.contains(-1)==true)
            const Padding(padding:EdgeInsets.all(10),child:Text('Bazı sayaçlar yüklenemedi. Diğer yönetim araçlarını kullanabilir, sayaçları yeniden deneyebilirsin.',style:TextStyle(color:Colors.black54,fontSize:12))),
          if(v['founderId']==_communityUid450&&_communityMember450(v))
            ListTile(leading:const Icon(Icons.delete_forever,color:Colors.red),
              title:const Text('Topluluğu tamamen sil',style:TextStyle(color:Colors.red,fontWeight:FontWeight.w700)),
              subtitle:const Text('Topluluk ve bağlı kayıtları kalıcı olarak silinir'),
              onTap:()=>ngelx543DeleteCommunity(c,widget.id)),
          TextButton.icon(
            onPressed: () => setState(() => counts = load()),""")
 return s

def community(s):
 s=once(s,"Topluluk sunucusu bu işleme izin vermedi. Kurucu/yönetici yetkisi ve canlı Firebase güvenlik kuralları kontrol edilmeli.","Bu işlem için topluluk yetkisi doğrulanamadı. Tekrar dene; sorun sürerse Destek ve hata bildir bölümünden ilet.")
 # Validate editable form dynamically instead of leaving a disabled save button
 # fixed at the initial value of a short legacy name.
 s=once(s,"onPressed: n.text.trim().length < 3\n                ? null\n                : () => Navigator.pop(c, true),", "onPressed: () {if(n.text.trim().length>=3)Navigator.pop(c,true);else ScaffoldMessenger.of(c).showSnackBar(const SnackBar(content:Text('Topluluk adı en az 3 karakter olmalı.')));},")
 # A deleted root must not leave the management route spinning forever.
 s=once(s,"        if (v == null) return const Center(child: CircularProgressIndicator());\n        if (!ngelx456Moderator(v))", "        if(s.hasError)return ngelx432YuklemeHatasi(()=>setState((){}),'Topluluk yüklenemedi.');\n        if(s.hasData&&!s.data!.exists)return const Center(child:Text('Bu topluluk artık mevcut değil.'));\n        if (v == null) return const Center(child: CircularProgressIndicator());\n        if (!ngelx456Moderator(v))")
 return s

def inbox(s):
 a=s.index('Widget ngelx542GroupTrailing(');b=s.index('\n// Build542 call refinements',a)
 s=once(s,'  await ngelxArkaPlanAramayiTemizle(name);\n  if(detail==null||me!=detail.uid)return;',"  if(detail==null||me==null||me!=detail.uid)return;\n  await ngelxArkaPlanAramayiTemizle(name);\n  if(name.startsWith('group_')){await ngelx542LeaveGroupCall(detail.ref,name,me,video:detail.video,displayName:FirebaseAuth.instance.currentUser?.displayName);return;}")
 a=s.index('Widget ngelx542GroupTrailing(');b=s.index('\n// Build542 call refinements',a)
 return s[:a]+"Widget ngelx542GroupTrailing(String chatId,Map<String,dynamic> chat,VoidCallback join,Widget usual)=>Ngelx543GroupJoin(key:ValueKey('call-join-$chatId'),chatId:chatId,seed:chat,join:join,usual:usual);\n"+s[b:]

def native(s):
 s=once(s,'import android.app.PictureInPictureParams\n','import android.app.PictureInPictureParams\nimport android.app.RemoteAction\nimport android.app.PendingIntent\nimport android.graphics.drawable.Icon\n')
 s=once(s,'        pipMethodChannel520=pip520','        pipMethodChannel520=pip520\n        Ngelx543PipEvents.channel=pip520')
 s=once(s,'.setAspectRatio(Rational(16,9)).build()', '.setAspectRatio(Rational(11,10)).setActions(pipActions543()).build()')
 s=once(s,'    override fun onPictureInPictureModeChanged(','''    private fun pipActions543(): List<RemoteAction> {
        val actions=listOf(
            Triple("microphone","Mikrofon",android.R.drawable.ic_btn_speak_now),
            Triple("speaker","Hoparlör",android.R.drawable.ic_lock_silent_mode_off),
            Triple("end","Bitir",android.R.drawable.ic_menu_close_clear_cancel))
        return actions.mapIndexed { index, item ->
            val intent=Intent(this,Ngelx543PipReceiver::class.java).apply { action="com.nnentx.ngelx_app.PIP543";putExtra("action543",item.first) }
            val pending=PendingIntent.getBroadcast(this,5430+index,intent,PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            RemoteAction(Icon.createWithResource(this,item.third),item.second,item.second,pending)
        }
    }
    override fun onUserLeaveHint(){
        super.onUserLeaveHint()
        if(Build.VERSION.SDK_INT>=26&&CallAudioService.active&&!isInPictureInPictureMode){
            pipMethodChannel520?.invokeMethod("background543",null)
        }
    }
    override fun onPictureInPictureModeChanged(''')
 s=once(s,'                else -> result.notImplemented()\n            }\n        }\n        // Build509:', '                \"endPip543\" -> { result.success(null); if(Build.VERSION.SDK_INT>=26&&isInPictureInPictureMode)finish() }\n                else -> result.notImplemented()\n            }\n        }\n        // Build509:')
 s=once(s,'        pipMethodChannel520=null','        Ngelx543PipEvents.channel=null\n        pipMethodChannel520=null')
 return s

def manifest(s):
 return once(s,'    </application>', '''        <receiver android:name=".Ngelx543PipReceiver" android:exported="false" />
    </application>''')
TRANSFORMS={'app/lib/main.dart':main,'app/lib/build445_inbox_model.dart':inbox,'app/lib/build520_livekit_pip.dart':bridge,'app/lib/build440_behavior.dart':behavior,'app/lib/build456_widgets.dart':dashboard,'app/lib/community450.dart':community,'app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt':native,'app/android/app/src/main/AndroidManifest.xml':manifest}
def transform(s,fn):return s if TAG in s else fn(s)+'\n'+TAG+'\n' if fn!=manifest else (s if '<!-- Build543 -->' in s else fn(s)+'\n<!-- Build543 -->\n')
if __name__=='__main__':
 changes=[]
 for name,fn in TRANSFORMS.items():
  p=Path(name);s=p.read_text();out=transform(s,fn);assert transform(out,fn)==out;changes.append((p,out))
 for p,s in changes:p.write_text(s)
 print('Build543 applied atomically; no production deployment')
