from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    question = Column(String(255), nullable=False)
    correct_answer = Column(String(255), nullable=False)

    lesson = relationship("Lesson", back_populates="quizzes")



    def __str__(self):
        return f"{self.lesson}" if self.lesson  else "No course"

    def __repr__(self):
        return f"{self.lesson}" if self.lesson  else "No course"
