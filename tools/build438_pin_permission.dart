bool ngelx438CanPin(Map<String, dynamic> group, String? uid) {
  if (uid == null || uid.isEmpty || group['isGroup'] != true) return false;
  final members = group['members'];
  if (members is! Iterable || !members.contains(uid)) return false;
  final admins = group['admins'];
  return group['createdBy'] == uid ||
      (admins is Iterable && admins.contains(uid)) ||
      group['onlyAdminsCanPin'] == false;
}
