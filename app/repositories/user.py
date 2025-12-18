from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[User]:
        """Get all users."""
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_jshshir(self, jshshir: str) -> Optional[User]:
        """Get user by JSHSHIR (passport number)."""
        result = await self.db.execute(
            select(User).where(User.jshshir == jshshir)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate, password: str) -> User:
        """Create new user with generated password."""
        user = User(
            full_name=user_data.full_name,
            jshshir=user_data.jshshir,
            password=password,
            roles=[role.value for role in user_data.roles],  # Convert enum to string list
            gender=user_data.gender,
            birth_date=user_data.birth_date,
            phone=user_data.phone
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        logger.info(f"Created user: {user.full_name} (jshshir={user.jshshir}, roles={user.roles})")
        return user

    async def update(self, user: User, user_data: UserUpdate) -> User:
        """Update user."""
        update_data = user_data.model_dump(exclude_unset=True)

        # Convert roles enum to string if present
        if "roles" in update_data and update_data["roles"]:
            update_data["roles"] = [role.value for role in update_data["roles"]]

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        logger.info(f"Updated user: {user.full_name} (id={user.id})")
        return user

    async def delete(self, user: User) -> None:
        """Delete user."""
        user_id = user.id
        user_name = user.full_name
        await self.db.delete(user)
        await self.db.commit()
        logger.info(f"Deleted user: {user_name} (id={user_id})")
