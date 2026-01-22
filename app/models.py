from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .database import Base

class UserRole(enum.Enum):
    CLIENT = "client"
    PROVIDER = "provider"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    appointments = relationship("Appointment", back_populates="owner")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slot_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="appointments")