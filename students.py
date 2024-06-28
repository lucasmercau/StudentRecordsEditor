import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('students.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Check if the 'student' table exists, if not, create it
resStudent = cursor.execute("SELECT name FROM sqlite_master WHERE name='student'")
if resStudent.fetchone() is None:
    create_table_sql = '''
    CREATE TABLE student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lastname TEXT NOT NULL,
        age INTEGER NOT NULL
    );
    '''
    cursor.execute(create_table_sql)

# Check if the 'class' table exists, if not, create it
resClass = cursor.execute("SELECT name FROM sqlite_master WHERE name='class'")
if resClass.fetchone() is None:
    create_class_table_sql = '''
    CREATE TABLE class (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classname TEXT NOT NULL,
        section TEXT NOT NULL
    );
    '''
    cursor.execute(create_class_table_sql)

# Check if the 'grades' table exists, if not, create it
resGrades = cursor.execute("SELECT name FROM sqlite_master WHERE name='grades'")
if resGrades.fetchone() is None:
    create_grades_table_sql = '''
    CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES student(id),
        FOREIGN KEY(class_id) REFERENCES class(id)
    );
    '''
    cursor.execute(create_grades_table_sql)

# Commit the changes to the database
conn.commit()

# Function to retrieve all students from the 'student' table
def get_students():
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]} Student: {row[2]}, {row[1]} Age: {row[3]}")

# Function to add a new student to the 'student' table
def add_student():
    name = input("Enter student's first name: ")
    lastname = input("Enter student's last name: ")
    age = input("Enter student's age: ")
    cursor.execute("INSERT INTO student (name, lastname, age) VALUES (?, ?, ?)", (name, lastname, age))
    conn.commit()
    print("Student added successfully!")

# Function to update an existing student in the 'student' table
def update_student():
    get_students()
    student_id = input("Enter the ID of the student to update: ")
    cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        name = input("Enter new first name: ")
        lastname = input("Enter new last name: ")
        age = input("Enter new age: ")
        cursor.execute("UPDATE student SET name = ?, lastname = ?, age = ? WHERE id = ?", (name, lastname, age, student_id))
        conn.commit()
        print("Student updated successfully!")
    else:
        print(f"Student with ID {student_id} does not exist.")

# Function to delete an existing student from the 'student' table
def delete_student():
    get_students()
    student_id = input("Enter the ID of the student to delete: ")
    cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        cursor.execute("DELETE FROM student WHERE id = ?", (student_id,))
        conn.commit()
        print("Student deleted successfully!")
    else:
        print(f"Student with ID {student_id} does not exist.")

# Function to retrieve all classes from the 'class' table
def get_classes():
    cursor.execute("SELECT * FROM class")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]} Class: {row[1]} Section: {row[2]}")

# Function to add a new class to the 'class' table
def add_class():
    classname = input("Enter class name: ")
    section = input("Enter section: ")
    cursor.execute("INSERT INTO class (classname, section) VALUES (?, ?)", (classname, section))
    conn.commit()
    print("Class added successfully!")

# Function to update an existing class in the 'class' table
def update_class():
    get_classes()
    class_id = input("Enter the ID of the class to update: ")
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    class_entry = cursor.fetchone()
    if class_entry:
        classname = input("Enter new class name: ")
        section = input("Enter new section: ")
        cursor.execute("UPDATE class SET classname = ?, section = ? WHERE id = ?", (classname, section, class_id))
        conn.commit()
        print("Class updated successfully!")
    else:
        print(f"Class with ID {class_id} does not exist.")

# Function to delete an existing class from the 'class' table
def delete_class():
    get_classes()
    class_id = input("Enter the ID of the class to delete: ")
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    class_entry = cursor.fetchone()
    if class_entry:
        cursor.execute("DELETE FROM class WHERE id = ?", (class_id,))
        conn.commit()
        print("Class deleted successfully!")
    else:
        print(f"Class with ID {class_id} does not exist.")

# Function to calculate and display the average grade of a student
def get_student_average_grade():
    """Calculate and display the average grade of a student based on their ID."""
    get_students()
    student_id = input("Enter the ID of the student: ")
    cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        cursor.execute("""
            SELECT grade
            FROM grades
            WHERE student_id = ?
        """, (student_id,))
        grades = cursor.fetchall()
        if grades:
            total = sum(float(grade[0]) for grade in grades)
            avg_grade = total / len(grades)
            print(f"Student's average grade: {avg_grade}")
        else:
            print(f"No grades found for student with ID {student_id}.")
    else:
        print(f"Student with ID {student_id} does not exist.")

# Function to retrieve and display all grades of a student
def get_student_grades():
    """Retrieve and display all grades of a student based on their ID."""
    get_students()
    student_id = input("Enter the ID of the student: ")
    cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        cursor.execute("""
            SELECT student.name, student.lastname, class.classname, class.section, grades.grade
            FROM grades
            JOIN student ON grades.student_id = student.id
            JOIN class ON grades.class_id = class.id
            WHERE grades.student_id = ?
        """, (student_id,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"Student: {row[1]}, {row[0]} | Class: {row[2]} Section: {row[3]} | Grade: {row[4]}")
        else:
            print(f"No grades found for student with ID {student_id}.")
    else:
        print(f"Student with ID {student_id} does not exist.")

# Function to add a new grade for a student in a class
def add_student_grade():
    get_students()
    student_id = input("Enter the ID of the student: ")
    cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        get_classes()
        class_id = input("Enter the ID of the class: ")
        cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
        class_entry = cursor.fetchone()
        if class_entry:
            grade = input("Enter grade: ")
            cursor.execute("INSERT INTO grades (student_id, class_id, grade) VALUES (?, ?, ?)", (student_id, class_id, grade))
            conn.commit()
            print("Grade added successfully!")
        else:
            print(f"Class with ID {class_id} does not exist.")
    else:
        print(f"Student with ID {student_id} does not exist.")

# Function to update an existing grade for a student
def update_student_grade():
    get_students()
    student_id = input("Enter the ID of the student: ")
    cursor.execute("""
        SELECT grades.id, student.name, student.lastname, class.classname, class.section, grades.grade
        FROM grades
        JOIN student ON grades.student_id = student.id
        JOIN class ON grades.class_id = class.id
        WHERE grades.student_id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} Student: {row[2]}, {row[1]} | Class: {row[3]} Section: {row[4]} | Grade: {row[5]}")
        grade_id = input("Enter the ID of the grade to update: ")
        cursor.execute("SELECT * FROM grades WHERE id = ? AND student_id = ?", (grade_id, student_id))
        grade = cursor.fetchone()
        if grade:
            new_grade = input("Enter new grade: ")
            cursor.execute("UPDATE grades SET grade = ? WHERE id = ?", (new_grade, grade_id))
            conn.commit()
            print("Grade updated successfully!")
        else:
            print(f"Grade with ID {grade_id} for student ID {student_id} does not exist.")
    else:
        print(f"No grades found for student with ID {student_id}")

# Function to delete an existing grade for a student
def delete_student_grade():
    get_students()
    student_id = input("Enter the ID of the student: ")
    cursor.execute("""
        SELECT grades.id, student.name, student.lastname, class.classname, class.section, grades.grade
        FROM grades
        JOIN student ON grades.student_id = student.id
        JOIN class ON grades.class_id = class.id
        WHERE grades.student_id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} Student: {row[2]}, {row[1]} | Class: {row[3]} Section: {row[4]} | Grade: {row[5]}")
        grade_id = input("Enter the ID of the grade to delete: ")
        cursor.execute("SELECT * FROM grades WHERE id = ? AND student_id = ?", (grade_id, student_id))
        grade = cursor.fetchone()
        if grade:
            cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
            conn.commit()
            print("Grade deleted successfully!")
        else:
            print(f"Grade with ID {grade_id} for student ID {student_id} does not exist.")
    else:
        print(f"No grades found for student with ID {student_id}")

# I created the structure of the program with Python, where the user can choose what to do. 
print("Welcome to Student Records Editor!")
print()
choice = "0"
while choice != "4":
    choice2 = "0"
    print("Please select a category:")
    print("1. Students")
    print("2. Classes")
    print("3. Grades")
    print("4. Quit")
    choice = input("Write a number: ")
    if choice == "1":
        print()
        print("1. Get Students")
        print("2. Add Student")
        print("3. Update Student")
        print("4. Delete Student")
        choice2 = input("Select a number: ")
        if choice2 == "1":
            get_students()
            print()
        elif choice2 == "2":
            add_student()
            print()
        elif choice2 == "3":
            update_student()
            print()
        elif choice2 == "4":
            delete_student()
            print()
    elif choice == "2":
        print()
        print("1. Get All Classes")
        print("2. Add Class")
        print("3. Update Class Name")
        print("4. Delete Class")
        choice2 = input("Select a number: ")
        if choice2 == "1":
            get_classes()
            print()
        elif choice2 == "2":
            add_class()
            print()
        elif choice2 == "3":
            update_class()
            print()
        elif choice2 == "4":
            delete_class()
            print()
    elif choice == "3":
        print()
        print("1. Get Student Average Grade")
        print("2. Get Student Grades")
        print("3. Add Student Grade")
        print("4. Update Student Grade")
        print("5. Delete Student Grade")
        choice2 = input("Select a number: ")
        if choice2 == "1":
            get_student_average_grade()
            print()
        elif choice2 == "2":
            get_student_grades()
            print()
        elif choice2 == "3":
            add_student_grade()
            print()
        elif choice2 == "4":
            update_student_grade()
            print()
        elif choice2 == "5":
            delete_student_grade()
            print()
    elif choice != "4":
        print()
        print("Please choose a number between 1-4.")
        print()

print("Thanks for using this app!")

# Close the connection
conn.close()
