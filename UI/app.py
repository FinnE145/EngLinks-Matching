from flask import Flask, flash, redirect, render_template, request, url_for

from data_utilities import load_shelve, next_id, shelve_data
from CoreAlg.matching import match

def create_app(tutor_data: dict | None = None, student_data: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"
    app.config["TUTOR_DATA"] = tutor_data if tutor_data is not None else (load_shelve("Data/tutor_data.shelve") or {})
    app.config["STUDENT_DATA"] = student_data if student_data is not None else (load_shelve("Data/student_data.shelve") or {})

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/new-student")
    def new_student():
        return render_template("input.html")

    @app.route("/view-matches")
    def view_matches():
        return render_template("matches.html")

    @app.route("/submit-student", methods=["POST"])
    def submit_student():
        name = request.form.get("name")
        raw_courses = request.form.get("courses")
        availability = request.form.getlist("availability")

        err = False
        
        try:
            courses = [course.strip().upper() for course in raw_courses.split(",")]
            if len(courses) < 1:
                flash("Please enter at least one course.", "error")
                err = True
        except AttributeError:
            flash("Invalid courses input. Please enter a comma-separated list of courses.", "error")
            err = True

        try:
            availability = [int(i) for i in availability]
            if len(availability) < 1:
                flash("Please select at least one availability slot.", "error")
                err = True
            if any(i < 0 or i > 6 for i in availability):
                raise ValueError
        except ValueError:
            flash("Invalid availability selection.", "error")
            err = True

        if not name or not courses or not availability:
            flash("Please fill out all fields.", "error")
            err = True

        if err:
            return render_template("input.html", name=name, courses=raw_courses, availability=availability)

        student_data = app.config["STUDENT_DATA"]
        student_id = next_id(student_data)
        student_data[student_id] = {
            "name": name,
            "courses": courses,
            "availability": availability,
            "tutor": None,
        }

        student_data[student_id]["tutor"] = match(student_data[student_id], app.config["TUTOR_DATA"])

        shelve_data(student_data, "Data/student_data.shelve")
        flash("Student submitted successfully.", "success")
        return redirect(url_for("view_matches"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)