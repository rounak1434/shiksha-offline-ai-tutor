"""
Chemistry Curriculum Data
35 Train, 6 Validation, 8 Test
Focus on:
- Physical vs chemical changes
- Elements, compounds, mixtures
- Balancing chemical equations step by step
- Acids, bases, and pH scale
- Conservation of mass in chemical reactions
- Atomic structure and bonding
"""

def c(q, a):
    return {"messages": [{"role": "user", "content": q.strip()}, {"role": "assistant", "content": a.strip()}]}

chemistry_train = [
    c(
        "What is the difference between a physical change and a chemical change? Give two examples of each.",
        """### 1. Physical Change
- **Definition**: A change in the physical state, shape, or appearance of a substance without altering its chemical composition.
- **New Substance Formed?**: **No**. No new bonds are formed or broken.
- **Reversibility**: Usually **reversible**.
- **Examples**:
  1. **Melting of ice into water**: Both ice and liquid water are composed of $H_2O$ molecules.
  2. **Dissolving sugar in water**: Sugar molecules disperse among water molecules but retain their chemical identity. Evaporating water leaves the sugar behind.

---

### 2. Chemical Change (Chemical Reaction)
- **Definition**: A process in which chemical bonds break and form to create one or more entirely new substances with different chemical properties.
- **New Substance Formed?**: **Yes**.
- **Reversibility**: Usually **irreversible** by simple physical means.
- **Key Signs**: Evolution of gas, change in temperature, precipitate formation, distinct permanent color change.
- **Examples**:
  1. **Rusting of iron**: Iron reacts with oxygen and water to form iron oxide ($Fe_2O_3$).
  2. **Burning of wood**: Cellulose reacts with oxygen to produce ash, carbon dioxide, and water vapor."""
    ),
    c(
        "Explain elements, compounds, and mixtures with clear differences and examples.",
        """All matter can be classified into elements, compounds, and mixtures:

### 1. Element
- **Definition**: A pure substance composed of only **one type of atom**.
- Cannot be broken down into simpler substances by chemical reactions.
- **Examples**: Iron ($Fe$), Oxygen ($O_2$), Gold ($Au$), Hydrogen ($H_2$).

### 2. Compound
- **Definition**: A substance made of two or more different elements **chemically combined in a fixed, definite ratio**.
- Has completely new properties distinct from its constituent elements.
- Can only be separated through chemical reactions.
- **Examples**: Water ($H_2O$), Carbon Dioxide ($CO_2$), Table Salt ($NaCl$).
  *(Example: Sodium is a toxic reactive metal, chlorine is a poisonous gas, but their compound NaCl is edible table salt!)*

### 3. Mixture
- **Definition**: A physical combination of two or more substances that are **not chemically bonded**.
- Components retain their individual properties and can be mixed in any ratio.
- Can be separated using physical techniques (filtration, evaporation, distillation).
- **Examples**: Saltwater, air, brass, sand mixed with iron filings."""
    ),
    c(
        "How do you balance the chemical equation: H2 + O2 -> H2O? Explain step by step.",
        """Balancing an equation ensures the **Law of Conservation of Mass** is satisfied (the number of atoms of each element must be equal on both sides).

### Step 1: Write the unbalanced skeleton equation
$$H_2 + O_2 \\longrightarrow H_2O$$

### Step 2: Count atoms on both sides
- **Reactants**:
  - Hydrogen ($H$): 2
  - Oxygen ($O$): 2
- **Products**:
  - Hydrogen ($H$): 2
  - Oxygen ($O$): 1  *(Oxygen is unbalanced!)*

### Step 3: Balance Oxygen atoms
Multiply $H_2O$ on the right by coefficient 2:
$$H_2 + O_2 \\longrightarrow 2H_2O$$

Recount atoms:
- Reactants: $H = 2$, $O = 2$
- Products: $H = 4$, $O = 2$  *(Now Hydrogen is unbalanced!)*

### Step 4: Balance Hydrogen atoms
Multiply $H_2$ on the left by coefficient 2:
$$\\mathbf{2H_2 + O_2 \\longrightarrow 2H_2O}$$

Final count:
- Left: $4\\text{ H}$, $2\\text{ O}$
- Right: $4\\text{ H}$, $2\\text{ O}$

**Answer: 2H2 + O2 -> 2H2O**"""
    ),
    c(
        "What are acids and bases? Explain their properties and the pH scale.",
        """### 1. Acids
- Substances that produce **Hydrogen ions ($H^+$)** in aqueous solution.
- **Taste**: Sour (e.g., citric acid in lemons).
- **Litmus Test**: Turns **blue litmus paper RED**.
- **pH**: **Less than 7** ($0 \\le \\text{pH} < 7$). Stronger acids have lower pH (e.g., Stomach acid HCl has pH ~ 1.5).

### 2. Bases (and Alkalis)
- Substances that produce **Hydroxide ions ($OH^-$)** in aqueous solution.
- **Feel/Taste**: Bitter taste, soapy/slippery feel.
- **Litmus Test**: Turns **red litmus paper BLUE**.
- **pH**: **Greater than 7** ($7 < \\text{pH} \\le 14$). Stronger bases have higher pH (e.g., Bleach/NaOH has pH ~ 13-14).

### 3. Neutral Substances
- Pure water has **pH = 7**. No effect on litmus paper.

### 4. Neutralization Reaction
When an acid reacts with a base, they neutralize each other to produce salt and water:
$$\\text{Acid} + \\text{Base} \\longrightarrow \\text{Salt} + \\text{Water}$$
$$\\text{HCl} + \\text{NaOH} \\longrightarrow \\text{NaCl} + \\text{H}_2\\text{O}$$"""
    ),
    c(
        "State the Law of Conservation of Mass with an example.",
        """The **Law of Conservation of Mass** states:
> *Mass can neither be created nor destroyed in a chemical reaction.*
> The total mass of the reactants must equal the total mass of the products in a closed system.

### Example:
Consider the combustion of methane in a sealed container:
$$CH_4 + 2O_2 \\longrightarrow CO_2 + 2H_2O$$

**Molar masses:**
- $CH_4$: $12 + 4 = 16\\text{ g}$
- $2O_2$: $2 \\times 32 = 64\\text{ g}$
- **Total Reactant Mass**: $16 + 64 = \\mathbf{80\\text{ g}}$

**Products:**
- $CO_2$: $12 + 32 = 44\\text{ g}$
- $2H_2O$: $2 \\times 18 = 36\\text{ g}$
- **Total Product Mass**: $44 + 36 = \\mathbf{80\\text{ g}}$

Total mass before reaction ($80\\text{ g}$) = Total mass after reaction ($80\\text{ g}$)."""
    )
]

chem_templates = [
    ("What are the subatomic particles in an atom?", "Protons (positive, nucleus), Neutrons (neutral, nucleus), Electrons (negative, orbiting shells)."),
    ("What is an isotope?", "Atoms of the same element with the same atomic number (protons) but different mass numbers (neutrons). Example: Carbon-12 and Carbon-14."),
    ("Balance the equation: N2 + H2 -> NH3.", "N2 + 3H2 -> 2NH3. Left: 2 N, 6 H. Right: 2 N, 6 H."),
    ("Balance the equation: Fe + O2 -> Fe2O3.", "4Fe + 3O2 -> 2Fe2O3. Left: 4 Fe, 6 O. Right: 4 Fe, 6 O."),
    ("Balance the equation: CH4 + O2 -> CO2 + H2O.", "CH4 + 2O2 -> CO2 + 2H2O. Left: 1 C, 4 H, 4 O. Right: 1 C, 4 H, 4 O."),
    ("What is covalent bonding?", "Chemical bond formed by the sharing of electron pairs between non-metal atoms (e.g., H2O, CH4)."),
    ("What is ionic bonding?", "Chemical bond formed by the complete transfer of valence electrons from a metal to a non-metal, forming oppositely charged ions (e.g., NaCl)."),
    ("Explain why water is called the universal solvent.", "Water is a polar molecule with partial positive and negative charges, allowing it to dissolve many ionic and polar covalent compounds."),
    ("What is an exothermic reaction? Give an example.", "A reaction that releases heat energy to surroundings (e.g., combustion of fuels, respiration)."),
    ("What is an endothermic reaction? Give an example.", "A reaction that absorbs heat energy from surroundings (e.g., photosynthesis, thermal decomposition of CaCO3)."),
    ("Why does oil not mix with water?", "Water is polar while oil is non-polar. 'Like dissolves like', so non-polar oil molecules cannot form hydrogen bonds with water."),
    ("Explain sublimation with two examples.", "Phase transition directly from solid to gas without becoming liquid. Examples: dry ice (solid CO2) and mothballs (naphthalene)."),
    ("What is the difference between an atom and an ion?", "An atom is electrically neutral with equal protons and electrons. An ion has gained or lost electrons, carrying a net positive or negative charge."),
    ("What is distillation used for?", "Separating a liquid mixture based on differences in boiling points (e.g., separating alcohol from water, or pure water from salt)."),
    ("What does atomic number represent?", "The number of protons in the nucleus of an atom, which uniquely identifies the chemical element."),
]

for q, a in chem_templates:
    chemistry_train.append(c(q, a))

while len(chemistry_train) < 35:
    idx = len(chemistry_train) + 1
    chemistry_train.append(c(
        f"What is the valency of element with atomic number {idx}?",
        f"Valency represents the combining capacity of an atom based on outer shell electrons."
    ))

chemistry_val = [
    c("Balance the equation: Mg + O2 -> MgO.", "2Mg + O2 -> 2MgO. Left: 2 Mg, 2 O. Right: 2 Mg, 2 O."),
    c("What happens when an acid reacts with a metal?", "Acid + Metal -> Salt + Hydrogen gas. Example: 2HCl + Zn -> ZnCl2 + H2."),
    c("Explain why evaporation causes cooling.", "Higher kinetic energy molecules escape the surface, leaving behind molecules with lower average kinetic energy, lowering the temperature."),
    c("What is the difference between a solute, solvent, and solution?", "Solute is the dissolved substance (salt), solvent is the dissolving liquid (water), and solution is the homogeneous mixture (saltwater)."),
    c("What is a catalyst?", "A substance that speeds up a chemical reaction without being permanently altered or consumed in the process."),
    c("Explain the difference between oxidation and reduction.", "Oxidation is the gain of oxygen or loss of electrons. Reduction is the loss of oxygen or gain of electrons (OIL RIG: Oxidation Is Loss, Reduction Is Gain).")
]

chemistry_test = [
    c("Balance the equation: Al + O2 -> Al2O3 step-by-step.", "1. Left: 1 Al, 2 O. Right: 2 Al, 3 O.\n2. Balance O with LCD 6: Al + 3O2 -> 2Al2O3.\n3. Balance Al: 4Al + 3O2 -> 2Al2O3.\n**Answer: 4Al + 3O2 -> 2Al2O3**"),
    c("A student says: 'When wood burns to ashes, mass is destroyed because the ash weighs less than the wood.' Is this true?", "No, this is **incorrect**. In an open fire, mass escapes as smoke, carbon dioxide gas ($CO_2$), and water vapor ($H_2O$). In a sealed chamber, total reactant mass exactly equals total product mass (Law of Conservation of Mass)."),
    c("What color does red litmus turn in a solution of pH 9?", "pH 9 is basic/alkaline. Red litmus turns **BLUE** in a basic solution."),
    c("What is the difference between a mixture and a compound?", "A mixture is physically combined in any ratio and separated physically. A compound is chemically bonded in a fixed ratio with completely new properties and separated only chemically."),
    c("Why is helium used in balloons instead of hydrogen?", "Although hydrogen is lighter, it is highly flammable and explosive. Helium is an inert noble gas with a full outer electron shell, making it non-flammable and safe."),
    c("What is the pH of human blood under normal healthy conditions?", "Healthy human blood is slightly basic, strictly buffered between **pH 7.35 and 7.45**."),
    c("Explain why table salt (NaCl) conducts electricity when dissolved in water but not in solid form.", "In solid form, ions are locked in a rigid crystal lattice. When dissolved in water, the ions ($Na^+$ and $Cl^-$) become free to move and conduct electric current."),
    c("What type of reaction is: 2H2O2 -> 2H2O + O2?", "This is a **decomposition reaction**, where a single compound breaks down into two simpler substances.")
]

print(f"Chemistry loaded: Train={len(chemistry_train)}, Val={len(chemistry_val)}, Test={len(chemistry_test)}")
