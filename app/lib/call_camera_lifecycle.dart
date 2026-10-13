class CallCameraLifecycle {
  final Future<void> Function(bool) apply;
  bool cameraWanted = true, foreground = true, _stopped = false;
  bool? _applied;
  Future<void> _queue = Future<void>.value();
  CallCameraLifecycle(this.apply);
  Future<void> setForeground(bool value) { foreground = value; return sync(); }
  Future<void> setCameraWanted(bool value) { cameraWanted = value; return sync(); }
  Future<void> sync({bool force = false}) {
    final next = _queue.catchError((_) {}).then((_) async {
      if (_stopped) return;
      final target = foreground && cameraWanted;
      if (!force && _applied == target) return;
      await apply(target);
      _applied = target;
    });
    _queue = next;
    return next;
  }
  void stop() { _stopped = true; }
}
