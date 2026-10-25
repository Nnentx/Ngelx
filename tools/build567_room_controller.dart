import 'package:flutter/foundation.dart';

typedef Ngelx567Request=Future<Map<String,dynamic>> Function(Map<String,dynamic> body);
class Ngelx567Failure implements Exception {
 final String code,message;
 const Ngelx567Failure(this.code,this.message);
 @override String toString()=>message;
}
class Ngelx567RoomController extends ChangeNotifier {
 final String id,uid;
 final Ngelx567Request request;
 final bool Function()? accountMatches;
 Map<String,dynamic> room;
 String error='';
 bool busy=false,leaving=false,detached=false,_disposed=false;
 int _generation=0,_sequence=0;
 Future<void>? _sync;
 Ngelx567RoomController({required this.id,required this.uid,required this.request,this.accountMatches,Map<String,dynamic>? initial}):room=initial??{};
 int get seat {
  for(final p in room['players']??[]){if(p['uid']==uid&&p['left']!=true)return (p['seat'] as num).toInt();}
  return -1;
 }
 bool get owner=>room['owner']==uid;
 bool get waiting=>room['status']=='waiting';
 bool get playing=>room['status']=='playing';
 bool get terminal=>detached||['closed','finished'].contains(room['status']);
 int get joined=>(room['players'] as List? ?? []).where((p)=>p['left']!=true).length;
 bool get canStart=>waiting&&owner&&joined==room['capacity']&&!busy&&!leaving&&!detached;
 void _notify(){if(!_disposed)notifyListeners();}
 bool _account(){if(accountMatches?.call()==false){detached=true;error='Oturum değişti. Lobiye dönebilirsin.';_notify();return false;}return true;}
 void _accept(Map<String,dynamic> next){
  if((next['revision'] as num? ?? -1)>=(room['revision'] as num? ?? -1))room=next;
 }
 Future<void> sync({bool join=false}){
  if(_disposed||busy||leaving||detached||!_account())return Future.value();
  if(_sync!=null)return _sync!;
  final generation=_generation;
  final task=()async{
   try{
    final next=await request({'action':join||room.isEmpty?'join':'sync','id':id});
    if(_disposed||generation!=_generation||leaving||!_account())return;
    _accept(next);error='';_notify();
   }catch(e){
    if(_disposed||generation!=_generation||leaving)return;
    if(e is Ngelx567Failure&&_alreadyGone(e.code))detached=true;
    error=_message(e);_notify();
   }
  }();
  _sync=task;
  return task.whenComplete((){if(identical(_sync,task))_sync=null;});
 }
 String _id()=> 'room567_${DateTime.now().microsecondsSinceEpoch}_${++_sequence}';
 Future<bool> perform(String action,[Map<String,dynamic> data=const {}])async{
  if(_disposed||busy||leaving||detached||room.isEmpty||!_account())return false;
  busy=true;error='';_generation++;_notify();
  try{
   final next=await request({'action':action,'id':id,'revision':room['revision'],'requestId':_id(),...data});
   if(_disposed||!_account())return false;
   _accept(next);error='';return true;
  }catch(e){if(!_disposed)error=_message(e);return false;}
  finally{busy=false;_notify();}
 }
 bool _alreadyGone(String code)=>['not_a_player','already_left','room_expired','room_not_found'].contains(code);
 Future<bool> leave()async{
  if(_disposed)return true;
  if(terminal||!_account())return true;
  if(busy||leaving)return false;
  leaving=true;busy=true;error='';_generation++;_notify();
  final key=_id();
  try{
   for(var attempt=0;attempt<2;attempt++){
    try{
     final next=await request({'action':'leave','id':id,'revision':room['revision'],'requestId':key});
     if(!_disposed)_accept(next);
     detached=true;error='';return true;
    }catch(e){
     if(e is Ngelx567Failure&&_alreadyGone(e.code)){detached=true;error='';return true;}
     if(attempt==0&&e is Ngelx567Failure&&e.code=='state_changed'){
      final next=await request({'action':'sync','id':id});if(!_disposed)_accept(next);continue;
     }
     rethrow;
    }
   }
   return false;
  }catch(e){
   if(e is Ngelx567Failure&&_alreadyGone(e.code)){detached=true;error='';return true;}
   if(!_disposed)error=_message(e);
   return false;
  }finally{busy=false;leaving=false;_notify();}
 }
 void dismissError(){error='';_notify();}
 String _message(Object e)=>e is Ngelx567Failure?e.message:e.toString().replaceFirst('Exception: ','');
 @override void dispose(){_disposed=true;_generation++;super.dispose();}
}
