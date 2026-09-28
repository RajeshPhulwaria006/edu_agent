from pydantic import BaseModel
from typing import Optional
class StudentCreate(BaseModel):
    name: str
    roll_no: str
    course: str
    semester: int
    section: Optional[str] = ""
    email: Optional[str] = ""
    previous_cgpa: float = 0
class StudentResponse(StudentCreate):
    id: int
    class Config:
        from_attributes = True
class PerformanceCreate(BaseModel):
    student_id: int
    subject: str
    attendance: float
    internal_marks: float
    assignment_marks: float
    practical_marks: float
    quiz_marks: float
class PerformanceResponse(PerformanceCreate):
    id: int
    class Config:
        from_attributes = True
