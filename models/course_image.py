from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class CourseImage(Base):
    __tablename__ = 'course_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    image = Column(String(255))

    course = relationship("Course", back_populates="images")
