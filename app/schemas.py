from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User creation input
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "ops" or "client"

# User login input
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response after login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# File upload response
class FileResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    uploaded_by: int

    class Config:
        orm_mode = True

# File download response
class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str



class LoginUser(BaseModel):
    email: EmailStr
    password: str

class Config:
    from_attributes = True
