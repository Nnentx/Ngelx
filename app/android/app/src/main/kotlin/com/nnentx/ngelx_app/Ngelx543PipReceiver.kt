package com.nnentx.ngelx_app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import io.flutter.plugin.common.MethodChannel

object Ngelx543PipEvents { var channel: MethodChannel? = null }
/** Explicit, unexported Android PiP actions. Dart rechecks the current owner/room. */
class Ngelx543PipReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != "com.nnentx.ngelx_app.PIP543" || !CallAudioService.active) return
        val action=intent.getStringExtra("action543") ?: return
        if(action in setOf("microphone","speaker","end"))Ngelx543PipEvents.channel?.invokeMethod("pipAction543",action)
    }
}
