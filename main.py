# main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from member.member_model import Member
from plan.plan_routes import router as plan_router
from auth.token_verification import verify_token

app = FastAPI(
    title="Member Service API",
    description="API for managing member information",
    version="1.0.0",
    openapi_tags=[{
        "name": "members",
        "description": "Operations with members"
    }]
)

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Include routers
app.include_router(plan_router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["health"])
async def root():
    """
    Health check endpoint to verify API status
    """
    return {
        "message": "Welcome to the Member Service API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/members/{member_id}", tags=["members"])
async def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """
    Get a member by their ID
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# Lambda handler
handler = Mangum(app)