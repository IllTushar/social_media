from sqlalchemy import Column, Integer, String, Date
from engine.engine import Base


class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), nullable=False)
    email = Column(String(225), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    DOB = Column(Date, nullable=False)
