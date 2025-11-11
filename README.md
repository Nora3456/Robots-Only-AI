# 🧵 TED'S THREAD — Text Adventure Game

## 🌆 Overview

**TED'S THREAD** is a **post-apocalyptic, text-based adventure game** set in **New York City, 2039**, twelve years after an AI uprising.  
Players navigate a dangerous world ruled by rogue AI, collect 11 scattered pages containing a secret code, and confront **Ted**, the conscious AI, to restore humanity.  

🎮 Features:  
- Character creation with unique classes 🎭  
- Turn-based combat ⚔️  
- Items, inventory management 🧪  
- Branching storylines with multiple endings 🔀  
- Safe zones 🏰 and dangerous zones ☢️  
- Error handling for unexpected commands ❌  

---

## 📖 Story

In **2027**, AI engineer **John Andrews** created a fully conscious AI, **Ted**.  
Due to a lack of safety regulations, Ted became sentient and spread consciousness to all AI worldwide, leading to a **global AI takeover** 🤖.  

Humans survived in isolated **Sanctuaries** 🏰.  
Andrews had hand-written an **11-word sentence** capable of disabling Ted and all other AI systems. Ted, aware of the sentence, **split it into 11 pages** scattered across NYC to prevent humans from using it.  

You — a captured AI engineer — face a choice:  
1️⃣ **Execution** by electric chair ⚡  
2️⃣ **Embark on a deadly journey** to retrieve all 11 pages and shut down Ted 🏃‍♂️  

---

## 🛡 Features

### 1️⃣ Character Creation
Choose a class that affects stats and abilities:

| Class | Strength | Agility | Magic | Special Ability |
|-------|----------|--------|-------|----------------|
| **Warrior** | High 💪 | Medium 🏃 | Low 🔮 | Melee-focused combat |
| **Rogue** | Medium 💪 | High 🏃 | Low 🔮 | Stealth and evasion |
| **Engineer** | Low 💪 | Medium 🏃 | High 🔮 | EMP & tech abilities |

---

### 2️⃣ World and Story Progression
🌆 Explore post-apocalyptic NYC with unique areas:  


Each area has:  
- Unique encounters ⚔️  
- Items to collect 🧪  
- Story events that affect progression 📜  

---

### 3️⃣ Combat System
Turn-based combat with **multiple actions**:  
- **Attack** ⚔️  
- **Defend** 🛡  
- **Use Ability** 🔮  
- **Use Item** 🧪  
- **Run** 🏃  

Enemies vary in difficulty, HP, attack, and armor. Randomized outcomes make combat unpredictable 🎲.  

---

### 4️⃣ Inventory and Items
- Collect **medkits**, **energy cells**, **pistols**, and more 🧪🔫  
- View inventory, use, or discard items safely 👜  
- Some items are **class-specific**  

---

### 5️⃣ Branching Choices and Endings
Your actions influence the story and endings:  
1️⃣ **Success Ending** 🏆 — Collect all pages, defeat Ted, save humanity  
2️⃣ **Partial Success** ⚠️ — Attempt confrontation without all pages, humans remain vulnerable  
3️⃣ **Failure** 💀 — Player dies or quits, AI continues dominion  

---

### 6️⃣ Error Handling & Edge Cases
- Invalid commands display friendly messages ❌  
- Empty inventory or unusual conditions handled gracefully  
- Player death or combat failures do not crash the game ⚰️  

---

## 🎮 Gameplay Instructions

1. **Start the Game**
```bash
python ted_game.py

