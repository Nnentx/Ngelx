import 'package:flutter_test/flutter_test.dart';
import '../lib/build550_live_totals.dart';

void main() {
  test('replayed changes do not double count; edits and deletes reconcile', () {
    final t = Ngelx550LiveTotals();
    t.apply('legacy', {});
    t.apply('join', {'kind': 'join'});
    t.apply('gift', {'kind': 'gift', 'points': 25, 'quantity': 2});
    t.apply('gift', {'kind': 'gift', 'points': 25, 'quantity': 2});
    expect([t.comments, t.points, t.gifts], [1, 25, 2]);
    t.apply('gift', {'kind': 'gift', 'points': 40, 'quantity': 100});
    expect([t.comments, t.points, t.gifts], [1, 40, 10]);
    t.apply('gift', {'kind': 'comment'});
    expect([t.comments, t.points, t.gifts], [2, 0, 0]);
    t.apply('legacy', null);
    t.apply('legacy', null);
    expect(t.comments, 1);
  });

  test('unchanged history needs no reapplication during 200 heartbeats', () {
    final t = Ngelx550LiveTotals();
    for (var i = 0; i < 250; i++) t.apply('$i', {'kind': 'gift', 'points': 1});
    for (var tick = 0; tick < 200; tick++) {
      expect([t.comments, t.points, t.gifts], [0, 250, 250]);
    }
    t.apply('249', null);
    expect([t.points, t.gifts], [249, 249]);
  });
}
