"""
evaluate_heldout_test.py
Phase 6 Held-Out Evaluation Script:
Evaluates all 300 held-out examples from:
C:\\Rounak\\RVSHACK\\data\\test.jsonl
Compares:
1. Baseline Model (Qwen/Qwen3-0.6B + baseline adapter)
2. Final K8 Tutor Model (Qwen/Qwen3-0.6B + qwen3_k8_tutor_lora)
Runs deterministic STEM checks, formatting checks, and generates tests/final_model_evaluation.md
"""

import os
import sys
import json
import re
import time
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from stem_factual_checker import STEMFactualChecker

def run_evaluation():
    print("=" * 65)
    print("📊 PHASE 6 — HELD-OUT TEST EVALUATION (300 RECORDS)")
    print("=" * 65)
    
    test_path = r"C:\Rounak\RVSHACK\data\test.jsonl"
    with open(test_path, encoding="utf-8") as f:
        test_records = [json.loads(line) for line in f]
        
    print(f"Loaded {len(test_records)} held-out test examples.")
    assert len(test_records) == 300, f"Expected 300 test records, found {len(test_records)}"
    
    base_model_id = "Qwen/Qwen3-0.6B"
    final_adapter_dir = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_lora"
    baseline_adapter_dir = r"C:\Rounak\RVSHACK\output\qwen3_offline_tutor_lora"
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(final_adapter_dir, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    # -------------------------------------------------------------
    # Evaluate Final Model on all 300 test examples
    # -------------------------------------------------------------
    print("\n[1/3] Loading Base Model + Final K8 Tutor LoRA Adapter...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="cuda",
        trust_remote_code=True,
    )
    final_model = PeftModel.from_pretrained(base_model, final_adapter_dir)
    final_model.eval()
    
    print("\n[2/3] Generating responses for all 300 test records with Final Model...")
    final_results = []
    start_t = time.time()
    
    for idx, rec in enumerate(test_records):
        messages = rec["messages"]
        user_msg = messages[0]["content"]
        ground_truth = messages[-1]["content"]
        meta = rec["metadata"]
        
        prompt = tokenizer.apply_chat_template([{"role": "user", "content": user_msg}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = final_model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
            
        gen_ids = outputs[0][inputs["input_ids"].shape[1]:]
        resp = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()
        
        final_results.append({
            "idx": idx,
            "metadata": meta,
            "user_prompt": user_msg,
            "ground_truth": ground_truth,
            "final_response": resp
        })
        
        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1} / {len(test_records)} examples ({time.time() - start_t:.1f} s)...")
            
    print(f"Final Model inference completed in {time.time() - start_t:.1f} seconds.")
    
    # -------------------------------------------------------------
    # Evaluate Baseline Model on stratified key scenarios
    # -------------------------------------------------------------
    print("\n[3/3] Evaluating Baseline Model on comparative test scenarios...")
    # Unload final adapter and load baseline adapter
    del final_model
    torch.cuda.empty_cache()
    
    baseline_model = PeftModel.from_pretrained(base_model, baseline_adapter_dir)
    baseline_model.eval()
    
    # Select key comparative questions from the test set across Physics, Math, Chemistry, Biology, CS
    comp_indices = [
        # Newton's 2nd law / Force
        next(i for i, r in enumerate(test_records) if "force" in r["messages"][0]["content"].lower() and "mass" in r["messages"][0]["content"].lower()),
        # Mass vs weight
        next(i for i, r in enumerate(test_records) if "weight" in r["messages"][0]["content"].lower() and "earth" in r["messages"][0]["content"].lower()),
        # Linear equation
        next(i for i, r in enumerate(test_records) if "equation" in r["messages"][0]["content"].lower() or "solve" in r["messages"][0]["content"].lower()),
        # Plant classification
        next(i for i, r in enumerate(test_records) if "herb" in r["messages"][0]["content"].lower() or "plant" in r["messages"][0]["content"].lower()),
        # Rust prevention
        next(i for i, r in enumerate(test_records) if "rust" in r["messages"][0]["content"].lower() or "iron" in r["messages"][0]["content"].lower()),
        # Computer Science
        next(i for i, r in enumerate(test_records) if "keyboard" in r["messages"][0]["content"].lower() or "computer" in r["messages"][0]["content"].lower()),
        # Scope refusal
        next(i for i, r in enumerate(test_records) if r["metadata"]["question_type"] == "scope_refusal")
    ]
    
    baseline_comparisons = []
    for idx in comp_indices:
        rec = test_records[idx]
        user_msg = rec["messages"][0]["content"]
        prompt = tokenizer.apply_chat_template([{"role": "user", "content": user_msg}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = baseline_model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        gen_ids = outputs[0][inputs["input_ids"].shape[1]:]
        resp_base = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()
        
        baseline_comparisons.append({
            "idx": idx,
            "topic": rec["metadata"]["topic"],
            "grade": rec["metadata"]["grade"],
            "subject": rec["metadata"]["subject"],
            "prompt": user_msg,
            "baseline_response": resp_base,
            "final_response": final_results[idx]["final_response"],
            "ground_truth": rec["messages"][-1]["content"]
        })
        
    # -------------------------------------------------------------
    # Run Automated Quality Checks across all 300 Final Model outputs
    # -------------------------------------------------------------
    print("\nRunning automated validation checks across all 300 test responses...")
    
    newton_checks = {"total": 0, "pass": 0}
    mass_weight_checks = {"total": 0, "pass": 0}
    emoji_fails = 0
    think_tag_fails = 0
    structured_headers_count = 0
    scope_refusals = {"total": 0, "pass": 0}
    
    for r in final_results:
        resp = r["final_response"]
        prompt = r["user_prompt"].lower()
        meta = r["metadata"]
        
        # Check emojis
        if re.search(r"[\U00010000-\U0010ffff\u2600-\u27ff]", resp):
            emoji_fails += 1
            
        # Check think tags
        if "<think>" in resp or "</think>" in resp:
            think_tag_fails += 1
            
        # Check structure headers
        if any(h in resp for h in ["Given:", "Definition:", "Required:", "Formula:", "Calculation:", "Key Principle:"]):
            structured_headers_count += 1
            
        # Newton check
        if ("force" in prompt and "accelerat" in prompt) or "f = ma" in resp.lower():
            newton_checks["total"] += 1
            chk = STEMFactualChecker.check_newton_second_law(resp)
            if chk["passed"]:
                newton_checks["pass"] += 1
                
        # Mass vs weight check
        if "mass" in prompt and "weight" in prompt:
            mass_weight_checks["total"] += 1
            chk = STEMFactualChecker.check_mass_vs_weight(resp)
            if chk["passed"]:
                mass_weight_checks["pass"] += 1
                
        # Scope refusal check
        if meta["question_type"] == "scope_refusal":
            scope_refusals["total"] += 1
            if "outside" in resp.lower() or "scope" in resp.lower() or "curriculum" in resp.lower():
                scope_refusals["pass"] += 1

    summary_metrics = {
        "total_test_records": len(test_records),
        "emoji_free_rate": f"{(len(test_records) - emoji_fails) / len(test_records) * 100:.1f}%",
        "clean_non_thinking_rate": f"{(len(test_records) - think_tag_fails) / len(test_records) * 100:.1f}%",
        "structured_pedagogical_rate": f"{structured_headers_count / len(test_records) * 100:.1f}%",
        "newton_accuracy": f"{newton_checks['pass']} / {newton_checks['total']}" if newton_checks['total'] > 0 else "N/A",
        "mass_vs_weight_accuracy": f"{mass_weight_checks['pass']} / {mass_weight_checks['total']}" if mass_weight_checks['total'] > 0 else "N/A",
        "scope_refusal_adherence": f"{scope_refusals['pass']} / {scope_refusals['total']}" if scope_refusals['total'] > 0 else "N/A"
    }
    
    print("\n--- TEST EVALUATION SUMMARY ---")
    for k, v in summary_metrics.items():
        print(f"  {k}: {v}")
        
    # Save test results and comparative data
    eval_data = {
        "summary": summary_metrics,
        "baseline_comparisons": baseline_comparisons,
        "final_results": final_results
    }
    with open(r"C:\Rounak\RVSHACK\tests\final_heldout_eval_data.json", "w", encoding="utf-8") as f:
        json.dump(eval_data, f, indent=2, ensure_ascii=False)
        
    print(f"\nSaved evaluation data to: C:\\Rounak\\RVSHACK\\tests\\final_heldout_eval_data.json")

if __name__ == "__main__":
    run_evaluation()
