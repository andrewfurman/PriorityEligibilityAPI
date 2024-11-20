from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mangum import Mangum
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from member.member_model import Member
import jwt
import requests
app = FastAPI(
    title="Member Service API",
    description="API for managing member information",
    version="1.0.0",
    openapi_tags=[{
        "name": "members",
        "description": "Operations with members"
    }]
)

security = HTTPBearer()

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add Cognito token verification
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        user_pool_id = os.environ['COGNITO_USER_POOL_ID']
        region = user_pool_id.split('_')[0]

        # Get JWT public keys from Cognito
        keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
        response = requests.get(keys_url)
        keys = response.json()['keys']

        # Verify token
        headers = jwt.get_unverified_header(token)
        key = [k for k in keys if k['kid'] == headers['kid']][0]

        # Decode and verify the token
        decoded = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=os.environ['COGNITO_APP_CLIENT_ID']
        )
        return decoded
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail='Invalid authentication credentials'
        )

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
    
    Parameters:
    - member_id: Unique identifier of the member
    
    Returns:
    - Member information including personal details and timestamps
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {
        "id": member.id,
        "member_id": member.member_id,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "relationship": member.relationship,
        "created_date": member.created_date,
        "created_by": member.created_by,
        "updated_date": member.updated_date
    }

handler = Mangum(app)