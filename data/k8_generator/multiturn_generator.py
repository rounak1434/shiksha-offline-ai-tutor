"""
multiturn_generator.py
Generates multi-turn tutoring dialogs for the training set (10-15% of train).
Teaches pedagogical patience, step clarifications, alternate analogies, and mistake correction.
"""

def make_multiturn_entry(grade, subject, topic, difficulty, dialog_turns, source="Curriculum-aligned Multi-turn Tutoring"):
    # First turn starts with standard prompt header
    messages = []
    for idx, (role, text) in enumerate(dialog_turns):
        if idx == 0 and role == "user":
            content = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {text.strip()}"
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

def generate_multiturn_records():
    dialogs = [
        # Dialog 1: Class 8 Algebra Clarification
        (8, "Mathematics", "Linear Equations", "medium", [
            ("user", "Can you solve 3x + 7 = 25 step-by-step?"),
            ("assistant", "**Step-by-step solution:**\n\n1. Equation: 3x + 7 = 25\n2. Subtract 7 from both sides: 3x = 18\n3. Divide both sides by 3: x = 6\n\nAnswer: x = 6"),
            ("user", "I don't understand step 2. Why did you subtract 7 from both sides instead of dividing by 3 first?"),
            ("assistant", "That is a great question! Let's understand why we subtract 7 first.\n\nThink of the equation like a balanced weighing scale:\n- On the left side, you have a bag with 3 mystery items (3x) plus 7 loose stones.\n- On the right side, you have 25 stones.\n\nTo find the weight of just the bag, it is much easier to remove the 7 loose stones from both sides first! That leaves you with:\n$$3x = 18$$\n\nIf you divided by 3 first, you would have to divide the 7 by 3 too, which gives messy fractions like $\\frac{7}{3}$. Subtracting first keeps the math clean and simple!"),
            ("user", "Oh, I see now! You isolate the variable term first. So if I have 4x - 5 = 15, I would add 5 first, right?"),
            ("assistant", "Spot on! That is exactly right.\n\nFirst add 5 to both sides:\n$$4x = 15 + 5 = 20$$\nThen divide by 4:\n$$x = 5$$\n\nYou've mastered the concept!")
        ]),

        # Dialog 2: Class 8 Physics Mass vs Weight
        (8, "Science (Physics)", "Mass vs Weight", "medium", [
            ("user", "My friend says their weight on Earth is 60 kg. Is that right?"),
            ("assistant", "Scientifically speaking, your friend's statement is **incorrect**.\n\nIn science, **60 kg is their mass**, not their weight.\n- **Mass** is the quantity of matter inside them, measured in kilograms (kg).\n- **Weight** is the gravitational downward pull on that mass, measured in Newtons (N).\n\nTheir weight on Earth is: $W = mg = 60 \\times 9.8 = \\mathbf{588\\text{ N}}$."),
            ("user", "Wait, if a bathroom scale shows 60 kg, why do people call it weight?"),
            ("assistant", "That is because everyday colloquial language is different from strict scientific language!\n\nBathroom scales actually measure the downward force you exert, but the dial is calibrated to divide that force by Earth's gravity (9.8) and display kilograms because people find kg easier to imagine than Newtons.\n\nHowever, if you took that exact same scale to the Moon:\n- Your mass would still be 60 kg.\n- But the scale would read only 10 kg because the Moon's gravity is 6 times weaker!\n\nThat is why physicists insist: **Mass is constant (kg), but weight changes with gravity (N)**."),
            ("user", "That makes total sense! So on the Moon, my mass is 60 kg, but my weight is only about 98 N."),
            ("assistant", "Precisely! You've got it exactly right.")
        ]),

        # Dialog 3: Class 6 Math Fraction Addition Error Correction
        (6, "Mathematics", "Fractions", "medium", [
            ("user", "I tried adding 1/2 and 1/3, and I got 2/5. Is that correct?"),
            ("assistant", "That is a very common mistake, but **2/5 is not correct**!\n\nLet's see why: when adding fractions, you **cannot just add the top numbers and bottom numbers together**.\n\nThink of it visually:\n- $\\frac{1}{2}$ is half a whole pizza.\n- $\\frac{2}{5}$ is *less* than half a pizza!\n- It is impossible to add half a pizza plus another third of a pizza and end up with *less* pizza than you started with!"),
            ("user", "Oh! I see what you mean. So how do I add them properly?"),
            ("assistant", "You must first make the slice sizes the same by finding a **common denominator**!\n\n1. Denominators are 2 and 3. The LCM is **6**.\n2. Convert to equivalent fractions with 6 at the bottom:\n   $$\\frac{1}{2} = \\frac{1 \\times 3}{2 \\times 3} = \\frac{3}{6}$$\n   $$\\frac{1}{3} = \\frac{1 \\times 2}{3 \\times 2} = \\frac{2}{6}$$\n3. Now add only the top numbers (numerators):\n   $$\\frac{3}{6} + \\frac{2}{6} = \\frac{3 + 2}{6} = \\mathbf{\\frac{5}{6}}$$\n\nNotice the bottom stays 6!"),
            ("user", "So the answer is 5/6! That makes much more sense because 5/6 is almost a whole pizza."),
            ("assistant", "Excellent observation! Always using that real-life sanity check will help you catch fraction mistakes.")
        ]),

        # Dialog 4: Class 7 Science Respiration vs Photosynthesis
        (7, "Science (Biology)", "Plant Respiration", "medium", [
            ("user", "Why shouldn't we sleep under a tree at night? My grandmother says trees give off poison gas at night."),
            ("assistant", "Your grandmother's advice has real scientific backing, though it isn't 'poison gas'—it is simply **carbon dioxide ($CO_2$)**!\n\nHere is what happens:\n1. **During the day**: Trees perform **photosynthesis** (taking in $CO_2$ and releasing lots of oxygen $O_2$) AND respiration.\n2. **At night**: Without sunlight, photosynthesis **stops completely**! But trees are living organisms, so their cellular respiration continues.\n3. This means at night, trees take in oxygen and release carbon dioxide into the immediate air under the branches.\n\nSleeping right under thick foliage can slightly reduce the fresh oxygen available immediately around you."),
            ("user", "Do trees breathe through their leaves?"),
            ("assistant", "Yes! Leaves have thousands of microscopic pores on their undersides called **stomata**.\n\nSpecial cells called **guard cells** open and close the stomata, allowing oxygen and carbon dioxide to diffuse in and out of the plant, just like tiny microscopic nostrils!")
        ]),

        # Dialog 5: Class 8 Physics Newton's 2nd Law Proportionality
        (8, "Science (Physics)", "Newton's Second Law", "hard", [
            ("user", "In F = ma, if I push two boxes with the same 20 N force, does the heavier one go faster?"),
            ("assistant", "No! The heavier box will accelerate **slower**, not faster!\n\nLet's write Newton's Second Law rearranged for acceleration:\n$$a = \\frac{F}{m}$$\n\nNotice that mass ($m$) is in the **denominator** (on the bottom). That means:\n- When force ($F$) is constant, acceleration is **inversely proportional** to mass ($a \\propto \\frac{1}{m}$).\n- More mass means **less acceleration**!"),
            ("user", "Can you give me a numbers example with a 2 kg box and a 10 kg box?"),
            ("assistant", "Absolutely! Let's calculate both with your $20\\text{ N}$ push:\n\n1. **For the light 2 kg box**:\n   $$a = \\frac{20\\text{ N}}{2\\text{ kg}} = \\mathbf{10\\text{ m/s}²}$$\n\n2. **For the heavy 10 kg box**:\n   $$a = \\frac{20\\text{ N}}{10\\text{ kg}} = \\mathbf{2\\text{ m/s}²}$$\n\nThe 2 kg box speeds up **5 times faster** than the 10 kg box because it has less inertia resisting your push!")
        ])
    ]
    
    records = []
    for grade, subj, topic, diff, turns in dialogs:
        records.append(make_multiturn_entry(grade, subj, topic, diff, turns))
        
    return records
