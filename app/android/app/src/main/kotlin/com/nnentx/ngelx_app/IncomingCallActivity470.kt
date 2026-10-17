package com.nnentx.ngelx_app

import android.app.Activity
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RadialGradient
import android.graphics.Shader
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView

/**
 * Build471: two native incoming call designs, inspired by the approved purple
 * group mockup. Keep the Build470 ringing lifecycle and original answer/reject.
 * This Activity performs NO network request and creates NO LiveKit connection.
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

    private fun dp(value: Int) = (value * resources.displayMetrics.density + .5f).toInt()
    private fun paint(a: Int, r: Int, g: Int, b: Int) = Color.argb(a, r, g, b)

    private fun gradient(vararg colors: Int, round: Int = 0): GradientDrawable {
        return GradientDrawable(GradientDrawable.Orientation.TL_BR, colors).apply {
            cornerRadius = dp(round).toFloat()
        }
    }

    /** Safe native canvas backdrop: no animation, bitmap or remote URL on lock screen. */
    private inner class CallBackdrop471(private val group: Boolean) : View(this@IncomingCallActivity470) {
        private val p = Paint(Paint.ANTI_ALIAS_FLAG)
        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val w = width.toFloat()
            val h = height.toFloat()
            if (w <= 0f || h <= 0f) return
            p.shader = android.graphics.LinearGradient(
                0f, 0f, w, h,
                if (group) intArrayOf(Color.rgb(39, 28, 87), Color.rgb(23, 14, 59), Color.rgb(18, 14, 49))
                else intArrayOf(Color.rgb(25, 43, 85), Color.rgb(24, 25, 67), Color.rgb(11, 22, 43)),
                null, Shader.TileMode.CLAMP
            )
            canvas.drawRect(0f, 0f, w, h, p)
            p.shader = RadialGradient(
                w * .10f, h * .05f, w * .85f,
                intArrayOf(if (group) paint(105, 110, 54, 210) else paint(92, 30, 115, 193),
                    Color.TRANSPARENT), null, Shader.TileMode.CLAMP
            )
            canvas.drawCircle(w * .10f, h * .05f, w * .85f, p)
            p.shader = RadialGradient(
                w * .90f, h * .82f, w * .7f,
                intArrayOf(if (group) paint(60, 109, 50, 193) else paint(54, 10, 151, 173),
                    Color.TRANSPARENT), null, Shader.TileMode.CLAMP
            )
            canvas.drawCircle(w * .90f, h * .82f, w * .7f, p)
            p.shader = null
            // Quiet waveform illustration only for groups; not a false speaker meter.
            if (group) {
                val center = h * .38f
                val bar = dp(4).toFloat()
                val gap = dp(10).toFloat()
                p.color = paint(105, 173, 102, 250)
                for (i in 0..7) {
                    val t = i / 7f
                    val magnitude = dp((8 + 36 * (1f - kotlin.math.abs(t - .5f) * 2)).toInt()).toFloat()
                    val x = dp(7).toFloat() + i * gap
                    val mirrored = w - x
                    canvas.drawRoundRect(x, center - magnitude, x + bar, center + magnitude, bar, bar, p)
                    canvas.drawRoundRect(mirrored - bar, center - magnitude, mirrored, center + magnitude, bar, bar, p)
                }
            }
        }
    }

    private fun label(value: String, size: Float, color: Int, bold: Boolean = false): TextView {
        return TextView(this).apply {
            text = value
            textSize = size
            gravity = Gravity.CENTER
            setTextColor(color)
            includeFontPadding = false
            if (bold) setTypeface(typeface, android.graphics.Typeface.BOLD)
            maxLines = 2
            ellipsize = android.text.TextUtils.TruncateAt.END
        }
    }

    private fun avatar(initial: String, group: Boolean): FrameLayout {
        val frame = FrameLayout(this).apply {
            background = gradient(
                if (group) Color.rgb(174, 101, 254) else Color.rgb(84, 192, 227),
                if (group) Color.rgb(72, 61, 180) else Color.rgb(43, 75, 150),
                round = 110
            ).apply { setStroke(dp(2), if (group) Color.rgb(198, 146, 255) else Color.rgb(132, 225, 241)) }
            elevation = dp(14).toFloat()
        }
        frame.addView(label(initial, if (group) 61f else 57f, Color.WHITE, true),
            FrameLayout.LayoutParams(-1, -1))
        return frame
    }

    private fun actionButton(text: String, reject: Boolean, onClick: () -> Unit): LinearLayout {
        val fill = if (reject) intArrayOf(Color.rgb(222, 48, 91), Color.rgb(168, 32, 81))
            else intArrayOf(Color.rgb(13, 182, 113), Color.rgb(3, 130, 100))
        val color = if (reject) Color.rgb(255, 105, 133) else Color.rgb(80, 225, 162)
        return LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            background = gradient(*fill, round = 38).apply { setStroke(dp(1), color) }
            elevation = dp(8).toFloat()
            isClickable = true
            isFocusable = true
            contentDescription = text
            setOnClickListener { onClick() }
            val icon = ImageView(this@IncomingCallActivity470).apply {
                setImageResource(android.R.drawable.sym_action_call)
                setColorFilter(Color.WHITE)
                if (reject) rotation = 135f
            }
            addView(icon, LinearLayout.LayoutParams(dp(22), dp(22)).apply { rightMargin = dp(8) })
            addView(label(text, 15f, Color.WHITE, true),
                LinearLayout.LayoutParams(-2, -2))
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= 27) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON)
        }
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        room = intent.getStringExtra("callRoom448").orEmpty()
        chat = intent.getStringExtra("callChat448").orEmpty()
        if (room.isBlank() || chat.isBlank() || !IncomingCallService.isStillRinging470(room)) {
            finish()
            return
        }

        val group = intent.getBooleanExtra("callGroup471", false)
        val title = intent.getStringExtra("callTitle470").orEmpty()
            .ifBlank { "NgelX araması" }.take(100)
        val video = intent.getBooleanExtra("callVideo470", false)
        val accent = if (group) Color.rgb(194, 141, 254) else Color.rgb(132, 225, 241)
        val faded = if (group) Color.rgb(210, 198, 232) else Color.rgb(194, 222, 236)
        val barColor = if (group) Color.rgb(24, 16, 51) else Color.rgb(14, 27, 51)
        window.statusBarColor = barColor
        window.navigationBarColor = barColor

        val root = FrameLayout(this)
        root.addView(CallBackdrop471(group), FrameLayout.LayoutParams(-1, -1))
        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(24), dp(30), dp(24), dp(30))
        }
        root.addView(content, FrameLayout.LayoutParams(-1, -1))

        val tag = if (group) {
            if (video) "Grup görüntülü araması" else "Grup sesli araması"
        } else {
            if (video) "Özel görüntülü arama" else "Özel sesli arama"
        }
        content.addView(label(tag, 15f, accent),
            LinearLayout.LayoutParams(-1, dp(36)))

        val headline = if (video) "Gelen görüntülü arama" else "Gelen sesli arama"
        content.addView(label(headline, 24f, Color.WHITE, false),
            LinearLayout.LayoutParams(-1, dp(55)))

        content.addView(View(this), LinearLayout.LayoutParams(1, 0, 0.7f))
        val size = if (group) 154 else 142
        content.addView(avatar(title.trim().firstOrNull()?.uppercaseChar()?.toString() ?: "N", group),
            LinearLayout.LayoutParams(dp(size), dp(size)))
        content.addView(label(title, if (group) 27f else 29f, Color.WHITE, true),
            LinearLayout.LayoutParams(-1, dp(83)).apply { topMargin = dp(16) })
        content.addView(label(
            if (group) "NgelX üzerinden arıyor..." else "Seni NgelX üzerinden arıyor...",
            16f, faded
        ), LinearLayout.LayoutParams(-1, dp(40)))

        content.addView(View(this), LinearLayout.LayoutParams(1, 0, 1.1f))
        val buttons = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        // Compact 52dp actions with visible separation, never crowding navigation.
        val buttonW = minOf(dp(126), (resources.displayMetrics.widthPixels - dp(100)) / 2)
        buttons.addView(actionButton("Reddet", true) { respond("reject") },
            LinearLayout.LayoutParams(buttonW, dp(52)))
        buttons.addView(View(this), LinearLayout.LayoutParams(0, 1, 1f))
        buttons.addView(actionButton("Cevapla", false) { respond("answer") },
            LinearLayout.LayoutParams(buttonW, dp(52)))
        content.addView(buttons, LinearLayout.LayoutParams(-1, dp(72)))
        content.addView(View(this), LinearLayout.LayoutParams(1, dp(14)))
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
