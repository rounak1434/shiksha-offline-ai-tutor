# 🎓 Offline AI Tutor — Evaluation Report

Side-by-side comparison between **Base Qwen3-0.6B** and **QLoRA Fine-Tuned Tutor**.

## Test Case 1: What is the difference between mass and weight?

### 🤖 Base Model (Qwen3-0.6B)

Mass and weight are related but distinct concepts:

- **Mass** is the amount of matter in an object. It is a **scalar quantity** and does not depend on the gravitational field. For example, two objects of the same mass will have the same mass, regardless of their location.

- **Weight** is the force exerted on an object due to gravity. It is a **vector quantity** and depends on the gravitational field. For example, an object of mass $ m $ will have a weight of $ W = m \cdot g $, where $ g $ is the acceleration due to gravity.

### Summary:
- **Mass** = amount of matter  
- **Weight** = force due to gravity (mass × gravity)  

They are not the same, but they are related.

### 🎓 Fine-Tuned Tutor (QLoRA)

**Mass** is the amount of matter in an object. It is constant and measured in kilograms (kg) or grams (g). Mass is independent of gravity.

**Weight** is the force due to gravity acting on an object. It depends on the gravitational field strength (acceleration due to gravity) and the mass of the object. Weight is measured in newtons (N) and is **dependent on gravity**.

**Example:**
- Mass of a 10 kg object = 10 kg (constant).
- Weight of a 10 kg object on Earth = 98 N (since g = 9.8 m/s²).
- Weight of a 10 kg object on the Moon = 10 * 1.6 = 16 N (g = 1.6 m/s²).

**Key point:** Mass is measured in kg, weight in N.

---

## Test Case 2: Explain Newton's second law to a class 8 student in simple language.

### 🤖 Base Model (Qwen3-0.6B)

Sure! Here's a simple explanation of **Newton's Second Law** in terms of a class 8 student:

---

**Newton's Second Law** is like saying:  
**If you push something harder, it moves faster.**

Let’s break it down with an example:

Imagine you are holding a ball and you push it harder. The ball will go **faster** and **stiffer**.  
This is because the **force** you apply is what makes the ball move.

So, in simple terms:

- **Force** = mass × acceleration  
  (F = ma)

- If you apply more force, the ball moves faster (acceleration increases).

---

**Example for a 8th grader:**

- If you push a ball harder, it goes faster.  
- If you push it less, it goes slower.  
- The harder you push, the faster it goes.

---

Let me know if you want a visual or a diagram! 😊

### 🎓 Fine-Tuned Tutor (QLoRA)

Newton's second law of motion says that **force equals mass times acceleration** (F = ma). 

**Simple example:**
- If a car is moving at 60 km/h and you apply a force to it, it will accelerate.
- If the force is too large, the car will stop or reverse.
- If the force is too small, the car will not accelerate.

**Key points:**
- Force = mass × acceleration
- Mass = mass (doesn't change)
- Acceleration = force / mass
- More force = more acceleration
- More mass = less acceleration

**Formula:**
F = m × a

**Example:**
- A 10 kg car is moving at 20 m/s. What is the force needed to stop it in 10 seconds?
- Acceleration = (Final velocity - Initial velocity) / time
- Final velocity = 0 (stopped)
- Acceleration = (0 - 20) / 10 = -2 m/s²
- Force = mass × acceleration = 10 kg × -2 m/s² = -20 N (force in opposite direction)

**Key takeaway:**
- Force is the reason why things change direction or speed.
- Mass doesn't change, but acceleration depends on force and mass.

---

## Test Case 3: A student says 'my weight is 50 kg'. Is this scientifically correct? Explain.

### 🤖 Base Model (Qwen3-0.6B)

The statement "my weight is 50 kg" is **scientifically incorrect**. Here's why:

1. **Weight is a measure of mass** at a specific location and time. It is not a direct measure of mass.  
   - Weight is calculated using the formula:  
     $ W = m \cdot g $, where $ W $ is weight, $ m $ is mass, and $ g $ is the acceleration due to gravity.  
   - Therefore, a person's weight (in kg) is a result of their mass and the gravitational field, not their mass itself.

2. **Mass is a measure of how much matter an object contains**, while weight is a force.  
   - For example, a 50 kg person would have a weight of approximately 50 kg × 9.8 m/s² ≈ 490 N (Newtons), not 50 kg.

3. **Weight is not a unit of mass**. The unit of mass is the kilogram (kg), and the unit of weight is the newton (N).  
   - So, a person's weight (in newtons) is not the same as their mass (in kilograms).

### Conclusion:
The statement "my weight is 50 kg" is **not scientifically correct**. Weight is a force, and it is not a measure of mass.

### 🎓 Fine-Tuned Tutor (QLoRA)

**Scientifically incorrect.**

Weight is a force, measured in Newtons (N). It depends on two factors:

1. **Mass**: How much matter is in the object. More mass means more weight (same height, same gravity).
2. **Gravity**: How strong the Earth's gravity is. On Earth, gravity is about 9.8 m/s².

**Weight = mass × gravity**

So, if a student weighs 50 kg on Earth, their mass is 50 kg. But their weight is 50 × 9.8 = 490 N.

**Key point:** Mass is measured in kilograms, weight in Newtons.

---

## Test Case 4: What is the difference between speed and velocity?

### 🤖 Base Model (Qwen3-0.6B)

Speed and velocity are both measures of how fast an object is moving, but they differ in one key aspect: **direction**.

### **Speed**:
- Is a scalar quantity, meaning it only describes how fast an object is moving, **without considering direction**.
- Example: A car moving at 60 km/h has a speed of 60 km/h.

### **Velocity**:
- Is a vector quantity, meaning it includes both magnitude and direction.
- Example: A car moving at 60 km/h to the east has both speed (60 km/h) and direction (east).

### Summary:
| **Speed** | **Velocity** |
|-----------|--------------|
| Scalar    | Vector      |
| Directional | Directional |
| Example: | Example: |

### 🎓 Fine-Tuned Tutor (QLoRA)

**Speed** and **velocity** are both measures of how fast an object is moving, but they differ in one key detail: **direction**.

**Speed** is a scalar quantity, meaning it only tells you how fast the object is moving, not the direction. It is calculated as distance divided by time.

**Velocity** is a vector quantity, meaning it includes both speed and direction. It is calculated as displacement divided by time.

**Example:**
- A car moving at 60 km/h (speed) has a speed of 60 km/h.
- A car moving at 60 km/h north (velocity) has both speed and direction.

**Key difference:**
- Speed = distance / time
- Velocity = displacement / time

**Note:** Speed is always less than or equal to velocity.

---

## Test Case 5: Why does an ice cube float on water?

### 🤖 Base Model (Qwen3-0.6B)

An ice cube floats on water because of **density**. Ice has a **lower density** than water, which means it is less dense than water. When water freezes, it forms a solid structure, and the ice cube floats on top of the water. This is a common phenomenon observed in nature and everyday life.

### 🎓 Fine-Tuned Tutor (QLoRA)

Ice cubes float on water because of **density differences** between ice and water.

**Ice:**
- Ice has a lower density than water.
- Density = mass / volume.
- Ice cubes are less dense than water, so they float.

**Water:**
- Water has a higher density than ice.
- Density = mass / volume.
- Ice cubes sink to the bottom of the water.

**Why does ice float?**
Ice forms a **lens shape** (icebergs) because it expands when water freezes. This shape allows ice to float on water.

**Key point: Ice is less dense than water.**

---

