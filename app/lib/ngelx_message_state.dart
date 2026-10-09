/// Shared, side-effect-free rules for inbox and story UI state.
/// Kept separate from existing screens so current navigation is unchanged.
class NgelxMessageState {
  const NgelxMessageState._();

  static int unreadCount(Iterable<Map<String, dynamic>> items, String userId) {
    if (userId.isEmpty) return 0;
    return items.where((item) {
      if (item['recipientId'] != userId) return false;
      if (item['deleted'] == true) return false;
      if (item['read'] == true) return false;
      return true;
    }).length;
  }

  static bool isStoryActive({required DateTime createdAt, required DateTime now,
    Duration lifetime = const Duration(hours: 24)}) {
    if (lifetime <= Duration.zero) return false;
    return !createdAt.isAfter(now) && now.isBefore(createdAt.add(lifetime));
  }

  static Duration storyRemaining({required DateTime createdAt, required DateTime now,
    Duration lifetime = const Duration(hours: 24)}) {
    final remaining = createdAt.add(lifetime).difference(now);
    return remaining.isNegative ? Duration.zero : remaining;
  }
}
