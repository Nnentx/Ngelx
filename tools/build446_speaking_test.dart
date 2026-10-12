import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:livekit_client/livekit_client.dart' as lk;
import 'package:ngelx_app/main.dart';
class Speaker446 implements lk.Participant {
  final _notifier=ChangeNotifier();
  @override void addListener(VoidCallback listener)=>_notifier.addListener(listener);
  @override void removeListener(VoidCallback listener)=>_notifier.removeListener(listener);
  @override Future<bool> dispose()async{_notifier.dispose();return true;}
  bool speaking=false;
  @override bool get isSpeaking=>speaking;
  void speak(bool value){speaking=value;_notifier.notifyListeners();}
  @override dynamic noSuchMethod(Invocation invocation)=>throw UnimplementedError(invocation.memberName.toString());
}
void main(){
 testWidgets('speaker ring animates only while participant speaks and disposes cleanly',(tester)async{
  final p=Speaker446();
  await tester.pumpWidget(MaterialApp(home:Center(child:Ngelx446SpeakingRing(participant:p,child:const CircleAvatar(radius:20)))));
  final initial=tester.getSize(find.byType(CircleAvatar));
  p.speak(true);await tester.pump();await tester.pump(const Duration(milliseconds:325));
  expect(tester.binding.hasScheduledFrame,isTrue);
  expect(tester.getSize(find.byType(CircleAvatar)),initial);
  p.speak(false);await tester.pump();await tester.pump(const Duration(seconds:1));
  expect(tester.binding.hasScheduledFrame,isFalse);
  p.speak(true);await tester.pump();
  await tester.pumpWidget(const SizedBox());
  expect(tester.takeException(),isNull);
  await p.dispose();
 });
}
