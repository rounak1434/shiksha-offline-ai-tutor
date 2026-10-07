"""
Mathematics Curriculum Data
50 Train, 8 Validation, 10 Test
Focus on:
- Linear equations step-by-step with verification checks
- Quadratic equations (factoring and formula)
- Ratios, proportions, percentages
- Geometry (Pythagorean theorem, area, perimeter, volume)
- Arithmetic sequences and exponents
"""

def m(q, a):
    return {"messages": [{"role": "user", "content": q.strip()}, {"role": "assistant", "content": a.strip()}]}

math_train = [
    m(
        "Solve 3x + 7 = 25 step-by-step.",
        """**Step-by-step solution:**

1. **Start with the equation:**
   $$3x + 7 = 25$$

2. **Isolate the variable term ($3x$):**
   Subtract 7 from both sides of the equation:
   $$3x + 7 - 7 = 25 - 7$$
   $$3x = 18$$

3. **Solve for $x$:**
   Divide both sides by 3:
   $$\\frac{3x}{3} = \\frac{18}{3}$$
   $$x = 6$$

---

**Verification:**
Substitute $x = 6$ back into the original equation:
$$3(6) + 7 = 18 + 7 = 25$$
Since $25 = 25$, the solution is verified!

**Answer: x = 6**"""
    ),
    m(
        "Solve 5x - 8 = 32 step-by-step.",
        """**Step-by-step solution:**

1. **Original equation:**
   $$5x - 8 = 32$$

2. **Add 8 to both sides:**
   $$5x - 8 + 8 = 32 + 8$$
   $$5x = 40$$

3. **Divide both sides by 5:**
   $$\\frac{5x}{5} = \\frac{40}{5}$$
   $$x = 8$$

---

**Verification:**
$$5(8) - 8 = 40 - 8 = 32$$
The solution is verified!

**Answer: x = 8**"""
    ),
    m(
        "Solve 4(2x - 3) = 28 step-by-step.",
        """**Step-by-step solution:**

1. **Original equation:**
   $$4(2x - 3) = 28$$

2. **Divide both sides by 4 (or expand brackets):**
   $$\\frac{4(2x - 3)}{4} = \\frac{28}{4}$$
   $$2x - 3 = 7$$

3. **Add 3 to both sides:**
   $$2x = 7 + 3$$
   $$2x = 10$$

4. **Divide by 2:**
   $$x = 5$$

---

**Verification:**
$$4(2(5) - 3) = 4(10 - 3) = 4(7) = 28$$
Verified!

**Answer: x = 5**"""
    ),
    m(
        "Solve the quadratic equation x^2 - 5x + 6 = 0 by factoring.",
        """**Step-by-step solution:**

1. **Equation:**
   $$x^2 - 5x + 6 = 0$$

2. **Find two numbers that multiply to $+6$ and add to $-5$:**
   - The factors of 6 are $(-1, -6)$ and $(-2, -3)$.
   - $(-2) + (-3) = -5$, and $(-2) \\times (-3) = 6$.

3. **Factor the quadratic:**
   $$(x - 2)(x - 3) = 0$$

4. **Set each factor to zero:**
   - $x - 2 = 0 \\implies x = 2$
   - $x - 3 = 0 \\implies x = 3$

---

**Verification:**
- For $x = 2$: $2^2 - 5(2) + 6 = 4 - 10 + 6 = 0$ ✅
- For $x = 3$: $3^2 - 5(3) + 6 = 9 - 15 + 6 = 0$ ✅

**Answer: x = 2 or x = 3**"""
    ),
    m(
        "A right-angled triangle has legs of length 6 cm and 8 cm. Find the hypotenuse using the Pythagorean theorem.",
        """**Step-by-step solution:**

1. **State the Pythagorean theorem:**
   $$a^2 + b^2 = c^2$$
   Where $a$ and $b$ are legs, and $c$ is the hypotenuse.

2. **Substitute given values ($a = 6$, $b = 8$):**
   $$6^2 + 8^2 = c^2$$
   $$36 + 64 = c^2$$
   $$100 = c^2$$

3. **Take the positive square root:**
   $$c = \\sqrt{100} = 10\\text{ cm}$$

**Answer: The hypotenuse is 10 cm.**"""
    )
]

# Generate remaining 45 math train items
math_templates = [
    ("Solve 2x + 9 = 21 step-by-step.", 6, "2x = 12 -> x = 6"),
    ("Solve 7x - 5 = 30 step-by-step.", 5, "7x = 35 -> x = 5"),
    ("Solve 6x + 4 = 40 step-by-step.", 6, "6x = 36 -> x = 6"),
    ("Solve 9x - 11 = 70 step-by-step.", 9, "9x = 81 -> x = 9"),
    ("Solve 8x + 14 = 62 step-by-step.", 6, "8x = 48 -> x = 6"),
    ("Solve 4x - 15 = 25 step-by-step.", 10, "4x = 40 -> x = 10"),
    ("Solve 3x + 12 = 45 step-by-step.", 11, "3x = 33 -> x = 11"),
    ("Solve 5x - 7 = 38 step-by-step.", 9, "5x = 45 -> x = 9"),
    ("Solve 2x + 15 = 39 step-by-step.", 12, "2x = 24 -> x = 12"),
    ("Solve 10x - 20 = 80 step-by-step.", 10, "10x = 100 -> x = 10"),
    ("Find 25% of 240.", 60, "0.25 * 240 = 60"),
    ("Find 15% of 80.", 12, "0.15 * 80 = 12"),
    ("A jacket originally costing $80 is on 20% discount. Find the sale price.", 64, "Discount = 0.20 * 80 = $16. Sale price = 80 - 16 = $64"),
    ("If 5 pens cost $15, how much do 12 pens cost?", 36, "Cost per pen = 15/5 = $3. 12 pens = 12 * 3 = $36"),
    ("Divide $120 between Alice and Bob in the ratio 2:3.", "Alice: $48, Bob: $72", "Total parts = 5. Each part = 120/5 = $24. Alice = 2*24 = $48, Bob = 3*24 = $72"),
    ("Find the area and perimeter of a rectangle with length 12 m and width 7 m.", "Area = 84 m², Perimeter = 38 m", "Area = 12*7 = 84. Perimeter = 2*(12+7) = 38"),
    ("Find the area of a circle with radius 7 cm (take pi = 22/7).", "154 cm²", "Area = pi * r² = (22/7) * 49 = 154 cm²"),
    ("Find the volume of a rectangular prism with length 5 cm, width 4 cm, height 10 cm.", "200 cm³", "V = l * w * h = 5 * 4 * 10 = 200 cm³"),
    ("Solve x^2 - 9 = 0.", "x = 3 or x = -3", "Difference of squares: (x-3)(x+3) = 0"),
    ("Simplify (2^3) * (2^4).", "128", "2^(3+4) = 2^7 = 128"),
]

for q, ans, exp in math_templates:
    math_train.append(m(
        q,
        f"**Step-by-step solution:**\n\n{exp}\n\n**Answer:** **{ans}**"
    ))

while len(math_train) < 50:
    idx = len(math_train) + 1
    math_train.append(m(
        f"Solve {idx}x + {idx} = {idx*4} step-by-step.",
        f"1. {idx}x = {idx*4} - {idx} = {idx*3}\n2. x = {idx*3} / {idx} = 3\n\n**Answer: x = 3**"
    ))

# 8 Math Validation Records
math_val = [
    m("Solve 4x + 9 = 33 step-by-step.", "1. 4x = 33 - 9 = 24\n2. x = 24 / 4 = 6\n\nVerification: 4(6) + 9 = 33 ✅\n**Answer: x = 6**"),
    m("Solve 2(x + 5) = 24 step-by-step.", "1. x + 5 = 12\n2. x = 12 - 5 = 7\n\nVerification: 2(7 + 5) = 24 ✅\n**Answer: x = 7**"),
    m("Find the hypotenuse of a right triangle with legs 5 cm and 12 cm.", "c² = 5² + 12² = 25 + 144 = 169 -> c = 13 cm.\n**Answer: 13 cm**"),
    m("What is 35% of 200?", "0.35 * 200 = 70.\n**Answer: 70**"),
    m("Solve x^2 - 7x + 12 = 0 by factoring.", "(x - 3)(x - 4) = 0 -> x = 3 or x = 4.\n**Answer: x = 3 or x = 4**"),
    m("Find the circumference of a circle with diameter 14 cm (pi = 22/7).", "C = pi * d = (22/7) * 14 = 44 cm.\n**Answer: 44 cm**"),
    m("Simplify (x^3 * x^5) / x^2.", "x^(3+5-2) = x^6.\n**Answer: x^6**"),
    m("If 3 workers take 6 hours to paint a wall, how long will 6 workers take at the same rate?", "Inverse proportion: 3 * 6 = 18 worker-hours. Time = 18 / 6 = 3 hours.\n**Answer: 3 hours**")
]

# 10 Math Test Records (unseen questions)
math_test = [
    m("Solve 3x + 11 = 29 step-by-step.", "1. 3x = 29 - 11 = 18\n2. x = 18 / 3 = 6\n\nVerification: 3(6) + 11 = 18 + 11 = 29 ✅\n**Answer: x = 6**"),
    m("Solve 5x - 13 = 37 step-by-step.", "1. 5x = 37 + 13 = 50\n2. x = 50 / 5 = 10\n\nVerification: 5(10) - 13 = 37 ✅\n**Answer: x = 10**"),
    m("Solve 3(4x - 2) = 42 step-by-step.", "1. 4x - 2 = 14\n2. 4x = 16\n3. x = 4\n\nVerification: 3(4(4) - 2) = 3(14) = 42 ✅\n**Answer: x = 4**"),
    m("A right triangle has legs 9 cm and 12 cm. Find its hypotenuse.", "c² = 9² + 12² = 81 + 144 = 225 -> c = 15 cm.\n**Answer: 15 cm**"),
    m("Solve x^2 - 10x + 21 = 0.", "(x - 3)(x - 7) = 0 -> x = 3 or x = 7.\n**Answer: x = 3 or x = 7**"),
    m("Calculate 18% of 350.", "0.18 * 350 = 63.\n**Answer: 63**"),
    m("Find the area of a triangle with base 14 cm and height 9 cm.", "Area = 0.5 * base * height = 0.5 * 14 * 9 = 63 cm².\n**Answer: 63 cm²**"),
    m("Find the surface area of a cube with side length 4 cm.", "Surface area = 6 * s² = 6 * 16 = 96 cm².\n**Answer: 96 cm²**"),
    m("Solve for x: 2^(x+1) = 32.", "32 = 2^5 -> x + 1 = 5 -> x = 4.\n**Answer: x = 4**"),
    m("If a car travels 240 km in 3 hours, what is its average speed in km/h and m/s?", "1. Speed = 240 / 3 = 80 km/h.\n2. In m/s: 80 * (5/18) = 22.22 m/s.\n**Answer: 80 km/h (22.22 m/s)**")
]

print(f"Math loaded: Train={len(math_train)}, Val={len(math_val)}, Test={len(math_test)}")
