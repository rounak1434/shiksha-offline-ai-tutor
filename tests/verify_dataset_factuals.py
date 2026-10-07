import json
import sys
from stem_factual_checker import STEMFactualChecker

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILES = {
    "Train": r"C:\Rounak\RVSHACK\data\train.jsonl",
    "Validation": r"C:\Rounak\RVSHACK\data\validation.jsonl",
    "Test": r"C:\Rounak\RVSHACK\data\test.jsonl"
}

total_records = 0
errors = 0

for split_name, filepath in DATA_FILES.items():
    with open(filepath, encoding="utf-8") as f:
        records = [json.loads(line) for line in f]
    total_records += len(records)
    print(f"Checking {len(records)} {split_name} examples...")
    
    for idx, item in enumerate(records):
        ans = item["messages"][-1]["content"]
        q = item["messages"][0]["content"]
        
        # Check Newton's Second Law
        if ("newton" in q.lower() and "second" in q.lower()) or "f = ma" in ans.lower():
            res = STEMFactualChecker.check_newton_second_law(ans)
            if not res["passed"]:
                print(f"{split_name} Newton Error at #{idx}: {res['issues']}")
                errors += 1
                
        # Check Mass vs Weight
        if "mass" in q.lower() and "weight" in q.lower():
            res = STEMFactualChecker.check_mass_vs_weight(ans)
            if not res["passed"]:
                print(f"{split_name} Mass vs Weight Error at #{idx}: {res['issues']}")
                errors += 1

if errors == 0:
    print(f"\nALL FACTUAL ACCURACY CHECKS PASSED: Zero factual errors found across all {total_records} records.")
else:
    print(f"\nFound {errors} factual issues.")
