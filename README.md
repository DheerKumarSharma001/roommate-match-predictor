# 🏠 RoomMatch: Hostel Roommate Compatibility Matcher

A simple, real-time Python application that helps college students find compatible hostel roommates based on their daily living habits.

* **Course:** Problem Solving and Python Programming
* **Core Concepts:** Tuples, Dictionaries, Mappings, Python Arrays, NumPy Vectors, Sorting, and File I/O
* **Dependencies:** Python 3 standard library + `numpy` (Zero SQL databases)

---

## 📌 Why RoomMatch?

In college hostels, rooms are usually assigned at random or by who stands first in the queue. This often leads to roommates fighting within the first month over simple everyday habits:
* **Night Owls vs Early Birds:** Someone turning on the room light at 6:00 AM while their roommate slept at 3:00 AM.
* **Neat vs Messy:** One roommate wanting a clean room while the other leaves things lying everywhere.
* **Quiet vs Loud Studiers:** Needing silence to focus while a roommate attends group calls or plays music.
* **Food Preferences:** Veg and non-veg food sharing preferences inside the room.

**RoomMatch** solves this by letting students register their habits, calculates how well two students will live together using weighted math, and ranks the best roommate matches.

---

## ⚙️ How the Matching Works

When a student registers, they provide 5 key habits. Each factor is given a specific weight in calculating compatibility:

| Factor | Weight | How It Is Evaluated |
| :--- | :---: | :--- |
| **Sleep Schedule** | **30%** | Early Bird, Moderate, or Night Owl. Same schedules get 100%, Early vs Night gets 20% (biggest conflict). |
| **Cleanliness** | **25%** | Rated 1 (relaxed) to 5 (spotless). Evaluated based on absolute difference. |
| **Noise Tolerance** | **20%** | Rated 1 (need silence) to 5 (music/calls fine). Evaluated based on absolute difference. |
| **Study Environment** | **15%** | Silent, Moderate, or Background Music. Same styles match best. |
| **Dietary Preference** | **10%** | Vegetarian, Non-Veg, or Any/Flexible. |

### Vector Math with NumPy
Each factor score (0–100) is stored in a score vector and multiplied by the weights vector using NumPy's dot product:

```python
score_vector = np.array([s_sleep, s_clean, s_noise, s_study, s_diet], dtype=np.float64)
overall_score = float(np.dot(score_vector, WEIGHT_ARRAY))
```

### Overall 5-Star Rating & Compatibility Tiers
The overall percentage is converted into a 5-star rating scale and compatibility tier:

* **90% – 100%:** `4.5 – 5.0 / 5.0` | `[*****]` | **EXCELLENT** (Great habit match)
* **75% – 89%:** `3.8 – 4.4 / 5.0` | `[**** ]` | **GOOD** (Solid match, minor differences)
* **50% – 74%:** `2.5 – 3.7 / 5.0` | `[***  ]` | **MODERATE** (Workable with good communication)
* **35% – 49%:** `1.8 – 2.4 / 5.0` | `[**   ]` | **FAIR** (Noticeable habit clashes)
* **Below 35%:** `0.0 – 1.7 / 5.0` | `[*    ]` | **LOW** (Severe clash, e.g. Early Bird vs Night Owl)

*(Clean ASCII characters like `[*****]` are used so the program runs smoothly on any terminal without Windows encoding issues).*

---

## 📁 Project Structure

The project is kept simple with just **3 custom Python files**:

```text
room_match_system/
├── main.py              # User interface: Menu, inputs, and formatted tables
├── matcher.py           # Core logic: Habits math, array/numpy, and JSON file saving
├── test_system.py       # 12 automated unit tests using Python's unittest
├── students_data.json   # JSON file where student profiles are stored
├── statement.md         # Formal project problem statement
└── README.md            # Project guide and documentation
```

---

## 🚀 How to Run the Project

### 1. Requirements
* Python 3.8 or newer
* `numpy` installed:
  ```bash
  pip install numpy
  ```

### 2. Run the Application
Open a terminal in the project folder and run:
```bash
python main.py
```

You will see the main menu:
```text
======================================================================
         RoomMatch: Student Roommate Compatibility Matcher
======================================================================

--- MENU ---
1. Register new student & view matches
2. View all registered students
3. Find roommate matches for an existing student
0. Exit

Enter your choice (0-3):
```

---

## 🖥️ Walkthrough of Menu Options

### Option 1: Register New Student
Enter your registration number, name, gender, department, year, and living habits:

```text
--- Student Registration ---
Enter Registration Number (e.g., 26BCE10284): 26BCE10284
Enter Full Name: Dheer
Enter Gender (M/F): F
Enter Department (e.g., CSE, ECE, MECH): CSE
Enter Year of Study [1-5, default 1]: 2

--- Living Habits & Preferences ---
Sleep Schedule: [1] Early Bird  [2] Moderate  [3] Night Owl
Your choice (1-3) [default 2]: 1
Cleanliness (1=Relaxed to 5=Spotless) [1-5, default 3]: 1
Noise Tolerance (1=Quiet to 5=Music Allowed) [1-5, default 3]: 1
Study Environment: [1] Silent  [2] Moderate  [3] Background Music
Your choice (1-3) [default 1]: 1
Dietary Preference: [1] Vegetarian  [2] Non-Veg  [3] Any/Flexible
Your choice (1-3) [default 3]: 1

Student '26BCE10284' registered successfully.
```

If matching candidates exist in the database, your top roommate matches appear right away!

### Sample Match Output:
```text
================================================================================
 Compatible Roommate Matches for: Dheer (26BCE10284)
 Profile: CSE, Year 2 | Sleep: EARLY | Cleanliness: 1/5 | Noise: 1/5
================================================================================

Rank | Reg No       | Name               | Dept     | Match %  | Rating         | Compatibility
--------------------------------------------------------------------------------
#1   | 26BCE10190   | Ananya Iyer        | CSE      | 100.0%   | 5.0/5.0 [*****] | EXCELLENT
#2   | 26BIT10452   | Sneha Reddy        | IT       | 93.8%    | 4.7/5.0 [*****] | EXCELLENT
#3   | 25BEC10078   | Priya Sharma       | ECE      | 76.5%    | 3.8/5.0 [**** ] | GOOD
#4   | 26BCE10891   | Rhea Sen           | CSE      | 54.5%    | 2.7/5.0 [***  ] | MODERATE
#5   | 25BME10304   | Tanvi Kapoor       | MECH     | 27.5%    | 1.4/5.0 [*    ] | LOW
```

*Note: Male students only match with male students, and female students only match with female students.*

---

### Option 2: View All Registered Students
Prints a clean table showing everyone currently in the database:

```text
--- Registered Students ---
Total Registered Students: 2
Reg No       | Name             | Gender | Dept   | Yr | Sleep    | Clean | Noise | Study    | Diet
--------------------------------------------------------------------------------------------
26BCE10284   | Dheer            | F      | CSE    | 2  | EARLY    | 1/5   | 1/5   | SILENT   | VEG
26BCE10190   | Ananya Iyer      | F      | CSE    | 2  | EARLY    | 1/5   | 1/5   | SILENT   | VEG
```

---

### Option 3: Find Matches for an Existing Student
Enter any registered student's registration number (e.g., `26BCE10284`) to view their latest ranked matches without re-registering.

---

## 🧪 Testing the Code

The project includes an automated test file `test_system.py` built using Python's standard `unittest` module.

Run all tests with:
```bash
python test_system.py
```

### What the 12 tests verify:
1. **Dictionary Lookups:** Quick $O(1)$ student record retrieval by Reg No.
2. **Tuple Integrity:** Verifying that student details and habits are stored as immutable tuples.
3. **Duplicate Prevention:** Making sure two students can't register with the same Reg No.
4. **Weights Sum:** Ensuring all 5 weights add up to 1.0 (100%).
5. **Score Calculations:** Verifying distance formulas for cleanliness, noise, sleep, etc.
6. **Rating Tiers:** Testing percentage to 5-star rating conversion.
7. **Symmetry:** Checking that compatibility between Student A and Student B is identical to B and A.
8. **Sorting Order:** Ensuring roommate results are always sorted from highest score to lowest score.
9. **Gender Filter:** Ensuring male and female students are never matched together.
10. **Array Features:** Testing conversion of habits into Python's `array('d')`.
11. **NumPy Dot Product:** Checking the vectorized math against expected scores.
12. **File Persistence:** Verifying that student data saves to JSON and reloads without loss.

**Result:**
```
............
----------------------------------------------------------------------
Ran 12 tests in 0.060s

OK
```

---

## 💡 Python Concepts Used in This Project

* **Tuples:** Used for `(name, gender, dept, year)` and `(sleep, clean, noise, study, diet)` to make sure student data cannot be modified accidentally after creation.
* **Dictionaries:** Used for the student registry (`students_db[reg_no]`), allowing fast lookups and easy saving to JSON.
* **Mappings:** Used for weights (`WEIGHT_MAPPING`) and menu choice dictionaries (`SLEEP_MAP`, `STUDY_MAP`, `DIET_MAP`).
* **Python Arrays:** Demonstrates standard library `array('d', [...])` for compact numeric storage.
* **NumPy:** Used for vector math (`np.dot`, `np.abs`, `np.clip`) to calculate the final weighted compatibility.
* **Sorting:** Uses Python's native `sorted()` with a custom `key=lambda` to sort candidates by match percentage descending.
* **File Handling:** Uses `json.dump()` and `json.load()` to save data to disk so students aren't lost when closing the program.
* **Defensive Inputs:** Uses helper functions with `try/except` and range bounds so bad user input never crashes the program.
