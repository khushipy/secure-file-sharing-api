from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.auth import get_db, hash_password, verify_password, create_access_token
from datetime import timedelta
from app.utils import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# User Sign Up
@router.post("/signup")
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate role
    if user_data.role not in ["ops", "client"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'ops' or 'client'.")

    # Create user
    new_user = models.User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    print(f"Simulated Email → http://localhost:8000/auth/verify-email/{new_user.id}")

    return {"message": "User created. Check email for verification link."}


# Email Verification
@router.get("/verify-email/{user_id}")
def verify_email(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Already verified"}

    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


# User Login
@router.post("/login", response_model=schemas.TokenResponse)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Email not verified")

    token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login-ops")
def login_ops(user: schemas.LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if db_user.role != "ops":
        raise HTTPException(status_code=403, detail="Access restricted to Ops users")

    return {"message": "Ops user logged in successfully"}
