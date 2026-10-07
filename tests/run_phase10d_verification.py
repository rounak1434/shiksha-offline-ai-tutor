import os
import re
import subprocess
import sys
import json
import gguf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_tutor_q4_k_m.gguf"
LLAMA_CLI = r"C:\Rounak\RVSHACK\llama.cpp\build_bin\llama-cli.exe"

print("=" * 70)
print("1. FILE SIZE")
print("=" * 70)
file_size_bytes = os.path.getsize(MODEL_PATH)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"Exact File Size: {file_size_bytes} bytes ({file_size_mb:.2f} MB)")

print("\n" + "=" * 70)
print("2. GGUF METADATA VERIFICATION")
print("=" * 70)
reader = gguf.GGUFReader(MODEL_PATH)
fields_to_check = [
    "general.architecture",
    "general.name",
    "general.file_type",
    "general.quantization_version",
    "qwen2.context_length",
    "qwen3.context_length",
    "qwen2.embedding_length",
    "qwen3.embedding_length",
    "qwen2.block_count",
    "qwen3.block_count",
    "qwen2.feed_forward_length",
    "qwen3.feed_forward_length",
    "qwen2.attention.head_count",
    "qwen3.attention.head_count",
    "qwen2.attention.head_count_kv",
    "qwen3.attention.head_count_kv",
    "tokenizer.ggml.model",
    "tokenizer.chat_template"
]

metadata_dict = {}
for k, field in reader.fields.items():
    val = field.parts[-1].tolist() if hasattr(field.parts[-1], "tolist") else field.parts[-1]
    if isinstance(val, (bytes, bytearray)):
        try:
            val = val.decode("utf-8")
        except Exception:
            val = str(val)
    metadata_dict[k] = val

for f in fields_to_check:
    if f in metadata_dict:
        val = metadata_dict[f]
        if f == "tokenizer.chat_template":
            print(f"{f}: Present (Length: {len(str(val))} chars)")
            print(f"Chat template snippet: {repr(str(val)[:120])}...")
        else:
            print(f"{f}: {val}")

print(f"Total Tensors Count: {len(reader.tensors)}")

print("\n" + "=" * 70)
print("3. RUNNING LLAMA-CLI INFERENCE TESTS")
print("=" * 70)

TEST_PROMPTS = [
    ("Test 1: Newton's Second Law", "Explain Newton's second law to a class 8 student in simple language."),
    ("Test 2: Math Step-by-Step", "Solve 3x + 7 = 25 step-by-step."),
    ("Test 3: Mass vs Weight", "Explain mass vs weight."),
    ("Test 4: Specific Misconception Test", "A student says: my weight is 50 kg. Is this scientifically correct?")
]

results = []

for title, user_query in TEST_PROMPTS:
    print(f"\n{'='*70}")
    print(f"EXECUTING: {title}")
    print(f"Query: {user_query}")
    print(f"{'='*70}")
    
    # Format with Qwen3 non-thinking prompt structure:
    prompt_str = f"<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", prompt_str,
        "-n", "350",
        "-c", "2048",
        "-t", "4",
        "--temp", "0.0",
        "--no-warmup",
        "--single-turn",
        "--simple-io",
        "--verbose"
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    stdout = proc.stdout
    stderr = proc.stderr
    full_log = stdout + "\n" + stderr
    
    # Extract load time & memory
    load_time_match = re.search(r"load time\s*=\s*([\d\.]+)\s*ms", full_log)
    if not load_time_match:
        load_time_match = re.search(r"total load time\s*=\s*([\d\.]+)\s*ms", full_log)
        
    # Extract prompt eval
    prompt_eval_match = re.search(r"prompt eval time\s*=\s*([\d\.]+)\s*ms\s*/\s*(\d+)\s*tokens.*?([\d\.]+)\s*tokens per second", full_log)
    prompt_summary = re.search(r"Prompt:\s*([\d\.]+)\s*t/s", stdout)
    
    # Extract generation eval
    eval_match = re.search(r"eval time\s*=\s*([\d\.]+)\s*ms\s*/\s*(\d+)\s*runs.*?([\d\.]+)\s*tokens per second", full_log)
    if not eval_match:
        eval_match = re.search(r"eval time\s*=\s*([\d\.]+)\s*ms\s*/\s*(\d+)\s*tokens.*?([\d\.]+)\s*tokens per second", full_log)
    gen_summary = re.search(r"Generation:\s*([\d\.]+)\s*t/s", stdout)
    
    total_time_match = re.search(r"total time\s*=\s*([\d\.]+)\s*ms", full_log)
    
    # Detect CPU/GPU offloading
    is_cpu = "CPU" in full_log or "Host" in full_log
    offload_info = "CPU (0 GPU layers offloaded)"
    if "offloaded" in full_log.lower():
        for line in full_log.splitlines():
            if "offload" in line.lower():
                offload_info = line.strip()
                break
    elif "CPU compute buffer" in full_log:
        buf_match = re.search(r"CPU compute buffer size is\s*([\d\.]+)\s*MiB", full_log)
        offload_info = f"CPU (Host memory, compute buffer: {buf_match.group(1)} MiB)" if buf_match else "CPU"

    # Filter real errors/warnings
    warnings_errors = []
    for line in stderr.splitlines():
        line_l = line.lower()
        if any(err_word in line_l for err_word in ["error:", "failed", "crash", "cuda error", "exception"]):
            warnings_errors.append(line.strip())
            
    # Extract clean answer
    clean_output = stdout
    if "[Start thinking]" in clean_output:
        clean_output = clean_output.split("[Start thinking]")[-1]
    if "[ Prompt:" in clean_output:
        clean_output = clean_output.split("[ Prompt:")[0]
    if "Exiting..." in clean_output:
        clean_output = clean_output.split("Exiting...")[0]
    clean_output = clean_output.strip()

    prompt_tps = prompt_eval_match.group(3) if prompt_eval_match else (prompt_summary.group(1) if prompt_summary else "N/A")
    gen_tps = eval_match.group(3) if eval_match else (gen_summary.group(1) if gen_summary else "N/A")
    load_time_val = load_time_match.group(1) if load_time_match else "N/A"
    
    res_data = {
        "title": title,
        "query": user_query,
        "clean_output": clean_output,
        "load_time_ms": load_time_val,
        "prompt_tps": prompt_tps,
        "gen_tps": gen_tps,
        "offload_info": offload_info,
        "warnings_errors": warnings_errors,
        "has_think_leak": "<think>" in clean_output or "</think>" in clean_output,
        "exit_code": proc.returncode
    }
    
    results.append(res_data)
    
    print(f"Exit code: {proc.returncode}")
    print(f"Load time: {load_time_val} ms")
    print(f"Prompt processing speed: {prompt_tps} t/s")
    print(f"Generation speed: {gen_tps} t/s")
    print(f"Compute mode: {offload_info}")
    print(f"Think tag leak: {res_data['has_think_leak']}")
    print(f"\n--- Model Output ---\n{clean_output}\n")

# Save results
out_json_path = r"C:\Rounak\RVSHACK\tests\phase10d_complete_results.json"
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump({
        "file_size_bytes": file_size_bytes,
        "file_size_mb": file_size_mb,
        "metadata": {k: str(v) for k, v in metadata_dict.items() if any(k.startswith(p) for p in ["general.", "qwen2.", "qwen3.", "tokenizer."])},
        "results": results
    }, f, indent=2)

print(f"\nVerification finished successfully. Results saved to {out_json_path}")
