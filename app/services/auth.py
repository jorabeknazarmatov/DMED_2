from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.utils.jwt import create_access_token
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """
        Authenticate user with JSHSHIR and password.

        Args:
            login_data: Login credentials (jshshir, password)

        Returns:
            LoginResponse with access token and user data

        Raises:
            HTTPException: If credentials are invalid
        """
        logger.info(f"Login attempt for jshshir: {login_data.jshshir}")

        # Get user by JSHSHIR
        user = await self.user_repo.get_by_jshshir(login_data.jshshir)

        # Check if user exists
        if not user:
            logger.warning(f"Login failed: User not found with jshshir={login_data.jshshir}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JSHSHIR or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check password (plain text comparison)
        if user.password != login_data.password:
            logger.warning(f"Login failed: Invalid password for jshshir={login_data.jshshir}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JSHSHIR or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create JWT token
        token_data = {
            "sub": user.jshshir,
            "user_id": user.id,
            "roles": user.roles,
            "full_name": user.full_name
        }
        access_token = create_access_token(token_data)

        logger.info(f"Login successful for user: {user.full_name} (jshshir={user.jshshir})")

        # Return token and user data
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "full_name": user.full_name,
                "jshshir": user.jshshir,
                "roles": user.roles,
                "phone": user.phone
            }
        )
