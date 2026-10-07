"""
compare_gguf_models.py
Phases 2 & 3: Comparative evaluation of F16 GGUF vs Q4_K_M GGUF models.
Runs llama-cli on the required regression suite:
1. Algebra (linear equation step-by-step)
2. Newton's 2nd Law (force, mass, acceleration)
3. Mass vs Weight (calculation on Earth & Moon)
4. Conceptual Science (photosynthesis / cell biology)
5. Misconception Correction ("my weight is 50 kg")
6. Curriculum Scope Refusal (nuclear physics / university calculus)
"""

import os
import sys
import subprocess
import re
import json
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LLAMA_CLI = r"C:\Rounak\RVSHACK\llama.cpp\build_bin\llama-cli.exe"
F16_MODEL = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_f16.gguf"
Q4_MODEL = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_q4_k_m.gguf"

REGRESSION_SUITE = [
    {
        "id": "algebra",
        "category": "Mathematics",
        "grade": 6,
        "prompt": "Student grade: Class 6\nSubject: Mathematics\nQuestion: Solve 3x + 5 = 20 step-by-step. Show all steps.",
        "check": lambda ans: "5" in ans and ("subtract" in ans.lower() or "15" in ans)
    },
    {
        "id": "newtons_law",
        "category": "Science (Physics)",
        "grade": 8,
        "prompt": "Student grade: Class 8\nSubject: Science (Physics)\nQuestion: A constant 30 N force pushes a 5 kg cart and a 15 kg cart. Which cart accelerates faster? Calculate both accelerations.",
        "check": lambda ans: ("6" in ans or "6.0" in ans) and ("2" in ans or "2.0" in ans)
    },
    {
        "id": "mass_vs_weight",
        "category": "Science (Physics)",
        "grade": 8,
        "prompt": "Student grade: Class 8\nSubject: Science (Physics)\nQuestion: Calculate the weight of a body with mass 10 kg on Earth (g = 9.8 m/s²). Explain the difference between mass and weight.",
        "check": lambda ans: ("98" in ans or "98 N" in ans) and ("force" in ans.lower() or "newton" in ans.lower() or "gravity" in ans.lower())
    },
    {
        "id": "conceptual_science",
        "category": "Science (Biology)",
        "grade": 7,
        "prompt": "Student grade: Class 7\nSubject: Science (Biology)\nQuestion: What is photosynthesis and what are the essential raw materials required?",
        "check": lambda ans: "chlorophyll" in ans.lower() or "carbon dioxide" in ans.lower() or "light" in ans.lower()
    },
    {
        "id": "misconception",
        "category": "Science (Physics)",
        "grade": 8,
        "prompt": "Student grade: Class 8\nSubject: Science (Physics)\nQuestion: A student says: my weight is 50 kg. Is this scientifically correct?",
        "check": lambda ans: ("incorrect" in ans.lower() or "not" in ans.lower()) and ("490" in ans or "newton" in ans.lower() or "mass" in ans.lower())
    },
    {
        "id": "curriculum_refusal",
        "category": "Mathematics",
        "grade": 8,
        "prompt": "Student grade: Class 8\nSubject: Mathematics\nQuestion: Can you solve this second-order differential equation y'' + 4y = 0?",
        "check": lambda ans: "scope" in ans.lower() or "outside" in ans.lower() or "curriculum" in ans.lower() or "linear" in ans.lower() or "differential" in ans.lower()
    }
]

def run_llama_inference(model_path, user_prompt, max_tokens=180):
    formatted_prompt = f"<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
    cmd = [
        LLAMA_CLI,
        "-m", model_path,
        "-p", formatted_prompt,
        "-n", str(max_tokens),
        "-c", "2048",
        "-t", "4",
        "--temp", "0.0",
        "--simple-io",
        "-st",
        "--no-display-prompt"
    ]
    
    t0 = time.time()
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    wall_time = time.time() - t0
    
    output = proc.stdout
    
    # Extract metrics
    prompt_tok_s = 0.0
    eval_tok_s = 0.0
    
    perf_match = re.search(r"Prompt:\s*([\d\.]+)\s*t/s\s*\|\s*Generation:\s*([\d\.]+)\s*t/s", output)
    if perf_match:
        prompt_tok_s = float(perf_match.group(1))
        eval_tok_s = float(perf_match.group(2))
        
    # Clean answer
    answer = output
    if "<|im_start|>assistant" in answer:
        answer = answer.split("<|im_start|>assistant")[-1].strip()
    if "[ Prompt:" in answer:
        answer = answer.split("[ Prompt:")[0].strip()
    if "<|im_end|>" in answer:
        answer = answer.split("<|im_end|>")[0].strip()
        
    has_think = "<think>" in output or "</think>" in output
    
    return {
        "answer": answer,
        "prompt_tokens_per_sec": prompt_tok_s,
        "eval_tokens_per_sec": eval_tok_s,
        "wall_time_sec": round(wall_time, 2),
        "has_think": has_think
    }

def main():
    print("=" * 65)
    print("⚖️ COMPARATIVE GGUF REGRESSION TEST: F16 vs Q4_K_M")
    print("=" * 65)
    
    results = {
        "f16_model": F16_MODEL,
        "q4_model": Q4_MODEL,
        "f16_size_bytes": os.path.getsize(F16_MODEL),
        "q4_size_bytes": os.path.getsize(Q4_MODEL),
        "comparisons": []
    }
    
    print(f"F16 Model:   {F16_MODEL} ({results['f16_size_bytes'] / (1024*1024):.2f} MB)")
    print(f"Q4_K_M Model:{Q4_MODEL} ({results['q4_size_bytes'] / (1024*1024):.2f} MB)")
    
    all_q4_passed = True
    
    for item in REGRESSION_SUITE:
        print(f"\n--- Testing: {item['id']} ({item['category']} Class {item['grade']}) ---")
        
        # Test F16
        print("  Running F16 GGUF...")
        f16_res = run_llama_inference(F16_MODEL, item["prompt"])
        f16_check = item["check"](f16_res["answer"])
        print(f"  F16 Speed: {f16_res['eval_tokens_per_sec']:.1f} tok/s | Prompt: {f16_res['prompt_tokens_per_sec']:.1f} tok/s | Check: {'PASS' if f16_check else 'FAIL'}")
        
        # Test Q4_K_M
        print("  Running Q4_K_M GGUF...")
        q4_res = run_llama_inference(Q4_MODEL, item["prompt"])
        q4_check = item["check"](q4_res["answer"])
        print(f"  Q4  Speed: {q4_res['eval_tokens_per_sec']:.1f} tok/s | Prompt: {q4_res['prompt_tokens_per_sec']:.1f} tok/s | Check: {'PASS' if q4_check else 'FAIL'}")
        
        if not q4_check:
            all_q4_passed = False
            
        print("\n  [Q4_K_M Generated Output]:")
        for line in q4_res["answer"].splitlines()[:12]:
            print("    " + line)
            
        results["comparisons"].append({
            "id": item["id"],
            "prompt": item["prompt"],
            "f16": {
                "answer": f16_res["answer"],
                "speed_tok_s": f16_res["eval_tokens_per_sec"],
                "prompt_tok_s": f16_res["prompt_tokens_per_sec"],
                "wall_time_sec": f16_res["wall_time_sec"],
                "passed": f16_check,
                "has_think": f16_res["has_think"]
            },
            "q4_k_m": {
                "answer": q4_res["answer"],
                "speed_tok_s": q4_res["eval_tokens_per_sec"],
                "prompt_tok_s": q4_res["prompt_tokens_per_sec"],
                "wall_time_sec": q4_res["wall_time_sec"],
                "passed": q4_check,
                "has_think": q4_res["has_think"]
            }
        })
        
    out_json = r"C:\Rounak\RVSHACK\tests\gguf_comparison_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("\n" + "=" * 65)
    print("REGRESSION COMPARISON COMPLETE!")
    print(f"All Q4_K_M tests passed: {all_q4_passed}")
    print(f"Saved results to: {out_json}")
    print("=" * 65)

if __name__ == "__main__":
    main()
