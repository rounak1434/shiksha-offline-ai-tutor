"""
Phase 10A: Verify Merged Model
Directly loads C:\Rounak\RVSHACK\output\qwen3_tutor_merged using Transformers,
tests chat template, non-thinking mode generation, and records exact outputs.
"""

import os
import sys
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_tutor_merged"

TEST_PROMPTS = [
    "Explain Newton's second law to a class 8 student in simple language.",
    "Solve 3x + 7 = 25 step-by-step.",
    "Explain mass vs weight."
]

def main():
    print("=" * 60)
    print("PHASE 10A: VERIFYING MERGED MODEL")
    print("=" * 60)

    print(f"\n1. Loading tokenizer from {MODEL_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    print("Tokenizer loaded. Vocab size:", len(tokenizer))
    print("Chat template present:", bool(tokenizer.chat_template))

    print(f"\n2. Loading merged model from {MODEL_PATH} (bfloat16 on CUDA)...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=True
    )
    model.eval()
    print("Model loaded successfully!")
    print(f"Allocated VRAM: {torch.cuda.memory_allocated() / (1024**3):.2f} GB")

    results = []
    print("\n3. Testing 3 educational prompts (non-thinking mode enabled)...")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"\n--- [Prompt {i}] {prompt} ---")
        messages = [{"role": "user", "content": prompt}]
        # Testing non-thinking mode behavior
        try:
            formatted_prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False
            )
            thinking_flag_used = True
        except TypeError:
            # Fallback if enable_thinking argument is not supported
            formatted_prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            thinking_flag_used = False

        inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
        prompt_len = inputs["input_ids"].shape[1]

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        gen_tokens = outputs[0][prompt_len:]
        decoded = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

        print(f"Prompt tokens: {prompt_len}, Generated tokens: {len(gen_tokens)}")
        print(f"Thinking flag used in template: {thinking_flag_used}")
        print("Response:\n" + decoded)

        # Check for unexpected thinking trace leakage
        has_thinking_tag = "<think>" in decoded or "</think>" in decoded
        print(f"Contains <think> tag: {has_thinking_tag}")

        results.append({
            "prompt": prompt,
            "response": decoded,
            "has_thinking_tag": has_thinking_tag,
            "tokens": len(gen_tokens)
        })

    out_file = r"C:\Rounak\RVSHACK\tests\phase10a_merged_verification.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("PHASE 10A: MERGED MODEL VERIFICATION RESULTS\n")
        f.write("=" * 60 + "\n\n")
        for i, res in enumerate(results, 1):
            f.write(f"PROMPT {i}: {res['prompt']}\n")
            f.write(f"GENERATED TOKENS: {res['tokens']}\n")
            f.write(f"HAS THINK TAG: {res['has_thinking_tag']}\n")
            f.write("RESPONSE:\n" + res["response"] + "\n\n" + "-" * 50 + "\n\n")

    print(f"\nAll 3 prompts completed. Detailed log saved to: {out_file}")
    all_ok = all(len(r["response"]) > 20 for r in results)
    if all_ok:
        print("\nSTATUS: PASS - Merged model generation verified successfully!")
    else:
        print("\nSTATUS: FAIL - Empty or corrupted generation detected!")

if __name__ == "__main__":
    main()
