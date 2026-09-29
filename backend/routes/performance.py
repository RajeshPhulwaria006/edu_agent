from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Performance
from schemas import PerformanceCreate, PerformanceResponse
from ml.predictor import predict_risk

router = APIRouter(prefix="/performance", tags=["Performance"])

@router.post("/", response_model=PerformanceResponse)
def add_performance(data: PerformanceCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == data.student_id).first()

    if not student:
        raise HTTPException(404, "Student not found")

    obj = Performance(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{student_id}")
def get_performance(student_id: int, db: Session = Depends(get_db)):
    return db.query(Performance).filter(
        Performance.student_id == student_id
    ).all()


@router.get("/{student_id}/analysis")
def analyze(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(404, "Student not found")
    
    records = db.query(Performance).filter(
        Performance.student_id == student_id).all()
    
    if not records:
        return {"message": "No performance data available"}
    
    avg = lambda field: sum(getattr(r, field) for r in records) / len(records)
    attendance = avg("attendance")
    internal = avg("internal_marks")
    assignment = avg("assignment_marks")
    practical = avg("practical_marks")
    quiz = avg("quiz_marks")
    
    prediction = predict_risk(
        attendance, internal, assignment,
        practical, quiz, student.previous_cgpa
    )
    overall = (
        attendance*.20 + internal*.25 + assignment*.15 +
        practical*.20 + quiz*.20
    )
    recommendations = []
    
    if attendance < 75:
        recommendations.append("Improve class attendance.")
    if internal < 50:
        recommendations.append("Attend internal-test preparation sessions.")
    if assignment < 50:
        recommendations.append("Complete pending assignments.")
    if practical < 50:
        recommendations.append("Practice laboratory exercises regularly.")
    if quiz < 50:
        recommendations.append("Take more quizzes and revision tests.")
    if not recommendations:
        recommendations.append("Continue the current study strategy.")
    
    return {
        "student_id": student.id,
        "student_name": student.name,
        "attendance": round(attendance,2),
        "internal_marks": round(internal,2),
        "assignment_marks": round(assignment,2),
        "practical_marks": round(practical,2),
        "quiz_marks": round(quiz,2),
        "overall_score": round(overall,2),
        "risk": prediction["risk"],
        "high_risk_probability": prediction["high_risk_probability"],
        "recommendations": recommendations
    }
