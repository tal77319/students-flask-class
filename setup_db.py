import sqlite3
import faker
import random


def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


def create_tables():
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL, 
            role TEXT NOT NULL
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students_courses (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE(student_id, course_id)
        )
    """)


def create_fake_data(students_num=40, teachers_num=4):
    fake = faker.Faker()
    for student in range(students_num):
        execute_query(
            f"INSERT INTO students (name, email) VALUES ('{fake.name()}','{fake.email()}')")
    for teacher in range(teachers_num):
        execute_query(
            f"INSERT INTO teachers (name, email) VALUES ('{fake.name()}','{fake.email()}')")
    courses = ['python', 'java', 'html', 'css', 'javascript']
    for course_name in courses:
        teacher_ids = [tup[0]
                       for tup in execute_query("SELECT id FROM teachers")]
        execute_query(
            f"INSERT INTO courses (name, teacher_id) VALUES ('{course_name}', '{random.choice(teacher_ids)}')")
    execute_query("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
    execute_query("INSERT INTO users (username, password, role) VALUES ('tal', 'tal', 'student')")

if __name__ == "__main__":
    print(__name__)
    create_tables()
    create_fake_data()
