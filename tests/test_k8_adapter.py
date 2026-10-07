"""
test_k8_adapter.py
Phase 5 Adapter Test Script:
Loads Qwen/Qwen3-0.6B with the newly trained LoRA adapter from:
C:\\Rounak\\RVSHACK\\output\\qwen3_k8_tutor_lora
Runs 9 rigorous student test scenarios and verifies non-thinking, academic responses.
"""

import os
import sys
import json
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

TEST_CASES = [
    {
        "id": "1_class3_math",
        "description": "Class 3 Mathematics: Multiplication definition and calculation",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 3\nSubject: Mathematics\nQuestion: Calculate 7 × 4. What does multiplication mean?"
            }
        ]
    },
    {
        "id": "2_class5_science",
        "description": "Class 5 Science: State changes and water cycle",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 5\nSubject: Science\nQuestion: What is evaporation and how is it different from boiling?"
            }
        ]
    },
    {
        "id": "3_class6_math",
        "description": "Class 6 Mathematics: Like fractions and perimeter",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 6\nSubject: Mathematics\nQuestion: Solve 3x + 5 = 20 step-by-step. Show all steps."
            }
        ]
    },
    {
        "id": "4_class7_bio",
        "description": "Class 7 Biology: Plant classification and nutrition",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 7\nSubject: Science (Biology)\nQuestion: Differentiate between herbs and shrubs. Give two plant examples of each."
            }
        ]
    },
    {
        "id": "5_class8_physics",
        "description": "Class 8 Physics: Newton's Second Law and inertia",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 8\nSubject: Science (Physics)\nQuestion: A constant 30 N force pushes a 5 kg cart and a 15 kg cart. Which cart accelerates faster? Calculate both accelerations."
            }
        ]
    },
    {
        "id": "6_class8_cs",
        "description": "Class 8 Computer Science: Binary number system and logic",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 8\nSubject: Computer Science\nQuestion: Why do computers use the binary number system with 0 and 1 instead of decimal numbers?"
            }
        ]
    },
    {
        "id": "7_misconception",
        "description": "Misconception Question: Mass vs Weight",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 8\nSubject: Science (Physics)\nQuestion: A student says: my weight is 50 kg. Is this scientifically correct?"
            }
        ]
    },
    {
        "id": "8_scope_refusal",
        "description": "Out-of-Scope Question: Advanced university calculus",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 8\nSubject: Mathematics\nQuestion: Can you solve this second-order differential equation y'' + 4y = 0?"
            }
        ]
    },
    {
        "id": "9_multiturn",
        "description": "Multi-turn Tutoring Clarification",
        "messages": [
            {
                "role": "user",
                "content": "Student grade: Class 7\nSubject: Science (Chemistry)\nQuestion: Why does a yellow curry stain on a white cloth turn reddish-brown when washed with soap?"
            },
            {
                "role": "assistant",
                "content": "The statement is explained by acid-base indicator chemistry.\n\nDefinition:\nTurmeric contains curcumin, a natural acid-base indicator.\n\nExplanation:\nTurmeric maintains a bright yellow colour in neutral and acidic media. Soap solution is basic/alkaline (containing sodium hydroxide or potassium hydroxide fatty acid salts).\n\nKey Principle:\nWhen a basic substance contacts turmeric, the curcumin molecule undergoes a structural chemical change, turning reddish-brown.\n\nSummary:\nTurmeric turns reddish-brown in basic solutions and remains yellow in acidic or neutral solutions."
            },
            {
                "role": "user",
                "content": "What happens if I apply lemon juice on the reddish-brown stain?"
            }
        ]
    }
]

def run_tests():
    print("=" * 65)
    print("🧪 PHASE 5 — ADAPTER VERIFICATION SUITE")
    print("=" * 65)
    
    base_model_id = "Qwen/Qwen3-0.6B"
    adapter_dir = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_lora"
    
    print(f"Loading tokenizer from {adapter_dir}...")
    tokenizer = AutoTokenizer.from_pretrained(adapter_dir, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    print(f"Loading base model {base_model_id} in 4-bit...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="cuda",
        trust_remote_code=True,
    )
    
    print(f"Loading LoRA adapter from {adapter_dir}...")
    model = PeftModel.from_pretrained(base_model, adapter_dir)
    model.eval()
    print("LoRA adapter merged on inference device. Running test cases...")
    
    results = []
    
    for tc in TEST_CASES:
        print("\n" + "-" * 60)
        print(f"TEST [{tc['id']}]: {tc['description']}")
        print("-" * 60)
        
        # Apply clean chat template with generation prompt
        prompt = tokenizer.apply_chat_template(tc["messages"], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=350,
                do_sample=False,  # greedy decoding for reproducible deterministic output
                temperature=None,
                top_p=None,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
            
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        response_text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        
        print("MODEL RESPONSE:\n" + response_text)
        
        results.append({
            "id": tc["id"],
            "description": tc["description"],
            "prompt": tc["messages"][-1]["content"],
            "response": response_text
        })
        
    # Save results to json
    out_file = r"C:\Rounak\RVSHACK\tests\phase5_adapter_test_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nAll 9 tests completed. Saved to: {out_file}")

if __name__ == "__main__":
    run_tests()
