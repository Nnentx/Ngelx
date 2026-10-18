#!/usr/bin/env python3
"""Build487: one incoming visual surface and one audible ringtone owner.

Apply AFTER the older Build395..Build484 transforms. Leave all call signaling,
answer/reject, account checks, LiveKit sessions, and mini-call overlay intact.

Android's native CALL notification/full-screen activity owns incoming call UI
when notification permission is granted. Only when it is denied does Flutter
show its original in-app incoming banner as a fallback.

Android's manually guarded RingtoneManager owns the audible ringing. The CALL
notification channel is intentionally SILENT (new ID needed because Android
never edits an existing channel's sound after creation).
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
    channel_old='const val CHANNEL = "ngelx_incoming_calls467"'
    channel_new='const val CHANNEL = "ngelx_incoming_calls487_one_ring"'
    if channel_new in src:return src
    src=replace_one(src,channel_old,channel_new,"fresh silent notification channel")
    src=replace_one(src,"channel.enableVibration(true)","channel.enableVibration(false)","one notification vibration policy")
    src=replace_one(src,
        "channel.setSound(ringtone, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE).build())",
        """// Build487: notification is the visual surface, NOT a second ringtone.
            // Manually guarded RingtoneManager below is the single audio owner.
            channel.setSound(null, null)""","channel sound")
    src=replace_one(src,
        ".setSound(ringtone, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE).build())",
        ".setSound(null)","pre Android 8 notification sound")
    src=replace_one(src,
        "notification.flags = notification.flags or Notification.FLAG_INSISTENT",
        "// Build487: do not trigger an insistent second system notification ring.","old insistent flag")
    for token in (
        "if(alerts.containsKey(room))",
        "sound.play()",
        "AudioManager.RINGER_MODE_NORMAL",
        "ringing.remove(room)",
        "setFullScreenIntent(fullScreenCall, true)",
        "rememberOwner470",
        "fun isStillRinging470(room:",
        "manager.notify(room.hashCode(), notification)",
    ):
        if token not in src:
            raise RuntimeError("Build487: missing retained native call contract: "+token)
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
