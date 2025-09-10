from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    username = Column(String(150), unique=True, index=True)
    password = Column(String(255))
    token = Column(String(255), nullable=True)
    phone = Column(String(20))
    role = Column(String(50))

    payments = relationship("Payment", back_populates="user")

    def __str__(self):
        return f"{self.name}" if self.name else "No name"

    def __repr__(self):
        return f"{self.name}" if self.name else "No name"
