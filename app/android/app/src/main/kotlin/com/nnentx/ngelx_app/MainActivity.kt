package com.nnentx.ngelx_app

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.database.Cursor
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageDecoder
import android.os.Build
import android.net.Uri
import android.provider.OpenableColumns
import java.io.FileOutputStream
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
import kotlin.math.max

class MainActivity : FlutterActivity() {
    companion object {
        private const val REQUEST_PICK = 3061
    }

    private val mediaChannel = "com.nnentx.ngelx_app/media"
    private var pendingPickerResult: MethodChannel.Result? = null
    private var pickerAllowMultiple = false
    private var pickerRequestedImage = false
    private val executor = Executors.newCachedThreadPool()
    private val mainHandler = Handler(Looper.getMainLooper())

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, mediaChannel)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "pickDocument", "pickDocuments" -> {
                        if (pendingPickerResult != null) {
                            result.error("PICKER_BUSY", "Medya seçici zaten açık.", null)
                            return@setMethodCallHandler
                        }
                        val mimeTypes = call.argument<List<String>>("mimeTypes")
                            ?.filter { it.isNotBlank() }
                            ?.distinct()
                            .orEmpty()
                        pickerAllowMultiple = call.method == "pickDocuments"
                        pickerRequestedImage = mimeTypes.any { it == "image/*" || it.startsWith("image/") }
                        pendingPickerResult = result
                        launchPicker(mimeTypes, pickerAllowMultiple)
                    }

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

                    else -> result.notImplemented()
                }
            }
    }

    private fun launchPicker(mimeTypes: List<String>, multiple: Boolean) {
        val cleanTypes = mimeTypes.ifEmpty { listOf("*/*") }
        val primaryType = if (cleanTypes.size == 1) cleanTypes.first() else "*/*"

        fun build(action: String) = Intent(action).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = primaryType
            putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiple)
            if (cleanTypes.size > 1) {
                putExtra(Intent.EXTRA_MIME_TYPES, cleanTypes.toTypedArray())
            }
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }

        try {
            startActivityForResult(build(Intent.ACTION_GET_CONTENT), REQUEST_PICK)
        } catch (first: ActivityNotFoundException) {
            try {
                startActivityForResult(build(Intent.ACTION_OPEN_DOCUMENT), REQUEST_PICK)
            } catch (second: Exception) {
                finishPickerWithError(
                    "PICKER_LAUNCH",
                    "Android medya seçicisi başlatılamadı: ${second.message ?: first.message}",
                )
            }
        } catch (e: Exception) {
            finishPickerWithError("PICKER_LAUNCH", "Seçici başlatma hatası: ${e.message}")
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_PICK) return
        val result = pendingPickerResult ?: return
        pendingPickerResult = null
        val requestedImage = pickerRequestedImage
        pickerRequestedImage = false

        if (resultCode != Activity.RESULT_OK || data == null) {
            if (pickerAllowMultiple) result.success(emptyList<Map<String, Any?>>())
            else result.success(null)
            return
        }

        try {
            val uris = mutableListOf<Uri>()
            data.clipData?.let { clip ->
                for (i in 0 until clip.itemCount) {
                    val uri = clip.getItemAt(i).uri
                    if (!uris.contains(uri)) uris.add(uri)
                }
            }
            data.data?.let { if (!uris.contains(it)) uris.add(it) }
            val files = uris.map { copyUriToCache(it, requestedImage) }
            if (pickerAllowMultiple) result.success(files) else result.success(files.firstOrNull())
        } catch (e: Exception) {
            result.error("PICKER_COPY", "Seçilen medya okunamadı: ${e.message}", null)
        }
    }

    private fun copyUriToCache(uri: Uri, requestedImage: Boolean): Map<String, Any?> {
        val originalName = displayName(uri).ifBlank { "ngelx_${System.currentTimeMillis()}" }
        val mimeType = contentResolver.getType(uri)?.lowercase()
        val gif = mimeType == "image/gif" || originalName.lowercase().endsWith(".gif")

        // Bazı Android galeri/bulut sağlayıcıları image/* seçimine rağmen MIME
        // bilgisini null veya application/octet-stream döndürüyor. İstek resimse
        // uzantıya/MIME'a güvenmeden yerel codec ile normalize etmeyi dene.
        if ((requestedImage || mimeType?.startsWith("image/") == true) && !gif) {
            val normalized = normalizeImageToJpeg(uri)
            if (normalized != null && normalized.length() > 0L) {
                val baseName = originalName.substringBeforeLast('.', originalName)
                    .replace(Regex("[^A-Za-z0-9._-]"), "_")
                    .ifBlank { "ngelx_${System.currentTimeMillis()}" }
                return mapOf(
                    "path" to normalized.absolutePath,
                    "name" to "$baseName.jpg",
                    "mimeType" to "image/jpeg",
                    "size" to normalized.length(),
                )
            }
        }

        val safeName = originalName.replace(Regex("[^A-Za-z0-9._-]"), "_")
            .ifBlank { "ngelx_${System.currentTimeMillis()}" }
        val pickerDir = File(cacheDir, "ngelx_picker").apply { mkdirs() }
        val target = File(pickerDir, "${System.currentTimeMillis()}_$safeName")
        contentResolver.openInputStream(uri).use { input ->
            requireNotNull(input) { "Dosya akışına erişilemedi." }
            FileOutputStream(target).use { output -> input.copyTo(output) }
        }
        val detected = if (requestedImage) detectImageType(target) else null
        return mapOf(
            "path" to target.absolutePath,
            "name" to if (detected == null) originalName else originalName.substringBeforeLast('.', originalName) + "." + detected.first,
            "mimeType" to (detected?.second ?: mimeType),
            "size" to target.length(),
        )
    }

    private fun detectImageType(file: File): Pair<String, String>? {
        return try {
            val bytes = ByteArray(32)
            val count = file.inputStream().use { it.read(bytes) }
            fun ascii(offset: Int, length: Int): String =
                if (count >= offset + length) String(bytes, offset, length, Charsets.US_ASCII) else ""
            when {
                count >= 3 && bytes[0] == 0xFF.toByte() && bytes[1] == 0xD8.toByte() && bytes[2] == 0xFF.toByte() -> "jpg" to "image/jpeg"
                count >= 8 && bytes.sliceArray(0..7).contentEquals(byteArrayOf(0x89.toByte(), 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A)) -> "png" to "image/png"
                ascii(0, 4) == "GIF8" -> "gif" to "image/gif"
                ascii(0, 4) == "RIFF" && ascii(8, 4) == "WEBP" -> "webp" to "image/webp"
                ascii(4, 4) == "ftyp" && ascii(8, 4).lowercase() in setOf("avif", "avis") -> "avif" to "image/avif"
                ascii(4, 4) == "ftyp" && ascii(8, 4).lowercase() in setOf("heic", "heix", "hevc", "hevx") -> "heic" to "image/heic"
                ascii(4, 4) == "ftyp" && ascii(8, 4).lowercase() in setOf("mif1", "msf1") -> "heif" to "image/heif"
                else -> null
            }
        } catch (_: Throwable) {
            null
        }
    }

    private fun normalizeImageToJpeg(uri: Uri): File? {
        return try {
            val bitmap: Bitmap? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                val source = ImageDecoder.createSource(contentResolver, uri)
                ImageDecoder.decodeBitmap(source) { decoder, info, _ ->
                    decoder.allocator = ImageDecoder.ALLOCATOR_SOFTWARE
                    val width = info.size.width
                    val height = info.size.height
                    val largest = max(width, height)
                    if (largest > 4096) {
                        val ratio = 4096.0 / largest.toDouble()
                        decoder.setTargetSize(
                            max(1, (width * ratio).toInt()),
                            max(1, (height * ratio).toInt()),
                        )
                    }
                }
            } else {
                val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                contentResolver.openInputStream(uri).use { input ->
                    if (input != null) BitmapFactory.decodeStream(input, null, bounds)
                }
                var sample = 1
                while (
                    bounds.outWidth > 0 &&
                    bounds.outHeight > 0 &&
                    max(bounds.outWidth / sample, bounds.outHeight / sample) > 4096
                ) {
                    sample *= 2
                }
                val options = BitmapFactory.Options().apply { inSampleSize = sample }
                contentResolver.openInputStream(uri).use { input ->
                    if (input == null) null else BitmapFactory.decodeStream(input, null, options)
                }
            }

            if (bitmap == null) return null
            val pickerDir = File(cacheDir, "ngelx_picker").apply { mkdirs() }
            val target = File(pickerDir, "normalized_${System.currentTimeMillis()}.jpg")
            val ok = FileOutputStream(target).use { output ->
                bitmap.compress(Bitmap.CompressFormat.JPEG, 92, output)
            }
            bitmap.recycle()
            if (!ok || target.length() <= 0L) {
                target.delete()
                null
            } else {
                target
            }
        } catch (_: Throwable) {
            null
        }
    }

    private fun displayName(uri: Uri): String {
        var cursor: Cursor? = null
        return try {
            cursor = contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
            if (cursor != null && cursor.moveToFirst()) {
                val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (index >= 0) cursor.getString(index) ?: uri.lastPathSegment.orEmpty()
                else uri.lastPathSegment.orEmpty()
            } else {
                uri.lastPathSegment.orEmpty()
            }
        } finally {
            cursor?.close()
        }
    }

    private fun finishPickerWithError(code: String, message: String) {
        pendingPickerResult?.error(code, message, null)
        pendingPickerResult = null
        pickerRequestedImage = false
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
        pendingPickerResult?.error("PICKER_DESTROYED", "Medya seçici kapatıldı.", null)
        pendingPickerResult = null
        executor.shutdownNow()
        super.onDestroy()
    }
}
