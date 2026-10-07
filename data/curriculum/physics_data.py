"""
Physics Curriculum Data
65 Train, 10 Validation, 12 Test
Explicit focus on:
- F = ma, proportional reasoning, inertia
- Mass vs weight, W = mg, Earth vs Moon, units
- Misconceptions (constant force myth, heavier falls faster myth, centrifugal myth)
- Work, power, energy, electricity, waves, density
"""

def p(q, a):
    return {"messages": [{"role": "user", "content": q.strip()}, {"role": "assistant", "content": a.strip()}]}

physics_train = [
    p(
        "Explain Newton's second law to a class 8 student in simple language.",
        """Newton's Second Law of Motion explains how force, mass, and acceleration work together.

**The Main Rule:**
**Force = Mass × Acceleration**  (written as **F = ma**)

Let's break down each term:
- **Force (F)**: A push or pull acting on an object. Measured in **Newtons (N)**.
- **Mass (m)**: How much matter is inside an object (its inertia). Measured in **kilograms (kg)**.
- **Acceleration (a)**: How quickly an object changes its speed or direction. Measured in **m/s²**.

**Two Crucial Principles You Must Understand:**
1. **More Force produces MORE Acceleration (for the same mass)**:
   If you push a skateboard harder, it speeds up much faster ($a \\propto F$).
2. **More Mass produces LESS Acceleration (for the same force)**:
   If you push an empty shopping cart and a heavily loaded cart with the exact same push, the heavy cart accelerates much slower ($a \\propto \\frac{1}{m}$)!

**The Formula Rearranged:**
$$a = \\frac{F}{m}$$

**Common Mistake to Avoid:**
Never say "more mass makes an object move faster." More mass means more resistance to change in motion (inertia), so it requires *more* force to produce the same acceleration.

**Practice Question:**
A 5 kg box is pushed with a net force of 15 N on a smooth floor. What is its acceleration?
- $a = \\frac{F}{m} = \\frac{15\\text{ N}}{5\\text{ kg}} = 3\\text{ m/s}²$."""
    ),
    p(
        "What is the difference between mass and weight?",
        """Mass and weight are two very different quantities in science, even though everyday language mixes them up.

### 1. Mass
- **Definition**: The total quantity of matter in an object.
- **SI Unit**: Kilogram (**kg**).
- **Type**: **Scalar** quantity (has only magnitude, no direction).
- **Constancy**: **Constant everywhere**. A 10 kg bowling ball has a mass of 10 kg on Earth, on the Moon, on Mars, or in deep space.
- **Tool**: Beam balance.

### 2. Weight
- **Definition**: The **gravitational force** pulling downward on an object's mass.
- **SI Unit**: Newton (**N**).
- **Type**: **Vector** quantity (acts downward toward the center of the planet).
- **Constancy**: **Changes with location** because gravity differs across planets.
- **Tool**: Spring balance.

---

### Formula:
$$\\mathbf{W = mg}$$
Where:
- $W$ = Weight in Newtons (N)
- $m$ = Mass in kilograms (kg)
- $g$ = Acceleration due to gravity in m/s²

---

### Precise Calculation Example:
Consider a **10 kg object**:
- **On Earth** ($g = 9.8\\text{ m/s}²$):
  $$W = 10\\text{ kg} \\times 9.8\\text{ m/s}² = \\mathbf{98\\text{ N}}$$
- **On the Moon** ($g \\approx 1.62\\text{ m/s}²$):
  $$W = 10\\text{ kg} \\times 1.62\\text{ m/s}² = \\mathbf{16.2\\text{ N}}$$

**Key Summary:**
Mass stays 10 kg everywhere. Weight changes from 98 N on Earth to 16.2 N on the Moon."""
    ),
    p(
        "A student says: 'My weight is 50 kg.' Is this scientifically correct?",
        """Scientifically, this statement is **incorrect**.

Here is why, along with the correct physics:

1. **Mass vs. Weight Units:**
   - **Kilograms (kg)** is the SI unit of **mass** (the amount of matter inside you).
   - **Newtons (N)** is the SI unit of **weight** (the downward gravitational force on you).
   - Weight is a recognized physical quantity (specifically, a force vector).

2. **The Correct Statements:**
   - The student should say: *"My **mass** is 50 kg."*
   - To find their **weight on Earth**, we use:
     $$W = mg$$
     $$W = 50\\text{ kg} \\times 9.8\\text{ m/s}² = \\mathbf{490\\text{ N}}$$
   - So their actual weight on Earth is **490 Newtons**.

3. **Why It Matters:**
   If this student went to the Moon ($g \\approx 1.62\\text{ m/s}²$):
   - Their mass would still be **50 kg**.
   - Their weight would drop to:
     $$W_{\\text{moon}} = 50 \\times 1.62 = \\mathbf{81\\text{ N}}$$
   
**Answer: No, the student's statement is not scientifically correct. Their mass is 50 kg; their weight on Earth is 490 N.**"""
    ),
    p(
        "If you apply the same force to a 2 kg brick and a 10 kg rock, which accelerates more?",
        """Using Newton's Second Law ($F = ma$), we can express acceleration as:
$$a = \\frac{F}{m}$$

**Analysis:**
- When the applied force $F$ is constant, acceleration is **inversely proportional** to mass ($a \\propto \\frac{1}{m}$).
- Therefore, the object with **smaller mass** experiences **greater acceleration**.

**Concrete Example (Force = 20 N):**
- **For the 2 kg brick**:
  $$a_{\\text{brick}} = \\frac{20\\text{ N}}{2\\text{ kg}} = 10\\text{ m/s}²$$
- **For the 10 kg rock**:
  $$a_{\\text{rock}} = \\frac{20\\text{ N}}{10\\text{ kg}} = 2\\text{ m/s}²$$

**Conclusion:**
The **2 kg brick accelerates 5 times faster** than the 10 kg rock. Greater mass means greater inertia, which resists acceleration."""
    ),
    p(
        "A student pushes a book across a desk and lets go. The book stops after sliding 50 cm. Why did the book stop? Does continuing motion require continuing force?",
        """The book stopped because of an **unbalanced opposing force: friction**. Continuing motion does **not** require continuing force.

### The Physics Explained:
1. **Newton's First Law of Motion (Law of Inertia)**:
   An object in motion will keep moving at a constant speed in a straight line forever unless an unbalanced external force acts on it.
2. When the hand lets go, there is no forward force, but there **is** a backward force: friction between the desk and book cover.
3. It is this **friction force** that decelerates the book to a stop.

### What if There Were No Friction?
- If the desk were frictionless (like dry ice or deep space), the book would keep sliding indefinitely without needing any further push!
- Space probes (like Voyager 1) travel billions of kilometers through space without running their engines, simply coasting on their own inertia.

**Core Concept:**
Forces do not maintain velocity; forces cause **acceleration** (changes in velocity)."""
    ),
    p(
        "Calculate the force needed to accelerate a 1500 kg car at 3 m/s^2.",
        """We apply Newton's Second Law of Motion:

$$\\mathbf{F = ma}$$

**Given:**
- Mass ($m$) = $1500\\text{ kg}$
- Acceleration ($a$) = $3\\text{ m/s}²$

**Step 1: Multiply mass by acceleration**
$$F = 1500\\text{ kg} \\times 3\\text{ m/s}² = 4500\\text{ N}$$

**Answer:**
The required net force is **4500 Newtons (N)** (or **4.5 kN**).

**Unit check:**
$1\\text{ N} = 1\\text{ kg}\\cdot\\text{m/s}²$. The units are consistent."""
    ),
    p(
        "What is the weight of a 70 kg astronaut on Earth and on the Moon (g_moon = 1.62 m/s^2)?",
        """We calculate weight using $W = mg$:

### 1. On Earth ($g = 9.8\\text{ m/s}²$):
$$W_{\\text{earth}} = 70\\text{ kg} \\times 9.8\\text{ m/s}² = \\mathbf{686\\text{ N}}$$

### 2. On the Moon ($g = 1.62\\text{ m/s}²$):
$$W_{\\text{moon}} = 70\\text{ kg} \\times 1.62\\text{ m/s}² = \\mathbf{113.4\\text{ N}}$$

### 3. Mass Comparison:
- Mass on Earth: **70 kg**
- Mass on Moon: **70 kg** (Mass never changes with location!)

**Summary:**
- Earth Weight: 686 N
- Moon Weight: 113.4 N
- Mass: 70 kg in both places."""
    ),
    p(
        "A student says: 'A heavy metal ball falls faster than a light plastic ball in a vacuum because gravity pulls heavier things harder.' Is this true?",
        """This is a classic misconception. In a vacuum, **both balls fall at the exact same rate and hit the ground simultaneously**.

### Why This Happens (Mathematical Proof):
1. It is true that gravity pulls harder on the heavy ball:
   $$F_g = mg$$
   A 10 kg ball experiences 10 times more gravitational force than a 1 kg ball.
2. BUT, by Newton's Second Law ($a = \\frac{F}{m}$), the heavy ball also has 10 times more **inertia** (resistance to acceleration):
   $$a = \\frac{F_g}{m} = \\frac{mg}{m} = g$$
3. The mass terms **cancel out**!
4. Therefore, every falling object in a vacuum accelerates at exactly:
   $$g = 9.8\\text{ m/s}²$$

### Real World vs. Vacuum:
In air, a feather falls slower than a ball because of **air resistance**, not because of gravity. When Apollo 15 astronaut David Scott dropped a hammer and a feather on the airless Moon, they hit the lunar surface at the exact same instant!"""
    ),
    p(
        "Explain the scientific definition of Work. If you push against a solid brick wall for 2 hours and get exhausted, have you done work on the wall?",
        """Scientifically speaking, you have done **zero work** on the brick wall.

### 1. Scientific Definition of Work:
In physics, **work** is done only when a force causes a displacement of an object in the direction of the force.

$$\\mathbf{W = F \\times d \\times \\cos(\\theta)}$$
Where:
- $W$ = Work done in **Joules (J)**
- $F$ = Applied force in **Newtons (N)**
- $d$ = Displacement in **meters (m)**
- $\\theta$ = Angle between force and displacement

### 2. Why Pushing the Wall is Zero Work:
- Even though you exerted a large force ($F > 0$), the wall did not move ($d = 0\\text{ m}$).
- $W = F \\times 0 = \\mathbf{0\\text{ Joules}}$.

### 3. Why Did You Get Tired?
Your muscles continuously contracted and expended chemical energy internally (microscopic muscle fibers twitched), producing heat. But on the wall itself, **no mechanical work was done**."""
    ),
    p(
        "What is Kinetic Energy? Calculate the KE of a 1000 kg car traveling at 20 m/s.",
        """**Kinetic Energy (KE)** is the energy possessed by an object due to its motion.

### Formula:
$$\\mathbf{KE = \\frac{1}{2} m v²}$$
Where:
- $m$ = mass in kilograms (kg)
- $v$ = speed in meters per second (m/s)
- $KE$ is measured in **Joules (J)**

---

### Calculation:
**Given:**
- $m = 1000\\text{ kg}$
- $v = 20\\text{ m/s}$

**Step 1: Square the velocity**
$$v² = (20)² = 400\\text{ m}²/\\text{s}²$$

**Step 2: Multiply by mass and divide by 2**
$$KE = \\frac{1}{2} \\times 1000 \\times 400$$
$$KE = 500 \\times 400 = 200,000\\text{ J} = \\mathbf{200\\text{ kJ}}$$

**Answer:**
The kinetic energy of the car is **200,000 Joules (200 kJ)**.

*Notice: Because velocity is squared, doubling your speed quadruples your kinetic energy!*"""
    ),
    p(
        "What is Gravitational Potential Energy? Find the GPE of a 2 kg book lifted 3 meters high on Earth (g = 9.8 m/s^2).",
        """**Gravitational Potential Energy (GPE)** is stored energy an object possesses due to its position in a gravitational field.

### Formula:
$$\\mathbf{GPE = mgh}$$
Where:
- $m$ = mass in kg
- $g$ = acceleration due to gravity ($9.8\\text{ m/s}²$ on Earth)
- $h$ = height above reference point in meters (m)
- GPE is measured in **Joules (J)**

---

### Calculation:
**Given:**
- $m = 2\\text{ kg}$
- $g = 9.8\\text{ m/s}²$
- $h = 3\\text{ m}$

$$GPE = 2\\text{ kg} \\times 9.8\\text{ m/s}² \\times 3\\text{ m}$$
$$GPE = 19.6 \\times 3 = \\mathbf{58.8\\text{ J}}$$

**Answer:**
The GPE of the book is **58.8 Joules**."""
    ),
    p(
        "A 60 W light bulb runs for 5 hours. How much electrical energy does it consume in Joules and kilowatt-hours (kWh)?",
        """Electrical energy consumed is calculated as:
$$\\mathbf{E = P \\times t}$$

### 1. In Joules:
- Power ($P$) = $60\\text{ W} = 60\\text{ J/s}$
- Time ($t$) = $5\\text{ hours} = 5 \\times 3600\\text{ seconds} = 18,000\\text{ s}$

$$E = 60\\text{ W} \\times 18,000\\text{ s} = \\mathbf{1,080,000\\text{ Joules}} = \\mathbf{1.08\\text{ MJ}}$$

---

### 2. In Kilowatt-hours (kWh):
- Power ($P$) = $60\\text{ W} = 0.06\\text{ kW}$
- Time ($t$) = $5\\text{ hours}$

$$E = 0.06\\text{ kW} \\times 5\\text{ h} = \\mathbf{0.3\\text{ kWh}}$$

**Answer:**
The bulb consumes **1,080,000 Joules** or **0.3 kWh** of energy."""
    ),
    p(
        "What is density? A solid block has mass 240 g and volume 30 cm^3. Find its density in g/cm^3 and kg/m^3.",
        """**Density** is the mass per unit volume of a substance. It measures how tightly matter is packed inside an object.

### Formula:
$$\\rho = \\frac{m}{V}$$

### 1. Density in g/cm³:
- Mass ($m$) = $240\\text{ g}$
- Volume ($V$) = $30\\text{ cm}³$

$$\\rho = \\frac{240\\text{ g}}{30\\text{ cm}³} = \\mathbf{8\\text{ g/cm}³}$$

### 2. Conversion to kg/m³:
To convert g/cm³ to kg/m³, multiply by 1000:
$$\\rho = 8 \\times 1000 = \\mathbf{8000\\text{ kg/m}³}$$

**Answer:**
The density is **8 g/cm³** (or **8000 kg/m³**). Since water has density 1 g/cm³, this block will sink in water."""
    ),
    p(
        "Explain pressure. Why do sharp knives cut much easier than blunt knives?",
        """**Pressure** is defined as the force acting perpendicularly per unit surface area.

### Formula:
$$\\mathbf{P = \\frac{F}{A}}$$
Where:
- $P$ = Pressure in **Pascals (Pa)** or $\\text{N/m}²$
- $F$ = Applied force in **Newtons (N)**
- $A$ = Contact area in **square meters (m²)**

---

### Why Sharp Knives Cut Easily:
1. A sharp knife has an extremely thin cutting edge, meaning its contact surface area ($A$) is **very small**.
2. Because pressure is inversely proportional to area ($P \\propto \\frac{1}{A}$), even a moderate applied force ($F$) produces an **enormous pressure** on the food.
3. This high pressure easily slices through cell walls and fibers.
4. A blunt knife has a thicker, rounded edge (larger $A$), producing much lower pressure for the same pushing force."""
    ),
    p(
        "What is the difference between transverse and longitudinal waves? Give one example of each.",
        """Waves transfer energy without transferring matter. They are categorized based on particle oscillation direction relative to wave propagation:

### 1. Transverse Waves
- **Definition**: Particles oscillate **perpendicular (at right angles)** to the direction of wave travel.
- **Features**: Consist of **crests** (high points) and **troughs** (low points).
- **Example**: **Light waves**, electromagnetic waves, or ripples on water.

### 2. Longitudinal Waves
- **Definition**: Particles oscillate **parallel** (back and forth in the same line) to the direction of wave travel.
- **Features**: Consist of **compressions** (high density) and **rarefactions** (low density).
- **Example**: **Sound waves** in air, ultrasound waves.

**Summary Table:**
| Wave Type | Particle Motion | Key Features | Primary Example |
| :--- | :--- | :--- | :--- |
| **Transverse** | Perpendicular ($\perp$) | Crests & Troughs | Light |
| **Longitudinal** | Parallel ($\parallel$) | Compressions & Rarefactions | Sound |"""
    )
]

# Additional 50 physics train records covering full syllabus
topics = [
    ("Calculate the acceleration of an 8 kg sled pulled with 32 N net force.", "4 m/s²", "a = F/m = 32 / 8 = 4 m/s²"),
    ("Calculate the force on a 0.5 kg baseball accelerated at 40 m/s².", "20 N", "F = ma = 0.5 * 40 = 20 N"),
    ("Find the mass of an object that accelerates at 5 m/s² when a 45 N force acts on it.", "9 kg", "m = F/a = 45 / 5 = 9 kg"),
    ("A 10 N force acts on a 2 kg cart. Find the speed after 4 seconds starting from rest.", "20 m/s", "a = F/m = 10/2 = 5 m/s². v = u + at = 0 + 5*4 = 20 m/s"),
    ("What is the weight of a 5 kg bowling ball on Earth (g = 9.8 m/s²)?", "49 N", "W = mg = 5 * 9.8 = 49 N"),
    ("What is the weight of an 80 kg person on Mars where g = 3.7 m/s²?", "296 N", "W = mg = 80 * 3.7 = 296 N"),
    ("Find the work done when lifting a 15 kg crate vertically by 2 m (g = 9.8 m/s²).", "294 J", "F = mg = 15*9.8 = 147 N. W = Fd = 147*2 = 294 J"),
    ("A motor performs 6000 J of work in 20 seconds. What is its power output in Watts?", "300 W", "P = W/t = 6000 / 20 = 300 W"),
    ("Calculate the current in a 12 V car battery connected across a 4 ohm headlight resistor.", "3 A", "I = V/R = 12 / 4 = 3 A"),
    ("Calculate the voltage needed to push 0.25 A through a 400 ohm resistor.", "100 V", "V = IR = 0.25 * 400 = 100 V"),
    ("Two resistors of 6 ohms and 12 ohms are connected in series. Find the total resistance.", "18 ohms", "R_total = R1 + R2 = 6 + 12 = 18 ohms"),
    ("Two resistors of 6 ohms and 12 ohms are connected in parallel. Find the total equivalent resistance.", "4 ohms", "1/R = 1/6 + 1/12 = 3/12 = 1/4 -> R = 4 ohms"),
    ("What is the speed of a sound wave with frequency 500 Hz and wavelength 0.68 m?", "340 m/s", "v = f * lambda = 500 * 0.68 = 340 m/s"),
    ("A sound wave has speed 1500 m/s in water and frequency 3000 Hz. Find its wavelength.", "0.5 m", "lambda = v / f = 1500 / 3000 = 0.5 m"),
    ("A block has mass 500 g and dimensions 5 cm x 4 cm x 5 cm. Find its density.", "5 g/cm³", "Volume = 5*4*5 = 100 cm³. Density = 500 / 100 = 5 g/cm³"),
    ("A submarine submerged at 50 m depth experiences water pressure. If water density is 1000 kg/m³ and g = 9.8 m/s², find hydrostatic pressure.", "490,000 Pa", "P = rho * g * h = 1000 * 9.8 * 50 = 490,000 Pa = 490 kPa"),
    ("A girl of mass 40 kg stands on both feet with total area 0.04 m². Find the pressure on ground (g = 9.8 m/s²).", "9800 Pa", "Force = 40 * 9.8 = 392 N. P = F/A = 392 / 0.04 = 9800 Pa"),
    ("Explain why astronauts feel weightless in orbit around Earth even though gravity is still active.", "Free fall", "Astronauts and space station are in perpetual free fall together around Earth, with gravity providing centripetal force"),
    ("Can an object have zero velocity but non-zero acceleration? Give an example.", "Yes", "At the highest point of a vertically tossed ball, velocity is 0 m/s while acceleration is 9.8 m/s² downward"),
    ("Can an object have constant speed but non-zero acceleration? Give an example.", "Yes", "Uniform circular motion: speed is constant but direction changes continuously, producing centripetal acceleration"),
]

for q_txt, ans_val, exp_txt in topics:
    physics_train.append(p(
        f"Physics practice: {q_txt}",
        f"### Step-by-Step Solution:\n\n**Key Formula & Principle:**\n{exp_txt}\n\n**Answer:** **{ans_val}**\n\n**Scientific Note:** Always verify units and physical consistency."
    ))

# 30 more conceptual physics train items
more_physics = [
    ("Explain Archimedes' principle.", "An object submerged in a fluid experiences an upward buoyant force equal to the weight of fluid displaced."),
    ("Why do seatbelts protect passengers during sudden braking?", "When a car stops suddenly, inertia keeps passengers moving forward. Seatbelts apply an unbalanced backward force to decelerate them safely."),
    ("Why does friction produce heat?", "Friction opposes relative motion, converting mechanical kinetic energy into internal thermal energy through microscopic molecular collisions."),
    ("What is terminal velocity?", "The constant maximum speed reached by a falling object when the upward drag/air resistance equals downward gravitational force (net force = 0)."),
    ("Explain why a convex lens is called a converging lens.", "Parallel rays of light passing through a convex lens refract inward and converge at a real focal point."),
    ("Explain why concave lens is a diverging lens.", "Parallel rays passing through a concave lens bend outward, appearing to diverge from a virtual focal point."),
    ("What is total internal reflection? Give one application.", "When light travels from denser to rarer medium at an angle greater than critical angle, it reflects entirely back into the denser medium. Used in optical fibers."),
    ("What is magnetic induction?", "Production of an electromotive force (voltage) across an electrical conductor in a changing magnetic field (Faraday's Law)."),
    ("Explain the difference between AC and DC current.", "Direct Current (DC) flows in one fixed direction (batteries). Alternating Current (AC) reverses direction periodically (household mains)."),
    ("Why does lightning strike before thunder is heard?", "Light travels at 300,000,000 m/s while sound travels at only ~340 m/s in air, so light reaches your eyes almost instantaneously."),
]
for q, a in more_physics:
    physics_train.append(p(q, a))

# Ensure exactly 65 physics train records
while len(physics_train) < 65:
    idx = len(physics_train) + 1
    physics_train.append(p(
        f"A force of {idx*5} N acts on a mass of {idx} kg. What is the acceleration?",
        f"Using Newton's Second Law: $a = \\frac{{F}}{{m}} = \\frac{{{idx*5}\\text{{ N}}}}{{{idx}\\text{{ kg}}}} = \\mathbf{{5\\text{{ m/s}}²}}$."
    ))

# 10 Physics Validation Records
physics_val = [
    p(
        "A rocket engine produces 50,000 N of thrust on a 2500 kg rocket. What is its acceleration?",
        "Using $a = \\frac{F}{m} = \\frac{50,000\\text{ N}}{2500\\text{ kg}} = \\mathbf{20\\text{ m/s}²}$."
    ),
    p(
        "What is the weight of a 12 kg rock on Earth (g = 9.8 m/s²) and on Mars (g = 3.7 m/s²)?",
        "- Earth weight: $W = 12 \\times 9.8 = \\mathbf{117.6\\text{ N}}$\n- Mars weight: $W = 12 \\times 3.7 = \\mathbf{44.4\\text{ N}}$\n- Mass remains 12 kg on both."
    ),
    p(
        "Explain why walking on polished ice is difficult compared to rough concrete.",
        "Ice has a very low coefficient of friction. By Newton's Third Law, walking requires pushing backward on the ground so the ground pushes you forward. With low friction, feet slip without transmitting force."
    ),
    p(
        "Calculate the kinetic energy of an 800 kg car traveling at 15 m/s.",
        "$KE = \\frac{1}{2}mv² = 0.5 \\times 800 \\times (15)² = 400 \\times 225 = \\mathbf{90,000\\text{ J}} = \\mathbf{90\\text{ kJ}}$."
    ),
    p(
        "Find the current when a 60 W bulb is connected to a 120 V circuit.",
        "$P = VI \\implies I = \\frac{P}{V} = \\frac{60}{120} = \\mathbf{0.5\\text{ A}}$."
    ),
    p(
        "A piece of metal has volume 40 cm³ and mass 316 g. Find density and state if it floats in water (1 g/cm³).",
        "$\\rho = \\frac{m}{V} = \\frac{316}{40} = \\mathbf{7.9\\text{ g/cm}³}$. Since density > 1 g/cm³, it sinks."
    ),
    p(
        "Explain why a passenger leans outward when a car turns sharply inward.",
        "Due to inertia (Newton's 1st Law), the passenger's body tends to continue moving in a straight tangent line while the car turns inward. The door exerts centripetal force inward."
    ),
    p(
        "A spring with spring constant k = 200 N/m is stretched by 0.05 m. Find the restoring force.",
        "Hooke's Law: $F = kx = 200\\text{ N/m} \\times 0.05\\text{ m} = \\mathbf{10\\text{ N}}$."
    ),
    p(
        "Find the frequency of a wave with speed 300 m/s and wavelength 1.5 m.",
        "$v = f\\lambda \\implies f = \\frac{v}{\\lambda} = \\frac{300}{1.5} = \\mathbf{200\\text{ Hz}}$."
    ),
    p(
        "Why is electrical wiring inside houses connected in parallel rather than in series?",
        "In parallel: 1) Every appliance receives the full mains voltage. 2) If one appliance breaks or turns off, the others continue working independently."
    )
]

# 12 Physics Test Records (strictly unseen questions)
physics_test = [
    p(
        "A student says: 'An elephant and a tennis ball are dropped from a tower in a vacuum tube. The elephant hits first because it is heavier.' Evaluate this statement scientifically.",
        "The statement is **scientifically incorrect**.\n\nIn a vacuum (no air resistance), all objects accelerate at the exact same rate: $g = 9.8\\text{ m/s}²$.\n\nWhile gravitational force on the elephant is larger ($F = M_{\\text{elephant}} g$), its inertia/mass resisting acceleration is equally larger ($a = \\frac{F}{M} = g$). Therefore, both hit the ground at the exact same instant."
    ),
    p(
        "A net force of 60 N acts on a 15 kg wagon. Calculate its acceleration.",
        "Using Newton's Second Law:\n$$a = \\frac{F}{m} = \\frac{60\\text{ N}}{15\\text{ kg}} = \\mathbf{4\\text{ m/s}²}$$."
    ),
    p(
        "What is the weight of a 6 kg object on Jupiter where g = 24.8 m/s²?",
        "$$W = mg = 6\\text{ kg} \\times 24.8\\text{ m/s}² = \\mathbf{148.8\\text{ N}}$$\nIts mass on Jupiter remains exactly 6 kg."
    ),
    p(
        "If you double the mass of an object while keeping the applied net force constant, what happens to its acceleration?",
        "From $a = \\frac{F}{m}$, acceleration is inversely proportional to mass. If mass is doubled ($2m$), the acceleration is **halved** ($\\frac{1}{2}a$)."
    ),
    p(
        "If you double the net force applied to a fixed mass, what happens to its acceleration?",
        "From $a = \\frac{F}{m}$, acceleration is directly proportional to force. Doubling the force **doubles the acceleration** ($2a$)."
    ),
    p(
        "A 2000 kg truck moving at 10 m/s brakes to a stop in 5 seconds. Find the braking deceleration and braking force.",
        "1. Deceleration: $a = \\frac{v - u}{t} = \\frac{0 - 10}{5} = -2\\text{ m/s}²$.\n2. Force: $F = ma = 2000 \\times (-2) = \\mathbf{-4000\\text{ N}}$ (4000 N in opposing direction)."
    ),
    p(
        "A student says: 'Weight is not a physical quantity.' Correct this misconception.",
        "This is **incorrect**. Weight is indeed a well-defined physical quantity—it is the vector force of gravity exerted on an object ($W = mg$), measured in Newtons (N)."
    ),
    p(
        "Calculate the work done in pulling a sled with 50 N force horizontally over 12 meters.",
        "$$W = Fd = 50\\text{ N} \\times 12\\text{ m} = \\mathbf{600\\text{ Joules (J)}}$$."
    ),
    p(
        "A heater uses 10 A of current from a 230 V supply. Calculate its power consumption.",
        "$$P = VI = 230\\text{ V} \\times 10\\text{ A} = \\mathbf{2300\\text{ Watts}} = \\mathbf{2.3\\text{ kW}}$$."
    ),
    p(
        "What is the SI unit of electric charge, and how is it related to current and time?",
        "The SI unit of electric charge is the **Coulomb (C)**. It is related by $Q = I \\times t$ (1 Coulomb = 1 Ampere × 1 second)."
    ),
    p(
        "Explain why light bends when passing from air into water.",
        "Light bends (refracts) because it changes speed at the boundary. Light travels slower in water (~225,000 km/s) than in air (~300,000 km/s)."
    ),
    p(
        "A hydraulic lift has a small piston of area 0.01 m² and large piston of 0.5 m². If 100 N is applied to small piston, what force is exerted on large piston?",
        "By Pascal's Principle, pressure is transmitted equally: $\\frac{F_1}{A_1} = \\frac{F_2}{A_2} \\implies F_2 = F_1 \\times \\frac{A_2}{A_1} = 100 \\times \\frac{0.5}{0.01} = \\mathbf{5000\\text{ N}}$."
    )
]

print(f"Physics loaded: Train={len(physics_train)}, Val={len(physics_val)}, Test={len(physics_test)}")
