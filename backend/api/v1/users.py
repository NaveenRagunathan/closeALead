from fastapi import APIRouter, Depends
from core.security import get_current_user
from models.user import User

router = APIRouter()

@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return user.to_dict()

@router.put("/profile")
async def update_profile(user: User = Depends(get_current_user)):
    # Implement profile update logic
    return {"message": "Profile updated successfully"}
