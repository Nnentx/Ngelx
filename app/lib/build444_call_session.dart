/// Process-wide call ownership, including pending launches and minimized calls.
/// A generation prevents a late asynchronous connection from reviving an ended call.
class NgelxCallSession444 {
  String? room;
  bool attached = false;
  bool background = false;
  int generation = 0;
  void Function()? onChanged;
  bool get busy => room != null;
  bool reserve(String name) {
    if (name.isEmpty || busy) return false;
    room = name;
    generation++;
    onChanged?.call();
    return true;
  }
  bool attach(String name) {
    if (room == null && !reserve(name)) return false;
    if (room != name || attached) return false;
    attached = true;
    background = false;
    return true;
  }
  bool current(String name, int epoch) => room == name && generation == epoch;
  void minimize(String name) {
    if (room != name) return;
    attached = false;
    background = true;
  }
  void releasePending(String name) {
    if (room == name && !attached && !background) release(name);
  }
  void release(String name) {
    if (room != name) return;
    room = null;
    attached = background = false;
    generation++;
    onChanged?.call();
  }
}
