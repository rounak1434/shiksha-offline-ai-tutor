"""
Phase 10D: Local llama.cpp CLI Test Harness
Tests Q4_K_M GGUF model with official llama-cli.exe on the 3 required prompts.
Extracts load time, prompt eval speed, eval speed, token counts, and coherence.
"""

import subprocess
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LLAMA_CLI = r"C:\Rounak\RVSHACK\llama.cpp\build_bin\llama-cli.exe"
MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_tutor_q4_k_m.gguf"
REPORT_FILE = r"C:\Rounak\RVSHACK\tests\phase10d_llama_cli_results.txt"

PROMPTS = [
    ("Prompt 1: Newton's Second Law", "Explain Newton's second law to a class 8 student in simple language."),
    ("Prompt 2: Math Step-by-Step", "Solve 3x + 7 = 25 step-by-step."),
    ("Prompt 3: Mass vs Weight", "Explain mass vs weight.")
]

def run_test(title, question):
    print(f"\n{'='*60}\nRUNNING: {title}\nQuestion: {question}\n{'='*60}")
    
    # Format with official Qwen3 non-thinking prompt structure:
    # <|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n
    formatted_prompt = f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", formatted_prompt,
        "-n", "300",
        "-c", "2048",
        "-t", "4",
        "--temp", "0.0",
        "--no-warmup"
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    
    stdout = proc.stdout
    stderr = proc.stderr
    full_output = stdout + "\n" + stderr
    
    # Extract metrics from stderr / stdout
    load_time = re.search(r"load time\s*=\s*([\d\.]+)\s*ms", full_output)
    prompt_eval = re.search(r"prompt eval time\s*=\s*([\d\.]+)\s*ms\s*/\s*(\d+)\s*tokens.*?([\d\.]+)\s*tokens per second", full_output)
    eval_speed = re.search(r"eval time\s*=\s*([\d\.]+)\s*ms\s*/\s*(\d+)\s*runs.*?([\d\.]+)\s*tokens per second", full_output)
    
    print("--- GENERATED OUTPUT ---")
    # Clean output of prompt echo
    ans = stdout
    if "<|im_start|>assistant" in ans:
        ans = ans.split("<|im_start|>assistant")[-1]
    if "</think>" in ans:
        ans = ans.split("</think>")[-1].strip()
    
    print(ans)
    print("--- TIMING STATS ---")
    if load_time:
        print(f"Model Load Time: {load_time.group(1)} ms")
    if prompt_eval:
        print(f"Prompt Eval Speed: {prompt_eval.group(3)} tokens/sec ({prompt_eval.group(2)} tokens in {prompt_eval.group(1)} ms)")
    if eval_speed:
        print(f"Generation Speed: {eval_speed.group(3)} tokens/sec ({eval_speed.group(2)} tokens in {eval_speed.group(1)} ms)")

    return {
        "title": title,
        "question": question,
        "answer": ans,
        "load_time_ms": load_time.group(1) if load_time else "N/A",
        "prompt_tokens": prompt_eval.group(2) if prompt_eval else "N/A",
        "prompt_tps": prompt_eval.group(3) if prompt_eval else "N/A",
        "gen_tokens": eval_speed.group(2) if eval_speed else "N/A",
        "gen_tps": eval_speed.group(3) if eval_speed else "N/A",
        "has_think_leak": "<think>" in ans or "</think>" in ans,
        "exit_code": proc.returncode
    }

def main():
    results = []
    for title, q in PROMPTS:
        res = run_test(title, q)
        results.append(res)
    
    file_size_mb = os.path.getsize(MODEL_PATH) / (1024*1024)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("PHASE 10D: LOCAL LLAMA.CPP TEST RESULTS\n")
        f.write("="*60 + "\n\n")
        f.write(f"Model Path: {MODEL_PATH}\n")
        f.write(f"Actual File Size: {file_size_mb:.2f} MB\n")
        f.write(f"Context Size: 2048\n\n")
        for r in results:
            f.write(f"### {r['title']}\n")
            f.write(f"Question: {r['question']}\n")
            f.write(f"Model Load Time: {r['load_time_ms']} ms\n")
            f.write(f"Prompt Processing: {r['prompt_tps']} t/s ({r['prompt_tokens']} tokens)\n")
            f.write(f"Generation Speed: {r['gen_tps']} t/s ({r['gen_tokens']} tokens)\n")
            f.write(f"Think Tag Leaked: {r['has_think_leak']}\n\n")
            f.write("Answer:\n" + r['answer'] + "\n\n" + "-"*50 + "\n\n")
    
    print(f"\nAll tests finished. Full report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
