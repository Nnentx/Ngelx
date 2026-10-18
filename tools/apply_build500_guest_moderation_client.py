#!/usr/bin/env python3
"""Build500 QA: connect guest host actions exclusively to an authenticated server API.

Run AFTER the Build489 and Build490 source transformations, and before Flutter
analysis/build. The previous Flutter-side guest policy stays read-only.
When no HTTPS moderation service is configured, actions fail closed.
"""
from pathlib import Path
import re

FILE = Path("app/lib/live_broadcast_studio.dart")
MAIN = Path("app/lib/main.dart")
MARKER = "// Build500: authenticated LiveKit guest moderation; no client Firestore writes"

NEW_METHOD = r"""  // Build500: authenticated LiveKit guest moderation; no client Firestore writes.
  final Set<String> _guestModerationPending500=<String>{};

  Future<void> _hostGuestAction489(String uid,String action)async{
    if(!mounted||!widget.yayinSahibi||uid.isEmpty||uid==widget.ownerId||
        FirebaseAuth.instance.currentUser?.uid!=widget.ownerId||
        !const ['mute','unmute','kick'].contains(action)||
        _guestModerationPending500.contains(uid))return;

    // Intentionally empty in ordinary QA APKs. Never fall back to client-only
    // Firestore updates or claim that the remote guest was actually muted.
    const endpoint=String.fromEnvironment('NGELX_LIVEKIT_GUEST_MODERATION_URL');
    final uri=Uri.tryParse(endpoint);
    if(uri==null||uri.scheme!='https'||uri.host.isEmpty||uri.userInfo.isNotEmpty||
        uri.fragment.isNotEmpty){
      ngelxDurumMesaji(context,'Güvenli konuk yönetimi bu test sürümünde etkin değil.',tip:'uyari');
      return;
    }

    setState(()=>_guestModerationPending500.add(uid));
    try{
      final user=FirebaseAuth.instance.currentUser;
      if(user==null||user.uid!=widget.ownerId)throw StateError('auth_required');
      final idToken=await user.getIdToken();
      if(idToken==null||idToken.isEmpty||FirebaseAuth.instance.currentUser?.uid!=widget.ownerId){
        throw StateError('auth_expired');
      }
      final response=await Dio(BaseOptions(
        connectTimeout:const Duration(seconds:8),
        sendTimeout:const Duration(seconds:8),
        receiveTimeout:const Duration(seconds:15),
        followRedirects:false,
        validateStatus:(code)=>code!=null&&code>=200&&code<500,
      )).postUri(uri,
        data:{'liveId':widget.belgeId,'guestUid':uid,'action':action},
        options:Options(
          headers:{'Authorization':'Bearer $idToken','Content-Type':'application/json'},
          responseType:ResponseType.json,
        ),
      );
      if(response.statusCode!=200||response.data is! Map||
         response.data['ok']!=true){
        throw StateError('moderation_failed');
      }
      if(mounted)ngelxDurumMesaji(context,
        action=='mute'?'Konuk sessize alındı.':
        action=='kick'?'Konuk yayından çıkarıldı.':'Konuk mikrofon izni açıldı.',
        tip:'basari');
    }catch(_){
      if(mounted)ngelxDurumMesaji(context,
        'Konuk yönetimi sunucuda doğrulanamadı. Yeniden dene.',tip:'hata');
    }finally{
      if(mounted){
        setState(()=>_guestModerationPending500.remove(uid));
      }else{
        _guestModerationPending500.remove(uid);
      }
    }
  }

"""

def replace_once(src, old, new, label):
    n=src.count(old)
    if n!=1:
        raise RuntimeError(f"Build500 {label}: expected exactly one match, found {n}")
    return src.replace(old,new,1)

def transform_live(src):
    if MARKER in src:
        return src
    start=src.index("class _CanliYayinPageState")
    begin=src.index("  Future<void> _hostGuestAction489(",start)
    end=src.index("  Widget _guestTile489(",begin)
    original=src[begin:end]
    for required in (
        "ngelx448GuestAction(context,widget.belgeId,widget.ownerId,uid,'reject')",
        "FirebaseFirestore.instance.runTransaction",
        "'guestAudioMutedUids'",
    ):
        if required not in original:
            raise RuntimeError("Build500 original host-only action changed: "+required)
    out=src[:begin]+NEW_METHOD+src[end:]
    if "_guestTile489(" not in out or "_guestAudioPolicySub489" not in out:
        raise RuntimeError("Build500 live guest controls missing")
    return out

def transform_main(src):
    if "import 'package:dio/dio.dart';" in src or 'import "package:dio/dio.dart";' in src:
        return src
    found=re.search(r"^import\s+['\"]",src,re.MULTILINE)
    if not found: raise RuntimeError("Build500 generated main has no import boundary")
    return src[:found.start()]+"import 'package:dio/dio.dart';\n"+src[found.start():]

def main():
    live=FILE.read_text(encoding="utf-8")
    updated=transform_live(live)
    if updated!=live:FILE.write_text(updated,encoding="utf-8")
    main=MAIN.read_text(encoding="utf-8")
    updated_main=transform_main(main)
    if main!=updated_main:MAIN.write_text(updated_main,encoding="utf-8")
    print("Build500: Firebase-authenticated, HTTPS-only remote moderation; no direct client write")

if __name__=="__main__":
    main()
