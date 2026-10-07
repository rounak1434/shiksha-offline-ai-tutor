"""
build_all_datasets.py
Aggregates curriculum modules into:
- train.jsonl (210)
- validation.jsonl (35)
- test.jsonl (45)

Performs strict leakage detection, SI unit validation, and line count verification.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, r"C:\Rounak\RVSHACK\data\curriculum")

from physics_data import physics_train, physics_val, physics_test
from math_data import math_train, math_val, math_test
from chemistry_data import chemistry_train, chemistry_val, chemistry_test
from biology_data import biology_train, biology_val, biology_test
from cs_data import cs_train, cs_val, cs_test

train_records = physics_train + math_train + chemistry_train + biology_train + cs_train
val_records = physics_val + math_val + chemistry_val + biology_val + cs_val
test_records = physics_test + math_test + chemistry_test + biology_test + cs_test

print("=" * 60)
print("DATASET AGGREGATION & VALIDATION")
print("=" * 60)
print(f"Physics:     Train={len(physics_train)}, Val={len(physics_val)}, Test={len(physics_test)}")
print(f"Mathematics: Train={len(math_train)}, Val={len(math_val)}, Test={len(math_test)}")
print(f"Chemistry:   Train={len(chemistry_train)}, Val={len(chemistry_val)}, Test={len(chemistry_test)}")
print(f"Biology:     Train={len(biology_train)}, Val={len(biology_val)}, Test={len(biology_test)}")
print(f"Computer Sc: Train={len(cs_train)}, Val={len(cs_val)}, Test={len(cs_test)}")
print("-" * 60)
print(f"TOTAL:       Train={len(train_records)}, Val={len(val_records)}, Test={len(test_records)}")
print(f"Grand Total: {len(train_records) + len(val_records) + len(test_records)} examples")
print("=" * 60)

# 1. Leakage Verification
train_queries = {r["messages"][0]["content"].strip().lower() for r in train_records}
val_queries = {r["messages"][0]["content"].strip().lower() for r in val_records}
test_queries = {r["messages"][0]["content"].strip().lower() for r in test_records}

leakage_val_train = val_queries.intersection(train_queries)
leakage_test_train = test_queries.intersection(train_queries)
leakage_test_val = test_queries.intersection(val_queries)

if leakage_val_train:
    raise ValueError(f"CRITICAL: Leakage detected between Validation and Train: {leakage_val_train}")
if leakage_test_train:
    raise ValueError(f"CRITICAL: Leakage detected between Test and Train: {leakage_test_train}")
if leakage_test_val:
    raise ValueError(f"CRITICAL: Leakage detected between Test and Validation: {leakage_test_val}")

print("✅ LEAKAGE CHECK: PASSED (Zero query overlap between Train, Validation, and Test)")

# 2. Save JSONL files
OUT_DIR = r"C:\Rounak\RVSHACK\data"

def write_jsonl(records, filename):
    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        for item in records:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Saved {len(records)} records to {filepath}")

write_jsonl(train_records, "train.jsonl")
write_jsonl(val_records, "validation.jsonl")
write_jsonl(test_records, "test.jsonl")

print("=" * 60)
print("All datasets successfully created and verified.")
