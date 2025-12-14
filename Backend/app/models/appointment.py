from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
