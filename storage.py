# storage.py
# Real-time student data storage using Python Dictionaries, Tuples, and File I/O.
# Pure Python data structures - No SQL, No mock seed data. 100% Real-Time Operations.

import os
import json
from config import DATA_FILE

# In-memory dictionary: reg_no -> {"info": tuple, "habits": tuple}
students_db = {}

def ensure_loaded(filepath=DATA_FILE):
    """Ensures data is loaded into memory from the JSON file."""
    global students_db
    if not students_db and os.path.exists(filepath):
        load_from_file(filepath)

def save_to_file(filepath=DATA_FILE):
    """
    File Output: Persists real-time students_db dictionary to JSON file.
    Converts tuples to lists for JSON serialization.
    """
    global students_db
    serializable_data = {}
    for reg_no, data in students_db.items():
        serializable_data[reg_no] = {
            "info": list(data["info"]),
            "habits": list(data["habits"])
        }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable_data, f, indent=4)

def load_from_file(filepath=DATA_FILE):
    """
    File Input: Loads real-time student data from JSON file into memory.
    If file doesn't exist, starts with a completely empty dictionary {}.
    """
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
    """
    Real-Time Registration:
    Packs personal details into an immutable 'info' tuple and living habits into a 'habits' tuple.
    Inserts into students_db dictionary and saves directly to file.
    """
    global students_db
    ensure_loaded(filepath)
    reg_clean = reg_no.strip().upper()

    # Prevent duplicate registration
    if reg_clean in students_db:
        return False, f"Registration Number '{reg_clean}' is already registered."

    # Pack into immutable tuples
    info_tuple = (name.strip(), gender.strip().upper(), dept.strip().upper(), int(year))
    habits_tuple = (sleep_time.strip().upper(), int(clean), int(noise), study.strip().upper(), diet.strip().upper())

    # Map in dictionary
    students_db[reg_clean] = {
        "info": info_tuple,
        "habits": habits_tuple
    }

    # Save to file in real-time
    save_to_file(filepath)
    return True, f"Student '{reg_clean}' registered successfully in real-time."

def get_student(reg_no):
    """Dictionary Lookup: Retrieves a student's real-time record by Registration Number."""
    global students_db
    ensure_loaded()
    reg_clean = reg_no.strip().upper()
    return students_db.get(reg_clean)

def get_all_students():
    """Dictionary Items: Returns all real-time registered students."""
    global students_db
    ensure_loaded()
    return students_db

def clear_all_data(filepath=DATA_FILE):
    """Clears all stored student records."""
    global students_db
    students_db = {}
    save_to_file(filepath)
