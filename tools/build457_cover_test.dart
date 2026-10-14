import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('Founder recognized with missing legacy admin entry', () {
    expect(ngelx457CanEditCover({'founderId': 'owner', 'admins': <String>[]}, 'owner'), isTrue);
    expect(ngelx457CanEditCover({'founderId': 'owner', 'admins': ['admin']}, 'admin'), isTrue);
    expect(ngelx457CanEditCover({'founderId': 'owner', 'admins': ['admin']}, 'member'), isFalse);
    expect(ngelx457CanEditCover({'founderId': 'owner'}, ''), isFalse);
  });
  test('Framing edits never overwrite the existing cover photo URL', () {
    final patch = ngelx457CoverChanges(alignment: .5);
    expect(patch, {'coverAlignment': .5});
    expect(patch.containsKey('coverUrl'), isFalse);
    expect(ngelx457CoverChanges(alignment: -.5, replacementUrl: 'https://example.com/new.jpg'),
        {'coverAlignment': -.5, 'coverUrl': 'https://example.com/new.jpg'});
  });
}
