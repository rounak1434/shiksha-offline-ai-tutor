"""
Offline AI Tutor — Comparative Evaluation Script
Compares Base Qwen3-0.6B vs QLoRA Fine-Tuned Tutor Model
"""

import os
import sys
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

MODEL_ID = "Qwen/Qwen3-0.6B"
ADAPTER_PATH = r"C:\Rounak\RVSHACK\output\qwen3_offline_tutor_lora"
REPORT_PATH = r"C:\Rounak\RVSHACK\tests\evaluation_report.md"

TEST_QUESTIONS = [
    "What is the difference between mass and weight?",
    "Explain Newton's second law to a class 8 student in simple language.",
    "A student says 'my weight is 50 kg'. Is this scientifically correct? Explain.",
    "What is the difference between speed and velocity?",
    "Why does an ice cube float on water?",
]

def generate_response(model, tokenizer, prompt):
    messages = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    response = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return response.strip()

def main():
    print("=" * 60)
    print("🔍 OFFLINE AI TUTOR — EVALUATION & COMPARISON")
    print("=" * 60)

    print("\n[1/4] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

    print("\n[2/4] Loading base model (bf16, CUDA)...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=True,
    )
    base_model.eval()

    print("\n[3/4] Generating responses from BASE MODEL...")
    base_results = {}
    for q in TEST_QUESTIONS:
        print(f"  Generating base response for: {q[:45]}...")
        base_results[q] = generate_response(base_model, tokenizer, q)

    print("\n[4/4] Attaching LoRA adapter and generating FINE-TUNED responses...")
    ft_model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    ft_model.eval()

    ft_results = {}
    for q in TEST_QUESTIONS:
        print(f"  Generating fine-tuned response for: {q[:45]}...")
        ft_results[q] = generate_response(ft_model, tokenizer, q)

    # Generate Markdown Report
    print(f"\nWriting report to {REPORT_PATH}...")
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🎓 Offline AI Tutor — Evaluation Report\n\n")
        f.write("Side-by-side comparison between **Base Qwen3-0.6B** and **QLoRA Fine-Tuned Tutor**.\n\n")
        
        for i, q in enumerate(TEST_QUESTIONS, 1):
            f.write(f"## Test Case {i}: {q}\n\n")
            f.write("### 🤖 Base Model (Qwen3-0.6B)\n\n")
            f.write(f"{base_results[q]}\n\n")
            f.write("### 🎓 Fine-Tuned Tutor (QLoRA)\n\n")
            f.write(f"{ft_results[q]}\n\n")
            f.write("---\n\n")

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE!")
    print(f"Report saved to: {REPORT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
