package com.nnentx.ngelx_app

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import java.security.MessageDigest

/** Same token has the same document ID across native and Flutter restarts. */
object PushRegistration585 {
    fun save(token: String, done: (Boolean) -> Unit = {}) {
        val user = FirebaseAuth.getInstance().currentUser
        if (user == null || user.isAnonymous || token.length !in 21..4095) {
            done(false)
            return
        }
        val id = MessageDigest.getInstance("SHA-256").digest(token.toByteArray())
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        if (FirebaseAuth.getInstance().currentUser?.uid != user.uid) {
            done(false)
            return
        }
        FirebaseFirestore.getInstance().collection("_call_devices").document(user.uid)
            .collection("tokens").document(id)
            .set(mapOf("token" to token, "uid" to user.uid, "updatedAt" to FieldValue.serverTimestamp()))
            .addOnSuccessListener { done(true) }
            .addOnFailureListener { done(false) }
    }
}
