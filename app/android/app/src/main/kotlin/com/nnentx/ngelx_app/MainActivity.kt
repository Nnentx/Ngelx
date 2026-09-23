package com.nnentx.ngelx_app

import android.os.Handler
import android.os.Looper
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MainActivity : FlutterActivity() {
    private val mediaChannel = "com.nnentx.ngelx_app/media"
    private val executor = Executors.newCachedThreadPool()
    private val mainHandler = Handler(Looper.getMainLooper())

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, mediaChannel)
            .setMethodCallHandler { call, result ->
                if (call.method != "upload") {
                    result.notImplemented()
                    return@setMethodCallHandler
                }

                val target = call.argument<String>("url")
                val token = call.argument<String>("token")
                val contentType = call.argument<String>("contentType") ?: "application/octet-stream"
                val legacyPath = call.argument<String>("legacyPath") ?: ""
                val bytes = call.argument<ByteArray>("bytes")

                if (target.isNullOrBlank() || token.isNullOrBlank() || bytes == null || bytes.isEmpty()) {
                    result.error("INVALID_UPLOAD", "Yükleme verisi eksik.", null)
                    return@setMethodCallHandler
                }

                executor.execute {
                    var connection: HttpURLConnection? = null
                    try {
                        connection = URL(target).openConnection() as HttpURLConnection
                        connection.requestMethod = "POST"
                        connection.connectTimeout = 15000
                        connection.readTimeout = 90000
                        connection.doInput = true
                        connection.doOutput = true
                        connection.useCaches = false
                        connection.instanceFollowRedirects = true
                        connection.setRequestProperty("Authorization", "Bearer $token")
                        connection.setRequestProperty("Content-Type", contentType)
                        connection.setRequestProperty("Content-Length", bytes.size.toString())
                        connection.setRequestProperty("X-NgelX-Client", "android-native-httpurlconnection")
                        connection.setRequestProperty("X-NgelX-Filename", legacyPath)

                        connection.outputStream.use { output ->
                            output.write(bytes)
                            output.flush()
                        }

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
                    } catch (e: Exception) {
                        mainHandler.post {
                            result.error(
                                "NATIVE_UPLOAD",
                                e.javaClass.simpleName + ": " + (e.message ?: "bağlantı hatası"),
                                null
                            )
                        }
                    } finally {
                        connection?.disconnect()
                    }
                }
            }
    }

    override fun onDestroy() {
        executor.shutdownNow()
        super.onDestroy()
    }
}
