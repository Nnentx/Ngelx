package com.nnentx.ngelx_app

import android.app.Activity
import android.content.ClipData
import android.content.Intent
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import androidx.core.content.FileProvider
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.security.MessageDigest
import java.util.concurrent.Executors

/** Only our cache/update APKs are exposed, and only to Android's consent UI. */
class Ngelx564Updater(private val activity: Activity) {
    private val executor = Executors.newSingleThreadExecutor()
    private val main = Handler(Looper.getMainLooper())
    private val directory get() = File(activity.cacheDir, "ngelx_updates").apply { mkdirs() }

    @Suppress("DEPRECATION")
    private fun installed(): PackageInfo = activity.packageManager.getPackageInfo(activity.packageName, (if (Build.VERSION.SDK_INT >= 28) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES))
    @Suppress("DEPRECATION")
    private fun code(info: PackageInfo): Long = if (Build.VERSION.SDK_INT >= 28) info.longVersionCode else info.versionCode.toLong()
    @Suppress("DEPRECATION")
    private fun signatures(info: PackageInfo): Set<String> {
        val signatures = if (Build.VERSION.SDK_INT >= 28) info.signingInfo?.apkContentsSigners else info.signatures
        return signatures.orEmpty().map { signature ->
            MessageDigest.getInstance("SHA-256").digest(signature.toByteArray()).joinToString("") { "%02x".format(it) }
        }.toSet()
    }
    private fun updateFile(path: String): File {
        val file = File(path).canonicalFile
        require(file.parentFile == directory.canonicalFile && file.name.matches(Regex("NgelX-[0-9]+\\.apk"))) { "Geçersiz güncelleme dosyası." }
        return file
    }
    @Suppress("DEPRECATION")
    private fun verify(path: String, build: Long, size: Long, digest: String): File {
        val file = updateFile(path)
        require(file.isFile && file.length() == size && size in 1..209715200L) { "İndirme tamamlanmadı. Tekrar dene." }
        require(digest.matches(Regex("[a-fA-F0-9]{64}"))) { "Güncelleme doğrulaması eksik." }
        val hash = MessageDigest.getInstance("SHA-256")
        file.inputStream().use { input -> val buffer=ByteArray(65536);var read=input.read(buffer);while(read!=-1){hash.update(buffer,0,read);read=input.read(buffer)} }
        require(hash.digest().joinToString("") { "%02x".format(it) }.equals(digest, true)) { "İndirilen dosya doğrulanamadı. Tekrar dene." }
        val apk = activity.packageManager.getPackageArchiveInfo(file.path, (if (Build.VERSION.SDK_INT >= 28) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES))
            ?: error("Güncelleme paketi okunamadı.")
        val current = installed()
        require(apk.packageName == activity.packageName && code(apk) == build && code(apk) > code(current)) { "Bu güncelleme mevcut NgelX sürümü için uygun değil." }
        val expected=signatures(current)
        require(expected.isNotEmpty() && signatures(apk) == expected) { "Güncelleme NgelX imzasıyla eşleşmiyor." }
        return file
    }
    private fun allowed() = Build.VERSION.SDK_INT < 26 || activity.packageManager.canRequestPackageInstalls()

    fun attach(engine: FlutterEngine) {
        MethodChannel(engine.dartExecutor.binaryMessenger, "com.nnentx.ngelx_app/update564").setMethodCallHandler { call, result ->
            when (call.method) {
                "status" -> {
                    val info=installed()
                    result.success(mapOf("build" to code(info),"version" to (info.versionName ?: ""),"canInstall" to allowed()))
                }
                "prepare" -> {
                    val build=(call.argument<Number>("build") ?: 0).toLong()
                    if(build<=code(installed())) { result.error("VERSION", "NgelX zaten güncel.", null);return@setMethodCallHandler }
                    directory.listFiles()?.filter { it.name != "NgelX-$build.apk" }?.forEach { it.delete() }
                    result.success(File(directory,"NgelX-$build.apk").path)
                }
                "verify", "install" -> {
                    val path=call.argument<String>("path") ?: ""
                    val build=(call.argument<Number>("build") ?: 0).toLong()
                    val size=(call.argument<Number>("size") ?: 0).toLong()
                    val digest=call.argument<String>("sha256") ?: ""
                    executor.execute {
                        try {
                            val file=verify(path,build,size,digest)
                            main.post {
                                try {
                                    if(call.method=="verify") { result.success("verified") }
                                    else if(!allowed()) {
                                        activity.startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:${activity.packageName}")))
                                        result.success("permission")
                                    } else {
                                        val uri=FileProvider.getUriForFile(activity,"${activity.packageName}.updates564",file)
                                        activity.startActivity(Intent(Intent.ACTION_VIEW).apply {
                                            setDataAndType(uri,"application/vnd.android.package-archive")
                                            clipData=ClipData.newRawUri("NgelX güncellemesi",uri)
                                            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                        })
                                        result.success("installer")
                                    }
                                } catch(e: Exception) { result.error("INSTALL", "Android yükleme ekranı açılamadı. Tekrar dene.", null) }
                            }
                        } catch(e: Exception) { main.post { result.error("VERIFY", e.message ?: "Güncelleme doğrulanamadı.", null) } }
                    }
                }
                else -> result.notImplemented()
            }
        }
    }
}
