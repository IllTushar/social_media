from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey,Text
from engine.engine import Base
from sqlalchemy.orm import relationship


class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), nullable=False)
    email = Column(String(225), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    DOB = Column(Date, nullable=False)
    post = relationship("Post", back_populates='user_table')


class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    captions = Column(Text, nullable=True)
    images = Column(LargeBinary, nullable=False)
    user_table = relationship("UserTable", back_populates='post')
