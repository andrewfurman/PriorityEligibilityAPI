# plan/plan_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from member.create_member_database import get_db
from .plan_model import Plan
from auth.token_verification import verify_token

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={404: {"description": "Plan not found"}}
)

@router.get("/{plan_id}")
async def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """
    Get a plan by its ID
    """
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan