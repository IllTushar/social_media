from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey, Text
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
    comments_table = relationship("CommentsTable", back_populates="user_table")


class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    captions = Column(Text, nullable=True)
    images = Column(LargeBinary, nullable=False)
    user_table = relationship("UserTable", back_populates='post')
    comments_table = relationship("CommentsTable", back_populates="post_table")


class CommentsTable(Base):
    __tablename__ = 'Comment_Table'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Posts.id'), nullable=False)
    comments = Column(String(225), nullable=False)
    user_table = relationship("UserTable", back_populates="comments_table")
    post_table = relationship("Post", back_populates="comments_table")
