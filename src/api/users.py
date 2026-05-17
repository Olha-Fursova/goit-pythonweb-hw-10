from fastapi import APIRouter, Depends
from src.database.models import User
from src.services.dependencies import get_current_user
from src.core.limiter import limiter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
@limiter.limit("5/minute")
async def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar": current_user.avatar,
        "confirmed": current_user.confirmed,
        "created_at": current_user.created_at
    }