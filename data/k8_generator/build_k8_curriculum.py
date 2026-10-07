"""
build_k8_curriculum.py
Generates the complete 2,000-example Class 1–8 curriculum-aligned dataset.
"""

import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = r"C:\Rounak\RVSHACK\data"
random.seed(42)

def record(grade, subject, topic, difficulty, qtype, q, a, source="NCERT/State Board Aligned"):
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

def multiturn(grade, subject, topic, difficulty, turns, source="NCERT Multi-turn Tutoring"):
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
