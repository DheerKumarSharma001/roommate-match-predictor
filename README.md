# 🏠 RoomMatch UI + DBMS Edition

RoomMatch is now a **web UI application** with **SQLite DBMS-backed storage** for handling larger student datasets and room assignment workflows.

## ✅ What's new

- Migrated from terminal-only CLI flow to a Flask-powered UI.
- Added SQLite schema with indexed student records.
- Added scalable student listing with search + pagination.
- Added roommate match pages powered by the existing compatibility engine.
- Added room management features:
  - automatic room assignment
  - manual room assignment
- Kept core matching math and existing compatibility tests.

## 📁 Project Structure

```text
roommate-match-predictor/
├── app.py                  # Flask UI routes and controllers
├── dbms.py                 # SQLite schema + data/room assignment operations
├── matcher.py              # Matching and scoring logic (NumPy based)
├── templates/              # HTML templates for UI pages
├── main.py                 # App entrypoint
├── test_system.py          # Existing compatibility logic tests
├── test_dbms.py            # New DBMS and assignment feature tests
├── roommatch.db            # SQLite DB (auto-created at runtime)
└── requirements.txt
```

## 🚀 Run the UI

```bash
pip install -r requirements.txt
python main.py
```

Then open: `http://127.0.0.1:5000`

## 🧪 Run tests

```bash
python -m unittest test_system.py test_dbms.py
```

## 🗄️ DBMS Highlights

- `students` table for profile + habit data.
- `room_assignments` table for room allocation.
- Indexes on `gender`, `dept`, `year`, and `room_no`.
- Query-level pagination (`LIMIT/OFFSET`) for large datasets.

