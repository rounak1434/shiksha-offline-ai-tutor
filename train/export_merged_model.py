"""
Offline AI Tutor — Model Merge Script
Merges QLoRA adapter weights back into base Qwen3-0.6B model
Output is saved in Hugging Face 16-bit format, ready for GGUF conversion via llama.cpp
"""

import os
import sys
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL_ID = "Qwen/Qwen3-0.6B"
ADAPTER_PATH = r"C:\Rounak\RVSHACK\output\qwen3_offline_tutor_lora"
MERGED_OUTPUT_PATH = r"C:\Rounak\RVSHACK\output\qwen3_tutor_merged"

def main():
    print("=" * 60)
    print("🔄 OFFLINE AI TUTOR — MERGE LORA ADAPTER")
    print("=" * 60)

    print(f"\n[1/4] Loading tokenizer from {ADAPTER_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH, trust_remote_code=True)

    print(f"\n[2/4] Loading base model ({BASE_MODEL_ID}) in bfloat16...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="cpu",  # Use CPU to avoid GPU VRAM peak during merge
        trust_remote_code=True,
    )

    print(f"\n[3/4] Attaching LoRA adapter and fusing weights...")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    merged_model = model.merge_and_unload()

    print(f"\n[4/4] Saving fused standalone model to {MERGED_OUTPUT_PATH}...")
    os.makedirs(MERGED_OUTPUT_PATH, exist_ok=True)
    merged_model.save_pretrained(MERGED_OUTPUT_PATH, safe_serialization=True)
    tokenizer.save_pretrained(MERGED_OUTPUT_PATH)

    print("\n" + "=" * 60)
    print("FUSION COMPLETE!")
    print(f"Stand-alone model saved at: {MERGED_OUTPUT_PATH}")
    print("Ready for llama.cpp GGUF conversion!")
    print("=" * 60)

if __name__ == "__main__":
    main()
