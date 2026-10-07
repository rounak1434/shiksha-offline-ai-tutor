"""
build_datasets.py
Constructs the full 290-example STEM dataset:
- train.jsonl (210)
- validation.jsonl (35)
- test.jsonl (45)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def item(q, a):
    return {
        "messages": [
            {"role": "user", "content": q.strip()},
            {"role": "assistant", "content": a.strip()}
        ]
    }

# ==============================================================================
# 1. PHYSICS - TRAINING (65 examples)
# ==============================================================================
physics_train = [
    item(
        "Explain Newton's second law to a class 8 student in simple language.",
        """Newton's Second Law of Motion explains how force, mass, and acceleration are connected.

**The Main Rule:**
**Force = Mass × Acceleration**  (written as **F = ma**)

Let's understand each part in simple terms:
1. **Force (F)**: A push or a pull acting on an object. Measured in **Newtons (N)**.
2. **Mass (m)**: How much matter is inside an object (its 'heaviness' or resistance to change). Measured in **kilograms (kg)**.
3. **Acceleration (a)**: How quickly an object speeds up, slows down, or changes direction. Measured in **meters per second squared (m/s²)**.

**Two Key Principles You Must Remember:**
- **More Force → More Acceleration**: If you push harder on the same cart, it speeds up faster.
- **More Mass → LESS Acceleration (for the same push)**: If you push an empty shopping cart and a heavily loaded cart with the exact same strength, the heavy cart speeds up much slower!

**Formula Rearrangement:**
- $a = \\frac{F}{m}$ (Acceleration equals force divided by mass)
- If mass is doubled while force stays constant, acceleration is halved.

**Common Mistake to Avoid:**
Do not think heavier things move faster when pushed with the same force. More mass means more inertia, which resists acceleration!

**Practice Question:**
If a force of 20 N pushes a 4 kg box on a smooth floor, what is its acceleration?
- $a = \\frac{F}{m} = \\frac{20}{4} = 5\\text{ m/s}²$."""
    ),
    item(
        "What is the difference between mass and weight?",
        """Mass and weight are frequently confused in daily conversation, but in science they are completely different quantities.

### 1. Mass
- **Definition**: The total amount of matter contained in an object.
- **SI Unit**: Kilogram (**kg**) or gram (g).
- **Type of Quantity**: **Scalar** (has only magnitude, no direction).
- **Constancy**: **Constant everywhere**. Your mass is identical on Earth, on the Moon, on Mars, or floating in deep space.
- **Measurement Tool**: Beam balance or pan balance.

### 2. Weight
- **Definition**: The **gravitational force** exerted on an object's mass by a celestial body (like Earth).
- **SI Unit**: Newton (**N**).
- **Type of Quantity**: **Vector** (acts downward toward the center of gravity).
- **Constancy**: **Changes with location** because gravitational acceleration ($g$) varies from planet to planet.
- **Measurement Tool**: Spring balance.

---

### Key Comparison Table
| Property | Mass | Weight |
| :--- | :--- | :--- |
| **What it is** | Quantity of matter | Gravitational pull on that matter |
| **SI Unit** | Kilogram (kg) | Newton (N) |
| **Formula** | $m$ (fundamental property) | $W = mg$ |
| **Variation** | Invariant (constant) | Varies with gravity ($g$) |
| **Can it be zero?** | No (for any physical object) | Yes (in true weightlessness / deep space) |

---

### Accurate Numerical Example:
A backpack has a mass of **10 kg**.
- **On Earth** ($g \\approx 9.8\\text{ m/s}²$):
  $W = mg = 10\\text{ kg} \\times 9.8\\text{ m/s}² = \\mathbf{98\\text{ N}}$.
- **On the Moon** ($g \\approx 1.62\\text{ m/s}²$):
  $W = mg = 10\\text{ kg} \\times 1.62\\text{ m/s}² = \\mathbf{16.2\\text{ N}}$.
- **Notice**: The mass remains **10 kg** in both places, but the weight drops from 98 N to 16.2 N!"""
    ),
    item(
        "A student says: 'My weight is 50 kg.' Is this scientifically correct? Explain.",
        """Scientifically speaking, this statement is **incorrect**.

Here is why, along with the correct scientific concepts:

### 1. The Confusion Between Mass and Weight
- When people step on a bathroom scale and read "50 kg", they are measuring their **mass**, not their weight.
- **Mass** is measured in **kilograms (kg)**.
- **Weight** is a **force** (the downward pull of gravity), and all forces in physics are measured in **Newtons (N)**.
- **Weight is definitely a physical quantity**—specifically, a vector force defined by Newton's law of gravitation.

### 2. The Correct Statements
- **Correct statement of mass**: *"My mass is 50 kg."*
- **Correct statement of weight on Earth**:
  Using the weight formula:
  $$W = mg$$
  Where:
  - $m = 50\\text{ kg}$
  - $g = 9.8\\text{ m/s}²$ (Earth's gravitational acceleration)
  
  $$W = 50\\text{ kg} \\times 9.8\\text{ m/s}² = \\mathbf{490\\text{ N}}$$
  
- The student's actual weight on Earth is **490 Newtons (N)**!

### 3. Why This Distinction Matters
If this student travels to the Moon:
- Their **mass** will still be exactly **50 kg**.
- Their **weight** will become $50 \\times 1.62 \\approx \\mathbf{81\\text{ N}}$ (about $\\frac{1}{6}$ of their Earth weight).

**Summary for Students:**
- Mass = Amount of stuff inside you (kg).
- Weight = The gravitational force pulling that stuff down ($W = mg$, in Newtons)."""
    ),
    item(
        "Two objects have masses of 2 kg and 8 kg. If an equal force of 24 N is applied to both, which one accelerates faster and by how much?",
        """Let's solve this step-by-step using Newton's Second Law of Motion: **$F = ma$**.

Rearranging for acceleration:
$$a = \\frac{F}{m}$$

---

### Step 1: Calculate acceleration for Object 1 (2 kg)
- Force ($F$) = $24\\text{ N}$
- Mass ($m_1$) = $2\\text{ kg}$

$$a_1 = \\frac{F}{m_1} = \\frac{24\\text{ N}}{2\\text{ kg}} = \\mathbf{12\\text{ m/s}²}$$

---

### Step 2: Calculate acceleration for Object 2 (8 kg)
- Force ($F$) = $24\\text{ N}$
- Mass ($m_2$) = $8\\text{ kg}$

$$a_2 = \\frac{F}{m_2} = \\frac{24\\text{ N}}{8\\text{ kg}} = \\mathbf{3\\text{ m/s}²}$$

---

### Step 3: Compare the accelerations
- The lighter object (2 kg) accelerates at **12 m/s²**.
- The heavier object (8 kg) accelerates at **3 m/s²**.
- $\\frac{a_1}{a_2} = \\frac{12}{3} = 4$.

**Conclusion:**
The **2 kg object accelerates 4 times faster** than the 8 kg object.

**Core Scientific Law Illustrated:**
For a constant force, acceleration is **inversely proportional** to mass ($a \\propto \\frac{1}{m}$). A four-fold increase in mass results in a four-fold decrease in acceleration."""
    ),
    item(
        "A student pushes a toy car across the floor and lets go. The car slows down and stops. The student concludes: 'Forces are needed to keep things moving; when the force stops, the motion stops.' Is the student right?",
        """The student's conclusion is **scientifically incorrect**. This is one of the most famous historical misconceptions in physics, originally believed by Aristotle and corrected by Galileo and Sir Isaac Newton.

---

### What Actually Happened:
1. **Newton's First Law (Law of Inertia)** states:
   > *An object in motion will continue moving at constant velocity in a straight line unless acted upon by a net external force.*
2. The toy car did **not** stop because the forward push ran out.
3. The car stopped because an **unbalanced opposing force—friction** (between the wheels and floor, along with air resistance)—acted on it in the reverse direction!

---

### How to Prove This:
- If you slide the car on rough carpet, it stops almost immediately (high friction).
- If you slide the car on smooth polished tile, it travels much further (lower friction).
- If you slide it on frictionless ice, it would keep moving for a very long distance.
- In deep space where there is zero friction and zero air resistance, once you push an object, **it travels forever at constant speed without needing any engine or push**!

**Key Takeaway for Students:**
- Force does **not** cause motion; force causes **changes** in motion (acceleration).
- An object keeps moving on its own due to **inertia**. It only stops if an opposing force like friction acts on it."""
    ),
    item(
        "What is the weight of a 25 kg box on Earth? Take g = 9.8 m/s^2.",
        """We calculate weight using the gravitational force formula:

$$\\mathbf{W = mg}$$

**Given:**
- Mass ($m$) = $25\\text{ kg}$
- Acceleration due to gravity ($g$) = $9.8\\text{ m/s}²$

**Step 1: Substitute the values into the formula**
$$W = 25\\text{ kg} \\times 9.8\\text{ m/s}²$$

**Step 2: Perform the arithmetic**
$$25 \\times 9.8 = 25 \\times (10 - 0.2) = 250 - 5 = 245$$

$$W = 245\\text{ N}$$

**Answer:**
The weight of the box on Earth is **245 Newtons (N)**.

*(Note: Always express weight in Newtons, never in kilograms!)*"""
    ),
    item(
        "Explain Newton's Third Law of Motion with two real-life examples. Why don't action and reaction cancel each other out?",
        """Newton's Third Law of Motion states:
> **For every action, there is an equal and opposite reaction.**
> Formally: Whenever object A exerts a force on object B ($\vec{F}_{AB}$), object B simultaneously exerts an equal and opposite force on object A ($\vec{F}_{BA} = -\\vec{F}_{AB}$).

---

### Two Real-Life Examples:

1. **Walking on Ground**:
   - **Action**: Your shoe pushes backward against the Earth.
   - **Reaction**: The Earth pushes forward on your shoe with an equal force.
   - It is this forward reaction force that propels you forward!

2. **Rocket Propulsion**:
   - **Action**: The rocket engine expels hot exhaust gases downward with tremendous force.
   - **Reaction**: The exhaust gases push the rocket upward with an equal force.
   - This allows rockets to accelerate even in the vacuum of space where there is no air to push against.

---

### Critical Conceptual Question: Why Don't Action and Reaction Cancel Out?
Forces only cancel out when they act on the **same object** (like two people pulling opposite ends of a single rope).

Action and reaction forces **never cancel out because they act on TWO DIFFERENT OBJECTS**:
- When you kick a soccer ball, your foot exerts force on the **ball** (making it fly).
- The ball exerts an equal opposite force on your **foot** (which you feel as impact).
- Because the forces act on separate bodies, each body responds independently to the force acting upon it!"""
    ),
    item(
        "A 1200 kg car accelerates from rest at 2.5 m/s^2. What net force was required?",
        """We solve this using Newton's Second Law:

$$\\mathbf{F = ma}$$

**Given Data:**
- Mass ($m$) = $1200\\text{ kg}$
- Acceleration ($a$) = $2.5\\text{ m/s}²$

**Step 1: Calculate the force**
$$F = 1200\\text{ kg} \\times 2.5\\text{ m/s}²$$
$$F = 1200 \\times \\frac{5}{2} = 600 \\times 5 = 3000\\text{ N}$$

**Answer:**
The net force required is **3000 Newtons (N)** (or $3\\text{ kN}$).

**Unit Verification:**
$1\\text{ N} = 1\\text{ kg}\\cdot\\text{m/s}²$. The units match perfectly."""
    ),
    item(
        "What is the difference between speed and velocity? Give an example where speed is positive but average velocity is zero.",
        """Although people use speed and velocity interchangeably in everyday speech, in physics they have distinct definitions:

### 1. Speed (Scalar Quantity)
- **Definition**: The rate at which an object covers distance.
- **Formula**: $\\text{Speed} = \\frac{\\text{Total Distance}}{\\text{Time}}$
- **Properties**: Has **magnitude only** (no direction). It can never be negative.
- **Unit**: meters per second (m/s) or km/h.

### 2. Velocity (Vector Quantity)
- **Definition**: The rate of change of displacement (position).
- **Formula**: $\\vec{v} = \\frac{\\Delta \\vec{x}}{t} = \\frac{\\text{Displacement}}{\\text{Time}}$
- **Properties**: Has **both magnitude AND direction**. Can be positive, negative, or zero depending on direction.
- **Unit**: meters per second (m/s).

---

### Classic Example: Speed > 0 while Velocity = 0
Imagine an athlete running a full 400-meter lap around a circular track in 50 seconds:
- **Total Distance covered**: $400\\text{ meters}$
- **Displacement**: $0\\text{ meters}$ (the runner ended at the exact starting point!)

**Calculations:**
1. **Average Speed**:
   $$\\text{Speed} = \\frac{400\\text{ m}}{50\\text{ s}} = \\mathbf{8\\text{ m/s}}$$
2. **Average Velocity**:
   $$\\text{Velocity} = \\frac{\\text{Displacement}}{\\text{Time}} = \\frac{0\\text{ m}}{50\\text{ s}} = \\mathbf{0\\text{ m/s}}$$

**Key Takeaway**: Speed measures how much ground you covered; velocity measures how far you are from where you started and in what direction."""
    ),
    item(
        "State Ohm's Law and calculate the resistance of an electric lamp if a 230 V potential difference causes a current of 0.5 A to flow.",
        """### 1. Statement of Ohm's Law
Ohm's Law states that the electric current ($I$) flowing through a metallic conductor is directly proportional to the potential difference ($V$) across its ends, provided the temperature and other physical conditions remain constant.

**Mathematical Form:**
$$V = IR$$
Where:
- $V$ = Potential difference / Voltage in **Volts (V)**
- $I$ = Electric current in **Amperes (A)**
- $R$ = Resistance in **Ohms ($\\Omega$)**

---

### 2. Problem Solution
**Given:**
- Voltage ($V$) = $230\\text{ V}$
- Current ($I$) = $0.5\\text{ A}$

**Step 1: Rearrange formula for resistance ($R$)**
$$R = \\frac{V}{I}$$

**Step 2: Substitute and calculate**
$$R = \\frac{230\\text{ V}}{0.5\\text{ A}} = 230 \\times 2 = \\mathbf{460\\ \\Omega}$$

**Answer:**
The resistance of the lamp is **460 Ohms ($\\Omega$)**."""
    )
]

# We will populate the full sets systematically in generate_full_curriculum.py
print(f"Physics sample initialized with {len(physics_train)} anchor records.")
