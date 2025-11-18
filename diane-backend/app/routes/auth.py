from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import UserLoginRequest, UserSignupRequest, UserResponse
from app.access import user_access
from app.database import get_db_transactional

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=UserResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db_transactional)):
    """Simple email-based login - creates user if doesn't exist"""
    user = user_access.get_or_create_user(session=db, email=request.email)
    return user


@router.post("/signup", response_model=UserResponse)
async def signup(request: UserSignupRequest, db: Session = Depends(get_db_transactional)):
    """Create new user with email and first name"""
    user = user_access.get_or_create_user(
        session=db, email=request.email, first_name=request.first_name
    )
    return user
