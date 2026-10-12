import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:livekit_client/livekit_client.dart' as lk;
import 'package:ngelx_app/main.dart';
class Speaker446 extends ChangeNotifier implements lk.Participant {
  bool speaking=false;
  @override bool get isSpeaking=>speaking;
  void speak(bool value){speaking=value;notifyListeners();}
  @override dynamic noSuchMethod(Invocation invocation)=>super.noSuchMethod(invocation);
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
  p.dispose();
 });
}
