from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime
import pytz

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    data_time = Column(DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Tashkent")))

    sections = relationship("Section", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
