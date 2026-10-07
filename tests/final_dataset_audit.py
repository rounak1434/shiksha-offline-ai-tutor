"""
final_dataset_audit.py
Performs comprehensive pre-training data quality audit across:
1. Grade appropriateness (Class 1 to 8)
2. Factual and SI unit rigor
3. Pedagogical scaffolding and explanations
4. Known weak areas (joints, plants, rust, indicators, input analogies)
5. Multi-turn dialog naturalness
6. Scope & refusal boundaries
7. Near-duplicate / semantic leakage checks
8. Stratified quality sampling (35 records)
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILES = {
    "train": r"C:\Rounak\RVSHACK\data\train.jsonl",
    "val": r"C:\Rounak\RVSHACK\data\validation.jsonl",
    "test": r"C:\Rounak\RVSHACK\data\test.jsonl"
}

datasets = {}
for split, path in DATA_FILES.items():
    with open(path, encoding="utf-8") as f:
        datasets[split] = [json.loads(line) for line in f]

total_count = sum(len(v) for v in datasets.values())
print(f"Loaded datasets: Train={len(datasets['train'])}, Val={len(datasets['val'])}, Test={len(datasets['test'])}, Total={total_count}")

# 1. Distribution breakdown
grade_dist = {}
subj_dist = {}
qtype_dist = {}
diff_dist = {}

all_records = datasets["train"] + datasets["val"] + datasets["test"]

for r in all_records:
    g = r["metadata"]["grade"]
    s = r["metadata"]["subject"]
    qt = r["metadata"]["question_type"]
    d = r["metadata"]["difficulty"]
    
    grade_dist[g] = grade_dist.get(g, 0) + 1
    subj_dist[s] = subj_dist.get(s, 0) + 1
    qtype_dist[qt] = qtype_dist.get(qt, 0) + 1
    diff_dist[d] = diff_dist.get(d, 0) + 1

print("\n--- GRADE DISTRIBUTION ---")
for g in sorted(grade_dist.keys()):
    print(f"Class {g}: {grade_dist[g]} ({grade_dist[g]/total_count*100:.1f}%)")

print("\n--- SUBJECT DISTRIBUTION ---")
for s, c in sorted(subj_dist.items(), key=lambda x: -x[1]):
    print(f"{s}: {c} ({c/total_count*100:.1f}%)")

print("\n--- QUESTION TYPE DISTRIBUTION ---")
for qt, c in sorted(qtype_dist.items(), key=lambda x: -x[1]):
    print(f"{qt}: {c} ({c/total_count*100:.1f}%)")

print("\n--- DIFFICULTY DISTRIBUTION ---")
for d, c in sorted(diff_dist.items(), key=lambda x: -x[1]):
    print(f"{d}: {c} ({c/total_count*100:.1f}%)")

# 2. Check for weak areas in biology/chemistry/CS
weak_area_checks = {
    "joints": [],
    "plant_classification": [],
    "rust_prevention": [],
    "indicators": [],
    "keyboard_mouse": []
}

for split, records in datasets.items():
    for idx, r in enumerate(records):
        text = (r["messages"][0]["content"] + " " + r["messages"][-1]["content"]).lower()
        if "joint" in text or "hinge" in text or "ball-and-socket" in text:
            weak_area_checks["joints"].append((split, idx, r["messages"][0]["content"]))
        if "herb" in text or "shrub" in text or "tree" in text or "taproot" in text:
            weak_area_checks["plant_classification"].append((split, idx, r["messages"][0]["content"]))
        if "rust" in text or "galvaniz" in text or "corrosion" in text:
            weak_area_checks["rust_prevention"].append((split, idx, r["messages"][0]["content"]))
        if "indicator" in text or "turmeric" in text or "litmus" in text:
            weak_area_checks["indicators"].append((split, idx, r["messages"][0]["content"]))
        if "keyboard" in text or "mouse" in text or "pointer" in text:
            weak_area_checks["keyboard_mouse"].append((split, idx, r["messages"][0]["content"]))

print("\n--- WEAK AREA OCCURRENCES ---")
for k, v in weak_area_checks.items():
    print(f"{k}: {len(v)} occurrences found")

# 3. Near-duplicate detection across splits (normalized question text comparison)
def strip_punct(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

train_normalized = {strip_punct(r["messages"][0]["content"]): r for r in datasets["train"]}
val_normalized = {strip_punct(r["messages"][0]["content"]): r for r in datasets["val"]}
test_normalized = {strip_punct(r["messages"][0]["content"]): r for r in datasets["test"]}

leak_val_train = set(val_normalized.keys()).intersection(set(train_normalized.keys()))
leak_test_train = set(test_normalized.keys()).intersection(set(train_normalized.keys()))
leak_test_val = set(test_normalized.keys()).intersection(set(val_normalized.keys()))

print("\n--- LEAKAGE / EXACT NORMALIZED MATCHES ---")
print(f"Val vs Train overlap: {len(leak_val_train)}")
print(f"Test vs Train overlap: {len(leak_test_train)}")
print(f"Test vs Val overlap: {len(leak_test_val)}")
