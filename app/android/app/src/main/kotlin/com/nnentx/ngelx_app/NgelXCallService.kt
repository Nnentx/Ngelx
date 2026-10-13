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

class NgelXCallService : Service() {
    companion object {
        const val SESSION = "ngelx_call_session"
        private const val CHANNEL = "ngelx_active_calls"
        private const val NOTIFICATION = 7341
        var requestedSession: String? = null
        var activeSession: String? = null
        var onFailure: ((String) -> Unit)? = null
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val session = intent?.getStringExtra(SESSION)
        if (session.isNullOrBlank() || session != requestedSession) {
            if (activeSession == null) stopSelf()
            return START_NOT_STICKY
        }
        val manager = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= 26) {
            manager.createNotificationChannel(NotificationChannel(CHANNEL, "Aktif aramalar", NotificationManager.IMPORTANCE_LOW))
        }
        val returnIntent = Intent(this, MainActivity::class.java).apply {
            this.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(SESSION, session)
        }
        val pending = PendingIntent.getActivity(this, 7341, returnIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        val builder = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, CHANNEL) else Notification.Builder(this)
        val notification = builder
            .setSmallIcon(android.R.drawable.sym_action_call)
            .setContentTitle("NgelX • Arama devam ediyor")
            .setContentText("Arama ekranına dönmek için dokun")
            .setCategory(Notification.CATEGORY_CALL)
            .setVisibility(Notification.VISIBILITY_PRIVATE)
            .setOngoing(true)
            .setContentIntent(pending)
            .build()
        try {
            if (Build.VERSION.SDK_INT >= 30) startForeground(NOTIFICATION, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE)
            else startForeground(NOTIFICATION, notification)
            activeSession = session
        } catch (_: Exception) {
            if (requestedSession == session) requestedSession = null
            onFailure?.invoke(session)
            stopSelf()
        }
        return START_NOT_STICKY
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        stopSelf()
        super.onTaskRemoved(rootIntent)
    }

    override fun onDestroy() {
        if (requestedSession == activeSession) requestedSession = null
        activeSession = null
        if (Build.VERSION.SDK_INT >= 24) stopForeground(STOP_FOREGROUND_REMOVE) else stopForeground(true)
        super.onDestroy()
    }
}
