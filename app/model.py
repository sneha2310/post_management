from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Assuming owner_id is the ID of the user who created the post

    owner = relationship("User") # This creates a relationship to the User model, allowing access to the user who owns the post

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes") 