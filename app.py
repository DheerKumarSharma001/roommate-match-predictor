from flask import Flask, render_template, request, redirect, url_for, flash

from dbms import (
    init_db,
    add_student,
    get_student,
    list_students,
    find_top_roommates,
    list_room_assignments,
    auto_assign_rooms,
    manual_assign_room,
)
from matcher import SLEEP_MAP, STUDY_MAP, DIET_MAP

app = Flask(__name__)
app.secret_key = "roommatch-dev-secret"

init_db()


def _parse_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def index():
    page = _parse_int(request.args.get("page", 1), 1)
    query = request.args.get("q", "")
    page_size = 20

    students, total = list_students(page=page, page_size=page_size, query=query)
    total_pages = max(1, (total + page_size - 1) // page_size)
    return render_template(
        "index.html",
        students=students,
        total=total,
        page=page,
        total_pages=total_pages,
        query=query,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success, msg = add_student(
            reg_no=request.form.get("reg_no", ""),
            name=request.form.get("name", ""),
            gender=request.form.get("gender", ""),
            dept=request.form.get("dept", "CSE"),
            year=_parse_int(request.form.get("year", 1), 1),
            sleep=SLEEP_MAP.get(request.form.get("sleep", "2"), "MODERATE"),
            cleanliness=_parse_int(request.form.get("cleanliness", 3), 3),
            noise=_parse_int(request.form.get("noise", 3), 3),
            study=STUDY_MAP.get(request.form.get("study", "1"), "SILENT"),
            diet=DIET_MAP.get(request.form.get("diet", "3"), "ANY"),
        )
        flash(msg, "success" if success else "error")
        if success:
            return redirect(url_for("matches", reg_no=request.form.get("reg_no", "").strip().upper()))

    return render_template("register.html")


@app.route("/matches/<reg_no>")
def matches(reg_no):
    student = get_student(reg_no)
    if not student:
        flash(f"Student '{reg_no}' not found.", "error")
        return redirect(url_for("index"))

    matches_data = find_top_roommates(reg_no, top_n=10)
    return render_template(
        "matches.html",
        reg_no=reg_no,
        student=student,
        matches=matches_data,
    )


@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "auto_assign":
            count = auto_assign_rooms()
            flash(f"Auto-assigned {count} students to rooms.", "success")
        elif action == "manual_assign":
            success, msg = manual_assign_room(
                reg_no=request.form.get("reg_no", ""),
                room_no=request.form.get("room_no", ""),
            )
            flash(msg, "success" if success else "error")

        return redirect(url_for("rooms"))

    assignments = list_room_assignments()
    return render_template("rooms.html", assignments=assignments)


if __name__ == "__main__":
    app.run()
