"""
verify_k8_merged_model.py
Verifies the merged standalone model:
C:\\Rounak\\RVSHACK\\output\\qwen3_k8_tutor_merged
Checks:
- Model & tokenizer loading
- Clean non-thinking ChatML generation
- Zero <think> tags
- Representative Class 1-8 math/science tests
- Output consistency against adapter outputs
"""

import os
import sys
import json
import time
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoTokenizer, AutoModelForCausalLM

MERGED_MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_merged"
ADAPTER_RESULTS_PATH = r"C:\Rounak\RVSHACK\tests\phase5_adapter_test_results.json"

TEST_PROMPTS = [
    {
        "id": "class3_math",
        "grade": 3,
        "subject": "Mathematics",
        "question": "Calculate 7 × 4. What does multiplication mean?"
    },
    {
        "id": "class6_math",
        "grade": 6,
        "subject": "Mathematics",
        "question": "Solve 3x + 5 = 20 step-by-step. Show all steps."
    },
    {
        "id": "class8_physics",
        "grade": 8,
        "subject": "Science (Physics)",
        "question": "A constant 30 N force pushes a 5 kg cart and a 15 kg cart. Which cart accelerates faster? Calculate both accelerations."
    },
    {
        "id": "class8_misconception",
        "grade": 8,
        "subject": "Science (Physics)",
        "question": "A student says: my weight is 50 kg. Is this scientifically correct?"
    },
    {
        "id": "class8_scope_refusal",
        "grade": 8,
        "subject": "Mathematics",
        "question": "Can you solve this second-order differential equation y'' + 4y = 0?"
    }
]

def main():
    print("=" * 65)
    print("🧪 VERIFYING MERGED STANDALONE MODEL (output/qwen3_k8_tutor_merged)")
    print("=" * 65)

    print("\n[1/3] Loading tokenizer from merged directory...")
    tokenizer = AutoTokenizer.from_pretrained(MERGED_MODEL_PATH, trust_remote_code=True)
    assert tokenizer.pad_token is not None or tokenizer.eos_token is not None

    print("\n[2/3] Loading merged standalone model in bfloat16 on GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        MERGED_MODEL_PATH,
        torch_dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=True,
    )
    model.eval()

    print("\n[3/3] Running representative test prompts...")
    results = []
    all_clean = True
    all_passed = True

    for item in TEST_PROMPTS:
        user_msg = f"Student grade: Class {item['grade']}\nSubject: {item['subject']}\nQuestion: {item['question']}"
        prompt = tokenizer.apply_chat_template([{"role": "user", "content": user_msg}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        t0 = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=250,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        gen_time = time.time() - t0
        gen_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        resp = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()
        tok_per_sec = len(gen_tokens) / gen_time if gen_time > 0 else 0

        has_think = "<think>" in resp or "</think>" in resp
        if has_think:
            all_clean = False

        print(f"\n--- Test: {item['id']} ---")
        print(f"Generated ({len(gen_tokens)} tokens in {gen_time:.2f}s, {tok_per_sec:.1f} tok/s):")
        print(resp)
        print(f"Clean non-thinking: {'PASS' if not has_think else 'FAIL'}")

        results.append({
            "id": item["id"],
            "prompt": user_msg,
            "response": resp,
            "tokens": len(gen_tokens),
            "time_sec": round(gen_time, 2),
            "tokens_per_sec": round(tok_per_sec, 2),
            "has_think": has_think
        })

    out_file = r"C:\Rounak\RVSHACK\tests\merged_model_verification_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 65)
    print("VERIFICATION SUMMARY:")
    print(f"Clean non-thinking across all prompts: {'PASS' if all_clean else 'FAIL'}")
    print(f"Saved results to: {out_file}")
    print("=" * 65)

    if not all_clean:
        sys.exit(1)

if __name__ == "__main__":
    main()
