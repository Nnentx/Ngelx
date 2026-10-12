/// Keep stored filter identifiers stable across UI translations.
bool ngelx445ChatFilter(String filter, {required bool group, required bool pending, required bool hidden}) {
  if (hidden || pending) return false;
  switch (filter) {
    case 'Tümü': return true;
    case 'Mesajlar': return !group;
    case 'Gruplar': return group;
    default: return false;
  }
}
int ngelx445AllUnread(int privateUnread, int groupUnread) => privateUnread + groupUnread;
