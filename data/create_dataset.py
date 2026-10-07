"""
Creates train.jsonl - 40 high-quality educational Q&A examples
covering Physics, Math, Chemistry, Biology, and Computer Science.
Key focus: clearly distinguishing easily confused concepts.
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

examples = [
  # ============================================================
  # PHYSICS
  # ============================================================
  {
    "messages": [
      {"role": "user", "content": "Explain Newton's second law to a class 8 student in simple language."},
      {"role": "assistant", "content": (
        "Newton's Second Law of Motion says:\n\n"
        "**Force = Mass x Acceleration**  (written as F = ma)\n\n"
        "Let's break each part down:\n\n"
        "- **Force (F)**: A push or a pull on an object. Measured in Newtons (N).\n"
        "- **Mass (m)**: The amount of matter in an object. A heavy truck has more mass than a bicycle. Measured in kilograms (kg).\n"
        "- **Acceleration (a)**: How quickly an object speeds up, slows down, or changes direction. Measured in m/s^2.\n\n"
        "The law tells us two important things:\n"
        "1. The greater the force you apply, the greater the acceleration.\n"
        "2. The greater the mass of the object, the harder it is to accelerate.\n\n"
        "Example: Imagine pushing an empty shopping cart vs a full one. "
        "You need more force to give the full cart the same acceleration.\n\n"
        "Formula: F = ma\n"
        "Units: 1 Newton = 1 kg x 1 m/s^2"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between mass and weight?"},
      {"role": "assistant", "content": (
        "Mass and weight are different things, even though people often confuse them in everyday life.\n\n"
        "**Mass:**\n"
        "- The amount of matter (stuff) in an object.\n"
        "- Does NOT change based on location.\n"
        "- Measured in kilograms (kg).\n"
        "- Example: Your mass is 50 kg whether you are on Earth, the Moon, or in space.\n\n"
        "**Weight:**\n"
        "- The force of gravity pulling on your mass.\n"
        "- CHANGES based on location because gravity differs on different planets.\n"
        "- Measured in Newtons (N).\n"
        "- Formula: Weight = mass x gravitational acceleration  (W = mg)\n\n"
        "Example:\n"
        "- On Earth (g = 9.8 m/s^2): A 10 kg object weighs 98 N.\n"
        "- On the Moon (g = 1.6 m/s^2): The same 10 kg object weighs only 16 N.\n"
        "- The mass stays 10 kg everywhere.\n\n"
        "Key point: Your mass never changes. Your weight depends on gravity."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "A student said 'my weight is 60 kg'. Is this scientifically correct? Explain."},
      {"role": "assistant", "content": (
        "Scientifically, this statement is **incorrect**.\n\n"
        "In physics, **weight** is a force and must be measured in **Newtons (N)**, not kilograms.\n\n"
        "What the student actually means is that their **mass** is 60 kg.\n\n"
        "**Correct terminology:**\n"
        "- My **mass** is 60 kg.\n"
        "- My **weight** on Earth = mass x g = 60 x 9.8 = **588 N**.\n\n"
        "**Key distinction:**\n"
        "- Mass (kg): How much matter you contain. Constant everywhere.\n"
        "- Weight (N): The gravitational force acting on your mass. Changes with location.\n\n"
        "On the Moon (g = 1.6 m/s^2), your mass is still 60 kg, "
        "but your weight would be 60 x 1.6 = 96 N — much less than on Earth."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between speed and velocity?"},
      {"role": "assistant", "content": (
        "Speed and velocity sound similar, but they are different in physics.\n\n"
        "**Speed:**\n"
        "- Tells you how fast an object is moving.\n"
        "- Does NOT include direction.\n"
        "- Speed is a *scalar* quantity (only magnitude).\n"
        "- Formula: Speed = Distance / Time\n"
        "- Example: A car moving at 60 km/h.\n\n"
        "**Velocity:**\n"
        "- Tells you how fast AND in which direction an object is moving.\n"
        "- Velocity is a *vector* quantity (has both magnitude and direction).\n"
        "- Formula: Velocity = Displacement / Time\n"
        "- Example: A car moving at 60 km/h towards the north.\n\n"
        "Why does direction matter?\n"
        "Imagine running a full lap around a circular track and returning to the start. "
        "Your speed was not zero throughout, but your *average velocity* was zero, "
        "because your displacement (change in position) was zero.\n\n"
        "Key point: Speed asks 'how fast?' Velocity asks 'how fast and which way?'"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between force and acceleration?"},
      {"role": "assistant", "content": (
        "Force and acceleration are related but they are not the same thing.\n\n"
        "**Force:**\n"
        "- A push or pull that acts on an object.\n"
        "- Measured in Newtons (N).\n"
        "- Force is the *cause*.\n"
        "- Example: You push a box with 10 N of force.\n\n"
        "**Acceleration:**\n"
        "- The rate at which an object's velocity changes over time.\n"
        "- Measured in m/s^2.\n"
        "- Acceleration is the *effect* produced by force.\n"
        "- Example: The box speeds up at 2 m/s^2 because of the force.\n\n"
        "The relationship (Newton's Second Law): F = ma\n"
        "- More force on the same mass = more acceleration.\n"
        "- Same force on a larger mass = less acceleration.\n\n"
        "Key point: Force causes acceleration. One is the cause, the other is the effect. They are not interchangeable."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "A car of mass 1000 kg accelerates at 2 m/s^2. What force is applied?"},
      {"role": "assistant", "content": (
        "We use Newton's Second Law: **F = ma**\n\n"
        "**Given:**\n"
        "- Mass (m) = 1000 kg\n"
        "- Acceleration (a) = 2 m/s^2\n\n"
        "**Step 1:** Apply the formula.\n"
        "F = m x a\n"
        "F = 1000 x 2\n\n"
        "**Step 2:** Calculate.\n"
        "F = 2000 N\n\n"
        "**Answer: The applied force is 2000 Newtons (N).**\n\n"
        "Note: 1 Newton = 1 kg.m/s^2. Always include units in your answer."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is Newton's First Law of Motion?"},
      {"role": "assistant", "content": (
        "Newton's First Law of Motion is also called the **Law of Inertia**.\n\n"
        "**Statement:** An object at rest stays at rest, and an object in motion stays in motion "
        "at the same speed and in the same direction, unless acted upon by an unbalanced (net) force.\n\n"
        "**What is inertia?**\n"
        "Inertia is the tendency of an object to resist changes in its state of motion. "
        "Heavier objects have more inertia.\n\n"
        "**Real-life examples:**\n"
        "1. When a bus stops suddenly, passengers lurch forward. Their bodies wanted to keep moving.\n"
        "2. A ball rolling on the floor eventually stops because friction acts on it.\n"
        "3. Planets keep orbiting the Sun because there is almost no friction in space.\n\n"
        "Key point: Objects do not change their motion on their own. A net force is always needed to start, stop, or change motion."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is Newton's Third Law? Give two real-life examples."},
      {"role": "assistant", "content": (
        "Newton's Third Law states:\n"
        "**For every action, there is an equal and opposite reaction.**\n\n"
        "When object A exerts a force on object B, object B simultaneously exerts an equal force "
        "in the opposite direction on object A.\n\n"
        "**Example 1 - Rocket launch:**\n"
        "The rocket pushes hot gas downward (action). The gas pushes the rocket upward (reaction). "
        "This is what lifts the rocket off the ground.\n\n"
        "**Example 2 - Walking:**\n"
        "Your foot pushes backward on the ground (action). The ground pushes your foot forward (reaction). "
        "This reaction force is what moves you forward.\n\n"
        "**Important note:**\n"
        "Action and reaction forces are equal in size and opposite in direction, "
        "but they act on DIFFERENT objects. This is why they do not cancel each other out."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is Ohm's Law? A resistor has 10 ohms resistance and 20 V is applied. Find the current."},
      {"role": "assistant", "content": (
        "**Ohm's Law** states that the current through a conductor is directly proportional "
        "to the voltage across it (at constant temperature).\n\n"
        "**Formula:** V = I x R\n\n"
        "Where:\n"
        "- V = Voltage (Volts, V)\n"
        "- I = Current (Amperes, A)\n"
        "- R = Resistance (Ohms)\n\n"
        "Rearranged to find current: I = V / R\n\n"
        "**Problem:** R = 10 ohms, V = 20 V, find I.\n\n"
        "Step 1: Use I = V / R\n"
        "I = 20 / 10\n"
        "I = 2 A\n\n"
        "**Answer: Current = 2 Amperes**\n\n"
        "Physical meaning:\n"
        "- Higher voltage = more current (stronger push for electrons).\n"
        "- Higher resistance = less current (harder for electrons to flow).\n\n"
        "Analogy: Voltage = water pressure, current = flow rate, resistance = pipe narrowness."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is gravitational potential energy? Calculate GPE for a 2 kg book on a 3 m shelf."},
      {"role": "assistant", "content": (
        "**Gravitational Potential Energy (GPE)** is the energy stored in an object "
        "because of its height above a reference point (usually the ground).\n\n"
        "The higher an object is lifted, the more GPE it has.\n\n"
        "**Formula:** GPE = m x g x h\n\n"
        "Where:\n"
        "- m = mass (kg)\n"
        "- g = acceleration due to gravity = 9.8 m/s^2 on Earth\n"
        "- h = height above the ground (m)\n"
        "- GPE is measured in Joules (J)\n\n"
        "**Problem:** m = 2 kg, h = 3 m\n\n"
        "GPE = 2 x 9.8 x 3\n"
        "GPE = 58.8 J\n\n"
        "**Answer: GPE = 58.8 Joules**\n\n"
        "When the book falls, this potential energy converts into kinetic energy (the energy of motion).\n"
        "Key point: No height = no gravitational PE."
      )}
    ]
  },
  # ============================================================
  # MATHEMATICS
  # ============================================================
  {
    "messages": [
      {"role": "user", "content": "Solve 3x + 5 = 20. Show all steps."},
      {"role": "assistant", "content": (
        "**Equation:** 3x + 5 = 20\n\n"
        "**Step 1:** Move the constant to the right side.\n"
        "Subtract 5 from both sides:\n"
        "3x + 5 - 5 = 20 - 5\n"
        "3x = 15\n\n"
        "**Step 2:** Isolate x.\n"
        "Divide both sides by 3:\n"
        "3x / 3 = 15 / 3\n"
        "x = 5\n\n"
        "**Answer: x = 5**\n\n"
        "**Verification:** Substitute x = 5 into the original equation:\n"
        "3(5) + 5 = 15 + 5 = 20 — correct!"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the Pythagorean theorem? A right triangle has legs 3 cm and 4 cm. Find the hypotenuse."},
      {"role": "assistant", "content": (
        "The **Pythagorean theorem** applies to right-angled triangles.\n\n"
        "**Theorem:** In a right triangle, the square of the hypotenuse equals the sum of the squares of the two legs.\n\n"
        "**Formula:** a^2 + b^2 = c^2\n\n"
        "Where a and b are the legs and c is the hypotenuse (the side opposite the right angle).\n\n"
        "**Problem:** a = 3 cm, b = 4 cm, find c.\n\n"
        "Step 1: Apply the formula.\n"
        "3^2 + 4^2 = c^2\n"
        "9 + 16 = c^2\n"
        "25 = c^2\n\n"
        "Step 2: Take the square root.\n"
        "c = sqrt(25) = 5 cm\n\n"
        "**Answer: The hypotenuse is 5 cm.**\n\n"
        "This is the classic 3-4-5 right triangle — a very common geometry example."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "A student scored 45 out of 60 marks. What is the percentage?"},
      {"role": "assistant", "content": (
        "**Percentage Formula:**\n"
        "Percentage = (Obtained Marks / Total Marks) x 100\n\n"
        "**Given:** Obtained = 45, Total = 60\n\n"
        "Step 1: Divide.\n"
        "45 / 60 = 0.75\n\n"
        "Step 2: Multiply by 100.\n"
        "0.75 x 100 = 75\n\n"
        "**Answer: The student scored 75%.**\n\n"
        "Quick check: 75% of 60 = 0.75 x 60 = 45 — correct!"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Calculate simple interest on Rs. 5000 at 6% per year for 3 years."},
      {"role": "assistant", "content": (
        "**Simple Interest (SI)** is calculated only on the original principal, not on accumulated interest.\n\n"
        "**Formula:** SI = (P x R x T) / 100\n\n"
        "Where:\n"
        "- P = Principal = Rs. 5000\n"
        "- R = Rate per year = 6%\n"
        "- T = Time = 3 years\n\n"
        "Step 1: Substitute values.\n"
        "SI = (5000 x 6 x 3) / 100\n\n"
        "Step 2: Calculate numerator.\n"
        "5000 x 6 = 30000\n"
        "30000 x 3 = 90000\n\n"
        "Step 3: Divide by 100.\n"
        "SI = 90000 / 100 = Rs. 900\n\n"
        "**Answer: Simple Interest = Rs. 900**\n\n"
        "Total amount = Principal + SI = 5000 + 900 = **Rs. 5900**"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are prime numbers? List all prime numbers up to 30."},
      {"role": "assistant", "content": (
        "A **prime number** is a whole number greater than 1 that has exactly two factors: 1 and itself.\n\n"
        "It cannot be divided evenly by any other whole number.\n\n"
        "**Examples:**\n"
        "- 7 is prime: divisible only by 1 and 7.\n"
        "- 9 is NOT prime: divisible by 1, 3, and 9.\n\n"
        "**All prime numbers up to 30:**\n"
        "2, 3, 5, 7, 11, 13, 17, 19, 23, 29\n\n"
        "That is **10 prime numbers** up to 30.\n\n"
        "**Important notes:**\n"
        "- 2 is the only even prime number.\n"
        "- 1 is NOT prime (it has only one factor, not two)."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Find the area and perimeter of a rectangle with length 8 cm and width 5 cm."},
      {"role": "assistant", "content": (
        "**Given:** Length (l) = 8 cm, Width (w) = 5 cm\n\n"
        "**Area of a Rectangle:**\n"
        "Formula: Area = l x w\n"
        "Area = 8 x 5 = **40 cm^2**\n"
        "(Area is always measured in square units.)\n\n"
        "**Perimeter of a Rectangle:**\n"
        "Formula: Perimeter = 2 x (l + w)\n"
        "Perimeter = 2 x (8 + 5) = 2 x 13 = **26 cm**\n"
        "(Perimeter is the total distance around the shape.)\n\n"
        "**Summary:**\n"
        "- Area = 40 cm^2\n"
        "- Perimeter = 26 cm"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Explain ratio and proportion with a solved example."},
      {"role": "assistant", "content": (
        "**Ratio** compares two quantities of the same kind.\n"
        "Example: 3 apples to 5 oranges = ratio 3:5\n\n"
        "**Proportion** states that two ratios are equal.\n"
        "Example: 3:5 = 6:10 (both equal 0.6)\n\n"
        "**Solving a proportion problem:**\n"
        "If 4 pencils cost Rs. 12, how much do 10 pencils cost?\n\n"
        "Set up the proportion:\n"
        "4 / 12 = 10 / x\n\n"
        "Cross-multiply:\n"
        "4 x x = 12 x 10\n"
        "4x = 120\n"
        "x = 30\n\n"
        "**Answer: 10 pencils cost Rs. 30.**\n\n"
        "Key rule: In a proportion, product of means = product of extremes."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Explain kinetic energy and potential energy with the example of a falling ball."},
      {"role": "assistant", "content": (
        "**Kinetic Energy (KE):** Energy of motion.\n"
        "Formula: KE = (1/2) x m x v^2\n"
        "More speed = more kinetic energy.\n\n"
        "**Potential Energy (PE):** Stored energy due to position.\n"
        "Formula (gravitational): PE = m x g x h\n"
        "More height = more potential energy.\n\n"
        "**Example — A ball dropped from a height:**\n\n"
        "- At the top: PE is maximum, KE = 0 (ball is not moving yet).\n"
        "- While falling: PE decreases, KE increases as speed builds up.\n"
        "- Just before hitting the ground: KE is maximum, PE is minimum.\n\n"
        "This demonstrates the **Law of Conservation of Energy:**\n"
        "Energy is never created or destroyed — it only converts from one form to another.\n\n"
        "Total energy = PE + KE = constant throughout the fall (ignoring air resistance)."
      )}
    ]
  },
  # ============================================================
  # CHEMISTRY
  # ============================================================
  {
    "messages": [
      {"role": "user", "content": "What is the difference between a physical change and a chemical change? Give examples."},
      {"role": "assistant", "content": (
        "**Physical Change:**\n"
        "- Only form or appearance changes. No new substance is formed.\n"
        "- Usually reversible.\n"
        "- Examples:\n"
        "  - Melting ice (water changes form but is still H2O)\n"
        "  - Cutting paper (smaller pieces, still paper)\n"
        "  - Dissolving sugar in water\n\n"
        "**Chemical Change:**\n"
        "- A new substance with different properties is formed.\n"
        "- Usually irreversible.\n"
        "- Examples:\n"
        "  - Burning wood (produces ash and smoke)\n"
        "  - Rusting of iron (iron becomes iron oxide)\n"
        "  - Cooking an egg\n\n"
        "**Signs of a chemical change:**\n"
        "Change in colour, production of gas, new smell, formation of a precipitate, "
        "or release/absorption of heat (energy change)."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are acids and bases? How do you test for them?"},
      {"role": "assistant", "content": (
        "**Acids:**\n"
        "- Produce hydrogen ions (H+) in water.\n"
        "- Taste sour. Turn blue litmus paper RED.\n"
        "- pH less than 7.\n"
        "- Examples: lemon juice (citric acid), vinegar (acetic acid), stomach acid (HCl).\n\n"
        "**Bases:**\n"
        "- Produce hydroxide ions (OH-) in water.\n"
        "- Feel slippery, taste bitter. Turn red litmus paper BLUE.\n"
        "- pH greater than 7.\n"
        "- Examples: baking soda, soap, ammonia.\n\n"
        "**Neutral:** pH = 7. Example: pure water.\n\n"
        "**Testing with litmus paper:**\n"
        "- Blue litmus turns RED in acid.\n"
        "- Red litmus turns BLUE in base.\n"
        "- No change = neutral.\n\n"
        "**pH scale:** 0 (strongly acidic) to 14 (strongly basic). 7 is neutral."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are elements, compounds, and mixtures?"},
      {"role": "assistant", "content": (
        "**Element:**\n"
        "- Made of only one type of atom.\n"
        "- Cannot be broken down chemically into simpler substances.\n"
        "- Examples: Oxygen (O), Iron (Fe), Gold (Au)\n\n"
        "**Compound:**\n"
        "- Two or more elements chemically joined in a fixed ratio.\n"
        "- Properties differ completely from the original elements.\n"
        "- Can only be separated by chemical reactions.\n"
        "- Examples: Water (H2O), Carbon dioxide (CO2), Table salt (NaCl)\n\n"
        "**Mixture:**\n"
        "- Two or more substances physically combined (not chemically bonded).\n"
        "- Each substance keeps its own properties.\n"
        "- Can be separated by physical methods (filtering, evaporation, magnetism).\n"
        "- Ratio is not fixed.\n"
        "- Examples: Salt water, air, sand and iron filings.\n\n"
        "Key difference: Compound = chemically bonded. Mixture = physically combined."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is photosynthesis? Write the chemical equation."},
      {"role": "assistant", "content": (
        "**Photosynthesis** is the process by which green plants use sunlight, water, "
        "and carbon dioxide to produce glucose (food) and release oxygen.\n\n"
        "It happens in the **chloroplasts** of plant cells, using the green pigment **chlorophyll**.\n\n"
        "**Word equation:**\n"
        "Carbon dioxide + Water --[sunlight + chlorophyll]--> Glucose + Oxygen\n\n"
        "**Chemical equation:**\n"
        "6CO2 + 6H2O --[light energy]--> C6H12O6 + 6O2\n\n"
        "Breaking it down:\n"
        "- 6CO2: Carbon dioxide absorbed from air through stomata.\n"
        "- 6H2O: Water absorbed through roots.\n"
        "- C6H12O6: Glucose — the plant's food, stored as energy.\n"
        "- 6O2: Oxygen released into the air (which is why plants are vital for life).\n\n"
        "Key point: Photosynthesis is how plants make food. "
        "It is also why plants are called **producers** in a food chain."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are the states of matter and how do they differ?"},
      {"role": "assistant", "content": (
        "Matter exists in three main states: **solid, liquid, and gas**.\n\n"
        "**Solid:**\n"
        "- Particles tightly packed in fixed positions.\n"
        "- Definite shape AND definite volume.\n"
        "- Examples: ice, iron, rock.\n\n"
        "**Liquid:**\n"
        "- Particles close together but can flow past each other.\n"
        "- Definite volume but NO definite shape (takes shape of container).\n"
        "- Examples: water, milk, mercury.\n\n"
        "**Gas:**\n"
        "- Particles far apart, move rapidly and randomly.\n"
        "- NO definite shape, NO definite volume (expands to fill container).\n"
        "- Examples: oxygen, steam, air.\n\n"
        "**Changes of state (with heat changes):**\n"
        "- Solid to Liquid: Melting (absorbs heat)\n"
        "- Liquid to Gas: Evaporation / Boiling (absorbs heat)\n"
        "- Gas to Liquid: Condensation (releases heat)\n"
        "- Liquid to Solid: Freezing (releases heat)\n"
        "- Solid to Gas: Sublimation (e.g., dry ice, camphor)"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the water cycle? Explain each stage."},
      {"role": "assistant", "content": (
        "The **water cycle** (hydrological cycle) is the continuous movement of water through Earth's systems.\n\n"
        "**Stages:**\n\n"
        "1. **Evaporation:** The Sun heats water in oceans, rivers, and lakes. "
        "Water turns into water vapour and rises into the atmosphere.\n\n"
        "2. **Transpiration:** Plants release water vapour through their leaves into the air.\n\n"
        "3. **Condensation:** As water vapour rises and cools, it turns back into tiny water droplets. "
        "These collect around dust to form clouds.\n\n"
        "4. **Precipitation:** Water droplets in clouds grow heavy and fall as rain, snow, sleet, or hail.\n\n"
        "5. **Collection:** Precipitation collects in oceans, rivers, and lakes. "
        "Some soaks into the ground (groundwater). Then the cycle repeats.\n\n"
        "Key point: The total amount of water on Earth stays constant. It just keeps changing form and moving."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are renewable and non-renewable energy sources? Give two examples of each."},
      {"role": "assistant", "content": (
        "**Renewable Energy Sources:**\n"
        "- Naturally replenished and will not run out on human timescales.\n"
        "- Generally cleaner and more environmentally friendly.\n"
        "- Examples:\n"
        "  1. Solar energy — captured using solar panels.\n"
        "  2. Wind energy — captured using wind turbines.\n"
        "  (Other examples: hydroelectric, geothermal, tidal energy)\n\n"
        "**Non-Renewable Energy Sources:**\n"
        "- Formed over millions of years. Once used, cannot be replaced quickly.\n"
        "- Burning them releases CO2, contributing to climate change.\n"
        "- Examples:\n"
        "  1. Coal — burned in power plants to generate electricity.\n"
        "  2. Petroleum (oil) — refined into petrol and diesel for vehicles.\n"
        "  (Other examples: natural gas, uranium)\n\n"
        "Key point: Renewable = replenishes naturally. Non-renewable = limited supply, takes millions of years to form."
      )}
    ]
  },
  # ============================================================
  # BIOLOGY
  # ============================================================
  {
    "messages": [
      {"role": "user", "content": "What is the difference between a plant cell and an animal cell?"},
      {"role": "assistant", "content": (
        "Both plant and animal cells are eukaryotic (have a nucleus), but they have important differences.\n\n"
        "**Parts found in BOTH:**\n"
        "- Nucleus, cell membrane, cytoplasm, mitochondria, ribosomes\n\n"
        "**Plant cell ONLY (three unique features):**\n"
        "1. **Cell wall** — rigid outer layer made of cellulose; gives shape and support.\n"
        "2. **Chloroplasts** — contain chlorophyll; site of photosynthesis.\n"
        "3. **Large central vacuole** — stores water, helps maintain cell pressure.\n\n"
        "**Animal cell ONLY:**\n"
        "1. **Centrioles** — help organise cell division.\n"
        "2. No cell wall, no chloroplasts, no large central vacuole.\n\n"
        "Key difference: Plant cells can make their own food (photosynthesis). "
        "Animal cells cannot — they must consume food for energy."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Explain the human digestive system step by step."},
      {"role": "assistant", "content": (
        "The digestive system breaks down food into nutrients the body can absorb.\n\n"
        "**Step-by-step:**\n\n"
        "1. **Mouth:** Teeth break food physically (mechanical digestion). "
        "Saliva contains amylase, which begins breaking down starch (chemical digestion).\n\n"
        "2. **Oesophagus:** Muscular contractions (peristalsis) push food down to the stomach.\n\n"
        "3. **Stomach:** Gastric acid (HCl) kills bacteria; pepsin breaks down proteins. "
        "Food becomes a semi-liquid called chyme.\n\n"
        "4. **Small Intestine:** Main site of digestion and absorption. "
        "Bile (from liver) breaks fats; pancreatic enzymes digest carbohydrates, proteins, and fats. "
        "Nutrients absorbed into the bloodstream.\n\n"
        "5. **Large Intestine:** Water is absorbed from remaining material.\n\n"
        "6. **Rectum and Anus:** Solid waste is stored, then expelled.\n\n"
        "Key point: Digestion = mechanical (physical breaking) + chemical (enzyme-based breakdown)."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between mitosis and meiosis?"},
      {"role": "assistant", "content": (
        "Both are types of cell division, but they serve very different purposes.\n\n"
        "**Mitosis:**\n"
        "- Produces 2 identical daughter cells.\n"
        "- Each daughter cell has the SAME number of chromosomes as the parent (46 in humans).\n"
        "- Cells are genetically identical.\n"
        "- Purpose: growth, repair, and replacement of body cells.\n"
        "- Example: skin cells and liver cells dividing.\n\n"
        "**Meiosis:**\n"
        "- Produces 4 genetically different daughter cells.\n"
        "- Each daughter cell has HALF the chromosomes (23 in humans).\n"
        "- Purpose: production of sex cells (sperm and eggs).\n\n"
        "**Why halving matters:**\n"
        "When sperm (23 chromosomes) fuses with egg (23 chromosomes) at fertilisation, "
        "the resulting cell (zygote) has 46 chromosomes — the correct full number.\n\n"
        "Memory tip: Mitosis = **m**akes **m**ore cells (copies). Meiosis = **m**akes sex cells (halves)."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is DNA and why is it important?"},
      {"role": "assistant", "content": (
        "**DNA** stands for **Deoxyribonucleic Acid**.\n\n"
        "It is a molecule found in the nucleus of nearly every living cell. "
        "DNA contains the genetic instructions for building, operating, and reproducing an organism.\n\n"
        "**Structure:**\n"
        "- Shaped like a twisted ladder called a **double helix**.\n"
        "- The sides are made of alternating sugar and phosphate groups.\n"
        "- The rungs are pairs of nitrogen bases:\n"
        "  - Adenine (A) pairs with Thymine (T)\n"
        "  - Guanine (G) pairs with Cytosine (C)\n\n"
        "**Why is DNA important?**\n"
        "1. Blueprint of life: Contains all instructions (genes) to build proteins that control body functions.\n"
        "2. Heredity: DNA is passed from parents to offspring, explaining family resemblance.\n"
        "3. Unique identity: Every person's DNA is unique (except identical twins) — used in forensic science.\n"
        "4. Cell division: DNA copies itself so each new cell gets a complete set of instructions.\n\n"
        "Key point: DNA is the instruction manual for all living things."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between a food chain and a food web?"},
      {"role": "assistant", "content": (
        "**Food Chain:**\n"
        "- A simple, linear sequence showing who eats whom.\n"
        "- Example: Grass -> Grasshopper -> Frog -> Snake -> Eagle\n"
        "- Shows energy flow in one straight path.\n\n"
        "**Food Web:**\n"
        "- A complex network of many interconnected food chains.\n"
        "- More realistic: most animals eat multiple food sources and are eaten by multiple predators.\n"
        "- Example: A rabbit is eaten by both foxes AND eagles.\n\n"
        "**Energy flow rule:**\n"
        "Energy flows from producers (plants) to consumers. "
        "At each step, about 90% of energy is lost as heat. "
        "This is why food chains rarely have more than 4-5 levels.\n\n"
        "**Levels in a food chain:**\n"
        "- Producer: makes its own food (plants, algae).\n"
        "- Primary consumer: eats producers (herbivores).\n"
        "- Secondary consumer: eats primary consumers.\n"
        "- Apex predator: at the top, not eaten by others.\n\n"
        "Key point: Food chain = simple, linear. Food web = complex, interconnected, more realistic."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What are the differences between arteries, veins, and capillaries?"},
      {"role": "assistant", "content": (
        "All three are blood vessels, but they serve different functions.\n\n"
        "**Arteries:**\n"
        "- Carry blood AWAY from the heart.\n"
        "- Usually carry oxygenated blood (exception: pulmonary artery).\n"
        "- Thick, muscular, elastic walls to handle high pressure.\n"
        "- No valves needed.\n\n"
        "**Veins:**\n"
        "- Carry blood TOWARD the heart.\n"
        "- Usually carry deoxygenated blood (exception: pulmonary vein).\n"
        "- Thinner walls than arteries, lower pressure.\n"
        "- Have valves to prevent backflow.\n\n"
        "**Capillaries:**\n"
        "- Microscopic vessels connecting arteries to veins.\n"
        "- Walls only one cell thick — allows exchange of oxygen, nutrients, and waste "
        "between blood and body cells.\n"
        "- Found in every tissue of the body.\n\n"
        "Memory tip: **A**rteries carry blood **A**way from the heart."
      )}
    ]
  },
  # ============================================================
  # COMPUTER SCIENCE
  # ============================================================
  {
    "messages": [
      {"role": "user", "content": "What is the difference between RAM and storage (HDD/SSD)?"},
      {"role": "assistant", "content": (
        "RAM and storage are both types of memory, but they serve completely different purposes.\n\n"
        "**RAM (Random Access Memory):**\n"
        "- Temporary, working memory.\n"
        "- Stores data the computer is CURRENTLY using.\n"
        "- Very fast to read and write.\n"
        "- Data is LOST when the computer is switched off.\n"
        "- Typically 4-32 GB in modern computers.\n"
        "- Example: When you open a browser, it loads into RAM so the CPU can access it quickly.\n\n"
        "**Storage (HDD / SSD):**\n"
        "- Permanent memory.\n"
        "- Stores data even when the computer is off.\n"
        "- Slower than RAM (SSDs are much faster than HDDs).\n"
        "- Holds your files, operating system, and installed programs.\n"
        "- Typically 256 GB to 2 TB or more.\n\n"
        "**Analogy:** RAM is your desk (active work area). Storage is your filing cabinet (permanent storage).\n\n"
        "Key point: More RAM = run more programs at once. More storage = save more files."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is an algorithm? Write a simple algorithm to find the largest of three numbers."},
      {"role": "assistant", "content": (
        "An **algorithm** is a step-by-step set of instructions to solve a problem.\n\n"
        "A good algorithm must be:\n"
        "- Clear (each step is unambiguous)\n"
        "- Finite (must end after a fixed number of steps)\n"
        "- Effective (actually solves the problem)\n\n"
        "**Algorithm — Find the largest of three numbers A, B, C:**\n\n"
        "Step 1: Read three numbers: A, B, C.\n"
        "Step 2: Set Largest = A.\n"
        "Step 3: If B > Largest, set Largest = B.\n"
        "Step 4: If C > Largest, set Largest = C.\n"
        "Step 5: Print Largest.\n"
        "Step 6: Stop.\n\n"
        "**Python code:**\n"
        "```python\n"
        "a = int(input('First number: '))\n"
        "b = int(input('Second number: '))\n"
        "c = int(input('Third number: '))\n"
        "largest = a\n"
        "if b > largest:\n"
        "    largest = b\n"
        "if c > largest:\n"
        "    largest = c\n"
        "print('Largest:', largest)\n"
        "```\n\n"
        "Key point: Plan the algorithm before writing code."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is a programming loop? Show a Python for loop and while loop example."},
      {"role": "assistant", "content": (
        "A **loop** repeats a block of code multiple times, avoiding repetitive code.\n\n"
        "**1. for loop** — used when you know how many times to repeat.\n\n"
        "```python\n"
        "for i in range(5):\n"
        "    print(i)\n"
        "```\n"
        "Output: 0, 1, 2, 3, 4\n\n"
        "**2. while loop** — repeats as long as a condition is True.\n\n"
        "```python\n"
        "count = 1\n"
        "while count <= 3:\n"
        "    print('Hello')\n"
        "    count = count + 1\n"
        "```\n"
        "Output: Hello, Hello, Hello\n\n"
        "**Use cases:**\n"
        "- Printing a multiplication table\n"
        "- Processing every item in a list\n"
        "- Repeating until user gives valid input\n\n"
        "Key point: Use for loop when repeat count is known. Use while loop when based on a condition."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is binary? Convert the decimal number 13 to binary."},
      {"role": "assistant", "content": (
        "**Binary** is the base-2 number system used by computers. It uses only two digits: **0** and **1**.\n\n"
        "Computers use binary because electronic switches have two states: OFF (0) and ON (1).\n\n"
        "**Converting 13 (decimal) to binary:**\n\n"
        "Method: Divide by 2 repeatedly and record remainders.\n\n"
        "13 / 2 = 6 remainder **1**\n"
        "6  / 2 = 3 remainder **0**\n"
        "3  / 2 = 1 remainder **1**\n"
        "1  / 2 = 0 remainder **1**\n\n"
        "Read remainders from BOTTOM to TOP: **1101**\n\n"
        "**Answer: 13 in decimal = 1101 in binary**\n\n"
        "**Verification (binary back to decimal):**\n"
        "1x2^3 + 1x2^2 + 0x2^1 + 1x2^0\n"
        "= 8 + 4 + 0 + 1 = 13 — correct!"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between the Internet and the World Wide Web?"},
      {"role": "assistant", "content": (
        "People often use these terms interchangeably, but they are different.\n\n"
        "**The Internet:**\n"
        "- A global network of interconnected computers and servers.\n"
        "- It is the physical infrastructure: cables, routers, satellites.\n"
        "- Carries all kinds of data: emails, video calls, file transfers, websites.\n"
        "- Has existed since the 1960s (started as ARPANET).\n\n"
        "**The World Wide Web (WWW):**\n"
        "- A system of web pages that runs ON TOP of the internet.\n"
        "- Web pages are written in HTML and accessed via a browser.\n"
        "- Invented by Tim Berners-Lee in 1989.\n\n"
        "**Analogy:**\n"
        "- The internet is like the road network.\n"
        "- The WWW is like the cars that travel on those roads.\n"
        "- Email and video calls also use the internet but are NOT part of the WWW.\n\n"
        "Key point: All websites use the internet. But not all internet services are part of the WWW."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is the difference between a conductor and an insulator? Give examples."},
      {"role": "assistant", "content": (
        "**Conductor:**\n"
        "- Allows electric current to flow through it easily.\n"
        "- Has free electrons that can move.\n"
        "- Examples:\n"
        "  1. Copper — most common material for electrical wires.\n"
        "  2. Aluminium — used in power transmission lines.\n\n"
        "**Insulator:**\n"
        "- Does NOT allow electric current to flow through it.\n"
        "- Electrons are tightly bound and cannot move freely.\n"
        "- Examples:\n"
        "  1. Rubber — used to coat electrical wires.\n"
        "  2. Plastic — used for handles of tools and plug covers.\n\n"
        "**Real-life application:**\n"
        "An electric wire has a copper core (conductor) coated with plastic or rubber (insulator). "
        "The copper lets electricity flow. The insulator stops you from getting an electric shock.\n\n"
        "Key point: Conductors let electricity through. Insulators block it."
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "What is refraction? Why does a pencil look bent in water?"},
      {"role": "assistant", "content": (
        "**Refraction** is the bending of light when it passes from one medium into another medium "
        "with a different optical density.\n\n"
        "Light travels at different speeds in different media:\n"
        "- In air: ~300,000 km/s\n"
        "- In water: ~225,000 km/s (slower)\n"
        "- In glass: ~200,000 km/s (even slower)\n\n"
        "When light changes speed, it also changes direction — this bending is refraction.\n\n"
        "**Why does a pencil look bent in water?**\n"
        "1. Light from the submerged part of the pencil travels through water.\n"
        "2. When it reaches the water-air boundary, it speeds up and bends (refracts).\n"
        "3. Your eyes trace the incoming light back in a straight line and perceive the pencil "
        "as being in a different position.\n"
        "4. This creates an optical illusion — the pencil appears bent or broken at the water surface.\n\n"
        "Other examples of refraction:\n"
        "- Rainbows (light refracts inside water droplets)\n"
        "- Lenses in glasses and cameras\n"
        "- A swimming pool that looks shallower than it actually is"
      )}
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "How does a function work in Python? Show two examples."},
      {"role": "assistant", "content": (
        "A **function** is a reusable block of code that performs a specific task. "
        "You define it once and call it as many times as needed.\n\n"
        "**Why use functions?**\n"
        "- Avoids repeating the same code.\n"
        "- Makes programs easier to read and debug.\n"
        "- Breaks large problems into smaller parts.\n\n"
        "**Syntax:**\n"
        "```python\n"
        "def function_name(parameters):\n"
        "    # code\n"
        "    return result\n"
        "```\n\n"
        "**Example 1 — Area of a rectangle:**\n"
        "```python\n"
        "def calculate_area(length, width):\n"
        "    area = length * width\n"
        "    return area\n\n"
        "print(calculate_area(8, 5))  # Output: 40\n"
        "```\n\n"
        "**Example 2 — Even or odd checker:**\n"
        "```python\n"
        "def check_even_odd(n):\n"
        "    if n % 2 == 0:\n"
        "        return 'Even'\n"
        "    else:\n"
        "        return 'Odd'\n\n"
        "print(check_even_odd(7))   # Output: Odd\n"
        "print(check_even_odd(12))  # Output: Even\n"
        "```\n\n"
        "Key point: def creates the function. Writing the function name with () calls it."
      )}
    ]
  },
]

out_path = r"C:\Rounak\RVSHACK\data\train.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"Written {len(examples)} examples to {out_path}")

# Validate every line
errors = []
with open(out_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        try:
            obj = json.loads(line.strip())
            assert "messages" in obj, "Missing 'messages' key"
            assert len(obj["messages"]) >= 2, "Need at least 2 messages"
            assert obj["messages"][0]["role"] == "user", "First message must be 'user'"
            assert obj["messages"][-1]["role"] == "assistant", "Last message must be 'assistant'"
        except Exception as e:
            errors.append(f"Line {i}: {e}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print(f"Validation: ALL {len(examples)} lines are valid JSONL")
    print("STATUS: PASS")
