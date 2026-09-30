# main.py
# RoomMatch: Hostel Roommate Compatibility Matcher
# Interactive menu-driven console interface

from matcher import (
    load_from_file,
    add_student,
    get_student,
    get_all_students,
    find_top_roommates,
    SLEEP_MAP,
    STUDY_MAP,
    DIET_MAP
)

def show_banner():
    print("\n" + "=" * 70)
    print("         RoomMatch: Student Roommate Compatibility Matcher")
    print("=" * 70)

def prompt_range(prompt_text, min_val, max_val, default):
    """Helper to cleanly read an integer in range without crashing on invalid input."""
    raw = input(f"{prompt_text} [{min_val}-{max_val}, default {default}]: ").strip()
    if not raw:
        return default
    try:
        val = int(raw)
        return max(min_val, min(max_val, val))
    except ValueError:
        return default

def register_student_and_match():
    """Takes input for a new student, saves it, and shows potential matches."""
    print("\n--- Student Registration ---")
    reg_no = input("Enter Registration Number (e.g., 26BCE10284): ").strip().upper()
    if not reg_no:
        print("Registration number cannot be empty.")
        return

    # Check for existing student
    if get_student(reg_no):
        print(f"Student with Reg No '{reg_no}' is already registered!")
        return

    name = input("Enter Full Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    # Keep prompting if they make a typo instead of kicking them out
    while True:
        gender = input("Enter Gender (M/F): ").strip().upper()
        if gender in ('M', 'F'):
            break
        print("Invalid input. Please enter 'M' or 'F'.")

    dept = input("Enter Department (e.g., CSE, ECE, MECH): ").strip().upper() or "CSE"
    year = prompt_range("Enter Year of Study", 1, 5, default=1)

    print("\n--- Living Habits & Preferences ---")
    print("Sleep Schedule: [1] Early Bird  [2] Moderate  [3] Night Owl")
    sleep_choice = input("Your choice (1-3) [default 2]: ").strip()
    sleep_time = SLEEP_MAP.get(sleep_choice, "MODERATE")

    clean = prompt_range("Cleanliness (1=Relaxed to 5=Spotless)", 1, 5, default=3)
    noise = prompt_range("Noise Tolerance (1=Quiet to 5=Music Allowed)", 1, 5, default=3)

    print("Study Environment: [1] Silent  [2] Moderate  [3] Background Music")
    study_choice = input("Your choice (1-3) [default 1]: ").strip()
    study_habit = STUDY_MAP.get(study_choice, "SILENT")

    print("Dietary Preference: [1] Vegetarian  [2] Non-Veg  [3] Any/Flexible")
    diet_choice = input("Your choice (1-3) [default 3]: ").strip()
    diet_pref = DIET_MAP.get(diet_choice, "ANY")

    # Save to database
    success, msg = add_student(reg_no, name, gender, dept, year, sleep_time, clean, noise, study_habit, diet_pref)
    if not success:
        print(f"\nError: {msg}")
        return

    print(f"\n{msg}")

    # Immediately show matches
    display_matches(reg_no)

def display_matches(reg_no):
    """Finds and displays the most compatible roommates for a student."""
    student = get_student(reg_no)
    if not student:
        print(f"\nNo student found with Registration Number '{reg_no}'.")
        return

    name, gender, dept, year = student["info"]
    sleep, clean, noise, study, diet = student["habits"]

    gender_label = "Male" if gender == "M" else "Female"
    print("\n" + "=" * 80)
    print(f" Compatible Roommate Matches for: {name} ({reg_no})")
    print(f" Profile: {dept}, Year {year} | Sleep: {sleep} | Cleanliness: {clean}/5 | Noise: {noise}/5")
    print("=" * 80)

    sorted_matches = find_top_roommates(reg_no, top_n=5)

    if not sorted_matches:
        all_students = get_all_students()
        other_same_gender = [r for r, d in all_students.items() if r != reg_no and d["info"][1] == gender]
        if len(other_same_gender) == 0:
            print(f"\nNotice: {name} is currently the only registered {gender_label} student.")
            print("As more students register, compatible matches will appear here automatically.")
        else:
            print("\nNo eligible matches found at this time.")
        return

    print(f"\n{'Rank':<4} | {'Reg No':<12} | {'Name':<18} | {'Dept':<8} | {'Match %':<8} | {'Rating':<14} | {'Compatibility'}")
    print("-" * 80)
    for idx, match in enumerate(sorted_matches, 1):
        score, cand_reg, cand_name, cand_dept, cand_year, breakdown = match
        rating_str = f"{breakdown['rating']}/5.0 {breakdown['stars']}"
        print(f"#{idx:<3} | {cand_reg:<12} | {cand_name:<18} | {cand_dept:<8} | {score:<6.1f}% | {rating_str:<14} | {breakdown['tier']}")

def list_students():
    """Prints all registered students with full profile habits."""
    all_students = get_all_students()
    total_count = len(all_students)

    print("\n--- Registered Students ---")
    if total_count == 0:
        print("Database is currently empty (0 students registered).")
        print("Choose Option 1 from the menu to register a student!")
        return

    print(f"Total Registered Students: {total_count}")
    print(f"{'Reg No':<12} | {'Name':<16} | {'Gender':<6} | {'Dept':<6} | {'Yr':<2} | {'Sleep':<8} | {'Clean':<5} | {'Noise':<5} | {'Study':<8} | {'Diet'}")
    print("-" * 92)

    for reg_no, data in all_students.items():
        name, gender, dept, year = data["info"]
        sleep, clean, noise, study, diet = data["habits"]
        print(f"{reg_no:<12} | {name:<16} | {gender:<6} | {dept:<6} | {year:<2} | {sleep:<8} | {clean}/5   | {noise}/5   | {study:<8} | {diet}")

def run_menu():
    show_banner()
    while True:
        print("\n--- MENU ---")
        print("1. Register new student & view matches")
        print("2. View all registered students")
        print("3. Find roommate matches for an existing student")
        print("0. Exit")

        choice = input("\nEnter your choice (0-3): ").strip()

        if choice == "1":
            register_student_and_match()
        elif choice == "2":
            list_students()
        elif choice == "3":
            reg = input("\nEnter Registration Number: ").strip().upper()
            display_matches(reg)
        elif choice == "0":
            print("\nThanks for using RoomMatch. Goodbye!\n")
            break
        else:
            print("Invalid choice, please enter 0, 1, 2, or 3.")

def main():
    load_from_file()
    run_menu()

if __name__ == "__main__":
    main()
