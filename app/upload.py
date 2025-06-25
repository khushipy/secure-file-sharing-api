
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import get_current_user, get_db
from app import models

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can upload files")
    
    content = file.file.read()
    
    return {"filename": file.filename, "size": len(content)}
