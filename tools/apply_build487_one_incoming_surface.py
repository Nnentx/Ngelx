#!/usr/bin/env python3
"""Build487: one incoming visual surface and one audible ringtone owner.

Apply AFTER the older Build395..Build484 transforms. Leave all call signaling,
answer/reject, account checks, LiveKit sessions, and mini-call overlay intact.

Android's native CALL notification/full-screen activity owns incoming call UI
when notification permission is granted. Only when it is denied does Flutter
show its original in-app incoming banner as a fallback.

Android's CALL notification channel owns the audible ringing and preserves
existing per-channel mute/DND settings. The extra manually started ringtone
callback is removed; the original channel ID remains unchanged.
"""
from pathlib import Path

DART=Path("app/lib/main.dart")
SERVICE=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt")
MARKER="// Build487: native incoming UI owns Android call presentation"


def replace_one(src, old, new, label):
    matches=src.count(old)
    if matches!=1:
        raise RuntimeError(f"Build487 {label}: expected 1 matching anchor, got {matches}")
    return src.replace(old,new,1)


def patch_dart(src):
    if MARKER in src:return src
    start=src.index("class _AnaEkranState extends State<AnaEkran>")
    stop=src.index("  Widget _aktifSayfa()",start)
    segment=src[start:stop]
    segment=replace_one(segment,
        "  Widget gelenAramaKatmani(){",
        """  Widget gelenAramaKatmani(){
    // Build487: native incoming UI owns Android call presentation.
    // Do NOT show the legacy Flutter banner over the native CALL heads-up /
    // full-screen Activity. Preserve Flutter fallback if user denied the
    // Android notification permission; preserve existing non-Android UI.
    if(!kIsWeb && defaultTargetPlatform==TargetPlatform.android){
      return FutureBuilder<PermissionStatus>(
        future:Permission.notification.status,
        builder:(context,permission){
          if(permission.data==null||permission.data!.isGranted){
            return const SizedBox.shrink();
          }
          return _gelenAramaFlutterFallback487();
        },
      );
    }
    return _gelenAramaFlutterFallback487();
  }

  Widget _gelenAramaFlutterFallback487(){""","legacy banner gating")
    # No changes to Flutter's existing call answer/reject implementation:
    # when native notifications are denied, that legacy UI still works.
    for token in (
        "StreamBuilder<QuerySnapshot<Map<String,dynamic>>>",
        "callRoomName",
        "_gelenAramaButon(",
        "Navigator.push(context",
    ):
        if token not in segment:
            raise RuntimeError("Build487: missing original Flutter fallback contract: "+token)
    return src[:start]+segment+src[stop:]


def patch_service(src):
    marker="// Build487: notification channel is the sole audible ringtone."
    if marker in src:return src
    # Android notification is the one visual AND audible call owner. Keep its
    # original persisted channel ID and the user's sound, vibration and DND
    # preferences; FLAG_INSISTENT supplies the telephone-like repeating ring.
    # The historical manual RingtoneManager timer is the second ring: remove
    # only that callback after all older Build454..Build471 transformations.
    anchor="            alerts.put(room, timeout)?.let { timer.removeCallbacks(it) }\n"
    tail="            timer.postDelayed(timeout, 60000)"
    if src.count(anchor)!=1 or src.count(tail)!=1:
        raise RuntimeError("Build487 native notification lifecycle anchors drifted")
    begin=src.index(anchor)+len(anchor)
    finish=src.index(tail,begin)
    second=src[begin:finish]
    for token in ("timer.post {","sound.play()","ringing.put(room, sound)",
                  "AudioManager.RINGER_MODE_NORMAL","ring_blocked settings:"):
        if token not in second:
            raise RuntimeError("Build487 native manual ringing source drifted: "+token)
    assert second.rstrip().endswith("}")
    src=src[:begin]+"            "+marker+"\n"+src[finish:]
    for token in (
        'const val CHANNEL = "ngelx_incoming_calls467"',
        "channel.enableVibration(true)",
        "channel.setSound(ringtone, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE).build())",
        "setFullScreenIntent(fullScreenCall, true)",
        "Notification.FLAG_INSISTENT",
        "ringing.remove(room)",
        "fun isStillRinging470(room:",
        "manager.notify(room.hashCode(), notification)",
        "cancel(application, room)",
    ):
        if token not in src:
            raise RuntimeError("Build487 native system ringtone policy drifted: "+token)
    if "sound.play()" in src:
        raise RuntimeError("Build487: second ringtone source remained")
    return src


def main():
    files=((DART,patch_dart),(SERVICE,patch_service))
    changes=[]
    for file,fn in files:
        previous=file.read_text(encoding="utf-8")
        modified=fn(previous)
        changes.append((file,previous,modified))
    # All-or-nothing guards; don't write one file if the other drifts.
    for file,previous,modified in changes:
        if modified!=previous:
            file.write_text(modified,encoding="utf-8")
        print("Build487: checked",file,"changed=",modified!=previous)


if __name__=="__main__":
    main()
