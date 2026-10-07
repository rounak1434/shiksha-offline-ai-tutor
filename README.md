# SHIKSHA — Offline AI Tutor for School Education (Class 1–8)

SHIKSHA is an offline AI tutoring system fine-tuned specifically for elementary and middle school students (Class 1–8, with primary emphasis on Class 5–8 STEM). It runs completely on-device without internet access, providing structured, age-appropriate explanations, formulas, calculations, and misconception corrections.

---

## Current Project Status: BACKEND PRODUCTION COMPLETE (PASS)

- **Fine-Tuning:** 1-epoch QLoRA on `Qwen/Qwen3-0.6B` with 1,500 curriculum-aligned samples.
- **Evaluation:** Evaluated on 300 held-out test questions (100% clean non-thinking output, 100% factual pass on Newton's laws and mass vs weight).
- **Standalone Model:** LoRA weights merged into standalone HF model (`output/qwen3_k8_tutor_merged/`).
- **GGUF Conversion:** Exported to high-fidelity F16 GGUF (`output/qwen3_k8_tutor_f16.gguf`, 1.14 GB).
- **Quantization:** Quantized to production Android candidate `Q4_K_M` (`output/qwen3_k8_tutor_q4_k_m.gguf`, **378.32 MB**).
- **Native Backend:** Production inference service with REST and Server-Sent Events (SSE) streaming (`backend/`).
- **Automated Tests:** 9/9 automated backend tests passing (`tests/test_backend_service.py`).
- **Android Integration:** JNI bridge, Kotlin Platform Channels, and decoupled Flutter Dart service (`android_integration/`).

---

## Quickstart

### 1. Run Local Backend Service
```powershell
python backend/service.py 8080
```

### 2. Run PC Benchmark
```powershell
python backend/benchmark.py
```

### 3. Run Automated Tests
```powershell
python tests/test_backend_service.py
```

---

## Architecture Documentation

See [`docs/backend_architecture.md`](docs/backend_architecture.md) for full architectural specifications, API schemas, and Android integration guides.
