import 'dart:convert';
import 'dart:math';
import 'package:dio/dio.dart';

const ngelx566GameEndpoints=['https://oyun.ngelxsocial.com/ludo','https://ngelx-live-moderation.alihancaglar76.workers.dev/ludo'];
class Ngelx566LudoTransport {
 final Dio client;
 Ngelx566LudoTransport({Dio? client}):client=client??Dio(BaseOptions(connectTimeout:const Duration(seconds:12),receiveTimeout:const Duration(seconds:25),sendTimeout:const Duration(seconds:12)));
 Map<String,dynamic> prepare(Map<String,dynamic> body){
  if(body['action']!='create'||body.containsKey('requestId'))return Map.of(body);
  final random=Random.secure();return {...body,'requestId':List.generate(16,(_)=>random.nextInt(256).toRadixString(16).padLeft(2,'0')).join()};
 }
 Future<Map<String,dynamic>> request(Map<String,dynamic> body,{required String token})async{
  final payload=prepare(body);
  for(var i=0;i<ngelx566GameEndpoints.length;i++){
   try{
    final r=await client.post<dynamic>(ngelx566GameEndpoints[i],data:payload,options:Options(headers:{'Authorization':'Bearer $token','content-type':'application/json'},followRedirects:false));
    final value=r.data is String?jsonDecode(r.data as String):r.data;
    if(value is! Map||value['room'] is! Map)throw const FormatException('Oyun yanıtı okunamadı.');
    final room=Map<String,dynamic>.from(value['room'] as Map);
    if(!RegExp(r'^[A-F0-9]{16}$').hasMatch('${room['id']}')||room['revision'] is! num)throw const FormatException('Oyun yanıtı doğrulanamadı.');
    return room;
   }on DioException catch(e){
    final data=e.response?.data,code=data is Map?data['error']:null;
    final retry=code==null||['temporarily_unavailable','service_not_configured'].contains(code);
    final status=e.response?.statusCode;
    if(i==ngelx566GameEndpoints.length-1||!retry||(status!=null&&![403,502,503,504].contains(status)))rethrow;
   }
  }
  throw StateError('Oyun bağlantısı kurulamadı.');
 }
}
