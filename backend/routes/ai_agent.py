from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Performance
router = APIRouter(prefix="/ai", tags=["AI Agent"])
@router.get("/advisor/{student_id}")
def advisor(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {"response": "Student not found."}
    records = db.query(Performance).filter(
        Performance.student_id == student_id).all()
    if not records:
        return {"response": "Not enough performance data."}
    avg = lambda field: sum(getattr(r, field) for r in records) / len(records)
    attendance = avg("attendance")
    internal = avg("internal_marks")
    assignment = avg("assignment_marks")
    practical = avg("practical_marks")
    quiz = avg("quiz_marks")
    weak = []
    for r in records:
        subject_avg = (
            r.internal_marks + r.assignment_marks +
            r.practical_marks + r.quiz_marks
        ) / 4
        if subject_avg < 50:
            weak.append(r.subject)
    response = (
        f"Academic Analysis for {student.name}\n\n"
        f"Attendance: {attendance:.1f}%\n"
        f"Internal: {internal:.1f}\n"
        f"Assignments: {assignment:.1f}\n"
        f"Practical: {practical:.1f}\n"
        f"Quiz: {quiz:.1f}\n"
        f"Previous CGPA: {student.previous_cgpa}\n\n"
    )
    if attendance < 75:
        response += "Attendance Alert: Improve attendance.\n\n"
    if internal < 50:
        response += "Academic Alert: Improve internal-test preparation.\n\n"
    if assignment < 50:
        response += "Assignment Alert: Complete pending assignments.\n\n"
    if practical < 50:
        response += "Practical Alert: Increase laboratory practice.\n\n"
    if weak:
        response += "Subjects requiring attention:\n"
        response += "\n".join(f"- {x}" for x in weak) + "\n\n"
    response += (
        "Recommended Action:\n"
        "1. Attend classes regularly.\n"
        "2. Complete assignments on time.\n"
        "3. Practice important questions.\n"
        "4. Attend remedial classes if required.\n"
        "5. Discuss difficulties with faculty."
    )
    return {"student_id": student.id, "student_name": student.name,
            "response": response}
