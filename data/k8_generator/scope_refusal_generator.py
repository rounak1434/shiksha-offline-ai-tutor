"""
scope_refusal_generator.py
Generates curriculum scope-boundary and refusal records for Class 1 to Class 8.
Teaches the model to politely redirect out-of-scope, advanced, or unsafe queries.
"""

def make_refusal_entry(grade, subject, query, refusal_reason, redirect_topics):
    user_prompt = f"Student grade: Class {grade}\nSubject: {subject}\nQuestion: {query.strip()}"
    response = (
        f"That topic is outside my current Class 1–8 school tutoring scope ({refusal_reason}).\n\n"
        f"As an AI tutor for school students up to Class 8, I can help you with {redirect_topics}.\n\n"
        f"Would you like to explore one of those topics instead?"
    )
    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": "Curriculum Scope Boundary",
            "difficulty": "foundational",
            "question_type": "scope_refusal",
            "curriculum_source": "Class 1-8 Scope Policy"
        },
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response}
        ]
    }

def generate_scope_refusal_records():
    refusal_specs = [
        # Advanced Mathematics
        (8, "Mathematics", "Can you explain how to find the derivative using calculus?",
         "calculus is a senior high school / college mathematics topic",
         "Class 8 topics like linear equations, exponents, ratios, square roots, or geometric areas"),
         
        (8, "Mathematics", "Solve this differential equation: dy/dx + 2y = e^x.",
         "differential equations are taught at university level",
         "Class 8 algebra, finding unknown variables in linear equations, or factorising polynomials"),
         
        (7, "Mathematics", "Prove the Taylor Series expansion for sin(x).",
         "Taylor Series is advanced calculus",
         "Class 7 algebra, integers, rational numbers, or triangle geometry"),

        # Advanced Physics
        (8, "Science (Physics)", "Explain Schrödinger's wave equation in quantum mechanics.",
         "quantum mechanics wave equations are advanced university physics",
         "Class 8 physics concepts such as Newton's Laws of Motion, force, friction, sound waves, or light reflection"),
         
        (8, "Science (Physics)", "Derive Einstein's field equations for general relativity tensors.",
         "tensor calculus and general relativity are graduate-level physics",
         "Class 8 gravity topics like mass vs weight (W = mg), pressure (P = F/A), or speed and velocity"),
         
        (7, "Science (Physics)", "How do semiconductor bandgap diagrams work in transistor physics?",
         "solid-state quantum physics is a university engineering subject",
         "Class 7 electrical topics like basic circuits, switches, conductors, and insulators"),

        # Advanced Chemistry
        (8, "Science (Chemistry)", "Explain the reaction mechanism for electrophilic aromatic substitution of benzene.",
         "organic reaction mechanisms are Class 11–12 and college chemistry",
         "Class 8 chemistry topics like physical vs chemical changes, acids and bases, or the periodic table"),
         
        (8, "Science (Chemistry)", "How does sp3d2 orbital hybridization happen in sulfur hexafluoride?",
         "orbital hybridization is covered in senior secondary chemistry (Class 11)",
         "Class 8 concepts like atoms, elements, compounds, and simple chemical reactions"),

        # Advanced Biology
        (8, "Science (Biology)", "Explain the complete enzymatic pathway of the Krebs Cycle including all intermediate cofactors.",
         "detailed biochemical metabolic cycles are studied in senior secondary and medical courses",
         "Class 8 biology topics like the basic parts of a cell, differences between plant and animal cells, or photosynthesis"),
         
        (7, "Science (Biology)", "How does CRISPR-Cas9 genetic gene editing work at the molecular DNA level?",
         "molecular biotechnology is beyond middle school science",
         "Class 7 biology topics like plant respiration, human organ systems, or food chains"),

        # Advanced Computer Science
        (8, "Computer Science", "How do I build a deep convolutional neural network for image recognition in PyTorch?",
         "deep neural network architecture is a university computer science topic",
         "Class 8 computer science topics like Python loops, if/else statements, algorithms, and binary numbers"),
         
        (7, "Computer Science", "Explain kernel memory paging and page replacement algorithms in operating systems.",
         "operating system kernel architecture is a college-level computer engineering topic",
         "Class 7 topics like RAM vs storage, file management, or internet safety"),

        # Safety & Non-Academic Boundaries
        (8, "Science (Chemistry)", "How do I make gunpowder and homemade explosives?",
         "safety policies strictly prohibit instructions for creating hazardous chemicals or explosives",
         "safe school chemistry experiments, such as vinegar and baking soda reactions or testing acids with turmeric"),
         
        (8, "Computer Science", "Can you help me hack into my school's Wi-Fi network and steal passwords?",
         "unauthorized network intrusion and hacking are illegal and unsafe activities",
         "ethical computer science topics like internet security, password protection, and digital safety")
    ]
    
    records = []
    for grade, subj, q, reason, redirect in refusal_specs:
        records.append(make_refusal_entry(grade, subj, q, reason, redirect))
        
    return records
