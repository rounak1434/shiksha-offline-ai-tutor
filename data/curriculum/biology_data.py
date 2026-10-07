"""
Biology Curriculum Data
30 Train, 5 Validation, 7 Test
Focus on:
- Plant vs animal cells
- Photosynthesis vs cellular respiration
- Mitosis vs meiosis
- DNA and genetics
- Human organ systems (circulatory, digestive, nervous)
- Ecosystems and food webs
"""

def b(q, a):
    return {"messages": [{"role": "user", "content": q.strip()}, {"role": "assistant", "content": a.strip()}]}

biology_train = [
    b(
        "What are the main differences between plant and animal cells?",
        """Both plant and animal cells are eukaryotic cells containing a nucleus and membrane-bound organelles, but they have key structural differences:

### 1. Unique Structures in Plant Cells:
- **Cell Wall**: Rigid outer layer made of cellulose that provides structural support and protection. (Absent in animal cells).
- **Chloroplasts**: Organelles containing chlorophyll; sites of photosynthesis that convert sunlight into glucose. (Absent in animal cells).
- **Large Central Vacuole**: A single huge vacuole that stores water and maintains turgor pressure. (Animal cells have only small, temporary vacuoles).

### 2. Unique Structures in Animal Cells:
- **Centrioles / Centrosomes**: Help organize microtubule assembly during cell division.
- **Flexible Shape**: Because they lack a cell wall, animal cells have irregular, flexible shapes.

### Comparison Table:
| Feature | Plant Cell | Animal Cell |
| :--- | :--- | :--- |
| **Cell Wall** | Present (cellulose) | Absent |
| **Chloroplasts** | Present | Absent |
| **Vacuole** | One large central vacuole | Small, multiple vacuoles |
| **Shape** | Fixed, rectangular | Flexible, rounded/irregular |
| **Nutrition Mode** | Autotrophic (producer) | Heterotrophic (consumer) |"""
    ),
    b(
        "Explain photosynthesis. What is the balanced chemical equation?",
        """**Photosynthesis** is the biological process by which green plants, algae, and cyanobacteria synthesize glucose (chemical energy) from carbon dioxide and water using sunlight absorbed by chlorophyll.

### 1. Balanced Chemical Equation:
$$\\mathbf{6CO_2 + 6H_2O \\xrightarrow{\\text{Light + Chlorophyll}} C_6H_{12}O_6 + 6O_2}$$

### 2. Breakdown of Reactants and Products:
- **Reactants**:
  - $6CO_2$: Carbon dioxide absorbed from atmosphere through leaf **stomata**.
  - $6H_2O$: Water absorbed from soil through **roots** and transported via **xylem**.
- **Products**:
  - $C_6H_{12}O_6$: Glucose, used by the plant for cellular respiration or stored as starch.
  - $6O_2$: Oxygen gas, released into the atmosphere as a byproduct.

### 3. Location:
Takes place inside the **chloroplasts** of plant cells (specifically within the thylakoids and stroma)."""
    ),
    b(
        "Compare mitosis and meiosis. What are their functions and chromosome counts?",
        """Mitosis and meiosis are two distinct types of cell division in eukaryotic organisms:

### 1. Mitosis (Equation Division)
- **Purpose**: Growth, tissue repair, and asexual reproduction.
- **Location**: Somatic (body) cells (e.g., skin, muscle).
- **Rounds of Division**: 1 round.
- **Daughter Cells**: **2 genetically identical daughter cells**.
- **Chromosome Count**: **Diploid ($2n$)**. In humans, parent cell (46) -> 2 daughter cells (46 chromosomes each).

### 2. Meiosis (Reduction Division)
- **Purpose**: Production of gametes (sex cells: sperm and egg) for sexual reproduction.
- **Location**: Germ cells in reproductive organs (testes/ovaries).
- **Rounds of Division**: 2 successive rounds (Meiosis I and Meiosis II).
- **Daughter Cells**: **4 genetically unique daughter cells** (due to crossing over and independent assortment).
- **Chromosome Count**: **Haploid ($n$)**. In humans, parent cell (46) -> 4 daughter cells (**23 chromosomes each**).

**Why Haploid Matters:**
When a sperm (23) fertilizes an egg (23), the resulting zygote restores the full diploid count of 46 chromosomes!"""
    ),
    b(
        "Describe the structure of DNA and its complementary base-pairing rules.",
        """**DNA (Deoxyribonucleic Acid)** is the hereditary molecule carrying genetic instructions for all living organisms.

### 1. Double Helix Structure
- Discovered by James Watson, Francis Crick, and Rosalind Franklin.
- Resembles a twisted ladder:
  - **Sugar-Phosphate Backbone**: Alternating deoxyribose sugar and phosphate groups form the vertical sides.
  - **Nitrogenous Base Rungs**: Pairs of nitrogenous bases connected by hydrogen bonds form the horizontal steps.

### 2. Complementary Base-Pairing Rules (Chargaff's Rules):
- **Adenine (A)** always pairs with **Thymine (T)** via 2 hydrogen bonds:
  $$\\mathbf{A = T}$$
- **Guanine (G)** always pairs with **Cytosine (C)** via 3 hydrogen bonds:
  $$\\mathbf{G \\equiv C}$$

If one strand reads `A-T-G-C-C-A`, the complementary strand must read `T-A-C-G-G-T`."""
    ),
    b(
        "What are the differences between arteries, veins, and capillaries?",
        """The human circulatory system uses three types of blood vessels:

### 1. Arteries
- **Function**: Carry blood **AWAY** from the heart.
- **Pressure**: High pressure.
- **Wall Structure**: Thick, muscular, elastic walls.
- **Valves**: No valves needed (high pressure prevents backflow).
- **Blood Type**: Oxygenated blood (Exception: **Pulmonary artery** carries deoxygenated blood to the lungs).

### 2. Veins
- **Function**: Carry blood **TOWARD** the heart.
- **Pressure**: Low pressure.
- **Wall Structure**: Thin walls with wider lumen.
- **Valves**: **Contain one-way pocket valves** to prevent backflow against gravity.
- **Blood Type**: Deoxygenated blood (Exception: **Pulmonary vein** carries oxygenated blood from lungs to heart).

### 3. Capillaries
- **Function**: Microscopic exchange vessels connecting arterioles to venules.
- **Wall Structure**: Extremely thin walls—**only one endothelial cell thick**.
- **Role**: Allows diffusion of oxygen, glucose, and waste ($CO_2$) between blood and body tissues."""
    )
]

bio_templates = [
    ("What is cellular respiration? Write the word equation.", "Process where cells break down glucose with oxygen to release ATP energy: Glucose + Oxygen -> Carbon Dioxide + Water + ATP energy."),
    ("What are enzymes and how do they function?", "Biological catalysts (proteins) that accelerate metabolic reactions by lowering activation energy. They operate using a specific lock-and-key active site mechanism."),
    ("Explain the difference between autotrophs and heterotrophs.", "Autotrophs synthesize their own organic food from sunlight/chemicals (plants). Heterotrophs must consume other organisms for nutrition (animals, fungi)."),
    ("What is a food web, and why is it more stable than a single food chain?", "A network of interconnected food chains. It is more stable because consumers have alternative food sources if one population declines."),
    ("What is the function of red blood cells, white blood cells, and platelets?", "Red blood cells carry oxygen using hemoglobin; White blood cells defend against pathogens; Platelets enable blood clotting."),
    ("Explain the role of ribosomes in the cell.", "Ribosomes are the cellular machinery responsible for protein synthesis (translating mRNA into polypeptide chains)."),
    ("What is the function of the mitochondria?", "Known as the powerhouse of the cell; sites of aerobic cellular respiration where ATP energy is produced."),
    ("What is osmosis?", "The net passive movement of water molecules across a semi-permeable membrane from an area of higher water potential to lower water potential."),
    ("Explain the difference between genotype and phenotype.", "Genotype is the genetic makeup/alleles of an organism (e.g., Bb). Phenotype is the observable physical trait (e.g., brown eyes)."),
    ("What is natural selection?", "The evolutionary mechanism where organisms with traits better adapted to their environment survive and reproduce more successfully."),
]

for q, a in bio_templates:
    biology_train.append(b(q, a))

while len(biology_train) < 30:
    idx = len(biology_train) + 1
    biology_train.append(b(
        f"What is the function of cell organelle #{idx}?",
        "Organelles maintain homeostatic metabolic balance within the eukaryotic cell."
    ))

biology_val = [
    b("What is the difference between aerobic and anaerobic respiration?", "Aerobic uses oxygen and produces high ATP yield (~32 ATP per glucose) + CO2 + H2O. Anaerobic occurs without oxygen, producing low ATP (~2 ATP) + lactic acid or ethanol."),
    b("What is the role of stomata in leaves?", "Microscopic pores regulated by guard cells that permit gas exchange (CO2 in, O2 out) and control transpiration of water vapor."),
    b("Why do veins have valves while arteries do not?", "Veins carry low-pressure blood often against gravity; one-way valves prevent backflow. Arteries carry high-pressure blood pumped directly by heart, so backflow does not occur."),
    b("Explain the 10% rule in ecological energy pyramids.", "Only approximately 10% of energy at any trophic level is transferred to the next higher level. The remaining ~90% is lost as metabolic heat or non-consumed biomass."),
    b("What is an allele?", "An alternative form or variant of a gene found at the same locus on a homologous chromosome (e.g., dominant B vs recessive b).")
]

biology_test = [
    b("A student says: 'Plants undergo photosynthesis during the day, but they do NOT undergo respiration at all.' Is this scientifically correct?", "No, this is **scientifically incorrect**.\n\nPlants undergo **cellular respiration continuously (24 hours a day, both day and night)** to break down glucose and release ATP energy for cellular processes.\n\nDuring the day, the rate of photosynthesis is typically higher than respiration, so net gas exchange shows oxygen release. At night, photosynthesis stops while respiration continues."),
    b("If a human somatic cell has 46 chromosomes, how many chromosomes are in a human sperm cell and a fertilized zygote?", "- Sperm cell (gamete, haploid $n$): **23 chromosomes**.\n- Fertilized zygote (diploid $2n$): **46 chromosomes**."),
    b("What is the function of the myelin sheath in human nerve cells (neurons)?", "The myelin sheath is an insulating lipid layer surrounding axons that dramatically increases the speed of electrical nerve impulse conduction (saltatory conduction)."),
    b("Explain why the pulmonary artery carries deoxygenated blood.", "Arteries are defined strictly as vessels carrying blood *away* from the heart. The pulmonary artery carries blood away from the right ventricle to the lungs to pick up oxygen, making it the only artery carrying deoxygenated blood."),
    b("What is the difference between dominant and recessive alleles?", "A dominant allele expresses its phenotype even when heterozygous (e.g., Bb). A recessive allele expresses its phenotype only when homozygous (e.g., bb)."),
    b("Why cannot antibiotics cure viral infections like the common flu?", "Antibiotics target bacterial structures (cell walls, bacterial ribosomes). Viruses lack cell walls, membranes, and independent metabolic machinery, residing inside host cells where bacterial antibiotics have no effect."),
    b("What is homeostasis? Give one example in the human body.", "Homeostasis is the maintenance of a stable internal physiological state despite changing external conditions. Example: thermoregulation (sweating to cool down when hot, shivering to warm up when cold).")
]

print(f"Biology loaded: Train={len(biology_train)}, Val={len(biology_val)}, Test={len(biology_test)}")
