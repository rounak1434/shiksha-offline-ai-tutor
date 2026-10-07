"""
generate_curriculum_datasets.py
Generates the complete 290-example STEM dataset:
- train.jsonl (210 examples)
- validation.jsonl (35 examples)
- test.jsonl (45 examples)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"C:\Rounak\RVSHACK\data"

def make_record(prompt, response):
    return {
        "messages": [
            {"role": "user", "content": prompt.strip()},
            {"role": "assistant", "content": response.strip()}
        ]
    }

# We will build train_records (210), val_records (35), and test_records (45).
