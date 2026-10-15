#!/usr/bin/env python3
"""Build464: share/cache public photo loads, bound stalls and keep inbox avatar fallbacks.
Client-only; no data/rules/production deployment.
"""
from pathlib import Path
import re

MAIN=Path('app/lib/main.dart')
PUB=Path('app/pubspec.yaml')

def one(s,old,new,name):
    count=s.count(old)
    if count!=1:raise RuntimeError(f'Build464 {name}: anchor count {count}')
    return s.replace(old,new,1)

def optional(s,old,new,name):
    count=s.count(old)
    if count==1:return s.replace(old,new,1)
    if count>1:raise RuntimeError(f'Build464 {name}: ambiguous {count} matches')
    print(f'Build464 inbox markup changed; guarded direct match skipped: {name}')
    return s

def patch(s):
    s=one(s,"import 'package:cached_network_image/cached_network_image.dart';",
        "import 'package:cached_network_image/cached_network_image.dart';\nimport 'package:flutter_cache_manager/flutter_cache_manager.dart';",
        'cache manager import')
    a=s.index('final Map<String,Uint8List> _ngelxAgResmiBellek=')
    b=s.index('@immutable\nclass NgelXAgImageProvider',a)
    new='''// Build464: consistent, bounded image loads shared across NgelX widgets.
final Map<String,Uint8List> _ngelxAgResmiBellek=<String,Uint8List>{};
const int _ngelxAgResmiBellekSiniri=96;
final Map<String,Future<Uint8List>> _ngelx464BekleyenResimler={};
final CacheManager _ngelx464GenelResimCache=CacheManager(Config(
  'ngelx-public-media-v464',
  stalePeriod:const Duration(days:3),
  maxNrOfCacheObjects:160,
));
int _ngelx464AktifIndirme=0;
final List<Completer<void>> _ngelx464BeklemeSirasi=<Completer<void>>[];

Future<void> _ngelx464IndirmeSirasiBekle() async {
  if(_ngelx464AktifIndirme<6&&_ngelx464BeklemeSirasi.isEmpty){
    _ngelx464AktifIndirme++;
    return;
  }
  final ready=Completer<void>();
  _ngelx464BeklemeSirasi.add(ready);
  await ready.future;
}
void _ngelx464IndirmeSirasiBirak(){
  if(_ngelx464BeklemeSirasi.isNotEmpty){
    _ngelx464BeklemeSirasi.removeAt(0).complete();
  }else{
    _ngelx464AktifIndirme--;
  }
}
void _ngelx464BellegeAl(String url,Uint8List bytes){
  if(_ngelxAgResmiBellek.length>=_ngelxAgResmiBellekSiniri){
    _ngelxAgResmiBellek.remove(_ngelxAgResmiBellek.keys.first);
  }
  _ngelxAgResmiBellek[url]=bytes;
}
bool _ngelx464GuvenilirMedyaHost(String host)=> <String>[
  'media.ngelxsocial.com','media2.ngelxsocial.com',
  'ngelx-media.alihancaglar76.workers.dev',
  'ngelx-upload.alihancaglar76.workers.dev',
].contains(host.toLowerCase());

Future<Uint8List> _ngelxAgResmiBaytlari(String rawUrl){
  final url=rawUrl.trim();
  if(url.isEmpty)return Future<Uint8List>.error(StateError('Fotoğraf adresi boş.'));
  final memory=_ngelxAgResmiBellek[url];
  if(memory!=null&&memory.isNotEmpty)return Future<Uint8List>.value(memory);
  final pending=_ngelx464BekleyenResimler[url];
  if(pending!=null)return pending;
  final request=_ngelx464YukleVeTemizle(url);
  _ngelx464BekleyenResimler[url]=request;
  return request;
}
Future<Uint8List> _ngelx464YukleVeTemizle(String url)async{
  try{return await _ngelx464ResmiGetir(url);}
  finally{_ngelx464BekleyenResimler.remove(url);}
}

Future<Uint8List> _ngelx464ResmiGetir(String url)async{
  // Store only publicly accessible, decoded image bytes, never authenticated ones.
  try{
    final item=await _ngelx464GenelResimCache.getFileFromCache(url);
    if(item!=null){
      final raw=await item.file.readAsBytes();
      if(raw.length>=4&&raw.length<=3*1024*1024){
        final bytes=Uint8List.fromList(raw);
        _ngelx464BellegeAl(url,bytes);
        return bytes;
      }
      await _ngelx464GenelResimCache.removeFile(url);
    }
  }catch(_){}
  await _ngelx464IndirmeSirasiBekle();
  final cancellation=CancelToken();
  final watchdog=Timer(const Duration(seconds:28),(){
    if(!cancellation.isCancelled)cancellation.cancel('Fotoğraf zaman aşımı');
  });
  try{
    // Actual saved URL comes FIRST; alternate hosts are fallbacks only.
    final sources=<String>{url,...ngelxMedyaUrlAdaylari(url)}.toList();
    final dio=Dio(BaseOptions(
      connectTimeout:const Duration(seconds:6),
      receiveTimeout:const Duration(seconds:12),
      validateStatus:(s)=>s!=null,
    ));
    Object? lastError;
    String? token;
    for(final candidate in sources){
      if(cancellation.isCancelled)break;
      final uri=Uri.tryParse(candidate);
      if(uri==null||uri.scheme!='https'||uri.host.isEmpty)continue;
      Future<Response<List<int>>> download({String? bearer})=>dio.getUri<List<int>>(
        uri,cancelToken:cancellation,
        options:Options(responseType:ResponseType.bytes,headers:{
          'Accept':'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
          'X-NgelX-Client':'android-image-build464',
          if(bearer!=null)HttpHeaders.authorizationHeader:'Bearer '+bearer,
        }));
      try{
        var reply=await download();
        var status=reply.statusCode??0;
        var usedAuth=false;
        if((status==401||status==403)&&_ngelx464GuvenilirMedyaHost(uri.host)){
          token??=await FirebaseAuth.instance.currentUser?.getIdToken()
            .timeout(const Duration(seconds:4));
          if(token!=null&&token.isNotEmpty){
            reply=await download(bearer:token);
            status=reply.statusCode??0;
            usedAuth=true;
          }
        }
        final raw=reply.data;
        if(status!=200&&status!=206)throw StateError('HTTP '+status.toString());
        if(raw==null||raw.length<4||raw.length>12*1024*1024){
          throw StateError('Fotoğraf boş veya çok büyük.');
        }
        final bytes=Uint8List.fromList(raw);
        final codec=await ui.instantiateImageCodec(bytes);
        final frame=await codec.getNextFrame();
        frame.image.dispose();
        codec.dispose();
        _ngelx464BellegeAl(url,bytes);
        if(!usedAuth&&status==200&&bytes.length<=3*1024*1024){
          try{await _ngelx464GenelResimCache.putFile(
              url,bytes,maxAge:const Duration(days:3));}catch(_){}
        }
        return bytes;
      }catch(e){
        lastError=e;
        if(cancellation.isCancelled)break;
      }
    }
    throw StateError('Fotoğraf alınamadı: '+_ngelxKisaHata(lastError??'ağ hatası'));
  }finally{
    watchdog.cancel();
    _ngelx464IndirmeSirasiBirak();
  }
}

'''
    s=s[:a]+new+s[b:]
    s=one(s,
        "final bytes=await _ngelxAgResmiBaytlari(key.url).timeout(const Duration(seconds:18));",
        "final bytes=await _ngelxAgResmiBaytlari(key.url).timeout(const Duration(seconds:40));",
        'align widget timeout with bounded queued network download')
    s=one(s,"  _ngelxAgResmiBellek.remove(temiz);\n  for(final aday in ngelxMedyaUrlAdaylari(temiz)){",
        "  _ngelxAgResmiBellek.remove(temiz);\n  try{await _ngelx464GenelResimCache.removeFile(temiz);}catch(_){}\n  for(final aday in ngelxMedyaUrlAdaylari(temiz)){",
        'per-url cache invalidation')
    s=one(s,"    _ngelxAgResmiBellek.clear();\n    PaintingBinding.instance.imageCache.clear();",
        "    _ngelxAgResmiBellek.clear();\n    try{await _ngelx464GenelResimCache.emptyCache();}catch(_){}\n    PaintingBinding.instance.imageCache.clear();",
        'global cache invalidation')
    a=s.index('\nFuture<void> ngelxOverlayKapanisiniBekle() async')
    fallback='''// Build464: inbox photos must have a visible fallback, never empty circles.
class NgelXGuvenliAvatar extends StatelessWidget{
  final String url;
  final double radius;
  final Color backgroundColor;
  final Color iconColor;
  final IconData icon;
  const NgelXGuvenliAvatar({
    super.key,required this.url,this.radius=20,
    this.backgroundColor=const Color(0xFFECE6F8),
    this.iconColor=const Color(0xFF8B5CF6),
    this.icon=Icons.person_outline_rounded,
  });
  @override Widget build(BuildContext context)=>CircleAvatar(
    radius:radius,backgroundColor:backgroundColor,
    child:ClipOval(child:SizedBox(
      width:radius*2,height:radius*2,
      child:Stack(fit:StackFit.expand,children:[
        Center(child:Icon(icon,color:iconColor,size:radius*.95)),
        if(url.trim().isNotEmpty)NgelXAgResmi(
          url:url.trim(),fit:BoxFit.cover,
          placeholder:const SizedBox.shrink(),
          error:const SizedBox.shrink(),
        ),
      ]),
    )),
  );
}

'''
    s=s[:a]+ '\n'+fallback+s[a:]
    s=optional(s,
        "leading:CircleAvatar(backgroundColor:const Color(0xFFE9DDFF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.groups,color:mor):null)",
        "leading:NgelXGuvenliAvatar(url:foto,backgroundColor:const Color(0xFFE9DDFF),icon:Icons.groups_rounded)",
        'inbox group photo')
    s=optional(s,
        "child:CircleAvatar(backgroundImage:(p['photoUrl']??'').toString().isEmpty?null:NgelXAgImageProvider(p['photoUrl']))",
        "child:NgelXGuvenliAvatar(url:(p['photoUrl']??'').toString())",
        'inbox person photo')
    s=optional(s,
        "leading:CircleAvatar(\n                        backgroundColor:ngelxGroupGreenSoft,\n                        backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),\n                        child:foto.isEmpty?const Icon(Icons.groups_rounded,color:ngelxGroupGreen):null,\n                      )",
        "leading:NgelXGuvenliAvatar(url:foto,backgroundColor:ngelxGroupGreenSoft,iconColor:ngelxGroupGreen,icon:Icons.groups_rounded)",
        'archived group photo')
    # Inspect only code formatting, never user records or private media URLs.
    left=s.index('class _MesajPageState')
    right=s.index('class ArsivSohbetlerPage',left)
    region=s[left:right]
    for key in ['NgelXAgImageProvider(foto)','NgelXAgImageProvider(p[','CircleAvatar(','NgelXGuvenliAvatar(']:
        print('Build464 inbox source token '+key+' count='+str(region.count(key)))
    marker='NgelXAgImageProvider('
    pos=0
    for _ in range(8):
        at=region.find(marker,pos)
        if at<0:break
        print('Build464 inbox source-only avatar markup: '+repr(region[max(0,at-210):at+230]))
        pos=at+len(marker)
    return s

def run():
    yaml=PUB.read_text(encoding='utf-8')
    if not re.search(r'(?m)^\s*flutter_cache_manager\s*:',yaml):
        yaml=one(yaml,'  cached_network_image: ^4.0.0',
            '  cached_network_image: ^4.0.0\n  flutter_cache_manager: ^3.4.5',
            'existing lock-compatible cache dependency')
        PUB.write_text(yaml,encoding='utf-8')
    original=MAIN.read_text(encoding='utf-8')
    if '// Build464: consistent, bounded image loads' not in original:
        MAIN.write_text(patch(original),encoding='utf-8')
    print('Build464: 6 concurrent photo downloads, 28s upper bound, dedupe, public disk cache, inbox fallbacks.')

if __name__=='__main__':run()
