from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth as auth_routes
from app.routes import file
from app.upload import router as upload_router  # your upload file
from app.routes.auth import router as auth_router

app = FastAPI(debug=True)

app.include_router(file.router)
# Create tables
Base.metadata.create_all(bind=engine)

# Include auth routes
app.include_router(auth_routes.router)
app.include_router(upload_router)
@app.get("/ping")
def ping():
    return {"message": "pong"}
