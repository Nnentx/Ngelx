// Local projection of live comment changes. Never performs network requests.
class Ngelx550LiveTotals {
  final Map<String, ({int comments, int points, int gifts})> _rows = {};
  int comments = 0, points = 0, gifts = 0;

  void apply(String id, Map<String, dynamic>? data) {
    final before = _rows.remove(id);
    if (before != null) {
      comments -= before.comments;
      points -= before.points;
      gifts -= before.gifts;
    }
    if (data == null) return;
    final kind = data['kind'] ?? 'comment';
    final row = (
      comments: kind == 'comment' ? 1 : 0,
      points: kind == 'gift' ? (data['points'] as num?)?.toInt() ?? 0 : 0,
      gifts: kind == 'gift'
          ? ((data['quantity'] as num?)?.toInt() ?? 1).clamp(1, 10).toInt()
          : 0,
    );
    _rows[id] = row;
    comments += row.comments;
    points += row.points;
    gifts += row.gifts;
  }
}
