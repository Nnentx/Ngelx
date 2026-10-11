import 'build438_group_successor.dart';
void main(){
  void check(String? actual,String? expected){if(actual!=expected)throw StateError('$actual != $expected');}
  check(ngelx438Successor(['owner','old','admin'],['owner','admin'],'owner'),'admin');
  check(ngelx438Successor(['owner','old','new'],['owner'],'owner'),'old');
  check(ngelx438Successor(['owner'],['owner'],'owner'),null);
  check(ngelx438Successor(['owner','member'],['owner','stale'],'owner'),'member');
  check(ngelx438Successor(['owner','a','b'],['b','a'],'owner'),'a');
  print('Group successor: 5 scenarios passed');
}
