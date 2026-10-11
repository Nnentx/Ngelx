import 'build438_pin_permission.dart';
void main() {
  final group = <String,dynamic>{'isGroup':true,'members':['owner','admin','member'],'admins':['admin'],'createdBy':'owner'};
  final cases = <(Map<String,dynamic>,String?,bool)>[
    (group,'owner',true), (group,'admin',true), (group,'member',false),
    ({...group,'onlyAdminsCanPin':false},'member',true),
    ({...group,'onlyAdminsCanPin':false},'outside',false),
    ({...group,'admins':['outside']},'outside',false),
    (group,null,false), (<String,dynamic>{},'member',false),
  ];
  for (final (data,uid,expected) in cases) {
    if(ngelx438CanPin(data,uid)!=expected)throw StateError('Pin permission: $uid');
  }
  print('Group pin permission: 8 scenarios passed');
}
