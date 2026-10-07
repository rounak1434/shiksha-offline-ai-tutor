package org.shiksha.tutor

import android.content.Context
import android.util.Log
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import java.io.File

class ShikshaPlatformChannel(
    binaryMessenger: BinaryMessenger,
    private val context: Context? = null
) : MethodChannel.MethodCallHandler {
    companion object {
        private const val TAG = "ShikshaPlatformChannel"
        const val MODEL_FILENAME = "qwen3_base_q4_k_m.gguf"
        // Expected size of production qwen3_base_q4_k_m.gguf in bytes (~461.79 MB)
        const val EXPECTED_MODEL_SIZE = 484220192L
        const val MIN_VALID_SIZE = 480000000L
    }

    private val methodChannel = MethodChannel(binaryMessenger, "org.shiksha.tutor/inference")
    private val eventChannel = EventChannel(binaryMessenger, "org.shiksha.tutor/stream")
    
    private var streamEventSink: EventChannel.EventSink? = null
    private val scope = CoroutineScope(Dispatchers.IO)
    private var activeGenerationJob: Job? = null
    private val modelDeferred = CompletableDeferred<String>()

    init {
        methodChannel.setMethodCallHandler(this)
        eventChannel.setStreamHandler(object : EventChannel.StreamHandler {
            override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
                streamEventSink = events
            }

            override fun onCancel(arguments: Any?) {
                streamEventSink = null
            }
        })

        // Immediately trigger background extraction and model loading
        if (context != null) {
            scope.launch {
                try {
                    val extractedPath = ensureModelExtracted(context)
                    Log.i(TAG, "Model extraction verified at: $extractedPath. Pre-loading native llama.cpp...")
                    val loaded = LlamaBridge.loadModel(extractedPath, 4, 2048)
                    Log.i(TAG, "Native preload result: $loaded")
                    modelDeferred.complete(extractedPath)
                } catch (t: Throwable) {
                    Log.e(TAG, "Failed during background model extraction / preload: ${t.message}", t)
                    modelDeferred.completeExceptionally(t)
                }
            }
        }
    }

    @Synchronized
    private fun ensureModelExtracted(ctx: Context): String {
        val destFile = File(ctx.filesDir, MODEL_FILENAME)

        // 1. Check if model already exists and size matches expected size
        if (destFile.exists()) {
            val curLen = destFile.length()
            Log.i(TAG, "Found existing model at: ${destFile.absolutePath} (size: $curLen bytes)")
            if (curLen == EXPECTED_MODEL_SIZE || curLen >= MIN_VALID_SIZE) {
                val sizeMb = curLen / (1024.0 * 1024.0)
                Log.i(TAG, "Model already extracted and size verified: ${destFile.absolutePath} (size: $curLen bytes, ${"%.2f".format(sizeMb)} MB). Skipping copy.")
                return destFile.absolutePath
            } else {
                Log.w(TAG, "Existing model size ($curLen bytes) does not match expected ($EXPECTED_MODEL_SIZE bytes). Re-extracting from assets...")
                destFile.delete()
            }
        }

        // 2. Extract model from bundled APK assets
        Log.i(TAG, "Extracting bundled $MODEL_FILENAME from APK assets to app-private storage: ${destFile.absolutePath}")
        val tempFile = File(ctx.filesDir, "${MODEL_FILENAME}.tmp")
        if (tempFile.exists()) {
            tempFile.delete()
        }

        val startTime = System.currentTimeMillis()
        try {
            ctx.assets.open(MODEL_FILENAME).use { input ->
                tempFile.outputStream().use { output ->
                    val buffer = ByteArray(1024 * 1024) // 1MB streaming buffer
                    var bytesRead: Int
                    var totalWritten = 0L
                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                        totalWritten += bytesRead
                    }
                    output.flush()
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Asset copy failed for $MODEL_FILENAME: ${e.message}", e)
            tempFile.delete()
            throw IllegalStateException("Failed to extract bundled asset $MODEL_FILENAME: ${e.message}", e)
        }

        val elapsedSec = (System.currentTimeMillis() - startTime) / 1000.0
        val extractedSize = tempFile.length()
        Log.i(TAG, "Extraction stream finished in ${"%.2f".format(elapsedSec)}s. Extracted size: $extractedSize bytes")

        // 3. Verify copied file size
        if (extractedSize != EXPECTED_MODEL_SIZE && extractedSize < MIN_VALID_SIZE) {
            tempFile.delete()
            val err = "Model verification failed: extracted size ($extractedSize bytes) does not match expected ($EXPECTED_MODEL_SIZE bytes)"
            Log.e(TAG, err)
            throw IllegalStateException(err)
        }

        // Move temp file to final destination
        if (destFile.exists()) {
            destFile.delete()
        }
        if (!tempFile.renameTo(destFile)) {
            tempFile.copyTo(destFile, overwrite = true)
            tempFile.delete()
        }

        val finalSize = destFile.length()
        val finalMb = finalSize / (1024.0 * 1024.0)
        Log.i(TAG, "=== MODEL EXTRACTION & VERIFICATION SUCCESSFUL ===")
        Log.i(TAG, "Actual model path: ${destFile.absolutePath}")
        Log.i(TAG, "Actual model size: $finalSize bytes (${"%.2f".format(finalMb)} MB)")

        return destFile.absolutePath
    }

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "loadModel" -> {
                scope.launch {
                    try {
                        val path = if (context != null) {
                            modelDeferred.await()
                        } else {
                            call.argument<String>("model_path") ?: "/data/data/org.shiksha.shiksha_app/files/$MODEL_FILENAME"
                        }
                        val threads = call.argument<Int>("n_threads") ?: 4
                        val ctxSize = call.argument<Int>("ctx_size") ?: 2048
                        val success = LlamaBridge.loadModel(path, threads, ctxSize)
                        CoroutineScope(Dispatchers.Main).launch {
                            result.success(mapOf(
                                "status" to if (success) "loaded" else "failed",
                                "path" to path
                            ))
                        }
                    } catch (e: Throwable) {
                        Log.e(TAG, "loadModel error: ${e.message}", e)
                        CoroutineScope(Dispatchers.Main).launch {
                            result.error("LOAD_ERROR", e.message, null)
                        }
                    }
                }
            }
            "isModelReady" -> {
                val isReady = modelDeferred.isCompleted && !modelDeferred.isCancelled
                result.success(mapOf("ready" to isReady))
            }
            "unloadModel" -> {
                activeGenerationJob?.cancel()
                LlamaBridge.unloadModel()
                result.success(mapOf("status" to "unloaded"))
            }
            "stopGeneration" -> {
                activeGenerationJob?.cancel()
                LlamaBridge.stopGeneration()
                result.success(mapOf("cancelled" to true))
            }
            "getModelInfo" -> {
                result.success(mapOf(
                    "engine" to "llama.cpp Android",
                    "format" to "GGUF Q4_K_M",
                    "model" to MODEL_FILENAME,
                    "size_mb" to 461.79,
                    "offline" to true
                ))
            }
            "generateStream" -> {
                val prompt = call.argument<String>("prompt") ?: ""
                val maxTokens = call.argument<Int>("max_tokens") ?: 250
                val temperature = (call.argument<Double>("temperature") ?: 0.0).toFloat()
                
                // Cancel any previous in-flight generation job to guarantee clean sequential state
                activeGenerationJob?.cancel()
                LlamaBridge.resetState()

                activeGenerationJob = scope.launch {
                    try {
                        if (context != null) {
                            val path = modelDeferred.await()
                            LlamaBridge.loadModel(path, 4, 2048)
                        }
                    } catch (e: Throwable) {
                        Log.e(TAG, "Cannot start generation, model not ready: ${e.message}", e)
                        CoroutineScope(Dispatchers.Main).launch {
                            streamEventSink?.error("MODEL_NOT_READY", "Model extraction/loading failed: ${e.message}", null)
                        }
                        return@launch
                    }

                    val success = LlamaBridge.nativeGenerateStream(
                        prompt,
                        maxTokens,
                        temperature,
                        object : TokenStreamCallback {
                            override fun onToken(tokenPiece: String) {
                                CoroutineScope(Dispatchers.Main).launch {
                                    streamEventSink?.success(mapOf(
                                        "status" to "generating",
                                        "delta" to tokenPiece,
                                        "done" to false
                                    ))
                                }
                            }

                            override fun onComplete(tokensPerSec: Float, promptTokensPerSec: Float, totalTokens: Int) {
                                CoroutineScope(Dispatchers.Main).launch {
                                    streamEventSink?.success(mapOf(
                                        "status" to "completed",
                                        "done" to true,
                                        "metrics" to mapOf(
                                            "tokens_per_second" to tokensPerSec,
                                            "prompt_tokens_per_second" to promptTokensPerSec,
                                            "completion_tokens" to totalTokens
                                        )
                                    ))
                                }
                            }

                            override fun onError(errorMessage: String) {
                                CoroutineScope(Dispatchers.Main).launch {
                                    streamEventSink?.error("INFERENCE_ERROR", errorMessage, null)
                                }
                            }
                        }
                    )
                    if (!success) {
                        CoroutineScope(Dispatchers.Main).launch {
                            streamEventSink?.error("NATIVE_CALL_FAILED", "Native stream failed to start", null)
                        }
                    }
                }
                result.success(mapOf("started" to true))
            }
            else -> result.notImplemented()
        }
    }
}
