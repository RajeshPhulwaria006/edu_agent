from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, unique=True, nullable=False)
    course = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String, default="")
    email = Column(String, default="")
    previous_cgpa = Column(Float, default=0)
    performances = relationship("Performance", back_populates="student",
                                cascade="all, delete")
class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, nullable=False)
    attendance = Column(Float, default=0)
    internal_marks = Column(Float, default=0)
    assignment_marks = Column(Float, default=0)
    practical_marks = Column(Float, default=0)
    quiz_marks = Column(Float, default=0)
    student = relationship("Student", back_populates="performances")
