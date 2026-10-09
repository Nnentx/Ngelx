import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/ngelx_message_state.dart';

void main() {
  test('unread count includes only recipient unread non-deleted items', () {
    final items = <Map<String, dynamic>>[
      {'recipientId': 'a', 'read': false},
      {'recipientId': 'a', 'read': true},
      {'recipientId': 'b', 'read': false},
      {'recipientId': 'a', 'deleted': true},
    ];
    expect(NgelxMessageState.unreadCount(items, 'a'), 1);
    expect(NgelxMessageState.unreadCount(items, ''), 0);
  });

  test('story expiry uses a 24 hour exclusive end boundary', () {
    final start = DateTime.utc(2026, 10, 10);
    expect(NgelxMessageState.isStoryActive(createdAt: start, now: start), isTrue);
    expect(NgelxMessageState.isStoryActive(createdAt: start, now: start.add(const Duration(hours: 24))), isFalse);
    expect(NgelxMessageState.isStoryActive(createdAt: start, now: start.subtract(const Duration(seconds: 1))), isFalse);
    expect(NgelxMessageState.storyRemaining(createdAt: start, now: start.add(const Duration(hours: 25))), Duration.zero);
  });
}
