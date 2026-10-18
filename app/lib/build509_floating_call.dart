part of 'main.dart';

/// Build509 QA. A native system overlay can only be shown after the user
/// explicitly grants Android's "display over other apps" permission.
/// The overlay itself owns no LiveKit credentials and never starts a camera.
class Ngelx509FloatingCallBridge {
  static const _channel=MethodChannel('com.nnentx.ngelx_app/call_overlay_509');
  static bool _installed=false;

  static void install(){
    if(_installed)return;
    _installed=true;
    _channel.setMethodCallHandler((call)async{
      if(call.method!='floatingCallAction509')return;
      final action=(call.arguments is Map
        ?(call.arguments as Map)['action']:'').toString();
      final name=ngelxCallSession444.room;
      if(name==null)return;
      final detail=ngelx445CallDetails[name];
      final room=_ngelxArkaPlanAramaOdalari[name];
      if(detail==null||room==null||!ngelxCallSession444.background||
         FirebaseAuth.instance.currentUser?.uid!=detail.uid)return;
      if(action=='fullscreen'){
        await hide();
        ngelx448HiddenCallCard.value=null;
        ngelx445CallChanged();
        await ngelx445ReturnCall(name);
      }else if(action=='microphone'){
        if(ngelx446Calls.muted(name))return;
        final local=room.localParticipant;
        if(local==null)return;
        try{await local.setMicrophoneEnabled(!local.isMicrophoneEnabled());}
        catch(_){}
      }else if(action=='speaker'){
        try{
          final speaker=lk.AudioManager.instance.isSpeakerOutputPreferred;
          await lk.AudioManager.instance.setSpeakerOutputPreferred(!speaker);
        }catch(_){}
      }else if(action=='end'){
        await hide();
        await ngelx445EndBackground(name);
      }else if(action=='settings'){
        await requestPermission();
      }
    });
  }

  static Future<bool> hasPermission()async{
    try{return await _channel.invokeMethod<bool>('allowed')??false;}
    catch(_){return false;}
  }
  static Future<void> requestPermission()async{
    install();
    try{
      // Opening Settings is not permission approval.
      await _channel.invokeMethod<void>('request');
    }catch(_){}
  }
  static Future<void> showIfAllowed(String name)async{
    install();
    final detail=ngelx445CallDetails[name],room=_ngelxArkaPlanAramaOdalari[name];
    if(detail==null||room==null||!ngelxCallSession444.background||
       FirebaseAuth.instance.currentUser?.uid!=detail.uid)return;
    if(!await hasPermission())return;
    try{
      await _channel.invokeMethod<bool>('show',<String,String>{
        'title':detail.title,
      });
    }catch(_){}
  }
  static Future<void> hide()async{
    try{await _channel.invokeMethod<void>('hide');}catch(_){}
  }
}
