# SHIKSHA Backend Architecture & Production Inference Specification

**Project:** Offline AI Tutor for Class 1–8 School Students  
**Primary Target:** Classes 5–8 (STEM & Foundational Learning)  
**Deployment Target:** Offline Android (via Flutter + native llama.cpp) & Local Inference Service  

---

## 1. System Architecture Overview

```
+-----------------------------------------------------------------------------------+
|                            FLUTTER FRONTEND (UI)                                  |
|         (Stitch-Designed Classroom Interface: Chat, Steps, Formula Viewer)        |
+-----------------------------------------------------------------------------------+
                                       |
                   MethodChannel & EventChannel / Local HTTP & SSE
                                       |
+-----------------------------------------------------------------------------------+
|                        SHIKSHA INFERENCE ABSTRACTION LAYER                        |
|  - loadModel() / unloadModel()                                                    |
|  - streamGenerate() -> token chunks & structured pedagogical events              |
|  - stopGeneration() -> immediate native cancellation                              |
|  - getModelInfo() / benchmark()                                                   |
+-----------------------------------------------------------------------------------+
                                       |
                               JNI / Native C-API
                                       |
+-----------------------------------------------------------------------------------+
|                        NATIVE LLAMA.CPP INFERENCE RUNTIME                         |
|  - Model: Qwen3-0.6B Fine-Tuned (Q4_K_M Quantized GGUF, 378.32 MB)               |
|  - 100% Offline: Zero cloud, API, or external network dependencies               |
|  - CPU / ARM64 NEON Dot-Product Acceleration                                      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Model Artifacts & File Inventory

All models are stored locally under `output/`. Baseline artifacts have been strictly preserved.

| Artifact Path | Format | Size | Purpose |
| :--- | :--- | :--- | :--- |
| `output/qwen3_k8_tutor_q4_k_m.gguf` | GGUF (Q4_K_M) | **378.32 MB** (396,700,576 bytes) | **Production Android & Offline Candidate** |
| `output/qwen3_k8_tutor_f16.gguf` | GGUF (F16) | **1,142.67 MB** (1,198,178,208 bytes) | High-fidelity reference GGUF |
| `output/qwen3_k8_tutor_merged/` | Hugging Face BF16 | **1,147.80 MB** | Standalone merged transformer model |
| `output/qwen3_k8_tutor_lora/` | PEFT LoRA Adapter | **15.30 MB** (16,047,108 bytes) | Final trained K-8 LoRA adapter ($r=8, \alpha=16$) |
| `output/qwen3_tutor_q4_k_m.gguf` | GGUF (Q4_K_M) | **378.32 MB** | *Baseline preserved model* |
| `output/qwen3_tutor_merged/` | Hugging Face BF16 | **1,142.67 MB** | *Baseline preserved model* |
| `output/qwen3_offline_tutor_lora/` | PEFT LoRA Adapter | **15.30 MB** | *Baseline preserved adapter* |

---

## 3. Build & Conversion Commands

### Step 1: LoRA Merge
Fuses the trained LoRA adapter weights directly into the base `Qwen/Qwen3-0.6B` model:
```powershell
python train/merge_k8_tutor.py
```
*Output: `output/qwen3_k8_tutor_merged/`*

### Step 2: Convert to High-Fidelity F16 GGUF
```powershell
python llama.cpp/convert_hf_to_gguf.py output/qwen3_k8_tutor_merged --outtype f16 --outfile output/qwen3_k8_tutor_f16.gguf
```
*Output: `output/qwen3_k8_tutor_f16.gguf`*

### Step 3: Quantize to Production Q4_K_M GGUF
```powershell
llama.cpp/build_bin/llama-quantize.exe output/qwen3_k8_tutor_f16.gguf output/qwen3_k8_tutor_q4_k_m.gguf Q4_K_M
```
*Output: `output/qwen3_k8_tutor_q4_k_m.gguf` (378.32 MB)*

---

## 4. Run & Serving Commands

### Running Local CLI Inference
```powershell
llama.cpp\build_bin\llama-cli.exe -m output/qwen3_k8_tutor_q4_k_m.gguf -p "<|im_start|>user`nStudent grade: Class 6`nSubject: Mathematics`nQuestion: Solve 3x + 5 = 20 step-by-step.<|im_end|>`n<|im_start|>assistant`n" -n 150 --simple-io -st --no-display-prompt
```

### Starting the Local Offline Backend Service
```powershell
python backend/service.py 8080
```
Runs a local HTTP and SSE streaming server on `http://127.0.0.1:8080`.

---

## 5. API & Event Contract Specification

### 1. `POST /generate` (Synchronous Request)
**Request Body:**
```json
{
  "request_id": "req-101",
  "prompt": "Solve 3x + 5 = 20 step-by-step.",
  "grade": 6,
  "subject": "Mathematics",
  "max_tokens": 150,
  "temperature": 0.0
}
```

**Response Body:**
```json
{
  "request_id": "req-101",
  "status": "completed",
  "content": "Given: 3x + 5 = 20\n\nCalculation:\nStep 1: Subtract 5: 3x = 15\nStep 2: Divide by 3: x = 5\n\nVerification: 3(5) + 5 = 20\n\nFinal Answer: 5",
  "done": true,
  "metadata": {
    "answer_type": "numerical_step_by_step",
    "grade": 6,
    "subject": "Mathematics",
    "given": "3x + 5 = 20",
    "steps": [
      "Subtract 5: 3x = 15",
      "Divide by 3: x = 5"
    ],
    "verification": "3(5) + 5 = 20",
    "final_answer": "5"
  },
  "metrics": {
    "completion_tokens": 68,
    "tokens_per_second": 14.8,
    "prompt_tokens_per_second": 138.3,
    "latency_ms": 5210.4
  }
}
```

### 2. `POST /generate/stream` (Server-Sent Events)
Streams newline-delimited SSE chunks:
```text
data: {"request_id": "req-101", "status": "generating", "delta": "Given:", "accumulated": "Given:", "done": false}

data: {"request_id": "req-101", "status": "generating", "delta": " 3x + 5 = 20", "accumulated": "Given: 3x + 5 = 20", "done": false}

...

data: {"request_id": "req-101", "status": "completed", "delta": "", "accumulated": "...", "done": true, "metadata": {...}, "metrics": {...}}
```

### 3. `POST /cancel`
Cancels an ongoing generation process:
```json
{
  "request_id": "req-101"
}
```

---

## 6. Automated Testing & Verification

### Running Automated Backend Unit Tests
```powershell
python tests/test_backend_service.py
```
Tests:
- Model loading / unloading
- Synchronous inference
- Streaming token delivery
- In-flight cancellation
- Malformed inputs
- Missing model file handling
- Runtime metrics extraction
- Offline integrity (blocks external socket connections)
- Pedagogical structure parsing

### Running Comparative GGUF Regressions (F16 vs Q4_K_M)
```powershell
python tests/compare_gguf_models.py
```

---

## 7. Performance Benchmarks (PC Local Host)

> [!NOTE]  
> The following figures are strictly **PC benchmarks** executed on a Windows 11 host (llama.cpp CPU-x64, 4 threads). They do NOT represent Android hardware speeds.

| Metric | Measured Value (PC) |
| :--- | :--- |
| **Model Format** | GGUF Q4_K_M (378.32 MB) |
| **Cold Model Load Time** | **1.55 ms** (memory-mapped file) |
| **Average Prompt Processing Speed** | **137.83 tokens / sec** |
| **Average Generation Speed** | **14.47 tokens / sec** |
| **Average Turnaround Latency** | **8.01 seconds** (for ~120 token structured answer) |
| **Process Working Memory** | **~19.45 MB** (process wrapper) + mmap file cache |

---

## 8. Android Native Integration Boundary

### Native JNI Layer
- **Source:** [`android_integration/cpp/shiksha_llama_jni.cpp`](file:///C:/Rounak/RVSHACK/android_integration/cpp/shiksha_llama_jni.cpp)
- **Build Script:** [`android_integration/cpp/CMakeLists.txt`](file:///C:/Rounak/RVSHACK/android_integration/cpp/CMakeLists.txt)
- Connects directly to `llama.h` C-API, offloading token sampling to native code.

### Kotlin Platform Bridge
- **Files:**
  - [`android_integration/kotlin/LlamaBridge.kt`](file:///C:/Rounak/RVSHACK/android_integration/kotlin/LlamaBridge.kt)
  - [`android_integration/kotlin/ShikshaPlatformChannel.kt`](file:///C:/Rounak/RVSHACK/android_integration/kotlin/ShikshaPlatformChannel.kt)
- Exposes `MethodChannel` (`org.shiksha.tutor/inference`) and `EventChannel` (`org.shiksha.tutor/stream`) to Flutter.

### Flutter Dart Service
- **File:** [`android_integration/flutter/shiksha_tutor_service.dart`](file:///C:/Rounak/RVSHACK/android_integration/flutter/shiksha_tutor_service.dart)
- Provides a clean, UI-independent `IShikshaTutorService` abstraction with cancellation and structured event handling.

---

## 9. Known Limitations & Target Constraints

1. **Host PC vs Mobile CPU:**
   - PC achieves ~14.5 tokens/sec on desktop Intel CPU.
   - Low-end Android smartphones (e.g., MediaTek Helio G85 / Snapdragon 680) are expected to generate at ~5–8 tokens/sec. Streaming token-by-token output is therefore mandatory to keep perceived latency below 200 ms.
2. **RAM Ceiling:**
   - Android target devices have 3–4 GB total RAM.
   - At **378.32 MB**, `qwen3_k8_tutor_q4_k_m.gguf` comfortably fits within the 600 MB memory budget without triggering Android low-memory killer (LMK).
