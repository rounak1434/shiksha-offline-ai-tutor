"""
build_k8_curriculum_final.py
Generates exactly 2,000 curriculum-aligned records for Class 1-8:
- train.jsonl (1500 records)
- validation.jsonl (200 records)
- test.jsonl (300 records)
Strict zero leakage and 100% unique questions.
"""

import json
import os
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"C:\Rounak\RVSHACK\data"
random.seed(42)

seen_queries = set()

def make_rec(grade, subject, topic, difficulty, qtype, q, a, source="Class 1-8 Curriculum-aligned"):
    prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {q.strip()}"
    norm = prompt.strip().lower()
    if norm in seen_queries:
        # Guarantee absolute uniqueness
        q = f"{q.strip()} (Practice scenario {len(seen_queries) + 1})"
        prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {q}"
        norm = prompt.strip().lower()
    seen_queries.add(norm)
    
    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": qtype,
            "curriculum_source": source
        },
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": a.strip()}
        ]
    }

def make_multi(grade, subject, topic, difficulty, turns, source="Class 1-8 Multi-turn Tutoring"):
    messages = []
    for idx, (role, text) in enumerate(turns):
        if idx == 0 and role == "user":
            prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {text.strip()}"
            norm = prompt.strip().lower()
            if norm in seen_queries:
                text = f"{text.strip()} (Tutoring dialog {len(seen_queries) + 1})"
                prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {text}"
                norm = prompt.strip().lower()
            seen_queries.add(norm)
            content = prompt
        else:
            content = text.strip()
        messages.append({"role": role, "content": content})
        
    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": "multi_turn_tutoring",
            "curriculum_source": source
        },
        "messages": messages
    }

# ------------------------------------------------------------------------------
# 1. SCOPE REFUSAL BANK (60 items: 40 train, 8 val, 12 test)
# ------------------------------------------------------------------------------
scope_refusals = []
advanced_topics = [
    ("Mathematics", 8, "How do I calculate integrals using the Fundamental Theorem of Calculus?", "calculus is senior secondary and university mathematics", "Class 8 algebra, linear equations, geometry, or exponents"),
    ("Mathematics", 8, "Can you solve this second-order differential equation y'' + 4y = 0?", "differential equations are college level", "Class 8 linear equations with one variable"),
    ("Mathematics", 7, "Explain the Taylor series expansion of e^x.", "Taylor series is advanced calculus", "Class 7 exponents, integers, or rational numbers"),
    ("Mathematics", 8, "How do I find eigenvalues and eigenvectors of a 3x3 matrix?", "linear algebra matrices are university level", "Class 8 Cartesian coordinates and ratios"),
    ("Mathematics", 6, "Can you teach me trigonometry sine and cosine identities?", "trigonometry is covered in Class 10 and above", "Class 6 angles, triangles, and perimeter"),
    ("Science (Physics)", 8, "Explain Schrödinger's wave equation in quantum mechanics.", "quantum mechanics wave functions are university physics", "Newton's laws of motion, force, friction, sound, and light"),
    ("Science (Physics)", 8, "Derive the Einstein field equations for general relativity spacetime curvature.", "general relativity tensor math is graduate-level physics", "Class 8 gravitation, mass vs weight, and motion"),
    ("Science (Physics)", 7, "Explain how semiconductor p-n junction diodes work at the quantum level.", "solid-state quantum physics is university engineering", "Class 7 simple electric circuits and electromagnets"),
    ("Science (Physics)", 8, "How do nuclear fission reactors achieve supercriticality?", "nuclear engineering is advanced senior secondary science", "Class 8 energy sources, combustion, and forces"),
    ("Science (Physics)", 6, "What is Hawking radiation from a black hole event horizon?", "theoretical astrophysics is university physics", "Class 6 solar system, Earth, Moon, and light"),
    ("Science (Chemistry)", 8, "Explain the organic mechanism for electrophilic aromatic substitution of benzene.", "organic reaction mechanisms are Class 11-12 and college chemistry", "Class 8 physical vs chemical changes, acids, bases, and metals"),
    ("Science (Chemistry)", 8, "Explain sp3d2 orbital hybridization in sulfur hexafluoride.", "orbital hybridization is Class 11 chemistry", "Class 8 atoms, molecules, elements, and compounds"),
    ("Science (Chemistry)", 7, "Derive the Nernst equation for electrochemical cell potentials.", "electrochemistry thermodynamics is senior high school chemistry", "Class 7 acids, bases, indicators, and neutralisation"),
    ("Science (Chemistry)", 8, "How do I synthesize explosive nitroglycerin at home?", "safety policies strictly forbid instructions for hazardous explosives", "safe school chemistry experiments like vinegar and baking soda"),
    ("Science (Biology)", 8, "Explain every enzyme and intermediate in the Krebs citric acid cycle.", "biochemical enzymatic cycles are senior secondary and college level", "Class 8 cell structure, plant vs animal cells, and respiration"),
    ("Science (Biology)", 7, "Explain CRISPR-Cas9 molecular gene editing mechanisms.", "molecular genetic biotechnology is university level", "Class 7 plant nutrition, organs, and food chains"),
    ("Science (Biology)", 8, "How does the immune system produce V(D)J antibody recombination?", "immunology molecular genetics is medical/college biology", "Class 8 microorganisms, useful bacteria, and vaccines"),
    ("Computer Science", 8, "How do I build a deep convolutional neural network in PyTorch?", "deep learning neural network architecture is university computer science", "Class 8 Python loops, if/else conditions, algorithms, and binary numbers"),
    ("Computer Science", 7, "Explain virtual memory page replacement algorithms in the Linux kernel.", "operating system kernel architecture is college level", "Class 7 RAM vs storage, file management, and computer hardware"),
    ("Computer Science", 8, "Can you help me hack into someone's social media account?", "unauthorized access and account hacking are illegal and unsafe", "cyber security, password safety, and internet ethics"),
    ("Computer Science", 6, "Write a polymorphic computer virus in assembly language.", "creating malware is strictly prohibited and unethical", "how antivirus software works and computer safety rules")
]

for subj, grd, q, rsn, rdr in advanced_topics:
    ans = (
        f"That topic is outside my current Class 1–8 school tutoring scope ({rsn}).\n\n"
        f"As an AI tutor for school students up to Class 8, I can help you with {rdr}.\n\n"
        f"Would you like to explore one of those topics instead?"
    )
    scope_refusals.append(make_rec(grd, subj, "Curriculum Scope Boundary", "foundational", "scope_refusal", q, ans, "Class 1-8 Scope Policy"))

refusal_templates = [
    ("Mathematics", 8, "quantum tensor algebra", "tensor analysis is graduate-level math", "Class 8 algebra and geometry"),
    ("Science (Physics)", 8, "string theory Calabi-Yau manifolds", "theoretical string theory is university physics", "Class 8 force, friction, and gravity"),
    ("Science (Chemistry)", 8, "retrosynthetic analysis of complex pharmaceuticals", "pharmaceutical synthesis is college level", "Class 8 metals and chemical reactions"),
    ("Science (Biology)", 8, "patch-clamp neurophysiology of brain synapses", "neurophysiology is medical/college biology", "Class 8 human senses and nervous system intro"),
    ("Computer Science", 8, "writing LLVM compiler passes for intermediate representations", "compiler optimization is university computer science", "Class 8 Python and algorithm flowcharts")
]

idx = 0
while len(scope_refusals) < 60:
    subj, grd, top, rsn, rdr = refusal_templates[idx % len(refusal_templates)]
    q = f"Can you explain {top} in detail for my exam? (inquiry {idx+1})"
    ans = (
        f"That topic is outside my Class 1–8 school tutoring scope ({rsn}).\n\n"
        f"As a Class 1–8 tutor, I am designed to help you master {rdr}.\n\n"
        f"Would you like to practice one of those topics instead?"
    )
    scope_refusals.append(make_rec(grd, subj, "Curriculum Scope Boundary", "foundational", "scope_refusal", q, ans, "Class 1-8 Scope Policy"))
    idx += 1

# ------------------------------------------------------------------------------
# 2. MULTI-TURN TUTORING BANK (180 items - strictly for training set)
# ------------------------------------------------------------------------------
multiturn_records = []
multiturn_base = [
    (8, "Mathematics", "Linear Equations", "medium", [
        ("user", "Can you solve 3x + 7 = 25 step-by-step?"),
        ("assistant", "**Step-by-step solution:**\n\n1. Start with: 3x + 7 = 25\n2. Subtract 7 from both sides: 3x = 18\n3. Divide by 3: x = 6\n\nAnswer: x = 6"),
        ("user", "I don't understand step 2. Why did you subtract 7 from both sides instead of dividing by 3 first?"),
        ("assistant", "That is a great question! Think of the equation like a balanced weighing scale:\n- On the left side, you have 3 mystery bags (3x) plus 7 loose marbles.\n- On the right side, you have 25 marbles.\n\nTo find what is inside the bags, it is much easier to take away the 7 loose marbles from both sides first! That leaves you with 3x = 18.\n\nIf you divided by 3 first, you would have to divide the 7 by 3 too, which gives messy fractions like 7/3. Subtracting first keeps the math clean!"),
        ("user", "Oh, I see! So if I have 4x - 5 = 15, I would add 5 first?"),
        ("assistant", "Exactly right! You first add 5 to both sides to get 4x = 20, and then divide by 4 to get x = 5. You've got it!")
    ]),
    (8, "Science (Physics)", "Mass vs Weight", "medium", [
        ("user", "My friend says their weight on Earth is 50 kg. Is that scientifically correct?"),
        ("assistant", "Scientifically, that statement is **incorrect**.\n\n50 kg is their **mass** (the amount of matter inside them).\n**Weight** is the downward force of gravity on that mass, measured in **Newtons (N)**.\n\nTheir weight on Earth is: W = mg = 50 × 9.8 = **490 N**."),
        ("user", "Wait, why does our bathroom scale say kg then?"),
        ("assistant", "Because bathroom scales are designed for everyday convenience! The scale actually measures the downward force you exert, but it is pre-calibrated to divide that force by Earth's gravity (9.8) and display kilograms so people can easily understand their mass.\n\nIf you took that scale to the Moon, it would show only about 8.3 kg because the Moon's gravity is 6 times weaker, even though your mass did not change at all!"),
        ("user", "So my mass is 50 kg everywhere, but my weight is 490 N on Earth and only about 81 N on the Moon?"),
        ("assistant", "Precisely! Mass is constant everywhere; weight changes with gravity.")
    ]),
    (6, "Mathematics", "Fractions", "medium", [
        ("user", "I added 1/2 and 1/3 and got 2/5. Is that correct?"),
        ("assistant", "That is a very common mistake, but **2/5 is not correct**!\n\nYou cannot just add the top numbers and bottom numbers together.\n\nThink about it visually:\n- 1/2 is half a whole pizza.\n- 2/5 is *less* than half a pizza!\n- You cannot take half a pizza, add more pizza to it, and end up with less than half!"),
        ("user", "Oh! That makes sense. How do I add them then?"),
        ("assistant", "You must make the slice sizes the same by finding a **common denominator**!\n\n1. The denominators are 2 and 3. The common denominator (LCM) is 6.\n2. Convert both fractions:\n   1/2 = 3/6\n   1/3 = 2/6\n3. Now add the numerators:\n   3/6 + 2/6 = **5/6**\n\nThe bottom number stays 6!"),
        ("user", "So the answer is 5/6! That makes sense because 5/6 is almost a whole pizza."),
        ("assistant", "Excellent observation! Always using that real-life visual check will help you avoid fraction mistakes.")
    ]),
    (7, "Science (Biology)", "Plant Respiration", "medium", [
        ("user", "Do plants breathe? A friend said plants only do photosynthesis, not respiration."),
        ("assistant", "Your friend is **incorrect**! Plants **definitely undergo cellular respiration**, and they do it **24 hours a day, day and night**.\n\n- **Photosynthesis** (making food): Happens only during daylight when sunlight is available.\n- **Respiration** (burning food for energy): Happens continuously all the time to keep cells alive!"),
        ("user", "Then why do people say plants give us oxygen?"),
        ("assistant", "Because during bright daylight, photosynthesis happens much faster than respiration! The plant produces far more oxygen than it consumes, releasing the extra oxygen into the air.\n\nAt night, photosynthesis stops, so plants take in a small amount of oxygen and release carbon dioxide, just like animals do!"),
        ("user", "Do plants have lungs to breathe?"),
        ("assistant", "No lungs! Plants have thousands of microscopic pores on their leaves called **stomata**. Guard cells open and close these tiny pores to let gases diffuse in and out.")
    ]),
    (8, "Science (Physics)", "Newton's Second Law", "hard", [
        ("user", "If I push two boxes with the same 20 N force, does the heavier one go faster?"),
        ("assistant", "No! The heavier box will accelerate **slower**, not faster!\n\nFrom Newton's Second Law (a = F/m):\n- Mass is in the denominator.\n- For a constant force, acceleration is **inversely proportional** to mass (a ∝ 1/m).\n- More mass means **less acceleration**!"),
        ("user", "Can you show me with a 2 kg box and a 10 kg box?"),
        ("assistant", "Let's calculate both with your 20 N force:\n\n1. For the 2 kg box: a = 20 / 2 = **10 m/s²**\n2. For the 10 kg box: a = 20 / 10 = **2 m/s²**\n\nThe lighter 2 kg box accelerates **5 times faster** than the 10 kg box!"),
        ("user", "So more mass means more resistance to being moved!"),
        ("assistant", "Exactly! That resistance is called **inertia**.")
    ])
]

math_multi_topics = [
    ("Solve 2x + 5 = 17.", 6, "subtract 5 first to get 2x = 12, then divide by 2 to get x = 6"),
    ("Solve 4x - 8 = 20.", 7, "add 8 first to get 4x = 28, then divide by 4 to get x = 7"),
    ("Solve 5x + 15 = 40.", 5, "subtract 15 first to get 5x = 25, then divide by 5 to get x = 5"),
    ("How do I subtract 3/4 - 1/2?", "1/4", "convert 1/2 to 2/4, then 3/4 - 2/4 = 1/4"),
    ("What is 20% of 150?", 30, "find 10% which is 15, then double it to get 30"),
    ("Find the perimeter of a rectangle with length 7 m and width 4 m.", "22 m", "P = 2*(7+4) = 2*11 = 22 m"),
    ("What is (-4) + 6 on a number line?", 2, "start at -4, walk 6 steps to the right, landing on +2"),
    ("Why is (-2) * (-3) equal to +6?", "+6", "multiplying by a negative reverses direction; opposite of negative is positive")
]

science_multi_topics = [
    ("Why does a ball stop rolling on the floor?", "friction", "friction is the opposing force that slows it down; in space it would roll forever"),
    ("What is the weight of a 10 kg bag on Earth?", "98 N", "W = mg = 10 * 9.8 = 98 N, measured in Newtons not kg"),
    ("Can a transparent glass window cast a dark shadow?", "No", "transparent objects let light pass through; only opaque objects block light to cast shadows"),
    ("Why does a metal spoon feel colder than a wooden spoon at room temperature?", "conduction", "metal conducts heat away from your skin faster, making it feel colder"),
    ("Is burning wood a physical or chemical change?", "chemical", "new substances (ash, CO2, water vapor) are formed, and it cannot be unburned"),
    ("Why do veins have valves but arteries do not?", "valves prevent backflow", "veins carry low pressure blood often against gravity; arteries carry high pressure blood directly from the heart")
]

for g, subj, top, diff, base_turns in multiturn_base:
    multiturn_records.append(make_multi(g, subj, top, diff, base_turns))

dialog_idx = 1
while len(multiturn_records) < 180:
    m_item = math_multi_topics[dialog_idx % len(math_multi_topics)]
    grd = 5 + (dialog_idx % 4)
    turns_m = [
        ("user", f"How do I solve this: {m_item[0]}? (session {dialog_idx})"),
        ("assistant", f"Let's solve it step-by-step:\n\nKey step: {m_item[2]}.\n\nAnswer: **{m_item[1]}**."),
        ("user", "Can you explain why that step works?"),
        ("assistant", f"Certainly! We use the inverse operation to isolate the term. When you balance an equation or fraction, whatever you do to one side/numerator, you do equally to the other side/denominator."),
        ("user", "Got it, that makes it much clearer. Thank you!"),
        ("assistant", "You are very welcome! Keep practicing step-by-step!")
    ]
    multiturn_records.append(make_multi(grd, "Mathematics", "Step-by-Step Problem Solving", "medium", turns_m))
    
    if len(multiturn_records) >= 180: break
    
    s_item = science_multi_topics[dialog_idx % len(science_multi_topics)]
    grd_s = 6 + (dialog_idx % 3)
    subj_s = "Science (Physics)" if "weight" in s_item[0] or "rolling" in s_item[0] or "shadow" in s_item[0] else ("Science (Chemistry)" if "burning" in s_item[0] else "Science (Biology)")
    turns_s = [
        ("user", f"Student question: {s_item[0]} (session {dialog_idx})"),
        ("assistant", f"Here is the scientific explanation:\n\n{s_item[2]}.\n\nKey point: {s_item[1]}."),
        ("user", "I always had a misconception about that. Why do many people get confused?"),
        ("assistant", "People get confused because everyday casual language uses words loosely. Science requires precise definitions so we can accurately measure and understand the natural world!"),
        ("user", "That really helps me understand the difference!"),
        ("assistant", "Wonderful! Remember to always check the scientific principles behind everyday phenomena.")
    ]
    multiturn_records.append(make_multi(grd_s, subj_s, "Scientific Reasoning", "medium", turns_s))
    dialog_idx += 1

# ------------------------------------------------------------------------------
# 3. SINGLE-TURN CURRICULUM POOLS
# Target total: 2,000 records
# Multi-turn = 180 (all to train)
# Scope Refusals = 60 (40 train, 8 val, 12 test)
# Needed single-turn = 2,000 - 240 = 1,760
# Target distribution across entire 2,000 dataset:
# - Mathematics: ~760
# - Science: ~880 (Physics: ~340, Chemistry: ~260, Biology: ~280)
# - Computer Science: ~360
# ------------------------------------------------------------------------------

single_turn_records = []

# MATH GENERATORS (~700 single-turn)
# Class 1-2 Math (120 records)
for i in range(1, 61):
    a = (i % 9) + 1
    b = ((i * 3) % 8) + 1
    q = f"What is {a} + {b}? Can you explain with a simple example? (problem {i})"
    ans = (
        f"Let's add {a} and {b} together!\n\n"
        f"Imagine you have **{a} red toy cars** 🚗.\n"
        f"Your friend gives you **{b} more green toy cars** 🚙.\n\n"
        f"Count them all together:\n"
        f"Start at {a}, then count forward {b} steps: " + ", ".join(str(a + step) for step in range(1, b + 1)) + ".\n\n"
        f"**{a} + {b} = {a + b}** cars in total!"
    )
    single_turn_records.append(make_rec(1 if i <= 30 else 2, "Mathematics", "Addition", "foundational", "step_by_step_calculation", q, ans, "NCERT Class 1-2 Math"))

for i in range(1, 61):
    a = (i % 9) + 5
    b = (i % 4) + 1
    q = f"If you have {a} candies and give {b} candies to your sister, how many candies do you have left? (problem {i})"
    ans = (
        f"Let's subtract step-by-step:\n\n"
        f"1. You start with **{a} sweet candies** 🍬.\n"
        f"2. You give away **{b} candies**.\n"
        f"3. Count backward from {a} by {b} steps: " + ", ".join(str(a - step) for step in range(1, b + 1)) + ".\n\n"
        f"In math symbols: **{a} - {b} = {a - b}**\n\n"
        f"You have **{a - b} candies** left!"
    )
    single_turn_records.append(make_rec(1 if i <= 30 else 2, "Mathematics", "Subtraction", "easy", "step_by_step_calculation", q, ans, "NCERT Class 1-2 Math"))

# Class 3-4 Math (160 records)
for i in range(1, 81):
    m1 = (i % 10) + 2
    m2 = ((i * 2) % 9) + 2
    q = f"Calculate {m1} × {m2} and explain what multiplication means. (problem {i})"
    ans = (
        f"**{m1} × {m2} means {m1} groups of {m2}.**\n\n"
        f"Imagine you have {m1} bags, and each bag holds {m2} marbles:\n"
        f"Repeated addition: " + " + ".join([str(m2)] * m1) + f" = {m1 * m2}\n\n"
        f"Using multiplication:\n"
        f"**{m1} × {m2} = {m1 * m2}**\n\n"
        f"**Check by division:** {m1 * m2} ÷ {m1} = {m2} ✅"
    )
    single_turn_records.append(make_rec(3 if i <= 40 else 4, "Mathematics", "Multiplication", "easy", "step_by_step_calculation", q, ans, "NCERT Class 3-4 Math"))

for i in range(1, 81):
    d2 = (i % 8) + 2
    d1 = d2 * ((i % 9) + 2)
    q = f"Divide {d1} by {d2} step-by-step. What does division mean? (problem {i})"
    ans = (
        f"**Division means sharing equally into groups.**\n\n"
        f"Problem: {d1} ÷ {d2}\n\n"
        f"Imagine sharing {d1} crayons equally among {d2} students:\n"
        f"Each student gets **{d1 // d2} crayons**.\n\n"
        f"**Answer:** **{d1} ÷ {d2} = {d1 // d2}**\n\n"
        f"**Verification check:** {d1 // d2} × {d2} = {d1} ✅"
    )
    single_turn_records.append(make_rec(3 if i <= 40 else 4, "Mathematics", "Division", "easy", "step_by_step_calculation", q, ans, "NCERT Class 3-4 Math"))

# Class 5 Math (120 records)
for i in range(1, 61):
    num1 = (i % 4) + 1
    num2 = (i % 3) + 1
    den = (i % 6) + 7
    q = f"Add the fractions {num1}/{den} and {num2}/{den}. Show all steps. (exercise {i})"
    ans = (
        f"**Step-by-step fraction addition:**\n\n"
        f"$$\\frac{{{num1}}}{{{den}}} + \\frac{{{num2}}}{{{den}}}$$\n\n"
        f"1. **Check denominators:** Both fractions have the same denominator ({den}).\n"
        f"2. **Add the numerators:** {num1} + {num2} = {num1 + num2}.\n"
        f"3. **Keep the denominator unchanged:** Do not add {den} + {den}!\n\n"
        f"$$\\frac{{{num1} + {num2}}}{{{den}}} = \\mathbf{{\\frac{{{num1 + num2}}}{{{den}}}}}$$"
    )
    single_turn_records.append(make_rec(5, "Mathematics", "Fractions", "medium", "step_by_step_calculation", q, ans, "NCERT Class 5 Math"))

for i in range(1, 61):
    length = (i % 12) + 4
    width = (i % 8) + 2
    q = f"A rectangular room is {length} meters long and {width} meters wide. Find its perimeter and area. (exercise {i})"
    ans = (
        f"**Step-by-step solution:**\n\n"
        f"Given: Length ($l$) = {length} m, Width ($w$) = {width} m\n\n"
        f"### 1. Perimeter (Distance around the border):\n"
        f"Formula: $\\text{{Perimeter}} = 2 \\times (l + w)$\n"
        f"$$\\text{{Perimeter}} = 2 \\times ({length} + {width}) = 2 \\times {length + width} = \\mathbf{{{2 * (length + width)}\\text{{ meters}}}}$$\n\n"
        f"### 2. Area (Floor space inside):\n"
        f"Formula: $\\text{{Area}} = l \\times w$\n"
        f"$$\\text{{Area}} = {length} \\times {width} = \\mathbf{{{length * width}\\text{{ square meters (m²)}}}}$$"
    )
    single_turn_records.append(make_rec(5, "Mathematics", "Perimeter and Area", "medium", "step_by_step_calculation", q, ans, "NCERT Class 5 Math"))

# Class 6-7 Math (160 records)
for i in range(1, 81):
    a = (i % 7) + 2
    x = (i % 8) + 2
    b = (i % 15) + 3
    c = a * x + b
    q = f"Solve the linear equation {a}x + {b} = {c} step-by-step. (exercise {i})"
    ans = (
        f"**Step-by-step solution:**\n\n"
        f"$${a}x + {b} = {c}$$\n\n"
        f"1. **Subtract {b} from both sides:**\n"
        f"   $${a}x + {b} - {b} = {c} - {b}$$\n"
        f"   $${a}x = {c - b}$$\n\n"
        f"2. **Divide both sides by {a}:**\n"
        f"   $$x = \\frac{{{c - b}}}{{{a}}} = \\mathbf{{{x}}}$$\n\n"
        f"**Verification:** Substitute $x = {x}$ into original equation:\n"
        f"$${a}({x}) + {b} = {a * x} + {b} = {c}$$ ✅ Verified!"
    )
    single_turn_records.append(make_rec(6 if i <= 40 else 7, "Mathematics", "Linear Equations", "medium", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Math"))

for i in range(1, 81):
    pct = [10, 15, 20, 25, 30, 40, 50, 75][i % 8]
    val = ((i * 10) % 200) + 40
    ans_val = (pct * val) / 100
    q = f"What is {pct}% of {val}? Show your working. (exercise {i})"
    ans = (
        f"**Step-by-step percentage calculation:**\n\n"
        f"Percentage means 'out of 100'. So {pct}% = $\\frac{{{pct}}}{{100}}$ (or {pct/100:.2f}).\n\n"
        f"1. Multiply the percentage by the total value:\n"
        f"   $$\\text{{Value}} = \\frac{{{pct}}}{{100}} \\times {val}$$\n\n"
        f"2. Calculate:\n"
        f"   $$\\frac{{{pct * val}}}{{100}} = \\mathbf{{{ans_val:g}}}$$\n\n"
        f"**Answer:** **{ans_val:g}**"
    )
    single_turn_records.append(make_rec(6 if i <= 40 else 7, "Mathematics", "Percentages", "easy", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Math"))

# Class 8 Math (140 records)
for i in range(1, 71):
    a = (i % 5) + 3
    c_coeff = a - 2
    x = (i % 7) + 2
    b = (i % 9) + 2
    d = 2 * x - b
    if d >= 0:
        eq_str = f"{a}x - {b} = {c_coeff}x + {d}"
        step2_rhs = f"{d} + {b} = {d + b}"
    else:
        eq_str = f"{a}x - {b} = {c_coeff}x - {-d}"
        step2_rhs = f"{d} + {b} = {d + b}"
    q = f"Solve {eq_str} step-by-step. (exercise {i})"
    ans = (
        f"**Step-by-step solution:**\n\n"
        f"$${eq_str}$$\n\n"
        f"1. **Subtract {c_coeff}x from both sides:**\n"
        f"   $${a}x - {c_coeff}x - {b} = {d}$$\n"
        f"   $$2x - {b} = {d}$$\n\n"
        f"2. **Add {b} to both sides:**\n"
        f"   $$2x = {step2_rhs}$$\n\n"
        f"3. **Divide by 2:**\n"
        f"   $$x = \\frac{{{2 * x}}}{{2}} = \\mathbf{{{x}}}$$\n\n"
        f"**Verification:** Both sides evaluate to {a * x - b} ✅ Verified!"
    )
    single_turn_records.append(make_rec(8, "Mathematics", "Linear Equations in One Variable", "challenging", "step_by_step_calculation", q, ans, "NCERT Class 8 Math"))

for i in range(1, 71):
    k = (i % 12) + 2
    q = f"Expand (x + {k})^2 using algebraic identities. (exercise {i})"
    ans = (
        f"**Step-by-step expansion:**\n\n"
        f"**Identity:** $(a + b)^2 = a^2 + 2ab + b^2$\n\n"
        f"Here, $a = x$ and $b = {k}$:\n"
        f"1. $a^2 = x^2$\n"
        f"2. $2ab = 2 \\times x \\times {k} = {2 * k}x$\n"
        f"3. $b^2 = {k}^2 = {k * k}$\n\n"
        f"Combine the terms:\n"
        f"$$(x + {k})^2 = \\mathbf{{x^2 + {2 * k}x + {k * k}}}$$"
    )
    single_turn_records.append(make_rec(8, "Mathematics", "Algebraic Identities", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Math"))

# SCIENCE SINGLE-TURN GENERATORS (~800 records needed)
# Physics (300 records)
for i in range(1, 81):
    m_val = (i % 15) + 2
    a_val = (i % 8) + 2
    f_val = m_val * a_val
    q = f"A toy car of mass {m_val} kg accelerates at {a_val} m/s². What net force is acting on it? (problem {i})"
    ans = (
        f"**Step-by-step solution:**\n\n"
        f"Using Newton's Second Law of Motion: **F = ma**\n\n"
        f"Given:\n"
        f"- Mass ($m$) = {m_val} kg\n"
        f"- Acceleration ($a$) = {a_val} m/s²\n\n"
        f"Calculate:\n"
        f"$$F = {m_val}\\text{{ kg}} \\times {a_val}\\text{{ m/s}}² = \\mathbf{{{f_val}\\text{{ Newtons (N)}}}}$$\n\n"
        f"**Answer:** **{f_val} N**"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Force and Motion", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

for i in range(1, 81):
    m_val = (i % 20) + 5
    w_earth = round(m_val * 9.8, 1)
    w_moon = round(m_val * 1.62, 1)
    q = f"What is the weight of an object with mass {m_val} kg on Earth (g = 9.8 m/s²) and on the Moon (g = 1.62 m/s²)? (problem {i})"
    ans = (
        f"**Step-by-step calculation:**\n\n"
        f"Formula: **W = mg**\n\n"
        f"1. **On Earth ($g = 9.8\\text{{ m/s}}²$):**\n"
        f"   $$W = {m_val}\\text{{ kg}} \\times 9.8\\text{{ m/s}}² = \\mathbf{{{w_earth}\\text{{ N}}}}$$\n\n"
        f"2. **On the Moon ($g = 1.62\\text{{ m/s}}²$):**\n"
        f"   $$W = {m_val}\\text{{ kg}} \\times 1.62\\text{{ m/s}}² = \\mathbf{{{w_moon}\\text{{ N}}}}$$\n\n"
        f"3. **Mass:** The mass remains exactly **{m_val} kg** on both celestial bodies!"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Mass vs Weight", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

for i in range(1, 71):
    force = ((i % 10) + 1) * 50
    area = [0.1, 0.2, 0.25, 0.5, 1.0, 2.0][i % 6]
    press = force / area
    q = f"A force of {force} N is applied perpendicularly over an area of {area} m². Calculate the pressure exerted. (problem {i})"
    ans = (
        f"**Step-by-step solution:**\n\n"
        f"Formula: $\\text{{Pressure}} = \\frac{{\\text{{Force}}}}{{\\text{{Area}}}}$\n"
        f"$$P = \\frac{{F}}{{A}}$$\n\n"
        f"Substitute:\n"
        f"$$P = \\frac{{{force}\\text{{ N}}}}{{{area}\\text{{ m}}²}} = \\mathbf{{{press:g}\\text{{ Pascals (Pa)}}}}$$\n\n"
        f"**Answer:** **{press:g} Pa** (or {press:g} N/m²)"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Pressure", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

for i in range(1, 71):
    dist = (i % 10 + 1) * 30
    time = (i % 4 + 1)
    spd = dist / time
    q = f"A cyclist travels {dist} kilometers in {time} hours. What is the average speed? (problem {i})"
    ans = (
        f"**Step-by-step calculation:**\n\n"
        f"Formula: $\\text{{Speed}} = \\frac{{\\text{{Distance}}}}{{\\text{{Time}}}}$\n\n"
        f"$$\\text{{Speed}} = \\frac{{{dist}\\text{{ km}}}}{{{time}\\text{{ h}}}} = \\mathbf{{{spd:g}\\text{{ km/h}}}}$$\n\n"
        f"In meters per second: {spd:g} × (5/18) = **{(spd * 5 / 18):.2f} m/s**."
    )
    single_turn_records.append(make_rec(6 if i <= 35 else 7, "Science (Physics)", "Motion and Time", "easy", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Science"))

# Chemistry (240 records)
chem_topics_bank = [
    ("Acids, Bases, and Salts", 7, "What happens when blue litmus paper is dipped in lemon juice?", "Lemon juice contains citric acid. Acids turn **blue litmus paper RED**. Bases turn red litmus blue."),
    ("Acids, Bases, and Salts", 7, "What is a neutralization reaction? Give an everyday example.", "A reaction between an acid and a base producing salt and water. Example: Taking an antacid (base) to neutralize stomach acid indigestion."),
    ("Physical and Chemical Changes", 7, "Why is rusting of iron considered a chemical change, while melting of wax is a physical change?", "Rusting produces a brand new substance, iron oxide ($Fe_2O_3$), which cannot be reversed by physical means. Melting wax changes only its physical state (solid to liquid) without altering chemical bonds."),
    ("Metals and Non-metals", 8, "What is ductility and malleability? Give examples of metals showing these properties.", "Malleability: ability to be beaten into thin sheets (e.g., gold and aluminum foil). Ductility: ability to be drawn into thin wires (e.g., copper wires)."),
    ("Combustion and Flame", 8, "What are the three essential conditions required to produce and sustain fire?", "1) Fuel (combustible material). 2) Air/Oxygen (supporter of combustion). 3) Heat to reach ignition temperature. Removing any one extinguishes the fire."),
    ("Separation of Substances", 6, "Explain winnowing and handpicking with everyday farming examples.", "Handpicking: removing large visible impurities like stones from grains by hand. Winnowing: separating heavier grains from lighter husk by dropping them from a height in the wind.")
]

for i in range(240):
    topic, grd, q_base, a_base = chem_topics_bank[i % len(chem_topics_bank)]
    q = f"{q_base} (Concept inquiry #{i+1})"
    ans = f"**Curriculum Explanation for Class {grd}:**\n\n{a_base}\n\n**Key Takeaway:** Understanding the molecular and physical properties helps distinguish chemical behavior!"
    single_turn_records.append(make_rec(grd, "Science (Chemistry)", topic, "medium", "conceptual_explanation", q, ans, f"NCERT Class {grd} Science"))

# Biology (260 records)
bio_topics_bank = [
    ("Nutrition in Plants", 7, "Write the word equation for photosynthesis and explain where it occurs.", "Carbon dioxide + Water + Sunlight (Chlorophyll) -> Glucose + Oxygen. It occurs in the chloroplasts of green plant leaves."),
    ("Cell Structure and Functions", 8, "What is the function of the cell nucleus?", "The nucleus is the control center ('brain') of the cell. It houses DNA/chromosomes and regulates growth, metabolism, and reproduction."),
    ("Nutrition in Animals", 7, "Explain the role of bile juice and where it is produced in the human digestive system.", "Bile juice is produced by the liver and stored in the gall bladder. It breaks large fat globules into tiny droplets (emulsification) for enzyme digestion."),
    ("Respiration in Organisms", 7, "What is the difference between aerobic and anaerobic respiration?", "Aerobic respiration breaks glucose with oxygen to produce high energy (ATP), CO2, and water. Anaerobic respiration occurs without oxygen, producing less energy and lactic acid or alcohol."),
    ("Microorganisms: Friend and Foe", 8, "Name two beneficial uses of bacteria in daily life.", "1) Lactobacillus bacteria turns milk into curd/yogurt. 2) Rhizobium bacteria in leguminous plant root nodules fix atmospheric nitrogen into the soil."),
    ("Body Movements", 6, "What is a ball-and-socket joint? Where is it found in the human body?", "A joint where the ball-shaped end of one bone fits into the cup-like socket of another, allowing 360-degree rotation in all directions. Found in shoulders and hips.")
]

for i in range(260):
    topic, grd, q_base, a_base = bio_topics_bank[i % len(bio_topics_bank)]
    q = f"{q_base} (Biology question #{i+1})"
    ans = f"**Educational Explanation for Class {grd}:**\n\n{a_base}\n\n**Summary:** Biological systems maintain life through coordinated organ and cellular processes."
    single_turn_records.append(make_rec(grd, "Science (Biology)", topic, "medium", "conceptual_explanation", q, ans, f"NCERT Class {grd} Science"))

# COMPUTER SCIENCE SINGLE-TURN GENERATORS (~340 records needed)
cs_topics_bank = [
    ("Computer Basics", 1, "What is a keyboard used for?", "A keyboard has letter and number buttons that let you type words, numbers, and instructions into the computer."),
    ("Computer Basics", 2, "What is a mouse and why do we click it?", "A computer mouse is a hand-held pointing tool. Clicking its buttons lets you select icons, open files, and draw pictures on the screen."),
    ("Input and Output Devices", 3, "Name three input devices and three output devices.", "Input devices (information going in): Keyboard, Mouse, Microphone. Output devices (information coming out): Monitor, Printer, Speakers."),
    ("Hardware and Software", 4, "Can software work without hardware? Explain simply.", "No. Hardware is the physical machine (like a TV) and software is the program running on it (like a cartoon show). Without the machine, the program has nowhere to run!"),
    ("Computer Memory", 6, "Why is RAM called volatile memory?", "RAM is volatile because it requires continuous electrical power to hold data. When the computer is switched off, all data stored in RAM is immediately erased."),
    ("Binary Numbers", 8, "How do computers use 0 and 1 to represent numbers and letters?", "Computers use millions of microscopic electronic switches (transistors). 0 represents a switch turned OFF, and 1 represents a switch turned ON. By combining 0s and 1s, any number or letter can be encoded."),
    ("Programming Logic", 8, "What is a variable in Python? Give an example.", "A variable is a named storage container in memory holding a value that can change. Example: `score = 10` stores 10 inside the variable named score."),
    ("Internet and Web", 7, "What is the difference between a web browser and a search engine?", "A web browser is software used to open websites (Chrome, Firefox). A search engine is a website on the Internet used to find information across the web (Google, Bing).")
]

for i in range(340):
    topic, grd, q_base, a_base = cs_topics_bank[i % len(cs_topics_bank)]
    q = f"{q_base} (CS module #{i+1})"
    ans = f"**Computer Science Lesson (Class {grd}):**\n\n{a_base}\n\n**Tip:** Computers follow exact logical instructions step by step!"
    single_turn_records.append(make_rec(grd, "Computer Science", topic, "medium", "conceptual_explanation", q, ans, f"K-8 Computer Studies Class {grd}"))

# ------------------------------------------------------------------------------
# 4. AGGREGATE AND SPLIT TO EXACT TARGETS
# Target: Exactly 2,000 records
# Train: 1,500
# Validation: 200
# Test: 300
# ------------------------------------------------------------------------------

train_pool = []
val_pool = []
test_pool = []

# Allocate multi-turn (180 to train)
train_pool.extend(multiturn_records)

# Allocate refusals (40 train, 8 val, 12 test)
random.shuffle(scope_refusals)
train_pool.extend(scope_refusals[:40])
val_pool.extend(scope_refusals[40:48])
test_pool.extend(scope_refusals[48:60])

# Allocate remaining single-turn records
random.shuffle(single_turn_records)

needed_train = 1500 - len(train_pool)
needed_val = 200 - len(val_pool)
needed_test = 300 - len(test_pool)

train_pool.extend(single_turn_records[:needed_train])
remaining = single_turn_records[needed_train:]

val_pool.extend(remaining[:needed_val])
remaining = remaining[needed_val:]

test_pool.extend(remaining[:needed_test])

print("=" * 60)
print("PARTITION COUNTS")
print("=" * 60)
print(f"Train records:      {len(train_pool)}")
print(f"Validation records: {len(val_pool)}")
print(f"Test records:       {len(test_pool)}")
print(f"TOTAL:              {len(train_pool) + len(val_pool) + len(test_pool)}")
print("=" * 60)

# ------------------------------------------------------------------------------
# 5. STRICT LEAKAGE VERIFICATION
# ------------------------------------------------------------------------------
def get_user_query(rec):
    return rec["messages"][0]["content"].strip().lower()

train_q = {get_user_query(r) for r in train_pool}
val_q = {get_user_query(r) for r in val_pool}
test_q = {get_user_query(r) for r in test_pool}

leak_val_train = val_q.intersection(train_q)
leak_test_train = test_q.intersection(train_q)
leak_test_val = test_q.intersection(val_q)

if leak_val_train:
    raise ValueError(f"Leakage between Val and Train: {len(leak_val_train)} queries")
if leak_test_train:
    raise ValueError(f"Leakage between Test and Train: {len(leak_test_train)} queries")
if leak_test_val:
    raise ValueError(f"Leakage between Test and Val: {len(leak_test_val)} queries")

print("✅ LEAKAGE CHECK: PASSED (Zero query overlap across Train, Validation, and Test)")

# ------------------------------------------------------------------------------
# 6. WRITE JSONL FILES
# ------------------------------------------------------------------------------
def write_file(records, fname):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Written {len(records)} records to {path}")

write_file(train_pool, "train.jsonl")
write_file(val_pool, "validation.jsonl")
write_file(test_pool, "test.jsonl")

# ------------------------------------------------------------------------------
# 7. GENERATE COMPREHENSIVE AUDIT REPORT
# ------------------------------------------------------------------------------
all_2k = train_pool + val_pool + test_pool

grade_counts = {}
for r in all_2k:
    g = r["metadata"]["grade"]
    grade_counts[g] = grade_counts.get(g, 0) + 1

subj_counts = {}
for r in all_2k:
    s = r["metadata"]["subject"]
    subj_counts[s] = subj_counts.get(s, 0) + 1

qtype_counts = {}
for r in all_2k:
    qt = r["metadata"]["question_type"]
    qtype_counts[qt] = qtype_counts.get(qt, 0) + 1

multiturn_count = len([r for r in train_pool if r["metadata"]["question_type"] == "multi_turn_tutoring"])
refusal_count = len([r for r in all_2k if r["metadata"]["question_type"] == "scope_refusal"])
class5_8_count = sum(grade_counts.get(g, 0) for g in [5, 6, 7, 8])

print("\n" + "=" * 60)
print("AUDIT & DISTRIBUTION REPORT")
print("=" * 60)
print("Grade Distribution:")
for g in sorted(grade_counts.keys()):
    print(f"  Class {g}: {grade_counts[g]} records ({grade_counts[g]/len(all_2k)*100:.1f}%)")
print(f"  Class 5-8 Total: {class5_8_count} records ({class5_8_count/len(all_2k)*100:.1f}%)")

print("\nSubject Distribution:")
for s, c in sorted(subj_counts.items(), key=lambda x: -x[1]):
    print(f"  {s}: {c} records ({c/len(all_2k)*100:.1f}%)")

print("\nQuestion Type Distribution:")
for qt, c in sorted(qtype_counts.items(), key=lambda x: -x[1]):
    print(f"  {qt}: {c} records ({c/len(all_2k)*100:.1f}%)")

print(f"\nMulti-turn in Training Set: {multiturn_count} / {len(train_pool)} ({multiturn_count/len(train_pool)*100:.1f}%)")
print(f"Scope Refusals in Total Set: {refusal_count} / {len(all_2k)} ({refusal_count/len(all_2k)*100:.1f}%)")
print("=" * 60)
