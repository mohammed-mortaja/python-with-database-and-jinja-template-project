import mariadb
import jinja2
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template , request, jsonify

# Connect to the database
conn = mariadb.connect(
    user="gsg",
    password="gogo",
    host="localhost",
    database="sutdents"
)

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/courses")
def course():
    # Retrieve all courses from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    # Render the courses template
    return render_template("show_courses.html", courses=courses)

@app.route("/students")
def student():
    # Retrieve all courses from the database
    cursor = conn.cursor()
    query = """ 
    SELECT s.*, c.mobile_number, c.email
    FROM students AS s
    JOIN contacts AS c
    ON s.student_id = c.contact_id
    """
    cursor.execute(query)
    students = cursor.fetchall()

    # Render the courses template
    return render_template("show_students.html", students=students)


@app.route("/course_schedules")
def Course_Schedule():
    # Retrieve all courses from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course_schedules")
    c_schedules = cursor.fetchall()

    # Render the courses template
    return render_template("show_courses_schedules.html", c_schedules=c_schedules)

@app.route("/api/student_details", methods=["GET"])
def student_details():
    api_key = request.args.get("api_key")
    if api_key != api_key:
        return "Invalid API key", 401

    # Retrieve the student id
    student_id = request.args.get("student_id")

    # Retrieve the student details from the database
    cursor = conn.cursor()
    query = """ 
    SELECT s.*, c.mobile_number, c.email
    FROM students AS s
    JOIN contacts AS c
    ON s.student_id = c.contact_id WHERE s.student_id=%s"""
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()

    if student:
        return jsonify({"student id": student[0], "name": student[1], "contact id": student[2] ,
                        " Level id": student[3] , " age": student[4] , " mobile": student[5] ," email": student[6] })
    else:
        return "Student not found", 404

@app.route("/api/students", methods=["GET"])
def get_students():
    api_key = request.args.get("api_key")
    if api_key != api_key:
        return "Invalid API key", 401

    # Retrieve all students from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Return the list of students as a JSON response
    return jsonify(students)


app.run(debug=True)