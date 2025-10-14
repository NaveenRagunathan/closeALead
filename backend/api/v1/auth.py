from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from core.database import get_db
from core.security import verify_password, get_password_hash, create_access_token, get_current_user
from models.user import User, PlanType
import re

router = APIRouter()

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    # bcrypt accepts up to 72 bytes; we enforce a 72 character cap to be safe
    password: str = Field(..., min_length=8, max_length=72)
    plan: str = "free"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class AuthResponse(BaseModel):
    id: str
    name: str
    email: str
    plan: str
    offerCount: int
    token: str

def validate_password(password: str) -> bool:
    """Password must have at least 8 characters, 1 uppercase, and 1 number"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Validate password
    if not validate_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be 8-72 characters, with at least 1 uppercase and 1 number"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        name=request.name,
        email=request.email,
        password_hash=get_password_hash(request.password),
        plan=PlanType(request.plan) if request.plan in ["free", "professional", "agency"] else PlanType.FREE
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create token
    token = create_access_token({"sub": user.id})
    
    return AuthResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        plan=user.plan.value,
        offerCount=0,
        token=token
    )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token = create_access_token({"sub": user.id})
    
    return AuthResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        plan=user.plan.value,
        offerCount=len(user.offers),
        token=token
    )

@router.get("/me")
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user.to_dict()
