package com.nnentx.ngelx_app

import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

/**
 * Android's real incoming-call surface, including when Flutter has not started.
 * Launched by an explicitly scoped full-screen notification PendingIntent.
 * Never opens an additional LiveKit session or changes a Firestore permission.
 */
class IncomingCallActivity470 : Activity() {
    private var room = ""
    private var chat = ""
    private val timer = Handler(Looper.getMainLooper())
    private val check = object : Runnable {
        override fun run() {
            if (isFinishing || isDestroyed) return
            if (room.isEmpty() || !IncomingCallService.isStillRinging470(room)) {
                finish()
            } else timer.postDelayed(this, 1000)
        }
    }

    private fun px(dp: Int) = (dp * resources.displayMetrics.density + .5f).toInt()

    private fun background(): GradientDrawable =
        GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(Color.rgb(45, 29, 83), Color.rgb(20, 13, 42))
        )

    private fun actionButton(label: String, color: Int, action: String): Button {
        return Button(this).apply {
            text = label
            textSize = 17f
            setTextColor(Color.WHITE)
            isAllCaps = false
            background = GradientDrawable().apply {
                setColor(color)
                cornerRadius = px(32).toFloat()
            }
            setOnClickListener { respond(action) }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= 27) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                    WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        window.statusBarColor = Color.rgb(31, 20, 55)
        window.navigationBarColor = Color.rgb(31, 20, 55)

        room = intent.getStringExtra("callRoom448").orEmpty()
        chat = intent.getStringExtra("callChat448").orEmpty()
        if (room.isBlank() || chat.isBlank() || !IncomingCallService.isStillRinging470(room)) {
            finish()
            return
        }

        // The text is treated only as a label. No contact/photo/network lookup
        // occurs from the lockscreen activity or its background service.
        val title = intent.getStringExtra("callTitle470").orEmpty()
            .ifBlank { "NgelX araması" }.take(100)
        val video = intent.getBooleanExtra("callVideo470", false)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(px(24), px(65), px(24), px(48))
            background = background()
        }
        val heading = TextView(this).apply {
            text = if (video) "Gelen görüntülü arama" else "Gelen sesli arama"
            textSize = 19f
            setTextColor(Color.rgb(219, 205, 242))
            gravity = Gravity.CENTER
        }
        root.addView(heading, LinearLayout.LayoutParams(-1, px(48)))
        val initial = title.firstOrNull()?.uppercaseChar()?.toString() ?: "N"
        val avatar = TextView(this).apply {
            text = initial
            textSize = 56f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setTypeface(typeface, Typeface.BOLD)
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(Color.rgb(113, 73, 180))
            }
        }
        root.addView(avatar, LinearLayout.LayoutParams(px(140), px(140)).apply {
            topMargin = px(70)
        })
        root.addView(TextView(this).apply {
            text = title
            textSize = 27f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            setTypeface(typeface, Typeface.BOLD)
        }, LinearLayout.LayoutParams(-1, px(100)).apply {
            topMargin = px(18)
        })
        root.addView(TextView(this).apply {
            text = "NgelX üzerinden arıyor..."
            textSize = 16f
            gravity = Gravity.CENTER
            setTextColor(Color.rgb(218, 204, 235))
        }, LinearLayout.LayoutParams(-1, 0, 1f))

        val buttons = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }
        buttons.addView(actionButton("Reddet", Color.rgb(219, 48, 74), "reject"),
            LinearLayout.LayoutParams(0, px(66), 1f).apply { rightMargin = px(12) })
        buttons.addView(actionButton("Cevapla", Color.rgb(21, 178, 110), "answer"),
            LinearLayout.LayoutParams(0, px(66), 1f).apply { leftMargin = px(12) })
        root.addView(buttons, LinearLayout.LayoutParams(-1, px(80)))
        setContentView(root)
    }

    private fun respond(action: String) {
        if (room.isBlank() || chat.isBlank()) return
        val launch = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra("callChat448", chat)
            putExtra("callRoom448", room)
            putExtra("callAction448", action)
        }
        IncomingCallService.cancel(this, room)
        startActivity(launch)
        finish()
    }

    override fun onResume() {
        super.onResume()
        timer.postDelayed(check, 700)
    }
    override fun onPause() {
        timer.removeCallbacks(check)
        super.onPause()
    }
    override fun onDestroy() {
        timer.removeCallbacks(check)
        super.onDestroy()
    }
}
