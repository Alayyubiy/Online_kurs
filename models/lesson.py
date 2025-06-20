from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    video_url = Column(String(500))
    homework_file_url = Column(String(500))
    order = Column(Integer)
    section_id = Column(Integer, ForeignKey("sections.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    section = relationship("Section", back_populates="lessons", cascade="all, delete")
    progresses = relationship("Progress", back_populates="lesson", cascade="all, delete")
    quizzes = relationship("Quiz", back_populates="lesson", cascade="all, delete")
    test_histories = relationship("TestHistory", back_populates="lesson")
    teacher = relationship("User", backref="lessons_created")

    def __str__(self):
        return f"{self.title}" if self.title  else "No lesson"

    def __repr__(self):
        return f"{self.title}" if self.title  else "No lesson"