# Overview

This is an application written with Python that stores the grades of the students in a SQL relational database. The primary goal of this project was to create a functional and user-friendly application to manage students, classes, and their associated grades. This application allows users to perform CRUD operations on student and class data, as well as manage student grades efficiently.

The software is designed to provide an easy-to-use interface where users can add, view, update, and delete different things like grades, students, and classes. The integration with the SQL relational database ensures data integrity and supports complex queries to handle tasks like calculating average grades or retrieving specific student records. If you run "students.py" on a folder it will create a "students.db" database in the same folder. All the changes you made will be stored on that "student.db", so is really important that you don't delete it if you want to store some students grades.

You can watch a demo of my software here:
[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

The relational database used in this project is SQLite, which is a lightweight and easy-to-use database system. The database consists of three main tables: student, class, and grades.

## Table Structure:
Student Table:

- id: Integer, Primary Key, Auto-increment
- name: Text, Not Null
- lastname: Text, Not Null
- age: Integer, Not Null

Class Table:

- id: Integer, Primary Key, Auto-increment
- classname: Text, Not Null
- section: Text, Not Null

Grades Table:

- id: Integer, Primary Key, Auto-increment
- student_id: Integer, Foreign Key references student(id)
- class_id: Integer, Foreign Key references class(id)
- grade: Text, Not Null

These tables are related through foreign keys, which allow us to maintain relationships between students, their classes, and their grades.

# Development Environment

To develop this software, I used the following tools:

- Visual Studio Code
- Python 3.11.8 64-bit: The programming language for the application.
- SQLite: For the relational database management system.
- SQLite3 Library: To interact with the SQLite database from Python.
- Git/GitHub

# Useful Websites

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python sqlite3 Library](https://docs.python.org/3.11/library/sqlite3.html)
- [Python 3.11 Ref Manual](https://docs.python.org/3.11/library/functions.html)

# Future Work

For now everything is functional. Maybe in the future I could add other options to make this application more user-friendly.
