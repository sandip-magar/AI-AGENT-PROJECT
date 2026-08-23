from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import engine, Base
from pgvector.sqlalchemy import Vector

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean)
    created_at = Column(DateTime, default=func.now())

    documents = relationship('PDFDocument', back_populates='users', cascade="all, delete-orphan")
    messages = relationship('ChatMessage', back_populates='users', cascade="all, delete-orphan")

class PDFDocument(Base):
    __tablename__ = "pdf-files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    temp_file = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())

    content = Column(Text, nullable=False)
    embedding = Column(Vector(3072))

    users = relationship('User', back_populates="documents")

class ChatMessage(Base):
    __tablename__ = "chat-history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    users =relationship('User', back_populates="messages")

Base.metadata.create_all(bind=engine)