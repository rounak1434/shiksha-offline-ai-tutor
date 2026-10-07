"""
math_generator.py
Generates curriculum-aligned mathematics records for Class 1 to Class 8.
Strict adherence to step-by-step pedagogical scaffolding and verification checks.
"""

def make_entry(grade, topic, difficulty, q_type, q_text, ans_text, source="Curriculum-aligned NCERT/State Board"):
    user_prompt = f"Student grade: Class {grade}\nSubject: Mathematics\nQuestion: {q_text.strip()}"
    return {
        "metadata": {
            "grade": grade,
            "subject": "Mathematics",
            "topic": topic,
            "difficulty": difficulty,
            "question_type": q_type,
            "curriculum_source": source
        },
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": ans_text.strip()}
        ]
    }

def generate_math_records():
    records = []
    
    # -------------------------------------------------------------
    # CLASS 1 - 2 MATHEMATICS
    # -------------------------------------------------------------
    # Counting, addition, subtraction, shapes
    c1_2_data = [
        ("Counting", "foundational", "conceptual_explanation",
         "How do I count from 1 to 10? Can you help me?",
         "Let's count together using our fingers!\n\n1 (One little thumb)\n2 (Two fingers)\n3 (Three fingers)\n4 (Four fingers)\n5 (A whole high-five hand!)\n6 (Add one more finger)\n7 (Seven fingers)\n8 (Eight fingers)\n9 (Nine fingers)\n10 (All ten fingers up in the air!)\n\nPractice counting items around your room, like 10 crayons or 10 books!"),
        
        ("Addition", "foundational", "step_by_step_calculation",
         "If I have 3 red apples and my friend gives me 2 green apples, how many apples do I have in total?",
         "Let's count your apples together step-by-step:\n\n1. You start with **3 red apples**:\n   🍎 🍎 🍎\n\n2. Your friend gives you **2 more green apples**:\n   🍏 🍏\n\n3. Put them together and count all of them:\n   1, 2, 3... 4, 5!\n\nIn numbers: **3 + 2 = 5**\n\nYou have **5 apples** in total! Great job!"),
         
        ("Subtraction", "easy", "step_by_step_calculation",
         "There are 6 birds sitting on a tree branch. 2 birds fly away. How many birds are left?",
         "Let's solve this step-by-step:\n\n1. Start with **6 birds** on the branch:\n   🐦 🐦 🐦 🐦 🐦 🐦\n\n2. Now take away the **2 birds** that flew away:\n   Count backward from 6:\n   - 1 bird flies away -> 5 birds left\n   - 2nd bird flies away -> 4 birds left\n\nIn numbers: **6 - 2 = 4**\n\nThere are **4 birds** left on the branch!"),
         
        ("Shapes", "foundational", "conceptual_explanation",
         "What is the difference between a circle and a triangle?",
         "Here is the simple difference:\n\n### 1. A Circle (⚪)\n- It is perfectly round like a coin or a clock.\n- It has **zero straight sides** and **zero sharp corners**.\n\n### 2. A Triangle (🔺)\n- It has **3 straight sides**.\n- It has **3 pointy corners**.\n- Examples: A slice of pizza, a party hat, or a roof."),
         
        ("Comparison", "easy", "conceptual_explanation",
         "Which number is bigger: 7 or 4? How do I know?",
         "**7 is bigger than 4.**\n\nHere is how you know:\n- Imagine you have 4 candies: 🍬 🍬 🍬 🍬\n- Now imagine 7 candies: 🍬 🍬 🍬 🍬 🍬 🍬 🍬\n- You can see that 7 has 3 extra candies!\n\nWhen we count in order: 1, 2, 3, **4**, 5, 6, **7**...\nNumbers that come later are always bigger. So **7 > 4**.")
    ]
    
    for topic, diff, qtype, q, a in c1_2_data:
        records.append(make_entry(1 if "Counting" in topic else 2, topic, diff, qtype, q, a, "NCERT Class 1-2 Math-Magic"))
        
    # Additional parametric Class 1-2 problems
    for a in range(2, 8):
        for b in range(1, 6):
            if len(records) >= 60: break
            q = f"What is {a} + {b}?"
            ans = f"Let's add {a} and {b} step-by-step:\n\n1. Start with the bigger number: **{a}**.\n2. Count forward by {b} steps: " + ", ".join(str(a+i) for i in range(1, b+1)) + f".\n\n**{a} + {b} = {a+b}**"
            records.append(make_entry(1, "Addition", "easy", "step_by_step_calculation", q, ans, "NCERT Class 1 Math"))
            
    # -------------------------------------------------------------
    # CLASS 3 - 4 MATHEMATICS
    # -------------------------------------------------------------
    c3_4_data = [
        (3, "Multiplication", "easy", "conceptual_explanation",
         "What is multiplication? Can you explain it simply?",
         "Multiplication is just a fast way to do **repeated addition**!\n\nInstead of adding the same number again and again, you multiply.\n\n### The Apple Basket Example:\nImagine you have **3 baskets**.\nInside **each basket**, there are **4 red apples**.\n\n- If you add: $4 + 4 + 4 = 12$ apples.\n- With multiplication: **3 groups of 4 is 12**!\n- In math symbols: **3 × 4 = 12**\n\nThe \"×\" symbol simply means \"groups of\"!"),
         
        (3, "Division", "easy", "conceptual_explanation",
         "What is division? If I have 12 cookies and 3 friends, how do I divide them equally?",
         "**Division means sharing equally into groups.**\n\nLet's share your 12 cookies among 3 friends:\n- Friend 1 gets 1, Friend 2 gets 1, Friend 3 gets 1...\n- Keep dealing them out like cards until all 12 are shared.\n\nEach friend ends up with **4 cookies**!\n\nIn math symbols: **12 ÷ 3 = 4**\n\n**Check:** 3 friends × 4 cookies = 12 cookies. Correct!"),
         
        (4, "Fractions", "medium", "conceptual_explanation",
         "What is a fraction? What do the top and bottom numbers mean?",
         "A **fraction represents a part of a whole**.\n\nImagine a whole circular pizza cut into **4 equal slices**:\nIf you eat **1 slice**, you have eaten **1/4** of the pizza!\n\n### The Two Parts of a Fraction:\n- **Top Number (Numerator)**: How many parts you have or are talking about. Here, **1**.\n- **Bottom Number (Denominator)**: The total number of equal parts the whole was divided into. Here, **4**.\n\n**Memory Trick:**\n- **D**enominator = **D**own (at the bottom)!\n- **N**umerator = **N**umber of parts you have!"),
         
        (4, "Measurement", "medium", "step_by_step_calculation",
         "How many centimeters are in 3 meters? Show the conversion.",
         "**Step-by-step conversion:**\n\n1. **Remember the rule:**\n   $$1\\text{ meter (m)} = 100\\text{ centimeters (cm)}$$\n\n2. **To convert meters to centimeters, multiply by 100:**\n   $$3\\text{ m} = 3 \\times 100\\text{ cm}$$\n\n3. **Calculate:**\n   $$3 \\times 100 = 300\\text{ cm}$$\n\n**Answer:** There are **300 centimeters** in 3 meters.")
    ]
    for g, topic, diff, qtype, q, a in c3_4_data:
        records.append(make_entry(g, topic, diff, qtype, q, a, f"NCERT Class {g} Math-Magic"))
        
    # Parametric Class 3-4 multiplication and division
    for mult in [(3,6), (4,5), (6,7), (8,9), (7,4), (9,5), (6,6), (8,8), (7,7), (9,9)]:
        q = f"Calculate {mult[0]} × {mult[1]} step-by-step."
        ans = f"**Step-by-step solution:**\n\n{mult[0]} × {mult[1]} means **{mult[0]} groups of {mult[1]}**.\n\nUsing the multiplication tables:\n{mult[0]} × {mult[1]} = **{mult[0]*mult[1]}**.\n\n**Check by division:** {mult[0]*mult[1]} ÷ {mult[0]} = {mult[1]} ✅"
        records.append(make_entry(3, "Multiplication", "easy", "step_by_step_calculation", q, ans, "NCERT Class 3 Math"))

    # -------------------------------------------------------------
    # CLASS 5 MATHEMATICS
    # -------------------------------------------------------------
    c5_data = [
        ("Fractions", "medium", "step_by_step_calculation",
         "Add 2/7 and 3/7. Show your steps.",
         "**Step-by-step solution:**\n\n$$\\frac{2}{7} + \\frac{3}{7}$$\n\n1. **Check denominators:** Both fractions have the same denominator (7).\n2. **Add the numerators:** $2 + 3 = 5$.\n3. **Keep the denominator the same:** Do NOT add $7 + 7$!\n\n$$\\frac{2 + 3}{7} = \\frac{5}{7}$$\n\n**Answer: 5/7**"),
         
        ("Area and Perimeter", "medium", "step_by_step_calculation",
         "A rectangular garden is 8 meters long and 5 meters wide. Find its perimeter and area.",
         "**Step-by-step solution:**\n\nGiven: Length ($l$) = 8 m, Width ($w$) = 5 m\n\n### 1. Perimeter (Distance all the way around the outside):\nFormula: $\\text{Perimeter} = 2 \\times (l + w)$\n$$\\text{Perimeter} = 2 \\times (8 + 5) = 2 \\times 13 = \\mathbf{26\\text{ meters}}$$\n\n### 2. Area (Space inside the rectangle):\nFormula: $\\text{Area} = l \\times w$\n$$\\text{Area} = 8 \\times 5 = \\mathbf{40\\text{ square meters (m²)}}$$\n\n**Notice units:** Perimeter is in meters (m); Area is in square meters (m²)."),
         
        ("Decimals", "easy", "conceptual_explanation",
         "What is 0.5 as a fraction? Explain.",
         "**0.5 is equal to 1/2 (one half).**\n\nHere is why:\n- In decimals, the first spot after the point is the **tenths place**.\n- So 0.5 means **5 tenths**, written as $\\frac{5}{10}$.\n- If you simplify $\\frac{5}{10}$ by dividing both top and bottom by 5:\n  $$\\frac{5 \\div 5}{10 \\div 5} = \\frac{1}{2}$$\n\nTherefore, $0.5 = \\frac{1}{2}$!")
    ]
    for topic, diff, qtype, q, a in c5_data:
        records.append(make_entry(5, topic, diff, qtype, q, a, "NCERT Class 5 Math"))

    # -------------------------------------------------------------
    # CLASS 6 MATHEMATICS
    # -------------------------------------------------------------
    c6_data = [
        ("Fractions", "medium", "step_by_step_calculation",
         "How do I add 2/5 and 1/3? Show all steps.",
         "**Step-by-step solution:**\n\n$$\\frac{2}{5} + \\frac{1}{3}$$\n\n### Step 1: Find the Common Denominator (LCM)\nThe denominators are 5 and 3. The LCM of 5 and 3 is **15**.\n\n### Step 2: Convert to Equivalent Fractions\n- $\\frac{2 \\times 3}{5 \\times 3} = \\frac{6}{15}$\n- $\\frac{1 \\times 5}{3 \\times 5} = \\frac{5}{15}$\n\n### Step 3: Add the Numerators\n$$\\frac{6}{15} + \\frac{5}{15} = \\frac{6 + 5}{15} = \\frac{11}{15}$$\n\n**Answer: 11/15**"),
         
        ("Integers", "medium", "misconception_correction",
         "Why is (-3) + (-5) equal to -8, but (-3) × (-5) equal to +15?",
         "This is one of the most common confusions in Class 6 math!\n\n### 1. Addition: (-3) + (-5) = -8\n- Think of negative numbers as **owing money** (debt) or **moving left on a number line**.\n- If you owe 3 dollars, and then you borrow 5 more dollars, your total debt increases to 8 dollars.\n- Adding two negatives always gives a bigger negative!\n\n### 2. Multiplication: (-3) × (-5) = +15\n- Multiplication with negative numbers reverses direction.\n- Negative means \"opposite of\".\n- So multiplying by a negative means taking the \"opposite of a negative\", which turns **positive**!\n\n**Rule to Remember:**\n- Adding debts makes more debt: $(-a) + (-b) = -(a+b)$\n- Multiplying two negatives cancels out: $(-a) \\times (-b) = +(a \\times b)$"),
         
        ("Ratio and Proportion", "medium", "step_by_step_calculation",
         "If 4 notebooks cost $20, how much do 9 notebooks cost?",
         "We solve this using the **Unitary Method**:\n\n### Step 1: Find the cost of 1 notebook (unit cost)\n$$\\text{Cost of 1 notebook} = \\frac{20}{4} = \\$5$$\n\n### Step 2: Multiply by the new number of notebooks (9)\n$$\\text{Cost of 9 notebooks} = 9 \\times 5 = \\$45$$\n\n**Answer: 9 notebooks cost $45.**")
    ]
    for topic, diff, qtype, q, a in c6_data:
        records.append(make_entry(6, topic, diff, qtype, q, a, "NCERT Class 6 Mathematics"))

    # -------------------------------------------------------------
    # CLASS 7 MATHEMATICS
    # -------------------------------------------------------------
    c7_data = [
        ("Linear Equations", "medium", "step_by_step_calculation",
         "Solve 4x + 9 = 33 step-by-step.",
         "**Step-by-step solution:**\n\n$$4x + 9 = 33$$\n\n1. **Subtract 9 from both sides:**\n   $$4x + 9 - 9 = 33 - 9$$\n   $$4x = 24$$\n\n2. **Divide both sides by 4:**\n   $$\\frac{4x}{4} = \\frac{24}{4}$$\n   $$x = 6$$\n\n**Verification:** Substitute $x = 6$:\n$$4(6) + 9 = 24 + 9 = 33$$ ✅ Verified!\n\n**Answer: x = 6**"),
         
        ("Exponents and Powers", "easy", "step_by_step_calculation",
         "Simplify (2^3) × (2^4) using exponent laws.",
         "**Step-by-step solution:**\n\n**Law of Exponents:** When multiplying powers with the same base, add their exponents:\n$$a^m \\times a^n = a^{m+n}$$\n\nApplying the law:\n$$2^3 \\times 2^4 = 2^{3 + 4} = 2^7$$\n\nCalculating $2^7$:\n$$2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 2 = 128$$\n\n**Answer: 2^7 = 128**"),
         
        ("Geometry", "medium", "step_by_step_calculation",
         "In a triangle, two angles are 50° and 70°. Find the third angle.",
         "**Step-by-step solution:**\n\n**Angle Sum Property:** The sum of all three angles in any triangle is always **180°**.\n\n$$\\angle 1 + \\angle 2 + \\angle 3 = 180^\\circ$$\n$$50^\\circ + 70^\\circ + \\angle 3 = 180^\\circ$$\n$$120^\\circ + \\angle 3 = 180^\\circ$$\n$$\\angle 3 = 180^\\circ - 120^\\circ = 60^\\circ$$\n\n**Answer: The third angle is 60°.**")
    ]
    for topic, diff, qtype, q, a in c7_data:
        records.append(make_entry(7, topic, diff, qtype, q, a, "NCERT Class 7 Mathematics"))

    # -------------------------------------------------------------
    # CLASS 8 MATHEMATICS
    # -------------------------------------------------------------
    c8_data = [
        ("Linear Equations in One Variable", "challenging", "step_by_step_calculation",
         "Solve 5x - 7 = 2x + 8 step-by-step.",
         "**Step-by-step solution:**\n\n$$5x - 7 = 2x + 8$$\n\n1. **Move variable terms to the left:** Subtract $2x$ from both sides:\n   $$5x - 2x - 7 = 8$$\n   $$3x - 7 = 8$$\n\n2. **Move constants to the right:** Add 7 to both sides:\n   $$3x = 8 + 7$$\n   $$3x = 15$$\n\n3. **Divide by 3:**\n   $$x = \\frac{15}{3} = 5$$\n\n**Verification:**\n- Left side: $5(5) - 7 = 25 - 7 = 18$\n- Right side: $2(5) + 8 = 10 + 8 = 18$\nBoth sides match! ✅\n\n**Answer: x = 5**"),
         
        ("Algebraic Identities", "medium", "step_by_step_calculation",
         "Expand (x + 5)^2 using algebraic identities.",
         "**Step-by-step solution:**\n\n**Identity:** $(a + b)^2 = a^2 + 2ab + b^2$\n\nHere, $a = x$ and $b = 5$:\n1. $a^2 = x^2$\n2. $2ab = 2 \\times x \\times 5 = 10x$\n3. $b^2 = 5^2 = 25$\n\nCombine the terms:\n$$(x + 5)^2 = x^2 + 10x + 25$$\n\n**Answer: x² + 10x + 25**"),
         
        ("Mensuration", "challenging", "step_by_step_calculation",
         "Find the total surface area of a closed cylinder with radius 7 cm and height 10 cm (take pi = 22/7).",
         "**Step-by-step solution:**\n\nGiven: Radius ($r$) = 7 cm, Height ($h$) = 10 cm\n\nFormula for Total Surface Area (TSA):\n$$\\text{TSA} = 2\\pi r(r + h)$$\n\n1. Substitute values:\n   $$\\text{TSA} = 2 \\times \\frac{22}{7} \\times 7 \\times (7 + 10)$$\n\n2. The 7 cancels with the denominator 7:\n   $$\\text{TSA} = 2 \\times 22 \\times 17 = 44 \\times 17$$\n\n3. Calculate $44 \\times 17$:\n   $$44 \\times 10 = 440$$\n   $$44 \\times 7 = 308$$\n   $$440 + 308 = 748\\text{ cm²}$$\n\n**Answer: 748 cm²**")
    ]
    for topic, diff, qtype, q, a in c8_data:
        records.append(make_entry(8, topic, diff, qtype, q, a, "NCERT Class 8 Mathematics"))
        
    return records
