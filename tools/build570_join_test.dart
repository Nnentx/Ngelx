import 'package:flutter_test/flutter_test.dart';
import '../lib/build570_join_policy.dart';
void main(){test('join tone only on new identities; no initial or reconnect chime',(){final p=Ngelx570JoinPolicy();expect(p.update(['a'],connected:true),false);expect(p.update(['a','b'],connected:true),true);expect(p.update(['a','b'],connected:true),false);expect(p.update(['a'],connected:true),false);expect(p.update([],connected:false),false);expect(p.update(['a','b'],connected:true),false);expect(p.update(['a','b','c'],connected:true),true);});}
