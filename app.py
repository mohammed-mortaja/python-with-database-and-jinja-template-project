import json
import mariadb
import datetime
from datetime import timedelta

conn = mariadb.connect(
    user="gsg",
    password="gogo",
    host="localhost",
    database="sutdents")

cursor = conn.cursor()


def reg_student():
    while True:
        student_name = str(input("Enter Student Name: "))
        if student_name.strip() == "":
            print("Error: Student name cannot be empty.")
        else:
                cursor.execute(f"SELECT student_id FROM students WHERE student_name = '{student_name}'")
                student = cursor.fetchone()
                cursor.execute(f"INSERT INTO students (student_name) VALUES ('{student_name}')")
                conn.commit()
                print("student_name is added ")
                break
    while True:

        age = int(input("Enter Student Birdth Date: "))


        if age > 0 :
            cursor.execute(f"UPDATE students SET age = {age} WHERE student_name = '{student_name}'")
            conn.commit()
            print("student_date is added ")
            break
    while True:
        cursor.execute("SELECT level_name FROM levels")
        levels = cursor.fetchall()
        print("Available course levels:")
        for i, level in enumerate(levels):
            print(f"{i + 1}. {level[0]}")
        level = input("Please select a course level: ")
        l = f"levels: {levels}"
        if level not in f"levels: {levels}":
            print("Invalid course level. Please try again.")
        else:
            cursor.execute(f"SELECT level_id FROM levels WHERE level_name = '{level}'")
            level_id = cursor.fetchone()[0]
            print(f"Selected level ID: {level_id}")
            cursor.execute(f"UPDATE students SET level_id = {level_id} WHERE student_name = '{student_name}'")
            conn.commit()
            print("Successfully updated the student's level.")

            break


    while True:
        mobile_number = input("Enter Student Mobile Number: ")
        if mobile_number.strip() != "":
            cursor.execute(f"INSERT INTO contacts (mobile_number) VALUES ('{mobile_number}')")
            cursor.execute(f"SELECT contact_id FROM contacts WHERE mobile_number = '{mobile_number}'")
            contact_id = cursor.fetchone()[0]
            conn.commit()
            cursor.execute(f"UPDATE students SET contact_id = {contact_id} WHERE student_name = '{student_name}'")
            conn.commit()
            print("mobile_number is added ")
            break

    while True:
        email = input("Enter Student Email: ")
        if email.strip() != "":
            cursor.execute(f"UPDATE contacts SET email = '{email}' WHERE contact_id = {contact_id}")
            conn.commit()
            print("email is added ")
            break

def enroll_course():
    # طلب id الطالب
    student_id = input("Enter student ID: ")
    # طلب id الكورس
    course_id = input("Enter course ID: ")
    # التحقق من أن مستوى الكورس متساوي مع مستوى الطالب الحالي
    cursor.execute(f"SELECT level_id FROM students WHERE student_id = {student_id}")
    student_level = cursor.fetchone()[0]
    cursor.execute(f"SELECT level_id FROM courses WHERE course_id = {course_id}")
    course_level = cursor.fetchone()[0]
    if student_level != course_level:
        print("Error: Course level does not match student level.")
    else:
        print("Course level is match student level.")

    # التحقق من أن الطالب لم يسجل في الكورس من قبل
    cursor.execute(f"SELECT * FROM enrollment_histories WHERE student_id = {student_id} AND course_id = {course_id}")
    enrollment = cursor.fetchone()
    if enrollment is not None:
        print("Error: Student is already enrolled in this course.")
        return

    # التحقق من أن الكورس ليس ممتلئًا
    cursor.execute(f"SELECT max_capacity FROM courses WHERE course_id = {course_id}")
    capacity = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM enrollment_histories WHERE course_id = {course_id}")
    num_enrollments = cursor.fetchone()[0]
    if num_enrollments >= capacity:
        print("Error: Course is full.")
        return
    # التسجيل في الكورس
    cursor.execute(f"INSERT INTO enrollment_histories (student_id, course_id) VALUES ({student_id}, {course_id})")
    conn.commit()
    print("Successfully enrolled in course.")

def create_new_course():

    while True:
        course_id = input("Enter Course Id (Course Code)  OF This Course: ")
        cursor.execute(f"INSERT INTO courses (course_id) VALUES ({course_id})")
        conn.commit()
        print(" Course Id Is Added.")


        course_name = str(input("Enter Course Name  OF This Course : "))

        cursor.execute(f"UPDATE courses SET course_name = '{course_name}' WHERE course_id = {course_id}")
        conn.commit()
        print("course name is added ")

        max_capacity = int(input("Enter Max Capacity  OF This Course : "))
        cursor.execute(f"UPDATE courses SET max_capacity = {max_capacity} WHERE course_id = {course_id}")
        conn.commit()
        print("max capacity is added ")

        rate_per_hour = float(input("Enter Rate Per Hour OF This Course : "))
        cursor.execute(f"UPDATE courses SET rate_per_hour = {rate_per_hour} WHERE course_id = {course_id}")
        conn.commit()
        print("Hour Rate (Price)  is added ")

        cursor.execute("SELECT level_name FROM levels")
        levels = cursor.fetchall()
        print("Available course levels:")
        for i, level in enumerate(levels):
            print(f"{i + 1}. {level[0]}")
        level = input("Please select a course level: ")
        l = f"levels: {levels}"
        if level not in f"levels: {levels}":
            print("Invalid course level. Please try again.")
        else:
            cursor.execute(f"SELECT level_id FROM levels WHERE level_name = '{level}'")
            level_id = cursor.fetchone()[0]
            print(f"Selected level ID: {level_id}")
            cursor.execute(f"UPDATE courses SET level_id = {level_id} WHERE course_id = {course_id}")
            conn.commit()
            print("Successfully register the course's level.")

        break


def create_course_schedule():
    day = input("Enter the day of the week: ")

    course_id = input("Enter the course id: ")
    start_time = input("Enter the start time: ")
    duration = input("Enter the duration: ")

    end_time = start_time + duration

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course_schedules WHERE day=%s AND start_time<=%s AND duration + start_time>%s",
                   (day, start_time, end_time))
    conflicts = cursor.fetchall()

    if conflicts:
        print("There is a conflict in the schedule")
    else:
        cursor.execute("INSERT INTO course_schedules (course_id, day, start_time, duration) VALUES (%s, %s, %s, %s)",
                       (course_id, day, start_time, duration))
        conn.commit()
        print("Course added to schedule")

def display_student_schedule():
    student_id = input("Enter the student id: ")

    cursor = conn.cursor()
    cursor.execute("SELECT course_id FROM enrollment_histories WHERE student_id=%s", (student_id,))
    all_courses = cursor.fetchall()

    courses = []
    for cour in all_courses:

        cursor.execute("SELECT * FROM course_schedules WHERE course_id=%s", (cour[0],))
        courses.append(cursor.fetchone())

    print("Student Schedule:")
    for course in courses:
        print(f"Course: {course[1]}, Day: {course[2]}, Duration: {course[3]}, Start Time: {course[4]}")


while (True):
    x = int(input("1.Register New Student\n"
                  "2.Enroll Course\n"
                  "3.Create New Course\n"
                  "4.Create New Schedule\n"
                  "5.Display Student Courses Schedule\n"
                  "6.Exit"))

    if x == 1:
        reg_student()
    elif x == 2:
        enroll_course()
    elif x == 3:
        create_new_course()

    elif x == 4:
        create_course_schedule()

    elif x == 5:
        display_student_schedule()

    else:
        exit()
        pass

