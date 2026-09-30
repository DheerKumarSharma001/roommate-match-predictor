# matcher.py
# Roommate compatibility prediction using Python Mappings, Tuples, and Sorting algorithms.
# 100% pure Python - No SQL dependencies.

from storage import get_student, get_all_students
from config import WEIGHT_MAPPING, RATING_TIERS

def get_sleep_score(sleep1, sleep2):
    """Calculates sleep schedule compatibility between two students."""
    if sleep1 == sleep2:
        return 100.0
    elif 'MODERATE' in (sleep1, sleep2):
        return 75.0
    else:
        # Early bird vs Night owl causes major conflict
        return 20.0

def get_cleanliness_score(clean1, clean2):
    """Cleanliness rating difference (scale 1 to 5)."""
    diff = abs(clean1 - clean2)
    return max(0.0, 100.0 - (diff * 25.0))

def get_noise_score(noise1, noise2):
    """Noise tolerance difference (scale 1 to 5)."""
    diff = abs(noise1 - noise2)
    return max(0.0, 100.0 - (diff * 25.0))

def get_study_score(study1, study2):
    """Checks study habit compatibility (SILENT, MODERATE, MUSIC)."""
    if study1 == study2:
        return 100.0
    elif 'MODERATE' in (study1, study2):
        return 75.0
    else:
        # SILENT vs MUSIC
        return 25.0

def get_diet_score(diet1, diet2):
    """Evaluates dietary preference compatibility."""
    if diet1 == diet2 or diet1 == 'ANY' or diet2 == 'ANY':
        return 100.0
    else:
        return 65.0

def get_rating_and_tier(match_percentage):
    """
    OVERALL RATING CALCULATION:
    Converts 0-100% compatibility into a 5.0-point rating scale, star display, and harmony tier.
    Uses universal ASCII formatting to prevent Windows cp1252 UnicodeEncodeError.
    """
    rating = round((match_percentage / 100.0) * 5.0, 1)
    for threshold, base_rating, stars, tier in RATING_TIERS:
        if match_percentage >= threshold:
            return rating, stars, tier
    return rating, "[*    ]", "LOW"

def calculate_compatibility(habits1_tuple, habits2_tuple):
    """
    TUPLE UNPACKING & MAPPING COMPUTATION:
    Unpacks habit tuples: (sleep, clean, noise, study, diet)
    Applies WEIGHT_MAPPING to compute final overall percentage (0-100%) and overall 5-star rating.
    """
    sleep1, clean1, noise1, study1, diet1 = habits1_tuple
    sleep2, clean2, noise2, study2, diet2 = habits2_tuple

    s_sleep = get_sleep_score(sleep1, sleep2)
    s_clean = get_cleanliness_score(clean1, clean2)
    s_noise = get_noise_score(noise1, noise2)
    s_study = get_study_score(study1, study2)
    s_diet = get_diet_score(diet1, diet2)

    # Use mapping weights to calculate weighted average
    overall = (
        (WEIGHT_MAPPING["sleep"] * s_sleep) +
        (WEIGHT_MAPPING["cleanliness"] * s_clean) +
        (WEIGHT_MAPPING["noise"] * s_noise) +
        (WEIGHT_MAPPING["study"] * s_study) +
        (WEIGHT_MAPPING["diet"] * s_diet)
    )

    overall_pct = round(overall, 2)
    rating, stars, tier = get_rating_and_tier(overall_pct)

    # Return a breakdown dictionary containing overall rating
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
    """
    SEARCHING, MAPPING, AND SORTING:
    1. Looks up target student in students_db dictionary.
    2. Filters candidate students by gender.
    3. Calculates compatibility scores and overall 5-star ratings.
    4. Packs results into tuples: (score, reg_no, name, dept, year, breakdown_dict)
    5. SORTS tuples in descending order using Python's built-in sorted().
    """
    reg_clean = target_reg_no.strip().upper()
    target_data = get_student(reg_clean)
    if not target_data:
        return []

    # Unpack target student tuples
    target_name, target_gender, target_dept, target_year = target_data["info"]
    target_habits = target_data["habits"]

    all_students = get_all_students()
    candidate_matches = []

    # Iterate through dictionary items
    for cand_reg, cand_data in all_students.items():
        if cand_reg == reg_clean:
            continue  # Exclude self

        cand_name, cand_gender, cand_dept, cand_year = cand_data["info"]
        cand_habits = cand_data["habits"]

        # Gender filtering
        if cand_gender != target_gender:
            continue

        # Compute compatibility and overall rating
        scores = calculate_compatibility(target_habits, cand_habits)

        # Pack into a result tuple: (score, reg_no, name, dept, year, scores)
        match_tuple = (scores["overall"], cand_reg, cand_name, cand_dept, cand_year, scores)
        candidate_matches.append(match_tuple)

    # SORTING: Sort candidates by match score (index 0 of tuple) descending
    sorted_matches = sorted(candidate_matches, key=lambda item: item[0], reverse=True)

    return sorted_matches[:top_n]
