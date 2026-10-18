import os
import sqlite3
from typing import Dict, List, Tuple

from matcher import calculate_compatibility

DB_FILE = os.path.join(os.path.dirname(__file__), "roommatch.db")


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS students (
    reg_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('M', 'F')),
    dept TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 5),
    sleep TEXT NOT NULL,
    cleanliness INTEGER NOT NULL CHECK (cleanliness BETWEEN 1 AND 5),
    noise INTEGER NOT NULL CHECK (noise BETWEEN 1 AND 5),
    study TEXT NOT NULL,
    diet TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS room_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT NOT NULL,
    reg_no TEXT NOT NULL UNIQUE,
    assigned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reg_no) REFERENCES students(reg_no) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_students_gender ON students(gender);
CREATE INDEX IF NOT EXISTS idx_students_dept ON students(dept);
CREATE INDEX IF NOT EXISTS idx_students_year ON students(year);
CREATE INDEX IF NOT EXISTS idx_room_assignments_room_no ON room_assignments(room_no);
"""


def _connect(db_path: str = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_FILE) -> None:
    with _connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)


def _row_to_student_dict(row: sqlite3.Row) -> Dict:
    return {
        "info": (row["name"], row["gender"], row["dept"], int(row["year"])),
        "habits": (
            row["sleep"],
            int(row["cleanliness"]),
            int(row["noise"]),
            row["study"],
            row["diet"],
        ),
    }


def add_student(
    reg_no: str,
    name: str,
    gender: str,
    dept: str,
    year: int,
    sleep: str,
    cleanliness: int,
    noise: int,
    study: str,
    diet: str,
    db_path: str = DB_FILE,
) -> Tuple[bool, str]:
    reg_no = reg_no.strip().upper()
    if not reg_no:
        return False, "Registration number cannot be empty."

    payload = (
        reg_no,
        name.strip(),
        gender.strip().upper(),
        dept.strip().upper() or "CSE",
        int(year),
        sleep.strip().upper(),
        int(cleanliness),
        int(noise),
        study.strip().upper(),
        diet.strip().upper(),
    )

    try:
        with _connect(db_path) as conn:
            conn.execute(
                """
                INSERT INTO students (reg_no, name, gender, dept, year, sleep, cleanliness, noise, study, diet)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                payload,
            )
        return True, f"Student '{reg_no}' registered successfully."
    except sqlite3.IntegrityError:
        return False, f"Registration number '{reg_no}' is already registered or data is invalid."


def get_student(reg_no: str, db_path: str = DB_FILE) -> Dict | None:
    reg_no = reg_no.strip().upper()
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM students WHERE reg_no = ?", (reg_no,)).fetchone()
    return _row_to_student_dict(row) if row else None


def list_students(
    page: int = 1,
    page_size: int = 20,
    query: str = "",
    db_path: str = DB_FILE,
) -> Tuple[List[sqlite3.Row], int]:
    safe_page = max(1, int(page))
    safe_page_size = max(1, min(100, int(page_size)))
    offset = (safe_page - 1) * safe_page_size

    where_sql = ""
    params: List = []
    if query.strip():
        where_sql = "WHERE reg_no LIKE ? OR name LIKE ? OR dept LIKE ?"
        q = f"%{query.strip()}%"
        params.extend([q, q, q])

    with _connect(db_path) as conn:
        total = conn.execute(f"SELECT COUNT(*) AS c FROM students {where_sql}", params).fetchone()["c"]
        rows = conn.execute(
            f"""
            SELECT reg_no, name, gender, dept, year, sleep, cleanliness, noise, study, diet
            FROM students
            {where_sql}
            ORDER BY created_at DESC, reg_no ASC
            LIMIT ? OFFSET ?
            """,
            [*params, safe_page_size, offset],
        ).fetchall()

    return rows, int(total)


def _get_all_students_dict(db_path: str = DB_FILE) -> Dict[str, Dict]:
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM students").fetchall()
    return {row["reg_no"]: _row_to_student_dict(row) for row in rows}


def find_top_roommates(target_reg_no: str, top_n: int = 5, db_path: str = DB_FILE):
    reg_clean = target_reg_no.strip().upper()
    all_students = _get_all_students_dict(db_path)
    target = all_students.get(reg_clean)
    if not target:
        return []

    target_habits = target["habits"]
    target_gender = target["info"][1]
    matches = []

    for reg_no, student in all_students.items():
        if reg_no == reg_clean:
            continue
        cand_name, cand_gender, cand_dept, cand_year = student["info"]
        if cand_gender != target_gender:
            continue

        scores = calculate_compatibility(target_habits, student["habits"])
        matches.append((scores["overall"], reg_no, cand_name, cand_dept, cand_year, scores))

    matches.sort(key=lambda item: item[0], reverse=True)
    return matches[:top_n]


def manual_assign_room(reg_no: str, room_no: str, db_path: str = DB_FILE) -> Tuple[bool, str]:
    reg_clean = reg_no.strip().upper()
    room = room_no.strip().upper()
    if not room:
        return False, "Room number cannot be empty."

    with _connect(db_path) as conn:
        student = conn.execute("SELECT reg_no FROM students WHERE reg_no = ?", (reg_clean,)).fetchone()
        if not student:
            return False, f"Student '{reg_clean}' not found."

        conn.execute("DELETE FROM room_assignments WHERE reg_no = ?", (reg_clean,))
        conn.execute(
            "INSERT INTO room_assignments (room_no, reg_no) VALUES (?, ?)",
            (room, reg_clean),
        )
    return True, f"Assigned {reg_clean} to room {room}."


def auto_assign_rooms(start_room: int = 101, db_path: str = DB_FILE) -> int:
    all_students = _get_all_students_dict(db_path)

    with _connect(db_path) as conn:
        assigned = {
            row["reg_no"]
            for row in conn.execute("SELECT reg_no FROM room_assignments").fetchall()
        }

    unassigned = {k: v for k, v in all_students.items() if k not in assigned}
    grouped = {"M": [], "F": []}
    for reg_no, student in unassigned.items():
        grouped[student["info"][1]].append((reg_no, student))

    room_counter = start_room
    new_assignments = 0

    with _connect(db_path) as conn:
        for gender in ("M", "F"):
            pool = grouped[gender]
            while len(pool) >= 2:
                reg_a, student_a = pool.pop(0)

                best_idx = 0
                best_score = -1.0
                for idx, (_, candidate) in enumerate(pool):
                    score = calculate_compatibility(student_a["habits"], candidate["habits"])["overall"]
                    if score > best_score:
                        best_score = score
                        best_idx = idx

                reg_b, _ = pool.pop(best_idx)
                room_no = f"R{room_counter}"
                conn.execute("INSERT INTO room_assignments (room_no, reg_no) VALUES (?, ?)", (room_no, reg_a))
                conn.execute("INSERT INTO room_assignments (room_no, reg_no) VALUES (?, ?)", (room_no, reg_b))
                room_counter += 1
                new_assignments += 2

            if pool:
                reg_single, _ = pool.pop(0)
                room_no = f"R{room_counter}"
                conn.execute("INSERT INTO room_assignments (room_no, reg_no) VALUES (?, ?)", (room_no, reg_single))
                room_counter += 1
                new_assignments += 1

    return new_assignments


def list_room_assignments(db_path: str = DB_FILE):
    with _connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT ra.room_no, s.reg_no, s.name, s.gender, s.dept, s.year
            FROM room_assignments ra
            JOIN students s ON s.reg_no = ra.reg_no
            ORDER BY ra.room_no ASC, s.gender ASC, s.reg_no ASC
            """
        ).fetchall()
    return rows


def clear_all(db_path: str = DB_FILE) -> None:
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM room_assignments")
        conn.execute("DELETE FROM students")
