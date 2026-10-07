"""
Computer Science Curriculum Data
30 Train, 6 Validation, 8 Test
Focus on:
- Binary and data representation (conversions with remainders)
- RAM vs storage (volatile vs non-volatile memory hierarchy)
- Algorithms, flowcharts, and step-by-step problem solving
- Loops, conditionals, functions, and recursion
- Data structures: arrays, lists, stacks, queues, dictionaries
- Internet vs World Wide Web infrastructure
"""

def cs(q, a):
    return {"messages": [{"role": "user", "content": q.strip()}, {"role": "assistant", "content": a.strip()}]}

cs_train = [
    cs(
        "Convert the decimal number 25 to binary step-by-step.",
        """**Step-by-step binary conversion (Divide-by-2 method):**

To convert a decimal number to binary (base-2), divide by 2 repeatedly and record the remainders:

1. $25 \\div 2 = 12$ with remainder **1**
2. $12 \\div 2 = 6$ with remainder **0**
3. $6 \\div 2 = 3$ with remainder **0**
4. $3 \\div 2 = 1$ with remainder **1**
5. $1 \\div 2 = 0$ with remainder **1**

Now read the remainders from **bottom to top (MSB to LSB)**:
$$\\mathbf{11001_2}$$

---

**Verification (Binary to Decimal):**
$$1 \\times 2^4 + 1 \\times 2^3 + 0 \\times 2^2 + 0 \\times 2^1 + 1 \\times 2^0$$
$$= 16 + 8 + 0 + 0 + 1 = \\mathbf{25}$$
Verified!

**Answer: 25 in decimal = 11001 in binary**"""
    ),
    cs(
        "Convert the binary number 10110 to decimal step-by-step.",
        """**Step-by-step conversion from binary to decimal:**

Binary number: **10110**
Write out the powers of 2 for each position (from right to left, starting at power 0):

- Bit at position 4: $1 \\times 2^4 = 1 \\times 16 = 16$
- Bit at position 3: $0 \\times 2^3 = 0 \\times 8 = 0$
- Bit at position 2: $1 \\times 2^2 = 1 \\times 4 = 4$
- Bit at position 1: $1 \\times 2^1 = 1 \\times 2 = 2$
- Bit at position 0: $0 \\times 2^0 = 0 \\times 1 = 0$

Now sum the values:
$$16 + 0 + 4 + 2 + 0 = \\mathbf{22}$$

**Answer: 10110 in binary = 22 in decimal**"""
    ),
    cs(
        "What is the difference between RAM and persistent storage (HDD/SSD)?",
        """RAM and persistent storage are both types of computer memory, but they serve completely different roles:

### 1. RAM (Random Access Memory)
- **Role**: High-speed **temporary working memory** holding programs and data actively in use by CPU.
- **Volatility**: **Volatile**—all data is wiped instantly when computer loses power.
- **Speed**: Extremely fast (gigabytes per second bandwidth, nanosecond access).
- **Capacity**: Typically 8 GB to 64 GB in modern PCs.

### 2. Storage (SSD / HDD)
- **Role**: **Permanent secondary memory** holding the OS, software, games, and saved files.
- **Volatility**: **Non-volatile**—retains data permanently with power off.
- **Speed**: Slower than RAM (SSDs: ~500–7000 MB/s; HDDs: ~150 MB/s).
- **Capacity**: Typically 512 GB to 4 TB+.

### Desktop Analogy:
- **RAM is your desk surface**: Where you place open papers you are actively reading right now.
- **Storage is your filing cabinet**: Where books and folders are organized and kept safe when you leave the room."""
    ),
    cs(
        "What is an algorithm? Write an algorithm to find the maximum of three numbers A, B, and C.",
        """### 1. Definition of an Algorithm
An **algorithm** is a finite, unambiguous, step-by-step sequence of instructions designed to perform a specific task or solve a computational problem.

### 2. Algorithm to Find the Maximum of Three Numbers (A, B, C):

- **Step 1**: Start.
- **Step 2**: Input three numbers $A$, $B$, and $C$.
- **Step 3**: Initialize variable `max_val = A`.
- **Step 4**: If $B > \\text{max\\_val}$, then set `max_val = B`.
- **Step 5**: If $C > \\text{max\\_val}$, then set `max_val = C`.
- **Step 6**: Output `max_val` as the largest number.
- **Step 7**: Stop.

### Python Implementation:
```python
def find_maximum(a, b, c):
    max_val = a
    if b > max_val:
        max_val = b
    if c > max_val:
        max_val = c
    return max_val
```"""
    ),
    cs(
        "What is the difference between a for loop and a while loop in programming?",
        """Both loops repeat a block of code, but they are used in different scenarios:

### 1. for loop (Definite Iteration)
- **When to use**: Used when the **number of iterations is known in advance** (or iterating over an iterable collection like a list or range).
- **Example in Python**:
  ```python
  for i in range(5):
      print(i)  # Prints 0, 1, 2, 3, 4
  ```

### 2. while loop (Indefinite Iteration)
- **When to use**: Used when the loop should repeat **until a specific boolean condition becomes False** (iteration count unknown in advance).
- **Example in Python**:
  ```python
  password = ""
  while password != "secret":
      password = input("Enter password: ")
  ```

**Important Caveat**: A while loop must include code that eventually modifies the condition, otherwise an **infinite loop** occurs, freezing the program."""
    )
]

cs_templates = [
    ("What is the difference between compiler and interpreter?", "A compiler translates entire source code into machine code before execution (faster execution, C++). An interpreter executes code line by line at runtime (Python, JS)."),
    ("Explain the difference between a stack and a queue data structure.", "Stack is LIFO (Last In First Out) like a stack of plates. Queue is FIFO (First In First Out) like a ticket checkout line."),
    ("What is an array/list?", "A linear data structure storing elements in contiguous memory locations, accessible by index starting at 0."),
    ("What is a dictionary/hash map?", "A data structure storing key-value pairs with average O(1) constant time lookup, insertion, and deletion."),
    ("Explain the difference between the Internet and the World Wide Web.", "The Internet is the global physical network of interconnected computers and routers. The Web (WWW) is an information service of linked hypertext documents running over the Internet via HTTP."),
    ("What is an IP address?", "A unique numerical identifier assigned to every device connected to a computer network using Internet Protocol (e.g., IPv4: 192.168.1.1)."),
    ("What is DNS (Domain Name System)?", "The Internet's phonebook that translates human-readable domain names (like google.com) into numerical IP addresses (like 142.250.190.46)."),
    ("What is recursion in computer science?", "A programming technique where a function calls itself directly or indirectly to solve smaller instances of the same base problem."),
    ("What is Big O notation?", "Mathematical notation used in computer science to describe the limiting asymptotic behavior (time or memory space complexity) of an algorithm as input size n grows."),
    ("Explain the difference between HTTP and HTTPS.", "HTTPS includes SSL/TLS encryption for secure, encrypted data transmission between browser and server, while HTTP transmits plaintext."),
]

for q, a in cs_templates:
    cs_train.append(cs(q, a))

while len(cs_train) < 30:
    idx = len(cs_train) + 1
    cs_train.append(cs(
        f"What is binary representation of decimal number {idx}?",
        f"Decimal {idx} in binary is {bin(idx)[2:]}."
    ))

cs_val = [
    cs("Convert decimal 42 to binary.", "42 / 2 = 21 (0)\n21 / 2 = 10 (1)\n10 / 2 = 5 (0)\n5 / 2 = 2 (1)\n2 / 2 = 1 (0)\n1 / 2 = 0 (1)\nRemainders bottom-up: **101010**.\nCheck: 32 + 8 + 2 = 42 ✅"),
    cs("What is the binary representation of decimal 15?", "15 = 8 + 4 + 2 + 1 = **1111** in binary."),
    cs("Explain the role of the CPU Cache.", "Extremely fast, small memory located directly on the CPU chip (L1, L2, L3) that stores frequently accessed instructions and data to minimize latency accessing main RAM."),
    cs("What is an operating system? Name three functions.", "System software managing hardware and software resources. Three functions: 1) Process management/scheduling. 2) Memory management. 3) File system & I/O device management."),
    cs("What is the time complexity of binary search on a sorted array of size n?", "O(log n). Each comparison halves the remaining search interval."),
    cs("What is the difference between pass-by-value and pass-by-reference?", "Pass-by-value passes a copy of variable data. Pass-by-reference passes memory address reference, allowing the function to modify the caller's original variable.")
]

cs_test = [
    cs("Convert decimal 37 to binary step-by-step.", "1. 37 / 2 = 18 R 1\n2. 18 / 2 = 9 R 0\n3. 9 / 2 = 4 R 1\n4. 4 / 2 = 2 R 0\n5. 2 / 2 = 1 R 0\n6. 1 / 2 = 0 R 1\nReading bottom-up: **100101**.\nCheck: 32 + 4 + 1 = 37 ✅\n**Answer: 100101**"),
    cs("Convert binary 11101 to decimal step-by-step.", "1*16 + 1*8 + 1*4 + 0*2 + 1*1 = 16 + 8 + 4 + 0 + 1 = 29.\n**Answer: 29**"),
    cs("A student says: 'Adding more SSD storage to my laptop will allow me to run more browser tabs simultaneously without slowing down.' Is this correct?", "No, this is **incorrect**.\n\nBrowser tabs are active running programs loaded into **RAM (Random Access Memory)**. Running more simultaneous tabs requires more **RAM**, not more SSD storage. SSD only stores the files permanently."),
    cs("Write an algorithm to reverse an array of n integers in-place.", "1. Set two pointers: left = 0, right = n - 1.\n2. While left < right:\n   a. Swap array[left] and array[right].\n   b. left = left + 1, right = right - 1.\n3. Return reversed array."),
    cs("What is the difference between a variable and a constant?", "A variable is a named memory location whose value can change during program execution. A constant is an identifier whose assigned value is immutable and cannot be changed after declaration."),
    cs("Explain how a linear search algorithm works. What is its worst-case time complexity?", "Linear search checks every element of the collection sequentially from index 0 to n-1 until the target is found or end is reached. Worst-case time complexity is **O(n)**."),
    cs("What is the function of a router in a computer network?", "A router is a networking device that forwards data packets between computer networks based on IP routing tables, directing traffic across the Internet."),
    cs("Why are computer data sizes measured in powers of 2 (1 KB = 1024 Bytes)?", "Because digital computers use the binary number system (base 2). $2^{10} = 1024$, which is the closest power of 2 to 1000.")
]

print(f"CS loaded: Train={len(cs_train)}, Val={len(cs_val)}, Test={len(cs_test)}")
