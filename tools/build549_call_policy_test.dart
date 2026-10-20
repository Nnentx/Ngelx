import 'package:flutter_test/flutter_test.dart';
import '../lib/build549_call_policy.dart';
void main(){
  bool invite({bool group=false,String status='ringing',bool sameRoom=true,
    bool member=true,bool kicked=false,bool exited=false,int age=10})=>
    ngelx549CanAnswer(sameRoom:sameRoom,member:member,group:group,status:status,
      ageSeconds:age,kicked:kicked,exited:exited);
  test('private ringing and active group invitation are answerable',(){
    expect(invite(),true);
    expect(invite(group:true,status:'active'),true);
    expect(invite(status:'active'),false);
  });
  test('terminal calls and stale or future invitations cannot be answered',(){
    for(final status in ['ended','rejected','missed','']){
      expect(invite(group:true,status:status),false);
    }
    expect(invite(age:60),false);expect(invite(age:-1),false);
  });
  test('membership, exact room, kick and voluntary exit stay authoritative',(){
    expect(invite(member:false,group:true),false);
    expect(invite(sameRoom:false,group:true),false);
    expect(invite(kicked:true,group:true),false);
    expect(invite(exited:true,group:true),false);
  });
  test('one foreground/background request in flight and shared cooldown',(){
    final gate=Ngelx549RequestGate(),now=DateTime(2026,10,21);
    expect(gate.enter(now),true);expect(gate.enter(now),false);
    gate.finish(now);
    expect(gate.enter(now.add(const Duration(seconds:59))),false);
    expect(gate.enter(now.add(const Duration(seconds:60))),true);
  });
  test('quota waits two minutes without creating an automatic retry loop',(){
    final gate=Ngelx549RequestGate(),now=DateTime(2026,10,21);
    expect(gate.enter(now),true);gate.finish(now,quota:true);
    expect(gate.enter(now.add(const Duration(seconds:119))),false);
    expect(gate.enter(now.add(const Duration(seconds:120))),true);
  });
}
