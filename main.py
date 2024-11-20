from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mangum import Mangum
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from member.member_model import Member
import os, requests, jwt, json

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
from jwt.algorithms import RSAAlgorithm
import jwt
import json

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        app_client_id = os.environ.get('COGNITO_APP_CLIENT_ID')

        print(f"Debug - User Pool ID: {user_pool_id}")
        print(f"Debug - App Client ID: {app_client_id}")

        region = user_pool_id.split('_')[0]
        keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'

        response = requests.get(keys_url)
        keys = response.json()['keys']
        headers = jwt.get_unverified_header(token)

        # Find the key with matching kid
        key_index = next((index for (index, k) in enumerate(keys) if k["kid"] == headers["kid"]), None)
        if key_index is None:
            raise Exception('Public key not found in jwks.json')

        public_key = keys[key_index]
        public_key_pem = RSAAlgorithm.from_jwk(json.dumps(public_key))

        # Decode and verify the token
        decoded = jwt.decode(
            token,
            key=public_key_pem,
            algorithms=['RS256'],
            options={
                'verify_aud': False,  # Don't verify aud claim
                'verify_exp': True,   # Do verify expiration
                'verify_iss': True    # Do verify issuer
            }
        )

        # Manually verify client_id
        if decoded.get('client_id') != app_client_id:
            raise Exception('Token was not issued for this client_id')

        print(f"Debug - Successfully decoded token: {decoded}")
        return decoded

    except Exception as e:
        print(f"Debug - Verification failed: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
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