from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    order = Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="sections", cascade="all, delete")
    lessons = relationship("Lesson", back_populates="section", cascade="all, delete")


    def __str__(self):
        return f"{self.title}" if self.title  else "No course"

    def __repr__(self):
        return f"{self.title}" if self.title  else "No course"
