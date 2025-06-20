import pytz
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.now(pytz.timezone("Asia/Tashkent")))

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


    def __str__(self):
        return f"{self.user_id}" if self.user_id  else "No user"

    def __repr__(self):
        return f"{self.user_id}" if self.user_id  else "No user"
