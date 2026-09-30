# config.py
# Centralized configuration, weight mappings, and rating definitions for RoomMatch.
# Demonstrates Python Mappings and separation of configuration from logic.

import os

# Base directory and file storage path
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "students_data.json")

# 1. MAPPING: Lifestyle dimension weights for compatibility scoring (sums to 1.0 / 100%)
WEIGHT_MAPPING = {
    "sleep": 0.30,        # 30% weight for sleep cycle synchronization
    "cleanliness": 0.25,  # 25% weight for hygiene and cleanliness standards
    "noise": 0.20,        # 20% weight for noise tolerance and music preference
    "study": 0.15,        # 15% weight for study habits (silent vs music vs group)
    "diet": 0.10          # 10% weight for dietary compatibility
}

# 2. MAPPINGS: Menu choice mappings for user input validation
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

# 3. MAPPING: Rating thresholds, ASCII star indicators, and verbal Harmony Tiers
# Uses universal ASCII brackets [*****] to ensure cross-platform console safety.
RATING_TIERS = [
    (90.0, 5.0, "[*****]", "EXCELLENT"),
    (75.0, 4.0, "[**** ]", "GOOD"),
    (50.0, 3.0, "[***  ]", "MODERATE"),
    (35.0, 2.0, "[**   ]", "FAIR"),
    (0.0,  1.0, "[*    ]", "LOW")
]
