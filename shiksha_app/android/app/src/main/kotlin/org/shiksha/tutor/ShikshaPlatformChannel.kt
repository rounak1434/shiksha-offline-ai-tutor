package org.shiksha.tutor

import android.content.Context
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File

class ShikshaPlatformChannel(
    binaryMessenger: BinaryMessenger,
    private val context: Context? = null
) : MethodChannel.MethodCallHandler {
    private val methodChannel = MethodChannel(binaryMessenger, "org.shiksha.tutor/inference")
    private val eventChannel = EventChannel(binaryMessenger, "org.shiksha.tutor/stream")
    
    private var streamEventSink: EventChannel.EventSink? = null
    private val scope = CoroutineScope(Dispatchers.IO)
    private var activeGenerationJob: kotlinx.coroutines.Job? = null

    init {
        methodChannel.setMethodCallHandler(this)
        eventChannel.setStreamHandler(object : EventChannel.StreamHandler {
            override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
                streamEventSink = events
            }

            override fun onCancel(arguments: Any?) {
                // EventChannel.onCancel fires when a stream closes or client unlistens.
                // Do NOT invoke LlamaBridge.stopGeneration() here, because completed requests
                // will inadvertently cancel newly queued requests.
                streamEventSink = null
            }
        })
    }

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "loadModel" -> {
                var path = call.argument<String>("model_path")
                if (path.isNullOrEmpty() && context != null) {
                    val baseModel = File(context.filesDir, "qwen3_base_q4_k_m.gguf")
                    val k8Model = File(context.filesDir, "qwen3_k8_tutor_q4_k_m.gguf")
                    path = when {
                        baseModel.exists() -> baseModel.absolutePath
                        k8Model.exists() -> k8Model.absolutePath
                        else -> "/data/data/org.shiksha.shiksha_app/files/qwen3_base_q4_k_m.gguf"
                    }
                }
                
                val threads = call.argument<Int>("n_threads") ?: 4
                val ctxSize = call.argument<Int>("ctx_size") ?: 2048
                val success = if (path != null) LlamaBridge.loadModel(path, threads, ctxSize) else false
                result.success(mapOf(
                    "status" to if (success) "loaded" else "failed",
                    "path" to (path ?: "unknown")
                ))
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
                    "model" to "qwen3_base_q4_k_m.gguf",
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
