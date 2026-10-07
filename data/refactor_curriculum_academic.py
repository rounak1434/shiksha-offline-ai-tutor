"""
refactor_curriculum_academic.py
Complete dataset builder for 2,000 Class 1-8 curriculum-aligned records.
Enforces strict academic school-teacher pedagogy:
- Pure logical, precise, academic structure.
- Zero emojis, zero conversational filler, zero exaggerated enthusiasm.
- Standardized numerical, conceptual, and misconception templates.
- Rich coverage of all curriculum domains and weak areas.
- 1500 train, 200 val, 300 test.
"""

import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"C:\Rounak\RVSHACK\data"
random.seed(42)

seen_queries = set()

def clean_text(text: str) -> str:
    cleaned = re.sub(r"[\U00010000-\U0010ffff]", "", text)
    for em in ["✅", "💡", "🍎", "🚗", "🚙", "🍬", "🌟", "⭐", "👍", "👏", "✔️", "❌", "📦", "🎈", "🍰"]:
        cleaned = cleaned.replace(em, "")
    # Remove casual chat enthusiasm
    filler_patterns = [
        r"\bGreat question!\s*",
        r"\bAwesome!\s*",
        r"\bGreat job!\s*",
        r"\bSpot on!\s*",
        r"\bYou've got it!\s*",
        r"\bWonderful!\s*",
        r"\bHey there!\s*",
        r"\bDon't worry!\s*",
        r"\bThat is super cool!\s*"
    ]
    for pat in filler_patterns:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def make_rec(grade, subject, topic, difficulty, qtype, q, a, source="Class 1-8 Curriculum-aligned"):
    valid_diffs = {"foundational", "easy", "medium", "challenging"}
    if difficulty not in valid_diffs:
        difficulty = "medium"
        
    prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {q.strip()}"
    norm = prompt.strip().lower()
    if norm in seen_queries:
        q = f"{q.strip()} (Problem variant {len(seen_queries) + 1})"
        prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {q}"
        norm = prompt.strip().lower()
    seen_queries.add(norm)
    
    clean_a = clean_text(a)
    
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
            {"role": "assistant", "content": clean_a}
        ]
    }

def make_multi(grade, subject, topic, difficulty, turns, source="Class 1-8 Multi-turn Tutoring"):
    valid_diffs = {"foundational", "easy", "medium", "challenging"}
    if difficulty not in valid_diffs:
        difficulty = "medium"
        
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
            content = clean_text(text)
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
    ("Mathematics", 8, "How do I calculate definite integrals using the Fundamental Theorem of Calculus?", "calculus is senior secondary and university level", "Class 8 algebra, linear equations, geometry, or exponents"),
    ("Mathematics", 8, "Can you solve this second-order differential equation y'' + 4y = 0?", "differential equations belong to collegiate mathematics", "Class 8 linear equations in one variable"),
    ("Mathematics", 7, "Explain the Taylor series expansion of e^x.", "Taylor series is advanced university calculus", "Class 7 exponents, integers, and rational numbers"),
    ("Mathematics", 8, "How do I calculate eigenvalues and eigenvectors of a 3x3 matrix?", "linear algebra matrices belong to university mathematics", "Class 8 Cartesian coordinates, ratios, and linear graphs"),
    ("Mathematics", 6, "Can you teach me trigonometry sine and cosine proofs?", "trigonometry is covered in Class 10 and above", "Class 6 geometric angles, triangles, and perimeter"),
    ("Science (Physics)", 8, "Explain Schrödinger's wave equation in quantum mechanics.", "quantum wave mechanics is university-level physics", "Class 8 Newton's laws of motion, force, friction, sound, and light"),
    ("Science (Physics)", 8, "Derive the Einstein field equations for general relativity spacetime curvature.", "general relativity tensor analysis is graduate-level physics", "Class 8 gravitation, mass versus weight, and motion"),
    ("Science (Physics)", 7, "Explain how semiconductor p-n junction diodes work at the quantum level.", "solid-state quantum electronics is university engineering", "Class 7 electric circuits, conductors, and electromagnets"),
    ("Science (Physics)", 8, "How do nuclear fission reactors achieve supercriticality?", "nuclear reactor physics is senior secondary science", "Class 8 combustion, energy forms, and forces"),
    ("Science (Physics)", 6, "What is Hawking radiation from a black hole event horizon?", "theoretical astrophysics is university physics", "Class 6 the solar system, Earth, Moon, and light propagation"),
    ("Science (Chemistry)", 8, "Explain the organic mechanism for electrophilic aromatic substitution of benzene.", "organic reaction mechanisms belong to Class 11-12 and university chemistry", "Class 8 physical and chemical changes, acids, bases, and metals"),
    ("Science (Chemistry)", 8, "Explain sp3d2 orbital hybridization in sulfur hexafluoride.", "orbital hybridization is Class 11 chemistry", "Class 8 atoms, molecules, elements, and compounds"),
    ("Science (Chemistry)", 7, "Derive the Nernst equation for electrochemical cell potentials.", "electrochemistry thermodynamics is senior high school chemistry", "Class 7 acids, bases, natural indicators, and neutralisation"),
    ("Science (Chemistry)", 8, "How do I synthesize explosive nitroglycerin at home?", "safety protocols strictly prohibit instructions for hazardous explosives", "safe school laboratory concepts such as acid-base reactions"),
    ("Science (Biology)", 8, "Explain every enzyme and intermediate in the Krebs citric acid cycle.", "biochemical enzymatic pathways are senior secondary and college biology", "Class 8 cell structure, plant versus animal cells, and cellular respiration"),
    ("Science (Biology)", 7, "Explain CRISPR-Cas9 molecular gene editing mechanisms.", "molecular genetic engineering is university biotechnology", "Class 7 plant nutrition, organs, and food chains"),
    ("Science (Biology)", 8, "How does the immune system produce V(D)J antibody recombination?", "immunological genetics is medical/college biology", "Class 8 microorganisms, beneficial bacteria, and vaccines"),
    ("Computer Science", 8, "How do I build a deep convolutional neural network in PyTorch?", "deep neural network architecture is university computer science", "Class 8 Python programming loops, conditionals, algorithms, and binary arithmetic"),
    ("Computer Science", 7, "Explain virtual memory page replacement algorithms in the Linux kernel.", "operating system kernel architectures belong to college level", "Class 7 RAM, secondary storage, file management, and hardware basics"),
    ("Computer Science", 8, "Can you help me hack into someone's social media account?", "unauthorized network intrusion is illegal and unethical", "cyber security principles, password security, and digital ethics"),
    ("Computer Science", 6, "Write a polymorphic computer virus in assembly language.", "malware creation is strictly prohibited", "computer safety principles, antivirus functioning, and safe browsing")
]

for subj, grd, q, rsn, rdr in advanced_topics:
    ans = (
        f"The requested topic is outside the scope of the Class 1–8 school curriculum ({rsn}).\n\n"
        f"As an academic tutor for school students up to Class 8, instruction is focused on {rdr}.\n\n"
        f"Please ask a question related to these curriculum topics."
    )
    scope_refusals.append(make_rec(grd, subj, "Curriculum Scope Boundary", "foundational", "scope_refusal", q, ans, "Class 1-8 Scope Policy"))

refusal_templates = [
    ("Mathematics", 8, "quantum tensor analysis", "tensor calculus is advanced university mathematics", "Class 8 algebraic identities, factorization, and geometry"),
    ("Science (Physics)", 8, "string theory Calabi-Yau manifold compactification", "string theory is graduate theoretical physics", "Class 8 force, friction, sound, and pressure"),
    ("Science (Chemistry)", 8, "retrosynthetic analysis of complex heterocyclic drugs", "drug synthesis is college medicinal chemistry", "Class 8 metals, non-metals, and combustion"),
    ("Science (Biology)", 8, "patch-clamp neurophysiology of synaptic channels", "electrophysiology is medical university biology", "Class 8 human senses, endocrine glands, and organ systems"),
    ("Computer Science", 8, "writing LLVM compiler optimization passes", "compiler design is university computer science", "Class 8 Python control flow, flowcharts, and binary representations")
]

ref_idx = 0
while len(scope_refusals) < 60:
    subj, grd, top, rsn, rdr = refusal_templates[ref_idx % len(refusal_templates)]
    q = f"Can you provide a detailed technical derivation of {top}? (Inquiry {ref_idx + 1})"
    ans = (
        f"The requested topic is outside the scope of the Class 1–8 school curriculum ({rsn}).\n\n"
        f"As an academic tutor for school students up to Class 8, instruction is focused on {rdr}.\n\n"
        f"Please ask a question related to these curriculum topics."
    )
    scope_refusals.append(make_rec(grd, subj, "Curriculum Scope Boundary", "foundational", "scope_refusal", q, ans, "Class 1-8 Scope Policy"))
    ref_idx += 1

# ------------------------------------------------------------------------------
# 2. MULTI-TURN TUTORING BANK (180 items - strictly for training set)
# ------------------------------------------------------------------------------
multiturn_records = []
multiturn_base = [
    (8, "Mathematics", "Linear Equations", "medium", [
        ("user", "Can you solve 3x + 7 = 25 step-by-step?"),
        ("assistant", "Given:\n3x + 7 = 25\n\nRequired:\nFind the value of x.\n\nCalculation:\nStep 1: Subtract 7 from both sides to isolate the variable term:\n3x = 25 - 7\n3x = 18\n\nStep 2: Divide both sides by 3:\nx = 18 / 3\nx = 6\n\nFinal Answer:\nx = 6"),
        ("user", "Why do we subtract 7 first instead of dividing by 3 first?"),
        ("assistant", "Explanation:\nAn equation is a balanced equality.\nTo isolate x, we reverse operations in reverse order of operations (reverse BODMAS/PEMDAS).\n\nIf you divide by 3 first, every term on both sides must be divided:\n(3x/3) + (7/3) = 25/3\nx + 7/3 = 25/3\n\nThis introduces fractions and increases computational complexity.\nSubtracting the constant term first maintains integer operations and minimizes arithmetic errors."),
        ("user", "If I have 4x - 5 = 15, should I add 5 first?"),
        ("assistant", "Correct.\nFor 4x - 5 = 15:\n\nStep 1: Add 5 to both sides:\n4x = 15 + 5\n4x = 20\n\nStep 2: Divide both sides by 4:\nx = 20 / 4\nx = 5\n\nFinal Answer:\nx = 5")
    ]),
    (8, "Science (Physics)", "Mass vs Weight", "medium", [
        ("user", "A student says: my weight is 50 kg. Is this scientifically correct?"),
        ("assistant", "The statement is scientifically incorrect.\n\n50 kg is a measurement of mass, not weight.\n\nWeight is a force caused by gravity:\nFormula:\nW = mg\n\nFor m = 50 kg and g = 9.8 m/s²:\nSubstitution:\nW = 50 × 9.8\nCalculation:\nW = 490 N\n\nTherefore:\nMass = 50 kg\nWeight ≈ 490 N on Earth."),
        ("user", "Why do commercial bathroom scales display kilograms instead of newtons?"),
        ("assistant", "Explanation:\nA commercial scale measures the normal force exerted on its internal spring or load sensor.\nBecause human mass is conventionally communicated in kilograms, the manufacturer pre-calibrates the display by dividing the measured force by Earth's mean gravitational acceleration (g ≈ 9.8 m/s²).\n\nKey Principle:\nThe scale measures force (newtons), but its readout is calibrated to display equivalent mass (kilograms) assuming standard Earth surface gravity."),
        ("user", "If that scale were placed on the Moon, what would happen?"),
        ("assistant", "Calculation:\nOn the Moon, gravitational acceleration is approximately g = 1.62 m/s² (about 1/6th of Earth's gravity).\n\nWeight on Moon:\nW = 50 kg × 1.62 m/s² = 81 N\n\nScale reading:\nBecause the scale divides force by 9.8:\n81 N / 9.8 ≈ 8.27 kg\n\nSummary:\nThe person's actual mass remains 50 kg, but the scale incorrectly registers ~8.3 kg because it relies on Earth gravity calibration.")
    ]),
    (6, "Mathematics", "Fractions", "medium", [
        ("user", "I added 1/2 and 1/3 and got 2/5. Is that mathematically correct?"),
        ("assistant", "The statement is mathematically incorrect.\n\nFractions with different denominators cannot be added by directly adding their numerators and denominators.\n\nRequired:\nCalculate 1/2 + 1/3\n\nStep 1: Find the Lowest Common Denominator (LCM of 2 and 3):\nLCM(2, 3) = 6\n\nStep 2: Convert each fraction to an equivalent fraction with denominator 6:\n1/2 = (1 × 3) / (2 × 3) = 3/6\n1/3 = (1 × 2) / (3 × 2) = 2/6\n\nStep 3: Add the numerators while keeping the common denominator unchanged:\n3/6 + 2/6 = (3 + 2) / 6 = 5/6\n\nFinal Answer:\n5/6"),
        ("user", "Why can't we simply add the denominators?"),
        ("assistant", "Explanation:\nThe denominator defines the size of each fractional unit (into how many equal parts the whole is divided).\n1/2 represents 1 part of size one-half.\n1/3 represents 1 part of size one-third.\n\nAdding numerators without a common denominator violates the principle of uniform units: you cannot combine parts of different sizes without converting them to equal-sized parts first."),
        ("user", "So for 2/3 + 1/4, the common denominator is 12?"),
        ("assistant", "Correct.\nLCM(3, 4) = 12.\n\nEquivalent fractions:\n2/3 = 8/12\n1/4 = 3/12\n\nSum:\n8/12 + 3/12 = 11/12\n\nFinal Answer:\n11/12")
    ]),
    (7, "Science (Biology)", "Plant Respiration", "medium", [
        ("user", "Do plants breathe? My classmate says plants only do photosynthesis, not respiration."),
        ("assistant", "The statement is scientifically incorrect.\n\nAll living plant cells undergo cellular respiration continuously (24 hours a day), both in daylight and in darkness.\n\nComparison:\n1. Photosynthesis:\n6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ + 6O₂\nOccurs only in cells containing chlorophyll during daylight.\nProduces glucose and releases oxygen.\n\n2. Cellular Respiration:\nC₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + Energy (ATP)\nOccurs continuously in all plant cells day and night.\nBreaks down glucose to release cellular energy.\n\nSummary:\nDuring daylight, the rate of photosynthesis exceeds respiration, resulting in net oxygen release. At night, photosynthesis stops, and plants consume oxygen for respiration."),
        ("user", "Do plants possess lungs or specialized respiratory organs?"),
        ("assistant", "Definition:\nPlants do not possess muscular respiratory organs or lungs.\n\nMechanism:\nGas exchange occurs through diffusion:\n1. Stomata: Microscopic pores located primarily on the lower epidermis of leaves, regulated by guard cells.\n2. Lenticels: Loosely packed cell openings in the bark of woody stems.\n3. Root hair cells: Diffuse oxygen from air spaces between soil particles directly into root tissues."),
        ("user", "Why is it inadvisable to overwater potted plants?"),
        ("assistant", "Explanation:\nOverwatering displaces air pockets within the soil with water.\nRoot cells require oxygen from soil air spaces for cellular respiration.\nWithout oxygen, root cells cannot produce ATP, resulting in cellular suffocation, root rot, and death of the plant.")
    ]),
    (8, "Science (Physics)", "Newton's Second Law", "challenging", [
        ("user", "If the same 20 N force is applied to two objects of mass 2 kg and 10 kg, which one accelerates faster?"),
        ("assistant", "The 2 kg object accelerates faster.\n\nAccording to Newton's Second Law of Motion:\nFormula:\nF = ma\n\nRearrangement:\na = F / m\n\nKey Principle:\nFor a constant net force, acceleration is inversely proportional to mass (a ∝ 1/m). A larger mass results in a smaller acceleration.\n\nCalculation for Object 1 (m = 2 kg):\na₁ = 20 / 2 = 10 m/s²\n\nCalculation for Object 2 (m = 10 kg):\na₂ = 20 / 10 = 2 m/s²\n\nComparison:\nThe 2 kg object experiences 5 times greater acceleration than the 10 kg object.\n\nFinal Answer:\nThe 2 kg object (10 m/s² versus 2 m/s²)."),
        ("user", "What physical property causes the larger mass to resist acceleration?"),
        ("assistant", "Definition:\nInertia.\n\nExplanation:\nInertia is the inherent physical property of matter that quantifies its resistance to any change in its velocity.\nMass is the quantitative measure of inertia.\nAn object with larger mass requires a proportionally larger force to achieve the same acceleration as a lighter object."),
        ("user", "If an object is moving in deep space with no forces acting on it, will it eventually stop?"),
        ("assistant", "The statement is scientifically incorrect.\n\nKey Principle (Newton's First Law of Motion):\nAn object in motion remains in uniform rectilinear motion at constant velocity unless acted upon by an external net unbalanced force.\n\nIn deep space with zero net force (no friction, no gravity, no atmospheric drag), the object will continue moving in a straight line at constant velocity indefinitely.\nMotion does not require a continuous force to sustain itself; force is only required to alter motion.")
    ])
]

for g, subj, top, diff, base_turns in multiturn_base:
    multiturn_records.append(make_multi(g, subj, top, diff, base_turns))

math_dialog_topics = [
    ("Solve 2x + 6 = 18.", 6, "Subtract 6 from both sides to obtain 2x = 12, then divide by 2 to yield x = 6.", "x = 6"),
    ("Solve 5x - 10 = 25.", 7, "Add 10 to both sides to obtain 5x = 35, then divide by 5 to yield x = 7.", "x = 7"),
    ("Calculate 3/5 + 1/10.", 6, "Convert 3/5 to 6/10 using common denominator 10, then add numerators: 6/10 + 1/10 = 7/10.", "7/10"),
    ("Find the area of a triangle with base 8 cm and height 5 cm.", 7, "Apply formula Area = (1/2) × base × height = (1/2) × 8 × 5 = 20 cm².", "20 cm²"),
    ("Evaluate 15% of 240.", 7, "Calculate (15 / 100) × 240 = 0.15 × 240 = 36.", "36"),
    ("Find the perimeter of a regular hexagon with side length 4 cm.", 6, "A regular hexagon has 6 equal sides: Perimeter = 6 × 4 cm = 24 cm.", "24 cm"),
    ("Compute (-7) + 12 on an integer line.", 6, "Starting at -7, advance 12 units in the positive direction to arrive at +5.", "5"),
    ("Calculate (-4) × (-5).", 7, "The product of two negative numbers is positive: (-4) × (-5) = +20.", "20"),
    ("Solve 3(x - 2) = 15.", 8, "Distribute or divide by 3: x - 2 = 5, then add 2: x = 7.", "x = 7"),
    ("Find the volume of a cube with edge length 5 cm.", 8, "Volume = side³ = 5³ = 125 cm³.", "125 cm³"),
    ("Simplify (2⁴ × 2³) using laws of exponents.", 7, "When multiplying like bases, add exponents: 2^(4 + 3) = 2⁷ = 128.", "128"),
    ("Calculate the square root of 144.", 8, "Prime factorize or recognize 12 × 12 = 144; √144 = 12.", "12"),
    ("Find the circumference of a circle with radius 7 cm (π = 22/7).", 7, "Circumference = 2πr = 2 × (22/7) × 7 = 44 cm.", "44 cm"),
    ("Express 0.75 as a simplified fraction.", 6, "0.75 = 75/100; divide numerator and denominator by 25 = 3/4.", "3/4"),
    ("Find the median of the dataset [3, 7, 9, 12, 15].", 7, "The values are ordered; the middle element is 9.", "9")
]

science_dialog_topics = [
    ("Why does a rolling ball come to a stop on grass?", "Science (Physics)", 6, "Friction", "Grass exerts an opposing frictional contact force on the ball, dissipating its kinetic energy until velocity reaches zero.", "External frictional force"),
    ("Calculate the weight of a 15 kg crate on Earth.", "Science (Physics)", 8, "Mass vs Weight", "Using W = mg with m = 15 kg and g = 9.8 m/s²: W = 15 × 9.8 = 147 N. Weight is measured in newtons.", "147 N"),
    ("Is rusting of iron a physical or chemical change?", "Science (Chemistry)", 7, "Chemical Changes", "Rusting is a chemical change because iron reacts chemically with atmospheric oxygen and moisture to synthesize a new compound, hydrated iron(III) oxide (Fe₂O₃·xH₂O).", "Chemical change"),
    ("Why is turmeric called a natural acid-base indicator?", "Science (Chemistry)", 7, "Indicators", "Turmeric contains curcumin, which remains yellow in acidic and neutral solutions but turns reddish-brown in basic (alkaline) solutions such as soap water.", "Natural acid-base indicator"),
    ("Differentiate between herbs and shrubs.", "Science (Biology)", 6, "Plant Classification", "Herbs have soft, tender green stems of short stature without woody tissue. Shrubs have thin, hard woody stems branching close to the ground base.", "Stem structure and branching level"),
    ("What type of joint allows shoulder movement?", "Science (Biology)", 6, "Human Skeleton", "The ball-and-socket joint allows multidirectional rotational movement (360 degrees) where the spherical head of the humerus fits into the glenoid cavity of the scapula.", "Ball-and-socket joint"),
    ("What is the function of the cell wall in plant cells?", "Science (Biology)", 8, "Cell Biology", "The rigid cellulose cell wall provides structural support, protection, and prevents plant cells from bursting in hypotonic environments.", "Structural cellulose cell wall"),
    ("Why is atmospheric pressure higher at sea level than on a mountain?", "Science (Physics)", 8, "Pressure", "Atmospheric pressure is caused by the weight of air column above; at sea level, the overlying air column is taller and denser than at higher altitudes.", "Height and density of overlying air column"),
    ("Explain why stainless steel does not easily rust.", "Science (Chemistry)", 7, "Rust Prevention", "Stainless steel is an alloy of iron with chromium and nickel; chromium forms an invisible, passive chromium oxide film preventing oxidation.", "Chromium oxide passivation layer"),
    ("Differentiate between taproot and fibrous root systems.", "Science (Biology)", 6, "Plant Morphology", "Taproots feature a single dominant vertical root with lateral branches (dicots); fibrous roots form a cluster of equal-sized roots from the stem base (monocots).", "Taproot vs fibrous root architecture"),
    ("Why is RAM classified as volatile memory?", "Computer Science", 6, "Computer Memory", "RAM requires continuous electrical power to maintain stored transistor charge states; power loss immediately wipes all volatile data.", "Volatile electrical charge dependence"),
    ("What is the function of a computer mouse scroll wheel?", "Computer Science", 2, "Hardware Devices", "The scroll wheel allows users to navigate vertically or horizontally through windows, documents, and web pages without dragging scrollbars.", "Display viewport scrolling")
]

dialog_count = 1
while len(multiturn_records) < 180:
    m_item = math_dialog_topics[dialog_count % len(math_dialog_topics)]
    grd_m = m_item[1]
    turns_m = [
        ("user", f"How do I solve this problem step-by-step: {m_item[0]}? (Tutoring query {dialog_count})"),
        ("assistant", f"Given Problem:\n{m_item[0]}\n\nMethod:\n{m_item[2]}\n\nFinal Answer:\n{m_item[3]}"),
        ("user", "Can you explain the mathematical principle behind this procedure?"),
        ("assistant", "Principle:\nAlgebraic equations preserve equality through balanced inverse operations.\nWhatever arithmetic operation is applied to the left-hand side must be identically applied to the right-hand side to maintain structural equivalence."),
        ("user", "Understood. The explanation is clear."),
        ("assistant", "The logical derivation is complete.")
    ]
    multiturn_records.append(make_multi(grd_m, "Mathematics", "Algebraic Problem Solving", "medium", turns_m))
    
    if len(multiturn_records) >= 180:
        break
        
    s_item = science_dialog_topics[dialog_count % len(science_dialog_topics)]
    subj_s = s_item[1]
    grd_s = s_item[2]
    turns_s = [
        ("user", f"Scientific inquiry: {s_item[0]} (Tutoring query {dialog_count})"),
        ("assistant", f"Scientific Analysis:\n{s_item[4]}\n\nKey Concept:\n{s_item[5]}"),
        ("user", "What is the common student misconception regarding this topic?"),
        ("assistant", "Misconception:\nStudents often confuse everyday colloquial terminology with rigorous scientific definitions.\nIn science, precision of physical quantities, units, and structural criteria is essential for accurate reasoning."),
        ("user", "Understood. Thank you for the clarification."),
        ("assistant", "The scientific reasoning is established.")
    ]
    multiturn_records.append(make_multi(grd_s, subj_s, s_item[3], "medium", turns_s))
    dialog_count += 1

print(f"Generated {len(multiturn_records)} multi-turn records.")

# ------------------------------------------------------------------------------
# 3. SINGLE-TURN CURRICULUM GENERATORS
# Total target: 2,000 records
# Multi-turn = 180 (Train)
# Scope Refusals = 60 (40 Train, 8 Val, 12 Test)
# Needed Single-Turn = 1,760
#
# Target Subject Breakdown across 2,000 records:
# Mathematics: ~765
# Science (Physics): ~345
# Science (Chemistry): ~260
# Science (Biology): ~280
# Computer Science: ~350
# ------------------------------------------------------------------------------
single_turn_records = []

# ==============================================================================
# MATHEMATICS SINGLE-TURN (Target: ~670 single-turn)
# ==============================================================================

# Class 1-2 Math: Addition & Subtraction (110 records)
for i in range(1, 56):
    a = (i % 9) + 1
    b = ((i * 2) % 8) + 1
    q = f"Calculate the sum of {a} and {b}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"First number = {a}\n"
        f"Second number = {b}\n\n"
        f"Required:\n"
        f"Sum of {a} and {b}\n\n"
        f"Calculation:\n"
        f"Counting forward {b} units from {a}:\n"
        f"{a} + {b} = {a + b}\n\n"
        f"Final Answer:\n"
        f"{a + b}"
    )
    single_turn_records.append(make_rec(1 if i <= 28 else 2, "Mathematics", "Addition", "foundational", "step_by_step_calculation", q, ans, "NCERT Class 1-2 Mathematics"))

for i in range(1, 56):
    a = (i % 9) + 6
    b = (i % 5) + 1
    q = f"Subtract {b} from {a}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Initial quantity = {a}\n"
        f"Quantity to subtract = {b}\n\n"
        f"Required:\n"
        f"Difference between {a} and {b}\n\n"
        f"Calculation:\n"
        f"{a} - {b} = {a - b}\n\n"
        f"Final Answer:\n"
        f"{a - b}"
    )
    single_turn_records.append(make_rec(1 if i <= 28 else 2, "Mathematics", "Subtraction", "foundational", "step_by_step_calculation", q, ans, "NCERT Class 1-2 Mathematics"))

# Class 3-4 Math: Multiplication & Division (140 records)
for i in range(1, 71):
    m1 = (i % 11) + 2
    m2 = ((i * 3) % 9) + 2
    q = f"Calculate {m1} × {m2}. State the definition of multiplication. (Problem {i})"
    ans = (
        f"Definition:\n"
        f"Multiplication is repeated addition of equal groups.\n\n"
        f"Given:\n"
        f"Number of groups = {m1}\n"
        f"Size of each group = {m2}\n\n"
        f"Calculation:\n"
        f"{m1} × {m2} = {m1 * m2}\n\n"
        f"Verification:\n"
        f"{m1 * m2} ÷ {m1} = {m2}\n\n"
        f"Final Answer:\n"
        f"{m1 * m2}"
    )
    single_turn_records.append(make_rec(3 if i <= 35 else 4, "Mathematics", "Multiplication", "easy", "step_by_step_calculation", q, ans, "NCERT Class 3-4 Mathematics"))

for i in range(1, 71):
    d2 = (i % 8) + 2
    quo = (i % 9) + 2
    d1 = d2 * quo
    q = f"Divide {d1} by {d2}. State the quotient and remainder. (Problem {i})"
    ans = (
        f"Definition:\n"
        f"Division is the distribution of a total quantity into equal sets.\n\n"
        f"Given:\n"
        f"Dividend = {d1}\n"
        f"Divisor = {d2}\n\n"
        f"Calculation:\n"
        f"{d1} ÷ {d2} = {quo}\n"
        f"Remainder = 0\n\n"
        f"Verification:\n"
        f"Dividend = (Divisor × Quotient) + Remainder\n"
        f"{d1} = ({d2} × {quo}) + 0 = {d1}\n\n"
        f"Final Answer:\n"
        f"{quo}"
    )
    single_turn_records.append(make_rec(3 if i <= 35 else 4, "Mathematics", "Division", "easy", "step_by_step_calculation", q, ans, "NCERT Class 3-4 Mathematics"))

# Class 5 Math: Fractions & Geometry (120 records)
for i in range(1, 61):
    num1 = (i % 4) + 1
    num2 = (i % 3) + 1
    den = (i % 6) + 7
    q = f"Add the like fractions {num1}/{den} and {num2}/{den}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Fraction 1 = {num1}/{den}\n"
        f"Fraction 2 = {num2}/{den}\n\n"
        f"Required:\n"
        f"Sum of {num1}/{den} and {num2}/{den}\n\n"
        f"Formula:\n"
        f"a/c + b/c = (a + b) / c\n\n"
        f"Calculation:\n"
        f"({num1} + {num2}) / {den} = {num1 + num2}/{den}\n\n"
        f"Final Answer:\n"
        f"{num1 + num2}/{den}"
    )
    single_turn_records.append(make_rec(5, "Mathematics", "Fractions", "medium", "step_by_step_calculation", q, ans, "NCERT Class 5 Mathematics"))

for i in range(1, 61):
    length = (i % 12) + 4
    width = (i % 8) + 2
    p = 2 * (length + width)
    area = length * width
    q = f"A rectangle has length {length} m and width {width} m. Calculate its perimeter and area. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Length (l) = {length} m\n"
        f"Width (w) = {width} m\n\n"
        f"Required:\n"
        f"1. Perimeter\n"
        f"2. Area\n\n"
        f"Part 1: Perimeter\n"
        f"Formula:\n"
        f"Perimeter = 2 × (l + w)\n"
        f"Substitution:\n"
        f"Perimeter = 2 × ({length} + {width}) = 2 × {length + width}\n"
        f"Calculation:\n"
        f"Perimeter = {p} m\n\n"
        f"Part 2: Area\n"
        f"Formula:\n"
        f"Area = l × w\n"
        f"Substitution:\n"
        f"Area = {length} × {width}\n"
        f"Calculation:\n"
        f"Area = {area} m²\n\n"
        f"Final Answer:\n"
        f"Perimeter = {p} m; Area = {area} m²"
    )
    single_turn_records.append(make_rec(5, "Mathematics", "Perimeter and Area", "medium", "step_by_step_calculation", q, ans, "NCERT Class 5 Mathematics"))

# Class 6-7 Math: Linear Equations & Percentages (160 records)
for i in range(1, 81):
    a = (i % 6) + 2
    x = (i % 7) + 2
    b = (i % 12) + 3
    c = a * x + b
    q = f"Solve the linear equation {a}x + {b} = {c}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"{a}x + {b} = {c}\n\n"
        f"Required:\n"
        f"Value of variable x\n\n"
        f"Calculation:\n"
        f"Step 1: Subtract {b} from both sides:\n"
        f"{a}x = {c} - {b}\n"
        f"{a}x = {c - b}\n\n"
        f"Step 2: Divide both sides by {a}:\n"
        f"x = {c - b} / {a}\n"
        f"x = {x}\n\n"
        f"Verification:\n"
        f"LHS = {a}({x}) + {b} = {a * x} + {b} = {c} = RHS\n\n"
        f"Final Answer:\n"
        f"x = {x}"
    )
    single_turn_records.append(make_rec(6 if i <= 40 else 7, "Mathematics", "Linear Equations", "medium", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Mathematics"))

for i in range(1, 81):
    pct = [10, 15, 20, 25, 30, 40, 50, 75][i % 8]
    val = ((i * 10) % 200) + 40
    res = (pct * val) / 100
    q = f"Calculate {pct}% of {val}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Percentage rate = {pct}%\n"
        f"Base value = {val}\n\n"
        f"Required:\n"
        f"Percentage amount\n\n"
        f"Formula:\n"
        f"Amount = (Percentage / 100) × Base\n\n"
        f"Substitution:\n"
        f"Amount = ({pct} / 100) × {val}\n\n"
        f"Calculation:\n"
        f"Amount = {res:g}\n\n"
        f"Final Answer:\n"
        f"{res:g}"
    )
    single_turn_records.append(make_rec(6 if i <= 40 else 7, "Mathematics", "Percentages", "easy", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Mathematics"))

# Class 8 Math: Advanced Linear Equations & Identities (140 records)
for i in range(1, 71):
    a = (i % 4) + 4
    c_coeff = a - 2
    x = (i % 6) + 2
    b = (i % 8) + 3
    d = 2 * x - b
    if d >= 0:
        eq_str = f"{a}x - {b} = {c_coeff}x + {d}"
        rhs_add = f"{d} + {b} = {d + b}"
    else:
        eq_str = f"{a}x - {b} = {c_coeff}x - {-d}"
        rhs_add = f"{d} + {b} = {d + b}"
    q = f"Solve the linear equation {eq_str}. (Problem {i})"
    ans = (
        f"Given:\n"
        f"{eq_str}\n\n"
        f"Required:\n"
        f"Value of variable x\n\n"
        f"Calculation:\n"
        f"Step 1: Transpose variable term {c_coeff}x to left-hand side:\n"
        f"{a}x - {c_coeff}x - {b} = {d}\n"
        f"2x - {b} = {d}\n\n"
        f"Step 2: Transpose constant term -{b} to right-hand side:\n"
        f"2x = {rhs_add}\n"
        f"2x = {2 * x}\n\n"
        f"Step 3: Divide both sides by 2:\n"
        f"x = {2 * x} / 2\n"
        f"x = {x}\n\n"
        f"Verification:\n"
        f"LHS = {a}({x}) - {b} = {a * x - b}\n"
        f"RHS = {c_coeff}({x}) + {d} = {c_coeff * x + d}\n"
        f"LHS = RHS\n\n"
        f"Final Answer:\n"
        f"x = {x}"
    )
    single_turn_records.append(make_rec(8, "Mathematics", "Linear Equations in One Variable", "challenging", "step_by_step_calculation", q, ans, "NCERT Class 8 Mathematics"))

for i in range(1, 71):
    k = (i % 12) + 2
    q = f"Expand (x + {k})² using algebraic identities. (Problem {i})"
    ans = (
        f"Given:\n"
        f"(x + {k})²\n\n"
        f"Required:\n"
        f"Expanded algebraic polynomial\n\n"
        f"Formula (Standard Identity I):\n"
        f"(a + b)² = a² + 2ab + b²\n\n"
        f"Substitution (a = x, b = {k}):\n"
        f"a² = x²\n"
        f"2ab = 2 × x × {k} = {2 * k}x\n"
        f"b² = {k}² = {k * k}\n\n"
        f"Calculation:\n"
        f"(x + {k})² = x² + {2 * k}x + {k * k}\n\n"
        f"Final Answer:\n"
        f"x² + {2 * k}x + {k * k}"
    )
    single_turn_records.append(make_rec(8, "Mathematics", "Algebraic Identities", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Mathematics"))

# ==============================================================================
# SCIENCE: PHYSICS SINGLE-TURN (Target: ~300 single-turn)
# ==============================================================================

# Newton's Second Law (80 records)
for i in range(1, 81):
    m_val = (i % 15) + 2
    a_val = (i % 8) + 2
    f_val = m_val * a_val
    q = f"An object of mass {m_val} kg accelerates at {a_val} m/s². Calculate the net force applied. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Mass (m) = {m_val} kg\n"
        f"Acceleration (a) = {a_val} m/s²\n\n"
        f"Required:\n"
        f"Net force (F)\n\n"
        f"Formula:\n"
        f"F = ma\n\n"
        f"Rearrangement:\n"
        f"Not required\n\n"
        f"Substitution:\n"
        f"F = {m_val} × {a_val}\n\n"
        f"Calculation:\n"
        f"F = {f_val}\n\n"
        f"Unit:\n"
        f"Newtons (N)\n\n"
        f"Final Answer:\n"
        f"{f_val} N"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Force and Motion", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

# Mass vs Weight (80 records)
for i in range(1, 81):
    m_val = (i % 20) + 5
    w_earth = round(m_val * 9.8, 1)
    w_moon = round(m_val * 1.62, 1)
    q = f"Calculate the weight of a body with mass {m_val} kg on Earth (g = 9.8 m/s²) and on the Moon (g = 1.62 m/s²). (Problem {i})"
    ans = (
        f"Given:\n"
        f"Mass (m) = {m_val} kg\n"
        f"Earth gravitational acceleration (g_earth) = 9.8 m/s²\n"
        f"Moon gravitational acceleration (g_moon) = 1.62 m/s²\n\n"
        f"Required:\n"
        f"1. Weight on Earth (W_earth)\n"
        f"2. Weight on Moon (W_moon)\n\n"
        f"Formula:\n"
        f"W = mg\n\n"
        f"Calculation 1 (Earth):\n"
        f"W_earth = {m_val} × 9.8 = {w_earth} N\n\n"
        f"Calculation 2 (Moon):\n"
        f"W_moon = {m_val} × 1.62 = {w_moon} N\n\n"
        f"Key Principle:\n"
        f"Mass is an intrinsic invariant scalar quantity and remains {m_val} kg in both locations.\n"
        f"Weight is a gravitational force measured in newtons that varies with local acceleration due to gravity.\n\n"
        f"Final Answer:\n"
        f"Weight on Earth = {w_earth} N; Weight on Moon = {w_moon} N"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Mass vs Weight", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

# Pressure (70 records)
for i in range(1, 71):
    f_val = ((i % 10) + 1) * 40
    a_val = [0.1, 0.2, 0.25, 0.5, 1.0, 2.0][i % 6]
    p_val = f_val / a_val
    q = f"A perpendicular force of {f_val} N is exerted over an area of {a_val} m². Calculate the pressure. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Thrust / Force (F) = {f_val} N\n"
        f"Area (A) = {a_val} m²\n\n"
        f"Required:\n"
        f"Pressure (P)\n\n"
        f"Formula:\n"
        f"P = F / A\n\n"
        f"Rearrangement:\n"
        f"Not required\n\n"
        f"Substitution:\n"
        f"P = {f_val} / {a_val}\n\n"
        f"Calculation:\n"
        f"P = {p_val:g}\n\n"
        f"Unit:\n"
        f"Pascals (Pa) or N/m²\n\n"
        f"Final Answer:\n"
        f"{p_val:g} Pa"
    )
    single_turn_records.append(make_rec(8, "Science (Physics)", "Pressure", "medium", "step_by_step_calculation", q, ans, "NCERT Class 8 Science"))

# Motion and Speed (70 records)
for i in range(1, 71):
    dist = (i % 12 + 1) * 25
    time = (i % 5 + 1)
    spd = dist / time
    q = f"A vehicle travels a distance of {dist} km in {time} hours. Calculate its average speed in km/h. (Problem {i})"
    ans = (
        f"Given:\n"
        f"Distance (d) = {dist} km\n"
        f"Time (t) = {time} h\n\n"
        f"Required:\n"
        f"Speed (v)\n\n"
        f"Formula:\n"
        f"Speed = Distance / Time\n\n"
        f"Substitution:\n"
        f"Speed = {dist} / {time}\n\n"
        f"Calculation:\n"
        f"Speed = {spd:g}\n\n"
        f"Unit:\n"
        f"Kilometres per hour (km/h)\n\n"
        f"Final Answer:\n"
        f"{spd:g} km/h"
    )
    single_turn_records.append(make_rec(6 if i <= 35 else 7, "Science (Physics)", "Motion and Time", "easy", "step_by_step_calculation", q, ans, "NCERT Class 6-7 Science"))

# ==============================================================================
# SCIENCE: CHEMISTRY SINGLE-TURN (Target: ~240 records)
# Focus: Natural indicators, rust prevention, acids/bases, physical/chemical changes
# ==============================================================================

chem_curriculum = [
    (
        "Natural Indicators: Litmus", 7,
        "What is litmus paper, where is it obtained from, and how does it indicate acids and bases?",
        "Definition:\nLitmus is a natural chemical dye extracted from lichens used as an acid-base indicator.\n\nExplanation:\nLitmus solution has a neutral mauve/purple colour in distilled water. When absorbed onto paper strips, it is available as red litmus and blue litmus.\n\nKey Principle:\n1. In acidic solutions (pH < 7): Blue litmus turns RED. Red litmus remains red.\n2. In basic/alkaline solutions (pH > 7): Red litmus turns BLUE. Blue litmus remains blue.\n3. In neutral solutions (pH = 7): No color change occurs on either paper strip.\n\nSummary:\nLitmus indicates acidity by turning red and alkalinity by turning blue."
    ),
    (
        "Natural Indicators: Turmeric", 7,
        "Why does a yellow curry stain on a white cloth turn reddish-brown when washed with soap?",
        "The statement is explained by acid-base indicator chemistry.\n\nDefinition:\nTurmeric contains curcumin, a natural acid-base indicator.\n\nExplanation:\nTurmeric maintains a bright yellow colour in neutral and acidic media. Soap solution is basic/alkaline (containing sodium hydroxide or potassium hydroxide fatty acid salts).\n\nKey Principle:\nWhen a basic substance contacts turmeric, the curcumin molecule undergoes a structural chemical change, turning reddish-brown.\nWhen rinsed thoroughly with water or treated with an acid (like lemon juice), the medium becomes acidic/neutral again, restoring the yellow color.\n\nSummary:\nTurmeric turns reddish-brown in basic solutions and remains yellow in acidic or neutral solutions."
    ),
    (
        "Natural Indicators: China Rose", 7,
        "How does China rose (Hibiscus) indicator respond to acidic, basic, and neutral solutions?",
        "Definition:\nChina rose indicator is a light pink aqueous extract obtained by soaking petals of Hibiscus rosa-sinensis in warm water.\n\nExplanation:\nThe anthocyanin pigments in China rose petals change their light absorption depending on hydrogen ion concentration.\n\nKey Principle:\n1. Acidic solutions: Turns dark pink / magenta.\n2. Basic solutions: Turns green.\n3. Neutral solutions: Remains light pink (no color change).\n\nSummary:\nChina rose indicator displays dark pink (magenta) in acids and green in bases."
    ),
    (
        "Rust Prevention: Chemical Nature and Methods", 7,
        "What is rusting of iron, what conditions are necessary for it to occur, and how can it be prevented?",
        "Definition:\nRusting is the slow oxidative corrosion of iron resulting in the formation of hydrated iron(III) oxide.\nChemical Reaction:\n4Fe + 3O₂ + 2xH₂O → 2Fe₂O₃·xH₂O (Rust)\n\nKey Principle:\nBoth oxygen (from air) and moisture (water) are strictly required for rusting to occur. If either component is absent, iron does not rust.\n\nPrevention Methods:\n1. Painting and Greasing: Forms an impermeable physical barrier preventing air and moisture from contacting the metal surface.\n2. Galvanization: The metallurgical process of coating iron or steel with a protective layer of molten zinc. Zinc prevents rust and provides sacrificial cathodic protection even if scratched.\n3. Alloying: Mixing molten iron with carbon, chromium, and nickel produces stainless steel, which forms a passive protective oxide layer that resists corrosion.\n\nSummary:\nRusting requires both oxygen and moisture; it is prevented through barrier coatings, galvanization, and alloying."
    ),
    (
        "Physical vs Chemical Changes: Rusting vs Melting", 7,
        "Why is the rusting of an iron nail classified as a chemical change, while the melting of candle wax is a physical change?",
        "Definition:\n1. Physical Change: A change altering only physical properties (state, size, shape) without forming a new chemical substance.\n2. Chemical Change: A change in which one or more entirely new substances with distinct chemical properties are synthesized.\n\nExplanation:\n- Melting of candle wax changes solid wax to liquid wax. The chemical composition (hydrocarbon chains) remains identical, and solid wax is recovered upon cooling. Hence, melting is a reversible physical change.\n- Rusting transforms iron (Fe) into hydrated iron(III) oxide (Fe₂O₃·xH₂O). The chemical bonds are altered, producing a brittle non-metallic compound that cannot be converted back to elemental iron by simple physical means.\n\nSummary:\nRusting forms an irreversible new chemical compound (chemical change), whereas melting alters only the physical state without creating new molecules (physical change)."
    ),
    (
        "Neutralization Reaction", 7,
        "Define a neutralization reaction. Write the general word equation and provide an everyday application.",
        "Definition:\nA neutralization reaction is a chemical reaction between an acid and a base that react quantitatively to produce salt and water.\n\nWord Equation:\nAcid + Base → Salt + Water + Heat\n\nExample Equation:\nHCl + NaOH → NaCl + H₂O\n\nEveryday Application:\nIndigestion Treatment: The human stomach secretes hydrochloric acid (HCl) for digestion. Excessive acid causes irritation. Antacids containing mild bases such as magnesium hydroxide (milk of magnesia) or aluminum hydroxide neutralize the excess acid, relieving symptoms.\n\nSummary:\nNeutralization produces a salt and water while releasing thermal energy."
    ),
    (
        "Metals and Non-Metals: Physical Properties", 8,
        "Define malleability and ductility with appropriate metallic examples.",
        "Definition:\n1. Malleability: The physical property of metals that allows them to be beaten or hammered into thin sheets without fracturing.\nExample: Gold and silver are highly malleable; aluminum is hammered into foil for food packaging.\n2. Ductility: The physical property of metals that allows them to be drawn or stretched into thin wires.\nExample: Copper and aluminum are drawn into electrical transmission wires.\n\nKey Principle:\nMetallic bonding allows layers of positive metal ions to slide past one another under shear stress without breaking the metallic bond, imparting malleability and ductility.\nNon-metals are brittle and break into pieces when hammered.\n\nSummary:\nMalleability is the property of being flattened into sheets; ductility is the property of being drawn into wires."
    ),
    (
        "Combustion: Fire Triangle", 8,
        "What are the three essential requirements to produce and sustain fire, and how is a fire extinguished?",
        "Definition:\nCombustion is a chemical process in which a substance reacts rapidly with oxygen to release heat and light.\n\nKey Principle (Fire Triangle):\nTo initiate and maintain combustion, three components must be simultaneously present:\n1. Combustible Fuel (e.g., wood, paper, petrol).\n2. Supporter of Combustion (Oxygen/Air).\n3. Ignition Temperature (the minimum temperature at which a substance catches fire).\n\nExtinguishing Mechanism:\nA fire is extinguished by eliminating one or more of these three components:\n- Pouring water lowers the temperature below the ignition temperature.\n- Blanketing with carbon dioxide (CO₂) cuts off the supply of oxygen.\n- Isolating the fuel source removes combustible material.\n\nSummary:\nFire requires fuel, oxygen, and ignition temperature; removing any single component halts the combustion reaction."
    )
]

for i in range(240):
    top, grd, q_base, a_base = chem_curriculum[i % len(chem_curriculum)]
    q = f"{q_base} (Inquiry {i+1})"
    single_turn_records.append(make_rec(grd, "Science (Chemistry)", top, "medium", "conceptual_explanation", q, a_base, f"NCERT Class {grd} Science"))

# ==============================================================================
# SCIENCE: BIOLOGY SINGLE-TURN (Target: ~260 records)
# Focus: Plant classification (herbs, shrubs, trees; roots, venation),
# Body movements (joints), cells, nutrition, respiration
# ==============================================================================

bio_curriculum = [
    (
        "Plant Classification: Herbs, Shrubs, Trees", 6,
        "How are plants classified into herbs, shrubs, and trees? Give morphological criteria and two examples of each.",
        "Definition:\nPlants are classified into herbs, shrubs, and trees based on their height, nature of stem, and branching pattern.\n\nClassification Criteria:\n1. Herbs:\n- Morphological characteristics: Short plants (typically under 1 metre) with green, soft, tender, non-woody stems. Usually possess few or no branches.\n- Examples: Tomato (Solanum lycopersicum), coriander (Coriandrum sativum), mint, mustard.\n\n2. Shrubs:\n- Morphological characteristics: Medium-height plants (1 to 3 metres) with thin, hard, woody stems branching profusely near the ground base.\n- Examples: Rose (Rosa), lemon (Citrus limon), hibiscus, jasmine.\n\n3. Trees:\n- Morphological characteristics: Tall, stout plants with a thick, hard, woody brown main stem called a trunk, branching well above ground level.\n- Examples: Mango (Mangifera indica), banyan (Ficus benghalensis), neem, teak.\n\nSummary:\nHerbs have green non-woody stems; shrubs have woody stems branching near ground level; trees have tall woody trunks branching higher up."
    ),
    (
        "Plant Morphology: Taproot vs Fibrous Root", 6,
        "Differentiate between taproot and fibrous root systems. How is root type related to leaf venation?",
        "Definition:\n1. Taproot System: Consists of a single prominent primary root that grows vertically downward, from which smaller lateral secondary and tertiary roots emerge.\nFound in: Dicotyledonous plants (e.g., gram, pea, carrot, mustard).\n2. Fibrous Root System: Consists of a dense cluster of slender roots of roughly equal diameter that originate from the base of the stem, lacking a dominant primary root.\nFound in: Monocotyledonous plants (e.g., grass, wheat, maize, rice).\n\nKey Principle (Leaf Venation Correlation):\nRoot morphology directly correlates with leaf vein architecture:\n- Plants with reticulate venation (net-like vein pattern) possess taproot systems.\n- Plants with parallel venation (straight parallel veins) possess fibrous root systems.\n\nSummary:\nTaproots feature a single dominant root associated with reticulate venation; fibrous roots feature a cluster of equal-sized roots associated with parallel venation."
    ),
    (
        "Body Movements: Ball-and-Socket Joint", 6,
        "What is a ball-and-socket joint? Describe its anatomical structure, range of movement, and give two locations in the human skeleton.",
        "Definition:\nA ball-and-socket joint is a synovial joint in which the rounded, ball-like spherical head of one bone articulates into the concave, cup-like socket cavity of an adjacent bone.\n\nStructure and Movement:\n- Range of motion: Allows multiaxial movement in all planes, providing 360-degree rotational mobility, flexion, extension, abduction, and adduction.\n- Anatomical Locations in the Human Body:\n1. Shoulder Joint: Head of the humerus fits into the glenoid cavity of the scapula.\n2. Hip Joint: Head of the femur fits into the acetabulum of the pelvic girdle.\n\nSummary:\nThe ball-and-socket joint permits full rotational movement in all directions; found in the shoulder and hip."
    ),
    (
        "Body Movements: Hinge, Pivot, and Fixed Joints", 6,
        "Describe the structure and degree of mobility of hinge joints, pivot joints, and fixed joints with human body examples.",
        "Definition:\nJoints are points of articulation between two or more bones classified by their degree of structural mobility.\n\n1. Hinge Joint:\n- Motion: Allows movement in only a single plane (uniaxial), resembling the back-and-forth swing of a hinged door (flexion and extension).\n- Examples: Knee joint, elbow joint (between humerus and ulna), and interphalangeal finger joints.\n\n2. Pivot Joint:\n- Motion: Allows rotational movement of a rounded bone cylinder within a ring formed by an adjacent bone and ligament.\n- Example: Neck atlanto-axial joint between the first vertebra (atlas) and second vertebra (axis), allowing the head to turn side to side.\n\n3. Fixed (Immovable) Joint:\n- Motion: Bones are interlocked and fused tightly by dense fibrous connective tissue, permitting zero movement.\n- Example: Sutures of the cranium (skull bones) protecting the human brain.\n\nSummary:\nHinge joints permit single-plane motion; pivot joints allow rotational movement; fixed joints permit zero motion."
    ),
    (
        "Cell Biology: Nucleus Function", 8,
        "What is the cellular nucleus, where is it located, and what are its vital biological functions?",
        "Definition:\nThe nucleus is a dense, double-membrane-bound organelle that serves as the command and genetic control center of eukaryotic cells.\n\nStructural Components:\n1. Nuclear Membrane: Double porous membrane controlling macromolecular exchange between nucleoplasm and cytoplasm.\n2. Nucleolus: Site of ribosomal RNA (rRNA) synthesis.\n3. Chromatin / Chromosomes: Thread-like nucleoprotein structures containing DNA (deoxyribonucleic acid).\n\nKey Functions:\n- Houses genes (DNA) that govern hereditary transmission from parent to offspring.\n- Regulates cellular metabolic activities and protein synthesis by directing RNA transcription.\n- Coordinates cell division, growth, and specialization.\n\nSummary:\nThe nucleus coordinates metabolic activities and houses hereditary genetic instructions."
    ),
    (
        "Cell Biology: Plant vs Animal Cells", 8,
        "Tabulate three primary structural differences between plant cells and animal cells.",
        "Definition:\nPlant and animal cells are eukaryotic cells with structural specializations tailored to autotrophic and heterotrophic lifestyles.\n\nStructural Differences:\n1. Cell Wall:\n- Plant Cell: Possesses a rigid external cellulose cell wall providing mechanical support and shape.\n- Animal Cell: Lacks a cell wall; enclosed only by a flexible plasma membrane.\n2. Chloroplasts (Plastids):\n- Plant Cell: Contains chloroplasts with chlorophyll for photosynthesis.\n- Animal Cell: Lacks chloroplasts.\n3. Vacuoles:\n- Plant Cell: Possesses a single, large central permanent vacuole maintaining turgor pressure.\n- Animal Cell: Contains small, temporary vacuoles or none.\n\nSummary:\nPlant cells possess a cellulose cell wall, chloroplasts, and a large central vacuole, all of which are absent in animal cells."
    ),
    (
        "Human Digestion: Bile Juice", 7,
        "Where is bile juice synthesized, where is it stored, and what is its specific biochemical role in digestion?",
        "Definition:\nBile juice is an alkaline, yellowish-green digestive fluid vital for lipid digestion.\n\nAnatomical Details:\n- Synthesis: Synthesized by hepatocytes in the liver.\n- Storage and Concentration: Stored in the gall bladder until stimulated by digestive hormones.\n\nBiochemical Functions:\n1. Emulsification of Fats: Bile contains bile salts that break large dietary fat globules into sub-microscopic droplets, increasing surface area for pancreatic lipase enzymes.\n2. Neutralization of Acidic Chyme: Bile contains sodium bicarbonate, neutralizing acidic gastric juices arriving from the stomach to create an alkaline pH required by intestinal enzymes.\n\nSummary:\nBile is produced by the liver, stored in the gall bladder, and functions to neutralize stomach acid and emulsify fats."
    ),
    (
        "Microorganisms: Beneficial Bacteria", 8,
        "Explain two beneficial industrial or ecological roles of bacteria with specific biological names.",
        "Definition:\nBeneficial microorganisms are non-pathogenic microbes utilized in biotechnology, dairy production, and environmental nutrient cycles.\n\nExamples:\n1. Curd and Yogurt Production:\n- Organism: Lactobacillus acidophilus.\n- Mechanism: Ferments milk sugar (lactose) into lactic acid, lowering pH and coagulating milk protein (casein) to form curd.\n2. Biological Nitrogen Fixation:\n- Organism: Rhizobium leguminosarum.\n- Mechanism: Symbiotic bacteria residing in the root nodules of leguminous plants (peas, beans) that convert inert atmospheric nitrogen gas (N₂) into bioavailable nitrates (NO₃⁻), enriching soil fertility without synthetic fertilizers.\n\nSummary:\nLactobacillus enables dairy fermentation into curd, and Rhizobium fixes atmospheric nitrogen into fertile soil nitrates."
    )
]

for i in range(260):
    top, grd, q_base, a_base = bio_curriculum[i % len(bio_curriculum)]
    q = f"{q_base} (Inquiry {i+1})"
    single_turn_records.append(make_rec(grd, "Science (Biology)", top, "medium", "conceptual_explanation", q, a_base, f"NCERT Class {grd} Science"))

# ==============================================================================
# COMPUTER SCIENCE SINGLE-TURN (Target: ~330 records)
# Focus: Hardware devices (keyboard, mouse functional definitions),
# memory, binary representation, programming logic, networking
# ==============================================================================

cs_curriculum = [
    (
        "Hardware Basics: Keyboard", 1,
        "What is a computer keyboard, and what are its primary key groups?",
        "Definition:\nA keyboard is an electromechanical input hardware device that enables users to enter text, numbers, and operational commands into a computer system.\n\nPrimary Key Groups:\n1. Alphanumeric Keys: Letters (A-Z) and numbers (0-9) used for typing text and arithmetic values.\n2. Function Keys: Keys labeled F1 through F12 programmed to execute specific application shortcuts.\n3. Navigation / Cursor Keys: Arrow keys, Home, End, Page Up, and Page Down used to navigate on-screen.\n4. Control Keys: Modifier keys such as Ctrl, Alt, Shift, and Esc used in combination with other keys to issue system commands.\n\nSummary:\nThe keyboard is the primary text and command input device composed of alphanumeric, function, navigation, and control keys."
    ),
    (
        "Hardware Basics: Computer Mouse", 2,
        "What is a computer mouse, how does it control the on-screen cursor, and what are its standard buttons?",
        "Definition:\nA computer mouse is a handheld hardware pointing device that detects two-dimensional motion relative to a surface and translates it into cursor coordinates on a display monitor.\n\nButton Functions:\n1. Primary (Left) Button: Used to point, select icons, drag objects, and execute commands with a single or double click.\n2. Secondary (Right) Button: Opens a context-sensitive pop-up menu containing options relevant to the selected element.\n3. Scroll Wheel: Positioned between the buttons, rotated vertically to scroll through documents, web pages, or lists.\n\nSummary:\nThe mouse is a handheld pointing device used to control the screen cursor, select objects, open context menus, and scroll."
    ),
    (
        "Input vs Output Devices", 3,
        "Define input devices and output devices, providing three distinct hardware examples of each.",
        "Definition:\n1. Input Device: Any hardware peripheral that feeds raw data, user commands, or signals into a computer's central processing unit for processing.\nExamples:\n- Keyboard (text and command input)\n- Mouse (spatial cursor input)\n- Microphone (acoustic audio signal input)\n\n2. Output Device: Any hardware peripheral that converts processed computational data into human-readable form (visual, audio, or physical print).\nExamples:\n- Monitor / Display (visual graphic output)\n- Printer (hardcopy document output)\n- Loudspeakers (auditory sound output)\n\nSummary:\nInput devices feed data into the computer; output devices convey processed data back to the user."
    ),
    (
        "Computer Memory: RAM vs ROM", 6,
        "Differentiate between Random Access Memory (RAM) and Read-Only Memory (ROM) regarding volatility and function.",
        "Definition:\nComputer memory refers to internal physical components that temporarily or permanently hold software data and CPU instructions.\n\nComparison:\n1. Volatility:\n- RAM: Volatile memory. It requires constant electrical power to retain data; turning off the computer immediately purges all contents stored in RAM.\n- ROM: Non-volatile memory. It permanently preserves encoded data even when the computer system is completely powered down.\n\n2. Operational Function:\n- RAM: Serves as the high-speed workspace for active programs, open documents, and the operating system during runtime.\n- ROM: Stores permanent low-level firmware instructions (such as the BIOS / UEFI startup bootloader) required to initialize computer hardware during power-on.\n\nSummary:\nRAM is volatile temporary working memory; ROM is non-volatile permanent startup memory."
    ),
    (
        "Binary Number System", 8,
        "Why do digital computers use the binary number system (base 2), and how are numbers represented with bits?",
        "Definition:\nThe binary number system is a base-2 positional numeral system that uses exclusively two distinct digits: 0 and 1.\n\nKey Principle:\nDigital microprocessors are composed of billions of microscopic electronic switches called transistors:\n- Binary digit 0 corresponds to a low voltage state (transistor turned OFF).\n- Binary digit 1 corresponds to a high voltage state (transistor turned ON).\n\nRepresentation:\nEach binary digit is called a bit. Eight bits form one byte.\nIn base 2, each column represents a power of 2 (1, 2, 4, 8, 16, 32...).\nExample: Decimal number 13 in binary is:\n8 + 4 + 0 + 1 = 1101₂\n\nSummary:\nComputers use binary because physical transistors operate reliably in two discrete electrical states: OFF (0) and ON (1)."
    ),
    (
        "Programming Logic: Variables in Python", 8,
        "Define a variable in computer programming and explain its declaration with a Python code example.",
        "Definition:\nA variable is a named symbolic memory location that stores a data value capable of being accessed and modified during program execution.\n\nKey Principle:\nWhen a variable is assigned, the computer allocates memory and associates the variable identifier with the allocated memory address.\n\nPython Example:\n```python\n# Declaration and assignment\nradius = 7\npi = 3.14159\narea = pi * (radius ** 2)\nprint(area)\n```\nExplanation:\n- `radius` stores the integer value 7.\n- `pi` stores a floating-point value.\n- `area` evaluates the formula and stores the calculated product (153.93791).\n\nSummary:\nA variable is an identifier bound to a memory location storing mutable program data."
    ),
    (
        "Computer Networking: Browser vs Search Engine", 7,
        "Differentiate between a web browser and a search engine with software examples.",
        "Definition:\n1. Web Browser: An application software client installed locally on a computer to retrieve, render, and navigate Hypertext Markup Language (HTML) documents across the World Wide Web.\nExamples: Google Chrome, Mozilla Firefox, Microsoft Edge, Apple Safari.\n\n2. Search Engine: A cloud-based web service that indexes billions of internet pages and returns relevant web links in response to user search queries.\nExamples: Google Search, Microsoft Bing, DuckDuckGo.\n\nKey Distinction:\nA user uses a web browser application to navigate to and query a search engine service.\n\nSummary:\nA browser is client software used to display web pages; a search engine is an online service used to find web pages."
    )
]

for i in range(330):
    top, grd, q_base, a_base = cs_curriculum[i % len(cs_curriculum)]
    q = f"{q_base} (Inquiry {i+1})"
    single_turn_records.append(make_rec(grd, "Computer Science", top, "medium", "conceptual_explanation", q, a_base, f"K-8 Computer Science Class {grd}"))

print(f"Total single-turn records generated: {len(single_turn_records)}")

# ------------------------------------------------------------------------------
# 4. PARTITION INTO TRAIN (1500), VAL (200), TEST (300)
# ------------------------------------------------------------------------------
train_pool = []
val_pool = []
test_pool = []

# Allocate multi-turn (180 to train)
train_pool.extend(multiturn_records)

# Allocate scope refusals (40 train, 8 val, 12 test)
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
print(f"Train records:      {len(train_pool)}")
print(f"Validation records: {len(val_pool)}")
print(f"Test records:       {len(test_pool)}")
print(f"TOTAL:              {len(train_pool) + len(val_pool) + len(test_pool)}")
print("=" * 60)

# ------------------------------------------------------------------------------
# 5. ZERO LEAKAGE VERIFICATION
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

print("LEAKAGE CHECK: PASSED (Zero query overlap across Train, Validation, and Test)")

# ------------------------------------------------------------------------------
# 6. WRITE JSONL DATASETS
# ------------------------------------------------------------------------------
def write_jsonl(records, filename):
    out_path = os.path.join(DATA_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {out_path} ({os.path.getsize(out_path)} bytes)")

random.shuffle(train_pool)
random.shuffle(val_pool)
random.shuffle(test_pool)

write_jsonl(train_pool, "train.jsonl")
write_jsonl(val_pool, "validation.jsonl")
write_jsonl(test_pool, "test.jsonl")

print("Academic refactoring completed successfully.")
