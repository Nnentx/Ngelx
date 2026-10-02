
import 'dart:async';

import 'package:banuba_sdk/banuba_sdk.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

/// NgelX Pro Beauty kamera.
///
/// Kalite kuralı:
/// - BANUBA_CLIENT_TOKEN yoksa bu ekran açılmaz.
/// - Eski "tüm kareye blur/parlaklık" rötuşu burada kullanılmaz.
/// - Yüz işlemleri TouchUp effect içindeki Skin / FaceMorph / Eyes / Teeth
///   operatörlerine gider.
///
/// Build:
/// flutter build apk --dart-define=BANUBA_CLIENT_TOKEN=...
///
/// Resmi TouchUp effect paketi app/effects/TouchUp altında bulunmalıdır.
class NgelXProBeautyCameraPage extends StatefulWidget {
  final bool baslangicVideo;
  final Duration maxVideo;

  const NgelXProBeautyCameraPage({
    super.key,
    this.baslangicVideo = false,
    this.maxVideo = const Duration(minutes: 10),
  });

  static const String clientToken = String.fromEnvironment(
    'BANUBA_CLIENT_TOKEN',
    defaultValue: '',
  );

  static const String effectPath = String.fromEnvironment(
    'BANUBA_TOUCHUP_EFFECT',
    defaultValue: 'effects/TouchUp',
  );

  static bool get isConfigured => clientToken.trim().isNotEmpty;

  @override
  State<NgelXProBeautyCameraPage> createState() =>
      _NgelXProBeautyCameraPageState();
}

class _NgelXProBeautyCameraPageState
    extends State<NgelXProBeautyCameraPage> with WidgetsBindingObserver {
  final BanubaSdkManager _sdk = BanubaSdkManager();
  final EffectPlayerWidget _player = EffectPlayerWidget(key: null);

  late final List<_BeautyFeature> _features = <_BeautyFeature>[
    _BeautyFeature(
      key: 'smooth',
      label: 'Pürüzsüz',
      icon: Icons.water_drop_outlined,
      min: 0,
      max: 1,
      script: (v) => <String>[
        'Skin.softening(' + (v * 100).toStringAsFixed(2) + ')'
      ],
    ),
    _BeautyFeature(
      key: 'eyes',
      label: 'Göz',
      icon: Icons.remove_red_eye_outlined,
      min: -0.35,
      max: 0.35,
      script: (v) => <String>[
        'FaceMorph.eyes({enlargement: ' +
            (v * 100).toStringAsFixed(2) +
            '})'
      ],
    ),
    _BeautyFeature(
      key: 'nose',
      label: 'Burun',
      icon: Icons.face_retouching_natural_outlined,
      min: -0.35,
      max: 0.35,
      script: (v) => <String>[
        'FaceMorph.nose({width: ' +
            (v * 100).toStringAsFixed(2) +
            ', length: ' +
            (v * 70).toStringAsFixed(2) +
            ', tip_width: ' +
            (-v * 100).toStringAsFixed(2) +
            '})'
      ],
    ),
    _BeautyFeature(
      key: 'face',
      label: 'Yüz',
      icon: Icons.face_6_outlined,
      min: -0.35,
      max: 0.35,
      script: (v) => <String>[
        'FaceMorph.face({narrowing: ' +
            (v * 100).toStringAsFixed(2) +
            '})'
      ],
    ),
    _BeautyFeature(
      key: 'jaw',
      label: 'Çene',
      icon: Icons.account_circle_outlined,
      min: -0.30,
      max: 0.30,
      script: (v) => <String>[
        'FaceMorph.face({jaw_narrowing: ' +
            (v * 100).toStringAsFixed(2) +
            ', chin_narrowing: ' +
            (v * 70).toStringAsFixed(2) +
            '})'
      ],
    ),
    _BeautyFeature(
      key: 'lips',
      label: 'Dudak',
      icon: Icons.sentiment_satisfied_alt_outlined,
      min: -0.30,
      max: 0.30,
      script: (v) => <String>[
        'FaceMorph.lips({size: ' +
            (v * 100).toStringAsFixed(2) +
            '})'
      ],
    ),
    _BeautyFeature(
      key: 'eyeWhite',
      label: 'Göz ışığı',
      icon: Icons.auto_awesome_outlined,
      min: 0,
      max: 1,
      script: (v) => <String>[
        'Eyes.whitening(' + (v * 100).toStringAsFixed(2) + ')'
      ],
    ),
    _BeautyFeature(
      key: 'teeth',
      label: 'Diş',
      icon: Icons.brightness_7_outlined,
      min: 0,
      max: 1,
      script: (v) => <String>[
        'Teeth.whitening(' + (v * 100).toStringAsFixed(2) + ')'
      ],
    ),
  ];

  final Map<String, double> _values = <String, double>{};

  bool _ready = false;
  bool _loading = true;
  bool _front = true;
  bool _flash = false;
  bool _video = false;
  bool _recording = false;
  bool _beautyOpen = false;
  bool _toolsExpanded = true;
  int _timerSeconds = 0;
  int _activeCountdown = 0;
  String _ratio = '9:16';
  String? _error;
  String _selectedFeature = 'smooth';
  double _zoom = 1;
  double _zoomStart = 1;
  Duration _recordingDuration = Duration.zero;
  Timer? _recordingTimer;
  String? _recordingPath;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _video = widget.baslangicVideo;
    for (final f in _features) {
      _values[f.key] = 0;
    }
    unawaited(_initialize());
  }

  Future<void> _initialize() async {
    if (!NgelXProBeautyCameraPage.isConfigured) {
      if (mounted) {
        setState(() {
          _loading = false;
          _error =
              'Pro güzellik motoru yapılandırılmadı. Kalitesiz yedek efekt gösterilmiyor.';
        });
      }
      return;
    }

    try {
      final camera = await Permission.camera.request();
      if (!camera.isGranted) {
        throw Exception('Kamera izni verilmedi.');
      }
      if (_video) {
        final mic = await Permission.microphone.request();
        if (!mic.isGranted) {
          throw Exception('Video için mikrofon izni verilmedi.');
        }
      }

      await _sdk.initialize(
        const <String>[],
        NgelXProBeautyCameraPage.clientToken,
        SeverityLevel.info,
      );
      await _sdk.openCamera();
      await _sdk.attachWidget(_player.banubaId);
      _sdk.startPlayer();
      _sdk.loadEffect(NgelXProBeautyCameraPage.effectPath, false);

      if (!mounted) return;
      setState(() {
        _ready = true;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _error = 'Pro kamera başlatılamadı: ' + e.toString();
      });
    }
  }

  void _eval(List<String> scripts) {
    if (!_ready) return;
    for (final script in scripts) {
      _sdk.evalJs(script);
    }
  }

  void _setFeature(_BeautyFeature feature, double value) {
    final safe = value.clamp(feature.min, feature.max).toDouble();
    setState(() {
      _selectedFeature = feature.key;
      _values[feature.key] = safe;
    });
    _eval(feature.script(safe));
  }

  void _resetBeauty() {
    for (final f in _features) {
      _values[f.key] = 0;
      _eval(f.script(0));
    }
    if (mounted) setState(() {});
  }

  Future<String> _newPath(String prefix, String ext) async {
    final dir = await getTemporaryDirectory();
    return dir.path +
        '/' +
        prefix +
        DateTime.now().microsecondsSinceEpoch.toString() +
        ext;
  }

  Future<void> _capture() async {
    if (!_ready || _activeCountdown > 0) return;

    if (_timerSeconds > 0) {
      for (var i = _timerSeconds; i > 0; i--) {
        if (!mounted) return;
        setState(() => _activeCountdown = i);
        await Future<void>.delayed(const Duration(seconds: 1));
      }
      if (!mounted) return;
      setState(() => _activeCountdown = 0);
    }

    if (_video) {
      if (_recording) {
        await _stopVideo();
      } else {
        await _startVideo();
      }
    } else {
      await _takePhoto();
    }
  }

  Future<void> _takePhoto() async {
    try {
      final path = await _newPath('ngelx_pro_photo_', '.png');
      await _sdk.takePhoto(path, 1080, 1920);
      if (!mounted) return;
      Navigator.pop<Map<String, dynamic>>(context, <String, dynamic>{
        'file': XFile(path, mimeType: 'image/png'),
        'video': false,
        'mimeType': 'image/png',
        'proBeauty': true,
        'engine': 'banuba_touchup',
      });
    } catch (e) {
      _showError('Fotoğraf alınamadı: ' + e.toString());
    }
  }

  Future<void> _startVideo() async {
    try {
      final mic = await Permission.microphone.request();
      if (!mic.isGranted) {
        _showError('Video için mikrofon izni gerekli.');
        return;
      }
      final path = await _newPath('ngelx_pro_video_', '.mp4');
      await _sdk.startVideoRecording(path, true, 720, 1280);
      _recordingPath = path;
      _recordingDuration = Duration.zero;
      _recordingTimer?.cancel();
      _recordingTimer = Timer.periodic(const Duration(seconds: 1), (_) {
        if (!mounted) return;
        final next = _recordingDuration + const Duration(seconds: 1);
        if (next >= widget.maxVideo) {
          unawaited(_stopVideo());
          return;
        }
        setState(() => _recordingDuration = next);
      });
      if (mounted) setState(() => _recording = true);
    } catch (e) {
      _showError('Video başlatılamadı: ' + e.toString());
    }
  }

  Future<void> _stopVideo() async {
    if (!_recording) return;
    try {
      await _sdk.stopVideoRecording();
      _recordingTimer?.cancel();
      final path = _recordingPath;
      if (!mounted || path == null) return;
      setState(() => _recording = false);
      Navigator.pop<Map<String, dynamic>>(context, <String, dynamic>{
        'file': XFile(path, mimeType: 'video/mp4'),
        'video': true,
        'mimeType': 'video/mp4',
        'proBeauty': true,
        'engine': 'banuba_touchup',
        'durationMs': _recordingDuration.inMilliseconds,
      });
    } catch (e) {
      _showError('Video tamamlanamadı: ' + e.toString());
    }
  }

  void _flipCamera() {
    if (!_ready || _recording) return;
    _front = !_front;
    _sdk.setCameraFacing(_front);
    if (mounted) setState(() {});
  }

  void _toggleFlash() {
    if (!_ready || _front) return;
    _flash = !_flash;
    _sdk.enableFlashlight(_flash);
    if (mounted) setState(() {});
  }

  void _setZoom(double value) {
    _zoom = value.clamp(1.0, 4.0).toDouble();
    _sdk.setZoom(_zoom);
    if (mounted) setState(() {});
  }

  void _showError(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(message)));
  }

  String get _recordingLabel {
    final mm = _recordingDuration.inMinutes.toString().padLeft(2, '0');
    final ss =
        (_recordingDuration.inSeconds % 60).toString().padLeft(2, '0');
    return mm + ':' + ss;
  }

  _BeautyFeature get _activeFeature =>
      _features.firstWhere((f) => f.key == _selectedFeature);

  Widget _tool(
    IconData icon,
    String label,
    VoidCallback? onTap, {
    bool active = false,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 9),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          InkWell(
            onTap: onTap,
            borderRadius: BorderRadius.circular(28),
            child: Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: active
                    ? const Color(0xFF7A46F6)
                    : Colors.black.withValues(alpha: 0.50),
                border: Border.all(color: Colors.white24),
              ),
              child: Icon(icon, color: Colors.white, size: 25),
            ),
          ),
          if (label.isNotEmpty) ...<Widget>[
            const SizedBox(height: 3),
            Text(
              label,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 9.5,
                fontWeight: FontWeight.w700,
                shadows: <Shadow>[
                  Shadow(color: Colors.black87, blurRadius: 4)
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _beautyPanel() {
    final feature = _activeFeature;
    final current = _values[feature.key] ?? 0;
    final scale = feature.max.abs() > feature.min.abs()
        ? feature.max.abs()
        : feature.min.abs();
    final percent =
        scale <= 0 ? 0 : ((current / scale) * 100).round();

    return Align(
      alignment: Alignment.bottomCenter,
      child: Container(
        margin: const EdgeInsets.fromLTRB(8, 0, 8, 112),
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 14),
        decoration: BoxDecoration(
          color: const Color(0xEE0B0B0F),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: Colors.white10),
        ),
        child: SafeArea(
          top: false,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Row(
                children: <Widget>[
                  const Text(
                    'Yüz',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 17,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  const Spacer(),
                  TextButton.icon(
                    onPressed: _resetBeauty,
                    icon: const Icon(Icons.restart_alt_rounded, size: 18),
                    label: const Text('Sıfırla'),
                  ),
                  IconButton(
                    onPressed: () => setState(() => _beautyOpen = false),
                    icon: const Icon(
                      Icons.keyboard_arrow_down_rounded,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 80,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  itemCount: _features.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 10),
                  itemBuilder: (_, i) {
                    final f = _features[i];
                    final selected = f.key == _selectedFeature;
                    final changed =
                        (_values[f.key] ?? 0).abs() > 0.001;
                    return InkWell(
                      onTap: () =>
                          setState(() => _selectedFeature = f.key),
                      borderRadius: BorderRadius.circular(16),
                      child: SizedBox(
                        width: 64,
                        child: Column(
                          children: <Widget>[
                            Stack(
                              clipBehavior: Clip.none,
                              children: <Widget>[
                                AnimatedContainer(
                                  duration:
                                      const Duration(milliseconds: 150),
                                  width: 48,
                                  height: 48,
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    color: selected
                                        ? const Color(0xFF202127)
                                        : Colors.white12,
                                    border: Border.all(
                                      color: selected
                                          ? const Color(0xFFFF2D55)
                                          : Colors.white24,
                                      width: selected ? 2.5 : 1,
                                    ),
                                  ),
                                  child: Icon(
                                    f.icon,
                                    color: Colors.white,
                                    size: 24,
                                  ),
                                ),
                                if (changed)
                                  const Positioned(
                                    right: -1,
                                    bottom: -1,
                                    child: CircleAvatar(
                                      radius: 4,
                                      backgroundColor: Colors.white,
                                    ),
                                  ),
                              ],
                            ),
                            const SizedBox(height: 5),
                            Text(
                              f.label,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                color: selected
                                    ? Colors.white
                                    : Colors.white70,
                                fontSize: 10,
                                fontWeight: selected
                                    ? FontWeight.w900
                                    : FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
              Row(
                children: <Widget>[
                  SizedBox(
                    width: 48,
                    child: Text(
                      percent.toString(),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  Expanded(
                    child: Slider(
                      min: feature.min,
                      max: feature.max,
                      value: current
                          .clamp(feature.min, feature.max)
                          .toDouble(),
                      activeColor: const Color(0xFFFF2D55),
                      inactiveColor: Colors.white24,
                      onChanged: (v) => _setFeature(feature, v),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (!_ready) return;
    if (state == AppLifecycleState.resumed) {
      _sdk.startPlayer();
    } else if (state == AppLifecycleState.inactive ||
        state == AppLifecycleState.paused) {
      _sdk.stopPlayer();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _recordingTimer?.cancel();
    _sdk.unloadEffect();
    _sdk.stopPlayer();
    _sdk.closeCamera();
    _sdk.deinitialize();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
      );
    }

    if (_error != null) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(28),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  const Icon(
                    Icons.auto_awesome_rounded,
                    color: Colors.white,
                    size: 54,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    _error!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w800,
                      height: 1.35,
                    ),
                  ),
                  const SizedBox(height: 20),
                  OutlinedButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Geri dön'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          fit: StackFit.expand,
          children: <Widget>[
            GestureDetector(
              onScaleStart: (_) => _zoomStart = _zoom,
              onScaleUpdate: (d) {
                if (d.pointerCount < 2) return;
                _setZoom(_zoomStart * d.scale);
              },
              child: ClipRRect(
                borderRadius: BorderRadius.circular(28),
                child: _player,
              ),
            ),
            Positioned(
              top: 10,
              left: 10,
              right: 10,
              child: Row(
                children: <Widget>[
                  _tool(
                    Icons.close_rounded,
                    '',
                    () => Navigator.pop(context),
                  ),
                  const Spacer(),
                  if (_recording)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 7,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFFF3B30),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: Text(
                        _recordingLabel,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                ],
              ),
            ),
            Positioned(
              right: 10,
              top: 70,
              child: Column(
                children: <Widget>[
                  _tool(
                    _toolsExpanded
                        ? Icons.keyboard_arrow_up_rounded
                        : Icons.keyboard_arrow_down_rounded,
                    '',
                    () =>
                        setState(() => _toolsExpanded = !_toolsExpanded),
                  ),
                  if (_toolsExpanded) ...<Widget>[
                    _tool(
                      Icons.cameraswitch_rounded,
                      'Çevir',
                      _recording ? null : _flipCamera,
                    ),
                    _tool(
                      _flash
                          ? Icons.flash_on_rounded
                          : Icons.flash_off_rounded,
                      'Flaş',
                      _front ? null : _toggleFlash,
                      active: _flash,
                    ),
                    _tool(
                      Icons.timer_outlined,
                      _timerSeconds == 0
                          ? 'Sayaç'
                          : _timerSeconds.toString() + 's',
                      _recording
                          ? null
                          : () => setState(() {
                                _timerSeconds = _timerSeconds == 0
                                    ? 3
                                    : _timerSeconds == 3
                                        ? 10
                                        : 0;
                              }),
                      active: _timerSeconds > 0,
                    ),
                    _tool(
                      Icons.aspect_ratio_rounded,
                      _ratio,
                      _recording
                          ? null
                          : () => setState(() {
                                _ratio = _ratio == '9:16'
                                    ? '1:1'
                                    : _ratio == '1:1'
                                        ? '16:9'
                                        : '9:16';
                              }),
                      active: _ratio != '9:16',
                    ),
                    _tool(
                      Icons.face_retouching_natural_rounded,
                      'Rötuş',
                      () => setState(
                        () => _beautyOpen = !_beautyOpen,
                      ),
                      active: _beautyOpen ||
                          _values.values
                              .any((v) => v.abs() > 0.001),
                    ),
                  ],
                ],
              ),
            ),
            if (_activeCountdown > 0)
              Center(
                child: Text(
                  _activeCountdown.toString(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 100,
                    fontWeight: FontWeight.w900,
                    shadows: <Shadow>[
                      Shadow(color: Colors.black87, blurRadius: 20),
                    ],
                  ),
                ),
              ),
            if (_beautyOpen) _beautyPanel(),
            Positioned(
              left: 12,
              right: 12,
              bottom: 16,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      TextButton(
                        onPressed: _recording
                            ? null
                            : () =>
                                setState(() => _video = false),
                        child: Text(
                          'FOTOĞRAF',
                          style: TextStyle(
                            color: !_video
                                ? Colors.white
                                : Colors.white54,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      GestureDetector(
                        onTap: () => unawaited(_capture()),
                        child: AnimatedContainer(
                          duration:
                              const Duration(milliseconds: 160),
                          width: 86,
                          height: 86,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: _recording
                                ? const Color(0xFFFF3B30)
                                : Colors.white,
                            border:
                                Border.all(color: Colors.white, width: 5),
                            boxShadow: const <BoxShadow>[
                              BoxShadow(
                                color: Colors.black54,
                                blurRadius: 14,
                              ),
                            ],
                          ),
                          child: Icon(
                            _recording
                                ? Icons.stop_rounded
                                : _video
                                    ? Icons.videocam_rounded
                                    : Icons.camera_alt_rounded,
                            color: _recording
                                ? Colors.white
                                : Colors.black,
                            size: 34,
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      TextButton(
                        onPressed: _recording
                            ? null
                            : () async {
                                final mic = await Permission.microphone
                                    .request();
                                if (!mic.isGranted) {
                                  _showError(
                                    'Video için mikrofon izni gerekli.',
                                  );
                                  return;
                                }
                                if (mounted) {
                                  setState(() => _video = true);
                                }
                              },
                        child: Text(
                          'VİDEO',
                          style: TextStyle(
                            color:
                                _video ? Colors.white : Colors.white54,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ),
                    ],
                  ),
                  if (_zoom > 1.01)
                    Text(
                      _zoom.toStringAsFixed(1) + 'x',
                      style: const TextStyle(
                        color: Colors.white70,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _BeautyFeature {
  final String key;
  final String label;
  final IconData icon;
  final double min;
  final double max;
  final List<String> Function(double value) script;

  const _BeautyFeature({
    required this.key,
    required this.label,
    required this.icon,
    required this.min,
    required this.max,
    required this.script,
  });
}
