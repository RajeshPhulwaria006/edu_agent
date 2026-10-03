from copy import error

from database import SessionLocal, engine, Base
from models import Student, Performance
import pandas as pd
import numpy as np

def seed_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Avoid creating duplicate demo data
        if db.query(Student).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        students = [
            Student(
                name="Aarav Sharma",
                roll_no="BCA001",
                course="BCA",
                semester=5,
                section="A",
                email="aarav@example.com",
                previous_cgpa=8.2,
            ),
            Student(
                name="Priya Verma",
                roll_no="BCA002",
                course="BCA",
                semester=5,
                section="A",
                email="priya@example.com",
                previous_cgpa=7.4,
            ),
            Student(
                name="Rahul Meena",
                roll_no="BCA003",
                course="BCA",
                semester=4,
                section="B",
                email="rahul@example.com",
                previous_cgpa=6.1,
            ),
            Student(
                name="Ananya Singh",
                roll_no="BCA004",
                course="BCA",
                semester=3,
                section="A",
                email="ananya@example.com",
                previous_cgpa=8.8,
            ),
        ]

        db.add_all(students)
        db.commit()

        # Refresh to obtain generated IDs
        for student in students:
            db.refresh(student)

        performances = [
            # Aarav - Good performance
            Performance(
                student_id=students[0].id,
                subject="Python",
                attendance=92,
                internal_marks=86,
                assignment_marks=90,
                practical_marks=88,
                quiz_marks=85,
            ),
            Performance(
                student_id=students[0].id,
                subject="Database Management",
                attendance=89,
                internal_marks=82,
                assignment_marks=87,
                practical_marks=84,
                quiz_marks=80,
            ),

            # Priya - Moderate performance
            Performance(
                student_id=students[1].id,
                subject="Python",
                attendance=78,
                internal_marks=68,
                assignment_marks=72,
                practical_marks=70,
                quiz_marks=65,
            ),
            Performance(
                student_id=students[1].id,
                subject="Computer Networks",
                attendance=74,
                internal_marks=62,
                assignment_marks=65,
                practical_marks=68,
                quiz_marks=60,
            ),

            # Rahul - Higher-risk performance
            Performance(
                student_id=students[2].id,
                subject="Python",
                attendance=62,
                internal_marks=48,
                assignment_marks=45,
                practical_marks=50,
                quiz_marks=42,
            ),
            Performance(
                student_id=students[2].id,
                subject="Database Management",
                attendance=58,
                internal_marks=44,
                assignment_marks=48,
                practical_marks=46,
                quiz_marks=40,
            ),

            # Ananya - Strong performance
            Performance(
                student_id=students[3].id,
                subject="Data Structures",
                attendance=95,
                internal_marks=91,
                assignment_marks=94,
                practical_marks=92,
                quiz_marks=90,
            ),
            Performance(
                student_id=students[3].id,
                subject="Operating Systems",
                attendance=93,
                internal_marks=88,
                assignment_marks=91,
                practical_marks=89,
                quiz_marks=87,
            ),
        ]

        db.add_all(performances)
        db.commit()

        print("Demo database seeded successfully.")
        print(f"Students added: {len(students)}")
        print(f"Performance records added: {len(performances)}")

    except Exception as error:
        db.rollback()
        print(f"Error while seeding database: {error}")

    finally:
        db.close()

def seed_dummy_data():
    """
    Seeds the database with dummy 100 student's data for testing purposes.
    This function can be expanded to add more diverse data as needed.
    """
    data = pd.read_csv('ml/student_data.csv')[:100]  # Limit to first 100 rows for seeding
    db = SessionLocal()

    try:
        for _, row in data.iterrows():
            student = Student(
                name=row['name'],
                roll_no=row['roll_no'],
                course=row['course'],
                semester=row['semester'],
                section=row['section'],
                email=row['email'],
                previous_cgpa=row['previous_cgpa'],
            )
            db.add(student)
            db.commit()
            db.refresh(student)

            performance = Performance(
                student_id=student.id,
                subject=row['subject'],
                attendance=row['attendance'],
                internal_marks=row['internal_marks'],
                assignment_marks=row['assignment_marks'],
                practical_marks=row['practical_marks'],
                quiz_marks=row['quiz_marks'],
            )
            db.add(performance)
            db.commit()

    except Exception as error:
        db.rollback()
        print(f"Error while seeding dummy data: {error}")
    finally:
        db.close()

        print("Dummy data seeded successfully.")
    
if __name__ == "__main__":
    # seed_database()
    seed_dummy_data()
