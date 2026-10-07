"""
k8_builder.py
Constructs the complete 2,000-example Class 1–8 dataset.
"""

import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = r"C:\Rounak\RVSHACK\data"
random.seed(42)

def make_entry(grade, subject, topic, difficulty, qtype, q, a, source="Class 1-8 Curriculum-aligned"):
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

def make_multiturn(grade, subject, topic, difficulty, turns, source="Class 1-8 Multi-turn Tutoring"):
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
