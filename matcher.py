# matcher.py
# Core matching logic and data storage for RoomMatch
# Calculates compatibility using lifestyle habit vectors, mappings, and sorting

import os
import json
from array import array
import numpy as np

# File path for saving student records
DATA_FILE = os.path.join(os.path.dirname(__file__), "students_data.json")

# In-memory student records: reg_no -> {"info": tuple, "habits": tuple}
students_db = {}

# Factor weights for calculating overall compatibility (sums to 1.0)
WEIGHT_MAPPING = {
    "sleep": 0.30,
    "cleanliness": 0.25,
    "noise": 0.20,
    "study": 0.15,
    "diet": 0.10
}
# 1D weight vector for NumPy dot product
WEIGHT_ARRAY = np.array([0.30, 0.25, 0.20, 0.15, 0.10], dtype=np.float64)

# Habit code mappings for user choices
SLEEP_MAP = {
    "1": "EARLY",
    "2": "MODERATE",
    "3": "NIGHT"
}

STUDY_MAP = {
    "1": "SILENT",
    "2": "MODERATE",
    "3": "MUSIC"
}

DIET_MAP = {
    "1": "VEG",
    "2": "NON_VEG",
    "3": "ANY"
}

# Rating thresholds, visual stars, and compatibility tiers
RATING_TIERS = [
    (90.0, 5.0, "[*****]", "EXCELLENT"),
    (75.0, 4.0, "[**** ]", "GOOD"),
    (50.0, 3.0, "[***  ]", "MODERATE"),
    (35.0, 2.0, "[**   ]", "FAIR"),
    (0.0,  1.0, "[*    ]", "LOW")
]

# ----------------- Storage Functions -----------------

def ensure_loaded(filepath=DATA_FILE):
    """Loads student records into memory if not already loaded."""
    global students_db
    if not students_db and os.path.exists(filepath):
        load_from_file(filepath)

def save_to_file(filepath=DATA_FILE):
    """Saves the student dictionary to a JSON file."""
    global students_db
    serializable = {}
    for reg_no, data in students_db.items():
        serializable[reg_no] = {
            "info": list(data["info"]),
            "habits": list(data["habits"])
        }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=4)

def load_from_file(filepath=DATA_FILE):
    """Loads student records from a JSON file and restores tuples."""
    global students_db
    if not os.path.exists(filepath):
        students_db = {}
        save_to_file(filepath)
        return students_db

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            students_db = {}
            for reg_no, data in raw_data.items():
                students_db[reg_no] = {
                    "info": tuple(data["info"]),
                    "habits": tuple(data["habits"])
                }
    except Exception:
        students_db = {}
        save_to_file(filepath)

    return students_db

def add_student(reg_no, name, gender, dept, year, sleep_time, clean, noise, study, diet, filepath=DATA_FILE):
    """Registers a student profile as immutable tuples and saves to file."""
    global students_db
    ensure_loaded(filepath)
    reg_clean = reg_no.strip().upper()

    if reg_clean in students_db:
        return False, f"Registration number '{reg_clean}' is already registered."

    info_tuple = (name.strip(), gender.strip().upper(), dept.strip().upper(), int(year))
    habits_tuple = (sleep_time.strip().upper(), int(clean), int(noise), study.strip().upper(), diet.strip().upper())

    students_db[reg_clean] = {
        "info": info_tuple,
        "habits": habits_tuple
    }

    save_to_file(filepath)
    return True, f"Student '{reg_clean}' registered successfully."

def get_student(reg_no):
    """Looks up a student record by Registration Number."""
    global students_db
    ensure_loaded()
    reg_clean = reg_no.strip().upper()
    return students_db.get(reg_clean)

def get_all_students():
    """Returns all registered student records."""
    global students_db
    ensure_loaded()
    return students_db

def clear_all_data(filepath=DATA_FILE):
    """Clears all records in memory and empties the JSON file."""
    global students_db
    students_db = {}
    save_to_file(filepath)

# ----------------- Compatibility & Rating Logic -----------------

def get_sleep_score(sleep1, sleep2):
    """Calculates sleep schedule compatibility."""
    if sleep1 == sleep2:
        return 100.0
    elif 'MODERATE' in (sleep1, sleep2):
        return 75.0
    else:
        # Early bird and Night owl clash the most
        return 20.0

def get_cleanliness_score(clean1, clean2):
    """Calculates cleanliness compatibility on a 1-5 scale."""
    diff = float(np.abs(clean1 - clean2))
    return float(np.clip(100.0 - (diff * 25.0), 0.0, 100.0))

def get_noise_score(noise1, noise2):
    """Calculates noise tolerance compatibility on a 1-5 scale."""
    diff = float(np.abs(noise1 - noise2))
    return float(np.clip(100.0 - (diff * 25.0), 0.0, 100.0))

def get_study_score(study1, study2):
    """Calculates study habit compatibility."""
    if study1 == study2:
        return 100.0
    elif 'MODERATE' in (study1, study2):
        return 75.0
    else:
        return 25.0

def get_diet_score(diet1, diet2):
    """Calculates dietary preference compatibility."""
    if diet1 == diet2 or diet1 == 'ANY' or diet2 == 'ANY':
        return 100.0
    else:
        return 65.0

def student_to_array(habits_tuple):
    """Converts a student's habits tuple into a standard Python array of doubles."""
    sleep_str, clean, noise, study_str, diet_str = habits_tuple
    sleep_code = {"EARLY": 1.0, "MODERATE": 2.0, "NIGHT": 3.0}.get(sleep_str, 2.0)
    study_code = {"SILENT": 1.0, "MODERATE": 2.0, "MUSIC": 3.0}.get(study_str, 2.0)
    diet_code = {"VEG": 1.0, "NON_VEG": 2.0, "ANY": 3.0}.get(diet_str, 3.0)
    return array('d', [sleep_code, float(clean), float(noise), study_code, diet_code])

def student_to_numpy_vector(habits_tuple):
    """Converts habit features into a 1D NumPy vector for numerical calculations."""
    arr = student_to_array(habits_tuple)
    return np.array(arr, dtype=np.float64)

def get_rating_and_tier(match_percentage):
    """Converts compatibility percentage into a 5-star rating and harmony tier."""
    rating = round((match_percentage / 100.0) * 5.0, 1)
    for threshold, base_rating, stars, tier in RATING_TIERS:
        if match_percentage >= threshold:
            return rating, stars, tier
    return rating, "[*    ]", "LOW"

def calculate_compatibility(habits1_tuple, habits2_tuple):
    """Unpacks two habit tuples and calculates weighted compatibility using NumPy dot product."""
    sleep1, clean1, noise1, study1, diet1 = habits1_tuple
    sleep2, clean2, noise2, study2, diet2 = habits2_tuple

    s_sleep = get_sleep_score(sleep1, sleep2)
    s_clean = get_cleanliness_score(clean1, clean2)
    s_noise = get_noise_score(noise1, noise2)
    s_study = get_study_score(study1, study2)
    s_diet = get_diet_score(diet1, diet2)

    # 1D array of dimension scores
    score_vector = np.array([s_sleep, s_clean, s_noise, s_study, s_diet], dtype=np.float64)

    # Weighted sum via vector dot product
    overall = float(np.dot(score_vector, WEIGHT_ARRAY))
    overall_pct = round(overall, 2)
    rating, stars, tier = get_rating_and_tier(overall_pct)

    return {
        "overall": overall_pct,
        "rating": rating,
        "stars": stars,
        "tier": tier,
        "sleep": s_sleep,
        "cleanliness": s_clean,
        "noise": s_noise,
        "study": s_study,
        "diet": s_diet
    }

def find_top_roommates(target_reg_no, top_n=5):
    """Finds candidates of the same gender and ranks them in descending order of compatibility."""
    reg_clean = target_reg_no.strip().upper()
    target_data = get_student(reg_clean)
    if not target_data:
        return []

    target_name, target_gender, target_dept, target_year = target_data["info"]
    target_habits = target_data["habits"]

    all_students = get_all_students()
    candidate_matches = []

    for cand_reg, cand_data in all_students.items():
        if cand_reg == reg_clean:
            continue  # Don't match student with themselves

        cand_name, cand_gender, cand_dept, cand_year = cand_data["info"]
        cand_habits = cand_data["habits"]

        # Only evaluate same-gender candidates
        if cand_gender != target_gender:
            continue

        scores = calculate_compatibility(target_habits, cand_habits)
        match_tuple = (scores["overall"], cand_reg, cand_name, cand_dept, cand_year, scores)
        candidate_matches.append(match_tuple)

    # Sort candidates by overall score descending
    sorted_matches = sorted(candidate_matches, key=lambda item: item[0], reverse=True)
    return sorted_matches[:top_n]
