# main.py
# RoomMatch: Real-Time Student Roommate Compatibility Match Predictor
# Built with pure Python: Dictionaries, Tuples, Mappings, Sorting, and File Input/Output.
# No SQL, No mock seed data. 100% Real-Time Operations with Overall 5-Star Ratings.

import sys
import argparse
from storage import load_from_file, add_student, get_student, get_all_students
from matcher import find_top_roommates
from config import SLEEP_MAP, STUDY_MAP, DIET_MAP

def show_banner():
    print("\n" + "=" * 76)
    print("      ROOMMATCH: REAL-TIME ROOMMATE COMPATIBILITY PREDICTOR     ")
    print("     Pure Python: Tuples, Dictionaries, Mappings & Sorting     ")
    print("=" * 76)

def register_student_and_match():
    """
    REAL-TIME REGISTRATION & MATCHING:
    Takes live student inputs, validates fields, packs them into tuples,
    saves directly to the real-time database, and instantly calculates predictions.
    """
    print("\n--- REAL-TIME STUDENT REGISTRATION ---")
    reg_no = input("Enter your VIT Registration Number (e.g., 26BCE10284): ").strip().upper()
    if not reg_no:
        print("[ERROR] Registration number cannot be empty.")
        return

    # Check if already registered
    if get_student(reg_no):
        print(f"[ERROR] Student with Registration Number '{reg_no}' is already registered!")
        return

    name = input("Enter your Full Name: ").strip()
    gender = input("Enter Gender (M/F): ").strip().upper()
    if gender not in ('M', 'F'):
        print("[ERROR] Gender must be 'M' or 'F'.")
        return

    dept = input("Enter Department (e.g., CSE, ECE, MECH): ").strip().upper()
    try:
        year = int(input("Enter Year of Study (1-5): ").strip())
    except ValueError:
        print("[ERROR] Year must be an integer between 1 and 5.")
        return

    print("\n--- ENTER YOUR LIVING HABITS & PREFERENCES ---")
    print("Sleep Schedule: [1] EARLY (Early Bird)  [2] MODERATE  [3] NIGHT (Night Owl)")
    sleep_choice = input("Choice (1-3) [default 2]: ").strip()
    sleep_time = SLEEP_MAP.get(sleep_choice, "MODERATE")

    clean = int(input("Cleanliness Expectation (1=Relaxed to 5=Spotless) [1-5]: ").strip() or "3")
    clean = max(1, min(5, clean))

    noise = int(input("Noise Tolerance (1=Dead Silent to 5=Music Allowed) [1-5]: ").strip() or "3")
    noise = max(1, min(5, noise))

    print("Study Environment: [1] SILENT  [2] MODERATE  [3] MUSIC")
    study_choice = input("Choice (1-3) [default 1]: ").strip()
    study_habit = STUDY_MAP.get(study_choice, "SILENT")

    print("Dietary Preference: [1] VEG  [2] NON_VEG  [3] ANY")
    diet_choice = input("Choice (1-3) [default 3]: ").strip()
    diet_pref = DIET_MAP.get(diet_choice, "ANY")

    # Save to real-time storage
    success, msg = add_student(reg_no, name, gender, dept, year, sleep_time, clean, noise, study_habit, diet_pref)
    if not success:
        print(f"\n[ERROR] {msg}")
        return

    print(f"\n[SUCCESS] {msg}")

    # Immediately display real-time prediction
    display_matches(reg_no)

def display_matches(reg_no):
    """
    REAL-TIME MATCH PREDICTIONS:
    Retrieves real-time candidate roommates of matching gender, sorts by compatibility,
    and displays matching percentage along with an Overall 5-Star Rating and Harmony Tier.
    """
    student = get_student(reg_no)
    if not student:
        print(f"\n[ERROR] No student with Registration Number '{reg_no}' found in the real-time database.")
        return

    name, gender, dept, year = student["info"]
    sleep, clean, noise, study, diet = student["habits"]

    print("\n" + "=" * 86)
    print(f"      REAL-TIME PREDICTIONS FOR [{reg_no}] {name}      ")
    print(f"      Dept: {dept} | Year: {year} | Habits: {sleep}, Clean: {clean}/5, Noise: {noise}/5")
    print("=" * 86)

    # find_top_roommates returns sorted list of tuples: (score, reg_no, name, dept, year, breakdown)
    sorted_matches = find_top_roommates(reg_no, top_n=5)

    if not sorted_matches:
        all_students = get_all_students()
        other_same_gender = [r for r, d in all_students.items() if r != reg_no and d["info"][1] == gender]
        if len(other_same_gender) == 0:
            print(f"\n[REAL-TIME STATUS] {name} is currently the only registered {gender} student.")
            print("Register additional students of the same gender to view real-time compatibility predictions!")
        else:
            print("\nNo eligible candidate roommates found.")
        return

    print(f"\n{'Rank':<4} | {'Reg No':<12} | {'Name':<18} | {'Dept':<8} | {'Match %':<8} | {'Overall Rating':<14} | {'Harmony Tier'}")
    print("-" * 86)
    for idx, match in enumerate(sorted_matches, 1):
        score, cand_reg, cand_name, cand_dept, cand_year, breakdown = match
        rating_str = f"{breakdown['rating']}/5.0 {breakdown['stars']}"
        print(f"#{idx:<3} | {cand_reg:<12} | {cand_name:<18} | {cand_dept:<8} | {score:<6.1f}% | {rating_str:<14} | {breakdown['tier']}")

def list_students():
    """
    REAL-TIME REGISTRY LISTING:
    Displays all students currently registered in the database.
    """
    all_students = get_all_students()
    total_count = len(all_students)

    print("\n--- REAL-TIME REGISTERED STUDENTS ---")
    if total_count == 0:
        print("Database is currently empty (0 students registered).")
        print("Select Option 1 from the main menu to register a student in real time.")
        return

    print(f"Total Registered Students: {total_count}")
    print(f"{'Reg No':<12} | {'Name':<18} | {'Sex':<3} | {'Dept':<8} | {'Year':<4} | {'Sleep':<8} | {'Clean':<5} | {'Noise':<5}")
    print("-" * 75)

    for reg_no, data in all_students.items():
        name, gender, dept, year = data["info"]
        sleep, clean, noise, study, diet = data["habits"]
        print(f"{reg_no:<12} | {name:<18} | {gender:<3} | {dept:<8} | {year:<4} | {sleep:<8} | {clean}/5   | {noise}/5")

def run_menu():
    show_banner()
    while True:
        print("\nMAIN MENU:")
        print("1. Register as a New Student (Input Reg No & Habits -> Real-Time Match)")
        print("2. View All Registered Students (Real-Time Live Registry)")
        print("3. Predict Roommates for a Registered Student")
        print("0. Exit")

        choice = input("\nSelect an option (0-3): ").strip()

        if choice == "1":
            register_student_and_match()
        elif choice == "2":
            list_students()
        elif choice == "3":
            reg = input("\nEnter Student Reg No (e.g. 26BCE10284): ").strip().upper()
            display_matches(reg)
        elif choice == "0":
            print("\nExiting RoomMatch. Have a good day!\n")
            sys.exit(0)
        else:
            print("Invalid choice, please select between 0 and 3.")

def main():
    parser = argparse.ArgumentParser(description="RoomMatch: Real-Time Roommate Compatibility Predictor")
    parser.add_argument("--register", action="store_true", help="Register a student interactively in real time")
    parser.add_argument("--list", action="store_true", help="List all currently registered students")
    parser.add_argument("--match", type=str, metavar="REG_NO", help="Predict real-time roommates for a Reg No (e.g. 26BCE10284)")

    args = parser.parse_args()

    # Load real-time data from file into memory
    load_from_file()

    if len(sys.argv) == 1:
        run_menu()
        return

    if args.register:
        register_student_and_match()
    elif args.list:
        list_students()
    elif args.match is not None:
        display_matches(args.match)

if __name__ == "__main__":
    main()
