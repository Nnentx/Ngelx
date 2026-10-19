part of 'main.dart';

// Build520: genuine Flutter/LiveKit video remains the media renderer in Android
// system Picture-in-Picture (PiP), instead of a synthetic native placeholder.
// Enter PiP only after the current user deliberately taps the call control.
// Native activity never receives a LiveKit access token or camera permission.
class Ngelx520PipBridge {
  static const _channel=MethodChannel('com.nnentx.ngelx_app/call_pip_520');
  static final ValueNotifier<bool> active=ValueNotifier<bool>(false);
  static bool _installed=false;

  static void install(){
    if(_installed)return;
    _installed=true;
    _channel.setMethodCallHandler((call)async{
      if(call.method=='pipMode520'&&call.arguments is bool){
        active.value=call.arguments as bool;
      }
    });
  }
  static Future<bool> enter()async{
    install();
    try{
      // Android may reject PiP (device, OS, multitasking settings). Never
      // change the call session or claim success until Android returns true.
      final started=await _channel.invokeMethod<bool>('enter')??false;
      if(started)active.value=true;
      return started;
    }catch(_){return false;}
  }
}
