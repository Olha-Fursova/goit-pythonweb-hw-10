from fastapi import APIRouter, Depends, HTTPException, status, Path, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import UserModel, UserResponse
from src.services.users import UserService
from src.services.auth import (
    verify_password,
    create_access_token,
)
from src.services.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserModel,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)

    if await service.get_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email or username already exists")
    
    if await service.get_by_username(body.username):
        raise HTTPException(status_code=409, detail="Email or username already exists")

    user = await service.create_user(body)

    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        token=user.verification_token,
    )
 
    return UserResponse.model_validate(user)

@router.post("/login")
async def login(
    body: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)

    user = await service.get_by_username(body.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Wrong password or username"
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=401,
            detail="Email not confirmed"
        )

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Wrong password or username"
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/verify/{token}")
async def verify_email(
    token: str = Path(...),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)

    user = await service.confirm_email(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

    return {"message": "Email verified successfully"}