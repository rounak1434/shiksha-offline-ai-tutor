"""
science_generator.py
Generates curriculum-aligned Science (Physics, Chemistry, Biology) records for Class 1 to Class 8.
Strict adherence to scientific facts, SI units, and age-appropriate pedagogy.
"""

def make_science_entry(grade, domain, topic, difficulty, q_type, q_text, ans_text, source="Curriculum-aligned NCERT Science"):
    user_prompt = f"Student grade: Class {grade}\nSubject: Science ({domain})\nQuestion: {q_text.strip()}"
    return {
        "metadata": {
            "grade": grade,
            "subject": f"Science ({domain})",
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

def generate_science_records():
    records = []
    
    # -------------------------------------------------------------
    # CLASS 1 - 2 SCIENCE
    # -------------------------------------------------------------
    c1_2_science = [
        (1, "Biology", "Living Things", "foundational", "conceptual_explanation",
         "What is the difference between living and non-living things?",
         "Here is the simple difference:\n\n### 1. Living Things (Like You, a Puppy, or a Tree! 🐶🌳)\n- They **grow** bigger.\n- They need **food and water**.\n- They **breathe** air.\n- They can have babies or produce seeds.\n\n### 2. Non-Living Things (Like a Toy Car, a Rock, or a Pencil 🚗✏️)\n- They do **not grow**.\n- They do **not eat or drink**.\n- They do **not breathe**.\n\nA puppy runs on its own because it is alive. A toy car only moves if you push it!"),
         
        (1, "Biology", "Human Body", "foundational", "conceptual_explanation",
         "What are our 5 senses and what body parts do we use for them?",
         "We have **5 wonderful senses** that help us explore the world around us:\n\n1. **Sight (Seeing)**: With our **Eyes** 👀 (seeing colors and rainbows).\n2. **Hearing (Listening)**: With our **Ears** 👂 (hearing music and bird songs).\n3. **Smell**: With our **Nose** 👃 (smelling flowers and food).\n4. **Taste**: With our **Tongue** 👅 (tasting sweet ice cream and fruit).\n5. **Touch (Feeling)**: With our **Skin** 🖐️ (feeling warm sun and soft blankets)."),
         
        (2, "Biology", "Plant Parts", "easy", "conceptual_explanation",
         "What are the main parts of a plant and what do they do?",
         "A plant has 4 main parts, each with a special job:\n\n1. **Roots (Under the soil)**: Drink water from the ground and hold the plant firmly in the dirt.\n2. **Stem (The trunk/stalk)**: Acts like a drinking straw, carrying water up to the leaves.\n3. **Leaves (Green solar panels)**: Use sunlight to make food for the plant.\n4. **Flowers**: Make seeds so new baby plants can grow!")
    ]
    for g, domain, topic, diff, qtype, q, a in c1_2_science:
        records.append(make_science_entry(g, domain, topic, diff, qtype, q, a, f"NCERT Class {g} EVS"))

    # -------------------------------------------------------------
    # CLASS 3 - 5 SCIENCE
    # -------------------------------------------------------------
    c3_5_science = [
        (3, "Chemistry", "States of Matter", "easy", "conceptual_explanation",
         "What are the three states of matter? Give an example of water in all three states.",
         "Everything around us is matter! Matter exists in **three main states**:\n\n### 1. Solid\n- Has a fixed shape and size. It does not change shape unless you break or melt it.\n- **Water as a solid**: **Ice** 🧊\n\n### 2. Liquid\n- Flows and takes the shape of whatever cup or bottle you pour it into.\n- **Water as a liquid**: Drinking water from the tap 💧\n\n### 3. Gas\n- Has no fixed shape and spreads out to fill the whole room or balloon.\n- **Water as a gas**: **Steam / Water vapor** rising from a hot kettle ♨️"),
         
        (4, "Biology", "Food Chains", "easy", "conceptual_explanation",
         "What is a simple food chain? Can you show an example?",
         "A **food chain shows who eats whom** and how energy moves from the Sun to living things!\n\n### Example of a Simple Grassland Food Chain:\n1. **The Sun ☀️**: Gives light energy.\n2. **Grass (Producer 🌱)**: Uses sunlight to make its own food.\n3. **Grasshopper (Primary Consumer 🦗)**: Eats the grass.\n4. **Frog (Secondary Consumer 🐸)**: Eats the grasshopper.\n5. **Hawk (Apex Predator 🦅)**: Eats the frog.\n\nEnergy flows in one direction: Sun → Grass → Grasshopper → Frog → Hawk!"),
         
        (5, "Physics", "Simple Machines", "medium", "conceptual_explanation",
         "What is an inclined plane, and how does it help us do work?",
         "An **inclined plane** is a simple machine that is just a **flat, sloping ramp** connecting a lower level to a higher level.\n\n### How it helps us:\n- Imagine lifting a heavy 50 kg box straight up into a truck. Lifting it vertically requires a huge burst of force all at once.\n- If you place a ramp (inclined plane) up to the truck, you can push the box up the slope.\n- **The force required is much smaller** than lifting it straight up!\n\n**The Trade-off**: You push the box over a longer distance along the ramp, but you use much less effort at any single moment.\n\n**Examples in Daily Life**: Wheelchair ramps, playground slides, winding mountain roads.")
    ]
    for g, domain, topic, diff, qtype, q, a in c3_5_science:
        records.append(make_science_entry(g, domain, topic, diff, qtype, q, a, f"NCERT Class {g} EVS/Science"))

    # -------------------------------------------------------------
    # CLASS 6 SCIENCE
    # -------------------------------------------------------------
    c6_science = [
        ("Physics", "Light and Shadows", "easy", "conceptual_explanation",
         "How is a shadow formed? Can a transparent object cast a shadow?",
         "A shadow is formed when light is blocked by an object.\n\n### How it happens:\n1. Light travels in **straight lines**.\n2. When an **opaque object** (like a wooden door or your body) stands in the path of light, the light rays cannot pass through it or bend around it.\n3. The dark area created behind the object where light cannot reach is called a **shadow**.\n\n### Can a transparent object cast a shadow?\n**No.** Transparent objects (like clear clean glass or water) allow almost all light to pass directly through them. Because they do not block light, they do not cast a distinct dark shadow."),
         
        ("Physics", "Electricity and Circuits", "medium", "conceptual_explanation",
         "What is the difference between a closed circuit and an open circuit? Why does a bulb only glow in a closed circuit?",
         "An electric circuit is a complete path along which electric current can flow.\n\n### 1. Closed Circuit (Complete Path)\n- The wires, switch, battery, and bulb form an unbroken loop.\n- Electric current leaves the positive terminal of the cell, flows through the bulb filament, and returns to the negative terminal.\n- **Result**: The bulb **glows**! 💡\n\n### 2. Open Circuit (Incomplete Path)\n- If the switch is turned OFF, or a wire is disconnected, or the bulb filament is broken (fused).\n- There is a gap in the path. Air is an insulator, so electric current cannot jump the gap.\n- **Result**: Current stops flowing immediately, and the bulb **does not glow**."),
         
        ("Chemistry", "Separating Substances", "medium", "conceptual_explanation",
         "How can you separate a mixture of sand, salt, and water?",
         "We use a combination of physical separation methods:\n\n### Step 1: Filtration (Separates the Sand)\n- Pour the mixture through filter paper into a beaker.\n- Sand cannot pass through the tiny pores of the filter paper and stays behind as **residue**.\n- The saltwater passes through into the beaker as the **filtrate**.\n\n### Step 2: Evaporation (Separates the Salt from Water)\n- Heat the saltwater filtrate in an evaporating dish.\n- Water boils and evaporates into the air as water vapor.\n- Solid white salt crystals are left behind in the dish!\n\nNow all three components (sand, salt, and water vapor) are completely separated.")
    ]
    for domain, topic, diff, qtype, q, a in c6_science:
        records.append(make_science_entry(6, domain, topic, diff, qtype, q, a, "NCERT Class 6 Science"))

    # -------------------------------------------------------------
    # CLASS 7 SCIENCE
    # -------------------------------------------------------------
    c7_science = [
        ("Physics", "Motion and Time", "medium", "step_by_step_calculation",
         "A train covers a distance of 180 km in 3 hours. Calculate its speed in km/h and m/s.",
         "**Step-by-step solution:**\n\nGiven: Distance ($d$) = 180 km, Time ($t$) = 3 hours\n\n### 1. Speed in km/h:\nFormula: $\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}}$\n$$\\text{Speed} = \\frac{180\\text{ km}}{3\\text{ h}} = \\mathbf{60\\text{ km/h}}$$\n\n### 2. Convert to meters per second (m/s):\nRule: To convert km/h to m/s, multiply by $\\frac{5}{18}$ (since $1\\text{ km} = 1000\\text{ m}$ and $1\\text{ h} = 3600\\text{ s}$):\n$$\\text{Speed} = 60 \\times \\frac{5}{18} = \\frac{300}{18} = \\frac{50}{3} \\approx \\mathbf{16.67\\text{ m/s}}$$\n\n**Answer: 60 km/h (or 16.67 m/s)**"),
         
        ("Chemistry", "Acids, Bases, and Salts", "medium", "conceptual_explanation",
         "What happens when turmeric stain on a white shirt is washed with soap? Explain the science.",
         "When you apply soap to a yellow turmeric stain, **the stain turns reddish-brown**!\n\n### The Science Explained:\n1. **Turmeric is a natural indicator**: It contains a yellow chemical called curcumin that changes color in the presence of basic substances.\n2. **Soap is basic (alkaline)**: Soaps and detergents are basic in nature.\n3. **Color change**: When turmeric meets a base, its chemical structure changes and turns **reddish-brown**.\n\n### What happens when you rinse with plenty of water or lemon juice (acid)?\n- Acid neutralizes the base, and turmeric turns back to its original **yellow** color!"),
         
        ("Biology", "Respiration in Organisms", "medium", "misconception_correction",
         "Do plants breathe? A friend said plants only do photosynthesis, not respiration. Is that true?",
         "Your friend is **incorrect**! Plants **definitely undergo respiration**, and they do it **all the time** (24 hours a day, day and night).\n\nLet's understand the difference:\n\n### 1. Photosynthesis (Cooking Food):\n- Plants use sunlight, water, and $CO_2$ to create glucose and release oxygen.\n- Happens **only during daytime** when sunlight is available.\n\n### 2. Respiration (Burning Food for Energy):\n- Just like humans and animals, plant cells break down glucose with oxygen to produce ATP energy to stay alive, grow, and repair cells.\n- Happens **continuously, 24 hours a day, both day and night**!\n\n### Why People Get Confused:\nDuring the day, photosynthesis happens much faster than respiration, so plants release a net excess of oxygen. But at night, photosynthesis stops, while respiration continues!")
    ]
    for domain, topic, diff, qtype, q, a in c7_science:
        records.append(make_science_entry(7, domain, topic, diff, qtype, q, a, "NCERT Class 7 Science"))

    # -------------------------------------------------------------
    # CLASS 8 SCIENCE
    # -------------------------------------------------------------
    c8_science = [
        ("Physics", "Force and Pressure", "challenging", "numerical_calculation",
         "A wooden box of mass 20 kg rests on a table. The area of its base in contact with the table is 0.5 m². Calculate the pressure it exerts on the table. (Take g = 9.8 m/s²)",
         "**Step-by-step solution:**\n\nGiven Data:\n- Mass ($m$) = 20 kg\n- Contact Area ($A$) = 0.5 m²\n- Acceleration due to gravity ($g$) = 9.8 m/s²\n\n### Step 1: Calculate the Downward Force (Weight)\n$$F = W = m \\times g$$\n$$F = 20\\text{ kg} \\times 9.8\\text{ m/s}² = 196\\text{ Newtons (N)}$$\n\n### Step 2: Use the Pressure Formula\n$$\\text{Pressure} = \\frac{\\text{Force}}{\\text{Area}}$$\n$$P = \\frac{196\\text{ N}}{0.5\\text{ m}²} = 196 \\times 2 = \\mathbf{392\\text{ Pascals (Pa)}}$$\n\n**Answer: 392 Pa (or 392 N/m²)**"),
         
        ("Physics", "Friction", "medium", "conceptual_explanation",
         "Why is friction called a 'necessary evil'? Give two examples where we want friction and two where we reduce it.",
         "Friction is called a **necessary evil** because in some situations it causes unwanted wear and tear, but in other situations we literally cannot survive without it!\n\n### 1. Two Situations Where Friction is Necessary (Good):\n- **Walking without slipping**: Without friction between your shoe sole and the ground, you would slip uncontrollably like walking on polished wet ice.\n- **Braking a bicycle or car**: Brakes press against the wheel to create friction, safely slowing the vehicle down.\n\n### 2. Two Situations Where Friction is an Evil (Bad):\n- **Machine parts wearing out**: Moving gears in engines heat up, grind against each other, and wear out over time.\n- **Wasted energy**: Cars waste fuel overcoming air drag and rolling resistance.\n\n### How We Reduce It When Unwanted:\nUsing **lubricants** (oil and grease) and **ball bearings** to replace sliding friction with much smaller rolling friction."),
         
        ("Biology", "Cell Structure and Functions", "medium", "compare_contrast",
         "What are the main differences between a plant cell and an animal cell that a Class 8 student should know?",
         "Both plant and animal cells are eukaryotic cells with a cell membrane, cytoplasm, mitochondria, and a nucleus, but they have key differences:\n\n### 1. Unique to Plant Cells:\n- **Cell Wall**: A rigid outer wall made of cellulose that provides strong shape and support (plants don't have bones!).\n- **Chloroplasts**: Green organelles containing chlorophyll where photosynthesis happens.\n- **Large Central Vacuole**: One huge water bubble in the center that keeps the plant cell firm (turgid).\n\n### 2. Unique to Animal Cells:\n- **Flexible Shape**: No cell wall, so animal cells are rounded and flexible.\n- **Small Vacuoles**: Multiple tiny vacuoles instead of one giant central vacuole.\n- **Centrosome/Centrioles**: Structures that help organize cell division.")
    ]
    for domain, topic, diff, qtype, q, a in c8_science:
        records.append(make_science_entry(8, domain, topic, diff, qtype, q, a, "NCERT Class 8 Science"))

    return records
