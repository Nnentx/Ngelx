import 'package:flutter_test/flutter_test.dart';
import '../lib/build548_policy.dart';
void main(){
  test('private call identity is the other member in both directions',(){
    expect(ngelx548PeerUid(['alperen','ahsen'],'alperen'),'ahsen');
    expect(ngelx548PeerUid(['alperen','ahsen'],'ahsen'),'alperen');
    expect(ngelx548PeerUid(['alperen'],'alperen'),isNull);
    expect(ngelx548PeerUid(['alperen','ahsen','ayaz'],'alperen'),isNull);
  });
  test('tall screenshot fits both limits without any padded width',(){
    final size=ngelx548PhotoSize(694,1536,400,800);
    expect(size.height,320);expect(size.width,closeTo(694/1536*320,.001));
    expect(size.width/size.height,closeTo(694/1536,.00001));
  });
  test('wide photos keep their full content and natural ratio',(){
    final size=ngelx548PhotoSize(1920,1080,400,800);
    expect(size.width,260);expect(size.height,closeTo(146.25,.001));
    final small=ngelx548PhotoSize(100,100,240,500);
    expect(small.width,lessThanOrEqualTo(240*.68));
    expect(small.height,lessThanOrEqualTo(200));
  });
  test('one to three guests stay in right rail, larger groups use grid',(){
    for(final n in [0,1,2,3])expect(ngelx548UseGrid(n),false);
    for(final n in [4,5,8,10])expect(ngelx548UseGrid(n),true);
    expect(ngelx548GridColumns(5),2);expect(ngelx548GridColumns(9),3);
  });
  test('free gift catalog rejects forged values and invalid quantities',(){
    expect(ngelx548ValidGift('Gül',1,1),true);
    expect(ngelx548ValidGift('Galaksi',100,10),true);
    expect(ngelx548ValidGift('Galaksi',1,1),false);
    expect(ngelx548ValidGift('unknown',1,1),false);
    expect(ngelx548ValidGift('Gül',1,0),false);
    expect(ngelx548ValidGift('Gül',1,11),false);
  });
}
