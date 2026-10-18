package com.nnentx.ngelx_app

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.LinearLayout
import android.widget.TextView
import io.flutter.plugin.common.MethodChannel
import kotlin.math.abs
import kotlin.math.max

/** Build509 QA — native system-wide call window. User approval is mandatory.
 * No video media surface or automatic camera capture is implemented here.
 */
object Ngelx509FlutterEvents {
    var methodChannel: MethodChannel? = null
    fun send(action: String) {
        Handler(Looper.getMainLooper()).post {
            methodChannel?.invokeMethod("floatingCallAction509", mapOf("action" to action))
        }
    }
}

class Ngelx509FloatingCallWindow(private val owner: Context) {
    private enum class Mode { COMPACT, EXPANDED, COLLAPSED }
    private val manager = owner.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val handler = Handler(Looper.getMainLooper())
    private var root: LinearLayout? = null
    private var layout: WindowManager.LayoutParams? = null
    private var mode = Mode.COMPACT
    private var title = "Görüşme sürüyor"
    private var x = 24
    private var y = 220
    private var epoch = 0
    private val density = owner.resources.displayMetrics.density
    private fun dp(n: Int) = (n * density).toInt()

    fun show(name: String): Boolean {
        if (Build.VERSION.SDK_INT < 26 || !Settings.canDrawOverlays(owner)) return false
        title = name.trim().take(64).ifBlank { "NgelX görüşmesi" }
        mode = Mode.COMPACT
        return refresh()
    }
    fun remove() {
        epoch++
        val old = root
        root = null
        layout = null
        if (old != null) try { manager.removeView(old) } catch (_: Exception) {}
    }
    private fun surface() = GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,
        intArrayOf(Color.rgb(96,47,78),Color.rgb(233,167,71))).apply {
            cornerRadius = dp(20).toFloat()
        }
    private fun label(message: String, size: Float = 13f) = TextView(owner).apply {
        text = message
        setTextColor(Color.WHITE)
        textSize = size
        gravity = Gravity.CENTER
        maxLines = 2
        setPadding(dp(4),dp(4),dp(4),dp(4))
    }
    private fun action(name: String, callback: () -> Unit) = label(name).apply {
        contentDescription = name
        isClickable = true
        setOnClickListener { callback() }
    }
    private fun view(): LinearLayout {
        val panel = LinearLayout(owner).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            background = surface()
            setPadding(dp(7),dp(7),dp(7),dp(7))
            elevation = dp(10).toFloat()
        }
        if (mode == Mode.COLLAPSED) {
            panel.addView(action("☎") { mode=Mode.COMPACT; refresh() })
            return panel
        }
        if (mode == Mode.EXPANDED) {
            val top = LinearLayout(owner)
            top.addView(action("⚙") { Ngelx509FlutterEvents.send("settings") },
                LinearLayout.LayoutParams(0,dp(35),1f))
            top.addView(action("×") { mode=Mode.COMPACT; refresh() },
                LinearLayout.LayoutParams(0,dp(35),1f))
            panel.addView(top)
        }
        panel.addView(label(title,12f),LinearLayout.LayoutParams(-1,dp(48)))
        panel.addView(label("●",38f),LinearLayout.LayoutParams(-1,dp(56)))
        panel.addView(label("Sen · Görüşme sürüyor",11f),LinearLayout.LayoutParams(-1,dp(40)))
        if (mode == Mode.EXPANDED) {
            panel.addView(action("⛶  Tam ekran") {
                try {
                    owner.startActivity(Intent(owner, MainActivity::class.java).apply {
                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP or
                            Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
                    })
                } catch (_: Exception) {}
                handler.postDelayed({ Ngelx509FlutterEvents.send("fullscreen") }, 350)
            },
                LinearLayout.LayoutParams(-1,dp(35)))
            val row = LinearLayout(owner)
            row.addView(action("Mik") { Ngelx509FlutterEvents.send("microphone") },
                LinearLayout.LayoutParams(0,dp(40),1f))
            row.addView(action("Ses") { Ngelx509FlutterEvents.send("speaker") },
                LinearLayout.LayoutParams(0,dp(40),1f))
            row.addView(action("Bitir") { Ngelx509FlutterEvents.send("end") },
                LinearLayout.LayoutParams(0,dp(40),1f))
            panel.addView(row)
        } else panel.setOnClickListener { mode=Mode.EXPANDED; refresh(); autoCollapse() }
        return panel
    }
    private fun autoCollapse() {
        val expected=++epoch
        handler.postDelayed({
            if(epoch==expected&&mode==Mode.EXPANDED&&root!=null){
                mode=Mode.COMPACT
                refresh()
            }
        },7000)
    }
    private fun drag(panel: View) {
        var startX=0f
        var startY=0f
        var previousX=0
        var previousY=0
        var moved=false
        panel.setOnTouchListener { v,event ->
            when(event.actionMasked){
                MotionEvent.ACTION_DOWN -> {
                    startX=event.rawX
                    startY=event.rawY
                    previousX=x
                    previousY=y
                    moved=false
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    val dx=event.rawX-startX
                    val dy=event.rawY-startY
                    if(abs(dx)>dp(10)||abs(dy)>dp(10))moved=true
                    if(moved){
                        val display=owner.resources.displayMetrics
                        x=(previousX+dx).toInt().coerceIn(0,max(0,display.widthPixels-(layout?.width?:dp(164))))
                        y=(previousY+dy).toInt().coerceIn(dp(28),
                            max(dp(28),display.heightPixels-(layout?.height?:dp(212))-dp(44)))
                        layout?.let { it.x=x;it.y=y;try{manager.updateViewLayout(root,it)}catch(_:Exception){}}
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if(moved&&event.rawY-startY>dp(96)){mode=Mode.COLLAPSED;refresh()}
                    else if(!moved)v.performClick()
                    true
                }
                MotionEvent.ACTION_OUTSIDE -> {
                    if(mode==Mode.EXPANDED){mode=Mode.COMPACT;refresh()}
                    false
                }
                else -> false
            }
        }
    }
    private fun refresh(): Boolean {
        if(Build.VERSION.SDK_INT<26||!Settings.canDrawOverlays(owner)){remove();return false}
        val size=when(mode){
            Mode.COLLAPSED -> Pair(58,58)
            Mode.COMPACT -> Pair(164,212)
            Mode.EXPANDED -> Pair(218,295)
        }
        root?.let {try{manager.removeView(it)}catch(_:Exception){}}
        val panel=view()
        root=panel
        val p=WindowManager.LayoutParams(dp(size.first),dp(size.second),
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH or
                WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT)
        p.gravity=Gravity.TOP or Gravity.START
        val display=owner.resources.displayMetrics
        x=x.coerceIn(0,max(0,display.widthPixels-p.width))
        y=y.coerceIn(dp(28),max(dp(28),display.heightPixels-p.height-dp(44)))
        p.x=x;p.y=y
        layout=p
        drag(panel)
        return try{manager.addView(panel,p);true}catch(_:Exception){root=null;layout=null;false}
    }
}
