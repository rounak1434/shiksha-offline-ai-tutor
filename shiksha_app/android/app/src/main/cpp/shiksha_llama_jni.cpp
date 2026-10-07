/**
 * shiksha_llama_jni.cpp
 * JNI Native Bridge connecting Android Kotlin runtime with offline llama.cpp inference engine.
 * Target: Low-cost Android smartphones running SHIKSHA K-8 offline AI tutor.
 */

#include <jni.h>
#include <string>
#include <android/log.h>
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>
#include <mutex>
#include <algorithm>

#include "llama.h"

#define TAG "ShikshaLlamaJNI"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, TAG, __VA_ARGS__)
#define LOGW(...) __android_log_print(ANDROID_LOG_WARN, TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, TAG, __VA_ARGS__)

static std::mutex g_model_mutex;
static llama_model* g_model = nullptr;
static std::string g_loaded_model_path = "";
static int g_default_threads = 4;
static int g_default_ctx_size = 2048;

static std::atomic<bool> g_is_generating(false);
static std::atomic<bool> g_cancel_requested(false);

// Extracts complete UTF-8 sequences and leaves trailing incomplete multi-byte bytes in buffer
static std::string extract_complete_utf8(std::string& buffer) {
    if (buffer.empty()) return "";

    size_t i = 0;
    size_t last_valid_end = 0;
    const size_t len = buffer.length();

    while (i < len) {
        unsigned char c = (unsigned char)buffer[i];
        size_t seq_len = 0;
        if (c < 0x80) {
            seq_len = 1;
        } else if ((c & 0xE0) == 0xC0) {
            seq_len = 2;
        } else if ((c & 0xF0) == 0xE0) {
            seq_len = 3;
        } else if ((c & 0xF8) == 0xF0) {
            seq_len = 4;
        } else {
            // Invalid lead byte, advance 1
            i++;
            last_valid_end = i;
            continue;
        }

        if (i + seq_len <= len) {
            bool valid = true;
            for (size_t j = 1; j < seq_len; ++j) {
                if (((unsigned char)buffer[i + j] & 0xC0) != 0x80) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                i += seq_len;
                last_valid_end = i;
            } else {
                i++;
                last_valid_end = i;
            }
        } else {
            // Incomplete sequence at end of buffer: keep in buffer for next token
            break;
        }
    }

    if (last_valid_end == 0) {
        return "";
    }

    std::string complete_str = buffer.substr(0, last_valid_end);
    buffer = buffer.substr(last_valid_end);
    return complete_str;
}

// Converts UTF-8 string to a safe Java String via UTF-16, avoiding Modified UTF-8 JNI aborts
static jstring create_java_string_from_utf8(JNIEnv* env, const std::string& utf8_str) {
    if (utf8_str.empty()) {
        return env->NewString(nullptr, 0);
    }
    std::vector<jchar> utf16;
    utf16.reserve(utf8_str.size());
    size_t i = 0;
    while (i < utf8_str.size()) {
        uint32_t cp = 0;
        unsigned char c = (unsigned char)utf8_str[i];
        if (c < 0x80) {
            cp = c;
            i += 1;
        } else if ((c & 0xE0) == 0xC0 && i + 1 < utf8_str.size()) {
            cp = ((c & 0x1F) << 6) | (utf8_str[i + 1] & 0x3F);
            i += 2;
        } else if ((c & 0xF0) == 0xE0 && i + 2 < utf8_str.size()) {
            cp = ((c & 0x0F) << 12) | ((utf8_str[i + 1] & 0x3F) << 6) | (utf8_str[i + 2] & 0x3F);
            i += 3;
        } else if ((c & 0xF8) == 0xF0 && i + 3 < utf8_str.size()) {
            cp = ((c & 0x07) << 18) | ((utf8_str[i + 1] & 0x3F) << 12) | ((utf8_str[i + 2] & 0x3F) << 6) | (utf8_str[i + 3] & 0x3F);
            i += 4;
        } else {
            cp = 0xFFFD;
            i += 1;
        }

        if (cp < 0x10000) {
            utf16.push_back((jchar)cp);
        } else {
            cp -= 0x10000;
            utf16.push_back((jchar)(0xD800 + (cp >> 10)));
            utf16.push_back((jchar)(0xDC00 + (cp & 0x3FF)));
        }
    }
    return env->NewString(utf16.data(), (jsize)utf16.size());
}

extern "C" {

JNIEXPORT jboolean JNICALL
Java_org_shiksha_tutor_LlamaBridge_nativeLoadModel(
    JNIEnv* env,
    jobject /* this */,
    jstring model_path,
    jint n_threads,
    jint ctx_size) {
    
    std::lock_guard<std::mutex> lock(g_model_mutex);
    const char* path = env->GetStringUTFChars(model_path, nullptr);
    std::string path_str(path ? path : "");
    if (path) {
        env->ReleaseStringUTFChars(model_path, path);
    }

    LOGI("Native loadModel: %s (threads: %d, ctx: %d)", path_str.c_str(), n_threads, ctx_size);

    if (g_model != nullptr && g_loaded_model_path == path_str) {
        LOGI("Model already loaded at %s, reusing handle", path_str.c_str());
        return JNI_TRUE;
    }

    if (g_model != nullptr) {
        LOGI("Freeing previously loaded model");
        llama_model_free(g_model);
        g_model = nullptr;
    }

    llama_backend_init();

    llama_model_params model_params = llama_model_default_params();
    model_params.n_gpu_layers = 0; // Pure CPU execution on mobile

    g_model = llama_model_load_from_file(path_str.c_str(), model_params);
    if (g_model == nullptr) {
        LOGE("Failed to load GGUF model from path: %s", path_str.c_str());
        return JNI_FALSE;
    }

    g_loaded_model_path = path_str;
    g_default_threads = n_threads > 0 ? n_threads : 4;
    g_default_ctx_size = ctx_size > 0 ? ctx_size : 2048;

    LOGI("Successfully loaded GGUF model from %s", path_str.c_str());
    return JNI_TRUE;
}

JNIEXPORT void JNICALL
Java_org_shiksha_tutor_LlamaBridge_nativeUnloadModel(
    JNIEnv* env,
    jobject /* this */) {
    std::lock_guard<std::mutex> lock(g_model_mutex);
    LOGI("Native unloadModel called");
    g_cancel_requested.store(true);
    if (g_model != nullptr) {
        llama_model_free(g_model);
        g_model = nullptr;
    }
    g_loaded_model_path = "";
    llama_backend_free();
}

JNIEXPORT void JNICALL
Java_org_shiksha_tutor_LlamaBridge_nativeStopGeneration(
    JNIEnv* env,
    jobject /* this */) {
    LOGI("Native stopGeneration called: requesting cancellation");
    g_cancel_requested.store(true);
}

JNIEXPORT void JNICALL
Java_org_shiksha_tutor_LlamaBridge_nativeResetState(
    JNIEnv* env,
    jobject /* this */) {
    LOGI("Native resetState called: clearing cancellation and generation flags");
    g_cancel_requested.store(false);
    g_is_generating.store(false);
}

JNIEXPORT jboolean JNICALL
Java_org_shiksha_tutor_LlamaBridge_nativeGenerateStream(
    JNIEnv* env,
    jobject /* this */,
    jstring prompt,
    jint max_tokens,
    jfloat temperature,
    jobject token_callback) {
    
    const char* p = env->GetStringUTFChars(prompt, nullptr);
    std::string prompt_str(p ? p : "");
    if (p) {
        env->ReleaseStringUTFChars(prompt, p);
    }

    LOGI("nativeGenerateStream: incoming prompt length = %zu chars", prompt_str.length());

    // Reset cancellation and generation state cleanly at start of every request
    g_cancel_requested.store(false);
    g_is_generating.store(true);

    jclass callback_class = env->GetObjectClass(token_callback);
    jmethodID on_token_method = env->GetMethodID(callback_class, "onToken", "(Ljava/lang/String;)V");
    jmethodID on_complete_method = env->GetMethodID(callback_class, "onComplete", "(FFI)V");
    jmethodID on_error_method = env->GetMethodID(callback_class, "onError", "(Ljava/lang/String;)V");

    if (!on_token_method || !on_complete_method || !on_error_method) {
        LOGE("Could not locate callback methods");
        g_is_generating.store(false);
        return JNI_FALSE;
    }

    std::lock_guard<std::mutex> lock(g_model_mutex);

    // Fallback model load if loadModel was not yet invoked
    if (g_model == nullptr) {
        const char* default_path = "/data/data/org.shiksha.shiksha_app/files/qwen3_base_q4_k_m.gguf";
        LOGI("Model handle null, attempting autoload from: %s", default_path);
        llama_backend_init();
        llama_model_params model_params = llama_model_default_params();
        model_params.n_gpu_layers = 0;
        g_model = llama_model_load_from_file(default_path, model_params);
        if (g_model == nullptr) {
            LOGE("Failed to autoload model from %s", default_path);
            jstring jerr = create_java_string_from_utf8(env, "Model file could not be loaded on device.");
            env->CallVoidMethod(token_callback, on_error_method, jerr);
            env->DeleteLocalRef(jerr);
            g_is_generating.store(false);
            return JNI_TRUE;
        }
        g_loaded_model_path = default_path;
    }

    const llama_vocab* vocab = llama_model_get_vocab(g_model);
    if (vocab == nullptr) {
        LOGE("Failed to get vocab from model");
        jstring jerr = create_java_string_from_utf8(env, "Model vocabulary unavailable.");
        env->CallVoidMethod(token_callback, on_error_method, jerr);
        env->DeleteLocalRef(jerr);
        g_is_generating.store(false);
        return JNI_TRUE;
    }

    // Tokenize the prompt
    int n_prompt_estimate = -llama_tokenize(vocab, prompt_str.c_str(), prompt_str.size(), nullptr, 0, true, true);
    if (n_prompt_estimate <= 0) {
        n_prompt_estimate = 2048;
    }
    std::vector<llama_token> prompt_tokens(n_prompt_estimate);
    int n_prompt = llama_tokenize(vocab, prompt_str.c_str(), prompt_str.size(), prompt_tokens.data(), prompt_tokens.size(), true, true);
    if (n_prompt < 0) {
        prompt_tokens.resize(-n_prompt);
        n_prompt = llama_tokenize(vocab, prompt_str.c_str(), prompt_str.size(), prompt_tokens.data(), prompt_tokens.size(), true, true);
    }
    if (n_prompt <= 0) {
        LOGE("Failed to tokenize prompt");
        jstring jerr = create_java_string_from_utf8(env, "Failed to tokenize prompt.");
        env->CallVoidMethod(token_callback, on_error_method, jerr);
        env->DeleteLocalRef(jerr);
        g_is_generating.store(false);
        return JNI_TRUE;
    }
    prompt_tokens.resize(n_prompt);
    LOGI("Tokenized prompt: %d tokens", n_prompt);

    // Initialize a fresh context for this request to guarantee clean KV-cache and state
    llama_context_params ctx_params = llama_context_default_params();
    uint32_t needed_ctx = (uint32_t)(n_prompt + max_tokens + 128);
    ctx_params.n_ctx = std::max(needed_ctx, (uint32_t)g_default_ctx_size);
    ctx_params.n_batch = 512;
    ctx_params.n_threads = g_default_threads;
    ctx_params.n_threads_batch = g_default_threads;
    ctx_params.no_perf = true;

    llama_context* ctx = llama_init_from_model(g_model, ctx_params);
    if (ctx == nullptr) {
        LOGE("Failed to allocate llama_context");
        jstring jerr = create_java_string_from_utf8(env, "Failed to allocate inference context.");
        env->CallVoidMethod(token_callback, on_error_method, jerr);
        env->DeleteLocalRef(jerr);
        g_is_generating.store(false);
        return JNI_TRUE;
    }

    // Configure sampling chain
    auto sparams = llama_sampler_chain_default_params();
    sparams.no_perf = true;
    llama_sampler* smpl = llama_sampler_chain_init(sparams);



    if (temperature > 0.05f) {
        llama_sampler_chain_add(smpl, llama_sampler_init_temp(temperature));
        llama_sampler_chain_add(smpl, llama_sampler_init_dist(LLAMA_DEFAULT_SEED));
    } else {
        llama_sampler_chain_add(smpl, llama_sampler_init_greedy());
    }

    llama_batch_ext* batch = llama_batch_ext_init(ctx);
    auto t_start = std::chrono::high_resolution_clock::now();

    // Ingest prompt in chunks of n_batch (512)
    const int32_t n_batch_limit = 512;
    bool prompt_failed = false;

    for (int32_t i = 0; i < n_prompt; i += n_batch_limit) {
        if (g_cancel_requested.load()) {
            LOGI("Cancelled before prompt ingestion completed");
            prompt_failed = true;
            break;
        }
        int32_t chunk_size = std::min(n_prompt - i, n_batch_limit);
        llama_batch_ext_clear(batch);
        for (int32_t j = 0; j < chunk_size; ++j) {
            int32_t idx = llama_batch_ext_add_token(batch, 0, prompt_tokens[i + j]);
            llama_pos pos = (llama_pos)(i + j);
            llama_batch_ext_set_pos(batch, idx, &pos);
        }
        if (i + chunk_size == n_prompt) {
            llama_batch_ext_set_output_logits(batch, chunk_size - 1, true);
        }

        if (llama_process(ctx, LLAMA_PROCESS_TYPE_DECODE, batch)) {
            LOGE("llama_process failed on prompt chunk starting at token %d", i);
            prompt_failed = true;
            break;
        }
    }

    if (prompt_failed) {
        llama_batch_ext_free(batch);
        llama_sampler_free(smpl);
        llama_free(ctx);
        g_is_generating.store(false);
        if (g_cancel_requested.load()) {
            LOGI("Request cancelled early, exiting gracefully");
            return JNI_TRUE;
        }
        jstring jerr = create_java_string_from_utf8(env, "Inference failed during prompt evaluation.");
        env->CallVoidMethod(token_callback, on_error_method, jerr);
        env->DeleteLocalRef(jerr);
        return JNI_TRUE;
    }

    // Autoregressive generation loop
    int total_generated = 0;
    llama_pos current_pos = (llama_pos)n_prompt;
    bool in_think_block = false;
    std::string utf8_accumulator = "";

    while (total_generated < max_tokens) {
        if (g_cancel_requested.load()) {
            LOGI("Generation cancelled during decoding loop at token %d", total_generated);
            break;
        }

        llama_token new_token_id = llama_sampler_sample(smpl, ctx, -1);
        if (llama_vocab_is_eog(vocab, new_token_id)) {
            LOGI("EOG token reached: %d", new_token_id);
            break;
        }

        char piece_buf[256];
        int piece_len = llama_token_to_piece(vocab, new_token_id, piece_buf, sizeof(piece_buf), 0, false);
        if (piece_len > 0) {
            std::string piece(piece_buf, piece_len);

            // Filter out <think> ... </think> reasoning traces
            if (piece.find("<think>") != std::string::npos) {
                in_think_block = true;
            }
            if (in_think_block) {
                if (piece.find("</think>") != std::string::npos) {
                    in_think_block = false;
                }
            } else if (piece != "<|im_end|>" && piece != "<|endoftext|>" && piece.find("</think>") == std::string::npos) {
                utf8_accumulator += piece;
                std::string to_emit = extract_complete_utf8(utf8_accumulator);
                if (!to_emit.empty()) {
                    jstring jtok = create_java_string_from_utf8(env, to_emit);
                    env->CallVoidMethod(token_callback, on_token_method, jtok);
                    env->DeleteLocalRef(jtok);
                }
            }
        }

        total_generated++;

        // Prepare single-token batch for next iteration
        llama_batch_ext_clear(batch);
        int32_t idx = llama_batch_ext_add_token(batch, 0, new_token_id);
        llama_batch_ext_set_pos(batch, idx, &current_pos);
        llama_batch_ext_set_output_logits(batch, 0, true);
        current_pos++;

        if (llama_process(ctx, LLAMA_PROCESS_TYPE_DECODE, batch)) {
            LOGE("llama_process failed on generated token index %d", total_generated);
            break;
        }
    }

    // Flush any remaining characters in accumulator
    if (!utf8_accumulator.empty() && !in_think_block) {
        jstring jtok = create_java_string_from_utf8(env, utf8_accumulator);
        env->CallVoidMethod(token_callback, on_token_method, jtok);
        env->DeleteLocalRef(jtok);
        utf8_accumulator.clear();
    }

    auto t_end = std::chrono::high_resolution_clock::now();
    float elapsed_s = std::chrono::duration<float>(t_end - t_start).count();
    float tok_per_sec = elapsed_s > 0 ? (total_generated / elapsed_s) : 0.0f;

    LOGI("Generation finished: %d tokens generated in %.2f s (%.2f t/s)", total_generated, elapsed_s, tok_per_sec);

    // Send onComplete event to Flutter
    env->CallVoidMethod(token_callback, on_complete_method, tok_per_sec, 0.0f, total_generated);

    // Guaranteed cleanup of request resources
    llama_batch_ext_free(batch);
    llama_sampler_free(smpl);
    llama_free(ctx);

    g_is_generating.store(false);
    return JNI_TRUE;
}

} // extern "C"
