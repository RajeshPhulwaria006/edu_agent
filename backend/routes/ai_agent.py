from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Performance
from backend.ml.agents_config import Agent

router = APIRouter(prefix="/ai", tags=["AI Agent"])
# Initialize the AI agent
ai_agent = Agent(
    name="Student performance analyser",
    description="You are a professional and experienced consultant in education from last 10+ years. You have a deep understanding of student performance metrics and can provide actionable insights to improve academic outcomes. You are skilled in analyzing student data, identifying areas of improvement, and recommending effective strategies to enhance learning experiences."
)

@router.get("/advisor/{student_id}")
def advisor(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"response": "Student not found."}

    records = db.query(Performance).filter(
        Performance.student_id == student_id
    ).all()

    if not records:
        return {"response": "Not enough performance data."}

    avg = lambda field: sum(getattr(r, field) for r in records) / len(records)
    attendance = avg("attendance")
    internal = avg("internal_marks")
    assignment = avg("assignment_marks")
    practical = avg("practical_marks")
    quiz = avg("quiz_marks")
    weak = []
    subjects = {}

    for r in records:
        subject_avg = (
            r.internal_marks + r.assignment_marks +
            r.practical_marks + r.quiz_marks
        ) / 4
        subjects[r.subject] = subject_avg

        if subject_avg < 50:
            weak.append(r.subject)

    # response = (
    #     f"Academic Analysis for {student.name}\n\n"
    #     f"Attendance: {attendance:.1f}%\n"
    #     f"Internal: {internal:.1f}\n"
    #     f"Assignments: {assignment:.1f}\n"
    #     f"Practical: {practical:.1f}\n"
    #     f"Quiz: {quiz:.1f}\n"
    #     f"Previous CGPA: {student.previous_cgpa}\n\n"
    # )

    # calling agent to analyze the performance on student data.
    analysis = ai_agent.analyze(input={
        'student_name': student.name,
        'attendance': attendance,
        'internal_marks': internal,
        'practical_marks': practical,
        'assignment_marks': assignment,
        'quiz': quiz,
        'previous_cgpa': student.previous_cgpa,
        'weak_subjects': weak,
        'subjects_avg': subjects
    })
    
    return {
        "student_id": student.id, 
        "student_name": student.name,
        "response": analysis
    }
