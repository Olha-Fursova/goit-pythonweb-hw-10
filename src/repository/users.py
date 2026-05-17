from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserModel
from src.services.auth import get_password_hash


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_email(self, email: str):
        stmt = select(User).filter_by(email=email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str):
        stmt = select(User).filter_by(username=username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, body: UserModel):
        user = User(
            username=body.username,
            email=body.email,
            hashed_password=get_password_hash(body.password)
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user