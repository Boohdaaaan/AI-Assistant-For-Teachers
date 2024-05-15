import os
import pandas as pd
import sqlite3 as sq
from typing import Optional, Dict

from utils import send_plan
from plan_generation import get_model, generate_plan, generate_practical_exercises


def create_students_db(file_path: str, db_path: str, table_name: str):
    """
    Create a SQLite database table from a CSV or Excel file.

    Parameters:
    - file_path (str): Path to the input file (CSV or Excel).
    - db_path (str): Path to the SQLite database file.
    - table_name (str): Name of the table to be created in the database.

    Returns:
    None
    """
    # Check if the input file is an Excel file
    if ".xlsx" in file_path:
        # Read the Excel file into a DataFrame
        df = pd.DataFrame(pd.read_excel(file_path))
    # Check if the input file is a CSV file
    elif ".csv" in file_path:
        # Read the CSV file into a DataFrame
        df = pd.DataFrame(pd.read_csv(file_path))

    # Establish a connection to the SQLite database
    with sq.connect(db_path) as con:
        # Write the DataFrame to the specified table in the SQLite database
        # If the table already exists, append the data to it
        df.to_sql(table_name, con, if_exists='append', index=False)


def get_student_data(db_path: str, student_email: str) -> Optional[Dict[str, str]]:
    """
    Retrieve student data from the database based on the provided email address.

    Args:
        db_path (str): The path to the SQLite database.
        student_email (str): The email address of the student to retrieve data for.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the student data if found, or None if no data is found.
    """
    with sq.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM students WHERE email=?", (student_email,))

        # Fetch the result
        row = cur.fetchall()

        if row:
            # Extract column names from cursor description
            columns = [col[0] for col in cur.description]
            # Construct dictionary with column names as keys and row values as values
            student_data = dict(zip(columns, row[0]))

            return student_data
        else:
            # If no data found, return None
            return None


if __name__ == '__main__':
    # Create a SQLite database table from the provided CSV file
    create_students_db(file_path="./data/students.csv", db_path="database.db", table_name="students")
    
    # Define details of the lesson
    lesson_subject = "Future simple"
    lesson_duration = 60
    student_email = "rachel_white@gmail.com"

    # Get the model
    model = get_model(model="gpt-4")

    # Retrieve student data from the database
    student_data = get_student_data(db_path="database.db", student_email=student_email)

    # Generate a lesson plan
    lesson_plan = generate_plan(model=model, lesson_subject=lesson_subject, lesson_duration=lesson_duration,
                                student_data=student_data)

    # Generate practical exercises
    practical_exercises = generate_practical_exercises(model=model, lesson_subject=lesson_subject, student_data=student_data)

    # Write practical exercises to a text file
    with open("exercises.txt", "w") as file:
        file.write(practical_exercises)

    # Send the lesson plan and exercises to the student
    send_plan(lesson_subject=lesson_subject, lesson_duration=lesson_duration, lesson_plan=lesson_plan,
              student_data=student_data, tutor_data={"Full Name": "Bohdan", "Email": "Bohdan1404@gmail.com"},
              attachment_path="exercises.txt")

    # Delete text file with practical exercises
    os.remove("exercises.txt")

