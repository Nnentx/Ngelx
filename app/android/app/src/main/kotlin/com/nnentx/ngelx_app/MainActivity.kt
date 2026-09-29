package com.nnentx.ngelx_app

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.provider.OpenableColumns
import android.os.Handler
import android.os.Looper
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MainActivity : FlutterActivity() {
    private val mediaChannel = "com.nnentx.ngelx_app/media"
    private val executor = Executors.newCachedThreadPool()
    private val mainHandler = Handler(Looper.getMainLooper())
    private val nativePickerRequestCode = 8701
    private val nativeMultiPickerRequestCode = 8702
    private var pendingPickerResult: MethodChannel.Result? = null

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, mediaChannel)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "get" -> {
                        val target = call.argument<String>("url")
                        val token = call.argument<String>("token")
                        if (target.isNullOrBlank() || token.isNullOrBlank()) {
                            result.error("INVALID_REQUEST", "GET isteği verisi eksik.", null)
                            return@setMethodCallHandler
                        }
                        executeGet(target, token, result)
                    }

                    "upload" -> {
                        val target = call.argument<String>("url")
                        val token = call.argument<String>("token")
                        val contentType = call.argument<String>("contentType") ?: "application/octet-stream"
                        val legacyPath = call.argument<String>("legacyPath") ?: ""
                        val bytes = call.argument<ByteArray>("bytes")
                        if (target.isNullOrBlank() || token.isNullOrBlank() || bytes == null || bytes.isEmpty()) {
                            result.error("INVALID_UPLOAD", "Yükleme verisi eksik.", null)
                            return@setMethodCallHandler
                        }
                        executeBodyRequest(
                            target = target,
                            method = "POST",
                            contentType = contentType,
                            bytes = bytes,
                            token = token,
                            legacyPath = legacyPath,
                            client = "android-native-httpurlconnection-fixed",
                            result = result,
                        )
                    }

                    "putBytes" -> {
                        val target = call.argument<String>("url")
                        val contentType = call.argument<String>("contentType") ?: "application/octet-stream"
                        val bytes = call.argument<ByteArray>("bytes")
                        if (target.isNullOrBlank() || bytes == null || bytes.isEmpty()) {
                            result.error("INVALID_PUT", "R2 PUT verisi eksik.", null)
                            return@setMethodCallHandler
                        }
                        executeBodyRequest(
                            target = target,
                            method = "PUT",
                            contentType = contentType,
                            bytes = bytes,
                            token = null,
                            legacyPath = "",
                            client = "android-native-r2-put-bytes",
                            result = result,
                        )
                    }

                    "putFile" -> {
                        val target = call.argument<String>("url")
                        val contentType = call.argument<String>("contentType") ?: "application/octet-stream"
                        val path = call.argument<String>("path")
                        if (target.isNullOrBlank() || path.isNullOrBlank()) {
                            result.error("INVALID_PUT_FILE", "R2 dosya PUT verisi eksik.", null)
                            return@setMethodCallHandler
                        }
                        executeFilePut(target, contentType, path, result)
                    }

                    "pickDocument" -> {
                        launchDocumentPicker(
                            call.argument<List<String>>("mimeTypes") ?: listOf("*/*"),
                            allowMultiple = false,
                            result = result,
                        )
                    }

                    "pickDocuments" -> {
                        launchDocumentPicker(
                            call.argument<List<String>>("mimeTypes") ?: listOf("*/*"),
                            allowMultiple = true,
                            result = result,
                        )
                    }

                    else -> result.notImplemented()
                }
            }
    }

    private fun launchDocumentPicker(
        mimeTypes: List<String>,
        allowMultiple: Boolean,
        result: MethodChannel.Result,
    ) {
        if (pendingPickerResult != null) {
            result.error("PICKER_BUSY", "Dosya seçici zaten açık.", null)
            return
        }
        try {
            val cleanTypes = mimeTypes.filter { it.isNotBlank() }.ifEmpty { listOf("*/*") }
            val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE)
                type = if (cleanTypes.size == 1) cleanTypes.first() else "*/*"
                if (cleanTypes.size > 1) {
                    putExtra(Intent.EXTRA_MIME_TYPES, cleanTypes.toTypedArray())
                }
                putExtra(Intent.EXTRA_ALLOW_MULTIPLE, allowMultiple)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            pendingPickerResult = result
            startActivityForResult(
                Intent.createChooser(intent, if (allowMultiple) "Dosyaları seç" else "Dosya seç"),
                if (allowMultiple) nativeMultiPickerRequestCode else nativePickerRequestCode,
            )
        } catch (e: Exception) {
            pendingPickerResult = null
            result.error("PICKER_LAUNCH", e.javaClass.simpleName + ": " + (e.message ?: "seçici açılamadı"), null)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == nativePickerRequestCode || requestCode == nativeMultiPickerRequestCode) {
            val callback = pendingPickerResult
            pendingPickerResult = null
            if (callback == null) return
            if (resultCode != Activity.RESULT_OK || data == null) {
                callback.success(if (requestCode == nativeMultiPickerRequestCode) emptyList<Map<String, String>>() else null)
                return
            }
            try {
                if (requestCode == nativeMultiPickerRequestCode) {
                    val uris = mutableListOf<Uri>()
                    data.clipData?.let { clip ->
                        for (i in 0 until clip.itemCount) uris.add(clip.getItemAt(i).uri)
                    }
                    data.data?.let { if (!uris.contains(it)) uris.add(it) }
                    callback.success(uris.mapNotNull { copyPickedUriToCache(it) })
                } else {
                    val uri = data.data
                    callback.success(if (uri == null) null else copyPickedUriToCache(uri))
                }
            } catch (e: Exception) {
                callback.error("PICKER_COPY", e.javaClass.simpleName + ": " + (e.message ?: "dosya okunamadı"), null)
            }
            return
        }
        super.onActivityResult(requestCode, resultCode, data)
    }

    private fun copyPickedUriToCache(uri: Uri): Map<String, String>? {
        val mime = contentResolver.getType(uri) ?: "application/octet-stream"
        var displayName = ""
        contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { cursor ->
            val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
            if (index >= 0 && cursor.moveToFirst()) displayName = cursor.getString(index) ?: ""
        }
        if (displayName.isBlank()) {
            val ext = when {
                mime.startsWith("image/") -> mime.substringAfter("image/").replace("jpeg", "jpg")
                mime.startsWith("video/") -> mime.substringAfter("video/")
                mime.startsWith("audio/") -> mime.substringAfter("audio/").replace("mpeg", "mp3").replace("mp4", "m4a")
                else -> "bin"
            }
            displayName = "ngelx_${System.currentTimeMillis()}.$ext"
        }
        val safeName = displayName.replace(Regex("[^A-Za-z0-9._-]"), "_")
        val pickerDir = File(cacheDir, "native_picker").apply { mkdirs() }
        val outFile = File(pickerDir, "${System.currentTimeMillis()}_$safeName")
        contentResolver.openInputStream(uri)?.use { input ->
            outFile.outputStream().buffered().use { output ->
                input.copyTo(output, 64 * 1024)
            }
        } ?: return null
        if (!outFile.exists() || outFile.length() <= 0L) return null
        return mapOf(
            "path" to outFile.absolutePath,
            "name" to displayName,
            "mimeType" to mime,
        )
    }

    private fun executeGet(target: String, token: String, result: MethodChannel.Result) {
        executor.execute {
            var connection: HttpURLConnection? = null
            try {
                connection = URL(target).openConnection() as HttpURLConnection
                connection.requestMethod = "GET"
                connection.connectTimeout = 15000
                connection.readTimeout = 30000
                connection.doInput = true
                connection.useCaches = false
                connection.instanceFollowRedirects = true
                connection.setRequestProperty("Authorization", "Bearer $token")
                connection.setRequestProperty("Accept", "application/json")
                connection.setRequestProperty("Connection", "close")
                connection.setRequestProperty("Cache-Control", "no-cache")
                connection.setRequestProperty("X-NgelX-Client", "android-native-presign-fallback")
                connection.connect()
                respond(connection, result)
            } catch (e: Exception) {
                fail("NATIVE_GET", e, target, result)
            } finally {
                connection?.disconnect()
            }
        }
    }

    private fun executeBodyRequest(
        target: String,
        method: String,
        contentType: String,
        bytes: ByteArray,
        token: String?,
        legacyPath: String,
        client: String,
        result: MethodChannel.Result,
    ) {
        executor.execute {
            var connection: HttpURLConnection? = null
            try {
                connection = URL(target).openConnection() as HttpURLConnection
                connection.requestMethod = method
                connection.connectTimeout = 20000
                connection.readTimeout = 120000
                connection.doInput = true
                connection.doOutput = true
                connection.useCaches = false
                connection.instanceFollowRedirects = true
                if (!token.isNullOrBlank()) {
                    connection.setRequestProperty("Authorization", "Bearer $token")
                }
                connection.setRequestProperty("Content-Type", contentType)
                connection.setRequestProperty("Accept", "application/json, text/plain, */*")
                connection.setRequestProperty("Connection", "close")
                connection.setRequestProperty("X-NgelX-Client", client)
                if (legacyPath.isNotBlank()) {
                    connection.setRequestProperty("X-NgelX-Filename", legacyPath)
                }
                connection.setFixedLengthStreamingMode(bytes.size)
                connection.connect()

                connection.outputStream.use { output ->
                    output.write(bytes)
                    output.flush()
                }

                respond(connection, result)
            } catch (e: Exception) {
                fail(if (method == "PUT") "NATIVE_R2_PUT" else "NATIVE_UPLOAD", e, target, result)
            } finally {
                connection?.disconnect()
            }
        }
    }

    private fun executeFilePut(
        target: String,
        contentType: String,
        path: String,
        result: MethodChannel.Result,
    ) {
        executor.execute {
            var connection: HttpURLConnection? = null
            try {
                val file = File(path)
                if (!file.exists() || !file.isFile || file.length() <= 0L) {
                    mainHandler.post {
                        result.error("INVALID_PUT_FILE", "Yüklenecek dosya bulunamadı veya boş.", null)
                    }
                    return@execute
                }

                connection = URL(target).openConnection() as HttpURLConnection
                connection.requestMethod = "PUT"
                connection.connectTimeout = 20000
                connection.readTimeout = 120000
                connection.doInput = true
                connection.doOutput = true
                connection.useCaches = false
                connection.instanceFollowRedirects = true
                connection.setRequestProperty("Content-Type", contentType)
                connection.setRequestProperty("Accept", "application/json, text/plain, */*")
                connection.setRequestProperty("Connection", "close")
                connection.setRequestProperty("X-NgelX-Client", "android-native-r2-put-file")
                connection.setFixedLengthStreamingMode(file.length())
                connection.connect()

                file.inputStream().buffered(64 * 1024).use { input ->
                    connection.outputStream.buffered(64 * 1024).use { output ->
                        input.copyTo(output, 64 * 1024)
                        output.flush()
                    }
                }

                respond(connection, result)
            } catch (e: Exception) {
                fail("NATIVE_R2_PUT_FILE", e, target, result)
            } finally {
                connection?.disconnect()
            }
        }
    }

    private fun respond(connection: HttpURLConnection, result: MethodChannel.Result) {
        val status = connection.responseCode
        val stream = if (status in 200..299) connection.inputStream else connection.errorStream
        val body = if (stream != null) {
            BufferedReader(InputStreamReader(stream, Charsets.UTF_8)).use { it.readText() }
        } else {
            ""
        }
        mainHandler.post {
            result.success(mapOf("status" to status, "body" to body))
        }
    }

    private fun fail(code: String, error: Exception, target: String, result: MethodChannel.Result) {
        mainHandler.post {
            result.error(
                code,
                error.javaClass.simpleName + ": " + (error.message ?: "bağlantı hatası") + " [" + target + "]",
                null,
            )
        }
    }

    override fun onDestroy() {
        executor.shutdownNow()
        super.onDestroy()
    }
}
