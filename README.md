# 🏠 RoomMatch: Real-Time Student Roommate Compatibility Match Predictor

> **A Pure Python Real-Time Roommate Matching System for University Hostels**  
> *Course Domain:* Problem Solving and Python Programming | *Evaluation:* VITyarthi Flipped Course Project  
> *Core Data Structures:* **Tuples** • **Dictionaries** • **Mappings** • **Sorting Algorithms** • **File I/O**  
> *Dependencies:* **100% Python Standard Library (Zero External Packages, Zero SQL)**

---

## 📋 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Key Python Concepts & Architecture](#2-key-python-concepts--architecture)
3. [Compatibility Scoring & Overall 5-Star Rating](#3-compatibility-scoring--overall-5-star-rating)
4. [File Structure](#4-file-structure)
5. [How to Run the Project](#5-how-to-run-the-project)
6. [Unit Testing & Verification](#6-unit-testing--verification)
7. [Sample Real-Time Terminal Execution](#7-sample-real-time-terminal-execution)
8. [Submission Guidelines Checklist](#8-submission-guidelines-checklist)

---

## 1. Project Overview

In university student accommodations, roommate pairings are traditionally assigned at random or by registration queue. This arbitrary matching creates severe interpersonal friction:
- **Sleep Desynchronization:** Early birds (waking up at 5:30 AM) clash with night owls (active past 2:00 AM).
- **Cleanliness Discrepancies:** Tidy students face stress living alongside messy peers.
- **Noise & Study Clashes:** Silent studiers clash with students who listen to music or study in groups.
- **Dietary Preferences:** Friction regarding vegetarian vs non-vegetarian shared living spaces.

**RoomMatch** solves this problem by providing an objective, real-time matching system written in pure Python. It captures student demographics and lifestyle habits, computes weighted multi-factor compatibility scores, converts scores into an **Overall 5-Star Rating** and **Harmony Tier**, and ranks prospective roommates in real time.

---

## 2. Key Python Concepts & Architecture

The application is purposefully built to demonstrate mastery of core Python programming concepts:

| Python Concept | How It Is Implemented | Location in Code |
| :--- | :--- | :--- |
| **Immutable Tuples** | Student personal info `(name, gender, dept, year)` and habit vectors `(sleep, clean, noise, study, diet)` are packed into immutable tuples to prevent accidental mutation. | [`storage.py`](file:///d:/New%20folder/room_match_system/storage.py) |
| **Dictionaries** | Fast \(O(1)\) hash map storage mapping unique Registration Numbers (`reg_no`) to student records. | [`storage.py`](file:///d:/New%20folder/room_match_system/storage.py) |
| **Mappings** | Dictionary mappings decouple business logic from configuration: `WEIGHT_MAPPING`, `SLEEP_MAP`, `STUDY_MAP`, `DIET_MAP`. | [`matcher.py`](file:///d:/New%20folder/room_match_system/matcher.py), [`main.py`](file:///d:/New%20folder/room_match_system/main.py) |
| **Sorting Algorithms** | Candidate matches are packed into tuples and sorted in descending order of compatibility using Python's built-in `sorted(..., reverse=True)`. | [`matcher.py`](file:///d:/New%20folder/room_match_system/matcher.py) |
| **File Input & Output** | Real-time persistence using standard file I/O (`open()`, `json.dump()`, `json.load()`) to persist registered students between runs without SQL. | [`storage.py`](file:///d:/New%20folder/room_match_system/storage.py) |
| **Console I/O** | Clean interactive `input()` validation, formatted ASCII tables, and status notifications. | [`main.py`](file:///d:/New%20folder/room_match_system/main.py) |

---

## 3. Compatibility Scoring & Overall 5-Star Rating

### A. Weighted Lifestyle Dimensions
Compatibility is calculated across 5 dimensions using `WEIGHT_MAPPING`:
$$\text{Score} = (0.30 \times \text{Sleep}) + (0.25 \times \text{Cleanliness}) + (0.20 \times \text{Noise}) + (0.15 \times \text{Study}) + (0.10 \times \text{Diet})$$

- **Sleep Schedule (30%):** Early Bird vs Night Owl synchronization.
- **Cleanliness Level (25%):** Distance formula: $\max(0, 100 - |C_1 - C_2| \times 25)$.
- **Noise Tolerance (20%):** Distance formula: $\max(0, 100 - |N_1 - N_2| \times 25)$.
- **Study Environment (15%):** Silent, Moderate, or Music compatibility.
- **Dietary Preference (10%):** Veg, Non-Veg, or Any.

### B. Overall 5-Star Rating & Harmony Tiers
Match percentages are automatically converted into a 5.0-point rating scale and verbal harmony tier:

| Match Percentage | Overall Rating | Star Representation | Harmony Tier |
| :---: | :---: | :---: | :---: |
| **90.0% – 100%** | **4.5 – 5.0 / 5.0** | ★★★★★ | `EXCELLENT` |
| **75.0% – 89.9%** | **3.8 – 4.4 / 5.0** | ★★★★☆ | `GOOD` |
| **50.0% – 74.9%** | **2.5 – 3.7 / 5.0** | ★★★☆☆ | `MODERATE` |
| **35.0% – 49.9%** | **1.8 – 2.4 / 5.0** | ★★☆☆☆ | `FAIR` |
| **Below 35.0%** | **0.0 – 1.7 / 5.0** | ★☆☆☆☆ | `LOW` |

---

## 4. File Structure

```text
room_match_system/
├── config.py              # Centralized configuration, weight mappings, and rating definitions
├── storage.py             # Dictionaries, Tuples, and File Input/Output persistence
├── matcher.py             # Mappings, scoring logic, Overall 5-Star Ratings, and Sorting
├── main.py                # Real-time CLI interface, input validation, and output tables
├── test_system.py         # Automated unit test suite (9 tests, 100% passing)
├── students_data.json     # Real-time data file (starts clean, persists live inputs)
├── RoomMatch_Report.docx  # 15-Section Project Report DOCX (editable academic report)
├── RoomMatch_Report.pdf   # 15-Section Project Report PDF (for portal upload)
├── statement.md           # Problem statement & technical scope document
├── README.md              # Clear setup and execution guide
├── requirements.txt       # Dependencies (standard library only)
└── .gitignore             # Keeps Git repository clean
```

---

## 5. How to Run the Project

### Prerequisites
- Python 3.8 or higher installed.
- No external libraries required (pure standard library).

Navigate into the project directory:
```bash
cd "d:\New folder\room_match_system"
```

### Option A: Interactive Real-Time Terminal Menu
```bash
python main.py
```
This launches the clean 3-option menu:
```text
============================================================================
      ROOMMATCH: REAL-TIME ROOMMATE COMPATIBILITY PREDICTOR     
     Pure Python: Tuples, Dictionaries, Mappings & Sorting     
============================================================================

MAIN MENU:
1. Register as a New Student (Input Reg No & Habits -> Real-Time Match)
2. View All Registered Students (Real-Time Live Registry)
3. Predict Roommates for a Registered Student
0. Exit

Select an option (0-3):
```

### Option B: Quick Command-Line Flags
```bash
# Register a student interactively in real time
python main.py --register

# View all real-time registered students in a formatted table
python main.py --list

# Predict roommate matches for a specific student registration number
python main.py --match 26BCE10284
```

---

## 6. Unit Testing & Verification

Run the automated test suite with Python's built-in `unittest`:
```bash
python test_system.py
```

### Test Coverage (9/9 Tests Passing):
1. `test_dictionary_lookup`: Verifies $O(1)$ dictionary key retrieval by registration number.
2. `test_tuple_structure_and_unpacking`: Validates that student details and habit vectors are stored as immutable tuples.
3. `test_duplicate_registration_rejected`: Confirms dictionary key uniqueness prevents duplicate registrations.
4. `test_weight_mapping_completeness`: Confirms dimension weight mappings sum to exactly 1.0 (100%).
5. `test_sleep_and_cleanliness_logic`: Validates mathematical distance formulas for living habits.
6. `test_overall_rating_and_tier_calculation`: Verifies score-to-stars conversion ($95\% \to 4.8/5.0 \text{ ★★★★★}$).
7. `test_compatibility_symmetry`: Proves mathematical symmetry ($\text{Match}(A, B) == \text{Match}(B, A)$).
8. `test_sorting_order_of_predictions`: Confirms candidate tuples are sorted in descending order of match percentage.
9. `test_gender_isolation_in_matching`: Confirms male students only match with male roommates (and female with female).

---

## 7. Sample Real-Time Terminal Execution

```text
$ python main.py --match 26BCE10284

======================================================================================
      REAL-TIME PREDICTIONS FOR [26BCE10284] Aarav Sharma      
      Dept: CSE | Year: 1 | Habits: NIGHT, Clean: 4/5, Noise: 2/5
======================================================================================

Rank | Reg No       | Name               | Dept     | Match %  | Overall Rating | Harmony Tier
--------------------------------------------------------------------------------------
#1   | 26BCE10042   | Rohan Verma        | CSE      | 95.0%    | 4.8/5.0 ★★★★★  | EXCELLENT
#2   | 25BEC10088   | Neeraj Kumar       | ECE      | 93.8%    | 4.7/5.0 ★★★★★  | EXCELLENT
#3   | 26BIT10319   | Siddharth Patel    | IT       | 77.5%    | 3.9/5.0 ★★★★☆  | GOOD
#4   | 25BCE10521   | Kabir Mehta        | CIVIL    | 38.8%    | 1.9/5.0 ★★☆☆☆  | FAIR
#5   | 25BME10115   | Vikram Singh       | MECH     | 33.8%    | 1.7/5.0 ★☆☆☆☆  | LOW
```

---

## 8. Submission Guidelines Checklist

- [x] **Public GitHub Repository:** Strictly formatted root URL (`https://github.com/DheerKumarSharma001/roommate-match-predictor`).
- [x] **README.md at root:** Complete setup, running, and testing documentation included.
- [x] **statement.md at root:** Contains problem statement, scope, target users, and features.
- [x] **Project Report PDF:** 15-Section PDF matching the exact VITyarthi guidelines.
- [x] **Zero Mock Data:** Runs 100% on live, real-time input data.
- [x] **Standard Library Only:** Zero external dependencies or complex database engines needed.
