package com.nnentx.ngelx_app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Person
import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.media.RingtoneManager
import android.os.Build
import android.os.Handler
import android.os.Looper
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class IncomingCallService : FirebaseMessagingService() {
    override fun onMessageReceived(message: RemoteMessage) {
        val d = message.data
        if (d["recipientUid"] != FirebaseAuth.getInstance().currentUser?.uid) return
        val room = d["roomName"] ?: return
        if (d["kind"] == "call_end") { cancel(this, room); return }
        val expires = d["expiresAt"]?.toLongOrNull() ?: return
        if (expires <= System.currentTimeMillis()) return
        val chat = d["chatId"] ?: return
        if (d["kind"] != "incoming_call") return
        show(this, chat, room, d["title"] ?: "NgelX araması", d["video"] == "true")
    }
    companion object {
        const val CHANNEL = "ngelx_incoming_calls448"
        private val timer = Handler(Looper.getMainLooper())
        private val alerts = java.util.concurrent.ConcurrentHashMap<String, Runnable>()
        fun cancel(context: Context, room: String) {
            alerts.remove(room)?.let { timer.removeCallbacks(it) }
            context.getSystemService(NotificationManager::class.java).cancel(room.hashCode())
        }
        fun show(context: Context, chat: String, room: String, title: String, video: Boolean) {
            val manager = context.getSystemService(NotificationManager::class.java)
            val ringtone = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            if (Build.VERSION.SDK_INT >= 26) {
            val channel = NotificationChannel(CHANNEL, "Gelen aramalar", NotificationManager.IMPORTANCE_HIGH)
            channel.enableVibration(true)
            channel.setSound(ringtone, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE).build())
            manager.createNotificationChannel(channel)
            }
            fun action(value: String): PendingIntent {
                val intent = Intent(context, MainActivity::class.java).apply {
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
                    putExtra("callChat448", chat); putExtra("callRoom448", room); putExtra("callAction448", value)
                }
                return PendingIntent.getActivity(context, (room+value).hashCode(), intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            }
            val answer = action("answer"); val reject = action("reject")
            val builder = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(context, CHANNEL) else Notification.Builder(context)
            builder
                .setSmallIcon(android.R.drawable.sym_call_incoming).setContentTitle(title)
                .setContentText(if(video) "Gelen görüntülü arama" else "Gelen sesli arama")
                .setCategory(Notification.CATEGORY_CALL).setOngoing(true).setAutoCancel(false)
                .setContentIntent(action("open")).setOnlyAlertOnce(true)
            if (Build.VERSION.SDK_INT >= 26) builder.setTimeoutAfter(60000)
            if (Build.VERSION.SDK_INT < 26) {
                builder.setPriority(Notification.PRIORITY_MAX)
                    .setSound(ringtone, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE).build())
                    .setVibrate(longArrayOf(0, 500, 500))
            }
            if (Build.VERSION.SDK_INT >= 31) {
                builder.setStyle(Notification.CallStyle.forIncomingCall(Person.Builder().setName(title).setImportant(true).build(), reject, answer))
            } else {
                builder.addAction(Notification.Action.Builder(null,"Reddet",reject).build())
                builder.addAction(Notification.Action.Builder(null,"Yanıtla",answer).build())
            }
            val notification = builder.build()
            notification.flags = notification.flags or Notification.FLAG_INSISTENT
            manager.notify(room.hashCode(), notification)
            val application = context.applicationContext
            val timeout = Runnable { cancel(application, room) }
            alerts.put(room, timeout)?.let { timer.removeCallbacks(it) }
            timer.postDelayed(timeout, 60000)
        }
    }
}
