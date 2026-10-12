"""Apply capture protection after the Build442 generated source pipeline."""
from pathlib import Path

p=Path('app/lib/main.dart');s=p.read_text()
assert "import 'build443_capture_guard.dart';" not in s
s="import 'build443_capture_guard.dart';\n"+s
for start,end,uid in [
 ('class _KullaniciProfilPageState','class ', 'widget.uid'),
 ('class _ProfilPageState','class ', "FirebaseAuth.instance.currentUser?.uid??''")]:
 a=s.index(start);b=s.index(end,a+len(start));region=s[a:b]
 marker='Widget build(BuildContext context) {'
 assert region.count(marker)==1,start
 region=region.replace(marker,
   "Widget build(BuildContext context) => NgelxProfileCaptureGuard(key:ValueKey("+uid+"),uid:"+uid+",child:_buildProfile(context));\n\n  Widget _buildProfile(BuildContext context) {",1)
 s=s[:a]+region+s[b:]
s=s.replace('  String mesajIzni=', '  bool profilKayitIzni=false, _captureLoaded=false, _captureSaving=false;\n  String mesajIzni=',1)
s=s.replace("      ekranGoruntusu=v['allowStoryScreenshot']==true;", "      ekranGoruntusu=v['allowStoryScreenshot']==true;\n      profilKayitIzni=v['allowProfileCapture']==true;\n      _captureLoaded=true;",1)
marker='  Future<void> kaydet(String k,bool v) async {'
assert marker in s
s=s.replace(marker,"""  Future<void> profilKayitIzniKaydet(bool value) async {
    final userId=uid;
    if(userId==null||!_captureLoaded||_captureSaving)return;
    final old=profilKayitIzni;
    setState(()=>_captureSaving=true);
    try{
      await FirebaseFirestore.instance.collection('users').doc(userId)
        .set({'allowProfileCapture':value},SetOptions(merge:true));
      if(mounted&&uid==userId)setState(()=>profilKayitIzni=value);
    }catch(_){
      if(mounted&&uid==userId){
        setState(()=>profilKayitIzni=old);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(_ngelx438Ui('Tercih kaydedilemedi. Tekrar dene.'))));
      }
    }finally{if(mounted)setState(()=>_captureSaving=false);}
  }

"""+marker,1)
marker="          satir(t('profileShareFriendsOnly'),"
assert marker in s
s=s.replace(marker,"""          satir('Profil ekran kaydı ve görüntüsüne izin ver',
            'Kapalıysa Android’de profilin ve açılan profil medyası ekran kaydı ve ekran görüntüsünden korunur.',
            profilKayitIzni,profilKayitIzniKaydet,etkin:_captureLoaded&&!_captureSaving),
"""+marker,1)
p.write_text(s)
p=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt');s=p.read_text()
assert 'setCaptureLease' not in s
s=s.replace('import android.app.Activity','import android.view.WindowManager\nimport android.app.Activity',1)
s=s.replace('    private val mediaChannel', '    private val captureLeases = mutableSetOf<String>()\n\n    private val mediaChannel',1)
marker='        super.configureFlutterEngine(flutterEngine)'
assert marker in s
s=s.replace(marker,marker+"""
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.nnentx.ngelx_app/capture")
            .setMethodCallHandler { call, result ->
                if (call.method != "setCaptureLease") {
                    result.notImplemented()
                    return@setMethodCallHandler
                }
                val lease = call.argument<String>("lease")
                val secure = call.argument<Boolean>("secure")
                if (lease.isNullOrBlank() || secure == null) {
                    result.error("INVALID_LEASE", "Capture lease required", null)
                    return@setMethodCallHandler
                }
                if (secure) captureLeases.add(lease) else captureLeases.remove(lease)
                if (captureLeases.isNotEmpty()) {
                    window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
                } else {
                    window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
                }
                result.success(null)
            }
""",1)
p.write_text(s)
print('Build443: owner/visitor profile guards, durable privacy preference and native independent capture leases')
