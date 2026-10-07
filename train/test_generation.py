import os, sys, torch
os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
# Force UTF-8 output on Windows console
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen3-0.6B"
print(f"Loading tokenizer ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print("Loading model (bf16, CUDA) ...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    device_map="cuda",
)
model.eval()

used = torch.cuda.memory_allocated() / 1024**3
total = torch.cuda.get_device_properties(0).total_memory / 1024**3
print(f"VRAM after load: {used:.2f} / {total:.2f} GB")

question = "Explain Newton's second law to a class 8 student in simple language."
messages = [{"role": "user", "content": question}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False,
)
inputs = tokenizer(text, return_tensors="pt").to("cuda")
print(f"Prompt tokens: {inputs['input_ids'].shape[1]}")
print("Generating ...\n")

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=350,
        do_sample=False,
        temperature=None,
        top_p=None,
        pad_token_id=tokenizer.eos_token_id,
    )

decoded = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

# Write to file to avoid console encoding issues
out_path = r"C:\Rounak\RVSHACK\tests\base_generation_test.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"QUESTION: {question}\n\n")
    f.write(f"BASE MODEL RESPONSE:\n{decoded}\n")
print(f"Response saved to: {out_path}")
print("\n--- RESPONSE PREVIEW (ASCII-safe) ---")
print(decoded.encode("ascii", errors="replace").decode("ascii"))

used2 = torch.cuda.memory_allocated() / 1024**3
print(f"\nVRAM after generation: {used2:.2f} / {total:.2f} GB")
print("STATUS: PASS")
