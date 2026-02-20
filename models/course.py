from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime
import pytz


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    category = Column(String(100))
    duration = Column(String(30))
    level = Column(String(30))
    price = Column(Integer)
    teacher = Column(String(100))
    lessons = Column(Integer)
    views = Column(Integer)


    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)


    sections = relationship("Section", back_populates="course")
    payments = relationship("Payment", back_populates="course")
    images = relationship("CourseImage", back_populates="course", cascade="all, delete")


    def __str__(self):
        return f"{self.name}" if self.name  else "No course"

    def __repr__(self):
        return f"{self.name}" if self.name  else "No course"
