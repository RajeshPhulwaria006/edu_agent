from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentCreate, StudentResponse
router = APIRouter(prefix="/students", tags=["Students"])
@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.roll_no == student.roll_no).first():
        raise HTTPException(400, "Roll number already exists")
    obj = Student(**student.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(404, "Student not found")
    return obj
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(404, "Student not found")
    db.delete(obj)
    db.commit()
    return {"message": "Student deleted successfully"}
