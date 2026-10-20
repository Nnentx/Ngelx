from pathlib import Path
TAG='// Build546 incoming caller/group photo'
def transform(s):
 if TAG in s:return s
 a='    private fun actionButton('
 assert s.count(a)==1
 s=s.replace(a,Path('tools/build546_incoming_photo.kt').read_text()+'\n'+a,1)
 old='''        content.addView(avatar(title.trim().firstOrNull()?.uppercaseChar()?.toString() ?: "N", group),
            LinearLayout.LayoutParams(dp(size), dp(size)))'''
 assert s.count(old)==1
 s=s.replace(old,'''        val photoFrame546=avatar(title.trim().firstOrNull()?.uppercaseChar()?.toString() ?: "N", group)
        content.addView(photoFrame546,LinearLayout.LayoutParams(dp(size),dp(size)))
        loadPhoto546(photoFrame546,group)''',1)
 s=s.replace('        timer.removeCallbacks(check)\n        super.onDestroy()', '        timer.removeCallbacks(check)\n        photoExecutor546.shutdownNow()\n        super.onDestroy()',1)
 s=s.replace(' * This Activity performs NO network request and creates NO LiveKit connection.', ' * Photo loading is bounded and asynchronous; this creates NO LiveKit connection.')
 return s+'\n'+TAG+'\n'
if __name__=='__main__':
 p=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt')
 p.write_text(transform(p.read_text()))
