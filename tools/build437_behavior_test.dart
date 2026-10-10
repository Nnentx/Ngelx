import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../lib/main.dart';
void main(){
  test('read receipts require a visible foreground newest message',(){
    for(var mask=0;mask<32;mask++){
      final result=ngelx437ReceiptVisible(foreground:mask&1!=0,currentRoute:mask&2!=0,listReady:mask&4!=0,atBottom:mask&8!=0,searching:mask&16!=0);
      expect(result,mask==15);
    }
  });
  test('shared emoji ignores contradictory private legacy settings',(){
    final chat=<String,dynamic>{'quickEmoji':'❤️','quickEmoji_a':'👍','quickEmoji_b':'😂'};
    expect(ngelx437SharedEmoji(chat),'❤️');
    expect(ngelx437SharedEmoji({'quickEmoji':''}),'👍');
    expect(ngelx437SharedEmoji({'quickEmoji':123}),'👍');
  });
  test('media list expires at 48h, actual messages at 14 days',(){
    final now=DateTime.utc(2026,10,10);
    final stamp=Timestamp.fromDate(now.subtract(const Duration(hours:48)));
    expect(ngelx437MediaInList(stamp,now),false);
    expect(ngelx437MessageExpired(stamp,now),false);
    expect(ngelx437MessageExpired(Timestamp.fromDate(now.subtract(const Duration(days:14))),now),true);
    expect(ngelx437MessageExpired(null,now),false);
  });
}
