package com.nnentx.ngelx_app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import android.os.PowerManager

class CallAudioService : Service() {
    companion object {
        const val SHOW_FLOATING_509 = "com.nnentx.ngelx_app.SHOW_FLOATING_509"
        const val HIDE_FLOATING_509 = "com.nnentx.ngelx_app.HIDE_FLOATING_509"
        @Volatile var active = false
            private set
    }
    private var floating509: Ngelx509FloatingCallWindow? = null
    private var wakeLock: PowerManager.WakeLock? = null
    override fun onCreate() {
        super.onCreate()
        active = true
        val manager = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= 26) manager.createNotificationChannel(
            NotificationChannel("ngelx_call", "Devam eden görüşme", NotificationManager.IMPORTANCE_LOW))
        val intent = Intent(this, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        val pending = PendingIntent.getActivity(this, 446, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        val builder = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, "ngelx_call") else Notification.Builder(this)
        val notification = builder.setContentTitle("NgelX görüşmesi devam ediyor")
            .setContentText("Görüşmeye dönmek için dokun")
            .setSmallIcon(android.R.drawable.sym_call_incoming).setContentIntent(pending).setOngoing(true).build()
        if (Build.VERSION.SDK_INT >= 30) startForeground(446, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE)
        else startForeground(446, notification)
        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "NgelX:CallAudio").apply { acquire(12 * 60 * 60 * 1000L) }
    }
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            SHOW_FLOATING_509 -> {
                val name = intent.getStringExtra("callName") ?: "Görüşme sürüyor"
                if (active) {
                    if (floating509 == null) floating509 = Ngelx509FloatingCallWindow(this)
                    floating509?.show(name)
                }
            }
            HIDE_FLOATING_509 -> { floating509?.remove(); floating509 = null }
        }
        return START_NOT_STICKY
    }
    override fun onTaskRemoved(rootIntent: Intent?) { stopSelf(); super.onTaskRemoved(rootIntent) }
    override fun onBind(intent: Intent?): IBinder? = null
    override fun onDestroy() {
        floating509?.remove()
        floating509 = null
        active = false
        wakeLock?.let { if (it.isHeld) it.release() }; wakeLock = null
        stopForeground(STOP_FOREGROUND_REMOVE)
        super.onDestroy()
    }
}
