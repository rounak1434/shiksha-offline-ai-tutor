import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open(r"C:\Rounak\RVSHACK\data\train.jsonl", encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

by_grade = {}
for r in train_records:
    g = r['metadata']['grade']
    by_grade.setdefault(g, []).append(r)

samples = []
for g in [1, 2]:
    samples.extend(by_grade[g][:3 if g == 1 else 2])
for g in [3, 4]:
    samples.extend(by_grade[g][:3 if g == 3 else 2])
samples.extend(by_grade[5][:5])
samples.extend(by_grade[6][:5])
samples.extend(by_grade[7][:5])
samples.extend(by_grade[8][:10])

print(f"Total selected audit samples: {len(samples)}")
for idx, s in enumerate(samples, 1):
    m = s['metadata']
    q = s['messages'][0]['content'].split('\n')[-1]
    ans = s['messages'][-1]['content'].replace('\n', ' ')
    if len(ans) > 120:
        ans = ans[:120] + "..."
    print(f"\nSample {idx}:")
    print(f"  Class: {m['grade']} | Subject: {m['subject']} | Topic: {m['topic']}")
    print(f"  Difficulty: {m['difficulty']} | Type: {m['question_type']}")
    print(f"  Question: {q}")
    print(f"  Response: {ans}")
