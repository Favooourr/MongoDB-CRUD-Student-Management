
import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError("MONGO_URI is missing from .env")

client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=10000
)

db = client["student_management"]
students = db["students"]

@app.route("/")
def home():
    return "Welcome to Student Management System!"

from flask import request, redirect, url_for

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()
        age_text = request.form.get("age", "").strip()

        if not name or not course or not age_text.isdigit():
            return "Please enter valid student details.", 400

        age = int(age_text)

        students.insert_one({
            "name": name,
            "course": course,
            "age": age
        })

        return redirect(url_for("add_student"))

    return """
    <h2>Add New Student</h2>
    <form method="POST">
        <label>Student Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Course:</label><br>
        <input type="text" name="course" required><br><br>

        <label>Age:</label><br>
        <input type="number" name="age"
               min="1" required><br><br>

        <button type="submit">Add Student</button>
    </form>
    """

from markupsafe import escape

@app.route("/students")
def view_students():
    all_students = students.find()

    html = "<h2>Student Records</h2>"
    html += "<a href='/add'>Add New Student</a>"
    html += "<hr>"

    for student in all_students:
        html += f"""
        <p>
            <b>Name:</b> {escape(student['name'])}<br>
            <b>Course:</b> {escape(student['course'])}<br>
            <b>Age:</b> {escape(str(student['age']))}

<a href="/edit/{student['_id']}">Edit Student</a>

<form method="POST" action="/delete/{student['_id']}">
    <button type="submit">Delete Student</button>
</form>

        </p>
        <hr>
        """

    return html

from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import abort
from markupsafe import escape

@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    try:
        student = students.find_one({
            "_id": ObjectId(student_id)
        })
    except InvalidId:
        abort(404)

    if student is None:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()
        age_text = request.form.get("age", "").strip()

        if not name or not course or not age_text.isdigit():
            return "Please enter valid details.", 400

        students.update_one(
            {"_id": student["_id"]},
            {"$set": {
                "name": name,
                "course": course,
                "age": int(age_text)
            }}
        )

        return redirect(url_for("view_students"))

    return f"""
    <h2>Edit Student</h2>
    <form method="POST">
        <label>Name:</label><br>
        <input name="name"
               value="{escape(student['name'])}"
               required><br><br>

        <label>Course:</label><br>
        <input name="course"
               value="{escape(student['course'])}"
               required><br><br>

        <label>Age:</label><br>
        <input type="number" name="age"
               min="1"
               value="{escape(str(student['age']))}"
               required><br><br>

        <button type="submit">Save Changes</button>
    </form>
    """

@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        student_object_id = ObjectId(student_id)
    except InvalidId:
        abort(404)

    result = students.delete_one({
        "_id": student_object_id
    })

    if result.deleted_count == 0:
        abort(404)

    return redirect(url_for("view_students"))

if __name__ == "__main__":
    client.admin.command("ping")
    app.run(debug=True)
