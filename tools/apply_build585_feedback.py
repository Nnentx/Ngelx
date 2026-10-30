"""Patch the exact assembled Build584 app; keep all unrelated screens intact."""
from pathlib import Path
import hashlib
import sys
root = Path(__file__).resolve().parents[1]
app = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'app'
def one(s, old, new):
    assert s.count(old)==1, (s.count(old), old[:100])
    return s.replace(old,new,1)
pub=app/'pubspec.yaml'
if 'version: 1.0.355+585' in pub.read_text():
    print('Build585 already applied');raise SystemExit
assert 'version: 1.0.354+584' in pub.read_text()
f=app/'lib/build565_ludo.dart';s=f.read_text()
s=one(s,'// Build583: manual play always waits for the player to touch a legal pawn.',
      'unawaited(_autoSingleMove574()); // Build585: only one legal choice needs no tap.')
s=one(s,'_startPoll();unawaited(_restoreSound575());',
      '_startPoll();unawaited(_restoreSound575());\n  WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)unawaited(_autoSingleMove574());});')
s=one(s,'if(game.pendingAuto580!=null||_asking||_singleMoveInFlight574',
      'if(widget.watch||_chatOpen||WidgetsBinding.instance.lifecycleState!=AppLifecycleState.resumed||game.pendingAuto580!=null||_asking||_singleMoveInFlight574')
s=one(s,'const Duration(milliseconds:380)','const Duration(milliseconds:220)')
s=one(s,'if(_asking||(autoNow578',
      'if(_chatOpen||WidgetsBinding.instance.lifecycleState!=AppLifecycleState.resumed||game.pendingAuto580!=null||_asking||(autoNow578')
start=s.index('     Column(mainAxisSize:MainAxisSize.min,children:[Ngelx570Clock(')
end=s.index('    ]),const SizedBox(height:8),',start)
s=s[:start]+s[end:]
# Avatar dice remains the sole roll button, the board and Auto remain unchanged.
s=one(s,"else Expanded(child:Text(myTurn&&room['dice']==null&&room['lastRoll'] is Map?'Son zar: ${room['lastRoll']['value']}':widget.watch?'İZLEYİCİ':'KLASİK LUDO',",
      "else Expanded(child:Text(widget.watch?'İZLEYİCİ':'KLASİK LUDO',")
s=one(s,'Duration(milliseconds:math.min(2400,math.max(260,(widget.position-from).abs()*190)))',
      'ngelx585PawnDuration(from,widget.position)')
s=one(s,'class _MovingPawn567 extends StatefulWidget {',
      'Duration ngelx585PawnDuration(int from,int to)=>Duration(milliseconds:math.min(1320,math.max(180,(to-from).abs()*110)));\nclass _MovingPawn567 extends StatefulWidget {')
s=one(s,'Duration(milliseconds:i*190)','Duration(milliseconds:i*110)')
s=one(s,'Duration(milliseconds:math.max(260,steps*190))','Duration(milliseconds:math.max(180,steps*110))')
f.write_text(s)
f=app/'lib/build448_incoming_calls.dart';s=f.read_text()
s=one(s,"await FirebaseFirestore.instance.collection('_call_devices').doc(user.uid).collection('tokens').doc(token.hashCode.toUnsigned(32).toString()).set({'token':token,'uid':user.uid,'updatedAt':FieldValue.serverTimestamp()}).timeout(const Duration(seconds:8));",
      "final saved=await channel.invokeMethod<bool>('registerPushToken585',{'token':token}).timeout(const Duration(seconds:8));\n          if(saved!=true)throw StateError('device_not_registered');")
# Pruned expired devices must allow the next newest valid device to be tried.
s=one(s,"final next=body['nextOffset'];if(next==null)return true;",
      "if(((body['invalidDevices'] as num?)?.toInt()??0)>0&&((body['sent'] as num?)?.toInt()??0)==0)return false;\n        final next=body['nextOffset'];if(next==null)return true;")
f.write_text(s)
k=app/'android/app/src/main/kotlin/com/nnentx/ngelx_app'
f=k/'IncomingCallService.kt';s=f.read_text()
s=one(s,'class IncomingCallService : FirebaseMessagingService() {',
      'class IncomingCallService : FirebaseMessagingService() {\n    override fun onNewToken(token: String) {\n        super.onNewToken(token)\n        PushRegistration585.save(token)\n    }')
f.write_text(s)
f=k/'MainActivity.kt';s=f.read_text()
s=one(s,'                    "getPushToken" ->',
      '                    "registerPushToken585" -> {\n                        val token = call.argument<String>("token").orEmpty()\n                        PushRegistration585.save(token) { saved -> runOnUiThread { result.success(saved) } }\n                    }\n                    "getPushToken" ->')
f.write_text(s)
(k/'PushRegistration585.kt').write_text((root/'tools/build585_push_registration.kt').read_text())
f=app/'android/app/build.gradle.kts';s=f.read_text()
s=one(s,'    implementation("com.google.firebase:firebase-auth")',
      '    implementation("com.google.firebase:firebase-auth")\n    implementation("com.google.firebase:firebase-firestore")')
f.write_text(s)
pub.write_text(one(pub.read_text(),'version: 1.0.354+584','version: 1.0.355+585'))
print('Build585 Ludo and background token registration fixes applied')
