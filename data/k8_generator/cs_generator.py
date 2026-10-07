"""
cs_generator.py
Generates curriculum-aligned Computer Science records for Class 1 to Class 8.
"""

def make_cs_entry(grade, topic, difficulty, q_type, q_text, ans_text, source="Curriculum-aligned K-8 CS"):
    user_prompt = f"Student grade: Class {grade}\nSubject: Computer Science\nQuestion: {q_text.strip()}"
    return {
        "metadata": {
            "grade": grade,
            "subject": "Computer Science",
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

def generate_cs_records():
    records = []
    
    # Class 1-2 CS
    records.append(make_cs_entry(
        1, "Computer Basics", "foundational", "conceptual_explanation",
        "What is a computer? Can you explain it simply?",
        "A computer is a smart electronic machine that helps us do many tasks quickly and easily!\n\nJust like a microwave heats food and a bicycle helps you travel faster, a computer helps you:\n- Draw colorful pictures\n- Play learning games\n- Listen to music\n- Write stories and count numbers\n\nIt works very fast and does not get tired like humans do!"
    ))
    records.append(make_cs_entry(
        2, "Computer Parts", "easy", "conceptual_explanation",
        "What are the four main parts of a desktop computer?",
        "A desktop computer has 4 main parts that work together like a team:\n\n1. **Monitor (Screen) 🖥️**: Looks like a TV. Shows you what the computer is doing.\n2. **CPU Box (Central Processing Unit) 🧠**: The 'brain' of the computer that does all the thinking and calculations.\n3. **Keyboard ⌨️**: Has letters and numbers so you can type messages and numbers into the computer.\n4. **Mouse 🖱️**: A small pointing device that lets you click, drag, and open files on the screen."
    ))

    # Class 3-4 CS
    records.append(make_cs_entry(
        3, "Input and Output Devices", "easy", "conceptual_explanation",
        "What is the difference between an input device and an output device? Give examples.",
        "Think of a computer like your own brain:\n\n### 1. Input Devices (Information GOING IN)\n- These tools let **you send information or instructions into the computer**.\n- **Examples**:\n  - **Keyboard**: Types words into the computer.\n  - **Mouse**: Clicks and selects items.\n  - **Microphone**: Sends your voice into the computer.\n\n### 2. Output Devices (Information COMING OUT)\n- These tools let **the computer show or give results back to you**.\n- **Examples**:\n  - **Monitor (Screen)**: Shows pictures and text.\n  - **Printer**: Prints papers for you to hold.\n  - **Speakers / Headphones**: Plays sound and music."
    ))
    records.append(make_cs_entry(
        4, "Hardware and Software", "medium", "compare_contrast",
        "What is the difference between hardware and software? Give a simple analogy.",
        "Here is the easiest way to understand the difference:\n\n### 1. Hardware (The Physical Body)\n- Any physical part of the computer that you can **touch, hold, and see**.\n- **Examples**: The keyboard, screen, mouse, wires, and internal hard drive.\n\n### 2. Software (The Mind and Programs)\n- The set of digital instructions and programs that tell the hardware what to do.\n- You **cannot touch software with your physical hands**.\n- **Examples**: Microsoft Word, games like Minecraft, web browsers like Chrome, and the Windows Operating System.\n\n### The Analogy:\nThink of a storybook:\n- The paper pages, ink, and binding are the **Hardware** (you can touch them).\n- The story and words written inside are the **Software** (ideas and instructions)!"
    ))

    # Class 5-6 CS
    records.append(make_cs_entry(
        5, "Storage Devices", "easy", "conceptual_explanation",
        "What is a USB flash drive, and why do we use it?",
        "A **USB flash drive** (also called a thumb drive or pen drive) is a small, portable storage device.\n\n### Why we use it:\n1. **Portable**: It fits right inside your pocket or backpack.\n2. **Saves Data Permanently**: It does not lose files when you unplug it from the computer.\n3. **Easy Transfer**: You can save a school presentation from your home computer onto the USB drive, and then plug it into your classroom computer to present it!"
    ))
    records.append(make_cs_entry(
        6, "Computer Memory", "medium", "misconception_correction",
        "What is the difference between RAM and storage (Hard Drive/SSD)? Does adding more storage make games run faster?",
        "RAM and Storage are both types of computer memory, but they do completely different jobs!\n\n### 1. RAM (Random Access Memory) - The Active Desk\n- **Temporary, super-fast working memory**.\n- Holds only the programs and browser tabs you are **actively using right this second**.\n- When you turn off the computer, everything in RAM is erased (it is **volatile**).\n\n### 2. Storage (SSD or Hard Drive) - The Filing Cabinet\n- **Permanent, slower storage**.\n- Holds all your saved files, photos, installed games, and operating system safely, even when power is off.\n\n### Does adding more storage make games run faster?\n**No.** If your game is lagging, it is usually because you need more **RAM** or a faster graphics card, not more storage space. Buying a bigger filing cabinet does not help you write essays faster at your desk!"
    ))
    records.append(make_cs_entry(
        6, "Algorithms", "medium", "step_by_step_calculation",
        "What is an algorithm? Write an algorithm for making a cup of instant hot chocolate.",
        "An **algorithm** is a clear, step-by-step set of instructions to solve a problem or complete a task.\n\n### Algorithm for Making Hot Chocolate:\n- **Step 1**: Start.\n- **Step 2**: Take a clean ceramic mug from the cupboard.\n- **Step 3**: Add 2 teaspoons of cocoa powder and 1 teaspoon of sugar into the mug.\n- **Step 4**: Heat 1 cup of milk in a pan until warm.\n- **Step 5**: Pour the warm milk carefully into the mug.\n- **Step 6**: Stir thoroughly with a spoon for 30 seconds until the powder dissolves.\n- **Step 7**: Serve and enjoy your drink.\n- **Step 8**: Stop.\n\nComputers follow step-by-step algorithms exactly like this!"
    ))

    # Class 7-8 CS
    records.append(make_cs_entry(
        7, "Internet Safety", "easy", "conceptual_explanation",
        "What are three important safety rules every student should follow online?",
        "Staying safe on the Internet is just like staying safe when walking in a busy city:\n\n1. **Keep Private Information Secret**: Never share your full real name, home address, phone number, school name, or passwords online.\n2. **Think Before You Click**: Do not click on suspicious links, pop-ups claiming you won a prize, or strange email attachments.\n3. **Tell a Trusted Adult**: If anyone online makes you feel uncomfortable, asks to meet in person, or asks for photos, tell a parent or teacher immediately!"
    ))
    records.append(make_cs_entry(
        8, "Binary Numbers", "medium", "step_by_step_calculation",
        "Convert the decimal number 13 to binary step-by-step.",
        "**Step-by-step conversion using the Divide-by-2 method:**\n\nDivide 13 by 2 repeatedly and record the remainders:\n\n1. $13 \\div 2 = 6$ with remainder **1**\n2. $6 \\div 2 = 3$ with remainder **0**\n3. $3 \\div 2 = 1$ with remainder **1**\n4. $1 \\div 2 = 0$ with remainder **1**\n\nNow write the remainders from **bottom to top (MSB to LSB)**:\n$$\\mathbf{1101_2}$$\n\n**Verification (Binary to Decimal):**\n$$1 \\times 2^3 + 1 \\times 2^2 + 0 \\times 2^1 + 1 \\times 2^0$$\n$$= 8 + 4 + 0 + 1 = 13$$\nVerified! ✅\n\n**Answer: 13 in decimal = 1101 in binary**"
    ))
    records.append(make_cs_entry(
        8, "Programming Logic", "medium", "code_and_concept",
        "What is an infinite loop in Python, and how do I prevent it?",
        "An **infinite loop** is a loop that never stops running because its condition **never becomes False**.\n\n### Example of an Infinite Loop (A Common Mistake):\n```python\ncount = 1\nwhile count <= 5:\n    print(count)\n    # We forgot to increase count!\n```\n`count` stays 1 forever, so the computer prints 1 endlessly until it freezes!\n\n### How to Fix It:\nAlways update the loop variable inside the loop body:\n```python\ncount = 1\nwhile count <= 5:\n    print(count)\n    count = count + 1  # count increases: 1, 2, 3, 4, 5, then stops at 6!\n```"
    ))

    return records
