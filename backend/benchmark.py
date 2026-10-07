"""
backend/benchmark.py
SHIKSHA Backend Benchmark CLI.
Measures:
- Cold model load time
- Prompt processing speed (tokens/sec)
- Generation speed (tokens/sec)
- Peak / observed memory (RAM / VRAM)
- Latency (ms)
Clearly labels results as PC Benchmarks (not Android).
"""

import os
import sys
import json
import time
import psutil

sys.path.insert(0, r"C:\Rounak\RVSHACK")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from backend.inference_engine import ShikshaInferenceEngine

MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_q4_k_m.gguf"

def run_pc_benchmark(num_runs: int = 3):
    print("=" * 65)
    print("⚡ SHIKSHA BACKEND BENCHMARK (PC / LOCAL HOST)")
    print("⚠️  NOTE: These are PC benchmarks, NOT Android figures.")
    print("=" * 65)
    
    process = psutil.Process()
    mem_before_mb = process.memory_info().rss / (1024 * 1024)
    
    print(f"\nModel: {MODEL_PATH}")
    print(f"File size: {os.path.getsize(MODEL_PATH) / (1024 * 1024):.2f} MB")
    print(f"Base host RAM in use: {mem_before_mb:.2f} MB")
    
    engine = ShikshaInferenceEngine(model_path=MODEL_PATH)
    
    # 1. Cold load time
    print("\n[1/3] Measuring cold model load time...")
    t0 = time.time()
    info = engine.load_model()
    cold_load_time_ms = round((time.time() - t0) * 1000, 2)
    print(f"  Cold Load Time: {cold_load_time_ms:.2f} ms")
    
    # 2. Warm up & test queries
    test_queries = [
        ("Calculate 7 × 4.", 3, "Mathematics"),
        ("Solve 3x + 5 = 20 step-by-step.", 6, "Mathematics"),
        ("Calculate the weight of a body with mass 10 kg on Earth.", 8, "Science (Physics)")
    ]
    
    print("\n[2/3] Running benchmark inference queries...")
    results = []
    
    for q, gr, subj in test_queries:
        print(f"\n  Query (Class {gr} {subj}): '{q}'")
        resp = engine.generate(question=q, grade=gr, subject=subj, max_tokens=120)
        
        m = resp.metrics
        mem_during_mb = process.memory_info().rss / (1024 * 1024)
        
        print(f"    Latency:          {m.latency_ms:.2f} ms")
        print(f"    Prompt Speed:     {m.prompt_tokens_per_second:.1f} tok/s")
        print(f"    Generation Speed: {m.tokens_per_second:.1f} tok/s")
        print(f"    Completion Toks:  {m.completion_tokens}")
        print(f"    Process Memory:   {mem_during_mb:.2f} MB")
        
        results.append({
            "query": q,
            "grade": gr,
            "subject": subj,
            "latency_ms": m.latency_ms,
            "prompt_tok_s": m.prompt_tokens_per_second,
            "gen_tok_s": m.tokens_per_second,
            "completion_tokens": m.completion_tokens,
            "process_memory_mb": round(mem_during_mb, 2)
        })
        
    avg_gen_speed = round(sum(r["gen_tok_s"] for r in results) / len(results), 2)
    avg_prompt_speed = round(sum(r["prompt_tok_s"] for r in results) / len(results), 2)
    avg_latency = round(sum(r["latency_ms"] for r in results) / len(results), 2)
    
    report = {
        "benchmark_environment": "PC / Local Host (Windows 11, Intel Core i5 / NVIDIA RTX 2050, llama.cpp CPU-x64)",
        "model_file": os.path.basename(MODEL_PATH),
        "model_size_mb": round(os.path.getsize(MODEL_PATH) / (1024 * 1024), 2),
        "cold_load_time_ms": cold_load_time_ms,
        "avg_prompt_processing_speed_tok_s": avg_prompt_speed,
        "avg_generation_speed_tok_s": avg_gen_speed,
        "avg_latency_ms": avg_latency,
        "queries_evaluated": len(test_queries),
        "detailed_runs": results,
        "label": "PC Benchmark (Explicitly labeled: NOT Android Performance)"
    }
    
    out_file = r"C:\Rounak\RVSHACK\tests\pc_benchmark_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print("\n" + "=" * 65)
    print("📊 BENCHMARK SUMMARY (PC ONLY)")
    print(f"  Cold Load Time:         {cold_load_time_ms} ms")
    print(f"  Avg Prompt Speed:       {avg_prompt_speed} tok/s")
    print(f"  Avg Generation Speed:   {avg_gen_speed} tok/s")
    print(f"  Avg Latency:            {avg_latency} ms")
    print(f"  Results saved to:       {out_file}")
    print("=" * 65)

if __name__ == "__main__":
    run_pc_benchmark()
