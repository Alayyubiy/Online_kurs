import pytz
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Tashkent")))

    user = relationship("User", back_populates="progresses")
    lesson = relationship("Lesson", back_populates="progresses")
