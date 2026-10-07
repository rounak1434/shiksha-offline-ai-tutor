package org.shiksha.tutor

import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File

class ShikshaPlatformChannel(binaryMessenger: BinaryMessenger) : MethodChannel.MethodCallHandler {
    private val methodChannel = MethodChannel(binaryMessenger, "org.shiksha.tutor/inference")
    private val eventChannel = EventChannel(binaryMessenger, "org.shiksha.tutor/stream")
    
    private var streamEventSink: EventChannel.EventSink? = null
    private val scope = CoroutineScope(Dispatchers.IO)

    init {
        methodChannel.setMethodCallHandler(this)
        eventChannel.setStreamHandler(object : EventChannel.StreamHandler {
            override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
                streamEventSink = events
            }

            override fun onCancel(arguments: Any?) {
                streamEventSink = null
                LlamaBridge.stopGeneration()
            }
        })
    }

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "loadModel" -> {
                val path = call.argument<String>("model_path")
                if (path == null) {
                    result.error("INVALID_ARG", "model_path is required", null)
                    return
                }
                val threads = call.argument<Int>("n_threads") ?: 4
                val ctxSize = call.argument<Int>("ctx_size") ?: 2048
                val success = LlamaBridge.loadModel(path, threads, ctxSize)
                result.success(mapOf("status" to if (success) "loaded" else "failed", "path" to path))
            }
            "unloadModel" -> {
                LlamaBridge.unloadModel()
                result.success(mapOf("status" to "unloaded"))
            }
            "stopGeneration" -> {
                LlamaBridge.stopGeneration()
                result.success(mapOf("cancelled" to true))
            }
            "getModelInfo" -> {
                result.success(mapOf(
                    "engine" to "llama.cpp Android",
                    "format" to "GGUF Q4_K_M",
                    "offline" to true
                ))
            }
            "generateStream" -> {
                val prompt = call.argument<String>("prompt") ?: ""
                val maxTokens = call.argument<Int>("max_tokens") ?: 250
                val temperature = (call.argument<Double>("temperature") ?: 0.0).toFloat()
                
                scope.launch {
                    LlamaBridge.nativeGenerateStream(
                        prompt,
                        maxTokens,
                        temperature,
                        object : TokenStreamCallback {
                            override fun onToken(tokenPiece: String) {
                                streamEventSink?.success(mapOf(
                                    "status" to "generating",
                                    "delta" to tokenPiece,
                                    "done" to false
                                ))
                            }

                            override fun onComplete(tokensPerSec: Float, promptTokensPerSec: Float, totalTokens: Int) {
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

                            override fun onError(errorMessage: String) {
                                streamEventSink?.error("INFERENCE_ERROR", errorMessage, null)
                            }
                        }
                    )
                }
                result.success(mapOf("started" to true))
            }
            else -> result.notImplemented()
        }
    }
}
