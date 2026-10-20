// Admission always rechecks authoritative server data in the transaction.
bool ngelx549CanAnswer({required bool sameRoom,required bool member,
  required bool group,required String status,required int ageSeconds,
  required bool kicked,required bool exited}) =>
  sameRoom&&member&&!kicked&&!exited&&ageSeconds>=0&&ageSeconds<60&&
  (status=='ringing'||group&&status=='active');

class Ngelx549RequestGate {
  DateTime? next;
  bool running=false;
  bool enter(DateTime now){
    if(running||next!=null&&now.isBefore(next!))return false;
    running=true;return true;
  }
  void finish(DateTime now,{bool quota=false}){
    running=false;next=now.add(Duration(seconds:quota?120:60));
  }
}
