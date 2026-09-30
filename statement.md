# Project Statement: RoomMatch (Roommate Compatibility Match Predictor)

**Subject / Course Domain:** Problem Solving and Python Programming  
**Project Title:** RoomMatch: Real-Time Student Roommate Compatibility Match Predictor  
**Author:** Student Submission (VITyarthi Flipped Course Evaluation)  
**Implementation Language:** Python 3.10+ (Standard Library Only: No SQL, No External Packages)  

---

## 1. Problem Statement

In universities, residential hostels, and student accommodations, roommate pairings are traditionally determined at random or based solely on registration arrival order. This arbitrary assignment creates severe interpersonal friction and lifestyle clashes:

- **Sleep Schedule Desynchronization:** Early birds (waking up at 5:30 AM) clash with night owls (studying or taking calls past 2:00 AM).
- **Cleanliness Discrepancies:** Students with high personal hygiene expectations experience constant stress when co-living with messy roommates.
- **Noise Tolerance and Study Habits:** Silent studiers cannot concentrate when roommates play music, watch videos, or host late-night group discussions.
- **Dietary Differences:** Unspoken friction regarding vegetarian and non-vegetarian food sharing in shared living spaces.

These persistent clashes lead to roommate disputes, mental fatigue, reduced academic performance, and administrative strain. 

The **RoomMatch** system solves this problem using foundational computer science and Python data structures. By collecting quantified lifestyle parameters tied to university registration numbers (e.g., `26BCE10284`), the system applies a multi-attribute weighted similarity algorithm to calculate compatibility percentages, computes an **Overall 5-Star Rating** with harmony tiers, and ranks the most compatible prospective roommates in real time.

---

## 2. Scope of the Project

- **Real-Time Data Representation:** Managing student demographic profiles and living habit parameters in real time using in-memory Python **Dictionaries** and **Immutable Tuples**.
- **Quantified Lifestyle Parameters:** Capturing five essential living habits:
  1. Sleep Schedule (`EARLY`, `MODERATE`, `NIGHT`)
  2. Cleanliness Expectation (Rating scale 1 to 5)
  3. Noise Tolerance (Rating scale 1 to 5)
  4. Study Environment (`SILENT`, `MODERATE`, `MUSIC`)
  5. Dietary Preference (`VEG`, `NON_VEG`, `ANY`)
- **Mapping & Mathematical Evaluation:** Computing weighted similarity using dictionary weight mappings (`WEIGHT_MAPPING`) without external mathematical libraries.
- **Overall 5-Star Rating Scale:** Converting match percentages (0–100%) into an objective 5.0 rating scale, star representation (`★★★★★`), and harmony category (`EXCELLENT`, `GOOD`, `MODERATE`, `FAIR`, `LOW`).
- **Sorting Algorithms:** Ranking candidate roommates dynamically in descending order of compatibility using Python's built-in `sorted()` algorithm.
- **Console & File Input/Output:** Providing interactive console input validation, formatted tabular output, and real-time JSON file persistence (`open()`, `json.dump()`, `json.load()`).

---

## 3. Target Users

1. **University Students:**
   - Register their personal details using their unique Registration Number (e.g., `26BCE10284`).
   - Input daily lifestyle preferences and living expectations.
   - Instantly view ranked prospective roommates of the same gender along with compatibility percentages and overall 5-star ratings.

2. **Hostel Administrators & Wardens:**
   - View the live, real-time registry of all registered students and their habits in a clean tabular view.
   - Run predictions between any registered students to assist in peaceful, harmonious room assignments.

---

## 4. High-Level Features & Concept Mapping

| Feature | Description | Python Implementation |
| :--- | :--- | :--- |
| **Immutable Records** | Student demographics and habit vectors cannot be modified in-place accidentally. | Packed into Python **Tuples** `(name, gender, dept, year)` and `(sleep, clean, noise, study, diet)`. |
| **Keyed Registry** | Prevents duplicate student registrations and enables $O(1)$ fast lookups. | Python **Dictionaries** keyed by uppercase Registration Number (`students_db[reg_no]`). |
| **Configurable Weights** | Modular lifestyle weights that can be tuned without altering calculation logic. | Python **Mappings** (`WEIGHT_MAPPING = {"sleep": 0.30, "cleanliness": 0.25, ...}`). |
| **Overall 5-Star Rating** | Translates percentage match into an intuitive rating and harmony tier. | Scaled rating function `get_rating_and_tier()` returning score, stars, and tier. |
| **Candidate Ranking** | Sorts compatible candidates from highest to lowest match score. | Python's built-in **Sorting** (`sorted(..., key=lambda item: item[0], reverse=True)`). |
| **Real-Time Persistence** | Automatically saves and loads registered students without database servers. | Python **File I/O** (`with open("students_data.json", ...)`) updating live. |
| **Automated Verification** | Full test suite verifying dictionary keys, tuple unpacking, mapping sums, and sort orders. | Built-in **unittest** module (9 unit tests, 100% pass rate). |
