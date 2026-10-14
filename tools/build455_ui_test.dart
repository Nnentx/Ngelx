import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import '../lib/main.dart';

class LocalVideo455 extends VideoPlayerController {
  LocalVideo455() : super.networkUrl(Uri.parse('https://example.invalid/video')) {
    value = const VideoPlayerValue(duration: Duration(seconds: 10), isInitialized: true, size: Size(100, 200));
  }
  @override Future<void> setVolume(double volume) async { value = value.copyWith(volume: volume); }
  @override Future<void> play() async { value = value.copyWith(isPlaying: true); }
  @override Future<void> pause() async { value = value.copyWith(isPlaying: false); }
}

void main() {
  test('offscreen and barely visible posts do not count as viewed', () {
    const viewport = Rect.fromLTWH(0, 50, 320, 600);
    expect(ngelx455PostVisible(const Rect.fromLTWH(0, 700, 320, 200), viewport), isFalse);
    expect(ngelx455PostVisible(const Rect.fromLTWH(0, 600, 320, 200), viewport), isFalse);
    expect(ngelx455PostVisible(const Rect.fromLTWH(0, 100, 320, 200), viewport), isTrue);
    expect(ngelx455PostVisible(const Rect.fromLTWH(0, 50, 320, 1400), viewport), isTrue);
  });
  test('empty and brand placeholders fall through to the actual person name', () {
    expect(ngelx455ProfileName({'displayName':'', 'name':'Asya Sever'}), 'Asya Sever');
    expect(ngelx455ProfileName({'displayName':'NgelX','username':'ahsen'}), 'ahsen');
    expect(ngelx455ProfileName({'displayName':'  ADEM baykar  '}), 'ADEM baykar');
    expect(ngelx455ProfileName({},fallback:'Yükleniyor…'), 'Yükleniyor…');
  });
  test('feed video responds silently during a call and restores its volume afterwards', () async {
    final changed = ngelxCallSession444.onChanged;
    ngelxCallSession444.onChanged = null;
    final video = LocalVideo455();
    try {
      await video.setVolume(.6);
      expect(ngelxCallSession444.reserve('test455'), isTrue);
      await ngelx444MediaPlay(video);
      expect(video.value.isPlaying, isTrue);
      expect(video.value.volume, 0);
      ngelxCallSession444.release('test455');
      await ngelx444MediaPlay(video);
      expect(video.value.volume, .6);
    } finally {
      ngelxCallSession444.release('test455');
      ngelxCallSession444.onChanged = changed;
      await video.pause();
    }
  });
}
