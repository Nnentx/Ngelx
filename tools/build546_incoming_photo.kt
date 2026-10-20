    // Build546: bounded, account-scoped photo lookup. Ring/answer never waits for it.
    private val photoExecutor546 = java.util.concurrent.Executors.newSingleThreadExecutor()
    private fun field546(value: org.json.JSONObject, key: String): String =
        value.optJSONObject(key)?.optString("stringValue").orEmpty()
    private fun readBounded546(stream: java.io.InputStream, limit: Int): ByteArray {
        val out=java.io.ByteArrayOutputStream()
        val buffer=ByteArray(8192)
        while(true){val n=stream.read(buffer);if(n<0)break
            if(out.size()+n>limit)throw java.io.IOException("Image size limit")
            out.write(buffer,0,n)}
        return out.toByteArray()
    }
    private fun json546(url: String, token: String): org.json.JSONObject {
        val c = java.net.URL(url).openConnection() as java.net.HttpURLConnection
        c.connectTimeout=2500;c.readTimeout=2500;c.instanceFollowRedirects=false
        c.setRequestProperty("Authorization", "Bearer $token")
        try {
            if(c.responseCode!=200)throw java.io.IOException("Photo lookup unavailable")
            val data=c.inputStream.use { readBounded546(it,262144) }
            if(data.size>262144)throw java.io.IOException("Photo lookup too large")
            return org.json.JSONObject(String(data, Charsets.UTF_8)).getJSONObject("fields")
        } finally { c.disconnect() }
    }
    private fun loadPhoto546(frame: FrameLayout, group: Boolean) {
        val user=com.google.firebase.auth.FirebaseAuth.getInstance().currentUser ?: return
        val uid=user.uid
        user.getIdToken(false).addOnSuccessListener { auth ->
            val token=auth.token ?: return@addOnSuccessListener
            if(isFinishing||isDestroyed)return@addOnSuccessListener
            try { photoExecutor546.execute {
                try {
                    val base="https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents/"
                    val data=json546(base+"chats/"+android.net.Uri.encode(chat),token)
                    if(field546(data,"callRoomName")!=room)return@execute
                    val members=data.optJSONObject("members")?.optJSONObject("arrayValue")?.optJSONArray("values")
                    if(members==null || !(0 until members.length()).any { field546(org.json.JSONObject().put("x",members.getJSONObject(it)),"x")==uid })return@execute
                    val url=if(group)field546(data,"groupPhotoUrl") else {
                        val caller=field546(data,"callStartedBy")
                        if(caller.isEmpty()||caller==uid||caller.contains('/'))return@execute
                        field546(json546(base+"users/"+android.net.Uri.encode(caller),token),"photoUrl")
                    }
                    val uri=android.net.Uri.parse(url)
                    val host=uri.host.orEmpty().lowercase()
                    if(uri.scheme!="https"||uri.userInfo!=null||uri.port !in listOf(-1,443)||
                        host !in setOf("media.ngelxsocial.com","media2.ngelxsocial.com","ngelx-media.alihancaglar76.workers.dev","firebasestorage.googleapis.com","storage.googleapis.com"))return@execute
                    val c=java.net.URL(url).openConnection() as java.net.HttpURLConnection
                    c.connectTimeout=2500;c.readTimeout=2500;c.instanceFollowRedirects=false
                    val bytes=try {
                        if(c.responseCode!=200)return@execute
                        if(c.contentLength>2097152)return@execute
                        c.inputStream.use { readBounded546(it,2097152) }
                    }finally{c.disconnect()}
                    if(bytes.size>2097152)return@execute
                    val bounds=android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds=true }
                    android.graphics.BitmapFactory.decodeByteArray(bytes,0,bytes.size,bounds)
                    if(bounds.outWidth<=0||bounds.outHeight<=0)return@execute
                    var sample=1
                    while(bounds.outWidth/sample>512||bounds.outHeight/sample>512)sample*=2
                    val bitmap=android.graphics.BitmapFactory.decodeByteArray(bytes,0,bytes.size,
                        android.graphics.BitmapFactory.Options().apply { inSampleSize=sample }) ?: return@execute
                    runOnUiThread {
                        if(isFinishing||isDestroyed||!IncomingCallService.isStillRinging470(room)||
                            com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid!=uid){bitmap.recycle();return@runOnUiThread}
                        frame.clipToOutline=true
                        frame.addView(ImageView(this).apply {
                            setImageBitmap(bitmap);scaleType=ImageView.ScaleType.CENTER_CROP
                            contentDescription=if(group)"Grup fotoğrafı" else "Arayan kişinin profil fotoğrafı"
                        },FrameLayout.LayoutParams(-1,-1))
                    }
                }catch(_:Exception){ /* Keep the visible fallback; never interrupt a call. */ }
            }}catch(_:java.util.concurrent.RejectedExecutionException){}
        }
    }
