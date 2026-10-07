"""
Offline AI Tutor — QLoRA Fine-Tuning Script
Target Model: Qwen/Qwen3-0.6B
Hardware: NVIDIA GeForce RTX 2050 (4 GB VRAM), Windows
"""

import os
import sys
import time
import json
import torch

os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

def main():
    print("=" * 60)
    print("🎓 OFFLINE AI TUTOR — QLoRA FINE-TUNING")
    print("=" * 60)
    
    start_time = time.time()
    
    # 1. Load Tokenizer
    model_id = "Qwen/Qwen3-0.6B"
    print(f"\n[1/6] Loading tokenizer for {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print(f"Tokenizer vocab size: {len(tokenizer)}")

    # 2. Load Dataset
    data_path = r"C:\Rounak\RVSHACK\data\train.jsonl"
    print(f"\n[2/6] Loading dataset from {data_path}...")
    dataset = load_dataset("json", data_files=data_path)["train"]
    print(f"Loaded {len(dataset)} training examples.")

    # 3. Configure 4-bit Quantization
    print("\n[3/6] Setting up 4-bit NF4 quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    # 4. Load Base Model
    print(f"Loading base model {model_id} on CUDA...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="cuda",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)
    
    init_vram = torch.cuda.memory_allocated() / (1024**3)
    print(f"Base model loaded in 4-bit. VRAM allocated: {init_vram:.2f} GB")

    # 5. Configure LoRA
    print("\n[4/6] Configuring LoRA adapter...")
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # 6. SFT Training Configuration
    output_dir = r"C:\Rounak\RVSHACK\output\qwen3_offline_tutor_lora"
    checkpoints_dir = r"C:\Rounak\RVSHACK\checkpoints"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(checkpoints_dir, exist_ok=True)

    print("\n[5/6] Setting up SFTConfig...")
    sft_config = SFTConfig(
        output_dir=checkpoints_dir,
        max_length=512,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_steps=5,
        bf16=True,
        optim="paged_adamw_8bit",
        logging_steps=5,
        save_strategy="no",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=sft_config,
    )

    # 7. Start Training
    print("\n[6/6] Starting QLoRA Training...")
    torch.cuda.reset_peak_memory_stats()
    train_result = trainer.train()

    peak_vram = torch.cuda.max_memory_allocated() / (1024**3)
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Total training time: {elapsed_time:.1f} seconds ({elapsed_time/60:.2f} minutes)")
    print(f"Peak VRAM used: {peak_vram:.2f} GB / 4.00 GB")
    print(f"Final training loss: {train_result.training_loss:.4f}")

    # 8. Save LoRA Adapter and Tokenizer
    print(f"\nSaving fine-tuned LoRA adapter to: {output_dir}...")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    metrics_file = os.path.join(output_dir, "training_metrics.json")
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump({
            "model_id": model_id,
            "train_samples": len(dataset),
            "num_epochs": 3,
            "training_loss": train_result.training_loss,
            "peak_vram_gb": round(peak_vram, 2),
            "elapsed_seconds": round(elapsed_time, 2),
            "lora_r": 8,
            "lora_alpha": 16,
            "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]
        }, f, indent=2)

    print(f"Metrics saved to: {metrics_file}")
    print("STATUS: SUCCESS")

if __name__ == "__main__":
    main()
