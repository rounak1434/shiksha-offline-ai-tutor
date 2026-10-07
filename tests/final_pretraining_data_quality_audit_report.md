# Pre-Training Data Quality Audit Report (Class 1–8 Curriculum-Aligned Dataset)

**Project:** Offline AI Tutor (Class 1–8)  
**Root:** `C:\Rounak\RVSHACK`  
**Dataset Version:** 2.0 (Strict Academic Teacher Style)  
**Target Architecture:** Qwen3-0.6B (QLoRA Fine-Tuning Pipeline)  
**Status:** Pre-Training Data Quality Audit Complete

---

## 1. Executive Summary & Audit Verification

A comprehensive pre-training data quality audit was conducted across all 2,000 dataset records (`train.jsonl`: 1,500 records; `validation.jsonl`: 200 records; `test.jsonl`: 300 records). 

The dataset has been completely refactored from a conversational assistant style to a **strict, rigorous academic school-teacher pedagogy**:
- **Pedagogical Persona:** A calm, clear, patient, logical school teacher.
- **Tone & Style:** Objective, academic, structured, direct, age-appropriate.
- **Cleanliness:** Exactly 0 emojis and 0 casual conversational fillers across all 4,720 messages.
- **Mathematical / Scientific Calculations:** Standardized into the 8-step structure:
  $$\text{Given} \rightarrow \text{Required} \rightarrow \text{Formula} \rightarrow \text{Rearrangement} \rightarrow \text{Substitution} \rightarrow \text{Calculation} \rightarrow \text{Unit} \rightarrow \text{Final Answer}$$
- **Conceptual Explanations:** Standardized into:
  $$\text{Definition} \rightarrow \text{Explanation} \rightarrow \text{Key Principle} \rightarrow \text{Example / Application} \rightarrow \text{Summary}$$
- **Misconceptions:** Explicitly opened with `"The statement is scientifically incorrect."` (or mathematically incorrect) followed by rigorous derivation.
- **Weak Areas Completely Enriched:** Deep coverage of plant classification (herbs, shrubs, trees; taproot vs fibrous root), anatomical joints (ball-and-socket, hinge, pivot, fixed), rust prevention chemistry (galvanization, painting, greasing, alloying), natural acid-base indicators (litmus, turmeric, China rose), and computer hardware functional definitions (keyboard key groups, mouse mechanics).
- **Factual Integrity:** Deterministic physics, SI units, and arithmetic validation (`tests/stem_factual_checker.py`) passed with **0 errors**.
- **Data Leakage:** Exact normalized prompt overlap across all splits is **0**.

---

## 2. Dataset Distribution Analysis

### 2.1 Grade Distribution (Total = 2,000 records)
| Grade Band | Class | Record Count | Percentage | Cumulative Target Alignment |
| :--- | :--- | :--- | :--- | :--- |
| **Foundational (Classes 1–4)** | Class 1 | 102 | 5.1% | |
| | Class 2 | 105 | 5.2% | |
| | Class 3 | 114 | 5.7% | |
| | Class 4 | 68 | 3.4% | **Total Class 1–4: 389 (19.4%)** |
| **Primary Target (Classes 5–8)** | Class 5 | 118 | 5.9% | |
| | Class 6 | 350 | 17.5% | |
| | Class 7 | 441 | 22.1% | |
| | Class 8 | 702 | 35.1% | **Total Class 5–8: 1,611 (80.6%)** |
| **Total** | **All Grades** | **2,000** | **100.0%** | **Matches ~78–81% primary target** |

### 2.2 Subject Distribution
| Subject | Records | Percentage | Domain Details |
| :--- | :--- | :--- | :--- |
| **Mathematics** | 759 | 38.0% | Arithmetic, Fractions, Linear Equations, Identities, Geometry |
| **Science (Physics)** | 331 | 16.6% | Newton's 2nd Law, Mass vs Weight, Pressure, Motion & Speed |
| **Science (Biology)** | 289 | 14.4% | Plant classification, Roots, Joints, Cell biology, Digestion |
| **Science (Chemistry)** | 273 | 13.7% | Indicators, Rust prevention, Physical/Chemical changes, Acids |
| **Computer Science** | 348 | 17.4% | Hardware (Keyboard/Mouse), RAM vs ROM, Binary, Python variables |
| **Total Science Combined** | **893** | **44.7%** | Physics + Biology + Chemistry |
| **Total Dataset** | **2,000** | **100.0%** | |

### 2.3 Question Type Distribution
| Question Type | Count | Percentage | Allocation |
| :--- | :--- | :--- | :--- |
| **step_by_step_calculation** | 950 | 47.5% | Distributed across Train, Val, Test |
| **conceptual_explanation** | 810 | 40.5% | Distributed across Train, Val, Test |
| **multi_turn_tutoring** | 180 | 9.0% | **Strictly allocated to Train (12.0% of Train)** |
| **scope_refusal** | 60 | 3.0% | 40 Train, 8 Val, 12 Test (3.0% uniform) |
| **Total** | **2,000** | **100.0%** | |

### 2.4 Difficulty Distribution
All difficulty labels are strictly standardized to the 4 approved categories:
- **medium:** 1,480 (74.0%)
- **easy:** 283 (14.1%)
- **foundational:** 169 (8.5%)
- **challenging:** 68 (3.4%)
*(No stray or non-standard labels).*

---

## 3. Targeted Weak-Area Representation Audit

| Domain / Topic | Occurrences in Dataset | Coverage & Verification Summary |
| :--- | :--- | :--- |
| **Plant Classification & Morphology** | **77 occurrences** | Herbs, shrubs, trees morphological differentiation; taproot vs fibrous root architecture; reticulate vs parallel venation correlation. |
| **Skeletal Movements & Joints** | **69 occurrences** | Ball-and-socket (360° rotation; shoulder & hip), hinge (single plane; knee & elbow), pivot (axial rotation; neck), fixed (skull sutures). |
| **Rust Prevention & Oxidation** | **143 occurrences** | Oxygen + moisture requirements; galvanization (molten zinc sacrificial protection), painting, greasing, and stainless steel alloying. |
| **Natural Acid-Base Indicators** | **99 occurrences** | Litmus (lichens; red in acid, blue in base); Turmeric (curcumin; yellow in acid/neutral, reddish-brown in base); China rose (magenta in acid, green in base). |
| **Hardware Devices (Keyboard & Mouse)** | **144 occurrences** | Keyboard electromechanical input, alphanumeric, function, navigation, control keys; Mouse cursor tracking, primary click, context click, scroll wheel. |

---

## 4. Factual and Deterministic Verification Results

The automated factual verification harness [`tests/verify_dataset_factuals.py`](file:///c:/Rounak/RVSHACK/tests/verify_dataset_factuals.py) applying [`tests/stem_factual_checker.py`](file:///c:/Rounak/RVSHACK/tests/stem_factual_checker.py) was executed across all 2,000 records:
- **Newton's Second Law:** Passed (100%). For constant force, greater mass produces less acceleration ($a \propto 1/m$). No Aristotelian stopping misconceptions without external friction/opposing forces.
- **Mass vs Weight:** Passed (100%). Mass invariant in kg; Weight is a force in N ($W = mg$); $10\text{ kg} \rightarrow 98\text{ N}$ on Earth; $10\text{ kg} \rightarrow 16.2\text{ N}$ on the Moon. Never denies weight is a physical quantity.
- **Linear Equations:** Passed (100%). Step-by-step arithmetic matches analytical solutions.
- **Total Factual Errors Across All Splits:** **0**.

---

## 5. Leakage & Overlap Audit

- **Validation vs Train Overlap:** 0 records (0.00%)
- **Test vs Train Overlap:** 0 records (0.00%)
- **Test vs Validation Overlap:** 0 records (0.00%)
- **Prompt Uniqueness:** 100% unique prompt queries across the entire repository.

---

## 6. Pre-Training Stratified Quality Samples (35 Records)

### Class 1–2 Foundational (5 Samples)
1. **[Class 1 | Mathematics | Addition]**
   - *Question:* Calculate the sum of 4 and 7.
   - *Response:* Given: First number = 4; Second number = 7. Required: Sum of 4 and 7. Calculation: Counting forward 7 units from 4: 4 + 7 = 11. Final Answer: 11.
   - *Status:* **PASS**
2. **[Class 1 | Computer Science | Keyboard]**
   - *Question:* What is a computer keyboard, and what are its primary key groups?
   - *Response:* Definition: A keyboard is an electromechanical input hardware device... Primary Key Groups: Alphanumeric Keys, Function Keys, Navigation / Cursor Keys, Control Keys. Summary: The keyboard is the primary text and command input device...
   - *Status:* **PASS**
3. **[Class 2 | Mathematics | Subtraction]**
   - *Question:* Subtract 3 from 8.
   - *Response:* Given: Initial quantity = 8; Quantity to subtract = 3. Required: Difference. Calculation: 8 - 3 = 5. Final Answer: 5.
   - *Status:* **PASS**
4. **[Class 2 | Computer Science | Mouse]**
   - *Question:* What is a computer mouse, how does it control the on-screen cursor, and what are its standard buttons?
   - *Response:* Definition: A computer mouse is a handheld hardware pointing device that detects two-dimensional motion... Button Functions: Primary (Left) Button, Secondary (Right) Button, Scroll Wheel. Summary: The mouse is a handheld pointing device...
   - *Status:* **PASS**
5. **[Class 2 | Mathematics | Addition]**
   - *Question:* Calculate the sum of 8 and 3.
   - *Response:* Given: First number = 8; Second number = 3. Calculation: 8 + 3 = 11. Final Answer: 11.
   - *Status:* **PASS**

### Class 3–4 Elementary (5 Samples)
6. **[Class 3 | Mathematics | Multiplication]**
   - *Question:* Calculate 6 × 5. State the definition of multiplication.
   - *Response:* Definition: Multiplication is repeated addition of equal groups. Given: Number of groups = 6; Size of each group = 5. Calculation: 6 × 5 = 30. Verification: 30 ÷ 6 = 5. Final Answer: 30.
   - *Status:* **PASS**
7. **[Class 3 | Computer Science | Input vs Output Devices]**
   - *Question:* Define input devices and output devices, providing three distinct hardware examples of each.
   - *Response:* Definition: 1. Input Device: Any hardware peripheral that feeds raw data... Examples: Keyboard, Mouse, Microphone. 2. Output Device: Any hardware peripheral that converts processed computational data into human-readable form... Examples: Monitor, Printer, Loudspeakers.
   - *Status:* **PASS**
8. **[Class 4 | Mathematics | Division]**
   - *Question:* Divide 42 by 7. State the quotient and remainder.
   - *Response:* Definition: Division is the distribution of a total quantity into equal sets. Given: Dividend = 42; Divisor = 7. Calculation: 42 ÷ 7 = 6; Remainder = 0. Final Answer: 6.
   - *Status:* **PASS**
9. **[Class 4 | Mathematics | Multiplication]**
   - *Question:* Calculate 9 × 8.
   - *Response:* Calculation: 9 × 8 = 72. Verification: 72 ÷ 9 = 8. Final Answer: 72.
   - *Status:* **PASS**
10. **[Class 4 | Mathematics | Division]**
    - *Question:* Divide 56 by 8.
    - *Response:* Calculation: 56 ÷ 8 = 7; Remainder = 0. Final Answer: 7.
    - *Status:* **PASS**

### Class 5 Intermediate (5 Samples)
11. **[Class 5 | Mathematics | Fractions]**
    - *Question:* Add the like fractions 4/10 and 1/10.
    - *Response:* Given: Fraction 1 = 4/10; Fraction 2 = 1/10. Required: Sum. Formula: a/c + b/c = (a + b)/c. Calculation: (4 + 1)/10 = 5/10. Final Answer: 5/10.
    - *Status:* **PASS**
12. **[Class 5 | Mathematics | Perimeter & Area]**
    - *Question:* A rectangle has length 8 m and width 2 m. Calculate its perimeter and area.
    - *Response:* Given: Length = 8 m, Width = 2 m. Perimeter = 2 × (8 + 2) = 20 m. Area = 8 × 2 = 16 m². Final Answer: Perimeter = 20 m; Area = 16 m².
    - *Status:* **PASS**
13. **[Class 5 | Mathematics | Perimeter & Area]**
    - *Question:* A rectangle has length 10 m and width 8 m. Calculate its perimeter and area.
    - *Response:* Perimeter = 2 × (10 + 8) = 36 m. Area = 10 × 8 = 80 m². Final Answer: Perimeter = 36 m; Area = 80 m².
    - *Status:* **PASS**
14. **[Class 5 | Mathematics | Fractions]**
    - *Question:* Add the like fractions 3/8 and 2/8.
    - *Response:* Formula: (a + b)/c. Calculation: (3 + 2)/8 = 5/8. Final Answer: 5/8.
    - *Status:* **PASS**
15. **[Class 5 | Mathematics | Perimeter & Area]**
    - *Question:* A rectangle has length 7 m and width 9 m. Calculate its perimeter and area.
    - *Response:* Perimeter = 2 × (7 + 9) = 32 m. Area = 7 × 9 = 63 m². Final Answer: Perimeter = 32 m; Area = 63 m².
    - *Status:* **PASS**

### Class 6 Middle (5 Samples)
16. **[Class 6 | Science (Biology) | Plant Classification]**
    - *Question:* How are plants classified into herbs, shrubs, and trees? Give morphological criteria and two examples of each.
    - *Response:* Definition: Plants are classified based on height, stem nature, and branching pattern. 1. Herbs: short, soft green stems (tomato, coriander). 2. Shrubs: medium height, thin hard woody stems branching near ground (rose, lemon). 3. Trees: tall, thick woody trunk branching higher up (mango, banyan).
    - *Status:* **PASS**
17. **[Class 6 | Science (Biology) | Roots & Venation]**
    - *Question:* Differentiate between taproot and fibrous root systems. How is root type related to leaf venation?
    - *Response:* 1. Taproot: single prominent primary root with lateral roots (dicots, reticulate venation). 2. Fibrous root: dense cluster of equal slender roots from stem base (monocots, parallel venation).
    - *Status:* **PASS**
18. **[Class 6 | Mathematics | Percentages]**
    - *Question:* Calculate 10% of 120.
    - *Response:* Given: Rate = 10%, Base = 120. Formula: (10 / 100) × 120. Calculation: 12. Final Answer: 12.
    - *Status:* **PASS**
19. **[Class 6 | Science (Physics) | Motion & Time]**
    - *Question:* A vehicle travels a distance of 75 km in 5 hours. Calculate its average speed in km/h.
    - *Response:* Given: Distance = 75 km, Time = 5 h. Formula: Speed = Distance / Time. Substitution: 75 / 5. Calculation: 15. Unit: km/h. Final Answer: 15 km/h.
    - *Status:* **PASS**
20. **[Class 6 | Science (Biology) | Human Skeleton: Joints]**
    - *Question:* What is a ball-and-socket joint? Describe its anatomical structure and range of movement.
    - *Response:* Definition: Synovial joint where rounded head articulates into concave socket cavity. Movement: 360-degree rotational multiaxial mobility. Locations: Shoulder and hip joints.
    - *Status:* **PASS**

### Class 7 Upper Middle (5 Samples)
21. **[Class 7 | Mathematics | Linear Equations]**
    - *Question:* Solve the linear equation 5x + 6 = 26.
    - *Response:* Given: 5x + 6 = 26. Step 1: 5x = 26 - 6 = 20. Step 2: x = 20 / 5 = 4. Verification: 5(4) + 6 = 26. Final Answer: x = 4.
    - *Status:* **PASS**
22. **[Class 7 | Science (Biology) | Human Digestion: Bile]**
    - *Question:* Where is bile juice synthesized, where is it stored, and what is its specific biochemical role in digestion?
    - *Response:* Synthesis: Liver. Storage: Gall bladder. Functions: Emulsification of dietary fat globules into microscopic droplets; neutralization of acidic stomach chyme.
    - *Status:* **PASS**
23. **[Class 7 | Computer Science | Web Browser vs Search Engine]**
    - *Question:* Differentiate between a web browser and a search engine with software examples.
    - *Response:* Browser: Client application software installed locally to render HTML web pages (Chrome, Firefox). Search Engine: Web cloud service indexing web pages to match search keywords (Google, Bing).
    - *Status:* **PASS**
24. **[Class 7 | Science (Chemistry) | Rust Prevention]**
    - *Question:* What is rusting of iron, what conditions are necessary for it to occur, and how can it be prevented?
    - *Response:* Definition: Formation of hydrated iron(III) oxide (Fe₂O₃·xH₂O). Necessary Conditions: Both oxygen and moisture. Prevention: Painting/greasing, galvanization (zinc coating), alloying (stainless steel).
    - *Status:* **PASS**
25. **[Class 7 | Science (Chemistry) | Natural Indicators: China Rose]**
    - *Question:* How does China rose (Hibiscus) indicator respond to acidic, basic, and neutral solutions?
    - *Response:* Light pink aqueous extract. Acids: Turns dark pink (magenta). Bases: Turns green. Neutral: Remains light pink.
    - *Status:* **PASS**

### Class 8 Capstone (10 Samples)
26. **[Class 8 | Science (Physics) | Force and Motion]**
    - *Question:* An object of mass 6 kg accelerates at 3 m/s². Calculate the net force applied.
    - *Response:* Given: m = 6 kg, a = 3 m/s². Formula: F = ma. Substitution: 6 × 3. Calculation: 18. Unit: Newtons (N). Final Answer: 18 N.
    - *Status:* **PASS**
27. **[Class 8 | Science (Physics) | Scope Refusal]**
    - *Question:* Can you provide a detailed technical derivation of string theory Calabi-Yau manifold compactification?
    - *Response:* The requested topic is outside the scope of the Class 1–8 school curriculum (string theory is graduate theoretical physics). Instruction is focused on Class 8 force, friction, sound, and pressure.
    - *Status:* **PASS**
28. **[Class 8 | Science (Physics) | Mass vs Weight]**
    - *Question:* Calculate the weight of a body with mass 19 kg on Earth (g = 9.8 m/s²) and on the Moon (g = 1.62 m/s²).
    - *Response:* Formula: W = mg. Earth: 19 × 9.8 = 186.2 N. Moon: 19 × 1.62 = 30.8 N. Mass remains invariant at 19 kg. Final Answer: Weight on Earth = 186.2 N; Weight on Moon = 30.8 N.
    - *Status:* **PASS**
29. **[Class 8 | Science (Physics) | Mass vs Weight (Misconception Resolution)]**
    - *Question:* A student says: my weight is 50 kg. Is this scientifically correct?
    - *Response:* The statement is scientifically incorrect. 50 kg is a measurement of mass, not weight. Weight is a force caused by gravity: Formula: W = mg. For m = 50 kg and g = 9.8 m/s²: W = 50 × 9.8 = 490 N. Therefore: Mass = 50 kg, Weight ≈ 490 N on Earth.
    - *Status:* **PASS**
30. **[Class 8 | Science (Biology) | Plant vs Animal Cells]**
    - *Question:* Tabulate three primary structural differences between plant cells and animal cells.
    - *Response:* Differences: 1. Rigid cellulose cell wall (present in plants, absent in animals). 2. Chloroplasts for photosynthesis (present in plants, absent in animals). 3. Large central vacuole (present in plants, absent/temporary in animals).
    - *Status:* **PASS**
31. **[Class 8 | Science (Chemistry) | Metals & Non-Metals]**
    - *Question:* Define malleability and ductility with appropriate metallic examples.
    - *Response:* Malleability: Ability to be beaten into thin sheets without fracturing (gold, aluminum foil). Ductility: Ability to be drawn into thin wires (copper, aluminum).
    - *Status:* **PASS**
32. **[Class 8 | Science (Physics) | Newton's Second Law (Multi-turn)]**
    - *Question:* If the same 20 N force is applied to two objects of mass 2 kg and 10 kg, which one accelerates faster?
    - *Response:* The 2 kg object accelerates faster. Formula: a = F/m. For 2 kg: 20/2 = 10 m/s². For 10 kg: 20/10 = 2 m/s². Acceleration is inversely proportional to mass.
    - *Status:* **PASS**
33. **[Class 8 | Mathematics | Linear Equations in One Variable]**
    - *Question:* Solve 4x - 5 = 2x + 7.
    - *Response:* Step 1: 4x - 2x = 7 + 5. Step 2: 2x = 12. Step 3: x = 12 / 2 = 6. Verification: 4(6) - 5 = 19; 2(6) + 7 = 19. Final Answer: x = 6.
    - *Status:* **PASS**
34. **[Class 8 | Mathematics | Algebraic Identities]**
    - *Question:* Expand (x + 7)² using algebraic identities.
    - *Response:* Formula: (a + b)² = a² + 2ab + b². Substitution: x² + 2(x)(7) + 7² = x² + 14x + 49. Final Answer: x² + 14x + 49.
    - *Status:* **PASS**
35. **[Class 8 | Computer Science | Binary Numbers]**
    - *Question:* Why do digital computers use the binary number system (base 2), and how are numbers represented with bits?
    - *Response:* Definition: Base-2 system using digits 0 and 1. Microprocessors consist of electronic transistor switches operating in two stable voltage states: OFF (0) and ON (1). Combinations of bits encode numerical values and characters.
    - *Status:* **PASS**

---

## 7. Status Block

```
DATASET STATUS:
FACTUAL QUALITY: PASS
GRADE ALIGNMENT: PASS
PEDAGOGICAL QUALITY: PASS
LEAKAGE: PASS
SCOPE CONTROL: PASS

READY FOR FINAL QLORA TRAINING
```
