import os
import tempfile
import unittest

import dbms


class TestDbmsFeatures(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        dbms.init_db(self.db_path)

        dbms.add_student("26BCE10001", "A", "M", "CSE", 2, "EARLY", 4, 3, "SILENT", "VEG", self.db_path)
        dbms.add_student("26BCE10002", "B", "M", "CSE", 2, "EARLY", 4, 3, "SILENT", "VEG", self.db_path)
        dbms.add_student("26BCE10003", "C", "F", "ECE", 3, "NIGHT", 2, 4, "MUSIC", "NON_VEG", self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_student_pagination(self):
        rows, total = dbms.list_students(page=1, page_size=2, query="", db_path=self.db_path)
        self.assertEqual(total, 3)
        self.assertEqual(len(rows), 2)

    def test_roommate_matches(self):
        matches = dbms.find_top_roommates("26BCE10001", top_n=5, db_path=self.db_path)
        self.assertTrue(matches)
        self.assertEqual(matches[0][1], "26BCE10002")

    def test_room_assignment(self):
        count = dbms.auto_assign_rooms(db_path=self.db_path)
        self.assertEqual(count, 3)
        assignments = dbms.list_room_assignments(self.db_path)
        self.assertEqual(len(assignments), 3)


if __name__ == "__main__":
    unittest.main()
