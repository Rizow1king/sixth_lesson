import psycopg2

class DatabaseManager:
    def __init__(self):
        self.database = psycopg2.connect(
            dbname="test",
            user="postgres",
            host="localhost",
            password="1"
        )

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                result = None
                if commit:
                    db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                return result

    def create_tables(self):
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS students(
                student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                student_age INTEGER CHECK(student_age > 0),
                student_email VARCHAR(255) NOT NULL UNIQUE
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS courses(
                course_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                course_code VARCHAR(10) NOT NULL UNIQUE,
                course_credit INTEGER CHECK(course_credit BETWEEN 1 AND 5)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS enrollment(
                enrollment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEYv,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE SET NULL,
                student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS teachers(
                teacher_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                experience_years INTEGER CHECK(experience_years >= 0)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS course_assignments(
                course_assignments_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE SET DEFAULT,
                teacher_id INTEGER REFERENCES teachers(teacher_id) ON DELETE CASCADE
            );
            '''
        ]
        for query in queries:
            self.manager(query, commit=True)

    def insert_data(self):
        students = [
            (18, "Safobek@gmail.com"),
            (22, "Sherdorbek@gmail.com"),
            (20, "Abdulvosit@gmail.com"),
            (19, "Azizbek@gmail.com"),
            (21, "Javohir@gmail.com"),
            (23, "Umar@gmail.com"),
            (18, "Mubina@gmail.com"),
        ]
        for age, email in students:
            self.manager("INSERT INTO students (student_age, student_email) VALUES (%s, %s)", age, email, commit=True)

        courses = [
            ("Matematika", 5),
            ("English", 3),
            ("Biologiya", 4),
        ]
        for code, credit in courses:
            self.manager("INSERT INTO courses (course_code, course_credit) VALUES (%s, %s)", code, credit, commit=True)

        teachers = [
            (5,),
            (10,)
        ]
        for exp in teachers:
            self.manager("INSERT INTO teachers (experience_years) VALUES (%s)", exp, commit=True)

        course_assignments = [
            (1, 1),
            (2, 2)
        ]
        for course_id, teacher_id in course_assignments:
            self.manager("INSERT INTO course_assignments (course_id, teacher_id) VALUES (%s, %s)", course_id, teacher_id, commit=True)

    def modify_tables(self):
        self.manager("ALTER TABLE students RENAME TO learners", commit=True)
        self.manager("ALTER TABLE learners RENAME COLUMN student_age TO age", commit=True)

    def update_data(self):
        self.manager("UPDATE learners SET age = 25 WHERE age = 18", commit=True)

    def delete_data(self):
        self.manager("DELETE FROM learners WHERE age = 25 LIMIT 2", commit=True)


db = DatabaseManager()
db.create_tables()
db.insert_data()
db.modify_tables()
db.update_data()
db.delete_data()
