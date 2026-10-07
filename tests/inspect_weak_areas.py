import json

path = r"C:\Rounak\RVSHACK\data\train.jsonl"
with open(path, encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

for idx, r in enumerate(train_records[:300]):
    text = (r["messages"][0]["content"] + " " + r["messages"][-1]["content"]).lower()
    if "joint" in text:
        print(f"--- JOINT RECORD ({idx}) ---")
        print("Q:", r["messages"][0]["content"][:100])
        print("A:", r["messages"][-1]["content"][:200])
        break

for idx, r in enumerate(train_records[:300]):
    text = (r["messages"][0]["content"] + " " + r["messages"][-1]["content"]).lower()
    if "rust" in text:
        print(f"--- RUST RECORD ({idx}) ---")
        print("Q:", r["messages"][0]["content"][:100])
        print("A:", r["messages"][-1]["content"][:200])
        break

for idx, r in enumerate(train_records[:300]):
    text = (r["messages"][0]["content"] + " " + r["messages"][-1]["content"]).lower()
    if "indicator" in text or "turmeric" in text:
        print(f"--- INDICATOR RECORD ({idx}) ---")
        print("Q:", r["messages"][0]["content"][:100])
        print("A:", r["messages"][-1]["content"][:200])
        break

for idx, r in enumerate(train_records[:300]):
    text = (r["messages"][0]["content"] + " " + r["messages"][-1]["content"]).lower()
    if "mouse" in text or "keyboard" in text:
        print(f"--- KEYBOARD/MOUSE RECORD ({idx}) ---")
        print("Q:", r["messages"][0]["content"][:100])
        print("A:", r["messages"][-1]["content"][:200])
        break
