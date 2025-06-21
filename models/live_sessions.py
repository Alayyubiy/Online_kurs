from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base

class LiveSession(Base):
    __tablename__ = "live_sessions"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    host_id = Column(ForeignKey("users.id"))         # Admin yoki Teacher
    course_id = Column(ForeignKey("courses.id"))     # Qaysi kursga tegishli
    start_time = Column(DateTime)
    room_link = Column(String(255))

    user = relationship("User", back_populates="live_sessions")
    course = relationship("Course", back_populates="live_sessions")
