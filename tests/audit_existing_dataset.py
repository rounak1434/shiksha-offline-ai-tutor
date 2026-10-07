import json
import re

files = {
    'train': r"C:\Rounak\RVSHACK\data\train.jsonl",
    'val': r"C:\Rounak\RVSHACK\data\validation.jsonl",
    'test': r"C:\Rounak\RVSHACK\data\test.jsonl"
}

data = {}
for split, path in files.items():
    with open(path, encoding='utf-8') as f:
        data[split] = [json.loads(line) for line in f]

total = sum(len(v) for v in data.values())
print(f"Total records: {total} (Train={len(data['train'])}, Val={len(data['val'])}, Test={len(data['test'])})")

# Let's inspect grade level suitability
# Standard NCERT / CBSE curriculum standards for Class 1-8:
# Class 1-2: Numbers, counting, basic addition/subtraction, shapes, animals, plants, our body, senses
# Class 3-5: Multiplication/division, fractions intro, measurement, time, states of matter, life cycles, food chains, simple machines, water cycle
# Class 6: Motion & measurement of distances, light/shadows/reflection, electricity & circuits, sorting materials, plants & components of food, integers, fractions/decimals, ratio/proportion
# Class 7: Heat & temperature, acids/bases/salts, physical & chemical changes, respiration in organisms, transportation in animals/plants, reproduction in plants, motion & time, electric current effects, light, algebraic expressions, linear equations
# Class 8: Force and pressure, friction, sound, chemical effects of electric current, light, cells - structure & functions, reproduction in animals, microorganisms, conservation, linear equations in one variable, algebraic identities, mensuration, exponents

too_advanced_patterns = [
    (r"big o|asymptotic", "Big-O complexity (University CS)"),
    (r"saltatory|myelin sheath", "Neurobiology / Myelin sheath (Class 11/12 Biology)"),
    (r"hydraulic lift|pascal's principle", "Pascal's principle hydraulics (Class 11 Physics)"),
    (r"quadratic equation|x\^2\s*-\s*\d+x", "Quadratic equations by factoring (Class 9-10 Math)"),
    (r"faraday|electromotive force", "Electromagnetic induction / Faraday (Class 10/12 Physics)"),
    (r"terminal velocity", "Terminal velocity viscous drag (Class 11 Physics)"),
    (r"molar mass|combustion of methane", "Stoichiometry & molar masses (Class 9-10 Chemistry)"),
    (r"covalent bonding|ionic bonding", "Chemical bonding mechanisms (Class 9-10 Chemistry)"),
    (r"ac and dc|alternating current", "AC vs DC waveforms (Class 10 Physics)"),
    (r"coulomb", "Coulombs law / quantitative charge (Class 10/12 Physics)")
]

flagged = []
for split, items in data.items():
    for idx, item in enumerate(items):
        q = item['messages'][0]['content']
        a = item['messages'][1]['content']
        text = q + " " + a
        for pat, desc in too_advanced_patterns:
            if re.search(pat, text, re.IGNORECASE):
                flagged.append((split, idx, desc, q))
                break

print(f"\nAdvanced Topics Flagged: {len(flagged)}")
for f in flagged:
    print(f"- [{f[0]}:{f[1]}] {f[2]} -> '{f[3]}'")
