# Project Problem Statement: RoomMatch

**Project Title:** RoomMatch – Hostel Roommate Compatibility Matcher  
**Course:** Problem Solving and Python Programming  
**Technology:** Python 3 (using `os`, `json`, `array`, `numpy`, `unittest`)  
**Data Storage:** JSON Flat-File (No SQL required)  

---

## 1. Introduction & Background

When students move into university hostels, room allotment is usually done at random, by queue number, or by alphabetical roll call. While this is easy for hostel administration, it frequently leads to severe roommate conflicts within weeks of moving in.

In shared dorm rooms, conflicts almost always come down to clashing daily routines rather than personality differences:
- **Sleep Timings:** A student waking up at 5:30 AM turns on lights and makes noise, disturbing a roommate who studies until 2:00 AM.
- **Cleanliness:** A student who likes a spotless desk and made bed gets frustrated living with a roommate who leaves clothes and food packets around.
- **Study Environment:** Some students need complete silence, while others study best with music playing or study in groups.
- **Dietary Preferences:** Students who are strictly vegetarian sometimes prefer living with other vegetarians to feel comfortable about food in the shared room.

**RoomMatch** is a Python-based roommate compatibility tool designed to solve this problem. It allows students to enter their registration number, branch, and five key lifestyle habits. Using weighted similarity scoring and vector math with NumPy and arrays, it predicts compatibility, provides an overall 5-star rating, and ranks prospective roommates in order of suitability.

---

## 2. Project Objectives

1. **Simple Lifestyle Profiling:** Capture 5 essential habit parameters (Sleep schedule, Cleanliness, Noise tolerance, Study style, and Dietary preference).
2. **Gender-Specific Matching:** Ensure male students are only matched with male roommates, and female students with female roommates.
3. **No Heavy Database Overhead:** Avoid complex SQL servers. Instead, use Python dictionaries and immutable tuples with clean JSON file saving.
4. **Vectorized Mathematical Scoring:** Represent habit scores as numeric vectors and calculate the weighted overall score using NumPy's dot product (`np.dot`).
5. **Clear 5-Star Rating System:** Convert the percentage score into an easy-to-understand 5.0 rating with star bars (`[*****]`) and harmony tiers (`EXCELLENT`, `GOOD`, `MODERATE`, `FAIR`, `LOW`).
6. **Instant Candidate Ranking:** Sort all eligible roommates from highest to lowest compatibility using Python's built-in sorting.
7. **Comprehensive Unit Testing:** Ensure the system is fully verified with automated unit tests for scoring, sorting, and file persistence.

---

## 3. Scope of the System

### What the system does:
- **Interactive Registration:** Prompts students for their Registration Number (e.g., `26BCE10284`), name, gender, department, year, and living habits.
- **Input Validation:** Prevents duplicate registrations and validates ranges (e.g., year between 1 and 5, cleanliness scale 1 to 5).
- **Real-Time Matching:** Compares the student against all registered candidates of the same gender.
- **Automated Ranking:** Displays the top matched roommates in a clean tabular view.
- **Persistent Storage:** Saves profiles directly into `students_data.json` so records are preserved between runs.
- **Registry View:** Allows hostel admins or students to view all currently registered students in a formatted table.

### What is kept out of scope (to keep the system clean and lightweight):
- No external relational database engines (no MySQL, PostgreSQL, or SQLite).
- No complex web frameworks; runs directly in standard Python terminal.
- No dummy/mock seed data hardcoded; the database starts empty and populates dynamically.

---

## 4. Python Concepts & Implementation

| Python Concept | Where It Is Used in the Code | Why It Was Chosen |
| :--- | :--- | :--- |
| **Immutable Tuples** | Student info `(name, gender, dept, year)` and habits `(sleep, clean, noise, study, diet)` in `matcher.py`. | Prevents accidental modification of student data once entered. |
| **Dictionaries** | In-memory student database `students_db[reg_no]` and score breakdowns. | Provides fast $O(1)$ lookups by registration number and prevents duplicate entries. |
| **Mappings** | `WEIGHT_MAPPING`, `SLEEP_MAP`, `STUDY_MAP`, `DIET_MAP`, and `RATING_TIERS`. | Keeps factor weights and menu choices organized in one place without hardcoding numbers inside functions. |
| **Standard Array (`array`)** | `student_to_array()` in `matcher.py` creates `array('d', [...])`. | Compact, type-restricted storage of numerical feature vectors. |
| **NumPy Vectors (`numpy`)** | `WEIGHT_ARRAY`, `np.abs`, `np.clip`, and `np.dot(score_vector, WEIGHT_ARRAY)`. | Clean vector math for calculating the overall weighted compatibility score. |
| **Sorting** | `sorted(candidate_matches, key=lambda item: item[0], reverse=True)`. | Ranks candidates in descending order of compatibility score. |
| **File I/O** | `json.dump()` and `json.load()` in `matcher.py`. | Saves and restores student records to `students_data.json` automatically. |
| **Defensive Input Handling** | `prompt_range()` and while loops in `main.py`. | Catches invalid numbers and typo errors gracefully without crashing the program. |
| **Unit Testing** | `test_system.py` with 12 tests using `unittest`. | Verifies that all calculations, lookups, and file operations work correctly. |

---

## 5. Mathematical Scoring Model

The compatibility score between two students is calculated across 5 dimensions:

### 1. Dimension Calculations (0% to 100%):
- **Sleep Schedule (30% weight):**
  - Same schedule: `100%`
  - One is Moderate: `75%`
  - Early Bird vs Night Owl: `20%` (major conflict)
- **Cleanliness (25% weight):**
  - Difference on 1-5 scale: $\max(0, 100 - |C_1 - C_2| \times 25)$
- **Noise Tolerance (20% weight):**
  - Difference on 1-5 scale: $\max(0, 100 - |N_1 - N_2| \times 25)$
- **Study Environment (15% weight):**
  - Same environment: `100%`
  - One is Moderate: `75%`
  - Silent vs Music: `25%`
- **Dietary Preference (10% weight):**
  - Same preference or either is Any/Flexible: `100%`
  - Veg vs Non-Veg: `65%`

### 2. Weighted Overall Score (via NumPy dot product):
$$\text{Scores Vector} = [S_{\text{sleep}}, S_{\text{clean}}, S_{\text{noise}}, S_{\text{study}}, S_{\text{diet}}]$$
$$\text{Weight Vector} = [0.30, 0.25, 0.20, 0.15, 0.10]$$
$$\text{Overall Score} = \mathbf{S} \cdot \mathbf{W}$$

### 3. Overall 5-Star Rating Conversion:
$$\text{Rating} = \text{round}\left(\frac{\text{Overall Score}}{100} \times 5.0, 1\right)$$

- **90% – 100%**: `4.5 – 5.0 / 5.0` | `[*****]` | `EXCELLENT`
- **75% – 89%**: `3.8 – 4.4 / 5.0` | `[**** ]` | `GOOD`
- **50% – 74%**: `2.5 – 3.7 / 5.0` | `[***  ]` | `MODERATE`
- **35% – 49%**: `1.8 – 2.4 / 5.0` | `[**   ]` | `FAIR`
- **Below 35%**: `0.0 – 1.7 / 5.0` | `[*    ]` | `LOW`

---

## 6. Project Files Summary

The project consists of 3 Python files and 1 data file:
- `matcher.py`: Core calculation engine, array/numpy math, and file saving/loading.
- `main.py`: Interactive user menu and registration interface.
- `test_system.py`: 12 automated unit tests verifying the system.
- `students_data.json`: Flat-file storage holding registered student profiles.
