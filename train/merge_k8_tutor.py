"""
merge_k8_tutor.py
Phase 1: Merges final K8 QLoRA adapter weights back into base Qwen3-0.6B model.
Base Model: Qwen/Qwen3-0.6B
Adapter: C:\\Rounak\\RVSHACK\\output\\qwen3_k8_tutor_lora
Destination: C:\\Rounak\\RVSHACK\\output\\qwen3_k8_tutor_merged
Preserves baseline artifacts intact.
"""

import os
import sys
import time
import json
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL_ID = "Qwen/Qwen3-0.6B"
ADAPTER_PATH = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_lora"
MERGED_OUTPUT_PATH = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_merged"

def merge_model():
    print("=" * 65)
    print("🔄 PHASE 1: MERGING K-8 LORA ADAPTER INTO BASE MODEL")
    print("=" * 65)
    start_time = time.time()

    assert os.path.exists(ADAPTER_PATH), f"Adapter path not found: {ADAPTER_PATH}"
    print(f"Base model: {BASE_MODEL_ID}")
    print(f"Adapter:    {ADAPTER_PATH}")
    print(f"Target:     {MERGED_OUTPUT_PATH}")

    # 1. Load tokenizer
    print("\n[1/4] Loading tokenizer from adapter directory...")
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. Load base model in bfloat16 on CPU
    print(f"\n[2/4] Loading base model ({BASE_MODEL_ID}) in bfloat16 on CPU...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
        trust_remote_code=True,
    )

    # 3. Attach LoRA adapter and merge
    print(f"\n[3/4] Attaching final K-8 LoRA adapter and fusing weights...")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    merged_model = model.merge_and_unload()

    # 4. Save merged model
    print(f"\n[4/4] Saving fused standalone model to {MERGED_OUTPUT_PATH}...")
    os.makedirs(MERGED_OUTPUT_PATH, exist_ok=True)
    merged_model.save_pretrained(MERGED_OUTPUT_PATH, safe_serialization=True)
    tokenizer.save_pretrained(MERGED_OUTPUT_PATH)

    elapsed = time.time() - start_time
    total_size = sum(
        os.path.getsize(os.path.join(MERGED_OUTPUT_PATH, f))
        for f in os.listdir(MERGED_OUTPUT_PATH)
        if os.path.isfile(os.path.join(MERGED_OUTPUT_PATH, f))
    )

    metrics = {
        "base_model": BASE_MODEL_ID,
        "adapter_path": ADAPTER_PATH,
        "merged_path": MERGED_OUTPUT_PATH,
        "merge_time_seconds": round(elapsed, 2),
        "total_artifact_size_bytes": total_size,
        "total_artifact_size_mb": round(total_size / (1024 * 1024), 2),
        "status": "PASS"
    }

    metrics_file = os.path.join(MERGED_OUTPUT_PATH, "merge_metrics.json")
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("\n" + "=" * 65)
    print("✅ MERGE COMPLETED SUCCESSFULLY!")
    print(f"Time taken:   {elapsed:.2f} s")
    print(f"Artifact size: {total_size / (1024 * 1024):.2f} MB")
    print(f"Saved metrics to: {metrics_file}")
    print("=" * 65)

if __name__ == "__main__":
    merge_model()
