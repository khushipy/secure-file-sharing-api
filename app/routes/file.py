from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from app.auth import get_current_user
from app.database import SessionLocal
from app.models import User
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from cryptography.fernet import Fernet
load_dotenv()

router = APIRouter()

UPLOAD_DIR = "uploads"
FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY)

os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".pptx", ".docx", ".xlsx"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Only 'ops' users can upload files")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": "File uploaded successfully"}




@router.get("/list-files")
async def list_files(user: User = Depends(get_current_user)):
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can list files")

    files = os.listdir(UPLOAD_DIR)
    return {"files": files}


@router.get("/generate-download-link/{filename}")
def generate_download_link(filename: str, user: User = Depends(get_current_user)):
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can generate download links")

    token = fernet.encrypt(filename.encode()).decode()
    return {
        "download-link": f"http://localhost:8000/download-file/{token}",
        "message": "success"
    }


@router.get("/download-file/{token}")
def download_file(token: str, user: User = Depends(get_current_user)):
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can download files")

    try:
        filename = fernet.decrypt(token.encode()).decode()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired download token")

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")


