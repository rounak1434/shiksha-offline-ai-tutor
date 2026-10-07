package org.shiksha.tutor

import android.util.Log

interface TokenStreamCallback {
    fun onToken(tokenPiece: String)
    fun onComplete(tokensPerSec: Float, promptTokensPerSec: Float, totalTokens: Int)
    fun onError(errorMessage: String)
}

object LlamaBridge {
    private const val TAG = "LlamaBridge"

    init {
        try {
            System.loadLibrary("ggml-base")
            System.loadLibrary("ggml-cpu")
            System.loadLibrary("ggml")
            System.loadLibrary("llama")
            System.loadLibrary("llama-common")
            System.loadLibrary("shiksha_llama")
            Log.i(TAG, "Successfully loaded native llama.cpp and libshiksha_llama.so")
        } catch (e: UnsatisfiedLinkError) {
            Log.w(TAG, "Native library load issue: ${e.message}")
        }
    }

    external fun nativeLoadModel(modelPath: String, nThreads: Int, ctxSize: Int): Boolean
    external fun nativeUnloadModel()
    external fun nativeStopGeneration()
    external fun nativeResetState()
    external fun nativeGenerateStream(
        prompt: String,
        maxTokens: Int,
        temperature: Float,
        callback: TokenStreamCallback
    ): Boolean

    fun loadModel(modelPath: String, threads: Int = 4, ctxSize: Int = 2048): Boolean {
        return try {
            nativeLoadModel(modelPath, threads, ctxSize)
        } catch (e: Throwable) {
            Log.e(TAG, "Error loading model: ${e.message}")
            false
        }
    }

    fun unloadModel() {
        try {
            nativeUnloadModel()
        } catch (e: Throwable) {
            Log.e(TAG, "Error unloading model: ${e.message}")
        }
    }

    fun resetState() {
        try {
            nativeResetState()
        } catch (e: Throwable) {
            Log.e(TAG, "Error resetting state: ${e.message}")
        }
    }

    fun stopGeneration() {
        try {
            nativeStopGeneration()
        } catch (e: Throwable) {
            Log.e(TAG, "Error stopping generation: ${e.message}")
        }
    }
}
