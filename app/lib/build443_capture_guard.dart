import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

/// One native lease per mounted profile; descendants keep their parent's lease.
class NgelxProfileCaptureGuard extends StatefulWidget {
  final String uid;
  final Widget child;
  final Stream<bool>? privacyStream;
  const NgelxProfileCaptureGuard({super.key, required this.uid, required this.child, this.privacyStream});
  @override
  State<NgelxProfileCaptureGuard> createState() => _ProfileCaptureGuardState();
}

class _ProfileCaptureGuardState extends State<NgelxProfileCaptureGuard> {
  static const _channel = MethodChannel('com.nnentx.ngelx_app/capture');
  static int _nextLease = 0;
  late final String _lease = 'profile-${++_nextLease}';
  StreamSubscription<bool>? _subscription;
  int _generation = 0;
  int _policyRevision = 0;
  bool _ready = false;
  bool _failed = false;
  bool get _android => !kIsWeb && defaultTargetPlatform == TargetPlatform.android;

  @override
  void initState() { super.initState(); _start(); }

  @override
  void didUpdateWidget(covariant NgelxProfileCaptureGuard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.uid != widget.uid) _start();
  }

  void _start() {
    final generation = ++_generation;
    unawaited(_subscription?.cancel());
    _subscription = null;
    _ready = false;
    _failed = false;
    if (!_android) { _ready = true; return; }
    // Unknown, cached, missing and failed preferences always keep protection.
    unawaited(_apply(true, generation).then((_) {
      if (!mounted || generation != _generation || _failed || widget.uid.isEmpty) return;
      final stream = widget.privacyStream ?? FirebaseFirestore.instance.collection('users').doc(widget.uid)
          .snapshots(includeMetadataChanges: true).map((snapshot) =>
              !snapshot.metadata.isFromCache && !snapshot.metadata.hasPendingWrites &&
              snapshot.exists && snapshot.data()?['allowProfileCapture'] == true);
      _subscription = stream.listen((allow) {
        unawaited(_apply(!allow, generation));
      }, onError: (Object _) { unawaited(_apply(true, generation)); });
    }));
  }

  Future<void> _apply(bool secure, int generation) async {
    if (!mounted || generation != _generation) return;
    final revision = ++_policyRevision;
    // Hide content until Android acknowledges the requested window policy.
    setState(() { _ready = false; _failed = false; });
    try {
      await _channel.invokeMethod<void>('setCaptureLease', {'lease': _lease, 'secure': secure});
      if (mounted && generation == _generation && revision == _policyRevision) setState(() => _ready = true);
    } catch (_) {
      if (mounted && generation == _generation && revision == _policyRevision) setState(() { _ready = false; _failed = true; });
    }
  }

  @override
  void dispose() {
    ++_generation;
    unawaited(_subscription?.cancel());
    if (_android) {
      // Keep the final profile frame protected until it has left the surface.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        unawaited(_channel.invokeMethod<void>('setCaptureLease', {'lease': _lease, 'secure': false})
            .catchError((Object _) {}));
      });
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Preserve descendants and their leases during asynchronous policy changes.
    // Offstage content cannot paint, receive taps or contribute capture pixels.
    return Stack(fit: StackFit.expand, children: [
      Offstage(offstage: !_ready, child: widget.child),
      if (!_ready) ColoredBox(color: Colors.white, child: Center(child: _failed
          ? IconButton(icon: const Icon(Icons.refresh), onPressed: _start)
          : const CircularProgressIndicator())),
    ]);
  }
}
