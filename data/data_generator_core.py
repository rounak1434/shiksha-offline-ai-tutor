"""
data_generator_core.py
Core dataset definitions and builders for high-quality STEM tutoring curriculum.
Splits across Train (210), Validation (35), and Test (45).
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def save_jsonl(records, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Saved {len(records)} records to {filepath}")

def make_item(prompt, answer):
    return {
        "messages": [
            {"role": "user", "content": prompt.strip()},
            {"role": "assistant", "content": answer.strip()}
        ]
    }
