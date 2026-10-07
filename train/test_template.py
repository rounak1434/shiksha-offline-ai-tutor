import json
import sys
from transformers import AutoTokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B", trust_remote_code=True)
clean_template = (
    "{%- for message in messages %}"
    "{{- '<|im_start|>' + message['role'] + '\n' + message['content'].strip() + '<|im_end|>\n' }}"
    "{%- endfor %}"
    "{%- if add_generation_prompt %}"
    "{{- '<|im_start|>assistant\n' }}"
    "{%- endif %}"
)
tokenizer.chat_template = clean_template

with open(r"C:\Rounak\RVSHACK\data\train.jsonl", encoding="utf-8") as f:
    sample = json.loads(f.readline())

formatted = tokenizer.apply_chat_template(sample["messages"], tokenize=False)
print("--- CLEAN NON-THINKING CHATML ---")
print(formatted[:400])
print("Contains <think>?:", "<think>" in formatted)
