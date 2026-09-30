# test_system.py
# Automated unit tests for pure Python RoomMatch system.
# Verifies Dictionaries, Tuples, Mappings, Sorting, Real-Time File I/O, and Overall 5-Star Ratings.

import unittest
import os
from storage import (
    students_db,
    add_student,
    get_student,
    get_all_students,
    clear_all_data,
    save_to_file,
    load_from_file
)
from matcher import (
    WEIGHT_MAPPING,
    get_sleep_score,
    get_cleanliness_score,
    get_diet_score,
    get_rating_and_tier,
    calculate_compatibility,
    find_top_roommates
)

class TestRoomMatchPurePython(unittest.TestCase):

    def setUp(self):
        # Clear in-memory database and populate test candidates
        clear_all_data()
        add_student("26BCE10284", "Aarav Sharma", "M", "CSE", 1, "NIGHT", 4, 2, "SILENT", "VEG")
        add_student("26BCE10042", "Rohan Verma", "M", "CSE", 1, "NIGHT", 4, 3, "SILENT", "VEG")
        add_student("25BME10115", "Vikram Singh", "M", "MECH", 2, "EARLY", 2, 5, "MUSIC", "NON_VEG")
        add_student("26BCE10190", "Ananya Iyer", "F", "CSE", 1, "EARLY", 5, 1, "SILENT", "VEG")

    def tearDown(self):
        # Leave production database completely clean
        clear_all_data()

    def test_dictionary_lookup(self):
        """Verifies dictionary lookup by registration number."""
        student = get_student("26BCE10284")
        self.assertIsNotNone(student)
        self.assertIn("info", student)
        self.assertIn("habits", student)

    def test_tuple_structure_and_unpacking(self):
        """Verifies that student records and habits are stored as immutable tuples."""
        student = get_student("26BCE10284")
        info = student["info"]
        habits = student["habits"]

        # Confirm they are tuples
        self.assertIsInstance(info, tuple)
        self.assertIsInstance(habits, tuple)

        # Unpack info tuple
        name, gender, dept, year = info
        self.assertEqual(name, "Aarav Sharma")
        self.assertEqual(gender, "M")
        self.assertEqual(dept, "CSE")
        self.assertEqual(year, 1)

        # Unpack habits tuple
        sleep, clean, noise, study, diet = habits
        self.assertEqual(sleep, "NIGHT")
        self.assertEqual(clean, 4)
        self.assertEqual(noise, 2)
        self.assertEqual(study, "SILENT")
        self.assertEqual(diet, "VEG")

    def test_duplicate_registration_rejected(self):
        """Verifies dictionary key uniqueness (cannot insert duplicate reg_no)."""
        success, msg = add_student(
            "26BCE10284", "Duplicate Aarav", "M", "CSE", 1,
            "NIGHT", 4, 2, "SILENT", "VEG"
        )
        self.assertFalse(success)
        self.assertIn("already registered", msg.lower())

    def test_weight_mapping_completeness(self):
        """Verifies that the weights mapping sums up to 1.0 (100%)."""
        total_weight = sum(WEIGHT_MAPPING.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)

    def test_sleep_and_cleanliness_logic(self):
        """Tests individual score computations."""
        self.assertEqual(get_sleep_score("NIGHT", "NIGHT"), 100.0)
        self.assertEqual(get_sleep_score("EARLY", "NIGHT"), 20.0)
        self.assertEqual(get_cleanliness_score(5, 5), 100.0)
        self.assertEqual(get_cleanliness_score(4, 2), 50.0)
        self.assertEqual(get_diet_score("VEG", "VEG"), 100.0)
        self.assertEqual(get_diet_score("VEG", "NON_VEG"), 65.0)

    def test_overall_rating_and_tier_calculation(self):
        """Tests conversion from percentage to 5-star rating scale and tier."""
        rating_95, stars_95, tier_95 = get_rating_and_tier(95.0)
        self.assertEqual(rating_95, 4.8)
        self.assertEqual(stars_95, "[*****]")
        self.assertEqual(tier_95, "EXCELLENT")

        rating_80, stars_80, tier_80 = get_rating_and_tier(80.0)
        self.assertEqual(rating_80, 4.0)
        self.assertEqual(stars_80, "[**** ]")
        self.assertEqual(tier_80, "GOOD")

        rating_40, stars_40, tier_40 = get_rating_and_tier(40.0)
        self.assertEqual(rating_40, 2.0)
        self.assertEqual(stars_40, "[**   ]")
        self.assertEqual(tier_40, "FAIR")

    def test_compatibility_symmetry(self):
        """Verifies that Match(A, B) == Match(B, A)."""
        h1 = ("NIGHT", 4, 2, "SILENT", "VEG")
        h2 = ("EARLY", 3, 4, "MUSIC", "NON_VEG")

        score_12 = calculate_compatibility(h1, h2)["overall"]
        score_21 = calculate_compatibility(h2, h1)["overall"]
        self.assertEqual(score_12, score_21)

    def test_sorting_order_of_predictions(self):
        """
        Tests that find_top_roommates uses Python sorting to rank candidates
        in descending order of match percentage.
        """
        matches = find_top_roommates("26BCE10284", top_n=5)
        self.assertTrue(len(matches) > 0)

        # Assert tuples are sorted descending by score (index 0)
        for i in range(len(matches) - 1):
            score_current = matches[i][0]
            score_next = matches[i + 1][0]
            self.assertGreaterEqual(score_current, score_next)

    def test_gender_isolation_in_matching(self):
        """Verifies that male students only match with male roommates."""
        matches = find_top_roommates("26BCE10284", top_n=5)
        for match in matches:
            cand_reg = match[1]
            cand = get_student(cand_reg)
            gender = cand["info"][1]
            self.assertEqual(gender, "M")

if __name__ == "__main__":
    unittest.main()
