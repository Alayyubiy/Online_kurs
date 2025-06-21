import pytz
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    amount = Column(Float, nullable=False)
    status = Column(String(100), default="pending")  # pending, paid, failed
    paid_at = Column(DateTime, default=datetime.now(pytz.timezone("Asia/Tashkent")))

    user = relationship("User", back_populates="payments")
    course = relationship("Course", back_populates="payments")

    def __str__(self):
        return f"{self.user_id}" if self.user_id else "No user"

    def __repr__(self):
        return f"{self.user_id}" if self.user_id else "No user"
