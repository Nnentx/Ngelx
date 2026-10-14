import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';

void main() {
  test('empty and brand placeholders fall through to the actual person name', () {
    expect(ngelx455ProfileName({'displayName':'', 'name':'Asya Sever'}), 'Asya Sever');
    expect(ngelx455ProfileName({'displayName':'NgelX','username':'ahsen'}), 'ahsen');
    expect(ngelx455ProfileName({'displayName':'  ADEM baykar  '}), 'ADEM baykar');
    expect(ngelx455ProfileName({},fallback:'Yükleniyor…'), 'Yükleniyor…');
  });
}
