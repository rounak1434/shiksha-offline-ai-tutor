"""
generate_stem_curriculum.py
Generates the comprehensive STEM Tutor curriculum dataset split into:
- train.jsonl (210 examples)
- validation.jsonl (35 examples)
- test.jsonl (45 examples)

Ensures zero leakage between train and test, strict factual rigor,
complete SI units, step-by-step mathematical scaffolding, and explicit
correction of fundamental student misconceptions.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"C:\Rounak\RVSHACK\data"
os.makedirs(DATA_DIR, exist_ok=True)

# Helper function to create message record
def make_example(user_query: str, tutor_response: str) -> dict:
    return {
        "messages": [
            {"role": "user", "content": user_query.strip()},
            {"role": "assistant", "content": tutor_response.strip()}
        ]
    }

print("Loading curriculum generation module...")
