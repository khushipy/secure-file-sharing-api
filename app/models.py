from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="client")  # 'client' or 'ops'
    user_type = Column(String)
    files = relationship("File", back_populates="user")



class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")
    

class DownloadToken(Base):
    __tablename__ = "download_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)
