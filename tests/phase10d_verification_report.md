# Phase 10D: Local llama.cpp & Q4_K_M GGUF Verification Report

## Status Summary

| Check | Result |
| :--- | :--- |
| **ENGINEERING PIPELINE** | **PASS** |
| **GGUF FILE & METADATA** | **PASS** |
| **LLAMA.CPP LOCAL INFERENCE** | **PASS** |
| **EDUCATIONAL FACTUAL ACCURACY** | **FAIL / NEEDS IMPROVEMENT** |
| **TUTOR SCAFFOLDING & FORMAT** | **PASS (Structure maintained)** |
| **QUANTIZATION INTEGRITY** | **PASS (Conversion intact)** |

> [!WARNING]
> **Factual Accuracy Audit Findings:**
> 1. **Newton's 2nd Law - Inverse Proportionality Error**: Output stated *"The more mass ... the faster it moves."* (Physically incorrect: for a constant force, greater mass results in *less* acceleration: $a = F/m$).
> 2. **Inertia / 1st Law Violation**: Output stated *"If you stop pushing, the ball stops moving."* (Propagates the Aristotelian misconception that force is required to sustain velocity; in the absence of net external forces like friction, an object in motion continues in uniform motion).
> 3. **Mass vs. Weight - Earth Arithmetic Error**: Output claimed *"A 10 kg bag of apples weighs 10 N on Earth."* (Calculated incorrectly; $W = mg = 10 \times 9.8 = 98\text{ N}$).
> 4. **Mass vs. Weight - Moon Arithmetic Error**: Output claimed a 10 kg object weighs 10 N on the Moon ($g_{\text{moon}} \approx 1.62\text{ m/s}^2 \implies W \approx 16.2\text{ N}$).
> 5. **Misconception Response - Physical Quantity Misstatement**: Output stated *"weight ... is not a physical quantity itself."* (Weight is indeed a physical quantity—specifically a vector force with magnitude measured in Newtons).


---

## 1. Model File & Size
- **File Path**: `C:\Rounak\RVSHACK\output\qwen3_tutor_q4_k_m.gguf`
- **Exact File Size**: `396,704,544 bytes` (378.33 MB)
- **Quantization Type**: `Q4_K_M` (File type 15, Quantization version 2)

---

## 2. GGUF Metadata Verification
- **Architecture**: `qwen3`
- **Model Name**: `Qwen3_Tutor_Merged`
- **Context Length**: `40,960`
- **Embedding Length**: `1024`
- **Block Count (Layers)**: `28`
- **Feed Forward Length**: `3072`
- **Attention Heads**: `16` (KV heads: `8`, GQA ratio 2:1)
- **Total Tensors Count**: `310`
- **Tokenizer Model**: `gpt2` (Byte-level BPE)
- **Tokenizer Chat Template**: Present (`tokenizer.chat_template`, 18,688 characters)

---

## 3. Local llama-cli Engine & Hardware Execution
- **CLI Binary**: `C:\Rounak\RVSHACK\llama.cpp\build_bin\llama-cli.exe` (v0.6.0-dev build 11466, Clang 20.1.8 x86_64)
- **Execution Mode**: **Pure CPU Execution**
  - GPU Offloading: `0 layers` (CPU Host memory; `Available devices: (none)`)
  - Working Compute Buffer: `68.02 MiB`
- **Process Load Latency**: ~3.0s (cold process start, model map, context initialization)

---

## 4. Benchmark Performance Metrics (Local CPU - 4 Threads)

| Test Query | Prompt Speed | Generation Speed | Exit Code |
| :--- | :--- | :--- | :--- |
| **Test 1: Newton's Second Law** | 417.1 t/s | 54.1 t/s | 0 |
| **Test 2: Math Step-by-Step** | 451.9 t/s | 56.1 t/s | 0 |
| **Test 3: Mass vs Weight** | 366.5 t/s | 58.0 t/s | 0 |
| **Test 4: Specific Misconception Test** | 450.4 t/s | 59.5 t/s | 0 |
| **Average** | **421.5 tokens/sec** | **56.9 tokens/sec** | **All 0** |

---

## 5. Test Outputs & Educational Behavior Analysis

### Test 1: Newton's Second Law
**Prompt**: *"Explain Newton's second law to a class 8 student in simple language."*
```text
Newton's second law is a fundamental law of physics that explains how force changes motion. It says: Force equals mass times acceleration (F = ma).

Simple explanation for a class 8 student:

Imagine a ball on a table. If you push the ball with a stick, it starts moving. Now, if you keep pushing it, it keeps moving faster. This is acceleration. The more mass (like a big ball) and the more force (like a stick), the faster the ball moves. The more mass, the slower it moves. The more force, the faster it moves.

Example:
- A car with a lot of mass and a lot of force (like a truck) moves very fast.
- A ball with a lot of mass and a little force (like a ball on a stick) moves slowly.

Key points:
- F = ma (force equals mass times acceleration)
- If you keep pushing a ball, it keeps moving faster.
- If you stop pushing, the ball stops moving.

Why is this important?
- It helps engineers build machines like rockets or cars.
- It explains why astronauts float in space.
- It helps scientists understand how objects move in space.

Practice question:
If a 10 kg ball is pushed with a force of 10 N, what is its acceleration?
```
*Tutor Behavior*: Retains class 8 scaffolding, bulleted summary, real-world examples, and an active practice question.

---

### Test 2: Algebra Step-by-Step
**Prompt**: *"Solve 3x + 7 = 25 step-by-step."*
```text
Step-by-step solution:

1. Start with the equation: 3x + 7 = 25.

2. Subtract 7 from both sides to isolate the term with x:
   3x + 7 - 7 = 25 - 7
   3x = 18

3. Divide both sides by 3 to solve for x:
   3x / 3 = 18 / 3
   x = 6

Answer: x = 6

Check:
Substitute x = 6 into the original equation:
3(6) + 7 = 18 + 7 = 25 ✅ Correct.
```
*Tutor Behavior*: Correct algebraic manipulation, isolated steps, and explicit step check/validation.

---

### Test 3: Mass vs. Weight
**Prompt**: *"Explain mass vs weight."*
```text
Mass and weight are related but not the same. Here's how they work:

1. Mass is the amount of matter in an object. It is measured in kilograms (kg) or grams (g). It is constant for all objects.

2. Weight is the force that acts on an object due to gravity. It is measured in Newtons (N). It depends on the object's location and the gravitational field strength.

Key Difference:
| Property | Mass | Weight |
|---------|-----|--------|
| Constant | Same for all objects | Changes with location (e.g., on Earth vs. Moon) |
| Measured in kg or g | Measured in kg or g | Measured in N (Newton) |
| Example | A 10 kg bag of apples | A 10 kg bag of apples |

Example:
- A 10 kg bag of apples weighs 10 N on Earth.
- A 10 kg bag of apples weighs 10 N on the Moon (where gravity is 1/6th Earth's).

Important Note:
- Mass is measured in kg.
- Weight is measured in N.
- Mass is constant, weight changes with location.
```
*Tutor Behavior*: Conceptual clarity, Markdown table contrast, unit differentiation (kg vs. N).

---

### Test 4: Specific Misconception Test
**Prompt**: *"A student says: my weight is 50 kg. Is this scientifically correct?"*
```text
No, this is not scientifically correct.

Scientifically speaking, weight is a measure of mass and gravitational force. It is measured in Newtons (N), and is not a physical quantity itself. It is a measure of mass (kg) multiplied by the gravitational acceleration (9.8 m/s²).

Key points:
- Weight = mass × gravitational acceleration
- Mass = weight / gravitational acceleration
- Weight = mass × g (where g = 9.8 m/s² on Earth)

Example:
- A person with a mass of 60 kg would weigh approximately 600 N (60 kg × 9.8 m/s²).
- A person with a mass of 50 kg would weigh approximately 490 N (50 kg × 9.8 m/s²).

Why is this important?
- Weight is the force that acts on an object (like gravity).
- It is a measure of mass and gravitational force.
- It is not a physical quantity itself.

Conclusion:
- Weight is a measure of mass and gravitational force.
- It is not a physical quantity itself.
- It is a measure of mass (kg) multiplied by the gravitational acceleration (g = 9.8 m/s²).

Answer: No, this is not scientifically correct.
```

**Verification against specific pedagogical criteria:**
- **Distinguishes mass in kg**: YES (`"person with a mass of 50 kg"`, `"measure of mass (kg)"`)
- **Distinguishes weight as force in N**: YES (`"measured in Newtons (N)"`, `"Weight is the force that acts on an object"`, calculates $50 \times 9.8 = 490\text{ N}$)
- **Formulates $W = mg$**: YES (`Weight = mass × g (where g = 9.8 m/s² on Earth)`)

---

## 6. Template & Mode Integrity
- **Chat Template**: Qwen3 ChatML format (`<|im_start|>user...<|im_end|><|im_start|>assistant...`) functioned properly with zero parsing failures.
- **Non-Thinking Mode**: The empty `<think>\n\n</think>\n\n` assistant prefix immediately triggered direct educational output without wasting compute tokens or leaking reasoning traces.
- **Quantization Integrity**: Fine-tuned tutor traits (pedagogical patience, clear formatting, self-check, formula grounding) completely survived the PyTorch merged fp16 -> GGUF fp16 -> Q4_K_M quantization pipeline.
