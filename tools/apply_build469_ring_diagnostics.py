#!/usr/bin/env python3
"""Build469 call-ring cause tracing (no DND bypass, no account/payload logging).
Keep existing ringtone lifecycle and push transport intact.
"""
from pathlib import Path
SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
TAG='// Build469 incoming-ring QA: record safe reasons for silent/dropped calls'
def one(s,old,new,label):
    if s.count(old)!=1:raise RuntimeError(f'Build469 native ringtone {label}: {s.count(old)}')
    return s.replace(old,new,1)
def transform(src):
    if TAG in src:return src
    s=one(src,'import android.os.Looper\n','import android.os.Looper\nimport android.util.Log\n','import logger')
    s=one(s,
      """        val d = message.data
        if (d["recipientUid"] != FirebaseAuth.getInstance().currentUser?.uid) return
        val room = d["roomName"] ?: return""",
      """        // Build469 incoming-ring QA: record safe reasons for silent/dropped calls.
        // Never log UIDs, names, chat IDs or tokens.
        val d = message.data
        val signedIn = FirebaseAuth.getInstance().currentUser?.uid
        if (signedIn == null) {
            Log.w("NgelxIncoming", "push_ignored_auth_not_ready")
            return
        }
        if (d["recipientUid"] != signedIn) {
            Log.w("NgelxIncoming", "push_ignored_different_recipient")
            return
        }
        val room = d["roomName"] ?: run {
            Log.w("NgelxIncoming", "push_ignored_missing_room")
            return
        }""",'push account gate')
    s=one(s,
      """        if (expires <= System.currentTimeMillis()) return
        val chat = d["chatId"] ?: return
        if (d["kind"] != "incoming_call") return
        show(this, chat, room, d["title"] ?: "NgelX araması", d["video"] == "true")""",
      """        if (expires <= System.currentTimeMillis()) {
            Log.i("NgelxIncoming", "push_ignored_expired")
            return
        }
        val chat = d["chatId"] ?: return
        if (d["kind"] != "incoming_call") return
        Log.i("NgelxIncoming", "incoming_call_delivered kind=" + (if (d["video"] == "true") "video" else "voice"))
        show(this, chat, room, d["title"] ?: "NgelX araması", d["video"] == "true")""",'incoming delivered trace')
    s=one(s,
      'if(alerts.containsKey(room)) return // Do not replace an already ringing notification from the Firestore observer.',
      '''if(alerts.containsKey(room)) {
                Log.i("NgelxIncoming", "already_ringing_same_call")
                return
            } // Do not replace an already ringing notification from the Firestore observer.''','duplicate call trace')
    s=one(s,
      """                if(allowed) try {
                    val sound = RingtoneManager.getRingtone(application, ringtone)""",
      """                if(!allowed) Log.w("NgelxIncoming", "ring_blocked settings: notifications=" +
                    (Build.VERSION.SDK_INT < 24 || manager.areNotificationsEnabled()).toString() +
                    " channel=" + (channel == null || (channel.importance > 0 && channel.sound != null)).toString() +
                    " ringer=" + (audio.ringerMode == AudioManager.RINGER_MODE_NORMAL).toString() +
                    " volume=" + (audio.getStreamVolume(AudioManager.STREAM_RING) > 0).toString() +
                    " dnd=" + (Build.VERSION.SDK_INT < 23 || manager.currentInterruptionFilter == NotificationManager.INTERRUPTION_FILTER_ALL).toString())
                if(allowed) try {
                    val sound = RingtoneManager.getRingtone(application, ringtone)""",'audible gating trace')
    s=one(s,'                    sound.play()\n                } catch(_: Exception) {}',
      '''                    sound.play()
                    Log.i("NgelxIncoming", "ringer_started")
                } catch(e: Exception) {
                    Log.w("NgelxIncoming", "ringer_start_failed: " + e.javaClass.simpleName)
                }''','start diagnostics')
    for marker in ('ringing.remove(room)','manager.notify(room.hashCode(), notification)',
                   'sound.play()','AudioManager.RINGER_MODE_NORMAL',
                   'Notification.FLAG_INSISTENT','manager.currentInterruptionFilter'):
        if marker not in s:raise RuntimeError('ringer safety guard missing '+marker)
    return s
if __name__=='__main__':
    before=SERVICE.read_text(encoding='utf-8')
    after=transform(before)
    if before!=after:SERVICE.write_text(after,encoding='utf-8')
    print('Build469: ringtone reception/gating diagnostics without loosening user notification settings')
