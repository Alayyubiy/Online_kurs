from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime
import pytz


class TestHistory(Base):
    __tablename__ = "test_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    score = Column(Float)  # 0 dan 100 gacha
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    taken_at = Column(DateTime, default=datetime.now(pytz.timezone("Asia/Tashkent")))

    user = relationship("User", back_populates="test_histories")
    lesson = relationship("Lesson", back_populates="test_histories")


