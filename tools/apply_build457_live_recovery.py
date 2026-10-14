"""Build457 video recovery applied AFTER legacy live patches (448, 453, 456).

Never edit the source before Build448's git apply; those patches expect its
historical context. No live-data writes, token changes, or media-upload edits.
"""
from pathlib import Path

SOURCE=Path("app/lib/live_broadcast_studio.dart")

HELPER="""// A missing live camera track should not leave a permanent spinner.
bool ngelx457CanRetryLiveVideo({
  required bool cameraEnabled,
  required bool reconnecting,
  required int elapsedWithoutVideoSeconds,
}) => cameraEnabled && !reconnecting && elapsedWithoutVideoSeconds >= 10;

"""

METHOD="""  Future<void> _recoverLiveVideo() async {
    if (_recoveringVideo || kapatildi || yayinBitti) return;
    _recoveringVideo = true;
    if (mounted) setState(() {});
    try {
      if (widget.yayinSahibi) {
        if (!kameraAcik) return;
        final local = widget.oda.localParticipant;
        if (local == null) throw StateError('Kamera katılımcısı bulunamadı');
        await local.setCameraEnabled(false);
        await Future<void>.delayed(const Duration(milliseconds: 180));
        if (kapatildi || yayinBitti) return;
        await local.setCameraEnabled(true,
          cameraCaptureOptions: widget.kameraAyarlari.copyWith(
            cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front,
          ),
        );
      } else {
        // Force the receiver to obtain a new subscription when the video
        // track is absent despite an active room connection.
        await widget.oda.disconnect();
        if (kapatildi || yayinBitti) return;
        await _otomatikYenidenBaglan();
      }
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Yayın görüntüsü yenilenemedi. Tekrar dene.')),
        );
      }
    } finally {
      _lastVisibleVideoSecond = saniye;
      _recoveringVideo = false;
      if (mounted) setState(() {});
    }
  }

"""

FALLBACK_OLD="""    return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      const CircularProgressIndicator(color:Colors.white),
      const SizedBox(height:12),
      Text(saniye<8?'Yayın görüntüsü hazırlanıyor…':'Yayın görüntüsü alınamadı. Bağlantı sürüyorsa kamerayı yeniden açmayı dene.',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
    ]));
  }"""

FALLBACK_NEW="""    // Build448 increments this notifier without rebuilding the whole video
    // surface. Subscribe here so the 10-second retry action really appears.
    return ValueListenableBuilder<int>(
      valueListenable: _clock448,
      builder: (_, seconds, __) {
        final canRetry = ngelx457CanRetryLiveVideo(
          cameraEnabled: true,
          reconnecting: _recoveringVideo,
          elapsedWithoutVideoSeconds: seconds - _lastVisibleVideoSecond,
        );
        return ColoredBox(
          color: Colors.black,
          child: Center(child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 30),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              if (!canRetry)
                const CircularProgressIndicator(color: Colors.white)
              else
                const Icon(Icons.videocam_off_outlined, color: Colors.white70, size: 48),
              const SizedBox(height: 12),
              Text(
                canRetry
                    ? 'Yayın görüntüsü alınamadı. Bağlantıyı ve kamera izinlerini kontrol et.'
                    : 'Yayın görüntüsü hazırlanıyor…',
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w700),
              ),
              if (canRetry) ...[
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: _recoverLiveVideo,
                  icon: const Icon(Icons.refresh_rounded),
                  label: Text(widget.yayinSahibi
                      ? 'Kamerayı yeniden başlat'
                      : 'Yayına yeniden bağlan'),
                ),
              ],
            ]),
          )),
        );
      },
    );
  }"""

def replace_once(s,old,new,reason):
    found=s.count(old)
    if found != 1:
        raise ValueError(f"live {reason}: expected 1 anchor, got {found}")
    return s.replace(old,new,1)

def transform(source):
    if "bool ngelx457CanRetryLiveVideo({" in source:
        return source
    source=replace_once(source,
        "class _CanliYayinPageState extends State<CanliYayinPage> {",
        HELPER+"class _CanliYayinPageState extends State<CanliYayinPage> {\n  int _lastVisibleVideoSecond = 0;\n  bool _recoveringVideo = false;",
        "live state and helper")
    source=replace_once(source,
        "  Widget _goruntuYokEkrani(){",
        METHOD+"  Widget _goruntuYokEkrani(){",
        "recover method")
    source=replace_once(source,FALLBACK_OLD,FALLBACK_NEW,"finite fallback")
    source=replace_once(source,
        "    final track = _goruntu();\n",
        "    final track = _goruntu();\n    if (track != null) _lastVisibleVideoSecond = saniye;\n",
        "visible track reset")
    # Build448 already supplies _liveStream448. Reuse it without another listener.
    if "_liveStream448" not in source:
        raise ValueError("Build448 live stream is missing: wrong patch order")
    return source

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if before!=after:
        SOURCE.write_text(after)
    print("Build457: live recovery applied after all legacy patches")

if __name__=="__main__":
    main()
