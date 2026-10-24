part of 'main.dart';

const ngelx564UpdateFeed='https://ngelxsocial.com/android-update.json';
const _ngelx564Channel=MethodChannel('com.nnentx.ngelx_app/update564');

class Ngelx564Release {
  final int build,size;
  final String version,url,sha256,notes;
  const Ngelx564Release({required this.build,required this.size,required this.version,required this.url,required this.sha256,this.notes=''});
  static Ngelx564Release parse(Map<String,dynamic> json){
    final build=json['build'],size=json['size'];
    final url=(json['url']??'').toString(),sha=(json['sha256']??'').toString();
    final uri=Uri.tryParse(url);
    if(json['schema']!=1||json['package']!='com.nnentx.ngelx_app'||json['abi']!='arm64-v8a'||
       build is! int||build<=0||size is! int||size<=0||size>209715200||
       uri==null||uri.scheme!='https'||uri.host!='github.com'||uri.userInfo.isNotEmpty||uri.hasQuery||uri.hasFragment||
       !uri.path.startsWith('/Nnentx/Ngelx/releases/download/')||!uri.path.endsWith('.apk')||
       !RegExp(r'^[a-fA-F0-9]{64}$').hasMatch(sha))throw const FormatException('Geçersiz NgelX güncellemesi');
    return Ngelx564Release(build:build,size:size,version:(json['version']??'').toString(),url:url,sha256:sha.toLowerCase(),notes:(json['notes']??'').toString());
  }
  Map<String,dynamic> toJson()=>{'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','build':build,'size':size,'version':version,'url':url,'sha256':sha256,'notes':notes};
}

class Ngelx564UpdateController extends ChangeNotifier {
  final Dio dio;
  Ngelx564UpdateController({Dio? client}):dio=client??Dio(BaseOptions(connectTimeout:const Duration(seconds:15),receiveTimeout:const Duration(seconds:45)));
  Ngelx564Release? release;
  String state='idle',error='',currentVersion='';
  int currentBuild=0;
  double progress=0;
  String? _path;
  CancelToken? _cancel;
  bool get busy=>['checking','downloading','verifying','opening'].contains(state);
  bool get available=>release!=null&&release!.build>currentBuild;
  Future<void> check() async {
    if(busy||state=='permission')return;
    state='checking';error='';notifyListeners();
    try{
      final status=await _ngelx564Channel.invokeMapMethod<String,dynamic>('status');
      currentBuild=(status?['build'] as num?)?.toInt()??0;currentVersion=(status?['version']??'').toString();
      final response=await dio.get<dynamic>(ngelx564UpdateFeed,options:Options(headers:{'Cache-Control':'no-cache'},responseType:ResponseType.json));
      final raw=response.data is String?jsonDecode(response.data as String):response.data;
      if(raw is! Map)throw const FormatException('Güncelleme bilgisi okunamadı');
      final next=Ngelx564Release.parse(Map<String,dynamic>.from(raw));
      release=next;state=available?'available':'current';
      final prefs=await SharedPreferences.getInstance();
      if(available&&prefs.getInt('update564_build')==next.build&&prefs.getString('update564_sha')==next.sha256){
        final path=prefs.getString('update564_path');
        if(path!=null&&await File(path).exists()){_path=path;state='ready';}
      }
      if(!available){await prefs.remove('update564_path');await prefs.remove('update564_build');await prefs.remove('update564_sha');}
    }catch(_){state='error';error='Güncellemeler kontrol edilemedi. Bağlantını kontrol edip tekrar dene.';}
    notifyListeners();
  }
  Future<void> download() async {
    if(!available||busy)return;
    final next=release!;
    state='downloading';error='';progress=0;_cancel=CancelToken();notifyListeners();
    try{
      final path=await _ngelx564Channel.invokeMethod<String>('prepare',{'build':next.build});
      if(path==null)throw const FormatException('İndirme başlatılamadı');
      _path=path;
      await dio.download(next.url,path,cancelToken:_cancel,onReceiveProgress:(received,total){
        if(received>next.size){_cancel?.cancel('size');return;}
        final value=(received/next.size).clamp(0.0,1.0).toDouble();
        if(value-progress>=.01||received==next.size){progress=value;notifyListeners();}
      });
      state='verifying';notifyListeners();
      await _ngelx564Channel.invokeMethod<String>('verify',_arguments());
      final prefs=await SharedPreferences.getInstance();
      await prefs.setString('update564_path',path);await prefs.setInt('update564_build',next.build);await prefs.setString('update564_sha',next.sha256);
      state='ready';progress=1;notifyListeners();
      await install();
    }catch(e){
      final cancelled=e is DioException&&CancelToken.isCancel(e)&&e.error=='user';
      state=cancelled?'available':'error';error=cancelled?'':'Güncelleme indirilemedi veya doğrulanamadı. Tekrar dene.';
      final path=_path;_path=null;if(path!=null){try{await File(path).delete();}catch(_){}}
      notifyListeners();
    }finally{_cancel=null;}
  }
  Map<String,dynamic> _arguments()=>{'path':_path,'build':release!.build,'size':release!.size,'sha256':release!.sha256};
  Future<void> install() async {
    if(_path==null||release==null||busy)return;
    state='opening';error='';notifyListeners();
    try{
      final result=await _ngelx564Channel.invokeMethod<String>('install',_arguments());
      state=result=='permission'?'permission':'installer';
    }catch(_){state='ready';error='Yükleme ekranı açılamadı. Tekrar dene.';}
    notifyListeners();
  }
  Future<void> resumePermission() async {
    if(state!='permission')return;
    final status=await _ngelx564Channel.invokeMapMethod<String,dynamic>('status');
    if(status?['canInstall']==true){state='ready';await install();}
    else{state='ready';error='Yüklemek için Android ayarlarında NgelX’e izin vermelisin.';notifyListeners();}
  }
  void cancel(){_cancel?.cancel('user');}
}
final ngelx564Updater=Ngelx564UpdateController();

class Ngelx564UpdateGate extends StatefulWidget {
  final Widget child;
  const Ngelx564UpdateGate({super.key,required this.child});
  @override State<Ngelx564UpdateGate> createState()=>_Ngelx564UpdateGateState();
}
class _Ngelx564UpdateGateState extends State<Ngelx564UpdateGate> with WidgetsBindingObserver {
  Timer? _timer;
  bool _showing=false;
  DateTime? _checked;
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);_timer=Timer(const Duration(seconds:5),()=>unawaited(_check()));}
  @override void dispose(){_timer?.cancel();WidgetsBinding.instance.removeObserver(this);super.dispose();}
  Future<void> _check() async {
    if(!mounted||kIsWeb||defaultTargetPlatform!=TargetPlatform.android||_showing||ngelxCallSession444.busy||ngelx564Updater.busy)return;
    if(_checked!=null&&DateTime.now().difference(_checked!)<const Duration(hours:6))return;
    _checked=DateTime.now();await ngelx564Updater.check();
    if(!mounted||!ngelx564Updater.available||ngelxCallSession444.busy)return;
    final prefs=await SharedPreferences.getInstance();
    final next=ngelx564Updater.release!;
    final dismissed=prefs.getInt('update564_later_${next.build}')??0;
    if(DateTime.now().millisecondsSinceEpoch-dismissed<const Duration(hours:24).inMilliseconds)return;
    final context=ngelxNavigatorKey.currentState?.overlay?.context;
    if(context==null||!context.mounted)return;
    _showing=true;
    await showDialog<void>(context:context,barrierDismissible:false,builder:(_)=>const Ngelx564UpdateDialog());
    _showing=false;
  }
  @override void didChangeAppLifecycleState(AppLifecycleState state){
    if(state==AppLifecycleState.resumed){
      unawaited(ngelx564Updater.resumePermission().catchError((_){ }));
      unawaited(_check());
    }
  }
  @override Widget build(BuildContext context)=>widget.child;
}

class Ngelx564UpdateDialog extends StatelessWidget {
  final Ngelx564UpdateController? controller;
  const Ngelx564UpdateDialog({super.key,this.controller});
  @override Widget build(BuildContext context){
    final updater=controller??ngelx564Updater;
    return Theme(data:ThemeData.light(),child:ListenableBuilder(listenable:updater,builder:(context,_) {
      final downloading=updater.state=='downloading',verifying=updater.state=='verifying';
      final ready=['ready','permission','installer'].contains(updater.state);
      final title=downloading?'Güncelleme indiriliyor':verifying?'Güncelleme doğrulanıyor':updater.state=='current'?'NgelX güncel':updater.state=='checking'?'Güncellemeler kontrol ediliyor':'Yeni güncelleme hazır';
      return PopScope(canPop:!updater.busy,child:Dialog(backgroundColor:Colors.white,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(26)),child:SingleChildScrollView(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
        Container(width:68,height:68,decoration:const BoxDecoration(shape:BoxShape.circle,gradient:LinearGradient(colors:[mor,Color(0xFF258AFF)])),child:const Icon(Icons.system_update_rounded,color:Colors.white,size:36)),
        const SizedBox(height:20),Text(title,textAlign:TextAlign.center,style:const TextStyle(fontSize:22,fontWeight:FontWeight.w900,color:Color(0xFF111827))),
        const SizedBox(height:10),
        if(updater.release!=null&&updater.available)Text('NgelX ${updater.release!.version}',style:const TextStyle(color:Colors.black54)),
        if(updater.available&&!updater.busy&&updater.release!.notes.isNotEmpty)Padding(padding:const EdgeInsets.only(top:8),child:Text(updater.release!.notes,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54))),
        const SizedBox(height:14),
        if(downloading||verifying||updater.state=='checking'||updater.state=='opening')...[
          LinearProgressIndicator(value:downloading?updater.progress:null,color:mor,backgroundColor:const Color(0xFFEEEBF5)),const SizedBox(height:10),
          Text(downloading?'%${(updater.progress*100).round()}':'Lütfen bekle…',style:const TextStyle(color:Colors.black87)),
        ],
        if(updater.state=='permission')const Text('Android ayarlarında “Bu kaynaktan izin ver” seçeneğini açıp NgelX’e dön.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)),
        if(updater.state=='installer')const Text('Android yükleme ekranında “Güncelle”ye dokun. İptal ettiysen tekrar açabilirsin.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54)),
        if(updater.error.isNotEmpty)Text(updater.error,textAlign:TextAlign.center,style:const TextStyle(color:Colors.red)),
        if(updater.available&&!updater.busy)const Padding(padding:EdgeInsets.only(top:10),child:Text('Uygulamayı silmen gerekmez. Son yüklemeyi Android ekranında onaylarsın.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:12))),
        const SizedBox(height:18),
        if(!updater.busy&&updater.available)SizedBox(width:double.infinity,child:DecoratedBox(decoration:BoxDecoration(gradient:const LinearGradient(colors:[mor,Color(0xFF258AFF)]),borderRadius:BorderRadius.circular(20)),child:FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.transparent,shadowColor:Colors.transparent),onPressed:()=>ready?updater.install():updater.download(),child:Text(ready?'Yüklemeyi aç':updater.state=='error'?'Tekrar dene':'Güncelle')))),
        if(updater.state=='error'&&!updater.available)FilledButton(onPressed:updater.check,child:const Text('Tekrar dene')),
        if(downloading)TextButton(onPressed:updater.cancel,child:const Text('İndirmeyi iptal et')),
        if(!updater.busy)TextButton(onPressed:()async{
          final next=updater.release;
          if(next!=null){final prefs=await SharedPreferences.getInstance();await prefs.setInt('update564_later_${next.build}',DateTime.now().millisecondsSinceEpoch);}
          if(context.mounted)Navigator.pop(context);
        },child:Text(updater.available?'Daha sonra':'Kapat')),
      ])))));
    }));
  }
}

class Ngelx564UpdatesPage extends StatefulWidget {
  const Ngelx564UpdatesPage({super.key});
  @override State<Ngelx564UpdatesPage> createState()=>_Ngelx564UpdatesPageState();
}
class _Ngelx564UpdatesPageState extends State<Ngelx564UpdatesPage> {
  @override void initState(){super.initState();WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)unawaited(_open());});}
  Future<void> _open() async {
    if(!kIsWeb&&defaultTargetPlatform==TargetPlatform.android)await ngelx564Updater.check();
    if(mounted)await showDialog<void>(context:context,barrierDismissible:false,builder:(_)=>const Ngelx564UpdateDialog());
    if(mounted)setState((){});
  }
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:const Text('Güncellemeler')),body:Center(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
    const Icon(Icons.system_update_rounded,size:72,color:mor),const SizedBox(height:16),
    Text('NgelX ${ngelx564Updater.currentVersion.isEmpty?ngelxVersionName:ngelx564Updater.currentVersion}',style:const TextStyle(fontSize:23,fontWeight:FontWeight.w900)),const SizedBox(height:10),
    const Text('Yeni sürümleri uygulama içinden kontrol edebilirsin.',textAlign:TextAlign.center),const SizedBox(height:20),
    FilledButton.icon(onPressed:_open,icon:const Icon(Icons.refresh_rounded),label:const Text('Güncellemeleri kontrol et')),
  ])))));
}
