package com.nnentx.ngelx_app

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import java.io.File

/** Fast account/chat-scoped cache. No token, call action or audio ownership. */
object CallPhoto547 {
    private const val PREFS="ngelx_call_photo547"
    private fun key(uid: String,chat: String): String = java.security.MessageDigest
        .getInstance("SHA-256").digest("$uid|$chat".toByteArray())
        .joinToString("") { "%02x".format(it) }
    fun remember(context: Context,uid: String,chat: String,path: String) {
        if(uid.isEmpty()||chat.isEmpty()||chat.length>150||path.length>4096)return
        if(com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid!=uid)return
        try {
            val file=File(path).canonicalFile
            val cache=context.cacheDir.canonicalPath+File.separator
            if(!file.path.startsWith(cache)||!file.isFile||file.length()>2097152)return
            val pref=context.getSharedPreferences(PREFS,Context.MODE_PRIVATE)
            val k=key(uid,chat)
            pref.edit().putString(k,file.path).putLong("${k}_at",System.currentTimeMillis()).apply()
        }catch(_:Exception){}
    }
    fun read(context: Context,uid: String,chat: String): Bitmap? {
        if(com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid!=uid)return null
        try {
            val p=context.getSharedPreferences(PREFS,Context.MODE_PRIVATE);val k=key(uid,chat)
            val age=System.currentTimeMillis()-p.getLong("${k}_at",0)
            if(age<0||age>24L*60*60*1000)return null
            val file=File(p.getString(k,"").orEmpty()).canonicalFile
            if(!file.path.startsWith(context.cacheDir.canonicalPath+File.separator)||!file.isFile||file.length()>2097152)return null
            val bounds=BitmapFactory.Options().apply { inJustDecodeBounds=true }
            BitmapFactory.decodeFile(file.path,bounds)
            if(bounds.outWidth<=0||bounds.outHeight<=0)return null
            var sample=1
            while(bounds.outWidth/sample>512||bounds.outHeight/sample>512)sample*=2
            return BitmapFactory.decodeFile(file.path,BitmapFactory.Options().apply { inSampleSize=sample })
        }catch(_:Exception){return null}
    }
    fun store(context: Context,uid: String,chat: String,bytes: ByteArray) {
        if(bytes.size>2097152||com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid!=uid)return
        try {
            val dir=File(context.cacheDir,"call_photos547").apply { mkdirs() }
            // Bound this extra native cache; Flutter-owned files are never deleted.
            dir.listFiles()?.sortedByDescending { it.lastModified() }?.drop(79)?.forEach { it.delete() }
            val file=File(dir,key(uid,chat)+".img")
            file.writeBytes(bytes)
            remember(context,uid,chat,file.path)
        }catch(_:Exception){}
    }
}
