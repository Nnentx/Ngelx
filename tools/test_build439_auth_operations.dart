import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/build439_auth_operations.dart';
void main(){
 test('late sign-in after timeout finishes before sign-out',()async{
  final auth=NgelXAuthOperations<String>();
  final pending=Completer<String>();String? user;
  final login=auth.signIn(()async{user=await pending.future;return user!;});
  await expectLater(login.timeout(Duration.zero),throwsA(isA<TimeoutException>()));
  final logout=auth.signOut(()async{user=null;});
  await expectLater(auth.signIn(()async=>'other'),throwsStateError);
  pending.complete('old-account');await logout;
  expect(user,isNull);
 });
 test('failed login does not prevent sign-out; repeated taps share operation',()async{
  final auth=NgelXAuthOperations<String>();final pending=Completer<String>();
  var starts=0,exits=0;
  final one=auth.signIn((){starts++;return pending.future;});
  final two=auth.signIn((){starts++;return Future.value('wrong');});
  expect(identical(one,two),isTrue);expect(starts,1);
  final failure=expectLater(one,throwsStateError);
  final exit=auth.signOut(()async{exits++;});
  pending.completeError(StateError('failed'));await failure;await exit;
  expect(exits,1);
  expect(await auth.signIn(()async=>'new-account'),'new-account');
 });
}
