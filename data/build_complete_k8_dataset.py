"""
build_complete_k8_dataset.py
Generates the complete 2,000-example Class 1–8 curriculum-aligned dataset.
Partitions:
- train.jsonl (1500 records)
- validation.jsonl (200 records)
- test.jsonl (300 records)
"""

import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = r"C:\Rounak\RVSHACK\data"
random.seed(42)

def make_rec(grade, subject, topic, difficulty, qtype, q, a, source="Class 1-8 Curriculum-aligned"):
    prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {q.strip()}"
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
            {"role": "assistant", "content": a.strip()}
        ]
    }

def make_multi(grade, subject, topic, difficulty, turns, source="Class 1-8 Multi-turn Tutoring"):
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
