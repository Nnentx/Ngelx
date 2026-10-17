#!/usr/bin/env python3
"""Build470: native real incoming call screen via Android full-screen CALL notification.
Keep user sound preferences, account ownership check and existing Flutter call route.
"""
from pathlib import Path
MANIFEST=Path('app/android/app/src/main/AndroidManifest.xml')
SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
MAIN=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
TAG='// Build470: Android platform incoming call UI and owner fallback'
def exactly(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f'Build470 {label}: expected one, found {n}')
    return s.replace(old,new,1)
def patch_manifest(s):
    if 'IncomingCallActivity470' in s:return s
    s=exactly(s,'    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',
      '    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\n'
      '    <uses-permission android:name="android.permission.USE_FULL_SCREEN_INTENT" />',
      'full-screen call permission')
    s=exactly(s,'        <activity\n            android:name=".MainActivity"',
       '        <!-- Build470: native incoming-call surface when Flutter is in background / locked. -->\n'
       '        <activity android:name=".IncomingCallActivity470" android:exported="false"\n'
       '            android:theme="@android:style/Theme.Material.NoActionBar"\n'
       '            android:showWhenLocked="true" android:turnScreenOn="true"\n'
       '            android:excludeFromRecents="true" />\n'
       '        <activity\n            android:name=".MainActivity"', 'activity')
    if 'com.google.firebase.MESSAGING_EVENT' not in s:
      raise RuntimeError('Existing Firebase foreground/background service must stay registered')
    return s
def patch_service(s):
    if TAG in s:return s
    s=exactly(s,'import android.os.Looper\n','import android.os.Looper\nimport android.content.SharedPreferences\n','prefs import')
    owner='''
        // Build470: Android platform incoming call UI and owner fallback.
        // The cache is an exact signed-in account UID, cleared on sign-out by
        // Flutter. It is ONLY used when FirebaseAuth is warming a cold process.
        // No account name, photo, token, chat content or phone number is cached.
        private const val OWNER_PREFS470 = "ngelx_call_owner470"
        fun rememberOwner470(context: Context, uid: String?) {
            context.getSharedPreferences(OWNER_PREFS470, Context.MODE_PRIVATE).edit().apply {
                if (uid.isNullOrEmpty()) {
                    remove("uid")
                    remove("stamp")
                } else {
                    putString("uid", uid)
                    putLong("stamp", System.currentTimeMillis())
                }
                apply()
            }
        }
        private fun currentRecipient470(context: Context): String? {
            val current = FirebaseAuth.getInstance().currentUser?.uid
            if (!current.isNullOrEmpty()) return current
            val prefs = context.getSharedPreferences(OWNER_PREFS470, Context.MODE_PRIVATE)
            val stamp = prefs.getLong("stamp", 0L)
            val age = System.currentTimeMillis() - stamp
            // Limit warm-start fallback; never reuse indefinitely.
            if (age < 0 || age > 72L*60L*60L*1000L) return null
            return prefs.getString("uid", null)
        }
        fun isStillRinging470(room: String): Boolean = room.isNotEmpty() && alerts.containsKey(room)
'''
    s=exactly(s,
        '        private val timer = Handler(Looper.getMainLooper())',
        owner+'        private val timer = Handler(Looper.getMainLooper())','owner + visible ringing')
    # Build469 already introduced explicit diagnostic signedIn checks;
    # keep its logs and permission-denied branches as-is.
    if '        if (d["recipientUid"] != FirebaseAuth.getInstance().currentUser?.uid) return' in s:
        s=exactly(s,
            '        if (d["recipientUid"] != FirebaseAuth.getInstance().currentUser?.uid) return',
            '        if (d["recipientUid"] != currentRecipient470(this)) return',
            'old cold-start account gate')
    else:
        s=exactly(s,
            '        val signedIn = FirebaseAuth.getInstance().currentUser?.uid',
            '        val signedIn = currentRecipient470(this)',
            'Build469 diagnostic cold-start gate')
    needle='''            val answer = action("answer"); val reject = action("reject")'''
    replacement='''            val answer = action("answer"); val reject = action("reject")
            // For a real telephone-like incoming call, Android itself owns
            // the lockscreen/background UI; Flutter is only launched on action.
            val incomingIntent = Intent(context, IncomingCallActivity470::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                putExtra("callChat448", chat)
                putExtra("callRoom448", room)
                putExtra("callTitle470", title.take(100))
                putExtra("callVideo470", video)
            }
            val fullScreenCall = PendingIntent.getActivity(context,
                (room+"native470").hashCode(), incomingIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
'''
    s=exactly(s,needle,replacement,'native screen intent')
    s=exactly(s,'.setContentIntent(action("open")).setOnlyAlertOnce(true)',
        '''.setContentIntent(fullScreenCall).setOnlyAlertOnce(true)
                // High-priority CALL notification remains usable as heads-up
                // when Android 14+ denies full-screen intent permission.
                .setFullScreenIntent(fullScreenCall, true)''',
        'fullscreen + heads-up fallback')
    if 'NotificationManager.IMPORTANCE_HIGH' not in s or 'ringing.remove(room)' not in s:
       raise RuntimeError('Existing ringtone and stop semantics changed')
    return s
def patch_main(s):
    if 'rememberOwner470' in s:return s
    # The existing MethodChannel only handles trusted in-process calls from
    # Flutter's signed-in user listener.
    s=exactly(s,
        '                    "getPushToken" ->',
        '''                    "setCallOwner470" -> {
                        val owner = call.argument<String>("uid")
                        IncomingCallService.rememberOwner470(this, owner)
                        result.success(null)
                    }
                    "getPushToken" ->''','account registration method')
    return s
def write(path,patch):
    before=path.read_text(encoding='utf-8')
    after=patch(before)
    if after!=before:path.write_text(after,encoding='utf-8')
    print('Build470 patched',path)
if __name__=='__main__':
    write(MANIFEST,patch_manifest)
    write(SERVICE,patch_service)
    write(MAIN,patch_main)
