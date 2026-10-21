from pathlib import Path
import sys
TAG='// Build553 live viewport and screen ownership'
def once(s,a,b):
 if s.count(a)!=1: raise RuntimeError(f'Build553 expected one anchor, found {s.count(a)}: {a[:90]}')
 return s.replace(a,b,1)
def apply(root=Path('app')):
 p=root/'lib/live_broadcast_studio.dart';s=p.read_text()
 if TAG in s:return
 s=once(s,'class _CanliYayinPageState extends State<CanliYayinPage> {','class _CanliYayinPageState extends State<CanliYayinPage> with WidgetsBindingObserver {')
 anchor='  int _lastVisibleVideoSecond = 0;'
 s=once(s,anchor,'''  bool? _screen553;
  final String _screenOwner553='live-${DateTime.now().microsecondsSinceEpoch}';
  Future<void> _keepLiveScreen553(bool enabled) async {
    if(!Platform.isAndroid || _screen553==enabled)return;
    _screen553=enabled;
    try {
      await const MethodChannel('com.nnentx.ngelx_app/call_screen')
        .invokeMethod<void>('keepScreenOn',{'enabled':enabled,'owner':_screenOwner553});
    } catch (_) { _screen553=null; }
  }
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    // Volume and permission overlays must not interrupt RTC media.
    if(state==AppLifecycleState.inactive)return;
    unawaited(_keepLiveScreen553(state==AppLifecycleState.resumed&&!kapatildi&&!yayinBitti));
  }
'''+anchor)
 a=s.index('class _CanliYayinPageState');head=s[:a];body=s[a:]
 body=once(body,'    super.initState();','''    super.initState();
    WidgetsBinding.instance.addObserver(this);
    unawaited(_keepLiveScreen553(true));''')
 body=once(body,'    kapatildi = true;','    kapatildi = true;\n    unawaited(_keepLiveScreen553(false));')
 body=once(body,'  void dispose() {','''  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    unawaited(_keepLiveScreen553(false));''')
 body=once(body,'    final track = _goruntu();','''    if(yayinBitti||kapatildi)unawaited(_keepLiveScreen553(false));
    final track = _goruntu();''')
 body=once(body,'              _commentSection490(),\n              const SizedBox(height:8),\n              _liveBottom540(),','''              ConstrainedBox(
                constraints:BoxConstraints(maxHeight:math.max(48.0,
                  (MediaQuery.sizeOf(context).height-MediaQuery.viewInsetsOf(context).bottom-
                    MediaQuery.paddingOf(context).vertical-28)*.52)),
                child:SingleChildScrollView(
                  keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag,
                  child:Column(mainAxisSize:MainAxisSize.min,children:[
                    _commentSection490(),const SizedBox(height:4),_liveBottom540(),
                  ]))),''')
 body=once(body,'maxHeight:keyboard?76:148','maxHeight:keyboard?56:112')
 body=once(body,'    _guestStatus546(),','    if(MediaQuery.viewInsetsOf(context).bottom==0)_guestStatus546(),')
 s=head+body+'\n'+TAG+'\n';p.write_text(s)
 p=root/'lib/build540_reference_ui.dart';s=p.read_text()
 s=once(s,'    color: Colors.transparent,','    color: const Color(0xC01A1721),')
 s=once(s,'''      child: Row(children: [
        Expanded(child: composer),
        if (MediaQuery.viewInsetsOf(context).bottom == 0) ...actions,
      ]),''','''      child: LayoutBuilder(builder:(_,box) {
        final keyboard=MediaQuery.viewInsetsOf(context).bottom>0;
        final wrap=box.maxWidth<390 || MediaQuery.textScalerOf(context).scale(1)>1.2;
        if(keyboard)return composer;
        if(wrap)return Column(mainAxisSize:MainAxisSize.min,children:[
          composer,Wrap(alignment:WrapAlignment.end,crossAxisAlignment:WrapCrossAlignment.center,children:actions),
        ]);
        return Row(children:[Expanded(child:composer),...actions]);
      }),''')
 p.write_text(s)
 p=root/'android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt';s=p.read_text()
 s=once(s,'        // Build492: keep foreground video-call screen awake only.','''        // Build553: independent owners prevent a closing call/live from clearing another session.
        val screenOwners553 = mutableSetOf<String>()
        // Build492: keep foreground video-call screen awake only.''')
 s=once(s,'                    val enabled = call.argument<Boolean>("enabled") == true\n                    runOnUiThread {\n                        if (enabled) window.addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)', '''                    val enabled = call.argument<Boolean>("enabled") == true
                    val owner = call.argument<String>("owner") ?: "call"
                    runOnUiThread {
                        if (enabled) screenOwners553.add(owner) else screenOwners553.remove(owner)
                        if (screenOwners553.isNotEmpty()) window.addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)''')
 p.write_text(s)
if __name__=='__main__':apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path('app'))
