"""
generate_full_k8_dataset.py
Orchestrates the creation of the complete 2,000-record Class 1–8 dataset:
- train.jsonl (1500 records)
- validation.jsonl (200 records)
- test.jsonl (300 records)

Enforces:
1. Student grade in prompt header
2. Exact grade distribution (78% in Class 5–8)
3. Subject balance (Math ~760, Science ~880, CS ~360)
4. Multi-turn tutoring (~12% in train)
5. Scope / refusal handling
6. Deterministic factual verification
7. Zero test-train leakage
"""

import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = r"C:\Rounak\RVSHACK\data"

# Seed for reproducibility
random.seed(42)

def make_record(grade, subject, topic, difficulty, qtype, user_q, tutor_ans, source="NCERT Class 1-8 Curriculum-aligned"):
    prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {user_q.strip()}"
    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": qtype,
            "curriculum_source": source
        },
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": tutor_ans.strip()}
        ]
    }

def make_multiturn(grade, subject, topic, difficulty, turns, source="NCERT Class 1-8 Multi-turn"):
    messages = []
    for idx, (role, text) in enumerate(turns):
        if idx == 0 and role == "user":
            content = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {text.strip()}"
        else:
            content = text.strip()
        messages.append({"role": role, "content": content})
    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": "multi_turn_tutoring",
            "curriculum_source": source
        },
        "messages": messages
    }

print("Initializing generation pools...")
