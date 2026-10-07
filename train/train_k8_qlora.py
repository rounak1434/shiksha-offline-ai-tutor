"""
train_k8_qlora.py
Final QLoRA training script for Offline AI Tutor (Class 1-8 curriculum).
Hardware: NVIDIA GeForce RTX 2050 (4 GB VRAM), Windows
Base Model: Qwen/Qwen3-0.6B
Target Output: C:\\Rounak\\RVSHACK\\output\\qwen3_k8_tutor_lora
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
    print("=" * 65)
    print("🎓 OFFLINE AI TUTOR (CLASS 1–8) — FINAL QLoRA TRAINING RUN")
    print("=" * 65)
    
    start_time = time.time()
    
    # ---------------------------------------------------------
    # 1. Preflight Validation
    # ---------------------------------------------------------
    print("\n[1/7] Running preflight system and dataset validation...")
    assert torch.cuda.is_available(), "CUDA is not available!"
    gpu_name = torch.cuda.get_device_name(0)
    total_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"CUDA Device: {gpu_name} (Total VRAM: {total_vram_gb:.2f} GB)")
    
    train_path = r"C:\Rounak\RVSHACK\data\train.jsonl"
    val_path = r"C:\Rounak\RVSHACK\data\validation.jsonl"
    test_path = r"C:\Rounak\RVSHACK\data\test.jsonl"
    
    with open(train_path, encoding="utf-8") as f:
        train_count = sum(1 for _ in f)
    with open(val_path, encoding="utf-8") as f:
        val_count = sum(1 for _ in f)
    with open(test_path, encoding="utf-8") as f:
        test_count = sum(1 for _ in f)
        
    print(f"Dataset Counts verified: Train={train_count}, Validation={val_count}, Test={test_count}")
    assert train_count == 1500, f"Expected 1500 train records, found {train_count}"
    assert val_count == 200, f"Expected 200 val records, found {val_count}"
    assert test_count == 300, f"Expected 300 test records, found {test_count}"
    
    # Verify baseline adapter directory is untouched
    baseline_dir = r"C:\Rounak\RVSHACK\output\qwen3_offline_tutor_lora"
    assert os.path.exists(baseline_dir), f"Baseline directory missing: {baseline_dir}"
    print(f"Baseline directory verified intact: {baseline_dir}")
    
    output_dir = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_lora"
    checkpoints_dir = r"C:\Rounak\RVSHACK\checkpoints\k8_run"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(checkpoints_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 2. Tokenizer & Chat Template Setup
    # ---------------------------------------------------------
    model_id = "Qwen/Qwen3-0.6B"
    print(f"\n[2/7] Loading tokenizer for {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    # Standard clean non-thinking ChatML template (no <think> traces)
    clean_template = (
        "{%- for message in messages %}"
        "{{- '<|im_start|>' + message['role'] + '\n' + message['content'].strip() + '<|im_end|>\n' }}"
        "{%- endfor %}"
        "{%- if add_generation_prompt %}"
        "{{- '<|im_start|>assistant\n' }}"
        "{%- endif %}"
    )
    tokenizer.chat_template = clean_template
    print(f"Configured clean non-thinking ChatML template. Vocab size: {len(tokenizer)}")
    
    # ---------------------------------------------------------
    # 3. Load Datasets
    # ---------------------------------------------------------
    print("\n[3/7] Loading training and validation datasets...")
    train_dataset = load_dataset("json", data_files=train_path)["train"]
    val_dataset = load_dataset("json", data_files=val_path)["train"]
    print(f"Training dataset: {len(train_dataset)} examples")
    print(f"Validation dataset: {len(val_dataset)} examples")
    
    # ---------------------------------------------------------
    # 4. 4-bit NF4 Quantization & Base Model
    # ---------------------------------------------------------
    print("\n[4/7] Configuring 4-bit NF4 base model loading...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    print(f"Loading {model_id} onto GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="cuda",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)
    init_vram = torch.cuda.memory_allocated() / (1024**3)
    print(f"Base model loaded in 4-bit. VRAM allocated: {init_vram:.2f} GB")
    
    # ---------------------------------------------------------
    # 5. LoRA Configuration
    # ---------------------------------------------------------
    print("\n[5/7] Configuring LoRA adapter (r=8, alpha=16)...")
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    # ---------------------------------------------------------
    # 6. SFT Training Configuration
    # ---------------------------------------------------------
    print("\n[6/7] Configuring SFTTrainer...")
    sft_config = SFTConfig(
        output_dir=checkpoints_dir,
        max_length=512,
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_steps=15,
        bf16=True,
        optim="paged_adamw_8bit",
        logging_steps=25,
        eval_strategy="epoch",
        save_strategy="no",
        report_to="none",
        gradient_checkpointing=True,
    )
    
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=sft_config,
    )
    
    trainable_params, all_params = trainer.model.get_nb_trainable_parameters()
    print(f"Trainable LoRA parameters: {trainable_params:,} / {all_params:,} ({trainable_params/all_params*100:.2f}%)")
    
    # ---------------------------------------------------------
    # 7. Start Training & Evaluation
    # ---------------------------------------------------------
    print("\n[7/7] Launching 1-epoch QLoRA training...")
    torch.cuda.reset_peak_memory_stats()
    
    train_result = trainer.train()
    
    peak_vram = torch.cuda.max_memory_allocated() / (1024**3)
    train_time = time.time() - start_time
    
    print("\nRunning post-epoch validation evaluation...")
    eval_metrics = trainer.evaluate()
    val_loss = eval_metrics.get("eval_loss", 0.0)
    
    print("\n" + "=" * 65)
    print("TRAINING RUN COMPLETE!")
    print("=" * 65)
    print(f"Total training time:     {train_time:.1f} s ({train_time/60:.2f} min)")
    print(f"Training steps:          {train_result.global_step}")
    print(f"Training loss:           {train_result.training_loss:.4f}")
    print(f"Validation loss:         {val_loss:.4f}")
    print(f"Peak VRAM used:          {peak_vram:.2f} GB / {total_vram_gb:.2f} GB")
    
    # ---------------------------------------------------------
    # 8. Save LoRA Adapter & Training Metrics
    # ---------------------------------------------------------
    print(f"\nSaving fine-tuned LoRA adapter to: {output_dir}...")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Calculate adapter size on disk
    adapter_bytes = sum(
        os.path.getsize(os.path.join(output_dir, f))
        for f in os.listdir(output_dir)
        if os.path.isfile(os.path.join(output_dir, f))
    )
    
    # Save detailed training metrics
    metrics_file = os.path.join(output_dir, "training_metrics.json")
    metrics_data = {
        "model_id": model_id,
        "train_samples": len(train_dataset),
        "val_samples": len(val_dataset),
        "test_samples": test_count,
        "epochs_completed": 1,
        "global_steps": train_result.global_step,
        "effective_batch_size": 2,  # per_device_batch_size 1 * grad_accum 2
        "learning_rate": 2e-4,
        "train_loss": round(float(train_result.training_loss), 4),
        "val_loss": round(float(val_loss), 4),
        "peak_vram_gb": round(float(peak_vram), 2),
        "total_vram_gb": round(float(total_vram_gb), 2),
        "training_time_seconds": round(float(train_time), 2),
        "trainable_parameters": trainable_params,
        "total_parameters": all_params,
        "adapter_size_bytes": adapter_bytes,
        "adapter_dir": output_dir,
        "status": "PASS"
    }
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
        
    print(f"Metrics saved to: {metrics_file}")
    print(f"LoRA Adapter saved successfully. Total adapter size: {adapter_bytes:,} bytes ({adapter_bytes/1024**2:.2f} MB)")
    print("STATUS: PASS")

if __name__ == "__main__":
    main()
